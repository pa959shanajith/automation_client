#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pavan.nayak
#
# Created:     02-02-2017
# Copyright:   (c) pavan.nayak 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


from constants import *
from mobile_app_constants import *
from appium.webdriver.common.touch_action import TouchAction
import logging
import logger
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains
import os
import subprocess



class Action_Key():




    def action_key(self,webelement,inputs,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        status=None

        try:
            adb=os.environ['ANDROID_HOME']+"\\platform-tools\\adb.exe"
            if inputs[0].lower()== 'enter' :
                input=int(inputs[1])
                if input > 0 :
                    while True:
                        cmd = adb +' shell input keyevent 66'
                        s = subprocess.check_output(cmd.split(), creationflags=subprocess.CREATE_NO_WINDOW)
                        time.sleep(1)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        input=input-1
                        if input < 1 :
                            break
                else :
                    logger.print_on_console('Invalid Input')
            elif inputs[0].lower() == 'keydown' :
                input=int(inputs[1])
                if input > 0 :
                    while True:
                        cmd = adb +' shell input keyevent 20'
                        s = subprocess.check_output(cmd.split(), creationflags=subprocess.CREATE_NO_WINDOW)
                        time.sleep(1)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        input=input-1
                        if input < 1 :
                            break
                else :
                    logger.print_on_console('Invalid Input')
            elif inputs[0].lower() == 'keyup' :
                input=int(inputs[1])
                if input > 0 :
                    while True:
                        cmd = adb +' shell input keyevent 19'
                        s = subprocess.check_output(cmd.split(), creationflags=subprocess.CREATE_NO_WINDOW)
                        time.sleep(1)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        input=input-1
                        if input < 1 :
                            break
                else :
                   logger.print_on_console('Invalid Input')
            elif inputs[0].lower() == 'tab' :
                input=int(inputs[1])
                if input > 0 :
                    while True:
##                        actions = ActionChains(android_scrapping.driver)
                        cmd = adb +' shell input keyevent 61'
                        s = subprocess.check_output(cmd.split(), creationflags=subprocess.CREATE_NO_WINDOW)
                        time.sleep(1)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        input=input-1
                        if input < 1 :
                            break
                else :
                    logger.print_on_console('Invalid Input')
            else :
                logger.print_on_console('Invalid Input')



        except Exception as e:
                err_msg='error occured'
                logger.print_on_console('error occured')
                import traceback
                traceback.print_exc()
        return status,methodoutput,output,err_msg



##    def tab_key(self,inputs,*args):
##
##        mobile_server_utilities.cleardata()
##        status=TEST_RESULT_FAIL
####        methodoutput=TEST_RESULT_FALSE
##        value=''
##        try:
####            if type(webelement) is list:
####               webelement=webelement[0]
####            else:
####                webelement=webelement
####            if objectname is not None:
####                xpath_ele=objectname.split(';')
####                element=xpath_ele[2]
##                input=int(inputs[1])
##                if input > 0 :
##                    while True:
##                        actions = ActionChains(mobile_browser_keywords.driver_obj)
##                        result=actions.send_keys(Keys.TAB).perform()
##                        time.sleep(1)
##                        status=TEST_RESULT_PASS
##                        input=input-1
##                        if input < 1 :
##                            break
##
##
##
##                else :
##                    mobile_key_objects.custom_msg.append("ERR_INVALID_INPUT")
####                methodoutput=TEST_RESULT_TRUE
##
##        except Exception as e:
##            mobile_key_objects.custom_msg.append("ERR_WEB_DRIVER")
##            e_type=Exceptions.error(e)
##        mobile_key_objects.keyword_output.append(str(status))
##
##        mobile_key_objects.keyword_output.append(str(value))
##
##    def down_Arrow(self,inputs,*args):
##
##        mobile_server_utilities.cleardata()
##        status=webconstants.TEST_RESULT_FAIL
####        methodoutput=TEST_RESULT_FALSE
##        value=''
##        try:
####            if type(webelement) is list:
####               webelement=webelement[0]
####            else:
####                webelement=webelement
####            if objectname is not None:
####                xpath_ele=objectname.split(';')
####                element=xpath_ele[2]
##                input=int(inputs[1])
##                if input > 0 :
##                    while True:
##                        actions = ActionChains(mobile_browser_keywords.driver_obj)
##                        result=actions.send_keys(Keys.DOWN).perform()
##                        time.sleep(1)
##                        status=webconstants.TEST_RESULT_PASS
##                        input=input-1
##                        if input < 1 :
##                            break
##
##
##
##                else :
##                    mobile_key_objects.custom_msg.append("ERR_INVALID_INPUT")
##                methodoutput=TEST_RESULT_TRUE
##
##        except Exception as e:
##            mobile_key_objects.custom_msg.append("ERR_WEB_DRIVER")
##            e_type=Exceptions.error(e)
##        mobile_key_objects.keyword_output.append(str(status))
##
##        mobile_key_objects.keyword_output.append(str(value))
##
##
##
##    def up_Arrow(self,inputs,*args):
##
##        mobile_server_utilities.cleardata()
##        status=webconstants.TEST_RESULT_FAIL
####        methodoutput=TEST_RESULT_FALSE
##        value=''
##        try:
####            if type(webelement) is list:
####               webelement=webelement[0]
####            else:
####                webelement=webelement
####            if objectname is not None:
####                xpath_ele=objectname.split(';')
####                element=xpath_ele[2]
##                input=int(inputs[1])
##                if input > 0 :
##                    while True:
##                        actions = ActionChains(mobile_browser_keywords.driver_obj)
##                        result=actions.send_keys(Keys.UP).perform()
##                        time.sleep(1)
##                        status=webconstants.TEST_RESULT_PASS
##                        input=input-1
##                        if input < 1 :
##                            break
##
##
##
##                else :
##                    mobile_key_objects.custom_msg.append("ERR_INVALID_INPUT")
##                methodoutput=TEST_RESULT_TRUE
##
##        except Exception as e:
##            mobile_key_objects.custom_msg.append("ERR_WEB_DRIVER")
##            e_type=Exceptions.error(e)
##        mobile_key_objects.keyword_output.append(str(status))
##
##        mobile_key_objects.keyword_output.append(str(value))
##
##
##    def enter_key(self,inputs,*args):
##
##        mobile_server_utilities.cleardata()
##        status=webconstants.TEST_RESULT_FAIL
####        methodoutput=TEST_RESULT_FALSE
##        value=''
##        try:
####            if type(webelement) is list:
####               webelement=webelement[0]
####            else:
####                webelement=webelement
####            if objectname is not None:
####                xpath_ele=objectname.split(';')
####                element=xpath_ele[2]
####                input=input[0]
####                input=input.lower()
##                input=int(inputs[1])
##                if input > 0 :
##                    while True:
##                        actions = ActionChains(mobile_browser_keywords.driver_obj)
##                        result=actions.send_keys(Keys.ENTER).perform()
##                        time.sleep(1)
##                        status=webconstants.TEST_RESULT_PASS
##                        input=input-1
##                        if input < 1 :
##                            break
##
##
##
##                else :
##                    mobile_key_objects.custom_msg.append("ERR_INVALID_INPUT")
####                methodoutput=TEST_RESULT_TRUE
##
##        except Exception as e:
##            mobile_key_objects.custom_msg.append("ERR_WEB_DRIVER")
##            e_type=Exceptions.error(e)
##        mobile_key_objects.keyword_output.append(str(status))
##
##        mobile_key_objects.keyword_output.append(str(value))


