#-------------------------------------------------------------------------------
# Name:        browser_Keywords.py
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
import logger
import webconstants
driver_obj = None
parent_handle=None
all_handles=[]
recent_handles=[]
webdriver_list = []
import threading
import time
import os
from constants import *
import logging
drivermap = []
log = logging.getLogger('browser_Keywords.py')
import platform
if platform.system() != 'Darwin':
    import win32gui
    import win32api
    import utils_web
import psutil
import readconfig
import core_utils
import time
from sendfunction_keys import SendFunctionKeys as SF
pid_set = set()
configobj = readconfig.readConfig()
configvalues = configobj.readJson()
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
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        self.browser_num=browser_num[0]
        try:
            global driver_obj
            global webdriver_list
            global parent_handle
            global pid_set
            obj = Singleton_DriverUtil()
##            if driver_obj == None:
##                driver_obj = driver.check_available_driver(self.browser_num)
##
            #Logic to make sure that logic of usage of existing driver is not applicable to execution
            if  browser_num[-1] != EXECUTE:
                d = obj.chech_if_driver_exists_in_map(self.browser_num)
                if d == 'stale':
                    #stale logic
                    try:
                        import win32com.client
                        my_processes = ['chromedriver.exe','IEDriverServer.exe','IEDriverServer64.exe','CobraWinLDTP.exe','phantomjs.exe']
                        wmi=win32com.client.GetObject('winmgmts:')
                        for p in wmi.InstancesOf('win32_process'):
                            if p.Name in my_processes:
                                os.system("TASKKILL /F /IM " + p.Name)
                    except Exception as e:
                        log.error(e)
                    del drivermap[:]
                    driver_obj = obj.getBrowser(self.browser_num)
                elif d != None:
                    #driver exist in map, get it
                    driver_obj = d
                else:
                    #instantiate new browser and add it to the map
                    driver_obj = obj.getBrowser(self.browser_num)
            elif browser_num[-1] == EXECUTE:
                driver_obj=obj.getBrowser(self.browser_num)
                del drivermap[:]
            if platform.system()!='Darwin':
                utilobject = utils_web.Utils()
                pid = None
                if (self.browser_num == '1'):
                    #logic to the pid of chrome window
                    p = psutil.Process(driver_obj.service.process.pid)
                    pidchrome = p.children()[0]
                    pid = pidchrome.pid
                    pid_set.add(pid)
                elif(self.browser_num == '2'):
                    #logic to get the pid of the firefox window
                    try:
                        pid = driver_obj.binary.process.pid
                    except Exception as e:
                        p = psutil.Process(driver_obj.service.process.pid)
                        pidchrome = p.children()[0]
                        pid = pidchrome.pid
                        pid_set.add(pid)
                elif(self.browser_num == '3'):
                    #Logic to get the pid of the ie window
                    p = psutil.Process(driver_obj.iedriver.process.pid)
                    pidie = p.children()[0]
                    pid = pidie.pid
                    pid_set.add(pid)
                hwndg = utilobject.bring_Window_Front(pid)
            webdriver_list.append(driver_obj)
            parent_handle = driver_obj.current_window_handle
            self.update_recent_handle(parent_handle)
            all_handles.append(parent_handle)
            logger.print_on_console('Browser opened')
            log.info('Browser opened')
            status=webconstants.TEST_RESULT_PASS
            result=webconstants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


    def openNewBrowser(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            global driver_obj
            global webdriver_list
            driver = Singleton_DriverUtil()
            driver_obj=driver.getBrowser(self.browser_num)
            webdriver_list.append(driver_obj)
            parent_handle = driver_obj.current_window_handle
            self.update_recent_handle(parent_handle)
            all_handles.append(parent_handle)
            logger.print_on_console('Opened new browser')
            log.info('Opened new browser')
            status=webconstants.TEST_RESULT_PASS
            result=webconstants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg

    def refresh(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(driver_obj != None):
                driver_obj.refresh()
                logger.print_on_console('Browser refreshed')
                log.info('Browser refreshed')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg
    def navigateToURL(self ,webelement, url , *args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            url = url[0]
            if not (url is None and url is ''):
                url.strip()
                if url[0:4].lower()!='http' and url[0:4].lower()!='file':
                    url='http://'+url
                driver_obj.get(url)
                #ignore certificate implementation
                try:
                    ignore_certificate = configvalues['ignore_certificate']
                    if ((ignore_certificate.lower() == 'yes') and ((driver_obj.title !=None) and ('Certificate' in driver_obj.title))):
                        driver_obj.execute_script("""document.getElementById('overridelink').click();""")
                except Exception as k:
                    logger.print_on_console('Exception while ignoring the certificate')
                logger.print_on_console('Navigated to URL')
                log.info('Navigated to URL')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console(webconstants.INVALID_INPUT)
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
        """
        def : navigate_with_authenticate
        purpose : To open a URL which throws a popup and automatically fill
        the credentials and proceed to next window.
        param : URL,userID,password,timeout(Optional)
        return : bool
        """

        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if (url[0] is not None and url[0] != '')\
             and (url[1] is not None and url[1] != '')\
              and (url[2] is not None and url[2] != ''):
                from encryption_utility import AESCipher
                encryption_obj = AESCipher()
                input_val = encryption_obj.decrypt(url[2])
                url[2]=input_val
                t=TestThread(url)
                if len(url)>3:
                    url[3]=int(url[3])
                    timeout=url[3]
                    time.sleep(int(timeout))
                else:
                    time.sleep(6)

                # defect #193 added functionality for authentication automation in browser popup (Himanshu)
                if(isinstance(driver_obj,webdriver.Ie)):
                    obj=SF()
                    username=url[1].strip()
                    password=url[2]
                    obj.type(username)
                    obj.execute_key('tab',1)
                    obj.type(password)
                    obj.execute_key('tab',1)
                    obj.execute_key('spacebar',1)
                    obj.execute_key('tab',1)
                    obj.execute_key('enter',1)
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
                else:
                    obj=SF()
                    username=url[1].strip()
                    match_found_flag = False
                    password=url[2]
                    obj.type(username)
                    obj.execute_key('tab',1)
                    obj.type(password)
                    obj.execute_key('tab',1)
                    obj.execute_key('enter',1)
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE

            else:
                logger.print_on_console(webconstants.INVALID_INPUT)
                log.error(webconstants.INVALID_INPUT)
                err_msg = webconstants.INVALID_INPUT
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


    def getPageTitle(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        page_title = None
        err_msg=None
        try:
            if (driver_obj!= None):
                page_title= driver_obj.title
                if (page_title is ''):
                    page_title= driver_obj.current_url
                page_title.strip()
##                logger.print_on_console('Page title is ',page_title)
                log.info('Page title is ' + page_title)
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
                log.error('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,page_title,err_msg

    def verify_page_title(self,webelement,input_val,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
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
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Page title mismatched')
                    logger.print_on_console(EXPECTED,userinput)
                    log.info(EXPECTED)
                    log.info(userinput)
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
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        url = None
        err_msg=None
        try:
            if (driver_obj!= None):
                url= driver_obj.current_url
                url.strip()
                logger.print_on_console('URL: ',url)
                log.info('URL: '+ url)
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
                log.error('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,url,err_msg

    def verifyCurrentURL(self ,webelement, input_url,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
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
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
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
                log.error(webconstants.INVALID_INPUT)
                logger.print_on_console(webconstants.INVALID_INPUT)
                err_msg = webconstants.INVALID_INPUT
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


    def closeBrowser(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        if(len(webdriver_list) > 0):
            try:
                driver_instance = len(webdriver_list)-1
                winHandles = webdriver_list[driver_instance].window_handles
                current_handle = webdriver_list[driver_instance].current_window_handle
                count = 0
                for x in winHandles:
                    count+=1
                    if(current_handle == x):
                        break
                count = count - 2
                webdriver_list[driver_instance].quit()
                logger.print_on_console('browser closed')
                log.info('browser closed')
                ## Issue #190 Driver control won't switch back to parent window
                webdriver_list.pop(len(webdriver_list)-1)
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        else:
            logger.print_on_console('For this close browser open browser or open new browser is not present')
            log.error('For this close browser open browser or open new browser is not present')
        return status,result,output,err_msg


    def maximizeBrowser(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(driver_obj!= None):
                driver_obj.maximize_window()
                logger.print_on_console('browser maximized')
                log.info('browser maximized')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
                log.error('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


    def closeSubWindows(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        ## Issue #190 Driver control won't switch back to parent window
        global all_handles
        global parent_handle
        global recent_handles
        err_msg=None
        try:
            if (len(args) > 1):
                inp = args[1]
                inp = str(inp[0])
            if len(all_handles) > 1:
                if(inp == 'ALL'):
                    while all_handles[-1]!=parent_handle:
                        try:
                            driver_obj.switch_to.window(all_handles[-1])
                            driver_obj.close()
                            all_handles=all_handles[0:-1]
                            logger.print_on_console('Sub window closed')
                            log.info('Sub window closed')
                        except Exception as e:
                            err_msg=self.__web_driver_exception(e)
                else:
                    try:
                        driver_obj.switch_to.window(all_handles[-1])
                        driver_obj.close()
                        all_handles=all_handles[0:-1]
                        logger.print_on_console('Sub window closed')
                        log.info('Sub windows closed')
                    except Exception as e:
                        err_msg=self.__web_driver_exception(e)

                if(len(all_handles) >= 1):
                    driver_obj.switch_to.window(parent_handle)
                    self.update_recent_handle(parent_handle)
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('No sub windows to close')
                log.info('No sub windows to close')

        except Exception as e:
            err_msg=self.__web_driver_exception(e)
            driver_obj.switch_to.window(parent_handle)
        return status,result,output,err_msg

    def clear_cache(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
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
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE

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

    def update_window_handles(self):
    	## Issue #190 Driver control won't switch back to parent window
        global driver_obj
        global all_handles
        global recent_handles
        if driver_obj is not None:
            try:
                delay_time=float(configvalues['delay'])
                time.sleep(delay_time)
                winHandles=list(driver_obj.window_handles)
                new_handles=[]
                invalid_handles=[]
                all_handles=list(OrderedDict.fromkeys(all_handles))
                for h in all_handles:
                    if h in winHandles:
                        new_handles.append(h)
                        winHandles.remove(h)
                    else:
                        invalid_handles.append(h)
                del all_handles[:]
                if len(winHandles)>0:
                    all_handles=new_handles+winHandles
                else:
                    all_handles=new_handles
                #parent_handle=all_handles[0]
                recent_handles=filter(lambda a:a not in invalid_handles,recent_handles)
                if len(recent_handles)>0:
                    driver_obj.switch_to.window(recent_handles[-1])
            except Exception as e:
                log.error(e)

    def validate_current_window_handle(self):
    	## Issue #190 Driver control won't switch back to parent window
        global driver_obj
        if driver_obj is not None:
            try:
                winHandles=driver_obj.window_handles
                curHandle=driver_obj.current_window_handle
            except Exception as e:
                log.error(e)
                rev_recent_handles=list(recent_handles)
                rev_recent_handles.reverse()
                for h in rev_recent_handles:
                    try:
                        driver_obj.switch_to.window(h)
                    except Exception as e:
                        log.error(e)

    def update_recent_handle(self,h):
        global recent_handles
        if len(recent_handles)==0 or recent_handles[-1]!=h:
            recent_handles.append(h)


class Singleton_DriverUtil():
##    def check_available_driver(self,browser_num):
##        global driver_obj
##        import os
##        try:
##            import browserops
##            log.debug("browserops.driver ",browserops.driver)
####            scrapedriver = browserops.driver
##            toCheck = browserops.driver.window_handles
##            print toCheck
##            if(len(toCheck)== 0):
##                import win32com.client
##                my_processes = ['IEDriverServer.exe','IEDriverServer64.exe']
##                wmi=win32com.client.GetObject('winmgmts:')
##                for p in wmi.InstancesOf('win32_process'):
##                    if p.Name in my_processes:
##                        os.system("TASKKILL /F /IM " + p.Name)
##                if browserops.driver.name == 'internet explorer':
##                    driver_instance = self.driver('3')
##                    return driver_instance
##            else:
##                return browserops.driver
##
##
##        except Exception as e:
##            import win32com.client
##            my_processes = ['chromedriver.exe','phantomjs.exe','geckodriver.exe']
##            wmi=win32com.client.GetObject('winmgmts:')
##            for p in wmi.InstancesOf('win32_process'):
##                if p.Name in my_processes:
##                    os.system("TASKKILL /F /IM " + p.Name)
##            if browserops.driver == None:
##                return self.driver(browser_num)
##            else:
##                if browserops.driver.name == 'chrome':
##                    driver_instance =self.driver('1')
##                    return driver_instance
##                elif browserops.driver.name == 'firefox':
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
        elif browserType == '6':
            if len(drivermap) > 0:
                for i in drivermap:
                    if isinstance(i, webdriver.Safari):
                        try:
                            if len(i.window_handles) == 0:
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
        global recent_handles
        global all_handles
        del recent_handles[:]
        del all_handles[:]
        driver=None
        log.debug('BROWSER NUM: ')
        log.debug(browser_num)
        logger.print_on_console( 'BROWSER NUM: ',browser_num)

        if (browser_num == '1'):
            chrome_path = configvalues['chrome_path']
            exec_path = webconstants.CHROME_DRIVER_PATH
            if ((str(chrome_path).lower()) == 'default'):
                choptions = webdriver.ChromeOptions()
                choptions.add_argument('start-maximized')
                choptions.add_argument('--disable-extensions')
                driver = webdriver.Chrome(chrome_options=choptions, executable_path=exec_path)
            else:
                choptions = webdriver.ChromeOptions()
                choptions.add_argument('start-maximized')
                choptions.add_argument('--disable-extensions')
                driver = webdriver.Chrome(desired_capabilities= choptions.to_capabilities(), executable_path = exec_path)
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
##                def find_file(root_folder, rex):
##                    found = False
##                    for root,dirs,files in os.walk(root_folder):
##                        for f in files:
##                            result = rex.search(f)
##                            if result:
##                                found = True
##                                firefox_path = os.path.join(root,f)
##                                firefox_arr = [firefox_path,found]
##                                break
##                        if found:
##                            break
##                    return firefox_arr
##
##                def find_file_in_all_drives(file_name):
##                    #create a regular expression for the file
##                    rex = re.compile(file_name)
##                    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
##                        found = find_file( drive, rex )
##                        path=found[0]
##                        flag=found[1]
##                        if flag:
##                            break
##                    return path
##
##                path = find_file_in_all_drives( 'firefox.exe' )
##                # To fetch the version of the firefox browser
##                info = win32api.GetFileVersionInfo(path, "\\")
##                ms = info['ProductVersionMS']
##                ls = info['ProductVersionLS']
##                ver = win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls)
##                version = ver[0]
##
##                # opening firefox browser through selenium if the version 47 and less than 47
##                ignore_certificate = configvalues['ignore_certificate']
##                profile = webdriver.FirefoxProfile()
##                if ignore_certificate.lower() == 'yes':
##                    profile.accept_untrusted_certs = True
##                if int(version) < 48:
##                    driver = webdriver.Firefox(firefox_profile=profile)
##                    drivermap.append(driver)
##                    driver.maximize_window()
##                    logger.print_on_console('Firefox browser started')
##                    log.info('Firefox browser started')
##                else:
                    caps=webdriver.DesiredCapabilities.FIREFOX
                    caps['marionette'] = True
                    driver = webdriver.Firefox(capabilities=caps,executable_path=webconstants.GECKODRIVER_PATH)
                    drivermap.append(driver)
                    driver.maximize_window()
                    logger.print_on_console('Firefox browser started using geckodriver')
                    log.info('Firefox browser started using geckodriver ')
            except Exception as e:
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
                iepath = webconstants.IE_DRIVER_PATH_32
            else:
                iepath = webconstants.IE_DRIVER_PATH_64
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
            driver = webdriver.PhantomJS(executable_path=webconstants.PHANTOM_DRIVER_PATH)
            drivermap.append(driver)
            logger.print_on_console('Phantom browser started')

        elif(browser_num == '6'):
            print 'This will be our new safari'
            driver = webdriver.Safari()
            drivermap.append(driver)

            
            logger.print_on_console('Safari browser started')
            log.info('Safari browser started')
##        print __driver
        return driver





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