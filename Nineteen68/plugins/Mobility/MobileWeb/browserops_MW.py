#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pavan.nayak
#
# Created:     29-11-2016
# Copyright:   (c) pavan.nayak 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import platform
##import psutil
##import win32process
##import xml.etree.ElementTree as ET
import domconstants_MW
##import utils
##import win32gui
import logger
import Exceptions_MW
import mobile_server_utilities
import webconstants_MW
import mobile_key_objects
##xtree = ET.parse(domconstants_MW.CONFIG_FILE)
##xroot = xtree.getroot()
hwndg = None
status = ''
driver = None
browser = 0
class BrowserOperations():
    """
    ___init__ def
    """
    def __init__(self):
       logger.log( '------------Opening the browser ------------')
       self.status = ''
##        self.xtree = ET.parse(domconstants_MW.CONFIG_FILE)
##        self.xroot = xtree.getroot()
    """
    def: openBrowser
    param : Browser name such as CH - Chrome, IE - Internet Explorer, ANDROID - Android Chrome, and FX - Firefox
    """

    def start_server(self):
        try:
            import subprocess
            import os
##            maindir = os.getcwd()
##            os.chdir('..')
            curdir = os.environ["NINETEEN68_HOME"]
            path= curdir + '\\Nineteen68\\plugins\\Mobility\\MobileApp\\node_modules\\appium\\build\\lib\\main.js'
            nodePath = os.environ["NINETEEN68_HOME"] + "\\Drivers"+'\\node.exe'
            proc = subprocess.Popen([nodePath, path], shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
            import time
            time.sleep(15)
            logger.print_on_console('Server started')
        except Exception as e:
            logger.print_on_console('Exception in starting server')


    def stop_server(self):
            try:
                import psutil
                import os
                processes = psutil.net_connections()
                for line in processes:
                    p =  line.laddr
                    if p[1] == 4723:
                        os.system("TASKKILL /F /PID " + str(line.pid))
                        logger.print_on_console('Server stopped')
            except Exception as e:
                logger.print_on_console('Exception in stopping server')

    def closeandroidBrowser(self  , *args):
         mobile_server_utilities.cleardata()
         status=webconstants_MW.TEST_RESULT_FAIL
         result=webconstants_MW.TEST_RESULT_FALSE
         value=''
         try:

            if( driver!= None):

                driver.close()

                logger.log('chrome browser closed')
                status=webconstants_MW.TEST_RESULT_PASS
                result=webconstants_MW.TEST_RESULT_TRUE
            else:
                mobile_key_objects.custom_msg.append("ERR_WEB_DRIVER_EXCEPTION")
         except Exception as e:
            mobile_key_objects.custom_msg.append("ERR_WEB_DRIVER")

         mobile_key_objects.keyword_output.append(str(status))
         mobile_key_objects.keyword_output.append(str(value))

    def openBrowser(self,inputs):
       try:
           if platform.system() == "Darwin":
               global driver
               input_list = inputs.split(';')
               time.sleep(5)
               desired_caps = {}
               desired_caps['platformName'] = 'iOS'
               desired_caps['platformVersion'] =input_list[1]
               desired_caps['deviceName'] = input_list[0]
               ##desired_caps['udid'] = input_list[0]
               desired_caps['browserName'] = 'Safari'
               ##desired_caps['appium-version'] = '1.4.0'
               desired_caps['fullReset'] = False
               desired_caps['newCommandTimeout'] = 3600
               desired_caps['launchTimeout'] = 180000
               driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

               logger.log('FILE: browserops_MW.py , DEF: openSafariBrowser() , MSG:  Navigating to blank page')
               driver.get(domconstants_MW.BLANK_PAGE)
               ##            p = psutil.Process(driver.service.process.pid)
               ##            # logging.warning(p.get_children(recursive=True))
               ##            pidchrome = p.children()[0]
               ##            logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Pid is obtained')
               ##            # logging.warning(pidchrome.pid)
               ##            global hwndg
               ##            hwndg = util.bring_Window_Front(pidchrome.pid)
               ##            logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Using Pid handle is obtained')
               logger.log(
                   'FILE: browserops_MW.py , DEF: openSafariBrowser() , MSG:  Safari browser opened successfully')
               status = domconstants_MW.STATUS_SUCCESS
           else:
                global driver
                self.start_server()
                input_list = inputs.split(';')
                time.sleep(5)
                desired_caps = {}
                desired_caps['platformName'] = 'Android'
                ##desired_caps['platformVersion'] =input_list[1]
                desired_caps['deviceName'] = input_list[0]
                desired_caps['udid'] = input_list[0]
                desired_caps['browserName'] = 'Chrome'
                ##desired_caps['appium-version'] = '1.4.0'
                desired_caps['newCommandTimeout'] = '36000'
                driver= webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
                logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Navigating to blank page')
                driver.get(domconstants_MW.BLANK_PAGE)
        ##            p = psutil.Process(driver.service.process.pid)
        ##            # logging.warning(p.get_children(recursive=True))
        ##            pidchrome = p.children()[0]
        ##            logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Pid is obtained')
        ##            # logging.warning(pidchrome.pid)
        ##            global hwndg
        ##            hwndg = util.bring_Window_Front(pidchrome.pid)
        ##            logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Using Pid handle is obtained')
                logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Chrome browser opened successfully')
                status = domconstants_MW.STATUS_SUCCESS
       except Exception as e:
            mobile_key_objects.custom_msg.append("ERR_WEB_DRIVER")
            status = domconstants_MW.STATUS_FAIL
            Exceptions_MW.error(e)
       return status
##    def openIeBrowser(self):
##        logger.log('FILE: browserops_MW.py , DEF: openIeBrowser() , MSG: Reading config.xml file.....')
##        for child in xroot:
##            if(child.tag == domconstants_MW.BIT_64):
##                try:
##                    global browser
##                    browser = 3
##                    util = utils.Utils()
##                    caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
##                    caps['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS'] = True
##                    caps['ignoreProtectedModeSettings'] = True
##                    caps['IE_ENSURE_CLEAN_SESSION'] = True
##                    caps['ignoreZoomSetting'] = True
##                    caps['NATIVE_EVENTS'] = True
##                    logger.log('FILE: browserops_MW.py , DEF: openIeBrowser() , MSG:  IE capabilities are added.....')
##                    if(child.text == domconstants_MW.YES):
##                        logger.log('FILE: browserops_MW.py , DEF: openIeBrowser() , MSG: Opening IE browser.....')
##                        global driver
##                        driver = webdriver.Ie(capabilities=caps, executable_path=domconstants_MW.IEDRIVER_BIT64)
##                    else:
##                        logger.log('FILE: browserops_MW.py , DEF: openIeBrowser() , MSG: Opening IE browser.....')
##                        global driver
##                        driver = webdriver.Ie(capabilities=caps, executable_path=domconstants_MW.IEDRIVER_BIT32)
##                    logger.log('FILE: browserops_MW.py , DEF: openIeBrowser() , MSG:  Navigating to blank page')
##                    driver.get(domconstants_MW.BLANK_PAGE)
##                    p = psutil.Process(driver.iedriver.process.pid)
##                    pidie = p.children()[0]
##                    logger.log('FILE: browserops_MW.py , DEF: openIeBrowser() , MSG:  Pid is obtained')
##                    global hwndg
##                    hwndg = util.bring_Window_Front(pidie.pid)
##                    logger.log('FILE: browserops_MW.py , DEF: openIeBrowser() , MSG:  Using Pid handle is obtained')
##                    logger.log('FILE: browserops_MW.py , DEF: openIeBrowser() , MSG:  IE browser opened successfully')
##                    status = domconstants_MW.STATUS_SUCCESS
##                except Exception as e:
##                    Exceptions_MW.error(e)
##        return status
##        """
##        def: openChromeBrowser
##        param : Browser name  CHE - Google Chrome
##        """
##    def openChromeBrowser(self):
##        try:
##            global browser
##            browser = 1
##            util = utils.Utils()
##            choptions = webdriver.ChromeOptions()
##            choptions.add_argument('start-maximized')
##            logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG: Reading config.xml file.....')
##            for child in xroot:
##                if(child.tag == domconstants_MW.CHROME_PATH):
##                    if(child.text == domconstants_MW.DEFAULT):
##                        logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG: Opening Chrome browser.....')
##                        global driver
##                        driver = webdriver.Chrome(chrome_options=choptions, executable_path=domconstants_MW.CHROMEDRIVER)
##                    else:
##                        choptions.binary_location = child.text
##                        logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG: Opening Chrome browser.....')
##                        global driver
##                        driver = webdriver.Chrome(chrome_options=choptions, executable_path=domconstants_MW.CHROMEDRIVER)
##            logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Navigating to blank page')
##            driver.get(domconstants_MW.BLANK_PAGE)
##            p = psutil.Process(driver.service.process.pid)
##            # logging.warning(p.get_children(recursive=True))
##            pidchrome = p.children()[0]
##            logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Pid is obtained')
##            # logging.warning(pidchrome.pid)
##            global hwndg
##            hwndg = util.bring_Window_Front(pidchrome.pid)
##            logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Using Pid handle is obtained')
##            logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Chrome browser opened successfully')
##            status = domconstants_MW.STATUS_SUCCESS
##        except Exception as e:
##            status = domconstants_MW.STATUS_FAIL
##            Exceptions_MW.error(e)
##        return status
##    """
##    def: openFirefoxBrowser
##    param : Browser name  FX - Mozilla Firefox
##    def
##    """
##    def openFirefoxBrowser(self):
##        try:
##            global browser
##            browser = 2
##            util = utils.Utils()
##            logger.log('FILE: browserops_MW.py , DEF: openFirefoxBrowser() , MSG: Opening Chrome browser.....')
##            driver = webdriver.Firefox()
##            driver.maximize_window()
##            logger.log('FILE: browserops_MW.py , DEF: openFirefoxBrowser() , MSG:  Navigating to blank page')
##            driver.get(domconstants_MW.BLANK_PAGE)
##            p = driver.binary.process.pid
##            logger.log('FILE: browserops_MW.py , DEF: openFirefoxBrowser() , MSG:  Pid is obtained')
##            hwndg = util.bring_Window_Front(p)
##            logger.log('FILE: browserops_MW.py , DEF: openFirefoxBrowser() , MSG:  Using Pid handle is obtained')
##            logger.log('FILE: browserops_MW.py , DEF: openFirefoxBrowser() , MSG:  Chrome browser opened successfully')
##            status = domconstants_MW.STATUS_SUCCESS
##        except Exception as e:
##            status = domconstants_MW.STATUS_FAIL
##            Exceptions_MW.error(e)
##        return status

   # def openAndroidChromeBrowser(self):
##        try:
##            desired_caps = {}
##            desired_caps['platformName'] = 'Android'
##            desired_caps['platformVersion'] = '5.1.1'
##            desired_caps['deviceName'] = 'F7AZFG04V017'
##            desired_caps['browserName'] = 'Chrome'
##            desired_caps['appium-version'] = '1.4.0'
##            desired_caps['newCommandTimeout'] = '36000'
##            driver= webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
##            global driver
##            logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Navigating to blank page')
##            driver.get(domconstants_MW.BLANK_PAGE)
####            p = psutil.Process(driver.service.process.pid)
####            # logging.warning(p.get_children(recursive=True))
####            pidchrome = p.children()[0]
####            logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Pid is obtained')
####            # logging.warning(pidchrome.pid)
####            global hwndg
####            hwndg = util.bring_Window_Front(pidchrome.pid)
####            logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Using Pid handle is obtained')
##            logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Chrome browser opened successfully')
##            status = domconstants_MW.STATUS_SUCCESS
##        except Exception as e:
##            status = domconstants_MW.STATUS_FAIL
##            Exceptions_MW.error(e)
##        return status
