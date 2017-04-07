#-------------------------------------------------------------------------------
# Name:        text_keywords_sap
# Purpose:    Module for textbox keywords
#
#Author:      anas.ahmed1,kavyashree,sakshi.goyal,saloni.goyal
#
# Created:     07-04-2017
# Copyright:   (c) anas.ahmed1 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sap_constants
##from text_keywords_sap import Text_Box
##from launch_keywords import ldtp
import launch_keywords
import win32com.client
##from ldtp.client_exception import LdtpExecutionError
from constants import *
from sap_scraping import Scrape
##import sap_scraping.Scrape
import logger
import time
##import logging
class Text_Keywords():
    def attach(self,sap_id,*args):
        SapGui=None
        try:
            time.sleep(2)
            #logger.print_on_console( 'inside try block')
            SapGui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
            #logger.print_on_console( 'SapGui-------',SapGui)
            scrappingObj=Scrape()
            #logger.print_on_console( 'scrappingObj',scrappingObj)

            wnd = scrappingObj.getWindow(SapGui)
            #logger.print_on_console( 'wnd--------------------',wnd)
            wndId =  wnd.__getattr__('id')
            i = wndId.index('wnd')
            wndNumber = wndId[i+4]
            j = wndId.index('ses')
            sesId = wndId[j:j+6]
            #print sesId
            ses = SapGui.FindByid(str(sesId))
            sesNumber = wndId[j+4]
            k = wndId.index('con')
            conNumber = wndId[k+4]
            index = sap_id.index('/')
            path = sap_id[index:]

            id = '/app/con[' + conNumber + ']/ses[' + sesNumber + ']/wnd[' + wndNumber + ']' + path
            return id,ses
        except Exception as e:

            logger.print_on_console( 'no instance open error :',e)


    def getText(self, sap_id,url, *args):
##        logger.print_on_console('inside  setText')
##        logger.print_on_console('sap_id:  ',sap_id)
##        logger.print_on_console('input_va type: ',type(input_va))
##        logger.print_on_console('input_val type: ',type(input_val))
        tk=Text_Keywords()
        time.sleep(10)
        id,ses=tk.attach(sap_id)
        status=sap_constants.TEST_RESULT_FALSE
        result=sap_constants.TEST_RESULT_FAIL
        err_msg=None
        value=''
        try:
            if(id != None):
                if(ses.FindById(id).type == 'GuiCTextField' or 'GuiTextField'):
                    #ses.FindById(id).text
                    status = sap_constants.TEST_RESULT_TRUE
                    result = sap_constants.TEST_RESULT_PASS
                    value=ses.FindById(id).text
                    #logger.print_on_console('The text obtained is ',result)
                else:
                    logger.print_on_console('Element state does not allow to perform the operation')
                    err_msg = sap_constants.ERROR_MSG
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
                  err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            Exceptions.error(e)
            logger.print_on_console('Error cooured in getText and is a :',e)
        return status,result,value,err_msg

    def setText(self, sap_id,url,input_va, *args):
        input_val=input_va[0]
##        logger.print_on_console('inside  setText')
##        logger.print_on_console('sap_id:  ',sap_id)
##        logger.print_on_console('input_va type: ',type(input_va))
##        logger.print_on_console('input_val type: ',type(input_val))
        tk=Text_Keywords()
        time.sleep(8)
        id,ses=tk.attach(sap_id)
##        logger.print_on_console('ses from attach method :',ses)
##        logger.print_on_console('id from attach method :',id)
        status=sap_constants.TEST_RESULT_FALSE
        result=sap_constants.TEST_RESULT_FAIL
        value=''
        err_msg=None
        #iid='/app/con[0]/ses[0]/wnd[0]/usr/txtRSYST-MANDT'
        try:
            if(id != None):
                #logger.print_on_console('inside first if ')
                if(ses.FindById(id).type == 'GuiCTextField' or 'GuiTextField'):
                    #logger.print_on_console('type of element is :')
                    #logger.print_on_console('inside second if and type of ID is ',ses.FindById(id).type)
                    #logger.print_on_console('inputvale is :',input_val)

                    #logger.print_on_console('wait time started')
                    #time.sleep(2)
                    #logger.print_on_console('wait time ended')
                    try:
                     ses.FindById(id).text = input_val
                     status = sap_constants.TEST_RESULT_TRUE
                     result = sap_constants.TEST_RESULT_PASS
                    except Exception as e:
                        err_msg = sap_constants.ERROR_MSG
                        logger.print_on_console('error in set text:  :',e)
                        import traceback
                        traceback.print_exc()

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
##            logger.print_on_console('Error cooured in getText and is a :',e)
##        logger.print_on_console('The text obtained is ',result)
##        logger.print_on_console('The text obtained is ',status)
##        logger.print_on_console('The text obtained is ',value)
##        logger.print_on_console('The text obtained is ',err_msg)
        return status,result,value,err_msg

    def clearText(self, sap_id,url, *args):
        #input_val=input_va[0]
        logger.print_on_console('inside  setText')
        logger.print_on_console('sap_id:  ',sap_id)
        #logger.print_on_console('input_va type: ',type(input_va))
        #logger.print_on_console('input_val type: ',type(input_val))
        tk=Text_Keywords()
        time.sleep(10)
        id,ses=tk.attach(sap_id)
        status=sap_constants.TEST_RESULT_FALSE
        result=sap_constants.TEST_RESULT_FAIL
        err_msg=None
        value=''
        try:
            if(id != None):
              if(ses.FindById(id).Changeable == True):
                if(ses.FindById(id).type == 'GuiCTextField' or 'GuiTextField'):
                    ses.FindById(id).text = ""
                    status = sap_constants.TEST_RESULT_TRUE
                    result = sap_constants.TEST_RESULT_PASS
                else:
                    logger.print_on_console('Element state does not allow to perform the operation')
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
##            Exceptions.error(e)
            logger.print_on_console('Error cooured in getText and is a :',e)
        return status,result,value,err_msg

    def verifyText(self, sap_id,url,text, *args):
        input_val=text[0]
##        logger.print_on_console('inside  setText')
##        logger.print_on_console('sap_id:  ',sap_id)
##        logger.print_on_console('input_va type: ',type(input_va))
##        logger.print_on_console('input_val type: ',type(input_val))
        tk=Text_Keywords()
        time.sleep(3)
        id,ses=tk.attach(sap_id)
        status=sap_constants.TEST_RESULT_FALSE
        result=sap_constants.TEST_RESULT_FAIL
        err_msg=None
        value=''
        try:
            if(id != None):
                if(ses.FindById(id).text == text):
                    status = sap_constants.TEST_RESULT_TRUE
                    result = sap_constants.TEST_RESULT_PASS
                    logger.print_on_console('The text obtained is ',result)
                else:
                    logger.print_on_console('Element state does not allow to perform the operation')
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            Exceptions.error(e)
##            logger.print_on_console('Error cooured in getText and is a :',e)
##        logger.print_on_console('The text obtained is ',result)
##        logger.print_on_console('The text obtained is ',status)
##        logger.print_on_console('The text obtained is ',value)
##        logger.print_on_console('The text obtained is ',err_msg)
        return status,result,value,err_msg

    def getTextboxLength(self, sap_id,url, *args):
        #input_val=input_va[0]
##        logger.print_on_console('inside  setText')
##        logger.print_on_console('sap_id:  ',sap_id)
        #logger.print_on_console('input_va type: ',type(input_va))
        #logger.print_on_console('input_val type: ',type(input_val))
        tk=Text_Keywords()
        time.sleep(3)
        id,ses=tk.attach(sap_id)
        status=sap_constants.TEST_RESULT_FALSE
        result=sap_constants.TEST_RESULT_FAIL
        err_msg=None
        value=''
        try:
            if(id != None):
                if(ses.FindById(id).type == "GuiTextField" or "GuiCTextField"):
                    value= ses.FindById(id).MaxLength#1:40
                    status = sap_constants.TEST_RESULT_FAIL
                    result = sap_constants.TEST_RESULT_PASS
                    #logger.print_on_console('The lenght obtained is ',result)
                else:
                    logger.print_on_console('Element state does not allow to perform the operation')
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            Exceptions.error(e)
            logger.print_on_console('Error cooured in getText and is a :',e)
        return status,result,value,err_msg


    def verifyTextboxLength(self, sap_id,url, *args):
        #input_val=input_va[0]
        logger.print_on_console('inside  setText')
        logger.print_on_console('sap_id:  ',sap_id)
        #logger.print_on_console('input_va type: ',type(input_va))
        #logger.print_on_console('input_val type: ',type(input_val))
        tk=Text_Keywords()
        time.sleep(3)
        id,ses=tk.attach(sap_id)
        status=sap_constants.TEST_RESULT_FALSE
        result=sap_constants.TEST_RESULT_FAIL
        err_msg=None
        value=''
        try:
            if(id != None):
              if(ses.FindById(id).Changeable == True):
                if(ses.FindById(id).MaxLength == length):
                    value = ses.FindById(id).MaxLength
                    result=sap_constants.TEST_RESULT_PASS
                    status = sap_constants.TEST_RESULT_TRUE

                else:
                    logger.print_on_console('Element state does not allow to perform the operation')

            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            Exceptions.error(e)
            logger.print_on_console('Error cooured in getText and is a :',e)
        return status,result,value,err_msg