#-------------------------------------------------------------------------------
# Name:        fullscrape.py
# Purpose:     Performs fullscrape operation on a web page
#
# Author:      wasimakram.sutar
# Modified By: nikunj.jain
#
# Created:     28-09-2016
# Copyright:   (c) nikunj.jain 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import browserops
import platform
if platform.system()!='Darwin':
    import win32gui
    import win32con
import json
import domconstants
import logging
import os
import time
from selenium import webdriver
log = logging.getLogger('fullscrape.py')
currenthandle = ''
status = domconstants.STATUS_FAIL
browserops_obj=browserops.BrowserOperations()
from core_utils import CoreUtils
from webscrape_utils import WebScrape_Utils

class Fullscrape():
    def fullscrape(self):
        start_time = time.clock()
        data = {}
        driver = browserops.driver
        webscrape_utils_obj = WebScrape_Utils()
        try:
            log.info(' Inside fullscrape method .....')
            hwndg = browserops.hwndg
            maindir = os.environ["NINETEEN68_HOME"]
            screen_shot_path = maindir + '/Nineteen68/plugins/WebScrape' + domconstants.SCREENSHOT_IMG
            log.info('Obtained browser handle and driver from browserops.py class .....')
            if platform.system()!='Darwin':
                toolwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(toolwindow, win32con.SW_MINIMIZE)
            log.info(' Minimizing the foreground window i.e tool and assuming AUT on top .....')
            time.sleep(2)
            if platform.system() != 'Darwin':
                actwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(actwindow, win32con.SW_MAXIMIZE)
            browserops_obj.checkPopups()
            javascript_hasfocus = """return(document.hasFocus());"""
##            time.sleep(6)
            for eachdriverhand in driver.window_handles:
                log.info('Iterating through the number of windows open by the driver')
                driver.switch_to.window(eachdriverhand)
                log.info('Switching to each handle and checking weather it has focus ')
                if (driver.execute_script(javascript_hasfocus)):
                    log.info('Got the window which has the focus')
                    global currenthandle
                    currenthandle = eachdriverhand
                    break
            tempne = []
            log.info('Performing the full scrape operation on default/outer page')
            tempreturn = driver.execute_script(webscrape_utils_obj.javascript_fullscrape, driver.current_url)
            log.info('full scrape operation on default/outer page is done and data is obtained')
            tempne.extend(tempreturn)

            """Method to perform fullscrape on iframes (and frames) recursively"""
            def callback_fullscrape_iframes(myipath, tempne):
                for iframes in (range(len(driver.find_elements_by_tag_name(domconstants.IFRAME)))):
                    path = myipath + str(iframes) + 'i' + '/'
                    if webscrape_utils_obj.switchtoframe_webscrape(driver,currenthandle,path):
                        log.debug('switched to iframe/frame %s', path)
                        temp = driver.execute_script(webscrape_utils_obj.javascript_fullscrape, path)
                        if temp is not None:
                            log.debug('full scrape operation on iframe %s is done and data is obtained',path)
                            tempne.extend(temp)
                        callback_fullscrape_iframes(path,tempne)
                        callback_fullscrape_frames(path,tempne)
                    else:
                        log.info('could not switch to iframe/frame %s', path)

            """Method to perform fullscrape on frames (and iframes) recursively"""
            def callback_fullscrape_frames(myipath, tempne):
                for frames in (range(len(driver.find_elements_by_tag_name(domconstants.FRAME)))):
                    path = myipath + str(frames) + 'f' +  '/'
                    if webscrape_utils_obj.switchtoframe_webscrape(driver,currenthandle,path):
                        log.debug('switched to iframe/frame %s', path)
                        temp = driver.execute_script(webscrape_utils_obj.javascript_fullscrape, path)
                        if temp is not None:
                            log.debug('full scrape operation on frame %s is done and data is obtained',path)
                            tempne.extend(temp)
                        callback_fullscrape_frames(path, tempne)
                        callback_fullscrape_iframes(path, tempne)
                    else:
                        log.info('could not switch to iframe/frame %s', path)

            if platform.system()!='Darwin':
                callback_fullscrape_iframes('', tempne)
                driver.switch_to.window(currenthandle)
                callback_fullscrape_frames('', tempne)
                log.info('full scrape operation on iframe/frame pages is completed')
                driver.switch_to.window(currenthandle)
                driver.switch_to_default_content()
            tempne = json.dumps(tempne)
            tempne = json.loads(tempne)
            new_obj=[]
            obj = CoreUtils()
            # XPath Encryption logic implemented
            for a in tempne:
                a['url']= obj.scrape_wrap(a['url'])
                xpath_string=a['xpath'].split(';')
                left_part=obj.scrape_wrap(';'.join(xpath_string[:2]))
                right_part=obj.scrape_wrap(';'.join(xpath_string[3:]))
                a['xpath'] = left_part+';'+xpath_string[2]+';'+right_part
                new_obj.append(a)
            tempne=new_obj
            log.info('json operations dumps and loads are performed on the return data')
            scrape_time = time.clock() - start_time
            log.info("Time taken in fullscrape: %s seconds",str(scrape_time))
            if (isinstance(driver,webdriver.Firefox) or isinstance(driver,webdriver.Chrome)):
                screen = webscrape_utils_obj.fullpage_screenshot(driver, screen_shot_path )
            else:
                screen = driver.get_screenshot_as_base64()
            scrapedin = ''
            if browserops.browser == 2:
                scrapedin = 'FX'
            elif browserops.browser == 3:
                scrapedin =  'IE'
            elif browserops.browser == 1:
                scrapedin =  'CH'
            data['scrapetype'] = 'fs'
            data['scrapedin'] = scrapedin
            data['view'] = tempne
            data['mirror'] = screen
            log.info('Creating a json object with key view with value as return data')
            with open('domelements.json', 'w') as outfile:
                log.info('Opening domelements.json file to write view object')
                json.dump(data, outfile, indent=4, sort_keys=False)
                log.info('view is dumped into  domelements.json file ')
            outfile.close()
            log.info('domelements.json file closed ')
            if driver.current_url == domconstants.BLANK_PAGE:
                log.info('url is blank so cannot perform full scrape operation ')
                status = domconstants.STATUS_FAIL
                data = domconstants.STATUS_FAIL
            else:
                status = domconstants.STATUS_SUCCESS
                data['scrapedurl'] = driver.current_url
##            log.info('FILE: fullscrape.py , DEF: fullscrape() , MSG: Maximizing the tool once full scrape is done ')
##            win32gui.ShowWindow(toolwindow, win32con.SW_MAXIMIZE)
        except Exception as e:
            status = domconstants.STATUS_FAIL
            data = domconstants.STATUS_FAIL
            print 'Error while performing full scrape'
            log.error(e)
            if (isinstance(driver,webdriver.Ie)):
                print 'Please make sure security settings are at the same level by clicking on Tools ->Internet Options -> Security tab(either all the checkboxes should be  checked or unchecked) and retry'
        return data
