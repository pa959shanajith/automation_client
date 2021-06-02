#-------------------------------------------------------------------------------
# Name:        button_link_keyword.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     08-11-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import logger
import webconstants
import time
from selenium import webdriver
from constants import SYSTEM_OS
if SYSTEM_OS == 'Windows' :
    from pyrobot import Robot, Keys
    import win32process
import browser_Keywords
import logging
from constants import *
import core_utils
import threading
from string_ops_keywords import *
from utilweb_operations import *
import pyautogui
import psutil
local_blk = threading.local()
##text_javascript = """function stext_content(f) {     var sfirstText = '';     var stextdisplay = '';     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     return (stextdisplay); }; return stext_content(arguments[0])"""
class ButtonLinkKeyword():
    def __init__(self):
        local_blk.log = logging.getLogger('button_link_keyword.py')
        local_blk.text_javascript = """function stext_content(f) {     var sfirstText = '';     var stextdisplay = '';     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     return (stextdisplay); }; return stext_content(arguments[0])"""
        #self.copy_text=None

    def click(self,webelement,*args):
        local_blk.log.debug('Got the driver object from browser keyword class')
        local_blk.log.debug(browser_Keywords.local_bk.driver_obj)
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        clickinfo=None
        output=OUTPUT_CONSTANT
        local_blk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        #click keyword implementation
        try:
            if webelement != None:
                local_blk.log.info('Recieved web element from the web dispatcher')
                local_blk.log.debug(webelement)
                local_blk.log.debug('Check for the element enable')
                if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Firefox ):
                    browser_Keywords.local_bk.driver_obj.execute_script('arguments[0].scrollIntoView()',webelement)
                if webelement.tag_name =='input' and webelement.get_attribute("type") == 'file':
                    local_blk.log.info(WEB_ELEMENT_FILE_TYPE)
                    err_msg=ERROR_CODE_DICT['CLICKABLE_EXCEPTION']
                    logger.print_on_console(ERROR_CODE_DICT['CLICKABLE_EXCEPTION'])
                elif webelement.is_enabled():
                    local_blk.log.debug(WEB_ELEMENT_ENABLED)
                    if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Ie):
                        local_blk.log.info('Opened browser : Internet Explorer Instance')
                        try:
                            local_blk.log.debug('Going to perform click operation')
                            clickinfo = browser_Keywords.local_bk.driver_obj.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                            time.sleep(5)
                            local_blk.log.info('Click operation performed using javascript click')
                            local_blk.log.debug('click operation info: ')
                            local_blk.log.debug(clickinfo)
                            local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                        except Exception as e:
                            local_blk.log.error('Javascript error occured, Trying to click using Action class')
                            webdriver.ActionChains(browser_Keywords.local_bk.driver_obj).move_to_element(webelement).click(webelement).perform()
                            local_blk.log.info('click operation  info: Clicked using Actions class')
                            local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE

                    elif SYSTEM_OS == 'Darwin' or SYSTEM_OS == 'Linux':
                        try:
                            clickinfo = browser_Keywords.local_bk.driver_obj.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                            local_blk.log.info('Click operation performed using javascript click')
                            local_blk.log.debug('click operation info: ')
                            local_blk.log.debug(clickinfo)
                            local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                        except Exception as e:
                            local_blk.log.debug('Going to perform click operation')
                            time.sleep(0.5)
                            webelement.click()
                            local_blk.log.info('Click operation performed using selenium click')
                            local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                    else:
                        try:
                            local_blk.log.debug('Going to perform click operation')
                            time.sleep(0.5)
                            local_blk.log.debug(webelement)
                            if len(args)>0 and args[0][0]!='':
                                coords=args[0][0].split(',')
                                x_coord = coords[0]
                                y_coord = coords[1]
                                if(len(coords)==2):
                                    action = webdriver.common.action_chains.ActionChains(browser_Keywords.local_bk.driver_obj)
                                    logger.print_on_console("Clicking on coordinates "+x_coord+", "+y_coord)
                                    action.move_to_element_with_offset(webelement, int(x_coord), int(y_coord)).click().perform()
                                    status = webconstants.TEST_RESULT_PASS
                                    methodoutput = webconstants.TEST_RESULT_TRUE
                                else:
                                    err_msg = 'Invalid number of coordinates given!'
                                    logger.print_on_console(err_msg)
                                # Js="""function clickon(x,y){var ev=document.createEvent("MouseEvent");var el=document.elementFromPoint(x,y);ev.initMouseEvent("click",true,true,window,null,x,y,0,0,false,false,false,false,0,null);el.dispatchEvent(ev);} arguments[0].clickon(arguments[1],arguments[2])"""
                                # browser_Keywords.local_bk.driver_obj.execute_script(Js,webelement,x_coord,y_coord)
                            else:
                                clickinfo = browser_Keywords.local_bk.driver_obj.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                                status = webconstants.TEST_RESULT_PASS
                                methodoutput = webconstants.TEST_RESULT_TRUE
                                local_blk.log.info('Click operation performed using javascript click')
                                local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                        except Exception as e:
                            # local_blk.log.info('Click operation performed using javascript click')
                            # local_blk.log.error('selenium click  error occured, Trying to click using Javascript')
                            webelement.click()
                            local_blk.log.info('Click operation performed using selenium click')
                            local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    local_blk.log.info(WEB_ELEMENT_DISABLED)
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            local_blk.log.error(e)
            local_blk.log.error(err_msg)
            logger.print_on_console(err_msg)
            
        local_blk.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def get_button_name(self,webelement,inputs,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        local_blk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        #verify_button_name keyword implementation
        try:
            if webelement != None:
                local_blk.log.info('Recieved web element from the web dispatcher')
                local_blk.log.debug(webelement)
                #fetch the text (button name) using selenium webelement.text
                local_blk.log.debug('Going to fetch the button name')
                buttonname = webelement.text
                local_blk.log.info('Button name fetched from the AUT using selenium')

                if buttonname != None and len(buttonname)>0:
                    output = buttonname
                    logger.print_on_console('Button name : ' , buttonname)
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE

                if buttonname == None or len(buttonname) == 0:
                    local_blk.log.debug('Button name not recieved using selenium text method, Getting value attribute')
                    #if text is empty search for the value attribute
                    buttonname = webelement.get_attribute(webconstants.VALUE)
                    local_blk.log.info('Button name fetched from the AUT using value attribute')
                    local_blk.log.info(buttonname)
                    logger.print_on_console('Button name : ' , buttonname)
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                    output = buttonname
                if buttonname == None or len(buttonname) == 0:
                    local_blk.log.debug('Button name not recieved using selenium text method/ value attribute, Getting name attribute')
                    #if value is empty search for the name attribute
                    buttonname = webelement.get_attribute(webconstants.NAME)
                    local_blk.log.info('Button name fetched from the AUT using name attribute')
                    local_blk.log.info(buttonname)
                    logger.print_on_console('Button name : ' , buttonname)
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                    output = buttonname
        except Exception as e:
            local_blk.log.error(e)
            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        return status,methodoutput,output,err_msg

    def verify_button_name(self,webelement,inputs,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_blk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        #verify_button_name keyword implementation
        try:
            if webelement != None:
                local_blk.log.info('Recieved web element from the web dispatcher')
                local_blk.log.debug(webelement)
                #fetch the text (button name) using selenium webelement.text
                local_blk.log.debug('Going to fetch the button name')
                buttonname = webelement.text
                local_blk.log.info('Button name fetched from the AUT using selenium')
                logger.print_on_console('Button name : ' , buttonname)

                if buttonname == None or len(buttonname) == 0:
                    local_blk.log.debug('Button name not recieved using selenium text method, Getting value attribute')
                    #if text is empty search for the value attribute
                    buttonname = webelement.get_attribute(webconstants.VALUE)
                    local_blk.log.info('Button name fetched from the AUT using value attribute')
                    local_blk.log.info(buttonname)
                    logger.print_on_console('Button name : ' , buttonname)
                if buttonname == None or len(buttonname) == 0:
                    local_blk.log.debug('Button name not recieved using selenium text method/ value attribute, Getting name attribute')
                    #if value is empty search for the name attribute
                    buttonname = webelement.get_attribute(webconstants.NAME)
                    local_blk.log.info('Button name fetched from the AUT using name attribute')
                    local_blk.log.info(buttonname)
                    logger.print_on_console('Button name : ' , buttonname)

                #Remove the leading and trailing spaces
                input = inputs[0]
                input = input.strip()
                logger.print_on_console('Input text : ' , input)
                #Check for the input
                if input != None and len(input) != 0:
                    local_blk.log.info('Input is valid, Continue..')
                    coreutilsobj=core_utils.CoreUtils()
                    input=coreutilsobj.get_UTF_8(input)
                    if buttonname == input:
                        local_blk.log.info('Button name matched with the input, set the status to Pass')
                        logger.print_on_console('Button name  matched')
                        local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = webconstants.TEST_RESULT_PASS
                        methodoutput = webconstants.TEST_RESULT_TRUE
                    else:
                        err_msg='Button name mismatched'
                        local_blk.log.info('Button name does not matched with the input, set the status to Fail')
                        logger.print_on_console(err_msg)
                        logger.print_on_console(EXPECTED,input)
                        local_blk.log.info(EXPECTED)
                        local_blk.log.info(input)
                        logger.print_on_console(ACTUAL,buttonname)
                        local_blk.log.info(ACTUAL)
                        local_blk.log.info(buttonname)

                else:
                    local_blk.log.error(INVALID_INPUT)
                    err_msg=INVALID_INPUT
                    logger.print_on_console(INVALID_INPUT)

        except Exception as e:
            local_blk.log.error(e)

            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        local_blk.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def get_link_text(self,webelement,input,*args):
        #get_link_text keyword implementation
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        local_blk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        linktext = None
        err_msg = None
        try:
            if webelement != None:
                local_blk.log.info('Recieved web element from the web dispatcher')
                local_blk.log.debug(webelement)
                local_blk.log.debug('Getting href attribute')
                linktext = browser_Keywords.local_bk.driver_obj.execute_script(local_blk.text_javascript,webelement)
##                import ftfy
##                linktext = ftfy.fix_text(linktext)
                coreutilsobj=core_utils.CoreUtils()
                linktext=coreutilsobj.get_UTF_8(linktext)
                linktext = linktext.replace('\n','')
                linktext = linktext.strip()
                if linktext == None or linktext == '':
                    linktext = webelement.get_attribute(webconstants.HREF)
##                    local_blk.log.info('Link text: ' +text)
                if linktext == None or linktext == '':
##                    local_blk.log.info('Web element is a valid link and it has href attribute')
                    linktext = webelement.text
##                    local_blk.log.info('Link text: ' +linktext)
                logger.print_on_console('Link text: ' )
                logger.print_on_console(linktext)
                if linktext != None and linktext !='':
##                    local_blk.log.info('Web element is a valid link and it has href attribute')
##                    linktext = webelement.text
##                    if linktext == None:
##                        linktext = ''
                    local_blk.log.info('Link text: ' +linktext)
                    local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    err_msg='There is no link text for the given element'
                    logger.print_on_console(err_msg)
                    local_blk.log.info(err_msg)
##            else:
##                logger.print_on_console('Element not found')
##            print 'Keyword result: ',status

        except Exception as e:
            local_blk.log.error(e)

            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        local_blk.log.info(RETURN_RESULT)
        return status,methodoutput,linktext,err_msg

    def verify_link_text(self,webelement,inputs,*args):
        #verify_link_text keyword implementation
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_blk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement != None:
                input = inputs[0]
                input = input.strip()
                coreutilsobj=core_utils.CoreUtils()
                input=coreutilsobj.get_UTF_8(input)
                if input != None and len(input) != 0:
                    local_blk.log.debug('Input is valid, Continue..')
                    local_blk.log.debug('Getting href attribute')
                    linktext = browser_Keywords.local_bk.driver_obj.execute_script(local_blk.text_javascript,webelement)
##                    import ftfy
##                    linktext = ftfy.fix_text(linktext)
                    linktext=coreutilsobj.get_UTF_8(linktext)
                    linktext = linktext.replace('\n','')
                    linktext = linktext.strip()
                    if linktext == None or linktext == '':
                        linktext = webelement.get_attribute(webconstants.HREF)
                        local_blk.log.info('Link text: ' +linktext)
                    if linktext == None or linktext == '':
                        local_blk.log.info('Web element is a valid link and it has href attribute')
                        linktext = webelement.text
                        local_blk.log.info('Link text: ' +linktext)
                    if linktext != None and linktext !='':
                        if linktext == input:
                            err_msg='Link Text matched'
                            logger.print_on_console(err_msg)
                            local_blk.log.info(err_msg)
                            local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                        else:
                            err_msg='Link Text mismatched'
                            logger.print_on_console(err_msg)
                            local_blk.log.info(err_msg)
                            logger.print_on_console(EXPECTED,input)
                            local_blk.log.info(EXPECTED)
                            local_blk.log.info(input)
                            logger.print_on_console(ACTUAL,linktext)
                            local_blk.log.info(ACTUAL)
                            local_blk.log.info(linktext)
                    else:
                        err_msg='There is no link text for the given element'
                        logger.print_on_console(err_msg)
                        local_blk.log.info(err_msg)
                else:
                    err_msg=INVALID_INPUT
                    local_blk.log.error(err_msg)
                    logger.print_on_console(err_msg)
        except Exception as e:
            local_blk.log.error(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            local_blk.log.error(err_msg)
            logger.print_on_console(err_msg)
        local_blk.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    #Below keyword specifically written for to support mnt CBU
    def press(self,webelement,input,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_blk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
       #press keyword implementation
        try:
            if webelement != None:
                local_blk.log.info('Recieved web element from the web dispatcher')
                local_blk.log.debug(webelement)
                local_blk.log.debug('Check for the element enable')
                if webelement.is_enabled():
                    if webelement.tag_name =='input' and webelement.get_attribute("type") == 'file':
                        local_blk.log.info(WEB_ELEMENT_FILE_TYPE)
                        err_msg=ERROR_CODE_DICT['PRESSABLE_EXCEPTION']
                    else:
                        local_blk.log.debug(WEB_ELEMENT_ENABLED)
                        local_blk.log.debug('Going to perform click operation')
                        time.sleep(0.5)
                        webelement.click()
                        local_blk.log.info('press operation performed using selenium click')
                        local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = webconstants.TEST_RESULT_PASS
                        methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    err_msg = WEB_ELEMENT_DISABLED
        except Exception as e:
            local_blk.log.error(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        if err_msg:
            local_blk.log.error(err_msg)
            logger.print_on_console(err_msg)
        local_blk.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def double_click(self,webelement,input,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_blk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
       #double_click keyword implementation
        try:
            if webelement != None:
                local_blk.log.info('Recieved web element from the web dispatcher')
                local_blk.log.debug(webelement)
                local_blk.log.debug('Check for the element enable')
                if webelement.is_enabled():
                    webdriver.ActionChains(browser_Keywords.local_bk.driver_obj).move_to_element(webelement).double_click(webelement).perform()
                    local_blk.log.info('double click operation performed using Action class')
                    local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    err_msg = WEB_ELEMENT_DISABLED
        except Exception as e:
            local_blk.log.error(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        if err_msg:
            local_blk.log.error(err_msg)
            logger.print_on_console(err_msg)
        local_blk.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def right_click(self,webelement,input,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_blk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
       #right_click keyword implementation
        try:
            if webelement != None:
                local_blk.log.info('Recieved web element from the web dispatcher')
                local_blk.log.debug(webelement)
                local_blk.log.debug('Check for the element enable')
                if webelement.is_enabled():
                    webdriver.ActionChains(browser_Keywords.local_bk.driver_obj).move_to_element(webelement).context_click(webelement).perform()
                    local_blk.log.info('right click operation performed using Action class')
                    local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    err_msg = WEB_ELEMENT_DISABLED
        except Exception as e:
            local_blk.log.error(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        if err_msg:
            local_blk.log.error(err_msg)
            logger.print_on_console(err_msg)
        local_blk.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def upload_file(self,webelement,inputs,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        local_blk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        #upload_file keyword implementation
        try:
            filepath = inputs[0]
            filename = inputs[1]
            inputfile = os.path.join(filepath, filename)
            if webelement != None:
                local_blk.log.info('Recieved web element from the web dispatcher')
                local_blk.log.debug(webelement)
                local_blk.log.debug('Check for the element enable')
                if webelement.is_enabled():
                    if webelement.tag_name =='input' and webelement.get_attribute('type') == 'file':
                        if os.path.isfile(inputfile):
                            webelement.send_keys(inputfile)
                            status = webconstants.TEST_RESULT_PASS
                        else:
                            err_msg=ERROR_CODE_DICT['ERR_IIO_EXCEPTION']
                    elif SYSTEM_OS == 'Windows' and isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Firefox):
                        local_blk.log.debug('Mozilla Firefox Instance')
                        clickinfo = browser_Keywords.local_bk.driver_obj.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                        local_blk.log.info('upload_file click info')
                        local_blk.log.info(clickinfo)
                        filestatus = self.__upload_operation(inputfile,inputs)
                        local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                        if filestatus:
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                    else:
                        if self.__click_for_file_upload(browser_Keywords.local_bk.driver_obj,webelement):
                            filestatus =self.__upload_operation(inputfile,inputs)
                            local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                            if filestatus:
                                status = webconstants.TEST_RESULT_PASS
                                methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    err_msg = WEB_ELEMENT_DISABLED
        except Exception as e:
            local_blk.log.error(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        if err_msg:
            local_blk.log.error(err_msg)
            logger.print_on_console(err_msg)
        local_blk.log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def get_ppid_browser(self):
        ppid=None
        browser_name = browser_Keywords.local_bk.driver_obj.capabilities.get('browserName')
        platform_name = browser_Keywords.local_bk.driver_obj.capabilities.get('platformName')
        try:
            if platform_name != 'Darwin':
                if (browser_name == 'chrome'):
                    ppid = browser_Keywords.local_bk.driver_obj.service.process.pid
                elif(browser_name == 'firefox'):
                    if hasattr(browser_Keywords.local_bk.driver_obj, 'binary'):
                        ppid = browser_Keywords.local_bk.driver_obj.binary.process.pid
                    else:
                        ppid = browser_Keywords.local_bk.driver_obj.service.process.pid
                elif(browser_name == 'internet explorer'):
                    ppid = browser_Keywords.local_bk.driver_obj.iedriver.process.pid
                elif(browser_name == 'edge legacy') or (browser_name == 'edge chromium'):
                    ppid = browser_Keywords.local_bk.driver_obj.edge_service.process.pid
        except Exception as e:
            local_blk.log.debug("Problem while getting the ppid: {}".format(e))
        
        return ppid

    def check_fileDialogOpen(self):
        hwnds = []
        ppid = self.get_ppid_browser()
        if ppid == None:
            return False
        def winEnumHandler(hwnd, hwnd_list):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == "Open":
                hwnd_list.append(hwnd)
        win32gui.EnumWindows(winEnumHandler, hwnds)
        pids = [win32process.GetWindowThreadProcessId(h)[1] for h in hwnds]
        ppids = [psutil.Process(p).parent().ppid() for p in pids]
        return ppid in ppids

    def upload_time_func(self,tries=10, time_sleep=0.5):
        while tries > 0:
            if self.check_fileDialogOpen():
                local_blk.log.info("Window Found and returning the true")
                return True
            time.sleep(time_sleep)
            tries -= 1
        return False

    def __upload_operation(self,inputfile,args):
        status = False
        try:
            local_blk.log.debug('using Robot class to perform keyboard operation')
            robot = Robot()
            time.sleep(1)
            #self.__set_clipboard_data(inputfile)
            robot.sleep(1)
            maxTries = 10
            time_sleep = 0.5
            if len(args) > 2:
                maxTries = int(int(args[2]) / time_sleep)
            result_call = self.upload_time_func(maxTries, time_sleep)
            if result_call!=False:
                pyautogui.PAUSE = 1
                pyautogui.keyDown('alt')
                pyautogui.keyDown('n')
                pyautogui.PAUSE = 1
                pyautogui.keyUp('alt')
                pyautogui.keyUp('n')
                pyautogui.PAUSE = 1
                pyautogui.typewrite(inputfile, interval=0.25)
                pyautogui.PAUSE = 1
                pyautogui.keyDown('enter')
                pyautogui.PAUSE = 1
                pyautogui.keyUp('enter')
                pyautogui.PAUSE = 1
                status = True
            else:
                status = False
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            local_blk.log.error(EXCEPTION_OCCURED)
            local_blk.log.error(e)
        return status

    def __set_clipboard_data(self,inputfile):
        status = False
        try:
            #robot = Robot()
            #SO = StringOperation()
            local_blk.log.debug('Copying input file path to the clipboard')
            #robot.add_to_clipboard(inputfile.encode(encoding='utf8'))
            #SO.save_to_clip_board(inputfile.encode(encoding='utf8'))
            #self.copy_text=robot.get_clipboard_data().decode('utf8')
            #self.copy_text=SO.get_from_clip_board()
            local_blk.log.debug(' input file path Copied to  clipboard')
            status = True
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            local_blk.log.error(EXCEPTION_OCCURED)
            local_blk.log.error(e)
        return status
    def __click_for_file_upload(self,driver,webelement):
        status = False
        try:
            if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Ie):
                try:
                    local_blk.log.info("IE: Click operation performed using mousehover and keydown")
                    UW=UtilWebKeywords()
                    browser_Keywords.local_bk.driver_obj.execute_script(webconstants.FOUCS_ELE,webelement)
                    UW.mouse_hover(webelement,(1,))
                    pyautogui.PAUSE = 1
                    pyautogui.keyDown('enter')
                    #pyautogui.press('enter')
                    pyautogui.PAUSE = 1
                    pyautogui.keyUp('enter')
                except:
                    local_blk.log.debug('Going to perform click operation')
                    clickinfo = browser_Keywords.local_bk.driver_obj.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                    local_blk.log.info('Click operation performed using javascript click')
                    local_blk.log.debug('click operation info: ')
                    local_blk.log.debug(clickinfo)
                local_blk.log.info(STATUS_METHODOUTPUT_UPDATE)
                status = True
            else:
                try:
                    local_blk.log.info("Click operation performed using mousehover and keydown")
                    UW=UtilWebKeywords()
                    browser_Keywords.local_bk.driver_obj.execute_script(webconstants.FOUCS_ELE,webelement)
                    UW.mouse_hover(webelement,(1,))
                    pyautogui.PAUSE = 1
                    pyautogui.keyDown('enter')
                    #pyautogui.press('enter')
                    pyautogui.PAUSE = 1
                    pyautogui.keyUp('enter')

                except:
                    local_blk.log.debug('Going to perform click operation')
                    webelement.click()
                    #self.click(webelement)
                    local_blk.log.info('Click operation performed using selenium click')
                status = True
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            local_blk.log.error(EXCEPTION_OCCURED)
            local_blk.log.error(e)
        return status
