#-------------------------------------------------------------------------------
# Name:        toggle_keywords.py
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
import logging
import logger

log = logging.getLogger('toggle_keywords.py')

class ToggleKeywords():

    def __driver_exception(self,e):
        err_msg=ANDROID_ERROR
        log.error(e)
        logger.print_on_console(err_msg)
        return err_msg

    def toggle_on(self, element,input_val,*args):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                visibility=element.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=element.is_enabled()
                    if enable:
                        log.debug(WEB_ELEMENT_ENABLED)
                        log.debug('performing the action')
                        res=element.text
                        log.debug('Result is '+res)
                        if res.upper()=='OFF':
                            action = TouchAction(install_and_launch.driver)
                            action.tap(element).perform()
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            err_msg=TOGGLE_ON
                            log.error(err_msg)
                            logger.print_on_console(err_msg)
                    else:
                        err_msg=WEB_ELEMENT_DISABLED
                        log.error(err_msg)
                        logger.print_on_console(err_msg)
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    log.error(err_msg)
                    logger.print_on_console(err_msg)

        except Exception as e:
            err_msg=self.__driver_exception(e)
        return status,methodoutput,output,err_msg

    def toggle_off(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        status=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:

                if element is not None:
                    visibility=element.is_displayed()
                    log.debug('element is visible')
                    if visibility:
                        enable=element.is_enabled()
                        if enable:
                            log.debug(WEB_ELEMENT_ENABLED)
                            log.debug('performing the action')
                            res=element.get_attribute("checked")
                            if res.upper()=='ON':
                                action = TouchAction(install_and_launch.driver)
                                action.tap(element).perform()
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                            else:
                                 err_msg=TOGGLE_OFF
                                 log.error(err_msg)
                                 logger.print_on_console(err_msg)
                        else:
                            err_msg=WEB_ELEMENT_DISABLED
                            log.error(err_msg)
                            logger.print_on_console(err_msg)
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                        log.error(err_msg)
                        logger.print_on_console(err_msg)
            except Exception as e:
                err_msg=self.__driver_exception(e)
        return status,methodoutput,output,err_msg

