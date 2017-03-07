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
import logging
import logger

log = logging.getLogger('button_link_keywords_mobility.py')

class Button_Keywords():

    def press(self, element,input_val,*args):

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
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=install_and_launch.driver
                        action = TouchAction(driver)
                        action.tap(element).perform()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)

        except Exception as e:
            log.error(e)
            logger.print_on_console(err_msg)

        return status,methodoutput,output,err_msg


    def long_press(self, element,input_val,*args):
        print 'inside the long ores'
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
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        driver=install_and_launch.driver
                        action = TouchAction(driver)
                        action.long_press(element).perform()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)

        except Exception as e:
            print 'error occured'
            print e
            import traceback
            traceback.print_exc()
            log.error(e)
            logger.print_on_console(err_msg)

        return status,methodoutput,output,err_msg


    def get_button_name(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if type(webelement) is list:
                   webelement=webelement[0]
            if webelement is not None:
                    if webelement.is_enabled():
                        log.debug(WEB_ELEMENT_ENABLED)
                        output=webelement.text
                        status=TEST_RESULT_PASS
                        result=TEST_RESULT_TRUE
                    else:
                        err_msg='ERR_DISABLED_OBJECT'
        except Exception as e:
                log.error(e)
                logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def verify_button_name(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            input_val=input[0]
            if len(input_val)>0 :
                if type(webelement) is list:
                       webelement=webelement[0]
                if webelement is not None:
                        if webelement.is_enabled():
                            log.debug(WEB_ELEMENT_ENABLED)
                            if webelement.text==input_val:
                                log.debug('text matched')
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                        else:
                            err_msg='ERR_DISABLED_OBJECT'
                            logger.print_on_console(err_msg)
        except Exception as e:
                log.error(e)
                logger.print_on_console(err_msg)
        return status,result,output,err_msg

