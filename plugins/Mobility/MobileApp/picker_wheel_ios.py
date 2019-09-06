#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Chethan.singh
#
# Created:     16-06-2017
# Copyright:   (c) Chethan.singh 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from constants import *
from mobile_app_constants import *
import install_and_launch
import logging
import logger

log = logging.getLogger('picker_wheel_ios.py')

class Picker_Wheel_Keywords():
    # def __init__(self):
    #     self.status={'radio':'Selected',
    #                 'checkbox':'Checked'}

    def set_value(self, element,input_val,*args):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                visibility=element.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=element.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        log.info('set value pass',input_val)
                        logger.print_on_console('set value pass')
                        logger.print_on_console(input_val[0])
                        # for set value
                        element.set_value(input_val[0])
                        status = TEST_RESULT_PASS
                        # print element.text
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg='element is disabled'
                        print('element is disabled')
                        log.error('element is disabled')
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)

        except Exception as e:
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


    def get_value(self, element,input_val,*args):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if element is not None:
                visibility=element.is_displayed()
                log.debug('element is visible')
                if visibility:
                    enable=element.is_enabled()
                    log.debug(WEB_ELEMENT_ENABLED)
                    if enable:
                        log.debug('performing the action')
                        # for set value
                        # element.set_value(input_val[0])
                        output=element.text
                        logger.print_on_console("Output: "+output)
                        status = TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg='element is disabled'
                        log.error(err_msg)
                        logger.print_on_console(err_msg)
                else:
                    err_msg='element is not visible'
                    log.error('element is not visible')
                    logger.print_on_console(err_msg)

        except Exception as e:
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg