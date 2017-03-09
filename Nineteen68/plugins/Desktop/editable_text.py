#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     17-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from launch_keywords import ldtp
import desktop_constants
from encryption_utility import AESCipher
import logger

import launch_keywords
from ldtp.client_exception import LdtpExecutionError
import logging
from constants import *
import logger
log = logging.getLogger('editable_text.py')

class Text_Box:
    def set_text(self , element , parent , input_val ,*args):
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
                input_val = input_val[0]
                log.info('Input value obtained')
                log.info(input_val)
                check = self.verify_parent(dektop_element[0],parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check == True):
                    log.info('Parent matched')
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    log.debug('state of element')
                    log.debug(states)
                    if(desktop_constants.ENABLED_CHECK in states):
                        log.info('Element state is enabled')
                        ldtp.grabfocus(launch_keywords.window_name,dektop_element[0])
                        ldtp.activatetext(launch_keywords.window_name,dektop_element[0])
                        ldtp.settextvalue(launch_keywords.window_name,dektop_element[0], input_val)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        log.log('Element state does not allow to perform the operation')
                        err_msg = 'Element state does not allow to perform the operation'
                else:
                    log.log('element not present on the page where operation is trying to be performed')
                    err_msg = 'element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console('Unable to perform SetText')
            err_msg='Unable to perform SetText'
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg


    def set_secure_text(self, element , parent , input_val , *args):
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
                input_val = input_val[0]
                log.info('Input value obtained')
                log.info(input_val)
                check = self.verify_parent(dektop_element[0],parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check == True):
                    log.info('Parent matched')
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    log.debug('states of element')
                    log.debug(states)
                    if(desktop_constants.ENABLED_CHECK in states):
                        log.info('Element state is enabled')
                        ldtp.grabfocus(launch_keywords.window_name,dektop_element[0])
                        ldtp.activatetext(launch_keywords.window_name,dektop_element[0])
                        encryption_obj = AESCipher()
                        input_val_temp = encryption_obj.decrypt(input_val)
                        if input_val_temp is not None:
                            ldtp.settextvalue(launch_keywords.window_name,dektop_element[0],input_val_temp)
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
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

    def get_text(self, element , parent  , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        output=None
        err_msg=None
        try:
            if launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element.split(';')
                check = self.verify_parent(dektop_element[0],parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check == True):

                    log.info('Parent matched')
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    log.debug('states of element')
                    log.debug(states)
                    if(desktop_constants.ENABLED_CHECK in states):

                        log.info('Element state is enabled')
                        ldtp.grabfocus(launch_keywords.window_name,dektop_element[0])
                        ldtp.activatetext(launch_keywords.window_name,dektop_element[0])
                        output = ldtp.gettextvalue(launch_keywords.window_name,dektop_element[0])
                        logger.print_on_console('Text obtained : ' , output)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:

                        output = ldtp.gettextvalue(launch_keywords.window_name,dektop_element[0])
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg = 'element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            print exception
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,output,err_msg

    def clear_text(self, element , parent, *args):
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
                check = self.verify_parent(dektop_element[0],parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check == True):
                    log.info('Parent matched')
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    log.debug('states of element')
                    log.debug(states)
                    if(desktop_constants.ENABLED_CHECK in states):
                        log.info('Element state is enabled')
                        index = 0
                        ldtp.grabfocus(launch_keywords.window_name,dektop_element[0])
                        ldtp.activatetext(launch_keywords.window_name,dektop_element[0])
                        ldtp.deletetext(launch_keywords.window_name,dektop_element[0],index)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        log.info('Element state does not allow to perform the operation')
                        err_msg = 'Element state does not allow to perform the operation'
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg = 'element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console('Unable to perform ClearText')
            err_msg='Unable to perform ClearText'
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg

    def verify_text(self, element , parent , input_val, *args):
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
                input_val = input_val[0]
                log.info('Input Value obtained')
                log.info(input_val)
                check = self.verify_parent(dektop_element[0],parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check == True):
                    log.info('Parent matched')
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    log.debug('states of element')
                    log.debug(states)
                    if(desktop_constants.ENABLED_CHECK in states):
                        log.info('Element state is enabled')
                        ldtp.grabfocus(launch_keywords.window_name,dektop_element[0])
                        ldtp.activatetext(launch_keywords.window_name,dektop_element[0])
                        output = ldtp.gettextvalue(launch_keywords.window_name,dektop_element[0])
                        log.debug('output from inbuilt call')
                        log.debug(output)
                        if (output == input_val):
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        log.info('Element state does not allow to perform the operation')
                        err_msg = 'Element state does not allow to perform the operation'
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg='element not present on the page where operation is trying to be performed'
        except LdtpExecutionError as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg



    def verify_parent(self,element,parent):
        status=False
        try:
            real_parent=ldtp.getobjectproperty(launch_keywords.window_name,element,'parent')
            parent=parent.strip()
            if(parent == 'pagetitle'):
                parent=launch_keywords.window_name
            if(parent[0:3] == 'dlg'):
                parent = parent.replace('dlg','')
            if(real_parent[0:3] == 'dlg'):
                real_parent = real_parent.replace('dlg','')
            real_parent = real_parent.replace(' ','')
            parent = parent.replace(' ','')
            if(real_parent == parent):
                status= True
            else:
                logger.log('verify parent is false')
                status= False

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        desktop_constants.ELEMENT_FOUND=status
        return status


