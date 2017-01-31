#-------------------------------------------------------------------------------
# Name:        mobile_browser_keywords.py
# Purpose:
#
# Author:      rakesh.v
#
# Created:     08-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from selenium import webdriver

import logger
import mobileconstants
driver_obj = None
parent_handle=None
webdriver_list = []

import threading
import time

from constants import *
import logging

log = logging.getLogger('mobile_browser_keywords.py')

#New Thread to navigate to given url for the keyword 'naviagteWithAut'
class TestThread(threading.Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self,url):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self.url=url
        self.start()
          # start the thread

    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        time.sleep(2)
        driver_obj.get(self.url[0])



class BrowserKeywords():
    def __init__(self):
        self.browser_num=''

    def __web_driver_exception(self,e):
        log.error(e)

        logger.print_on_console(e)
        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        return err_msg

    def openBrowser(self,webelement,browser_num,*args):
        status=mobileconstants.TEST_RESULT_FAIL
        result=mobileconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        self.browser_num=browser_num[0]
        try:
            global driver_obj
            global webdriver_list
            global parent_handle
            driver = Singleton_DriverUtil()
            driver_obj=driver.driver(browser_num)
            webdriver_list.append(driver_obj)
            parent_handle = driver_obj.current_window_handle
            logger.print_on_console('Browser opened')
            log.info('Browser opened')
            status=mobileconstants.TEST_RESULT_PASS
            result=mobileconstants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


    def openNewBrowser(self,*args):
        status=mobileconstants.TEST_RESULT_FAIL
        result=mobileconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            global driver_obj
            global webdriver_list
            driver = Singleton_DriverUtil()
            driver_obj=driver.driver(self.browser_num)
            webdriver_list.append(driver_obj)
            parent_handle = driver_obj.current_window_handle
            logger.print_on_console('Opened new browser')
            log.info('Opened new browser')
            status=mobileconstants.TEST_RESULT_PASS
            result=mobileconstants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg

    def refresh(self,*args):
        status=mobileconstants.TEST_RESULT_FAIL
        result=mobileconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(driver_obj != None):
                driver_obj.refresh()
                logger.print_on_console('Browser refreshed')
                log.info('Browser refreshed')
                status=mobileconstants.TEST_RESULT_PASS
                result=mobileconstants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


    def navigateToURL(self ,webelement, url , *args):
        status=mobileconstants.TEST_RESULT_FAIL
        result=mobileconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            url = url[0]
            if not (url is None and url is ''):
            	url.strip()
                driver_obj.get(url)
                logger.print_on_console('Navigated to URL')
                log.info('Navigated to URL')
                status=mobileconstants.TEST_RESULT_PASS
                result=mobileconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console(mobileconstants.INVALID_INPUT)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg

    def type(self,url):
        """thread worker function"""
        try:
            from sendfunction_keys import SendFunctionKeys
            obj=SendFunctionKeys()
            username=url[1].strip()
            password=url[2]
            obj.type(username)
            obj.execute_key('tab',1)
            obj.type(password)
            obj.execute_key('tab',1)
            obj.execute_key('enter',1)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return



    def navigate_with_authenticate(self ,webelement, url , *args):
        status=mobileconstants.TEST_RESULT_FAIL
        result=mobileconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if url[0] is not None and url[0] != '':
                from encryption_utility import AESCipher
                encryption_obj = AESCipher()
                input_val = encryption_obj.decrypt(url[2])
                url[2]=input_val
                t=TestThread(url)
                import win32gui

                if len(url)>3:
                    timeout=url[3]
                    time.sleep(int(timeout))
                hwndMain = win32gui.FindWindow(None, "Authentication Required")
                if hwndMain>0:
                    self.type(url)
                    status=mobileconstants.TEST_RESULT_PASS
                    result=mobileconstants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Authentication popup not found')
                    log.error('Authentication popup not found')
                    err_msg = 'Authentication popup not found'
            else:
                logger.print_on_console(mobileconstants.INVALID_INPUT)
                log.error(mobileconstants.INVALID_INPUT)
                err_msg = mobileconstants.INVALID_INPUT
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


    def getPageTitle(self,*args):
        status=mobileconstants.TEST_RESULT_FAIL
        result=mobileconstants.TEST_RESULT_FALSE
        page_title = None
        err_msg=None

        try:
            if (driver_obj!= None):
                page_title= driver_obj.title
                if (page_title is ''):
                    page_title= driver_obj.current_url
                page_title.strip()
                logger.print_on_console('Page title is ',page_title)
                log.info('Page title is ' + str(page_title))
                status=mobileconstants.TEST_RESULT_PASS
                result=mobileconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
                log.error('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,page_title,err_msg

    def verify_page_title(self,webelement,input_val,*args):
        status=mobileconstants.TEST_RESULT_FAIL
        result=mobileconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if (driver_obj!= None):
                page_title= driver_obj.title
                if (page_title is ''):
                    page_title= driver_obj.current_url
                page_title.strip()
                if(page_title == input_val[0]):
                    logger.print_on_console('Page title matched')
                    log.info('Page title matched')
                    status=mobileconstants.TEST_RESULT_PASS
                    result=mobileconstants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Page title mismatched')
                    logger.print_on_console(EXPECTED,input_val[0])
                    log.info(EXPECTED)
                    log.info(input_val[0])
                    logger.print_on_console(ACTUAL,page_title)
                    log.info(ACTUAL)
                    log.info(page_title)
            else:
                log.error('Driver object is null')
                logger.print_on_console('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


    def getCurrentURL(self,*args):
        status=mobileconstants.TEST_RESULT_FAIL
        result=mobileconstants.TEST_RESULT_FALSE
        url = None
        err_msg=None
        try:
            if (driver_obj!= None):
                url= driver_obj.current_url
                url.strip()
                logger.print_on_console('URL: ',url)
                log.info('URL: '+ str(url))
                status=mobileconstants.TEST_RESULT_PASS
                result=mobileconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
                log.error('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,url,err_msg

    def verifyCurrentURL(self ,webelement, input_url,*args):
        status=mobileconstants.TEST_RESULT_FAIL
        result=mobileconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if not (input_url is None and input_url is ''):
                url= driver_obj.current_url
                url.strip()
                input_url=input_url[0].strip()
                if (url == input_url):
                    logger.print_on_console('Current url matched')
                    log.info('Current url matched')
                    status=mobileconstants.TEST_RESULT_PASS
                    result=mobileconstants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Current url mismatched')
                    log.error('Current url mismatched')
                    logger.print_on_console(EXPECTED,input_url)
                    log.info(EXPECTED)
                    log.info(input_url)
                    logger.print_on_console(ACTUAL,url)
                    log.info(ACTUAL)
                    log.info(url)
            else:
                log.error(mobileconstants.INVALID_INPUT)
                logger.print_on_console(mobileconstants.INVALID_INPUT)
                err_msg = mobileconstants.INVALID_INPUT
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


    def closeBrowser(self,*args):
        status=mobileconstants.TEST_RESULT_FAIL
        result=mobileconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            if(driver_obj != None):

                driver_obj.close()

                logger.log('chrome browser closed')
                status=mobile_constants.TEST_RESULT_PASS
                result=mobile_constants.TEST_RESULT_TRUE
            else:
                logger.log('Driver is None')
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


    def maximizeBrowser(self,*args):
        status=mobileconstants.TEST_RESULT_FAIL
        result=mobileconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(driver_obj!= None):
                driver_obj.maximize_window()
                logger.print_on_console('browser maximized')
                log.info('browser maximized')
                status=mobileconstants.TEST_RESULT_PASS
                result=mobileconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
                log.error('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg

    def closeSubWindows(self,*args):
        status=mobileconstants.TEST_RESULT_FAIL
        result=mobileconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            winHandles = driver_obj.window_handles
            winHandles = driver_obj.window_handles
            for x in winHandles:
                if(not(parent_handle == x)):
                    try:
                        driver_obj.switch_to.window(parent_handle)
                        driver_obj.switch_to.window(x)
                        driver_obj.close()
                        logger.print_on_console('Sub windows closed')
                        log.info('Sub windows closed')
                    except Exception as e:
                        err_msg=self.__web_driver_exception(e)
            after_close = driver_obj.window_handles
            after_close = driver_obj.window_handles
            if(len(after_close) == 1):
                driver_obj.switch_to.window(parent_handle)
                status=mobileconstants.TEST_RESULT_PASS
                result=mobileconstants.TEST_RESULT_TRUE

        except Exception as e:
            err_msg=self.__web_driver_exception(e)
            driver_obj.switch_to.window(parent_handle)
        return status,result,output,err_msg

    def clear_cache(self,*args):
        status=mobileconstants.TEST_RESULT_FAIL
        result=mobileconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if driver_obj != None and isinstance(driver_obj,webdriver.Ie):
                #get all the cookies
                cookies=driver_obj.get_cookies()
                if len(cookies)>0:
                    cookies_list=[]
                    for x in cookies:
                        cookies_list.append(x['name'])
                    logger.print_on_console('Cookies are ',cookies_list)
                    log.info('Cookies are: ')
                    log.info(cookies_list)
                    #delete_all_cookies()
                    driver_obj.delete_all_cookies()

                else:
                    logger.print_on_console('No Cookies found')
                    log.error('No Cookies found')
                    err_msg = 'No Cookies found'
            else:
                logger.print_on_console("This feature is available only for Internet Explorer.")
                log.error("This feature is available only for Internet Explorer.")
                err_msg = "This feature is available only for Internet Explorer."
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


class Singleton_DriverUtil():
    def driver(self,inputs):
        driver=None
        global driver_obj
        self.start_server()
        if driver_obj is not None:
            driver_obj.quit()
        desired_caps = {}
       #capabilities.setCapability("noReset", true);
       #desired_caps['noReset']='true'
        try:
           desired_caps['platformName'] = 'Android'
           desired_caps['platformVersion'] = inputs[0]
           desired_caps['deviceName'] = inputs[1]
           desired_caps['browserName'] = 'Chrome'
##           desired_caps['appium-version'] = '1.4.0'
           desired_caps['newCommandTimeout'] = 36000


           driver_obj= webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        except Exception as e:
            err_msg = str(e)
            logger.print_on_console(err_msg)
            log.error(e)

        logger.log('Chrome browser started')
        return driver_obj

    def start_server(self):
        import subprocess
        log.debug(' logic to start server')
        import os
        maindir = os.getcwd()
        os.chdir('..')
        curdir= os.getcwd()
        file_path= curdir + '//Nineteen68//plugins//Mobility//node_modules//appium//build//lib//main.js'
        nodePath = maindir+'//node.exe'
        log.info(nodePath)
        proc = subprocess.Popen([nodePath, file_path], shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
        import time
        time.sleep(15)
        os.chdir(maindir)

    def stop_server(self):
        print 'logic to stop server'
        import psutil
        import os
        processes = psutil.net_connections()
        for line in processes:
            p =  line.laddr
            if p[1] == 4723:
                log.debug('Found')
                log.debug('Pid : '+str(line.pid))
                os.system("TASKKILL /F /PID " + str(line.pid))






##driver = Singleton_DriverUtil()
##driver.driver('1','D:\Browser\chromedriver.exe')
##driver.driver('2')
##obj = BrowserKeywords()
##obj.openBrowser('1','D:\Browser\chromedriver.exe')
##obj.navigateToURL('https://cvg53.ngahrhosting.com/Main/careerportal/JobAgent.cfm')
##import dropdown_listbox
##obj1 = DropdownKeywords()
##obj1.selectValueByIndex('cboRadius','4')
##obj.openBrowser('2')
##obj.navigateToURL('https://cvg53.ngahrhosting.com/Main/careerportal/JobAgent.cfm')
##import dropdown_listbox
##obj1 = DropdownKeywords()
##obj1.selectValueByIndex('cboRadius','4')
##obj.getPageTitle()
##obj.getCurrentURL()
##obj.verifyCurrentURL('http://10.41.31.131/users/sign_in')