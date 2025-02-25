#-------------------------------------------------------------------------------
# Name:        textbox_operations_MW.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     08-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import selenium
import browser_Keywords_MW
from webconstants_MW import *
from utilweb_operations_MW import UtilWebKeywords
import logger
from encryption_utility import AESCipher
from selenium.common.exceptions import *
import logging
from constants import *
import platform
import readconfig


log = logging.getLogger('textbox_operations_MW.py')

class TextboxKeywords:

    def validate_input(self,webelement,input):
        log.debug('Validating user input for max_length attribute')
        user_input=None
        max_len=self.__gettexbox_length(webelement)
        if not(max_len is None or max_len is ''):
            max_len=int(max_len)
            if len(input) > max_len:
                user_input=input[0:max_len]
        log.debug('user_input is: ')
        log.debug(user_input)
        return user_input

    def set_text(self,webelement,input,*args):
        """
        def : set_text
        purpose : sets the text on the given webelemnt
        param : webelement,input(text to be set)
        return : bool

        """
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    log.debug(WEB_ELEMENT_ENABLED)
                    utilobj=UtilWebKeywords()
                    is_visble=utilobj.is_visible(webelement)
                    if len(args)>0 and args[0] != '':
                        visibilityFlag=args[0]
                    input=input[0]
                    logger.print_on_console(INPUT_IS+input)
                    log.info(INPUT_IS)
                    log.info(input)
                    if input is not None:
                        readonly_value=webelement.get_attribute("readonly")
                        if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                            user_input=self.validate_input(webelement,input)
                            if user_input is not None:
                                input=user_input
                            if not(visibilityFlag and is_visble):
                                self.clear_text(webelement)
                            else:
                                webelement.clear()
                            log.debug('Setting the text')
                            browser_Keywords_MW.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input)
                            # configvalues = readconfig.configvalues
                            # hide_soft_key = configvalues['hide_soft_key']
                            # if browser_Keywords_MW.driver_obj.is_keyboard_shown() and (hide_soft_key == "Yes"):
                            #     browser_Keywords_MW.driver_obj.hide_keyboard()
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            err_msg=ERROR_CODE_DICT['ERR_ELEMENT_IS_READONLY']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
            except InvalidElementStateException as e:
                err_msg=ERROR_CODE_DICT['ERR_INVALID_ELEMENT_STATE_EXCEPTION']
                log.error(e)
            except Exception as e:
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                log.error(e)
            if err_msg is not None:
                logger.print_on_console(err_msg)
                log.error(err_msg)
        return status,methodoutput,output,err_msg

    def send_value(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    log.debug(WEB_ELEMENT_ENABLED)
                    utilobj=UtilWebKeywords()
                    isvisble=utilobj.is_visible(webelement)
                    if len(args)>0 and args[0] != '':
                        visibilityFlag=args[0]
                    input=input[0]
                    logger.print_on_console(INPUT_IS+input)
                    log.info(INPUT_IS)
                    log.info(input)
                    if input is not None:
                        readonly_value=webelement.get_attribute("readonly")
                        if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                            user_input=self.validate_input(webelement,input)
                            if user_input is not None:
                                input=user_input
                            if not(visibilityFlag and isvisble):
                                self.clear_text(webelement)
                                log.debug('Sending the value via part 1')
                                browser_Keywords_MW.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input)
                            else:
                                webelement.clear()
                                if SYSTEM_OS== "Darwin":
                                    log.debug('Sending the value via part 1')
                                    browser_Keywords_MW.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input)
                                else:
                                    log.debug('Sending the value via part 2')
                                    if SYSTEM_OS!= "Darwin":
                                        webelement.send_keys(input)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            err_msg=ERROR_CODE_DICT['ERR_ELEMENT_IS_READONLY']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
            except InvalidElementStateException as e:
                err_msg=ERROR_CODE_DICT['ERR_INVALID_ELEMENT_STATE_EXCEPTION']
            except Exception as e:
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                log.error(e)
            if err_msg is not None:
                logger.print_on_console(err_msg)
                log.error(err_msg)
        return status,methodoutput,output,err_msg

    def __get_text(self,webelement):
        text=''
        text=webelement.get_attribute('value')
        if text is None or text is '':
            text=webelement.get_attribute('placeholder')
        log.debug('Text retruning from __get_text is '+text)
        return text

    def __clear_text(self,webelement):
        log.debug('Clearing the text')
        browser_Keywords_MW.driver_obj.execute_script(CLEAR_TEXT_SCRIPT,webelement)

    def __gettexbox_length(self,webelement):
        log.debug('Get the maxlength of the textbox')
        return webelement.get_attribute('maxlength')


    def get_text(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        text=None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
               text=self.__get_text(webelement)
               status=TEST_RESULT_PASS
               methodoutput=TEST_RESULT_TRUE
            except Exception as e:
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                log.error(err_msg)
                log.error(e)

        logger.print_on_console(METHOD_OUTPUT+str(text))
        return status,methodoutput,text,err_msg

    def verify_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
               text=self.__get_text(webelement)
               log.debug('Text is '+text)
               input=input[0]
               if text==input:
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
               else:
                err_msg='Text mismatched'
                logger.print_on_console(err_msg)
                logger.print_on_console(EXPECTED,input)
                log.info(EXPECTED)
                log.info(input)
                logger.print_on_console(ACTUAL,text)
                log.info(ACTUAL)
                log.info(text)

            except Exception as e:
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                log.error(err_msg)
                log.error(e)
        return status,methodoutput,output,err_msg

    def clear_text(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    log.debug(WEB_ELEMENT_ENABLED)
                    readonly_value=webelement.get_attribute("readonly")
                    if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                        obj=UtilWebKeywords()
                        if obj.is_visible(webelement):
                            webelement.clear()
                            if SYSTEM_OS != "Darwin":
                                from selenium.webdriver.common.keys import Keys
                                webelement.send_keys(Keys.BACK_SPACE)
                        else:
                            self.__clear_text(webelement)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_ELEMENT_IS_READONLY']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
            except InvalidElementStateException as e:
                err_msg=ERROR_CODE_DICT['ERR_INVALID_ELEMENT_STATE_EXCEPTION']
            except Exception as e:
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                log.error(e)
            if err_msg is not None:
                logger.print_on_console(err_msg)
                log.error(err_msg)
        return status,methodoutput,output,err_msg

    def gettextbox_length(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        length=None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                length = self.__gettexbox_length(webelement)
                if length is not None:
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg='Textbox does not have length'
            except Exception as e:
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                log.error(e)
            if err_msg is not None:
                logger.print_on_console(err_msg)
                log.error(err_msg)
        # logger.print_on_console('Textbox length is '+str(length))
        log.info('Textbox length is '+str(length))
        return status,methodoutput,length,err_msg

    def verifytextbox_length(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                length = self.__gettexbox_length(webelement)
                input=input[0]
                logger.print_on_console(INPUT_IS+str(input))
                log.info(INPUT_IS)
                log.info(input)

                if length != None and length != '':
                    if '.' in input:
                        input=input[0:input.find('.')]
                    if length==input:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg='Textbox length mismatched'
                        logger.print_on_console(err_msg)
                        logger.print_on_console(EXPECTED,input)
                        log.info(EXPECTED)
                        log.info(input)
                        logger.print_on_console(ACTUAL,length)
                        log.info(ACTUAL)
                        log.info(length)
                else:
                    err_msg='Textbox length is None or empty'

            except Exception as e:
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                log.error(e)
            if err_msg is not None:
                logger.print_on_console(err_msg)
                log.error(err_msg)    
        return status,methodoutput,output,err_msg

    def setsecuretext(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    log.debug(WEB_ELEMENT_ENABLED)
                    utilobj=UtilWebKeywords()
                    is_visble=utilobj.is_visible(webelement)
                    if len(args)>0 and args[0] != '':
                        visibilityFlag=args[0]
                    input=input[0]
                    logger.print_on_console(INPUT_IS+str(input))
                    log.info(INPUT_IS)
                    log.info(input)
                    if input is not None:
                        readonly_value=webelement.get_attribute("readonly")
                        if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                            if not(visibilityFlag and is_visble):
                                self.clear_text(webelement)
                            else:
                                webelement.clear()
                            encryption_obj = AESCipher()
                            input_val = encryption_obj.decrypt(input)
                            if input_val is not None:
                                user_input=self.validate_input(webelement,input_val)
                                if user_input is not None:
                                    input_val=user_input
                                browser_Keywords_MW.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input_val)
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                            # else:
                            #     err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        else:
                            err_msg=ERROR_CODE_DICT['ERR_ELEMENT_IS_READONLY']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
            except InvalidElementStateException as e:
                err_msg=ERROR_CODE_DICT['ERR_INVALID_ELEMENT_STATE_EXCEPTION']
            except Exception as e:
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                log.error(e)
            if err_msg is not None:
                logger.print_on_console(err_msg)
                log.error(err_msg)
        return status,methodoutput,output,err_msg



    def sendSecureValue(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    log.debug(WEB_ELEMENT_ENABLED)
                    utilobj=UtilWebKeywords()
                    is_visble=utilobj.is_visible(webelement)
                    if len(args)>0 and args[0] != '':
                        visibilityFlag=args[0]
                    input=input[0]
                    logger.print_on_console(INPUT_IS+str(input))
                    log.info(INPUT_IS)
                    log.info(input)
                    if input is not None:
                        readonly_value=webelement.get_attribute("readonly")
                        if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                            encryption_obj = AESCipher()
                            input_val = encryption_obj.decrypt(input)
                            user_input=self.validate_input(webelement,input_val)
                            if user_input is not None:
                                input_val=user_input
                            if not(visibilityFlag and is_visble):
                                self.clear_text(webelement)
                                log.debug('Sending the value via part 1')
                                browser_Keywords_MW.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input_val)
                            else:
                                webelement.clear()
                                if(isinstance(browser_Keywords_MW.driver_obj,selenium.webdriver.Ie) and self.__check_IE_64bit_from_config):
                                    for i in range (0,len(input_val)+1):
                                        browser_Keywords_MW.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input_val[0:i])
                                else:
                                    webelement.send_keys(input_val)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            err_msg=ERROR_CODE_DICT['ERR_ELEMENT_IS_READONLY']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
            except InvalidElementStateException as e:
                err_msg=ERROR_CODE_DICT['ERR_INVALID_ELEMENT_STATE_EXCEPTION']
            except Exception as e:
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                log.error(e)
            if err_msg is not None:
                logger.print_on_console(err_msg)
                log.error(err_msg)
        return status,methodoutput,output,err_msg












