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
#from appium.webdriver.common.touch_action import TouchAction
#import install_and_launch
import android_scrapping
import logging
import logger
import  platform
log = logging.getLogger('swipe_keywords.py')
import time

class SliderKeywords():

    def find_coordinates_horizontal(self):
        size=android_scrapping.driver.get_window_size()
        log.debug('Window size is '+str(size))
        startx=(size['width']*0.75)
        endx=(size['width']/4)
        starty=(size['height']/2)
        log.debug(startx,starty,endx)
        return startx,starty,endx

    def find_coordinates_vertical(self):
        size=android_scrapping.driver.get_window_size()
        log.debug('Window size is '+str(size))
        min_y=(size['height']/4)
        max_y=(size['height']*0.75)
        x_Value=(size['width']/2)
        log.debug(x_Value,max_y,min_y)
        return x_Value,max_y,min_y



    def swipe_left(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            startx,starty,endx=self.find_coordinates_horizontal()
            #Swipe from Right to Left
            android_scrapping.driver.swipe(startx, starty, endx, starty, 3000)
            time.sleep(2)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg='Error thrown by android driver'
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
            android_scrapping.driver.swipe(endx, starty, startx, starty, 3000)
            time.sleep(2)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg='Error thrown by android driver'
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
            x_Value,max_y,min_y=self.find_coordinates_vertical()
            #Swipe from down to up
            if SYSTEM_OS == 'Darwin':
                android_scrapping.driver.execute_script('mobile: scroll', {'direction': 'down'})
            else:
                android_scrapping.driver.swipe(x_Value, max_y, x_Value, min_y, 3000)
            time.sleep(2)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            import traceback
            traceback.print_exc()
            err_msg='Error thrown by android driver'
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
            x_Value,max_y,min_y=self.find_coordinates_vertical()
            #Swipe from up to bottom
            android_scrapping.driver.swipe(x_Value, min_y, x_Value, max_y, 3000)
            time.sleep(2)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg='Error thrown by android driver'
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def hide_soft_keyboard(self,obj,inputval,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            startx,starty,endx=self.find_coordinates_vertical()
            #Swipe from up to bottom
            if android_scrapping.driver.is_keyboard_shown():
                android_scrapping.driver.hide_keyboard()
            time.sleep(1)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg='Error thrown by android driver'
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def backPress(self,inputval,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
##            startx,starty,endx=self.find_coordinates_vertical()
            #Swipe from up to bottom
            android_scrapping.driver.keyevent(4)
            time.sleep(2)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg='Error thrown by android driver'
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


