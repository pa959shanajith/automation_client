#-------------------------------------------------------------------------------
# Name:        highlight_MW.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     29-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import domconstants_MW
import clickandadd_MW
import time
# import browserops
import browser_Keywords_MW
import fullscrape_MW
from selenium import webdriver
import logger
import logging
status =domconstants_MW.STATUS_FAIL
from core_utils import CoreUtils
log = logging.getLogger(__name__)
from webscrape_utils_MW import WebScrape_Utils

class Highlight():
    coreutilsobj = CoreUtils()
    webscrapeutilsobj = WebScrape_Utils()

    def __init__(self):
        # self.driver = browserops.driver
        self.driver = browser_Keywords_MW.driver_obj
        self.currenthandle = None

    def perform_highlight(self,elementxpath,elementurl):
        try:
            status = domconstants_MW.STATUS_FAIL
            log.info('Inside perform_highlight method')

            # Find the current handle
            self.currenthandle = clickandadd_MW.currenthandle
            if self.currenthandle is '' or self.currenthandle is None:
                self.currenthandle = fullscrape_MW.currenthandle
            if self.currenthandle is '' or self.currenthandle is None:
                javascript_hasfocus = """return(document.hasFocus());"""
                for eachdriverhand in self.driver.window_handles:
                    log.info( 'Iterating through the number of windows open by the driver')
                    self.driver.switch_to.window(eachdriverhand)
                    log.info( 'Switching to each handle and checking weather it has focus ')
                    time.sleep(3)
                    if (self.driver.execute_script(javascript_hasfocus)):
                            log.info( 'Got the window which has the focus')
                            self.currenthandle = eachdriverhand

            # Switch to current handle and further to outer page
            if self.currenthandle != None:
                self.driver.switch_to.window(self.currenthandle)
            self.driver.switch_to.default_content()

            # XPath and URL decryption logic implemented
            xpath_string = elementxpath.split(';')
            if len(xpath_string) == 3:
                left_part = self.coreutilsobj.scrape_unwrap(xpath_string[0])
                right_part = self.coreutilsobj.scrape_unwrap(xpath_string[2])
            else:
                left_part = str(xpath_string[0])
                right_part = ';'.join(map(str,xpath_string[2:]))
            decryptedxpath = left_part + ';' + xpath_string[1] + ';' + right_part
            decryptedelementurl = self.coreutilsobj.scrape_unwrap(elementurl)
            identifiers = decryptedxpath.split(';')

            # If the element URL is of frame/iframe, switch to that
            if self.webscrapeutilsobj.is_iframe_frame_url(decryptedelementurl):
                self.webscrapeutilsobj.switchtoframe_webscrape(self.driver, self.currenthandle, decryptedelementurl)

            # Locate the webelement
            webElement = self.webscrapeutilsobj.locate_webelement(self.driver, identifiers)

            # If found, Highlight the element
            if webElement is not None:

                webElement = webElement[0]
                # Store the original style for reverting the element back
                original_style = webElement.get_attribute('style')
                original_style_background = webElement.value_of_css_property('background')
                original_style_border = webElement.value_of_css_property('border')
                original_style_outline = webElement.value_of_css_property('outline')
                log.info('Original style obtained')

                # Apply Avo Assure highlight style
                apply_status = self.apply_style(webElement,str(original_style) + self.webscrapeutilsobj.AVO_ASSURE_WEBELEMENT_HIGHLIGHT_STYLE, 3)
                log.info('Element highlighted')

                # Decide which style attributes need to be reverted
                extra_style = ""
                if original_style_background is None:
                    extra_style = extra_style + "background: 0; "
                if original_style_border is None:
                    extra_style = extra_style + "border: 0px none; "
                if original_style_outline is None:
                    extra_style = extra_style + "outline: none"

                # Now remove the Avo Assure highlight style and apply original style
                remove_status = self.apply_style(webElement,str(original_style) + extra_style, 0)
                if apply_status and remove_status:
                    log.info('element highlighted successfully')
                    status = domconstants_MW.STATUS_SUCCESS
            else:
                err_msg="Error while highlighting"
                log.info('could not find the element')
                status = domconstants_MW.STATUS_FAIL
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            log.error(e,exc_info=True)
            status = domconstants_MW.STATUS_FAIL
            if (isinstance(self.driver,webdriver.Ie)):
                err_msg='Please make sure security settings are at the same level by clicking on Tools ->Internet Options -> Security tab(either all the checkboxes should be  checked or unchecked)'
            logger.print_on_console(err_msg)
        return status

    def apply_style(self,element,style, sec):
        applystylestatus = False
        try:
            log.info('Inside apply_style method .....')
            if self.driver.name == 'internet explorer':
                log.info('Before applying color to the element in IE browser .....')
                self.driver.execute_script("arguments[0].style.setAttribute('cssText', arguments[1]);",
                                           element, style)
                log.info('Applied color to the element in IE browser .....')
            else:
                log.info('Before applying color to the element in chrome/firefox browser .....')
                self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                           element, style)
                log.info('Applied color to the element in chrome/firefox browser .....')
            time.sleep(sec)
            applystylestatus = True
        except Exception as e:
            log.error(e)
        return applystylestatus


