#-------------------------------------------------------------------------------
# Name:        desktop_tab_control_keywords.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     09/06/2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import desktop_launch_keywords
import logger
from desktop_editable_text import Text_Box
import desktop_constants
import desktop_editable_text
import time
from constants import *
editable_text = desktop_editable_text.Text_Box()
import logging
log = logging.getLogger('desktop_tab_control_keywords.py')
class Tab_Control_Keywords():

        def selectTabByIndex(self, element, parent, input_val, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            try:
                if ( desktop_launch_keywords.window_name != None ):
                    log.info( 'Recieved element from the desktop dispatcher' )
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element, parent)
                    log.debug( 'Parent of element while scraping' )
                    log.debug( parent )
                    log.debug( 'Parent check status' )
                    log.debug( check )
                    if ( check ):
                        log.info( 'Parent matched' )
                        if ( element.is_enabled() ):
                            item_index = int(input_val[0])
                            item_count = element.tab_count()
                            if ( item_index <= item_count ):
                                if ( element.is_enabled() ):
                                    selected_index = int(element.get_selected_tab())
                                    if ( selected_index == item_index - 1 ):
                                        err_msg = 'Tab control with given index is already selected'
                                    else:
                                        if ( item_index <= 0 ):
                                            err_msg = 'Tab control index starts with 1'
                                        else:
                                            element.select(item_index - 1)
                                            log.info( 'tab in Tab control  selected' )
                                            logger.print_on_console( 'tab in Tab control  selected' )
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                            log.info( STATUS_METHODOUTPUT_UPDATE )
                                else:
                                    err_msg = 'Tab control state does not allow to perform the operation'
                            else:
                                err_msg = 'There is no tab in Tab control with the given index'
                        else:
                            err_msg = 'Tab control not present on the page where operation is trying to be performed'
                if ( err_msg ):
                    log.info( err_msg )
                    logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
            return status, result, verb, err_msg


        def getSelectedTab(self, element, parent, input_val, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            items = []
            #---------------------------------------------checker(32 or 64)
            import platform
            info_32 = platform.architecture()
            if ( info_32[0] == '32bit' ):
                logger.print_on_console( 'Warning:You are using 32bit version of Avo Assure Client Engine.This keyword is unstable for this version.' )
            #---------------------------------------------
            try:
               verify_obj = Text_Box()
               check = verify_obj.verify_parent(element, parent)
               log.debug( 'Parent of element while scraping' )
               log.debug( parent )
               log.debug( 'Parent check status' )
               log.debug( check )
               if ( check ):
                        log.info( 'Parent matched' )
                        if( element.is_enabled() ):
                            #-----------------------------------checking if element is uia or win32
                            selected_tab_index = int(element.get_selected_tab())
                            if ( element.backend.name == 'win32' ):
                                verb = str(element.get_tab_text(selected_tab_index))
                            elif ( element.backend.name == 'uia' ):
                                tab_texts = element.texts()
                                verb = tab_texts[selected_tab_index]
                            #-----------------------------------checking if element is uia or win32
                            if ( verb == "" ):
                                handle = element.handle
                                import pywinauto
                                import pythoncom
                                pythoncom.CoInitialize()
                                text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem = handle, cache_enable = False).name
                                verb = text
                            logger.print_on_console('Selected Tab : ', verb)
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info( STATUS_METHODOUTPUT_UPDATE )
                        else:
                            err_msg = 'Tab control state does not allow to perform the operation'
               else:
                   err_msg = 'Tab control not present on the page where operation is trying to be performed'
               if ( err_msg ):
                    log.info( err_msg )
                    logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
            return status, result, verb, err_msg

        def verifySelectedTab(self, element, parent, input_val, *args):
                status = desktop_constants.TEST_RESULT_FAIL
                result = desktop_constants.TEST_RESULT_FALSE
                verb = OUTPUT_CONSTANT
                err_msg=None
                #---------------------------------------------checker(32 or 64)
                import platform
                info_32 = platform.architecture()
                if ( info_32[0] == '32bit' ):
                    logger.print_on_console( 'Warning:You are using 32bit version of Avo Assure Client Engine.This keyword is unstable for this version.' )
                #---------------------------------------------
                try:
                   verify_obj = Text_Box()
                   check = verify_obj.verify_parent(element, parent)
                   log.debug( 'Parent of element while scraping' )
                   log.debug( parent )
                   log.debug( 'Parent check status' )
                   log.debug( check )
                   if ( check ):
                            log.info( 'Parent matched' )
                            if( element.is_enabled() ):
                                #-----------------------------------checking if element is uia or win32
                                selected_tab_index = int(element.get_selected_tab())
                                if ( element.backend.name == 'win32' ):
                                    selected = str(element.get_tab_text(selected_tab_index))
                                elif ( element.backend.name == 'uia' ):
                                    tab_texts = element.texts()
                                    selected = tab_texts[selected_tab_index]
                                #-----------------------------------checking if element is uia or win32
                                if ( selected == '' ):
                                    handle = element.handle
                                    import pywinauto
                                    import pythoncom
                                    pythoncom.CoInitialize()
                                    text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem = handle, cache_enable = False).name
                                    selected = text
                                if ( selected == input_val[0] ):
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE
                                    log.info( STATUS_METHODOUTPUT_UPDATE )
                            else:
                                err_msg = 'Tab control state does not allow to perform the operation'
                   else:
                       err_msg = 'Tab control not present on the page where operation is trying to be performed'
                   if ( err_msg ):
                        log.info( err_msg )
                        logger.print_on_console( err_msg )
                except Exception as exception:
                    err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                    log.error( err_msg )
                    logger.print_on_console( err_msg )
                return status, result, verb, err_msg

        def selectTabByText(self, element, parent, input_val, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            result = desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg = None
            flag = False
            #---------------------------------------------checker(32 or 64)
            import platform
            info_32 = platform.architecture()
            if ( info_32[0] == '32bit' ):
                logger.print_on_console( 'Warning:You are using 32bit version of Avo Assure Client Engine.This keyword is unstable for this version.' )
            #---------------------------------------------
            try:
                if ( desktop_launch_keywords.window_name != None ):
                    log.info( 'Recieved element from the desktop dispatcher' )
                    verify_obj = Text_Box()
                    check = verify_obj.verify_parent(element, parent)
                    log.debug( 'Parent of element while scraping' )
                    log.debug( parent )
                    log.debug( 'Parent check status' )
                    log.debug( check )
                    if ( check ):
                        log.info( 'Parent matched' )
                        if ( element.is_enabled() ):
                            item_text = str(input_val[0])
                            if ( item_text != '' or item_text != None ):
                                if ( element.is_enabled() ):
                                    selected_tab_index=  int(element.get_selected_tab())
                                    #-----------------------------------checking if element is uia or win32
                                    if ( element.backend.name == 'win32' ):
                                        selected = str(element.get_tab_text(selected_tab_index))
                                    elif ( element.backend.name == 'uia' ):
                                        tab_texts = element.texts()
                                        selected = tab_texts[selected_tab_index]
                                    #-----------------------------------checking if element is uia or win32
                                    if ( selected == item_text ):
                                        err_msg = 'Tab control with given text is already selected'
                                    else:
                                        try:
                                            if ( element.backend.name == 'win32' ):
                                                element.select(item_text)
                                                flag = True
                                            elif ( element.backend.name == 'uia' ):
                                                try:
                                                    logger.print_on_console( 'SelectTabByText returns inconsistent outputs for method B elements' )
                                                    element.select(item_text)
                                                    flag = True
                                                except Exception as e:
                                                    log.error('Tab error via method B')
                                                    log.info('Tab error via method B')
                                                    log.error(e)
                                            if ( flag == True ):
                                                log.info( 'Tab control with given text selected' )
                                                logger.print_on_console( 'Tab control with given text selected' )
                                                status = desktop_constants.TEST_RESULT_PASS
                                                result = desktop_constants.TEST_RESULT_TRUE
                                                log.info( STATUS_METHODOUTPUT_UPDATE )
                                        except Exception as e:
                                            err_msg = 'There is no tab in Tab control with the given text'
                                else:
                                    err_msg = 'Tab control state does not allow to perform the operation'
                            else:
                                err_msg = 'There is no tab  in Tab control with the given text'
                        else:
                            err_msg = 'Tab control not present on the page where operation is trying to be performed'
                if ( err_msg ):
                    log.info( err_msg )
                    logger.print_on_console( err_msg )
            except Exception as exception:
                err_msg = desktop_constants.ERROR_MSG + ' : ' + str(exception)
                log.error( err_msg )
                logger.print_on_console( err_msg )
            return status, result, verb, err_msg