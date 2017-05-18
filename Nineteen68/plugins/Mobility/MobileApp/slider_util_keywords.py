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
from appium.webdriver.common.touch_action import TouchAction
import install_and_launch
import logging
import logger
import time
import mobile_app_dispatcher

log = logging.getLogger('slider_util_keywords.py')

class SliderKeywords():


    def verify_enabled(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                visibility=element.is_displayed()
                if visibility:
                    log.debug(ERROR_CODE_DICT['ERR_OBJECT_VISIBLE'])
                    enable=element.is_enabled()
                    if enable:
                        log.info(WEB_ELEMENT_ENABLED)
                        log.debug('performing the action')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=WEB_ELEMENT_DISABLED
                        log.error(err_msg)
                        logger.print_on_console(err_msg)
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    log.error(err_msg)
                    logger.print_on_console(err_msg)

        except Exception as e:
            err_msg=ANDROID_ERROR
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


    def verify_disabled(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                visibility=element.is_displayed()
                if visibility:
                    log.debug(ERROR_CODE_DICT['ERR_OBJECT_VISIBLE'])
                    enable=element.is_enabled()
                    if not(enable):
                        log.info(WEB_ELEMENT_DISABLED)
                        log.debug('performing the action')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=WEB_ELEMENT_ENABLED
                        log.error(err_msg)
                        logger.print_on_console(err_msg)
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    log.error(err_msg)
                    logger.print_on_console(err_msg)

        except Exception as e:
            err_msg=ANDROID_ERROR
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


    def verify_visible(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                visibility=element.is_displayed()
                if visibility:
                    log.info(ERROR_CODE_DICT['ERR_OBJECT_VISIBLE'])
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    log.error(err_msg)
                    logger.print_on_console(err_msg)

        except Exception as e:
            err_msg=ANDROID_ERROR
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def verify_hidden(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                visibility=element.is_displayed()
                if not(visibility):
                    log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_OBJECT_VISIBLE']
                    log.error(err_msg)
                    logger.print_on_console(err_msg)

        except Exception as e:
            err_msg=ANDROID_ERROR
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def verify_exists(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                log.info(ERROR_CODE_DICT['MSG_ELEMENT_EXISTS'])
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE

            else:
                err_msg=ERROR_CODE_DICT['ERR_ELEMENT_NOT_EXISTS']
                log.error(err_msg)
                logger.print_on_console(err_msg)

        except Exception as e:
            err_msg=ANDROID_ERROR
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


    def waitforelement_exists(self, object_name,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            dispatcher=mobile_app_dispatcher.MobileDispatcher()
            timeout='120'
            if timeout!=None:
                start_time = time.time()
                while True:
                    element=dispatcher.getMobileElement(install_and_launch.driver,object_name)
                    later=time.time()
                    if int(later-start_time)>=int(timeout):
                        break
                    if element!=None:
                        logger.print_on_console('Element not found')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        break
            else:
                err_msg='Invalid Input'
        except Exception as e:
            import traceback
            traceback.print_exc()
            err_msg='error occured'
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

