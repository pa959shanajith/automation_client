#-------------------------------------------------------------------------------
# Name:        slider_util_keywords.py
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     20-01-2017
# Copyright:   (c) prudhvi.gujjuboyina 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from constants import *
from mobile_app_constants import *
import android_scrapping
import logging
import logger
import time
import mobile_app_dispatcher
import readconfig

log = logging.getLogger('slider_util_keywords.py')

class SliderKeywords():

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def set_slide_value(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        element.set_value(input_val[0])
                        methodoutput=TEST_RESULT_TRUE
                        status = TEST_RESULT_PASS
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in SetSlideValue")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def get_slide_value(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        output= x=str(float(element.get_attribute('value').replace('%',''))/100)[:3]
                        logger.print_on_console("Slide value: "+element.text)
                        methodoutput=TEST_RESULT_TRUE
                        status = TEST_RESULT_PASS

                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in GetSlideValue")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def verify_enabled(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in VerifyEnabled")
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg


    def verify_disabled(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if not(element.is_enabled()):
                        log.info(ELEMENT_DISABLED)
                        log.debug('performing the action')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = self.print_error(ELEMENT_ENABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in VerifyDisabled")
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg


    def verify_visible(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.info(ELEMENT_VISIBLE)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in VerifyVisible")
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg


    def verify_hidden(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if not(element.is_displayed()):
                    log.info(ELEMENT_HIDDEN)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg = self.print_error(ELEMENT_VISIBLE)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in VerifyHidden")
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg


    def verify_exists(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                log.info(ELEMENT_EXISTS)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in VerifyExists")
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg


    def verify_does_not_exists(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is None:
                log.info(ELEMENT_NOT_EXIST)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            else:
                err_msg = self.print_error(ELEMENT_EXISTS)
        except Exception as e:
            err_msg = self.print_error("Error occurred in VerifyDoesNotExists")
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg


    def waitforelement_exists(self, object_name,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            dispatcher=mobile_app_dispatcher.MobileDispatcher()
            configvalues = readconfig.configvalues
            timeout= configvalues['timeOut']
            if timeout!=None:
                start_time = time.time()
                while True:
                    element, xpath=dispatcher.getMobileElement(android_scrapping.driver,object_name)
                    later=time.time()
                    if int(later-start_time)>=int(timeout):
                        err_msg = self.print_error(DELAY_TIMEOUT)
                        break
                    if element is not None:
                        logger.print_on_console(ELEMENT_EXISTS)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        break
            else:
                err_msg = self.print_error(INVALID_INPUT)
        except Exception as e:
            err_msg = self.print_error("Error occurred in WaitForElementExists")
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg

