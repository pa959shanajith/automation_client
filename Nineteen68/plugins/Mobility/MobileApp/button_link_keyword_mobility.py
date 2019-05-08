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
                        driver=android_scrapping.driver
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

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        input = input_val[0]
        try:
            if element is not None:
                visibility=element.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=element.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
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

                        log.debug(WEB_ELEMENT_ENABLED)
                        output=webelement.text
                        logger.print_on_console("Button name: "+output)
                        status=TEST_RESULT_PASS
                        result=TEST_RESULT_TRUE

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

                            log.debug(WEB_ELEMENT_ENABLED)
                            if webelement.text==input_val:
                                log.debug('text matched')
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE

        except Exception as e:
                log.error(e)
                logger.print_on_console(err_msg)
        return status,result,output,err_msg

