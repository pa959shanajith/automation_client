#-------------------------------------------------------------------------------
# Name:        ButtonLinkKeyword
# Purpose:     Module for Button link keywords
#
# Author:      anas.ahmed1,kavyasree.l.Sakshi,Saloni
#
# Created:     07-04-2017
# Copyright:   (c) anas.ahmed1 (2017)
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sap_constants
from sap_launch_keywords import Launch_Keywords
from saputil_operations import SapUtilKeywords
from constants import *
import logger
import logging
import logging.config
log = logging.getLogger('button_link_keywords_sap.py')

class ButtonLinkKeyword():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()

##    def click(self, sap_id, *args):
##        self.lk.setWindowToForeground(sap_id)
##        id,ses=self.uk.getSapElement(sap_id)
##        status=sap_constants.TEST_RESULT_FAIL
##        result=sap_constants.TEST_RESULT_FALSE
##        #log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
##        #verb = OUTPUT_CONSTANT
##        value=OUTPUT_CONSTANT
##        err_msg=None
##        try:
##                if(id != None):
##                 if(ses.FindById(id).Changeable == True):
##                    ses.FindById(id).Press()
##                    status =sap_constants.TEST_RESULT_PASS
##                    result = sap_constants.TEST_RESULT_TRUE
##                 else:
##                        log.info('Element state does not allow to perform the operation')
##                        err_msg = 'Element state does not allow to perform the operation'
##                else:
##                    log.info('element not present on the page where operation is trying to be performed')
##                    err_msg = 'element not present on the page where operation is trying to be performed'
##        except Exception as e:
##            import traceback
##            traceback.getexc()
####            logger.print_on_console('Error has occured',e)
##            log.error(e)
##        return status,result,value,err_msg

    def get_button_name(self,  sap_id , *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):
               if(ses.FindById(id).Text != None):
                 value=ses.FindById(id).Text
                 status =sap_constants.TEST_RESULT_PASS
                 result = sap_constants.TEST_RESULT_TRUE
               else:
                 logger.print_on_console('Button name is not defined')
            else:
                log.info('element not present on the page where operation is trying to be performed')
                err_msg = 'element not present on the page where operation is trying to be performed'
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in getButtonName")
        return status,result,value,err_msg

    def verify_button_name(self,  sap_id , input_val, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        name=input_val[0]
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):
                if(ses.FindById(id).Text != None and ses.FindById(id).Text.lstrip() == name.lstrip()):
                    status =sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    log.info('Button name is not Matching')
                    err_msg = 'Button name is not Matching'
            else:
                log.info('element not present on the page where operation is trying to be performed')
                err_msg = 'element not present on the page where operation is trying to be performed'
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in verifyButtonName")
        return status,result,value,err_msg

    def button_uploadFile(self,sap_id, input_val, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        filepath=input_val[0]
        log.debug('Got window name after launching application')
        log.debug(sap_launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            result = None
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    j = 1
                    index = 0
                    li = []
                    """finding the occurence of \ (backslash) in filepath and appending the index in list"""
                    for letter in filepath:
                        if(letter == '\\'):
                            li.append(index)
                        index = index + 1
                    """for every occurence of backslash which is not succeeded with another backslash, appending it with another backslash
                     so that it is not considered as an escape character"""
                    for i in li:
                        if(filepath[i+1] != '\\'):
                            filepath = filepath[:i] + '\\' + filepath[i:]
                            """incresing the indexes stored in the list by one...since one more backslash has been added in the string"""
                            for k in range(j, len(li)):
                                li[k] = li[k] + 1
                            j = j + 1
                    ses.FindById(id).text = filepath
                    status =sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg = 'element not present on the page where operation is trying to be performed'
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in uploadFile")
        return status,result,value,err_msg


