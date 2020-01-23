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
        try:
            global driver
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
        global driver, browser
        status=False

    ##        print 'driver:',driver
        browser = browserType
        # if browser_Keywords.driver_pre:
        #     browser_Keywords.local_bk.driver_obj=browser_Keywords.driver_pre
        #     driver = browser_Keywords.local_bk.driver_obj
        #     return True
        d = self.check_if_driver_exists_in_list(browser)
        if d is not None:
            browser_Keywords.local_bk.driver_obj = d
            driver = d
            status=True
        else:
            obj = browser_Keywords.BrowserKeywords()
            s = obj.openBrowser(None,browser)
    ##        print 'status in :',s
    ##        print 'status type',type(s)
            if s[0] == 'Pass':
    ##            global driver_obj
    ##            print 'browserkeywords ::::',browser_Keywords.driver_obj
                driver = browser_Keywords.local_bk.driver_obj
    ##            print 'my driver ::::',driver
                status=True
        return status

    def check_if_driver_exists_in_list(self,browserType):
        d = None
        instance={
            '1':webdriver.Chrome,
            '2':webdriver.Firefox,
            '3':webdriver.Ie,
            '6':webdriver.Safari,
            '7':webdriver.Edge
        }
        if len(browser_Keywords.drivermap) > 0:
            for i in browser_Keywords.drivermap:
                if isinstance(i,instance[browserType]):
                    try:
                        if (browserType == '1') or (browserType == '2'):
                            if len (i.window_handles) > 0:
                                d = i
                        else:
                            if len (i.window_handles) == 0:
                                d = 'stale'
                                break
                            else:
                                d = i
                    except Exception as e:
                        d = 'stale'
                        break
        return d