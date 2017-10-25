#-------------------------------------------------------------------------------
# Name:        radio_checkbox_keywords_desktop.py
# Purpose:     Radio check box operations
#
# Author:      wasimakram.sutar
#
# Created:     09-05-2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import desktop_constants
from desktop_editable_text import Text_Box
import desktop_launch_keywords
from constants import *
import logger
import logging

log = logging.getLogger('radio_checkbox_keywords_desktop.py')
class Radio_Checkbox_keywords():
    def select_radiobutton(self, element , parent  , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if desktop_launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check):
                    log.info('Parent matched')
                    if(element.is_enabled()):
                        state = self.get_status(element,parent)
                        if state[2] == 'Selected':
                            log.info( 'Radio button already selected')
                            err_msg='Radio button already selected'
                            logger.print_on_console('Radio button already selected')

                        else:
                            element.check_by_click()
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                      log.info('Element state does not allow to perform the operation')
                      logger.print_on_console('Element state does not allow to perform the operation')
                      err_msg= 'Element state does not allow to perform the operation'
                else:
                   log.info('Element not present on the page where operation is trying to be performed')
                   err_msg='Element not present on the page where operation is trying to be performed'
                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
        except Exception as exception:
            log.error(exception)
            logger.print_on_console(exception)
            err_msg = desktop_constants.ERROR_MSG
        return status,result,verb,err_msg

    def select_checkbox(self, element , parent  , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if desktop_launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check):
                    log.info('Parent matched')
                    if(element.is_enabled()):
                        state = self.get_status(element,parent)
                        if state[2] == 'Checked':
                            log.info( 'Check box is already checked')
                            err_msg='Check box is already checked'
                            logger.print_on_console('Check box is already checked')
                        else:
                            element.check()
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                      log.info('Element state does not allow to perform the operation')
                      logger.print_on_console('Element state does not allow to perform the operation')
                      err_msg= 'Element state does not allow to perform the operation'
                else:
                   log.info('Element not present on the page where operation is trying to be performed')
                   err_msg='Element not present on the page where operation is trying to be performed'
                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
        except Exception as exception:
            log.error(exception)
            logger.print_on_console(exception)
            err_msg = desktop_constants.ERROR_MSG
        return status,result,verb,err_msg

    def unselect_checkbox(self, element , parent  , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if desktop_launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check):
                    log.info('Parent matched')
                    if(element.is_enabled()):
                        state = self.get_status(element,parent)
                        if state[2] == 'UnChecked':
                            log.info( 'Check box is already unchecked')
                            err_msg='Check box is already unchecked'
                            logger.print_on_console('Check box is already unchecked')
                        else:
                            element.uncheck()
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                      log.info('Element state does not allow to perform the operation')
                      logger.print_on_console('Element state does not allow to perform the operation')
                      err_msg= 'Element state does not allow to perform the operation'
                else:
                   log.info('Element not present on the page where operation is trying to be performed')
                   err_msg='Element not present on the page where operation is trying to be performed'
                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
        except Exception as exception:
            log.error(exception)
            logger.print_on_console(exception)
            err_msg = desktop_constants.ERROR_MSG
        return status,result,verb,err_msg

    def get_status(self, element , parent  , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        flag=None
        err_msg=None
        try:
            if desktop_launch_keywords.window_name!=None:
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                if (check):
                    tag = element.friendly_class_name()
                    status = element.get_check_state()
                    if(tag == 'CheckBox'):
                        if(status == 1):
                            flag = 'Checked'
                            status=desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                        else:
                            flag = 'UnChecked'
                            status=desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                    if(tag == 'RadioButton'):
                        if(status == 1):
                            flag = 'Selected'
                            status=desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                        else:
                            flag = 'UnSelected'
                            status=desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                    elif(tag == 'Button'):
                        flag = status
                        status=desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE

                else:
                   log.info('Element not present on the page where operation is trying to be performed')
                   err_msg='Element not present on the page where operation is trying to be performed'
                   logger.print_on_console('Element not present on the page where operation is trying to be performed')

        except Exception as exception:
            Exceptions.error(exception)
            err_msg = desktop_constants.ERROR_MSG
        return status,result,flag,err_msg
