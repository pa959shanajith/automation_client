#-------------------------------------------------------------------------------
# Name:        textbox_operations.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     08-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import selenium
import browser_Keywords
from webconstants import *
from utilweb_operations import UtilWebKeywords
import logger
from encryption_utility import AESCipher
from selenium.common.exceptions import *
import logging
from constants import *
import core_utils
import readconfig
import threading
import table_keywords
from utils_web import Utils
local_to = threading.local()

class TextboxKeywords:
    def __init__(self):
        local_to.log = logging.getLogger('textbox_operations.py')
        self.tblobj = table_keywords.TableOperationKeywords()

    def validate_input(self,webelement,input):
        local_to.log.debug('Validating user input for max_length attribute')
        user_input=None
        max_len=self.__gettexbox_length(webelement)
        if not(max_len is None or max_len is '' or max_len == 'null'):
            max_len=int(float(max_len))
            if len(input) > max_len:
                user_input=input[0:max_len]
        local_to.log.debug('user_input is: ')
        local_to.log.debug(user_input)
        return user_input

    def __read_only(self):
        err_msg=ERROR_CODE_DICT['ERR_ELEMENT_IS_READONLY']
        logger.print_on_console(err_msg)
        local_to.log.error(err_msg)
        return err_msg

    def __element_disabled(self):
        err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
        logger.print_on_console(err_msg)
        local_to.log.error(err_msg)
        return err_msg

    def _invalid_input(self):
        err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
        local_to.log.info(err_msg)
        logger.print_on_console(err_msg)
        return err_msg
    
    def _invalid_index(self):
        err_msg=("list index out of range")
        local_to.log.info(err_msg)
        logger.print_on_console(err_msg)
        return err_msg

    def _index_zero(self):
        err_msg = ERROR_CODE_DICT['INVALID_TABLE_INDEX']
        local_to.log.info(err_msg)
        logger.print_on_console(err_msg)
        return err_msg

    def __unbound_local_error(self,e):
        err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
        local_to.log.error(e)
        local_to.log.info(err_msg)
        logger.print_on_console(err_msg)
        return err_msg

    def __invalid_element_state(self,e):
        err_msg=ERROR_CODE_DICT['ERR_INVALID_ELEMENT_STATE_EXCEPTION']
        local_to.log.error(e)
        logger.print_on_console(err_msg)
        return err_msg

    def __web_driver_exception(self,e):
        local_to.log.error(e)
        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        logger.print_on_console(err_msg)
        return err_msg

    def __check_visibility_from_config(self):
        return readconfig.configvalues['ignoreVisibilityCheck'].strip().lower() == "yes"

    def __check_IE_64bit_from_config(self):
        return readconfig.configvalues['bit_64'].strip().lower() == "yes"
    
    def __invalidInput(self):
        err_msg="Input cannot be empty/null"
        local_to.log.error(err_msg)
        logger.print_on_console(err_msg)
        return err_msg

    def _noneGetText(self):
        err_msg="GetText encountered None"
        local_to.log.error(err_msg)
        return err_msg

    def set_text(self,webelement,input,*args):
        """
        def : set_text
        purpose : sets the text on the given webelemnt
        param : webelement,input(text to be set)
        return : bool

        """
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        check_flag=True
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if(input[0].isspace() or input[0]==''):
            err_msg=self.__invalidInput()
            return status,methodoutput,output,err_msg
        
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    if webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'grid':
                        body = True
                        right = True
                        index = False
                        if len(input)>=5:
                            if (input[3].lower() == 'body') : body = True
                            elif (input[3].lower() == 'header') : body = False
                            else: err_msg = "Invalid input"
                            if (input[4].lower() == 'right') : right = True
                            elif (input[4].lower() == 'left') : right = False
                            elif not(err_msg): err_msg = "Invalid input"
                        if not (err_msg):
                            if len(input)<=5:
                                index = True
                                row_number=int(input[0])-1
                                col_number=int(input[1])-1
                            else:
                                row_number=input[0]
                                col_number=input[1]
                            if body:
                                if right:
                                    try:
                                        container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                    except:
                                        container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                                else:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                                rows = container.find_elements_by_xpath(".//div[@role='row']")
                            else:
                                if right:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                                else:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
                                rows = container.find_elements_by_xpath(".//div[contains(@class,'ag-header-row')]")
                            if (index):
                                row_count = len(rows)
                                if(row_count>=row_number):
                                    try:
                                        if body:
                                            cells = rows[row_number].find_elements_by_xpath(".//div[@role='gridcell']")
                                        else:
                                            cells = rows[row_number].find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                        coloumn_count = len(cells)
                                        if (coloumn_count>=col_number):
                                            try:
                                                #cells[col_number].click()
                                                txt_box=cells[col_number].find_elements_by_tag_name('input')
                                                if len(txt_box)>0:
                                                    webelement = txt_box[0]
                                                    input = [input[2]]
                                                else:
                                                    check_flag=False
                                                    err_msg='Object not found: Textbox not found inside the cell'
                                                    local_to.log.error(err_msg)
                                                    logger.print_on_console(err_msg)
                                                status=TEST_RESULT_PASS
                                                methodoutput=TEST_RESULT_TRUE
                                            except Exception as e:
                                                check_flag=False
                                                local_to.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        else:
                                            check_flag=False
                                            err_msg='Invalid input: Col number more than col count'
                                            local_to.log.error(err_msg)
                                            logger.print_on_console(err_msg)
                                    except Exception as e:
                                        check_flag=False
                                        local_to.log.error(e)
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                else:
                                    check_flag=False
                                    err_msg='Invalid input: Row number more than row count'
                                    local_to.log.error('Invalid input: Row number more than row count')
                                    logger.print_on_console('Invalid input: Row number more than row count')
                            else:
                                for i in rows:
                                    if i.get_attribute(input[5]) == row_number:
                                        if body:
                                            cells = i.find_elements_by_xpath(".//div[@role='gridcell']")
                                        else:
                                            cells = i.find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                        for j in cells:
                                            if j.get_attribute(input[6]) == col_number:
                                                try:
                                                    #j.click()
                                                    txt_box=j.find_elements_by_tag_name('input')
                                                    if len(txt_box)>0:
                                                        for t in txt_box:
                                                            if t.get_attribute('type').lower() in ['text','email','number','password','range','search','url']:
                                                                webelement = t
                                                                input = [input[3]]
                                                                break
                                                    break
                                                except Exception as e:
                                                    check_flag=False
                                                    local_to.log.error(e)
                                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        break
                                if webelement.get_attribute('type').lower() not in ['text','email','number','password','range','search','url']:
                                    check_flag=False
                                    err_msg='Object not found: Textbox not found inside the cell'
                                    local_rco.log.error(err_msg)
                                    logger.print_on_console(err_msg)
                    if webelement.tag_name == 'table':
                        if len(input) == 5 and int(input[3]) <= 0:
                            err_msg = self._index_zero()
                        elif len(input)==5:
                            row_num=int(input[0])
                            col_num=int(input[1])
                            obj_type=input[2].lower()
                            index_val=int(input[3])-1
                            inp_list=[]
                            inp_list.append(input[4])
                            local_to.log.info(input)
                            input = inp_list
                            row_count=self.tblobj.getRowCountJs(webelement)
                            col_count=self.tblobj.getColoumnCountJs(webelement)
                            if (obj_type=="textbox" or obj_type=="input") and index_val>=0:
                                if row_num>row_count or col_num>col_count:
                                    check_flag=False
                                    err_msg=self._invalid_input()
                                else:
                                    cell=self.tblobj.javascriptExecutor(webelement,row_num-1,col_num-1)
                                    txt_box=cell.find_elements_by_tag_name('input')
                                    if len(txt_box)>0:
                                        if index_val >= len(txt_box):
                                            check_flag= False
                                            err_msg=self._invalid_index()
                                        else:
                                        #checking for type of input tag
                                        #allowed list contains types on which action can be performed 
                                        #not included types are :
                                        #button(submit,reset,button,radio),checkbox,week,month,color,hidden,password,image,range,time
                                            tag_type=txt_box[index_val].get_attribute('type').lower()
                                            allowed=['url','text','tel','search','number','email','password']
                                            if tag_type in allowed:
                                                webelement = txt_box[index_val]
                                            else:
                                                check_flag = False
                                                err_msg = self._invalid_input()
                                    else:
                                        check_flag=False
                                        err_msg=self._invalid_input()
                            elif obj_type!= "textbox" or obj_type!= "input":
                                check_flag=False
                                err_msg=self._invalid_input()
                        else:
                            err_msg = self._invalid_input()
                    if check_flag==True and not err_msg:
                        local_to.log.debug(WEB_ELEMENT_ENABLED)
                        utilobj=UtilWebKeywords()
                        obj=Utils()
                        is_visble=utilobj.is_visible(webelement)
                        input=input[0]
                        coreutilsobj=core_utils.CoreUtils()
                        input=coreutilsobj.get_UTF_8(input)
                        logger.print_on_console(INPUT_IS+input)
                        local_to.log.info(INPUT_IS)
                        local_to.log.info(input)
                        if input is not None:
                            readonly_value=webelement.get_attribute("readonly")
                            if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                                user_input=self.validate_input(webelement,input)
                                if user_input is not None:
                                    input=user_input
                                if not(is_visble) and self.__check_visibility_from_config():
                                    self.clear_text(webelement)
                                else:
                                    if not utilobj.is_inView(webelement):
                                        obj.get_element_location(webelement)
                                    webelement.clear()
                                local_to.log.debug('Setting the text')
                                browser_Keywords.local_bk.driver_obj.execute_script(SET_TEXT_SCRIPT, webelement, input)
                                # Bug #19221. To check if value is set or not.
                                value = browser_Keywords.local_bk.driver_obj.execute_script('return arguments[0].value', webelement)
                                if value == input:
                                    # implies that the value has been set in the textbox
                                    status = TEST_RESULT_PASS
                                    methodouput = TEST_RESULT_TRUE
                                else:
                                    if webelement.get_attribute('type') == 'number':
                                        err_msg = ERROR_CODE_DICT['ERR_INPUT_TYPE_MISMATCH']
                                        logger.print_on_console(err_msg)
                            else:
                                err_msg=self.__read_only()
                else:
                    err_msg=self.__element_disabled()
            except UnboundLocalError as e:
                err_msg=self.__unbound_local_error(e)

            except InvalidElementStateException as e:
                err_msg=self.__invalid_element_state(e)

            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def send_value(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        check_flag=True
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if(input[0].isspace() or input[0]==''):
            err_msg=self.__invalidInput()
            return status,methodoutput,output,err_msg
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    if webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'grid':
                        body = True
                        right = True
                        index = False
                        if len(input)>=5:
                            if (input[3].lower() == 'body') : body = True
                            elif (input[3].lower() == 'header') : body = False
                            else: err_msg = "Invalid input"
                            if (input[4].lower() == 'right') : right = True
                            elif (input[4].lower() == 'left') : right = False
                            elif not(err_msg): err_msg = "Invalid input"
                        if not (err_msg):
                            if len(input)<=5:
                                index = True
                                row_number=int(input[0])-1
                                col_number=int(input[1])-1
                            else:
                                row_number=input[0]
                                col_number=input[1]
                            if body:
                                if right:
                                    try:
                                        container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                    except:
                                        container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                                else:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                                rows = container.find_elements_by_xpath(".//div[@role='row']")
                            else:
                                if right:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                                else:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
                                rows = container.find_elements_by_xpath(".//div[contains(@class,'ag-header-row')]")
                            if (index):
                                row_count = len(rows)
                                if(row_count>=row_number):
                                    try:
                                        if body:
                                            cells = rows[row_number].find_elements_by_xpath(".//div[@role='gridcell']")
                                        else:
                                            cells = rows[row_number].find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                        coloumn_count = len(cells)
                                        if (coloumn_count>=col_number):
                                            try:
                                                #cells[col_number].click()
                                                txt_box=cells[col_number].find_elements_by_tag_name('input')
                                                if len(txt_box)>0:
                                                    webelement = txt_box[0]
                                                    input = [input[2]]
                                                else:
                                                    check_flag=False
                                                    err_msg='Object not found: Textbox not found inside the cell'
                                                    local_to.log.error(err_msg)
                                                    logger.print_on_console(err_msg)
                                                status=TEST_RESULT_PASS
                                                methodoutput=TEST_RESULT_TRUE
                                            except Exception as e:
                                                check_flag=False
                                                local_to.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        else:
                                            check_flag=False
                                            err_msg='Invalid input: Col number more than col count'
                                            local_to.log.error(err_msg)
                                            logger.print_on_console(err_msg)
                                    except Exception as e:
                                        check_flag=False
                                        local_to.log.error(e)
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                else:
                                    check_flag=False
                                    err_msg='Invalid input: Row number more than row count'
                                    local_to.log.error('Invalid input: Row number more than row count')
                                    logger.print_on_console('Invalid input: Row number more than row count')
                            else:
                                for i in rows:
                                    if i.get_attribute(input[5]) == row_number:
                                        if body:
                                            cells = i.find_elements_by_xpath(".//div[@role='gridcell']")
                                        else:
                                            cells = i.find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                        for j in cells:
                                            if j.get_attribute(input[6]) == col_number:
                                                try:
                                                    #j.click()
                                                    txt_box=j.find_elements_by_tag_name('input')
                                                    if len(txt_box)>0:
                                                        for t in txt_box:
                                                            if t.get_attribute('type').lower() in ['text','email','number','password','range','search','url']:
                                                                webelement = t
                                                                input = [input[3]]
                                                                break
                                                    break
                                                except Exception as e:
                                                    check_flag=False
                                                    local_to.log.error(e)
                                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        break
                                if webelement.get_attribute('type').lower() not in ['text','email','number','password','range','search','url']:
                                    check_flag=False
                                    err_msg='Object not found: Textbox not found inside the cell'
                                    local_rco.log.error(err_msg)
                                    logger.print_on_console(err_msg)
                    if webelement.tag_name == 'table':
                        if len(input) == 5 and int(input[3]) <= 0:
                            err_msg = self._index_zero()
                        elif len(input)==5:
                            row_num=int(input[0])
                            col_num=int(input[1])
                            obj_type=input[2].lower()
                            index_val=int(input[3])-1
                            inp_list=[]
                            inp_list.append(input[4])
                            local_to.log.info(input)
                            input = inp_list
                            row_count=self.tblobj.getRowCountJs(webelement)
                            col_count=self.tblobj.getColoumnCountJs(webelement)
                            if (obj_type=="textbox" or obj_type=="input") and not err_msg:
                                if row_num>row_count or col_num>col_count:
                                    check_flag=False
                                    err_msg=self._invalid_input()
                                else:
                                    cell=self.tblobj.javascriptExecutor(webelement,row_num-1,col_num-1)
                                    txt_box=cell.find_elements_by_tag_name('input')
                                    if len(txt_box)>0:
                                        if index_val >= len(txt_box):
                                            check_flag=False
                                            err_msg=self._invalid_index()
                                        else:
                                            tag_type = txt_box[index_val].get_attribute('type')
                                            allowed=['url','text','tel','search','number','email','password']
                                            if tag_type in allowed:
                                                webelement = txt_box[index_val]
                                            else:
                                                check_flag = False
                                                err_msg = self._invalid_input()
                                    else:
                                        check_flag=False
                                        err_msg=self._invalid_input()
                            elif (obj_type!= "textbox" or obj_type!= "input") and not err_msg:
                                check_flag=False
                                err_msg=self._invalid_input()
                        else:
                            err_msg = self._invalid_input()
                    if check_flag==True and not err_msg:
                        local_to.log.debug(WEB_ELEMENT_ENABLED)
                        utilobj=UtilWebKeywords()
                        isvisble=utilobj.is_visible(webelement)
                        input=input[0]
                        coreutilsobj=core_utils.CoreUtils()
                        input=coreutilsobj.get_UTF_8(input)
                        logger.print_on_console(INPUT_IS+input)
                        local_to.log.info(INPUT_IS)
                        local_to.log.info(input)
                        if input is not None:
                            readonly_value=webelement.get_attribute("readonly")
                            if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                                user_input=self.validate_input(webelement,input)
                                if user_input is not None:
                                    input=user_input
                                if not(isvisble) and self.__check_visibility_from_config():
                                    try:
                                        self.clear_text(webelement)
                                    except Exception as e:
                                        local_to.log.error('Exception in clearing text')
                                        pass
                                    local_to.log.debug('Sending the value via part 1')
                                    browser_Keywords.local_bk.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input)
                                else:
                                    try:
                                        webelement.clear()
                                    except Exception as e:
                                        local_to.log.error('Exception in clearing text')
                                        pass
                                    if(isinstance(browser_Keywords.local_bk.driver_obj,selenium.webdriver.Ie) and self.__check_IE_64bit_from_config):
                                        input=input+" "
                                        for i in range (0,len(input)+1):
                                            browser_Keywords.local_bk.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input[0:i])
                                        from sendfunction_keys import SendFunctionKeys
                                        obj=SendFunctionKeys()
                                        obj.sendfunction_keys("backspace",*args)
                                    else:
                                        from selenium.webdriver.common.keys import Keys
                                        text = self.__get_text(webelement)
                                        if text and (len(text) > 0):
                                            webelement.send_keys(Keys.BACK_SPACE * len(text))
                                        webelement.send_keys(input)
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                            else:
                                err_msg=self.__read_only()
                else:
                    err_msg=self.__element_disabled()
            except UnboundLocalError as e:
                err_msg=self.__unbound_local_error(e)
            except InvalidElementStateException as e:
                err_msg=self.__invalid_element_state(e)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def __get_text(self,webelement):
        text=''
        #get the text using selenium in-built method
        if webelement.tag_name == 'option':
            text = webelement.get_attribute('innerText')
            return text
        text=webelement.get_attribute('value')
        if text is None or text == '':
            if webelement.tag_name != "input":
                text = browser_Keywords.local_bk.driver_obj.execute_script("""return arguments[0].textContent""",webelement)
            else:
                #if failed, use javascript to get the text
                text = browser_Keywords.local_bk.driver_obj.execute_script("""return arguments[0].value""",webelement)
                if text is None or text is '':
                    #if failed, use the id to get the text
                    id = webelement.get_attribute('id')
                    if(id != '' and id is not None):
                        text = browser_Keywords.local_bk.driver_obj.execute_script("return document.getElementById(arguments[0]).value",id)
                        #finally everything failed then return the placeholder
                        if text is None or text is '':
                            text=webelement.get_attribute('placeholder')
        local_to.log.debug('Text returning from __get_text is ')
        local_to.log.debug(text)
        return text

    def __clear_text(self,webelement):
        local_to.log.debug('Clearing the text')
        browser_Keywords.local_bk.driver_obj.execute_script(CLEAR_TEXT_SCRIPT,webelement)

    def __gettexbox_length(self,webelement):
        local_to.log.debug('Get the maxlength of the textbox')
        return webelement.get_attribute('maxlength')


    def get_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        text=None
        err_msg=None
        check_flag=True
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'grid':
                    body = True
                    right = True
                    index = False
                    if len(input)>=4:
                        if (input[2].lower() == 'body') : body = True
                        elif (input[2].lower() == 'header') : body = False
                        else: err_msg = "Invalid input"
                        if (input[3].lower() == 'right') : right = True
                        elif (input[3].lower() == 'left') : right = False
                        elif not(err_msg): err_msg = "Invalid input"
                    if not (err_msg):
                        if len(input)<=4:
                            index = True
                            row_number=int(input[0])-1
                            col_number=int(input[1])-1
                        else:
                            row_number=input[0]
                            col_number=input[1]
                        if body:
                            if right:
                                try:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                except:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                            else:
                                container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                            rows = container.find_elements_by_xpath(".//div[@role='row']")
                        else:
                            if right:
                                container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                            else:
                                container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
                            rows = container.find_elements_by_xpath(".//div[contains(@class,'ag-header-row')]")
                        if (index):
                            row_count = len(rows)
                            if(row_count>=row_number):
                                try:
                                    if body:
                                        cells = rows[row_number].find_elements_by_xpath(".//div[@role='gridcell']")
                                    else:
                                        cells = rows[row_number].find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                    coloumn_count = len(cells)
                                    if (coloumn_count>=col_number):
                                        try:
                                            #cells[col_number].click()
                                            txt_box=cells[col_number].find_elements_by_tag_name('input')
                                            if len(txt_box)>0:
                                                webelement = txt_box[0]
                                            else:
                                                check_flag=False
                                                err_msg='Object not found: Textbox not found inside the cell'
                                                local_to.log.error(err_msg)
                                                logger.print_on_console(err_msg)
                                            status=TEST_RESULT_PASS
                                            methodoutput=TEST_RESULT_TRUE
                                        except Exception as e:
                                            check_flag=False
                                            local_to.log.error(e)
                                            logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                    else:
                                        check_flag=False
                                        err_msg='Invalid input: Col number more than col count'
                                        local_to.log.error(err_msg)
                                        logger.print_on_console(err_msg)
                                except Exception as e:
                                    check_flag=False
                                    local_to.log.error(e)
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                            else:
                                check_flag=False
                                err_msg='Invalid input: Row number more than row count'
                                local_to.log.error('Invalid input: Row number more than row count')
                                logger.print_on_console('Invalid input: Row number more than row count')
                        else:
                            for i in rows:
                                if i.get_attribute(input[4]) == row_number:
                                    if body:
                                        cells = i.find_elements_by_xpath(".//div[@role='gridcell']")
                                    else:
                                        cells = i.find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                    for j in cells:
                                        if j.get_attribute(input[5]) == col_number:
                                            try:
                                                #j.click()
                                                txt_box=j.find_elements_by_tag_name('input')
                                                if len(txt_box)>0:
                                                    for t in txt_box:
                                                        if t.get_attribute('type').lower() in ['text','email','number','password','range','search','url']:
                                                            webelement = t
                                                            break
                                                break
                                            except Exception as e:
                                                check_flag=False
                                                local_to.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                    break
                            if webelement.get_attribute('type').lower() not in ['text','email','number','password','range','search','url']:
                                check_flag=False
                                err_msg='Object not found: Textbox not found inside the cell'
                                local_rco.log.error(err_msg)
                                logger.print_on_console(err_msg)
                elif webelement.tag_name == 'table':
                    if len(input) == 4 and int(input[3]) <= 0:
                        err_msg = self._index_zero()
                    elif len(input)==4:
                        row_num=int(input[0])
                        col_num=int(input[1])
                        obj_type=input[2].lower()
                        index_val=int(input[3])-1
                        row_count=self.tblobj.getRowCountJs(webelement)
                        col_count=self.tblobj.getColoumnCountJs(webelement)
                        if ( obj_type=="textbox" or obj_type=="input") and index_val>=0:
                            if row_num>row_count or col_num>col_count:
                                check_flag=False
                                err_msg=self._invalid_input()
                            else:
                                cell=self.tblobj.javascriptExecutor(webelement,row_num-1,col_num-1)
                                txt_box=cell.find_elements_by_tag_name('input')
                                if len(txt_box)>0:
                                    if index_val >= len(txt_box):
                                        check_flag=False
                                        err_msg=self._invalid_index()
                                    else:
                                        #checking for type of input tag
                                        #allowed list contains types on which action can be performed
                                        #not included types are :
                                        #button(submit,reset,button,radio),checkbox,week,month,color,hidden,password,image,range,time
                                        tag_type = txt_box[index_val].get_attribute('type').lower()
                                        allowed=['url','text','tel','search','number','email']
                                        if tag_type in allowed:
                                            webelement = txt_box[index_val]
                                        else:
                                            check_flag = False
                                            err_msg = self._invalid_input()
                                else:
                                    check_flag=False
                                    err_msg=self._invalid_input()
                        elif obj_type!= "textbox" or obj_type!= "input":
                            check_flag=False
                            err_msg=self._invalid_input()
                        else:
                            check_flag=False
                            err_msg=self._index_zero()
                    else:
                        err_msg = self._invalid_input()
                if webelement.tag_name[0:9] == 'lightning':
                    text=webelement.text
                    if '\xa0' in text:
                        text = text.replace('\xa0', " ")
                    if(text!=None and text!=''):
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE  
                        check_flag=False
                if check_flag==True and not err_msg:
                    text=self.__get_text(webelement)
                    if '\xa0' in text:
                        text = text.replace('\xa0', " ")
                    if text is None:
                        err_msg=self._noneGetText()
                    else:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE                   
            except UnboundLocalError as e:
                err_msg=self.__unbound_local_error(e)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        logger.print_on_console(METHOD_OUTPUT)
        logger.print_on_console(text)
        return status,methodoutput,text,err_msg

    def verify_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        check_flag=True
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                # 4243:Failure of the test step along with appriopriate error message
                if input[0] is None:
                    err_msg=ERROR_CODE_DICT['NULL_DATA']
                    local_to.log.error(err_msg)
                    logger.print_on_console(err_msg)
                    return status,methodoutput,output,err_msg
                if webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'grid':
                    body = True
                    right = True
                    index = False
                    if len(input)>=5:
                        if (input[3].lower() == 'body') : body = True
                        elif (input[3].lower() == 'header') : body = False
                        else: err_msg = "Invalid input"
                        if (input[4].lower() == 'right') : right = True
                        elif (input[4].lower() == 'left') : right = False
                        elif not(err_msg): err_msg = "Invalid input"
                    if not (err_msg):
                        if len(input)<=5:
                            index = True
                            row_number=int(input[0])-1
                            col_number=int(input[1])-1
                        else:
                            row_number=input[0]
                            col_number=input[1]
                        if body:
                            if right:
                                try:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                except:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                            else:
                                container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                            rows = container.find_elements_by_xpath(".//div[@role='row']")
                        else:
                            if right:
                                container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                            else:
                                container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
                            rows = container.find_elements_by_xpath(".//div[contains(@class,'ag-header-row')]")
                        if (index):
                            row_count = len(rows)
                            if(row_count>=row_number):
                                try:
                                    if body:
                                        cells = rows[row_number].find_elements_by_xpath(".//div[@role='gridcell']")
                                    else:
                                        cells = rows[row_number].find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                    coloumn_count = len(cells)
                                    if (coloumn_count>=col_number):
                                        try:
                                            #cells[col_number].click()
                                            txt_box=cells[col_number].find_elements_by_tag_name('input')
                                            if len(txt_box)>0:
                                                webelement = txt_box[0]
                                                input = [input[2]]
                                            else:
                                                check_flag=False
                                                err_msg='Object not found: Textbox not found inside the cell'
                                                local_to.log.error(err_msg)
                                                logger.print_on_console(err_msg)
                                            status=TEST_RESULT_PASS
                                            methodoutput=TEST_RESULT_TRUE
                                        except Exception as e:
                                            check_flag=False
                                            local_to.log.error(e)
                                            logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                    else:
                                        check_flag=False
                                        err_msg='Invalid input: Col number more than col count'
                                        local_to.log.error(err_msg)
                                        logger.print_on_console(err_msg)
                                except Exception as e:
                                    check_flag=False
                                    local_to.log.error(e)
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                            else:
                                check_flag=False
                                err_msg='Invalid input: Row number more than row count'
                                local_to.log.error('Invalid input: Row number more than row count')
                                logger.print_on_console('Invalid input: Row number more than row count')
                        else:
                            for i in rows:
                                if i.get_attribute(input[5]) == row_number:
                                    if body:
                                        cells = i.find_elements_by_xpath(".//div[@role='gridcell']")
                                    else:
                                        cells = i.find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                    for j in cells:
                                        if j.get_attribute(input[6]) == col_number:
                                            try:
                                                #j.click()
                                                txt_box=j.find_elements_by_tag_name('input')
                                                if len(txt_box)>0:
                                                    for t in txt_box:
                                                        if t.get_attribute('type').lower() in ['text','email','number','password','range','search','url']:
                                                            webelement = t
                                                            input = [input[3]]
                                                            break
                                                break
                                            except Exception as e:
                                                check_flag=False
                                                local_to.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                    break
                            if webelement.get_attribute('type').lower() not in ['text','email','number','password','range','search','url']:
                                check_flag=False
                                err_msg='Object not found: Textbox not found inside the cell'
                                local_rco.log.error(err_msg)
                                logger.print_on_console(err_msg)
                if webelement.tag_name == 'table':
                    if len(input) == 5 and int(input[3]) <= 0:
                        err_msg = self._index_zero()
                    elif len(input)==5:
                        row_num=int(input[0])
                        col_num=int(input[1])
                        obj_type=input[2].lower()
                        index_val=int(input[3])-1
                        inp_list=[]
                        inp_list.append(input[4])
                        local_to.log.info(input)
                        row_count=self.tblobj.getRowCountJs(webelement)
                        col_count=self.tblobj.getColoumnCountJs(webelement)
                        input = inp_list
                        if (obj_type=="textbox" or obj_type=="input") and index_val>=0:
                            if row_num>row_count or col_num>col_count:
                                check_flag=False
                                err_msg=self._invalid_input()
                            else:
                                cell=self.tblobj.javascriptExecutor(webelement,row_num-1,col_num-1)
                                txt_box=cell.find_elements_by_tag_name('input')
                                if len(txt_box)>0:
                                    if index_val >= len(txt_box):
                                        check_flag=False
                                        err_msg=self._invalid_index()
                                    else:
                                        #checking for type of input tag
                                        #allowed list contains types on which action can be performed
                                        #not included types are :
                                        #button(submit,reset,button,radio),checkbox,week,month,color,hidden,password,image,range,time
                                        tag_type = txt_box[index_val].get_attribute('type')
                                        allowed=['url','text','tel','search','number','email']
                                        if tag_type in allowed:
                                            webelement = txt_box[index_val]
                                        else:
                                            check_flag = False
                                            err_msg = self._invalid_input()
                                else:
                                    check_flag=False
                                    err_msg=self._invalid_input()
                        elif obj_type!= "textbox" or obj_type!="input":
                            check_flag=False
                            err_msg=self._invalid_input()
                        else:
                            check_flag=False
                            err_msg=self._index_zero()
                    else:
                        err_msg = self._invalid_input()
                if webelement.tag_name[0:9] == 'lightning':
                    text=webelement.text
                    if '\xa0' in text:
                        text = text.replace('\xa0', " ")
                    if '\xa0' in input:
                        input = input.replace('\xa0', " ")
                    if(text==input):
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE  
                        check_flag=False
                if check_flag==True and not err_msg:
                    text=self.__get_text(webelement)
                    if '\xa0' in text:
                        text = text.replace('\xa0', " ")
                    input=input[0]
                    coreutilsobj=core_utils.CoreUtils()
                    input=coreutilsobj.get_UTF_8(input)
                    if '\xa0' in input:
                        input = input.replace('\xa0', " ")
                    if text==input:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg='Text mismatched'
                        logger.print_on_console(err_msg)
                        logger.print_on_console(EXPECTED,input)
                        local_to.log.info(EXPECTED)
                        local_to.log.info(input)
                        logger.print_on_console(ACTUAL,text)
                        local_to.log.info(ACTUAL)
                        local_to.log.info(text)
            except UnboundLocalError as e:
                err_msg=self.__unbound_local_error(e)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def clear_text(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        check_flag=True
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    if webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'grid':
                        body = True
                        right = True
                        index = False
                        if len(input)>=4:
                            if (input[2].lower() == 'body') : body = True
                            elif (input[2].lower() == 'header') : body = False
                            else: err_msg = "Invalid input"
                            if (input[3].lower() == 'right') : right = True
                            elif (input[3].lower() == 'left') : right = False
                            elif not(err_msg): err_msg = "Invalid input"
                        if not (err_msg):
                            if len(input)<=4:
                                index = True
                                row_number=int(input[0])-1
                                col_number=int(input[1])-1
                            else:
                                row_number=input[0]
                                col_number=input[1]
                            if body:
                                if right:
                                    try:
                                        container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                    except:
                                        container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                                else:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                                rows = container.find_elements_by_xpath(".//div[@role='row']")
                            else:
                                if right:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                                else:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
                                rows = container.find_elements_by_xpath(".//div[contains(@class,'ag-header-row')]")
                            if (index):
                                row_count = len(rows)
                                if(row_count>=row_number):
                                    try:
                                        if body:
                                            cells = rows[row_number].find_elements_by_xpath(".//div[@role='gridcell']")
                                        else:
                                            cells = rows[row_number].find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                        coloumn_count = len(cells)
                                        if (coloumn_count>=col_number):
                                            try:
                                                #cells[col_number].click()
                                                txt_box=cells[col_number].find_elements_by_tag_name('input')
                                                if len(txt_box)>0:
                                                    webelement = txt_box[0]
                                                else:
                                                    check_flag=False
                                                    err_msg='Object not found: Textbox not found inside the cell'
                                                    local_to.log.error(err_msg)
                                                    logger.print_on_console(err_msg)
                                                status=TEST_RESULT_PASS
                                                methodoutput=TEST_RESULT_TRUE
                                            except Exception as e:
                                                check_flag=False
                                                local_to.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        else:
                                            check_flag=False
                                            err_msg='Invalid input: Col number more than col count'
                                            local_to.log.error(err_msg)
                                            logger.print_on_console(err_msg)
                                    except Exception as e:
                                        check_flag=False
                                        local_to.log.error(e)
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                else:
                                    check_flag=False
                                    err_msg='Invalid input: Row number more than row count'
                                    local_to.log.error('Invalid input: Row number more than row count')
                                    logger.print_on_console('Invalid input: Row number more than row count')
                            else:
                                for i in rows:
                                    if i.get_attribute(input[4]) == row_number:
                                        if body:
                                            cells = i.find_elements_by_xpath(".//div[@role='gridcell']")
                                        else:
                                            cells = i.find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                        for j in cells:
                                            if j.get_attribute(input[5]) == col_number:
                                                try:
                                                    #j.click()
                                                    txt_box=j.find_elements_by_tag_name('input')
                                                    if len(txt_box)>0:
                                                        for t in txt_box:
                                                            if t.get_attribute('type').lower() in ['text','email','number','password','range','search','url']:
                                                                webelement = t
                                                                break
                                                    break
                                                except Exception as e:
                                                    check_flag=False
                                                    local_to.log.error(e)
                                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        break
                                if webelement.get_attribute('type').lower() not in ['text','email','number','password','range','search','url']:
                                    check_flag=False
                                    err_msg='Object not found: Textbox not found inside the cell'
                                    local_rco.log.error(err_msg)
                                    logger.print_on_console(err_msg)
                    if webelement.tag_name == 'table':
                        if len(input) == 4 and int(input[3]) <= 0:
                            self._index_zero()
                        elif len(input)==4:
                            row_num=int(input[0])
                            col_num=int(input[1])
                            obj_type=input[2].lower()
                            index_val=int(input[3])-1
                            row_count=self.tblobj.getRowCountJs(webelement)
                            col_count=self.tblobj.getColoumnCountJs(webelement)
                            if ( obj_type=="textbox" or obj_type=="input") and index_val>=0:
                                if row_num>row_count or col_num>col_count:
                                    check_flag=False
                                    err_msg=self._invalid_input()
                                else:
                                    cell=self.tblobj.javascriptExecutor(webelement,row_num-1,col_num-1)
                                    txt_box=cell.find_elements_by_tag_name('input')
                                    if len(txt_box)>0:
                                        if index_val >= len(txt_box):
                                            check_flag=False
                                            err_msg=self._invalid_index()
                                        else:
                                        #checking for type of input tag
                                        #allowed list contains types on which action can be performed
                                        #not included types are :
                                        #button(submit,reset,button,radio),file,checkbox,week,month,color,hidden,image,range,time
                                            tag_type = txt_box[index_val].get_attribute('type')
                                            allowed=['password','url','text','tel','search','number','email']
                                            if tag_type in allowed:
                                                webelement = txt_box[index_val]
                                            else:
                                                check_flag = False
                                                err_msg = self._invalid_input()
                                    else:
                                        check_flag=False
                                        err_msg=self._invalid_input()
                            elif obj_type!= "textbox" or obj_type!= "input":
                                check_flag=False
                                err_msg=self._invalid_input()
                            else:
                                check_flag=False
                                err_msg=self._index_zero()
                        else:
                            err_msg = self._invalid_input()
                    if check_flag==True and not err_msg:
                        local_to.log.debug(WEB_ELEMENT_ENABLED)
                        readonly_value=webelement.get_attribute("readonly")
                        if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                            obj=UtilWebKeywords()
                            if obj.is_visible(webelement):
                                webelement.clear()
                                from selenium.webdriver.common.keys import Keys
                                try:
                                    webelement.send_keys(Keys.BACK_SPACE)
                                except Exception as e:
                                    local_to.log.debug('Warning!: Could not perform backspace function due to error : '+str(e))
                            else:
                                self.__clear_text(webelement)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            err_msg=self.__read_only()
                else:
                    err_msg=self.__element_disabled()
            except UnboundLocalError as e:
                err_msg=self.__unbound_local_error(e)
            except InvalidElementStateException as e:
                err_msg=self.__invalid_element_state(e)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def gettextbox_length(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        length=None
        err_msg=None
        check_flag=True
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'grid':
                    body = True
                    right = True
                    index = False
                    if len(input)>=4:
                        if (input[2].lower() == 'body') : body = True
                        elif (input[2].lower() == 'header') : body = False
                        else: err_msg = "Invalid input"
                        if (input[3].lower() == 'right') : right = True
                        elif (input[3].lower() == 'left') : right = False
                        elif not(err_msg): err_msg = "Invalid input"
                    if not (err_msg):
                        if len(input)<=4:
                            index = True
                            row_number=int(input[0])-1
                            col_number=int(input[1])-1
                        else:
                            row_number=input[0]
                            col_number=input[1]
                        if body:
                            if right:
                                try:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                except:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                            else:
                                container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                            rows = container.find_elements_by_xpath(".//div[@role='row']")
                        else:
                            if right:
                                container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                            else:
                                container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
                            rows = container.find_elements_by_xpath(".//div[contains(@class,'ag-header-row')]")
                        if (index):
                            row_count = len(rows)
                            if(row_count>=row_number):
                                try:
                                    if body:
                                        cells = rows[row_number].find_elements_by_xpath(".//div[@role='gridcell']")
                                    else:
                                        cells = rows[row_number].find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                    coloumn_count = len(cells)
                                    if (coloumn_count>=col_number):
                                        try:
                                            #cells[col_number].click()
                                            txt_box=cells[col_number].find_elements_by_tag_name('input')
                                            if len(txt_box)>0:
                                                webelement = txt_box[0]
                                            else:
                                                check_flag=False
                                                err_msg='Object not found: Textbox not found inside the cell'
                                                local_to.log.error(err_msg)
                                                logger.print_on_console(err_msg)
                                            status=TEST_RESULT_PASS
                                            methodoutput=TEST_RESULT_TRUE
                                        except Exception as e:
                                            check_flag=False
                                            local_to.log.error(e)
                                            logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                    else:
                                        check_flag=False
                                        err_msg='Invalid input: Col number more than col count'
                                        local_to.log.error(err_msg)
                                        logger.print_on_console(err_msg)
                                except Exception as e:
                                    check_flag=False
                                    local_to.log.error(e)
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                            else:
                                check_flag=False
                                err_msg='Invalid input: Row number more than row count'
                                local_to.log.error('Invalid input: Row number more than row count')
                                logger.print_on_console('Invalid input: Row number more than row count')
                        else:
                            for i in rows:
                                if i.get_attribute(input[4]) == row_number:
                                    if body:
                                        cells = i.find_elements_by_xpath(".//div[@role='gridcell']")
                                    else:
                                        cells = i.find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                    for j in cells:
                                        if j.get_attribute(input[5]) == col_number:
                                            try:
                                                #j.click()
                                                txt_box=j.find_elements_by_tag_name('input')
                                                if len(txt_box)>0:
                                                    for t in txt_box:
                                                        if t.get_attribute('type').lower() in ['text','email','number','password','range','search','url']:
                                                            webelement = t
                                                            break
                                                break
                                            except Exception as e:
                                                check_flag=False
                                                local_to.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                    break
                            if webelement.get_attribute('type').lower() not in ['text','email','number','password','range','search','url']:
                                check_flag=False
                                err_msg='Object not found: Textbox not found inside the cell'
                                local_rco.log.error(err_msg)
                                logger.print_on_console(err_msg)
                if webelement.tag_name == 'table':
                    if len(input) == 4 and int(input[3]) <= 0:
                        err_msg = self._index_zero()
                    elif len(input)==4:
                        row_num=int(input[0])
                        col_num=int(input[1])
                        obj_type=input[2].lower()
                        index_val=int(input[3])-1
                        row_count=self.tblobj.getRowCountJs(webelement)
                        col_count=self.tblobj.getColoumnCountJs(webelement)
                        if (obj_type=="textbox" or obj_type=="input") and index_val>=0:
                            if row_num>row_count or col_num>col_count:
                                check_flag=False
                                err_msg=self._invalid_input()
                            else:
                                cell=self.tblobj.javascriptExecutor(webelement,row_num-1,col_num-1)
                                txt_box=cell.find_elements_by_tag_name('input')
                                if len(txt_box)>0:
                                    if index_val >= len(txt_box):
                                        check_flag=False
                                        err_msg=self._invalid_index()
                                    else:
                                        #checking for type of input tag
                                        #allowed list contains types on which action can be performed
                                        #not included types are :
                                        #button(submit,reset,button,radio),checkbox,week,month,color,hidden,password,image,range,time
                                        tag_type = txt_box[index_val].get_attribute('type')
                                        allowed=['url','text','tel','search','number','email']
                                        if tag_type in allowed:
                                            webelement = txt_box[index_val]
                                        else:
                                            check_flag = False
                                            err_msg = self._invalid_input()
                                else:
                                    check_flag=False
                                    err_msg=self._invalid_input()
                        elif obj_type!= "textbox" or obj_type!="input":
                            check_flag=False
                            err_msg=self._invalid_input()
                        else:
                            check_flag=False
                            err_msg=self._index_zero()             
                    else:
                        err_msg = self._invalid_input()            
                if check_flag==True and not err_msg:
                    length = self.__gettexbox_length(webelement)
                    if length is not None:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg='Textbox length is '+str(length)
            except UnboundLocalError as e:
                err_msg=self.__unbound_local_error(e)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        logger.print_on_console('Textbox length is '+str(length))
        local_to.log.info('Textbox length is '+str(length))
        return status,methodoutput,length,err_msg

    def verifytextbox_length(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        check_flag=True
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'grid':
                    body = True
                    right = True
                    index = False
                    if len(input)>=5:
                        if (input[3].lower() == 'body') : body = True
                        elif (input[3].lower() == 'header') : body = False
                        else: err_msg = "Invalid input"
                        if (input[4].lower() == 'right') : right = True
                        elif (input[4].lower() == 'left') : right = False
                        elif not(err_msg): err_msg = "Invalid input"
                    if not (err_msg):
                        if len(input)<=5:
                            index = True
                            row_number=int(input[0])-1
                            col_number=int(input[1])-1
                        else:
                            row_number=input[0]
                            col_number=input[1]
                        if body:
                            if right:
                                try:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                except:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                            else:
                                container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                            rows = container.find_elements_by_xpath(".//div[@role='row']")
                        else:
                            if right:
                                container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                            else:
                                container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
                            rows = container.find_elements_by_xpath(".//div[contains(@class,'ag-header-row')]")
                        if (index):
                            row_count = len(rows)
                            if(row_count>=row_number):
                                try:
                                    if body:
                                        cells = rows[row_number].find_elements_by_xpath(".//div[@role='gridcell']")
                                    else:
                                        cells = rows[row_number].find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                    coloumn_count = len(cells)
                                    if (coloumn_count>=col_number):
                                        try:
                                            #cells[col_number].click()
                                            txt_box=cells[col_number].find_elements_by_tag_name('input')
                                            if len(txt_box)>0:
                                                webelement = txt_box[0]
                                                input = [input[2]]
                                            else:
                                                check_flag=False
                                                err_msg='Object not found: Textbox not found inside the cell'
                                                local_to.log.error(err_msg)
                                                logger.print_on_console(err_msg)
                                            status=TEST_RESULT_PASS
                                            methodoutput=TEST_RESULT_TRUE
                                        except Exception as e:
                                            check_flag=False
                                            local_to.log.error(e)
                                            logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                    else:
                                        check_flag=False
                                        err_msg='Invalid input: Col number more than col count'
                                        local_to.log.error(err_msg)
                                        logger.print_on_console(err_msg)
                                except Exception as e:
                                    check_flag=False
                                    local_to.log.error(e)
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                            else:
                                check_flag=False
                                err_msg='Invalid input: Row number more than row count'
                                local_to.log.error('Invalid input: Row number more than row count')
                                logger.print_on_console('Invalid input: Row number more than row count')
                        else:
                            for i in rows:
                                if i.get_attribute(input[5]) == row_number:
                                    if body:
                                        cells = i.find_elements_by_xpath(".//div[@role='gridcell']")
                                    else:
                                        cells = i.find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                    for j in cells:
                                        if j.get_attribute(input[6]) == col_number:
                                            try:
                                                #j.click()
                                                txt_box=j.find_elements_by_tag_name('input')
                                                if len(txt_box)>0:
                                                    for t in txt_box:
                                                        if t.get_attribute('type').lower() in ['text','email','number','password','range','search','url']:
                                                            webelement = t
                                                            input = [input[3]]
                                                            break
                                                break
                                            except Exception as e:
                                                check_flag=False
                                                local_to.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                    break
                            if webelement.get_attribute('type').lower() not in ['text','email','number','password','range','search','url']:
                                check_flag=False
                                err_msg='Object not found: Textbox not found inside the cell'
                                local_rco.log.error(err_msg)
                                logger.print_on_console(err_msg)
                if webelement.tag_name == 'table':
                    if len(input) == 5 and int(input[3]) <= 0:
                        self._index_zero()
                    elif len(input)==5:
                        row_num=int(input[0])
                        col_num=int(input[1])
                        obj_type=input[2].lower()
                        index_val=int(input[3])-1
                        inp_list=[]
                        inp_list.append(input[4])
                        local_to.log.info(input)
                        row_count=self.tblobj.getRowCountJs(webelement)
                        col_count=self.tblobj.getColoumnCountJs(webelement)
                        input = inp_list
                        if (obj_type=="textbox" or obj_type=="input") and index_val>=0:
                            if row_num>row_count or col_num>col_count:
                                check_flag=False
                                err_msg=self._invalid_input()
                            else:
                                cell=self.tblobj.javascriptExecutor(webelement,row_num-1,col_num-1)
                                txt_box=cell.find_elements_by_tag_name('input')
                                if len(txt_box)>0:
                                    if index_val >= len(txt_box):
                                        check_flag=False
                                        err_msg=self._invalid_index()
                                    else:
                                        #checking for type of input tag
                                        #allowed list contains types on which action can be performed
                                        #not included types are :
                                        #button(submit,reset,button,radio),checkbox,week,month,color,hidden,password,image,range,time
                                        tag_type = txt_box[index_val].get_attribute('type')
                                        allowed=['url','text','tel','search','number','email']
                                        if tag_type in allowed:
                                            webelement = txt_box[index_val]
                                        else:
                                            check_flag = False
                                            err_msg = self._invalid_input()
                                else:
                                    check_flag=False
                                    err_msg=self._invalid_input()
                        elif obj_type!= "textbox" or obj_type!="input":
                            check_flag=False
                            err_msg=self._invalid_input()
                        else:
                            check_flag=False
                            err_msg=self._index_zero()            
                    else:
                        err_msg = self._invalid_input()         
                if check_flag==True and not err_msg:
                    length = self.__gettexbox_length(webelement)
                    input=input[0]
                    logger.print_on_console(INPUT_IS+str(input))
                    local_to.log.info(INPUT_IS)
                    local_to.log.info(input)

                    if length != None and length != '':
                        if '.' in input:
                            input=input[0:input.find('.')]
                        if length==input:
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            err_msg='Textbox length mismatched'
                            logger.print_on_console(err_msg)
                            logger.print_on_console(EXPECTED,input)
                            local_to.log.info(EXPECTED)
                            local_to.log.info(input)
                            logger.print_on_console(ACTUAL,length)
                            local_to.log.info(ACTUAL)
                            local_to.log.info(length)
                    else:
                        err_msg='Textbox length is None or empty'
            except UnboundLocalError as e:
                err_msg=self.__unbound_local_error(e)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def setsecuretext(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        check_flag=True
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    if webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'grid':
                        body = True
                        right = True
                        index = False
                        if len(input)>=5:
                            if (input[3].lower() == 'body') : body = True
                            elif (input[3].lower() == 'header') : body = False
                            else: err_msg = "Invalid input"
                            if (input[4].lower() == 'right') : right = True
                            elif (input[4].lower() == 'left') : right = False
                            elif not(err_msg): err_msg = "Invalid input"
                        if not (err_msg):
                            if len(input)<=5:
                                index = True
                                row_number=int(input[0])-1
                                col_number=int(input[1])-1
                            else:
                                row_number=input[0]
                                col_number=input[1]
                            if body:
                                if right:
                                    try:
                                        container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                    except:
                                        container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                                else:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                                rows = container.find_elements_by_xpath(".//div[@role='row']")
                            else:
                                if right:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                                else:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
                                rows = container.find_elements_by_xpath(".//div[contains(@class,'ag-header-row')]")
                            if (index):
                                row_count = len(rows)
                                if(row_count>=row_number):
                                    try:
                                        if body:
                                            cells = rows[row_number].find_elements_by_xpath(".//div[@role='gridcell']")
                                        else:
                                            cells = rows[row_number].find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                        coloumn_count = len(cells)
                                        if (coloumn_count>=col_number):
                                            try:
                                                #cells[col_number].click()
                                                txt_box=cells[col_number].find_elements_by_tag_name('input')
                                                if len(txt_box)>0:
                                                    webelement = txt_box[0]
                                                    input = [input[2]]
                                                else:
                                                    check_flag=False
                                                    err_msg='Object not found: Textbox not found inside the cell'
                                                    local_to.log.error(err_msg)
                                                    logger.print_on_console(err_msg)
                                                status=TEST_RESULT_PASS
                                                methodoutput=TEST_RESULT_TRUE
                                            except Exception as e:
                                                check_flag=False
                                                local_to.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        else:
                                            check_flag=False
                                            err_msg='Invalid input: Col number more than col count'
                                            local_to.log.error(err_msg)
                                            logger.print_on_console(err_msg)
                                    except Exception as e:
                                        check_flag=False
                                        local_to.log.error(e)
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                else:
                                    check_flag=False
                                    err_msg='Invalid input: Row number more than row count'
                                    local_to.log.error('Invalid input: Row number more than row count')
                                    logger.print_on_console('Invalid input: Row number more than row count')
                            else:
                                for i in rows:
                                    if i.get_attribute(input[5]) == row_number:
                                        if body:
                                            cells = i.find_elements_by_xpath(".//div[@role='gridcell']")
                                        else:
                                            cells = i.find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                        for j in cells:
                                            if j.get_attribute(input[6]) == col_number:
                                                try:
                                                    #j.click()
                                                    txt_box=j.find_elements_by_tag_name('input')
                                                    if len(txt_box)>0:
                                                        for t in txt_box:
                                                            if t.get_attribute('type').lower() in ['text','email','number','password','range','search','url']:
                                                                webelement = t
                                                                input = [input[3]]
                                                                break
                                                    break
                                                except Exception as e:
                                                    check_flag=False
                                                    local_to.log.error(e)
                                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        break
                                if webelement.get_attribute('type').lower() not in ['text','email','number','password','range','search','url']:
                                    check_flag=False
                                    err_msg='Object not found: Textbox not found inside the cell'
                                    local_rco.log.error(err_msg)
                                    logger.print_on_console(err_msg)
                    if webelement.tag_name == 'table':
                        if len(input) == 5 and int(input[3]) <= 0:
                            err_msg = self._index_zero() 
                        elif len(input)==5:
                            row_num=int(input[0])
                            col_num=int(input[1])
                            obj_type=input[2].lower()
                            index_val=int(input[3])-1
                            inp_list=[]
                            inp_list.append(input[4])
                            local_to.log.info(input)
                            row_count=self.tblobj.getRowCountJs(webelement)
                            col_count=self.tblobj.getColoumnCountJs(webelement)
                            input = inp_list
                            if (obj_type=="textbox"or obj_type=="input" )and index_val>=0:
                                if row_num>row_count or col_num>col_count:
                                    check_flag=False
                                    err_msg=self._invalid_input()
                                else:
                                    cell=self.tblobj.javascriptExecutor(webelement,row_num-1,col_num-1)
                                    txt_box=cell.find_elements_by_tag_name('input')
                                    if len(txt_box)>0:
                                        if index_val >= len(txt_box):
                                            check_flag=False
                                            err_msg=self._invalid_index()
                                        else:
                                            tag_type = txt_box[index_val].get_attribute('type')
                                            allowed=['url','text','tel','search','number','email','password']
                                            if tag_type in allowed:
                                                webelement = txt_box[index_val]
                                            else:
                                                check_flag = False
                                                err_msg = self._invalid_input()
                                    else:
                                        check_flag=False
                                        err_msg=self._invalid_input()
                            elif obj_type!="textbox":
                                check_flag=False
                                err_msg=self._invalid_input()
                            else:
                                check_flag=False
                                err_msg=self._index_zero()
                        else:
                            err_msg = self._invalid_input()
                    if check_flag==True and not err_msg:
                        local_to.log.debug(WEB_ELEMENT_ENABLED)
                        utilobj=UtilWebKeywords()
                        is_visble=utilobj.is_visible(webelement)
                        input=input[0]
                        coreutilsobj=core_utils.CoreUtils()
                        input=coreutilsobj.get_UTF_8(input)
                        logger.print_on_console(INPUT_IS+input)
                        local_to.log.info(INPUT_IS)
                        local_to.log.info(input)
                        if input is not None:
                            readonly_value=webelement.get_attribute("readonly")
                            if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                                if not(is_visble) and self.__check_visibility_from_config():
                                    self.clear_text(webelement)
                                else:
                                    webelement.clear()
                                encryption_obj = AESCipher()
                                input_val = encryption_obj.decrypt(input)
                                if input_val is not None:
                                    user_input=self.validate_input(webelement,input_val)
                                    if user_input is not None:
                                        input_val=user_input
                                    browser_Keywords.local_bk.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input_val)
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                                else:
                                    err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
                            else:
                                err_msg=self.__read_only()
                else:
                    err_msg=self.__element_disabled()
            except UnboundLocalError as e:
                err_msg=self.__unbound_local_error(e)
            except InvalidElementStateException as e:
                err_msg=self.__invalid_element_state(e)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def sendSecureValue(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        check_flag=True
        local_to.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    if webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'grid':
                        body = True
                        right = True
                        index = False
                        if len(input)>=5:
                            if (input[3].lower() == 'body') : body = True
                            elif (input[3].lower() == 'header') : body = False
                            else: err_msg = "Invalid input"
                            if (input[4].lower() == 'right') : right = True
                            elif (input[4].lower() == 'left') : right = False
                            elif not(err_msg): err_msg = "Invalid input"
                        if not (err_msg):
                            if len(input)<=5:
                                index = True
                                row_number=int(input[0])-1
                                col_number=int(input[1])-1
                            else:
                                row_number=input[0]
                                col_number=input[1]
                            if body:
                                if right:
                                    try:
                                        container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                    except:
                                        container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                                else:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                                rows = container.find_elements_by_xpath(".//div[@role='row']")
                            else:
                                if right:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                                else:
                                    container = webelement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
                                rows = container.find_elements_by_xpath(".//div[contains(@class,'ag-header-row')]")
                            if (index):
                                row_count = len(rows)
                                if(row_count>=row_number):
                                    try:
                                        if body:
                                            cells = rows[row_number].find_elements_by_xpath(".//div[@role='gridcell']")
                                        else:
                                            cells = rows[row_number].find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                        coloumn_count = len(cells)
                                        if (coloumn_count>=col_number):
                                            try:
                                                #cells[col_number].click()
                                                txt_box=cells[col_number].find_elements_by_tag_name('input')
                                                if len(txt_box)>0:
                                                    webelement = txt_box[0]
                                                    input = [input[2]]
                                                else:
                                                    check_flag=False
                                                    err_msg='Object not found: Textbox not found inside the cell'
                                                    local_to.log.error(err_msg)
                                                    logger.print_on_console(err_msg)
                                                status=TEST_RESULT_PASS
                                                methodoutput=TEST_RESULT_TRUE
                                            except Exception as e:
                                                check_flag=False
                                                local_to.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        else:
                                            check_flag=False
                                            err_msg='Invalid input: Col number more than col count'
                                            local_to.log.error(err_msg)
                                            logger.print_on_console(err_msg)
                                    except Exception as e:
                                        check_flag=False
                                        local_to.log.error(e)
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                else:
                                    check_flag=False
                                    err_msg='Invalid input: Row number more than row count'
                                    local_to.log.error('Invalid input: Row number more than row count')
                                    logger.print_on_console('Invalid input: Row number more than row count')
                            else:
                                for i in rows:
                                    if i.get_attribute(input[5]) == row_number:
                                        if body:
                                            cells = i.find_elements_by_xpath(".//div[@role='gridcell']")
                                        else:
                                            cells = i.find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                        for j in cells:
                                            if j.get_attribute(input[6]) == col_number:
                                                try:
                                                    #j.click()
                                                    txt_box=j.find_elements_by_tag_name('input')
                                                    if len(txt_box)>0:
                                                        for t in txt_box:
                                                            if t.get_attribute('type').lower() in ['text','email','number','password','range','search','url']:
                                                                webelement = t
                                                                input = [input[3]]
                                                                break
                                                    break
                                                except Exception as e:
                                                    check_flag=False
                                                    local_to.log.error(e)
                                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        break
                                if webelement.get_attribute('type').lower() not in ['text','email','number','password','range','search','url']:
                                    check_flag=False
                                    err_msg='Object not found: Textbox not found inside the cell'
                                    local_rco.log.error(err_msg)
                                    logger.print_on_console(err_msg)
                    if webelement.tag_name == 'table':
                        if len(input) == 5 and int(input[3]) <= 0:
                            err_msg = self._index_zero()
                        elif len(input)==5:
                            row_num=int(input[0])
                            col_num=int(input[1])
                            obj_type=input[2].lower()
                            index_val=int(input[3])-1
                            inp_list=[]
                            inp_list.append(input[4])
                            local_to.log.info(input)
                            row_count=self.tblobj.getRowCountJs(webelement)
                            col_count=self.tblobj.getColoumnCountJs(webelement)
                            input = inp_list
                            if (obj_type=="textbox" or obj_type=="input") and index_val>=0:
                                if row_num>row_count or col_num>col_count:
                                    check_flag=False
                                    err_msg=self._invalid_input()
                                else:
                                    cell=self.tblobj.javascriptExecutor(webelement,row_num-1,col_num-1)
                                    txt_box=cell.find_elements_by_tag_name('input')
                                    if len(txt_box)>0:
                                        if index_val >= len(txt_box):
                                            check_flag=False
                                            err_msg=self._invalid_index()
                                        else:
                                            webelement = txt_box[index_val]
                                    else:
                                        check_flag=False
                                        err_msg=self._invalid_input()
                            elif obj_type!="textbox":
                                check_flag=False
                                err_msg=self._invalid_input()
                            else:
                                check_flag=False
                                err_msg=self._index_zero()
                        else:
                            err_msg = self._invalid_input()
                    if check_flag==True and not err_msg:
                        local_to.log.debug(WEB_ELEMENT_ENABLED)
                        utilobj=UtilWebKeywords()
                        isvisble=utilobj.is_visible(webelement)
                        input=input[0]
                        coreutilsobj=core_utils.CoreUtils()
                        input=coreutilsobj.get_UTF_8(input)
                        logger.print_on_console(INPUT_IS,input)
                        local_to.log.info(INPUT_IS)
                        local_to.log.info(input)
                        if input is not None:
                            readonly_value=webelement.get_attribute("readonly")
                            if not(readonly_value is not None and readonly_value.lower() =='true' or readonly_value is ''):
                                encryption_obj = AESCipher()
                                input_val = encryption_obj.decrypt(input)
                                user_input=self.validate_input(webelement,input_val)
                                if user_input is not None:
                                    input_val=user_input
                                if not(isvisble) and self.__check_visibility_from_config():
                                    self.clear_text(webelement)
                                    local_to.log.debug('Sending the value via part 1')
                                    browser_Keywords.local_bk.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input_val)
                                else:
                                    webelement.clear()
                                    if(isinstance(browser_Keywords.local_bk.driver_obj,selenium.webdriver.Ie) and self.__check_IE_64bit_from_config):
                                        for i in range (0,len(input_val)+1):
                                            browser_Keywords.local_bk.driver_obj.execute_script(SET_TEXT_SCRIPT,webelement,input_val[0:i])
                                    else:
                                        from selenium.webdriver.common.keys import Keys
                                        text = self.__get_text(webelement)
                                        if text and (len(text) > 0):
                                            webelement.send_keys(Keys.BACK_SPACE * len(text))
                                        webelement.send_keys(input_val)
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                            else:
                                err_msg=self.__read_only()
                else:
                    err_msg=self.__element_disabled()
            except UnboundLocalError as e:
                err_msg=self.__unbound_local_error(e)
            except InvalidElementStateException as e:
                err_msg=self.__invalid_element_state(e)
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg
