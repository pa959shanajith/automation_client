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

import xml.etree.ElementTree as ET
import domconstants
from constants import SYSTEM_OS
if SYSTEM_OS!='Darwin':
    import utils_sc
    import win32gui
    import win32api
import logger
import Exceptions
import logging
import re
import os
log = logging.getLogger('browserops.py')
##xtree = ET.parse(domconstants.CONFIG_FILE)
##xroot = xtree.getroot()
hwndg = None
status = ''
driver = None
browser = 0
import browser_Keywords
class BrowserOperations():
    """
    ___init__ def
    """
    def __init__(self):
       log.info( '------------Opening the browser ------------')
##        self.status = ''
##        self.xtree = ET.parse(domconstants.CONFIG_FILE)
##        self.xroot = xtree.getroot()


    """
    def: checkPopups
    param : None
    """
    def checkPopups(self):
        global driver
        try:
            alertObj=driver.switch_to_alert()
            alertObj.accept()
            logger.print_on_console('Popup Found!\nPopup accepted.')
            log.info('Popup Found and accepted')
        except:
            log.info('No popup found')
        try:
            win_handles=driver.window_handles
            if len(win_handles)>0:
                driver.switch_to_window(win_handles[-1])
        except:
            log.info('Error while switching to any window handle')

    """
    def: openBrowser
    param : Browser name such as CH - Chrome, IE - Internet Explorer and FX - Firefox
    """
    def openBrowser(self,browserType):
        global driver
        global browser
        status=False


##        print 'driver:',driver
        browser = browserType
        obj = browser_Keywords.BrowserKeywords()
        s = obj.openBrowser(None,browserType)

##        print 'status in :',s
##        print 'status type',type(s)


        if s[0] == 'Pass':
##            global driver_obj
##            print 'browserkeywords ::::',browser_Keywords.driver_obj
            driver = browser_Keywords.driver_obj
##            print 'my driver ::::',driver
            status=True
        return status

