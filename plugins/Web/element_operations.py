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
from utilweb_operations import UtilWebKeywords
from button_link_keyword import ButtonLinkKeyword
import browser_Keywords
from webconstants import *
import readconfig

import logging
from constants import *
import threading
local_eo = threading.local()
##DROP_JS = """var target = arguments[0],     offsetX = arguments[1],     offsetY = arguments[2],     document = target.ownerDocument || document,     window = document.defaultView || window;  var input = document.createElement('INPUT'); input.type = 'file'; input.style.display = 'none'; input.onchange = function() {     target.scrollIntoView(true);      var rect = target.getBoundingClientRect(),         x = rect.left + (offsetX || (rect.width >> 1)),         y = rect.top + (offsetY || (rect.height >> 1)),         dataTransfer = {             files: this.files         };      ['dragenter', 'dragover', 'drop'].forEach(function(name) {         var evt = document.createEvent('MouseEvent');         evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);         evt.dataTransfer = dataTransfer;         target.dispatchEvent(evt);     });      setTimeout(function() {         document.body.removeChild(input);     }, 25); }; document.body.appendChild(input); return input;"""
##log = logging.getLogger('element_operations.py')

class ElementKeywords:
    def __init__(self):
        global local_eo
        local_eo.DROP_JS = """var target = arguments[0],     offsetX = arguments[1],     offsetY = arguments[2],     document = target.ownerDocument || document,     window = document.defaultView || window;  var input = document.createElement('INPUT'); input.type = 'file'; input.style.display = 'none'; input.onchange = function() {     target.scrollIntoView(true);      var rect = target.getBoundingClientRect(),         x = rect.left + (offsetX || (rect.width >> 1)),         y = rect.top + (offsetY || (rect.height >> 1)),         dataTransfer = {             files: this.files         };      ['dragenter', 'dragover', 'drop'].forEach(function(name) {         var evt = document.createEvent('MouseEvent');         evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);         evt.dataTransfer = dataTransfer;         target.dispatchEvent(evt);     });      setTimeout(function() {         document.body.removeChild(input);     }, 25); }; document.body.appendChild(input); return input;"""
        local_eo.log = logging.getLogger('element_operations.py')

    def __getelement_text(self,webelement):
##        # Fixed issue #311
        text=''
        try:
            text = webelement.text
            if text is None or text is '':
                text=webelement.get_attribute('value')
            if text is None or text is '':
                text=webelement.get_attribute('name')
            if text is None or text is '':
                text=self.__get_tooltip(webelement)
            if text is None or text is '':
                text=webelement.get_attribute('placeholder')
            if text is None or text is '':
                text=webelement.get_attribute('href')
        except Exception as e:
            local_eo.log.error(e)
            logger.print_on_console(e)
        return text

    def __get_tooltip(self,webelement):
        text=''
        try:
            text = webelement.get_attribute('title')
            if text =='':
                text = webelement.get_attribute('data-original-title')
        except Exception as e:
            local_eo.log.error(e)
            logger.print_on_console(e)
        return text



    def get_element_text(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        text=None
        err_msg=None
        configvalues = readconfig.configvalues
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                util = UtilWebKeywords()
                if not(util.is_visible(webelement)) and configvalues['ignoreVisibilityCheck'].strip().lower() == "yes":
                    local_eo.log.debug('element is invisible, performing js code')
                    text = browser_Keywords.local_bk.driver_obj.execute_script("""return arguments[0].innerText""",webelement)
                    logger.print_on_console('Element text: ',text)
                    local_eo.log.info('Element text: ')
                    local_eo.log.info(text)
                    status=TEST_RESULT_PASS
                    result=TEST_RESULT_TRUE
                    local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                else:
                    if(util.is_visible(webelement)):
                        text=self.__getelement_text(webelement)
                        logger.print_on_console('Element text: ',text)
                        local_eo.log.info('Element text: ')
                        local_eo.log.info(text)
                        local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = 'Element is not displayed'
                        logger.print_on_console('Element is not displayed')
                        local_eo.log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
            except Exception as e:
                local_eo.log.error(e)
                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        local_eo.log.info(RETURN_RESULT)
        return status,methodoutput,text,err_msg

    def verify_element_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        configvalues = readconfig.configvalues
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                input=input[0]
                if input is not None:
                    util = UtilWebKeywords()
                    if not(util.is_visible(webelement)) and configvalues['ignoreVisibilityCheck'].strip().lower() == "yes":
                        text = browser_Keywords.local_bk.driver_obj.execute_script("""return arguments[0].innerText""",webelement)
                    else:
                        text=self.__getelement_text(webelement)
                    if text==input:
                       logger.print_on_console('Element Text matched')
                       local_eo.log.info('Element Text matched')
                       local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                       status=TEST_RESULT_PASS
                       methodoutput=TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Element Text mismatched')
                        local_eo.log.info('Element Text mismatched')
                        logger.print_on_console('Expected: ',input)
                        local_eo.log.info('Expected:')
                        local_eo.log.info(input)
                        logger.print_on_console('Actual: ',text)
                        local_eo.log.info('Actual:')
                        local_eo.log.info(text)
                else:
                    local_eo.log.error(INVALID_INPUT)
                    err_msg=INVALID_INPUT
                    logger.print_on_console(INVALID_INPUT)
            except Exception as e:
                local_eo.log.error(e)
                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        local_eo.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def click_element(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    local_eo.log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                    click_obj=ButtonLinkKeyword()
                    local_eo.log.debug('ButtonLinkKeyword object created to call the click method')
                    status,methodoutput,output,err_msg=click_obj.click(webelement)
                    local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    local_eo.log.error(ERR_DISABLED_OBJECT)
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    logger.print_on_console(ERR_DISABLED_OBJECT)
            except Exception as e:
                local_eo.log.error(e)

                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        local_eo.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def drag(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    local_eo.log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                    obj=Utils()
                    local_eo.log.debug('Utils object created to call the get_element_location method')
                     #find the location of the element w.r.t viewport
                    location=obj.get_element_location(webelement)
                    local_eo.log.info('location is :')
                    local_eo.log.info(location)
                    from selenium import webdriver
                    if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Firefox):
                        yoffset=browser_Keywords.local_bk.driver_obj.execute_script(MOUSE_HOVER_FF)
                        obj.mouse_move(int(location.get('x')+9),int(location.get('y')+yoffset))
                    else:
                        obj.enumwindows()
                        if len(obj.rect)>1:
                            obj.mouse_move(int(location.get('x')+9),int(location.get('y')+obj.rect[1]+6))
                        else:
                            err_msg='Element to be dragged should be on top'
                            local_eo.log.error=err_msg
                            logger.print_on_console(err_msg)
                    import time
                    time.sleep(0.5)
                    obj.mouse_press(LEFT_BUTTON)
                    local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    local_eo.log.error(ERR_DISABLED_OBJECT)
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    logger.print_on_console(ERR_DISABLED_OBJECT)
            except Exception as e:
                local_eo.log.error(e)
                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        local_eo.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def drop(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    local_eo.log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                    obj=Utils()
                    local_eo.log.debug('Utils object created to call the get_element_location method')
                     #find the location of the element w.r.t viewport
                    location=obj.get_element_location(webelement)
                    local_eo.log.info('location is :')
                    local_eo.log.info(location)
                    import time
                    time.sleep(0.5)
                    from selenium import webdriver
                    if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Firefox):
                        yoffset=browser_Keywords.local_bk.driver_obj.execute_script(MOUSE_HOVER_FF)
                        obj.slide(int(location.get('x')+9),int(location.get('y')+yoffset), 0);
                    else:
                        obj.enumwindows()
                        if len(obj.rect)>1:
                            obj.slide(int(location.get('x')+9),int(location.get('y')+obj.rect[1]+6), "slow")
                        else:
                            err_msg='Element to be dragged should be on top'
                            local_eo.log.error=err_msg
                            logger.print_on_console(err_msg)
                    time.sleep(0.5)
                    obj.mouse_release(LEFT_BUTTON)
                    local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    local_eo.log.error(ERR_DISABLED_OBJECT)
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    logger.print_on_console(ERR_DISABLED_OBJECT)
            except Exception as e:
                local_eo.log.error(e)

                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        local_eo.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg


    def get_tooltip_text(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        tool_tip=None
        err_msg=None
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
               tool_tip=self.__get_tooltip(webelement)
               if tool_tip is not None and tool_tip != '':
                   local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                   status=TEST_RESULT_PASS
                   methodoutput=TEST_RESULT_TRUE
               else:
                    tool_tip=None
                    err_msg = 'No tool tip text found'
               local_eo.log.info('Tool tip text is : ')
               local_eo.log.info(tool_tip)
##               logger.print_on_console('Tool tip text: '+str(tool_tip))
               logger.print_on_console('Tool tip text: ',tool_tip)
            except Exception as e:
                local_eo.log.error(e)
                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        local_eo.log.info(RETURN_RESULT)
        return status,methodoutput,tool_tip,err_msg


    def verify_tooltip_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        tool_tip = None
        if webelement is not None:
            try:
                input=input[0]
                if input is not None and input != '':
                    tool_tip=self.__get_tooltip(webelement)
                    if input==tool_tip:
                        logger.print_on_console('Tool tip Text matched')
                        local_eo.log.info('Tool tip Text matched')
                        local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Tool tip Text mismatched')
                        local_eo.log.info('Tool tip Text mismatched')
                        logger.print_on_console('Expected: ',input)
                        local_eo.log.info('Expected:')
                        local_eo.log.info(input)
                        logger.print_on_console('Actual: ',tool_tip)
                        local_eo.log.info('Actual:')
                        local_eo.log.info(tool_tip)
                else:
                    local_eo.log.error(INVALID_INPUT)
                    err_msg=INVALID_INPUT
                    logger.print_on_console(INVALID_INPUT)
            except Exception as e:
                local_eo.log.error(e)

                logger.print_on_console(e)
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        local_eo.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def waitforelement_visible(self,webelement,objectname,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        configvalues = readconfig.configvalues
        try:
            if objectname is not None:
                delay=int(configvalues['timeOut'])
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.common.exceptions import TimeoutException
                from selenium.webdriver.common.by import By
                element_present = EC.presence_of_element_located((By.XPATH, objectname))
                WebDriverWait(browser_Keywords.local_bk.driver_obj, delay).until(element_present)
                local_eo.log.info('Element is visible')
                logger.print_on_console('Element is visible')
                local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except TimeoutException as e:
            logger.print_on_console('Delay timeout exceeded')
            local_eo.log.error(e)

            logger.print_on_console(e)
            err_msg='Delay timeout exceeded'
        except Exception as e:
            local_eo.log.error(e)

            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        return status,methodoutput,output,err_msg

    def drop_file(self,webelement,inputs,*args):
        status = TEST_RESULT_FAIL
        methodoutput =TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        #upload_file keyword implementation
        try:
            filepath = inputs[0]
            filename = inputs[1]
            inputfile = filepath + '\\' + filename
            if webelement is not None:
                local_eo.log.info('Recieved web element from the web dispatcher')
                local_eo.log.debug(webelement)
                local_eo.log.debug('Check for the element enable')
                if webelement.is_enabled():
                    i = browser_Keywords.local_bk.driver_obj.execute_script(local_eo.DROP_JS,webelement,0,0)
                    i.send_keys(inputfile)
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
                else:
                    local_eo.log.info(WEB_ELEMENT_DISABLED)
                    err_msg = WEB_ELEMENT_DISABLED
                    logger.print_on_console(WEB_ELEMENT_DISABLED)
        except Exception as e:
            local_eo.log.error(e)
            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        local_eo.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg



