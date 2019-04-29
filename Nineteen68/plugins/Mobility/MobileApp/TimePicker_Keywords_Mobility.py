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
        input_date=input[0].split(':')


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
                        action = TouchAction(driver)
                        Date_picker=driver.find_elements_by_class_name('android.widget.TimePicker')
                        count= len(Date_picker)
                        Date_picker2=driver.find_elements_by_class_name('android.widget.RadialTimePickerView$RadialPickerTouchHelper')
                        count2= len(Date_picker2)

                        if count2 == 12 :
                            if input_date[0] !='':
                                inphr = int(input_date[0]) - 1
                                action.tap(Date_picker2[inphr]).perform()
                                if input_date[1] !='':
                                    if int(input_date[1]) <= 59:
                                        inpmin = int(input_date[1]) / 5
                                        action.tap(Date_picker2[inpmin]).perform()
                                        if input_date[2] !='':
                                            ampm = driver.find_elements_by_class_name('android.widget.RadioButton')
                                            lenAMPM = len(ampm)
                                            if lenAMPM == 2:
                                                if input_date[2] == 'AM':
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


                        elif count == 1:
                            if input_date[0] !='':
                                element=driver.find_elements_by_class_name('android.widget.EditText')
                                element[0].set_text(input_date[0])
                                Tflag = True
                            else:
                                err_msg='Invalid input'
                                log.error('Invalid input')
                                logger.print_on_console(err_msg)

                            if input_date[1] !='':
                                element[1].set_text(input_date[1])
                                value=element[1].text
                                Tflag1 = True
                            else:
                                err_msg='Invalid input'
                                log.error('Invalid input')
                                logger.print_on_console(err_msg)

                            if input_date[2] !='':
                                element[2].set_text(input_date[2])
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
                                if value0 != input_date[0]:
                                    element[0].set_text(input_date[0])
                                    time.sleep(3)
                                    value0=element[0].text
                                if value1 != input_date[1]:
                                    element[1].set_text(input_date[1])
                                    time.sleep(3)
                                    value1=element[1].text
                                if value2 != input_date[2]:
                                    element[2].set_text(input_date[2])
                                    time.sleep(3)
                                    value2=element[2].text

                                if value0 == input_date[0] and value1== input_date[1] and value2==input_date[2]:
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
            log.error(e)
        try:
            if driver.is_keyboard_shown():
                driver.hide_keyboard()
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error hiding the Soft. keyboard")
        return status,result,output,err_msg

    def Get_Time(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        #className=''
        err_msg=None
        #text=[]
        #obj=[]
        #input_date=input[0].split(':')
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
                        driver1=android_scrapping.driver
                        Date_picker=driver1.find_elements_by_class_name('android.widget.TimePicker')
                        count= len(Date_picker)
                        Date_picker2=driver1.find_elements_by_class_name('android.widget.RadialTimePickerView$RadialPickerTouchHelper')
                        count2= len(Date_picker2)
                        if count2 == 12 :
                            element1=driver1.find_elements_by_class_name('android.widget.TextView')
                            AmorPm=driver1.find_elements_by_class_name('android.widget.RadioButton')
                            Hour=element1[0].text
                            Min=element1[2].text
                            if AmorPm[0].get_attribute("checked"):
                                AMorPM="AM"
                            else:
                                AMorPM="PM"
                            output=Hour+':'+Min+':'+AMorPM
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE

                        elif count == 1 :
                            element=driver1.find_elements_by_class_name('android.widget.EditText')
                            Hour=element[0].text
                            Min=element[1].text
                            AMorPM=element[2].text
                            output=Hour+':'+Min+':'+AMorPM
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
        status,result,output,err_msg = self.Get_Time(webelement,None)
        try:
            input_time = input[0].split(':')
            output_time = output.split(':')
            if len(input_time) == 3:
                for i in range(3):
                    if input_time[i] != output_time[i]:
                        output=OUTPUT_CONSTANT
                        status=TEST_RESULT_FAIL
                        result=TEST_RESULT_FALSE
                        err_msg='Verifying time Failed'
                        break
                if output != OUTPUT_CONSTANT:
                    output=OUTPUT_CONSTANT
                    status=TEST_RESULT_PASS
                    result=TEST_RESULT_TRUE
                    err_msg=None
            else:
                output=OUTPUT_CONSTANT
                status=TEST_RESULT_FAIL
                result=TEST_RESULT_FALSE
                err_msg = 'Invalid input'
        except Exception as e:
            logger.print_on_console(err_msg)
            log.error(e,exc_info = True)
        return status,result,output,err_msg