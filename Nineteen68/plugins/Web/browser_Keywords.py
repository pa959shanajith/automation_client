#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     08-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from selenium import webdriver
import Exceptions
import logger
import webconstants
driver_obj = None
parent_handle=None
webdriver_list = []

import threading
import time

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

    def openBrowser(self,webelement,browser_num,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        self.browser_num=browser_num[0]
        try:
            global driver_obj
            global webdriver_list
            global parent_handle
            driver = Singleton_DriverUtil()
            driver_obj=driver.driver(self.browser_num)
            webdriver_list.append(driver_obj)
            parent_handle = driver_obj.current_window_handle
            logger.print_on_console('Opened browser')
            status=webconstants.TEST_RESULT_PASS
            result=webconstants.TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,result


    def openNewBrowser(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        try:
            global driver_obj
            global webdriver_list
            driver = Singleton_DriverUtil()
            driver_obj=driver.driver(self.browser_num)
            webdriver_list.append(driver_obj)
            parent_handle = driver_obj.current_window_handle
            logger.print_on_console('Opened new browser')
            status=webconstants.TEST_RESULT_PASS
            result=webconstants.TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,result

    def refresh(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        try:
            if(driver_obj != None):
                driver_obj.refresh()
                logger.print_on_console('Browser refreshed')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,result


    def navigateToURL(self ,webelement, url , *args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        try:
            url = url[0]
            if not (url is None and url is ''):
            	url.strip()
                driver_obj.get(url)
                logger.print_on_console('Navigated to URL')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console(webconstants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,result

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
            Exceptions.error(e)
        return



    def navigate_with_authenticate(self ,webelement, url , *args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
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
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Authentication popup not found')
            else:
                logger.print_on_console(webconstants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,result


    def getPageTitle(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        page_title = None
        try:
            if (driver_obj!= None):
                page_title= driver_obj.title
                if (page_title is ''):
                    page_title= driver_obj.current_url
                page_title.strip()
                logger.print_on_console('Page title is ',page_title)
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
        except Exception as e:
            Exceptions.error(e)
        return status,result,page_title

    def verify_page_title(self,webelement,input_val,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        try:
            if (driver_obj!= None):
                page_title= driver_obj.title
                if (page_title is ''):
                    page_title= driver_obj.current_url
                page_title.strip()
                if(page_title == input_val[0]):
                    logger.print_on_console('Page title is ',page_title)
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
        except Exception as e:
            Exceptions.error(e)
        return status,result


    def getCurrentURL(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        try:
            if (driver_obj!= None):
                url= driver_obj.current_url
                url.strip()
                logger.print_on_console(url)
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
        except Exception as e:
            Exceptions.error(e)
        return status,result,url

    def verifyCurrentURL(self ,webelement, input_url,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        try:
            if not (input_url is None and input_url is ''):
                url= driver_obj.current_url
                url.strip()
                input_url=input_url[0].strip()
                if (url == input_url):
                    logger.print_on_console('verified current url')
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console(webconstants.INVALID_INPUT)

        except Exception as e:
            Exceptions.error(e)
        return status,result


    def closeBrowser(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
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
                webdriver_list[driver_instance].close()
                logger.print_on_console('browser closed')
                if(len(winHandles) > 1):
                    webdriver_list[driver_instance].switch_to.window(winHandles[count])
                if(len(winHandles) == 1):
                    webdriver_list.pop(len(webdriver_list)-1)
                    print 'Kill driver logic'
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE

            except Exception as e:
                Exceptions.error(e)
        else:
            logger.print_on_console('For this close browser open browser or open new browser is not present')
        return status,result


    def maximizeBrowser(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        try:
            if(driver_obj!= None):
                driver_obj.maximize_window()
                logger.print_on_console('browser maximized')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Driver object is null')
        except Exception as e:
            Exceptions.error(e)
        return status,result

    def closeSubWindows(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        try:
            winHandles = driver_obj.window_handles
            winHandles = driver_obj.window_handles
            for x in winHandles:
                if(not(parent_handle == x)):
                    try:
                        driver_obj.switch_to.window(parent_handle)
                        driver_obj.switch_to.window(x)
                        driver_obj.close()
                        logger.print_on_console('Closed sub windows')
                    except Exception as e:
                        Exceptions.error(e)
            after_close = driver_obj.window_handles
            after_close = driver_obj.window_handles
            if(len(after_close) == 1):
                driver_obj.switch_to.window(parent_handle)
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE

        except Exception as e:
            Exceptions.error(e)
            driver_obj.switch_to.window(parent_handle)
        return status,result

    def clear_cache(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        try:
            if driver_obj != None and isinstance(driver_obj,webdriver.Ie):
                #get all the cookies
                cookies=driver_obj.get_cookies()
                if len(cookies)>0:
                    cookies_list=[]
                    for x in cookies:
                        cookies_list.append(x['name'])
                    logger.print_on_console('Cookies are ',cookies_list)
                    #delete_all_cookies()
                    driver_obj.delete_all_cookies()

                else:
                    logger.print_on_console('No Cookies found')
            else:
				 logger.print_on_console("This feature is available only for Internet Explorer.")
        except Exception as e:
            Exceptions.error(e)

        return status,result


class Singleton_DriverUtil():
    def driver(self,browser_num):
        driver=None
        print 'BROWSER NUM',browser_num
        if (browser_num == '1'):
            choptions = webdriver.ChromeOptions()
            choptions.add_argument('start-maximized')
            choptions.add_argument('--disable-extensions')
            driver = webdriver.Chrome(chrome_options=choptions, executable_path=webconstants.CHROME_DRIVER_PATH)
            logger.print_on_console('Chrome browser started')

        elif(browser_num == '2'):
            driver = webdriver.Firefox()
            driver.maximize_window()
            logger.print_on_console('Firefox browser started')

        elif(browser_num == '3'):
            caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
            caps['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS'] = True
            caps['ignoreProtectedModeSettings'] = True
            caps['IE_ENSURE_CLEAN_SESSION'] = True
            caps['ignoreZoomSetting'] = True
            caps['NATIVE_EVENTS'] = True
            driver = webdriver.Ie(capabilities=caps,executable_path=webconstants.IE_DRIVER_PATH_64)
            logger.print_on_console('IE browser started')

        elif(browser_num == '4'):
            driver = webdriver.Opera()
            logger.print_on_console('Opera browser started')

        elif(browser_num == '5'):
            driver = webdriver.Safari()
            logger.print_on_console('Safari browser started')
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