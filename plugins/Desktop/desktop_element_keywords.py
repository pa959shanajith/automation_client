#-------------------------------------------------------------------------------
# Name:        desktop_element_keywords.py
# Purpose:     script  to handle element objects
#
# Author:      wasimakram.sutar
#
# Created:     29/05/2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import desktop_constants
from desktop_editable_text import Text_Box, CursorPositionCorrection
import desktop_launch_keywords
import pywinauto
import pythoncom
import logging
from constants import *
import logger
import pyautogui
import time
log = logging.getLogger( 'desktop_element_keywords.py' )

class ElementKeywords():
    def verify_element_exists(self, element, parent, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        log.debug( 'Got window name : ' )
        log.debug( desktop_launch_keywords.window_name )
        log.info( STATUS_METHODOUTPUT_LOCALVARIABLES )
        verb = OUTPUT_CONSTANT
        err_msg = None
        try:
            if ( desktop_launch_keywords.window_name ):
                log.info( 'Recieved element from the desktop dispatcher' )
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element, parent)
                log.debug( 'Parent of element while scraping' )
                log.debug( parent )
                log.debug( 'Parent check status' )
                log.debug( check )
                if ( check ):
                    log.info( 'Parent matched' )
                    if ( element.is_visible() ):
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

    def verify_element_doesNot_exists(self, element, parent, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        log.debug( desktop_launch_keywords.window_name )
        log.info( STATUS_METHODOUTPUT_LOCALVARIABLES )
        verb = OUTPUT_CONSTANT
        err_msg = None
        try:
            if ( desktop_launch_keywords.window_name ):
                log.info( 'Recieved element from the desktop dispatcher' )
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element, parent)
                log.debug( 'Parent of element while scraping' )
                log.debug( parent )
                log.debug( 'Parent check status' )
                log.debug( check )
                if ( check ):
                    log.info( 'Parent matched' )
                    if(not element.is_visible()):
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

    def click_element(self, element, parent, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        log.debug( desktop_launch_keywords.window_name )
        log.info( STATUS_METHODOUTPUT_LOCALVARIABLES )
        verb = OUTPUT_CONSTANT
        err_msg = None
        try:
            if ( desktop_launch_keywords.window_name ):
                log.info( 'Recieved element from the desktop dispatcher' )
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element, parent)
                log.debug( 'Parent of element while scraping' )
                log.debug( parent )
                log.debug( 'Parent check status' )
                log.debug( check )
                if ( check ):
                    log.info( 'Parent matched' )
                    if ( element.is_enabled() ):
                        cursor_obj = CursorPositionCorrection()
                        cursor_obj.getOriginalPosition()
                        element.set_focus()
                        cursor_obj.setOriginalPosition()
                        element.click()
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info( STATUS_METHODOUTPUT_UPDATE )
                    else:
                      err_msg = 'Element state does not allow to perform the operation'
                else:
                   err_msg='Element not present on the page where operation is trying to be performed'
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
            log.error( err_msg )
            logger.print_on_console( err_msg )
        log.info( RETURN_RESULT )
        return status, result, verb, err_msg

    def get_element_text(self, element, parent, *args):
        pythoncom.CoInitialize()
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
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element, parent)
                log.debug( 'Parent of element while scraping' )
                log.debug( parent )
                log.debug( 'Parent check status' )
                log.debug( check )
                if ( check ):
                    log.info( 'Parent matched' )
                    if element.backend.name == "win32":
                        output = element.texts()
                        if isinstance(output, list) and len(output) > 0:
                            output = output[0]

                        if output != None and len(output) == 0:
                            output = element.element_info.rich_text
                            if output != None and len(output) == 0:
                                output = element.element_info.name
                    elif element.backend.name == "uia":
                        output = element.element_info.rich_text
                        if output != None and len(output) == 0:
                            output = element.element_info.name

                    if output != None and len(output) == 0:
                        handle = element.handle
                        output = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem = handle, cache_enable = False).name
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

    def verify_element_text(self, element, parent, input_value, *args):
        pythoncom.CoInitialize()
        if ( len(input_value) > 1 ):
            text_verify = input_value[3]
        else:
            text_verify = input_value[0]
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
                input_val = text_verify
                log.info( 'input value obtained' )
                log.info( input_val )
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element, parent)
                log.debug( 'Parent of element while scraping' )
                log.debug( parent )
                log.debug( 'Parent check status' )
                log.debug( check )
                if ( check ):
                    log.debug( 'Parent matched' )
                    handle = element.handle
                    text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem = handle, cache_enable = False).name
                    logger.print_on_console('Text obtained : ', text)
                    log.info( 'Text obtained' )
                    log.info( str(text) )
                    if ( str(text) == input_val ):
                        log.info( STATUS_METHODOUTPUT_UPDATE )
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = 'Element Text mismatched'
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

    def mouseHover(self, element, parent, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        Rect = ''
        try:
            #----------get the element coordinates
            try:
                Rect = str(element.rectangle())
            except:
                pass
            Rect = Rect[1:len(Rect)-1]
            Rect = Rect.split(",")
            Left = Rect[0].strip()#left
            if ( "L" in Left ):
                Left = int(Left[1:])
            else:
                Left = int(Left)
            Top=Rect[1].strip()#top
            if ( "T" in Top ):
                Top = int(Top[1:])
            else:
                Top = int(Top)
            Right = Rect[2].strip()#right
            if ( "R" in Right ):
                Right = int(Right[1:])
            else:
                Right = int(Right)
            Bottom = Rect[3].strip()#bottom
            if ( "B" in Bottom ):
                Bottom = int(Bottom[1:])
            else:
                Bottom = int(Bottom)
            #---------------------Finding height and width
            height = Bottom - Top
            width = Right - Left
            #--------------------Finding X and Y co-ordinates
            x = Left + width / 2
            y = Top + height / 2
            pywinauto.mouse.move(coords = (int(x), int(y)))
            status = desktop_constants.TEST_RESULT_PASS
            result = desktop_constants.TEST_RESULT_TRUE
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
            log.error( err_msg )
            logger.print_on_console( err_msg )
        log.info( RETURN_RESULT )
        return status, result, verb, err_msg
    
    def get_element_color(self, element, parent, input, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        log.debug( desktop_launch_keywords.window_name )
        log.info( STATUS_METHODOUTPUT_LOCALVARIABLES )
        verb = OUTPUT_CONSTANT
        err_msg = None
        try:
            if ( desktop_launch_keywords.window_name ):
                log.info( 'Recieved element from the desktop dispatcher' )
                dektop_element = element
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element, parent)
                log.debug( 'Parent of element while scraping' )
                log.debug( parent )
                log.debug( 'Parent check status' )
                log.debug( check )
                if ( check ):
                    log.info( 'Parent matched' )
                    if ( element.is_enabled() ):
                        input = input[0]
                        cursor_obj = CursorPositionCorrection()
                        cursor_obj.getOriginalPosition()
                        element.set_focus()
                        cursor_obj.setOriginalPosition()
                        rect = element.rectangle() #--------use this if element is textbox
                        element_properties = element.get_properties()
                        left = element_properties['rectangle'].left
                        top = element_properties['rectangle'].top
                        left = left+8
                        top = top+8
                        color = pyautogui.pixel(left, top)
                        output = color
                        logger.print_on_console( f'RGB color value of the element is: {color}' )
                        if not (input is None or input is ''):
                            if ( str(color) == input):
                                log.info( STATUS_METHODOUTPUT_UPDATE )
                                logger.print_on_console( f'RGB color values match' )
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                            else:
                                err_msg = 'RGB color values mismatched'
                                log.info( err_msg )
                        else:
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info( STATUS_METHODOUTPUT_UPDATE )
                    else:
                      err_msg = 'Element state does not allow to perform the operation'
                else:
                   err_msg='Element not present on the page where operation is trying to be performed'
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
            log.error( err_msg )
            logger.print_on_console( err_msg )
        log.info( RETURN_RESULT )
        return status, result, output, err_msg
    
    def drag(self, element, parent, input_val, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        Rect = ''
        try:
            if input_val != [''] and ( len(input_val) >= 1 ):    #-----------Drag operation for table.
                index = int(input_val[0])
                if ( element.friendly_class_name() == 'Table' and (element.texts()[0] == 'DataGridView' or 'RadGridView' in element.texts()[0])):
                    log.info( 'Valid row number' )
                    c = element.children()
                    const = 0
                    for i in range(0,len(c)):
                        if ( c[i].friendly_class_name().lower() == "scrollbar" ):
                            const += 1
                    if ( (len(c) - const - 1) >= index ):
                        # rect = element.rectangle()
                        c[const + index].click_input()
                        pyautogui.mouseDown()
                        pyautogui.move(0,1)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
            else:
                #----------get the element coordinates
                try:
                    Rect = str(element.rectangle())
                except:
                    pass
                Rect = Rect[1:len(Rect)-1]
                Rect = Rect.split(",")
                Left = Rect[0].strip()#left
                if ( "L" in Left ):
                    Left = int(Left[1:])
                else:
                    Left = int(Left)
                Top=Rect[1].strip()#top
                if ( "T" in Top ):
                    Top = int(Top[1:])
                else:
                    Top = int(Top)
                Right = Rect[2].strip()#right
                if ( "R" in Right ):
                    Right = int(Right[1:])
                else:
                    Right = int(Right)
                Bottom = Rect[3].strip()#bottom
                if ( "B" in Bottom ):
                    Bottom = int(Bottom[1:])
                else:
                    Bottom = int(Bottom)
                #---------------------Finding height and width
                height = Bottom - Top
                width = Right - Left
                #--------------------Finding X and Y co-ordinates
                x = Left + width / 2
                y = Top + height / 2
                pywinauto.mouse.move(coords = (int(x), int(y)))
                pywinauto.mouse.press(button='left', coords = (int(x), int(y)))
                pywinauto.mouse.move(coords = (int(x+1), int(y+1)))
                # pyautogui.mouseDown()
                status = desktop_constants.TEST_RESULT_PASS
                result = desktop_constants.TEST_RESULT_TRUE
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
            log.error( err_msg )
            logger.print_on_console( err_msg )
        log.info( RETURN_RESULT )
        return status, result, verb, err_msg
    
    def drop(self, element, parent, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        Rect = ''
        try:
            #----------get the element coordinates
            try:
                Rect = str(element.rectangle())
            except:
                pass
            Rect = Rect[1:len(Rect)-1]
            Rect = Rect.split(",")
            Left = Rect[0].strip()#left
            if ( "L" in Left ):
                Left = int(Left[1:])
            else:
                Left = int(Left)
            Top=Rect[1].strip()#top
            if ( "T" in Top ):
                Top = int(Top[1:])
            else:
                Top = int(Top)
            Right = Rect[2].strip()#right
            if ( "R" in Right ):
                Right = int(Right[1:])
            else:
                Right = int(Right)
            Bottom = Rect[3].strip()#bottom
            if ( "B" in Bottom ):
                Bottom = int(Bottom[1:])
            else:
                Bottom = int(Bottom)
            #---------------------Finding height and width
            height = Bottom - Top
            width = Right - Left
            #--------------------Finding X and Y co-ordinates
            x = Left + width / 2
            y = Top + height / 2
            pywinauto.mouse.move(coords = (int(x), int(y)))
            # pyautogui.moveTo(x, y) #---------use this if element doesn't support pwa
            time.sleep(1)
            pywinauto.mouse.release(button='left', coords = (int(x), int(y)))
            # pyautogui.mouseDown()
            status = desktop_constants.TEST_RESULT_PASS
            result = desktop_constants.TEST_RESULT_TRUE
        except Exception as exception:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
            log.error( err_msg )
            logger.print_on_console( err_msg )
        log.info( RETURN_RESULT )
        return status, result,verb, err_msg