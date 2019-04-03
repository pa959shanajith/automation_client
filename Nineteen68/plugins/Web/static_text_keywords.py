#-------------------------------------------------------------------------------
# Name:        static_text_keywords.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     24-11-2016
#
# Modified By: nikunj.jain (27-08-2018)
#
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger
import browser_Keywords
from webconstants import *
from constants import *
import core_utils
text_occurrences = 0
import logging
import threading
local_stk = threading.local()
##log = logging.getLogger(__name__)
##occurrences_javascript = """function occurrences(string, subString, allowOverlapping) {      string += "";     subString += "";     if (subString.length <= 0) return (string.length + 1);      var n = 0,pos = 0,step = allowOverlapping ? 1 : subString.length;      while (true) {         pos = string.indexOf(subString, pos);         if (pos >= 0) {             ++n;             pos += step;         } else break;     }     return n; }; function saddNodesOuter(sarray, scollection) { 	for (var i = 0; scollection && scollection.length && i < scollection.length; i++) { 		sarray.push(scollection[i]); 	} }; function stext_content(f) { 	var sfirstText = ''; 	var stextdisplay = ''; 	for (var z = 0; z < f.childNodes.length; z++) { 		var scurNode = f.childNodes[z]; 		swhitespace = /^\s*$/; 		if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) { 			sfirstText = scurNode.nodeValue; 			stextdisplay = stextdisplay + sfirstText; 		} 	} 	return (stextdisplay); }; var sae = []; var substr = arguments[0]; var sele = arguments.length > 1 ? arguments[1].getElementsByTagName('*') :  document.getElementsByTagName('*'); var text_occurrences = 0; saddNodesOuter(sae, sele);  for(var j=0;j<sae.length;j++){ 	stagname = sae[j].tagName.toLowerCase(); 	 	if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') { 		text_occurrences += occurrences(stext_content(sae[j]),substr); 	} 	 }; return text_occurrences;bstr = arguments[0]; var sele = arguments.length > 1 ? arguments[1].getElementsByTagName('*') :  document.getElementsByTagName('*'); var text_occurrences = 0; saddNodesOuter(sae, sele);  for(var j=0;j<sae.length;j++){ 	stagname = sae[j].tagName.toLowerCase(); 	 	if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') { 		text_occurrences += occurrences(stext_content(sae[j]),substr); 	} 	 }; return text_occurrences;"""
class StaticTextKeywords:
    def __init__(self):
        local_stk.log = logging.getLogger(__name__)
        local_stk.occurrences_javascript = """function occurrences(string, subString, allowOverlapping) {      string += "";     subString += "";     if (subString.length <= 0) return (string.length + 1);      var n = 0,pos = 0,step = allowOverlapping ? 1 : subString.length;      while (true) {         pos = string.indexOf(subString, pos);         if (pos >= 0) {             ++n;             pos += step;         } else break;     }     return n; }; function saddNodesOuter(sarray, scollection) { 	for (var i = 0; scollection && scollection.length && i < scollection.length; i++) { 		sarray.push(scollection[i]); 	} }; function stext_content(f) { 	var sfirstText = ''; 	var stextdisplay = ''; 	for (var z = 0; z < f.childNodes.length; z++) { 		var scurNode = f.childNodes[z]; 		swhitespace = /^\s*$/; 		if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) { 			sfirstText = scurNode.nodeValue; 			stextdisplay = stextdisplay + sfirstText; 		} 	} 	return (stextdisplay); }; var sae = []; var substr = arguments[0]; var sele = arguments.length > 1 ? arguments[1].getElementsByTagName('*') :  document.getElementsByTagName('*'); var text_occurrences = 0; saddNodesOuter(sae, sele);  for(var j=0;j<sae.length;j++){ 	stagname = sae[j].tagName.toLowerCase(); 	 	if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') { 		text_occurrences += occurrences(stext_content(sae[j]),substr); 	} 	 }; return text_occurrences;bstr = arguments[0]; var sele = arguments.length > 1 ? arguments[1].getElementsByTagName('*') :  document.getElementsByTagName('*'); var text_occurrences = 0; saddNodesOuter(sae, sele);  for(var j=0;j<sae.length;j++){ 	stagname = sae[j].tagName.toLowerCase(); 	 	if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') { 		text_occurrences += occurrences(stext_content(sae[j]),substr); 	} 	 }; return text_occurrences;"""

    """Method to switch to frames and iframes"""
    def switch_to_iframe(self,mypath):
        cond_flag = False
        try:
            indiframes = mypath.split("/")
            browser_Keywords.local_bk.driver_obj.switch_to.default_content()
            for i in indiframes:
                if i is not '':
                    frame_iframe = IFRAME
                    j = i.rstrip(i[-1:])
                    if i[-1:] == 'f':
                        frame_iframe = FRAME
                    if (browser_Keywords.local_bk.driver_obj.find_elements_by_tag_name(frame_iframe)[int(j)]).is_displayed():
                        browser_Keywords.local_bk.driver_obj.switch_to.frame(browser_Keywords.local_bk.driver_obj.find_elements_by_tag_name(frame_iframe)[int(j)])
                        cond_flag = True
                    else:
                        cond_flag = False
                        break
        except Exception as e:
            local_stk.log.error(e)
            cond_flag = False
        return cond_flag

    """Method to get count of text inside frames (and iframes) recursively"""
    def get_text_count_frames(self,frame_path,actual_text,coreutilsobj):
        global text_occurrences
        for frame in (list(range(len(browser_Keywords.local_bk.driver_obj.find_elements_by_tag_name(FRAME))))):
            path = frame_path + str(frame) + 'f' +  '/'
            if self.switch_to_iframe(path):
                local_stk.log.debug('switched to frame %s', path)
                try:
                    text_occurrences = text_occurrences + int(browser_Keywords.local_bk.driver_obj.execute_script(local_stk.occurrences_javascript,actual_text))
                except Exception as e:
                    local_stk.log.error(e)
                self.get_text_count_frames(path,actual_text,coreutilsobj)
                self.get_text_count_iframes(path,actual_text,coreutilsobj)
            else:
                local_stk.log.info('could not switch to frame %s', path)

    """Method to get count of text inside iframes (and frames) recursively"""
    def get_text_count_iframes(self,iframe_path,actual_text,coreutilsobj):
        global text_occurrences
        for iframe in (list(range(len(browser_Keywords.local_bk.driver_obj.find_elements_by_tag_name(IFRAME))))):
            path = iframe_path + str(iframe) + 'i' +  '/'
            if self.switch_to_iframe(path):
                local_stk.log.debug('switched to iframe %s', path)
                try:
                    text_occurrences = text_occurrences + int(browser_Keywords.local_bk.driver_obj.execute_script(local_stk.occurrences_javascript,actual_text))
                except Exception as e:
                    local_stk.log.error(e)
                self.get_text_count_iframes(path,actual_text,coreutilsobj)
                self.get_text_count_frames(path,actual_text,coreutilsobj)
            else:
                local_stk.log.info('could not switch to iframe %s', path)


    def verify_text_exists(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        actual_text=input[0]
        coreutilsobj=core_utils.CoreUtils()
        actual_text=coreutilsobj.get_UTF_8(actual_text)
        err_msg=None
        output=OUTPUT_CONSTANT
        global text_occurrences
        try:
            if actual_text is not None and len(actual_text) > 0:
                if webelement == None:
                    text_occurrences = text_occurrences + int(browser_Keywords.local_bk.driver_obj.execute_script(local_stk.occurrences_javascript,actual_text))
                    browser_Keywords.local_bk.driver_obj.switch_to.default_content()
                    self.get_text_count_frames('',actual_text,coreutilsobj)
                    browser_Keywords.local_bk.driver_obj.switch_to.default_content()
                    self.get_text_count_iframes('',actual_text,coreutilsobj)
                    browser_Keywords.local_bk.driver_obj.switch_to.default_content()
                else:
                    text_occurrences = text_occurrences + int(browser_Keywords.local_bk.driver_obj.execute_script(local_stk.occurrences_javascript,actual_text,webelement))

                if text_occurrences != 0:
                    logger.print_on_console('Text is present')
                    local_stk.log.info('Text is present')
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                    output = text_occurrences
                    logger.print_on_console('No. of occurrences of the text ',actual_text, ' is ',str(text_occurrences),' time(s).')
                else:
                    output = 0
                    logger.print_on_console('Text is not present')
                    local_stk.log.error('Text is not present')
                text_occurrences = 0
            else:
                local_stk.log.error(INVALID_INPUT)
                err_msg=INVALID_INPUT
                logger.print_on_console(INVALID_INPUT)
        except Exception as e:
                local_stk.log.error(e)
                logger.print_on_console(e)
        return status,methodoutput,output,err_msg

