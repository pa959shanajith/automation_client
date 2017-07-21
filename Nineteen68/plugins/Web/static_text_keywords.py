#-------------------------------------------------------------------------------
# Name:        static_text_keywords.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     24-11-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger

import browser_Keywords
from webconstants import *
from constants import *
##import ftfy
import core_utils
sourcetext= ''
separator = '~@~'
import logging
log = logging.getLogger('static_text_keywords.py')
tags = ['html','body','form','meta','script','head','style','link','noscript']
text_javascript = """function stext_content(f) {     var sfirstText = '';     var stextdisplay = '';     for (var z = 0; z < f.childNodes.length; z++) {         var scurNode = f.childNodes[z];         swhitespace = /^\s*$/;         if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) {             sfirstText = scurNode.nodeValue;             stextdisplay = stextdisplay + sfirstText;         }     }     return (stextdisplay); }; return stext_content(arguments[0])"""
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
        global sourcetext
        path = myipath
        for iframes in (range(len(browser_Keywords.driver_obj.find_elements_by_tag_name(FRAME)))):
            path = myipath + str(iframes) + 'f' +  '/'
            if self.switchtoiframe(path):
                elements = browser_Keywords.driver_obj.find_elements_by_tag_name("*")
                for element in elements:
                    try:
                        if element.tag_name.lower() not in tags:
                            text = browser_Keywords.driver_obj.execute_script(text_javascript,element)
##                            import ftfy
##                            text = ftfy.fix_text(text)
                            text = text.replace('\n','')
                            text = text.strip()
                            if len(text) != 0:
                                sourcetext = sourcetext + separator + text
                    except Exception as e:
                        print e
                for frames in (range(len(browser_Keywords.driver_obj.find_elements_by_tag_name(IFRAME)))):
                    inpath = path + str(frames) + 'i' +  '/'
                    if self.switchtoiframe(inpath):
                        elements = browser_Keywords.driver_obj.find_elements_by_tag_name("*")
                        for element in elements:
                            try:
                                if element.tag_name.lower() not in tags:
                                    text = browser_Keywords.driver_obj.execute_script(text_javascript,element)
##                                    import ftfy
##                                    text = ftfy.fix_text(text)
                                    text = text.replace('\n','')
                                    text = text.strip()
                                    if len(text) != 0:
                                        sourcetext = sourcetext + separator + text
                            except Exception as e:
                                print e
                    self.get_source1(ipath)
                for frames in (range(len(browser_Keywords.driver_obj.find_elements_by_tag_name(FRAME)))):
                    inpath = path + str(frames) + 'f' +  '/'
                    if self.switchtoiframe(inpath):
                        elements = browser_Keywords.driver_obj.find_elements_by_tag_name("*")
                        for element in elements:
                            try:
                                if element.tag_name.lower() not in tags:
                                    text = browser_Keywords.driver_obj.execute_script(text_javascript,element)
##                                    import ftfy
##                                    text = ftfy.fix_text(text)
                                    text = text.replace('\n','')
                                    text = text.strip()
                                    if len(text) != 0:
                                        sourcetext = sourcetext + separator + text
                            except Exception as e:
                                print e
                    self.get_source1(ipath)
                self.get_source1(path)


    def get_source2(self,myipath):
        global sourcetext
        path = myipath
        for iframes in (range(len(browser_Keywords.driver_obj.find_elements_by_tag_name(IFRAME)))):
            path = myipath + str(iframes) + 'i' +  '/'
            if self.switchtoiframe(path):
                elements = browser_Keywords.driver_obj.find_elements_by_tag_name("*")
                for element in elements:
                    try:
                        if element.tag_name.lower() not in tags:
                            text = browser_Keywords.driver_obj.execute_script(text_javascript,element)
##                            import ftfy
##                            text = ftfy.fix_text(text)
                            text = text.replace('\n','')
                            text = text.strip()
                            if len(text) != 0:
                                sourcetext = sourcetext + separator + text
                    except Exception as e:
                        print e
                for frames in (range(len(browser_Keywords.driver_obj.find_elements_by_tag_name(FRAME)))):
                    inpath = path + str(frames) + 'f' +  '/'
                    if self.switchtoiframe(inpath):
                       elements = browser_Keywords.driver_obj.find_elements_by_tag_name("*")
                       for element in elements:
                            try:
                                if element.tag_name.lower() not in tags:
                                    text = browser_Keywords.driver_obj.execute_script(text_javascript,element)
##                                    import ftfy
##                                    text = ftfy.fix_text(text)
                                    text = text.replace('\n','')
                                    text = text.strip()
                                    if len(text) != 0:
                                        sourcetext = sourcetext + separator + text
                            except Exception as e:
                                print e
                    self.get_source2(inpath)
                for frames in (range(len(browser_Keywords.driver_obj.find_elements_by_tag_name(IFRAME)))):
                    inpath = path + str(frames) + 'i' +  '/'
                    if self.switchtoiframe(inpath):
                       elements = browser_Keywords.driver_obj.find_elements_by_tag_name("*")
                       for element in elements:
                            try:
                                if element.tag_name.lower() not in tags:
                                    text = browser_Keywords.driver_obj.execute_script(text_javascript,element)
##                                    import ftfy
##                                    text = ftfy.fix_text(text)
                                    text = text.replace('\n','')
                                    text = text.strip()
                                    if len(text) != 0:
                                        sourcetext = sourcetext + separator + text
                            except Exception as e:
                                print e
                    self.get_source2(inpath)
                self.get_source2(path)



    def verify_text_exists(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        global sourcetext
##        actualtext = str(input[0])
        actualtext=input[0]
        coreutilsobj=core_utils.CoreUtils()
        actualtext=coreutilsobj.get_UTF_8(actualtext)
        err_msg=None
        output=OUTPUT_CONSTANT
        text=''
        text_count = 0
        countflag = False
        if webelement == None:
            try:
                if actualtext is not None or len(actualtext) > 0:
                    elements = browser_Keywords.driver_obj.find_elements_by_tag_name("*")
                    for element in elements:
                        try:
                            if element.tag_name.lower()  not in tags:
                                text = browser_Keywords.driver_obj.execute_script(text_javascript,element)
##                                import ftfy
##                                text = ftfy.fix_text(text)
                                text = text.replace('\n','')
                                text = text.strip()
                                if len(text) != 0:
                                    sourcetext = sourcetext + separator + text
                        except Exception as e:
                            print e
                    browser_Keywords.driver_obj.switch_to.default_content()
                    self.get_source1('')
                    browser_Keywords.driver_obj.switch_to.default_content()
                    self.get_source2('')
                    browser_Keywords.driver_obj.switch_to.default_content()

    ##                sourcetext = ftfy.fix_text(sourcetext)
                    texts = sourcetext.split('~@~')
                    log.info('texts array :')
                    log.info(texts)
                    for i in texts:
                        i=coreutilsobj.get_UTF_8(i)
                        if actualtext in i:
                            countflag = True
                            cnt = i.count(actualtext)
                            text_count = text_count + cnt

                    sourcetext = ''

                    if countflag:
                        logger.print_on_console('Text  present')
                        log.info('Text  present')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        output = text_count
                        logger.print_on_console('No. of occurance of the text ',actualtext, ' is ',str(text_count),' time(s).')
                    else:
                        output = 0
                        logger.print_on_console('Text not present')
                        log.error('Text not present')
                else:
                    log.error(INVALID_INPUT)
                    err_msg=INVALID_INPUT
                    logger.print_on_console(INVALID_INPUT)
            except Exception as e:
                    import traceback
                    traceback.print_exc()
                    log.error(e)
                    logger.print_on_console(e)
        else:
            try:
                if actualtext is not None or len(actualtext) > 0:
                    elements = webelement.find_elements_by_tag_name("*")
                    for element in elements:
                        if element.tag_name.lower()  not in tags:
                            text = browser_Keywords.driver_obj.execute_script(text_javascript,element)
##                            import ftfy
##                            text = ftfy.fix_text(text)
                            text = text.replace('\n','')
                            text = text.strip()
                            if len(text) != 0:
                                sourcetext = sourcetext + separator + text
                            texts = sourcetext.split('~@~')
                            log.info('texts array :')
                            log.info(texts)
                            for i in texts:
                                i=coreutilsobj.get_UTF_8(i)
                                if actualtext in i:
                                    countflag = True
                                    cnt = i.count(actualtext)
                                    text_count = text_count + cnt

                            sourcetext = ''
                    if countflag:
                        logger.print_on_console('Text  present')
                        log.info('Text  present')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        output = text_count
                        logger.print_on_console('No. of occurance of the text ',actualtext, ' is ',str(text_count),' time(s).')
                    else:
                        output = 0
                        logger.print_on_console('Text not present')
                        log.error('Text not present')
                else:
                    log.error(INVALID_INPUT)
                    err_msg=INVALID_INPUT
                    logger.print_on_console(INVALID_INPUT)
            except Exception as e:
                print e
        return status,methodoutput,output,err_msg

