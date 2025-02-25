#-------------------------------------------------------------------------------
# Name:        fullscrape_MW.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     28-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


from constants import SYSTEM_OS
if SYSTEM_OS=='Windows':
    import win32gui
    import win32con
import json
import domconstants_MW
import logging
import os
import time
import browser_Keywords_MW
# from selenium import webdriver
log = logging.getLogger('fullscrape_MW.py')
currenthandle = ''
status = domconstants_MW.STATUS_FAIL
from core_utils import CoreUtils
import logger
from webscrape_utils_MW import WebScrape_Utils

class Fullscrape():
    def fullscrape(self,scrape_option,window_handle_number,visiblity_status):
        global currenthandle
        start_time = time.clock()
        data = {}
        driver = browser_Keywords_MW.driver_obj
        webscrape_utils_obj = WebScrape_Utils()
        try:
            log.info(' Inside fullscrape method .....')
            log.info('scrape_option is: %s',scrape_option)
            # hwndg = browserops.hwndg
            maindir = os.environ["AVO_ASSURE_HOME"]
            screen_shot_path = maindir + '/output/' + domconstants_MW.SCREENSHOT_IMG
            log.info('Obtained browser handle and driver from browserops.py class .....')
            if SYSTEM_OS=='Windows':
                toolwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(toolwindow, win32con.SW_MINIMIZE)
            log.info(' Minimizing the foreground window i.e tool and assuming AUT on top .....')
            time.sleep(2)
            if SYSTEM_OS=='Windows':
                actwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(actwindow, win32con.SW_MAXIMIZE)
            # browserops_obj.checkPopups()
            javascript_hasfocus = """return(document.hasFocus());"""
##            time.sleep(6)
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
            tempne = []
            log.info('Performing the full scrape operation on default/outer page')
            if scrape_option[0].lower() == 'select a section using xpath':
                if len(scrape_option) > 1 and len(scrape_option[1]) > 0:
                    reference_element = driver.find_element_by_xpath(scrape_option[1])
                    tempreturn = []
                    scrape_option[1] = reference_element
                else:
                    raise ValueError('invalid xpath')
            if visiblity_status == True:
                tempreturn = driver.execute_script(webscrape_utils_obj.javascript_fullscrape_Visiblity, driver.current_url,scrape_option)
            else:
                tempreturn = driver.execute_script(webscrape_utils_obj.javascript_fullscrape, driver.current_url,scrape_option)
            log.info('full scrape operation on default/outer page is done and data is obtained')
            tempne.extend(tempreturn)

            """Method to perform fullscrape on iframes (and frames) recursively"""
            def callback_fullscrape_iframes(myipath, tempne):
                for iframes in (list(range(len(driver.find_elements_by_tag_name(domconstants_MW.IFRAME))))):
                    path = myipath + str(iframes) + 'i' + '/'
                    if webscrape_utils_obj.switchtoframe_webscrape(driver,currenthandle,path):
                        log.debug('switched to iframe/frame %s', path)
                        if visiblity_status ==True:
                            temp = driver.execute_script(webscrape_utils_obj.javascript_fullscrape_Visiblity, path,scrape_option)
                        else:
                            temp = driver.execute_script(webscrape_utils_obj.javascript_fullscrape, path,scrape_option)
                        if temp is not None:
                            log.debug('full scrape operation on iframe %s is done and data is obtained',path)
                            tempne.extend(temp)
                        callback_fullscrape_iframes(path,tempne)
                        callback_fullscrape_frames(path,tempne)
                    else:
                        log.info('could not switch to iframe/frame %s', path)

            """Method to perform fullscrape on frames (and iframes) recursively"""
            def callback_fullscrape_frames(myipath, tempne):
                for frames in (list(range(len(driver.find_elements_by_tag_name(domconstants_MW.FRAME))))):
                    path = myipath + str(frames) + 'f' +  '/'
                    if webscrape_utils_obj.switchtoframe_webscrape(driver,currenthandle,path):
                        log.debug('switched to iframe/frame %s', path)
                        if visiblity_status ==True:
                            temp = driver.execute_script(webscrape_utils_obj.javascript_fullscrape_Visiblity, path,scrape_option)
                        else:
                            temp = driver.execute_script(webscrape_utils_obj.javascript_fullscrape, path,scrape_option)
                        if temp is not None:
                            log.debug('full scrape operation on frame %s is done and data is obtained',path)
                            tempne.extend(temp)
                        callback_fullscrape_frames(path, tempne)
                        callback_fullscrape_iframes(path, tempne)
                    else:
                        log.info('could not switch to iframe/frame %s', path)

            # scrape through iframes/frames iff OS is windows and scrape_option is not the xpath one
            if SYSTEM_OS == 'Windows' and scrape_option[0].lower() != 'select a section using xpath':
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
                # a['url']= obj.scrape_wrap(a['url'])
                xpath_string=a['xpath'].split(';')+ ["null",a['tag']]
                # left_part=obj.scrape_wrap(';'.join(xpath_string[:2]))
                # right_part=obj.scrape_wrap(';'.join(xpath_string[3:]))
                # a['xpath'] = left_part+';'+xpath_string[2]+';'+right_part
                a['xpath'] = ';'.join(map(str,xpath_string))
                new_obj.append(a)
            tempne=new_obj
            log.info('json operations dumps and loads are performed on the return data')
            scrape_time = time.clock() - start_time
            log.info("Time taken in fullscrape: %s seconds",str(scrape_time))
            # if (isinstance(driver,webdriver.Firefox) or isinstance(driver,webdriver.Chrome)):
            #     screen = webscrape_utils_obj.fullpage_screenshot(driver, screen_shot_path )
            # else:
            screen = driver.get_screenshot_as_base64()
            scrapedin = 'CH'
            data['scrapetype'] = 'fs'
            data['scrapedin'] = scrapedin
            data['view'] = tempne
            data['mirror'] = screen
            data['mirrorwidth'] = driver.execute_script("return window.innerWidth")
            data['mirrorheight'] = driver.execute_script("return window.innerHeight")
            log.info('Creating a json object with key vie with value as return data')
            with open(os.environ["AVO_ASSURE_HOME"] + '/output/domelements.json', 'w') as outfile:
                log.info('Opening domelements.json file to write view object')
                json.dump(data, outfile, indent=4, sort_keys=False)
                log.info('view is dumped into  domelements.json file ')
            outfile.close()
            log.info('domelements.json file closed ')
            if driver.current_url == domconstants_MW.BLANK_PAGE:
                log.info('url is blank so cannot perform full scrape operation ')
                status = domconstants_MW.STATUS_FAIL
                data = domconstants_MW.STATUS_FAIL
            else:
                status = domconstants_MW.STATUS_SUCCESS
                data['scrapedurl'] = driver.current_url
##            log.info('FILE: fullscrape.py , DEF: fullscrape() , MSG: Maximizing the tool once full scrape is done ')
##            win32gui.ShowWindow(toolwindow, win32con.SW_MAXIMIZE)
        except Exception as e:
            status = domconstants_MW.STATUS_FAIL
            data = domconstants_MW.STATUS_FAIL
            log.error(e)
            ename = type(e).__name__
            if ename in ('NoSuchElementException','ValueError','InvalidSelectorException'):
                logger.print_on_console("Invalid input, provide a valid xpath of the element to start the section")
                logger.print_on_console('Error while performing full scrape')
            # if (isinstance(driver,webdriver.Ie)):
            #     logger.logger.print_on_console( 'Please make sure security settings are at the same level by clicking on Tools ->Internet Options -> Security tab(either all the checkboxes should be  checked or unchecked) and retry')
        return data


