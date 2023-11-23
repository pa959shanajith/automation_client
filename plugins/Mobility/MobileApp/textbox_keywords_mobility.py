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
import action_keywords_app
import readconfig
import web_keywords_MA
log = logging.getLogger('textbox_keywords_mobility.py')

class Textbox_keywords():

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def set_text(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        text=input_val[0]
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:            
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('Setting the text')
                        if len(element.text)>0:
                            log.debug('clearing  the existing text')
                            element.clear()
                        if SYSTEM_OS == 'Darwin': element.set_value(text)
                        elif SYSTEM_OS == 'Windows': element.set_text(text)
                        else:
                            if args[1] == 'saucelabs':
                                action = TouchAction(web_keywords_MA.local_mak.driver)
                                element.set_text(text)
                            else:    
                                action = TouchAction(android_scrapping.local_mak.driver)
                                action.tap(element).perform()
                                text1 = []
                                text1.append(text)
                                obj = action_keywords_app.Action_Key_App()
                                status,methodoutput,output,err_msg = obj.action_key(element,text1)
                        configvalues = readconfig.configvalues
                        hide_soft_key = configvalues['hide_soft_key']
                        if args[1] != 'saucelabs':
                            if  android_scrapping.driver.is_keyboard_shown() and (hide_soft_key == "Yes"):
                                android_scrapping.driver.hide_keyboard()
                        if (text == element.text):
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            try:
                                element_type = element.get_attribute('type')
                            except:
                                element_type = 'None'
                            if 'Secure' in element_type:
                                log.error('Element text can\'t be verified:'+str(element.text))
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error("Error occurred in SetText")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def clear_text(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        if len(element.text)>0:
                            log.debug('clearing  the existing text')
                            element.clear()
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error("Error occurred in ClearText")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def setsecuretext(self,element,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        if len(args)>0 and args[0] != '':
                            visibilityFlag=args[0]
                        input=input[0]
                        log.info(input)
                        if input != '':
                            if len(element.text)>0:
                                log.debug('clearing  the existing text')
                                element.clear()
                            encryption_obj = AESCipher()
                            input_val = encryption_obj.decrypt(input)
                            if SYSTEM_OS != 'Darwin': 
                                element.set_text(input_val)
                                status=TEST_RESULT_PASS
                            else: element.set_value(input_val)
                            configvalues = readconfig.configvalues
                            hide_soft_key = configvalues['hide_soft_key']
                            if android_scrapping.driver.is_keyboard_shown() and (hide_soft_key == "Yes"):
                                android_scrapping.driver.hide_keyboard()
                            if (input_val == element.text):
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                            else:
                                try:
                                    element_type = element.get_attribute('type')
                                except:
                                    element_type = 'None'
                                if 'Secure' in element_type:
                                    log.error('Element text can\'t be verified:'+str(element.text))
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error("Error occurred in SetSecureText")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def send_value(self, element,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            text=input_val[0]
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('Sending the keys')
                        if len(element.text)>0:
                            log.debug('clearing  the existing text')
                            element.clear()
                        if SYSTEM_OS == 'Darwin': element.set_value(text)
                        elif SYSTEM_OS == 'Windows': element.set_text(text)
                        else:
                            action = TouchAction(android_scrapping.driver)
                            action.tap(element).perform()
                            text1 = []
                            text1.append(text)
                            obj = action_keywords_app.Action_Key_App()
                            status,methodoutput,output,err_msg = obj.action_key(element,text1)
                        configvalues = readconfig.configvalues
                        hide_soft_key = configvalues['hide_soft_key']
                        if android_scrapping.driver.is_keyboard_shown() and (hide_soft_key == "Yes"):
                            android_scrapping.driver.hide_keyboard()
                        if (element.text == text):
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            try:
                                element_type = element.get_attribute('type')
                            except:
                                element_type = 'None'
                            if 'Secure' in element_type:
                                log.error('Element text can\'t be verified:'+str(element.text))
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error("Error occurred in SendValue")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def get_text(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            # if type(element) is list:
            #     element=element[0]
            if element is not None:
                if element.is_enabled():
                    log.debug(ELEMENT_ENABLED)
                    output=element.text
                    logger.print_on_console("Element text: "+output)
                    status=TEST_RESULT_PASS
                    result=TEST_RESULT_TRUE
                else:
                    err_msg=self.print_error(ELEMENT_DISABLED)
                    output=element.text
                    logger.print_on_console("Element text: "+output)
                    status=TEST_RESULT_PASS
                    result=TEST_RESULT_TRUE
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error("Error occurred in GetText")
            log.error(e,exc_info=True)
        return status,result,output,err_msg


    def verify_text(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            input_val=input[0]
            if len(input_val)>0 :
                if element is not None:
                    elem_text = element.text
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        if elem_text==input_val:
                            logger.print_on_console("Element text: "+elem_text)
                            log.debug('text matched')
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            logger.print_on_console("Element text: "+elem_text)
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                        if elem_text==input_val:
                            logger.print_on_console("Element text: "+elem_text)
                            log.debug('text matched')
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            logger.print_on_console("Element text: "+elem_text)
                else:
                    err_msg=self.print_error(ELEMENT_NOT_EXIST)
            else:
                err_msg=self.print_error(INVALID_INPUT)
        except Exception as e:
            err_msg=self.print_error("Error occurred in VerifyText")
            log.error(e,exc_info=True)
        return status,result,output,err_msg
