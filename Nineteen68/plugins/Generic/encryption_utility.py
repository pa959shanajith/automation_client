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
from Crypto import Random
from Crypto.Cipher import AES
import hashlib
import logger
import generic_constants
import Exceptions
import logging
from loggermessages import *
from constants import *
log = logging.getLogger('encryption_utility.py')

##standard padding and unpadding based on PKCS5PADDING standard
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

class AESCipher:

    def __init__( self ):
        self.key = b'\x74\x68\x69\x73\x49\x73\x41\x53\x65\x63\x72\x65\x74\x4b\x65\x79'

    def encrypt( self, raw ):
        try:
            if not (raw is None and raw is ''):
                raw = pad(raw)
                cipher = AES.new( self.key, AES.MODE_ECB)
                return base64.b64encode(cipher.encrypt( raw ) )
            else:
                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
        except Exception as e:
            log.error(e)
            
            logger.print_on_console(e)

    def decrypt( self, enc ):
        try:
            if not (enc is None and enc is ''):
                enc = base64.b64decode(enc)
                cipher = AES.new(self.key, AES.MODE_ECB )
                return unpad(cipher.decrypt( enc))
            else:
                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
        except Exception as e:
            log.error(e)
            
            logger.print_on_console(e)

    def encrypt_md5(self,input):
        try:
            if not (input is None and input is ''):
                encrypted_md5_output = hashlib.md5(input.encode("utf")).hexdigest()
                return encrypted_md5_output
            else:
                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
        except Exception as e:
            log.error(e)
            
            logger.print_on_console(e)

    def encrypt_base64(self,input):
        try:
            if not (input is None and input is ''):
                encrypted_base64_output  = base64.b64encode(input)
                return encrypted_base64_output
            else:
                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
        except Exception as e:
            log.error(e)
            
            logger.print_on_console(e)

    def fieldEncrypt(self,input,*args):
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        if not (input is None and input is ''):
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
        if not (input is None and input is ''):
            try:
                decryptedValue=self.decrypt(input)
                logger.print_on_console('field Decrypt')
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
            except Exception as e:
                Exceptions.error(e)
        return status,result,decryptedValue



##cipher = AESCipher()
##encrypted = cipher.encrypt('bytestringbyrrrbytestringbyrrr12bytestringrrr123')
##decrypted = cipher.decrypt(encrypted)
##print encrypted
##print decrypted
##a = cipher.encrypt_md5('Rakesh')
##print a
##b = cipher.encrypt_base64('Rakesh')
##print b

