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

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

class AESCipher:

    def __init__( self ):
        self.key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

    def encrypt( self, raw ):
        try:
            if not (raw is None and raw is ''):
                raw = pad(raw)
                iv = Random.new().read( AES.block_size )
                cipher = AES.new( self.key, AES.MODE_ECB, iv )
                return base64.b64encode( iv + cipher.encrypt( raw ) )
            else:
                logger.log(generic_constants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)

    def decrypt( self, enc ):
        try:
            if not (enc is None and enc is ''):
                enc = base64.b64decode(enc)
                iv = enc[:16]
                cipher = AES.new(self.key, AES.MODE_ECB, iv )
                return unpad(cipher.decrypt( enc[16:] ))
            else:
                logger.log(generic_constants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)

    def encrypt_md5(self,input):
        try:
            if not (input is None and input is ''):
                encrypted_md5_output = hashlib.md5(input.encode("utf")).hexdigest()
                return encrypted_md5_output
            else:
                logger.log(generic_constants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)

    def encrypt_base64(self,input):
        try:
            if not (input is None and input is ''):
                encrypted_base64_output  = base64.b64encode(input)
                return encrypted_base64_output
            else:
                logger.log(generic_constants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)

    def fieldEncrypt(self,input,*args):
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        if not (input is None and input is ''):
            try:
                encryptedValue=self.encrypt(input)
                logger.log('field encrypt')
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
                logger.log('field Decrypt')
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
            except Exception as e:
                Exceptions.error(e)
        return status,result,decryptedValue



##cipher = AESCipher()
##encrypted = cipher.encrypt('version2.0_Test')
##decrypted = cipher.decrypt(encrypted)
##print encrypted
##print decrypted
##a = cipher.encrypt_md5('Rakesh')
##print a
##b = cipher.encrypt_base64('Rakesh')
##print b
