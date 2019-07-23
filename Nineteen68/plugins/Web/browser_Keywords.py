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
import threading
import os
from constants import *
import logging
import clientwindow
import platform
if SYSTEM_OS != 'Darwin':
    import win32gui
    import win32api
    import utils_web
    import win32process
    import win32con
    from pywinauto import Application
import psutil
import readconfig
import core_utils
import time
from sendfunction_keys import SendFunctionKeys as SF
driver_pre =None
local_bk = threading.local()

#New Thread to navigate to given url for the keyword 'naviagteWithAut'
class TestThread(threading.Thread):
    """Test Worker Thread Class."""
    def __init__(self,url):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self.url=url

    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        time.sleep(1)
        local_bk.driver_obj.get(self.url)



class BrowserKeywords():
    def __init__(self):
        self.browser_num=''
        self.windows=[]
        self.params=[]
        local_bk.driver_obj = None
        local_bk.parent_handle=None
        local_bk.all_handles=[]
        local_bk.recent_handles=[]
        local_bk.webdriver_list = []
        local_bk.drivermap = []
        local_bk.pid_set = []
        local_bk.log = logging.getLogger('browser_Keywords.py')

    def __web_driver_exception(self,e):
        local_bk.log.error(e,exc_info=True)
        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        logger.print_on_console(err_msg)
        return err_msg

    def openBrowser(self,webelement,browser_num,*args):
        global local_bk,driver_pre
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        self.browser_num=browser_num[0]
        configvalues = readconfig.configvalues
        try:
            obj = Singleton_DriverUtil()
            # ref: <gitlabpath>/nineteen68v2.0/Nineteen68/issues/1556
            # Logic for config file status on `enableSecurityCheck`
            enableSecurityFlag = False
            if (str(configvalues['enableSecurityCheck']).lower() == 'yes'):
                enableSecurityFlag = True
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
                        local_bk.log.error(e)
                    del local_bk.drivermap[:]
                    local_bk.driver_obj = obj.getBrowser(self.browser_num)
                elif d != None:
                    #driver exist in map, get it
                    local_bk.driver_obj = d
                else:
                    #instantiate new browser and add it to the map
                    local_bk.driver_obj = obj.getBrowser(self.browser_num)
            elif browser_num[-1] == EXECUTE:
                local_bk.driver_obj=obj.getBrowser(self.browser_num)
                del local_bk.drivermap[:]
            if(local_bk.driver_obj == None):
                result = TERMINATE
            else:
                if SYSTEM_OS!='Darwin':
                    utilobject = utils_web.Utils()
                    pid = None
                    if (self.browser_num == '1'):
                        #Logic to the pid of chrome window
                        p = psutil.Process(local_bk.driver_obj.service.process.pid)
                        pidchrome = p.children()[0]
                        pid = pidchrome.pid
                        local_bk.pid_set.append(pid)
                    elif(self.browser_num == '2'):
                        #logic to get the pid of the firefox window
                        try:
                            pid = local_bk.driver_obj.binary.process.pid
                        except Exception as e:
                            p = psutil.Process(local_bk.driver_obj.service.process.pid)
                            pidchrome = p.children()[0]
                            pid = pidchrome.pid
                            local_bk.pid_set.append(pid)
                    elif(self.browser_num == '3'):
                        # Logic checks if security settings needs to be addressed
                        # ref: <gitlabpath>/nineteen68v2.0/Nineteen68/issues/1556
                        if enableSecurityFlag:
                            local_bk.driver_obj = obj.set_security_zones(
                                self.browser_num, local_bk.driver_obj)
                        #Logic to get the pid of the ie window
                        p = psutil.Process(local_bk.driver_obj.iedriver.process.pid)
                        pidie = p.children()[0]
                        pid = pidie.pid
                        local_bk.pid_set.append(pid)
                    hwndg = utilobject.bring_Window_Front(pid)
                self.update_pid_set(enableSecurityFlag)
                local_bk.webdriver_list.append(local_bk.driver_obj)
                local_bk.parent_handle =  None
                try:
                    local_bk.parent_handle = local_bk.driver_obj.current_window_handle
                except Exception as nosuchWindowExc:
                    local_bk.log.error(nosuchWindowExc)
                    local_bk.log.warn("A window or tab was closed manually from the browser!")
                if local_bk.parent_handle is not None:
                    self.update_recent_handle(local_bk.parent_handle)
                    local_bk.all_handles.append(local_bk.parent_handle)
                elif len(local_bk.all_handles) > 0:
                    driver_handles = local_bk.driver_obj.window_handles
                    switch_to_handle = None
                    for handle in local_bk.all_handles:
                        if handle in driver_handles:
                            switch_to_handle = handle
                            break
                    if switch_to_handle is not None:
                        local_bk.log.info("driver will now switch to the first window/tab")
                        local_bk.driver_obj.switch_to.window(switch_to_handle)
                    else:
                        local_bk.log.info("driver will now switch to any available window/tab")
                        local_bk.driver_obj.switch_to.window(driver_handles[0])
                logger.print_on_console('Browser opened')
                local_bk.log.info('Browser opened')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        driver_pre = local_bk.driver_obj
        return status,result,output,err_msg


    def openNewBrowser(self,*args):
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        configvalues = readconfig.configvalues
        try:
            driver = Singleton_DriverUtil()
            # ref: <gitlabpath>/nineteen68v2.0/Nineteen68/issues/1556
            # Logic for config file status on `enableSecurityCheck`
            enableSecurityFlag = False
            if (str(configvalues['enableSecurityCheck']).lower() == 'yes'):
                enableSecurityFlag = True
            local_bk.driver_obj=driver.getBrowser(self.browser_num)
            if(local_bk.driver_obj == None):
                result = TERMINATE
            else:
                # Logic checks if security settings needs to be addressed
                # ref: <gitlabpath>/nineteen68v2.0/Nineteen68/issues/1556
                if enableSecurityFlag:
                    local_bk.driver_obj = driver.set_security_zones(
                        self.browser_num, local_bk.driver_obj)
                self.update_pid_set(enableSecurityFlag)
                local_bk.webdriver_list.append(local_bk.driver_obj)
                local_bk.parent_handle = local_bk.driver_obj.current_window_handle
                self.update_recent_handle(local_bk.parent_handle)
                local_bk.all_handles.append(local_bk.parent_handle)
                logger.print_on_console('Opened new browser')
                local_bk.log.info('Opened new browser')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg

    def refresh(self,*args):
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(local_bk.driver_obj != None):
                local_bk.driver_obj.refresh()
                logger.print_on_console('Browser refreshed')
                local_bk.log.info('Browser refreshed')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg

    def navigateToURL(self, webelement, url, *args):
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            url = url[0]
            if not (url is None and url.strip() is ''):
                url = url.strip()
                if url[0:7].lower()!='http://' and url[0:8].lower()!='https://' and url[0:5].lower()!='file:':
                    url='http://'+url
                local_bk.driver_obj.get(url)
                #ignore certificate implementation
                try:
                    ignore_certificate = readconfig.configvalues['ignore_certificate']
                    if ((ignore_certificate.lower() == 'yes') and ((local_bk.driver_obj.title !=None) and ('Certificate' in local_bk.driver_obj.title))):
                        local_bk.driver_obj.execute_script("""document.getElementById('overridelink').click();""")
                except Exception as k:
                    logger.print_on_console('Exception while ignoring the certificate')
                logger.print_on_console('Navigated to URL')
                local_bk.log.info('Navigated to URL')
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

    #helper functions for navigate_with_authenticate
    def enum_window_callback(self,hwnd, pid):
        tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
        if pid == current_pid and win32gui.IsWindowVisible(hwnd):
            self.windows.append(hwnd)



    def princon(self,hwnd, lparam):
        if win32gui.GetClassName(hwnd)=="Edit":
            self.params.append(hwnd)

    def navigate_with_authenticate(self,webelement, url, *args):
        """
        def : navigate_with_authenticate
        purpose : To open a URL which throws a popup and automatically fill
        the credentials and proceed to next window.
        param : URL,userID,password,timeout(Optional)
        return : bool
        """
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None

        try:
            inputURL = url[0]
            if (inputURL is not None or inputURL != '') and (url[1] is not None or url[1] != '') and (url[2] is not None or url[2] != ''):
                from encryption_utility import AESCipher
                encryption_obj = AESCipher()
                input_val = encryption_obj.decrypt(url[2])
                url[2]=input_val
                inputURL = inputURL.strip()
                if len(inputURL)<7 or (inputURL[0:7].lower()!='http://' and inputURL[0:8].lower()!='https://' and inputURL[0:7].lower()!='file://'):
                    inputURL='http://'+inputURL
                if len(url)>3:
                    timeout=int(url[3])
                    time.sleep(timeout)
                else:
                    time.sleep(6)

                # defect #193 added functionality for authentication automation in browser popup (Himanshu)
                if(isinstance(local_bk.driver_obj,webdriver.Ie)):
                    local_bk.driver_obj.get(inputURL)
                    time.sleep(6)
                    driver_pid=local_bk.driver_obj.iedriver.process.pid
                    auth_window_pid=psutil.Process(psutil.Process(driver_pid).children()[0].pid).children()[0].pid
                    win32gui.EnumWindows(self.enum_window_callback, auth_window_pid)
                    try:
                        for i in self.windows:
                            if win32gui.GetWindowText(i)=="Windows Security":
                                win32gui.EnumChildWindows(i, self.princon, "extra")
                    except Exception as e:
                        err_msg = ERROR_CODE_DICT['ERR_EXCEPTION']
                        logger.error(e)
                    if len(self.params)>1:
                        win32gui.SendMessage(self.params[0], win32con.WM_SETTEXT,0,url[1])
                        time.sleep(0.5)
                        win32gui.SendMessage(self.params[1], win32con.WM_SETTEXT,0,url[2])
                        time.sleep(0.5)
                        app=Application().connect(process=auth_window_pid)
                        win=app['Windows Security']
                        children_win=win.children()
                        for c in children_win:
                            if str(c.friendly_class_name())=="Button":
                                win_text=c.Texts()
                                if str(win_text[0]) =='OK':
                                    c.Click()
                                    status=webconstants.TEST_RESULT_PASS
                                    result=webconstants.TEST_RESULT_TRUE
                        if status!=webconstants.TEST_RESULT_PASS:
                            err_msg=ERROR_CODE_DICT['ERR_WIN32']
                    elif len(self.params)==1:
                        app=Application().connect(process=auth_window_pid)
                        win=app['Windows Security']
                        children_win=win.children()
                        for c in children_win:
                            if str(c.friendly_class_name())=="Button":
                                win_text=c.Texts()
                                if str(win_text[0]) =='Cancel':
                                    c.Click()
                        err_msg = ERROR_CODE_DICT['ERR_REMEMBERED_CREDENTIALS_PRESENT']
                        #condition when password is saved  by windows credential manager
                        #return with Failed flag
                    else:
                        from pywinauto.application import Application as appl
                        app = appl().Connect(title=u'Windows Security')
                        credentialdialogxamlhost = app['Windows Security']
                        time.sleep(0.5)
                        credentialdialogxamlhost.ClickInput()
                        credentialdialogxamlhost.TypeKeys(url[1])
                        time.sleep(0.5)
                        credentialdialogxamlhost.TypeKeys("{TAB}")
                        credentialdialogxamlhost.TypeKeys(url[2])
                        time.sleep(0.5)
                        credentialdialogxamlhost.TypeKeys("{ENTER}")
                        status=webconstants.TEST_RESULT_PASS
                        result=webconstants.TEST_RESULT_TRUE
                    self.params = []
                    self.windows = []
                else:
                    auth_url=None
                    if inputURL[0:5]=="https":
                        auth_url=inputURL[0:8]+url[1]+":"+url[2]+"@"+inputURL[8:]
                    else:
                        auth_url=inputURL[0:7]+url[1]+":"+url[2]+"@"+inputURL[7:]
                    #chrome supports basic auth!
                    local_bk.driver_obj.get(auth_url)
                try:
                    ignore_certificate = readconfig.configvalues['ignore_certificate']
                    if ((ignore_certificate.lower() == 'yes') and ((local_bk.driver_obj.title !=None) and ('Certificate' in local_bk.driver_obj.title))):
                        local_bk.driver_obj.execute_script("""document.getElementById('overridelink').click();""")
                except Exception as k:
                    local_bk.log.error(k)
                    err_msg='Exception while ignoring the certificate'
                logger.print_on_console('Navigated to URL')
                local_bk.log.info('Navigated to URL')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                err_msg = webconstants.INVALID_INPUT
            if err_msg:
                logger.print_on_console(err_msg)
                local_bk.log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg

    def getPageTitle(self,*args):
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        page_title = None
        err_msg=None
        try:
            if (local_bk.driver_obj!= None):
                page_title= local_bk.driver_obj.title
                if (page_title is ''):
                    page_title= local_bk.driver_obj.current_url
                page_title.strip()
                logger.print_on_console('Page title is ',page_title)
                local_bk.log.info('Page title is ' + page_title)
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
                local_bk.log.error('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,page_title,err_msg

    def verify_page_title(self,webelement,input_val,*args):
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if (local_bk.driver_obj!= None):
                page_title= local_bk.driver_obj.title
                if (page_title is ''):
                    page_title= local_bk.driver_obj.current_url
                page_title.strip()
                coreutilsobj=core_utils.CoreUtils()
                userinput=coreutilsobj.get_UTF_8(input_val[0])
                if(page_title == userinput):
                    logger.print_on_console('Page title matched')
                    local_bk.log.info('Page title matched')
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Page title mismatched')
                    logger.print_on_console(EXPECTED,userinput)
                    local_bk.log.info(EXPECTED)
                    local_bk.log.info(userinput)
                    logger.print_on_console(ACTUAL,page_title)
                    local_bk.log.info(ACTUAL)
                    local_bk.log.info(page_title)
            else:
                local_bk.log.error('Driver object is null')
                logger.print_on_console('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


    def getCurrentURL(self,*args):
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        url = None
        err_msg=None
        try:
            if (local_bk.driver_obj!= None):
                url= local_bk.driver_obj.current_url
                url.strip()
                logger.print_on_console('URL: ',url)
                local_bk.log.info('URL: '+ url)
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
                local_bk.log.error('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,url,err_msg

    def verifyCurrentURL(self ,webelement, input_url,*args):
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if not (input_url is None and input_url is ''):
                url= local_bk.driver_obj.current_url
                url.strip()
                input_url=input_url[0].strip()
                if (url == input_url):
                    logger.print_on_console('Current url matched')
                    local_bk.log.info('Current url matched')
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Current url mismatched')
                    local_bk.log.error('Current url mismatched')
                    logger.print_on_console(EXPECTED,input_url)
                    local_bk.log.info(EXPECTED)
                    local_bk.log.info(input_url)
                    logger.print_on_console(ACTUAL,url)
                    local_bk.log.info(ACTUAL)
                    local_bk.log.info(url)
            else:
                local_bk.log.error(webconstants.INVALID_INPUT)
                logger.print_on_console(webconstants.INVALID_INPUT)
                err_msg = webconstants.INVALID_INPUT
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


    def closeBrowser(self,*args):
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        if(len(local_bk.webdriver_list) > 0):
            try:
                driver_instance = len(local_bk.webdriver_list)-1
                winHandles = local_bk.webdriver_list[driver_instance].window_handles
                current_handle = local_bk.webdriver_list[driver_instance].current_window_handle
                count = 0
                for x in winHandles:
                    count+=1
                    if(current_handle == x):
                        break
                count = count - 2
                local_bk.webdriver_list[driver_instance].quit()
                if SYSTEM_OS == 'Darwin':
                    import os
                    os.system("killall -9 Safari")
                logger.print_on_console('browser closed')
                local_bk.log.info('browser closed')
                ## Issue #190 Driver control won't switch back to parent window
                del local_bk.webdriver_list[:]
                del local_bk.pid_set[:]
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        else:
            logger.print_on_console('For this closeBrowser keyword, openBrowser or openNewBrowser keyword is not present')
            local_bk.log.error('For this closeBrowser keyword, openBrowser or openNewBrowser keyword is not present')
        return status,result,output,err_msg


    def maximizeBrowser(self,*args):
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(local_bk.driver_obj!= None):
                local_bk.driver_obj.maximize_window()
                logger.print_on_console('browser maximized')
                local_bk.log.info('browser maximized')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
                local_bk.log.error('Driver object is null')
                err_msg = 'Driver object is null'
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg


    def closeSubWindows(self,*args):
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        ## Issue #190 Driver control won't switch back to parent window
        err_msg=None
        try:
            if (len(args) > 1):
                inp = args[1]
                inp = str(inp[0])
            if len(local_bk.all_handles) > 1:
                if(inp == 'ALL'):
                    while local_bk.all_handles[-1]!=local_bk.parent_handle:
                        try:
                            local_bk.driver_obj.switch_to.window(local_bk.all_handles[-1])
                            local_bk.driver_obj.close()
                            local_bk.all_handles=local_bk.all_handles[0:-1]
                            logger.print_on_console('Sub window closed')
                            local_bk.log.info('Sub window closed')
                        except Exception as e:
                            err_msg=self.__web_driver_exception(e)
                else:
                    try:
                        local_bk.driver_obj.switch_to.window(local_bk.all_handles[-1])
                        local_bk.driver_obj.close()
                        local_bk.all_handles=local_bk.all_handles[0:-1]
                        logger.print_on_console('Sub window closed')
                        local_bk.log.info('Sub windows closed')
                    except Exception as e:
                        err_msg=self.__web_driver_exception(e)

                if(len(local_bk.all_handles) >= 1):
                    local_bk.driver_obj.switch_to.window(local_bk.parent_handle)
                    self.update_recent_handle(local_bk.parent_handle)
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('No sub windows to close')
                local_bk.log.info('No sub windows to close')

        except Exception as e:
            err_msg=self.__web_driver_exception(e)
            local_bk.driver_obj.switch_to.window(local_bk.parent_handle)
        return status,result,output,err_msg

    def clear_cache(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if local_bk.driver_obj != None and isinstance(local_bk.driver_obj,webdriver.Ie):
                #get all the cookies
                cookies=local_bk.driver_obj.get_cookies()
                if len(cookies)>0:
                    cookies_list=[]
                    for x in cookies:
                        cookies_list.append(x['name'])
                    logger.print_on_console('Cookies are ',str(cookies_list))
                    local_bk.log.info('Cookies are: ')
                    local_bk.log.info(cookies_list)
                    #delete_all_cookies()
                    local_bk.driver_obj.delete_all_cookies()
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE

                else:
                    logger.print_on_console('No Cookies found')
                    local_bk.log.error('No Cookies found')
                    err_msg = 'No Cookies found'
            else:
                logger.print_on_console("This feature is available only for Internet Explorer.")
                local_bk.log.error("This feature is available only for Internet Explorer.")
                err_msg = "This feature is available only for Internet Explorer."
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg

    def update_window_handles(self):
        global local_bk
    	## Issue #190 Driver control won't switch back to parent window
        if local_bk.driver_obj is not None:
            try:
                winHandles=list(local_bk.driver_obj.window_handles)
                new_handles=[]
                invalid_handles=[]
                local_bk.all_handles=list(OrderedDict.fromkeys(local_bk.all_handles))
                for h in local_bk.all_handles:
                    if h in winHandles:
                        new_handles.append(h)
                        winHandles.remove(h)
                    else:
                        invalid_handles.append(h)
                del local_bk.all_handles[:]
                if len(winHandles)>0:
                    local_bk.all_handles=new_handles+winHandles
                else:
                    local_bk.all_handles=new_handles
                #parent_handle=all_handles[0]
                local_bk.recent_handles=[a for a in local_bk.recent_handles if a not in invalid_handles]
                if len(local_bk.recent_handles)>0:
                    ## Fix Nineteen68#1278
                    if local_bk.driver_obj.current_window_handle != local_bk.recent_handles[-1]:
                        local_bk.driver_obj.switch_to.window(local_bk.recent_handles[-1])
            except Exception as e:
                local_bk.log.error(e)

    def validate_current_window_handle(self):
    	## Issue #190 Driver control won't switch back to parent window
        if local_bk.driver_obj is not None:
            try:
                winHandles=local_bk.driver_obj.window_handles
                curHandle=local_bk.driver_obj.current_window_handle
            except Exception as e:
                local_bk.log.error(e)
                rev_recent_handles=list(local_bk.recent_handles)
                rev_recent_handles.reverse()
                for h in rev_recent_handles:
                    try:
                        local_bk.driver_obj.switch_to.window(h)
                    except Exception as e:
                        local_bk.log.error(e)

    def update_recent_handle(self,h):
        global local_bk
        if len(local_bk.recent_handles)==0 or local_bk.recent_handles[-1]!=h:
            local_bk.recent_handles.append(h)

    def update_pid_set(self,enableSecurityFlag):
        if SYSTEM_OS!='Darwin':
            utilobject = utils_web.Utils()
            pid = None
            if (self.browser_num == '1'):
                #Logic to the pid of chrome window
                p = psutil.Process(local_bk.driver_obj.service.process.pid)
                pidchrome = p.children()[0]
                pid = pidchrome.pid
                local_bk.pid_set.append(pid)
            elif(self.browser_num == '2'):
                #logic to get the pid of the firefox window
                try:
                    pid = local_bk.driver_obj.binary.process.pid
                    local_bk.pid_set.append(pid)
                except Exception as e:
                    p = psutil.Process(local_bk.driver_obj.service.process.pid)
                    pidchrome = p.children()[0]
                    pid = pidchrome.pid
                    local_bk.pid_set.append(pid)

            elif(self.browser_num == '3'):
                # Logic checks if security settings needs to be addressed
                # ref: <gitlabpath>/nineteen68v2.0/Nineteen68/issues/1556
                if enableSecurityFlag:
                    local_bk.driver_obj = obj.set_security_zones(
                        self.browser_num, local_bk.driver_obj)
                #Logic to get the pid of the ie window
                p = psutil.Process(local_bk.driver_obj.iedriver.process.pid)
                pidie = p.children()[0]
                pid = pidie.pid
                local_bk.pid_set.append(pid)
            hwndg = utilobject.bring_Window_Front(pid)


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
        global local_bk
        d = None
##        drivermap.reverse()
        if browserType == '1':
            if len(local_bk.drivermap) > 0:
                for i in local_bk.drivermap:
                    if isinstance(i,webdriver.Chrome ):
                        try:
                            if len (i.window_handles) > 0:
                                d = i
                        except Exception as e:
                            d = 'stale'
                            break

        elif browserType == '2':
            if len(local_bk.drivermap) > 0:
                for i in local_bk.drivermap:
                    if isinstance(i,webdriver.Firefox ):
                        try:
                            if len (i.window_handles) > 0:
                                d = i
                        except Exception as e:
                            d = 'stale'
                            break
        elif browserType == '3':
            if len(local_bk.drivermap) > 0:
                for i in local_bk.drivermap:
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
            if len(local_bk.drivermap) > 0:
                for i in local_bk.drivermap:
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
        global local_bk
        del local_bk.recent_handles[:]
        del local_bk.all_handles[:]
        driver=None
        local_bk.log.debug('BROWSER NUM: ')
        local_bk.log.debug(browser_num)
        logger.print_on_console( 'BROWSER NUM: ',str(browser_num))
        flag1 = 0
        configvalues = readconfig.configvalues
        if (browser_num == '1'):
            try:
                chrome_path = configvalues['chrome_path']
                exec_path = webconstants.CHROME_DRIVER_PATH
                if  SYSTEM_OS == "Darwin":
                    exec_path = webconstants.drivers_path+"/chromedriver"
##                choptions1 = webdriver.ChromeOptions()
##                # --headless helps to run chrome without browser window
##                choptions1.add_argument('--headless')
##                driver = webdriver.Chrome(chrome_options=choptions1, executable_path=exec_path)
##                flag1 = self.chrome_version(driver)
##                driver = None
                ##print clientwindow.chromeFlag
                if( clientwindow.chromeFlag == True ):
                    choptions = webdriver.ChromeOptions()
                    choptions.add_argument('start-maximized')
                    if configvalues['extn_enabled'].lower()=='yes':
                        choptions.add_extension(webconstants.EXTENSION_PATH)
                    else:
                        choptions.add_argument('--disable-extensions')
                    if ((str(chrome_path).lower()) != 'default'):
                        choptions.binary_location=str(chrome_path)
                    driver = webdriver.Chrome(executable_path=exec_path,chrome_options=choptions)
                    ##driver = webdriver.Chrome(desired_capabilities= choptions.to_capabilities(), executable_path = exec_path)
                    local_bk.drivermap.append(driver)
                    driver.maximize_window()
                    logger.print_on_console('Chrome browser started')
                    local_bk.log.info('Chrome browser started')
                else:
                    logger.print_on_console('Chrome browser version not supported')
                    local_bk.log.info('Chrome browser version not supported')
                    driver = None
            except Exception as e:
                local_bk.log.error(e,exc_info=True)
                logger.print_on_console("Requested browser is not available")
                local_bk.log.info('Requested browser is not available')

        elif(browser_num == '2'):
            import os
            try:
                caps=webdriver.DesiredCapabilities.FIREFOX
                caps['marionette'] = True
                if SYSTEM_OS == "Darwin":
                    exec_path = webconstants.drivers_path+"/geckodriver"
                else:
                    exec_path = webconstants.GECKODRIVER_PATH
                if(clientwindow.firefoxFlag == True):
                    if str(configvalues['firefox_path']).lower()!="default":
                        from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
                        binary = FirefoxBinary(str(configvalues['firefox_path']))
                        driver = webdriver.Firefox(capabilities=caps, firefox_binary=binary, executable_path=exec_path)
                    else:
                        driver = webdriver.Firefox(capabilities=caps,executable_path=exec_path)
                    local_bk.drivermap.append(driver)
                    driver.maximize_window()
                    logger.print_on_console('Firefox browser started using geckodriver')
                    local_bk.log.info('Firefox browser started using geckodriver ')
                else:
                    driver = None
                    logger.print_on_console("Firefox browser version not supported")
                    local_bk.log.info('Firefox browser version not supported')
            except Exception as e:
                logger.print_on_console("Requested browser is not available")
                local_bk.log.info('Requested browser is not available')

        elif(browser_num == '3'):
            try:
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
##                browser_ver=driver.capabilities['version']
##                browser_ver1 = browser_ver.encode('utf-8')
##                browser_ver = int(browser_ver1)
##                if(browser_ver >= int(webconstants.IE_BROWSER_VERSION[0]) and browser_ver <= int(webconstants.IE_BROWSER_VERSION[1])):
                local_bk.drivermap.append(driver)
                driver.maximize_window()
                logger.print_on_console('IE browser started')
                local_bk.log.info('IE browser started')
##                else:
##                    driver.close()
##                    driver = None
##                    logger.print_on_console("IE browser version not supported")
##                    log.info('IE browser version not supported')
####                    logger.print_on_console("Browser version:",browser_ver)
##                    log.info('Browser version:',browser_ver)
            except Exception as e:
                logger.print_on_console("Requested browser is not available")
                local_bk.log.info('Requested browser is not available')

        elif(browser_num == '4'):
            try:
                driver = webdriver.Opera()
                local_bk.drivermap.append(driver)
                logger.print_on_console('Opera browser started')
            except Exception as e:
                logger.print_on_console("Requested browser is not available")
                local_bk.log.info('Requested browser is not available')

        elif(browser_num == '5'):
            try:
                driver = webdriver.PhantomJS(executable_path=webconstants.PHANTOM_DRIVER_PATH)
                local_bk.drivermap.append(driver)
                logger.print_on_console('Phantom browser started')
            except Exception as e:
                logger.print_on_console("Requested browser is not available")
                local_bk.log.info('Requested browser is not available')

        elif(browser_num == '6'):
            try:
                driver = webdriver.Safari()
                driver.set_window_size(1024, 768)
                local_bk.drivermap.append(driver)


                logger.print_on_console('Safari browser started')
                local_bk.log.info('Safari browser started')

            except Exception as e:
                logger.print_on_console("Requested browser is not available")
                local_bk.log.info('Requested browser is not available')
        return driver

    # ref: <gitlabpath>/nineteen68v2.0/Nineteen68/issues/1556
    def fetch_security_zones(self):
        try:
            import subprocess
            zonevalues = []
            # running the batch file to fetch assigned settings
            p = subprocess.Popen(webconstants.drivers_path + "\\regfile.bat",
                                 cwd=webconstants.drivers_path)
            stdout, stderr = p.communicate()
            zonespath = webconstants.drivers_path + "\\zones.txt"
            # reading the zones file containing zones specs
            if os.path.isfile(zonespath):
                with open(zonespath) as f:
                    content = f.readlines()
                    for eachline in content:
                        if ('2500' in eachline):
                            zonevalues.append(
                                str(eachline.strip()).split("0x")[1])
            # deleting the file generated by batch file
            os.remove(zonespath)
            # re-arranging the values based on the requirement
            # return list should be indexed in 2,0,1,3 order only
            return [zonevalues[2], zonevalues[0], zonevalues[1], zonevalues[3]]
        except Exception as fetch_security_zonesexc:
            logger.print_on_console('error in retrieving zones data.'
                                    , fetch_security_zonesexc)

    # ref: <gitlabpath>/nineteen68v2.0/Nineteen68/issues/1556
    def set_security_zones(self, browsernumber, driverobj):
            try:
                global local_bk
                # fetch the zones settings from registry
                zonevalues = list(self.fetch_security_zones())
                flag = False
                # checks if zone values are on the same lines
                if '3' in zonevalues and '0' in zonevalues:
                    flag = False
                else:
                    flag = True
                # checks if flag is false, performs action if condition is true.
                if not flag:
                    sendfunctionkeys_obj = SF()
                    sendfunctionkeys_obj.press_multiple_keys(['alt', 'x'], 1)
                    time.sleep(0.5)
                    sendfunctionkeys_obj.execute_key('o', 1)
                    time.sleep(0.5)
                    sendfunctionkeys_obj.press_multiple_keys(['ctrl', 'tab'], 1)
                    time.sleep(0.5)
                    if zonevalues[0] == '3':
                        sendfunctionkeys_obj.execute_key('leftarrow', 1)
                        time.sleep(0.5)
                        sendfunctionkeys_obj.press_multiple_keys(['alt', 'p'], 1)
                        time.sleep(0.5)
                        sendfunctionkeys_obj.press_multiple_keys(['alt', 'a'], 1)
                    else:
                        sendfunctionkeys_obj.execute_key('leftarrow', 1)
                    time.sleep(0.5)
                    if zonevalues[1] == '3':
                        sendfunctionkeys_obj.execute_key('rightarrow', 1)
                        time.sleep(0.5)
                        sendfunctionkeys_obj.press_multiple_keys(['alt', 'p'], 1)
                        time.sleep(0.5)
                        sendfunctionkeys_obj.press_multiple_keys(['alt', 'a'], 1)
                    else:
                        sendfunctionkeys_obj.execute_key('rightarrow', 1)
                    time.sleep(0.5)
                    if zonevalues[2] == '3':
                        sendfunctionkeys_obj.execute_key('rightarrow', 1)
                        time.sleep(0.5)
                        sendfunctionkeys_obj.press_multiple_keys(['alt', 'p'], 1)
                        time.sleep(0.5)
                        sendfunctionkeys_obj.press_multiple_keys(['alt', 'a'], 1)
                    else:
                        sendfunctionkeys_obj.execute_key('rightarrow', 1)
                    time.sleep(0.5)
                    if zonevalues[3] == '3':
                        sendfunctionkeys_obj.execute_key('rightarrow', 1)
                        time.sleep(0.5)
                        sendfunctionkeys_obj.press_multiple_keys(['alt', 'p'], 1)
                        time.sleep(0.5)
                        sendfunctionkeys_obj.press_multiple_keys(['alt', 'a'], 1)
                        time.sleep(0.5)
                    sendfunctionkeys_obj.execute_key('enter', 1)
                    time.sleep(0.5)
                    try:
                        driverobj.quit()
                        logger.print_on_console('Security zones modified, Browser closed.')
                        local_bk.driver_obj = self.getBrowser(browsernumber)
                    except Exception as internalexcsecuset:
                        logger.print_on_console('error setting '
                                                + 'Browsers Security.', internalexcsecuset)
                return local_bk.driver_obj
            except Exception as set_security_zonesexc:
                logger.print_on_console('error in setting updated zones data.'
                                        , set_security_zonesexc)


    def chrome_version(self,driver):
        browser_ver = driver.capabilities['version']
        browser_ver1 = browser_ver.encode('utf-8')
        browser_ver = int(browser_ver1[:2])
        local_bk.log.info('Browser version:',str(browser_ver))
        driver_ver = driver.capabilities['chrome']['chromedriverVersion']
        driver_ver1 = driver_ver.encode('utf-8')
        driver_ver = float(driver_ver1[:4])
##        logger.print_on_console('Driver version:',driver_ver)
        local_bk.log.info('Driver version:',str(driver_ver))

##        logger.print_on_console(webconstants.CHROME_DRIVER_VERSION[0][0])
##        logger.print_on_console(type(webconstants.CHROME_DRIVER_VERSION[0][0]))
        for i in range(0,len(webconstants.CHROME_DRIVER_VERSION)):
##            print i
            if(driver_ver == float(webconstants.CHROME_DRIVER_VERSION[i][0]) and browser_ver >= int(webconstants.CHROME_DRIVER_VERSION[i][1]) and browser_ver <= int(webconstants.CHROME_DRIVER_VERSION[i][2])):
                flag1 = 1
##                logger.print_on_console('Flag:',flag1)
                local_bk.log.info('Flag:',str(flag1))
                return flag1
            else:
                flag1 = 0
##        logger.print_on_console('Flag:',flag1)
        local_bk.log.info('Flag:',str(flag1))
        return flag1



