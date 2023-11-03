#-------------------------------------------------------------------------------
# Name:        browser_Keywords_MW.py
# Purpose:
#
# Author:      rakesh.v
#
# Created:     08-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from selenium import webdriver
from collections import OrderedDict
import domconstants_MW
import logger
import webconstants_MW
driver_obj = None
parent_handle=None
webdriver_list = []
import threading
import time
import os
import subprocess
from constants import *
import logging
import platform
drivermap = []
log = logging.getLogger('browser_Keywords_MW.py')
import utils_web_MW
import psutil
if SYSTEM_OS!='Darwin':
    import win32gui
    import win32api
import readconfig
import device_keywords_MW
import core_utils
import controller
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
        self.all_handles=[]
        self.recent_handles=[]
        # parent_handle=None


    def start_server(self):
        try:
            err_msg = None
            curdir = os.environ["AVO_ASSURE_HOME"]
            path_node_modules = curdir + '/node_modules'
            if not os.path.exists(path_node_modules):
                err_msg= 'node_modules Directory not Found in Avo Assure Client'
                return False
            if (SYSTEM_OS != 'Darwin'):
                path = curdir + '/node_modules/appium/build/lib/main.js'
                nodePath = os.environ["AVO_ASSURE_HOME"] + "/Lib/Drivers/node.exe"
                proc = subprocess.Popen([nodePath, path], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True, creationflags=subprocess.CREATE_NO_WINDOW)
                controller.process_ids.append(proc.pid)
                start = time.time()
                timeout = 120 #tentative; as it depends on the system performance.
                server_flag = False
                while(True):
                    if int(time.time()-start) >= timeout:
                        err_msg = 'Timeout starting the Appium server'
                        logger.print_on_console(err_msg)
                        log.error(err_msg)
                        break
                    processes = psutil.net_connections()
                    for line in processes:
                        p = line.laddr
                        if p[1] == 4723:
                            time.sleep(2)
                            server_flag = True
                            break
                    if server_flag: break
                    time.sleep(5)
                if err_msg is None:
                    logger.print_on_console('Browser session started')
                    return True
            else:
                path = curdir + '/node_modules/appium/build/lib/main.js'
                nodePath = curdir + '/node_modules/node_appium'
                proc = subprocess.Popen([nodePath, path], shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
                controller.process_ids.append(proc.pid)
                time.sleep(25) # psutil.net_connections() doesn't work on Mac, insearch of alternatives
                logger.print_on_console('Browser session started')
                return True
        except Exception as e:
            err_msg = 'Error while starting server'
            log.error(e,exc_info=True)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return False

    def openBrowser(self, webelement, inputs, *args):
        ##self.start_server()
        global driver_obj, driver, webdriver_list, parent_handle, device_id, input_list
        status = webconstants_MW.TEST_RESULT_FAIL
        result = webconstants_MW.TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        try:
            if SYSTEM_OS== 'Darwin':
                # Logic to make sure that logic of usage of existing driver is not applicable to execution
                if driver_obj is not None:
                    result = webconstants_MW.TEST_RESULT_TRUE
                    status = webconstants_MW.TEST_RESULT_PASS
                    return status, result, output, err_msg
                input_list = inputs
                device_id = input_list[0]
                if device_id != '':
                    self.start_server()
                    obj = Singleton_DriverUtil()
                    time.sleep(5)
                    desired_caps = {}
                    desired_caps['platformName'] = 'iOS'
                    desired_caps['platformVersion'] = input_list[1]
                    desired_caps['deviceName'] = input_list[0]
                    desired_caps['udid'] = input_list[2]
                    desired_caps['autoWebview'] = True
                    desired_caps['startIWDP'] = True
                    desired_caps['automationName'] = 'XCUITest'
                    desired_caps['browserName'] = 'Safari'
                    desired_caps['newCommandTimeout'] = '36000'
                    driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
                    log.info('FILE: browser_keywords_MW.py , DEF: openSafariBrowser() , MSG:  Navigating to blank page')
                    driver.get(domconstants_MW.BLANK_PAGE)
                    driver_obj = driver
                    log.info(
                        'FILE: browser_keywords_MW.py , DEF: openSafariBrowser() , MSG:  Safari browser opened successfully')
                    result = webconstants_MW.TEST_RESULT_TRUE
                    status = webconstants_MW.TEST_RESULT_PASS
            else:
                res_cb=self.check_browser_active(inputs)
                if driver_obj is not None and res_cb==webconstants_MW.TEST_RESULT_TRUE:
                    result = webconstants_MW.TEST_RESULT_TRUE
                    status = webconstants_MW.TEST_RESULT_PASS
                    return status, result, output, err_msg
                device_object = device_keywords_MW.Device_Keywords()
                input_list = inputs
                if len(input_list) >= 2:
                    device_id = input_list[0]
                    if device_id == 'wifi':
                        device_id=device_object.wifi_connect()
                    result_cdd=self.check_device_details(device_id,input_list[1])
                    if device_id != '' and result_cdd==webconstants_MW.TEST_RESULT_TRUE:
                        self.start_server()
                        obj = Singleton_DriverUtil()
                        # Logic to make sure that logic of usage of existing driver is not applicable to execution
                        time.sleep(5)
                        desired_caps = {}
                        desired_caps['platformName'] = 'Android'
                        desired_caps['platformVersion'] =input_list[1]
                        desired_caps['deviceName'] = device_id
                        desired_caps['udid'] = device_id
                        #desired_caps['skipUnlock'] = True
                        desired_caps['automationName'] = 'UiAutomator2'
                        desired_caps['browserName'] = 'Chrome'
                        desired_caps['clearSystemFiles']=True
                        desired_caps['noReset'] = True
                        desired_caps['fullReset'] = False
                        desired_caps['newCommandTimeout'] = 0
                        desired_caps['eventTimings'] = True
                        desired_caps['enablePerformanceLogging'] = True
                        desired_caps['chromedriverExecutable'] =  os.environ["AVO_ASSURE_HOME"] + "/Lib/Drivers/chromedriver_mobile.exe"
                        driver= webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
                        log.info('FILE: browser_keywords_MW.py , DEF: openChromeBrowser() , MSG:  Navigating to blank page')
                        driver.get(domconstants_MW.BLANK_PAGE)
                        driver_obj = driver
                        log.info('FILE: browser_keywords_MW.py , DEF: openChromeBrowser() , MSG:  Chrome browser opened successfully')
                        parent_handle =  None
                        try:
                            parent_handle = driver_obj.current_window_handle
                        except Exception as nosuchWindowExc:
                            log.error(nosuchWindowExc)
                            log.warn("A window or tab was closed manually from the browser!")
                        if parent_handle is not None:
                            self.update_recent_handle(parent_handle)
                            self.all_handles.append(parent_handle)
                        elif len(self.all_handles) > 0:
                            driver_handles = driver_obj.window_handles
                            switch_to_handle = None
                            for handle in self.all_handles:
                                if handle in driver_handles:
                                    switch_to_handle = handle
                                    break
                            if switch_to_handle is not None:
                                log.info("driver will now switch to the first window/tab")
                                driver_obj.switch_to.window(switch_to_handle)
                            else:
                                log.info("driver will now switch to any available window/tab")
                                driver_obj.switch_to.window(driver_handles[0])
                        result = webconstants_MW.TEST_RESULT_TRUE
                        status = webconstants_MW.TEST_RESULT_PASS
                else:
                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
        except Exception as e:
            err_msg = 'error occured while opening browser'
            if SYSTEM_OS == 'Darwin':
                curdir = os.environ["AVO_ASSURE_HOME"]
                path_node_modules = curdir + '/node_modules'
                if not os.path.exists(path_node_modules):
                    logger.print_on_console(
                        "node_modules Directory not Found in Avo Assure Client")
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status, result, output, err_msg

    def openBrowser_BrowserStack(self,url,inputs,*args):
        global driver_obj, driver
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        try:
            desired_cap = inputs
            driver = webdriver.Remote(url, desired_cap)
            driver_obj = driver
            status = TEST_RESULT_PASS            
            result = TEST_RESULT_TRUE
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            log.error(e)

        return status,result,output,err_msg    

    def closeBrowser_BrowserStack(self, input, *args):
        global driver_obj, driver
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        try:
            driver_obj.quit()
            driver_obj =None
            status = TEST_RESULT_PASS
            result = TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
        return status,result,output,err_msg

    def check_browser_active(self, inputs):
        res=webconstants_MW.TEST_RESULT_FALSE
        dv_name=inputs[0]
        try:
            adb=os.environ['ANDROID_HOME']+"\\platform-tools\\adb.exe"
            if dv_name is not None:
                cmd = adb + ' -s '+ dv_name+' shell pidof com.android.chrome'
            s = subprocess.check_output(cmd.split(),universal_newlines=True, creationflags=subprocess.CREATE_NO_WINDOW).strip()
            if s!="":
                res=webconstants_MW.TEST_RESULT_TRUE
        except subprocess.CalledProcessError as esc:
            log.error(esc)
        except Exception as e:
            logger.print_on_console("Not able to check browser active")
            log.error(e,exc_info=True)
        return res

    def check_device_details(self,dv_name,platform_ver):
        res_1=webconstants_MW.TEST_RESULT_TRUE
        res_2=webconstants_MW.TEST_RESULT_FALSE
        res=webconstants_MW.TEST_RESULT_FALSE
        try:
            device_keywords_object = device_keywords_MW.Device_Keywords()
            temp_res=device_keywords_object.get_device_list('')
            if dv_name not in temp_res[2]:
                logger.print_on_console("Please provide valid Device ID")
                res_1=webconstants_MW.TEST_RESULT_FALSE
            if platform_ver!='' and res_1==webconstants_MW.TEST_RESULT_TRUE:
                adb=os.environ['ANDROID_HOME']+"\\platform-tools\\adb.exe"
                if dv_name is not None:
                    cmd = adb + ' -s '+ dv_name+' shell getprop ro.build.version.release '
                s = subprocess.check_output(cmd.split(),universal_newlines=True, creationflags=subprocess.CREATE_NO_WINDOW).strip()
                if s==platform_ver:
                    res_2=webconstants_MW.TEST_RESULT_TRUE
                else:
                    logger.print_on_console("Please provide valid Platform version")
            if res_1==webconstants_MW.TEST_RESULT_TRUE and res_2==webconstants_MW.TEST_RESULT_TRUE:
                res=webconstants_MW.TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console("Not able to check device details")
            log.error(e,exc_info=True)
        return res

    def openNewTab(self ,*args):
        global driver_obj
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            driver_obj.execute_script("window.open('');")
            handles = driver_obj.window_handles
            driver_obj.switch_to.window(handles[-1])
            h=driver_obj.current_window_handle
            self.all_handles.append(h)
            self.recent_handles.append(h)
            status=webconstants_MW.TEST_RESULT_PASS
            result=webconstants_MW.TEST_RESULT_TRUE
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            log.error(e)
        return status,result,output,err_msg

    def refresh(self,*args):
        global driver_obj
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(driver_obj != None):
                driver_obj.refresh()
                logger.print_on_console('Browser refreshed')
                log.info('Browser refreshed')
                status=webconstants_MW.TEST_RESULT_PASS
                result=webconstants_MW.TEST_RESULT_TRUE
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            log.error(e)
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def validate_current_window_handle(self):
    	## Issue #190 Driver control won't switch back to parent window
        if driver_obj is not None:
            try:
                winHandles=driver_obj.window_handles
                curHandle=driver_obj.current_window_handle
            except Exception as e:
                log.error(e)
                rev_recent_handles=list(self.recent_handles)
                rev_recent_handles.reverse()
                for h in rev_recent_handles:
                    try:
                        driver_obj.switch_to.window(h)
                    except Exception as e:
                        log.error(e)

    def update_recent_handle(self,h): 
        if len(self.recent_handles)==0 or self.recent_handles[-1]!=h:
            self.recent_handles.append(h)

    def navigateToURL(self ,webelement, url , *args):
        global driver_obj
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            url = url[0]
            if not (url is None and url.strip() is ''):
                url = url.strip()
                if url[0:7].lower()!='http://' and url[0:8].lower()!='https://' and url[0:5].lower()!='file:':
                    url='http://'+url
                driver_obj.get(url)
                logger.print_on_console('Navigated to URL')
                log.info('Navigated to URL')
                status=webconstants_MW.TEST_RESULT_PASS
                result=webconstants_MW.TEST_RESULT_TRUE
            else:
                logger.print_on_console(webconstants_MW.INVALID_INPUT)
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
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
            err_msg='error occured in type function'
            logger.print_on_console(err_msg)
            log.error(e)
        return



    def navigate_with_authenticate(self ,webelement, url , *args):
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
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
                    status=webconstants_MW.TEST_RESULT_PASS
                    result=webconstants_MW.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Authentication popup not found')
                    log.error('Authentication popup not found')
                    err_msg = 'Authentication popup not found'
            else:
                logger.print_on_console(webconstants_MW.INVALID_INPUT)
                log.error(webconstants_MW.INVALID_INPUT)
                err_msg = webconstants_MW.INVALID_INPUT
        except Exception as e:
            err_msg='error occured in navigate with authenticate'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,result,output,err_msg


    def getPageTitle(self,*args):
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        page_title = None
        err_msg=None

        try:
            global driver_obj
            if (driver_obj!= None):
                page_title= driver_obj.title
                if (page_title is ''):
                    page_title= driver_obj.current_url
                page_title.strip()
                logger.print_on_console('Page title is ',page_title)
                log.info('Page title is ' + str(page_title))
                status=webconstants_MW.TEST_RESULT_PASS
                result=webconstants_MW.TEST_RESULT_TRUE
            else:
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg='error occured in get page title'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,result,page_title,err_msg

    def verify_page_title(self,webelement,input_val,*args):
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            global driver_obj
            if (driver_obj!= None):
                page_title= driver_obj.title
                if (page_title is ''):
                    page_title= driver_obj.current_url
                page_title.strip()
                coreutilsobj=core_utils.CoreUtils()
                userinput=coreutilsobj.get_UTF_8(input_val[0])
                if(page_title == userinput):
                    logger.print_on_console('Page title matched')
                    log.info('Page title matched')
                    status=webconstants_MW.TEST_RESULT_PASS
                    result=webconstants_MW.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Page title mismatched')
                    logger.print_on_console(EXPECTED,userinput)
                    log.info(EXPECTED)
                    log.info(userinput)
                    logger.print_on_console(ACTUAL,page_title)
                    log.info(ACTUAL)
                    log.info(page_title)
            else:
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg='error occured in verify page title'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,result,output,err_msg

    def navigate_back(self, webelement, url, *args):
        """performs a navigate_back back operation"""
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            driver_obj.execute_script("window.history.go(-1)")
            status=webconstants_MW.TEST_RESULT_PASS
            result=webconstants_MW.TEST_RESULT_TRUE
        except Exception as e:
            err_msg='error  occured in navigate back'
            logger.print_on_console(err_msg)
            log.error(e)
        return status,result,output,err_msg


    def getCurrentURL(self,*args):
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        url = None
        err_msg=None
        try:
            global driver_obj
            if (driver_obj!= None):
                url= driver_obj.current_url
                url.strip()
                logger.print_on_console('URL: ',url)
                log.info('URL: '+ str(url))
                status=webconstants_MW.TEST_RESULT_PASS
                result=webconstants_MW.TEST_RESULT_TRUE
            else:
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg='error occured in get current url'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,result,url,err_msg

    def verifyCurrentURL(self ,webelement, input_url,*args):
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            global driver_obj
            if not (input_url is None and input_url is ''):
                url= driver_obj.current_url
                url.strip()
                input_url=input_url[0].strip()
                if (url == input_url):
                    logger.print_on_console('Current url matched')
                    log.info('Current url matched')
                    status=webconstants_MW.TEST_RESULT_PASS
                    result=webconstants_MW.TEST_RESULT_TRUE
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
                err_msg = webconstants_MW.INVALID_INPUT
        except Exception as e:
            err_msg='error occured in verify current url'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,result,output,err_msg

    def closeBrowser(self,*args):
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
##        if(len(webdriver_list) > 0):
##
##                driver_instance = len(webdriver_list)-1
##                winHandles = webdriver_list[driver_instance].window_handles
##                current_handle = webdriver_list[driver_instance].current_window_handle
##                count = 0
##                for x in winHandles:
##                    count+=1
##                    if(current_handle == x):
##                        break
##
##                count = count - 2
##                webdriver_list[driver_instance].close()
##                logger.print_on_console('browser closed')
##                log.info('browser closed')
##                if(len(winHandles) > 1):
##                    webdriver_list[driver_instance].switch_to.window(winHandles[count])
##                if(len(winHandles) == 1):
##                    webdriver_list.pop(len(webdriver_list)-1)
##                    print 'Kill driver logic'
            global driver_obj
            if SYSTEM_OS== 'Darwin':
                driver_obj.quit()
                driver_obj = None
            else:
                android_home = os.environ['ANDROID_HOME']
                if android_home is not None:
                    adb=os.environ['ANDROID_HOME']+"\\platform-tools\\adb.exe"
                    cmd = adb + ' -s '+ device_id +' shell pm clear com.android.chrome '
                    s = subprocess.check_output(cmd.split(),universal_newlines=True, creationflags=subprocess.CREATE_NO_WINDOW).strip()
                    if (driver_obj) and s =='Success':
                        driver_obj = None
                        status=webconstants_MW.TEST_RESULT_PASS
                        result=webconstants_MW.TEST_RESULT_TRUE
                else:
                    err_msg='NO_ANDROID_HOME'

        except Exception as e:
            err_msg='exception in closing the browser'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,result,output,err_msg




    def closeSubWindows(self,*args):
            # closeSubWindows
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if (len(args) > 1):
                inp = args[1]
                inp = str(inp[0])
            if len(self.all_handles) > 1:
                if(inp == 'ALL'):
                    while self.all_handles[-1]!=parent_handle:
                        try:
                            driver_obj.switch_to.window(self.all_handles[-1])
                            driver_obj.close()
                            self.all_handles=self.all_handles[0:-1]
                            logger.print_on_console('Sub window closed')
                            log.info('Sub window closed')
                        except Exception as e:
                            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                else:
                    try:
                        driver_obj.switch_to.window(self.all_handles[-1])
                        driver_obj.close()
                        self.all_handles=self.all_handles[0:-1]
                        logger.print_on_console('Sub window closed')
                        log.info('Sub windows closed')
                    except Exception as e:
                        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']

                if(len(self.all_handles) >= 1):
                    driver_obj.switch_to.window(parent_handle)
                    self.update_recent_handle(parent_handle)
                    status=webconstants_MW.TEST_RESULT_PASS
                    result=webconstants_MW.TEST_RESULT_TRUE
            else:
                err_msg = 'No sub windows to close'

        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            driver_obj.switch_to.window(parent_handle)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,result,output,err_msg
        

    def clear_cache(self,*args):
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            global driver_obj
            if driver_obj != None and isinstance(driver_obj,webdriver.Ie):
                #get all the cookies
                cookies=driver_obj.get_cookies()
                if len(cookies)>0:
                    cookies_list=[]
                    for x in cookies:
                        cookies_list.append(x['name'])
                    logger.print_on_console('Cookies are ',str(cookies_list))
                    log.info('Cookies are: ')
                    log.info(cookies_list)
                    #delete_all_cookies()
                    driver_obj.delete_all_cookies()
                    status=webconstants_MW.TEST_RESULT_PASS
                    result=webconstants_MW.TEST_RESULT_TRUE

                else:
                    err_msg = 'No Cookies found'
            else:
                err_msg = "This feature is available only for Internet Explorer."
        except Exception as e:
            err_msg='exception in clear cache'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,result,output,err_msg

    def switch_to_window(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            input=input[0]
            try:
                to_window=int(input)
            except Exception as e:
                to_window = -1
            if not(input is None or input is '' or to_window <0):
                logger.print_on_console(INPUT_IS+input)
                log.info('Switching to the window ')
                log.info(to_window)
                self.update_window_handles()
                window_handles=self.__get_window_handles()
                ## Issue #190 Driver control won't switch back to parent window
                if to_window>len(window_handles):
                    err_msg='Window '+input+' not found'
                else:
                    log.info('The available window handles are ')
                    log.info(window_handles)
                    cur_handle=driver_obj.current_window_handle
                    from_window=-1
                    if cur_handle in window_handles:
                        from_window=window_handles.index(cur_handle)+1
                        log.info('Switching from the window')
                        log.info(from_window)
                    if from_window>-1:
                        driver_obj.switch_to.window(window_handles[to_window-1])
                        self.update_recent_handle(window_handles[to_window-1])
                        log.info('Switched to window handle '+str(driver_obj.current_window_handle))
                        logger.print_on_console('Control switched from window ' + str(from_window)
    							+ " to window " + str(to_window))
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg='Current window handle not found'
            elif (input is None or input is ''):
                window_handles=self.__get_window_handles()
                log.info('Current window handles are ')
                log.info(window_handles)
                log.debug(len(window_handles))
                if len(window_handles)>0:
                    total_handles=len(window_handles)
                    driver_obj.switch_to.window(window_handles[total_handles-1])
                    ## Issue #190 Driver control won't switch back to parent window
                    self.update_recent_handle(window_handles[total_handles-1])
                    logger.print_on_console('Control switched to latest window')
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
            else:
                err_msg=INVALID_INPUT
        except Exception as e:
            log.error(e)
            log.info('Inside Exception block')
            try:
                if isinstance(e,NoSuchWindowException):
                    window_handles=self.__get_window_handles()
                    log.info('Current window handles are ')
                    log.info(window_handles)
                    log.debug(len(window_handles))
                    if len(window_handles)>0:
                        total_handles=len(window_handles)
                        driver_obj.switch_to.window(window_handles[total_handles-1])
                        ## Issue #190 Driver control won't switch back to parent window
                        self.update_recent_handle(window_handles[total_handles-1])
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg='No handles found'
            except Exception as e:
                err_msg='exception in switch to window'
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,methodoutput,output,err_msg

    def __get_window_handles(self):
        window_handles=driver_obj.window_handles
        logger.print_on_console('Window handles size '+str(len(window_handles)))
        return window_handles

    def update_window_handles(self):
    	## Issue #190 Driver control won't switch back to parent window
        if driver_obj is not None:
            try:
                winHandles=list(driver_obj.window_handles)
                new_handles=[]
                invalid_handles=[]
                self.all_handles=list(OrderedDict.fromkeys(self.all_handles))
                for h in self.all_handles:
                    if h in winHandles:
                        new_handles.append(h)
                        winHandles.remove(h)
                    else:
                        invalid_handles.append(h)
                del self.all_handles[:]
                if len(winHandles)>0:
                    self.all_handles=new_handles+winHandles
                else:
                    self.all_handles=new_handles
                #parent_handle=all_handles[0]
                self.recent_handles=[a for a in self.recent_handles if a not in invalid_handles]
                if len(self.recent_handles)>0:
                    if driver_obj.current_window_handle != self.recent_handles[-1]:
                        driver_obj.switch_to.window(self.recent_handles[-1])
            except Exception as e:
                log.error(e)

class Singleton_DriverUtil():
##    def check_available_driver(self,browser_num):
##        global driver_obj
##        import os
##        try:
##            import browserops_MW
##            log.debug("browserops_MW.driver ",browserops_MW.driver)
####            scrapedriver = browserops_MW.driver
##            toCheck = browserops_MW.driver.window_handles
##            print toCheck
##            if(len(toCheck)== 0):
##                import win32com.client
##                my_processes = ['IEDriverServer.exe','IEDriverServer64.exe']
##                wmi=win32com.client.GetObject('winmgmts:')
##                for p in wmi.InstancesOf('win32_process'):
##                    if p.Name in my_processes:
##                        os.system("TASKKILL /F /IM " + p.Name)
##                if browserops_MW.driver.name == 'internet explorer':
##                    driver_instance = self.driver('3')
##                    return driver_instance
##            else:
##                return browserops_MW.driver
##
##
##        except Exception as e:
##            import win32com.client
##            my_processes = ['chromedriver.exe','phantomjs.exe','geckodriver.exe']
##            wmi=win32com.client.GetObject('winmgmts:')
##            for p in wmi.InstancesOf('win32_process'):
##                if p.Name in my_processes:
##                    os.system("TASKKILL /F /IM " + p.Name)
##            if browserops_MW.driver == None:
##                return self.driver(browser_num)
##            else:
##                if browserops_MW.driver.name == 'chrome':
##                    driver_instance =self.driver('1')
##                    return driver_instance
##                elif browserops_MW.driver.name == 'firefox':
##                    driver_instance =self.driver('2')
##                    return driver_instance

    def chech_if_driver_exists_in_map(self,browserType):
        d = None
##        drivermap.reverse()
        if browserType == '1':
            if len(drivermap) > 0:
                for i in drivermap:
                    if isinstance(i,webdriver.Chrome ):
                        try:
                            if len (i.window_handles) > 0:
                                d = i
                        except Exception as e:
                            d = 'stale'
                            break

        elif browserType == '2':
            if len(drivermap) > 0:
                for i in drivermap:
                    if isinstance(i,webdriver.Firefox ):
                        try:
                            if len (i.window_handles) > 0:
                                d = i
                        except Exception as e:
                            d = 'stale'
                            break
        elif browserType == '3':
            if len(drivermap) > 0:
                for i in drivermap:
                    if isinstance(i,webdriver.Ie ):
                        try:
                            if len (i.window_handles) == 0:
                                d = 'stale'
                                break
                            else:
                                d = i
                        except Exception as e:
                            d = 'stale'
                            break
##        drivermap.reverse()
        return d

    def getBrowser(self,browser_num):
        driver=None
        log.debug('BROWSER NUM: ')
        log.debug(browser_num)
        logger.print_on_console( 'BROWSER NUM: ',browser_num)
        configvalues = readconfig.configvalues

        if (browser_num == '1'):
            chrome_path = configvalues['chrome_path']
            if ((str(chrome_path).lower()) == 'default'):
                chrome_path = webconstants_MW.CHROME_DRIVER_PATH
            choptions = webdriver.ChromeOptions()
            choptions.add_argument('start-maximized')
            choptions.add_argument('--disable-extensions')
            driver = webdriver.Chrome(chrome_options=choptions, executable_path=chrome_path)
            controller.process_ids.append(driver.service.process.pid)
            drivermap.append(driver)
            logger.print_on_console('Chrome browser started')
            log.info('Chrome browser started')

        elif(browser_num == '2'):
            import re
            import win32api
            import os
            import win32process
            try:
                # search all the drives to take firefox path
                def find_file(root_folder, rex):
                    found = False
                    for root,dirs,files in os.walk(root_folder):
                        for f in files:
                            result = rex.search(f)
                            if result:
                                found = True
                                firefox_path = os.path.join(root,f)
                                firefox_arr = [firefox_path,found]
                                break
                        if found:
                            break
                    return firefox_arr

                def find_file_in_all_drives(file_name):
                    #create a regular expression for the file
                    rex = re.compile(file_name)
                    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
                        found = find_file( drive, rex )
                        path=found[0]
                        flag=found[1]
                        if flag:
                            break
                    return path

                path = find_file_in_all_drives( 'firefox.exe' )
                # To fetch the version of the firefox browser
                info = win32api.GetFileVersionInfo(path, "\\")
                ms = info['ProductVersionMS']
                ls = info['ProductVersionLS']
                ver = win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls)
                version = ver[0]

                # opening firefox browser through selenium if the version 47 and less than 47
                if int(version) < 48:
                    driver = webdriver.Firefox()
                    controller.process_ids.append(driver.service.process.pid)
                    drivermap.append(driver)
                    driver.maximize_window()
                    logger.print_on_console('Firefox browser started')
                    log.info('Firefox browser started')
                else:
                    caps=webdriver.DesiredCapabilities.FIREFOX
                    caps['marionette'] = True
                    driver = webdriver.Firefox(capabilities=caps,executable_path=webconstants_MW.GECKODRIVER_PATH)
                    controller.process_ids.append(driver.service.process.pid)
                    drivermap.append(driver)
                    driver.maximize_window()
                    logger.print_on_console('geckodriver started')
                    log.info('geckodriver started')

            except Exception as e:
                log.error(e,exc_info=True)
                logger.print_on_console(e)

        elif(browser_num == '3'):
            caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
            caps['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS'] = True
            caps['ignoreProtectedModeSettings'] = True
            caps['IE_ENSURE_CLEAN_SESSION'] = True
            caps['ignoreZoomSetting'] = True
            caps['NATIVE_EVENTS'] = True
            bit_64 = configvalues['bit_64']
            if ((str(bit_64).lower()) == 'no'):
                iepath = webconstants_MW.IE_DRIVER_PATH_32
            else:
                iepath = webconstants_MW.IE_DRIVER_PATH_64
            driver = webdriver.Ie(capabilities=caps,executable_path=iepath)
            controller.process_ids.append(driver.service.process.pid)
            drivermap.append(driver)
            driver.maximize_window()
            logger.print_on_console('IE browser started')
            log.info('IE browser started')

        elif(browser_num == '4'):
            driver = webdriver.Opera()
            controller.process_ids.append(driver.service.process.pid)
            drivermap.append(driver)
            logger.print_on_console('Opera browser started')

        elif(browser_num == '5'):
            driver = webdriver.PhantomJS(executable_path=webconstants_MW.PHANTOM_DRIVER_PATH)
            controller.process_ids.append(driver.service.process.pid)
            drivermap.append(driver)
            logger.print_on_console('Phantom browser started')

        elif(browser_num == '6'):
            driver = webdriver.Safari()
            controller.process_ids.append(driver.service.process.pid)
            drivermap.append(driver)
            logger.print_on_console('Safari browser started')
            log.info('Safari browser started')
        return driver






##driver = Singleton_DriverUtil()
##driver.driver('1','D:\Browser\chromedriver.exe')
##driver.driver('2')
##obj = BrowserKeywords()
##obj.openBrowser('1','D:\Browser\chromedriver.exe')
##obj.navigateToURL('https://cvg53.ngahrhosting.com/Main/careerportal/JobAgent.cfm')
##import dropdown_listbox_MW
##obj1 = DropdownKeywords()
##obj1.selectValueByIndex('cboRadius','4')
##obj.openBrowser('2')
##obj.navigateToURL('https://cvg53.ngahrhosting.com/Main/careerportal/JobAgent.cfm')
##import dropdown_listbox_MW
##obj1 = DropdownKeywords()
##obj1.selectValueByIndex('cboRadius','4')
##obj.getPageTitle()
##obj.getCurrentURL()
##obj.verifyCurrentURL('http://10.41.31.131/users/sign_in')