#-------------------------------------------------------------------------------
# Name:        SAP_Dropdown_Keywords
# Purpose:     Module for Dropdown_Keywords
#
# Author:      anas.ahmed1,kavyasree,sakshi.goyal,Saloni
#
# Created:     07-04-2017
# Copyright:   (c) anas.ahmed1 (2017)
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
import sap_constants
from constants import *
from saputil_operations import SapUtilKeywords
from sap_launch_keywords import Launch_Keywords
import logging
import logging.config
log = logging.getLogger('sap_dropdown_keywords.py')

class Dropdown_Keywords():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()

    def getSelected(self,sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value = OUTPUT_CONSTANT
        try:
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    value = ses.FindById(id).Text.strip()
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console( "Element is not changeable")
                    err_msg = "Element is not changeable"
                    log.info(err_msg)
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console("Error occured in getSelected")
        return status,result,value,err_msg



##    def selectValueByIndex(self,sap_id,url,input_val, *args):
##        id,ses=self.uk.getSapElement(sap_id)
##        status = sap_constants.TEST_RESULT_FAIL
##        result = sap_constants.TEST_RESULT_FALSE
##        verb = OUTPUT_CONSTANT
##        index=int(input_val[0])
##        #index=index+1
##        err_msg=None
##        i = 0
##        arr = []
##        try:
##            if(id != None):
##                if(ses.FindById(id).Changeable == True):
##                    entries = ses.FindById(id).Entries
##                    while True:
##                        try:
##                            arr.append(entries(i).value)
##                        except :
##                            break
##                        i = i + 1
##                    try:
##                        ses.FindById(id).value = arr[index]
##                        status=sap_constants.TEST_RESULT_PASS
##                        result=sap_constants.TEST_RESULT_TRUE
##                    except Exception as e:
##                         err_msg=e
##                         logger.print_on_console( 'index out of bound:',e)
##                else:
##                    logger.print_on_console( "Element is not changeable")
##                    err_msg = "Element is not changeable"
##                    log.info(err_msg)
##        except Exception as e:
##             log.error('Error occured',e)
##        return status,result,verb,err_msg

##    def getValueByIndex(self, sap_id, url,input_val,*args):
##        id,ses=self.uk.getSapElement(sap_id)
##        status = sap_constants.TEST_RESULT_FAIL
##        result = sap_constants.TEST_RESULT_FALSE
##        #verb = OUTPUT_CONSTANT
##        value=OUTPUT_CONSTANT
##        index=int(input_val[0])
##        #index=index+1
##        err_msg=None
##        i = 0
##        arr = []
##        try:
##            if(id != None):
##                if(ses.FindById(id).Changeable == True):
##                    entries = ses.FindById(id).Entries
##                    while True:
##                        try:
##                            arr.append(entries(i).value)
##                        except :
##                            break
##                        i = i + 1
##                    try:
##                        value = arr[index]
##                        status=sap_constants.TEST_RESULT_PASS
##                        result=sap_constants.TEST_RESULT_TRUE
##                    except Exception as e:
##                        err_msg=e
##                        logger.print_on_console( 'index out of bound:',e)
##                else:
##                    logger.print_on_console( "Element is not changeable")
##                    err_msg = "Element is not changeable"
##                    log.info(err_msg)
##        except Exception as e:
##            err_msg = sap_constants.ERROR_MSG
##            log.error(err_msg,e)
##        return status,result,value,err_msg

    def selectValueByText(self,sap_id,input_val, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        if(len(input_val)>1):
            text = input_val[2]
        else:
            text=input_val[0]
        value=OUTPUT_CONSTANT
        err_msg=None
        i = 0
        try:
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    entries = ses.FindById(id).Entries
                    while True:
                        try:
                            if(entries(i).value.strip() == text.strip()):
                                ses.FindById(id).value = text
                                status=sap_constants.TEST_RESULT_PASS
                                result=sap_constants.TEST_RESULT_TRUE
                        except Exception as e:
                            break
                        i = i + 1
                else:
                    logger.print_on_console( "Element is not changeable")
                    err_msg = "Element is not changeable"
                    log.info(err_msg)
        except Exception as e:
              log.error('Error occured',e)
              logger.print_on_console("Error occured in selectValueByText")
              err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg


    def verifySelectedValue(self,sap_id,input_val ,*args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        val=input_val[0]
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    if(ses.FindById(id).Text.strip() == val):
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = sap_constants.ERROR_MSG
                        log.info(err_msg)
                else:
                    logger.print_on_console( "Element is not changeable")
                    err_msg = "Element is not changeable"
                    log.info(err_msg)
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console("Error occured in verifySelectedValue")
        return status,result,value,err_msg


    def getCount(self,sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        count = 0
        try:
            if(id != None):
                entries = ses.FindById(id).Entries
                while True:
                    try:
                        value = entries(count).value
                        count = count + 1
                        value=count
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
                    except Exception as e:
                        break
        except Exception as e:
              log.error('Error occured',e)
              logger.print_on_console("Error occured in getCount")
              err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg

    def verifyCount(self,sap_id,input_val, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        length = int(input_val[0])
        verb = OUTPUT_CONSTANT
        value=OUTPUT_CONSTANT
        err_msg=''
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        count = 0
        try:
            if(id != None):
                entries = ses.FindById(id).Entries
                while True:
                    try:
                        value = entries(count).value
                        count = count + 1
                    except Exception as e:
                        break
                if(length == count):
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.ERROR_MSG
                    log.info('Count Verify has failed ')
        except Exception as e:
              log.error('Error occured',e)
              err_msg = sap_constants.ERROR_MSG
              logger.print_on_console("Error occured in verifyCount")
        return status,result,verb,err_msg

    def verifyValuesExists(self,sap_id,input_val, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg=None
        verb = OUTPUT_CONSTANT
        dd_entries = []
        i = 0
        flag=True
        try:
            if(id != None):
                entries = ses.FindById(id).Entries
                while True:
                    try:
                        dd_entries.append(str(entries(i).value).lower())
                        i = i + 1
                    except Exception as e:
                        break
                for inp in input_val:
                    if(inp.lower().strip() not in dd_entries):
                        flag = False
                        break
                if flag==True:
                    status =sap_constants.TEST_RESULT_PASS
                    result =sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.ERROR_MSG
        except Exception as e:
              log.error('Error occured',e)
              err_msg = sap_constants.ERROR_MSG
              logger.print_on_console("Error occured in verifyValuesExists")
        return status,result,verb,err_msg


    def verifyAllValues(self,sap_id,input_val, *args):
        self.lk.setWindowToForeground(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        id,ses=self.uk.getSapElement(sap_id)
        err_msg=None
        value = OUTPUT_CONSTANT
        i = 0
        dd_entries = []
        try:
            if(id != None):
                entries = ses.FindById(id).Entries
                while True:
                    try:
                        dd_entries.append(str(entries(i).value))
                        i = i + 1
                    except Exception as e:
                        break
                flag=True
                if len(dd_entries)==len(input_val):
                    for dd in dd_entries:
                        if dd not in input_val:
                            flag=False
                else:
                    flag=False
                if flag==True:
                    status =sap_constants.TEST_RESULT_PASS
                    result =sap_constants.TEST_RESULT_TRUE
                else:
                  err_msg = sap_constants.ERROR_MSG
        except Exception as e:
              log.error('Error occured',e)
              err_msg = sap_constants.ERROR_MSG
              logger.print_on_console("Error occured in verifyAllValues")
        return status,result,value,err_msg


