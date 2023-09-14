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
from constants import SYSTEM_OS
if SYSTEM_OS=='Windows':
    import win32gui
    import win32con
import json
import domconstants
import logging
import os
import time
import readconfig
from selenium import webdriver
log = logging.getLogger('fullscrape.py')
currenthandle = ''
status = domconstants.STATUS_FAIL
browserops_obj=browserops.BrowserOperations()
from core_utils import CoreUtils
import logger
from webscrape_utils import WebScrape_Utils

class Fullscrape():
    def fullscrape(self,scrape_option,window_handle_number,visiblity_status,tagfilter,xpathfilter,scenarioFlag):
        global currenthandle
        start_time = time.clock()
        data = {}
        driver = browserops.driver
        webscrape_utils_obj = WebScrape_Utils()
        try:
            log.info(' Inside fullscrape method .....')
            log.info('scrape_option is: %s',scrape_option)
            hwndg = browserops.hwndg
            maindir = os.environ["AVO_ASSURE_HOME"]
            screen_shot_path = maindir + '/output/' + domconstants.SCREENSHOT_IMG
            log.info('Obtained browser handle and driver from browserops.py class .....')
            if SYSTEM_OS=='Windows':
                toolwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(toolwindow, win32con.SW_MINIMIZE)
            log.info(' Minimizing the foreground window i.e tool and assuming AUT on top .....')
            time.sleep(2)
            if SYSTEM_OS=='Windows':
                actwindow = win32gui.GetForegroundWindow()
##            win32gui.ShowWindow(actwindow, win32con.SW_MAXIMIZE)
            browserops_obj.checkPopups()
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
            #Bug 610: Full scrape not working on IE after scraping on other browsers.
            if(isinstance(driver,webdriver.Ie) and currenthandle not in driver.window_handles and len(driver.window_handles)==1):
                currenthandle=driver.window_handles[0]
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
                for iframes in (list(range(len(driver.find_elements_by_tag_name(domconstants.IFRAME))))):
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
                for frames in (list(range(len(driver.find_elements_by_tag_name(domconstants.FRAME))))):
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
            new_obj_in_screen = []
            obj = CoreUtils()
            # XPath Encryption logic implemented
            for a in tempne:
                # a['url']= obj.scrape_wrap(a['url'])
                xpath_string=a['xpath'].split(';') + ["null",a['tag']]
                # left_part=obj.scrape_wrap(';'.join(xpath_string[:2]))
                # right_part=obj.scrape_wrap(';'.join(xpath_string[3:]))
                # a['xpath'] = left_part+';'+xpath_string[2]+';'+right_part
                a['xpath'] = ';'.join(map(str,xpath_string))
                
                if ((tagfilter=={} and xpathfilter=={}) or (tagfilter.get(a['tag']) and xpathfilter.get(xpath_string[0])==None and ((a['tag'] in ['button', 'a', 'table', 'tr', 'td', 'input', 'select']) or 'role' in a))):
                    new_obj.append(a)
                if scenarioFlag and xpathfilter.get(xpath_string[0])==None and ((a['tag'] in ['button', 'a', 'table', 'tr', 'td', 'input', 'select']) or 'role' in a):
                    new_obj_in_screen.append(a)
            tempne=new_obj
            log.info('json operations dumps and loads are performed on the return data')
            scrape_time = time.clock() - start_time
            log.info("Time taken in fullscrape: %s seconds",str(scrape_time))
            configvalues = readconfig.configvalues
            full_screenshot = str(configvalues['full_screenshot'])
            if (isinstance(driver,webdriver.Firefox) or isinstance(driver,webdriver.Chrome) or isinstance(driver,webdriver.Edge)):
                if ((str(full_screenshot).lower()) == 'yes'):
                    screen, total_width, total_height = webscrape_utils_obj.fullpage_screenshot(driver, screen_shot_path)
                else:
                    screen = driver.get_screenshot_as_base64()
            else:
                screen = driver.get_screenshot_as_base64()
            scrapedin = ''
            if browserops.browser == 2:
                scrapedin = 'FX'
            elif browserops.browser == 3:
                scrapedin =  'IE'
            elif browserops.browser == 1:
                scrapedin =  'CH'
            elif browserops.browser == 7:
                scrapedin = 'EDGE'
            elif browserops.browser == 8:
                scrapedin = 'EDGE CHROMIUM'
            data['scrapetype'] = 'fs'
            data['scrapedin'] = scrapedin
            #collecting new elements for analyze screen and scenario impact analyzer.
            if scenarioFlag:
                filtered_data={}
                filtered_data['new_obj_for_not_found']=tempne
                filtered_data['new_obj_in_screen']=new_obj_in_screen
                data['view']=filtered_data
            else:    
                data['view'] = tempne
            data['mirror'] = screen
            log.info('Creating a json object with key view with value as return data')
            with open(os.environ["AVO_ASSURE_HOME"] + '/output/domelements.json', 'w') as outfile:
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
            log.error(e)
            ename = type(e).__name__
            if ename in ('NoSuchElementException','ValueError','InvalidSelectorException'):
                logger.print_on_console("Invalid input, provide a valid xpath of the element to start the section")
                logger.print_on_console('Error while performing full scrape')
            if (isinstance(driver,webdriver.Ie)):
                logger.logger.print_on_console( 'Please make sure security settings are at the same level by clicking on Tools ->Internet Options -> Security tab(either all the checkboxes should be  checked or unchecked) and retry')
        return data