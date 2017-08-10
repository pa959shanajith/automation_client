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
import desktop_constants
from encryption_utility import AESCipher
import logger
#----------------------------------------win32 imports
##import win32gui
##import win32process
##import win32con
import win32api
#----------------------------------------win32 imports
import desktop_launch_keywords
import logging
from constants import *
import logger
log = logging.getLogger('desktop_editable_text.py')

class Text_Box:
    def set_text(self , element , parent , input_val ,*args):
        if(len(input_val)>1):
            text = input_val[2]
        else:
            text=input_val[0]
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(desktop_launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
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
                        input_val = text
                        cursor_x,cursor_y = win32api.GetCursorPos()#handling cursor move
                        element.type_keys(input_val,with_spaces = True)
                        win32api.SetCursorPos((cursor_x,cursor_y))#handling cursor move
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
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg


    def set_secure_text(self, element , parent , input_val , *args):
        if(len(input_val)>1):
            text = input_val[2]
        else:
            text=input_val[0]
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(desktop_launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
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
                        input_val = text
                        log.info('Element state is enabled')
                        encryption_obj = AESCipher()
                        input_val_temp = encryption_obj.decrypt(input_val)
                        if input_val_temp is not None:
                            cursor_x,cursor_y = win32api.GetCursorPos()#handling cursor move
                            element.type_keys(input_val_temp,with_spaces = True)
                            win32api.SetCursorPos((cursor_x,cursor_y))#handling cursor move
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
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg

    def get_text(self, element , parent  , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(desktop_launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        output=None
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
                    output = element.text_block()
                    status = desktop_constants.TEST_RESULT_PASS
                    result = desktop_constants.TEST_RESULT_TRUE
                    log.info(STATUS_METHODOUTPUT_UPDATE)

                else:
                   log.info('Element not present on the page where operation is trying to be performed')
                   err_msg='Element not present on the page where operation is trying to be performed'
                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
        except Exception as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,output,err_msg

    def clear_text(self, element , parent, *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(desktop_launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
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
                        cursor_x,cursor_y = win32api.GetCursorPos()#handling cursor move
                        element.type_keys('^a{BACKSPACE}')
                        win32api.SetCursorPos((cursor_x,cursor_y))#handling cursor move
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
        return status,result,verb,err_msg

    def verify_text(self, element , parent , input_val, *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        log.debug('Got window name after launching application')
        log.debug(desktop_launch_keywords.window_name)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if desktop_launch_keywords.window_name!=None:
                log.info('Recieved element from the desktop dispatcher')
                input_val = input_val[0]
                log.info('input value obtained')
                log.info(input_val)
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check):
                    log.debug('Parent matched')
                    text = element.text_block()
                    logger.print_on_console('Text : ' , text)
                    log.info('Text obtained')
                    text = str(text)
                    log.info(text)
                    if(text == input_val):
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE

                else:
                   log.info('Element not present on the page where operation is trying to be performed')
                   err_msg='Element not present on the page where operation is trying to be performed'
                   logger.print_on_console('Element not present on the page where operation is trying to be performed')
        except Exception as exception:
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status,result,verb,err_msg



    def verify_parent(self,element,parent):
        status=False
        try:
            app_uia = desktop_launch_keywords.app_uia
            win = app_uia.top_window()
            real_parent = win.texts()[0]
            if(parent in real_parent ):
                status= True
            else:
                logger.log('verify parent is false')
                status= False

        except Exception as e:
            log.error(e)
##            logger.print_on_console(e)
        desktop_constants.ELEMENT_FOUND=status
        return status


