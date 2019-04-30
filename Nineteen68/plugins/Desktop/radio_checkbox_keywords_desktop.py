#-------------------------------------------------------------------------------
# Name:        radio_checkbox_keywords_desktop.py
# Purpose:     Radio button/check box operations
#
# Author:      wasimakram.sutar,anas.ahmed
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
    def select_radiobutton(self,element ,parent ,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if ( desktop_launch_keywords.window_name!=None ):
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if ( check ):
                    log.info('Parent matched')
                    if( element.is_enabled() ):
                        state = self.get_status(element,parent)
                        if ( state[2] == 'Selected' ):
                            err_msg='Radio button already selected'
                        else:
                            if ( element.backend.name=='win32' ):
                                element.check_by_click()
                            elif ( element.backend.name=='uia' ):
                                element.select()
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        err_msg= 'Element state does not allow to perform the operation'
                else:
                    err_msg='Element not present on the page where operation is trying to be performed'
            if ( err_msg!=None ):
                log.info( err_msg )
                log.error( err_msg )
                logger.print_on_console( err_msg )
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG
            logger.print_on_console( err_msg )
            log.error( exception )
        return status,result,verb,err_msg

    def select_checkbox(self,element ,parent ,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if ( desktop_launch_keywords.window_name!=None ):
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if ( check ):
                    log.info('Parent matched')
                    if( element.is_enabled() ):
                        state = self.get_status(element,parent)
                        if ( state[2] == 'Checked' ):
                            err_msg='Check box is already checked'
                        else:
                            if ( element.backend.name=='win32' ):
                                element.check()
                            elif ( element.backend.name=='uia' ):
                                element.toggle()
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        err_msg= 'Element state does not allow to perform the operation'
                else:
                    err_msg='Element not present on the page where operation is trying to be performed'
            if ( err_msg!=None ):
                log.info( err_msg )
                log.error( err_msg )
                logger.print_on_console( err_msg )
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG
            logger.print_on_console( err_msg )
            log.error( exception )
        return status,result,verb,err_msg

    def unselect_checkbox(self,element ,parent ,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if ( desktop_launch_keywords.window_name!=None ):
                log.info('Recieved element from the desktop dispatcher')
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if ( check ):
                    log.info('Parent matched')
                    if( element.is_enabled() ):
                        state = self.get_status(element,parent)
                        if ( state[2] == 'UnChecked' ):
                            err_msg='Check box is already unchecked'
                        else:
                            if ( element.backend.name=='win32' ):
                                element.uncheck()
                            elif ( element.backend.name=='uia' ):
                                element.toggle()
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        err_msg= 'Element state does not allow to perform the operation'
                else:
                    err_msg='Element not present on the page where operation is trying to be performed'
            if ( err_msg!=None ):
                log.info( err_msg )
                log.error( err_msg )
                logger.print_on_console( err_msg )
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG
            logger.print_on_console( err_msg )
            log.error( exception )
        return status,result,verb,err_msg

    def get_status(self,element ,parent ,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        flag=None
        err_msg=None
        try:
            if ( desktop_launch_keywords.window_name!=None ):
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                if ( check ):
                    tag = element.friendly_class_name()
                    if ( element.backend.name=='uia' ):
                        if ( tag=='RadioButton' ):
                            status = element.is_selected()
                        elif ( tag=='CheckBox' ):
                            status = element.get_toggle_state()
                    else:
                        status = element.get_check_state()
                    if( tag == 'CheckBox' ):
                        if( status == 1 ):
                            flag = 'Checked'
                            status=desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                        else:
                            flag = 'UnChecked'
                            status=desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                    if( tag == 'RadioButton' ):
                        if( status == 1 ):
                            flag = 'Selected'
                            status=desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                        else:
                            flag = 'UnSelected'
                            status=desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                    elif( tag == 'Button' ):
                        flag = status
                        status=desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                else:
                    err_msg='Element not present on the page where operation is trying to be performed'
            if ( err_msg!=None ):
                log.info( err_msg )
                log.error( err_msg )
                logger.print_on_console( err_msg )
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG
            logger.print_on_console( err_msg )
            log.error( exception )
        return status,result,flag,err_msg