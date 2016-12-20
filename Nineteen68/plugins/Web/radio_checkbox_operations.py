#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     08-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import selenium
import Exceptions
from webconstants import *
import logger
import browser_Keywords
from utilweb_operations import UtilWebKeywords
import table_keywords
import webconstants
class RadioCheckboxKeywords():

    def __init__(self):
        self.utilobj=UtilWebKeywords()
        self.status={'radio':'Selected',
                    'checkbox':'Checked'}


    def select_radiobutton(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    is_visible=self.utilobj.is_visible(webelement)
                    if len(args)>0:
                        visibilityFlag=args[0]
                        if not(visibilityFlag and is_visible):
                            browser_Keywords.driver_obj.execute_script(CLICK_RADIO_CHECKBOX,webelement)
                        else:
                            webelement.click()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                else:
                    logger.log('Element is disabled')
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput


    def select_checkbox(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    if not(webelement.is_selected()):
                        is_visble=self.utilobj.is_visible(webelement)
                        if len(args)>0:
                            visibilityFlag=args[0]
                        if not(visibilityFlag and is_visble ):
                            browser_Keywords.driver_obj.execute_script(CLICK_RADIO_CHECKBOX,webelement)
                        else:
                            webelement.click()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        logger.log('Checkbox is already selected')
                else:
                    logger.log('Element is disabled')
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput


    def unselect_checkbox(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    if webelement.is_selected():
                        is_visible=self.utilobj.is_visible(webelement)
                        if len(args)>0:
                            visibilityFlag=args[0]
                        if not(visibilityFlag and is_visible ):
                            browser_Keywords.driver_obj.execute_script(CLICK_RADIO_CHECKBOX,webelement)
                        else:
                            webelement.click()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        logger.log('Checkbox is already Unselected')
                else:
                    logger.log('Element is disabled')
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput

    def get_status(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        status=None
        if webelement is not None:
            try:
                if webelement.tag_name=='table':
                    if len(input)==4:
                        webelement=self.getActualElement(webelement,input)
                    elif len(input)==3:
                        temp_status=self.__fetch_status_array(webelement,input)
                        status=temp_status[0]
##                        status=TEST_RESULT_PASS
                if status==None and webelement!=None:
                    status,methodoutput=self.__fetch_status(webelement)
##                logger.log('Status is:'+status)
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput

    def __fetch_status(self,webelement,*args):
        try:
            type=webelement.get_attribute('type').lower();
            if webelement.is_selected():
                status=self.status[type]
                methodoutput=TEST_RESULT_TRUE
            else:
                status='Un'+self.status[type].lower()
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

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
            Exceptions.error(e)
        print status_list
        return status_list

    def getActualElement(self,element,input):
        try:
            row_number=input[0]
            col_number=input[1]
            row_number=int(row_number)
            col_number=int(col_number)
            tag=input[2]
            index=input[3]
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
                                counter+=counter
                    else:
                        if tag=='dropdown':
                            if index==childindex:
                                eleStatus =True
                            else:
                                if counter==index:
                                    index =childindex
                                    eleStatus =True
                                else:
                                    counter+=counter

                  elif tag.lower()=='checkbox' or tag.lower()=='radio':
                    if tagName=='input' and tagType=='radio':
                        if index==childindex:
                                eleStatus =True
                        else:
                                if counter==index:
                                    index =childindex
                                    eleStatus =True
                                else:
                                    counter+=counter
                    elif tagName=='input' and tagType=='checkbox':
                            if index==childindex:
                                    eleStatus =True
                            else:
                                    if counter==index:
                                        index =childindex
                                        eleStatus =True
                                    else:
                                        counter+=counter
                  else:
                            eleStatus=True

                  if eleStatus==True:
                    actualElement=cellChild
                    break
        except Exception as e:
            Exceptions.error(e)

        return actualElement
