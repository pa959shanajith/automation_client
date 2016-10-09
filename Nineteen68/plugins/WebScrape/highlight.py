#-------------------------------------------------------------------------------
# Name:        highlight.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     29-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import Exceptions
import domconstants
import clickandadd
import time
import browserops
import fullscrape
import logger
status =domconstants.STATUS_FAIL
currentdriverhandle = ''
class Highlight():
    def highlight(self,data):
        try:
            logger.log('FILE: highlight.py , DEF: highlight() , MSG: Inside highlight method .....')
            driver = browserops.driver
            currentdriverhandle = clickandadd.currenthandle
            logger.log('FILE: highlight.py , DEF: highlight() , MSG: Obtained browser handle and driver from browserops.py class ......')
            if currentdriverhandle is  '' or currentdriverhandle is  None:
                currentdriverhandle = fullscrape.currenthandle
            #Split the string with delimiter ','
            highele = data.split(',')
            # find out if the highele[1] has id or name attrib
            identifiers = highele[1].split(';')
            url = highele[2]
            def highlight1(element):
                logger.log('FILE: highlight.py , DEF: highlight() , MSG: Inside highlight1 method .....')
                if element is not None:
                    """Highlights (blinks) a Selenium Webdriver element"""
                    def apply_style(s, sec):
                        logger.log('FILE: highlight.py , DEF: apply_style() , MSG: Inside apply_style method .....')
                        if driver.name == 'internet explorer' :
                            logger.log('FILE: highlight.py , DEF: apply_style() , MSG: Before applying color to the element in IE browser .....')
                            driver.execute_script("arguments[0].style.setAttribute('cssText', arguments[1]);",
                                              element, s)
                            logger.log('FILE: highlight.py , DEF: apply_style() , MSG: Applied color to the element in IE browser .....')
                        else:
                            logger.log('FILE: highlight.py , DEF: apply_style() , MSG: Before applying color to the element in chrome/firefox browser .....')
                            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                              element, s)
                            logger.log('FILE: highlight.py , DEF: apply_style() , MSG: Applied color to the element in chrome/firefox browser .....')
                        time.sleep(sec)
                    logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Before getting the original style .....')
                    original_style = element.get_attribute('style')
                    logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Original style obtained.....')
                    logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Before highlighting .....')
                    apply_style(original_style + "background: #fff300; border: 2px solid #cc3300;outline: 2px solid #fff300;", 3)
                    logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Element highlighted .....')
                    if (driver.capabilities['version'] != unicode(8)):
                        logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Before removing the style for ie8 .....')
                        apply_style(original_style, 0)
                        logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Removed the style for ie8 .....')
                    else:
                        logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Before removing the style for other browsers .....')
                        apply_style(original_style + "background: 0; border: 0px none 0; outline: none", 0)
                        logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Removed the style for other browsers .....')

            def is_int(url):
                try:
                    int(url[0])
                    logger.log('FILE: highlight.py , DEF: is_int() , MSG: The url is an iframe/frmae url .....')
                    return True
                except ValueError:
                    logger.log('FILE: highlight.py , DEF: is_int() , MSG: The url is an normal webpage url .....')
                    return False

            if is_int(url):
                logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Splitting Iframe/frame url by /')
                indiframes = url.split("/")
                driver.switch_to.window(currentdriverhandle)
                logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Switched to current window handle')
                for i in indiframes:
                    if i is not '':
                        frame_iframe = 'frame'
                        j = i.rstrip(i[-1:])
                        if i[-1:] == 'i':
                            frame_iframe = 'iframe'
                            logger.log('FILE: highlight.py , DEF: highlight1() , MSG: It is  iframe')
                        else:
                            logger.log('FILE: highlight.py , DEF: highlight1() , MSG: It is  frame')
                        driver.switch_to.frame(driver.find_elements_by_tag_name(frame_iframe)[int(j)])
                        logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Switched to frame/iframe')

                try:
                    #find by rxpath
                    tempwebElement = driver.find_elements_by_xpath(identifiers[0])
                    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                    webElement = tempwebElement
                except Exception as webEx:
                    try:
                        #find by id
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                        webElement = tempwebElement
                    except Exception as webEx:
                        try:
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                            webElement = tempwebElement
                        except Exception as webEx:
                            webElement = None
                if webElement is not None:
                    logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Element found inside frame/iframe .....')
                    highlight1(webElement[0])
                try:
##                            driver.switch_to.default_content()
                    driver.switch_to.window(currentdriverhandle)
                except Exception as e4:
                    evb = e4

            else:
                try:
##                            driver.switch_to.default_content()
                    driver.switch_to.window(currentdriverhandle)
                except Exception as e4:
                    evb = e4
                try:
                    tempwebElement = driver.find_elements_by_xpath(identifiers[0])
                    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                    webElement = tempwebElement
                except Exception as webEx:
                    try:
                        #find by id
                        tempwebElement = driver.find_elements_by_id(identifiers[1])
                        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                        webElement = tempwebElement
                    except Exception as webEx:
                        try:
                            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
                            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                                tempwebElement = None
                            webElement = tempwebElement
                        except Exception as webEx:
                            webElement = None
                if webElement is not None:
                    logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Element found inside main page .....')
                    highlight1(webElement[0])
                    print 'Highlight method executed'
                    try:
                        driver.switch_to.window(currentdriverhandle)
                    except Exception as e4:
                        evb = e4

            status = domconstants.STATUS_SUCCESS
        except Exception as e:
            Exceptions.error(e)
            status= domconstants.STATUS_FAIL
        logger.log('FILE: highlight.py , DEF: highlight1() , MSG: Highlight method execution done ')
        return status


