#-------------------------------------------------------------------------------
# Name:        custom_keyword_MW.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     29-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger
import browser_Keywords_MW
from webconstants_MW import *
from constants import *
from selenium.common.exceptions import *

import logging


log = logging.getLogger('custom_keyword_MW.py')

class CustomKeyword:

    def __init__(self):
        self.tagtype={'link':'a',
        'tablecell':'td',
        'textbox':'text',
        'radiobutton':'radio',
        'textbox':'text',
        }
        self.object_count_flag={'dropdown':0,
                            'listbox':1}
        self.list_flag=0

    def is_int(self,url):
        import re
        flag=True
        res = re.match(('-?\\d+(\\.\\d+)?'),url[0])
        log.debug('The url is '+url)
        if res is None:
            flag=False
        log.debug('It is a frame/iframe ')
        log.debug(flag)
        return flag

    def switch_to_parent(self):
        log.debug('Switching to Parent')
        curr_window_handle=browser_Keywords_MW.driver_obj.current_window_handle
        browser_Keywords_MW.driver_obj.switch_to.window(curr_window_handle)
        log.debug('Switched to Parent ')
        log.debug('curr_window_handle')


    def switch_to_iframe(self,url,window_handle):
        try:
            input_url=url.replace("f", "-frame");
            input_url=url.replace("i", "-iframe");
            curr_window_handle=browser_Keywords_MW.driver_obj.current_window_handle
            if window_handle !='':
                curr_window_handle=window_handle

##            logger.print_on_console('Url is '+url)
            indiframes = url.split('/')
            browser_Keywords_MW.driver_obj.switch_to.window(curr_window_handle)
            #0i/1f
            for i in indiframes:
                if i is not '':
                    frame_iframe = 'frame'
                    j = i.rstrip(i[-1:])
                    if i[-1:] == 'i':
                        frame_iframe = 'iframe'
##                    logger.print_on_console('It is '+frame_iframe)
                    if j=='':
                        continue
                    browser_Keywords_MW.driver_obj.switch_to.frame(browser_Keywords_MW.driver_obj.find_elements_by_tag_name(frame_iframe)[int(j)])
            log_msg='Control switched to frame/iframe '+input_url
##            logger.print_on_console(log_msg)
            log.info(log_msg)
        except WebDriverException as e:
            err_msg='Control failed to switched to frame/iframe '+input_url
            log.error(err_msg)
            logger.print_on_console(err_msg)



    def find_object(self,array_index, ele_type, visible_text, url, ele_index,local_index):
        return_list=browser_Keywords_MW.driver_obj.execute_script(CUSTOM_JS,'', array_index, ele_type, visible_text, ele_index,local_index)
        if return_list[0] == 'null':
            return None
        elif return_list[0] == FOUND:
            logger.print_on_console(WEB_ELEMENT_FOUND)
            return return_list[4]
        elif return_list[0] == 'stf':
            log.debug('Inside iframe/frame')
            iframe_ele=return_list[1]
            browser_Keywords_MW.driver_obj.switch_to.frame(iframe_ele)

            iframe_list = browser_Keywords_MW.driver_obj.execute_script(CUSTOM_IFRAME_JS,'', 0,ele_type, visible_text, ele_index,return_list[2])
            return_list[2]=iframe_list[2]
            if iframe_list[0]==FOUND:
                logger.print_on_console(WEB_ELEMENT_FOUND_INSIDE_IFRAME)
                log.info(WEB_ELEMENT_FOUND_INSIDE_IFRAME)
                return iframe_list[4]
            if self.is_int(url):
                self.switch_to_iframe(url,"");
            else:
                browser_Keywords_MW.driver_obj.switch_to.default_content()


        return self.find_object(return_list[3], ele_type, visible_text, url, ele_index,return_list[2])




    def getCustomobject(self,reference_ele,ele_type,visible_text,ele_index,url):
        custom_element=None
        msg1='Element type is '+str(ele_type)
        msg2='Visible text is '+str(visible_text)
        msg3='Index is '+str(ele_index)

        logger.print_on_console(msg1)
        log.info(msg1)
        logger.print_on_console(msg2)
        log.info(msg1)
        logger.print_on_console(msg3)
        log.info(msg3)

        if not(ele_type is None or ele_type=='' or visible_text is None or ele_index is None):
            ele_xpath=self.getElementXPath(reference_ele)
            logger.print_on_console('Debug: reference_ele_xpath is'+str(ele_xpath))
            try:
                ele_index=int(ele_index)
                if ele_index<0:
                    logger.print_on_console(ERROR_CODE_DICT['ERR_NEGATIVE_ELEMENT_INDEX'])
                else:
                    ele_type=ele_type.lower()
                    if ele_type in self.tagtype.keys():
                        ele_type=self.tagtype.get(ele_type)
                    array_index=browser_Keywords_MW.driver_obj.execute_script(FIND_INDEX_JS,reference_ele)
                    custom_element=self.find_object(array_index, ele_type, visible_text, url, ele_index,0);
                    if custom_element is not None:
                        logger.print_on_console(MSG_CUSTOM_FOUND)
                        log.info(MSG_CUSTOM_FOUND)
                    else:
                        logger.print_on_console(ERROR_CODE_DICT['ERR_CUSTOM_NOTFOUND'])
                        log.info(ERROR_CODE_DICT['ERR_CUSTOM_NOTFOUND'])



            except ValueError:
                log.error(INVALID_INPUT)
                logger.print_on_console(ERROR_CODE_DICT['ERR_NUMBER_FORMAT_EXCEPTION'])

        else:
            logger.print_on_console(INVALID_INPUT)
        return custom_element


    def get_object_count(self,reference_ele,ele_type):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        count=None
        ele_type=ele_type[0]
        err_msg=None
        msg1='Element type is '+str(ele_type)
        logger.print_on_console(msg1)
        log.info(msg1)
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:

            if not(ele_type is None or ele_type==''):
                ele_type=str(ele_type)
                ele_xpath=self.getElementXPath(reference_ele)
                log.debug('reference_ele_xpath is'+str(ele_xpath))

                ele_type=ele_type.lower()
                if ele_type in self.tagtype.keys():
                    ele_type=self.tagtype.get(ele_type)
                elif ele_type=='dropdown' or ele_type=='listbox':
                    self.list_flag=self.object_count_flag[ele_type]
                    ele_type='select'

                array_index=browser_Keywords_MW.driver_obj.execute_script(FIND_INDEX_JS,reference_ele)
                if array_index!= None:
                    count=self.get_count(0, ele_type,array_index)


                if count is not None:
                    logger.print_on_console('Number of objects found is ',count)
                    log.info('Number of objects found is ')
                    log.info(count)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Count is ',count)
                    log.info('Count is ')
                    log.info(count)

            else:
                logger.print_on_console(INVALID_INPUT)
                err_msg=INVALID_INPUT
                log.error(INVALID_INPUT)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']


        return status,methodoutput,count,err_msg

    def get_count(self,counter,ele_type,index):
        result=browser_Keywords_MW.driver_obj.execute_script(GET_OBJECT_COUNT_JS,counter,ele_type,index,self.list_flag)
        counter=result[0]
        index=result[2]
        index=index+1
        if len(result)>3:
            if result[3]=='done':
                return counter
        if result[1]!= None:
            counter=self.get_count_iframe(result[1],counter,ele_type);
        else:
            return counter


        return self.get_count(counter,ele_type,index)



    def get_count_iframe(self,iframe_ele,counter,ele_type):

        log.debug('Inside get_count_iframe method')
        browser_Keywords_MW.driver_obj.switch_to.frame(iframe_ele)
        req_elements = None
        index=0
        counter=self.get_count(counter, ele_type,index, self.list_flag)
        browser_Keywords_MW.driver_obj.switch_to.parent_frame()
        return counter




    def getElementXPath(self,webelement):
        try:
            return browser_Keywords_MW.driver_obj.execute_script(GET_XPATH_SCRIPT,webelement)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)






