#-------------------------------------------------------------------------------
# Name:        custom
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
from selenium.common.exceptions import *

class CustomKeyword:

    def __init__(self):
        self.tagtype={'link':'a',
        'tablecell':'td',
        'textbox':'text'
        }

    def is_int(self,url):
        import re
        flag=True
        res = re.match(('-?\\d+(\\.\\d+)?'),url[0])
        if res is None:
            flag=False
        return flag

    def switch_to_parent(self):
        curr_window_handle=browser_Keywords.driver_obj.current_window_handle
        browser_Keywords.driver_obj.switch_to.window(curr_window_handle)


    def switch_to_iframe(self,url,window_handle):
        try:
            input_url=url.replace("f", "-frame");
            input_url=url.replace("i", "-iframe");
            curr_window_handle=browser_Keywords.driver_obj.current_window_handle
            if window_handle !='':
                curr_window_handle=window_handle

            logger.log('Url is '+url)
            indiframes = url.split('/')
            browser_Keywords.driver_obj.switch_to.window(curr_window_handle)
            #0i/1f
            for i in indiframes:
                if i is not '':
                    frame_iframe = 'frame'
                    j = i.rstrip(i[-1:])
                    if i[-1:] == 'i':
                        frame_iframe = 'iframe'
                        logger.log('It is  iframe')
                    else:
                        logger.log('It is  frame')
                    if j=='':
                        continue
                    browser_Keywords.driver_obj.switch_to.frame(browser_Keywords.driver_obj.find_elements_by_tag_name(frame_iframe)[int(j)])

            logger.log('Control switched to frame/iframe '+input_url)
        except WebDriverException as e:
            logger.log('Control failed to switched to frame/iframe '+input_url)



    def find_object(self,array_index, ele_type, visible_text, url, ele_index,local_index):
        return_list=browser_Keywords.driver_obj.execute_script(CUSTOM_JS,'', array_index, ele_type, visible_text, ele_index,local_index)
        if return_list[0] == 'null':
			return None
        elif return_list[0] == 'found':
            logger.log('Element is found')
            return return_list[4]
        elif return_list[0] == 'stf':
            logger.log('Debug : Inside iframe')
            iframe_ele=return_list[1]
            browser_Keywords.driver_obj.switch_to.frame(iframe_ele)

            iframe_list = browser_Keywords.driver_obj.execute_script(CUSTOM_IFRAME_JS,'', 0,ele_type, visible_text, ele_index,return_list[2])
            return_list[2]=iframe_list[2]
            if iframe_list[0]=='found':
			  logger.log('Element is found inside iframe ')
			  return iframe_list[4]
            if self.is_int(url):
                self.switch_to_iframe(url,"");
            else:
                browser_Keywords.driver_obj.switch_to.default_content()


        return self.find_object(return_list[3], ele_type, visible_text, url, ele_index,return_list[2])




    def getCustomobject(self,reference_ele,ele_type,visible_text,ele_index,url):
        custom_element=None
        logger.log('Element type is '+str(ele_type))
        logger.log('Visible text is '+str(visible_text))
        logger.log('Index is '+str(ele_index))
        if not(ele_type is None and ele_type=='' and visible_text is None and index is None):
            ele_xpath=self.getElementXPath(reference_ele)
            logger.log('Debug: reference_ele_xpath is'+str(ele_xpath))
            try:
                ele_index=int(ele_index)
                if ele_index<0:
                    logger.log('Element index should be positive ')
                else:
                    ele_type=ele_type.lower()
                    if ele_type in self.tagtype.keys():
                        ele_type=self.tagtype.get(ele_type)
                    array_index=browser_Keywords.driver_obj.execute_script(FIND_INDEX_JS,reference_ele)
                    custom_element=self.find_object(array_index, ele_type, visible_text, url, ele_index,0);
                    if custom_element is not None:
                        logger.log('Custom object is found')
                    else:
                        logger.log('Custom object not found')



            except ValueError:
                logger.log('Invalid element index')

        else:
            logger.log('Invalid input')
        return custom_element


    def getElementXPath(self,webelement):
        return browser_Keywords.driver_obj.execute_script(GET_XPATH_SCRIPT,webelement)






