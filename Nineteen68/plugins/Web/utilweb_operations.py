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
import webconstants
from webconstants import *
from constants import SYSTEM_OS
if SYSTEM_OS!='Darwin':
    from pyrobot import Robot
    import win32gui
    import pyrobot
import table_keywords
import time
import urllib.request, urllib.parse, urllib.error, io
import core_utils
from selenium.webdriver.support.ui import Select
import logging
from constants import *
import readconfig
from  selenium.webdriver.common import action_chains
from selenium.webdriver.common.action_chains import ActionChains
import threading
local_uo = threading.local()

class UtilWebKeywords:
    def __init__(self):
        local_uo.log = logging.getLogger('utilweb_operations.py')
        self.verify_image_obj=None
        self.keys_info={}
        self.__create_keyinfo_dict()
        self.__load_Image_processingobj()
        self.bk_obj=browser_Keywords.BrowserKeywords()


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


    def __load_Image_processingobj(self):
        try:
            from verify_file_images import VerifyFileImages
            self.verify_image_obj=VerifyFileImages()
        except Exception as e:
            local_uo.log.error(e)

    def __web_driver_exception(self,e):
        local_uo.log.error(e)
        logger.print_on_console(e)
        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        return err_msg

    def is_visible(self,webelement):
        flag=False
        local_uo.log.debug('Checking the visibility of element')
        try:
            script="""var isVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })(); var s = arguments[0]; return isVisible(s);"""
            flag= browser_Keywords.local_bk.driver_obj.execute_script(script,webelement)
        except Exception as e:
            self.__web_driver_exception(e)
        local_uo.log.debug('Visibility is '+str(flag))
        return flag


    def is_enabled(self,webelement):
        local_uo.log.debug('Checking the enability of element')
        return webelement.is_enabled()

    def verify_visible(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                #call to highlight the webelement
                self.highlight(webelement)
                res=self.is_visible(webelement)
                local_uo.log.info('The visible status is '+str(res))
                logger.print_on_console('The visible status is '+str(res))
                if res:
                    logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_VISIBLE'])
                    local_uo.log.info(ERROR_CODE_DICT['ERR_OBJECT_VISIBLE'])
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    logger.print_on_console(err_msg)
                    local_uo.log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg


    def verify_exists(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None and webelement != '':
                #call to highlight the webelement
                if readconfig.configvalues['highlight_check'].strip().lower()=="yes":
                    self.highlight(webelement)
                logger.print_on_console(ERROR_CODE_DICT['MSG_ELEMENT_EXISTS'])
                local_uo.log.info(ERROR_CODE_DICT['MSG_ELEMENT_EXISTS'])
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
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is None or webelement == '':
            message=ERROR_CODE_DICT['ERR_ELEMENT_NOT_EXISTS']
            logger.print_on_console(message)
            local_uo.log.info(message)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        else:
            err_msg=ERROR_CODE_DICT['MSG_ELEMENT_EXISTS']
            local_uo.log.info(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


    def verify_enabled(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                #call to highlight the webelement
                self.highlight(webelement)
                if readconfig.configvalues['ignoreVisibilityCheck'].strip().lower()=="no":
                    res=self.is_visible(webelement)
                else:
                    res=True
                if webelement.is_enabled() and not(res):
                    info_msg=ERROR_CODE_DICT['The object is Hidden']
                    logger.print_on_console(err_msg)
                    local_uo.log.info(info_msg)
                elif webelement.is_enabled() and res:
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                    info_msg=ERROR_CODE_DICT['MSG_OBJECT_ENABLED']
                    logger.print_on_console(err_msg)
                    local_uo.log.info(info_msg)
                else:
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    logger.print_on_console(err_msg)
                    local_uo.log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def verify_disabled(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                #call to highlight the webelement
                self.highlight(webelement)
                flag=False
                unselectable_val=webelement.get_attribute('unselectable')
                local_uo.log.info('unselectable_val ',unselectable_val)
                if (unselectable_val!=None and unselectable_val.lower()=='on'):
                    flag=True
                local_uo.log.info('Disabled flag value ',str(flag))
                if not(webelement.is_enabled()) or flag:
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                    info_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    logger.print_on_console(info_msg)
                    local_uo.log.info(info_msg)
                else:
                    err_msg=ERROR_CODE_DICT['MSG_OBJECT_ENABLED']
                    logger.print_on_console(err_msg)
                    local_uo.log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg


    def verify_hidden(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                res=self.is_visible(webelement)
                if not(res):
                    info_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    logger.print_on_console(info_msg)
                    local_uo.log.info(info_msg)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_OBJECT_VISIBLE']
                    logger.print_on_console(err_msg)
                    local_uo.log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def verify_readonly(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                #call to highlight the webelement
                self.highlight(webelement)
                readonly_value=webelement.get_attribute("readonly")
                if readonly_value is not None and readonly_value.lower() =='true' or readonly_value is '':
                    info_msg=ERROR_CODE_DICT['ERR_ELEMENT_IS_READONLY']
                    logger.print_on_console(info_msg)
                    local_uo.log.info(info_msg)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_ELEMENT_IS_NOT_READONLY']
                    logger.print_on_console(err_msg)
                    local_uo.log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg


    def highlight(self,webelement):
        try:
            if browser_Keywords.local_bk.driver_obj is not None:
                browser_info=browser_Keywords.local_bk.driver_obj.capabilities
                browser_name=browser_info.get('browserName')
                browser_version=browser_info.get('version')
                ##local_uo.log.info('Browser is:'+browser_name+'Version is:'+browser_version)
                #get the original style of the element
                original_style = webelement.get_attribute('style')
                #Apply css to the element
                #check if driver instance is IE
                if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Ie):
                    browser_Keywords.local_bk.driver_obj.execute_script(HIGHLIGHT_SCRIPT_IE,webelement,original_style+APPLY_CSS)
                else:
                    browser_Keywords.local_bk.driver_obj.execute_script(HIGHLIGHT_SCRIPT,webelement,str(original_style)+APPLY_CSS)

                #highlight remains for 3 secs on the element
                import time
                time.sleep(3)

                #Remove css from the element  and applying the original style back to the element
                #check if driver instance is IE
                if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Ie):
                    if '8' in browser_version:
                        browser_Keywords.local_bk.driver_obj.execute_script(HIGHLIGHT_SCRIPT_IE,webelement,original_style+REMOVE_CSS_IE8)
                    else:
                        browser_Keywords.local_bk.driver_obj.execute_script(HIGHLIGHT_SCRIPT_IE,webelement,original_style)
                else:
                    browser_Keywords.local_bk.driver_obj.execute_script(HIGHLIGHT_SCRIPT,webelement,original_style)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)


    def __setfocus(self,webelement):
        status=TEST_RESULT_FAIL
        if browser_Keywords.local_bk.driver_obj is not None:
            browser_Keywords.local_bk.driver_obj.execute_script(FOUCS_ELE,webelement)
            status=TEST_RESULT_PASS
        return status

    def setfocus(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                status=self.__setfocus(webelement)
                if status==TEST_RESULT_PASS:
                    info_msg='Element is focused'
                    local_uo.log.info(info_msg)
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
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if(webelement is not None and len(args[0]) == 2):
                row = int(args[0][0])-1
                col = int(args[0][1])-1
                from table_keywords import TableOperationKeywords
                tableops = TableOperationKeywords()
                cell=tableops.javascriptExecutor(webelement,row,col)
                element_list=cell.find_elements_by_xpath('.//*')
                if len(list(element_list))>0:
                    xpath=tableops.getElemntXpath(element_list[0])
                    cell=browser_Keywords.local_bk.driver_obj.find_element_by_xpath(xpath)
                if(cell!=None):
                    webelement=cell

            elif(webelement is not None and len(args[0]) > 2):
                row = int(args[0][0])-1
                col = int(args[0][1])-1
                tag=args[0][2].lower()
                index=int(args[0][3])
                eleStatus = False
                counter = 1
                from table_keywords import TableOperationKeywords
                tableops = TableOperationKeywords()
                cell=tableops.javascriptExecutor(webelement,row,col)
                element_list=cell.find_elements_by_xpath('.//*')
                for member in element_list:
                    js1='function getElementXPath(elt) {var path = "";for (; elt && elt.nodeType == 1; elt = elt.parentNode){idx = getElementIdx(elt);xname = elt.tagName;if (idx >= 1){xname += "[" + idx + "]";}path = "/" + xname + path;}return path;}function getElementIdx(elt){var count = 1;for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling){if(sib.nodeType == 1 && sib.tagName == elt.tagName){count++;}}return count;}return getElementXPath(arguments[0]).toLowerCase();'
                    xpath=browser_Keywords.local_bk.driver_obj.execute_script(js1,member)
                    cellChild = browser_Keywords.local_bk.driver_obj.find_element_by_xpath(xpath)
                    tagName = cellChild.tag_name
                    tagType = cellChild.get_attribute('type')
                    xpath_elements=xpath.split('/')
                    lastElement=xpath_elements[len(xpath_elements)-1]
                    childindex=lastElement[lastElement.find("[")+1:lastElement.find("]")]
                    childindex = int(childindex)
                    if tag=='button':
                       if( (tagName==('input') and tagType==('button')) or tagType==('submit') or tagType==('reset') or tagType==('file')):
                          if index==childindex:
                            eleStatus =True
                          else:
                            if counter==index:
                               index =childindex
                               eleStatus =True
                            else:
                                counter+=1
                    elif tag=='image':
                        if(tagName==('input') and (tagType==('img') or tagType==('image'))):
                            if index==childindex:
                                eleStatus =True
                            else:
                                if counter==index:
                                    index =childindex
                                    eleStatus =True
                                else:
                                    counter+=1
                        elif tagName =='img':
                            if index==childindex:
                                eleStatus =True
                            else:
                                if counter==index:
                                   index =childindex
                                   eleStatus =True
                                else:
                                    counter+=1
                    elif tag=='img':
                         if index==childindex:
                                eleStatus =True
                         else:
                                if counter==index:
                                   index =childindex
                                   eleStatus =True
                                else:
                                    counter+=1
                    elif tag=='checkbox':
                         if(tagName==('input') and (tagType==('checkbox')) ):
                             if index==childindex:
                                eleStatus =True
                             else:
                                if counter==index:
                                   index =childindex
                                   eleStatus =True
                                else:
                                    counter+=1
                    elif tag=='radiobutton':
                         if (tagName==('input') and tagType==('radio')):
                            if index==childindex:
                                eleStatus =True
                            else:
                                if counter==index:
                                   index =childindex
                                   eleStatus =True
                                else:
                                    counter+=1
                    elif tag=='textbox':
                         if (tagName==('input') and (tagType==('text') or tagType==('email') or tagType==('password') or tagType==('range') or tagType==('search') or tagType==('url') or tagType==('button') or tagType==('checkbox') or tagType==('color') or tagType==('date') or tagType==('datetime-local') or tagType==('file') or tagType==('image') or tagType==('month') or tagType==('week') or tagType==('time') or tagType==('number') or tagType==('radio') or tagType==('reset') or tagType==('submit') or tagType==('tel') or tagType==('None')) ):
                            if index==childindex:
                                eleStatus =True
                            else:
                                if counter==index:
                                   index =childindex
                                   eleStatus =True
                                else:
                                    counter+=1
                    elif tag=='link':
                        if(tagName==('a')):
                            if index==childindex:
                                eleStatus =True
                            else:
                                if counter==index:
                                   index =childindex
                                   eleStatus =True
                                else:
                                    counter+=1
                    else:
                            eleStatus=True

                    if eleStatus==True:
                        webelement = cellChild
                        break
            if webelement is not None:
                location=webelement.location
                if SYSTEM_OS != 'Darwin':
                    if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Firefox):
                        javascript = "return window.mozInnerScreenY"
                        value=browser_Keywords.local_bk.driver_obj.execute_script(javascript)
                        logger.print_on_console(value)
                        offset=int(value)
                        robot=pyrobot.Robot()
                        robot.set_mouse_pos(int(location.get('x')+18),int(location.get('y')+offset+18))
                        local_uo.log.debug('hover performed')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        obj=Utils()
                        location=obj.get_element_location(webelement)
                        obj.enumwindows()
                        rect=obj.rect
                        robot=pyrobot.Robot()
                        obj.mouse_move(int(location.get('x'))+9,int(location.get('y')+rect[1]+6))
                        local_uo.log.debug('hover performed')
                if SYSTEM_OS == 'Darwin':
                    try:
                        ##clickinfo = browser_Keywords.local_bk.driver_obj.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                        hover = webdriver.ActionChains(browser_Keywords.local_bk.driver_obj).move_to_element(webelement)
                        hover.perform()
                        local_uo.log.info('Hover operation performed')
                        status = TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
                    except Exception as e:
                        local_uo.log.error(e)
                        logger.print_on_console("Cannot perform mouseHover operation.")
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            local_uo.log.error(e)
            err_msg=self.__web_driver_exception(e)
            logger.print_on_console("Cannot perform mouseHover operation.")
        return status,methodoutput,output,err_msg




    def tab(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                webelement.send_keys(Keys.TAB)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except WebDriverException as e:
            if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Chrome):
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
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                digits= 1
                input1=input[0]
                info_msg='Focus the given webelement '+webelement.tag_name+' before sending keys'
                local_uo.log.info(info_msg)
                logger.print_on_console(info_msg)
                self.__setfocus(webelement)
                if len(args)==0 and input1 in list(self.keys_info.keys()):
                    if webelement.get_attribute('type')!='text':
                        digits = [int(i)for i in input if i.isdigit()]
                        try:
                            webelement.send_keys(self.keys_info[input1.lower()]*digits[0])
                        except Exception as e:
                            local_uo.log.debug('Operated using option 2',e)
                            webelement.send_keys(self.keys_info[input1.lower()])
                    else:
                        local_uo.log.debug('It is a textbox')
                        #self.generic_sendfucntion_keys(input1.lower(),*args)
                        if(len(input)>1):
                            self.generic_sendfucntion_keys(input[0].lower(),input[1])
                        else:
                            self.generic_sendfucntion_keys(input[0].lower(),*args)
                else:
                    local_uo.log.debug('Calling Generic sendfunction keys')
                    #self.generic_sendfucntion_keys(input.lower(),*args)
                    if(len(input)>1):
                        self.generic_sendfucntion_keys(input[0].lower(),input[1])
                    else:
                        self.generic_sendfucntion_keys(input[0].lower(),*args)
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
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                if webelement.is_enabled():
                    local_uo.log.debug(WEB_ELEMENT_ENABLED)
                    if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Firefox):
                        info_msg='Firefox browser'
                        local_uo.log.info(info_msg)
                        logger.print_on_console(info_msg)
                        javascript = "return window.mozInnerScreenY"
                        value=browser_Keywords.local_bk.driver_obj.execute_script(javascript)
                        logger.print_on_console(value)
                        offset=int(value)
                        location = webelement.location
                        robot=pyrobot.Robot()
                        robot.set_mouse_pos(int(location.get('x')+9),int(location.get('y')+offset))
                        local_uo.log.debug('Setting the mouse position')
                        robot.click_mouse('right')
                        local_uo.log.debug('Performed Right click')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        from selenium.webdriver.common.action_chains import ActionChains
                        action_obj=ActionChains(browser_Keywords.local_bk.driver_obj)
                        action_obj.context_click(webelement).perform()
                        local_uo.log.debug('Performed Right click')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def mouse_click(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement !=None:
                local_uo.log.info(INPUT_IS)
                local_uo.log.info(input)
                if not(input is None):
                    row_num=int(input[0])-1
                    col_num=int(input[1])-1
                    from table_keywords import TableOperationKeywords
                    tableops = TableOperationKeywords()
                    cell=tableops.javascriptExecutor(webelement,row_num,col_num)
                    element_list=cell.find_elements_by_xpath('.//*')
                    if len(list(element_list))>0:
                        xpath=tableops.getElemntXpath(element_list[0])
                        cell=browser_Keywords.local_bk.driver_obj.find_element_by_xpath(xpath)

                    if(cell!=None):
                        local_uo.log.debug('checking for element enabled')
                        webelement=cell
                        if cell.is_enabled():
                            ele_coordinates=cell.location
                            logger.print_on_console(ele_coordinates)
                            hwnd=win32gui.GetForegroundWindow()
                            local_uo.log.debug('Handle found ')
                            local_uo.log.debug(hwnd)
                            if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Firefox):
                                info_msg='Firefox browser'
                                local_uo.log.info(info_msg)
                                logger.print_on_console(info_msg)
                                javascript = "return window.mozInnerScreenY"
                                value=browser_Keywords.local_bk.driver_obj.execute_script(javascript)
                                logger.print_on_console(value)
                                offset=int(value)
                                robot=pyrobot.Robot()
                                robot.set_mouse_pos(int(ele_coordinates.get('x')+9),int(ele_coordinates.get('y')+offset-5))
                                local_uo.log.debug('Setting the mouse position')
                                robot.mouse_down('left')
                                local_uo.log.debug('Mouse click performed')
                                robot.mouse_up('left')
                                local_uo.log.debug('Mouse release performed')
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE

                            else:
                                utils=Utils()
                                utils.enumwindows()
                                logger.print_on_console("UTIL WIND")
                                rect=utils.rect
                                robot=pyrobot.Robot()
                                local_uo.log.debug('Setting the mouse position')
                                logger.print_on_console('before loc')
                                location=utils.get_element_location(webelement)
                                logger.print_on_console(location)
                                robot.set_mouse_pos(int(location.get('x'))+9,int(location.get('y')+rect[1]+6))
                                logger.print_on_console('after loc')
                                robot.mouse_down('left')
                                logger.print_on_console('button press')
                                robot.mouse_up('left')
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
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            from PIL import Image
            if webelement!=None and webelement !='':
                img_src = webelement.get_attribute("src")
                file1 = io.BytesIO(urllib.request.urlopen(img_src).read())
                file2=input[0]
                local_uo.log.info(INPUT_IS)
                local_uo.log.info(file2)
                if file1 != None and file2 != None and  file2 != '' and os.path.exists(file2) :
                    local_uo.log.debug('comparing the images')
                    if self.verify_image_obj != None: #Meaning user has advanced image processing plugin
                        if self.verify_image_obj.imagecomparison(file1,file2):
                            info_msg=ERROR_CODE_DICT['MSG_IMAGE_COMPARE_PASS']
                            local_uo.log.info(info_msg)
                            logger.print_on_console(info_msg)
                            methodoutput=TEST_RESULT_TRUE
                            status=TEST_RESULT_PASS
                    else:
                            from PIL import Image
                            import numpy as np
                            size=(128,128)
                            img1 = Image.open(file1)
                            img2 = Image.open(file2)
                            img1 = img1.convert('RGB')
                            img2 = img2.convert('RGB')
                            img1 = img1.resize(size)
                            img2 = img2.resize(size)
                            imageA = np.asarray(img1)
                            imageB = np.asarray(img2)
                            err = np.sum((imageA.astype("float") - imageB.astype("float"))**2)
                            err /= float(imageA.shape[0] * imageA.shape[1])
                            if(err<1000):
                                info_msg=ERROR_CODE_DICT['MSG_IMAGE_COMPARE_PASS']
                                local_uo.log.info(info_msg)
                                logger.print_on_console(info_msg)
                                methodoutput=TEST_RESULT_TRUE
                                status=TEST_RESULT_PASS
                            else:
                                err_msg=ERROR_CODE_DICT['ERR_IMAGE_COMPARE_FAIL']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_NO_IMAGE_SOURCE']
            else:
                err_msg='Web element not found'
            if err_msg != None:
                logger.print_on_console(err_msg)
                local_uo.log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def image_similarity_percentage(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=None
        err_msg=None
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            from PIL import Image
            if webelement!=None and webelement !='':
                img_src = webelement.get_attribute("src")
                file1 = io.BytesIO(urllib.request.urlopen(img_src).read())
                file2=input[0]
                local_uo.log.info(INPUT_IS)
                local_uo.log.info(file2)
                if file1 != None and file2 != None and  file2 != '' and os.path.exists(file2) :
                    local_uo.log.debug('comparing the images')
                    if self.verify_image_obj != None: #Meaning user has advanced image processing plugin
                        if self.verify_image_obj.imagecomparison(file1,file2):
                            info_msg=ERROR_CODE_DICT['MSG_IMAGE_COMPARE_PASS']
                            local_uo.log.info(info_msg)
                            logger.print_on_console(info_msg)
                            methodoutput=TEST_RESULT_TRUE
                            status=TEST_RESULT_PASS
                    else:
                            from PIL import Image
                            import numpy as np
                            size=(128,128)
                            img1 = Image.open(file1)
                            img2 = Image.open(file2)
                            img1 = img1.convert('RGB')
                            img2 = img2.convert('RGB')
                            img1 = img1.resize(size)
                            img2 = img2.resize(size)
                            imageA = np.asarray(img1)
                            imageB = np.asarray(img2)
                            err = np.sum((imageA.astype("float") - imageB.astype("float"))**2)
                            err /= float(imageA.shape[0] * imageA.shape[1])
                            #print 'err: ',err
                            err /= float(size[0]*size[1]*3*255*255)
                            #print 'err %: ',err*100,'%'
                            output = str((1-err)*100)
                            logger.print_on_console("Image similarity percentage is: "+str((1-err)*100)+"%")
                            methodoutput=TEST_RESULT_TRUE
                            status=TEST_RESULT_PASS
                            local_uo.log.info('Result is ',output)
                            logger.print_on_console('Result is ',output)
                else:
                    err_msg=ERROR_CODE_DICT['ERR_NO_IMAGE_SOURCE']
                if err_msg != None:
                    logger.print_on_console(err_msg)
                    local_uo.log.error(err_msg)
        except Exception as e:
            local_uo.log.error(e)
            logger.print_on_console(e)
            err_msg=INPUT_ERROR
        return status,methodoutput,output,err_msg

    def get_element_tag_value(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=None
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    local_uo.log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                    output = str(webelement.tag_name)
                    local_uo.log.info(STATUS_METHODOUTPUT_UPDATE)
                    logger.print_on_console('Result: ',output)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    local_uo.log.error(ERR_DISABLED_OBJECT)
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    logger.print_on_console(ERR_DISABLED_OBJECT)
            except Exception as e:
                 err_msg=self.__web_driver_exception(e)
        local_uo.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg
