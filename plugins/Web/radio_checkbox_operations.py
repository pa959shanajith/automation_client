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
import utilweb_operations
import table_keywords
import webconstants
from constants import *
import logging
import readconfig
import threading
local_rco = threading.local()

class RadioCheckboxKeywords():

    def __init__(self):
        self.utilobj=utilweb_operations.UtilWebKeywords()
        self.status = { 'radio': 'Selected', 'checkbox': 'Checked' }
        local_rco.log = logging.getLogger('radio_checkbox_operations.py')

    def __element_disabled(self):
        err_msg=ERROR_CODE_DICT['ERR_DISABLED_OBJECT']
        logger.print_on_console(err_msg)
        local_rco.log.error(err_msg)
        return err_msg

    def __web_driver_exception(self,e):
        local_rco.log.error(e)
        logger.print_on_console(e)
        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
        return err_msg

    def __element_not_displayed(self):
        err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
        logger.print_on_console(err_msg)
        local_rco.log.error(err_msg)
        return err_msg

    def __check_visibility_from_config(self):
        return readconfig.configvalues['ignoreVisibilityCheck'].strip().lower() == "yes"

    def select_radiobutton(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_rco.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    local_rco.log.debug(WEB_ELEMENT_ENABLED)
                    if webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'grid':
                        body = True
                        right = True
                        index = False
                        input = args[0]
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
                                                radio=cells[col_number].find_elements_by_tag_name('input')
                                                if len(radio)>0:
                                                    for r in radio:
                                                        if r.get_attribute('type').lower() == 'radio':
                                                            webelement = r
                                                            break
                                                else:
                                                    err_msg='Object not found: Radio button not found inside the cell'
                                                    local_rco.log.error(err_msg)
                                                    logger.print_on_console(err_msg)
                                            except Exception as e:
                                                local_rco.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        else:
                                            err_msg='Invalid input: Col number more than col count'
                                            local_rco.log.error(err_msg)
                                            logger.print_on_console(err_msg)
                                    except Exception as e:
                                        local_rco.log.error(e)
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                else:
                                    err_msg='Invalid input: Row number more than row count'
                                    local_rco.log.error('Invalid input: Row number more than row count')
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
                                                    radio=j.find_elements_by_tag_name('input')
                                                    if len(radio)>0:
                                                        for r in radio:
                                                            if r.get_attribute('type').lower() == 'radio':
                                                                webelement = r
                                                                break
                                                    break
                                                except Exception as e:
                                                    local_rco.log.error(e)
                                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        break
                                if webelement.get_attribute('type').lower() != 'radio':
                                    err_msg='Object not found: Radio button not found inside the cell'
                                    local_rco.log.error(err_msg)
                                    logger.print_on_console(err_msg)

                    if err_msg == None:
                        if not (self.utilobj.is_visible(webelement)) and self.__check_visibility_from_config():
                            # performing js code
                            local_rco.log.debug('element is invisible, performing js code')
                            browser_Keywords.local_bk.driver_obj.execute_script(webconstants.CLICK_RADIO_CHECKBOX,webelement)
                            status = TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                        else:
                            if self.__check_visibility_from_config():
                                # performing js code
                                local_rco.log.debug('element is visible, performing js code')
                                browser_Keywords.local_bk.driver_obj.execute_script(webconstants.CLICK_RADIO_CHECKBOX,webelement)
                                status = TEST_RESULT_PASS
                                methodoutput = TEST_RESULT_TRUE
                            elif self.utilobj.is_visible(webelement):
                                # performing selenium code
                                local_rco.log.debug('element is visible, performing selenium code')
                                browser_Keywords.local_bk.driver_obj.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});", webelement)
                                webelement.click()
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                            else:
                                err_msg = self.__element_not_displayed()
                else:
                    err_msg=self.__element_disabled()
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg


    def select_checkbox(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_rco.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    local_rco.log.debug(WEB_ELEMENT_ENABLED)
                    if webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'grid':
                        body = True
                        right = True
                        index = False
                        input = args[0]
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
                                                chk_box=cells[col_number].find_elements_by_tag_name('input')
                                                if len(chk_box)>0:
                                                    for c in chk_box:
                                                        if c.get_attribute('type').lower() == 'checkbox':
                                                            webelement = c
                                                            break
                                                else:
                                                    err_msg='Object not found: Checkbox not found inside the cell'
                                                    local_rco.log.error(err_msg)
                                                    logger.print_on_console(err_msg)
                                            except Exception as e:
                                                local_rco.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        else:
                                            err_msg='Invalid input: Col number more than col count'
                                            local_rco.log.error(err_msg)
                                            logger.print_on_console(err_msg)
                                    except Exception as e:
                                        local_rco.log.error(e)
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                else:
                                    err_msg='Invalid input: Row number more than row count'
                                    local_rco.log.error('Invalid input: Row number more than row count')
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
                                                    chk_box=j.find_elements_by_tag_name('input')
                                                    if len(chk_box)>0:
                                                        for c in chk_box:
                                                            if c.get_attribute('type').lower() == 'checkbox':
                                                                webelement = c
                                                                break
                                                    break
                                                except Exception as e:
                                                    local_rco.log.error(e)
                                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        break
                                if webelement.get_attribute('type').lower() != 'checkbox':
                                    err_msg='Object not found: Checkbox not found inside the cell'
                                    local_rco.log.error(err_msg)
                                    logger.print_on_console(err_msg)
                    if not(webelement.is_selected()) and err_msg == None:
                        if not (self.utilobj.is_visible(webelement)) and self.__check_visibility_from_config():
                            # performing js code
                            local_rco.log.info('element is invisible and visibility is ignored, performing js code')
                            browser_Keywords.local_bk.driver_obj.execute_script(webconstants.CLICK_RADIO_CHECKBOX,webelement)
                            status = TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                        else:
                            if self.__check_visibility_from_config():
                                # performing js code
                                local_rco.log.info('element is visible, performing js code')
                                browser_Keywords.local_bk.driver_obj.execute_script(webconstants.CLICK_RADIO_CHECKBOX,webelement)
                                status = TEST_RESULT_PASS
                                methodoutput = TEST_RESULT_TRUE
                            elif self.utilobj.is_visible(webelement):
                                # performing selenium code
                                local_rco.log.info('element is visible, performing selenium code')
                                browser_Keywords.local_bk.driver_obj.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});", webelement)
                                webelement.click()
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                            else:
                                #For CNA, they required invisible checkbox selected with visibility not ignored.
                                local_rco.log.info('element is invisible and visibility is not ignored, performing js code')
                                browser_Keywords.local_bk.driver_obj.execute_script(webconstants.CLICK_RADIO_CHECKBOX,webelement)
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_OBJECTSELECTED']
                        logger.print_on_console(err_msg)
                        local_rco.log.error(err_msg)
                else:
                    err_msg=self.__element_disabled()
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg


    def unselect_checkbox(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        local_rco.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    local_rco.log.debug(WEB_ELEMENT_ENABLED)
                    if webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'checkbox':
                        if not (self.utilobj.is_visible(webelement)) and self.__check_visibility_from_config():
                            # performing js code
                            local_rco.log.debug('element is invisible, performing js code')
                            browser_Keywords.local_bk.driver_obj.execute_script(webconstants.CLICK_JAVASCRIPT,webelement)
                            status = TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                        else:
                            if self.utilobj.is_visible(webelement):
                                # performing selenium code
                                local_rco.log.debug('element is visible, performing selenium code')
                                browser_Keywords.local_bk.driver_obj.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});", webelement)
                                webelement.click()
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                            else:
                                err_msg = self.__element_not_displayed()   
                    else: 
                        if webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'grid':
                            body = True
                            right = True
                            index = False
                            input = args[0]
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
                                                    chk_box=cells[col_number].find_elements_by_tag_name('input')
                                                    if len(chk_box)>0:
                                                        for c in chk_box:
                                                            if c.get_attribute('type').lower() == 'checkbox':
                                                                webelement = c
                                                                break
                                                    else:
                                                        err_msg='Object not found: Checkbox not found inside the cell'
                                                        local_rco.log.error(err_msg)
                                                        logger.print_on_console(err_msg)
                                                    status=TEST_RESULT_PASS
                                                    methodoutput=TEST_RESULT_TRUE
                                                except Exception as e:
                                                    local_rco.log.error(e)
                                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                            else:
                                                err_msg='Invalid input: Col number more than col count'
                                                local_rco.log.error(err_msg)
                                                logger.print_on_console(err_msg)
                                        except Exception as e:
                                            local_rco.log.error(e)
                                            logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                    else:
                                        err_msg='Invalid input: Row number more than row count'
                                        local_rco.log.error('Invalid input: Row number more than row count')
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
                                                        chk_box=j.find_elements_by_tag_name('input')
                                                        if len(chk_box)>0:
                                                            for c in chk_box:
                                                                if c.get_attribute('type').lower() == 'checkbox':
                                                                    webelement = c
                                                                    break
                                                        break
                                                    except Exception as e:
                                                        local_rco.log.error(e)
                                                        logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                            break
                                    if webelement.get_attribute('type').lower() != 'checkbox':
                                        err_msg='Object not found: Checkbox not found inside the cell'
                                        local_rco.log.error(err_msg)
                                        logger.print_on_console(err_msg)
                        if webelement.is_selected() and err_msg == None:
                            if not (self.utilobj.is_visible(webelement)) and self.__check_visibility_from_config():
                                # performing js code
                                local_rco.log.debug('element is invisible, performing js code')
                                browser_Keywords.local_bk.driver_obj.execute_script(webconstants.CLICK_RADIO_CHECKBOX,webelement)
                                status = TEST_RESULT_PASS
                                methodoutput = TEST_RESULT_TRUE
                            else:
                                if self.utilobj.is_visible(webelement):
                                    # performing selenium code
                                    local_rco.log.debug('element is visible, performing selenium code')
                                    browser_Keywords.local_bk.driver_obj.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});", webelement)
                                    webelement.click()
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                                else:
                                    err_msg = self.__element_not_displayed()
                        else:
                            err_msg=ERROR_CODE_DICT['ERR_OBJECTUNSELECTED']
                            logger.print_on_console(err_msg)
                            local_rco.log.error(err_msg)
                else:
                    err_msg=self.__element_disabled()
            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def get_status(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=None
        err_msg=None
        status=None
        local_rco.log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            try:
                if webelement.tag_name.lower() == 'div' and (webelement.get_attribute('role') == 'checkbox' or webelement.get_attribute('role') == 'radio'):
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                    if webelement.get_attribute('role') == 'checkbox':
                        element_type = 'checkbox'
                    elif webelement.get_attribute('role') == 'radio':
                        element_type = 'radio'
                    if webelement.get_attribute('aria-checked') == "true":
                        output = True
                        logger.print_on_console('The '+element_type+' is checked')
                    else:
                        output = False
                        logger.print_on_console('The '+element_type+' is un-checked')
                else:
                    if webelement.tag_name=='table':
                        if len(input)==4 and int(input[3]) >= 1:
                            webelement=self.getActualElement(webelement,input)
                        elif len(input) == 4 and int(input[3]) <= 0:
                            status=TEST_RESULT_FAIL
                            err_msg = ERROR_CODE_DICT['INVALID_TABLE_INDEX']
                            local_rco.log.error(ERROR_CODE_DICT['INVALID_TABLE_INDEX'])
                            logger.print_on_console(ERROR_CODE_DICT['INVALID_TABLE_INDEX'])
                        elif len(input)==3:
                            temp_status=self.__fetch_status_array(webelement,input)
                            status=temp_status[0]
                    elif webelement.tag_name.lower() == 'div' and webelement.get_attribute('role') == 'grid':
                        body = True
                        right = True
                        index = False
                        input = args[0]
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
                                                chk_box=cells[col_number].find_elements_by_tag_name('input')
                                                if len(chk_box)>0:
                                                    for c in chk_box:
                                                        if (webelement.get_attribute('type').lower() in ['radio', 'checkbox']):
                                                            webelement = c
                                                            break
                                                else:
                                                    err_msg='Object not found: Textbox not found inside the cell'
                                                    local_rco.log.error(err_msg)
                                                    logger.print_on_console(err_msg)
                                                status=TEST_RESULT_PASS
                                                methodoutput=TEST_RESULT_TRUE
                                            except Exception as e:
                                                local_rco.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        else:
                                            err_msg='Invalid input: Col number more than col count'
                                            local_rco.log.error(err_msg)
                                            logger.print_on_console(err_msg)
                                    except Exception as e:
                                        local_rco.log.error(e)
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                else:
                                    err_msg='Invalid input: Row number more than row count'
                                    local_rco.log.error('Invalid input: Row number more than row count')
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
                                                    chk_box=j.find_elements_by_tag_name('input')
                                                    if len(chk_box)>0:
                                                        for c in chk_box:
                                                            if (webelement.get_attribute('type').lower() in ['radio', 'checkbox']):
                                                                webelement = c
                                                                break
                                                    break
                                                except Exception as e:
                                                    local_rco.log.error(e)
                                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        break
                                if not(webelement.get_attribute('type').lower() in ['radio', 'checkbox']):
                                    err_msg='Object not found inside the cell'
                                    local_rco.log.error(err_msg)
                                    logger.print_on_console(err_msg)
                    if status==None and webelement!=None and err_msg == None:
                        output=self.__fetch_status(webelement)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        logger.print_on_console('Result obtained is: ',output)

            except Exception as e:
                err_msg=self.__web_driver_exception(e)
        return status,methodoutput,output,err_msg

    def __fetch_status(self,webelement,*args):
        try:
            input_type=webelement.get_attribute('type').lower();
            local_rco.log.debug('Type is '+input_type)
            if webelement.is_selected():
                if input_type in ['submit','button','reset']:
                    status=webelement.is_selected()
                else:
                    status=self.status[input_type]
            else:
                if input_type in ['submit','button','reset']:
                    status=webelement.is_selected()
                else:
                    status='Un'+self.status[input_type].lower()
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return status

    def __fetch_status_array(self,webelement,input):
        status_list=[]
        try:
            driver=browser_Keywords.local_bk.driver_obj
            row_num=input[0]
            col_num=input[1]
            row_num=int(row_num)
            col_num=int(col_num)
            tag_name=input[2]
            cell=driver.execute_script(webconstants.GET_CELL_JS,webelement,row_num-1,col_num-1)
            element_list=cell.find_elements_by_xpath('.//*')
            if tag_name=='radio' or tag_name=='checkbox' or tag_name in ['submit','button','reset'] :
                local_rco.log.debug('Tagname is',tag_name)
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
                        elif tag_name=='input' and tag_type in ['submit','button','reset']:
                            status_list.append(self.__fetch_status(child))

        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        local_rco.log.debug(status_list)
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
                xpath=browser_Keywords.local_bk.driver_obj.execute_script(js1,member)
                cellChild = browser_Keywords.local_bk.driver_obj.find_element_by_xpath(xpath)
                tagName = cellChild.tag_name
                tagType = cellChild.get_attribute('type')
                xpath_elements=xpath.split('/')
                lastElement=xpath_elements[len(xpath_elements)-1]
                childindex=lastElement[lastElement.find("[")+1:lastElement.find("]")]
                childindex = int(childindex)
                if (tag.lower()=='dropdown' or tag.lower()=='listbox' or tag.lower()=='select') and tagName=='select':
                    multiSelect=cellChild.get_attribute('multiple')
                    if multiSelect!=None and (multiSelect=='true' or multiSelect=='multiple'):
                          if index==childindex:
                            eleStatus =True
                          else:
                            if counter==index:
                               index =childindex
                               eleStatus =True
                            else:
                                counter+=1
                    else:
                        if tag=='dropdown'or tag=='select':
                            if index==childindex:
                                eleStatus =True
                            else:
                                if counter==index:
                                    index =childindex
                                    eleStatus =True
                                else:
                                    counter+=1

                elif tag.lower()=='checkbox' or tag.lower()=='radio' or tag.lower()=='input':
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
                    # Commented next line, as because of this, loop was not going into next iteration
                    # eleStatus=True
                    continue
                if eleStatus==True:
                    actualElement=cellChild
                    break
        except Exception as e:
            err_msg=self.__web_driver_exception(e)
        return actualElement
