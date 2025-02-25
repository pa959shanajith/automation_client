#-------------------------------------------------------------------------------
# Name:        desktop_editable_text.py
# Purpose:     This module handles textbox/edit related keywords. Also has methods to verify parent and performs cursor position correction.
#
# Author:      rakesh.v,anas.ahmed
#
# Created:     17-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import desktop_constants
from encryption_utility import AESCipher
import logger
import pythoncom
import win32api
import desktop_launch_keywords
import logging
from constants import *
import logger
log = logging.getLogger( 'desktop_editable_text.py' )

class Text_Box:
    def set_text(self , element, parent, input_val, *args):
        if ( len(input_val) > 1 ):
            text = input_val[3]
        else:
            text = input_val[0]
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        log.debug( 'Got window name after launching application' )
        log.debug( desktop_launch_keywords.window_name )
        log.info( STATUS_METHODOUTPUT_LOCALVARIABLES )
        verb = OUTPUT_CONSTANT
        err_msg = None
        try:
            if ( desktop_launch_keywords.window_name ):
                log.info( 'Recieved element from the desktop dispatcher' )
                dektop_element = element
                check = self.verify_parent(element, parent)
                log.debug( 'Parent of element while scraping' )
                log.debug( parent )
                log.debug( 'Parent check status' )
                log.debug( check )
                if ( check ):
                    log.info( 'Parent matched' )
                    if ( element.is_enabled() ):
                        try:
                            element.set_edit_text(text, pos_start = None, pos_end = None)
                        except:
                            self.clear_text(element, parent)
                            cursor_obj = CursorPositionCorrection()
                            cursor_obj.getOriginalPosition()
                            element.type_keys(text, with_spaces = True)
                            cursor_obj.setOriginalPosition()
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info( STATUS_METHODOUTPUT_UPDATE )
                    else:
                        err_msg = 'Element state does not allow to perform the operation'
                else:
                    err_msg = 'Element not present on the page where operation is trying to be performed'
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
            log.error( err_msg )
            logger.print_on_console( err_msg )
        log.info( RETURN_RESULT )
        return status, result, verb, err_msg


    def set_secure_text(self, element, parent, input_val, *args):
        if ( len(input_val) > 1 ):
            text = input_val[3]
        else:
            text = input_val[0]
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        log.debug( 'Got window name after launching application' )
        log.debug( desktop_launch_keywords.window_name )
        log.info( STATUS_METHODOUTPUT_LOCALVARIABLES )
        verb = OUTPUT_CONSTANT
        err_msg = None
        try:
            if ( desktop_launch_keywords.window_name ):
                log.info( 'Recieved element from the desktop dispatcher' )
                dektop_element = element
                check = self.verify_parent(element, parent)
                log.debug( 'Parent of element while scraping' )
                log.debug( parent )
                log.debug( 'Parent check status' )
                log.debug( check )
                if ( check ):
                    log.info( 'Parent matched' )
                    if ( element.is_enabled() ):
                        self.clear_text(element, parent)
                        log.info( 'Element state is enabled' )
                        encryption_obj = AESCipher()
                        input_val_temp = encryption_obj.decrypt( text )
                        if ( input_val_temp is not None ):
                            try:
                                element.set_edit_text(input_val_temp, pos_start = None, pos_end = None)
                            except:
                                self.clear_text(element, parent)
                                cursor_obj = CursorPositionCorrection()
                                cursor_obj.getOriginalPosition()
                                element.type_keys(input_val_temp, with_spaces = True)
                                cursor_obj.setOriginalPosition()
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info( STATUS_METHODOUTPUT_UPDATE )
                    else:
                        err_msg = 'Element state does not allow to perform the operation'
                else:
                   err_msg = 'Element not present on the page where operation is trying to be performed'
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
            log.error( err_msg )
            logger.print_on_console( err_msg )
        log.info( RETURN_RESULT )
        return status, result, verb, err_msg

    def get_text(self, element, parent, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        log.debug( 'Got window name after launching application' )
        log.debug( desktop_launch_keywords.window_name )
        log.info( STATUS_METHODOUTPUT_LOCALVARIABLES )
        output = None
        err_msg = None
        try:
            if ( desktop_launch_keywords.window_name ):
                log.info( 'Recieved element from the desktop dispatcher' )
                dektop_element = element
                check = self.verify_parent(element, parent)
                log.debug( 'Parent of element while scraping' )
                log.debug( parent )
                log.debug( 'Parent check status' )
                log.debug( check )
                if ( check ):
                    log.info( 'Parent matched' )
                    if ( element.backend.name == 'uia' ):
                        output = element.get_value()
                    elif ( element.backend.name == 'win32' ):
                        output = element.text_block()
                    status = desktop_constants.TEST_RESULT_PASS
                    result = desktop_constants.TEST_RESULT_TRUE
                    log.info( STATUS_METHODOUTPUT_UPDATE )
                else:
                   err_msg = 'Element not present on the page where operation is trying to be performed'
                   log.info( err_msg )
                   logger.print_on_console( err_msg )
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
            log.error( err_msg )
            logger.print_on_console( err_msg )
        log.info( RETURN_RESULT )
        return status, result, output, err_msg

    def clear_text(self, element, parent, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        log.debug( 'Got window name after launching application' )
        log.debug( desktop_launch_keywords.window_name )
        log.info( STATUS_METHODOUTPUT_LOCALVARIABLES )
        verb = OUTPUT_CONSTANT
        err_msg = None
        try:
            if ( desktop_launch_keywords.window_name ):
                log.info( 'Recieved element from the desktop dispatcher' )
                dektop_element = element
                check = self.verify_parent(element, parent)
                log.debug( 'Parent of element while scraping' )
                log.debug( parent )
                log.debug( 'Parent check status' )
                log.debug( check )
                if ( check ):
                    log.info( 'Parent matched' )
                    if ( element.is_enabled() ):
                        cursor_obj = CursorPositionCorrection()
                        cursor_obj.getOriginalPosition()
                        for i in range(0, len(element.text_block())):
                            element.type_keys('^a{BACKSPACE}')
                        cursor_obj.setOriginalPosition()
                        element.set_text("", pos_start = None, pos_end = None)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info( STATUS_METHODOUTPUT_UPDATE )
                    else:
                        err_msg = 'Element state does not allow to perform the operation'
                else:
                    err_msg = 'Element not present on the page where operation is trying to be performed'
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
            log.error( err_msg )
            logger.print_on_console( err_msg )
        return status,result,verb,err_msg

    def verify_text(self, element, parent, input_val, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        log.debug( 'Got window name after launching application' )
        log.debug( desktop_launch_keywords.window_name )
        log.info( STATUS_METHODOUTPUT_LOCALVARIABLES )
        verb = OUTPUT_CONSTANT
        err_msg = None
        text = None
        try:
            if ( desktop_launch_keywords.window_name ):
                log.info( 'Recieved element from the desktop dispatcher' )
                input_val = input_val[0]
                log.info( 'input value obtained' )
                log.info( input_val )
                check = self.verify_parent(element, parent)
                log.debug( 'Parent of element while scraping' )
                log.debug( parent )
                log.debug( 'Parent check status' )
                log.debug( check )
                if ( check ):
                    log.debug( 'Parent matched' )
                    if ( element.backend.name == 'uia' ):
                        text = str(element.get_value())
                    elif ( element.backend.name == 'win32' ):
                        text = str(element.text_block())
                    log.info( 'Text obtained' )
                    log.info( text )
                    if ( text == input_val ):
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = 'Text mismatched'
                        log.info( err_msg )
                        logger.print_on_console( err_msg )
                else:
                    err_msg = 'Element not present on the page where operation is trying to be performed'
                    log.info( err_msg )
                    logger.print_on_console( err_msg )
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
            log.error( err_msg )
            logger.print_on_console( err_msg )
        log.info( RETURN_RESULT )
        return status, result, verb, err_msg

    def verify_parent(self, element, parent):
        status = True
        desktop_constants.ELEMENT_FOUND = status
        return status

    def sendsecurefunction_keys(self, element, parent, input_val, *args):
        if ( len(input_val) > 1 ):
            text = input_val[3]
        else:
            text = input_val[0]
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        log.debug( 'Got window name after launching application' )
        log.debug( desktop_launch_keywords.window_name )
        log.info( STATUS_METHODOUTPUT_LOCALVARIABLES )
        verb = OUTPUT_CONSTANT
        err_msg = None
        try:
            if ( desktop_launch_keywords.window_name ):
                log.info( 'Recieved element from the desktop dispatcher' )
                dektop_element = element
                check = self.verify_parent(element, parent)
                log.debug( 'Parent of element while scraping' )
                log.debug( parent )
                log.debug( 'Parent check status' )
                log.debug( check )
                if ( check ):
                    log.info( 'Parent matched' )
                    if ( element.is_enabled() ):
                        self.clear_text(element, parent)
                        log.info( 'Element state is enabled' )
                        from desktop_util_keywords import Util_Keywords
                        obj=Util_Keywords()
                        res=obj.setFocus(element, parent, *args)
                        log.info( "focused on text box" )
                        if res:
                            from sendfunction_keys import SendFunctionKeys
                            obj=SendFunctionKeys()
                            result=obj.sendsecurefunction_keys(text)
                            if result[0]!="Fail":
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info( STATUS_METHODOUTPUT_UPDATE )
                    else:
                        err_msg = 'Element state does not allow to perform the operation'
                else:
                   err_msg = 'Element not present on the page where operation is trying to be performed'
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
            log.error( err_msg )
            logger.print_on_console( err_msg )
        log.info( RETURN_RESULT )
        return status, result, verb, err_msg

class CursorPositionCorrection:
    """When using sendkeys or type keys, we have observed that the mouse cursor moves from the current position very haphazardly. This class aims to rectify this type of anomaly"""
    def _init_():
        self.cursor_x = None
        self.cursor_y = None
    def getOriginalPosition(self):
        try:
            pythoncom.CoInitialize()
            self.cursor_x, self.cursor_y = win32api.GetCursorPos()
        except:
            pass
    def setOriginalPosition(self):
        try:
            win32api.SetCursorPos((self.cursor_x, self.cursor_y))
            pythoncom.CoUninitialize()
        except:
            pass