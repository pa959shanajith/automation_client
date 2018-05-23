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
import win32com.client
from constants import *
from sap_scraping import Scrape
import logger
import logging
import logging.config
log = logging.getLogger('saputil_operations.py')
class SapUtilKeywords:


    def getSapObject(self):
        self.SapGui=None
        try:
            import pythoncom
            pythoncom.CoInitialize()
            self.SapGui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
        except Exception as e:
            logger.print_on_console( 'Not able to find SAPGUI object')
            log.error(e)
        return self.SapGui

    def getSapElement(self,sap_id,*args):
        id=''
        ses=''
        try:
            SapGui = self.getSapObject()
            scrapingObj=Scrape()                                   #calling scrape class
            wnd = scrapingObj.getWindow(SapGui)                      #calling window method
            wndId =  wnd.__getattr__('id')                         # windowid from name
            j = wndId.index('ses')
            sesId = wndId[0:j+6]
            ses = SapGui.FindByid(str(sesId))
            #-----------------------------------------------------Checking if there is a "/" in the sap_id, if exists take the index(i) after the "/"'s in title to append to id
            title = ses.ActiveWindow.Text
            if("/" in title):
                i = sap_id.index("/",len(title))
            else:
                i = sap_id.index("/")
                #-----------------------------------------------------
            id = wndId + sap_id[i:]
        except Exception as e:
            logger.print_on_console( 'No instance open error :',e)
        except AttributeError as e1:
            logger.print_on_console( ' Attribute  error :',e1)
        return id,ses


    def verifyEnabled(self, sap_id, *args):
        id,ses=self.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            if(id != None):
                if(ses.FindById(id).type == "GuiLabel" or ses.FindById(id).Changeable == True):
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console("Element is disabled.")
        except Exception as e:
            logger.print_on_console("Error occured in verifyEnabled")
            log.error(e)
        return status,result,value,err_msg

    def verifyDisabled(self, sap_id, *args):
        id,ses=self.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            if(id != None):
                if(ses.FindById(id).type == "GuiLabel" or ses.FindById(id).Changeable == False):
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console("Element is enabled.")
        except Exception as e:
            logger.print_on_console("Error occured in verifyDisabled")
            log.error(e)
        return status,result,value,err_msg

    def verifyExists(self, sap_id, *args):
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
            logger.print_on_console("Error occured in verifyExists")
            log.error(e)
        return status,result,value,err_msg

    def verifyHidden(self, sap_id, *args):
        id,ses=self.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            if(id != None):
                try:
                    ses.FindById(id)
                    err_msg="Element is visible"
                    logger.print_on_console("Element is visible")
                except Exception as e:
##                    if e[2][2]=='The control could not be found by id.':
##                        logger.print_on_console("Element is hidden")
                    logger.print_on_console("Element is hidden")
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console("Error occured in verifyHidden")
            log.error(e)
        return status,result,value,err_msg

    def verifyVisible(self, sap_id, *args):
        id,ses=self.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            if(id != None):
                try:
                    ses.FindById(id)
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                    logger.print_on_console("Element is visible")
                except Exception as e:
                    err_msg="Element is hidden"
                    if e[2][2]=='The control could not be found by id.':
                        logger.print_on_console("Element is hidden")
        except Exception as e:
            logger.print_on_console("Error occured in verifyVisible")
            log.error(e)
        return status,result,value,err_msg

    def getobjectforcustom(self, sap_id, eleType, eleIndex):
        data = []
        xpath = None
        try:
            id,ses=self.getSapElement(sap_id)
            reference_elem = ses.FindById(id)
            wnd_id = id[:26]
            wnd = ses.FindById(wnd_id)
            wnd_title = wnd.__getattr__("Text")
            scrapingObj=Scrape()
            data = scrapingObj.full_scrape(reference_elem, wnd_title)
            for elem in data:
                if elem['tag'].lower() == eleType.strip().lower():
                    eleIndex = int(eleIndex) - 1
                    if(eleIndex == 0):
                        xpath = elem['xpath']
        except Exception as e:
            logger.print_on_console("Error occured while finding custom object")
            log.error(e)
        return xpath

