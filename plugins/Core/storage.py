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
from threading import Timer, Lock
PAGINATE_INDEX = "p@gIn8"
sqlite_lock = Lock()

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

    def clear(self):
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
        if packetid.isnumeric(): packetid = int(packetid)
        if packetid in self.packets:
            del self.packets[packetid]

    def clear(self):
        for key in self.packets:
            del self.packets[key]


class SQLite(AbstractStorage):

    def __init__(self):
        self.db = None
        super(SQLite, self).__init__()
        db_path = os.environ["NINETEEN68_HOME"]+os.sep+'assets'+os.sep+'packets.db'
        #if os.path.isfile(db_path): os.rename(db_path, db_path[:-2]+str(int(time()*100000))+".db")
        if os.path.isfile(db_path): os.remove(db_path)  #####
        connection = sqlite3.connect(db_path, check_same_thread=False)
        connection.isolation_level = None
        self.db = connection.cursor()
        Timer(5, self.compact_db).start()
        self.db.execute("CREATE TABLE IF NOT EXISTS packets (packetid integer, subpacketid text, packet text)")
        last_pcktid = self.db.execute("SELECT packetid from packets").fetchall()[-1:]
        if len(last_pcktid) != 0: self._packet_id = last_pcktid[0][0] + 1

    def __del__(self):
        try:
            sqlite_lock.acquire(True)
            if bool(self.db):
                self.compact_db()
                self.db.connection.close()
        finally: sqlite_lock.release()

    @property
    def has_packet(self):
        try:
            sqlite_lock.acquire(True)
            hasp = (self.db.execute("SELECT count(packetid) FROM packets").fetchone()[0] > 0)
        finally: sqlite_lock.release()
        return hasp

    @property
    def next_id(self):
        try:
            sqlite_lock.acquire(True)
            nid = self.db.execute("SELECT packetid from packets").fetchone()[0]
        finally: sqlite_lock.release()
        return nid

    def save_packet(self, packetid, subid, packet):
        try:
            sqlite_lock.acquire(True)
            self.db.execute("INSERT INTO packets VALUES (?,?,?)", (packetid, subid, json.dumps(packet)))
        finally: sqlite_lock.release()

    def get_packet(self, packetid, subid = None):
        try:
            sqlite_lock.acquire(True)
            subpack_count = len(self.db.execute("SELECT subpacketid FROM packets WHERE packetid=?",(packetid,)).fetchall())
            if subpack_count > 1:
                if subid == "PAGIN" or subid == "" or subid is None: subid = PAGINATE_INDEX
                elif subid == PAGINATE_INDEX: subid = 1
                else: subid = int(subid) + 1
                if type(subid) == int and (subid + 1) == subpack_count: subid = "eof"
            else: subid = None
            data = self.db.execute("SELECT packet FROM packets WHERE packetid=? and subpacketid IS ?",(packetid,subid)).fetchone()
        finally: sqlite_lock.release()
        if data and len(data) > 0: return json.loads(data[0])
        return None

    def delete_packet(self, packetid):
        if packetid.isnumeric(): packetid = int(packetid)
        try:
            sqlite_lock.acquire(True)
            self.db.execute("DELETE FROM packets WHERE packetid=?",(packetid,))
        finally: sqlite_lock.release()

    def clear(self):
        try:
            sqlite_lock.acquire(True)
            self.db.execute("DELETE FROM packets")
            self.db.execute("SELECT name FROM sqlite_master where name = packets")
            self.compact_db()
        finally: sqlite_lock.release()

    def compact_db(self):
        try:
            sqlite_lock.acquire(True)
            self.db.execute("VACUUM")
        finally: sqlite_lock.release()
