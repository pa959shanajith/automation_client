#-------------------------------------------------------------------------------
# Name:        module1
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
from appium.webdriver.common.touch_action import TouchAction
#import install_and_launch
import android_scrapping
import logging
import logger

log = logging.getLogger('button_link_keywords_mobility.py')

class Button_Keywords():

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def press(self, element,input_val,*args):
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
                        driver=android_scrapping.driver
                        action = TouchAction(driver)
                        action.tap(element).perform()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in Press")
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg


    def click(self, element,input_val,*args):
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
                        element.click()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in Click")
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg


    def long_press(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        input = input_val[0]
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver
                        action = TouchAction(driver)
                        if input is not None and input != '' :
                            action.long_press(element).wait(int(input)*1000).release().perform()
                        else:
                            action.long_press(element).wait(3000).release().perform()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in LongPress")
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg


    def get_button_name(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if type(element) is list:
                element=element[0]
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(WEB_ELEMENT_ENABLED)
                        output=element.text
                        logger.print_on_console("Button name: "+output)
                        status=TEST_RESULT_PASS
                        result=TEST_RESULT_TRUE
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                        output=element.text
                        logger.print_on_console("Button name: "+output)
                        status=TEST_RESULT_PASS
                        result=TEST_RESULT_TRUE
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in GetButtonName")
            log.error(e,exc_info = True)
        return status,result,output,err_msg


    def verify_button_name(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            input_val=input[0]
            if len(input_val)>0 :
                if type(element) is list:
                    element=element[0]
                if element is not None:
                    if element.is_displayed():
                        log.debug(ELEMENT_VISIBLE)
                        if element.is_enabled():
                            log.debug(ELEMENT_ENABLED)
                            if element.text==input_val:
                                log.debug('text matched')
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                            else:
                                logger.print_on_console("Button name: "+element.text)
                        else:
                            err_msg = self.print_error(ELEMENT_DISABLED)
                            if element.text==input_val:
                                log.debug('text matched')
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                            else:
                                logger.print_on_console("Button name: "+element.text)
                    else:
                        err_msg = self.print_error(ELEMENT_HIDDEN)
                else:
                    err_msg = self.print_error(ELEMENT_NOT_EXIST)
            else:
                err_msg = self.print_error(INVALID_INPUT)
        except Exception as e:
            err_msg = self.print_error("Error occurred in VerifyButtonName")
            log.error(e,exc_info = True)
        return status,result,output,err_msg
