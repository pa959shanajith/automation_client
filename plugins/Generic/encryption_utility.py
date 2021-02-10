#-------------------------------------------------------------------------------
# Name:        encryption_utility.py
# Purpose:
#
# Author:      rakesh.v
#
# Created:     14-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import base64
from Crypto.Cipher import AES
import hashlib
import logger
import generic_constants
import logging
import codecs

from constants import *
log = logging.getLogger('encryption_utility.py')

##standard padding and unpadding based on PKCS5PADDING standard
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
unpad = lambda s : s[0:-ord(s[-1])]

class AESCipher:

    def __init__(self):
        self.key = b'\x74\x68\x69\x73\x49\x73\x41\x53\x65\x63\x72\x65\x74\x4b\x65\x79'

    def encrypt(self, raw):
        try:
            if (raw is None or raw is ''):
                err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
            else:
                cipher = AES.new(self.key, AES.MODE_ECB)
                raw = cipher.encrypt(pad(raw.encode('utf-8')))
                return base64.b64encode(raw)
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.info(err_msg)

    def decrypt(self, enc):
        try:
            if (enc is None or enc is ''):
                err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
            else:
                enc = base64.b64decode(enc)
                cipher = AES.new(self.key, AES.MODE_ECB)
                return unpad(cipher.decrypt(enc).decode('utf-8'))
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.info(err_msg)
