#-------------------------------------------------------------------------------
# Name:        objectspy
# Purpose:
#
# Author:      prudhvi.gujjuboyina
# Modified By: nikunj.jain
#
# Created:     28-09-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import json
import time
import domconstants
import browserops
import logging
import logger
import os
from selenium import webdriver
from core_utils import CoreUtils
log = logging.getLogger(__name__)
from webscrape_utils import WebScrape_Utils

class Object_Mapper():

    coreutilsobj = CoreUtils()
    webscrapeutilsobj = WebScrape_Utils()

    def __init__(self):
        self.driver = browserops.driver
        self.currenthandle = None
        self.changedobjects = []
        self.changedobjectskeys = []

        self.notchangedobjects = []

        self.notfoundobjects = []
        self.notfoundobjectskeys = []
        self.viewdata= []
        self.data ={}
        self.status = domconstants.STATUS_FAIL

    def perform_compare(self,elementsdata):
        try:
            log.info('Inside perform_compare method')
            javascript_hasfocus = """return(document.hasFocus());"""
            for eachdriverhand in self.driver.window_handles:
                log.info('Iterating through the number of windows open by the driver')
                self.driver.switch_to.window(eachdriverhand)
                log.info('Switching to each handle and checking weather it has focus ')
                time.sleep(3)
                if (self.driver.execute_script(javascript_hasfocus)):
                    log.info('Got the window which has the focus')
                    self.currenthandle = eachdriverhand
            log.info("Comparing %d objects",len(elementsdata['view']))
            if  not "scrapedurl" in elementsdata.keys():
                raise Exception("Invalid url, Unable to navigate to the website")
            count = 0
            for element in elementsdata['view']:
                # XPath and URL decryption logic implemented
                xpath_string = element['xpath'].split(';')
                check_xpath_list = [i for i in xpath_string if i.strip()]
                if len(check_xpath_list) == 0:
                    raise ValueError('xpath of the object is empty')
                if len(xpath_string) == 3:
                    left_part = self.coreutilsobj.scrape_unwrap(xpath_string[0])
                    right_part = self.coreutilsobj.scrape_unwrap(xpath_string[2])
                else:
                    left_part = str(xpath_string[0])
                    right_part = ';'.join(map(str,xpath_string[2:]))
                decryptedxpath = left_part + ';' + xpath_string[1] + ';' + right_part
                decryptedelementurl = self.coreutilsobj.scrape_unwrap(element['url'])
                identifiers = decryptedxpath.split(';')

                # Locate the webelement
                if self.webscrapeutilsobj.is_iframe_frame_url(decryptedelementurl):
                    self.webscrapeutilsobj.switchtoframe_webscrape(self.driver, self.currenthandle, decryptedelementurl)
                webElement = self.webscrapeutilsobj.locate_webelement(self.driver, identifiers)
                if webElement is not None:
                    new_properties = self.driver.execute_script(self.webscrapeutilsobj.javascript_get_object_properties,webElement[0],decryptedelementurl)[0]
                    if new_properties['xpath'] != decryptedxpath:
                        # print "new: ",new_properties['xpath']
                        # log.debug("changed object found")
                        # Xpath Encryption logic implemented
                        new_properties['custname']=element['custname']
                        new_properties['url'] = self.coreutilsobj.scrape_wrap(new_properties['url'])
                        xpath_string = new_properties['xpath'].split(';')
                        left_part = self.coreutilsobj.scrape_wrap(';'.join(xpath_string[:2]))
                        right_part = self.coreutilsobj.scrape_wrap(';'.join(xpath_string[3:]))
                        new_properties['xpath'] = left_part + ';' + xpath_string[2] + ';' + right_part
                        self.changedobjects.append(new_properties)
                        self.changedobjectskeys.append(count)
                    else:
                        log.debug("not changed object found")
                        self.notchangedobjects.append(element)
                else:
                    log.debug("object not found")
                    self.notfoundobjectskeys.append(count)
                    self.notfoundobjects.append(element)
                count = count + 1
                log.debug("processed object: %d",count)
            log.info("all %s elements are processed, changedobject: %d, notchangedobject: %d, notfoundobject: %d",
                     len(elementsdata['view']),len(self.changedobjects),len(self.notchangedobjects), len(self.notfoundobjects))
            self.viewdata.append({'changedobject' : self.changedobjects })
            self.viewdata.append({'notchangedobject': self.notchangedobjects})
            self.viewdata.append({'notfoundobject': self.notfoundobjects})
            comparedin = ''
            if browserops.browser == '2':
                comparedin = 'FX'
            elif browserops.browser == '3':
                comparedin = 'IE'
            elif browserops.browser == '1':
                comparedin = 'CH'

            log.info("taking fullpage screenshot")
            maindir = os.environ["AVO_ASSURE_HOME"]
            screen_shot_path = maindir + '/output/' + domconstants.SCREENSHOT_IMG
            if (isinstance(self.driver, webdriver.Firefox) or isinstance(self.driver, webdriver.Chrome)):
                screen, total_width, total_height = self.webscrapeutilsobj.fullpage_screenshot(self.driver, screen_shot_path)
            else:
                screen = self.driver.get_screenshot_as_base64()
            self.data['comparedin'] = comparedin
            self.data['view'] = self.viewdata
            self.data['mirror'] = screen
            self.data['scrapedurl'] = self.driver.current_url
            self.data['changedobjectskeys'] = self.changedobjectskeys
            self.data['notfoundobjectskeys'] = self.notfoundobjectskeys
            log.info("writing data into domelements.json")
            with open(os.environ["AVO_ASSURE_HOME"] + '/output/domelements.json', 'w') as outfile:
                json.dump(self.data, outfile, indent=4, sort_keys=False)
            self.status  = domconstants.STATUS_SUCCESS
        except ValueError as e:
            self.status = "EMPTY_OBJECT"
            logger.print_on_console("Unmapped object(s) found")
            log.error(e)
        except Exception as e:
            logger.print_on_console("Error while comparing objects")
            log.error(e)

        self.data['action'] = 'compare'
        self.data['status'] = self.status
        return self.data