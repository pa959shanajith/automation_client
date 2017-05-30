#-------------------------------------------------------------------------------
# Name:        button_link_keywords_desktop.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     29/05/2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import desktop_constants
from editable_text import Text_Box
##from launch_keywords import ldtp
import launch_keywords
from launch_keywords import Launch_Keywords
##from ldtp.client_exception import LdtpExecutionError
import logging
from constants import *
import logger
log = logging.getLogger('button_link_keywords_desktop.py')
import pywinauto
class ButtonLinkKeyword():
    def double_click(self, element , parent  , *args):
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check):
                    log.info('Parent matched')
                    if(element.is_enabled):
                        element.ClickInput(button='left', double=True, wheel_dist=0, pressed='')
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        log.info('Element state does not allow to perform the operation')
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg='element not present on the page where operation is trying to be performed'
        except Exception as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg

    def click(self, element , parent  , *args):
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check):
                    log.info('Parent matched')
                    if(element.is_enabled):
                        element.click()
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        log.info('Element state does not allow to perform the operation')
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg='element not present on the page where operation is trying to be performed'
        except Exception as exception:
            log.error(exception)
            logger.print_on_console(exception)
        return status,result,verb,err_msg

    def verify_button_name(self, element , parent , input, *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        verb = OUTPUT_CONSTANT
        err_msg=None
        text = None
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                input_val = input[0]
                log.info('input value obtained')
                log.info(input_val)
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check):
                    log.debug('Parent matched')
                    handle = element.handle
                    text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem=handle,cache_enable=False).name
                    logger.print_on_console('Button name : ' , text)
                    log.info('label obtained')
                    text = str(text)
                    log.info(text)
                    if(text == input_val):
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg = 'element not present on the page where operation is trying to be performed'
        except Exception as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg

    def get_button_name(self, element , parent , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        text=None
        err_msg = None
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check):
                    log.info('Parent matched')
                    if(element.is_enabled):
                        handle = element.handle
                        text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem=handle,cache_enable=False).name
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        log.info('Element state does not allow to perform the operation')
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg='element not present on the page where operation is trying to be performed'
        except Exception as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,text,err_msg

    def right_click(self, element , parent , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        label=None
        err_msg = None
        verb = OUTPUT_CONSTANT
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check):
                    log.info('Parent matched')
                    if(element.is_enabled):
                        element.right_click()
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        log.info('Element state does not allow to perform the operation')
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg='element not present on the page where operation is trying to be performed'
        except Exception as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg

    def get_link_text(self, element , parent , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        text=None
        err_msg = None
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check):
                    log.info('Parent matched')
                    if(element.is_enabled):
                        handle = element.handle
                        text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem=handle,cache_enable=False).name
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        log.info('Element state does not allow to perform the operation')
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg='element not present on the page where operation is trying to be performed'
        except Exception as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,link_text,err_msg

    def verify_link_text(self, element , parent , input, *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        err_msg = None
        verb = OUTPUT_CONSTANT
        text = None
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                input_val = input[0]
                log.info('input value obtained')
                log.info(input_val)
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check):
                    log.debug('Parent matched')
                    handle = element.handle
                    text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem=handle,cache_enable=False).name
                    logger.print_on_console('Button name : ' , text)
                    log.info('label obtained')
                    text = str(text)
                    log.info(text)
                    if(text == input_val):
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg = 'element not present on the page where operation is trying to be performed'
        except Exception as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg
