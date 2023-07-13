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
from appium.webdriver.common.touch_action import TouchAction
import android_scrapping
import logging
import logger
import time
import readconfig
import os
import subprocess

log = logging.getLogger('DatePicker_Keywords_Mobility.py')

class Date_Keywords():

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def Set_Date(self,element,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        driver=android_scrapping.driver
        input_date=input[0].split('/')
        input_date[1] = input_date[1][1:] if input_date[1][0]=='0' else input_date[1]
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        action = TouchAction(driver)
                        date_inputs = driver.find_elements_by_id('android:id/numberpicker_input')
                        count1 = len(date_inputs)
                        ViewGroup = driver.find_elements_by_class_name('android.view.ViewGroup')
                        countV = len(ViewGroup)
                        if countV == 1 :
                            monthEle = driver.find_element_by_id('android:id/date_picker_header_date')
                            month = monthEle.text
                            date = int(month[9:11])
                            month = month[5:8].lower()
                            months = ['jan', 'feb', 'mar', 'apr', 'may','jun','jul','aug','sep','oct','nov','dec']
                            monthInd = months.index(month)
                            yearEle = driver.find_element_by_id('android:id/date_picker_header_year')
                            year = yearEle.text
                            prevMonth = driver.find_element_by_id('android:id/prev')
                            nextMonth = driver.find_element_by_id('android:id/next')
                            if (input_date[0]) and (input_date[1]) and (input_date[2]):
                                if (input_date[2].isdigit()) and (input_date[1].isdigit()):
                                    if (str(input_date[0]).lower() in months) \
                                        and (int(input_date[2]) <= 2100) and (int(input_date[2]) >= 1900) \
                                        and  (int(input_date[1]) <= 31) and (int(input_date[1]) > 0):
                                        year_diff = int(input_date[2]) - int(year)
                                        action.tap(yearEle).perform()
                                        android_home = os.environ['ANDROID_HOME']
                                        if android_home is not None:
                                            cmd = android_home + '\\platform-tools\\'
                                            os.chdir(cmd)
                                            cmd = cmd + 'adb.exe'
                                            cmds = [
                                                cmd+' shell input keyevent 19',
                                                cmd+' shell input keyevent 20',
                                                cmd+' shell input keyevent 66'
                                            ]
                                            #logger.print_on_console("Do not change the focus area by tapping somewhere, it may cause the step to fail.")
                                            if (year_diff < 0):
                                                year_diff = abs(year_diff) + 1
                                                while (year_diff):
                                                    op = subprocess.check_output(cmds[0], creationflags=subprocess.CREATE_NO_WINDOW)
                                                    year_diff -= 1
                                                op = subprocess.check_output(cmds[2], creationflags=subprocess.CREATE_NO_WINDOW)
                                            elif (year_diff > 0):
                                                year_diff += 1
                                                while (year_diff):
                                                    op = subprocess.check_output(cmds[1], creationflags=subprocess.CREATE_NO_WINDOW)
                                                    year_diff -= 1
                                                op = subprocess.check_output(cmds[2], creationflags=subprocess.CREATE_NO_WINDOW)
                                            else:
                                                op = subprocess.check_output(cmds[2], creationflags=subprocess.CREATE_NO_WINDOW)
                                                op = subprocess.check_output(cmds[2], creationflags=subprocess.CREATE_NO_WINDOW)
                                            if (months.index(str(input_date[0]).lower()) != monthInd) :
                                                month_diff = months.index(str(input_date[0]).lower()) - monthInd
                                                if month_diff > 0 :
                                                    i = month_diff
                                                    while(i):
                                                        action.tap(nextMonth).perform()
                                                        i-=1
                                                elif month_diff < 0 :
                                                    i = month_diff
                                                    while(i):
                                                        action.tap(prevMonth).perform()
                                                        i+=1
                                            xpath_str = '//android.view.View[@text="'+input_date[1]+'"]'
                                            dayEle = driver.find_element_by_xpath(xpath_str)
                                            action.tap(dayEle).perform()
                                            monthEle = driver.find_element_by_id('android:id/date_picker_header_date')
                                            month = monthEle.text
                                            date = int(month[9:11])
                                            month = month[5:8].lower()
                                            yearEle = driver.find_element_by_id('android:id/date_picker_header_year')
                                            year = yearEle.text
                                            if input_date[0].lower() == month.lower() and int(input_date[1]) == date and int(input_date[2]) == int(year):
                                                status=TEST_RESULT_PASS
                                                methodoutput=TEST_RESULT_TRUE
                                        else:
                                            err_msg = self.print_error(NO_ANDROID_HOME)
                                    else :
                                        err_msg = self.print_error(INVALID_INPUT)
                                else :
                                    err_msg = self.print_error(INVALID_INPUT)
                            else :
                                err_msg = self.print_error(INVALID_INPUT)
                        elif count1 == 3:
                            if (input_date[0] and input_date[1] and input_date[2]):
                                android_home = os.environ['ANDROID_HOME']
                                if android_home is not None:
                                    cmd = android_home + '\\platform-tools\\'
                                    os.chdir(cmd)
                                    cmd = cmd + 'adb.exe'
                                    cmds = [
                                        cmd+' shell input keyevent 61',
                                        cmd+' shell input text '+input_date[0],
                                        cmd+' shell input keyevent 61',
                                        cmd+' shell input keyevent 61',
                                        cmd+' shell input text '+input_date[1],
                                        cmd+' shell input keyevent 61',
                                        cmd+' shell input keyevent 61',
                                        cmd+' shell input text '+input_date[2],
                                        cmd+' shell input keyevent 66',
                                        cmd+' shell input keyevent 61'
                                    ]
                                    #logger.print_on_console("Do not change the focus area by tapping somewhere, it may cause the step to fail.")
                                    for i in cmds:
                                        op = subprocess.check_output(i, creationflags=subprocess.CREATE_NO_WINDOW)
                                    if ((date_inputs[0].text).lower() == input_date[0].lower()) and (date_inputs[1].text == input_date[1]) and (date_inputs[2].text == input_date[2]):
                                        status=TEST_RESULT_PASS
                                        result=TEST_RESULT_TRUE
                                else:
                                    err_msg = self.print_error(NO_ANDROID_HOME)
                            else:
                                err_msg = self.print_error(INVALID_INPUT)
                        else:
                            err_msg = self.print_error(WIDGET_INCOMPATIBLE)
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in SetDate")
            log.error(e,exc_info=True)
        try:
            configvalues = readconfig.configvalues
            hide_soft_key = configvalues['hide_soft_key']
            if driver.is_keyboard_shown() and hide_soft_key == "Yes":
                driver.hide_keyboard()
        except Exception as e:
            self.print_error(SOFT_KEYBOARD_ERROR)
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg

    def Get_Date(self,element,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        driver=android_scrapping.driver
                        date_inputs = driver.find_elements_by_id('android:id/numberpicker_input')
                        count1 = len(date_inputs)
                        ViewGroup = driver.find_elements_by_class_name('android.view.ViewGroup')
                        countV = len(ViewGroup)
                        if countV == 1:
                            Year = driver.find_element_by_id('android:id/date_picker_header_year').text
                            DateText = driver.find_element_by_id('android:id/date_picker_header_date').text
                            Month = DateText[5:8]
                            Date = DateText[9:11]
                            output = Month+'/'+Date+'/'+Year
                            logger.print_on_console("Date: "+output)
                            status = TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                        elif count1 == 3:
                            Month=date_inputs[0].text
                            Date=date_inputs[1].text
                            Year=date_inputs[2].text
                            output=Month+'/'+Date+'/'+Year
                            logger.print_on_console("Date: "+output)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else :
                            err_msg = self.print_error(WIDGET_INCOMPATIBLE)
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in GetDate")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def verify_date(self,element,input,*args):
        err_msg=None
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        flag = True
        driver=android_scrapping.driver
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        input_date = input[0].split('/')
                        if len(input_date) == 3:
                            date_inputs = driver.find_elements_by_id('android:id/numberpicker_input')
                            ViewGroup = driver.find_elements_by_class_name('android.view.ViewGroup')
                            if len(ViewGroup) == 1:
                                Year = driver.find_element_by_id('android:id/date_picker_header_year').text
                                DateText = driver.find_element_by_id('android:id/date_picker_header_date').text
                                Month = DateText[5:8]
                                Date = DateText[9:11]
                                if (input_date[0] == Month and input_date[1] == Date and input_date[2] == Year):
                                    status=TEST_RESULT_PASS
                                    result=TEST_RESULT_TRUE
                            elif len(date_inputs) == 3:
                                for i in range(3):
                                    if (input_date[i] != date_inputs[i].text):
                                        flag = False
                                        break
                                if (flag == True):
                                    status=TEST_RESULT_PASS
                                    result=TEST_RESULT_TRUE
                            else:
                                err_msg = self.print_error(WIDGET_INCOMPATIBLE)
                        else:
                            err_msg = self.print_error(INVALID_INPUT)
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in VerifyDate")
            log.error(e,exc_info=True)
        return status,result,output,err_msg