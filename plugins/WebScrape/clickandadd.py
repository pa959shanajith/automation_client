#-------------------------------------------------------------------------------
# Name:        clickandadd.py
# Purpose:
#
# Author:      wasimakram.sutar
# Modified By: nikunj.jain
#
# Created:     28-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import browserops
from constants import SYSTEM_OS
from core_utils import CoreUtils
if SYSTEM_OS=='Windows':
    import win32gui
    import win32con
import time
import json
import domconstants
import logger
import Exceptions
import logging.config
import logging
import os
import time
import readconfig
from selenium import webdriver
from PIL import Image
log = logging.getLogger('clickandadd.py')
currenthandle = ''
status = domconstants.STATUS_FAIL
browserops_obj=browserops.BrowserOperations()
from webscrape_utils import WebScrape_Utils

class Clickandadd():
    def startclickandadd(self,window_handle_number):
        driver = browserops.driver
        webscrape_utils_obj = WebScrape_Utils()
        try:
            global currenthandle
            log.info('Inside startclickandadd method .....')
            browser = browserops.browser
            log.info('Obtained browser handle and driver'
                     ' from browserops.py class .....')
            if SYSTEM_OS=='Windows':
                toolwindow = win32gui.GetForegroundWindow()
            #win32gui.ShowWindow(toolwindow, win32con.SW_MINIMIZE)
            if SYSTEM_OS=='Windows':
                actwindow = win32gui.GetForegroundWindow()
            #win32gui.ShowWindow(actwindow, win32con.SW_MAXIMIZE)
            log.info('Minimizing the foreground window i.e tool and assuming AUT on top .....')
            javascript_hasfocus = """return(document.hasFocus());"""
            time.sleep(6)
            browserops_obj.checkPopups()

            if window_handle_number is not None and window_handle_number > 0:
                driver.switch_to.window(driver.window_handles[window_handle_number])
                currenthandle = driver.window_handles[window_handle_number]
            else:
                for eachdriverhand in driver.window_handles:
                    log.info('Iterating through the number of windows open by the driver')
                    driver.switch_to.window(eachdriverhand)
                    log.info('Switching to each handle and checking weather it has focus ')

                    if (driver.execute_script(javascript_hasfocus)):
                        log.info('Got the window which has the focus')
                        currenthandle = eachdriverhand
                        break

            if currenthandle in driver.window_handles:
                driver.switch_to.window(currenthandle)
            else:
                driver.switch_to.window(driver.current_window_handle)
            log.info('Performing the start click and add operation on default/outer page')
            driver.execute_script(webscrape_utils_obj.javascript_clicknadd, driver.current_url,browser)
            log.info('start click and add operation on default/outer page done')
            browserlogs = None
            if not(isinstance(driver,webdriver.Ie) or isinstance(driver,webdriver.Firefox)):
                browserlogs = driver.get_log("browser")
            if browserlogs and len(browserlogs) > 0 and browserlogs[0]['level'] == 'SEVERE' and 'Refused to apply inline style' in browserlogs[0]['message'] :
                logger.print_on_console('Content Security Policy directive restriction, element highlighting not possible.')
                log.error(browserlogs[0]['message'])

            """Method to perform Start ClickAndAdd on iframes (and frames) recursively"""
            def callback_scrape_start_cna_iframes(myipath):
                for iframes in range(len(driver.find_elements_by_tag_name(domconstants.IFRAME))):
                    path = myipath + str(iframes) + 'i' + '/'
                    if webscrape_utils_obj.switchtoframe_webscrape(driver, currenthandle, path):
                        log.debug('switched to iframe/frame %s', path)
                        driver.execute_script(webscrape_utils_obj.javascript_clicknadd, path, browser)
                        log.debug('Start ClickAndAdd scrape operation on iframe %s is done', path)
                        callback_scrape_start_cna_iframes(path)
                        callback_scrape_start_cna_frames(path)
                    else:
                        log.info('could not switch to iframe/frame %s', path)

            """Method to perform Start ClickAndAdd on frames (and iframes) recursively"""
            def callback_scrape_start_cna_frames(myipath):
                for frames in range(len(driver.find_elements_by_tag_name(domconstants.FRAME))):
                    path = myipath + str(frames) + 'f' + '/'
                    if webscrape_utils_obj.switchtoframe_webscrape(driver, currenthandle, path):
                        log.debug('switched to iframe/frame %s', path)
                        driver.execute_script(webscrape_utils_obj.javascript_clicknadd, path)
                        log.debug('Start ClickAndAdd scrape operation on frame %s is done', path)
                        callback_scrape_start_cna_frames(path)
                        callback_scrape_start_cna_iframes(path)
                    else:
                        log.info('could not switch to iframe/frame %s', path)

            callback_scrape_start_cna_iframes('')
            driver.switch_to.window(currenthandle)
            callback_scrape_start_cna_frames('')
            log.info('Start ClickAndAdd scrape operation on frame/iframe pages is completed')
            driver.switch_to.window(currenthandle)
            driver.switch_to_default_content()
            status = domconstants.STATUS_SUCCESS
        except Exception as e:
            log.error(e)
            status = domconstants.STATUS_FAIL
            logger.print_on_console('Error while performing start click and add scrape')
            if (isinstance(driver,webdriver.Ie)):
                logger.print_on_console('Please make sure security settings are at the same level by clicking on Tools ->Internet Options -> Security tab(either all the checkboxes should be  checked or unchecked) and retry')
        return status

    def stopclickandadd(self):
        data = {}
        webscrape_utils_obj = WebScrape_Utils()
        try:
            log.info('Inside stopclickandadd method .....')
            driver = browserops.driver
            maindir = os.environ["AVO_ASSURE_HOME"]
            screen_shot_path = maindir + '/output/' + domconstants.SCREENSHOT_IMG
            log.info('Obtained driver from browserops.py class .....')
            tempne_stopclicknadd = []
            log.info('Performing the stopclickandd operation on default/outer page')
            tempreturn_stopclicknadd = driver.execute_script(webscrape_utils_obj.javascript_stopclicknadd)
            log.info('stopclickandd operation on default/outer page is done and data is obtained')
            tempne_stopclicknadd.extend(tempreturn_stopclicknadd)

            """Method to perform Stop ClickAndAdd on iframes (and frames) recursively"""
            def callback_scrape_stop_cna_iframes(myipath, tempne_stopclicknadd):
                if_list = driver.find_elements_by_tag_name(domconstants.IFRAME)
                rect_list = []
                for iframes in if_list:
                    if iframes is not None:
                        rect_list.append(iframes.rect)
                for iframes in range(len(if_list)):
                    path = myipath + str(iframes) + 'i' + '/'
                    rect = rect_list[iframes]
                    if webscrape_utils_obj.switchtoframe_webscrape(driver, currenthandle, path):
                        in_iframe = driver.execute_script(webscrape_utils_obj.javascript_in_iframe)
                        log.debug('switched to iframe/frame %s', path)
                        temp = driver.execute_script(webscrape_utils_obj.javascript_stopclicknadd, path)
                        if temp is not None:
                            if in_iframe and rect is not None:
                                for element in temp:
                                    element['top'] = element['top'] + rect['y']
                                    element['left'] = element['left'] + rect['x']
                            log.debug('Stop ClickAndAdd scrape operation on iframe %s is done', path)
                            tempne_stopclicknadd.extend(temp)
                            callback_scrape_stop_cna_iframes(path, tempne_stopclicknadd)
                            callback_scrape_stop_cna_frames(path, tempne_stopclicknadd)
                    else:
                        log.info('could not switch to iframe/frame %s', path)

            """Method to perform Stop ClickAndAdd on frames (and iframes) recursively"""
            def callback_scrape_stop_cna_frames(myipath, tempne_stopclicknadd):
                for frames in range(len(driver.find_elements_by_tag_name(domconstants.FRAME))):
                    path = myipath + str(frames) + 'f' + '/'
                    if webscrape_utils_obj.switchtoframe_webscrape(driver, currenthandle, path):
                        log.debug('switched to iframe/frame %s', path)
                        temp = driver.execute_script(webscrape_utils_obj.javascript_stopclicknadd, path)
                        if temp is not None:
                            log.debug('Stop ClickAndAdd scrape operation on frame %s is done', path)
                            tempne_stopclicknadd.extend(temp)
                            callback_scrape_stop_cna_frames(path, tempne_stopclicknadd)
                            callback_scrape_stop_cna_iframes(path, tempne_stopclicknadd)
                    else:
                        log.info('could not switch to iframe/frame %s', path)
            callback_scrape_stop_cna_iframes('', tempne_stopclicknadd)
            driver.switch_to.window(currenthandle)
            callback_scrape_stop_cna_frames('', tempne_stopclicknadd)
            log.info('Stop ClickAndAdd scrape operation on frame/iframe pages is completed')
            driver.switch_to.window(currenthandle)
            driver.switch_to_default_content()
            configvalues = readconfig.configvalues
            full_screenshot = str(configvalues['full_screenshot'])
            if (isinstance(driver,webdriver.Firefox) or isinstance(driver,webdriver.Chrome) or isinstance(driver,webdriver.Edge)):
                if ((str(full_screenshot).lower()) == 'yes'):
                    screen, total_width, total_height = webscrape_utils_obj.fullpage_screenshot(driver, screen_shot_path)
                    fullSS=True
                else:
                    screen = driver.get_screenshot_as_base64()
                    fullSS=False 
            else:
                screen = driver.get_screenshot_as_base64()
                fullSS=False
            scrapedin = ''
            if browserops.browser == 2:
                scrapedin = 'FX'
            elif browserops.browser == 3:
                scrapedin = 'IE'
            elif browserops.browser == 1:
                scrapedin = 'CH'
            elif browserops.browser == 7:
                scrapedin = 'EDGE'
            elif browserops.browser == 8:
                scrapedin = 'EDGE CHROMIUM'
            data['scrapetype'] = 'cna'
            data['scrapedin'] = scrapedin
            #XPath encryption logic implemented
            new_obj=[]
            obj=CoreUtils()
            for a in tempne_stopclicknadd:
                a['url']= obj.scrape_wrap(a['url'])
                xpath_string=a['xpath'].split(';') + ["null",a['tag']]
                left_part=obj.scrape_wrap(';'.join(xpath_string[:2]))
                right_part=obj.scrape_wrap(';'.join(xpath_string[3:]))
                a['xpath'] = left_part+';'+xpath_string[2]+';'+right_part
                a['fullSS']=fullSS
                new_obj.append(a)
            tempne_stopclicknadd=new_obj
            data['view'] = tempne_stopclicknadd
            data['mirror'] = screen

            log.info('Creating a json object with key view with value as return data')
            with open(os.environ["AVO_ASSURE_HOME"] + '/output/domelements.json', 'w') as outfile:
                log.info('Opening domelements.json file to write view object')
                json.dump(data, outfile, indent=4, sort_keys=False)
                log.info('view is dumped into  domelements.json file ')
            outfile.close()
            log.info('domelements.json file closed ')
            if driver.current_url == domconstants.BLANK_PAGE:
                log.info('url is blank so cannot perform clickandadd operation')
                status = domconstants.STATUS_FAIL
                data = domconstants.STATUS_FAIL
            else:
                status = domconstants.STATUS_SUCCESS
                data['scrapedurl'] = driver.current_url
        except Exception as e:
            log.error(e)
            status = domconstants.STATUS_FAIL
            data = domconstants.STATUS_FAIL
            logger.print_on_console('Error while performing stop click and add scrape')
            if (isinstance(driver,webdriver.Ie)):
                logger.print_on_console('Please make sure security settings are at the same level by clicking on Tools ->Internet Options -> Security tab(either all the checkboxes should be  checked or unchecked) and retry')
                log.error(e,exc_info=True)
        return data