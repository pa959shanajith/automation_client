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
from appium.webdriver.common.touch_action import TouchAction
#import install_and_launch
import android_scrapping
import logging
import logger
import time
import readconfig
import subprocess
import os


log = logging.getLogger('Timepicker_Keywords_Mobility.py')

class Time_Keywords():

    def Set_Time(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        #className=''
        err_msg=None
        #text=[]
        #obj=[]
        Tflag=False
        Tflag1 =False
        Tflag2 =False
        input_time=input[0].split(':')
        driver=android_scrapping.driver


        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        action = TouchAction(driver)
                        time_picker=driver.find_elements_by_class_name('android.widget.TimePicker')
                        count = len(time_picker)
                        time_inputs = driver.find_elements_by_id('android:id/numberpicker_input')
                        count1 = len(time_inputs)
                        radial_buttons=driver.find_elements_by_class_name('android.widget.RadialTimePickerView$RadialPickerTouchHelper')
                        count2 = len(radial_buttons)

                        if (count2 == 12):
                            if input_time[0] !='':
                                inphr = int(input_time[0]) - 1
                                action.tap(radial_buttons[inphr]).perform()
                                if input_time[1] !='':
                                    if int(input_time[1]) <= 59:
                                        inpmin = int(input_time[1]) / 5
                                        action.tap(radial_buttons[inpmin]).perform()
                                        if input_time[2] !='':
                                            ampm = driver.find_elements_by_class_name('android.widget.RadioButton')
                                            lenAMPM = len(ampm)
                                            if lenAMPM == 2:
                                                if input_time[2] == 'AM':
                                                    action.tap(ampm[0]).perform()
                                                else:
                                                    action.tap(ampm[1]).perform()
                                            else:
                                                logger.print_on_console("More RadioButtons before Timepicker")
                                            status=TEST_RESULT_PASS
                                            result=TEST_RESULT_TRUE
                                        else:
                                            err_msg='Invalid input'
                                            log.error('Invalid input')
                                            logger.print_on_console(err_msg)
                                    else:
                                        err_msg='Invalid input'
                                        log.error('Invalid input')
                                        logger.print_on_console(err_msg)
                                else:
                                    err_msg='Invalid input'
                                    log.error('Invalid input')
                                    logger.print_on_console(err_msg)
                            else:
                                err_msg='Invalid input'
                                log.error('Invalid input')
                                logger.print_on_console(err_msg)
                        elif (count1 == 3):
                            if (input_time[0] and input_time[1] and input_time[2]):
                                android_home = os.environ['ANDROID_HOME']
                                cmd = android_home + '\\platform-tools\\'
                                os.chdir(cmd)
                                cmd = cmd + 'adb.exe'
                                cmds = [
                                    cmd+' shell input keyevent 61',
                                    cmd+' shell input text '+input_time[0],
                                    cmd+' shell input keyevent 61',
                                    cmd+' shell input keyevent 61',
                                    cmd+' shell input text '+input_time[1],
                                    cmd+' shell input keyevent 61',
                                    cmd+' shell input keyevent 61',
                                    cmd+' shell input keyevent '+('20' if (input_time[2]=='PM') else '19')
                                ]
                                for i in cmds:
                                    op = subprocess.check_output(i)
                                if ((time_inputs[0].text == input_time[0]) and (time_inputs[1].text == input_time[1]) and (time_inputs[2].text == input_time[2])):
                                    status=TEST_RESULT_PASS
                                    result=TEST_RESULT_TRUE
                                else:
                                    err_msg='Error in setting the provided time'
                                    log.error(err_msg)
                                    logger.print_on_console(err_msg)
                            else:
                                err_msg='Invalid input'
                                log.error(err_msg)
                                logger.print_on_console(err_msg)


                        elif (count == 1):
                            if input_time[0] !='':
                                element=driver.find_elements_by_class_name('android.widget.EditText')
                                element[0].set_text(input_time[0])
                                Tflag = True
                            else:
                                err_msg='Invalid input'
                                log.error('Invalid input')
                                logger.print_on_console(err_msg)

                            if input_time[1] !='':
                                element[1].set_text(input_time[1])
                                value=element[1].text
                                Tflag1 = True
                            else:
                                err_msg='Invalid input'
                                log.error('Invalid input')
                                logger.print_on_console(err_msg)

                            if input_time[2] !='':
                                element[2].set_text(input_time[2])
                                value=element[2].text
                                Tflag2 = True
                            else:
                                err_msg='Invalid input'
                                log.error('Invalid input')
                                logger.print_on_console(err_msg)

                            if Tflag == True and Tflag1 ==True and Tflag2== True:
                                value0=element[0].text
                                value1=element[1].text
                                value2=element[2].text
                                if value0 != input_time[0]:
                                    element[0].set_text(input_time[0])
                                    time.sleep(3)
                                    value0=element[0].text
                                if value1 != input_time[1]:
                                    element[1].set_text(input_time[1])
                                    time.sleep(3)
                                    value1=element[1].text
                                if value2 != input_time[2]:
                                    element[2].set_text(input_time[2])
                                    time.sleep(3)
                                    value2=element[2].text

                                if value0 == input_time[0] and value1== input_time[1] and value2==input_time[2]:
                                    status=TEST_RESULT_PASS
                                    result=TEST_RESULT_TRUE
                        else:
                            err_msg='Incompatible element'
                            log.error('Incompatible element')
                            logger.print_on_console(err_msg)
                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
            else:
                err_msg='webelement is None'
                log.error('webelement is None')
                logger.print_on_console(err_msg)
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console(e)
        try:
            configvalues = readconfig.configvalues
            hide_soft_key = configvalues['hide_soft_key']
            if driver.is_keyboard_shown() and (hide_soft_key == "Yes"):
                driver.hide_keyboard()
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console("Error hiding the Soft. keyboard")
        return status,result,output,err_msg

    def Get_Time(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        driver=android_scrapping.driver
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        time_picker=driver.find_elements_by_class_name('android.widget.TimePicker')
                        count = len(time_picker)
                        time_inputs = driver.find_elements_by_id('android:id/numberpicker_input')
                        count1 = len(time_inputs)
                        radial_buttons=driver.find_elements_by_class_name('android.widget.RadialTimePickerView$RadialPickerTouchHelper')
                        count2 = len(radial_buttons)
                        if count2 == 12 :
                            element1=driver.find_elements_by_class_name('android.widget.TextView')
                            AmorPm=driver.find_elements_by_class_name('android.widget.RadioButton')
                            Hour=element1[0].text
                            Min=element1[2].text
                            if AmorPm[0].get_attribute("checked"):
                                AMorPM="AM"
                            else:
                                AMorPM="PM"
                            output=Hour+':'+Min+':'+AMorPM
                            logger.print_on_console("Time: "+output)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE

                        elif count1 == 3:
                            Hour=time_inputs[0].text
                            Min=time_inputs[1].text
                            AMorPM=time_inputs[2].text
                            output=Hour+':'+Min+':'+AMorPM
                            logger.print_on_console("Time: "+output)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE

                        elif count == 1 :
                            element=driver.find_elements_by_class_name('android.widget.EditText')
                            Hour=element[0].text
                            Min=element[1].text
                            AMorPM=element[2].text
                            output=Hour+':'+Min+':'+AMorPM
                            logger.print_on_console("Time: "+output)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                    else:
                        err_msg='element is disabled'
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)
        except Exception as e:
                log.error(e)
        return status,result,output,err_msg

    def verify_time(self,webelement,input,*args):
        err_msg=None
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        flag = True
        driver=android_scrapping.driver
        try:
            input_time = input[0].split(':')
            time_inputs = driver.find_elements_by_id('android:id/numberpicker_input')
            if (len(input_time) == 3) and (len(time_inputs) == 3):
                for i in range(3):
                    if (input_time[i] != time_inputs[i].text):
                        flag = False
                        err_msg='Verify time Failed'
                        log.error(err_msg)
                        logger.print_on_console(err_msg)
                        break
                if (flag == True):
                    status=TEST_RESULT_PASS
                    result=TEST_RESULT_TRUE
            else:
                err_msg = 'Invalid input/object'
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            log.error(e)
        return status,result,output,err_msg