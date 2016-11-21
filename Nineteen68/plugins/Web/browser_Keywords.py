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
            logger.log('Opened browser')
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
            logger.log('Opened new browser')
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
                logger.log('Browser refreshed')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,result


    def navigateToURL(self ,webelement, url , *args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        try:
            if not (url is None and url is ''):
                url = url[0]
                url.strip()
                driver_obj.get(url)
                logger.log('Navigated to URL')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.log(webconstants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,result

    def getPageTitle(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        try:
            if (driver_obj!= None):
                page_title= driver_obj.title
                if (page_title is ''):
                    page_title= driver_obj.current_url
                page_title.strip()
                logger.log(page_title)
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.log('Driver object is null')
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
                        logger.log(page_title)
                        logger.log(input_val[0])
                        status=webconstants.TEST_RESULT_PASS
                        result=webconstants.TEST_RESULT_TRUE
            else:
                logger.log('Driver object is null')
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
                logger.log(url)
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.log('Driver object is null')
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
                    logger.log('verified current url')
                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
            else:
                logger.log(webconstants.INVALID_INPUT)

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
                logger.log('browser closed')
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
            logger.log('For this close browser open browser or open new browser is not present')
        return status,result


    def maximizeBrowser(self,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        try:
            if(driver_obj!= None):
                driver_obj.maximize_window()
                logger.log('browser maximized')
                status=webconstants.TEST_RESULT_PASS
                result=webconstants.TEST_RESULT_TRUE
            else:
                logger.log('Driver object is null')
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
                        logger.log('Closed sub windows')
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


class Singleton_DriverUtil():
    def driver(self,browser_num):
        driver=None
        print 'BROWSER NUM',browser_num
        if (browser_num == '1'):
            choptions = webdriver.ChromeOptions()
            choptions.add_argument('start-maximized')
            choptions.add_argument('--disable-extensions')
            import os
            driver = webdriver.Chrome(chrome_options=choptions, executable_path=webconstants.CHROME_DRIVER_PATH)
            logger.log('Chrome browser started')

        elif(browser_num == '2'):
            driver = webdriver.Firefox()
            driver = webdriver.Firefox()
            logger.log('Firefox browser started')

        elif(browser_num == '3'):
            caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
            caps['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS'] = True
            caps['ignoreProtectedModeSettings'] = True
            caps['IE_ENSURE_CLEAN_SESSION'] = True
            caps['ignoreZoomSetting'] = True
            caps['NATIVE_EVENTS'] = True
            driver = webdriver.Ie(capabilities=caps,executable_path=webconstants.IE_DRIVER_PATH_64)
            logger.log('IE browser started')

        elif(browser_num == '4'):
            driver = webdriver.Opera()
            logger.log('Opera browser started')

        elif(browser_num == '5'):
            driver = webdriver.Safari()
            logger.log('Safari browser started')
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