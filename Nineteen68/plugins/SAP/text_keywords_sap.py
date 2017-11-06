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
import win32com.client
from constants import *
from sap_scraping import Scrape
import logger
import time
from encryption_utility import AESCipher
from saputil_operations import SapUtilKeywords
from sap_launch_keywords import Launch_Keywords
class Text_Keywords():

    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk =Launch_Keywords()

    def getText(self, sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=''
        try:
            if(id != None):
##                if(ses.FindById(id).Changeable == True):
                    if(ses.FindById(id).type == 'GuiCTextField' or 'GuiTextField'):
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                        value=ses.FindById(id).text

                    else:
                        logger.print_on_console('Element state does not allow to perform the operation')
                        err_msg = sap_constants.ERROR_MSG
##                else:
##                    logger.print_on_console( "Element is not changeable")
##                    err_msg = "Element is not changeable"
##                    log.info(err_msg)
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
                  err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            Exceptions.error(e)
            logger.print_on_console('Error occured in getText and is a :',e)
        return status,result,value,err_msg

    def setText(self, sap_id,input_val, *args):
        ses=''
        id=''
        self.lk.setWindowToForeground(sap_id)
        if(len(input_val)>1):
            text = input_val[2]
        else:
            text=input_val[0]
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    if(ses.FindById(id).type == 'GuiCTextField' or 'GuiTextField'  or 'GuiPasswordField'):
                        try:
                         ses.FindById(id).text = text
                         status = sap_constants.TEST_RESULT_PASS
                         result = sap_constants.TEST_RESULT_TRUE
                        except Exception as e:
                            logger.print_on_console("Entered value is incorrect")
                            err_msg = "Entered value is incorrect"
                else:
                    logger.print_on_console( "Element is not changeable")
                    err_msg = "Element is not changeable"
                    log.info(err_msg)
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
                  err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            import traceback
            traceback.print_exc()
        return status,result,value,err_msg

    def setSecureText(self, sap_id, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        if(len(input_val)>1):
            text = input_val[2]
        else:
            text=input_val[0]
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        result = None
        encryption_obj = AESCipher()
        try:
            text_decrypted = encryption_obj.decrypt(text)
            #id = elem.__getattr__("Id")
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    ses.FindById(id).text = text_decrypted
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Element state does not allow to perform the operation')
                    err_msg = sap_constants.ERROR_MSG
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
                  err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            import traceback
            traceback.print_exc()
            logger.print_on_console(err_msg,e)
        return status,result,value,err_msg

    def clearText(self, sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            if(id != None):
              if(ses.FindById(id).Changeable == True):
                    if(ses.FindById(id).type == 'GuiCTextField' or 'GuiTextField' or 'GuiPasswordField'):
                        ses.FindById(id).text = ""
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Element state does not allow to perform the operation')
              else:
                    logger.print_on_console( "Element is not changeable")
                    err_msg = "Element is not changeable"
                    #log.info(err_msg)
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console('Error occurred in clearText and is a :',e)
        return status,result,value,err_msg

    def verifyText(self, sap_id,input_val, *args):
        self.lk.setWindowToForeground(sap_id)
        text=input_val[0].strip()
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            if(id != None):
                    if(ses.FindById(id).text.strip() == text):
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                        logger.print_on_console('The text obtained is ',result)
                    else:
                        logger.print_on_console('Element text does not match input text')
                        err_msg='Element text does not match input text'
            else:
                  logger.print_on_console('Element not present on the page where operation is trying to be performed')
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg

    def getTextboxLength(self, sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=''
        try:
            if(id != None):
##                if(ses.FindById(id).Changeable == True):
                    if(ses.FindById(id).type == "GuiTextField" or "GuiCTextField"):
                        value= ses.FindById(id).MaxLength#1:40
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Element state does not allow to perform the operation')
##                else:
##                    logger.print_on_console( "Element is not changeable")
##                    err_msg = "Element is not changeable"
##                    log.info(err_msg)
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console('Error occured in getText and is a :',e)
        return status,result,value,err_msg


    def verifyTextboxLength(self, sap_id,input_val, *args):
        self.lk.setWindowToForeground(sap_id)
        length=int(input_val[0])
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            if(id != None):
##              if(ses.FindById(id).Changeable == True):
                    if(ses.FindById(id).MaxLength == length):
                        #value = ses.FindById(id).MaxLength
                        status=sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = sap_constants.ERROR_MSG
                        logger.print_on_console('Given Length Does not match')
##              else:
##                logger.print_on_console( "Element is not changeable")
##                err_msg = "Element is not changeable"
##                log.info(err_msg)
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console('Error cooured in getText and is a :',e)
        return status,result,value,err_msg





