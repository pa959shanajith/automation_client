#-------------------------------------------------------------------------------
# Name:        radio_checkbox_operations.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     08-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import selenium
import logger
import browser_Keywords
from utilweb_operations import UtilWebKeywords
import table_keywords
import webconstants
from constants import *
import logging

log = logging.getLogger('radio_checkbox_operations.py')

class RadioCheckboxKeywords():

    def __init__(self):
        self.utilobj=UtilWebKeywords()
        self.status={'radio':'Selected',
                    'checkbox':'Checked'}

    def __element_disabled(self):
        err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
        logger.print_on_console(err_msg)
        log.error(err_msg)
        return err_msg

    def __web_driver_exception(self,e):
        log.error(e)
        logger.print_on_console(e)
        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        return err_msg


    def select_radiobutton(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        visibilityFlag=True
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    log.debug(WEB_ELEMENT_ENABLED)
                    is_visible=self.utilobj.is_visible(webelement)
                    if len(args)>0:
                        visibilityFlag=args[0]
                    if not(visibilityFlag and is_visible):
                        browser_Keywords.driver_obj.execute_script(webconstants.CLICK_RADIO_CHECKBOX,webelement)
                    else:
                        webelement.click()
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=self.__element_disabled()
            except Exception as e:
                err_msg=self.__web_driver_exception(e)

        return status,methodoutput,output,err_msg


    def select_checkbox(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    log.debug(WEB_ELEMENT_ENABLED)
                    if not(webelement.is_selected()):
                        is_visble=self.utilobj.is_visible(webelement)
                        if len(args)>0:
                            visibilityFlag=args[0]
                        if not(visibilityFlag and is_visble ):
                            browser_Keywords.driver_obj.execute_script(webconstants.CLICK_RADIO_CHECKBOX,webelement)
                        else:
                            webelement.click()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_OBJECTSELECTED']
                        logger.print_on_console(err_msg)
                        log.error(err_msg)
                else:
                    err_msg=self.__element_disabled()
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg


    def unselect_checkbox(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    log.debug(WEB_ELEMENT_ENABLED)
                    if webelement.is_selected():
                        is_visible=self.utilobj.is_visible(webelement)
                        if len(args)>0:
                            visibilityFlag=args[0]
                        if not(visibilityFlag and is_visible ):
                            browser_Keywords.driver_obj.execute_script(webconstants.CLICK_RADIO_CHECKBOX,webelement)
                        else:
                            webelement.click()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_OBJECTUNSELECTED']
                        logger.print_on_console(err_msg)
                        log.error(err_msg)
                else:
                    err_msg=self.__element_disabled()
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def get_status(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        output=OUTPUT_CONSTANT
        err_msg=None
        status=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.tag_name=='table':
                    if len(input)==4:
                        webelement=self.getActualElement(webelement,input)
                    elif len(input)==3:
                        temp_status=self.__fetch_status_array(webelement,input)
                        status=temp_status[0]
                if status==None and webelement!=None:
                    output=self.__fetch_status(webelement)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE

            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def __fetch_status(self,webelement,*args):
        try:
            input_type=webelement.get_attribute('type').lower();
            log.debug('Type is '+input_type)
            if webelement.is_selected():
                status=self.status[input_type]
            else:
                status='Un'+self.status[input_type].lower()
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status

    def __fetch_status_array(self,webelement,input):
        status_list=[]
        try:
            driver=browser_Keywords.driver_obj
            row_num=input[0]
            col_num=input[1]
            row_num=int(row_num)
            col_num=int(col_num)
            tag_name=input[2]
            cell=driver.execute_script(webconstants.GET_CELL_JS,webelement,row_num-1,col_num-1)
            element_list=cell.find_elements_by_xpath('.//*')
            if tag_name=='radio' or tag_name=='checkbox':
                log.debug('Tagname is',tag_name)
                for element in element_list:
                    element_xpath=driver.execute_script(webconstants.GET_XPATH_JS,element)
                    child=driver.find_element_by_xpath(element_xpath)
                    if child!=None:
                        tag_name=child.tag_name
                        tag_type=child.get_attribute('type')
                        if tag_name=='input' and tag_type=='radio':
                            status_list.append(self.__fetch_status(child))
                        elif tag_name=='input' and tag_type=='checkbox':
                            status_list.append(self.__fetch_status(child))

        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        log.debug(status_list)
        return status_list

    def getActualElement(self,element,input):
        try:
            row_number=input[0]
            col_number=input[1]
            row_number=int(row_number)
            col_number=int(col_number)
            tag=input[2].lower()
            index=int(input[3])
            eleStatus=False
            counter = 1
            actualElement=None
            table_keywords_obj=table_keywords.TableOperationKeywords()
            cell=table_keywords_obj.javascriptExecutor(element,row_number-1,col_number-1)
            element_list=cell.find_elements_by_xpath('.//*')
            for member in element_list:
                  js1='function getElementXPath(elt) {var path = "";for (; elt && elt.nodeType == 1; elt = elt.parentNode){idx = getElementIdx(elt);xname = elt.tagName;if (idx >= 1){xname += "[" + idx + "]";}path = "/" + xname + path;}return path;}function getElementIdx(elt){var count = 1;for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling){if(sib.nodeType == 1 && sib.tagName == elt.tagName){count++;}}return count;}return getElementXPath(arguments[0]).toLowerCase();'
                  xpath=browser_Keywords.driver_obj.execute_script(js1,member)
                  cellChild = browser_Keywords.driver_obj.find_element_by_xpath(xpath)
                  tagName = cellChild.tag_name
                  tagType = cellChild.get_attribute('type')
                  xpath_elements=xpath.split('/')
                  lastElement=xpath_elements[len(xpath_elements)-1]
                  childindex=lastElement[lastElement.find("[")+1:lastElement.find("]")]
                  childindex = int(childindex)
                  if tag.lower()=='dropdown' or tag.lower()=='listbox' and tagName=='select':
                    multiSelect=cellChild.get_attribute('multiple')
                    if multiSelect!=None and multiSelect=='true' or multiSelect=='multiple':
                          if index==childindex:
                            eleStatus =True
                          else:
                            if counter==index:
                               index =childindex
                               eleStatus =True
                            else:
                                counter+=1
                    else:
                        if tag=='dropdown':
                            if index==childindex:
                                eleStatus =True
                            else:
                                if counter==index:
                                    index =childindex
                                    eleStatus =True
                                else:
                                    counter+=1

                  elif tag.lower()=='checkbox' or tag.lower()=='radio':
                    if tagName=='input' and tagType=='radio':
                        if index==childindex:
                                eleStatus =True
                        else:
                                if counter==index:
                                    index =childindex
                                    eleStatus =True
                                else:
                                    counter+=1
                    elif tagName=='input' and tagType=='checkbox':
                            if index==childindex:
                                    eleStatus =True
                            else:
                                    if counter==index:
                                        index =childindex
                                        eleStatus =True
                                    else:
                                        counter+=1
                  else:
                            eleStatus=True

                  if eleStatus==True:
                    actualElement=cellChild
                    break
        except Exception as e:
            err_msg=self.__web_driver_exception(e)

        return actualElement
