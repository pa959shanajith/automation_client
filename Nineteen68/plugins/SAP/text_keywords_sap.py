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
import launch_keywords
import win32com.client
from constants import *
from sap_scraping import Scrape
import logger
import time
import pythoncom
from encryption_utility import AESCipher
class Text_Keywords():
    def getSapObject(self):
        SapGui=None
        try:
                pythoncom.CoInitialize()
                SapGui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
        except Exception as e:
                logger.print_on_console( 'Not able to find window to getSapElement',e)
                import traceback
                traceback.print_exc()
        return SapGui

    def getSapElement(self,sap_id,*args):
        try:
            tk=Text_Keywords()
            SapGui=tk.getSapObject()
            scrappingObj=Scrape()                                   #calling scrape class
            wnd = scrappingObj.getWindow(SapGui)                      #calling window method
            #logger.print_on_console( 'wnd--------------------',wnd)
            wndId =  wnd.__getattr__('id')                         # windowid from name
            i = wndId.index('wnd')
            wndNumber = wndId[i+4]                  #getting window number
            j = wndId.index('ses')
            sesId = wndId[0:j+6]
            #print sesId
            ses = SapGui.FindByid(str(sesId))
            sesNumber = wndId[j+4]                  #get session number
            k = wndId.index('con')
            conNumber = wndId[k+4]                   #get connection number
            index = sap_id.index('/')
            path = sap_id[index:]

            id = '/app/con[' + conNumber + ']/ses[' + sesNumber + ']/wnd[' + wndNumber + ']' + path
            return id,ses
        except Exception as e:
            logger.print_on_console( 'no instance open error :',e)
        except AttributeError as e1:
            logger.print_on_console( ' attribute  error :',e1)


    def getText(self, sap_id,url, *args):
        tk=Text_Keywords()
        time.sleep(2)
        id,ses=tk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=''
        try:
            if(id != None):
                if(ses.FindById(id).type == 'GuiCTextField' or 'GuiTextField'):
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                    value=ses.FindById(id).text

                else:
                    logger.print_on_console('Element state does not allow to perform the operation')
                    err_msg = sap_constants.ERROR_MSG
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
                  err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            Exceptions.error(e)
            logger.print_on_console('Error occured in getText and is a :',e)
        return status,result,value,err_msg

    def setText(self, sap_id,url,input_va, *args):
        input_val=input_va[0]
        tk=Text_Keywords()
        time.sleep(2)
        id,ses=tk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):
                if(ses.FindById(id).type == 'GuiCTextField' or 'GuiTextField'):
                    try:
                     ses.FindById(id).text = input_val
                     status = sap_constants.TEST_RESULT_PASS
                     result = sap_constants.TEST_RESULT_TRUE
                    except Exception as e:
                        err_msg = sap_constants.ERROR_MSG
                        logger.print_on_console('error in set text:  :',e)


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
        return status,result,value,err_msg

    def setSecureText(self, sap_id,url, input_val,*args):
        text=input_val[0]
        tk=Text_Keywords()
        time.sleep(2)
        id,ses=tk.getSapElement(sap_id)
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

    def clearText(self, sap_id,url, *args):
        logger.print_on_console('inside  setText')
        logger.print_on_console('sap_id:  ',sap_id)
        tk=Text_Keywords()
        time.sleep(2)
        id,ses=tk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            if(id != None):
              if(ses.FindById(id).Changeable == True):
                if(ses.FindById(id).type == 'GuiCTextField' or 'GuiTextField'):
                    ses.FindById(id).text = ""
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Element state does not allow to perform the operation')
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
##            Exceptions.error(e)
            logger.print_on_console('Error cooured in getText and is a :',e)
        return status,result,value,err_msg

    def verifyText(self, sap_id,url,input_val, *args):
        text=input_val[0]
        tk=Text_Keywords()
        time.sleep(2)
        id,ses=tk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            if(id != None):
                if(ses.FindById(id).text == text):
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                    logger.print_on_console('The text obtained is ',result)
                else:
                    logger.print_on_console('Element state does not allow to perform the operation')
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg

    def getTextboxLength(self, sap_id, *args):
        tk=Text_Keywords()
        time.sleep(2)
        id,ses=tk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=''
        try:
            if(id != None):
                if(ses.FindById(id).type == "GuiTextField" or "GuiCTextField"):
                    value= ses.FindById(id).MaxLength#1:40
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE

                else:
                    logger.print_on_console('Element state does not allow to perform the operation')
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console('Error cooured in getText and is a :',e)
        return status,result,value,err_msg


    def verifyTextboxLength(self, sap_id,url,input_val, *args):
        length=int(input_val[0])
        tk=Text_Keywords()
        time.sleep(2)
        id,ses=tk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            if(id != None):
              if(ses.FindById(id).Changeable == True):
                if(ses.FindById(id).MaxLength == length):
                    value = ses.FindById(id).MaxLength
                    status=sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE

                else:
                    err_msg = sap_constants.ERROR_MSG
                    logger.print_on_console('Given Length Does not match')

            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console('Error cooured in getText and is a :',e)
        return status,result,value,err_msg

