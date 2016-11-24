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

import Exceptions
import logger
import webconstants
import time
from selenium import webdriver
from pyrobot import Robot,Keys
import browser_Keywords


driver = browser_Keywords.driver_obj
##driver = None
class ButtonLinkKeyword():
##    def __init__(self):
##        driver = webdriver.Ie(executable_path = 'D:\Drivers\iedriverserver64')


    def click(self,webelement,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        #click keyword implementation
        try:
            if webelement != None:
                logger.log('Check for the element enable')
                if webelement.is_enabled():
                    if isinstance(driver,webdriver.Ie):
                        logger.log('Internet Explorer Instance')
                        try:
                            clickinfo = driver.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                            time.sleep(5)
                            logger.log('ButtonLinkKeyword info',clickinfo)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                        except Exception as e:
                            logger.log('Javascript error occured, Trying to click using Action class')
                            webdriver.ActionChains(driver).move_to_element(webelement).click(webelement).perform()
                            logger.log('ButtonLinkKeyword info: Clicked using Actions class')
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                    else:
                        try:
                            webelement.click()
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                        except Exception as e:
                            clickinfo = driver.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                            logger.log('ButtonLinkKeyword info',clickinfo)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    logger.log('Element is disabled, hence cannot perform Click operation')
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def verify_button_name(self,webelement,inputs,output,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        #verify_button_name keyword implementation
        try:
            if webelement != None:
                #fetch the text (button name) using selenium webelement.text
                buttonname = webelement.text
                if buttonname == None or len(buttonname) == 0:
                    logger.log('Getting value attribute')
                    #if text is empty search for the value attribute
                    buttonname = webelement.get_attribute(webconstants.VALUE)
                if buttonname == None or len(buttonname) == 0:
                    logger.log('Getting name attribute')
                    #if value is empty search for the name attribute
                    buttonname = webelement.get_attribute(webconstants.NAME)
                #Remove the leading and trailing spaces
                input = inputs[0]
                input = input.strip()
                #Check for the input
                if input != None and len(input) != 0:
                    logger.log('Input is valid, Continue..')
                    if buttonname == input:
                        logger.log('Button name matched with the input, set the status to Pass')
                        status = webconstants.TEST_RESULT_PASS
                        methodoutput = webconstants.TEST_RESULT_TRUE
                    else:
                        logger.log('Button name does not matched with the input, set the status to Fail')
                        status = webconstants.TEST_RESULT_FAIL
                        methodoutput = webconstants.TEST_RESULT_FAIL
                else:
                    logger.log('Invalid input')
            else:
                logger.log('Please pass the valid web element')
            logger.log('Keyword result: ' + status)
        except Exception as e:
            Exceptions.error(e)
        #return status and methodoutput
        logger.log('return status and methodoutput')
        return status,methodoutput

    def get_link_text(self,webelement,input,output,*args):
        #get_link_text keyword implementation
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        linktext = ''
        try:
            if webelement != None:
                logger.log('Getting href attribute')
                text = webelement.get_attribute(webconstants.HREF)
                if text != None:
                    linktext = webelement.text
                    logger.log('Link text: ' +linktext)

                    if linktext == None:
                        linktext = ''
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    logger.log('Object is not a link')
            else:
                logger.log('Element not found')
            print 'Keyword result: ',status

        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput,linktext

    def verify_link_text(self,webelement,inputs,output,*args):
        #verify_link_text keyword implementation
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        try:
            if webelement != None:
                text = webelement.text
                input = inputs[0]
                input = input.strip()
                if input != None and len(input) != 0:
                    logger.log('Input is valid, Continue..')
                    logger.log('Getting href attribute')
                    text = webelement.get_attribute(webconstants.HREF)
                    if text != None:
                        linktext = webelement.text
                        logger.log('Link text: ' +linktext)
                        if linktext == input:
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                        else:
                            logger.log('Link text does not matched with the input, set the status to Fail')
                            status = webconstants.TEST_RESULT_FAIL
                            methodoutput = webconstants.TEST_RESULT_FAIL
                    else:
                        logger.log('Please provide the input')
            else:
                logger.log('Element not found')
            print 'Keyword result: ',status
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    #Below keyword specifically written for to support mnt CBU
    def press(self,webelement,input,output,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
       #press keyword implementation
        try:
            if webelement != None:
                logger.log('Check for the element enable')
                if webelement.is_enabled():
                    webelement.click()
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    logger.log('Element is disabled, hence cannot perform press operation')
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def double_click(self,webelement,input,output,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
       #double_click keyword implementation
        try:
            if webelement != None:
                logger.log('Check for the element enable')
                if webelement.is_enabled():
                    webdriver.ActionChains(driver).move_to_element(webelement).double_click(webelement).perform()
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    logger.log('Element is disabled, hence cannot perform double click operation')
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def right_click(self,webelement,input,output,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
       #right_click keyword implementation
        try:
            if webelement != None:
                logger.log('Check for the element enable')
                if webelement.is_enabled():
                    webdriver.ActionChains(driver).move_to_element(webelement).context_click(webelement).perform()
                    status = webconstants.TEST_RESULT_PASS
                    methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    logger.log('Element is disabled, hence cannot perform right_click operation')
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def upload_file(self,webelement,inputs,output,*args):
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        #upload_file keyword implementation
        try:
            driver = browser_Keywords.driver_obj
            filepath = inputs[0]
            filename = inputs[1]
            inputfile = filepath + '\\' + filename
            if webelement != None:
                logger.log('Check for the element enable')
                if webelement.is_enabled():
                    if isinstance(driver,webdriver.Firefox):
                        logger.log('Mozilla Firefox Instance')
                        clickinfo = driver.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                        logger.log('upload_file click info',clickinfo)
                        filestatus = self.__upload_operation(inputfile)
                        status = webconstants.TEST_RESULT_PASS
                        methodoutput = webconstants.TEST_RESULT_TRUE
                    else:
                        if  self.__click_for_file_upload(driver,webelement):
                            filestatus =self.__upload_operation(inputfile)
                            status = webconstants.TEST_RESULT_PASS
                            methodoutput = webconstants.TEST_RESULT_TRUE
                else:
                    logger.log('Element is disabled, hence cannot perform upload_file operation')
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def __upload_operation(self,inputfile):
        status = False
        try:
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
            status = True
        except Exception as e:
            Exceptions.error(e)
        return status

    def __set_clipboard_data(self,inputfile):
        status = False
        try:
            robot = Robot()
            robot.add_to_clipboard(str(inputfile))
            status = True
        except Exception as e:
            Exceptions.error(e)
        return status
    def __click_for_file_upload(self,driver,webelement):
        status = False
        try:
            if isinstance(driver,webdriver.Ie):
                clickinfo = driver.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                logger.log('Upload File click info: ' + clickinfo)
                status = True
            else:
                webelement.click()
                status = True
        except Exception as e:
            Exceptions.error(e)
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
##    logger.log('ButtonLinkKeyword object created')
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







