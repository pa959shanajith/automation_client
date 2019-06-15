#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pavan.nayak, veeresh.koti
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
        err_msg=None
        input_time=input[0].split(':')
        driver=android_scrapping.driver
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                if webelement.is_displayed():
                    log.debug('element is visible')
                    if webelement.is_enabled():
                        log.debug(WEB_ELEMENT_ENABLED)
                        log.debug('performing the action')
                        time_picker=driver.find_elements_by_class_name('android.widget.TimePicker')
                        count = len(time_picker)
                        time_inputs = driver.find_elements_by_id('android:id/numberpicker_input')
                        count1 = len(time_inputs)
                        radial_buttons=driver.find_elements_by_class_name('android.widget.RadialTimePickerView$RadialPickerTouchHelper')
                        count2 = len(radial_buttons)
                        hr=input_time[0]
                        mn=input_time[1]
                        if (count2 == 12):
                            if (hr and mn and input_time[2]):
                                ampm = input_time[2].lower()
                                if (0 <= int(hr) <= 12) and (0 <= int(mn) < 60) and (ampm in ['am','pm']):
                                    android_home = os.environ['ANDROID_HOME']
                                    if android_home is not None:
                                        cmd = android_home + '\\platform-tools\\'
                                        os.chdir(cmd)
                                        cmd = cmd + 'adb.exe'
                                        cmds = [
                                            cmd+' shell input text '+str(hr),
                                            cmd+' shell input text '+str(mn),
                                            cmd+' shell input keyevent 61',
                                            cmd+' shell input keyevent 66'
                                        ]
                                        logger.print_on_console("Do not change the focus area by tapping somewhere, it may cause the step to fail.")
                                        subprocess.check_output(cmds[2])
                                        subprocess.check_output(cmds[0])
                                        if (str(hr) == '1'):
                                            subprocess.check_output(cmds[2])
                                        subprocess.check_output(cmds[1])
                                        subprocess.check_output(cmds[2])
                                        if (ampm == 'pm'):
                                            subprocess.check_output(cmds[2])
                                        subprocess.check_output(cmds[3])
                                        element1=driver.find_elements_by_class_name('android.widget.TextView')
                                        AmorPm=driver.find_elements_by_class_name('android.widget.RadioButton')
                                        Hour=element1[0].text
                                        Min=element1[2].text
                                        AMorPM= "am" if (AmorPm[0].get_attribute("checked")=='true') else "pm"
                                        if (Hour == hr) and (Min == mn) and (AMorPM == ampm):
                                            status=TEST_RESULT_PASS
                                            result=TEST_RESULT_TRUE
                                    else:
                                        logger.print_on_console('ANDROID_HOME not set in system path')
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
                                if android_home is not None:
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
                                        cmd+' shell input keyevent '+('20' if (input_time[2].lower()=='pm') else '19'),
                                        cmd+' shell input keyevent 66',
                                        cmd+' shell input keyevent 61'
                                    ]
                                    logger.print_on_console("Do not change the focus area by tapping somewhere, it may cause the step to fail.")
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
                                    logger.print_on_console('ANDROID_HOME not set in system path')
                            else:
                                err_msg='Invalid input'
                                log.error(err_msg)
                                logger.print_on_console(err_msg)
                        else:
                            err_msg='Widget not compatible'
                            log.error('Widget not compatible')
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
        output=None
        err_msg=None
        driver=android_scrapping.driver
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                if webelement.is_displayed():
                    log.debug('element is visible')
                    if webelement.is_enabled():
                        log.debug(WEB_ELEMENT_ENABLED)
                        log.debug('performing the action')
                        time_inputs = driver.find_elements_by_id('android:id/numberpicker_input')
                        radial_buttons=driver.find_elements_by_class_name('android.widget.RadialTimePickerView$RadialPickerTouchHelper')
                        if len(radial_buttons) == 12 :
                            element1=driver.find_elements_by_class_name('android.widget.TextView')
                            AmorPm=driver.find_elements_by_class_name('android.widget.RadioButton')
                            Hour=element1[0].text
                            Min=element1[2].text
                            AMorPM= "AM" if (AmorPm[0].get_attribute("checked")=='true') else "PM"
                            output=Hour+':'+Min+':'+AMorPM
                            logger.print_on_console("Time: "+output)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        elif len(time_inputs) == 3:
                            Hour=time_inputs[0].text
                            Min=time_inputs[1].text
                            AMorPM=time_inputs[2].text
                            output=Hour+':'+Min+':'+AMorPM
                            logger.print_on_console("Time: "+output)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        else:
                            err_msg='Widget not compatible'
                            log.error('Widget not compatible')
                            logger.print_on_console(err_msg)
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
            if webelement is not None:
                if webelement.is_displayed():
                    log.debug('element is visible')
                    if webelement.is_enabled():
                        log.debug(WEB_ELEMENT_ENABLED)
                        input_time = input[0].split(':')
                        if len(input_time) == 3:
                            time_inputs = driver.find_elements_by_id('android:id/numberpicker_input')
                            radial_buttons=driver.find_elements_by_class_name('android.widget.RadialTimePickerView$RadialPickerTouchHelper')
                            if len(radial_buttons) == 12 :
                                element1=driver.find_elements_by_class_name('android.widget.TextView')
                                AmorPm=driver.find_elements_by_class_name('android.widget.RadioButton')
                                Hour=element1[0].text
                                Min=element1[2].text
                                AMorPM= "am" if (AmorPm[0].get_attribute("checked")=='true') else "pm"
                                if (input_time[0] == Hour and input_time[1] == Min and input_time[2].lower() == AMorPM):
                                    status=TEST_RESULT_PASS
                                    result=TEST_RESULT_TRUE
                            elif len(time_inputs) == 3:
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
                                err_msg = 'Invalid object'
                                log.error(err_msg)
                                logger.print_on_console(err_msg)
                        else:
                            err_msg = 'Invalid input'
                            log.error(err_msg)
                            logger.print_on_console(err_msg)
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