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
from loggermessages import *
import logger
log = logging.getLogger('button_link_keywords_desktop.py')

class ButtonLinkKeyword():
    def double_click(self, element , parent  , *args):
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                log.debug(webelement)
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check == True):
                    log.debug('Parent matched')
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    log.debug('states of element')
                    log.debug(states)
                    if(desktop_constants.ENABLED_CHECK in states):
                       log.info('Element is enabled')
                       flag = ldtp.doubleclick(launch_keywords.window_name,dektop_element[0])
                       log.info(STATUS_METHODOUTPUT_UPDATE)
                       log.debug('status of double click operation')
                       log.debug(flag)
                       status = desktop_constants.TEST_RESULT_PASS
                       result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        log.info('Element state does not allow to perform the operation')
                        err_msg = 'Element state does not allow to perform the operation'
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg = 'element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg

    def click(self, element , parent  , *args):
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
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
                    log.debug('Parent matched')
                    temp_obj = Launch_Keywords()
                    temp_obj.set_to_foreground()
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    log.debug('states of element')
                    log.debug(states)
                    if(desktop_constants.ENABLED_CHECK  in states):
                        log.info('Element is enabled')
                        ldtp.wait()
                        objCoordinates = ldtp.getobjectsize(launch_keywords.window_name,dektop_element[0])
                        xCoordinate = 0;
                        yCoordinate = 0;
                        if((objCoordinates[2]/2)<20):
                            xCoordinate = objCoordinates[0]+(objCoordinates[2]/2)
                        else:
                            xCoordinate = objCoordinates[0]+20
                        yCoordinate = objCoordinates[1] + (objCoordinates[3]/2)
                        ldtp.generatemouseevent(xCoordinate, yCoordinate, 'b1c')
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        log.info('Element state does not allow to perform the operation')
                        err_msg = 'Element state does not allow to perform the operation'
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg = 'element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg

    def verify_button_name(self, element , parent , input, *args):
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
                log.info('input value obtained')
                log.info(input_val)
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check == True):
                    log.debug('Parent matched')
                    label = ldtp.getobjectproperty(launch_keywords.window_name, dektop_element[0],'label')
                    logger.print_on_console('Button name : ' , label)
                    log.info('label obtained')
                    log.info(label)
                    if(label == input_val):
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg = 'element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg

    def get_button_name(self, element , parent , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        label=None
        err_msg = None
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
                    log.debug('Parent matched')
                    label = ldtp.getobjectproperty(launch_keywords.window_name, dektop_element[0],'label')
                    logger.print_on_console('Button name : ' , label)
                    log.info('label obtained')
                    log.info(label)
                    if(label is not None):
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg = 'element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,label,err_msg

    def right_click(self, element , parent , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        label=None
        err_msg = None
        verb = OUTPUT_CONSTANT
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
                    ldtp.mouserightclick(launch_keywords.window_name,dektop_element[0])
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = desktop_constants.TEST_RESULT_PASS
                    result = desktop_constants.TEST_RESULT_TRUE
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg = 'element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg

    def get_link_text(self, element , parent , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        link_text=None
        err_msg = None
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
                    link_text = ldtp.getobjectproperty(launch_keywords.window_name, dektop_element[0],'label')
                    logger.print_on_console('link_text : ' , link_text)
                    log.info('link_text obtained')
                    log.info(link_text)
                    if(link_text is not None):
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg = 'element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,link_text,err_msg

    def verify_link_text(self, element , parent , input, *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        err_msg = None
        verb = OUTPUT_CONSTANT
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                input_val = input[0]
                log.info('input value obtained')
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
                    link_text = ldtp.getobjectproperty(launch_keywords.window_name, dektop_element[0],'label')
                    log.info('link_text obtained')
                    log.info(link_text)
                    if(link_text == input_val):
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg = 'element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg
