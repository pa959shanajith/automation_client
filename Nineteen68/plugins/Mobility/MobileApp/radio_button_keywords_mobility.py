#-------------------------------------------------------------------------------
# Name:        module1
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

log = logging.getLogger('radio_button_keywords_mobility.py')

class Radio_Button_Keywords():
    def __init__(self):
        self.status={'radio':'Selected',
                    'checkbox':'Checked'}

    def select_radio_button(self, element,input_val,*args):

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
                        action = TouchAction(install_and_launch.driver)
                        action.tap(element).perform()
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
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def get_status(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=None
        err_msg=None

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
                        import platform
                        if SYSTEM_OS == 'Darwin':
                           classname= webelement.get_attribute("type")
                        else:
                           classname= webelement.get_attribute("className")
                        if 'Switch' in classname:
                            output=webelement.text
                            output=str(output).upper()
                            import platform
                            if SYSTEM_OS == 'Darwin':
                                if output == 'TRUE':
                                    output = 'On'
                                else:
                                    output = "Off"
                        elif 'Radio' in classname:
                            output=webelement.get_attribute("checked")
                            if output=='true':
                                output='Selected'
                            else:
                                output="UnSelected"
                        elif 'CheckBox' in classname:
                            output=webelement.get_attribute("checked")
                            if output=='true':
                                output='Checked'
                            else:
                                output="UnChecked"
                        else :
                            output=webelement.get_attribute("checked")

                        if output!=None:
                            log.info(output)
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
                err_msg='error occured'

        return status,methodoutput,output,err_msg

    def select_checkbox(self, element,input_val,*args):

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
                        action = TouchAction(install_and_launch.driver)
                        action.tap(element).perform()
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
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


    def unselect_checkbox(self, element,input_val,*args):

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
                        action = TouchAction(install_and_launch.driver)
                        action.tap(element).perform()
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
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg
