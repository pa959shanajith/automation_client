#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     24-11-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger
import Exceptions
import browser_Keywords
from webconstants import *

sourcetext= ''
class StaticTextKeywords:
    def switchtoiframe(self,mypath):
        cond_flag = False
        try:
            indiframes = mypath.split("/")
            browser_Keywords.driver_obj.switch_to.default_content()
            for i in indiframes:
                if i is not '':
                    frame_iframe = IFRAME
                    j = i.rstrip(i[-1:])
                    if i[-1:] == 'f':
                        frame_iframe = FRAME
                    if (browser_Keywords.driver_obj.find_elements_by_tag_name(frame_iframe)[int(j)]).is_displayed():
                        browser_Keywords.driver_obj.switch_to.frame(browser_Keywords.driver_obj.find_elements_by_tag_name(frame_iframe)[int(j)])
                        cond_flag = True
                    else:
                        cond_flag = False
                        break
        except Exception as e:
            Exceptions.error(e)
            cond_flag = False
        return cond_flag

    def get_source1(self,myipath):
        path = myipath
        for iframes in (range(len(browser_Keywords.driver_obj.find_elements_by_tag_name(FRAME)))):
            path = myipath + str(iframes) + 'f' +  '/'
            if self.switchtoiframe(path):
                element = browser_Keywords.driver_obj.find_element_by_tag_name(HTML)
                text = str(element.text)
                text = text.replace('\n','')
                global sourcetext
                sourcetext = sourcetext + text
                for frames in (range(len(browser_Keywords.driver_obj.find_elements_by_tag_name(IFRAME)))):
                    path = path + str(frames) + 'i' +  '/'
                    if self.switchtoiframe(path):
                        element = browser_Keywords.driver_obj.find_element_by_tag_name(HTML)
                        text = str(element.text)
                        text = text.replace('\n','')
                        global sourcetext
                        sourcetext = sourcetext + text
                self.get_source1(path)

    def get_source2(self,myipath):
        path = myipath
        for iframes in (range(len(browser_Keywords.driver_obj.find_elements_by_tag_name(IFRAME)))):
            path = myipath + str(iframes) + 'i' +  '/'
            if self.switchtoiframe(path):
                element = browser_Keywords.driver_obj.find_element_by_tag_name(HTML)
                text = str(element.text)
                text = text.replace('\n','')
                global sourcetext
                sourcetext = sourcetext + text
                for frames in (range(len(browser_Keywords.driver_obj.find_elements_by_tag_name(FRAME)))):
                    path = path + str(frames) + 'f' +  '/'
                    if self.switchtoiframe(path):
                        element = browser_Keywords.driver_obj.find_element_by_tag_name(HTML)
                        text = str(element.text)
                        text = text.replace('\n','')
                        global sourcetext
                        sourcetext = sourcetext + text
                self.get_source2(path)



    def verify_text_exists(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        actualtext = str(input[0])
        text=''
        try:
            if actualtext is not None or len(actualtext) > 0:
                element = browser_Keywords.driver_obj.find_element_by_tag_name(HTML)
                text = element.text
##                text = str(text)
                text = text.replace('\n','')
                global sourcetext
                sourcetext = sourcetext + text
                browser_Keywords.driver_obj.switch_to.default_content()
                self.get_source1('')
                browser_Keywords.driver_obj.switch_to.default_content()
                self.get_source2('')
                browser_Keywords.driver_obj.switch_to.default_content()
                global sourcetext
                if actualtext in sourcetext:
                    print 'Text: ', actualtext ,' found'
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    print 'Text: ', actualtext ,' not found'
        except Exception as e:
                Exceptions.error(e)
        return status,methodoutput

