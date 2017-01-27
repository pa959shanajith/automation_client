#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     23-01-2017
# Copyright:   (c) rakesh.v 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import mobile_constants
from constants import *
import install_and_launch
from appium.webdriver.common.touch_action import TouchAction
import logger
import logging
log = logging.getLogger('list_view_mobility.py')

class ButtonKeywords():
    def getListCount(self, mobile_element,*args):
        status = mobile_constants.TEST_RESULT_FAIL
        methodoutput = mobile_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            print 'getListCount'
            if mobile_element.is_displayed():
                log.info(mobile_constants.ELEMENT_IS_DISPALYED)
                count = mobile_element.find_elements_by_class_name(mobile_constants.CLASS_NAME)
                output = len(count)
                logger.print_on_console('List view count is',output)
                if(len(output) > 0):
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    log.info('Unable to fetch list count')
                    err_msg='Unable to fetch list count'
            else:
                err_msg = mobile_constants.ELEMENT_NOT_DISPALYED
                logger.print_on_console(mobile_constants.ELEMENT_NOT_DISPALYED)

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg



    def selectViewByIndex(self,mobile_element,input_val,*args):
        status = mobile_constants.TEST_RESULT_FAIL
        methodoutput = mobile_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        inner_element = None
        index = None
        try:
            print ' selectViewByIndex'
            if input_val != None and len(input_val) != 0:
                if mobile_element.is_displayed():
                    log.info(mobile_constants.ELEMENT_IS_DISPALYED)
                    input_index = input_val[0]
                    log.info('Input val obtained is :')
                    log.info(input_index)
                    inner_element = mobile_element.find_elements_by_class_name(mobile_constants.CLASS_NAME)
                    log.debug('Count of elements')
                    log.debug(len(inner_element))
                    index = inner_element[input_index]
                    TouchAction(driver).tap(index).perform()
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    err_msg = mobile_constants.ELEMENT_NOT_DISPALYED
                    logger.print_on_console(mobile_constants.ELEMENT_NOT_DISPALYED)
            else:
                logger.print_on_console(mobile_constants.INVALID_INPUT)
                log.info(mobile_constants.INVALID_INPUT)
                err_msg = mobile_constants.INVALID_INPUT
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def GetListValueByIndex(self,mobile_element,input_val,*args):
        status = mobile_constants.TEST_RESULT_FAIL
        methodoutput = mobile_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        inner_element = None
        index = None
        try:
            print 'GetListValueByIndex'
            if input_val != None and len(input_val) != 0:
                if mobile_element.is_displayed():
                    log.info(mobile_constants.ELEMENT_IS_DISPALYED)
                    input_index = input_val[0]
                    log.info('Input val obtained is :')
                    log.info(input_index)
                    inner_element = mobile_element.find_elements_by_class_name(mobile_constants.CLASS_NAME)
                    log.debug('Count of elements')
                    log.debug(len(inner_element))
                    index = inner_element[input_index]


                else:
                    err_msg = mobile_constants.ELEMENT_NOT_DISPALYED
                    logger.print_on_console(mobile_constants.ELEMENT_NOT_DISPALYED)
            else:
                logger.print_on_console(mobile_constants.INVALID_INPUT)
                log.info(mobile_constants.INVALID_INPUT)
                err_msg = mobile_constants.INVALID_INPUT

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=''
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg


