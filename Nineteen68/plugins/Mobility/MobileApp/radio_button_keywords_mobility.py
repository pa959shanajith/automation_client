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
import install_and_launch
import android_scrapping
import logging
import logger

log = logging.getLogger('radio_button_keywords_mobility.py')

class Radio_Button_Keywords():

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def select_radio_button(self, element,input_val,*args):
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
                        action = TouchAction(android_scrapping.driver)
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
            err_msg = self.print_error("Error occurred in SelectRadioButton")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def get_status(self,element,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
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
                        classname= element.get_attribute("className")
                        if 'Switch' in classname:
                            res = element.text
                            if res.upper() == 'OFF' or element.get_attribute('checked') == 'false':
                                output = 'OFF'
                            else:
                                output = 'ON'
                        elif 'Radio' in classname:
                            output=element.get_attribute("checked")
                            if output=='true':
                                output='Selected'
                            else:
                                output="UnSelected"
                        elif 'CheckBox' in classname:
                            output=element.get_attribute("checked")
                            if output=='true':
                                output='Checked'
                            else:
                                output="UnChecked"
                        else :
                            output=element.get_attribute("checked")
                        if output is not None:
                            logger.print_on_console("Status: "+output)
                            log.info(output)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in GetStatus")
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg


    def select_checkbox(self, element,input_val,*args):
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
                        action = TouchAction(android_scrapping.driver)
                        if element.get_attribute('checked') == 'false':
                            action.tap(element).perform()
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        elif element.get_attribute('checked') == 'true':
                            logger.print_on_console('Element already selected')
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in SelectCheckBox")
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg


    def unselect_checkbox(self, element,input_val,*args):
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
                        action = TouchAction(android_scrapping.driver)
                        if element.get_attribute('checked') == 'true':
                            action.tap(element).perform()
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        elif element.get_attribute('checked') == 'false':
                            logger.print_on_console('Element already unselected')
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in UnSelectCheckBox")
            log.error(e,exc_info = True)
        return status,methodoutput,output,err_msg
