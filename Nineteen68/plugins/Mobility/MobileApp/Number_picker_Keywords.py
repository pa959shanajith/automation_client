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

class Number_Picker():

    def Select_Number(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        className=''
        err_msg=None
        text=[]
        obj=[]
        input_date=input[0]

        try:

            if webelement is not None:
                visibility=webelement.is_displayed()
                log.debug('element is visible')
                if visibility:

                    enable=webelement.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:

                        log.debug('performing the action')

                        try:

                            inp=int(input_date)

                            webelement.set_text(inp)
                            status=TEST_RESULT_PASS
                            result=TEST_RESULT_TRUE
                        except Exception as e:


                            err_msg='Invalid input'
                            log.error('Invalid input')
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
