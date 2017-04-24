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
from text_keywords_sap import Text_Keywords

#log = logging.getLogger('utilweb_operations.py')

class SapUtilKeywords:


    def verifyEnabled(self, sap_id, *args):
        tk=Text_Keywords()
        time.sleep(2)
        id,ses=tk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        result = None
        try:
##            id = elem.__getattr__("Id")
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
        tk=Text_Keywords()
        time.sleep(2)
        id,ses=tk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        result = None
        try:
##            id = elem.__getattr__("Id")
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
        tk=Text_Keywords()
        time.sleep(2)
        id,ses=tk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        result = None
        try:
##            id = elem.__getattr__("Id")
            if(id != None):
                result = True
                status=sap_constants.TEST_RESULT_PASS
                result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
             log.error('Error occured',e)
        return status,result,value,err_msg

    def setFocus(self, sap_id, *args):
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
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



