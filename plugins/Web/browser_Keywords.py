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
from selenium.common.exceptions import NoSuchWindowException
import edge_chromium_options
from collections import OrderedDict
import logger
import webconstants
import threading
import os
from constants import *
import logging
import core
import platform
import time
from network_data import NetworkData
if SYSTEM_OS == 'Windows':
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
import fileinput
import glob
from sendfunction_keys import SendFunctionKeys as SF
import cicd_core

driver_pre = None
drivermap = []
linux_drivermap=[]
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
        local_bk.pid_set = []
        local_bk.log = logging.getLogger('browser_Keywords.py')

    def __web_driver_exception(self,e):
        local_bk.log.error(e,exc_info=True)
        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        logger.print_on_console(err_msg)
        return err_msg

    def openBrowser(self,webelement,browser_num,*args):
        global local_bk, driver_pre, drivermap,linux_drivermap
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        self.browser_num=browser_num[0]
        configvalues = readconfig.configvalues
        try:
            obj = Singleton_DriverUtil()
            # Logic for config file status on `enableSecurityCheck`
            enableSecurityFlag = False
            if (str(configvalues['enableSecurityCheck']).lower() == 'yes'):
                enableSecurityFlag = True
            #Logic to make sure that logic of usage of existing driver is not applicable to execution
            if  browser_num[-1] != EXECUTE:
                d = obj.check_if_driver_exists_in_map(self.browser_num)
                if d == 'stale':
                    #stale logic
                    try:
                        import win32com.client
                        my_processes = ['chromedriver.exe','msedgedriver.exe','MicrosoftWebDriver.exe','MicrosoftEdge.exe','IEDriverServer.exe','IEDriverServer64.exe','CobraWinLDTP.exe','phantomjs.exe']
                        for i in drivermap:
                            if (i.capabilities['browserName'] == 'internet explorer'):
                                pid=local_bk.driver_obj.iedriver.process.pid
                                os.system("TASKKILL /F /T /PID " + str(pid))
                            else:
                                wmi=win32com.client.GetObject('winmgmts:')
                                for p in wmi.InstancesOf('win32_process'):
                                    if p.Name in my_processes:
                                        os.system("TASKKILL /F /IM " + p.Name)
                    except Exception as e:
                        local_bk.log.error(e)
                    del drivermap[:]
                    local_bk.driver_obj = obj.getBrowser(self.browser_num)
                elif d != None:
                    #driver exist in map, get it
                    local_bk.driver_obj = d
                    #  Bug 18160- Firefox browser does not come to foreground
                    if(SYSTEM_OS=='Windows' and isinstance(local_bk.driver_obj, webdriver.Firefox)):
                        try:
                            mozPid = local_bk.driver_obj.desired_capabilities['moz:processID']
                            mozApp = Application().connect(process=mozPid)
                            # check if firefox is minimized (iconic)
                            if (win32gui.IsIconic(mozApp.top_window().handle)):
                                win_name = local_bk.driver_obj.title+' — Mozilla Firefox'
                                if(win32gui.FindWindow(None, win_name) != 0):
                                    handle = win32gui.FindWindow(None, win_name)
                                    win32gui.ShowWindow(handle, win32con.SW_MAXIMIZE)
                                    win32gui.SetForegroundWindow(handle)
                                    # win32gui.ShowWindow(mozApp.top_window().handle, win32con.SW_MAXIMIZE)
                            else:
                                mozApp.top_window().set_focus()
                        except Exception as e:
                            local_bk.log.error(e)
                else:
                    #instantiate new browser and add it to the map
                    local_bk.driver_obj = obj.getBrowser(self.browser_num)
            elif browser_num[-1] == EXECUTE:
                local_bk.driver_obj=obj.getBrowser(self.browser_num)
                del drivermap[:]
                linux_drivermap.append(local_bk.driver_obj)
            if(local_bk.driver_obj == None):
                result = TERMINATE
            else:
                if SYSTEM_OS == 'Windows':
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
                        if enableSecurityFlag:
                            local_bk.driver_obj = obj.set_security_zones(
                                self.browser_num, local_bk.driver_obj)
                        #Logic to get the pid of the ie window
                        p = psutil.Process(local_bk.driver_obj.iedriver.process.pid)
                        pidie = p.children()[0]
                        pid = pidie.pid
                        local_bk.pid_set.append(pid)
                    elif(self.browser_num == '7'):
                        if enableSecurityFlag:
                            local_bk.driver_obj = obj.set_security_zones(
                                self.browser_num, local_bk.driver_obj)
                        p = psutil.Process(local_bk.driver_obj.edge_service.process.pid)
                        pidedge = p.children()[0]
                        pid = pidedge.pid
                        local_bk.pid_set.append(pid)
                    elif (self.browser_num == '8'):
                        p = psutil.Process(local_bk.driver_obj.edge_service.process.pid)
                        pidchromium = p.children()[0]
                        pid = pidchromium.pid
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
            # Logic for config file status on `enableSecurityCheck`
            enableSecurityFlag = False
            if (str(configvalues['enableSecurityCheck']).lower() == 'yes'):
                enableSecurityFlag = True
            local_bk.driver_obj=driver.getBrowser(self.browser_num)
            if(local_bk.driver_obj == None):
                result = TERMINATE
            else:
                # Logic checks if security settings needs to be addressed
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

    def openNewTab(self ,*args):
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if isinstance(local_bk.driver_obj,webdriver.Ie):
                err_msg = "openNewTab Keyword is not supported in IE"
                logger.print_on_console(err_msg)
                local_bk.log.warn(err_msg)
            else:
                cwh=local_bk.driver_obj.current_window_handle
                cwh_in=local_bk.all_handles.index(cwh)
                local_bk.driver_obj.execute_script("window.open('');")
                handles = local_bk.driver_obj.window_handles
                local_bk.driver_obj.switch_to.window(handles[-1])
                h=local_bk.driver_obj.current_window_handle
                local_bk.all_handles.insert(cwh_in+1,h)
                # local_bk.recent_handles.insert(cwh_in+1,h)
                # local_bk.all_handles.append(h)
                local_bk.recent_handles.append(h)
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

    def navigateToURL(self, webelement, url, socketIO, *args):
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        t = None
        try:
            url = url[0]
            if not (url is None and url.strip() is ''):
                url = url.strip()
                if url[0:7].lower()!='http://' and url[0:8].lower()!='https://' and url[0:5].lower()!='file:':
                    url='http://'+url
                if (isinstance(local_bk.driver_obj,webdriver.Firefox)) and url[0:5].lower() == 'file:' and url[0:10].count("/") != 5:
                    url = url.split(":")
                    url = url[0] + ":" + "///" + url[1]
                local_bk.driver_obj.get(url)
                #ignore certificate implementation
                try:
                    ignore_certificate = readconfig.configvalues['ignore_certificate']
                    tab_title = local_bk.driver_obj.title
                    if ((ignore_certificate.lower() == 'yes') and (tab_title is not None)):
                        if 'Certificate' in tab_title:
                            local_bk.driver_obj.execute_script("""document.getElementById('overridelink').click();""")
                        elif 'Privacy error' in tab_title:
                            local_bk.driver_obj.execute_script("""document.getElementById('details-button').click();document.getElementById('proceed-link').click();""")
                except Exception as k:
                    logger.print_on_console('Exception while ignoring the certificate')
                #Network Data Capture    
                network_operation = NetworkData(local_bk.driver_obj)
                network_operation.network_data()
        
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
                        app = Application().Connect(title=u'Windows Security')
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
                #Network Data Capture
                network_operation = NetworkData(local_bk.driver_obj)
                network_operation.network_data()
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

    def navigate_back(self, webelement, url, *args):
        """performs a back operation"""
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            local_bk.driver_obj.execute_script("window.history.go(-1)")
            status=webconstants.TEST_RESULT_PASS
            result=webconstants.TEST_RESULT_TRUE
            
            #Network Data Capture
            network_operation = NetworkData(local_bk.driver_obj)
            network_operation.network_data()
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg

    def execute_js(self, inputval, *args):
        """performs a back operation"""
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            inputval="return window."+args[0][0]
            op=local_bk.driver_obj.execute_script(inputval)
            if(op!=None):
                output=op
            status=webconstants.TEST_RESULT_PASS
            result=webconstants.TEST_RESULT_TRUE
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
                    if isinstance(local_bk.driver_obj, webdriver.Firefox) and (page_title == 'about:blank' or page_title == 'about:newtab'):
                        page_title="New Tab" 
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
        empty_ie_window_handle=False
        if(len(local_bk.webdriver_list) > 0):
            try:
                driver_instance = len(local_bk.webdriver_list)-1
                winHandles = local_bk.webdriver_list[driver_instance].window_handles
                if winHandles == []:
                    if (local_bk.webdriver_list[driver_instance].capabilities['browserName'] == 'internet explorer'):
                        pid=local_bk.webdriver_list[driver_instance].iedriver.process.pid
                        os.system("TASKKILL /F /T /PID " + str(pid))
                        time.sleep(5)
                        local_bk.driver_obj = None
                        empty_ie_window_handle = True
                else:
                    current_handle = local_bk.webdriver_list[driver_instance].current_window_handle
                count = 0
                for x in winHandles:
                    count+=1
                    if(current_handle == x):
                        break
                count = count - 2
                if isinstance(local_bk.driver_obj,webdriver.Ie):
                    if (empty_ie_window_handle!=True) and (local_bk.webdriver_list[driver_instance].capabilities['browserName'] == 'internet explorer'):
                        pid=local_bk.webdriver_list[driver_instance].iedriver.process.pid
                        os.system("TASKKILL /F /T /PID " + str(pid))
                        time.sleep(5)
                        local_bk.driver_obj = None
                    # import win32com.client
                    # wmi=win32com.client.GetObject('winmgmts:')
                    # proc=wmi.ExecQuery('select * from Win32_Process where Name="IEDriverServer64.exe"')
                    # if len(proc)>0:
                    #     for i in proc:
                    #         os.system("TASKKILL /F /T /PID " + str(i.ProcessId))
                    #         time.sleep(5)
                else:
                    if(empty_ie_window_handle!=True):
                        local_bk.webdriver_list[driver_instance].quit()
                local_bk.driver_obj = None
                if SYSTEM_OS == 'Darwin':
                    os.system("killall -9 Safari")
                logger.print_on_console('browser closed')
                local_bk.log.info('browser closed')
                ## Issue #190 Driver control won't switch back to parent window
                del drivermap[:]
                del local_bk.webdriver_list[:]
                del local_bk.pid_set[:]
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        else:
            err_msg = 'For this closeBrowser keyword, openBrowser or openNewBrowser keyword is not present'
            logger.print_on_console(err_msg)
            local_bk.log.error(err_msg)
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
        window_num_flag = False
        switch_window_flag = False
        handles_index=[]
        inp=None
        ## Issue #190 Driver control won't switch back to parent window
        err_msg=None
        try:
            if (len(args) > 1):
                if (len(args[1]) == 1 and not(args[1][0].strip().isdigit())):
                    inp = args[1]
                    inp = str(inp[0])
                    inp = inp.lower()
                else:
                    window_num_flag = True
                    inp_list=args[1]
            if len(local_bk.all_handles) > 1:
                if(inp == 'all'):
                    cur_handle=local_bk.driver_obj.current_window_handle
                    remove_handles=[]
                    try:
                        for i in local_bk.all_handles:
                            if i!=cur_handle:
                                local_bk.driver_obj.switch_to.window(i)
                                local_bk.driver_obj.close()
                                remove_handles.append(i)
                        for j in remove_handles:
                            local_bk.all_handles.remove(j)
                        logger.print_on_console('Sub window closed')
                        local_bk.log.info('Sub window closed')
                    except Exception as e:
                        err_msg=self.__web_driver_exception(e)
                elif window_num_flag == True:
                    remove_handles=[]
                    handles_not_found=[]
                    try:
                        cur_handle=local_bk.driver_obj.current_window_handle
                        cwh_index=local_bk.all_handles.index(cur_handle)
                        if len(inp_list)<len(local_bk.all_handles):
                            for i in inp_list:
                                inp = int(i)
                                inp = inp-1
                                if inp<len(local_bk.all_handles):
                                    if not(inp==-1 or i==0):
                                        window_num_flag = True
                                        win_h=local_bk.all_handles[inp]
                                        local_bk.driver_obj.switch_to.window(local_bk.all_handles[inp])
                                        local_bk.driver_obj.close()
                                        remove_handles.append(win_h) 
                                        local_bk.log.info('subwindow '+str(i)+' is closed')
                                        logger.print_on_console('subwindow '+str(i)+' is closed')
                                    else:
                                        local_bk.log.error(webconstants.INVALID_INPUT)
                                        logger.print_on_console(webconstants.INVALID_INPUT)
                                        err_msg = webconstants.INVALID_INPUT
                                        switch_window_flag = False
                                else: 
                                    local_bk.log.info('window handle ' +str(i)+' is not found ')
                                    handles_not_found.append(i)
                                    switch_window_flag = False
                            if len(remove_handles)>=1:
                                for j in remove_handles:   
                                    local_bk.all_handles.remove(j)
                                switch_window_flag = True
                            if len(handles_not_found)>=1:
                                err_msg = 'One or more window handle not found'
                                logger.print_on_console(err_msg)
                                local_bk.log.error(err_msg)
                        else:
                            window_num_flag = False
                            err_msg = "Input has to be one less than the total number of subwindows(tabs)"
                            logger.print_on_console(err_msg)
                            local_bk.log.error(err_msg)
                    except Exception as e:
                        err_msg=self.__web_driver_exception(e)
                elif not (window_num_flag==True or inp == 'all' or inp == ''):
                    local_bk.log.error(webconstants.INVALID_INPUT)
                    logger.print_on_console(webconstants.INVALID_INPUT)
                    err_msg = webconstants.INVALID_INPUT
                else:
                    try:
                        cur_handle=local_bk.driver_obj.current_window_handle
                        cwh_index=local_bk.all_handles.index(cur_handle)
                        local_bk.driver_obj.switch_to.window(local_bk.all_handles[-1])
                        local_bk.driver_obj.close()
                        local_bk.all_handles=local_bk.all_handles[0:-1]
                        logger.print_on_console('Sub window closed')
                        local_bk.log.info('Sub windows closed')
                    except Exception as e:
                        err_msg=self.__web_driver_exception(e)

                if(len(local_bk.all_handles) >= 1):
                    if (window_num_flag == True and switch_window_flag==True):                       
                        if not(cur_handle in local_bk.all_handles):
                            if len(inp_list)>1: 
                                if cwh_index > len(local_bk.all_handles):
                                    local_bk.driver_obj.switch_to.window(local_bk.all_handles[-1])
                                    self.update_recent_handle(local_bk.all_handles[-1])
                                elif cwh_index < len(local_bk.all_handles):
                                    prev_window=cwh_index-len(inp_list)
                                    local_bk.driver_obj.switch_to.window(local_bk.all_handles[prev_window])
                                    self.update_recent_handle(local_bk.all_handles[prev_window])
                                if len(inp_list) == len(remove_handles):
                                    status=webconstants.TEST_RESULT_PASS
                                    result=webconstants.TEST_RESULT_TRUE
                            else:
                                if cwh_index==0:
                                    prev_window=cwh_index
                                    local_bk.driver_obj.switch_to.window(local_bk.all_handles[prev_window])
                                    self.update_recent_handle(local_bk.all_handles[prev_window])
                                    status=webconstants.TEST_RESULT_PASS
                                    result=webconstants.TEST_RESULT_TRUE
                                else: 
                                    prev_window=cwh_index-1
                                    local_bk.driver_obj.switch_to.window(local_bk.all_handles[prev_window])
                                    self.update_recent_handle(local_bk.all_handles[prev_window])
                                    status=webconstants.TEST_RESULT_PASS
                                    result=webconstants.TEST_RESULT_TRUE
                        else:
                            local_bk.driver_obj.switch_to.window(cur_handle)
                            self.update_recent_handle(cur_handle)
                            if len(inp_list)>1:
                                if len(inp_list) == len(remove_handles):
                                    status=webconstants.TEST_RESULT_PASS
                                    result=webconstants.TEST_RESULT_TRUE
                            else:
                                status=webconstants.TEST_RESULT_PASS
                                result=webconstants.TEST_RESULT_TRUE
                    elif (inp == 'all' or inp == ''):
                        if inp == '':
                            if cwh_index == len(local_bk.all_handles):
                                local_bk.driver_obj.switch_to.window(local_bk.all_handles[-1])
                                self.update_recent_handle(local_bk.all_handles[-1])
                                status=webconstants.TEST_RESULT_PASS
                                result=webconstants.TEST_RESULT_TRUE
                            else:
                                local_bk.driver_obj.switch_to.window(cur_handle)
                                self.update_recent_handle(cur_handle)
                                status=webconstants.TEST_RESULT_PASS
                                result=webconstants.TEST_RESULT_TRUE
                        else:        
                            local_bk.driver_obj.switch_to.window(local_bk.all_handles[-1])
                            self.update_recent_handle(local_bk.all_handles[-1])
                            status=webconstants.TEST_RESULT_PASS
                            result=webconstants.TEST_RESULT_TRUE
            else:
                err_msg = 'No sub windows to close'
                logger.print_on_console(err_msg)
                local_bk.log.error(err_msg)

        except Exception as e:
            err_msg=self.__web_driver_exception(e)
            local_bk.driver_obj.switch_to.window(local_bk.all_handles[-1])
        return status,result,output,err_msg

    def clear_cache(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        configvalue=readconfig.configvalues
        try:
            if local_bk.driver_obj != None and isinstance(local_bk.driver_obj,webdriver.Ie) or local_bk.driver_obj.name=='MicrosoftEdge':
                if((str(configvalue['bit_64']).lower())=='yes' and isinstance(local_bk.driver_obj,webdriver.Ie)):
                    import subprocess
                    command = ['RunDll32.exe', 'InetCpl.cpl,ClearMyTracksByProcess', '2']
                    proc = subprocess.run(command)
                    if(proc.returncode==0):
                        status = webconstants.TEST_RESULT_PASS
                        result = webconstants.TEST_RESULT_TRUE
                else:
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
            #clear cache for chrome driver.
            elif local_bk.driver_obj != None and isinstance(local_bk.driver_obj,webdriver.Chrome):
                local_bk.driver_obj.get('chrome://settings/clearBrowserData')
                time.sleep(2)
                local_bk.driver_obj.execute_script('return document.querySelector("body > settings-ui").shadowRoot.querySelector("#container").querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("settings-privacy-page").shadowRoot.querySelector("settings-clear-browsing-data-dialog").shadowRoot.querySelector("#clearBrowsingDataDialog").querySelector("#clearBrowsingDataConfirm").click();')
                logger.print_on_console('Cleared cache')
                local_bk.log.info('Cleared Cache')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            #clear cache for chromium driver.
            elif local_bk.driver_obj != None and local_bk.driver_obj.name=='msedge':
                local_bk.driver_obj.get('edge://settings/clearBrowserData')
                time.sleep(2)
                local_bk.driver_obj.execute_script('return document.getElementById("clear-now").click();')
                logger.print_on_console('Cleared cache')
                local_bk.log.info('Cleared Cache')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            elif local_bk.driver_obj != None and isinstance(local_bk.driver_obj,webdriver.Firefox):
                local_bk.driver_obj.get('about:preferences#privacy')
                time.sleep(2)
                local_bk.driver_obj.find_element_by_css_selector('#clearSiteDataButton').click()
                time.sleep(2)
                if SYSTEM_OS =='Windows' or SYSTEM_OS=='Darwin':
                    local_bk.driver_obj.execute_script("document.getElementsByTagName('browser')[0].contentWindow.document.getElementsByTagName('dialog')[0].shadowRoot.children[3].children[2].click()")
                elif SYSTEM_OS=='Linux':
                    # click on clear button for linux as clear and cancel buttons are positioned differently in linux
                    local_bk.driver_obj.execute_script("document.getElementsByTagName('browser')[0].contentWindow.document.getElementsByTagName('dialog')[0].shadowRoot.children[3].children[6].click()")
                time.sleep(2)
                local_bk.driver_obj.switch_to.alert.accept()
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                err_msg = "This function is not available for "+BROWSER_NAME[self.browser_num]+'.'
                logger.print_on_console(err_msg)
                local_bk.log.error(err_msg)
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,output,err_msg

    def getBrowserName(self, *args):
        global local_bk
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        browsername=None
        err_msg=None
        configvalues = readconfig.configvalues
        try:
            if str(configvalues['headless_mode'])=='Yes':
                browsername = 'Headless'
                logger.print_on_console('Browser Name: ',browsername)
                local_bk.log.info('Browser Name: '+ browsername)
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            elif(local_bk.driver_obj != None):
                browsername = webconstants.BROWSER_NAME_MAP[local_bk.driver_obj.name.strip()]
                logger.print_on_console('Browser Name: ',browsername)
                local_bk.log.info('Browser Name: '+ browsername)
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                err_msg = 'Browser not available'
                logger.print_on_console(err_msg)
                local_bk.log.error(err_msg)
                local_bk.log.error('Driver object is null')
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status,result,browsername,err_msg

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
        if SYSTEM_OS == 'Windows':
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
                if enableSecurityFlag:
                    local_bk.driver_obj = obj.set_security_zones(
                        self.browser_num, local_bk.driver_obj)
                #Logic to get the pid of the ie window
                p = psutil.Process(local_bk.driver_obj.iedriver.process.pid)
                pidie = p.children()[0]
                pid = pidie.pid
                local_bk.pid_set.append(pid)
            elif(self.browser_num == '7'):
                if enableSecurityFlag:
                    local_bk.driver_obj = obj.set_security_zones(
                        self.browser_num, local_bk.driver_obj)
                #Logic to get the pid of the edge window
                p = psutil.Process(local_bk.driver_obj.edge_service.process.pid)
                pidedge = p.children()[0]
                pid = pidedge.pid
                local_bk.pid_set.append(pid)
            elif (self.browser_num == '8'):
                #Logic to get the pid of the edge_chromium window
                p = psutil.Process(local_bk.driver_obj.edge_service.process.pid)
                pidchromium = p.children()[0]
                pid = pidchromium.pid
                local_bk.pid_set.append(pid)
            hwndg = utilobject.bring_Window_Front(pid)

    def switch_to_window(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_bk.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            input=input[0]
            try:
                to_window=int(input)
            except Exception as e:
                to_window = -1
            if not(input is None or input is '' or to_window <0):
                logger.print_on_console(INPUT_IS+input)
                local_bk.log.info('Switching to the window ')
                local_bk.log.info(to_window)
                self.update_window_handles()
                window_handles=self.__get_window_handles()
                ## Issue #190 Driver control won't switch back to parent window
                if to_window>len(window_handles):
                    err_msg='Window '+input+' not found'
                    logger.print_on_console(err_msg)
                    local_bk.log.error(err_msg)
                else:
                    local_bk.log.info('The available window handles are ')
                    local_bk.log.info(window_handles)
                    cur_handle=local_bk.driver_obj.current_window_handle
                    from_window=-1
                    if cur_handle in window_handles:
                        from_window=window_handles.index(cur_handle)+1
                        local_bk.log.info('Switching from the window')
                        local_bk.log.info(from_window)
                    if from_window>-1:
                        local_bk.driver_obj.switch_to.window(window_handles[to_window-1])
                        self.update_recent_handle(window_handles[to_window-1])
                        local_bk.log.info('Switched to window handle '+str(local_bk.driver_obj.current_window_handle))
                        logger.print_on_console('Control switched from window ' + str(from_window)
    							+ " to window " + str(to_window))
                        if isinstance(local_bk.driver_obj,webdriver.Ie):
                            win_name=local_bk.driver_obj.title
                            if win_name == '':
                                win_name=local_bk.driver_obj.current_url
                                if win_name == '':
                                    win_name='Blank Page'
                            hwnd=win32gui.FindWindow(None, win_name+" - Internet Explorer")
                            if hwnd==0:
                                hwnd=win32gui.FindWindow(None, win_name+" - Windows Internet Explorer")
                            win32gui.SetForegroundWindow(hwnd)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg='Current window handle not found'
                        logger.print_on_console(err_msg)
                        local_bk.log.error(err_msg)
            elif (input is None or input is ''):
                window_handles=self.__get_window_handles()
                local_bk.log.info('Current window handles are ')
                local_bk.log.info(window_handles)
                local_bk.log.debug(len(window_handles))
                if len(window_handles)>0:
                    total_handles=len(window_handles)
                    local_bk.driver_obj.switch_to.window(window_handles[total_handles-1])
                    ## Issue #190 Driver control won't switch back to parent window
                    self.update_recent_handle(window_handles[total_handles-1])
                    logger.print_on_console('Control switched to latest window')
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
            else:
                logger.print_on_console(INVALID_INPUT)
                err_msg=INVALID_INPUT
                local_bk.log.error(INVALID_INPUT)
        except Exception as e:
            local_bk.log.error(e)
            local_bk.log.info('Inside Exception block')
            try:
                if isinstance(e,NoSuchWindowException):
                    window_handles=self.__get_window_handles()
                    local_bk.log.info('Current window handles are ')
                    local_bk.log.info(window_handles)
                    local_bk.log.debug(len(window_handles))
                    if len(window_handles)>0:
                        total_handles=len(window_handles)
                        local_bk.driver_obj.switch_to.window(window_handles[total_handles-1])
                        ## Issue #190 Driver control won't switch back to parent window
                        self.update_recent_handle(window_handles[total_handles-1])
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg='No handles found'
                        logger.print_on_console(err_msg)
                        local_bk.log.error(err_msg)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def __get_window_handles(self):
    	## Issue #190 Driver control won't switch back to parent window
        window_handles=local_bk.all_handles
        logger.print_on_console('Window handles size '+str(len(window_handles)))
        return window_handles

    def get_foreground_window(self, *args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None        
        verb = None 
        flag_firefox = False
        try:
            if SYSTEM_OS != 'Darwin':
                if (self.browser_num == '1'):
                    p = psutil.Process(local_bk.driver_obj.service.process.pid)
                    pidchrome = p.children()[-1]
                    pid = pidchrome.pid
                elif(self.browser_num == '2'):
                    if(isinstance(local_bk.driver_obj,webdriver.Firefox)):
                        try:
                            win_name=local_bk.driver_obj.title+' — Mozilla Firefox'
                            if(win32gui.FindWindow(None,win_name)!=0):
                                handle=win32gui.FindWindow(None,win_name)
                                win32gui.ShowWindow(handle,3)
                                win32gui.SetForegroundWindow(handle)
                                flag_firefox = True
                                status=webconstants.TEST_RESULT_PASS
                                result=webconstants.TEST_RESULT_TRUE
                                output = "Browser brought to foreground"
                        except:
                            local_bk.log.info("Unable to bring the window to foreground using the title")
                    if flag_firefox!=True:
                        try:
                            pid = local_bk.driver_obj.binary.process.pid
                        except Exception as e:
                            p = psutil.Process(local_bk.driver_obj.service.process.pid)
                            pidfirefox = p.children()[0]
                            pid = pidfirefox.pid
                elif(self.browser_num == '3'):
                    p = psutil.Process(local_bk.driver_obj.iedriver.process.pid)
                    pidie = p.children()[-1]
                    pid = pidie.pid
                elif(self.browser_num == '7'):
                    try:
                        win_name=local_bk.driver_obj.title
                        
                        if(win32gui.FindWindow(None,win_name)!=0):
                            handle=win32gui.FindWindow(None,win_name)
                            local_bk.driver_obj.minimize_window()
                            local_bk.driver_obj.maximize_window()
                            win32gui.BringWindowToTop(handle)
                            win32gui.ShowWindow(handle,3)
                            win32gui.SetForegroundWindow(handle)
                            status=webconstants.TEST_RESULT_PASS
                            result=webconstants.TEST_RESULT_TRUE
                            verb = "Browser brought to foreground"
                    except:
                        local_bk.log.info("Unable to bring the window to foreground using the title")
                elif (self.browser_num == '8'):
                    p = psutil.Process(local_bk.driver_obj.edge_service.process.pid)
                    pidchromium = p.children()[-1]
                    pid = pidchromium.pid
                elif (self.browser_num == '6'):
                    logger.print_on_console("This feature not support on {} platform".format(SYSTEM_OS))
                    local_bk.log.info("This feature not Supported")
                    
                if flag_firefox!=True:
                    utilobject = utils_web.Utils()
                    utilobject.bring_Window_Front(pid)
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
                    verb = "Browser brought to foreground"
            elif SYSTEM_OS == 'Darwin':
                if (self.browser_num == '6'):
                    local_bk.log.info("This feature not implemented")
                pass
        except Exception as e:
            err_msg = e
            local_bk.log.error( err_msg )
            if err_msg!= None:
                logger.print_on_console( "Browser unavailable" )
            else:
                logger.print_on_console(verb)
        logger.print_on_console(verb)
        return status, result, output, err_msg

    def __open_save_file_dialog(self, pidb):
        hwnds = []
        def winEnumHandler(hwnd, pidx): # get handles/windows of application/browser
            _, current_pid = win32process.GetWindowThreadProcessId(hwnd)
            if win32gui.IsWindowVisible(hwnd) and current_pid == pidx and len(win32gui.GetWindowText(hwnd).strip()) != 0:
                hwnds.append(hwnd)
        win32gui.EnumWindows(winEnumHandler, pidb)
        if len(hwnds) > 0:
            wind_brw = hwnds[0]
            app=Application().connect(handle=wind_brw,allow_magic_lookup=False)
            win=app[win32gui.GetWindowText(wind_brw)]
            win.type_keys('^s') # Send Ctrl+S to open save file dialouge
            time.sleep(1)

    def __get_file_dialog_handle(self, pid, ppid, browser_name, all_hwnds=False):
        hwnds = []
        if (browser_name == 'internet explorer' and 'Windows-10' in platform.platform()): pids = [pid]
        else: pids=[c.pid for c in psutil.Process(pid).children()]
        def winEnumHandler(hwnd, pidx): # get handle of save window
            _, current_pid = win32process.GetWindowThreadProcessId(hwnd)
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) in ["Save Webpage", "Save As", "Confirm Save As", "Error Saving Webpage"]:
                if browser_name == "edge legacy":
                    if psutil.Process(current_pid).name() == "PickerHost.exe":
                        hwnds.append(hwnd)
                elif current_pid in pidx:
                    hwnds.append(hwnd)
        win32gui.EnumWindows(winEnumHandler, pids)
        if all_hwnds: return hwnds
        handle = hwnds[0] if (len(hwnds) > 0) else None
        return handle

    def save_file(self,element,args):
        """
        def : save_file
        purpose : Saving a file in windows
        param : folder_path,file_path,wait_time
        return :

        """
        try:
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            output=OUTPUT_CONSTANT
            local_bk.log.debug('Reading the inputs')
            brute_logic = False
            folder_path=str(args[0]) if len(args) > 0 else None
            file_path=str(args[1]) if len(args) > 1 else None
            local_bk.log.debug('Folder path is '+str(folder_path)+' and File is '+str(file_path))
            if (not(folder_path is None or folder_path == '' or file_path is None or file_path == '') and os.path.exists(folder_path)):
                local_bk.log.debug('Saving the file')
                full_path = os.path.join(folder_path, file_path)
                if SYSTEM_OS=='Windows':
                    pid, ppid, pidb, browser_name = get_pid_ppid_browser()
                    if not ((ppid == None) or (pid == None and browser_name != "edge legacy")):
                        self.__open_save_file_dialog(pidb)
                        def __save_time_func(tries=10, time_sleep=0.5):
                            while tries > 0:
                                win_handle = self.__get_file_dialog_handle(pid, ppid, browser_name)
                                if win_handle is not None:
                                    local_bk.log.info("Window handle found: %s", win_handle)
                                    return win_handle
                                time.sleep(time_sleep)
                                tries -= 1
                            return None

                        maxTries = 10
                        time_sleep = 0.5
                        if len(args) > 2:
                            maxTries = int(int(args[2]) / time_sleep)
                        handle = __save_time_func(maxTries, time_sleep)
                        if handle is None: brute_logic = True
                        else:
                            try:
                                local_bk.log.info("Trying with method 1")
                                app=Application().connect(handle=handle,allow_magic_lookup=False)
                                win=app[win32gui.GetWindowText(handle)]
                                # win.minimize()
                                save_but = None
                                file_box = None
                                w_c = win.children()
                                for c in w_c:
                                    if str(c.friendly_class_name())=="Button" and c.window_text()=="&Save":
                                        save_but = c
                                        break
                                for i in range(len(w_c)):
                                    c = w_c[i]
                                    if (str(c.friendly_class_name())=="Edit" and c.is_visible()
                                    and w_c[i-1].class_name()=="ComboBox"):
                                        file_box = c
                                        break
                                if file_box and save_but:
                                    file_box.set_edit_text(full_path)
                                    time.sleep(0.5)
                                    save_but.set_focus()
                                    save_but.click()
                                    time.sleep(1)
                                    if win32process.GetWindowThreadProcessId(handle)[0] != 0:
                                        local_bk.log.info("Checking if save is clicked")
                                        win_handles = self.__get_file_dialog_handle(pid, ppid, browser_name, all_hwnds=True)
                                        # if len(win_handles) == 1 and ('Windows-7' in platform.platform() or browser_name == "internet explorer"):
                                        if len(win_handles) == 1:
                                            local_bk.log.info("Clicking save again")
                                            try:
                                                save_but.set_focus()
                                                save_but.click()
                                            except: pass
                                            time.sleep(1)
                                    if 'Windows-7' in platform.platform(): time.sleep(1)
                                    if win32process.GetWindowThreadProcessId(handle)[0] != 0:
                                        local_bk.log.info("File already present, trying to overwrite")
                                        win_handles = self.__get_file_dialog_handle(pid, ppid, browser_name, all_hwnds=True)
                                        wind_csa = None
                                        for hw in win_handles:
                                            if win32gui.GetWindowText(hw) == 'Confirm Save As':
                                                wind_csa = hw
                                                break
                                        if wind_csa:
                                            app2=Application().connect(handle=wind_csa,allow_magic_lookup=False)
                                            win2=app2['Confirm Save As']
                                            # win2.minimize()
                                            yes_but = None
                                            w_c = win2.children()
                                            for c in w_c:
                                                if str(c.friendly_class_name())=="Button" and c.window_text()=="&Yes":
                                                    yes_but = c
                                                    break
                                            yes_but.set_focus()
                                            yes_but.click()
                                            time.sleep(1)
                                            if 'Windows-7' in platform.platform(): time.sleep(1)
                                            if win32process.GetWindowThreadProcessId(handle)[0] != 0:
                                                local_bk.log.info("File already present, trying to overwrite with send function keys")
                                                # Added alt+y sendfunction key for automating overwrite process if the file is already existed.
                                                SF().press_multiple_keys(['alt','y'],1)
                                                time.sleep(1)
                                            if win32process.GetWindowThreadProcessId(handle)[0] == 0:
                                                if browser_name == "internet explorer":
                                                    local_bk.log.info("Checking if error popup is present for IE")
                                                    tleft = 6
                                                    while tleft > 0:
                                                        tleft -= 1
                                                        time.sleep(1)
                                                        win_handles = self.__get_file_dialog_handle(pid, ppid, browser_name, all_hwnds=True)
                                                        wind_esw = None
                                                        for hw in win_handles:
                                                            if win32gui.GetWindowText(hw) == 'Error Saving Webpage':
                                                                wind_esw = hw
                                                                tleft = 0
                                                                break
                                                    if wind_esw:
                                                        app2=Application().connect(handle=wind_esw,allow_magic_lookup=False)
                                                        win2=app2['Error Saving Webpage']
                                                        # win2.minimize()
                                                        ok_but = None
                                                        w_c = win2.children()
                                                        for c in w_c:
                                                            if str(c.friendly_class_name())=="Button" and c.window_text()=="&Yes":
                                                                ok_but = c
                                                                break
                                                        ok_but.click()
                                                        time.sleep(1)
                                                    else:
                                                        status=TEST_RESULT_PASS
                                                        methodoutput=TEST_RESULT_TRUE
                                                        local_bk.log.info('File has been saved')
                                                else:
                                                    status=TEST_RESULT_PASS
                                                    methodoutput=TEST_RESULT_TRUE
                                                    local_bk.log.info('File has been saved')
                                        else: brute_logic = True
                                    else:
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                        local_bk.log.info('File has been saved')
                            except Exception as e:
                                err_msg = EXCEPTION_OCCURED + " in method 1"
                                logger.print_on_console(err_msg)
                                local_bk.log.error(err_msg)
                                local_bk.log.error(e)
                                brute_logic = True
                else:
                    emsg = "For non-windows system, use @generic send function keys"
                    logger.print_on_console(emsg)
                    local_bk.log.info(emsg)

                if brute_logic:
                    import file_operations
                    file_obj = file_operations.FileOperations()
                    status,methodoutput,output,err_msg = file_obj.save_file(folder_path,file_path)
            else:
                err_msg='Invalid file path'
        except (IOError,WindowsError):
            err_msg=ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            local_bk.log.error(e)
            err_msg="Error while Saving file"
        if err_msg is not None and not brute_logic:
            local_bk.log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


class Singleton_DriverUtil():

    def check_if_driver_exists_in_map(self,browserType):
        global local_bk, drivermap
        if len(drivermap) == 0: return None
        d = None
        # drivermap.reverse()
        if browserType == '1':
            for i in drivermap:
                if isinstance(i,webdriver.Chrome):
                    try:
                        if len (i.window_handles) > 0:
                            d = i
                    except:
                        d = 'stale'
                        break
        elif browserType == '2':
            for i in drivermap:
                if isinstance(i,webdriver.Firefox):
                    try:
                        if len (i.window_handles) > 0:
                            d = i
                    except:
                        d = 'stale'
                        break
        elif browserType == '3':
            for i in drivermap:
                if isinstance(i,webdriver.Ie):
                    try:
                        if len (i.window_handles) == 0:
                            d = 'stale'
                            break
                        else:
                            d = i
                    except:
                        d = 'stale'
                        break
        elif browserType == '6':
            for i in drivermap:
                if isinstance(i, webdriver.Safari):
                    try:
                        if len(i.window_handles) == 0:
                            d = 'stale'
                            break
                        else:
                            d = i
                    except:
                        d = 'stale'
                        break
        elif browserType == '7':
            for i in drivermap:
                if isinstance(i, webdriver.Edge) and i.name=='MicrosoftEdge':
                    try:
                        if len (i.window_handles) == 0:
                            d = 'stale'
                            break
                        else:
                            d = i
                    except:
                        d = 'stale'
                        break
        elif browserType == '8':
            for i in drivermap:
                if isinstance(i, webdriver.Edge) and i.name=='msedge':
                    try:
                        if len (i.window_handles) == 0:
                            d = 'stale'
                            break
                        else:
                            d = i
                    except:
                        d = 'stale'
                        break
        return d

    def modify_file_as_text(self,text_file_path, text_to_search, replacement_text):
        with fileinput.FileInput(text_file_path, inplace=True, backup='.bak') as file:
            for line in file:
                line.replace(text_to_search, replacement_text)

    def getBrowser(self,browser_num):
        import controller
        global local_bk, drivermap
        del local_bk.recent_handles[:]
        del local_bk.all_handles[:]
        driver=None
        local_bk.log.debug('BROWSER NUM: ')
        local_bk.log.debug(browser_num)
        logger.print_on_console( 'BROWSER NUM: ',str(browser_num))
        configvalues = readconfig.configvalues
        cicd_headless_mode = cicd_core.cicd_isheadless
        if cicd_headless_mode == 'Yes':
            headless_mode = True
        else:
            headless_mode = str(configvalues['headless_mode'])=='Yes'
        use_custom_debugport = str(configvalues["use_custom_debugport"].lower()) == "yes"
        close_browser_popup = configvalues['close_browser_popup']
        incognito_private_mode = configvalues['incognito_private_mode']
        extension_path = configvalues['chrome_extnpath']
        extn_flag=False
        if (browser_num == '1'):
            try:
                chrome_path = configvalues['chrome_path']
                chrome_profile=os.path.normpath(configvalues["chrome_profile"])
                exec_path = webconstants.CHROME_DRIVER_PATH
                # flag1 = self.chrome_version(driver)
                if core.chromeFlag:
                    choptions = webdriver.ChromeOptions()
                    choptions.add_argument('start-maximized')
                    choptions.add_experimental_option('useAutomationExtension', False)
                    choptions.add_experimental_option("excludeSwitches",["enable-automation"])
                    extns=glob.glob(webconstants.EXTENSIONS_PATH+os.sep+"*.crx")
                    if headless_mode:
                        WINDOW_SIZE = "1350,650"
                        choptions.add_argument("--window-size=%s" % WINDOW_SIZE)
                        choptions.headless = True
                    if configvalues['extn_enabled'].lower()=='yes' and os.path.exists(webconstants.AVO_EXTENSION_PATH):
                        choptions.add_extension(webconstants.AVO_EXTENSION_PATH)
                    if extension_path.lower() != 'default':
                        extn=extension_path.split(";")
                        for i in extn:
                            if os.path.isfile(i):
                                if os.path.splitext(i)[-1].lower()=='.crx':
                                    extns.append(i)
                            elif os.path.isdir(i):
                                [extns.append(j) for j in glob.glob(i+os.sep+"*.crx")]
                    if len(extns) > 0:
                        for i in extns:
                            if i != webconstants.AVO_EXTENSION_PATH:
                                choptions.add_extension(os.path.abspath(i))
                                extn_flag=True
                    if extn_flag== False and configvalues['extn_enabled'].lower()=='no':
                        choptions.add_argument('--disable-extensions')
                    if str(chrome_path).lower() != 'default':
                        choptions.binary_location = str(chrome_path)
                    if str(chrome_profile).lower() != 'default':
                        # Don't use the default directory and create profiles for automation inside it,
                        # Create a separate directory for new automation profiles
                        choptions.add_argument("--user-data-dir="+os.path.dirname(chrome_profile))
                        choptions.add_argument("--profile-directory="+os.path.basename(chrome_profile))
                        try:
                            #To remove restore pages popup when chrome starts(* this may change with future chrome versions)
                            self.modify_file_as_text(chrome_profile+ '\\Preferences', '"exit_type":"Crashed"', '"exit_type":"Normal"')
                        except Exception as ex:
                            local_bk.log.error(ex,exc_info=True)
                    if str(close_browser_popup).lower() == 'yes':
                        prefs = {}
                        prefs["credentials_enable_service"] = False
                        prefs["profile.password_manager_enabled"] = False
                        choptions.add_experimental_option("prefs", prefs)
                        choptions.add_argument("--disable-notifications")

                    if str(incognito_private_mode).lower() == 'yes':
                        choptions.add_argument('--incognito')
                    if use_custom_debugport:
                        choptions.add_argument("--remote-debugging-port="+core_utils.find_open_port())

                    driver = webdriver.Chrome(executable_path=exec_path, options=choptions)
                    # driver.navigate().refresh()
                    if extn_flag == True:
                        time.sleep(3)
                        handles=driver.window_handles
                        main_handle=driver.current_window_handle
                        for i in handles:
                            driver.switch_to.window(i)
                            if driver.current_window_handle != main_handle:
                                driver.close()
                                driver.switch_to.window(driver.window_handles[-1])
                    controller.process_ids.append(driver.service.process.pid)
                    drivermap.append(driver)
                    driver.maximize_window()
                    msg = ('Headless ' if headless_mode else '') + 'Chrome browser started'
                    logger.print_on_console(msg)
                    local_bk.log.info(msg)
                else:
                    logger.print_on_console('Chrome browser version not supported')
                    local_bk.log.info('Chrome browser version not supported')
                    driver = None
            except Exception as e:
                local_bk.log.error(e,exc_info=True)
                logger.print_on_console("Requested browser is not available")
                local_bk.log.info('Requested browser is not available')

        elif(browser_num == '2'):
            try:
                exec_path = webconstants.GECKODRIVER_PATH
                if core.firefoxFlag:
                    firefox_options = webdriver.FirefoxOptions()
                    firefox_options.set_preference("useAutomationExtension", False)
                    if headless_mode:
                        firefox_options.headless = True
                    if str(close_browser_popup).lower() == 'yes':
                        firefox_options.set_preference("credentials_enable_service", False)
                    if str(incognito_private_mode).lower() == 'yes':
                        firefox_options.set_preference("browser.privatebrowsing.autostart", True)
                    if str(configvalues['firefox_path']).lower() != "default":
                        from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
                        firefox_options.binary = FirefoxBinary(str(configvalues['firefox_path']))
                    log_path = AVO_ASSURE_HOME + OS_SEP + "output" + OS_SEP +  "geckodriver.log"
                    driver = webdriver.Firefox(executable_path=exec_path, options=firefox_options, service_log_path=log_path)
                    # driver.navigate().refresh()
                    controller.process_ids.append(driver.service.process.pid)
                    drivermap.append(driver)
                    driver.maximize_window()
                    msg = ('Headless ' if headless_mode else '') + 'Firefox browser started'
                    logger.print_on_console(msg)
                    local_bk.log.info(msg)
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
                controller.process_ids.append(driver.iedriver.process.pid)
                # browser_ver=driver.capabilities['version']
                # browser_ver1 = browser_ver.encode('utf-8')
                # browser_ver = int(browser_ver1)
                # if(browser_ver >= int(webconstants.IE_BROWSER_VERSION[0]) and browser_ver <= int(webconstants.IE_BROWSER_VERSION[1])):
                drivermap.append(driver)
                driver.maximize_window()
                logger.print_on_console('IE browser started')
                local_bk.log.info('IE browser started')
                # else:
                #     driver.close()
                #     driver = None
                #     logger.print_on_console("IE browser version not supported")
                #     log.info('IE browser version not supported')
                #     logger.print_on_console("Browser version:",browser_ver)
                #     log.info('Browser version:',browser_ver)
            except Exception as e:
                logger.print_on_console("Requested browser is not available")
                local_bk.log.info('Requested browser is not available')

        elif(browser_num == '4'):
            try:
                driver = webdriver.Opera()
                controller.process_ids.append(driver.service.process.pid)
                drivermap.append(driver)
                logger.print_on_console('Opera browser started')
            except Exception as e:
                logger.print_on_console("Requested browser is not available")
                local_bk.log.info('Requested browser is not available')

        elif(browser_num == '5'):
            try:
                driver = webdriver.PhantomJS(executable_path=webconstants.PHANTOM_DRIVER_PATH)
                controller.process_ids.append(driver.service.process.pid)
                drivermap.append(driver)
                logger.print_on_console('Phantom browser started')
            except Exception as e:
                logger.print_on_console("Requested browser is not available")
                local_bk.log.info('Requested browser is not available')

        elif(browser_num == '6'):
            try:
                driver = webdriver.Safari()
                controller.process_ids.append(driver.service.process.pid)
                driver.maximize_window()
                drivermap.append(driver)

                logger.print_on_console('Safari browser started')
                local_bk.log.info('Safari browser started')

            except Exception as e:
                logger.print_on_console("Requested browser is not available")
                local_bk.log.info('Requested browser is not available')

        elif(browser_num == '7'):
            try:
                if core.edgeFlagComp:
                    if core.edgeFlag:
                        caps = webdriver.DesiredCapabilities.EDGE.copy()
                        bit_64 = configvalues['bit_64']
                        if ((str(bit_64).lower()) == 'no'):
                            edgepath = webconstants.EDGE_DRIVER_PATH
                        else:
                            edgepath = webconstants.EDGE_DRIVER_PATH
                        driver = webdriver.Edge(capabilities=caps,executable_path=edgepath)
                        drivermap.append(driver)
                        driver.maximize_window()
                        logger.print_on_console('Edge Legacy browser started')
                        local_bk.log.info('Edge Legacy browser started')
                    else:
                        logger.print_on_console('Edge Legacy is not supported')
                        local_bk.log.info('Edge Legacy is not supported')
                        driver = None
                else:
                    logger.print_on_console('Edge Legacy browser compatibility check failed')
                    local_bk.log.info('Edge Legacy browser compatibility check failed')
                    driver = None
            except Exception as e:
                logger.print_on_console("Requested browser is not available")
                local_bk.log.info('Requested browser is not available')

        elif(browser_num == '8'):
            try:
                if core.chromiumFlag:
                    extn_flag= False
                    msoptions = webdriver.EdgeChromiumOptions()
                    msoptions.add_argument('start-maximized')
                    msoptions.add_experimental_option('useAutomationExtension', False)
                    msoptions.add_experimental_option("excludeSwitches",["enable-automation"])
                    msoptions.add_experimental_option("excludeSwitches",["disable-sync"])
                    if headless_mode:
                        WINDOW_SIZE = "1350,650"
                        msoptions.add_argument("--window-size=%s" % WINDOW_SIZE)
                        msoptions.headless = True
                    extension_path = configvalues['chrome_extnpath']
                    extns=glob.glob(webconstants.EXTENSIONS_PATH+os.sep+"*.crx")
                    if extension_path.lower() != 'default':
                        extn=extension_path.split(";")
                        for i in extn:
                            if os.path.isfile(i):
                                if os.path.splitext(i)[-1].lower()=='.crx':
                                    extns.append(i)
                            elif os.path.isdir(i):
                                [extns.append(j) for j in glob.glob(i+os.sep+"*.crx")]
                    if len(extns) > 0:
                        for i in extns:
                            if i != webconstants.AVO_EXTENSION_PATH:
                                msoptions.add_extension(os.path.abspath(i))
                                extn_flag=True
                    if extn_flag== False:
                        msoptions.add_argument('--disable-extensions')
                    if str(close_browser_popup).lower() == 'yes':
                        prefs = {}
                        prefs["credentials_enable_service"] = False
                        prefs["profile.password_manager_enabled"] = False
                        msoptions.add_experimental_option("prefs", prefs)
                    if str(incognito_private_mode).lower() == 'yes':
                        msoptions.add_argument("-inprivate")
                    if use_custom_debugport:
                        msoptions.add_argument("--remote-debugging-port="+core_utils.find_open_port())
                    caps = msoptions.to_capabilities()
                    chromium_path = webconstants.EDGE_CHROMIUM_DRIVER_PATH
                    if SYSTEM_OS == "Darwin":
                        caps['platform'] = 'MAC'
                    if SYSTEM_OS=='Linux':
                        caps['platform'] = 'LINUX'
                    driver = webdriver.Edge(capabilities=caps,executable_path=chromium_path)
                    controller.process_ids.append(driver.edge_service.process.pid)
                    drivermap.append(driver)
                    driver.maximize_window()
                    if extn_flag == True:
                        time.sleep(3)
                        handles=driver.window_handles
                        main_handle=driver.current_window_handle
                        for i in handles:
                            driver.switch_to.window(i)
                            if driver.current_window_handle != main_handle:
                                driver.close()
                                driver.switch_to.window(driver.window_handles[-1])
                    msg = ('Headless ' if headless_mode else '') + 'Edge Chromium browser started'
                    logger.print_on_console(msg)
                    local_bk.log.info(msg)
                else:
                    logger.print_on_console('Edge Chromium version is not supported')
                    local_bk.log.info('Edge Chromium version is not supported')
                    driver = None
            except Exception as e:
                logger.print_on_console("Requested browser is not available")
                local_bk.log.info('Requested browser is not available')
        return driver

    def fetch_security_zones(self):
        try:
            import subprocess
            zonevalues = []
            # running the batch file to fetch assigned settings
            p = subprocess.Popen(webconstants.assets_path + "\\regfile.bat",
                                 cwd=webconstants.drivers_path)
            stdout, stderr = p.communicate()
            zonespath = webconstants.assets_path + "\\zones.txt"
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
                    err_msg = 'Error while setting Browsers Security'
                    logger.print_on_console(err_msg)
                    local_bk.log.error(err_msg)
                    local_bk.log.error(internalexcsecuset)
            return local_bk.driver_obj
        except Exception as set_security_zonesexc:
            err_msg = 'Error while updating security zones data'
            logger.print_on_console(err_msg)
            local_bk.log.error(err_msg)
            local_bk.log.error(set_security_zonesexc)

    def chrome_version(self,driver):
        browser_ver = driver.capabilities['version']
        browser_ver1 = browser_ver.encode('utf-8')
        browser_ver = int(browser_ver1[:2])
        local_bk.log.info('Browser version:',str(browser_ver))
        driver_ver = driver.capabilities['chrome']['chromedriverVersion']
        driver_ver1 = driver_ver.encode('utf-8')
        driver_ver = float(driver_ver1[:4])
        local_bk.log.info('Driver version:',str(driver_ver))
        flag1 = 0
        for i in range(0,len(webconstants.CHROME_DRIVER_VERSION)):
            if(driver_ver == float(webconstants.CHROME_DRIVER_VERSION[i][0]) and browser_ver >= int(webconstants.CHROME_DRIVER_VERSION[i][1]) and browser_ver <= int(webconstants.CHROME_DRIVER_VERSION[i][2])):
                flag1 = 1
                break
        local_bk.log.info('Flag:',str(flag1))
        return flag1


def get_pid_ppid_browser():
    pidb=pid=None
    ppid=None
    browser_name = local_bk.driver_obj.capabilities.get('browserName')
    platform_name = local_bk.driver_obj.capabilities.get('platformName')
    if platform_name is None: platform_name = local_bk.driver_obj.capabilities.get('platform')
    try:
        if platform_name.lower() == 'windows':
            if browser_name == 'chrome':
                ppid = local_bk.driver_obj.service.process.pid
            elif browser_name == 'firefox':
                try:
                    ppid = local_bk.driver_obj.binary.process.pid
                except:
                    ppid = local_bk.driver_obj.service.process.pid
            elif browser_name == 'internet explorer':
                ppid = local_bk.driver_obj.iedriver.process.pid
            elif browser_name == 'edge legacy' or browser_name == 'msedge':
                ppid = local_bk.driver_obj.edge_service.process.pid
            cprocs = psutil.Process(ppid).children()
            if len(cprocs) > 0:
                pidb=pid = cprocs[1].pid if cprocs[0].name() == 'conhost.exe' else cprocs[0].pid
            if browser_name == 'firefox':
                pidb = psutil.Process(pid).children()[0].pid
    except Exception as e:
        local_bk.log.debug("Problem while getting the process id: {}".format(e))
    return pid, ppid, pidb, browser_name
