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
import sqlite3
from time import time
from threading import Timer
PAGINATE_INDEX = "p@gIn8"

class AbstractStorage(object):

    def __init__(self):
        self._packet_id = 0

    @property
    def get_id(self):
        self._packet_id += 1
        return str(self._packet_id)

    @property
    def has_packet(self):
        return False

    @property
    def next_id(self):
        pass

    def save_packet(self, packetid, subid, packet):
        pass

    def get_packet(self, packetid, subid = None):
        pass

    def delete_packet(self, packetid):
        pass


class InMemory(AbstractStorage):

    def __init__(self):
        super(InMemory, self).__init__()
        self.packets = {}

    @property
    def has_packet(self):
        return (len(self.packets) > 0)

    @property
    def next_id(self):
        return list(self.packets.keys())[0]

    def save_packet(self, packetid, subid, packet):
        if subid is None:
            self.packets[packetid] = packet
        else:
            if packetid not in self.packets: self.packets[packetid] = {subid: packet}
            else: self.packets[packetid][subid] = packet

    def get_packet(self, packetid, subid = None):
        pckt = self.packets[packetid]
        if subid == "PAGIN":
            pckt = pckt[PAGINATE_INDEX]
        elif type(pckt) == dict:
            try:
                if subid == "" or subid is None: subid = PAGINATE_INDEX
                elif subid == PAGINATE_INDEX: subid = 1
                else: subid = int(subid) + 1
                if type(subid) == int and (subid + 1) == len(pckt): subid = "eof"
                pckt = pckt[str(subid)]
            except:
                pass
        return pckt

    def delete_packet(self, packetid):
        if packetid in self.packets:
            del self.packets[packetid]


class SQLite(AbstractStorage):

    def __init__(self):
        super(SQLite, self).__init__()
        db_path = os.environ["NINETEEN68_HOME"]+os.sep+'assets'+os.sep+'packets.db'
        #os.remove(db_path)  #####
        connection = sqlite3.connect(db_path, check_same_thread=False)
        connection.isolation_level = None
        self.db = connection.cursor()
        Timer(5, compact_db, (self.db,)).start()
        self.db.execute("CREATE TABLE IF NOT EXISTS packets (packetid integer, subpacketid text, packet text)")
        last_pcktid = self.db.execute("SELECT packetid from packets").fetchall()[-1:]
        if len(last_pcktid) != 0: self._packet_id = last_pcktid[0][0] + 1

    def __del__(self):
        if bool(self.db):
            compact_db(self.db)
            self.db.connection.close()

    @property
    def has_packet(self):
        return (self.db.execute("SELECT count(packetid) FROM packets").fetchone()[0] > 0)

    @property
    def next_id(self):
        return self.db.execute("SELECT packetid from packets").fetchone()[0]

    def save_packet(self, packetid, subid, packet):
        self.db.execute("INSERT INTO packets VALUES (?,?,?)", (packetid, subid, json.dumps(packet)))

    def get_packet(self, packetid, subid = None):
        subpack_count = len(self.db.execute("SELECT subpacketid FROM packets WHERE packetid=?",(packetid,)).fetchall())
        if subpack_count > 1:
            if subid == "PAGIN" or subid == "" or subid is None: subid = PAGINATE_INDEX
            elif subid == PAGINATE_INDEX: subid = 1
            else: subid = int(subid) + 1
            if type(subid) == int and (subid + 1) == subpack_count: subid = "eof"
        else: subid = None
        data = self.db.execute("SELECT packet FROM packets WHERE packetid=? and subpacketid IS ?",(packetid,subid)).fetchone()
        if data and len(data) > 0: return json.loads(data[0])
        return None

    def delete_packet(self, packetid):
        if packetid.isnumeric(): packetid = int(packetid)
        self.db.execute("DELETE FROM packets WHERE packetid=?",(packetid,))

def compact_db(db):
    db.execute("VACUUM")