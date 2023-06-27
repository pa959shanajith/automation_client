#-------------------------------------------------------------------------------
# Name:       text_keywords_sap
# Purpose:    Module for textbox keywords
#
#Author:      anas.ahmed1,kavyashree,sakshi.goyal,saloni.goyal
#
# Created:     07-04-2017
# Copyright:   (c) anas.ahmed1 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sap_constants
from constants import *
import logger
from encryption_utility import AESCipher
from saputil_operations import SapUtilKeywords
from sap_launch_keywords import Launch_Keywords
import logging
log = logging.getLogger('text_keywords_sap.py')

class Text_Keywords():

    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()

    def getText(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( ses.FindById(id).type == 'GuiCTextField' or 'GuiTextField' ):
                    value = ses.FindById(id).text
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Get Text' )
        return status, result, value, err_msg

    def setText(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)

            if ( id and ses ):
                if ( ses.FindById(id).Changeable == True ):
                    if ( ses.FindById(id).type == 'GuiCTextField' or 'GuiTextField'  or 'GuiPasswordField' ):
                        try:
                            if(len(input_val) > 1):
                                text = input_val[3]
                            else:
                                text = input_val[0]
                            ses.FindById(id).text = text
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                        except Exception as e:
                            err_msg = sap_constants.INVALID_INPUT
                            log.error(e)
                    else:
                        err_msg = sap_constants.INVALID_ELELMENT_TYPE
                else:
                    err_msg = sap_constants.ELEMENT_NOT_CHANGEABLE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Verify Set Text' )
        return status, result, value, err_msg

    def setSecureText(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( ses.FindById(id).Changeable == True ):
                    if ( len(input_val) > 1 ):
                        text = input_val[3]
                    else:
                        text = input_val[0]
                    encryption_obj = AESCipher()
                    text_decrypted = encryption_obj.decrypt(text)
                    ses.FindById(id).text = text_decrypted
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.ELEMENT_NOT_CHANGEABLE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Set Secure Text' )
        return status, result, value, err_msg

    def clearText(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( ses.FindById(id).Changeable == True ):
                    if ( ses.FindById(id).type == 'GuiCTextField' or 'GuiTextField' or 'GuiPasswordField' ):
                        ses.FindById(id).text = ""
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = sap_constants.INVALID_ELELMENT_TYPE
                else:
                    err_msg = sap_constants.ELEMENT_NOT_CHANGEABLE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info(err_msg)
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Clear Text' )
        return status, result, value, err_msg

    def verifyText(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                text = input_val[0].strip()
                if ( ses.FindById(id).text.strip() == text ):
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Element text does not match input text'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Verify Text' )
        return status, result, value, err_msg

    def getTextboxLength(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( ses.FindById(id).type == "GuiTextField" or "GuiCTextField" ):
                    value = ses.FindById(id).MaxLength
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Get Textbox Length' )
        return status, result, value, err_msg


    def verifyTextboxLength(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                length = int(input_val[0])
                if ( ses.FindById(id).MaxLength == length ):
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Given Length Does not match'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Verify Textbox Length' )
        return status, result, value, err_msg