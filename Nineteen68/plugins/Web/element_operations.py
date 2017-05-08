#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     10-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger

from utils_web import Utils
from button_link_keyword import ButtonLinkKeyword
from webconstants import *


import logging
from constants import *

log = logging.getLogger('element_operations.py')

class ElementKeywords:

    def __getelement_text(self,webelement):
        # Fixed issue #311
        text=''
        try:
            text=str(webelement.text)
            if text is None or text is '':
                text=str(webelement.get_attribute('value'))
            if text is None or text is '':
                text=str(webelement.get_attribute('name'))
            if text is None or text is '':
                text=self.__get_tooltip(webelement)
            if text is None or text is '':
                text=str(webelement.get_attribute('placeholder'))
            if text is None or text is '':
                text=str(webelement.get_attribute('href'))
        except Exception as e:
            import ftfy
            temp_txt = ''
            temp_txt = webelement.text
            if temp_txt is not None or temp_txt is not '':
                text = ftfy.fix_text(temp_txt)
            if temp_txt is None or temp_txt is '':
                temp_txt = webelement.get_attribute('value')
                text = ftfy.fix_text(temp_txt)
            if temp_txt is None or temp_txt is '':
                temp_txt = webelement.get_attribute('name')
                text = ftfy.fix_text(temp_txt)
            if temp_txt is None or temp_txt is '':
                text=self.__get_tooltip(webelement)
            if temp_txt is None or temp_txt is '':
                temp_txt = webelement.get_attribute('placeholder')
                text = ftfy.fix_text(temp_txt)
            if temp_txt is None or temp_txt is '':
                temp_txt = webelement.get_attribute('href')
                text = ftfy.fix_text(temp_txt)

        return text

    def __get_tooltip(self,webelement):
        text=''
        try:
            text = str(webelement.get_attribute('title'))
        except Exception as e:
            import ftfy
            temp_txt = webelement.get_attribute('title')
            text = ftfy.fix_text(temp_txt)
        return text



    def get_element_text(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        text=None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
               text=self.__getelement_text(webelement)
               logger.print_on_console('Element text: ',text)
               log.info('Element text: ')
               log.info(text)
               log.info(STATUS_METHODOUTPUT_UPDATE)
               status=TEST_RESULT_PASS
               methodoutput=TEST_RESULT_TRUE
            except Exception as e:
                log.error(e)
                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        log.info(RETURN_RESULT)
        return status,methodoutput,text,err_msg

    def verify_element_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                input=input[0]
                if input is not None:
                   text=self.__getelement_text(webelement)
                   if text==input:
                       logger.print_on_console('Element Text matched')
                       log.info('Element Text matched')
                       log.info(STATUS_METHODOUTPUT_UPDATE)
                       status=TEST_RESULT_PASS
                       methodoutput=TEST_RESULT_TRUE
                   else:
                        logger.print_on_console('Element Text mismatched')
                        log.info('Element Text mismatched')
                        logger.print_on_console('Expected: ',text)
                        log.info('Expected:')
                        log.info(text)
                        logger.print_on_console('Actual: ',input)
                        log.info('Actual:')
                        log.info(input)
                else:
                    log.error(INVALID_INPUT)
                    err_msg=INVALID_INPUT
                    logger.print_on_console(INVALID_INPUT)
            except Exception as e:
                log.error(e)

                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def click_element(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                    click_obj=ButtonLinkKeyword()
                    log.debug('ButtonLinkKeyword object created to call the click method')
                    status,methodoutput,output,err_msg=click_obj.click(webelement)
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    log.error(ERR_DISABLED_OBJECT)
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    logger.print_on_console(ERR_DISABLED_OBJECT)
            except Exception as e:
                log.error(e)

                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def drag(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                    obj=Utils()
                    log.debug('Utils object created to call the get_element_location method')
                     #find the location of the element w.r.t viewport
                    location=obj.get_element_location(webelement)
                    log.info('location is :')
                    log.info(location)
                    import browser_Keywords
                    from selenium import webdriver
                    if isinstance(browser_Keywords.driver_obj,webdriver.Firefox):
                        yoffset=browser_Keywords.driver_obj.execute_script(MOUSE_HOVER_FF)
                        obj.mouse_move(int(location.get('x')+9),int(location.get('y')+yoffset))
                    else:
                        obj.enumwindows()
                        if len(obj.rect)>1:
                            obj.mouse_move(int(location.get('x')+9),int(location.get('y')+obj.rect[1]+6))
                        else:
                            err_msg='Element to be dragged should be on top'
                            log.error=err_msg
                            logger.print_on_console(err_msg)
                    import time
                    time.sleep(0.5)
                    obj.mouse_press(LEFT_BUTTON)
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    log.error(ERR_DISABLED_OBJECT)
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    logger.print_on_console(ERR_DISABLED_OBJECT)
            except Exception as e:
                log.error(e)
                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def drop(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                    obj=Utils()
                    log.debug('Utils object created to call the get_element_location method')
                     #find the location of the element w.r.t viewport
                    location=obj.get_element_location(webelement)
                    log.info('location is :')
                    log.info(location)
                    import time
                    time.sleep(0.5)
                    import browser_Keywords
                    from selenium import webdriver
                    if isinstance(browser_Keywords.driver_obj,webdriver.Firefox):
                        yoffset=browser_Keywords.driver_obj.execute_script(MOUSE_HOVER_FF)
                        obj.slide(int(location.get('x')+9),int(location.get('y')+yoffset), 0);
                    else:
                        obj.enumwindows()
                        if len(obj.rect)>1:
                            obj.slide(int(location.get('x')+9),int(location.get('y')+obj.rect[1]+6), 0)
                        else:
                            err_msg='Element to be dragged should be on top'
                            log.error=err_msg
                            logger.print_on_console(err_msg)
                    time.sleep(0.5)
                    obj.mouse_release(LEFT_BUTTON)
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    log.error(ERR_DISABLED_OBJECT)
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    logger.print_on_console(ERR_DISABLED_OBJECT)
            except Exception as e:
                log.error(e)

                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg


    def get_tooltip_text(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        tool_tip=None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
               tool_tip=self.__get_tooltip(webelement)
               if tool_tip is not None and tool_tip != '':
                   log.info(STATUS_METHODOUTPUT_UPDATE)
                   status=TEST_RESULT_PASS
                   methodoutput=TEST_RESULT_TRUE
               else:
                    tool_tip=None
               log.info('Tool tip text is : ')
               log.info(tool_tip)
               logger.print_on_console('Tool tip text: '+str(tool_tip))
            except Exception as e:
                log.error(e)

                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,tool_tip,err_msg


    def verify_tooltip_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        tool_tip = None
        if webelement is not None:
            try:
                input=input[0]
                if input is not None and input != '':
                    tool_tip=self.__get_tooltip(webelement)
                    if input==tool_tip:
                        logger.print_on_console('Tool tip Text matched')
                        log.info('Tool tip Text matched')
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Tool tip Text mismatched')
                        log.info('Tool tip Text mismatched')
                        logger.print_on_console('Expected: ',tool_tip)
                        log.info('Expected:')
                        log.info(tool_tip)
                        logger.print_on_console('Actual: ',input)
                        log.info('Actual:')
                        log.info(input)
                else:
                    log.error(INVALID_INPUT)
                    err_msg=INVALID_INPUT
                    logger.print_on_console(INVALID_INPUT)
            except Exception as e:
                log.error(e)

                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def waitforelement_visible(self,webelement,objectname,*args):
        import browser_Keywords
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if objectname is not None:
                delay=3
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.common.exceptions import TimeoutException
                from selenium.webdriver.common.by import By
                element_present = EC.presence_of_element_located((By.XPATH, objectname))
                WebDriverWait(browser_Keywords.driver_obj, delay).until(element_present)
                log.info('Element is visible')
                logger.print_on_console('Element is visible')
                log.info(STATUS_METHODOUTPUT_UPDATE)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except TimeoutException as e:
            logger.print_on_console('Delay timeout exceeded')
            log.error(e)

            logger.print_on_console(e)
            err_msg='Delay timeout exceeded'
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        return status,methodoutput,output,err_msg



