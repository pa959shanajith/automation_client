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
import os
from selenium import webdriver
from utils_web import Utils
from utilweb_operations import UtilWebKeywords
from button_link_keyword import ButtonLinkKeyword
import browser_Keywords
from webconstants import *
import ast
import time
import readconfig
import time

import logging
from constants import *
import threading
local_eo = threading.local()
##DROP_JS = """var target = arguments[0],     offsetX = arguments[1],     offsetY = arguments[2],     document = target.ownerDocument || document,     window = document.defaultView || window;  var input = document.createElement('INPUT'); input.type = 'file'; input.style.display = 'none'; input.onchange = function() {     target.scrollIntoView(true);      var rect = target.getBoundingClientRect(),         x = rect.left + (offsetX || (rect.width >> 1)),         y = rect.top + (offsetY || (rect.height >> 1)),         dataTransfer = {             files: this.files         };      ['dragenter', 'dragover', 'drop'].forEach(function(name) {         var evt = document.createEvent('MouseEvent');         evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);         evt.dataTransfer = dataTransfer;         target.dispatchEvent(evt);     });      setTimeout(function() {         document.body.removeChild(input);     }, 25); }; document.body.appendChild(input); return input;"""
##log = logging.getLogger('element_operations.py')

class ElementKeywords:
    def __init__(self):
        global local_eo
        #local_eo.DROP_JS = """var target = arguments[0],     offsetX = arguments[1],     offsetY = arguments[2],     document = target.ownerDocument || document,     window = document.defaultView || window;  var input = document.createElement('INPUT'); input.type = 'file'; input.style.display = 'none'; input.onchange = function() {     target.scrollIntoView(true);      var rect = target.getBoundingClientRect(),         x = rect.left + (offsetX || (rect.width >> 1)),         y = rect.top + (offsetY || (rect.height >> 1)),         dataTransfer = {             files: this.files         };      ['dragenter', 'dragover', 'drop'].forEach(function(name) {         var evt = document.createEvent('MouseEvent');         evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);         evt.dataTransfer = dataTransfer;         target.dispatchEvent(evt);     });      setTimeout(function() {         document.body.removeChild(input);     }, 25); }; document.body.appendChild(input); return input;"""
        local_eo.DROP_JS="""var c=arguments,b=c[0],k=c[1];c=c[2];for(var d=b.ownerDocument||document,l=0;;){var e=b.getBoundingClientRect(),g=e.left+(k||e.width/2),h=e.top+(c||e.height/2),f=d.elementFromPoint(g,h);if(f&&b.contains(f))break;if(1<++l)throw b=Error('Element not interactable'),b.code=15,b;b.scrollIntoView({behavior:'instant',block:'center',inline:'center',display:'none'})}var a=d.createElement('INPUT');a.setAttribute('type','file');a.setAttribute('multiple','');a.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;display:none;');a.onchange=function(b){a.parentElement.removeChild(a);b.stopPropagation();var c={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:a.files,setData:function(){},getData:function(){},clearData:function(){},setDragImage:function(){}};window.DataTransferItemList&&(c.items=Object.setPrototypeOf(Array.prototype.map.call(a.files,function(a){return{constructor:DataTransferItem,kind:'file',type:a.type,getAsFile:function(){return a},getAsString:function(b){var c=new FileReader;c.onload=function(a){b(a.target.result)};c.readAsText(a)}}}),{constructor:DataTransferItemList,add:function(){},clear:function(){},remove:function(){}}));['dragenter','dragover','drop'].forEach(function(a){var b=d.createEvent('DragEvent');b.initMouseEvent(a,!0,!0,d.defaultView,0,0,0,g,h,!1,!1,!1,!1,0,null);Object.setPrototypeOf(b,null);b.dataTransfer=c;Object.setPrototypeOf(b,DragEvent.prototype);f.dispatchEvent(b)})};d.documentElement.appendChild(a);a.getBoundingClientRect();return a;"""
        local_eo.log = logging.getLogger('element_operations.py')

    def __getelement_text(self,webelement):
##        # Fixed issue #311
        text=''
        try:
            text = webelement.text
            if text is None or text is '':
                text=webelement.get_attribute('value')
                local_eo.log.debug('Element text found by Attribute value')
            if text is None or text is '':
                text=webelement.get_attribute('name')
                local_eo.log.debug('Element text found by Attribute name')
            if text is None or text is '':
                text=self.__get_tooltip(webelement)
            if text is None or text is '':
                text=webelement.get_attribute('placeholder')
                local_eo.log.debug('Element text found by Attribute placeholder')
            if text is None or text is '':
                text=webelement.get_attribute('href')
                local_eo.log.debug('Element text found by Attribute href')
        except Exception as e:
            local_eo.log.error(e)
            logger.print_on_console(e)
        return text

    def __get_tooltip(self,webelement):
        text=''
        try:
            text = webelement.get_attribute('title')
            if text : local_eo.log.debug('Element text found by tooltip-Attribute title')
            if text is None or text is '':
                text = webelement.get_attribute('data-original-title')
                if text is None or text is '':
                    try:
                        #Adding mutation observer to detect the tool tip element on appearance
                        browser_Keywords.local_bk.driver_obj.execute_script("""
                        j='';
                        observer = new MutationObserver((mutations)=>{
                        if (mutations[0].addedNodes.length)
                            j = (mutations[0].addedNodes[0].textContent);
                        });
                                                                            
                        observer.observe(document.body, {attributes: false, childList: true, characterData: false, subtree:true});
                        """)

                        #Performing mousehover through action chains class of selenium

                        hover = webdriver.ActionChains(browser_Keywords.local_bk.driver_obj).move_to_element(webelement)
                        hover.perform()

                        #Retreiving the tooltip
                        t=0
                        while((text==None or text=='') and t<10):
                            text = browser_Keywords.local_bk.driver_obj.execute_script("""
                            console.log(j);
                            return j;""")
                            time.sleep(0.5)
                            t=t+0.5


                        if text : local_eo.log.debug('Tooltip is through dynamic element. Captured using mutation observer.')

                    except Exception as e:
                        local_eo.log.error(e)
                        err_msg=self.__web_driver_exception(e)
                        logger.print_on_console("Error in adding mutation observer.")
                else:
                    local_eo.log.debug('Element text found by tooltip-Attribute data-original-title')
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
        delayconst = int(configvalues['element_load_timeout'])
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                util = UtilWebKeywords()
                for i in range(delayconst):
                    if not(util.is_visible(webelement)) and configvalues['ignoreVisibilityCheck'].strip().lower() == "yes":
                        local_eo.log.debug('element is invisible, performing js code')
                        text = browser_Keywords.local_bk.driver_obj.execute_script("""return arguments[0].innerText""",webelement)
                    else:
                        if(util.is_visible(webelement)):
                            text = webelement.get_attribute('innerText')
                            if text.find('\xa0')!=-1:text=text.replace('\xa0'," ")
                            # text=self.__getelement_text(webelement)
                            if text.find('\n')!=-1:
                                local_eo.log.debug("\\n detected. Fetching text using element.text method")
                                text = webelement.text
                        elif i+1 == delayconst:
                            err_msg = 'Element is not displayed'
                            logger.print_on_console('Element is not displayed')
                            local_eo.log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
                    if text:
                        logger.print_on_console('Element text: ',text)
                        local_eo.log.info('Element text: ')
                        local_eo.log.info(text)
                        local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                        status=TEST_RESULT_PASS
                        result=TEST_RESULT_TRUE
                        methodoutput=TEST_RESULT_TRUE
                        break
                    else:
                        time.sleep(1)
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
        delayconst = int(configvalues['element_load_timeout'])
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                input=input[0]
                if input.find('\xa0')!=-1:
                    input = input.replace("\xa0"," ")
                if input is not None:
                    util = UtilWebKeywords()
                    for i in range(delayconst):
                        if not(util.is_visible(webelement)) and configvalues['ignoreVisibilityCheck'].strip().lower() == "yes":
                            text = browser_Keywords.local_bk.driver_obj.execute_script("""return arguments[0].innerText""",webelement)
                        else:
                            text = webelement.get_attribute('innerText')
                            if text is None or text is '': 
                                local_eo.log.debug('Element Attribute not found,fetching with __getelement_text function')
                                text=self.__getelement_text(webelement)
                        if text is not None and text.find('\xa0') != -1: text = text.replace("\xa0", " ")
                        if text is not None and text.find('\n') != -1:
                            local_eo.log.debug("\\n detected. Fetching text using element.text method")
                            text = webelement.text
                        if text and text == input:
                            break
                        else:
                            time.sleep(1)
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
                    status,methodoutput,output,err_msg=click_obj.click(webelement,args[0])
                    #local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                    #status=TEST_RESULT_PASS
                    #methodoutput=TEST_RESULT_TRUE
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
                    if SYSTEM_OS == 'Darwin' or SYSTEM_OS == 'Windows':
                        local_eo.log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                        obj=Utils()
                        local_eo.log.debug('Utils object created to call the get_element_location method')
                        #find the location of the element w.r.t viewport
                        if webelement.is_displayed():
                            location=webelement.location
                        else:
                            location=obj.get_element_location(webelement)
                        size=webelement.size
                        local_eo.log.info('location is :')
                        local_eo.log.info(location)
                        if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Firefox):
                            yoffset=browser_Keywords.local_bk.driver_obj.execute_script(MOUSE_HOVER_FF)
                            obj.mouse_move(int(location.get('x')+9),int(location.get('y')+yoffset+6))
                        elif isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Ie):
                            offset = browser_Keywords.local_bk.driver_obj.execute_script("return window.outerHeight - window.innerHeight;")
                            if offset>0:
                                height=int(size.get('height')/2)
                                width=int(size.get('width')/2)
                                obj.mouse_move(int(location.get('x')+width),int(location.get('y')+offset+height-14))
                            else:
                                err_msg='Element to be dragged should be on top'
                                local_eo.log.error=err_msg
                                logger.print_on_console(err_msg)
                        else:
                            offset = browser_Keywords.local_bk.driver_obj.execute_script("return window.outerHeight - window.innerHeight;")
                            if offset>0:
                                height=int(size.get('height')/2)
                                width=int(size.get('width')/2)
                                obj.mouse_move(int(location.get('x')+width),int(location.get('y')+offset+height))
                            else:
                                err_msg='Element to be dragged should be on top'
                                local_eo.log.error=err_msg
                                logger.print_on_console(err_msg)
                        time.sleep(0.5)
                        obj.mouse_press(LEFT_BUTTON)
                        local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        import pyautogui as pag
                        if webelement.is_displayed():
                            location=webelement.location
                        else:
                            location=webelement.loaction_once_scrolled_into_view
                        size=webelement.size
                        local_eo.log.info('location is :')
                        local_eo.log.info(location)
                        if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Firefox):
                            yoffset=browser_Keywords.local_bk.driver_obj.execute_script(MOUSE_HOVER_FF)
                            pag.moveTo(int(location.get('x')+9),int(location.get('y')+yoffset+6))
                        else:
                            height=int(size.get('height')/2)
                            width=int(size.get('width')/2)
                            local_eo.log.info(width)
                            local_eo.log.info(height)
                            pag.moveTo(int(location.get('x')),int(location.get('y')+height))
                        time.sleep(0.5)
                        pag.mouseDown(button='left')
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
                    if SYSTEM_OS == 'Windows' or SYSTEM_OS == 'Darwin':
                        local_eo.log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                        obj=Utils()
                        local_eo.log.debug('Utils object created to call the get_element_location method')
                         #find the location of the element w.r.t viewport
                        if webelement.is_displayed():
                            location=webelement.location
                        else:
                            location=obj.get_element_location(webelement)
                        size=webelement.size
                        local_eo.log.info('location is :')
                        local_eo.log.info(location)
                        if len(args[0]) > 0:
                            if(args[0][0]!=''):
                                time1=float(args[0][0])
                                time.sleep(time1)
                            else:
                                time.sleep(0.5)
                        else:
                            time.sleep(0.5)
                        if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Firefox):
                            yoffset=browser_Keywords.local_bk.driver_obj.execute_script(MOUSE_HOVER_FF)
                            obj.slide(int(location.get('x')+9),int(location.get('y')+yoffset+6), 0)
                        elif isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Ie):
                            obj.enumwindows()
                            if len(obj.rect)>1:
                                height=int(size.get('height')/2)
                                width=int(size.get('width')/2)
                                obj.slide(int(location.get('x')+width),int(location.get('y')+obj.rect[1]+height+6), "slow")
                            else:
                                err_msg='Element to be dragged should be on top'
                                local_eo.log.error=err_msg
                                logger.print_on_console(err_msg)
                        else:
                            obj.enumwindows()
                            if len(obj.rect)>1:
                                height=int(size.get('height')/2)
                                width=int(size.get('width')/2)
                                obj.slide(int(location.get('x')+width),int(location.get('y')+obj.rect[1]+height), "slow")
                            else:
                                err_msg='Element to be dragged should be on top'
                                local_eo.log.error=err_msg
                                logger.print_on_console(err_msg)
                        if len(args[0]) > 0:
                            if(args[0][0]!=''):
                                time1=float(args[0][0])
                                time.sleep(time1)
                            else:
                                time.sleep(0.5)
                        else:
                            time.sleep(0.5)
                        obj.mouse_release(LEFT_BUTTON)
                        local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    if SYSTEM_OS =='Linux':
                        local_eo.log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                        local_eo.log.debug('Utils object created to call the get_element_location method')
                        if webelement.is_displayed():
                            location=webelement.location
                        else:
                            location=webelement.loaction_once_scrolled_into_view
                        size=webelement.size
                        local_eo.log.info('location is :')
                        local_eo.log.info(location)
                        if len(args[0]) > 0:
                            if(args[0][0]!=''):
                                time1=float(args[0][0])
                                time.sleep(time1)
                            else:
                                time.sleep(0.5)
                        else:
                            time.sleep(0.5)
                        obj=Utils()
                        import pyautogui as pag
                        if isinstance(browser_Keywords.local_bk.driver_obj, webdriver.Firefox):
                            yoffset=browser_Keywords.local_bk.driver_obj.execute_script(MOUSE_HOVER_FF)
                            obj.slide_linux(int(location.get('x')+9),int(location.get('y')+yoffset+6), 0)
                        else:
                            height=int(size.get('height')/2)
                            width=int(size.get('width')/2)
                            local_eo.log.info(width)
                            local_eo.log.info(height)
                            obj.slide_linux(int(location.get('x')),int(location.get('y')+height), 0)
                        if len(args[0]) > 0:
                            if(args[0][0]!=''):
                                time1=float(args[0][0])
                                time.sleep(time1)
                            else:
                                time.sleep(0.5)
                        else:
                            time.sleep(0.5)
                        pag.mouseUp(button='left')
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
        dynamic_tooltip=False
        if webelement is not None:
            try:
                if len(input)==2 and input[1]!="":
                    coords=ast.literal_eval(input[1])
                    x, y=int(coords[0]), int(coords[1])
                    input.pop()
                    dynamic_tooltip=True
                input=input[0]
                if input is not None and input != '':
                    if dynamic_tooltip:
                        tool_tip,err_msg=self.__get_ag_grid_tooltip_text(webelement,x,y)
                        if tool_tip!=None and '\n' in tool_tip:
                            tool_tip=tool_tip.replace("\n","")
                            tool_tip=tool_tip.replace(" ","")
                            input=input.replace(" ","")
                    else:
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
            err_msg=ERROR_CODE_DICT['ERR_TIMEOUT_EXCEEDED']
            logger.print_on_console(err_msg)
            local_eo.log.error(err_msg)
            local_eo.log.debug(e,exc_info=True)
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            local_eo.log.error(err_msg)
            logger.print_on_console(err_msg)
            local_eo.log.debug(e,exc_info=True)
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
            inputfile = filepath + os.sep + filename
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

    def get_ag_grid_tooltip_text(self,webelement,*args):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        text = None
        err_msg = None
        tooltip_text = None
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if args[0]!=['']:    
                coords = ast.literal_eval(args[0][0])
                x,y=int(coords[0]),int(coords[1])  
            tooltip_text,err_msg = self.__get_ag_grid_tooltip_text(webelement,x,y)
            if text != None or text != '':
                local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            else:
                if err_msg!=None:
                    err_msg = "Not able to fetch the dynamic ag-grid tooltip text "
                logger.print_on_console(err_msg)
        except Exception as e:
            local_eo.log.debug("Exception occured on getting the ag-grid tooltip")
            local_eo.log.error(e)
            err_msg="Please provide valid input"
        return status, methodoutput, tooltip_text, err_msg
    
    def __get_ag_grid_tooltip_text(self,webelement,x=None,y=None):
        """ Refrenced in get_ag_grid_tooltip_text and verify_tooltip_text
        This method is used to fetch the tooltip text of an grid element that does not have tittle or other attribute which renders the 
        tooltip.
        Usually a new element get appended in the DOM which renders the text for the tooltip.
        Mandatory mousehover is perfomed using selenium action chains so that the element gets appended in the DOM.
        ADD_OBS_JS attaches an mutationObserver constructor to the body of the html DOM and monitors any element that gets attached while 
        hover is performed.
        REMOVE_OBS_JS removes the mutationObserver from the DOM and returns the element texzt that it captured
        """
        local_eo.log.debug("Executing __get_ag_grid_tooltip_text")
        text=None
        err_msg=None
        try:
            if x is not None and y is not None:
                if webelement is not None :
                    import pyautogui 
                    curr_x,curr_y=pyautogui.position()
                    if curr_x-3<=x<=curr_x+3 and curr_y-3<=y<=curr_y+3:
                        pyautogui.FAILSAFE = False
                        pyautogui.moveTo(0,0)
                        time.sleep(2)
                    local_eo.log.debug("Finding tooltip for grid based")
                    ADD_OBS_JS = """console.log("Adding observation JS");try {window.texts = [];let config = {attributes: false,childList: true,subtree:true};const callback = function (mutationsList, observer) {for (const mutation of mutationsList) {if (mutation.type === 'childList' && mutation != undefined && mutation.addedNodes.length > 0) {console.log('A child node has been added or removed.');if(mutation.addedNodes[0].innerText!= undefined && mutation.addedNodes[0].innerText !=''){window.texts.push(mutation.addedNodes[0].innerText);}                                      }}};const observer = new MutationObserver(callback);observer.observe(document.body, config); window.obs = observer;} catch (err) {console.log("Error occured in ADD_OBS_JS");console.log(err);}"""
                    local_eo.log.debug("Initialzed ADD_OBS_JS")
                    import browser_Keywords
                    from utils_web import Utils
                    obj=Utils()
                    local_eo.log.debug("Imported browser_Keywords")
                    webdriver = browser_Keywords.local_bk.driver_obj
                    local_eo.log.debug("browser_Keywords.local_bk.driver_obj")
                    webdriver.execute_script(ADD_OBS_JS)
                    time.sleep(1)
                    local_eo.log.debug("Added ADD_OBS_JS")
                    REMOVE_OBS_JS = """try{window.obs.disconnect();console.log(window.texts);for(let i = 0;i<window.texts.length; i++){return window.texts;}}catch (err){console.log("Error occured in REMOVE_OBS_JS");console.log(err);}"""
                    local_eo.log.debug("Initialized REMOVE_OBS_JS")
                    obj.mouse_move(int(x),int(y))
                    # noticed that in client webpage its taking time to return the tooltip text from the JS code
                    time.sleep(3)
                    local_eo.log.debug("Performed ActionChains")
                    element_added = webdriver.execute_script(REMOVE_OBS_JS)
                    local_eo.log.debug("Removed observation from browser using JS")
                    if element_added!=None:
                        text = element_added[0]
                        local_eo.log.info(text)
                    else:
                        err_msg="dynamic ToolTip text not fetched"
                else:
                    err_msg="Element is not present"  
            else:
                err_msg="Please input the coordinates"
        except Exception as e:
            local_eo.log.debug("Exception occured in __get_ag_grid_tooltip_text")
            local_eo.log.error(e)
        return text, err_msg

    def get_child_element_count(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            local_eo.log.info('Recieved web element from the web dispatcher')
            if webelement.is_enabled():
                try:
                    if args[0][0]=="":
                        totalcount = browser_Keywords.local_bk.driver_obj.execute_script("""return arguments[0].childElementCount""",webelement)
                        local_eo.log.info('Number of child element is')
                        local_eo.log.info(totalcount)
                        if totalcount is not None:
                            output = str(totalcount)
                            status = TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                            logger.print_on_console('Number of child element is: ',output)
                            local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        op_list=[]
                        child_elements = browser_Keywords.local_bk.driver_obj.execute_script("""return arguments[0].children""",webelement)
                        for i in child_elements:
                            op_list.append(i.tag_name)
                        if len(op_list)!=0:
                            output=op_list.count(args[0][0])
                            if output>0:
                                local_eo.log.info('number of '+ args[0][0] +'is')
                                local_eo.log.info(child_elements)
                                logger.print_on_console('Number of '+ args[0][0] +' is: ',output)
                                local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                                status = TEST_RESULT_PASS
                                methodoutput = TEST_RESULT_TRUE
                            else:
                                local_eo.log.error(INVALID_INPUT)
                                err_msg=INVALID_INPUT
                                logger.print_on_console(INVALID_INPUT)
                except Exception as e:
                    local_eo.log.error(e)
                    logger.print_on_console(e)
        return status,methodoutput,output,err_msg

    def get_child_elements(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_eo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            local_eo.log.info('Recieved web element from the web dispatcher')
            if webelement.is_enabled():
                try:
                    if args[0][0]!="":
                        op_list=[]
                        child_elements = browser_Keywords.local_bk.driver_obj.execute_script("""return arguments[0].children""",webelement)
                        for i in child_elements:
                            op_list.append(i.tag_name)
                        if len(op_list)!=0:
                            if args[0][0].lower()=='tag':
                                output = op_list
                                status = TEST_RESULT_PASS
                                methodoutput = TEST_RESULT_TRUE
                                local_eo.log.info('Child elements are')
                                local_eo.log.info(child_elements)
                                local_eo.log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                local_eo.log.error(INVALID_INPUT)
                                err_msg=INVALID_INPUT
                                logger.print_on_console(INVALID_INPUT)
                    else:
                        err_msg="Input is empty, Please provide the valid input"
                        local_eo.log.error(err_msg)
                        logger.print_on_console(err_msg)
                except Exception as e:
                    local_eo.log.error(e)
                    logger.print_on_console(e)
        return status,methodoutput,output,err_msg