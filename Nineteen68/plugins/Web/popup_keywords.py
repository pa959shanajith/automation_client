#-------------------------------------------------------------------------------
# Name:        popup_keywords.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     09-11-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import Exceptions
import logger
import time
import webconstants
from selenium import webdriver

import browser_Keywords

class PopupKeywords():
    def accept_popup(self,webelement,input,output,*args):
        driver = browser_Keywords.driver_obj
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        try:
            #code to accept the pop up
            driver.switch_to.alert.accept()
            status = webconstants.TEST_RESULT_PASS
            methodoutput = webconstants.TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def dismiss_popup(self,webelement,input,output,*args):
        driver = browser_Keywords.driver_obj
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        try:
            #code to dismiss the pop up
            driver.switch_to.alert.dismiss()
            status = webconstants.TEST_RESULT_PASS
            methodoutput = webconstants.TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def get_popup_text(self,webelement,input,output,*args):
        driver = browser_Keywords.driver_obj
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        try:
            #code to get the pop up text
            text = driver.switch_to.alert.text
            logger.log('Alert text : ' + text)
            status = webconstants.TEST_RESULT_PASS
            methodoutput = webconstants.TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput,text

    def verify_popup_text(self,webelement,inputs,output,*args):
        driver = browser_Keywords.driver_obj
        status = webconstants.TEST_RESULT_FAIL
        methodoutput = webconstants.TEST_RESULT_FALSE
        try:
            #code to verify the pop up text
            text = driver.switch_to.alert.text
            logger.log('Alert text : ' + text)
            input = inputs[0]
            input = input.strip()
            if text == input:
                logger.log('Text matched')
                status = webconstants.TEST_RESULT_PASS
                methodoutput = webconstants.TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput



if __name__ == '__main__':
##    driver = webdriver.Chrome(executable_path = 'D:\Drivers\chromedriver')
    driver = webdriver.Ie(executable_path = 'D:\Drivers\iedriverserver64')
##    driver.get('https://converge/ManageUsers.aspx')
##    driver.get('https://www.google.co.in/?gfe_rd=cr&ei=y3ghWLqjAs-L8QfMjYGwDA&gws_rd=ssl')
    driver.get('https://www.irctc.co.in/eticketing/loginHome.jsf')

    obj = PopupKeywords()


    print 'Click on login button manually'
    time.sleep(5)
    obj.accept_popup()
    print '***accept_popup executed *****'

    print 'Click on login button manually'
    time.sleep(5)
    obj.dismiss_popup()
    print '***dismiss_popup executed *****'

    print 'Click on login button manually'
    time.sleep(5)
    status,methodoutput,text = obj.get_popup_text()
    print 'Status :',status
    print 'methodoutput :',methodoutput
    print 'text :',text
    print '***get_popup_text executed *****'

    status,methodoutput = obj.verify_popup_text('Enter User ID')
    print 'Status :',status
    print 'methodoutput :',methodoutput
    print '***get_popup_text executed *****'







