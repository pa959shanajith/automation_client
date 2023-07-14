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
import readconfig
import os
import subprocess

log = logging.getLogger('Number_picker_keywords.py')

class Number_Picker():

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def Select_Number(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        input_val=input[0]
        try:
            element = element.find_element_by_class_name("android.widget.EditText")
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        element.set_text(input_val)
                        android_home = os.environ['ANDROID_HOME']
                        if android_home is not None:
                            cmd = android_home + '\\platform-tools\\'
                            os.chdir(cmd)
                            cmd = cmd + 'adb.exe shell input keyevent 61'
                            op = subprocess.check_output(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
                            configvalues = readconfig.configvalues
                            hide_soft_key = configvalues['hide_soft_key']
                            if android_scrapping.driver.is_keyboard_shown() and hide_soft_key == "Yes":
                                android_scrapping.driver.hide_keyboard()
                            if (element.text == input_val):
                                status=TEST_RESULT_PASS
                                result=TEST_RESULT_TRUE
                            else:
                                err_msg=self.print_error("Failed to set the correct value")
                        else:
                            err_msg=self.print_error(NO_ANDROID_HOME)
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg=self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error("Error occurred in SetNumber")
            log.error(e,exc_info=True)
        return status,result,output,err_msg


    def Get_Selected_Number(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=None
        err_msg=None
        try:
            element = element.find_element_by_class_name("android.widget.EditText")
            if element is not None:
                if element.is_enabled():
                    log.debug(ELEMENT_ENABLED)
                    output = element.text
                    logger.print_on_console("Selected number: "+output)
                    status=TEST_RESULT_PASS
                    result=TEST_RESULT_TRUE
                else:
                    err_msg=self.print_error(ELEMENT_DISABLED)
            else:
                err_msg=self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg=self.print_error("Error occurred in GetNumber")
            log.error(e,exc_info=True)
        return status,result,output,err_msg


    def Verify_Selected_Number(self,element,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            element = element.find_element_by_class_name("android.widget.EditText")
            input_val=input[0]
            if len(input_val)>0 :
                if element is not None:
                    elem_text = element.text
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        if elem_text==input_val:
                            log.debug('text matched')
                            logger.print_on_console("Selected number: "+elem_text)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            logger.print_on_console("Selected number: "+elem_text)
                    else:
                        err_msg=self.print_error(ELEMENT_DISABLED)
                        if elem_text==input_val:
                            log.debug('text matched')
                            logger.print_on_console("Selected number: "+elem_text)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            logger.print_on_console("Selected number: ;"+elem_text)
                else:
                    err_msg=self.print_error(ELEMENT_NOT_EXIST)
            else:
                err_msg=self.print_error(INVALID_INPUT)
        except Exception as e:
            err_msg=self.print_error("Error occurred in VerifyNumber")
            log.error(e,exc_info=True)
        return status,result,output,err_msg