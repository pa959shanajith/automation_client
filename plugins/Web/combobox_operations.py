from selenium import webdriver
import browser_Keywords
from webconstants import *
import  utilweb_operations
import logger
import core_utils
import logging
from constants import *
import threading
if SYSTEM_OS=='Windows':
    from pyrobot import Robot
from selenium.webdriver.common.keys import Keys
local_cbo=threading.local()

class ComboboxKeywords():

    def __init__(self):
        self.util = utilweb_operations.UtilWebKeywords()
        local_cbo.log = logging.getLogger('combobox_operations.py')

    def getelement_text(self, webelement):
        """
        def : getelement_text
        purpose : to return text from element
        param : webelement
        return : string
        """
        text=''
        try:
            text = webelement.text
            if text is None or text is '':
                text = webelement.get_attribute('value')
            if text is None or text is '':
                text = webelement.get_attribute('name')
            if text is None or text is '':
                text = webelement.get_attribute('text')
        except Exception as e:
            print(e)
        return text

    def cmbSelectValueByIndex(self,webelement,input,*args):
        """
        def : cmbSelectValueByIndex
        purpose : to select combobox values based on index
        param  : webelement,list
        return : bool
        """
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        local_cbo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        index = None
        if webelement is not None:
            local_cbo.log.info('Recieved web element from the web dispatcher')
            if not err_msg and webelement.is_enabled():
                local_cbo.log.debug('element is enabled')
                try:
                    if (input is not None):
                        if index == None:
                            index = input[0]
                        if len(index.strip()) != 0:
                            input_val = int(index)
                            local_cbo.log.info('Input value obtained')
                            local_cbo.log.info(input_val)
                            # Performing Combobox logic
                            elementList = browser_Keywords.local_bk.driver_obj.execute_script(ELEMENT_LIST_JS, webelement)
                            if len(elementList) == 0:
                                webelement.click()
                                elementList=webelement.find_elements_by_xpath('//div[@role="listbox"]/*')
                            optionList = []
                            optionListSize = 0
                            for option in elementList:
                                if self.getelement_text(option):
                                    optionList.append(option)
                                    optionListSize += 1
                                else:
                                    continue
                            if (input_val < optionListSize):
                                for i in range(0, optionListSize):
                                    if (input_val == i):
                                        if (webelement.tag_name == 'input'):
                                            browser_Keywords.local_bk.driver_obj.execute_script("""arguments[0].focus()""", optionList[input_val])
                                            optionList[input_val].click()
                                            status = TEST_RESULT_PASS
                                            result = TEST_RESULT_TRUE
                                            local_cbo.log.info(STATUS_METHODOUTPUT_UPDATE)
                                        else:
                                            value = self.getelement_text(optionList[input_val])
                                            browser_Keywords.local_bk.driver_obj.execute_script(SET_VALUE_ATTRIBUTE, webelement, value)
                                            status = TEST_RESULT_PASS
                                            result = TEST_RESULT_TRUE
                                            local_cbo.log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                local_cbo.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            local_cbo.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            local_cbo.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                except Exception as e:
                    local_cbo.log.error(e)
                    logger.print_on_console(e)
            elif not err_msg:
                err_msg = 'Element is not enabled'
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                local_cbo.log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        
        local_cbo.log.info(RETURN_RESULT)
        return status,result,verb,err_msg

    def cmbGetCount(self,webelement,*args):
        """
        def : cmbGetCount
        purpose : to retrieve number of objects in combobox
        param  : webelement
        return : string
        """
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output = None
        err_msg=None
        local_cbo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            local_cbo.log.info('Recieved web element from the web dispatcher')
            if not err_msg and webelement.is_enabled():
                local_cbo.log.debug('element is enabled')
                try:
                    # Performing Combobox logic
                    elementList = browser_Keywords.local_bk.driver_obj.execute_script(ELEMENT_LIST_JS, webelement)
                    if len(elementList) == 0:
                        webelement.click()
                        elementList=webelement.find_elements_by_xpath('//div[@role="listbox"]/*')
                    optionList = []
                    optionListSize = 0
                    for option in elementList:
                        if self.getelement_text(option):
                            optionList.append(option)
                            optionListSize += 1
                        else:
                            continue
                    local_cbo.log.info('Count of combobox')
                    local_cbo.log.info(optionListSize)                   
                    webelement.send_keys(Keys.ESCAPE)   #Fixes for: list should be closed once the actions are performed
                    if (optionListSize >= 0):
                        output = str(optionListSize)
                        status=TEST_RESULT_PASS
                        result=TEST_RESULT_TRUE
                        logger.print_on_console('Result obtained is: ',output)
                        local_cbo.log.info(STATUS_METHODOUTPUT_UPDATE)
                except Exception as e:
                    local_cbo.log.error(e)
                    logger.print_on_console(e)
                local_cbo.log.info(RETURN_RESULT)
            elif not err_msg:
                err_msg = 'Element is not enabled'
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                local_cbo.log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,output,err_msg

    def cmbGetAllValues(self,webelement,*args):
        """
        def :cmbGetAllValues
        purpose: to get All values present in the combobox.
        param: webelement
        return : All combobox values
        """
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        output = None
        err_msg=None
        local_cbo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            local_cbo.log.info('Recieved web element from the web dispatcher')
            if not err_msg and webelement.is_enabled():
                local_cbo.log.debug('element is enabled')
                try:
                    # Performing Combobox logic
                    elementList = browser_Keywords.local_bk.driver_obj.execute_script(ELEMENT_LIST_JS, webelement)
                    if len(elementList) == 0:
                        webelement.click()
                        elementList=webelement.find_elements_by_xpath('//div[@role="listbox"]/*')
                    optionList = []
                    optionListSize = 0
                    for option in elementList:
                        if self.getelement_text(option):
                            optionList.append(option)
                            optionListSize += 1
                        else:
                            continue
                    temp = []
                    for x in range(0, optionListSize):
                        internal_val = self.getelement_text(optionList[x])
                        temp.append(internal_val)
                    local_cbo.log.info('temp value')
                    local_cbo.log.info(temp)
                    output=temp                    
                    webelement.send_keys(Keys.ESCAPE)   #Fixes for: list should be closed once the actions are performed     
                    if(len(temp) != 0 ):
                        status=TEST_RESULT_PASS
                        result=TEST_RESULT_TRUE
                        logger.print_on_console(output)
                        local_cbo.log.info(STATUS_METHODOUTPUT_UPDATE)
                except Exception as e:
                    local_cbo.log.error(e)
                    logger.print_on_console(e)
            elif not err_msg:
                err_msg = 'Element is not enabled'
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                local_cbo.log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,output,err_msg

    def cmbSelectValueByText(self,webelement,input,*args):
        """
        def : cmbSelectValueByText
        purpose : to select combobox values based on text
        param  : webelement,list
        return : bool
        """
        status=TEST_RESULT_FAIL
        result=TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        local_cbo.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            local_cbo.log.info('Recieved web element from the web dispatcher')
            if not err_msg and webelement.is_enabled():
                local_cbo.log.debug('element is enabled')
                try:
                    if (input is not None):
                        if len(input) == 1:
                            inp_val = input[0]
                            local_cbo.log.info('Input value obtained')
                            local_cbo.log.info(inp_val)
                        else:
                            inp_val = None
                        coreutilsobj = core_utils.CoreUtils()
                        inp_val = coreutilsobj.get_UTF_8(inp_val)
                        if (inp_val is not None):
                            if len(inp_val.strip()) != 0:
                                # Performing Combobox logic                                       
                                elementList = browser_Keywords.local_bk.driver_obj.execute_script(ELEMENT_LIST_JS, webelement)
                                if len(elementList) == 0:
                                    webelement.click()
                                    elementList=webelement.find_elements_by_xpath('//div[@role="listbox"]/*')
                                optionList = []
                                for option in elementList:
                                    if self.getelement_text(option):
                                        optionList.append(option)
                                    else:
                                        continue
                                flag = False
                                data_list = []
                                if len(input)==1:
                                    for i, each_item in enumerate(optionList):
                                        if inp_val.lower() in self.getelement_text(each_item).lower():
                                            data_list.append(self.getelement_text(each_item))
                                            break
                                if len(data_list) > 0:
                                    inp_val = data_list[0]
                                    flag = True
                                else:
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                    local_cbo.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                if (flag):
                                    if (webelement.tag_name == 'input'):                                          
                                        browser_Keywords.local_bk.driver_obj.execute_script("""arguments[0].focus()""", optionList[i])
                                        optionList[i].click()
                                        status = TEST_RESULT_PASS
                                        result = TEST_RESULT_TRUE
                                        local_cbo.log.info(STATUS_METHODOUTPUT_UPDATE)
                                    else:
                                        browser_Keywords.local_bk.driver_obj.execute_script(SET_VALUE_ATTRIBUTE, webelement, inp_val)
                                        status = TEST_RESULT_PASS
                                        result = TEST_RESULT_TRUE
                                        local_cbo.log.info(STATUS_METHODOUTPUT_UPDATE)
                                else:
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                    local_cbo.log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                    err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                local_cbo.log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            local_cbo.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    else:
                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        local_cbo.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                except Exception as e:
                    local_cbo.log.error(e)
                    from selenium.common.exceptions import NoSuchElementException
                    if type(e) == NoSuchElementException:
                        err_msg = str(e)
                    logger.print_on_console(e)
            elif not err_msg:
                err_msg = 'Element is not enabled'
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                local_cbo.log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,verb,err_msg
