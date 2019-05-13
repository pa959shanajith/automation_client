#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pavan.nayak
#
# Created:     31-05-2017
# Copyright:   (c) pavan.nayak 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from constants import *
from mobile_app_constants import *
import android_scrapping
import logging
import logger

log = logging.getLogger('Number_picker_keywords.py')

class Number_Picker():
    def Select_Number(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        input_date=str(input[0])
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        try:
                            #input_date=int(input_date)
                            webelement.set_text(input_date)
                            if android_scrapping.driver.is_keyboard_shown():
                                android_scrapping.driver.hide_keyboard()
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        except Exception as e:
                            err_msg='Invalid input'
                            log.error(e,exc_info=True)
                            logger.print_on_console(err_msg)
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
        return status,result,output,err_msg

    def Get_Selected_Number(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        output = webelement.text
                        logger.print_on_console("Selected number: "+output)
                        status=TEST_RESULT_PASS
                        result=TEST_RESULT_TRUE
                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:
            log.error(e,exc_info=True)
        return status,result,output,err_msg

    def Verify_Selected_Number(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            input_val=input[0]
            if len(input_val)>0 :
                #if type(webelement) is list:
                #       webelement=webelement[0]
                if webelement is not None:
                    elem_text = webelement.text
                    if webelement.is_enabled():
                        log.debug(WEB_ELEMENT_ENABLED)
                        if elem_text==input_val:
                            log.debug('text matched')
                            logger.print_on_console("Selected number: "+elem_text)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            logger.print_on_console("Selected number: "+elem_text)
                    else:
                        err_msg='ERR_DISABLED_OBJECT'
                        logger.print_on_console(err_msg)
                        if elem_text==input_val:
                            log.debug('text matched')
                            logger.print_on_console("Selected number: "+elem_text)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            logger.print_on_console("Selected number: ;"+elem_text)
        except Exception as e:
                log.error(e,exc_info=True)
                logger.print_on_console(err_msg)
        return status,result,output,err_msg