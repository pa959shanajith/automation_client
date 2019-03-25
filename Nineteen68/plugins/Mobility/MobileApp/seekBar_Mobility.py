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

    def Set_Min_Value(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        ##webelement.send_keys('0')
                        location=webelement.location
                        size=webelement.size
                        start_x=location['x'] + (size['width']/2)
                        start_y=location['y'] + (size['height']/2)
                        end_x=location['x'] + 1
                        end_y=location['y'] + (size['height']/2)
                        driver=android_scrapping.driver
                        driver.swipe(start_x,start_y,end_x,end_y,3000)
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

    def Set_Mid_Value(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            inp=input[0]
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        if inp != '':
                            inp = int(inp)
                            location=webelement.location
                            size=webelement.size
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
                        else:
                            webelement.click()
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


    def Set_Max_Value(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        location=webelement.location
                        size=webelement.size
                        start_x=location['x'] + (size['width']/2)
                        start_y=location['y'] + (size['height']/2)
                        end_x=location['x'] + (size['width'] - 1)
                        end_y=start_y
                        driver=android_scrapping.driver
                        driver.swipe(start_x,start_y,end_x,end_y,3000)
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
