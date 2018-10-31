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
if SYSTEM_OS!='Darwin':
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
            send_values={
            'enter':' shell input keyevent 66',
            'keydown':' shell input keyevent 20',
            'keyup': 'shell input keyevent 19',
            'tab' :' shell input keyevent 61',
            'a':' shell input keyevent 29',
            'b':' shell input keyevent 30',
            'c':' shell input keyevent 31',
            'd':' shell input keyevent 32',
            'e':' shell input keyevent 33',
            'f':' shell input keyevent 34',
            'g':' shell input keyevent 35',
            'h':' shell input keyevent 36',
            'i':' shell input keyevent 37',
            'j':' shell input keyevent 38',
            'k':' shell input keyevent 39',
            'l':' shell input keyevent 40',
            'm':' shell input keyevent 41',
            'n':' shell input keyevent 42',
            'o':' shell input keyevent 43',
            'p':' shell input keyevent 44',
            'q':' shell input keyevent 45',
            'r':' shell input keyevent 46',
            's':' shell input keyevent 47',
            't':' shell input keyevent 48',
            'u':' shell input keyevent 49',
            'v':' shell input keyevent 50',
            'w':' shell input keyevent 51',
            'x':' shell input keyevent 52',
            'y':' shell input keyevent 53',
            'z':' shell input keyevent 54',
            'contacts':' shell input keyevent 207',
            'search':' shell input keyevent 84',
            'menu':' shell input keyevent 82',
            'home':' shell input keyevent 3',
            '0':' shell input keyevent 7',
            '1':' shell input keyevent 8',
            '2':' shell input keyevent 9',
            '3':' shell input keyevent 10',
            '4':' shell input keyevent 11',
            '5':' shell input keyevent 12',
            '6':' shell input keyevent 12',
            '7':' shell input keyevent 14',
            '8':' shell input keyevent 15',
            '9':' shell input keyevent 16',
            'comma':' shell input keyevent 55',
            'space':' shell input keyevent 62',
            'volume_up':' shell input keyevent 24',
            'volume_down':' shell input keyevent 25'
            }
            adb=os.environ['ANDROID_HOME']+"\\platform-tools\\adb.exe"
            if(len(inputs)==2):
                inp_val= inputs[0].lower()
                if inp_val in send_values.keys():
                    input=int(inputs[1])
                    if input > 0 :
                        while True:
                            cmd = adb + ' -s '+ device+send_values[inp_val]
                            s = subprocess.check_output(cmd.split())
                            time.sleep(1)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                            input=input-1
                            if input < 1 :
                                break
                    else:
                        logger.print_on_console('Invalid Input')
                        status=constants.TEST_RESULT_FAIL
                        methodoutput=constants.TEST_RESULT_FALSE
                else:
                    logger.print_on_console('Invalid Input')
                    status=constants.TEST_RESULT_FAIL
                    methodoutput=constants.TEST_RESULT_FALSE
            else:
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


