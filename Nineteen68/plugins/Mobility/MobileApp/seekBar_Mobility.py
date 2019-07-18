#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pavan.nayak
#
# Created:     25-07-2017
# Copyright:   (c) pavan.nayak 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from constants import *
from mobile_app_constants import *
from appium.webdriver.common.touch_action import TouchAction
import install_and_launch
import android_scrapping
import logging
import logger
import time

log = logging.getLogger('seekBar_Mobility.py')

class Seek_Bar_Keywords():

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def Set_Min_Value(self,element,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        location=element.location
                        size=element.size
                        start_x=location['x'] + (size['width']/2)
                        start_y=location['y'] + (size['height']/2)
                        end_x=location['x'] + 1
                        end_y=location['y'] + (size['height']/2)
                        driver=android_scrapping.driver
                        driver.swipe(start_x,start_y,end_x,end_y,3000)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in SetMinValue")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def Set_Mid_Value(self,element,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            inp=input[0]
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        if (inp != ''):
                            if (inp.isdigit()):
                                inp = int(inp)
                                location=element.location
                                size=element.size
                                start_x=location['x'] + (size['width']/2)
                                start_y=location['y'] + (size['height']/2)
                                if inp <= 0:
                                    end_x=location['x'] + 1
                                elif inp >= 100:
                                    end_x=location['x'] + (size['width'] - 1)
                                else:
                                    end_x=location['x'] + (size['width'] * (inp/100))
                                end_y=start_y
                                driver=android_scrapping.driver
                                driver.swipe(start_x,start_y,end_x,end_y,3000)
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                            else:
                                err_msg = self.print_error(INVALID_INPUT)
                        else:
                            element.click()
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in SetValue")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def Set_Max_Value(self,element,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if element is not None:
                if element.is_displayed():
                    log.debug(ELEMENT_VISIBLE)
                    if element.is_enabled():
                        log.debug(ELEMENT_ENABLED)
                        log.debug('performing the action')
                        location=element.location
                        size=element.size
                        start_x=location['x'] + (size['width']/2)
                        start_y=location['y'] + (size['height']/2)
                        end_x=location['x'] + (size['width'] - 1)
                        end_y=start_y
                        driver=android_scrapping.driver
                        driver.swipe(start_x,start_y,end_x,end_y,3000)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = self.print_error(ELEMENT_DISABLED)
                else:
                    err_msg = self.print_error(ELEMENT_HIDDEN)
            else:
                err_msg = self.print_error(ELEMENT_NOT_EXIST)
        except Exception as e:
            err_msg = self.print_error("Error occurred in SetMaxValue")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg
