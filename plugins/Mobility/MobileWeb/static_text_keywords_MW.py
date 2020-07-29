#-------------------------------------------------------------------------------
# Name:        static_text_keywords_MW.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     24-11-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger

import browser_Keywords_MW
from webconstants_MW import *
from constants import *
sourcetext= ''
import logging
log = logging.getLogger('static_text_keywords_MW.py')

class StaticTextKeywords:
    def switchtoiframe(self,mypath):
        cond_flag = False
        try:
            indiframes = mypath.split("/")
            browser_Keywords_MW.driver_obj.switch_to.default_content()
            for i in indiframes:
                if i is not '':
                    frame_iframe = IFRAME
                    j = i.rstrip(i[-1:])
                    if i[-1:] == 'f':
                        frame_iframe = FRAME
                    if (browser_Keywords_MW.driver_obj.find_elements_by_tag_name(frame_iframe)[int(j)]).is_displayed():
                        browser_Keywords_MW.driver_obj.switch_to.frame(browser_Keywords_MW.driver_obj.find_elements_by_tag_name(frame_iframe)[int(j)])
                        cond_flag = True
                    else:
                        cond_flag = False
                        break
        except Exception as e:
            log.error(e)
            cond_flag = False
        return cond_flag

    def get_source1(self,myipath):
        global sourcetext
        path = myipath
        for iframes in (list(range(len(browser_Keywords_MW.driver_obj.find_elements_by_tag_name(FRAME))))):
            path = myipath + str(iframes) + 'f' +  '/'
            if self.switchtoiframe(path):
                element = browser_Keywords_MW.driver_obj.find_element_by_tag_name(HTML)
                text = str(element.text)
                text = text.replace('\n','')
                sourcetext = sourcetext + text
                for frames in (list(range(len(browser_Keywords_MW.driver_obj.find_elements_by_tag_name(IFRAME))))):
                    inpath = path + str(frames) + 'i' +  '/'
                    if self.switchtoiframe(inpath):
                        element = browser_Keywords_MW.driver_obj.find_element_by_tag_name(HTML)
                        text = str(element.text)
                        text = text.replace('\n','')
                        sourcetext = sourcetext + text
                self.get_source1(path)

    def get_source2(self,myipath):
        global sourcetext
        path = myipath
        for iframes in (list(range(len(browser_Keywords_MW.driver_obj.find_elements_by_tag_name(IFRAME))))):
            path = myipath + str(iframes) + 'i' +  '/'
            if self.switchtoiframe(path):
                element = browser_Keywords_MW.driver_obj.find_element_by_tag_name(HTML)
                text = str(element.text)
                text = text.replace('\n','')
                sourcetext = sourcetext + text
                for frames in (list(range(len(browser_Keywords_MW.driver_obj.find_elements_by_tag_name(FRAME))))):
                    inpath = path + str(frames) + 'f' +  '/'
                    if self.switchtoiframe(inpath):
                        element = browser_Keywords_MW.driver_obj.find_element_by_tag_name(HTML)
                        text = str(element.text)
                        text = text.replace('\n','')
                        sourcetext = sourcetext + text
                self.get_source2(path)



    def verify_text_exists(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        global sourcetext
        actualtext = str(input[0])
        err_msg=None
        output=OUTPUT_CONSTANT
        text=''
        try:
            if actualtext is not None or len(actualtext) > 0:
                element = browser_Keywords_MW.driver_obj.find_element_by_tag_name(HTML)
                text = element.text
##                text = str(text)
                text = text.replace('\n','')
                sourcetext = sourcetext + text
                browser_Keywords_MW.driver_obj.switch_to.default_content()
                self.get_source1('')
                browser_Keywords_MW.driver_obj.switch_to.default_content()
                self.get_source2('')
                browser_Keywords_MW.driver_obj.switch_to.default_content()
                if actualtext in sourcetext:
                    logger.print_on_console('Text  present')
                    log.info('Text  present')
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Text not present')
                    log.error('Text not present')
            else:
                log.error(INVALID_INPUT)
                err_msg=INVALID_INPUT
                logger.print_on_console(INVALID_INPUT)
        except Exception as e:
                log.error(e)
                
                logger.print_on_console(e)
        return status,methodoutput,output,err_msg

