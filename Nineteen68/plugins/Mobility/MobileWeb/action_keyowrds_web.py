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
import constants
from mobile_web_constants import *
from appium.webdriver.common.touch_action import TouchAction


import logging
import logger
import platform
if platform.system()!='Darwin':
    import browser_Keywords_MW
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains
import os
import subprocess



class Action_Key_App():




    def action_key(self,webelement,inputs,*args):
        status=constants.TEST_RESULT_FAIL
        methodoutput=constants.TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        status=None
        device=browser_Keywords_MW.device_id
##        print device,'android web'

##        print '123456789'
##        print 'device is',device

        try:
            adb=os.environ['ANDROID_HOME']+"\\platform-tools\\adb.exe"
            if(len(inputs)==2):
                if inputs[0].lower()== 'enter' :
                    input=int(inputs[1])
                    if input > 0 :
                        while True:
                            cmd = adb + ' -s '+ device+' shell input keyevent 66'
                            s = subprocess.check_output(cmd.split())
                            time.sleep(1)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                            input=input-1
                            if input < 1 :
                                break
                    else :
                        logger.print_on_console('Invalid Input')
                        status=constants.TEST_RESULT_FAIL
                        methodoutput=constants.TEST_RESULT_FALSE
                elif inputs[0].lower() == 'keydown' :
                    input=int(inputs[1])
                    if input > 0 :
                        while True:
    ##                               adb -s F7AZFG04V017 shell input keyevent 61
                            cmd = adb + ' -s '+ device +' shell input keyevent 20'
                            s = subprocess.check_output(cmd.split())
                            time.sleep(1)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                            input=input-1
                            if input < 1 :
                                break
                    else :
                        logger.print_on_console('Invalid Input')
                        status=constants.TEST_RESULT_FAIL
                        methodoutput=constants.TEST_RESULT_FALSE
                elif inputs[0].lower() == 'keyup' :
                    input=int(inputs[1])
                    if input > 0 :
                        while True:
                            cmd = adb + ' -s '+ device+' shell input keyevent 19'
                            s = subprocess.check_output(cmd.split())
                            time.sleep(1)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                            input=input-1
                            if input < 1 :
                                break
                    else :
                       logger.print_on_console('Invalid Input')
                       status=constants.TEST_RESULT_FAIL
                       methodoutput=constants.TEST_RESULT_FALSE
                elif inputs[0].lower() == 'tab' :
                    input=int(inputs[1])
                    if input > 0 :
                        while True:
    ##                        actions = ActionChains(install_and_launch.driver)
                            cmd = adb + ' -s '+ device+' shell input keyevent 61'
                            s = subprocess.check_output(cmd.split())
                            time.sleep(1)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                            input=input-1
                            if input < 1 :
                                break
                    else :
                        logger.print_on_console('Invalid Input')
                        status=constants.TEST_RESULT_FAIL
                        methodoutput=constants.TEST_RESULT_FALSE
                else :
                    logger.print_on_console('Invalid Input')
                    status=constants.TEST_RESULT_FAIL
                    methodoutput=constants.TEST_RESULT_FALSE
            else :
                    logger.print_on_console('Invalid Input')
                    status=constants.TEST_RESULT_FAIL
                    methodoutput=constants.TEST_RESULT_FALSE



        except Exception as e:
                err_msg='error occured'
                logger.print_on_console('error occured')
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
##                        actions = ActionChains(browser_Keywords_MW.driver_obj)
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
##        status=webconstants_MW.TEST_RESULT_FAIL
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
##                        actions = ActionChains(browser_Keywords_MW.driver_obj)
##                        result=actions.send_keys(Keys.DOWN).perform()
##                        time.sleep(1)
##                        status=webconstants_MW.TEST_RESULT_PASS
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
##        status=webconstants_MW.TEST_RESULT_FAIL
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
##                        actions = ActionChains(browser_Keywords_MW.driver_obj)
##                        result=actions.send_keys(Keys.UP).perform()
##                        time.sleep(1)
##                        status=webconstants_MW.TEST_RESULT_PASS
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
##        status=webconstants_MW.TEST_RESULT_FAIL
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
##                        actions = ActionChains(browser_Keywords_MW.driver_obj)
##                        result=actions.send_keys(Keys.ENTER).perform()
##                        time.sleep(1)
##                        status=webconstants_MW.TEST_RESULT_PASS
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


