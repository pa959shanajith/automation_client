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
log = logging.getLogger('action_keywords_app.py')

class Action_Key_App():

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def action_key(self,element,inputs,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        device=android_scrapping.device_id
        try:
            send_values={
            'enter':' shell input keyevent 66',
            'keydown':' shell input keyevent 20',
            'keyup':' shell input keyevent 19',
            'keyleft':' shell input keyevent 21',
            'keyright':' shell input keyevent 22',
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
                inp_val = inputs[0].replace(" ","\ ")
                if device is not None:
                    cmd = adb + ' -s '+ device+' shell input text '+inp_val
                else:
                    cmd = adb +' shell input text '+inp_val
                s = subprocess.check_output(cmd.split(), creationflags=subprocess.CREATE_NO_WINDOW)
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
                            s = subprocess.check_output(cmd.split(), creationflags=subprocess.CREATE_NO_WINDOW)
                            input=input-1
                            if input < 1 :
                                break
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = self.print_error(INVALID_INPUT+': Value 2 cannot be zero or less')
                else:
                    err_msg = self.print_error(INVALID_INPUT+': action not supported')
            else:
                err_msg = self.print_error(INVALID_INPUT+': Maximum two inputs Accepted')
        except Exception as e:
            err_msg = self.print_error("Error occurred in Action Key")
            log.error(e, exc_info=True)
        return status,methodoutput,output,err_msg
