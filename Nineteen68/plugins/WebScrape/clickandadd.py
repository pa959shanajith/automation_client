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
import platform
from core_utils import CoreUtils
if platform.system()!='Darwin':
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
from selenium import webdriver
from PIL import Image
log = logging.getLogger('clickandadd.py')
currenthandle = ''
status = domconstants.STATUS_FAIL
browserops_obj=browserops.BrowserOperations()
from webscrape_utils import WebScrape_Utils

class Clickandadd():
    def startclickandadd(self):
        driver = browserops.driver
        webscrape_utils_obj = WebScrape_Utils()
        try:
            log.info('Inside startclickandadd method .....')
            browser = browserops.browser
            log.info('Obtained browser handle and driver'
                     ' from browserops.py class .....')
            toolwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(toolwindow, win32con.SW_MINIMIZE)
            actwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(actwindow, win32con.SW_MAXIMIZE)
            log.info('Minimizing the foreground window i.e tool and assuming AUT on top .....')
            javascript_hasfocus = """return(document.hasFocus());"""
            time.sleep(6)
            browserops_obj.checkPopups()
            for eachdriverhand in driver.window_handles:
                log.info('Iterating through the number of windows open by the driver')
                driver.switch_to.window(eachdriverhand)
                log.info('Switching to each handle and checking weather it has focus ')

                if (driver.execute_script(javascript_hasfocus)):
                    log.info('Got the window which has the focus')
                    global currenthandle
                    currenthandle = eachdriverhand
                    break

            driver.switch_to.window(currenthandle)
            log.info('Performing the start click and add operation on default/outer page')
            driver.execute_script(webscrape_utils_obj.javascript_clicknadd, driver.current_url,browser)
            log.info('start click and add operation on default/outer page done')

            """Method to perform Start ClickAndAdd on iframes (and frames) recursively"""
            def callback_scrape_start_cna_iframes(myipath):
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                    path = myipath + str(iframes) + 'i' + '/'
                    if webscrape_utils_obj.switchtoframe_webscrape(driver, currenthandle, path):
                        log.debug('switched to iframe/frame %s', path)
                        driver.execute_script(webscrape_utils_obj.javascript_clicknadd, path)
                        log.debug('Start ClickAndAdd scrape operation on iframe %s is done', path)
                        callback_scrape_start_cna_iframes(path)
                        callback_scrape_start_cna_frames(path)
                    else:
                        log.info('could not switch to iframe/frame %s', path)

            """Method to perform Start ClickAndAdd on frames (and iframes) recursively"""
            def callback_scrape_start_cna_frames(myipath):
                for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
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
            status = domconstants.STATUS_FAIL
            print 'Error while performing start click and add scrape'
            if (isinstance(driver,webdriver.Ie)):
                print 'Please make sure security settings are at the same level by clicking on Tools ->Internet Options -> Security tab(either all the checkboxes should be  checked or unchecked) and retry'
        return status

    def stopclickandadd(self):
        data = {}
        webscrape_utils_obj = WebScrape_Utils()
        try:
            log.info('Inside stopclickandadd method .....')
            driver = browserops.driver
            maindir = os.environ["NINETEEN68_HOME"]
            screen_shot_path = maindir + '/Nineteen68/plugins/WebScrape' + domconstants.SCREENSHOT_IMG
            log.info('Obtained driver from browserops.py class .....')

            tempne_stopclicknadd = []
            log.info('Performing the stopclickandd operation on default/outer page')
            tempreturn_stopclicknadd = driver.execute_script(webscrape_utils_obj.javascript_stopclicknadd)
            log.info('stopclickandd operation on default/outer page is done and data is obtained')
            tempne_stopclicknadd.extend(tempreturn_stopclicknadd)

            """Method to perform Stop ClickAndAdd on iframes (and frames) recursively"""
            def callback_scrape_stop_cna_iframes(myipath, tempne_stopclicknadd):
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                    path = myipath + str(iframes) + 'i' + '/'
                    if webscrape_utils_obj.switchtoframe_webscrape(driver, currenthandle, path):
                        log.debug('switched to iframe/frame %s', path)
                        temp = driver.execute_script(webscrape_utils_obj.javascript_stopclicknadd, path)
                        if temp is not None:
                            log.debug('Stop ClickAndAdd scrape operation on iframe %s is done', path)
                            tempne_stopclicknadd.extend(temp)
                            callback_scrape_stop_cna_iframes(path, tempne_stopclicknadd)
                            callback_scrape_stop_cna_frames(path, tempne_stopclicknadd)
                    else:
                        log.info('could not switch to iframe/frame %s', path)

            """Method to perform Stop ClickAndAdd on iframes (and frames) recursively"""
            def callback_scrape_stop_cna_frames(myipath, tempne_stopclicknadd):
                for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
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

            if (isinstance(driver,webdriver.Firefox) or isinstance(driver,webdriver.Chrome)):
                screen = webscrape_utils_obj.fullpage_screenshot(driver, screen_shot_path )
            else:
                screen = driver.get_screenshot_as_base64()
            scrapedin = ''
            if browserops.browser == 2:
                scrapedin = 'FX'
            elif browserops.browser == 3:
                scrapedin = 'IE'
            elif browserops.browser == 1:
                scrapedin = 'CH'
            data['scrapetype'] = 'cna'
            data['scrapedin'] = scrapedin
            #XPath encryption logic implemented
            new_obj=[]
            obj=CoreUtils()
            for a in tempne_stopclicknadd:
                a['url']= obj.scrape_wrap(a['url'])
                xpath_string=a['xpath'].split(';')
                left_part=obj.scrape_wrap(';'.join(xpath_string[:2]))
                right_part=obj.scrape_wrap(';'.join(xpath_string[3:]))
                a['xpath'] = left_part+';'+xpath_string[2]+';'+right_part
                new_obj.append(a)
            tempne_stopclicknadd=new_obj
            data['view'] = tempne_stopclicknadd
            data['mirror'] = screen

            log.info('Creating a json object with key vie with value as return data')
            with open('domelements.json', 'w') as outfile:
                log.info('Opening domelements.json file to write vie object')
                json.dump(data, outfile, indent=4, sort_keys=False)
                log.info('vie is dumped into  domelements.json file ')
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
            status = domconstants.STATUS_FAIL
            data = domconstants.STATUS_FAIL
            print 'Error while performing stop click and add scrape'
            if (isinstance(driver,webdriver.Ie)):
                print 'Please make sure security settings are at the same level by clicking on Tools ->Internet Options -> Security tab(either all the checkboxes should be  checked or unchecked) and retry'
        return data

