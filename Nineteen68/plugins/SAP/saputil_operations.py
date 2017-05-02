#-------------------------------------------------------------------------------
# Name:        utilweb_operations.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     08-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sap_constants
import launch_keywords
import win32com.client
from constants import *
from sap_scraping import Scrape
import logger
import time

#log = logging.getLogger('saputil_operations.py')

class SapUtilKeywords:


    def getSapObject(self):
        self.SapGui=None
        try:
            import pythoncom
            pythoncom.CoInitialize()
            self.SapGui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
        except Exception as e:
            logger.print_on_console( 'Not able to find window to getSapElement',e)
            import traceback
            traceback.print_exc()
        return self.SapGui

    def getSapElement(self,sap_id,*args):
        try:
            SapGui = self.getSapObject()
            scrappingObj=Scrape()                                   #calling scrape class
            wnd = scrappingObj.getWindow(SapGui)                      #calling window method
            #logger.print_on_console( 'wnd--------------------',wnd)
            wndId =  wnd.__getattr__('id')                         # windowid from name
##            i = wndId.index('wnd')
##            wndNumber = wndId[i+4]                  #getting window number
            j = wndId.index('ses')
            sesId = wndId[0:j+6]
            #print sesId
            ses = SapGui.FindByid(str(sesId))
##            sesNumber = wndId[j+4]                  #get session number
##            k = wndId.index('con')
##            conNumber = wndId[k+4]                   #get connection number
##            index = sap_id.index('/')
##            path = sap_id[index:]
##            id = '/app/con[' + conNumber + ']/ses[' + sesNumber + ']/wnd[' + wndNumber + ']' + path
            i = sap_id.index("/")
            id = wndId + sap_id[i:]
            return id,ses
        except Exception as e:
            logger.print_on_console( 'No instance open error :',e)
        except AttributeError as e1:
            logger.print_on_console( ' Attribute  error :',e1)


    def verifyEnabled(self, sap_id, *args):
        time.sleep(2)
        id,ses=self.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        result = None
        try:
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    result = True
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                else:
                    result = False
        except Exception as e:
            log.error('Error occured',e)
        return status,result,value,err_msg

    def verifyDisabled(self, sap_id, *args):
        time.sleep(2)
        id,ses=self.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        result = None
        try:
            if(id != None):
                if(ses.FindById(id).Changeable == False):
                    result = True
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                else:
                    result = False
        except Exception as e:
            log.error('Error occured',e)
        return status,result,value,err_msg

    def VerifyExists(self, sap_id, *args):
        time.sleep(2)
        id,ses=self.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            if(id != None):
                status=sap_constants.TEST_RESULT_PASS
                result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
             log.error('Error occured',e)
        return status,result,value,err_msg

    def setFocus(self, sap_id, *args):
        id,ses=self.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            elem.SetFocus()
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg
