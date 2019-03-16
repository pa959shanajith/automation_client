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
from encryption_utility import AESCipher
from mobile_app_constants import *
import logging
import logger
import android_scrapping
from appium.webdriver.common.touch_action import TouchAction
import time
import action_keyowrds_app
log = logging.getLogger('textbox_keywords_mobility.py')

class Textbox_keywords():



    def set_text(self, element,input_val,*args):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        text=input_val[0]
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
##            logger.print_on_console(INPUT_IS+text)
##            log.info(INPUT_IS+text)
            if element is not None:
                visibility=element.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=element.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:

                        log.debug('Setting the text')
                        if len(element.text)>0:
                            log.debug('clearing  the existing text')
                            element.clear()
                        element.set_text(text)
                        if android_scrapping.driver.is_keyboard_shown():
                            android_scrapping.driver.hide_keyboard()
                        time.sleep(1)
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
            err_msg=e
            log.error(e)

            logger.print_on_console(err_msg)

        return status,methodoutput,output,err_msg


    def clear_text(self, element,input_val,*args):

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
                        if len(element.text)>0:
                            log.debug('clearing  the existing text')
                            element.clear()
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
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
            import traceback
            traceback.print_exc()
            logger.print_on_console(err_msg)

        return status,methodoutput,output,err_msg


    def setsecuretext(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                if webelement.is_enabled():
                    log.debug(WEB_ELEMENT_ENABLED)
                    is_visble=webelement.is_displayed()
                    if len(args)>0 and args[0] != '':
                        visibilityFlag=args[0]
                    input=input[0]
##                    logger.print_on_console(INPUT_IS+str(input))
##                    log.info(INPUT_IS)
                    log.info(input)
                    if input != '':
                        if len(webelement.text)>0:
                            log.debug('clearing  the existing text')
                            webelement.clear()
                        encryption_obj = AESCipher()
                        input_val = encryption_obj.decrypt(input)
##                            user_input=self.validate_input(webelement,input_val)
##                            if user_input is not None:
##                                input_val=user_input
                        webelement.set_text(input_val)
                        if android_scrapping.driver.is_keyboard_shown():
                            android_scrapping.driver.hide_keyboard()
                        time.sleep(3)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE

                else:
                    err_msg='element is disabled'

        except Exception as e:
            err_msg='exception occured'
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


    def send_value(self, element,input_val,*args):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            text=input_val[0]
##            logger.print_on_console(INPUT_IS+text)
##            log.info(INPUT_IS+text)
            if element is not None:
                visibility=element.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=element.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('Sending the keys')
                        if len(element.text)>0:
                            log.debug('clearing  the existing text')
                            element.clear()
                        action = TouchAction(android_scrapping.driver)
                        action.tap(element).perform()
                        text1 = []
                        text1.append(text)
                        obj = action_keyowrds_app.Action_Key_App()
                        status,methodoutput,output,err_msg = obj.action_key(element,text1)
                        if android_scrapping.driver.is_keyboard_shown():
                            android_scrapping.driver.hide_keyboard()
                        time.sleep(1)
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

    def get_text(self,webelement,input,*args):
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
                    output=webelement.text
                    status=TEST_RESULT_PASS
                    result=TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console(err_msg)
        return status,result,output,err_msg




    def verify_text(self,webelement,input,*args):
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
                    if webelement.is_enabled():
                        log.debug(WEB_ELEMENT_ENABLED)
                        if webelement.text==input_val:
                            log.debug('text matched')
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            logger.print_on_console("Element text:"+webelement.text)
                    else:
                        err_msg='ERR_DISABLED_OBJECT'
                        logger.print_on_console(err_msg)
                        if webelement.text==input_val:
                            log.debug('text matched')
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            logger.print_on_console("Element text:"+webelement.text)
        except Exception as e:
                log.error(e,exc_info=True)
                logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def get_textBoxLength(self,webelement,input,*args):
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
                    output=webelement.get_attribute('maxLength')
                    status=TEST_RESULT_PASS
                    result=TEST_RESULT_TRUE
                else:
                    err_msg='ERR_DISABLED_OBJECT'
                    logger.print_on_console(err_msg)
                    output=webelement.get_attribute('maxLength')
                    status=TEST_RESULT_PASS
                    result=TEST_RESULT_TRUE

        except Exception as e:
                err_msg='This element does not have the length property'
                log.error(e,exc_info=True)
                logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def verify_textBoxLength(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            log.debug('reading the input values')
            input_val=input[0]
            if len(input_val)>0 :
                if type(webelement) is list:
                       webelement=webelement[0]
                if webelement is not None:
                    if webelement.is_enabled():
                        log.debug(WEB_ELEMENT_ENABLED)
                        Len = webelement.get_attribute('maxLength')
                        if Len == int(input_val):
                            log.debug('text matched')
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            logger.print_on_console(str(Len))
                            
                    else:
                        err_msg='ERR_DISABLED_OBJECT'
                        logger.print_on_console(err_msg)
                        Len = webelement.get_attribute('maxLength')
                        if Len == int(input_val):
                            log.debug('text matched')
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            logger.print_on_console(str(Len))
            else:
                log.error('Invalid input')
                err_msg='Invalid input'
        except Exception as e:
                err_msg='This element does not have the length property'
                log.error(e,exc_info=True)
                logger.print_on_console(err_msg)
        return status,result,output,err_msg




