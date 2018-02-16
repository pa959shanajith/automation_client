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
from Crypto.Cipher import AES
BS=16
iv='0'*16
##key='Nineeteen68@ScrapeNineeteen68@Sc'
scrape_key='Nineeteen68@SecureScrapeDataPath'

class CoreUtils():

    #definition to fetch the data size in bytes/kilobytes/megabytes
    # sends data length in bytes if memoryformat not provided
    def getdatasize(self,inputdata,memoryformat):
        try:
            datalength = sys.getsizeof(inputdata)
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
                        if not isinstance(eachvalue,unicode):
                            if not all(ord(c) < 128 for c in eachvalue):
                                value.append(eachvalue.decode('utf-8'))
                else:
                    if not isinstance(value,unicode):
                        if not all(ord(c) < 128 for c in value):
                            value = value.decode('utf-8')
            return value
        except Exception as e:
            log.info(e)

    def pad(self,data):
        data=data.encode('utf-8')
        padding = BS - len(data) % BS
        return data + padding * chr(padding)

    def unpad(self,data):
        data=data.decode('utf-8')
        return data[0:-ord(data[-1])]

    def unwrap(self,hex_data,key):
        data = ''.join(map(chr, bytearray.fromhex(hex_data)))
        aes = AES.new(key, AES.MODE_CBC, iv)
        return self.unpad(aes.decrypt(data))

    def wrap(self,data,key):
        aes = AES.new(key, AES.MODE_CBC, iv)
        return aes.encrypt(self.pad(data)).encode('hex')

    def scrape_unwrap(self,hex_data):
        data = ''.join(map(chr, bytearray.fromhex(hex_data)))
        aes = AES.new(scrape_key, AES.MODE_CBC, iv)
        return self.unpad(aes.decrypt(data))

    def scrape_wrap(self,data):
        aes = AES.new(scrape_key, AES.MODE_CBC, iv)
        return aes.encrypt(self.pad(data)).encode('hex')

    def getMacAddress(self):
        mac=""
        if sys.platform == 'win32':
            for line in os.popen("ipconfig /all"):
                if line.lstrip().startswith('Physical Address'):
    ##                mac = line.split(':')[1].strip().replace('-',':')
                    mac = line.split(':')[1].strip()
                    break
        else:
            for line in os.popen("/sbin/ifconfig"):
                if line.find('Ether') > -1:
                    mac = line.split()[4]
                    break
        return str(mac).strip()
