#-------------------------------------------------------------------------------
# Name:        tab_control_keywords.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     09/06/2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import launch_keywords
import logger
from editable_text import Text_Box
import desktop_constants
import editable_text
import time
from constants import *
editable_text=editable_text.Text_Box()
import logging
log = logging.getLogger('tab_control_keywords.py')
class Tab_Control_Keywords():

        def selectTabByIndex(self,element,parent,input_val, *args):
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
                        if(element.is_enabled()):
                            item_index=int(input_val[0])
                            item_count = element.TabCount()
                            if item_index <= item_count:
                                if element.is_enabled():
                                    selected_index = element.GetSelectedTab()
                                    selected_index = int(selected_index)
                                    if selected_index == item_index -1:
                                        log.info('Tab control with given index is already selected')
                                        logger.print_on_console('Tab control with given index is already selected')
                                        err_msg = 'Tab control with given index is already selected'
                                    else:
                                        if item_index <=0:
                                            log.info('Tab control index starts with 1')
                                            logger.print_on_console('Tab control index starts with 1')
                                            err_msg = 'Tab control index starts with 1'
                                        else:
                                            element.select(item_index-1)
                                            log.info('tab in Tab control  selected')
                                            logger.print_on_console('tab in Tab control  selected')
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                            log.info(STATUS_METHODOUTPUT_UPDATE)
                                else:
                                    log.info('Tab control state does not allow to perform the operation')
                                    logger.print_on_console('Tab control state does not allow to perform the operation')
                                    err_msg = 'Tab control state does not allow to perform the operation'
                            else:
                                log.info('There is no tab in Tab control with the given index')
                                logger.print_on_console('There is no tab in Tab control with the given index')
                                err_msg = 'There is no tab in Tab control with the given index'
                        else:
                            log.info('Tab control not present on the page where operation is trying to be performed')
                            err_msg='Tab control not present on the page where operation is trying to be performed'
                            logger.print_on_console('Tab not present on the page where operation is trying to be performed')
            except Exception as exception:
                log.error(exception)
                logger.print_on_console(exception)
            return status,result,verb,err_msg


        def getSelectedTab(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            items=[]
            try:
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
                            selected_tab_index=element.GetSelectedTab()
                            selected_tab_index = int(selected_tab_index)
                            selected = element.GetTabText(selected_tab_index)
                            verb=selected
                            logger.print_on_console('selected tab:',verb)
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                        else:
                            log.info('Tab control state does not allow to perform the operation')
                            logger.print_on_console('Tab control state does not allow to perform the operation')
                            err_msg = 'Tab control state does not allow to perform the operation'
               else:
                   log.info('Tab control not present on the page where operation is trying to be performed')
                   err_msg='Tab control not present on the page where operation is trying to be performed'
            except Exception as exception:
                import traceback
                traceback.print_exc()
                log.error(exception)
                logger.print_on_console(exception)


            return status,result,verb,err_msg

        def verifySelectedTab(self,element,parent,input_val, *args):
                status=desktop_constants.TEST_RESULT_FAIL
                result=desktop_constants.TEST_RESULT_FALSE
                verb = OUTPUT_CONSTANT
                err_msg=None
                try:
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
                                selected_tab_index=element.GetSelectedTab()
                                selected_tab_index = int(selected_tab_index)
                                selected = element.GetTabText(selected_tab_index)
                                selected= str(selected)
                                input_val = input_val[0]
                                if selected == input_val:
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE
                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                log.info('Tab control state does not allow to perform the operation')
                                logger.print_on_console('Tab control state does not allow to perform the operation')
                                err_msg = 'Tab control state does not allow to perform the operation'
                   else:
                       log.info('Tab control not present on the page where operation is trying to be performed')
                       err_msg='Tab control not present on the page where operation is trying to be performed'
                       logger.print_on_console('Tab control not present on the page where operation is trying to be performed')
                except Exception as exception:
                    import traceback
                    traceback.print_exc()
                    log.error(exception)
                    logger.print_on_console(exception)

                return status,result,verb,err_msg

        def selectTabByText(self,element,parent,input_val, *args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            err_msg=None
            text_flag = False
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
                        if(element.is_enabled()):
                            item_text=str(input_val[0])
                            if item_text != '' or item_text != None:
                                if element.is_enabled():
                                    selected_tab_index=element.GetSelectedTab()
                                    selected_tab_index = int(selected_tab_index)
                                    selected = element.GetTabText(selected_tab_index)
                                    if selected == item_text:
                                        log.info('Tab control with given text is already selected')
                                        logger.print_on_console('Tab control with given text is already selected')
                                        err_msg = 'Tab control with given text is already selected'
                                    else:
                                        try:
                                            element.select(item_text)
                                            log.info('Tab control with given text selected')
                                            logger.print_on_console('Tab control with given text selected')
                                            status = desktop_constants.TEST_RESULT_PASS
                                            result = desktop_constants.TEST_RESULT_TRUE
                                            log.info(STATUS_METHODOUTPUT_UPDATE)
                                        except Exception as e:
                                            log.info('There is no tab in Tab control with the given text')
                                            logger.print_on_console('There is no tab in Tab control with the given text')
                                            err_msg = 'There is no tab in Tab control with the given text'
                                else:
                                    log.info('Tab control state does not allow to perform the operation')
                                    logger.print_on_console('Tab control state does not allow to perform the operation')
                                    err_msg = 'Tab control state does not allow to perform the operation'
                            else:
                                log.info('There is no tab  in Tab control with the given text')
                                logger.print_on_console('There is no tab  in Tab control with the given text')
                                err_msg = 'There is no tab  in Tab control with the given text'
                        else:
                            log.info('Tab control not present on the page where operation is trying to be performed')
                            err_msg='Tab control not present on the page where operation is trying to be performed'
                            logger.print_on_console('Tab control not present on the page where operation is trying to be performed')
            except Exception as exception:
                log.error(exception)
                logger.print_on_console(exception)
            return status,result,verb,err_msg


