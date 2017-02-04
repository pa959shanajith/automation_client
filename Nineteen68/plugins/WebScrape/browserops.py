#-------------------------------------------------------------------------------
# Name:        browserops.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     28-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import psutil
import win32process
import xml.etree.ElementTree as ET
import domconstants
import utils_sc
import win32gui
import win32api
import logger
import Exceptions
import re
import os

xtree = ET.parse(domconstants.CONFIG_FILE)
xroot = xtree.getroot()
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
##        self.status = ''
##        self.xtree = ET.parse(domconstants.CONFIG_FILE)
##        self.xroot = xtree.getroot()


    """
    def: openBrowser
    param : Browser name such as CH - Chrome, IE - Internet Explorer and FX - Firefox
    """
    def openBrowser(self,browserType):
        options = {
                "IE" : BrowserOperations.openIeBrowser,
                "CH" : BrowserOperations.openChromeBrowser,
                "FX" : BrowserOperations.openFirefoxBrowser,
            }
        return options[browserType](self)

    """
    def: openIeBrowser
    param : Browser name  IE - Internet Explorer
    """
    def openIeBrowser(self):
        logger.log('FILE: browserops.py , DEF: openIeBrowser() , MSG: Reading config.xml file.....')
        for child in xroot:
            if(child.tag == domconstants.BIT_64):
                try:
                    global browser
                    browser = 3
                    util = utils_sc.Utils()
                    caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
                    caps['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS'] = True
                    caps['ignoreProtectedModeSettings'] = True
                    caps['IE_ENSURE_CLEAN_SESSION'] = True
                    caps['ignoreZoomSetting'] = True
                    caps['NATIVE_EVENTS'] = True
                    logger.log('FILE: browserops.py , DEF: openIeBrowser() , MSG:  IE capabilities are added.....')
                    if(child.text == domconstants.YES):
                        logger.log('FILE: browserops.py , DEF: openIeBrowser() , MSG: Opening IE browser.....')
                        global driver
                        driver = webdriver.Ie(capabilities=caps, executable_path=domconstants.IEDRIVER_BIT64)
                    else:
                        logger.log('FILE: browserops.py , DEF: openIeBrowser() , MSG: Opening IE browser.....')
                        global driver
                        driver = webdriver.Ie(capabilities=caps, executable_path=domconstants.IEDRIVER_BIT32)
                    logger.log('FILE: browserops.py , DEF: openIeBrowser() , MSG:  Navigating to blank page')
                    driver.get(domconstants.BLANK_PAGE)
                    p = psutil.Process(driver.iedriver.process.pid)
                    pidie = p.children()[0]
                    logger.log('FILE: browserops.py , DEF: openIeBrowser() , MSG:  Pid is obtained')
                    global hwndg
                    hwndg = util.bring_Window_Front(pidie.pid)
                    logger.log('FILE: browserops.py , DEF: openIeBrowser() , MSG:  Using Pid handle is obtained')
                    logger.log('FILE: browserops.py , DEF: openIeBrowser() , MSG:  IE browser opened successfully')
                    status = domconstants.STATUS_SUCCESS
                except Exception as e:
                    Exceptions.error(e)
        return status

        """
        def: openChromeBrowser
        param : Browser name  CHE - Google Chrome
        """
    def openChromeBrowser(self):
        try:
            global browser
            browser = 1
            util = utils_sc.Utils()
            choptions = webdriver.ChromeOptions()
            choptions.add_argument('start-maximized')
            logger.log('FILE: browserops.py , DEF: openChromeBrowser() , MSG: Reading config.xml file.....')
            for child in xroot:
                if(child.tag == domconstants.CHROME_PATH):
                    if(child.text == domconstants.DEFAULT):
                        logger.log('FILE: browserops.py , DEF: openChromeBrowser() , MSG: Opening Chrome browser.....')
                        global driver
                        driver = webdriver.Chrome(chrome_options=choptions, executable_path=domconstants.CHROMEDRIVER)
                    else:
                        choptions.binary_location = child.text
                        logger.log('FILE: browserops.py , DEF: openChromeBrowser() , MSG: Opening Chrome browser.....')
                        global driver
                        driver = webdriver.Chrome(chrome_options=choptions, executable_path=domconstants.CHROMEDRIVER)
            logger.log('FILE: browserops.py , DEF: openChromeBrowser() , MSG:  Navigating to blank page')
            driver.get(domconstants.BLANK_PAGE)
            p = psutil.Process(driver.service.process.pid)
            # logging.warning(p.get_children(recursive=True))
            pidchrome = p.children()[0]
            logger.log('FILE: browserops.py , DEF: openChromeBrowser() , MSG:  Pid is obtained')
            # logging.warning(pidchrome.pid)
            global hwndg
            hwndg = util.bring_Window_Front(pidchrome.pid)
            logger.log('FILE: browserops.py , DEF: openChromeBrowser() , MSG:  Using Pid handle is obtained')
            logger.log('FILE: browserops.py , DEF: openChromeBrowser() , MSG:  Chrome browser opened successfully')
            status = domconstants.STATUS_SUCCESS
        except Exception as e:
            status = domconstants.STATUS_FAIL
            Exceptions.error(e)
        return status

    """
    def: openFirefoxBrowser
    param : Browser name  FX - Mozilla Firefox
    def
    """
    def openFirefoxBrowser(self):
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
                global driver
                logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG: Opening Firefox browser.....')
                driver = webdriver.Firefox()
                driver.maximize_window()
                driver.get('about:blank')
                parent_win_hwnd = driver.current_window_handle
                p = driver.binary.process.pid
##                hwndg = bring_Window_Front(p)
                #logging.warning('Opening FX')
                logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG:  Firefox browser opened successfully')
                status = domconstants.STATUS_SUCCESS
             # opening firefox browser through geckodriver if the version is 48 and above
            else:
                geckodriver = True
                caps=webdriver.DesiredCapabilities.FIREFOX
                caps['marionette'] = True
                profile= webdriver.FirefoxProfile()
                profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")
                logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG: Opening Firefox browser.....')
                global driver
                driver = webdriver.Firefox(firefox_profile=profile,capabilities=caps,executable_path='geckodriver.exe')
                driver.maximize_window()
                parent_win_hwnd = driver.current_window_handle
                p = psutil.Process(driver.service.process.pid)
                pidfirefox = p.children()[0]
##                hwndg = bring_Window_Front(pidfirefox.pid)
                #logging.warning('Opening FX')
                logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG:  Firefox browser opened successfully')
                status = domconstants.STATUS_SUCCESS
##            global browser
##            browser = 2
##            util = utils_sc.Utils()
##            logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG: Opening Firefox browser.....')
##            global driver
##            driver = webdriver.Firefox()
##            driver.maximize_window()
##            logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG:  Navigating to blank page')
##            driver.get(domconstants.BLANK_PAGE)
##            p = driver.binary.process.pid
##            logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG:  Pid is obtained')
##            hwndg = util.bring_Window_Front(p)
##            logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG:  Using Pid handle is obtained')
##            logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG:  Firefox browser opened successfully')
##            status = domconstants.STATUS_SUCCESS
        except Exception as e:
            status = domconstants.STATUS_FAIL
            Exceptions.error(e)
        return status





