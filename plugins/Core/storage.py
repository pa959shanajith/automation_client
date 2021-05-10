#-------------------------------------------------------------------------------
# Name:        storage
# Purpose:
#
# Author:      ranjan.agrawal
#
# Created:     20/01/2020
# Copyright:   (c) ranjan.agrawal 2020
#-------------------------------------------------------------------------------

import os
import json
import queue
import logging
import sqlite3
import itertools
from collections import OrderedDict
from threading import Timer, Lock

log = logging.getLogger("storage")

__all__ = ['InMemory', 'SQLite']

class AbstractStorage(object):
    """Abstract class for storing socket.io packets before sending. """

    def __init__(self):
        self._packet_id = 0
        self.type = ''
        self.page_index = os.getenv('ICE_PACKET_PAGINATE_INDEX')
        self._counter = self._get_counter()
        self.q = queue.Queue()
        self.q.Empty = queue.Empty
        self.lock = Lock()
        self._repopulate()

    def _get_counter(self, start=1):
        return itertools.count(start)

    def _repopulate(self):
        """Repopulates the queue with the packets available in storage """
        pass

    @property
    def id(self):
        """Returns a unique (incremental) id for storing packets """
        self._packet_id = next(self._counter)
        return str(self._packet_id)

    @property
    def lastid(self):
        """Returns the last generated packet id """
        return str(self._packet_id)

    @property
    def has_packet(self):
        """Returns True if packets are pending in the queue else returns False
        """
        return (self.q.qsize() > 0)

    def process_done(self):
        """Marks a queue task as done """
        try: self.q.task_done()
        except ValueError: pass

    def load(self):
        """Returns the next packet in the queue

        If there are no packets available in the queue then None is returned
        """
        packetid = chunkid = data = None
        with self.lock:
            log.debug("Fetching packet from queue")
            try:
                packetid, chunkid = self.q.get(block=False)
                data = self.load_packet(packetid, chunkid)
            except self.q.Empty:
                log.debug("No packets to load from queue")
                pass
        return packetid, chunkid, data

    def load_packet(self, packetid, chunkid=None):
        """Returns the packet data associated with the given packetid
        and chunkid if packet is paginated.

        If there is no such packet available then None is returned
        """
        log.debug("Fetching packetid %s and chunkid %s from storage",
            packetid, chunkid)
        data = self._load(packetid, chunkid)
        return data

    def save(self, packetid, chunkid, packet):
        """Stores the provided packet in the queue and storage """
        with self.lock:
            log.debug("Saving packetid %s and chunkid %s to queue and storage",
                packetid, chunkid)
            self.q.put((packetid, chunkid), block=False)
            self._save(packetid, chunkid, packet)

    def delete(self, packetid):
        """Removes the packet associated with provided id from the storage """
        with self.lock:
            log.debug("Deleting packetid %s from storage", packetid)
            self._delete(packetid)

    def clear(self):
        """Empties the queue and storage """
        with self.lock:
            log.debug("Clearing the queue")
            while self.q.qsize() > 0:
                try: self.q.get(block=False)
                except self.q.Empty: pass
            log.debug("Clearing the storage")
            self._clear()

    def re_add_ids(self, items):
        """Needs to be implemented by inheriting class """
        items_l = len(items)
        if items_l == 0: return
        with self.lock:
            with self.q.mutex:
                self.q.unfinished_tasks += items_l
                if items_l > 1: self.q.queue.extendleft(items)
                else: self.q.queue.appendleft(items[0])

    def _save(self, *args):
        """Needs to be implemented by inheriting class """
        raise NotImplementedError("_save method has to be explicitly "
            "implemented by inheriting class")

    def _load(self, *args):
        """Needs to be implemented by inheriting class """
        raise NotImplementedError("_load method has to be explicitly "
            "implemented by inheriting class")

    def _delete(self, *args):
        """Needs to be implemented by inheriting class """
        raise NotImplementedError("_delete method has to be explicitly "
            "implemented by inheriting class")

    def _clear(self):
        """Needs to be implemented by inheriting class """
        raise NotImplementedError("_clear method has to be explicitly "
            "implemented by inheriting class")

class InMemory(AbstractStorage):
    """Storing socket.io packets before sending.
    This is done if packet is lost while sending or there is too much data
    to send and need a place to hold all the outgoing packaets

    Packets are stored in a python's OrderedDict object in runtime memory.

    If program closes, then packet data is lost
    """

    def __init__(self):
        super(InMemory, self).__init__()
        self.type = 'memory'
        self.packets = {}

    def _save(self, packetid, chunkid, packet):
        """Stores the provided packet in the dict object """
        if chunkid is None:
            self.packets[packetid] = packet
        else:
            if packetid not in self.packets:
                self.packets[packetid] = {chunkid: packet}
            else: self.packets[packetid][chunkid] = packet

    def _load(self, packetid, chunkid = None):
        """Returns the packet data associated with the given packetid
        and chunkid if packet is paginated.

        If there is no packet available with given id then None is returned
        """
        pckt = None
        if packetid in self.packets:
            pckt = self.packets[packetid]
        if type(pckt) == dict:
            if chunkid in pckt: pckt = pckt[chunkid]
            else: pckt = None
        return pckt

    def _delete(self, packetid):
        """Removes the packet from the dict for provided id """
        if packetid.isnumeric(): packetid = int(packetid)
        if packetid in self.packets:
            del self.packets[packetid]

    def _clear(self):
        """Remove all packets from the dict """
        for key in self.packets:
            del self.packets[key]


class SQLite(AbstractStorage):
    """Storing socket.io packets before sending.
    This is done if packet is lost while sending or there is too much data
    to send and need a place to hold all the outgoing packaets

    Packets are stored in a sqlite database.

    If program closes, then packet data is retained and can be reloaded
    after program starts again.
    """

    def __init__(self):
        super(SQLite, self).__init__()
        self.type = 'db'
        self.db = None
        db_path = os.path.join(os.getenv("AVO_ASSURE_HOME"), 'assets',
            'packets.db')
        rm_db = os.getenv("ICE_CLEAR_STORAGE", "") and os.path.isfile(db_path)
        if rm_db: os.remove(db_path)
        self.mutex = Lock()
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.db = self.conn.cursor()
        self.write("CREATE TABLE IF NOT EXISTS packets (packetid integer, "
            "chunkid text, packet text)")
        if not rm_db: Timer(5, self._compact_db).start()

    def __del__(self):
        if bool(self.db):
            # self._compact_db()
            self.conn.close()

    def write(self, query, *args):
        """Performs the write operation on (Sqlite)db """
        with self.mutex:
            self.db.execute(query, args)
            self.conn.commit()

    def read(self, query, *args, return_cursor=False):
        """Performs the read operation on (Sqlite)db """
        resp = None
        with self.mutex:
            cursor = self.db.execute(query, args)
            if return_cursor: resp = cursor
            else:
                data = cursor.fetchone()
                if data and len(data) > 0: resp = data[0]
        return resp


    def _repopulate(self):
        """Repopulates the queue with the packets available in storage """
        try:
            last_pcktid = self.read("SELECT packetid from packets",
                return_cursor=True).fetchall()[-1:]
            if len(last_pcktid) != 0: self._packet_id = last_pcktid[0][0] + 1
        except Exception as e:
            log.info("Error while restoring packet queue from storage. "
                "Error: %s", e)

    def _save(self, packetid, chunkid, packet):
        """Stores the provided packet in the db """
        try:
            self.write("INSERT INTO packets VALUES (?,?,?)", packetid,
                chunkid, json.dumps(packet))
        except Exception as e:
            log.info("Error while saving packet into storage. Error: %s", e)

    def _load(self, packetid, chunkid = None):
        """Returns the packet data associated with the given packetid
        and chunkid if packet is paginated.

        If there is no packet available with given id then None is returned
        """
        if not packetid: return None
        try:
            data = self.read("SELECT packet FROM packets WHERE packetid=? and"
                " chunkid IS ?", packetid, chunkid)
            if data: return json.loads(data)
        except Exception as e:
            log.info("Error while fetching packet from storage. Error: %s", e)
        return None

    def _delete(self, packetid):
        """Removes the packet from the db for provided id """
        if packetid.isnumeric(): packetid = int(packetid)
        try:
            self.write("DELETE FROM packets WHERE packetid=?", packetid)
        except Exception as e:
            log.info("Error while deleting packet from storage. Error: %s", e)

    def _clear(self):
        """Remove all packets from the db """
        try:
            self.write("DELETE FROM packets")
            # self.read("SELECT name FROM sqlite_master where name = packets")
        except Exception as e:
            log.info("Error while deleting packets from storage. Error: %s", e)
        self._compact_db()

    def _compact_db(self):
        """Remove the the dead entries in db and thus reduces the size.

        When packets are deleted, they are marked as deleted but not actually
        removed permanently. With this method, we clear all the temporary data.
        """
        try:
            self.write("VACUUM")
        except Exception as e:
            log.info("Error while compacting storage. Error: %s", e)
