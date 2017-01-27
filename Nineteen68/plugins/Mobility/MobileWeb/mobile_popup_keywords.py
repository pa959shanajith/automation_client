#-------------------------------------------------------------------------------
# Name:        mobile_popup_keywords.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     09-11-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import logger
import time
import mobileconstants
from selenium import webdriver

import mobile_browser_keywords
import logging
from constants import *

log = logging.getLogger('mobile_popup_keywords.py')
class PopupKeywords():
    def accept_popup(self,webelement,*args):
        driver = mobile_browser_keywords.driver_obj
        log.debug('Got the driver object from browser keyword class')
        log.debug(driver)
        status = mobileconstants.TEST_RESULT_FAIL
        methodoutput = mobileconstants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            #code to accept the pop up
            log.debug('Switching to Alert')
            driver.switch_to.alert.accept()
            logger.print_on_console('Switched to Alert and accepted the alert')
            log.info('Switched to Alert and accepted')
            log.info(STATUS_METHODOUTPUT_UPDATE)
            status = mobileconstants.TEST_RESULT_PASS
            methodoutput = mobileconstants.TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            log.error(EXCEPTION_OCCURED)
            log.error(e)
        log.info(RETURN_RESULT)
        return status,methodoutput

    def dismiss_popup(self,webelement,*args):
        driver = mobile_browser_keywords.driver_obj
        log.debug('Got the driver object from browser keyword class')
        log.debug(driver)
        status = mobileconstants.TEST_RESULT_FAIL
        methodoutput = mobileconstants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            #code to dismiss the pop up
            log.debug('Switching to Alert')
            driver.switch_to.alert.dismiss()
            logger.print_on_console('Switched to Alert and dismissed(closed) the alert')
            log.info('Switched to Alert and dismissed(closed) the alert')
            log.info(STATUS_METHODOUTPUT_UPDATE)
            status = mobileconstants.TEST_RESULT_PASS
            methodoutput = mobileconstants.TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            log.error(EXCEPTION_OCCURED)
            log.error(e)
        log.info(RETURN_RESULT)
        return status,methodoutput

    def get_popup_text(self,webelement,*args):
        driver = mobile_browser_keywords.driver_obj
        log.debug('Got the driver object from browser keyword class')
        log.debug(driver)
        status = mobileconstants.TEST_RESULT_FAIL
        methodoutput = mobileconstants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            #code to get the pop up text
            log.debug('Switching to Alert')
            text = driver.switch_to.alert.text
            logger.print_on_console('Switched to Alert and retrieved the text')
            log.info('Switched to Alert and retrieved the text')
            logger.print_on_console('Alert text= ', text)
            log.info('Alert text= '+ str( text))
            log.info(STATUS_METHODOUTPUT_UPDATE)
            status = mobileconstants.TEST_RESULT_PASS
            methodoutput = mobileconstants.TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            log.error(EXCEPTION_OCCURED)
            log.error(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,text

    def verify_popup_text(self,webelement,inputs,*args):
        driver = mobile_browser_keywords.driver_obj
        log.debug('Got the driver object from browser keyword class')
        log.debug(driver)
        status = mobileconstants.TEST_RESULT_FAIL
        methodoutput = mobileconstants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            #code to verify the pop up text
            log.debug('Switching to Alert')
            text = driver.switch_to.alert.text
            logger.print_on_console('Switched to Alert and retrieved the text')
            log.info('Switched to Alert and retrieved the text')
            logger.print_on_console('Alert text : ' , text)
            log.info('Alert text= '+ str( text))
            input = inputs[0]
            input = input.strip()
            logger.print_on_console('Input text : ' , input)
            log.info('Input text= '+ str( input))
            if text == input:
                logger.print_on_console('Alert Text matched')
                log.info('Alert Text matched')
                log.info(STATUS_METHODOUTPUT_UPDATE)
                status = mobileconstants.TEST_RESULT_PASS
                methodoutput = mobileconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Alert Text mismatched')
                log.info('Alert Text mismatched')
                logger.print_on_console('Expected: ',text)
                log.info('Expected:')
                log.info(text)
                logger.print_on_console('Actual: ',input)
                log.info('Actual:')
                log.info(input)
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            log.error(EXCEPTION_OCCURED)
            log.error(e)
        log.info(RETURN_RESULT)
        return status,methodoutput








