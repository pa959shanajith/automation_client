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
import android_scrapping
import logging
import logger
import time
import readconfig
import os
import subprocess


log = logging.getLogger('DatePicker_Keywords_Mobility.py')

class Date_Keywords():

    def Set_Date(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        className=''
        err_msg=None
        text=[]
        Tflag=False
        Tflag1=False
        Tflag2=False
        obj=[]
        driver=android_scrapping.driver
        input_date=input[0].split('/')
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        years=[]
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
                        Date_picker=driver.find_elements_by_class_name('android.widget.DatePicker')
                        date_inputs = driver.find_elements_by_id('android:id/numberpicker_input')
                        count1 = len(date_inputs)
                        ViewGroup = driver.find_elements_by_class_name('android.view.ViewGroup')
                        countV = len(ViewGroup)
                        count = len(Date_picker)
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
                            if input_date[2] != '' and int(input_date[2]) <= 2100 and int(input_date[2]) >= 1900:
                                if int(input_date[2]) != int(year) :
                                    year_diff = int(input_date[2]) - int(year)
                                    action.tap(yearEle).perform()
                                    if 6 > year_diff and year_diff > -3 :
                                        years = driver.find_elements_by_class_name('android.widget.TextView')
                                        years = years[2:]
                                        for ele in years:
                                            if int(ele.text) == int(input_date[2]):
                                                action.tap(ele).perform()
                                                break
                                    else:
                                        i = (int(input_date[2]) - int(year)) / 6
                                        if i > 0:
                                            while (i):
                                                action.press(years[8]).moveTo(years[2]).release()
                                                i-=1
                                        else :
                                            while (i):
                                                action.press(years[2]).moveTo(years[8]).release()
                                                i+=1
                                        years = driver.find_elements_by_class_name('android.widget.TextView')
                                        years = years[2:]
                                        for ele in years:
                                            if int(ele.text) == int(input_date[2]):
                                                action.tap(ele).perform()
                                                break
                            else :
                                err_msg='Invalid input'
                                log.error('Invalid input')
                                logger.print_on_console(err_msg)

                            if input_date[0] != '' and str(input_date[0]).lower() in months :
                                if months.index(str(input_date[0]).lower()) != monthInd :
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
                            else :
                                err_msg='Invalid input'
                                log.error('Invalid input')
                                logger.print_on_console(err_msg)

                            if input_date[1] != '' and int(input_date[1]) <= 31 and int(input_date[1]) > 0 :
                                if int(input_date[1]) != date :
                                    daysEle = driver.find_elements_by_class_name('android.view.View')
                                    action.tap(daysEle[int(input_date[1])]).perform()
                            else :
                                err_msg='Invalid input'
                                log.error('Invalid input')
                                logger.print_on_console(err_msg)

                            monthEle = driver.find_element_by_id('android:id/date_picker_header_date')
                            month = monthEle.text
                            date = int(month[9:11])
                            month = month[5:8].lower()
                            yearEle = driver.find_element_by_id('android:id/date_picker_header_year')
                            year = yearEle.text

                            if input_date[0].lower() == month.lower() and int(input_date[1]) == date and int(input_date[2]) == int(year):
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE

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
                                    logger.print_on_console("Do not change the focus area by tapping somewhere, it may cause the step to fail.")
                                    for i in cmds:
                                        op = subprocess.check_output(i)
                                    if (((date_inputs[0].text).lower() == input_date[0].lower()) and (date_inputs[1].text == input_date[1]) and (date_inputs[2].text == input_date[2])):
                                        status=TEST_RESULT_PASS
                                        result=TEST_RESULT_TRUE
                                    else:
                                        err_msg='Error in setting the provided date'
                                        log.error(err_msg)
                                        logger.print_on_console(err_msg)
                                else:
                                    logger.print_on_console('ANDROID_HOME not set in system path')
                            else:
                                err_msg='Invalid input'
                                log.error(err_msg)
                                logger.print_on_console(err_msg)

                        elif count == 1 :
                            if int(input_date[1])>0 or int(input_date[2])>0 :
                                element=driver.find_elements_by_class_name('android.widget.EditText')
                                if input_date[0] !='':
                                    element[0].set_text(input_date[0])
                                    time.sleep(1)
                                    Tflag = True
                                else:
                                    err_msg='Invalid input'
                                    log.error('Invalid input')
                                    logger.print_on_console(err_msg)

                                if input_date[1] !='':
                                    element[1].set_text(input_date[1])
                                    time.sleep(2)
                                    Tflag1 = True
                                else:
                                    err_msg='Invalid input'
                                    log.error('Invalid input')
                                    logger.print_on_console(err_msg)

                                if input_date[2] !='':
                                    element[2].set_text(input_date[2])
                                    time.sleep(3)
                                    Tflag2=True
                                else:
                                    err_msg='Invalid input'
                                    log.error('Invalid input')
                                    logger.print_on_console(err_msg)

                                if Tflag == True and Tflag1 ==True and Tflag2== True:
                                    value0=element[0].text
                                    value1=element[1].text
                                    value2=element[2].text
                                    if value0 != input_date[0]:
                                        element[0].set_text(input_date[0])
                                        time.sleep(3)
                                        value00=element[0].text
                                    if value1 != input_date[1]:
                                        element[1].set_text(input_date[1])
                                        time.sleep(3)
                                        value11=element[1].text
                                    if value2 != input_date[2]:
                                        element[2].set_text(input_date[2])
                                        time.sleep(3)
                                        value22=element[2].text

                                    if value0 == input_date[0] and value1== input_date[1] and value2==input_date[2]:
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE

                                    elif value00 == input_date[0] and value11== input_date[1] and value22==input_date[2]:
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                            else:
                                err_msg='Invalid input'
                                log.error('Invalid input')
                                logger.print_on_console(err_msg)
                        else:
                            err_msg = 'Widget not compatible'
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
        try:
            configvalues = readconfig.configvalues
            hide_soft_key = configvalues['hide_soft_key']
            if driver.is_keyboard_shown() and hide_soft_key == "Yes":
                driver.hide_keyboard()
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error hiding the Soft. keyboard")
        return status,methodoutput,output,err_msg

    def Get_Date(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=None
        # className=''
        err_msg=None
        # text=[]
        # obj=[]
        # input_date=input[0].split('/')
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
                        driver=android_scrapping.driver
                        Date_picker=driver.find_elements_by_class_name('android.widget.DatePicker')
                        count= len(Date_picker)
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
                        elif count == 1 :
                            element=driver.find_elements_by_class_name('android.widget.EditText')
                            Month=element[0].text
                            Date=element[1].text
                            Year=element[2].text
                            output=Month+'/'+Date+'/'+Year
                            logger.print_on_console("Date: "+output)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else :
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

        return status,methodoutput,output,err_msg


    def verify_date(self,webelement,input,*args):
        err_msg=None
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        flag = True
        driver=android_scrapping.driver
        try:
            input_date = input[0].split('/')
            date_inputs = driver.find_elements_by_id('android:id/numberpicker_input')
            if len(input_date) == 3:
                for i in range(3):
                    if (input_date[i] != date_inputs[i].text):
                        flag = False
                        err_msg = 'Verifying date Failed'
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