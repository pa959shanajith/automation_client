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
import browserops_MW
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


    def start_server(self):
        try:
            err_msg = None
            curdir = os.environ["AVO_ASSURE_HOME"]
            path_node_modules = curdir + '/plugins/Mobility/MobileApp/node_modules'
            if not os.path.exists(path_node_modules):
                err_msg= 'node_modules Directory not Found in /plugins/Mobility/MobileApp'
                return False
            if (SYSTEM_OS != 'Darwin'):
                path = curdir + '/plugins/Mobility/MobileApp/node_modules/appium/build/lib/main.js'
                nodePath = os.environ["AVO_ASSURE_HOME"] + "/Lib/Drivers/node.exe"
                proc = subprocess.Popen([nodePath, path], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
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
                    logger.print_on_console('Server started')
                    return True
            else:
                path = curdir + '/plugins/Mobility/MobileApp/node_modules/appium/build/lib/main.js'
                nodePath = curdir + '/plugins/Mobility/MobileApp/node_modules/node_appium'
                proc = subprocess.Popen([nodePath, path], shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
                time.sleep(25) # psutil.net_connections() doesn't work on Mac, insearch of alternatives
                logger.print_on_console('Server started')
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
                self.start_server()
                obj = Singleton_DriverUtil()
                # Logic to make sure that logic of usage of existing driver is not applicable to execution

                input_list = inputs
                device_id = input_list[0]
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
                ##            desired_caps['appium-version'] = '1.4.0'

                desired_caps['newCommandTimeout'] = '36000'
                driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
                log.info('FILE: browserops_MW.py , DEF: openSafariBrowser() , MSG:  Navigating to blank page')
                driver.get(domconstants_MW.BLANK_PAGE)
                driver_obj = driver
                log.info(
                    'FILE: browserops_MW.py , DEF: openSafariBrowser() , MSG:  Safari browser opened successfully')
                result = webconstants_MW.TEST_RESULT_TRUE
                status = webconstants_MW.TEST_RESULT_PASS
            else:
                if driver_obj is not None:
                    result = webconstants_MW.TEST_RESULT_TRUE
                    status = webconstants_MW.TEST_RESULT_PASS
                    return status, result, output, err_msg
                browserops_object = browserops_MW.BrowserOperations()
                input_list = inputs
                device_id = input_list[0]
                if device_id == 'wifi':
                    device_id=browserops_object.wifi_connect()
                if device_id != '':
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
                    log.info('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Navigating to blank page')
                    driver.get(domconstants_MW.BLANK_PAGE)
                    driver_obj = driver
                    log.info('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Chrome browser opened successfully')
                    result = webconstants_MW.TEST_RESULT_TRUE
                    status = webconstants_MW.TEST_RESULT_PASS
        except Exception as e:
            err_msg = 'ERROR OCURRED WHILE OPENING BROWSER'
            if SYSTEM_OS == 'Darwin':
                curdir = os.environ["AVO_ASSURE_HOME"]
                path_node_modules = curdir + '/plugins/Mobility/MobileApp/node_modules'
                if not os.path.exists(path_node_modules):
                    logger.print_on_console(
                        "node_modules Directory not Found in /plugins/Mobility/MobileApp/")
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status, result, output, err_msg

    def openNewBrowser(self,*args):
        global driver_obj,webdriver_list
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            driver = Singleton_DriverUtil()
            driver_obj=driver.getBrowser(self.browser_num)
            webdriver_list.append(driver_obj)
            parent_handle = driver_obj.current_window_handle
            logger.print_on_console('Opened new browser')
            log.info('Opened new browser')
            status=webconstants_MW.TEST_RESULT_PASS
            result=webconstants_MW.TEST_RESULT_TRUE
        except Exception as e:
            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
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
            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,result,output,err_msg


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
            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
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
            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
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
            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
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
                logger.print_on_console('Driver object is null')
                log.error('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
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
                if(page_title == input_val[0]):
                    logger.print_on_console('Page title matched')
                    log.info('Page title matched')
                    status=webconstants_MW.TEST_RESULT_PASS
                    result=webconstants_MW.TEST_RESULT_TRUE
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
            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
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
                logger.print_on_console('Driver object is null')
                log.error('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
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
                log.error(webconstants_MW.INVALID_INPUT)
                logger.print_on_console(webconstants_MW.INVALID_INPUT)
                err_msg = webconstants_MW.INVALID_INPUT
        except Exception as e:
            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,result,output,err_msg

    def stop_server(self):
        try:
            if SYSTEM_OS!= 'Darwin':
                import psutil
                import os
                processes = psutil.net_connections()
                for line in processes:
                    p =  line.laddr
                    if p[1] == 4723:
                        os.system("TASKKILL /F /PID " + str(line.pid))
            else:
                import os
                os.system("killall -9 node_appium")
        except Exception as e:
            err_msg="Exception in stopping server"
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)

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
                driver_obj.close()
                driver_obj = None
                self.stop_server()
                status=webconstants_MW.TEST_RESULT_PASS
                result=webconstants_MW.TEST_RESULT_TRUE

        except Exception as e:
            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,result,output,err_msg


    def maximizeBrowser(self,*args):
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            global driver_obj
            if(driver_obj!= None):
                driver_obj.maximize_window()
                logger.print_on_console('browser maximized')
                log.info('browser maximized')
                status=webconstants_MW.TEST_RESULT_PASS
                result=webconstants_MW.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
                log.error('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,result,output,err_msg

    def closeSubWindows(self,*args):
        status=webconstants_MW.TEST_RESULT_FAIL
        result=webconstants_MW.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            global driver_obj
            winHandles = driver_obj.window_handles
            winHandles = driver_obj.window_handles
            if len(winHandles) > 1:
                for x in winHandles:
                    if(not(parent_handle == x)):
                        try:
                            driver_obj.switch_to.window(parent_handle)
                            driver_obj.switch_to.window(x)
                            driver_obj.close()
                            logger.print_on_console('Sub windows closed')
                            log.info('Sub windows closed')
                        except Exception as e:
                            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
                            log.error(e)
                after_close = driver_obj.window_handles
                after_close = driver_obj.window_handles
                if(len(after_close) == 1):
                    driver_obj.switch_to.window(parent_handle)
                    status=webconstants_MW.TEST_RESULT_PASS
                    result=webconstants_MW.TEST_RESULT_TRUE
            else:
                logger.print_on_console('No sub windows to close')
                log.info('No sub windows to close')

        except Exception as e:
            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
            log.error(e)
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
                    logger.print_on_console('Cookies are ',cookies_list)
                    log.info('Cookies are: ')
                    log.info(cookies_list)
                    #delete_all_cookies()
                    driver_obj.delete_all_cookies()
                    status=webconstants_MW.TEST_RESULT_PASS
                    result=webconstants_MW.TEST_RESULT_TRUE

                else:
                    logger.print_on_console('No Cookies found')
                    log.error('No Cookies found')
                    err_msg = 'No Cookies found'
            else:
                logger.print_on_console("This feature is available only for Internet Explorer.")
                log.error("This feature is available only for Internet Explorer.")
                err_msg = "This feature is available only for Internet Explorer."
        except Exception as e:
            err_msg='ERROR OCURRED WHILE OPENING BROWSER'
            log.error(e)
        if err_msg is not None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,result,output,err_msg


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
                    drivermap.append(driver)
                    driver.maximize_window()
                    logger.print_on_console('Firefox browser started')
                    log.info('Firefox browser started')
                else:
                    caps=webdriver.DesiredCapabilities.FIREFOX
                    caps['marionette'] = True
                    driver = webdriver.Firefox(capabilities=caps,executable_path=webconstants_MW.GECKODRIVER_PATH)
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
            drivermap.append(driver)
            driver.maximize_window()
            logger.print_on_console('IE browser started')
            log.info('IE browser started')

        elif(browser_num == '4'):
            driver = webdriver.Opera()
            drivermap.append(driver)
            logger.print_on_console('Opera browser started')

        elif(browser_num == '5'):
            driver = webdriver.PhantomJS(executable_path=webconstants_MW.PHANTOM_DRIVER_PATH)
            drivermap.append(driver)
            logger.print_on_console('Phantom browser started')

        elif(browser_num == '6'):
            driver = webdriver.Safari()
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