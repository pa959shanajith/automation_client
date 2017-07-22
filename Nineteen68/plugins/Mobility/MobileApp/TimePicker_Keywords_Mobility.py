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

class Time_Keywords():

    def Set_Time(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        className=''
        err_msg=None
        text=[]
        obj=[]
        print 'input',input
        input_date=input
        print 'input_date',input_date
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

                        Date_picker=driver.find_elements_by_class_name('android.widget.TimePicker')
                        count= len(Date_picker)

                        if count == 1 :
                                element=driver.find_elements_by_class_name('android.widget.EditText')
                                element[0].set_text(input_date[0])
                                value=element[0].text
                                print 'value1',value
                                print 'input_date[0]',input_date[0]
                                if value != input_date[0] :
                                    print '111'
                                    err_msg='Invalid input'
                                    log.error('Invalid input')
                                    logger.print_on_console(err_msg)
                                else :
                                    print '222'
                                    element[1].set_text(input_date[1])
                                    value=element[1].text
                                    print 'value2',value
                                    print 'input_date[1]',input_date[1]
                                    if value != input_date[1] :
                                        print '333'
                                        err_msg='Invalid input'
                                        log.error('Invalid input')
                                        logger.print_on_console(err_msg)
                                    else :
                                        print '44444'
                                        element[2].set_text(input_date[2])
                                        value=element[2].text
                                        print 'value3',value
                                        print 'input_date[2]',input_date[2]
                                        if value != input_date[2] :
                                            print '5555'
                                            err_msg='Invalid input'
                                            log.error('Invalid input')
                                            logger.print_on_console(err_msg)
                                        else :
                                            print '666'
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

    def Get_Time(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
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

                        Date_picker=driver.find_elements_by_class_name('android.widget.TimePicker')
                        count= len(Date_picker)

                        if count == 1 :
                                element=driver.find_elements_by_class_name('android.widget.EditText')

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

