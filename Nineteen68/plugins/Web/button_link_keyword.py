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


import logger
import webconstants
import time
from selenium import webdriver
import platform
if platform.system()!='Darwin':
    from pyrobot import Robot, Keys
import browser_Keywords
import logging
from constants import *
import core_utils


##driver = browser_Keywords.driver_obj
##driver = None
log = logging.getLogger('button_link_keyword.py')
text_javascript = """function stext_content(f) {     var sfirstText = '';     var stextdisplay = '';     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     return (stextdisplay); }; return stext_content(arguments[0])"""
class ButtonLinkKeyword():
##    def __init__(self):
##        driver = webdriver.Ie(executable_path = 'D:\Drivers\iedriverserver64')

    def click(self,webelement,*args):
        log.debug('Got the driver object from browser keyword class')
        log.debug(browser_Keywords.driver_obj)
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        #click keyword implementation
        try:
            if webelement != None:
                log.info('Recieved web element from the web dispatcher')
                log.debug(webelement)
                log.debug('Check for the element enable')
                if isinstance(browser_Keywords.driver_obj,webdriver.Firefox ):
                    browser_Keywords.driver_obj.execute_script('arguments[0].scrollIntoView()',webelement)
                if webelement.is_enabled():
                    log.debug(WEB_ELEMENT_ENABLED)
                    if isinstance(browser_Keywords.driver_obj,webdriver.Ie):
                        log.info('Opened browser : Internet Explorer Instance')
                        try:
                            log.debug('Going to perform click operation')
                            clickinfo = browser_Keywords.driver_obj.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                            time.sleep(5)
                            log.info('Click operation performed using javascript click')
                            log.debug('click operation info: ')
                            log.debug(clickinfo)
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                        except Exception as e:
                            log.error('Javascript error occured, Trying to click using Action class')
                            webdriver.ActionChains(browser_Keywords.driver_obj).move_to_element(webelement).click(webelement).perform()
                            log.info('click operation  info: Clicked using Actions class')
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE

                    elif platform.system() == 'Darwin':
                        try:
                            clickinfo = browser_Keywords.driver_obj.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                            log.info('Click operation performed using javascript click')
                            log.debug('click operation info: ')
                            log.debug(clickinfo)
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                        except Exception as e:
                            log.debug('Going to perform click operation')
                            time.sleep(0.5)
                            webelement.click()
                            log.info('Click operation performed using selenium click')
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                    else:
                        try:
                            log.debug('Going to perform click operation')
                            time.sleep(0.5)
                            webelement.click()
                            log.info('Click operation performed using selenium click')
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                        except Exception as e:
                            log.error('selenium click  error occured, Trying to click using Javascript')
                            clickinfo = browser_Keywords.driver_obj.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                            log.info('Click operation performed using javascript click')
                            log.debug('click operation info: ')
                            log.debug(clickinfo)
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    log.info(WEB_ELEMENT_DISABLED)
                    err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def get_button_name(self,webelement,inputs,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        #verify_button_name keyword implementation
        try:
            if webelement != None:
                log.info('Recieved web element from the web dispatcher')
                log.debug(webelement)
                #fetch the text (button name) using selenium webelement.text
                log.debug('Going to fetch the button name')
                buttonname = webelement.text
                log.info('Button name fetched from the AUT using selenium')

                if buttonname != None and len(buttonname)>0:
                    output = buttonname
                    logger.print_on_console('Button name : ' , buttonname)
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE

                if buttonname == None or len(buttonname) == 0:
                    log.debug('Button name not recieved using selenium text method, Getting value attribute')
                    #if text is empty search for the value attribute
                    buttonname = webelement.get_attribute(webconstants.VALUE)
                    log.info('Button name fetched from the AUT using value attribute')
                    log.info(buttonname)
                    logger.print_on_console('Button name : ' , buttonname)
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                    output = buttonname
                if buttonname == None or len(buttonname) == 0:
                    log.debug('Button name not recieved using selenium text method/ value attribute, Getting name attribute')
                    #if value is empty search for the name attribute
                    buttonname = webelement.get_attribute(webconstants.NAME)
                    log.info('Button name fetched from the AUT using name attribute')
                    log.info(buttonname)
                    logger.print_on_console('Button name : ' , buttonname)
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                    output = buttonname
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        return status,methodoutput,output,err_msg

    def verify_button_name(self,webelement,inputs,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        #verify_button_name keyword implementation
        try:
            if webelement != None:
                log.info('Recieved web element from the web dispatcher')
                log.debug(webelement)
                #fetch the text (button name) using selenium webelement.text
                log.debug('Going to fetch the button name')
                buttonname = webelement.text
                log.info('Button name fetched from the AUT using selenium')
                logger.print_on_console('Button name : ' , buttonname)

                if buttonname == None or len(buttonname) == 0:
                    log.debug('Button name not recieved using selenium text method, Getting value attribute')
                    #if text is empty search for the value attribute
                    buttonname = webelement.get_attribute(webconstants.VALUE)
                    log.info('Button name fetched from the AUT using value attribute')
                    log.info(buttonname)
                    logger.print_on_console('Button name : ' , buttonname)
                if buttonname == None or len(buttonname) == 0:
                    log.debug('Button name not recieved using selenium text method/ value attribute, Getting name attribute')
                    #if value is empty search for the name attribute
                    buttonname = webelement.get_attribute(webconstants.NAME)
                    log.info('Button name fetched from the AUT using name attribute')
                    log.info(buttonname)
                    logger.print_on_console('Button name : ' , buttonname)

                #Remove the leading and trailing spaces
                input = inputs[0]
                input = input.strip()
                logger.print_on_console('Input text : ' , input)
                #Check for the input
                if input != None and len(input) != 0:
                    log.info('Input is valid, Continue..')
                    coreutilsobj=core_utils.CoreUtils()
                    input=coreutilsobj.get_UTF_8(input)
                    if buttonname == input:
                        log.info('Button name matched with the input, set the status to Pass')
                        logger.print_on_console('Button name  matched')
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = webconstants.TEST_RESULT_PASS
                        methodoutput = webconstants.TEST_RESULT_TRUE
                    else:
                        err_msg='Button name mismatched'
                        log.info('Button name does not matched with the input, set the status to Fail')
                        logger.print_on_console(err_msg)
                        logger.print_on_console(EXPECTED,input)
                        log.info(EXPECTED)
                        log.info(input)
                        logger.print_on_console(ACTUAL,buttonname)
                        log.info(ACTUAL)
                        log.info(buttonname)

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

    def get_link_text(self,webelement,input,*args):
        #get_link_text keyword implementation
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        linktext = ''
        err_msg = None
        try:
            if webelement != None:
                log.info('Recieved web element from the web dispatcher')
                log.debug(webelement)
                log.debug('Getting href attribute')
                linktext = browser_Keywords.driver_obj.execute_script(text_javascript,webelement)
##                import ftfy
##                linktext = ftfy.fix_text(linktext)
                coreutilsobj=core_utils.CoreUtils()
                linktext=coreutilsobj.get_UTF_8(linktext)
                linktext = linktext.replace('\n','')
                linktext = linktext.strip()
                if linktext == None or linktext == '':
                    linktext = webelement.get_attribute(webconstants.HREF)
##                    log.info('Link text: ' +text)
                if linktext == None or linktext == '':
##                    log.info('Web element is a valid link and it has href attribute')
                    linktext = webelement.text
##                    log.info('Link text: ' +linktext)
                logger.print_on_console('Link text: ' )
                logger.print_on_console(linktext)
                if linktext != None and linktext !='':
##                    log.info('Web element is a valid link and it has href attribute')
##                    linktext = webelement.text
##                    if linktext == None:
##                        linktext = ''
                    log.info('Link text: ' +linktext)
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    err_msg='There is no link text for the given element'
                    logger.print_on_console(err_msg)
                    log.info(err_msg)
##            else:
##                logger.print_on_console('Element not found')
##            print 'Keyword result: ',status

        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,linktext,err_msg

    def verify_link_text(self,webelement,inputs,*args):
        #verify_link_text keyword implementation
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement != None:
                input = inputs[0]
                input = input.strip()
                coreutilsobj=core_utils.CoreUtils()
                input=coreutilsobj.get_UTF_8(input)
                if input != None and len(input) != 0:
                    log.debug('Input is valid, Continue..')
                    log.debug('Getting href attribute')
                    linktext = browser_Keywords.driver_obj.execute_script(text_javascript,webelement)
##                    import ftfy
##                    linktext = ftfy.fix_text(linktext)
                    linktext=coreutilsobj.get_UTF_8(linktext)
                    linktext = linktext.replace('\n','')
                    linktext = linktext.strip()
                    if linktext == None or linktext == '':
                        linktext = webelement.get_attribute(webconstants.HREF)
                        log.info('Link text: ' +linktext)
                    if linktext == None or linktext == '':
                        log.info('Web element is a valid link and it has href attribute')
                        linktext = webelement.text
                        log.info('Link text: ' +linktext)
                    if linktext != None and linktext !='':
                        if linktext == input:
                            err_msg='Link Text matched'
                            logger.print_on_console(err_msg)
                            log.info(err_msg)
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                        else:
                            err_msg='Link Text mismatched'
                            logger.print_on_console(err_msg)
                            log.info(err_msg)
                            logger.print_on_console(EXPECTED,input)
                            log.info(EXPECTED)
                            log.info(input)
                            logger.print_on_console(ACTUAL,linktext)
                            log.info(ACTUAL)
                            log.info(linktext)
                    else:
                        err_msg='There is no link text for the given element'
                        logger.print_on_console(err_msg)
                        log.info(err_msg)

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

    #Below keyword specifically written for to support mnt CBU
    def press(self,webelement,input,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
       #press keyword implementation
        try:
            if webelement != None:
                log.info('Recieved web element from the web dispatcher')
                log.debug(webelement)
                log.debug('Check for the element enable')
                if webelement.is_enabled():
                    log.debug(WEB_ELEMENT_ENABLED)
                    log.debug('Going to perform click operation')
                    time.sleep(0.5)
                    webelement.click()
                    log.info('press operation performed using selenium click')
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    log.info(WEB_ELEMENT_DISABLED)
                    err_msg = WEB_ELEMENT_DISABLED
                    logger.print_on_console(WEB_ELEMENT_DISABLED)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def double_click(self,webelement,input,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
       #double_click keyword implementation
        try:
            if webelement != None:
                log.info('Recieved web element from the web dispatcher')
                log.debug(webelement)
                log.debug('Check for the element enable')
                if webelement.is_enabled():
                    webdriver.ActionChains(browser_Keywords.driver_obj).move_to_element(webelement).double_click(webelement).perform()
                    log.info('double click operation performed using Action class')
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    log.info(WEB_ELEMENT_DISABLED)
                    err_msg = WEB_ELEMENT_DISABLED
                    logger.print_on_console(WEB_ELEMENT_DISABLED)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            import traceback
            traceback.print_exc()
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def right_click(self,webelement,input,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
       #right_click keyword implementation
        try:
            if webelement != None:
                log.info('Recieved web element from the web dispatcher')
                log.debug(webelement)
                log.debug('Check for the element enable')
                if webelement.is_enabled():
                    webdriver.ActionChains(browser_Keywords.driver_obj).move_to_element(webelement).context_click(webelement).perform()
                    log.info('right click operation performed using Action class')
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    log.info(WEB_ELEMENT_DISABLED)
                    err_msg = WEB_ELEMENT_DISABLED
                    logger.print_on_console(WEB_ELEMENT_DISABLED)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def upload_file(self,webelement,inputs,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        #upload_file keyword implementation
        try:
##            driver = browser_Keywords.driver_obj
            filepath = inputs[0]
            filename = inputs[1]
            inputfile = filepath + '\\' + filename
            if webelement != None:
                log.info('Recieved web element from the web dispatcher')
                log.debug(webelement)
                log.debug('Check for the element enable')
                if webelement.is_enabled():
                    if isinstance(browser_Keywords.driver_obj,webdriver.Firefox):
                        log.debug('Mozilla Firefox Instance')
                        clickinfo = browser_Keywords.driver_obj.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                        log.info('upload_file click info')
                        log.info(clickinfo)
                        filestatus = self.__upload_operation(inputfile)
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = webconstants.TEST_RESULT_PASS
                        methodoutput = webconstants.TEST_RESULT_TRUE
                    else:
                        if  self.__click_for_file_upload(browser_Keywords.driver_obj,webelement):
                            filestatus =self.__upload_operation(inputfile)
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    log.info(WEB_ELEMENT_DISABLED)
                    err_msg = WEB_ELEMENT_DISABLED
                    logger.print_on_console(WEB_ELEMENT_DISABLED)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    def __upload_operation(self,inputfile):
        status = False
        try:
            log.debug('using Robot class to perform keyboard operation')
            robot = Robot()
            time.sleep(1)
            self.__set_clipboard_data(inputfile)
            robot.sleep(1)
            robot.key_press(Keys.alt)
            robot.key_press(Keys.n)
            robot.sleep(0.5)
            robot.key_release(Keys.n)
            robot.key_release(Keys.alt)
            robot.sleep(0.5)
            robot.paste()
            robot.sleep(0.5)
            robot.key_press(Keys.enter)
            robot.sleep(0.5)
            robot.key_release(Keys.enter)
            robot.sleep(1)
            log.debug('copied clipboard data pasted to the input using robot')
            status = True
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            log.error(EXCEPTION_OCCURED)
            log.error(e)
        return status

    def __set_clipboard_data(self,inputfile):
        status = False
        try:
            robot = Robot()
            log.debug('Copying input file path to the clipboard')
            robot.add_to_clipboard(str(inputfile))
            log.debug(' input file path Copied to  clipboard')
            status = True
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            log.error(EXCEPTION_OCCURED)
            log.error(e)
        return status
    def __click_for_file_upload(self,driver,webelement):
        status = False
        try:
            if isinstance(browser_Keywords.driver_obj,webdriver.Ie):
                log.debug('Going to perform click operation')
                clickinfo = browser_Keywords.driver_obj.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                log.info('Click operation performed using javascript click')
                log.debug('click operation info: ')
                log.debug(clickinfo)
                log.info(STATUS_METHODOUTPUT_UPDATE)
                status = True
            else:
                log.debug('Going to perform click operation')
                webelement.click()
                log.info('Click operation performed using selenium click')
                status = True
        except Exception as e:
            logger.print_on_console(EXCEPTION_OCCURED,e)
            log.error(EXCEPTION_OCCURED)
            log.error(e)
        return status


##if __name__ == '__main__':
####    driver = webdriver.Chrome(executable_path = 'D:\Drivers\chromedriver')
##    driver = webdriver.Ie(executable_path = 'D:\Drivers\iedriverserver64')
##    driver.get('https://converge/ManageUsers.aspx')
##    driver.get('https://www.google.co.in/?gfe_rd=cr&ei=y3ghWLqjAs-L8QfMjYGwDA&gws_rd=ssl')
##    driver.get('https://www.irctc.co.in/eticketing/loginHome.jsf')
##
##    print 'Browser opened and navigaed to url'
##
####    element = driver.find_element_by_id('ctl00_MainContent_btnSearch')
##    element = driver.find_element_by_id('loginbutton')
##
##    print 'element obtained'
##
##
####    element = driver.find_element_by_name('btnI')
##    obj = ButtonLinkKeyword()
##    logger.print_on_console('ButtonLinkKeyword object created')
##
##    obj.click(element)
##    print ' ***click exected ***\n\n'
##    time.sleep(5)
##
##    obj.verify_button_name('Login',element)
##
##    print ' ***verify_button_name exected ***\n\n'
##
##    linkelement = driver.find_element_by_xpath('//*[@id="loginFormId"]/div[1]/div[4]/div/ul/li[1]/a')
##
##    status,methodoutput,linktext = obj.get_link_text(linkelement)
##    print 'Status: ',status
##    print 'Method Result: ',methodoutput
##    print 'Link text: ',linktext
##
##    print ' ***get_link_text exected ***\n\n'
##
##    status,methodoutput = obj.verify_link_text('Forgot Password',linkelement)
##
##    print 'Status: ',status
##    print 'Method Result: ',methodoutput
##
##    print ' ***verify_link_text exected ***\n\n'
##
####    obj.double_click(element)
####    print ' ***double_click exected ***\n\n'
##
##    driver.get('http://cgi-lib.berkeley.edu/ex/fup.html')
##
##    upele = driver.find_element_by_name('upfile')
##
##    folder = 'D:\M'
##    filename = 'test.txt'
##    obj.upload_file(upele,folder,filename)
##    print ' ***upload_file exected ***\n\n'
##
##
##    clele = driver.find_element_by_xpath('/html/body/form/input[3]')
####    obj.click(clele)
##







