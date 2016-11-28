#-------------------------------------------------------------------------------
# Name:        module1
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
import Exceptions
from encryption_utility import AESCipher
from selenium.common.exceptions import *
class TextboxKeywords:

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
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    utilobj=UtilWebKeywords()
                    is_visble=utilobj.is_visible(webelement)
                    if len(args)>0 and args[0] != '':
                        visibilityFlag=args[0]
                    input=input[0]
                    logger.log('Input is '+input)
                    if input is not None:
                        readonly_value=webelement.get_attribute("readonly")
                        if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                            if not(visibilityFlag and is_visble):
                                self.clear_text(webelement)
                            else:
                                webelement.clear()
                            browser_Keywords.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            logger.log('Element is read only')
                else:
                    logger.log('Element is disabled')
            except InvalidElementStateException as e:
                logger.log('InvalidElementState')

            except Exception as e:
                Exceptions.error(e)

        return status,methodoutput

    def send_value(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    utilobj=UtilWebKeywords()
                    isvisble=utilobj.is_visible(webelement)
                    if len(args)>0 and args[0] != '':
                        visibilityFlag=args[0]
                    input=input[0]
                    logger.log('Input is '+input)
                    if input is not None:
                        max_length=self.__gettexbox_length(webelement)
                        if max_length is not None:
                            input=input[0:max_length]
                        readonly_value=webelement.get_attribute("readonly")
                        if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                            if not(visibilityFlag and isvisble):
                                self.clear_text(webelement)
                                browser_Keywords.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input)
                            else:
                                webelement.clear()
                                webelement.send_keys(input)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            logger.log('Element is read only')
                else:
                    logger.log('Element is disabled')
            except InvalidElementStateException as e:
                logger.log('InvalidElementState')
            except Exception as e:
                Exceptions.error(e)

        return status,methodoutput

    def __get_text(self,webelement):
        text=''
        text=webelement.get_attribute('value')
        if text is None or text is '':
            text=webelement.get_attribute('placeholder')
        return text

    def __clear_text(self,webelement):
        browser_Keywords.driver_obj.execute_script(CLEAR_TEXT_SCRIPT,webelement)

    def __gettexbox_length(self,webelement):
        return webelement.get_attribute('maxlength')


    def get_text(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        text=None
        if webelement is not None:
            try:
                if webelement.is_enabled():
                   text=self.__get_text(webelement)
                   status=TEST_RESULT_PASS
                   methodoutput=TEST_RESULT_TRUE
                else:
                    logger.log('Element is disabled')
            except Exception as e:
                    Exceptions.error(e)
        logger.log('Result is '+text)
        return status,methodoutput,text

    def verify_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        text=None
        if webelement is not None:
            try:
               text=self.__get_text(webelement)
               input=input[0]
               logger.log('Input text is:'+input)
               logger.log('Actual text is:'+text)
               if text==input:
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput

    def clear_text(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        text=None
        if webelement is not None:
            try:
                if webelement.is_enabled():
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
                        logger.log('Element is read only')
                else:
                    logger.log('Element is disabled')
            except InvalidElementStateException as e:
                logger.log('InvalidElementState')
            except Exception as e:
                Exceptions.error(e)
        return status,methodoutput

    def gettextbox_length(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        length=None
        if webelement is not None:
            try:
                length = self.__gettexbox_length(webelement)
                if length is not None:
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
            except Exception as e:
                Exceptions.error(e)
        logger.log('Textbox length is '+str(length))
        return status,methodoutput,length

    def verifytextbox_length(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        length=None
        if webelement is not None:
            try:
                length = self.__gettexbox_length(webelement)
                input=input[0]
                logger.log('Input is:'+input)
                logger.log('Actual length is:'+str(length))
                if not (length is None and length is ''):
                    if length==input:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput

    def setsecuretext(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    utilobj=UtilWebKeywords()
                    is_visble=utilobj.is_visible(webelement)
                    if len(args)>0 and args[0] != '':
                        visibilityFlag=args[0]
                    input=input[0]
                    logger.log('Input is '+input)
                    if input is not None:
                        readonly_value=webelement.get_attribute("readonly")
                        if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                            if not(visibilityFlag and is_visble):
                                self.clear_text(webelement)
                            else:
                                logger.log('Hidden')
                                webelement.clear()
                            encryption_obj = AESCipher()
                            input_val = encryption_obj.decrypt(input)
                            browser_Keywords.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input_val)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            logger.log('Element is read only')
                else:
                    logger.log('Element is disabled')
            except InvalidElementStateException as e:
                logger.log('InvalidElementState')
            except Exception as e:
                Exceptions.error(e)
        return status,methodoutput












