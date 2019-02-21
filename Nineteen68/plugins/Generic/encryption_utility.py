#-------------------------------------------------------------------------------
# Name:        module2
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
                cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
                raw = cipher.encrypt(pad(raw.encode('utf-8')))
                return codecs.encode(raw, 'hex')
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.info(err_msg)

    def decrypt(self, enc):
        try:
            if (raw is None or raw is ''):
                err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
            else:
                enc = codecs.decode(enc, 'hex')
                cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
                return unpad(cipher.decrypt(data).decode('utf-8'))
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.info(err_msg)

    def encrypt_md5(self,input):
        try:
            if not (input is None or input is ''):
                encrypted_md5_output = hashlib.md5(input.encode("utf")).hexdigest()
                return encrypted_md5_output
            else:
                err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.info(err_msg)

    def encrypt_base64(self,input):
        try:
            if not (input is None or input is ''):
                encrypted_base64_output  = base64.b64encode(input)
                return encrypted_base64_output
            else:
                err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.info(err_msg)

    def fieldEncrypt(self,input,*args):
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        if not (input is None or input is ''):
            try:
                encryptedValue=self.encrypt(input)
                logger.print_on_console('field encrypt')
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
            except Exception as e:
                Exceptions.error(e)
        return status,result,encryptedValue

    def fieldDecrypt(self,input,*args):
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        if not (input is None or input is ''):
            try:
                decryptedValue=self.decrypt(input)
                logger.print_on_console('field Decrypt')
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
            except Exception as e:
                Exceptions.error(e)
        return status,result,decryptedValue
