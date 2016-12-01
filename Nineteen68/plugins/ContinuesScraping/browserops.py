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
import utils_cs
import win32gui
import logger
import Exceptions

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
                    util = utils_cs.Utils()
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
            util = utils_cs.Utils()
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
            global browser
            browser = 2
            util = utils_cs.Utils()
            logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG: Opening Chrome browser.....')
            driver = webdriver.Firefox()
            driver.maximize_window()
            logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG:  Navigating to blank page')
            driver.get(domconstants.BLANK_PAGE)
            p = driver.binary.process.pid
            logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG:  Pid is obtained')
            hwndg = util.bring_Window_Front(p)
            logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG:  Using Pid handle is obtained')
            logger.log('FILE: browserops.py , DEF: openFirefoxBrowser() , MSG:  Chrome browser opened successfully')
            status = domconstants.STATUS_SUCCESS
        except Exception as e:
            status = domconstants.STATUS_FAIL
            Exceptions.error(e)
        return status





