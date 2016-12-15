#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     10-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
import Exceptions
from utils_web import Utils
from button_link_keyword import ButtonLinkKeyword
from webconstants import *
class ElementKeywords:

    def __getelement_text(self,webelement):
        text=''
        text=webelement.text
        if text is None or text is '':
            text=webelement.get_attribute('value')
        if text is None or text is '':
            text=webelement.get_attribute('name')
        if text is None or text is '':
            text=self.__get_tooltip(webelement)
        if text is None or text is '':
            text=webelement.get_attribute('placeholder')
        if text is None or text is '':
            text=webelement.get_attribute('href')
        return text

    def __get_tooltip(self,webelement):
        return webelement.get_attribute('title')


    def get_element_text(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        text=None
        if webelement is not None:
            try:
               text=self.__getelement_text(webelement)
               status=TEST_RESULT_PASS
               methodoutput=TEST_RESULT_TRUE
            except Exception as e:
                Exceptions.error(e)
        logger.log('Result is '+text)
        return status,methodoutput,text

    def verify_element_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        if webelement is not None:
            try:
                input=input[0]
                if input is not None:
                   text=self.__getelement_text(webelement)
                   if text==input:
                       status=TEST_RESULT_PASS
                       methodoutput=TEST_RESULT_TRUE
                else:
                    logger.log('Invalid input')
            except Exception as e:
                Exceptions.error(e)
        return status,methodoutput

    def click_element(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    click_obj=ButtonLinkKeyword()
                    status,methodoutput=click_obj.click(webelement)
                else:
                    logger.log('Element is disabled')
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput

    def drag(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    obj=Utils()
                     #find the location of the element w.r.t viewport
                    location=obj.get_element_location(webelement)
                    logger.log('location is '+str(location))
                    import browser_Keywords
                    from selenium import webdriver
                    if isinstance(browser_Keywords.driver_obj,webdriver.Firefox):
                        yoffset=browser_Keywords.driver_obj.execute_script(MOUSE_HOVER_FF)
                        obj.mouse_move(int(location.get('x')+9),int(location.get('y')+yoffset))
                    else:
                        obj.enumwindows()
                        obj.mouse_move(int(location.get('x')+9),int(location.get('y')+obj.rect[1]+6))
                    import time
                    time.sleep(0.5)
                    obj.mouse_press(LEFT_BUTTON)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    logger.log('Element is disabled')
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput

    def drop(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    obj=Utils()
                     #find the location of the element w.r.t viewport
                    location=obj.get_element_location(webelement)
                    logger.log('location is '+str(location))
                    import time
                    time.sleep(0.5)
                    import browser_Keywords
                    from selenium import webdriver
                    if isinstance(browser_Keywords.driver_obj,webdriver.Firefox):
                        yoffset=browser_Keywords.driver_obj.execute_script(MOUSE_HOVER_FF)
                        obj.slide(int(location.get('x')+9),int(location.get('y')+yoffset), 0);
                    else:
                        obj.enumwindows()
                        obj.slide(int(location.get('x')+9),int(location.get('y')+obj.rect[1]+6), 0);
                    time.sleep(0.5)
                    obj.mouse_release(LEFT_BUTTON)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    logger.log('Element is disabled')
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput


    def get_tooltip_text(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        tool_tip=None
        if webelement is not None:
            try:
               tool_tip=self.__get_tooltip(webelement)
               if tool_tip is not None:
                   logger.log('Result is '+tool_tip)
                   status=TEST_RESULT_PASS
                   methodoutput=TEST_RESULT_TRUE
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput,tool_tip


    def verify_tooltip_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        if webelement is not None:
            try:
                input=input[0]
                if input is not None or input != '':
                    tool_tip=self.__get_tooltip(webelement)
                    if input==tool_tip:
                       status=TEST_RESULT_PASS
                       methodoutput=TEST_RESULT_TRUE
                else:
                    logger.log('Invalid input')

            except Exception as e:
                Exceptions.error(e)
        return status,methodoutput

    def waitforelement_visible(self,webelement,objectname,*args):
        import browser_Keywords
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if objectname is not None:
                delay=3
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.common.exceptions import TimeoutException
                from selenium.webdriver.common.by import By
                element_present = EC.presence_of_element_located((By.XPATH, objectname))
                WebDriverWait(browser_Keywords.driver_obj, delay).until(element_present)
                logger.log('Element is visible')
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except TimeoutException as e:
            logger.log('Delay timeout exceeded')
        except Exception as e:
            e_type=Exceptions.error(e)
        return status,methodoutput



