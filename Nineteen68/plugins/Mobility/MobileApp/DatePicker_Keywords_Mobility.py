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
import install_and_launch
import logging
import logger
import time


log = logging.getLogger('button_link_keywords_mobility.py')

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
        input_date=input[0].split('/')
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
                        driver=install_and_launch.driver
                        Date_picker=driver.find_elements_by_class_name('android.widget.DatePicker')
                        count= len(Date_picker)
                        if count == 1 :
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

    def Get_Date(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        className=''
        err_msg=None
        text=[]
        obj=[]
        input_date=input[0].split('/')
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
                        driver=install_and_launch.driver

                        Date_picker=driver.find_elements_by_class_name('android.widget.DatePicker')
                        count= len(Date_picker)

                        if count == 1 :
                                element=driver.find_elements_by_class_name('android.widget.EditText')

                                Month=element[0].text
                                Date=element[1].text
                                Year=element[2].text
                                output=Month+'/'+Date+'/'+Year
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE

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

