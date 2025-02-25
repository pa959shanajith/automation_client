#-------------------------------------------------------------------------------
# Name:        utilweb_operations_MW.py
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
import browser_Keywords_MW
from utils_web_MW import Utils
from webconstants_MW import *
from constants import *
if SYSTEM_OS!='Darwin':
    from pyrobot_MW import Robot
    import win32gui
    import pyrobot_MW
import table_keywords_MW
import time
import readconfig
import urllib.request, urllib.parse, urllib.error, io
import logging


log = logging.getLogger('utilweb_operations_MW.py')

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
        self.verify_image_obj=None
        self.keys_info={}
        self.__create_keyinfo_dict()
        self.__load_Image_processingobj()

    def __load_Image_processingobj(self):
        try:
            from verify_file_images import VerifyFileImages
            self.verify_image_obj=VerifyFileImages()
        except ImportError: pass
        except Exception as e:
            log.error(e)



    def is_visible(self,webelement):
        flag=False
        log.debug('Checking the visibility of element')
        try:
            script="""var isVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })(); var s = arguments[0]; return isVisible(s);"""
            flag= browser_Keywords_MW.driver_obj.execute_script(script,webelement)
        except Exception as e:
            logger.print_on_console("ERR_WEB_DRIVER_EXCEPTION")
            log.error(e)
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
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)       
        return status,methodoutput,output,err_msg


    def verify_exists(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                #call to highlight the webelement
                if readconfig.configvalues['highlight_check'].strip().lower()=="yes":
                    self.highlight(webelement)
                # self.highlight(webelement)
                logger.print_on_console(ERROR_CODE_DICT['MSG_ELEMENT_EXISTS'])
                log.info(ERROR_CODE_DICT['MSG_ELEMENT_EXISTS'])
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            logger.print_on_console(err_msg)
            log.error(e)
        return status,methodoutput,output,err_msg

    def verify_doesnot_exists(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is None or webelement == '':
            message=ERROR_CODE_DICT['ERR_ELEMENT_NOT_EXISTS']
            logger.print_on_console(message)
            log.info(message)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        else:
            err_msg=ERROR_CODE_DICT['MSG_ELEMENT_EXISTS']
            log.info(err_msg)
            logger.print_on_console(err_msg)
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
                visibility=webelement.is_displayed()
                if visibility:
                    self.highlight(webelement)
                    if readconfig.configvalues['ignoreVisibilityCheck'].strip().lower()=="no":
                        res=self.is_visible(webelement)
                    else:
                        res=True
                    if webelement.is_enabled() and not(res):
                        info_msg=ERROR_CODE_DICT['The object is Hidden']
                        logger.print_on_console(info_msg)
                        log.info(info_msg)
                    elif webelement.is_enabled() and res:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        info_msg=ERROR_CODE_DICT['MSG_OBJECT_ENABLED']
                        logger.print_on_console(info_msg)
                        log.info(info_msg)
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                else:
                    err_msg=ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
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
                flag=False
                unselectable_val=webelement.get_attribute('unselectable')
                log.info('unselectable_val ',unselectable_val)
                if (unselectable_val!=None and unselectable_val.lower()=='on'):
                    flag=True
                log.info('Disabled flag value ',str(flag))
                if not(webelement.is_enabled()) or flag:
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                    info_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
                    logger.print_on_console(info_msg)
                    log.info(info_msg)
                else:
                    err_msg=ERROR_CODE_DICT['MSG_OBJECT_ENABLED']
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
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
                    log.error(err_msg)
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
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
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,methodoutput,output,err_msg


    def highlight(self,webelement):
        try:
            if browser_Keywords_MW.driver_obj is not None:
                browser_info=browser_Keywords_MW.driver_obj.capabilities
                browser_name=browser_info.get('browserName')
                browser_version=browser_info.get('version')
                ##log.info('Browser is:'+browser_name+'Version is:'+browser_version)
                #get the original style of the element
                original_style = webelement.get_attribute('style')
                #Apply css to the element
                #check if driver instance is IE
                if isinstance(browser_Keywords_MW.driver_obj,webdriver.Ie):
                    browser_Keywords_MW.driver_obj.execute_script(HIGHLIGHT_SCRIPT_IE,webelement,original_style+APPLY_CSS)
                else:
                    browser_Keywords_MW.driver_obj.execute_script(HIGHLIGHT_SCRIPT,webelement,original_style+APPLY_CSS)

                #highlight remains for 3 secs on the element
                import time
                time.sleep(3)

                #Remove css from the element  and applying the original style back to the element
                #check if driver instance is IE
                if isinstance(browser_Keywords_MW.driver_obj,webdriver.Ie):
                    if '8' in browser_version:
                        browser_Keywords_MW.driver_obj.execute_script(HIGHLIGHT_SCRIPT_IE,webelement,original_style+REMOVE_CSS_IE8)
                    else:
                        browser_Keywords_MW.driver_obj.execute_script(HIGHLIGHT_SCRIPT_IE,webelement,original_style)
                else:
                    browser_Keywords_MW.driver_obj.execute_script(HIGHLIGHT_SCRIPT,webelement,original_style)
        except Exception as e:
            logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
            log.error(e)


    def __setfocus(self,webelement):
        status=TEST_RESULT_FAIL
        if browser_Keywords_MW.driver_obj is not None:
            browser_Keywords_MW.driver_obj.execute_script(FOUCS_ELE,webelement)
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
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            log.error(e)
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
            if isinstance(browser_Keywords_MW.driver_obj,webdriver.Chrome):
                self.__setfocus(webelement)
                robot=Robot()
                robot.key_press('tab')
                robot.key_release('tab')
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output,err_msg

    def iossendkey(self, webelement,input,*args):
        #print "send"
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                #print "webele"
                #print "inputt::",input
                input=input[0]
                if input is not None:
                    if input.lower() == "enter":
                        #print "enter"
                        webelement.send_keys(Keys.ENTER)
                    elif input.lower() == "tab":
                        webelement.send_keys(Keys.TAB)
                    elif input.lower() == "backspace":
                        webelement.send_keys(Keys.BACKSPACE)
                    elif input.lower() == "uparrow":
                        webelement.send_keys(Keys.ARROW_UP)
                    elif input.lower() == "downarrow":
                        webelement.send_keys(Keys.ARROW_DOWN)
                    elif input.lower() == "leftarrow":
                        webelement.send_keys(Keys.ARROW_LEFT)
                    elif input.lower() == "rightarrow":
                        webelement.send_keys(Keys.ARROW_RIGHT)
                    elif input.lower() == "a":
                        webelement.send_keys("a")
                    elif input.lower() == "b":
                        webelement.send_keys("b")
                    # elif input.lower() == "ctrl":
                    #     webelement.send_keys()
                    #key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
                    logger.print_on_console("Given "+str(input))
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
            except Exception as e:
                log.error(e)
                logger.print_on_console(e)

                err_msg = ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        log.info(RETURN_RESULT)
        return status, methodoutput, output, err_msg

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
                if len(args)==0 and input in list(self.keys_info.keys()):
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
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            log.error(e)
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
                    table_keywords_MW_obj=table_keywords_MW.TableOperationKeywords()
                    actual_xpath=table_keywords_MW_obj.getElemntXpath(webelement)
                    element = browser_Keywords_MW.driver_obj.find_element_by_xpath(actual_xpath)
                    cell=table_keywords_MW_obj.javascriptExecutor(element,row_num-1,col_num-1)
                    ele_coordinates=cell.location_once_scrolled_into_view
                    log.debug(ele_coordinates)
                    hwnd=win32gui.GetForegroundWindow()
                    log.debug('Handle found ')
                    log.debug(hwnd)
                    if isinstance(browser_Keywords_MW.driver_obj,webdriver.Firefox):
                        info_msg='Firefox browser'
                        log.info(info_msg)
                        logger.print_on_console(info_msg)
                        javascript = "return window.mozInnerScreenY"
                        value=browser_Keywords_MW.driver_obj.execute_script(javascript)
                        offset=int(value)
                        robot=pyrobot_MW.Robot()
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
                        robot=pyrobot_MW.Robot()
                        log.debug('Setting the mouse position')
                        robot.set_mouse_pos(ele_coordinates.get('x')+9,ele_coordinates.get('y')+rect[0])
                        robot.mouse_down('left')
                        log.debug('Mouse click performed')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            log.error(e)
        return status,methodoutput,output,err_msg

    def verify_web_images(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            from PIL import Image
            if webelement!=None and webelement !='':
                img_src = webelement.get_attribute("src")
                file1 = io.BytesIO(urllib.request.urlopen(img_src).read())
                file2=input[0]
                log.info(INPUT_IS)
                log.info(file2)
                if file1 != None and file2 != None and  file2 != '' and os.path.exists(file2) :
                    log.debug('comparing the images')
                    if self.verify_image_obj != None: #Meaning user has advanced image processing plugin
                        if self.verify_image_obj.imagecomparison(file1,file2):
                            info_msg=ERROR_CODE_DICT['MSG_IMAGE_COMPARE_PASS']
                            log.info(info_msg)
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
                                log.info(info_msg)
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
                log.error(err_msg)
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            log.error(e)
        return status,methodoutput,output,err_msg

    def image_similarity_percentage(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            from PIL import Image
            if webelement!=None and webelement !='':
                img_src = webelement.get_attribute("src")
                file1 = io.BytesIO(urllib.request.urlopen(img_src).read())
                file2=input[0]
                log.info(INPUT_IS)
                log.info(file2)
                if file1 != None and file2 != None and  file2 != '' and os.path.exists(file2) :
                    log.debug('comparing the images')
                    if self.verify_image_obj != None: #Meaning user has advanced image processing plugin
                        if self.verify_image_obj.imagecomparison(file1,file2):
                            info_msg=ERROR_CODE_DICT['MSG_IMAGE_COMPARE_PASS']
                            log.info(info_msg)
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
                            log.info('Result is ',output)
                            logger.print_on_console('Result is ',output)
                else:
                    err_msg=ERROR_CODE_DICT['ERR_NO_IMAGE_SOURCE']
                if err_msg != None:
                    logger.print_on_console(err_msg)
                    log.error(err_msg)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=INPUT_ERROR
        return status,methodoutput,output,err_msg

    
    def get_element_tag_value(self,webelement,*args):
        # get_element_tag_value
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                    output = str(webelement.tag_name)
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    logger.print_on_console('Result: ',output)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
            except Exception as e:
                err_msg="exception occur in get element tag value"
                log.error(e)
            if err_msg is not None:
                logger.print_on_console(err_msg)
                log.error(err_msg)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def get_attribute_value(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output=None
        attr_name=input[0]
        eleStatus=False
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if(len(input)==3):
                row_number=int(input[1])-1
                col_number=int(input[2])-1
                from table_keywords import TableOperationKeywords
                tableops = TableOperationKeywords()
                cell=tableops.javascriptExecutor(webelement,row_number,col_number)
                element_list=cell.find_elements_by_xpath('.//*')
                if len(list(element_list))>0:
                    xpath=tableops.getElemntXpath(element_list[0])
                    cell=browser_Keywords.local_bk.driver_obj.find_element_by_xpath(xpath)
                if(cell!=None):
                    webelement=cell
                    eleStatus=True
            elif(len(input)>3):
                webelement1=None
                row_number=int(input[1])-1
                col_number=int(input[2])-1
                tag=input[3].lower()
                index=int(input[4])
                eleStatus, webelement1=self.get_table_cell(webelement, row_number, col_number, tag, index)
                if(webelement1):
                    webelement=webelement1
                
            if(eleStatus or len(input)==1):
                if webelement != None and webelement !='':
                    local_uo.log.info(INPUT_IS)
                    local_uo.log.info(input)
                    if attr_name:
                        if attr_name != 'required':
                            output = webelement.get_attribute(attr_name)
                        else:
                            output = browser_Keywords.local_bk.driver_obj.execute_script("return arguments[0].getAttribute('required')",webelement)
                        if output != None and output !='':
                            logger.print_on_console('Output: ',output)
                            status = TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                        else:
                            err_msg = 'Attribute does not exists'
                            logger.print_on_console(err_msg)
                            local_uo.log.error(err_msg)
                    else:
                        err_msg = 'Failed to fetch the attribute value.'
                        logger.print_on_console(err_msg)
                        local_uo.log.error(err_msg)
        except Exception as e:
            err_msg = 'Error occured while fetching attribute value'
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
        attr_name=input[0]
        local_uo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if(len(input)==4):
                row_number=int(input[2])-1
                col_number=int(input[3])-1
                from table_keywords import TableOperationKeywords
                tableops = TableOperationKeywords()
                cell=tableops.javascriptExecutor(webelement,row_number,col_number)
                element_list=cell.find_elements_by_xpath('.//*')
                if len(list(element_list))>0:
                    xpath=tableops.getElemntXpath(element_list[0])
                    cell=browser_Keywords.local_bk.driver_obj.find_element_by_xpath(xpath)
                if(cell!=None):
                    webelement=cell
                    eleStatus=True

            elif(len(input)>4):
                webelement1=None
                row_number=int(input[2])-1
                col_number=int(input[3])-1
                tag=input[4].lower()
                index=int(input[5])+1
                eleStatus, webelement1=self.get_table_cell(webelement, row_number, col_number, tag, index)
                if(webelement1):
                    webelement=webelement1

            if(eleStatus or len(input)<=2):
                if webelement != None and webelement !='':
                    local_uo.log.info(INPUT_IS)
                    local_uo.log.info(input)
                    if attr_name:
                        if attr_name != 'required':
                            original_attr = webelement.get_attribute(attr_name)
                        else:
                            original_attr = browser_Keywords.local_bk.driver_obj.execute_script("return arguments[0].getAttribute('required')",webelement)
                        if original_attr != None and original_attr !='':
                            local_uo.log.info(original_attr)
                            if len(input)==2 and input[1] != '':
                                result = input[1]
                                if original_attr == result:
                                    local_uo.log.info('Attribute values matched')
                                    logger.print_on_console('Attribute values matched')
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
                    else:
                        err_msg = 'Input is empty.'
                        logger.print_on_console(err_msg)
                        local_uo.log.error(err_msg)
                else:
                    err_msg = 'Web element not found'
                    logger.print_on_console(err_msg)
                    local_uo.log.error(err_msg)
        except NoSuchAttributeException as ex:
            err_msg = 'Attribute does not exixts'
            logger.print_on_console(err_msg)
            local_uo.log.error(ex)
        except Exception as e:
            err_msg = 'Error occured while verifying attribute'
            logger.print_on_console(err_msg)
            local_uo.log.error(e)
        return status,methodoutput,output,err_msg





