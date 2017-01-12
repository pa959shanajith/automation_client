#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     21-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import desktop_constants
from editable_text import Text_Box
from launch_keywords import ldtp
import launch_keywords
from launch_keywords import Launch_Keywords
from ldtp.client_exception import LdtpExecutionError
import logging
from constants import *
import logger
log = logging.getLogger('element_keywords.py')

class ElementKeywords():
    def verify_element_exists(self, element , parent , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check == True):
                    log.info('Parent matched')
                    ldtp.wait()
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    log.debug('state of element')
                    log.debug(states)
                    if(desktop_constants.ENABLED_CHECK in states):
                        log.info('Element state is enabled')
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg='element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg

    def verify_element_doesNot_exists(self, element , parent , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check == True):
                    log.info('Parent matched')
                    ldtp.wait()
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    log.debug('state of element')
                    log.debug(states)
                    if(not(desktop_constants.VISIBLE_CHECK in states)):
                        log.info('Element state is visible')
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg='element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg

    def click_element(self, element , parent  , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check == True):
                    log.info('Parent matched')
                    temp_obj = Launch_Keywords()
                    temp_obj.set_to_foreground()
                    ldtp.wait()
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    log.debug('state of element')
                    log.debug(states)
                    if(desktop_constants.VISIBLE_CHECK  in states):
                        objCoordinates = ldtp.getobjectsize(launch_keywords.window_name,dektop_element[0])
                        xCoordinate = 0;
                        yCoordinate = 0;
                        if((objCoordinates[2]/2)<20):
                            xCoordinate = objCoordinates[0]+(objCoordinates[2]/2)
                        else:
                            xCoordinate = objCoordinates[0]+20
                        yCoordinate = objCoordinates[1] + (objCoordinates[3]/2)
                        ldtp.generatemouseevent(xCoordinate, yCoordinate, 'b1c')
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        log.info('Element state does not allow to perform the operation')
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg='element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg

    def get_element_text(self, element , parent , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        label=None
        err_msg=None
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check == True):
                    log.info('Parent matched')
                    label = ldtp.getobjectproperty(launch_keywords.window_name, dektop_element[0],'label')
                    logger.print_on_console('element text obtained: ' , label)
                    log.info('element text obtained')
                    log.info(label)
                    if(label is not None):
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg='element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,label,err_msg

    def verify_element_text(self, element , parent ,input, *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                input_val = input[0]
                log.info('Input value obtained')
                log.info(input_val)
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check == True):
                    log.info('Parent matched')
                    label = ldtp.getobjectproperty(launch_keywords.window_name, dektop_element[0],'label')
                    logger.print_on_console('element text obtained: ' , label)
                    log.info('element text obtained')
                    log.info(label)
                    if(link_text == input_val):
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg='element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg