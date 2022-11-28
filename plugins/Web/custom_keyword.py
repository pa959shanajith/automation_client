#-------------------------------------------------------------------------------
# Name:        custom_keyword.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     29-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger
import browser_Keywords
from webconstants import *
from constants import *
from selenium.common.exceptions import *
import core_utils
import logging
import threading
import time
import readconfig
from selenium.webdriver.common.by import By

local_ck = threading.local()

class CustomKeyword:

    def __init__(self):
        self.tagtype={'link':'a',
        'tablecell':'td',
        'textbox':'text',
        'radiobutton':'radio'
        }
        self.object_count_flag={'dropdown':0,
                            'listbox':1}
        self.list_flag=0
        local_ck.log = logging.getLogger('custom_keyword.py')

    def is_int(self,url):
        import re
        flag=True
        res = re.match(('-?\\d+(\\.\\d+)?'),url[0])
        local_ck.log.debug('The url is '+url)
        if res is None:
            flag=False
        local_ck.log.debug('It is a frame/iframe ')
        local_ck.log.debug(flag)
        return flag

    def switch_to_parent(self):
        local_ck.log.debug('Switching to Parent')
        curr_window_handle=browser_Keywords.local_bk.driver_obj.current_window_handle
        browser_Keywords.local_bk.driver_obj.switch_to.window(curr_window_handle)
        local_ck.log.debug('Switched to Parent ')
        local_ck.log.debug('curr_window_handle')


    def switch_to_iframe(self,url,window_handle,flag=False):
        configvalues = readconfig.configvalues
        try:
            if url.find('frame') != -1 or url.find('iframe') != -1:
                browser_Keywords.local_bk.driver_obj.switch_to.frame(browser_Keywords.local_bk.driver_obj.find_elements_by_xpath(url)[0])
                log_msg='Control switched to frame/iframe '
                logger.print_on_console(log_msg)
                local_ck.log.info(log_msg)
            else:
                input_url=url.replace("f", "-frame")
                input_url=url.replace("i", "-iframe")
                curr_window_handle=browser_Keywords.local_bk.driver_obj.current_window_handle
                if window_handle !='':
                    curr_window_handle=window_handle
                logger.print_on_console('Url is '+url)
                indiframes = url.split('/')
                browser_Keywords.local_bk.driver_obj.switch_to.window(curr_window_handle)
                #0i/1f
                for i in indiframes:
                    if i is not '':
                        frame_iframe = 'frame'
                        j = i.rstrip(i[-1:])
                        if i[-1:] == 'i':
                            frame_iframe = 'iframe'
                        logger.print_on_console('It is '+frame_iframe)
                        if j=='':
                            continue
                        if flag:
                            delay=int(configvalues['timeOut'])
                            start = time.time()
                            # fix for issue #4336
                            while delay and not (len(browser_Keywords.local_bk.driver_obj.find_elements_by_tag_name(frame_iframe))>=int(j)) and time.time() - start < delay:
                                continue
                        browser_Keywords.local_bk.driver_obj.switch_to.frame(browser_Keywords.local_bk.driver_obj.find_elements_by_tag_name(frame_iframe)[int(j)])
                log_msg='Control switched to frame/iframe '+input_url
                logger.print_on_console(log_msg)
                local_ck.log.info(log_msg)
        except WebDriverException as e:
            err_msg='Control failed to switch to frame/iframe '+input_url
            local_ck.log.error(err_msg)
            logger.print_on_console(err_msg)

    def find_object(self,array_index, ele_type, visible_text, url, ele_index,local_index,absMatch):
        return_list=browser_Keywords.local_bk.driver_obj.execute_script(CUSTOM_JS,'', array_index, ele_type, visible_text, ele_index,local_index,absMatch)
        if return_list[0] == 'null':
            return None
        elif return_list[0] == FOUND:
            logger.print_on_console(WEB_ELEMENT_FOUND)
            return return_list[4]
        elif return_list[0] == 'stf':
            local_ck.log.debug('Inside iframe/frame')
            iframe_ele=return_list[1]
            browser_Keywords.local_bk.driver_obj.switch_to.frame(iframe_ele)
            iframe_list = browser_Keywords.local_bk.driver_obj.execute_script(CUSTOM_IFRAME_JS,'', 0,ele_type, visible_text, ele_index,return_list[2])
            return_list[2]=iframe_list[2]
            if iframe_list[0]==FOUND:
                logger.print_on_console(WEB_ELEMENT_FOUND_INSIDE_IFRAME)
                local_ck.log.info(WEB_ELEMENT_FOUND_INSIDE_IFRAME)
                return iframe_list[4]
            if self.is_int(url):
                self.switch_to_iframe(url,"");
            else:
                browser_Keywords.local_bk.driver_obj.switch_to.default_content()
        return self.find_object(return_list[3], ele_type, visible_text, url, ele_index,return_list[2],absMatch)


    def getCustomobject(self,reference_ele,ele_type,visible_text,ele_index,url,absMatch):
        import web_dispatcher
        finalXpath = web_dispatcher.finalXpath
        custom_element=None
        msg1='Element type is '+str(ele_type)
        coreutilsobj=core_utils.CoreUtils()
        visible_text=coreutilsobj.get_UTF_8(visible_text)
        msg2='Visible text is '+visible_text
##        msg2='Visible text is '+str(visible_text)
        msg3='Index is '+str(ele_index)
        logger.print_on_console(msg1)
        local_ck.log.info(msg1)
        logger.print_on_console(msg2)
        local_ck.log.info(msg2)
        logger.print_on_console(msg3)
        local_ck.log.info(msg3)
        if not ele_type in list(self.tagtype.keys()):
            if visible_text!='':
                if reference_ele.get_attribute('role')!='option':
                    try:
                        dropDown =  reference_ele.find_element_by_tag_name('UL')
                    except:
                        dropDown = reference_ele
                else:
                    dropDown = reference_ele.find_element(By.XPATH,'..')
                rows = dropDown.find_elements(By.XPATH,'*')
                for row in rows:
                    if row.get_attribute('outerText')[::-1].find(visible_text[::-1])==0:
                        custom_element=row
                        break
            else:
                if reference_ele.get_attribute('role')!='option':
                    try:
                        dropDown =  reference_ele.find_element_by_tag_name('UL')
                    except:
                        dropDown = reference_ele
                    rows = dropDown.find_elements(By.XPATH,'*')
                    custom_element = rows[int(ele_index)]
                else:
                    childIndex = str(int(finalXpath[finalXpath.rindex('[')+1:-1])+int(ele_index))
                    finalXpath = finalXpath[:finalXpath.rindex('[')] +'['+ childIndex+ ']'
                    custom_element = browser_Keywords.local_bk.driver_obj.find_elements_by_xpath(finalXpath)[0]
        
        elif not(ele_type is None or ele_type=='' or visible_text is None or ele_index is None):
            #Commneting the getElementXPath script since it was freezing the application in MNT.
            #As of now, it's a hot fix for MNT to make sure custom keywords do not impact the application functionality
            #ele_xpath=self.getElementXPath(reference_ele)
            #logger.print_on_console('Debug: reference_ele_xpath is'+str(ele_xpath))
            try:
                ele_index=int(ele_index)
                if ele_index<0:
                    logger.print_on_console(ERROR_CODE_DICT['ERR_NEGATIVE_ELEMENT_INDEX'])
                else:
                    ele_type=ele_type.lower()
                    if ele_type in list(self.tagtype.keys()):
                        ele_type=self.tagtype.get(ele_type)
                    array_index=browser_Keywords.local_bk.driver_obj.execute_script(FIND_INDEX_JS,reference_ele)
                    custom_element=self.find_object(array_index, ele_type, visible_text, url, ele_index,0,absMatch);
                    if custom_element is not None:
                        logger.print_on_console(MSG_CUSTOM_FOUND)
                        local_ck.log.info(MSG_CUSTOM_FOUND)
                    else:
                        logger.print_on_console(ERROR_CODE_DICT['ERR_CUSTOM_NOTFOUND'])
                        local_ck.log.info(ERROR_CODE_DICT['ERR_CUSTOM_NOTFOUND'])
            except ValueError:
                local_ck.log.error(INVALID_INPUT)
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
        local_ck.log.info(msg1)
        local_ck.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if not(ele_type is None or ele_type==''):
                ele_type=str(ele_type)
                ele_xpath=self.getElementXPath(reference_ele)
                local_ck.log.debug('reference_ele_xpath is'+str(ele_xpath))
                ele_type=ele_type.lower()
                if ele_type in list(self.tagtype.keys()):
                    ele_type=self.tagtype.get(ele_type)
                elif ele_type=='dropdown' or ele_type=='listbox':
                    self.list_flag=self.object_count_flag[ele_type]
                    ele_type='select'
                array_index=browser_Keywords.local_bk.driver_obj.execute_script(FIND_INDEX_JS,reference_ele)
                if array_index!= None:
                    count=self.get_count(0, ele_type,array_index)
                if count is not None:
                    logger.print_on_console('Number of objects found is ',count)
                    local_ck.log.info('Number of objects found is ')
                    local_ck.log.info(count)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Count is ',count)
                    local_ck.log.info('Count is ')
                    local_ck.log.info(count)
            else:
                logger.print_on_console(INVALID_INPUT)
                err_msg=INVALID_INPUT
                local_ck.log.error(INVALID_INPUT)
        except Exception as e:
            local_ck.log.error(e)

            logger.print_on_console(e)
            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        return status,methodoutput,count,err_msg


    def get_object(self,reference_ele,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output= None
        if reference_ele:
            local_ck.log.info("Cutom object found")
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
            output=reference_ele
        else:
            local_ck.log.info("Custom object not found")
        return status,methodoutput,reference_ele,err_msg

    def get_count(self,counter,ele_type,index,*args):
        result=browser_Keywords.local_bk.driver_obj.execute_script(GET_OBJECT_COUNT_JS,counter,ele_type,index,self.list_flag)
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

        local_ck.log.debug('Inside get_count_iframe method')
        browser_Keywords.local_bk.driver_obj.switch_to.frame(iframe_ele)
        req_elements = None
        index=0
        counter=self.get_count(counter, ele_type,index, self.list_flag)
        browser_Keywords.local_bk.driver_obj.switch_to.parent_frame()
        return counter




    def getElementXPath(self,webelement):
        try:
            return browser_Keywords.local_bk.driver_obj.execute_script(GET_XPATH_SCRIPT,webelement)
        except Exception as e:
            local_ck.log.error(e)
            logger.print_on_console(e)






