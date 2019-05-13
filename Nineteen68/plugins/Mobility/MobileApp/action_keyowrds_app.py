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
import platform
if SYSTEM_OS!='Darwin':
    import android_scrapping
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains
import os
import subprocess

class Action_Key_App():

    def action_key(self,webelement,inputs,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        status=None
        device=android_scrapping.device_id

##        print '123456789'
##        print 'device is',device

        try:
            send_values={
            'enter':' shell input keyevent 66',
            'keydown':' shell input keyevent 20',
            'keyup':' shell input keyevent 19',
            'tab' :' shell input keyevent 61',
            'contacts':' shell input keyevent 207',
            'menu':' shell input keyevent 82',
            'home':' shell input keyevent 3',
            'volume_up':' shell input keyevent 24',
            'volume_down':' shell input keyevent 25',
            'back':' shell input keyevent 4',
            'del':' shell input keyevent 67',
            'pageup':' shell input keyevent 92',
            'pagedown':' shell input keyevent 93',
            'movehome':' shell input keyevent 122',
            'moveend':' shell input keyevent 123',
            'recents':' shell input keyevent 187',
            'semicolon':' shell input keyevent 74'
            }
            adb=os.environ['ANDROID_HOME']+"\\platform-tools\\adb.exe"
            if (len(inputs)==1):
                inp_val = inputs[0]
                if device is not None:
                    cmd = adb + ' -s '+ device+' shell input text '+inp_val
                else:
                    cmd = adb +' shell input text '+inp_val
                s = subprocess.check_output(cmd.split())
                time.sleep(1)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            elif(len(inputs)==2):
                inp_val= inputs[0].lower()
                if inp_val in list(send_values.keys()):
                    input=int(inputs[1])
                    if input > 0 :
                        while True:
                            if device is not None:
                                cmd = adb + ' -s '+ device+send_values[inp_val]
                            else:
                                cmd = adb +send_values[inp_val]
                            s = subprocess.check_output(cmd.split())
                            time.sleep(1)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                            input=input-1
                            if input < 1 :
                                break
                    else :
                        logger.print_on_console('Invalid Input; Value 2 cannot be zero or less')
                        status=TEST_RESULT_FAIL
                        methodoutput=TEST_RESULT_FALSE
                else :
                    logger.print_on_console('Invalid Input; not supported')
                    status=TEST_RESULT_FAIL
                    methodoutput=TEST_RESULT_FALSE
            else :
                    logger.print_on_console('Invalid Input; Maximum two inputs Accepted')
                    status=TEST_RESULT_FAIL
                    methodoutput=TEST_RESULT_FALSE



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


