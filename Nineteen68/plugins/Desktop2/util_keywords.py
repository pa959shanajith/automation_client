#-------------------------------------------------------------------------------
# Name:        util_keywords.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     08-05-2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import launch_keywords
import logger
import logging
import desktop_constants
import editable_text
from launch_keywords import Launch_Keywords
from constants import *
import pywinauto
##editable_text=editable_text.Text_Box()
from editable_text import Text_Box
log = logging.getLogger('util_keywords.py')
class Util_Keywords():

        def verifyEnabled(self,element,parent,*args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            try:
                if launch_keywords.window_name!=None:
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
                        if(element.is_enabled):
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                        else:
                            log.info('Element state does not allow to perform the operation')
                    else:
                        log.info('element not present on the page where operation is trying to be performed')
                        err_msg='element not present on the page where operation is trying to be performed'
            except Exception as exception:
                log.error(exception)
                err_msg = desktop_constants.ERROR_MSG
                logger.print_on_console(exception)
            return status,result,verb,err_msg

        def verifyDisabled(self,element,parent,*args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            try:
                if launch_keywords.window_name!=None:
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
                        if(not element.is_enabled):
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                        else:
                            log.info('Element state does not allow to perform the operation')
                    else:
                        log.info('element not present on the page where operation is trying to be performed')
                        err_msg='element not present on the page where operation is trying to be performed'
            except Exception as exception:
                log.error(exception)
                err_msg = desktop_constants.ERROR_MSG
                logger.print_on_console(exception)
            return status,result,verb,err_msg

        def verifyVisible(self,element,parent,*args):
                status=desktop_constants.TEST_RESULT_FAIL
                result=desktop_constants.TEST_RESULT_FALSE
                verb = OUTPUT_CONSTANT
                err_msg=None
                try:
                    if launch_keywords.window_name!=None:
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
                            if(element.is_visible):
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                log.info('Element state does not allow to perform the operation')
                        else:
                            log.info('element not present on the page where operation is trying to be performed')
                            err_msg='element not present on the page where operation is trying to be performed'
                except Exception as exception:
                    log.error(exception)
                    err_msg = desktop_constants.ERROR_MSG
                    logger.print_on_console(exception)
                return status,result,verb,err_msg

        def verifyExists(self,element,parent,*args):
                status=desktop_constants.TEST_RESULT_FAIL
                result=desktop_constants.TEST_RESULT_FALSE
                verb = OUTPUT_CONSTANT
                err_msg=None
                try:
                    if launch_keywords.window_name!=None:
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
                            if(element.is_enabled):
                                element.set_focus()
                                import desktop_highlight
                                highlightObj=desktop_highlight.highLight()
                                highlightObj.highlight_desktop_element(element)
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                log.info('Element state does not allow to perform the operation')
                        else:
                            log.info('element not present on the page where operation is trying to be performed')
                            err_msg='element not present on the page where operation is trying to be performed'
                except Exception as exception:
                    log.error(exception)
                    err_msg = desktop_constants.ERROR_MSG
                    logger.print_on_console(exception)
                return status,result,verb,err_msg

        def verifyHidden(self,element,parent,*args):
                status=desktop_constants.TEST_RESULT_FAIL
                result=desktop_constants.TEST_RESULT_FALSE
                verb = OUTPUT_CONSTANT
                err_msg=None
                try:
                    if launch_keywords.window_name!=None:
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
                            if(not element.is_enabled):
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                log.info('Element state does not allow to perform the operation')
                        else:
                            log.info('element not present on the page where operation is trying to be performed')
                            err_msg='element not present on the page where operation is trying to be performed'
                except Exception as exception:
                    log.error(exception)
                    err_msg = desktop_constants.ERROR_MSG
                    logger.print_on_console(exception)
                return status,result,verb,err_msg

        def verifyReadOnly(self,element,parent,*args):
                status=desktop_constants.TEST_RESULT_FAIL
                result=desktop_constants.TEST_RESULT_FALSE
                verb = OUTPUT_CONSTANT
                err_msg=None
                try:
                    if launch_keywords.window_name!=None:
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
                            if(not element.is_enabled):
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                log.info('Element state does not allow to perform the operation')
                        else:
                            log.info('element not present on the page where operation is trying to be performed')
                            err_msg='element not present on the page where operation is trying to be performed'
                except Exception as exception:
                    log.error(exception)
                    err_msg = desktop_constants.ERROR_MSG
                    logger.print_on_console(exception)
                return status,result,verb,err_msg

        def setFocus(self,element,parent,*args):
                status=desktop_constants.TEST_RESULT_FAIL
                result=desktop_constants.TEST_RESULT_FALSE
                verb = OUTPUT_CONSTANT
                err_msg=None
                try:
                    if launch_keywords.window_name!=None:
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
                            if(element.is_enabled):
                                obj = launch_keywords.Launch_Keywords()
                                obj.set_to_foreground()
                                winrect = launch_keywords.win_rect;
                                #CO ORDINATES WITH RESPECT TO AUT
                                coordinates_aut = element.client_rect()
                                #CO ORDINATES WITH RESPECT TO SCREEN
                                coordinates_screen = element.rectangle()
                                left = 0
                                top = 0
                                #get the width, height lef and top
                                width = coordinates_aut.width()
                                height = coordinates_aut.height()
                                left = coordinates_screen.left + 8
                                top = coordinates_screen.top + 8
                                if top < 0:
                                   top = -top
                                if left < 0:
                                   left = -left
                                pywinauto.mouse.move(coords=(left, top))
                                status = desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                log.info('Element state does not allow to perform the operation')
                        else:
                            log.info('element not present on the page where operation is trying to be performed')
                            err_msg='element not present on the page where operation is trying to be performed'
                except Exception as exception:
                    log.error(exception)
                    err_msg = desktop_constants.ERROR_MSG
                    logger.print_on_console(exception)
                    import traceback
                    traceback.print_exc()
                return status,result,verb,err_msg

