#-------------------------------------------------------------------------------
# Name:        swipe_keywords.py
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     20-01-2017
# Copyright:   (c) prudhvi.gujjuboyina 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from constants import *
from mobile_app_constants import *
from appium.webdriver.common.touch_action import TouchAction
import install_and_launch
import logging
import logger

log = logging.getLogger('swipe_keywords.py')
import time

class SliderKeywords():

    def find_coordinates_horizontal(self):
        size=install_and_launch.driver.get_window_size()
        log.debug('Window size is '+str(size))
        startx=(size['width']*0.70)
        endx=(size['width']*0.30)
        starty=(size['height']/2)
        log.debug(startx,starty,endx)
        return startx,starty,endx

    def find_coordinates_vertical(self):
        size=install_and_launch.driver.get_window_size()
        log.debug('Window size is '+str(size))
        starty=(size['width']*0.80)
        endy=(size['width']*0.20)
        startx=(size['height']/2)
        log.debug(startx,starty,endx)
        return startx,starty,endx



    def swipe_left(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            startx,starty,endx=self.find_coordinates_horizontal()
            #Swipe from Right to Left
            driver.swipe(startx, starty, endx, starty, 3000)
            time.sleep(3)
            status=TEST_RESULT_PASS
            result=TEST_RESULT_TRUE
        except Exception as e:
            err_msg='Error thrown be android driver'
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


    def swipe_right(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            startx,starty,endx=self.find_coordinates_horizontal()
            #Swipe from left to Right
            driver.swipe(endx, starty, startx, starty, 3000);
            time.sleep(3)
            status=TEST_RESULT_PASS
            result=TEST_RESULT_TRUE
        except Exception as e:
            err_msg='Error thrown be android driver'
            log.error(e)
            logger.print_on_console(err_msg)

        return status,methodoutput,output,err_msg


    def swipe_up(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            startx,starty,endx=self.find_coordinates_vertical()
            #Swipe from down to up
            driver.swipe(startx, starty, startx, endy, 3000)
            time.sleep(3)
            status=TEST_RESULT_PASS
            result=TEST_RESULT_TRUE
        except Exception as e:
            err_msg='Error thrown be android driver'
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


    def swipe_down(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            startx,starty,endx=self.find_coordinates_vertical()
            #Swipe from up to bottom
            driver.swipe(startx, endy, startx, starty, 3000)
            time.sleep(3)
            status=TEST_RESULT_PASS
            result=TEST_RESULT_TRUE
        except Exception as e:
            err_msg='Error thrown be android driver'
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


