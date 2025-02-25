#-------------------------------------------------------------------------------
# Name:        core_utils.py
# Purpose:		providing utility functions for the Core folder
#
# Author:      vishvas.a
#
# Created:     07-07-2017
# Copyright:   (c) vishvas.a 2017
# Licence:     <your licence>
#
#-------------------------------------------------------------------------------

import sys
import logging
log = logging.getLogger("core_utils.py")
import os
import json
import socket
import random
import codecs
from constants import *
from Crypto.Cipher import AES
path_added = []


class CoreUtils():

    def __init__(self):
        get_all_the_imports('Generic')

    #definition to fetch the data size in bytes/kilobytes/megabytes
    # sends data length in bytes if memoryformat not provided
    def getdatasize(self,inputdata,memoryformat):
        try:
            try:
                datalength = len(json.dumps(inputdata))
            except:
                try:
                    datalength = len(json.dumps(dict(inputdata)))
                except:
                    datalength = len(str(inputdata))
            log.info('Data size in bytes:')
            log.info(datalength)
            kilobytes = datalength/1024
            if memoryformat == 'kb':
                datalength = kilobytes
                log.info('Data size is: %s',str(datalength))
            elif memoryformat == 'mb':
                datalength = kilobytes/1024
                log.info('Data size is: %s',str(datalength))
            else:
                log.info('Data size is: %s',str(datalength))
            return datalength
        except Exception as e:
            log.info(e)

    #definition to convert to UTF-8 format when input is not within ascii 128
    def get_UTF_8(self,value):
        try:
            if isinstance(value,str) or isinstance(value, list):
                if isinstance(value, list):
                    for eachvalue in value:
                        if not isinstance(eachvalue,str):
                            if not all(ord(c) < 128 for c in eachvalue):
                                value.append(eachvalue.decode('utf-8'))
                else:
                    if not isinstance(value,str):
                        if not all(ord(c) < 128 for c in value):
                            value = value.decode('utf-8')
            return value
        except Exception as e:
            log.info(e)

    def pad(self, data):
        BS = 16
        padding = BS - len(data) % BS
        return data + padding * chr(padding).encode('utf-8')

    def unpad(self, data):
        return data[0:-ord(data[-1])]

    def unwrap(self, hex_data, key, iv=b'0'*16):
        dec_data=None
        try:
            data = codecs.decode(hex_data, 'hex')
            aes = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
            dec_data = self.unpad(aes.decrypt(data).decode('utf-8'))
        except Exception as e:
            log.error("Invalid input for Decryption")
        return dec_data

    def wrap(self, data, key, iv=b'0'*16):
        aes = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        hex_data = aes.encrypt(self.pad(data.encode('utf-8')))
        return codecs.encode(hex_data, 'hex')

    def scrape_unwrap(self, hex_data):
        key = "".join(['N','i','n','e','e','t','e','e','n','6','8','@','S','e',
            'c','u','r','e','S','c','r','a','p','e','D','a','t','a','P','a','t','h'])
        #to convert string to bytes
        hex_data=hex_data.encode('utf-8')
        return self.unwrap(hex_data, key)

    def scrape_wrap(self, data):
        key = "".join(['N','i','n','e','e','t','e','e','n','6','8','@','S','e',
            'c','u','r','e','S','c','r','a','p','e','D','a','t','a','P','a','t','h'])
        enc_text=self.wrap(data, key)
        #to convert bytes to string since concatenation should happen with rest of teh object identifiers which is not encrypted
        return enc_text.decode('utf-8')

    def getMacAddress(self):
        mac=""
        if sys.platform == 'win32':
            ##for line in os.popen("ipconfig /all"):
            ##    if line.lstrip().startswith('Physical Address'):
            ##        ##mac = line.split(':')[1].strip().replace('-',':')
            ##        mac = line.split(':')[1].strip()
            ##        break
            ipdata=os.popen("ipconfig /all").read()
            eth_st=ipdata.find("Ether")
            phy_st=ipdata[eth_st:].find("Physical Address")+eth_st
            phy_en=ipdata[phy_st:].find("\n")+phy_st
            mac=ipdata[phy_st:phy_en].split(':')[1].lower().strip()
        else:
            for line in os.popen("/sbin/ifconfig"):
                if line.strip().lower().find('ether') > -1:
                    if(sys.platform == 'darwin'):
                        mac = line.strip().lower()[6:]
                    else:
                        mac = line.split()[4]
                    break
        mac = str(mac).replace('-',':')
        return str(mac).strip()

def check_isadmin():
    is_admin = 0
    if SYSTEM_OS == 'Windows':
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() == 1
    return is_admin

def get_all_the_imports(plugin_path):
    if plugin_path in path_added: return True
    path_added.append(plugin_path)
    path = os.environ["AVO_ASSURE_HOME"] + os.sep + 'plugins' + os.sep + plugin_path
    sys.path.append(path)
    for _, dirs, _ in os.walk(path):
        for d in dirs:
            p = path + os.sep + d
            sys.path.append(p)

def find_open_port():
    while True:
        port = 30000 + int(random.random()*10000) + int(random.random()*10000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            res = sock.connect_ex(('localhost', port))
            if res == 10061:
                log.debug("Remote debugging port seleted is %s", port)
                return str(port)
