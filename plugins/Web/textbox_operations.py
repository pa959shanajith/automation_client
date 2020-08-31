#-------------------------------------------------------------------------------
# Name:        textbox_operations.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     08-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import selenium
import browser_Keywords
from webconstants import *
from utilweb_operations import UtilWebKeywords
import logger
from encryption_utility import AESCipher
from selenium.common.exceptions import *
import logging
from constants import *
import core_utils
import readconfig
import threading
local_to = threading.local()

class TextboxKeywords:
    def __init__(self):
        local_to.log = logging.getLogger('textbox_operations.py')

    def validate_input(self,webelement,input):
        local_to.log.debug('Validating user input for max_length attribute')
        user_input=None
        max_len=self.__gettexbox_length(webelement)
        if not(max_len is None or max_len is '' or max_len == 'null'):
            max_len=int(float(max_len))
            if len(input) > max_len:
                user_input=input[0:max_len]
        local_to.log.debug('user_input is: ')
        local_to.log.debug(user_input)
        return user_input

    def __read_only(self):
        err_msg=ERROR_CODE_DICT['ERR_ELEMENT_IS_READONLY']
        logger.print_on_console(err_msg)
        local_to.log.error(err_msg)
        return err_msg

    def __element_disabled(self):
        err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
        logger.print_on_console(err_msg)
        local_to.log.error(err_msg)
        return err_msg

    def __invalid_element_state(self,e):
        err_msg=ERROR_CODE_DICT['ERR_INVALID_ELEMENT_STATE_EXCEPTION']
        local_to.log.error(e)
        logger.print_on_console(err_msg)
        return err_msg

    def __web_driver_exception(self,e):
        logger.print_on_console(e)
        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        return err_msg

    def __check_visibility_from_config(self):
        return readconfig.configvalues['ignoreVisibilityCheck'].strip().lower() == "yes"

    def __check_IE_64bit_from_config(self):
        return readconfig.configvalues['bit_64'].strip().lower() == "yes"

    def set_text(self,webelement,input,*args):
        """
        def : set_text
        purpose : sets the text on the given webelemnt
        param : webelement,input(text to be set)
        return : bool

        """
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    local_to.log.debug(WEB_ELEMENT_ENABLED)
                    utilobj=UtilWebKeywords()
                    is_visble=utilobj.is_visible(webelement)
                    input=input[0]
                    coreutilsobj=core_utils.CoreUtils()
                    input=coreutilsobj.get_UTF_8(input)
                    logger.print_on_console(INPUT_IS+input)
                    local_to.log.info(INPUT_IS)
                    local_to.log.info(input)
                    if input is not None:
                        readonly_value=webelement.get_attribute("readonly")
                        if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                            user_input=self.validate_input(webelement,input)
                            if user_input is not None:
                                input=user_input
                            if not(is_visble) and self.__check_visibility_from_config():
                                self.clear_text(webelement)
                            else:
                                webelement.clear()
                            local_to.log.debug('Setting the text')
                            browser_Keywords.local_bk.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            err_msg=self.__read_only()
                else:
                    err_msg=self.__element_disabled()
            except InvalidElementStateException as e:
                err_msg=self.__invalid_element_state(e)

            except Exception as e:
                err_msg=self.__web_driver_exception(e)

        return status,methodoutput,output,err_msg

    def send_value(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    local_to.log.debug(WEB_ELEMENT_ENABLED)
                    utilobj=UtilWebKeywords()
                    isvisble=utilobj.is_visible(webelement)
                    input=input[0]
                    coreutilsobj=core_utils.CoreUtils()
                    input=coreutilsobj.get_UTF_8(input)
                    logger.print_on_console(INPUT_IS+input)
                    local_to.log.info(INPUT_IS)
                    local_to.log.info(input)
                    if input is not None:
                        readonly_value=webelement.get_attribute("readonly")
                        if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                            user_input=self.validate_input(webelement,input)
                            if user_input is not None:
                                input=user_input
                            if not(isvisble) and self.__check_visibility_from_config():
                                try:
                                    self.clear_text(webelement)
                                except Exception as e:
                                    local_to.log.error('Exception in clearing text')
                                    pass
                                local_to.log.debug('Sending the value via part 1')
                                browser_Keywords.local_bk.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input)
                            else:
                                try:
                                    webelement.clear()
                                except Exception as e:
                                    local_to.log.error('Exception in clearing text')
                                    pass
                                if(isinstance(browser_Keywords.local_bk.driver_obj,selenium.webdriver.Ie) and self.__check_IE_64bit_from_config):
                                    input=input+" "
                                    for i in range (0,len(input)+1):
                                        browser_Keywords.local_bk.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input[0:i])
                                    from sendfunction_keys import SendFunctionKeys
                                    obj=SendFunctionKeys()
                                    obj.sendfunction_keys("backspace",*args)
                                else:
                                    webelement.send_keys(input)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            err_msg=self.__read_only()
                else:
                    err_msg=self.__element_disabled()
            except InvalidElementStateException as e:
                err_msg=self.__invalid_element_state(e)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def __get_text(self,webelement):
        text=''
        #get the text using selenium in-built method
        text=webelement.get_attribute('value')
        if text is None or text == '':
            #if failed, use javascript to get the text
            text = browser_Keywords.local_bk.driver_obj.execute_script("""return arguments[0].value""",webelement)
            if text is None or text is '':
                #if failed, use the id to get the text
                id = webelement.get_attribute('id')
                if(id != '' and id is not None):
                    text = browser_Keywords.local_bk.driver_obj.execute_script("return document.getElementById(arguments[0]).value",id)
                    #finally everything failed then return the placeholder
                    if text is None or text is '':
                        text=webelement.get_attribute('placeholder')
        local_to.log.debug('Text returning from __get_text is ')
        local_to.log.debug(text)
        return text

    def __clear_text(self,webelement):
        local_to.log.debug('Clearing the text')
        browser_Keywords.local_bk.driver_obj.execute_script(CLEAR_TEXT_SCRIPT,webelement)

    def __gettexbox_length(self,webelement):
        local_to.log.debug('Get the maxlength of the textbox')
        return webelement.get_attribute('maxlength')


    def get_text(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        text=None
        err_msg=None
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
               text=self.__get_text(webelement)
               status=TEST_RESULT_PASS
               methodoutput=TEST_RESULT_TRUE
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        logger.print_on_console(METHOD_OUTPUT)
        logger.print_on_console(text)
        return status,methodoutput,text,err_msg

    def verify_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
               text=self.__get_text(webelement)
               local_to.log.debug('Text is '+text)
               input=input[0]
               coreutilsobj=core_utils.CoreUtils()
               input=coreutilsobj.get_UTF_8(input)
               if text==input:
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
               else:
                err_msg='Text mismatched'
                logger.print_on_console(err_msg)
                logger.print_on_console(EXPECTED,input)
                local_to.log.info(EXPECTED)
                local_to.log.info(input)
                logger.print_on_console(ACTUAL,text)
                local_to.log.info(ACTUAL)
                local_to.log.info(text)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def clear_text(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    local_to.log.debug(WEB_ELEMENT_ENABLED)
                    readonly_value=webelement.get_attribute("readonly")
                    if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                        obj=UtilWebKeywords()
                        if obj.is_visible(webelement):
                            webelement.clear()
                            from selenium.webdriver.common.keys import Keys
                            webelement.send_keys(Keys.BACK_SPACE)
                        else:
                            self.__clear_text(webelement)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=self.__read_only()
                else:
                    err_msg=self.__element_disabled()
            except InvalidElementStateException as e:
                err_msg=self.__invalid_element_state(e)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def gettextbox_length(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        length=None
        err_msg=None
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                length = self.__gettexbox_length(webelement)
                if length is not None:
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg='Textbox length is '+str(length)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        logger.print_on_console('Textbox length is '+str(length))
        local_to.log.info('Textbox length is '+str(length))
        return status,methodoutput,length,err_msg

    def verifytextbox_length(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                length = self.__gettexbox_length(webelement)
                input=input[0]
                logger.print_on_console(INPUT_IS+str(input))
                local_to.log.info(INPUT_IS)
                local_to.log.info(input)

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
                        local_to.log.info(EXPECTED)
                        local_to.log.info(input)
                        logger.print_on_console(ACTUAL,length)
                        local_to.log.info(ACTUAL)
                        local_to.log.info(length)
                else:
                    err_msg='Textbox length is None or empty'

            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def setsecuretext(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    local_to.log.debug(WEB_ELEMENT_ENABLED)
                    utilobj=UtilWebKeywords()
                    is_visble=utilobj.is_visible(webelement)
                    input=input[0]
                    coreutilsobj=core_utils.CoreUtils()
                    input=coreutilsobj.get_UTF_8(input)
                    logger.print_on_console(INPUT_IS+input)
                    local_to.log.info(INPUT_IS)
                    local_to.log.info(input)
                    if input is not None:
                        readonly_value=webelement.get_attribute("readonly")
                        if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                            if not(is_visble) and self.__check_visibility_from_config():
                                self.clear_text(webelement)
                            else:
                                webelement.clear()
                            encryption_obj = AESCipher()
                            input_val = encryption_obj.decrypt(input)
                            if input_val is not None:
                                user_input=self.validate_input(webelement,input_val)
                                if user_input is not None:
                                    input_val=user_input
                                browser_Keywords.local_bk.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input_val)
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                            else:
                                err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        else:
                            err_msg=self.__read_only()
                else:
                    err_msg=self.__element_disabled()
            except InvalidElementStateException as e:
                err_msg=self.__invalid_element_state(e)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def sendSecureValue(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    local_to.log.debug(WEB_ELEMENT_ENABLED)
                    utilobj=UtilWebKeywords()
                    isvisble=utilobj.is_visible(webelement)
                    input=input[0]
                    coreutilsobj=core_utils.CoreUtils()
                    input=coreutilsobj.get_UTF_8(input)
                    logger.print_on_console(INPUT_IS,input)
                    local_to.log.info(INPUT_IS)
                    local_to.log.info(input)
                    if input is not None:
                        readonly_value=webelement.get_attribute("readonly")
                        if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                            encryption_obj = AESCipher()
                            input_val = encryption_obj.decrypt(input)
                            user_input=self.validate_input(webelement,input_val)
                            if user_input is not None:
                                input_val=user_input
                            if not(isvisble) and self.__check_visibility_from_config():
                                self.clear_text(webelement)
                                local_to.log.debug('Sending the value via part 1')
                                browser_Keywords.local_bk.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input_val)
                            else:
                                webelement.clear()
                                if(isinstance(browser_Keywords.local_bk.driver_obj,selenium.webdriver.Ie) and self.__check_IE_64bit_from_config):
                                    for i in range (0,len(input_val)+1):
                                        browser_Keywords.local_bk.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input_val[0:i])
                                else:
                                    webelement.send_keys(input_val)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            err_msg=self.__read_only()
                else:
                    err_msg=self.__element_disabled()
            except InvalidElementStateException as e:
                err_msg=self.__invalid_element_state(e)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg