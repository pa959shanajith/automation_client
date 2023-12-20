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
from encryption_utility import AESCipher
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import logger
import browser_Keywords
from utils_web import Utils
import webconstants
from webconstants import *
from constants import SYSTEM_OS
if SYSTEM_OS == 'Windows' :
    from pyrobot import Robot
    import win32gui
    import pyrobot
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
from table_keywords import TableOperationKeywords, local_tk
import os


local_uo = threading.local()

class UtilWebKeywords:
    def __init__(self):
        local_uo.log = logging.getLogger('utilweb_operations.py')
        self.verify_image_obj=None
        self.keys_info={}
        self.__create_keyinfo_dict()
        self.__load_Image_processingobj()
        self.tblobj = TableOperationKeywords()

    def _invalid_input(self):
        err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
        local_uo.log.info(err_msg)
        logger.print_on_console(err_msg)
        return err_msg

    def _invalid_index(self):
        err_msg=("list index out of range")
        local_uo.log.info(err_msg)
        logger.print_on_console(err_msg)
        return err_msg

    def _index_zero(self):
        err_msg = ERROR_CODE_DICT['INVALID_TABLE_INDEX']
        local_uo.log.info(err_msg)
        logger.print_on_console(err_msg)
        return err_msg

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
        except ImportError: pass
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
            #Handled document fragments for salesforce. If document fragment is encountered, parentNode is replaced by host.
            script="""var isVisible = (function () {
    function inside(schild, sparent) {
        while (schild) {
            if (schild === sparent) return true;
            schild = schild.parentNode;
        }
        return false;
    };
    return function (selem) {
        if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;
        var srect = selem.getBoundingClientRect();
        if (window.getComputedStyle || selem.currentStyle) {
            var sel = selem,
                scomp = null;
            while (sel) {
                if (sel === document) {
                    break;
                } else if (!sel.parentNode) return false;
                scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;
                if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;
                sel = sel.parentNode;
                if (sel.toString()=='[object ShadowRoot]')
                    sel=sel.host;
            }
        }
        return true;
    }
})();
var s = arguments[0];
return isVisible(s);"""
            flag= browser_Keywords.local_bk.driver_obj.execute_script(script,webelement)
        except Exception as e:
            self.__web_driver_exception(e)
        local_uo.log.debug('Visibility is '+str(flag))
        return flag

    def is_inView(self,webelement):
        flag = False
        local_uo.log.debug('Checking whether the element is in view')
        try:
            flag = browser_Keywords.local_bk.driver_obj.execute_script(INVIEW,webelement)
        except Exception as e:
            self.__web_driver_exception(e)
        local_uo.log.debug('In View is '+str(flag))
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
                    local_uo.log.info(info_msg)
                elif webelement.is_enabled() and res:
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                    info_msg=ERROR_CODE_DICT['MSG_OBJECT_ENABLED']
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
                    status=TEST_RESULT_PASS
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
                elif webelement.get_attribute("type") in ['checkbox', 'radio'] and webelement.get_attribute("onclick") in ['return false', 'return false;', 'this.checked = false', 'this.checked = false;', 'this.checked=false', 'this.checked=false;']:
                    # Checking readonly property for checkbox and radio buttons which have onclick attribute value
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
        eleStatus = True
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if len(webelement.find_elements_by_xpath('.//ancestor::lightning-datatable')) >0:
                tableops = TableOperationKeywords()
                row_num=int(args[0][0])
                col_num=int(args[0][1])
                row_count=tableops.getRowCountJs(webelement)
                col_count=tableops.getColoumnCountJs(webelement)
                if row_num-1>row_count or col_num-1>col_count:
                    local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                else:
                    remoteWebElement=tableops.javascriptExecutor(webelement,row_num-1,col_num-1)
                    child_ele=[]
                    child_ele=remoteWebElement.find_elements_by_xpath('.//a')
                    if(len(child_ele)==0):
                        child_ele=remoteWebElement.find_elements_by_xpath('.//input')
                        if(len(child_ele)==0):
                            child_ele=remoteWebElement.find_elements_by_xpath('.//button')
                            if(len(child_ele)==0):
                                child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-base-formatted-text')
                                if(len(child_ele)==0):
                                    child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-date-time')
                                    if(len(child_ele)==0):
                                        child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-number')
                                        if(len(child_ele)==0):
                                            child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-email')
                                            if(len(child_ele)==0):
                                                child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-phone')
                                                if(len(child_ele)==0):
                                                    child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-url')
                                                    if(len(child_ele)==0):
                                                        child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-location')
                if(len(child_ele)>0):
                    webelement=child_ele[0]
            elif(webelement is not None and len(args[0]) == 2):
                row = int(args[0][0])-1
                col = int(args[0][1])-1
                if webelement.tag_name == 'div' and webelement.get_attribute('role') == 'grid':
                    row = webelement.find_elements_by_xpath(".//div[@role='row']")[row]
                    cell = row.find_elements_by_xpath(".//*")[col]
                else:
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
                       if( ((tagName==('input') or tagName==('button')) and tagType==('button')) or tagType==('submit') or tagType==('reset') or tagType==('file')):
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
                    elif tag=='textbox' or tag=='input':
                         if (tagName==('input') and (tagType==('text') or tagType==('email') or tagType==('password') or tagType==('search') or tagType==('url') or tagType==('color') or tagType==('date') or tagType==('datetime-local') or tagType==('file') or tagType==('month') or tagType==('week') or tagType==('time') or tagType==('number') or tagType==('tel') or tagType==('None')) ):
                            if index==childindex:
                                eleStatus =True
                            else:
                                if counter==index:
                                   index =childindex
                                   eleStatus =True
                                else:
                                    counter+=1
                    elif tag=='link' or tag=='a':
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
                            # Commented next line, as because of this, loop was not going into next iteration
                            # eleStatus=True
                            continue

                    if eleStatus==True:
                        webelement = cellChild
                        break
            if webelement is not None and eleStatus:
                if SYSTEM_OS == 'Darwin' or SYSTEM_OS == 'Linux':
                    obj = Utils()
                    if isinstance(browser_Keywords.local_bk.driver_obj, webdriver.Firefox):
                        javascript = "return window.mozInnerScreenY"
                        value = browser_Keywords.local_bk.driver_obj.execute_script(javascript)
                        offset = int(value)
                        location = webelement.location
                        obj.mouse_move_posix(int(location.get('x') + 18), int(location.get('y') + offset + 18))
                        #log.debug('hover performed')
                        status = TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
                    elif isinstance(browser_Keywords.local_bk.driver_obj, webdriver.Safari):
                        location = obj.get_element_location(webelement)
                        obj.mouse_move(int(location.get('x') + 9), int(location.get('y') + 70))
                    else:
                        location = obj.get_element_location(webelement)
                        obj.enumwindows()
                        obj.mouse_move(int(location.get('x')) + 9, int(location.get('y') + 150))
                        ##clickinfo = browser_Keywords.driver_obj.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                        # hover = webdriver.ActionChains(browser_Keywords.driver_obj).move_to_element(webelement)
                        # hover.perform()
                        log.info('Hover operation performed')
                        status = TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
                else:
                    obj=Utils()
                    location=webelement.location
                    if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Firefox):
                        #Scroll happens only if webelement is not displayed on screen.
                        if not self.is_inView(webelement):
                            # Scroll till the element is in the middle
                            desired_y_cor = (webelement.size['height'] / 2) + webelement.location['y']
                            current_y_cor = (browser_Keywords.local_bk.driver_obj.execute_script('return window.innerHeight') / 2) + browser_Keywords.local_bk.driver_obj.execute_script('return window.pageYOffset')
                            scroll_y_cor_by = desired_y_cor - current_y_cor
                            browser_Keywords.local_bk.driver_obj.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_cor_by)
                            page_yoffset = browser_Keywords.local_bk.driver_obj.execute_script('return window.pageYOffset')
                            location['y'] = location['y'] - page_yoffset
                        elif self.is_inView(webelement):
                            page_yoffset = browser_Keywords.local_bk.driver_obj.execute_script('return window.pageYOffset')
                            location['y'] = location['y'] - page_yoffset
                        javascript = "return window.mozInnerScreenY"
                        value=browser_Keywords.local_bk.driver_obj.execute_script(javascript)
                        offset=int(value)
                        robot=pyrobot.Robot()
                        robot.set_mouse_pos(int(location.get('x')+18),int(location.get('y')+offset+10))
                        local_uo.log.debug('hover performed')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        #Scroll happens only if webelement is not displayed on screen.
                        if not self.is_inView(webelement):
                            # Scroll till the element is in the middle
                            desired_y_cor = (webelement.size['height'] / 2) + webelement.location['y']
                            current_y_cor = (browser_Keywords.local_bk.driver_obj.execute_script('return window.innerHeight') / 2) + browser_Keywords.local_bk.driver_obj.execute_script('return window.pageYOffset')
                            scroll_y_cor_by = desired_y_cor - current_y_cor
                            browser_Keywords.local_bk.driver_obj.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_cor_by)
                            page_yoffset = browser_Keywords.local_bk.driver_obj.execute_script('return window.pageYOffset')
                            location['y'] = location['y'] - page_yoffset
                        elif self.is_inView(webelement):
                            page_yoffset = browser_Keywords.local_bk.driver_obj.execute_script('return window.pageYOffset')
                            location['y'] = location['y'] - page_yoffset
                        offset = browser_Keywords.local_bk.driver_obj.execute_script("return window.outerHeight - window.innerHeight;")
                        obj.mouse_move(int(location.get('x'))+9,int(location.get('y')+offset))
                        local_uo.log.debug('hover performed')
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
            if isinstance(browser_Keywords.local_bk.driver_obj, webdriver.Chrome) or isinstance(browser_Keywords.local_bk.driver_obj, webdriver.Firefox) or isinstance(browser_Keywords.local_bk.driver_obj, webdriver.Edge):
                self.__setfocus(webelement)
                robot=Robot()
                robot.key_press('tab')
                robot.key_release('tab')
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output,err_msg

    def generic_sendfucntion_keys(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        result = None
        from sendfunction_keys import SendFunctionKeys
        obj=SendFunctionKeys()
        try:
            result=obj.sendfunction_keys(input,*args)
            if result[0]!="Fail":
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            err_msg = e
        return status,methodoutput,output,err_msg


    def sendfunction_keys(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        result = None
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
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        local_uo.log.debug('It is a textbox')
                        #self.generic_sendfucntion_keys(input1.lower(),*args)
                        if(len(input)>1):
                            #self.generic_sendfucntion_keys(input[0],input[1])
                            result=self.generic_sendfucntion_keys(*input)
                        else:
                            result = self.generic_sendfucntion_keys(input[0],*args)
                else:
                    local_uo.log.debug('Calling Generic sendfunction keys')
                    #self.generic_sendfucntion_keys(input.lower(),*args)
                    if(len(input)>1):
                        #self.generic_sendfucntion_keys(input[0],input[1])
                        result = self.generic_sendfucntion_keys(*input)
                    else:
                        result = self.generic_sendfucntion_keys(input[0],*args)
                if (result is not None) and (result[0]!="Fail"):
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
        except ElementNotInteractableException as ex:
            err_msg='Element is not interactable'
            logger.print_on_console(ex)
            local_uo.log.info(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg


    def send_keys(self, webelement, input, *args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        text = False
        try:
            if len(input)>0:
                input1 = input[0]
                mul_inp = input1.split('+')
                digit = 1
                if len(input)==3 and ((input[2].startswith('|') and input[2].endswith('|')) or (input[2].startswith('{') and input[2].endswith('}'))):
                    text = True
                    digit = int(input[1]) if input[1].isdigit() else 1
                elif len(input)==2 and ((input[1].startswith('|') and input[1].endswith('|')) or (input[1].startswith('{') and input[1].endswith('}'))):
                    text = True
                actions = ActionChains(browser_Keywords.local_bk.driver_obj)
                if text == True:
                    for i in range(digit):
                        actions.send_keys(input1)
                        actions.perform()
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                elif input1.lower() in list(self.keys_info.keys()):
                    digit = int(input[1]) if len(input)>1 and input[1].isdigit() else 1
                    try:
                        actions.send_keys(self.keys_info[input1.lower()]*digit)
                        actions.perform()
                    except Exception as e:
                        local_uo.log.debug('Operated using option 2',e)
                        actions.send_keys(self.keys_info[input1.lower()])
                        actions.perform()
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                elif len(mul_inp)==2:
                    actions.key_down(self.keys_info[mul_inp[0].lower()])
                    actions.send_keys(self.keys_info[mul_inp[1].lower()])
                    actions.key_up(self.keys_info[mul_inp[0].lower()])
                    actions.perform()
                elif len(mul_inp)==3:
                    actions.key_down(self.keys_info[mul_inp[0].lower()])
                    actions.key_down(self.keys_info[mul_inp[1].lower()])
                    actions.send_keys(self.keys_info[mul_inp[2].lower()])
                    actions.perform()
                    actions.key_up(self.keys_info[mul_inp[1].lower()])
                    actions.key_up(self.keys_info[mul_inp[0].lower()])
                    actions.perform()
                else:
                    err_msg = "Function key '"+input1+"' is not recognized."
                    logger.print_on_console(err_msg)
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
                        if args[0][0]=='' or args[0][0]=='0':
                            local_uo.log.debug('Performing first type of Right click')
                            from selenium.webdriver.common.action_chains import ActionChains
                            action_obj=ActionChains(browser_Keywords.local_bk.driver_obj)
                            action_obj.context_click(webelement).perform()
                            local_uo.log.debug('Performed Right click')
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        elif args[0][0] != '' and args[0][0] == '1':
                            local_uo.log.debug('Performing second type of Right click')
                            from selenium.webdriver.common.keys import Keys
                            # focus on the element
                            browser_Keywords.local_bk.driver_obj.execute_script("""arguments[0].focus();""", webelement)
                            # send keys
                            webelement.send_keys(Keys.SHIFT+Keys.F10)
                            local_uo.log.debug('Performed second type Right click')
                            status = TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                        else:
                            err_msg = "Please provide Valid input"
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
                    tableops = TableOperationKeywords()
                    cell=tableops.javascriptExecutor(webelement,row_num,col_num)
                    element_list=cell.find_elements_by_xpath('.//*')
                    if len(webelement.find_elements_by_xpath('.//ancestor::lightning-datatable')) >0:
                        row_num=int(input[0])
                        col_num=int(input[1])
                        row_count=tableops.getRowCountJs(webelement)
                        col_count=tableops.getColoumnCountJs(webelement)
                        if row_num-1>row_count or col_num-1>col_count:
                            local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        else:
                            remoteWebElement=tableops.javascriptExecutor(webelement,row_num-1,col_num-1)
                            child_ele=[]
                            child_ele=remoteWebElement.find_elements_by_xpath('.//a')
                            if(len(child_ele)==0):
                                child_ele=remoteWebElement.find_elements_by_xpath('.//input')
                                if(len(child_ele)==0):
                                    child_ele=remoteWebElement.find_elements_by_xpath('.//button')
                                    if(len(child_ele)==0):
                                        child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-base-formatted-text')
                                        if(len(child_ele)==0):
                                            child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-date-time')
                                            if(len(child_ele)==0):
                                                child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-number')
                                                if(len(child_ele)==0):
                                                    child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-email')
                                                    if(len(child_ele)==0):
                                                        child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-phone')
                                                        if(len(child_ele)==0):
                                                            child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-url')
                                                            if(len(child_ele)==0):
                                                                child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-location')
                        if(len(child_ele)>0):
                            cell=child_ele[0]
                    elif len(list(element_list))>0:
                        xpath=tableops.getElemntXpath(element_list[0])
                        cell=browser_Keywords.local_bk.driver_obj.find_element_by_xpath(xpath)
                    if(cell!=None):
                        local_uo.log.debug('checking for element enabled')
                        webelement=cell
                        if cell.is_enabled():
                            ele_coordinates=cell.location
                            local_uo.log.debug(ele_coordinates)
                            if SYSTEM_OS == 'Windows' :
                                hwnd=win32gui.GetForegroundWindow()
                                local_uo.log.debug('Handle found ')
                                local_uo.log.debug(hwnd)
                                if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Firefox):
                                    info_msg='Firefox browser'
                                    local_uo.log.info(info_msg)
                                    javascript = "return window.mozInnerScreenY"
                                    value=browser_Keywords.local_bk.driver_obj.execute_script(javascript)
                                    local_uo.log.debug(value)
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
                                    local_uo.log.debug("UTIL WIND")
                                    rect=utils.rect
                                    robot=pyrobot.Robot()
                                    local_uo.log.debug('Setting the mouse position')
                                    local_uo.log.debug('before loc')
                                    location=utils.get_element_location(webelement)
                                    local_uo.log.debug(location)
                                    robot.set_mouse_pos(int(location.get('x'))+9,int(location.get('y')+rect[1]+6))
                                    local_uo.log.debug('after loc')
                                    robot.mouse_down('left')
                                    local_uo.log.debug('button press')
                                    robot.mouse_up('left')
                                    status=TEST_RESULT_PASS
                                    methodoutput = TEST_RESULT_TRUE
                            # linux implementation for click
                            else:
                                local_uo.log.debug('Performing mouse click on linux')
                                import pyautogui as pag
                                if isinstance(browser_Keywords.local_bk.driver_obj, webdriver.Firefox):
                                    javascript = "return window.mozInnerScreenY"
                                    value = browser_Keywords.local_bk.driver_obj.execute_script(javascript)
                                    offset = int(value)
                                    pag.click(x=int(ele_coordinates.get('x') + 9), y=int(ele_coordinates.get('y') + offset - 5))
                                else:
                                    utils = Utils()
                                    location = utils.get_element_location(webelement)
                                    pag.click(x=int(location.get('x')), y=int(location.get('y')+10))

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
                # if file path passed as network location in src attribute
                if "file:" in img_src and "///" not in img_src:
                    server_url = img_src.split(":")[1].replace("\\", "/")
                    file_name = server_url.split("/")[-1]
                    server_url = server_url.split("/")
                    server_path = "//"
                    for element in server_url[:-1]:
                        if element != '':
                            server_path += element + "/"
                    img_src = os.path.normpath(server_path) + os.sep
                    img_src = "file:" + img_src + file_name
                file1 = io.BytesIO(urllib.request.urlopen(img_src).read())
                file2=input[0]
                local_uo.log.info(INPUT_IS)
                local_uo.log.info(file2)
                if file1 != None and file2 != None and  file2 != '':
                    local_uo.log.debug('comparing the images')
                    # if file path passed as network location
                    if "file:" in file2 and "///" not in file2:
                        server_url = file2.split(":")[1].replace("\\", "/")
                        file_name = server_url.split("/")[-1]
                        server_url = server_url.split("/")
                        server_path = "//"
                        for element in server_url[:-1]:
                            if element != '':
                                server_path += element + "/"
                        img_src = os.path.normpath(server_path) + os.sep
                        img_src = "file:" + img_src + file_name
                        file2 = io.BytesIO(urllib.request.urlopen(img_src).read())
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
        except urllib.error.URLError as e:
            err_msg=ERROR_CODE_DICT['ERR_NO_IMAGE_SOURCE']
            local_uo.log.error(err_msg)
            logger.print_on_console(err_msg)
        except FileNotFoundError as e:
            err_msg=ERROR_CODE_DICT['ERR_NO_IMAGE_SOURCE']
            local_uo.log.error(err_msg)
            logger.print_on_console(err_msg)
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
                # if file path passed as network location in src attribute
                if "file:" in img_src and "///" not in img_src:
                    server_url = img_src.split(":")[1].replace("\\", "/")
                    file_name = server_url.split("/")[-1]
                    server_url = server_url.split("/")
                    server_path = "//"
                    for element in server_url[:-1]:
                        if element != '':
                            server_path += element + "/"
                    img_src = os.path.normpath(server_path) + os.sep
                    img_src = "file:" + img_src + file_name
                file1 = io.BytesIO(urllib.request.urlopen(img_src).read())
                file2=input[0]
                local_uo.log.info(INPUT_IS)
                local_uo.log.info(file2)
                if file1 != None and file2 != None and  file2 != '':
                    local_uo.log.debug('comparing the images')
                    # if file path passed as network location
                    if "file:" in file2 and "///" not in file2:
                        server_url = file2.split(":")[1].replace("\\", "/")
                        file_name = server_url.split("/")[-1]
                        server_url = server_url.split("/")
                        server_path = "//"
                        for element in server_url[:-1]:
                            if element != '':
                                server_path += element + "/"
                        img_src = os.path.normpath(server_path) + os.sep
                        img_src = "file:" + img_src + file_name
                        file2 = io.BytesIO(urllib.request.urlopen(img_src).read())
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
        except urllib.error.URLError as e:
            err_msg=ERROR_CODE_DICT['ERR_NO_IMAGE_SOURCE']
            local_uo.log.error(err_msg)
            logger.print_on_console(err_msg)
        except FileNotFoundError as e:
            err_msg=ERROR_CODE_DICT['ERR_NO_IMAGE_SOURCE']
            local_uo.log.error(err_msg)
            logger.print_on_console(err_msg)
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

    def get_attribute_value(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=None
        eleStatus=False
        index=0
        css_flag = False
        if input[-1].lower() == 'css':
            css_flag = True
            input.pop()
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement != None and webelement !='' and webelement.tag_name.lower()=='table' and len(input)!=1:
                if len(input) >= 4 and input[3] and int(input[3]) <= 0:
                    err_msg = self._index_zero()
                elif input[2]:
                    if(len(input) == 5 and all(v for v in input) and (not input[2] == 'tr')):
                        attr_name=input[4]
                        webelement1=None
                        row_number=int(input[0])-1
                        col_number=int(input[1])-1
                        tag=input[2].lower()
                        if input[3]: index=int(input[3])
                        eleStatus, webelement1 = self.get_table_cell(webelement, row_number, col_number, tag, index)
                        webelement=webelement1
                    elif(input[2]=='tr'): #fetch the attribute value of tr (index is needed)
                        if not(input[4]):
                            err_msg = 'Input Error: Please enter attribute name'
                            logger.print_on_console(err_msg)
                            local_uo.log.error(err_msg)
                        elif input[3] and int(input[3]) >= 1:
                            attr_name=input[4]
                            index=int(input[3])-1
                            tablerow_js='var targetTable = arguments[0]; var index = arguments[1]; var rowCount = targetTable.rows; return rowCount[index];'
                            webelement = browser_Keywords.local_bk.driver_obj.execute_script(tablerow_js,webelement,index)
                            eleStatus=True
                        elif input[3] and int(input[3]) <= 0:
                            err_msg = 'Invalid Input: Index input cannot be 0 for table'
                            logger.print_on_console(err_msg)
                            local_uo.log.error(err_msg)
                        else:
                            err_msg = 'Input Error: Missing index'
                            logger.print_on_console(err_msg)
                            local_uo.log.error(err_msg)
                # checking attribute value of table itself
                elif(len(input) == 5 and (not all(i for i in input[:-1]))):
                    attr_name=input[4]
                    eleStatus=True
                elif(len(input) == 5 and (not input[2])):
                    err_msg = 'Input Error: Please specify valid object type'
                    logger.print_on_console(err_msg)
                    local_uo.log.error(err_msg)
            elif(len(input)==1) and not err_msg:
                attr_name=input[0]
                eleStatus=True
            # elif css_flag and (len(input) == 2) and not err_msg:
            #     attr_name = input[0]
            #     eleStatus=True
            if(eleStatus):
                if webelement != None and webelement !='':
                    local_uo.log.info(INPUT_IS)
                    local_uo.log.info(input)
                    if attr_name:
                        if not css_flag:
                            if attr_name != 'required':
                                output = webelement.get_attribute(attr_name)
                            else:
                                output = browser_Keywords.local_bk.driver_obj.execute_script("return arguments[0].getAttribute('required')", webelement)
                            if output != None and output != '':
                                logger.print_on_console('Output: ', output)
                                status = TEST_RESULT_PASS
                                methodoutput = TEST_RESULT_TRUE
                            else:
                                err_msg = 'Attribute does not exists'
                                logger.print_on_console(err_msg)
                                local_uo.log.error(err_msg)
                        else:
                            value,childSearchFlag = self.fetchcss(webelement, attr_name)
                            if value != '':
                                # show output
                                output = value
                                logger.print_on_console('Output: ', output)
                                status = TEST_RESULT_PASS
                                methodoutput = TEST_RESULT_TRUE
                            elif not childSearchFlag:
                                err_msg = 'CSS property does not exists'
                                logger.print_on_console(err_msg)
                                local_uo.log.error(err_msg)
                    else:
                        err_msg = 'Failed to fetch the attribute value.'
                        logger.print_on_console(err_msg)
                        local_uo.log.error(err_msg)
            elif not err_msg:
                err_msg = 'Input Error: Invalid number of inputs'
                logger.print_on_console(err_msg)
                local_uo.log.error(err_msg)
        except Exception as e:
            err_msg = 'Error occured while fetching attribute value'
            logger.print_on_console(err_msg)
            local_uo.log.error(e)
        return status,methodoutput,output,err_msg

    def verify_style(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        eleStatus=False
        index=0
        try:
            if webelement != None and webelement !='' and webelement.tag_name.lower()=='table' and len(input)!=1:
                if len(input) >= 4 and input[3] and int(input[3]) <= 0:
                    err_msg = self._index_zero()
                elif input[2]:
                    if(len(input) == 6 and all(v for v in input) and (not input[2] == 'tr')):
                        attr_name=input[4]
                        attr_value = input[5]
                        webelement1=None
                        row_number=int(input[0])-1
                        col_number=int(input[1])-1
                        tag=input[2].lower()
                        if input[3]: index=int(input[3])
                        eleStatus, webelement1 = self.get_table_cell(webelement, row_number, col_number, tag, index)
                        webelement=webelement1
                    elif(input[2]=='tr'): #fetch the attribute value of tr (index is needed)
                        if not(input[4]):
                            err_msg = 'Input Error: Please enter attribute name'
                            logger.print_on_console(err_msg)
                            local_uo.log.error(err_msg)
                        elif input[3] and int(input[3]) >= 1:
                            attr_name=input[4]
                            attr_value = input[5]
                            index=int(input[3])-1
                            tablerow_js='var targetTable = arguments[0]; var index = arguments[1]; var rowCount = targetTable.rows; return rowCount[index];'
                            webelement = browser_Keywords.local_bk.driver_obj.execute_script(tablerow_js,webelement,index)
                            eleStatus=True
                        elif input[3] and int(input[3]) <= 0:
                            err_msg = 'Invalid Input: Index input cannot be 0 for table'
                            logger.print_on_console(err_msg)
                            local_uo.log.error(err_msg)
                        else:
                            err_msg = 'Input Error: Missing index'
                            logger.print_on_console(err_msg)
                            local_uo.log.error(err_msg)
                # checking attribute value of table itself
                elif(len(input) == 6 and (not all(i for i in input[:-1]))):
                    attr_name=input[4]
                    attr_value = input[5]
                    eleStatus=True
                elif(len(input) == 6 and (not input[2])):
                    err_msg = 'Input Error: Please specify valid object type'
                    logger.print_on_console(err_msg)
                    local_uo.log.error(err_msg)
            elif(len(input)==2) and not err_msg:
                attr_name=input[0]
                attr_value = input[1]
                eleStatus=True
            if(eleStatus):
                if webelement.is_enabled()==False:
                    local_uo.log.error(ERR_DISABLED_OBJECT)
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    logger.print_on_console(ERR_DISABLED_OBJECT)
                else:
                    verify_result = browser_Keywords.local_bk.driver_obj.execute_script(webconstants.VERIFY_STYLE, webelement,attr_name,attr_value)
                    if verify_result:
                        logger.print_on_console("The style attribute matches.")
                        methodoutput = TEST_RESULT_TRUE
                        status = TEST_RESULT_PASS
                    else:
                        logger.print_on_console("The style attribute doesn't match.")
            elif not err_msg:
                err_msg = 'Input Error: Invalid number of inputs'
                logger.print_on_console(err_msg)
                local_uo.log.error(err_msg)
        except Exception as e:
            err_msg = 'Error occured while fetching style value'
            logger.print_on_console(err_msg)
            local_uo.log.error(e)
        return status,methodoutput,output,err_msg
    
    def get_element_count(self, webelement, input, *args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            if webelement.is_enabled()==False:
                local_uo.log.error(ERR_DISABLED_OBJECT)
                err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                logger.print_on_console(ERR_DISABLED_OBJECT)  
            else:     
                output = len(webelement.find_elements_by_xpath('.//*[contains(@value,"'+input[0]+'")]'))|len(webelement.find_elements_by_xpath('.//*[contains(@text,"'+input[0]+'")]'))
                logger.print_on_console("Count of elements with "+input[0]+" is "+str(output)+".")
                methodoutput = TEST_RESULT_TRUE
                status = TEST_RESULT_PASS
        except Exception as e:
            err_msg = 'Error occured while fetching element'
            logger.print_on_console(err_msg)
            local_uo.log.error(e)
        return status,methodoutput,output,err_msg
    
    def verify_attribute(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        eleStatus=False
        original_attr=None
        output=OUTPUT_CONSTANT
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        css_flag = False
        if input[-1].lower() == 'css':
            css_flag = True
            input.pop()
        try:
            if webelement != None and webelement !='' and webelement.tag_name.lower()=='table':
                if len(input) >= 4 and input[3] and int(input[3]) <= 0:
                    err_msg = self._index_zero()
                elif input[2]:
                    if((len(input)==5 or len(input)==6) and all(v for v in input) and (not input[2]=='tr')):
                        attr_name=input[4]
                        webelement1=None
                        row_number=int(input[0])-1
                        col_number=int(input[1])-1
                        tag=input[2].lower()
                        if input[3]: index=int(input[3])
                        eleStatus, webelement1 = self.get_table_cell(webelement, row_number, col_number, tag, index)
                        webelement=webelement1
                    elif(input[2]=='tr'): #fetch the attribute value of tr (index is needed)
                        if not(input[4]):
                            err_msg = 'Input Error: Please enter attribute name'
                            logger.print_on_console(err_msg)
                            local_uo.log.error(err_msg)
                        elif input[3] and int(input[3]) >= 1:
                            attr_name=input[4]
                            index=int(input[3])-1
                            tablerow_js='var targetTable = arguments[0]; var index = arguments[1]; var rowCount = targetTable.rows; return rowCount[index];'
                            webelement = browser_Keywords.local_bk.driver_obj.execute_script(tablerow_js,webelement,index)
                            eleStatus=True
                        elif input[3] and int(input[3]) <= 0:
                            err_msg = 'Invalid Input: Index input cannot be 0 for table'
                            logger.print_on_console(err_msg)
                            local_uo.log.error(err_msg)
                        else:
                            err_msg = 'Input Error: Please specify index'
                            logger.print_on_console(err_msg)
                            local_uo.log.error(err_msg)
                elif((len(input)==5 or len(input)==6 ) and (not all(ip for ip in input[0:4]))): #checking attribute value of table itself
                    attr_name=input[4]
                    eleStatus=True
                elif((len(input)==5 or len(input)==6 ) and (not input[2])):
                    err_msg = 'Input Error: Please specify valid object type'
                    logger.print_on_console(err_msg)
                    local_uo.log.error(err_msg)
            elif(len(input)==1 or len(input)==2) and not err_msg:
                attr_name=input[0]
                eleStatus=True
            # elif css_flag and (len(input) == 2 or len(input) == 3) and not err_msg:
            #     attr_name = input[0]
            #     eleStatus = True
            if(eleStatus):
                if webelement != None and webelement !='':
                    local_uo.log.info(INPUT_IS)
                    local_uo.log.info(input)
                    result=None
                    if attr_name:
                        if not css_flag:
                            if attr_name != 'required':
                                original_attr = webelement.get_attribute(attr_name)
                            else:
                                original_attr = browser_Keywords.local_bk.driver_obj.execute_script("return arguments[0].getAttribute('required')",webelement)
                            if original_attr != None and original_attr !='':
                                local_uo.log.info(original_attr)
                                if len(input)==6: result = input[5]
                                if len(input)==2: result = input[1]
                                if result:
                                    if original_attr == result:
                                        local_uo.log.info('Attribute exists and values matched')
                                        logger.print_on_console('Attribute exists and values matched')
                                        status = TEST_RESULT_PASS
                                        methodoutput = TEST_RESULT_TRUE
                                    else:
                                        err_msg = 'Attribute values does not match'
                                        logger.print_on_console(err_msg)
                                        local_uo.log.error(err_msg)
                                else:
                                    local_uo.log.info('Attribute exists')
                                    logger.print_on_console('Attribute exists')
                                    status = TEST_RESULT_PASS
                                    methodoutput = TEST_RESULT_TRUE
                            else:
                                err_msg = 'Attribute does not exixts'
                                logger.print_on_console(err_msg)
                                local_uo.log.error(err_msg)
                        elif css_flag:
                            # childSearchFlag = False
                            value,childSearchFlag=self.fetchcss(webelement,attr_name)
                            if value != '':
                                # show output
                                if len(input) == 6: result = input[5]
                                if len(input) == 2: result = input[1]
                                if result:
                                    if value == result:
                                        local_uo.log.info('CSS property exists and values matched')
                                        logger.print_on_console('CSS property exists and values matched')
                                        status = TEST_RESULT_PASS
                                        methodoutput = TEST_RESULT_TRUE
                                    else:
                                        err_msg = 'CSS property exists but values didn\'t matched'
                                        logger.print_on_console(err_msg)
                                        local_uo.log.error(err_msg)
                                else:
                                    local_uo.log.info('CSS property exists')
                                    logger.print_on_console('CSS property exists')
                                    status = TEST_RESULT_PASS
                                    methodoutput = TEST_RESULT_TRUE
                            elif not childSearchFlag:
                                err_msg = 'CSS property does not exists'
                                logger.print_on_console(err_msg)
                                local_uo.log.error(err_msg)
                    else:
                        err_msg = 'Attribute name is empty.'
                        logger.print_on_console(err_msg)
                        local_uo.log.error(err_msg)
                else:
                    err_msg = 'Web element not found'
                    logger.print_on_console(err_msg)
                    local_uo.log.error(err_msg)
            elif not err_msg:
                err_msg = 'Input Error: Invalid number of inputs'
                logger.print_on_console(err_msg)
                local_uo.log.error(err_msg)
        except NoSuchAttributeException as ex:
            err_msg = 'Attribute does not exixts'
            logger.print_on_console(err_msg)
            local_uo.log.error(ex)
        except ValueError as ex1:
            err_msg = 'Input Error: Please verify inputs'
            logger.print_on_console(err_msg)
            local_uo.log.error(ex1)
        except Exception as e:
            err_msg = 'Error occured while verifying attribute'
            logger.print_on_console(err_msg)
            local_uo.log.error(e)
        return status,methodoutput,output,err_msg

    def get_table_cell(self,webelement, row_number, col_number, tag, index):
        eleStatus=False
        webelement1=None
        counter = 1
        tableops = TableOperationKeywords()
        cell=tableops.javascriptExecutor(webelement,row_number,col_number)
        if(tag=='tablecell' or tag=='td'):
            eleStatus=True
            webelement1=cell
            return eleStatus,webelement1
        element_list=cell.find_elements_by_xpath('.//*')
        if len(element_list)==0:
            element_list.append(cell)
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
            elif tag=='radiobutton' or tag=='radio':
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
                if (tagName==('input') and (tagType==('text') or tagType==('email') or tagType==('password') or tagType==('range') or tagType==('search') or tagType==('url')) ):
                    if index==childindex:
                        eleStatus =True
                    else:
                        if counter==index:
                            index =childindex
                            eleStatus =True
                        else:
                            counter+=1
            elif tag=='link' or tag=='a':
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
                if tag==tagName:
                    if index==childindex:
                        eleStatus =True
                    else:
                        if counter==index:
                            index =childindex
                            eleStatus =True
                        else:
                            counter+=1
            if eleStatus==True:
                webelement1=cellChild
                break
        return eleStatus, webelement1

    def sendsecurefunction_keys(self,webelement,input,*args):
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            check_flag=True
            output=OUTPUT_CONSTANT
            input_val = input[0]
            if webelement is not None:
                try:
                    if webelement.is_enabled():
                        if webelement.tag_name == 'table':
                            if len(input) == 5 and int(input[3]) <= 0:
                                err_msg = self._index_zero()
                            elif len(input)==5:
                                row_num=int(input[0])
                                col_num=int(input[1])
                                obj_type=input[2].lower()
                                index_val=int(input[3])-1
                                inp_list=[]
                                inp_list.append(input[4])
                                local_uo.log.info(input)
                                row_count=self.tblobj.getRowCountJs(webelement)
                                col_count=self.tblobj.getColoumnCountJs(webelement)
                                input = inp_list
                                if (obj_type=="textbox" or obj_type=="input") and index_val>=0:
                                    if row_num>row_count or col_num>col_count:
                                        check_flag=False
                                        err_msg=self._invalid_input()
                                    else:
                                        cell=self.tblobj.javascriptExecutor(webelement,row_num-1,col_num-1)
                                        txt_box=cell.find_elements_by_tag_name('input')
                                        if len(txt_box)>0:
                                            if index_val >= len(txt_box):
                                                check_flag=False
                                                err_msg=self._invalid_index()
                                            else:
                                                webelement = txt_box[index_val]
                                        else:
                                            check_flag=False
                                            err_msg=self._invalid_input()
                                elif obj_type!= "textbox":
                                    check_flag=False
                                    err_msg=self._invalid_input()
                                else:
                                    check_flag=False
                                    err_msg=self._index_zero()
                        if check_flag==True and not err_msg:
                            local_uo.log.debug(WEB_ELEMENT_ENABLED)
                            if input_val!="":
                                input_val = input[0]
                                self.__setfocus(webelement)
                                from sendfunction_keys import SendFunctionKeys
                                obj=SendFunctionKeys()
                                result=obj.sendsecurefunction_keys(input_val,*args)
                                if result[0]!="Fail":
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                            else:
                                err_msg = 'input value is empty'
                                logger.print_on_console(err_msg)
                                local_uo.log.error(err_msg)
                except Exception as e:
                    local_uo.log.error("Error in sendsecurefunction_keys")
                    err_msg=self.__web_driver_exception(e)
            return status,methodoutput,output,err_msg


    def check_user_activation(self, browserlogs):
        if browserlogs and len(browserlogs) > 0:
            for i in browserlogs:
                if i['level'] == 'WARNING' and 'File chooser dialog can only be shown with a user activation' in i['message']:
                    local_uo.log.error(i['message'])
                    return False
        return True


    def fetchcss(self, webelement, attr_name):
        """
        Returns the attribute (attr_name) for the webelement if found. Referenced in get_attribute_value and verify_attribute
        """
        childSearchFlag=False
        props = {'border': ['border-top', 'border-right', 'border-bottom', 'border-left'],
                 'margin': ['margin-top', 'margin-right', 'margin-bottom', 'margin-left'],
                 'padding': ['padding-top', 'padding-right', 'padding-bottom', 'padding-left']}
        value = webelement.value_of_css_property(attr_name)
        if value == '' and attr_name in ['padding', 'margin', 'border', 'border-top', 'border-right', 'border-bottom', 'border-left']:
            # shorthands dict contains all the shorthand properties of the parent property seperated by ';'
            shorthands = {'margin': 'margin-top;margin-right;margin-bottom;margin-left','padding': 'padding-top;padding-right;padding-bottom;padding-left'}
            if attr_name in ['padding',"margin"] and isinstance(browser_Keywords.local_bk.driver_obj, webdriver.Firefox):
                temp = []
                for k in shorthands[attr_name].split(';'):
                    temp.append(webelement.value_of_css_property(k))
                if len(set(temp))==1: value = temp[0]
                else: value = ' '.join(temp)
            else:
                err_msg = 'Please find attribute value using either of ('
                if attr_name == 'border' and isinstance(browser_Keywords.local_bk.driver_obj, webdriver.Firefox):
                    try:
                        c1 = ['border-top','border-right','border-bottom','border-left']
                        c2 = ['-width', '-style', '-color']
                        temp=[]
                        for l in c1:
                            v=''
                            for m in c2:
                                attr = l + m
                                v+=' '
                                v += webelement.value_of_css_property(attr)
                            temp.append(v)
                        err_msg = None
                        if len(set(temp))==1:value=temp[0].lstrip()
                    except NoSuchAttributeException as ex:
                        err_msg += 'border-top border-right border-bottom border-left )'
                # if attr_name in list(props.keys()):
                #     for i in props[attr_name]:
                #         newValue = webelement.value_of_css_property(i)
                #         if newValue != '':
                #             err_msg += ' '
                #             err_msg += i
                #             childSearchFlag = True
                #     err_msg += ')'
                #     logger.print_on_console(err_msg)
                #     local_uo.log.error(err_msg)
                elif attr_name in ['border-top', 'border-right', 'border-bottom', 'border-left']:
                    finalValue = ''
                    for j in ['-width', '-style', '-color']:
                        attr = attr_name + j
                        val = webelement.value_of_css_property(attr)
                        if val != '':
                            finalValue += val
                            finalValue += ' '
                    if finalValue:
                        value = finalValue.rstrip()
        return value, childSearchFlag
    
    def send_secure_keys(self, webelement, input_value, *args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        text = False
        try:
            if len(input_value)==1:
                encryption_obj = AESCipher()
                decrypted_input_value = encryption_obj.decrypt(input_value[0])
                actions = ActionChains(browser_Keywords.local_bk.driver_obj)
                actions.send_keys(decrypted_input_value)
                actions.perform()
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg