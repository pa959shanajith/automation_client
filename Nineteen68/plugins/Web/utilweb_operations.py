#-------------------------------------------------------------------------------
# Name:        utilweb_operations.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     08-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import logger
import browser_Keywords
from utils_web import Utils
from webconstants import *
from pyrobot import Robot
import win32gui
import pyrobot
import table_keywords
import time
import urllib, cStringIO
import logging
from constants import *

log = logging.getLogger('utilweb_operations.py')

class UtilWebKeywords:
    def __create_keyinfo_dict(self):
         self.keys_info['null']=Keys.NULL
         self.keys_info['cancel']=Keys.CANCEL
         self.keys_info['help']=Keys.HELP
         self.keys_info['backspace']=Keys.BACKSPACE
         self.keys_info['tab']=Keys.TAB
         self.keys_info['clear']=Keys.CLEAR
         self.keys_info['return']=Keys.RETURN
         self.keys_info['enter']=Keys.ENTER
         self.keys_info['control']=Keys.CONTROL
         self.keys_info['ctrl']=Keys.CONTROL
         self.keys_info['alt']=Keys.ALT
         self.keys_info['pause']=Keys.PAUSE
         self.keys_info['escape']=Keys.ESCAPE
         self.keys_info['space']=Keys.SPACE
         self.keys_info['pageup']=Keys.PAGE_UP
         self.keys_info['pagedown']=Keys.PAGE_DOWN
         self.keys_info['end']=Keys.END
         self.keys_info['home']=Keys.HOME
         self.keys_info['leftarrow']=Keys.LEFT
         self.keys_info['rightarrow']=Keys.RIGHT
         self.keys_info['uparrow']=Keys.UP
         self.keys_info['downarrow']=Keys.DOWN
         self.keys_info['insert']=Keys.INSERT
         self.keys_info['delete']=Keys.DELETE
         self.keys_info['semicolon']=Keys.SEMICOLON
         self.keys_info['equals']=Keys.EQUALS
         self.keys_info['numpad0']=Keys.NUMPAD0
         self.keys_info['numpad1']=Keys.NUMPAD1
         self.keys_info['numpad2']=Keys.NUMPAD2
         self.keys_info['numpad3']=Keys.NUMPAD3
         self.keys_info['numpad4']=Keys.NUMPAD4
         self.keys_info['numpad5']=Keys.NUMPAD5
         self.keys_info['numpad6']=Keys.NUMPAD6
         self.keys_info['numpad7']=Keys.NUMPAD7
         self.keys_info['numpad8']=Keys.NUMPAD8
         self.keys_info['numpad9']=Keys.NUMPAD9
         self.keys_info['f1']=Keys.F1
         self.keys_info['f2']=Keys.F2
         self.keys_info['f3']=Keys.F3
         self.keys_info['f4']=Keys.F4
         self.keys_info['f5']=Keys.F5
         self.keys_info['f6']=Keys.F6
         self.keys_info['f7']=Keys.F7
         self.keys_info['f8']=Keys.F8
         self.keys_info['f9']=Keys.F9
         self.keys_info['f10']=Keys.F10
         self.keys_info['f11']=Keys.F11
         self.keys_info['f12']=Keys.F12
         self.keys_info['multiply']=Keys.MULTIPLY
         self.keys_info['add']=Keys.ADD
         self.keys_info['subtract']=Keys.SUBTRACT
         self.keys_info['divide']=Keys.DIVIDE
         self.keys_info['separator']=Keys.SEPARATOR
         self.keys_info['decimal']=Keys.DECIMAL


    def __init__(self):
        self.keys_info={}
        self.__create_keyinfo_dict()

    def __web_driver_exception(self,e):
        log.error(e)
        logger.print_on_console(e)
        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        return err_msg

    def is_visible(self,webelement):
        flag=False
        log.debug('Checking the visibility of element')
        try:
            script="""var isVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && scomp.opacity != 1))) return false;                 sel = sel.parentNode;             }         }         return true;     } })(); var s = arguments[0]; return isVisible(s);"""
            flag= browser_Keywords.driver_obj.execute_script(script,webelement)
        except Exception as e:
            self.__web_driver_exception(e)
        log.debug('Visibility is '+str(flag))
        return flag


    def is_enabled(self,webelement):
        log.debug('Checking the enability of element')
        return webelement.is_enabled()

    def verify_visible(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                #call to highlight the webelement
                self.highlight(webelement)
                res=self.is_visible(webelement)
                log.info('The visible status is '+str(res))
                logger.print_on_console('The visible status is '+str(res))
                if res:
                    logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_VISIBLE'])
                    log.info(ERROR_CODE_DICT['ERR_OBJECT_VISIBLE'])
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    logger.print_on_console(err_msg)
                    log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg


    def verify_exists(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None and webelement != '':
                #call to highlight the webelement
                self.highlight(webelement)
                logger.print_on_console(ERROR_CODE_DICT['MSG_ELEMENT_EXISTS'])
                log.info(ERROR_CODE_DICT['MSG_ELEMENT_EXISTS'])
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
           err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def verify_doesnot_exists(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is None:
            logger.print_on_console(ERROR_CODE_DICT['ERR_ELEMENT_NOT_EXISTS'])
            log.info(ERROR_CODE_DICT['MSG_ELEMENT_EXISTS'])
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output,err_msg


    def verify_enabled(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                #call to highlight the webelement
                self.highlight(webelement)
                if webelement.is_enabled():
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                    info_msg=ERROR_CODE_DICT['MSG_OBJECT_ENABLED']
                    logger.print_on_console(err_msg)
                    log.info(info_msg)
                else:
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    logger.print_on_console(err_msg)
                    log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def verify_disabled(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                #call to highlight the webelement
                self.highlight(webelement)
                if not(webelement.is_enabled()):
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                    info_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    logger.print_on_console(info_msg)
                    log.info(info_msg)
                else:
                    err_msg=ERROR_CODE_DICT['MSG_OBJECT_ENABLED']
                    logger.print_on_console(err_msg)
                    log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def verify_hidden(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                res=self.is_visible(webelement)
                if not(res):
                    info_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    logger.print_on_console(info_msg)
                    log.info(info_msg)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_OBJECT_VISIBLE']
                    logger.print_on_console(err_msg)
                    log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def verify_readonly(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                #call to highlight the webelement
                self.highlight(webelement)
                readonly_value=webelement.get_attribute("readonly")
                if readonly_value is not None and readonly_value.lower() =='true' or readonly_value is '':
                    info_msg=ERROR_CODE_DICT['ERR_ELEMENT_IS_READONLY']
                    logger.print_on_console(info_msg)
                    log.info(info_msg)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_ELEMENT_IS_NOT_READONLY']
                    logger.print_on_console(err_msg)
                    log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg


    def highlight(self,webelement):
        try:
            if browser_Keywords.driver_obj is not None:
                browser_info=browser_Keywords.driver_obj.capabilities
                browser_name=browser_info.get('browserName')
                browser_version=browser_info.get('version')
                log.info('Browser is:'+browser_name+'Version is:'+browser_version)
                #get the original style of the element
                original_style = webelement.get_attribute('style')
                #Apply css to the element
                #check if driver instance is IE
                if isinstance(browser_Keywords.driver_obj,webdriver.Ie):
                    browser_Keywords.driver_obj.execute_script(HIGHLIGHT_SCRIPT_IE,webelement,original_style+APPLY_CSS)
                else:
                    browser_Keywords.driver_obj.execute_script(HIGHLIGHT_SCRIPT,webelement,original_style+APPLY_CSS)

                #highlight remains for 3 secs on the element
                import time
                time.sleep(3)

                #Remove css from the element  and applying the original style back to the element
                #check if driver instance is IE
                if isinstance(browser_Keywords.driver_obj,webdriver.Ie):
                    if '8' in browser_version:
                        browser_Keywords.driver_obj.execute_script(HIGHLIGHT_SCRIPT_IE,webelement,original_style+REMOVE_CSS_IE8)
                    else:
                        browser_Keywords.driver_obj.execute_script(HIGHLIGHT_SCRIPT_IE,webelement,original_style)
                else:
                    browser_Keywords.driver_obj.execute_script(HIGHLIGHT_SCRIPT,webelement,original_style)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)


    def __setfocus(self,webelement):
        status=TEST_RESULT_FAIL
        if browser_Keywords.driver_obj is not None:
            browser_Keywords.driver_obj.execute_script(FOUCS_ELE,webelement)
            status=TEST_RESULT_PASS
        return status

    def setfocus(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                status=self.__setfocus(webelement)
                if status==TEST_RESULT_PASS:
                    info_msg='Element is focused'
                    log.info(info_msg)
                    logger.print_on_console(info_msg)
                    methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg



    def mouse_hover(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                obj=Utils()
                 #find the location of the element w.r.t viewport
                location=obj.get_element_location(webelement)
                logger.print_on_console('location is '+str(location))
                if isinstance(browser_Keywords.driver_obj,webdriver.Firefox):
                    yoffset=browser_Keywords.driver_obj.execute_script(MOUSE_HOVER_FF)
                    logger.print_on_console('y offset is '+str(yoffset))
                    obj.mouse_move(int(location.get('x')+9),int(location.get('y')+yoffset))
                else:
                    obj.enumwindows()
                    obj.mouse_move(int(location.get('x')+9),int(location.get('y')+obj.rect[1]+6))
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg




    def tab(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                webelement.send_keys(Keys.TAB)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except WebDriverException as e:
            if isinstance(browser_Keywords.driver_obj,webdriver.Chrome):
                self.__setfocus(webelement)
                robot=Robot()
                robot.key_press('tab')
                robot.key_release('tab')
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output,err_msg

    def generic_sendfucntion_keys(self,input,*args):
        from sendfunction_keys import SendFunctionKeys
        obj=SendFunctionKeys()
        obj.sendfunction_keys(input,*args)


    def sendfunction_keys(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                input=input[0]
                info_msg='Focus the given webelement '+webelement.tag_name+' before sending keys'
                log.info(info_msg)
                logger.print_on_console(info_msg)
                self.__setfocus(webelement)
                if len(args)==0 and input in self.keys_info.keys():
                    if webelement.get_attribute('type')!='text':
                        webelement.send_keys(self.keys_info[input.lower()])
                        log.debug('It is not a textbox')
                    else:
                        log.debug('It is a textbox')
                        self.generic_sendfucntion_keys(input.lower(),*args)
                else:
                    log.debug('Calling Generic sendfunction keys')
                    self.generic_sendfucntion_keys(input.lower(),*args)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def rightclick(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                if webelement.is_enabled():
                    log.debug(WEB_ELEMENT_ENABLED)
                    from selenium.webdriver.common.action_chains import ActionChains
                    action_obj=ActionChains(browser_Keywords.driver_obj)
                    action_obj.context_click(webelement).perform()
                    log.debug('Performed Right click')
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def switch_to_window(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            input=input[0]
            logger.print_on_console(INPUT_IS+input)
            input=float(str(input))
            if not(input is None or int(input) <0):
                to_window=int(input)
                log.info('Switching to the window ')
                log.info(to_window)
                window_handles=self.__get_window_handles()
                log.info('The available window handles are ')
                log.info(window_handles)
                cur_handle=browser_Keywords.driver_obj.current_window_handle
                from_window=-1
                if cur_handle in window_handles:
                    from_window=window_handles.index(cur_handle)+1
                    log.info('Switching from the window')
                    log.info(from_window)
                if from_window>-1:
                    browser_Keywords.driver_obj.switch_to.window(window_handles[to_window-1])
                    logger.print_on_console('Switched to window handle'+browser_Keywords.driver_obj.current_window_handle)
                    logger.print_on_console('Control switched from window ' + str(from_window)
							+ " to window " + str(to_window))
                else:
                    err_msg='Current window handle not found'
                    logger.print_on_console(err_msg)
                    log.error(err_msg)

            else:
                logger.print_on_console(INVALID_INPUT)
                err_msg=INVALID_INPUT
                log.error(INVALID_INPUT)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            etype=type(e)
            err_msg=self.__web_driver_exception(e)
            log.info('Inside Exception block')
            try:
                if isinstance(etype,NoSuchWindowException):
                    window_handles=self.__get_window_handles()
                    log.info('Current window handles are ')
                    log.info(window_handles)
                    log.debug(len(window_handles))
                    if len(window_handles)>0:
                        total_handles=len(window_handles)
                        browser_Keywords.driver_obj.switch_to.window(window_handles[total_handles-1])
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg='No handles found'
                        logger.print_on_console(err_msg)
                        log.error(err_msg)
            except Exception as e:
                etype=type(e)
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def mouse_click(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement !=None:
                log.info(INPUT_IS)
                log.info(input)
                if not(input is None ):
                    row_num=int(input[0])
                    col_num=int(input[1])
                    table_keywords_obj=table_keywords.TableOperationKeywords()
                    actual_xpath=table_keywords_obj.getElemntXpath(webelement)
                    element = browser_Keywords.driver_obj.find_element_by_xpath(actual_xpath)
                    cell=table_keywords_obj.javascriptExecutor(element,row_num-1,col_num-1)
                    ele_coordinates=cell.location_once_scrolled_into_view
                    log.debug(ele_coordinates)
                    hwnd=win32gui.GetForegroundWindow()
                    log.debug('Handle found ')
                    log.debug(hwnd)
                    if isinstance(browser_Keywords.driver_obj,webdriver.Firefox):
                        info_msg='Firefox browser'
                        log.info(info_msg)
                        logger.print_on_console(info_msg)
                        javascript = "return window.mozInnerScreenY"
                        value=browser_Keywords.driver_obj.execute_script(javascript)
                        offset=int(value)
                        robot=pyrobot.Robot()
                        robot.set_mouse_pos(ele_coordinates.get('x')+9,ele_coordinates.get('y')+offset)
                        log.debug('Setting the mouse position')
                        robot.mouse_down('left')
                        log.debug('Mouse click performed')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        utils=Utils()
                        utils.enumwindows()
                        rect=utils.rect
                        robot=pyrobot.Robot()
                        log.debug('Setting the mouse position')
                        robot.set_mouse_pos(ele_coordinates.get('x')+9,ele_coordinates.get('y')+rect[0])
                        robot.mouse_down('left')
                        log.debug('Mouse click performed')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def verify_web_images(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            from PIL import Image
            img_src = webelement.get_attribute("src")
            file1 = cStringIO.StringIO(urllib.urlopen(img_src).read())
            file2=input[0]
            log.info(INPUT_IS)
            log.info(file2)
            if file1 != None and file2 != None and  file2 != '' and os.path.exists(file2) :
                from PIL import Image
                img1 = Image.open(file1)
                img2 = Image.open(file2)
                if img1==img2:
                    info_msg=ERROR_CODE_DICT['MSG_IMAGE_COMPARE_PASS']
                    logger.print_on_console(info_msg)
                    methodoutput=TEST_RESULT_TRUE
                    status=TEST_RESULT_PASS
                else:
                    err_msg=ERROR_CODE_DICT['ERR_IMAGE_COMPARE_FAIl']
            else:
                err_msg=ERROR_CODE_DICT['ERR_NO_IMAGE_SOURCE']
            if err_msg != None:
                logger.print_on_console(err_msg)
                log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def __get_window_handles(self):
        window_handles=browser_Keywords.driver_obj.window_handles
        window_handles=browser_Keywords.driver_obj.window_handles
        logger.print_on_console('Window handles size '+str(len(window_handles)))
        return window_handles



