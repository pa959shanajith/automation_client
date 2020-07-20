#-------------------------------------------------------------------------------
# Name:        popup_keywords.py
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
import webconstants
from selenium import webdriver
import browser_Keywords
import logging
from constants import *
import core_utils
import threading
local_pk = threading.local()

class PopupKeywords():
    def __init__(self):
        local_pk.log = logging.getLogger('popup_keywords.py')

    def accept_popup(self,webelement,*args):
        driver = browser_Keywords.local_bk.driver_obj
        local_pk.log.debug('Got the driver object from browser keyword class')
        local_pk.log.debug(driver)
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_pk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            #code to accept the pop up
            local_pk.log.debug('Switching to Alert')
            driver.switch_to.alert.accept()
            logger.print_on_console('Switched to Alert and accepted the alert')
            local_pk.log.info('Switched to Alert and accepted')
            local_pk.log.info(STATUS_METHODOUTPUT_UPDATE)
            status = webconstants.TEST_RESULT_PASS
            methodoutput = webconstants.TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            local_pk.log.error(EXCEPTION_OCCURED)
            err_msg = "EXCEPTION OCCURED"
        local_pk.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def dismiss_popup(self,webelement,*args):
        driver = browser_Keywords.local_bk.driver_obj
        local_pk.log.debug('Got the driver object from browser keyword class')
        local_pk.log.debug(driver)
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_pk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            #code to dismiss the pop up
            local_pk.log.debug('Switching to Alert')
            driver.switch_to.alert.dismiss()
            logger.print_on_console('Switched to Alert and dismissed(closed) the alert')
            local_pk.log.info('Switched to Alert and dismissed(closed) the alert')
            local_pk.log.info(STATUS_METHODOUTPUT_UPDATE)
            status = webconstants.TEST_RESULT_PASS
            methodoutput = webconstants.TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            local_pk.log.error(EXCEPTION_OCCURED)
            err_msg = "EXCEPTION OCCURED"
        local_pk.log.info(RETURN_RESULT)
        return status,methodoutput,output, err_msg

    def get_popup_text(self,webelement,*args):
        driver = browser_Keywords.local_bk.driver_obj
        local_pk.log.debug('Got the driver object from browser keyword class')
        local_pk.log.debug(driver)
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        text = None
        local_pk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            #code to get the pop up text
            local_pk.log.debug('Switching to Alert')
            text = driver.switch_to.alert.text
            logger.print_on_console('Switched to Alert and retrieved the text')
            local_pk.log.info('Switched to Alert and retrieved the text')
            logger.print_on_console('Alert text= ', text)
            local_pk.log.info('Alert text= ',text)
##            local_pk.log.info('Alert text= '+ str( text))
            local_pk.log.info(STATUS_METHODOUTPUT_UPDATE)
            status = webconstants.TEST_RESULT_PASS
            methodoutput = webconstants.TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            local_pk.log.error(EXCEPTION_OCCURED)
            local_pk.log.error(e)
            err_msg = "EXCEPTION OCCURED"
        local_pk.log.info(RETURN_RESULT)
        return status,methodoutput,text,err_msg

    def verify_popup_text(self,webelement,inputs,*args):
        driver = browser_Keywords.local_bk.driver_obj
        local_pk.log.debug('Got the driver object from browser keyword class')
        local_pk.log.debug(driver)
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_pk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            #code to verify the pop up text
            local_pk.log.debug('Switching to Alert')
            text = driver.switch_to.alert.text
            logger.print_on_console('Switched to Alert and retrieved the text')
            local_pk.log.info('Switched to Alert and retrieved the text')
            logger.print_on_console('Alert text : ' , text)
            local_pk.log.info('Alert text= ',text)
##            local_pk.log.info('Alert text= '+ str( text))
            input = inputs[0]
            coreutilsobj=core_utils.CoreUtils()
            input=coreutilsobj.get_UTF_8(input)
            input = input.strip()
            logger.print_on_console('Input text : ' , input)
            local_pk.log.info('Input text= ',input)
##            local_pk.log.info('Input text= '+ str( input))
            if text == input:
                logger.print_on_console('Alert Text matched')
                local_pk.log.info('Alert Text matched')
                local_pk.log.info(STATUS_METHODOUTPUT_UPDATE)
                status = webconstants.TEST_RESULT_PASS
                methodoutput = webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Alert Text mismatched')
                local_pk.log.info('Alert Text mismatched')
                logger.print_on_console('Expected: ',input)
                local_pk.log.info('Expected:')
                local_pk.log.info(input)
                logger.print_on_console('Actual: ',text)
                local_pk.log.info('Actual:')
                local_pk.log.info(text)
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            local_pk.log.error(EXCEPTION_OCCURED)
            err_msg = "EXCEPTION OCCURED"
        local_pk.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def check_if_no_popup_exists(self):
        driver = browser_Keywords.local_bk.driver_obj
        if driver is not None:
            local_pk.log.debug('Got the driver object from browser keyword class')
            local_pk.log.debug(driver)
            try:
                text = driver.switch_to.alert().text
                local_pk.log.debug('Popup exists with text : %s', text)
                return False
            except Exception as e:
                return True
        else:
            return False


