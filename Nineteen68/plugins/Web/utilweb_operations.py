#-------------------------------------------------------------------------------
# Name:        module1
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
import Exceptions
import logger
import browser_Keywords
from sendfunction_keys import SendFunctionKeys
from utils_web import Utils
from webconstants import *
from pyrobot import Robot
import win32gui

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

    def is_visible(self,webelement):
        flag=False
        try:
            script="""var isVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && scomp.opacity != 1))) return false;                 sel = sel.parentNode;             }         }         return true;     } })(); var s = arguments[0]; return isVisible(s);"""
            flag= browser_Keywords.driver_obj.execute_script(script,webelement)
        except Exception as e:
            Exceptions.error(e)
        return flag


    def is_enabled(self,webelement):
        return webelement.is_enabled()

    def verify_visible(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        print 'webelement',webelement
        try:
            if webelement is not None:
                #call to highlight the webelement
                self.highlight(webelement)
                status=self.is_visible(webelement)
                if status:
                    logger.log('Element is visible')
                    status=str(status)
                    methodoutput=TEST_RESULT_TRUE
                else:
                    logger.log('Element is not visible')
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput


    def verify_exists(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if webelement is not None:
                #call to highlight the webelement
                self.highlight(webelement)
                logger.log('Element exists')
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def verify_doesnot_exists(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        if webelement is None:
            logger.log('Element does not exists')
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        return status,methodoutput


    def verify_enabled(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if webelement is not None:
                #call to highlight the webelement
                self.highlight(webelement)
                if webelement.is_enabled():
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                    logger.log('Element is enabled')
                else:
                    logger.log('Element is not enabled')
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def verify_disabled(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if webelement is not None:
                #call to highlight the webelement
                self.highlight(webelement)
                if not(webelement.is_enabled()):
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                    logger.log('Element is disabled')
                else:
                    logger.log('Element is not disabled')
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def verify_hidden(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if webelement is not None:
                status=self.is_visible(webelement)
                if not(status):
                    logger.log('Element is hidden')
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    logger.log('Element is not hidden')
                    status=TEST_RESULT_FAIL
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def verify_readonly(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if webelement is not None:
                #call to highlight the webelement
                self.highlight(webelement)
                readonly_value=webelement.get_attribute("readonly")
                if readonly_value is not None and readonly_value.lower() =='true' or readonly_value is '':
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    logger.log('Element is not readonly')
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def highlight(self,webelement):
        try:
            if browser_Keywords.driver_obj is not None:
                browser_info=browser_Keywords.driver_obj.capabilities
                browser_name=browser_info.get('browserName')
                browser_version=browser_info.get('version')
                logger.log('Browser is:'+browser_name+'Version is:'+browser_version)
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
            Exceptions.error(e)


    def __setfocus(self,webelement):
        status=TEST_RESULT_FAIL
        if browser_Keywords.driver_obj is not None:
            browser_Keywords.driver_obj.execute_script(FOUCS_ELE,webelement)
            status=TEST_RESULT_PASS
        return status

    def setfocus(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if webelement is not None:
                status=self.__setfocus(webelement)
                if status==TEST_RESULT_PASS:
                    methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput



    def mouse_hover(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if webelement is not None:
                obj=Utils()
                 #find the location of the element w.r.t viewport
                location=obj.get_element_location(webelement)
                logger.log('location is '+str(location))
                if isinstance(browser_Keywords.driver_obj,webdriver.Firefox):
                    yoffset=browser_Keywords.driver_obj.execute_script(MOUSE_HOVER_FF)
                    logger.log('y offset is '+str(yoffset))
                    obj.mouse_move(int(location.get('x')+9),int(location.get('y')+yoffset))
                else:
                    obj.enumwindows()
                    obj.mouse_move(int(location.get('x')+9),int(location.get('y')+obj.rect[1]+6))
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput




    def tab(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
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
        return status,methodoutput

    def sendfunction_keys(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if webelement is not None:
                input=input[0]
                self.__setfocus(webelement)
                if len(args)==0 and input in self.keys_info.keys():
                    webelement.send_keys(self.keys_info[input.lower()])
                else:
                    obj=SendFunctionKeys()
                    import time
                    time.sleep(2)
                    obj.sendfunction_keys(input,*args)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def rightclick(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if webelement is not None:
                if webelement.is_enabled():
                    from selenium.webdriver.common.action_chains import ActionChains
                    action_obj=ActionChains(browser_Keywords.driver_obj)
                    action_obj.context_click(webelement).perform()
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def switch_to_window(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            input=input[0]
            logger.log('Input is '+input)
            input=float(str(input))
            if not(input is None or int(input) >0):
                to_window=int(input)
                window_handles=self.__get_window_handles()
                cur_handle=browser_Keywords.driver_obj.current_window_handle
                from_window=-1
                if cur_handle in window_handles:
                    from_window=window_handles.index(cur_handle)+1
                if from_window>-1:
                    browser_Keywords.driver_obj.switch_to.window(window_handles[to_window-1])
                    logger.log('Switched to window handle'+browser_Keywords.driver_obj.current_window_handle)
                    logger.log('Control switched from window ' + str(from_window)
							+ " to window " + str(to_window))
                else:
                    logger.log('Current window handle not found')
            else:
                logger.log('Invalid input')
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            etype=Exceptions.error(e)
            try:
                if isinstance(etype,NoSuchWindowException):
                    window_handles=self.__get_window_handles()
                    if len(window_handles)>0:
                        total_handles=len(window_handles)
                        browser_Keywords.driver_obj.switch_to.window(window_handles[total_handles-1])
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        logger.log('No handles found')
            except Exception as e:
                etype=Exceptions.error(e)
        return status,methodoutput

    def __get_window_handles(self):
        window_handles=browser_Keywords.driver_obj.window_handles
        window_handles=browser_Keywords.driver_obj.window_handles
        logger.log('Window handles size '+str(len(window_handles)))
        return window_handles



