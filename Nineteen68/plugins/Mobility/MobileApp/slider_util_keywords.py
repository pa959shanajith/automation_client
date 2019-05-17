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
import android_scrapping
import logging
import logger
import time
import mobile_app_dispatcher
import readconfig

log = logging.getLogger('slider_util_keywords.py')

class SliderKeywords():

    def set_slide_value(self, element,input_val,*args):
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
                        element.set_value(input_val[0])
                        methodoutput=TEST_RESULT_TRUE
                        status = TEST_RESULT_PASS
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

    def get_slide_value(self, element,input_val,*args):

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
                        output= x=str(float(element.get_attribute('value').replace('%',''))/100)[:3]
                        logger.print_on_console("Slide value: "+element.text)
                        methodoutput=TEST_RESULT_TRUE
                        status = TEST_RESULT_PASS

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
            else:
                err_msg=ERROR_CODE_DICT['ERR_ELEMENT_NOT_EXISTS']
                log.error(err_msg)
                logger.print_on_console(err_msg)

        except Exception as e:
            err_msg=ANDROID_ERROR
            log.error(e,exc_info = True)
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
                        err_msg=ELEMENT_ENABLED
                        log.error(err_msg)
                        logger.print_on_console(err_msg)
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    log.error(err_msg)
                    logger.print_on_console(err_msg)
            else:
                err_msg=ERROR_CODE_DICT['ERR_ELEMENT_NOT_EXISTS']
                log.error(err_msg)
                logger.print_on_console(err_msg)

        except Exception as e:
            err_msg=ANDROID_ERROR
            log.error(e,exc_info = True)
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
            else:
                err_msg=ERROR_CODE_DICT['ERR_ELEMENT_NOT_EXISTS']
                log.error(err_msg)
                logger.print_on_console(err_msg)

        except Exception as e:
            err_msg=ANDROID_ERROR
            log.error(e,exc_info = True)
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
                if visibility:
                    err_msg=ERROR_CODE_DICT['ERR_OBJECT_VISIBLE']
                    log.error(err_msg)
                    logger.print_on_console(err_msg)
                else:
                    log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
            else:
                err_msg=ERROR_CODE_DICT['ERR_ELEMENT_NOT_EXISTS']
                log.error(err_msg)
                logger.print_on_console(err_msg)

        except Exception as e:
            err_msg=ANDROID_ERROR
            log.error(e,exc_info = True)
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
            log.error(e,exc_info = True)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def verify_does_not_exists(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                err_msg=ERROR_CODE_DICT['ERR_ELEMENT_EXISTS']
                log.error(err_msg)
                logger.print_on_console(err_msg)
            else:
                log.info(ERROR_CODE_DICT['MSG_ELEMENT_NOT_EXISTS'])
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE

        except Exception as e:
            err_msg=ANDROID_ERROR
            log.error(e,exc_info = True)
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
            configvalues = readconfig.configvalues
            timeout= configvalues['timeOut']
##            timeout='120'
            if timeout!=None:
                start_time = time.time()
                while True:
                    element, xpath=dispatcher.getMobileElement(android_scrapping.driver,object_name)
                    later=time.time()
                    if int(later-start_time)>=int(timeout):
                        logger.print_on_console('Delay timeout')
                        break
                    if element is not None:
                        logger.print_on_console('Element Exists')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        break
            else:
                err_msg='Invalid Input'
        except Exception as e:
            err_msg='error occured'
            log.error(e,exc_info = True)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

