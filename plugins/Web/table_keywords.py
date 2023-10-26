#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     08-11-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


from selenium import webdriver

import webconstants
from constants import *
import logger
import json
from  selenium.webdriver.common import action_chains
if SYSTEM_OS=='Windows':
    from ctypes import *
else:
    from pynput.mouse import Controller
import time
from selenium.webdriver.support.ui import Select
import browser_Keywords
import logging
import core_utils
import threading
import readconfig
local_tk = threading.local()

class TableOperationKeywords():
        def __init__(self):
            local_tk.log = logging.getLogger('table_keywords.py')
            local_tk.driver=''

        def __check_visibility_from_config(self):
            return readconfig.configvalues['ignoreVisibilityCheck'].strip().lower() == "yes"

#   returns the row count of table if the table found with the given xpath
        def getRowCount(self,webElement,*args):
            local_tk.driver=browser_Keywords.local_bk.driver_obj
            local_tk.log.debug('got the driver instance from browser keyword')
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            row_count=0
            visibleFlag=True
            err_msg=None
            if visibleFlag==True:
                try:
                    local_tk.log.debug('checking for element')
                    if webElement!=None:
                        if webElement.tag_name.lower() != 'table' and webElement.get_attribute('role') == 'grid':
                            body = True
                            right = True
                            if (args[0] != ['']):
                                input_val = args[0]
                                if (input_val[0].lower() == 'body') : body = True
                                elif (input_val[0].lower() == 'header') : body = False
                                else: err_msg = "Invalid input"
                                if (input_val[1].lower() == 'right') : right = True
                                elif (input_val[1].lower() == 'left') : right = False
                                elif not(err_msg): err_msg = "Invalid input"
                            if not (err_msg):
                                if webElement.get_attribute('aria-rowcount'):
                                    row_count = webElement.get_attribute('aria-rowcount')
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                                    logger.print_on_console('Row count is  : ',str(row_count))
                                else:
                                    if body:
                                        if right:
                                            try:
                                                container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                            except:
                                                container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                                        else:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                                        rows = container.find_elements_by_xpath(".//div[@role='row']")
                                    else:
                                        if right:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                                        else:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
                                        rows = container.find_elements_by_xpath(".//div[contains(@class,'ag-header-row')]")
                                    row_count = len(rows)
                                    if(row_count>=0):
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                        logger.print_on_console('Row count is  : ',str(row_count))
                                    else:
                                        err_msg='Error fetching row count'
                                        local_tk.log.error('Error fetching row count')
                                        logger.print_on_console('Error fetching row count')
                        else:
                            local_tk.log.debug('performing java script on element')
                            js='var targetTable = arguments[0]; var rowCount = targetTable.rows; return rowCount.length;'
                            row_count = browser_Keywords.local_bk.driver_obj.execute_script(js,webElement)
                            if(row_count>=0):
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                                logger.print_on_console('Row count is  : ',str(row_count))
                            else:
                                err_msg='Error fetching row count'
                                local_tk.log.error('Error fetching row count')
                                logger.print_on_console('Error fetching row count')
                    else:
                        err_msg='Element not found'
                        local_tk.log.error('Element not found')
                        logger.print_on_console('Element not found')
                except Exception as e:
                    local_tk.log.error(e)
                    logger.print_on_console(e)
                    err_msg = ERROR_CODE_DICT['MSG_ELEMENT_NOT_FOUND']
            else:
                local_tk.log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                err_msg = ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                logger.print_on_console(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
            return status,methodoutput,row_count,err_msg

#   returns the no of coloumns of the table if the table found with the given xpath
        def getColoumnCount(self,webElement,*args):
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            coloumn_count=0
            err_msg=None
            local_tk.driver=browser_Keywords.local_bk.driver_obj
            local_tk.log.debug('got the driver instance from browser keyword')
            visibleFlag=True
            if visibleFlag==True:
                try:
                    local_tk.log.debug('checking for element')
                    if webElement!=None:
                        if webElement.tag_name.lower() != 'table' and webElement.get_attribute('role') == 'grid':
                            body = True
                            right = True
                            if (args[0] != ['']):
                                input_val = args[0]
                                if (input_val[0].lower() == 'body') : body = True
                                elif (input_val[0].lower() == 'header') : body = False
                                else: err_msg = "Invalid input"
                                if (input_val[1].lower() == 'right') : right = True
                                elif (input_val[1].lower() == 'left') : right = False
                                elif not(err_msg): err_msg = "Invalid input"
                            if not (err_msg):
                                if webElement.get_attribute('aria-colcount'):
                                    coloumn_count = webElement.get_attribute('aria-colcount')
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                                    logger.print_on_console('Column count is  : ',str(coloumn_count))
                                else:
                                    if body:
                                        if right:
                                            try:
                                                container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                            except:
                                                container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                                        else:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                                        rows = container.find_elements_by_xpath(".//div[@role='row']")
                                    else:
                                        if right:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                                        else:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
                                        rows = container.find_elements_by_xpath(".//div[contains(@class,'ag-header-row')]")
                                    for i in rows:
                                        try:
                                            if body:
                                                cells = i.find_elements_by_xpath(".//div[@role='gridcell']")
                                            else:
                                                cells = i.find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                            if coloumn_count == len(cells):
                                                break
                                            coloumn_count = len(cells)
                                        except:pass
                                    if(coloumn_count>=0):
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                        logger.print_on_console('Column count is : ',str(coloumn_count))
                                    else:
                                        err_msg='Error fetching column count'
                                        local_tk.log.error('Error fetching column count')
                                        logger.print_on_console('Error fetching column count')
                        else:
                            local_tk.log.debug('performing java script on element')
                            js='var targetTable = arguments[0]; var columnCount = 0; var rows = targetTable.rows; if(rows.length > 0) { 	for (var i = 0; i < rows.length; i++) { 		var cells = rows[i].cells; 		var tempColumnCount = 0; 		for (var j = 0; j < cells.length; j++) { 			tempColumnCount += cells[j].colSpan; 		} 		if (tempColumnCount > columnCount) { 			columnCount = tempColumnCount; 		} 	} } return columnCount;'
                            coloumn_count = browser_Keywords.local_bk.driver_obj.execute_script(js,webElement)
                            if(coloumn_count>=0):
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                                # local_tk.log.info('Column count is : ',coloumn_count)
                                logger.print_on_console('Column count is : ',str(coloumn_count))
                            else:
                                err_msg='Error fetching column count'
                                local_tk.log.error('Error fetching column count')
                                logger.print_on_console('Error fetching column count')
                except Exception as e:
                    local_tk.log.error(e)
                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            else:
                local_tk.log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                err_msg = ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                logger.print_on_console(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
            return status,methodoutput,coloumn_count,err_msg

#   returns the cell value of cell with ',' seperated values, if the table found with the given xpath
        def getCellValue(self,webElement,input_val,*args):
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            cellVal=None
            err_msg=None
            index = False
            lightning = False
            local_tk.driver=browser_Keywords.local_bk.driver_obj
            local_tk.log.debug('got the driver instance from browser keyword')
            visibleFlag=True
            try:
                if visibleFlag==True:
                    local_tk.log.debug('reading the inputs')
                    if(len(input_val) > 1):
                        try:
                            lightning = len(webElement.find_elements_by_xpath('.//ancestor::lightning-datatable'))>0
                        except:
                            lightning = False
                        if webElement.tag_name.lower() != 'table' and webElement.get_attribute('role') == 'grid':
                            body = True
                            right = True
                            if len(input_val)>=4:
                                if (input_val[2].lower() == 'body') : body = True
                                elif (input_val[2].lower() == 'header') : body = False
                                else: err_msg = "Invalid input"
                                if (input_val[3].lower() == 'right') : right = True
                                elif (input_val[3].lower() == 'left') : right = False
                                elif not(err_msg): err_msg = "Invalid input"
                            if not (err_msg):
                                if len(input_val)<=4:
                                    index = True
                                    row_number=int(input_val[0]) - 1
                                    col_number=int(input_val[1]) - 1
                                else:
                                    row_number=input_val[0]
                                    col_number=input_val[1]
                                
                                #handling for table made with div and role as grid
                                try:
                                    rows = webElement.find_elements_by_xpath(".//div[@role='row']")
                                    row = rows[row_number]
                                    cells = row.find_elements_by_xpath(".//div[@role='cell']")
                                    cell = cells[col_number]
                                    cellVal = local_tk.driver.execute_script('return arguments[0].textContent',cell)
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                                except:
                                    if body:
                                        if right:
                                            try:
                                                container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                            except:
                                                container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                                        else:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                                        rows = container.find_elements_by_xpath(".//div[@role='row']")
                                    else:
                                        if right:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                                        else:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
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
                                                        cellVal = self.getChildNodes(cells[col_number])
                                                        cellVal=cellVal.strip()
                                                        local_tk.log.info('Got the result : %s',str(cellVal))
                                                        logger.print_on_console('Cell value is : ',str(cellVal))
                                                        status=TEST_RESULT_PASS
                                                        methodoutput=TEST_RESULT_TRUE
                                                    except Exception as e:
                                                        local_tk.log.error(e)
                                                        logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                                else:
                                                    err_msg='Invalid input: Col number more than col count'
                                                    local_tk.log.error('Invalid input: Col number more than col count')
                                                    logger.print_on_console('Invalid input: Col number more than col count')
                                            except Exception as e:
                                                local_tk.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        else:
                                            err_msg='Invalid input: Row number more than row count'
                                            local_tk.log.error('Invalid input: Row number more than row count')
                                            logger.print_on_console('Invalid input: Row number more than row count')
                                    else:
                                        for i in rows:
                                            if i.get_attribute(input_val[4]) == row_number:
                                                if body:
                                                    cells = i.find_elements_by_xpath(".//div[@role='gridcell']")
                                                else:
                                                    cells = i.find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                                for j in cells:
                                                    if j.get_attribute(input_val[5]) == col_number:
                                                        cellVal = self.getChildNodes(j)
                                                        cellVal=cellVal.strip()
                                                        local_tk.log.info('Got the result : %s',str(cellVal))
                                                        logger.print_on_console('Cell value is : ',str(cellVal))
                                                        status=TEST_RESULT_PASS
                                                        methodoutput=TEST_RESULT_TRUE
                                                    else:
                                                        err_msg='Invalid input: Column not found'
                                                        local_tk.log.error('Invalid input: Column not found')
                                                        logger.print_on_console('Invalid input: Column not found')
                                            else:
                                                err_msg='Invalid input: Row not found'
                                                local_tk.log.error('Invalid input: Row not found')
                                                logger.print_on_console('Invalid input: Row not found')
                        elif (lightning):
                            row_num=int(input_val[0])
                            col_num=int(input_val[1])
                            row_count=self.getRowCountJs(webElement)
                            col_count=self.getColoumnCountJs(webElement)
                            if row_num-1>row_count or col_num-1>col_count:
                                local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            else:
                                cellVal = ""
                                remoteWebElement=self.javascriptExecutor(webElement,row_num-1,col_num-1)
                                # cellVal = remoteWebElement.text
                                child_ele=[]
                                if(cellVal == ""):
                                    child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-base-formatted-text')
                                    if(len(child_ele)==0):
                                        child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-date-time')
                                        if(len(child_ele)==0):
                                            child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-number')
                                            if(len(child_ele)==0):
                                                child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-email')
                                                if(len(child_ele)==0):
                                                    child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-phone')
                                                    if(len(child_ele)==0):
                                                        child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-url')
                                                        if(len(child_ele)==0):
                                                            child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-location')
                                if(len(child_ele)>0):
                                    cellVal=child_ele[0].text
                                elif(len(child_ele)==0):
                                    cellVal=remoteWebElement.text                      
                                cellVal = cellVal.strip()
                                local_tk.log.info('Got the result : %s',str(cellVal))
                                logger.print_on_console('Cell value is : ',str(cellVal))
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                        else:
                            row_num=int(input_val[0])
                            col_num=int(input_val[1])
                            row_count=self.getRowCountJs(webElement)
                            col_count=self.getColoumnCountJs(webElement)
                            if row_num-1>row_count or col_num-1>col_count:
                                local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            else:
                                remoteWebElement=self.javascriptExecutor(webElement,row_num-1,col_num-1)
                                cellVal=self.getChildNodes(remoteWebElement)
                                cellVal=cellVal.strip()
                                local_tk.log.info('Got the result : %s',str(cellVal))
                                logger.print_on_console('Cell value is : ',str(cellVal))
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                    else:
                        local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                else:
                    local_tk.log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                    err_msg = ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    logger.print_on_console(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
            except Exception as e:
                local_tk.log.error(e)
                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            return status,methodoutput,cellVal,err_msg

#   verifies the cell value with the given text input, if the table found with the given xpath
        def verifyCellValue(self,webElement,input_val,*args):
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            cellVal=None
            err_msg=None
            index = False
            lightning = False
            local_tk.driver=browser_Keywords.local_bk.driver_obj
            local_tk.log.debug('got the driver instance from browser keyword')
            visibleFlag=True
            output_res=OUTPUT_CONSTANT
            try:
                if visibleFlag==True:
                    local_tk.log.debug('reading the inputs')
                    if(len(input_val) > 1):
                        try:
                            lightning = len(webElement.find_elements_by_xpath('.//ancestor::lightning-datatable'))>0
                        except:
                            lightning = False
                        if webElement.tag_name.lower() != 'table' and webElement.get_attribute('role') == 'grid':
                            body = True
                            right = True
                            if len(input_val)>=5:
                                if (input_val[3].lower() == 'body') : body = True
                                elif (input_val[3].lower() == 'header') : body = False
                                else: err_msg = "Invalid input"
                                if (input_val[4].lower() == 'right') : right = True
                                elif (input_val[4].lower() == 'left') : right = False
                                elif not(err_msg): err_msg = "Invalid input"
                            if not (err_msg):
                                if len(input_val)<=5:
                                    index = True
                                    row_number=int(input_val[0]) - 1
                                    col_number=int(input_val[1]) - 1
                                else:
                                    row_number=input_val[0]
                                    col_number=input_val[1]
                                if body:
                                    if right:
                                        try:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                        except:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                                    else:
                                        container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                                    rows = container.find_elements_by_xpath(".//div[@role='row']")
                                else:
                                    if right:
                                        container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                                    else:
                                        container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
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
                                                    cellVal = self.getChildNodes(cells[col_number])
                                                    cellVal=cellVal.strip()
                                                    expected_value=input_val[2].strip()
                                                    coreutilsobj=core_utils.CoreUtils()
                                                    expected_value=coreutilsobj.get_UTF_8(expected_value)
                                                    if(cellVal == expected_value):
                                                        local_tk.log.info('Got the result : %s', 'PASS')
                                                        logger.print_on_console('Got the result : ','PASS')
                                                        status=TEST_RESULT_PASS
                                                        methodoutput=TEST_RESULT_TRUE
                                                    else:
                                                        local_tk.log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                                        err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                                        logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                                        logger.print_on_console('Actual value is : ',str(cellVal))
                                                        logger.print_on_console('Expected value is : ',str(expected_value))
                                                except Exception as e:
                                                    local_tk.log.error(e)
                                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                            else:
                                                err_msg='Invalid input: Col number more than col count'
                                                local_tk.log.error('Invalid input: Col number more than col count')
                                                logger.print_on_console('Invalid input: Col number more than col count')
                                        except Exception as e:
                                            local_tk.log.error(e)
                                            logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                    else:
                                        err_msg='Invalid input: Row number more than row count'
                                        local_tk.log.error('Invalid input: Row number more than row count')
                                        logger.print_on_console('Invalid input: Row number more than row count')
                                else:
                                    for i in rows:
                                        if i.get_attribute(input_val[5]) == row_number:
                                            if body:
                                                cells = i.find_elements_by_xpath(".//div[@role='gridcell']")
                                            else:
                                                cells = i.find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                            for j in cells:
                                                if j.get_attribute(input_val[6]) == col_number:
                                                    cellVal = self.getChildNodes(j)
                                                    cellVal=cellVal.strip()
                                                    expected_value=input_val[2].strip()
                                                    coreutilsobj=core_utils.CoreUtils()
                                                    expected_value=coreutilsobj.get_UTF_8(expected_value)
                                                    if(cellVal == expected_value):
                                                        local_tk.log.info('Got the result : %s', 'PASS')
                                                        logger.print_on_console('Got the result : ','PASS')
                                                        status=TEST_RESULT_PASS
                                                        methodoutput=TEST_RESULT_TRUE
                                                    else:
                                                        local_tk.log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                                        err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                                        logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                                        logger.print_on_console('Actual value is : ',str(cellVal))
                                                        logger.print_on_console('Expected value is : ',str(expected_value))
                                                else:
                                                    err_msg='Invalid input: Column not found'
                                                    local_tk.log.error('Invalid input: Column not found')
                                                    logger.print_on_console('Invalid input: Column not found')
                                        else:
                                            err_msg='Invalid input: Row not found'
                                            local_tk.log.error('Invalid input: Row not found')
                                            logger.print_on_console('Invalid input: Row not found')
                        elif (lightning):
                            row_num=int(input_val[0])
                            col_num=int(input_val[1])
                            row_count=self.getRowCountJs(webElement)
                            col_count=self.getColoumnCountJs(webElement)
                            if row_num-1>row_count or col_num-1>col_count:
                                local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            else:
                                cellVal = ""
                                remoteWebElement=self.javascriptExecutor(webElement,row_num-1,col_num-1)
                                # cellVal = remoteWebElement.text
                                child_ele=[]
                                if(cellVal == ""):
                                    child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-base-formatted-text')
                                    if(len(child_ele)==0):
                                        child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-date-time')
                                        if(len(child_ele)==0):
                                            child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-number')
                                            if(len(child_ele)==0):
                                                child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-email')
                                                if(len(child_ele)==0):
                                                    child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-phone')
                                                    if(len(child_ele)==0):
                                                        child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-url')
                                                        if(len(child_ele)==0):
                                                            child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-location')
                                if(len(child_ele)>0):
                                    cellVal=child_ele[0].text
                                cellVal = cellVal.strip()
                                expected_value=input_val[2].strip()
                                coreutilsobj=core_utils.CoreUtils()
                                expected_value=coreutilsobj.get_UTF_8(expected_value)
                                if(cellVal == expected_value):
                                    local_tk.log.info('Got the result : %s', 'PASS')
                                    logger.print_on_console('Got the result : ','PASS')
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                                else:
                                    local_tk.log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                    err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                    logger.print_on_console('Actual value is : ',str(cellVal))
                                    logger.print_on_console('Expected value is : ',str(expected_value))
                        else:
                            row_num=int(input_val[0])
                            col_num=int(input_val[1])
                            row_count=self.getRowCountJs(webElement)
                            col_count=self.getColoumnCountJs(webElement)
                            if row_num>row_count or col_num>col_count:
                                local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            else:
                                remoteWebElement=self.javascriptExecutor(webElement,row_num-1,col_num-1)
                                cellVal=self.getChildNodes(remoteWebElement)
                                cellVal=cellVal.strip()
                                if cellVal.find('\xa0')!=-1:
                                    cellVal = cellVal.replace("\xa0"," ")
                                expected_value=input_val[2].strip()
                                if expected_value.find('\xa0')!=-1:
                                    expected_value = expected_value.replace("\xa0"," ")
                                coreutilsobj=core_utils.CoreUtils()
                                expected_value=coreutilsobj.get_UTF_8(expected_value)
                                if(cellVal == expected_value):
                                    local_tk.log.info('Got the result : %s', 'PASS')
                                    logger.print_on_console('Got the result : ','PASS')
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                                else:
                                    local_tk.log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                    err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                    logger.print_on_console('Actual value is : ',str(cellVal))
                                    logger.print_on_console('Expected value is : ',str(expected_value))

                    else:
                        local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                else:
                    local_tk.log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                    err_msg = ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    logger.print_on_console(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
            except Exception as e:
                local_tk.log.error(e)
                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            return status,methodoutput,output_res,err_msg

#   returns the  tooltip text  of given cell, if the table found with the given xpath
        """
        author : arpitha.b.v
        224 Issue fixed : Invalid input are coming in getCellToolTip
        """
        def getCellToolTip(self,webElement,input_val,*args):
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            tooltip=None
            local_tk.driver=browser_Keywords.local_bk.driver_obj
            err_msg=None
            lightning = False
            local_tk.log.debug('got the driver instance from browser keyword')
            visibleFlag=True
            if visibleFlag==True:
                try:
                    try:
                        lightning = len(webElement.find_elements_by_xpath('.//ancestor::lightning-datatable'))>0
                    except:
                        lightning = False
                    local_tk.log.debug('reading the inputs')
                    if (lightning):
                        row_number=int(input_val[0])
                        col_number=int(input_val[1])
                        row_count=self.getRowCountJs(webElement)
                        col_count=self.getColoumnCountJs(webElement)
                        if row_number>row_count or col_number>col_count:
                            local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        else:
                            local_tk.log.debug('perfoming java script on element')
                            remoteWebElement=self.javascriptExecutor(webElement,row_number-1,col_number-1)
                            ele=remoteWebElement.find_elements_by_xpath('.//*')
                            for i in ele:
                                contents=i.get_attribute('title') 
                                if contents!=None and contents.strip() != '':
                                    tooltip=contents
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                                    local_tk.log.info('Got the result : %s',str(tooltip))
                                    logger.print_on_console('Got the result : ',str(tooltip))
                                    break
                                else:
                                    tooltip=None
                                    err_msg = 'No cell tool tip present for the cell'
                    elif(len(input_val) > 1):
                        row_number=int(input_val[0])
                        col_number=int(input_val[1])
                        row_count=self.getRowCountJs(webElement)
                        col_count=self.getColoumnCountJs(webElement)
                        if row_number>row_count or col_number>col_count:
                            local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        else:
                            local_tk.log.debug('perfoming java script on element')
                            contents = self.getTooltip(webElement, row_number,col_number)
                           
                            if contents !=None:
                                tooltip=contents
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                                local_tk.log.info('Got the result : %s',str(tooltip))
                                logger.print_on_console('Got the result : ',str(tooltip))
                            else:
                                tooltip=None
                                err_msg = 'No cell tool tip present for the cell'
                    else:
                        local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])

                except Exception as e:
                    local_tk.log.error(e)
                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            else:
                local_tk.log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                err_msg = ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                logger.print_on_console(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
            return status,methodoutput,tooltip,err_msg



            """
            author : arpitha.b.v
            def : verifyCellToolTip
            purpose : checking the toolTipvalue
            param  : webelement,list
            return : bool
            """


        def verifyCellToolTip(self,webElement,input_val,*args):
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            verifytooltip=None
            local_tk.driver=browser_Keywords.local_bk.driver_obj
            err_msg=None
            lightning = False
            local_tk.log.debug('got the driver instance from browser keyword')
            visibleFlag=True
            if visibleFlag==True:
                try:
                    local_tk.log.debug('reading the inputs')
                    if (len(input_val) > 1):
                        try:
                            lightning = len(webElement.find_elements_by_xpath('.//ancestor::lightning-datatable'))>0
                        except:
                            lightning = False
                        if (lightning):
                            row_number=int(input_val[0])
                            col_number=int(input_val[1])
                            row_count=self.getRowCountJs(webElement)
                            col_count=self.getColoumnCountJs(webElement)
                            if row_number>row_count or col_number>col_count:
                                local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            else:
                                local_tk.log.debug('perfoming java script on element')
                                remoteWebElement=self.javascriptExecutor(webElement,row_number-1,col_number-1)
                                ele=remoteWebElement.find_elements_by_xpath('.//*')
                                for i in ele:
                                    contents=i.get_attribute('title') 
                                    if contents !=None and contents.strip() != '':
                                        verifytooltip=contents
                                        expected_value=input_val[2].strip()
                                        coreutilsobj=core_utils.CoreUtils()
                                        expected_value=coreutilsobj.get_UTF_8(expected_value)
                                        break
                                if(verifytooltip == expected_value):
                                    local_tk.log.info('Got the result : %s', str(verifytooltip))
                                    logger.print_on_console('Got the result : ',str(verifytooltip))
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                                else:
                                    local_tk.log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                    err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                    logger.print_on_console('Actual value is : ',str(verifytooltip))
                                    logger.print_on_console('Expected value is : ',str(expected_value))
                        else:
                            row_number=int(input_val[0])
                            col_number=int(input_val[1])
                            row_count=self.getRowCountJs(webElement)
                            col_count=self.getColoumnCountJs(webElement)
                            if row_number>row_count or col_number>col_count:
                                local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            else:
                                local_tk.log.debug('perfoming java script on element')
                                contents = self.getTooltip(webElement, row_number, col_number)
                               
                                if contents !=None:
                                    verifytooltip=contents
                                    expected_value=input_val[2].strip()
                                    coreutilsobj=core_utils.CoreUtils()
                                    expected_value=coreutilsobj.get_UTF_8(expected_value)

                                if(verifytooltip == expected_value):
                                    local_tk.log.info('Got the result : %s', str(verifytooltip))
                                    logger.print_on_console('Got the result : ',str(verifytooltip))
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                                else:
                                    local_tk.log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                    err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                    logger.print_on_console('Actual value is : ',str(verifytooltip))
                                    logger.print_on_console('Expected value is : ',str(expected_value))
                    else:
                        local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])

                except Exception as e:
                    local_tk.log.error(e)
                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            else:
                local_tk.log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                err_msg = ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                logger.print_on_console(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
            return status,methodoutput,verifytooltip,err_msg


#   lclicks on the given cell, if the table found with the given xpath
        def cellClick(self,webElement,input_arr,*args):
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            index = False
            lightning = False
            output_val=OUTPUT_CONSTANT
            local_tk.log.debug('reading the inputs')
            if(len(input_arr) > 1):
                local_tk.driver=browser_Keywords.local_bk.driver_obj
                local_tk.log.debug('got the driver instance from browser keyword')
                visibleFlag=True
                if visibleFlag==True:
                    try:
                        try:
                            lightning = len(webElement.find_elements_by_xpath('.//ancestor::lightning-datatable'))>0
                        except:
                            lightning = False
                        if webElement.tag_name.lower() != 'table' and webElement.get_attribute('role') == 'grid':
                            body = True
                            right = True
                            if len(input_arr)>=4:
                                if (input_arr[2].lower() == 'body') : body = True
                                elif (input_arr[2].lower() == 'header') : body = False
                                else: err_msg = "Invalid input"
                                if (input_arr[3].lower() == 'right') : right = True
                                elif (input_arr[3].lower() == 'left') : right = False
                                elif not(err_msg): err_msg = "Invalid input"
                            if not (err_msg):
                                if len(input_arr)<=4:
                                    index = True
                                    row_number=int(input_arr[0])-1
                                    col_number=int(input_arr[1])-1
                                else:
                                    row_number=input_arr[0]
                                    col_number=input_arr[1]
                                try:
                                    rows = webElement.find_elements_by_xpath(".//div[@role='row']")
                                    row = rows[row_number]
                                    cells = row.find_elements_by_xpath(".//div[@role='cell']")
                                    cell = cells[col_number]
                                    cell.click()
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                                except:
                                    if body:
                                        if right:
                                            try:
                                                container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                            except:
                                                container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                                        else:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                                        rows = container.find_elements_by_xpath(".//div[@role='row']")
                                    else:
                                        if right:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                                        else:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
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
                                                        if self.__check_visibility_from_config():
                                                            local_tk.log.debug('performing java script click')
                                                            js = 'var evType; element=arguments[0]; if (document.createEvent) {     evType = "Click executed through part-1";     var evt = document.createEvent("MouseEvents");     evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = "Click executed through part-2";   	setTimeout(function() {     element.click();   	}, 100); } return (evType);'
                                                            click=local_tk.driver.execute_script(js,cells[col_number])
                                                            status=TEST_RESULT_PASS
                                                            methodoutput=TEST_RESULT_TRUE
                                                        else:
                                                            cells[col_number].click()
                                                            status=TEST_RESULT_PASS
                                                            methodoutput=TEST_RESULT_TRUE
                                                    except:
                                                        try:
                                                            local_tk.driver.execute_script("arguments[0].scrollIntoView(true);arguments[0].click();", cells[col_number])
                                                            status=TEST_RESULT_PASS
                                                            methodoutput=TEST_RESULT_TRUE
                                                        except Exception as e:
                                                            local_tk.log.error(e)
                                                            logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                                else:
                                                    err_msg='Invalid input: Col number more than col count'
                                                    local_tk.log.error('Invalid input: Col number more than col count')
                                                    logger.print_on_console('Invalid input: Col number more than col count')
                                            except Exception as e:
                                                local_tk.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                        else:
                                            err_msg='Invalid input: Row number more than row count'
                                            local_tk.log.error('Invalid input: Row number more than row count')
                                            logger.print_on_console('Invalid input: Row number more than row count')
                                    else:
                                        for i in rows:
                                            if i.get_attribute(input_arr[4]) == row_number:
                                                if body:
                                                    cells = i.find_elements_by_xpath(".//div[@role='gridcell']")
                                                else:
                                                    cells = i.find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                                for j in cells:
                                                    if j.get_attribute(input_arr[5]) == col_number:
                                                        try:
                                                            if self.__check_visibility_from_config():
                                                                local_tk.log.debug('performing java script click')
                                                                js = 'var evType; element=arguments[0]; if (document.createEvent) {     evType = "Click executed through part-1";     var evt = document.createEvent("MouseEvents");     evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = "Click executed through part-2";   	setTimeout(function() {     element.click();   	}, 100); } return (evType);'
                                                                click=local_tk.driver.execute_script(js,j)
                                                                status=TEST_RESULT_PASS
                                                                methodoutput=TEST_RESULT_TRUE
                                                                break
                                                            else:
                                                                j.click()
                                                                status=TEST_RESULT_PASS
                                                                methodoutput=TEST_RESULT_TRUE
                                                                break
                                                        except:
                                                            try:
                                                                local_tk.driver.execute_script("arguments[0].scrollIntoView(true);arguments[0].click(); ", j)
                                                                status=TEST_RESULT_PASS
                                                                methodoutput=TEST_RESULT_TRUE
                                                            except Exception as e:
                                                                local_tk.log.error(e)
                                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                                                    else:
                                                        err_msg='Invalid input: Column not found'
                                                        local_tk.log.error('Invalid input: Column not found')
                                                        logger.print_on_console('Invalid input: Column not found')
                                            else:
                                                err_msg='Invalid input: Row not found'
                                                local_tk.log.error('Invalid input: Row not found')
                                                logger.print_on_console('Invalid input: Row not found')
                        elif (lightning):
                            row_num=int(input_arr[0])
                            col_num=int(input_arr[1])
                            row_count=self.getRowCountJs(webElement)
                            col_count=self.getColoumnCountJs(webElement)
                            if row_num-1>row_count or col_num-1>col_count:
                                local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            else:
                                remoteWebElement=self.javascriptExecutor(webElement,row_num-1,col_num-1)
                                child_ele=[]
                                child_ele=remoteWebElement.find_elements_by_xpath('.//a')
                                if(len(child_ele)==0):
                                    child_ele=remoteWebElement.find_elements_by_xpath('.//input')
                                    if(len(child_ele)==0):
                                        child_ele=remoteWebElement.find_elements_by_xpath('.//button')
                                        if(len(child_ele)==0):
                                            child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-base-formatted-text')
                                            if(len(child_ele)==0):
                                                child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-date-time')
                                                if(len(child_ele)==0):
                                                    child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-number')
                                                    if(len(child_ele)==0):
                                                        child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-email')
                                                        if(len(child_ele)==0):
                                                            child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-phone')
                                                            if(len(child_ele)==0):
                                                                child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-url')
                                                                if(len(child_ele)==0):
                                                                    child_ele = remoteWebElement.find_elements_by_xpath('.//lightning-formatted-location')
                                if(len(child_ele)>0):
                                    child_ele[0].click()
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                        elif len(input_arr)==2:
                            local_tk.log.info('normal cell click')
                            #logger.print_on_console('normal cell click inside the cell')
                            row_number=int(input_arr[0])-1
                            col_number=int(input_arr[1])-1
                            if webElement.tag_name.lower() == 'table':
                                cell = local_tk.driver.execute_script("""debugger; return arguments[0].getElementsByTagName('tr')[arguments[1]].getElementsByTagName('td')[arguments[2]]""",webElement,row_number,col_number)
                            else:
                                cell=self.javascriptExecutor(webElement,row_number,col_number)
                            element_list=cell.find_elements_by_xpath('.//*')
                            # going inside the cell
                            # if len(list(element_list))>0:
                            #     xpath=self.getElemntXpath(element_list[0])
                            #     cell=local_tk.driver.find_element_by_xpath(xpath)
                            try:
                                local_tk.log.debug('checking for element not none')
                                if(cell!=None):
                                    local_tk.log.debug('checking for element enabled')
                                    if cell.is_enabled():
                                        if isinstance(local_tk.driver,webdriver.Ie):
                                            try:
                                                local_tk.log.debug('performing java script click')
                                                js = 'var evType; element=arguments[0]; if (document.createEvent) {     evType = "Click executed through part-1";     var evt = document.createEvent("MouseEvents");     evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = "Click executed through part-2";   	setTimeout(function() {     element.click();   	}, 100); } return (evType);'
                                                click=local_tk.driver.execute_script(js,cell)
                                                status=webconstants.TEST_RESULT_PASS
                                                methodoutput=TEST_RESULT_TRUE
                                                local_tk.log.info('click action performed successfully')
                                                #logger.print_on_console('click action performed successfully')
                                            except Exception as e:
                                                local_tk.log.debug('error occured so trying action events')
                                                action=action_chains.ActionChains(local_tk.driver)
                                                action.move_to_element(cell).click(cell).perform()
                                                status=TEST_RESULT_PASS
                                                methodoutput=TEST_RESULT_TRUE
                                                local_tk.log.info('click action performed successfully')
                                                #logger.print_on_console('click action performed successfully')
                                        else:
                                            try:
                                                local_tk.log.info('Checking if there is a clickable element in the cell')
                                                if len(cell.find_elements_by_xpath('.//a')):
                                                    cell = cell.find_elements_by_xpath('.//a')[0]
                                                    local_tk.log.info('Pointing to link.')
                                                elif  len(cell.find_elements_by_xpath('.//input')):
                                                    cell = cell.find_elements_by_xpath('.//input')[0]
                                                    local_tk.log.info('Pointing to input.')
                                                if self.__check_visibility_from_config():
                                                    local_tk.log.debug('performing java script click')
                                                    js = 'var evType; element=arguments[0]; if (document.createEvent) {     evType = "Click executed through part-1";     var evt = document.createEvent("MouseEvents");     evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = "Click executed through part-2";   	setTimeout(function() {     element.click();   	}, 100); } return (evType);'
                                                    click=local_tk.driver.execute_script(js,webElement)
                                                else:
                                                    local_tk.log.debug('performing click')
                                                    local_tk.driver.execute_script("""arguments[0].focus()""",webElement)
                                                    cell.click()
                                                status=TEST_RESULT_PASS
                                                methodoutput=TEST_RESULT_TRUE
                                                local_tk.log.info('click action performed successfully')
                                                #logger.print_on_console('click action performed successfully')
                                            except Exception as e:
                                                local_tk.log.debug('performing java script click')
                                                js = 'var evType; element=arguments[0]; if (document.createEvent) {     evType = "Click executed through part-1";     var evt = document.createEvent("MouseEvents");     evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = "Click executed through part-2";   	setTimeout(function() {     element.click();   	}, 100); } return (evType);'
                                                click=local_tk.driver.execute_script(js,webElement)
                                                status=TEST_RESULT_PASS
                                                methodoutput=TEST_RESULT_TRUE
                                                local_tk.log.info('click action performed successfully')
                                                #logger.print_on_console('click action performed successfully')
                            except Exception as e:
                                local_tk.log.error(e)
                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                        elif len(input_arr)>2 and self.checkInputs(input_arr):
                            local_tk.log.info('click on an element inside a cell')
                            #logger.print_on_console('click on an element inside a cell')
                            row_number=int(input_arr[0])-1
                            col_number=int(input_arr[1])-1
                            tag=input_arr[2].lower()
                            index=int(input_arr[3])
                            eleStatus=False
                            counter = 1
                            local_tk.log.debug('finding the cell with given inputs')
                            cell=self.javascriptExecutor(webElement,row_number,col_number)
                            element_list=cell.find_elements_by_xpath('.//*')
                            #---------------------------condition when element list returns empty
                            if len(element_list)==0:
                                element_list.append(cell)
                            #---------------------------condition when element list returns empty
                            for member in element_list:
                                  js1='function getElementXPath(elt) {var path = "";for (; elt && elt.nodeType == 1; elt = elt.parentNode){idx = getElementIdx(elt);xname = elt.tagName;if (idx >= 1){xname += "[" + idx + "]";}path = "/" + xname + path;}return path;}function getElementIdx(elt){var count = 1;for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling){if(sib.nodeType == 1 && sib.tagName == elt.tagName){count++;}}return count;}return getElementXPath(arguments[0]).toLowerCase();'
                                  xpath=browser_Keywords.local_bk.driver_obj.execute_script(js1,member)
                                  cellChild = member#browser_Keywords.local_bk.driver_obj.find_element_by_xpath(xpath)
                                  tagName = cellChild.tag_name
                                  tagType = cellChild.get_attribute('type')
                                  xpath_elements=xpath.split('/')
                                  lastElement=xpath_elements[len(xpath_elements)-1]
                                  childindex=lastElement[lastElement.find("[")+1:lastElement.find("]")]
                                  childindex = int(childindex)
                                  if tag=='button':
                                       local_tk.log.debug('clicking on button')
                                       if( ((tagName==('input') or tagName==("button"))and tagType==('button')) or tagType==('submit') or tagType==('reset') or tagType==('file')):
                                           if index==childindex:
                                             eleStatus =True
                                           else:
                                             if counter==index:
                                                index =childindex
                                                eleStatus =True
                                             else:
                                                counter+=1
                                  elif tag=='image':
                                      local_tk.log.debug('clicking on image')
                                      if(tagName==('input') and (tagType==('img') or tagType==('image'))):
                                         if index==childindex:
                                            eleStatus =True
                                         else:
                                            if counter==index:
                                               index =childindex
                                               eleStatus =True
                                            else:
                                                counter+=1
                                      elif tagName =='img':
                                         local_tk.log.debug('clicking on img')
                                         if index==childindex:
                                                eleStatus =True
                                         else:
                                                if counter==index:
                                                   index =childindex
                                                   eleStatus =True
                                                else:
                                                    counter+=1
                                  elif tag=='img':
                                     local_tk.log.debug('clicking on img')
                                     if index==childindex:
                                            eleStatus =True
                                     else:
                                            if counter==index:
                                               index =childindex
                                               eleStatus =True
                                            else:
                                                counter+=1
                                  elif tag=='checkbox':
                                     local_tk.log.debug('clicking on check box')
                                     if(tagName==('input') and (tagType==('checkbox')) ):
                                         if index==childindex:
                                            eleStatus =True
                                         else:
                                            if counter==index:
                                               index =childindex
                                               eleStatus =True
                                            else:
                                                counter+=1
                                  elif tag=='radiobutton':
                                     local_tk.log.debug('clicking on radio button')
                                     if (tagName==('input') and tagType==('radio')):
                                        if index==childindex:
                                            eleStatus =True
                                        else:
                                            if counter==index:
                                               index =childindex
                                               eleStatus =True
                                            else:
                                                counter+=1
                                  elif tag=='textbox':
                                     local_tk.log.debug('clicking on radio text box')
                                     if (tagName==('input') and (tagType==('text') or tagType==('email') or tagType==('password') or tagType==('range') or tagType==('search') or tagType==('url')) ):
                                        if index==childindex:
                                            eleStatus =True
                                        else:
                                            if counter==index:
                                               index =childindex
                                               eleStatus =True
                                            else:
                                                counter+=1
                                  elif tag=='link':
                                    local_tk.log.debug('clicking on link')
                                    if(tagName==('a') or tagName==('input')):
                                        if index==childindex:
                                            eleStatus =True
                                        else:
                                            if counter==index:
                                               index =childindex
                                               eleStatus =True
                                            else:
                                                counter+=1
                                  else:
                                    local_tk.log.debug('Found an occurence of '+tagName)
                                    if tag==tagName:
                                         if index==childindex:
                                            eleStatus =True
                                         else:
                                            if counter==index:
                                               index =childindex
                                               eleStatus =True
                                            else:
                                                counter+=1


                                  if eleStatus==True:
                                    if cellChild.is_enabled():
                                        try:
                                          if not (cellChild is None):
                                            browser_Keywords.local_bk.driver_obj.execute_script("arguments[0].scrollIntoView(true);",cellChild)
                                            if isinstance(browser_Keywords.local_bk.driver_obj,webdriver.Ie):
                                                try:
                                                    local_tk.log.debug('performing click')
                                                    js = 'var evType; element=arguments[0]; if (document.createEvent) {     evType = "Click executed through part-1";     var evt = document.createEvent("MouseEvents");     evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = "Click executed through part-2";   	setTimeout(function() {     element.click();   	}, 100); } return (evType);'
                                                    click=browser_Keywords.local_bk.driver_obj.execute_script(js,cellChild)
                                                    status=webconstants.TEST_RESULT_PASS
                                                    methodoutput=TEST_RESULT_TRUE
                                                    break
                                                except Exception as e:
                                                    local_tk.log.debug('performing click')
                                                    action=action_chains.ActionChains(browser_Keywords.local_bk.driver_obj)
                                                    action.move_to_element(cellChild).click(cellChild).perform()
                                                    status=webconstants.TEST_RESULT_PASS
                                                    methodoutput=TEST_RESULT_TRUE
                                                    break
                                            else:
                                                try:
                                                    local_tk.log.debug('performing click')
                                                    cellChild.click()
                                                    status=webconstants.TEST_RESULT_PASS
                                                    methodoutput=TEST_RESULT_TRUE
                                                    break
                                                except Exception as e:
                                                    local_tk.log.debug('performing click')
                                                    js = 'var evType; element=arguments[0]; if (document.createEvent) {     evType = "Click executed through part-1";     var evt = document.createEvent("MouseEvents");     evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = "Click executed through part-2";   	setTimeout(function() {     element.click();   	}, 100); } return (evType);'
                                                    click=browser_Keywords.local_bk.driver_obj.execute_script(js,cellChild)
                                                    status=TEST_RESULT_PASS
                                                    methodoutput=TEST_RESULT_TRUE
                                                    break


                                        except Exception as e:
                                             local_tk.log.error(e)
                                             logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                             err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                            if not eleStatus:
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                local_tk.log.info(err_msg)
                                logger.print_on_console(err_msg)
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['INVALID_TABLE_INDEX'])
                            err_msg = ERROR_CODE_DICT['INVALID_TABLE_INDEX']

                    except Exception as e:
                        local_tk.log.error(e)
                        logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                else:
                    local_tk.log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                    err_msg = ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    logger.print_on_console(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                # return status,methodoutput,output_val,err_msg
            else:
                local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
            
            return status,methodoutput,output_val,err_msg
##
##            return status,methodoutput,output_val,err_msg


        def doubleCellClick(self,webElement,input_arr,*args):
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            index = False
            output_val=OUTPUT_CONSTANT
            local_tk.log.debug('reading the inputs')
            if(len(input_arr) > 1):
                                              
                                              
                local_tk.driver=browser_Keywords.local_bk.driver_obj
                local_tk.log.debug('got the driver instance from browser keyword')
                visibleFlag=True
                if visibleFlag==True:
                    try:
                        if webElement.tag_name.lower() == 'table':
                            if len(input_arr)==2:
                                local_tk.log.info('normal doubleCellClick')
                                #logger.print_on_console('normal doubleCellClick inside the cell')
                                row_number=int(input_arr[0])-1
                                col_number=int(input_arr[1])-1
                                cell=self.javascriptExecutor(webElement,row_number,col_number)
                                element_list=cell.find_elements_by_xpath('.//*')
                                if len(list(element_list))>0:
                                    xpath=self.getElemntXpath(element_list[0])
                                    cell=local_tk.driver.find_element_by_xpath(xpath)
                                try:
                                    local_tk.log.debug('checking for element not none')
                                    if(cell!=None):
                                        local_tk.log.debug('checking for element enabled')
                                        if cell.is_enabled():
                                            try:
                                                local_tk.log.debug('performing doublecell click')
                                                webdriver.ActionChains(browser_Keywords.local_bk.driver_obj).move_to_element(cell).double_click(cell).perform()
                                                status=webconstants.TEST_RESULT_PASS
                                                methodoutput=TEST_RESULT_TRUE
                                                local_tk.log.info('click action performed successfully')
                                            except Exception as e:
                                                local_tk.log.debug('error occured in doublecellclick')
                                except Exception as e:
                                    local_tk.log.error(e)
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                            elif len(input_arr)>2 and self.checkInputs(input_arr):
                                local_tk.log.info('doubleclick on an element inside a cell')
                                #logger.print_on_console('doubleclick on an element inside a cell')
                                row_number=int(input_arr[0])-1
                                col_number=int(input_arr[1])-1
                                tag=input_arr[2].lower()
                                index=int(input_arr[3])
                                eleStatus=False
                                counter = 1
                                local_tk.log.debug('finding the cell with given inputs')
                                cell=self.javascriptExecutor(webElement,row_number,col_number)
                                element_list=cell.find_elements_by_xpath('.//*')
                                #---------------------------condition when element list returns empty
                                if len(element_list)==0:
                                    element_list.append(cell)
                                #---------------------------condition when element list returns empty
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
                                    if tag=='button':
                                        local_tk.log.debug('double clicking on button')
                                        if( ((tagName==('input')or tagName==('button')) and tagType==('button')) or tagType==('submit') or tagType==('reset') or tagType==('file')):
                                            if index==childindex:
                                                eleStatus =True
                                            else:
                                                if counter==index:
                                                    index =childindex
                                                    eleStatus =True
                                                else:
                                                    counter+=1
                                    elif tag=='image':
                                        local_tk.log.debug('double clicking on image')
                                        if(tagName==('input') and (tagType==('img') or tagType==('image'))):
                                            if index==childindex:
                                                eleStatus =True
                                            else:
                                                if counter==index:
                                                    index =childindex
                                                    eleStatus =True
                                                else:
                                                    counter+=1
                                        elif tagName =='img':
                                            local_tk.log.debug('double clicking on img')
                                            if index==childindex:
                                                eleStatus =True
                                            else:
                                                if counter==index:
                                                    index =childindex
                                                    eleStatus =True
                                                else:
                                                    counter+=1
                                    elif tag=='img':
                                        local_tk.log.debug('double clicking on img')
                                        if index==childindex:
                                                eleStatus =True
                                        else:
                                            if counter==index:
                                                index =childindex
                                                eleStatus =True
                                            else:
                                                counter+=1
                                    elif tag=='checkbox':
                                        local_tk.log.debug('double clicking on check box')
                                        if(tagName==('input') and (tagType==('checkbox')) ):
                                            if index==childindex:
                                                eleStatus =True
                                            else:
                                                if counter==index:
                                                    index =childindex
                                                    eleStatus =True
                                                else:
                                                    counter+=1
                                    elif tag=='radiobutton':
                                        local_tk.log.debug('double clicking on radio button')
                                        if (tagName==('input') and tagType==('radio')):
                                            if index==childindex:
                                                eleStatus =True
                                            else:
                                                if counter==index:
                                                    index =childindex
                                                    eleStatus =True
                                                else:
                                                    counter+=1
                                    elif tag=='textbox':
                                        local_tk.log.debug('double clicking on text box')
                                        if (tagName==('input') and (tagType==('text') or tagType==('email') or tagType==('password') or tagType==('range') or tagType==('search') or tagType==('url')) ):
                                            if index==childindex:
                                                eleStatus =True
                                            else:
                                                if counter==index:
                                                    index =childindex
                                                    eleStatus =True
                                                else:
                                                    counter+=1
                                    elif tag=='link':
                                        local_tk.log.debug('double clicking on link')
                                        if(tagName==('a')):
                                            if index==childindex:
                                                eleStatus =True
                                            else:
                                                if counter==index:
                                                    index =childindex
                                                    eleStatus =True
                                                else:
                                                    counter+=1
                                    else:
                                        local_tk.log.debug('Found an occurence of '+tagName)
                                        if tag==tagName:
                                            if index==childindex:
                                                eleStatus =True
                                            else:
                                                if counter==index:
                                                    index =childindex
                                                    eleStatus =True
                                                else:
                                                    counter+=1
                                    if eleStatus==True:
                                        if cellChild.is_enabled():
                                            try:
                                                if not (cellChild is None):
                                                    browser_Keywords.local_bk.driver_obj.execute_script("arguments[0].scrollIntoView(true);",cellChild)
                                                    try:
                                                        local_tk.log.debug('performing double click')
                                                        webdriver.ActionChains(browser_Keywords.local_bk.driver_obj).move_to_element(cellChild).double_click(cellChild).perform()
                                                        status=webconstants.TEST_RESULT_PASS
                                                        methodoutput=TEST_RESULT_TRUE
                                                        break
                                                    except Exception as e:
                                                        local_tk.log.debug('error occured in doublecellclick')
                                                        break
                                            except Exception as e:
                                                local_tk.log.error(e)
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['INVALID_TABLE_INDEX'])
                                err_msg = ERROR_CODE_DICT['INVALID_TABLE_INDEX']
                    except Exception as e:
                        local_tk.log.error(e)
                        logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                        err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                else:
                    local_tk.log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                    err_msg = ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    logger.print_on_console(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
            else:
                local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
            return status,methodoutput,output_val,err_msg

        def getRowNumByText(self,webElement,input_val,*args):
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            row_number=None
            err_msg=None
            container=None
            lightning = False
            local_tk.log.debug('reading the inputs')
            text=input_val[0].strip()
            coreutilsobj=core_utils.CoreUtils()
            text=coreutilsobj.get_UTF_8(text)
            local_tk.driver=browser_Keywords.local_bk.driver_obj
            local_tk.log.debug('got the driver instance from browser keyword')
            visibleFlag=True
            if (webElement is not None):
                if visibleFlag==True:
                    try:
                        try:
                            lightning = len(webElement.find_elements_by_xpath('.//ancestor::lightning-datatable'))>0
                        except:

                            lightning = False
                        if webElement.tag_name.lower() == 'div' and webElement.get_attribute('role') == 'grid':
                            cell = webElement.find_element_by_xpath(".//div[@role='cell']/*[text()='"+text+"']").find_element_by_xpath("..")
                            row = cell.find_element_by_xpath("..")
                            row_number = row.get_attribute('aria-rowindex')
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:                                                           
                            if webElement.tag_name.lower() != 'table' and webElement.get_attribute('role') == 'grid':
                                body = True
                                right = True
                                if len(input_val)>=3:
                                    if (input_val[1].lower() == 'body') : body = True
                                    elif (input_val[1].lower() == 'header') : body = False
                                    else: err_msg = "Invalid input"
                                    if (input_val[2].lower() == 'right') : right = True
                                    elif (input_val[2].lower() == 'left') : right = False
                                    elif not(err_msg): err_msg = "Invalid input"
                                if not (err_msg):
                                    if body:
                                        if right:
                                            try:
                                                container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                            except:
                                                container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                                        else:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                                        rows = container.find_elements_by_xpath(".//div[@role='row']")
                                    else:
                                        if right:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                                        else:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
                                        rows = container.find_elements_by_xpath(".//div[contains(@class,'ag-header-row')]")
                                    for i in range(len(rows)):
                                        if body:
                                            cells = rows[i].find_elements_by_xpath(".//div[@role='gridcell']")
                                        else:
                                            cells = rows[i].find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                        for j in range(len(cells)):
                                            cellVal = self.getChildNodes(cells[j])
                                            cellVal=cellVal.strip()
                                            local_tk.log.debug("cellvalue:"+cellVal+" ; text:"+text+" ; attr:"+input_val[3])
                                            if text in cellVal:
                                                if len(input_val)==4:
                                                    row_number = rows[i].get_attribute(input_val[3])
                                                else:
                                                    row_number = i+1
                                                break
                                        if row_number:
                                            break
                                    if row_number:
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                    else:
                                        err_msg = 'Error in fetching Row number'
                                        local_tk.log.info('Error in fetching Row number')
                                        logger.print_on_console('Error in fetching Row number')
                            elif (lightning):
                                cell=webElement.find_elements_by_xpath('//*[text()="'+text+'"]')
                                if len(cell)!=0:
                                    tr=cell[0].find_element_by_xpath('.//ancestor::tr')
                                    rows=webElement.find_elements_by_xpath('.//tr')
                                    for i in range(0,len(rows)):
                                        if rows[i]==tr:
                                            row_number=i+1
                                            status=TEST_RESULT_PASS
                                            methodoutput=TEST_RESULT_TRUE
                                            break
                                local_tk.log.info('Got the result : %s',str(row_number))
                                logger.print_on_console('Got the result : ',str(row_number))
                            else:
                                js='var temp = fun(arguments[0], arguments[1]); return temp; function fun(table, str) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy, child;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (cell.innerText.indexOf(str)>= 0 && cell.innerText && cell.innerText.trim()==str) return yyy + cell.rowSpan;             if (cell.children.length > 0) {                 for (var i = 0; i < cell.children.length; i++) {                     child = cell.children[i];                     var value = child.value || child.innerText;                     if (value && value.trim() == str) return yyy + cell.rowSpan; 					else{ 					var a=value; 					if(a){ 					var b=a; 					if(b.indexOf(str)>=0 && b==str)return yyy + cell.rowSpan; 					}	 				}			 					                 }             }         }     }     return null; };'
                                row_number=browser_Keywords.local_bk.driver_obj.execute_script(js,webElement,text)
                                if row_number:
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                        local_tk.log.info('Got the result : %s',str(row_number))
                        logger.print_on_console('Got the result : ',str(row_number))
                    except Exception as e:
                        local_tk.log.error(e)
                        if container==None:
                            js='var temp = fun(arguments[0], arguments[1]); return temp; function fun(table, str) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy, child;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (cell.innerText.indexOf(str)>= 0) return yyy + cell.rowSpan;             if (cell.children.length > 0) {                 for (var i = 0; i < cell.children.length; i++) {                     child = cell.children[i];                     var value = child.value || child.innerText;                     if (value && value.trim() == str) return yyy + cell.rowSpan; 					else{ 					var a=value; 					if(a){ 					var b=a; 					if(b.indexOf(str)>=0)return yyy + cell.rowSpan; 					}	 				}			 					                 }             }         }     }     return null; };'
                            row_number=browser_Keywords.local_bk.driver_obj.execute_script(js,webElement,text)
                            if row_number:
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                            local_tk.log.info('Got the result : %s',str(row_number))
                            logger.print_on_console('Got the result : ',str(row_number))
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                else:
                    local_tk.log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                    err_msg = ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    logger.print_on_console(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
            else:
                err_msg = ERROR_CODE_DICT['MSG_ELEMENT_NOT_FOUND']
            return status,methodoutput,row_number,err_msg

        def getColNumByText(self,webElement,input_val,*args):
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            col_number=None
            err_msg = None
            container = None
            lightning = False
            local_tk.driver=browser_Keywords.local_bk.driver_obj
            local_tk.log.debug('got the driver instance from browser keyword')
            visibleFlag=True
            local_tk.log.debug('reading the inputs')
            text=input_val[0].strip()
            coreutilsobj=core_utils.CoreUtils()
            text=coreutilsobj.get_UTF_8(text)
            if (webElement is not None):
                if visibleFlag==True:
                    try:
                        try:
                            lightning = len(webElement.find_elements_by_xpath('.//ancestor::lightning-datatable'))>0
                        except:
                            lightning = False
                        if webElement.tag_name.lower() != 'table' and webElement.get_attribute('role') == 'grid':
                            body = True
                            right = True
                            if len(input_val)>=3:
                                if (input_val[1].lower() == 'body') : body = True
                                elif (input_val[1].lower() == 'header') : body = False
                                else: err_msg = "Invalid input"
                                if (input_val[2].lower() == 'right') : right = True
                                elif (input_val[2].lower() == 'left') : right = False
                                elif not(err_msg): err_msg = "Invalid input"
                            if not(err_msg):
                                if body:
                                    if right:
                                        try:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-body-container')]")
                                        except:
                                            container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-center-cols-container')]")
                                    else:
                                        container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-cols-container')]")
                                    rows = container.find_elements_by_xpath(".//div[@role='row']")
                                else:
                                    if right:
                                        container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-header-viewport')]")
                                    else:
                                        container = webElement.find_element_by_xpath(".//div[contains(@class,'ag-pinned-left-header')]")
                                    rows = container.find_elements_by_xpath(".//div[contains(@class,'ag-header-row')]")
                                for i in range(len(rows)):
                                    if body:
                                        cells = rows[i].find_elements_by_xpath(".//div[@role='gridcell']")
                                    else:
                                        cells = rows[i].find_elements_by_xpath(".//div[contains(@class,'ag-header-cell')]")
                                    for j in range(len(cells)):
                                        cellVal = self.getChildNodes(cells[j])
                                        cellVal=cellVal.strip()
                                        local_tk.log.debug("cellvalue:"+cellVal+" ; text:"+text+" ; attr:"+input_val[3])
                                        if text in cellVal:
                                            if len(input_val)==4:
                                                col_number = cells[j].get_attribute(input_val[3])
                                            else:
                                                col_number = j+1
                                            break
                                    if col_number:
                                        break
                                if col_number:
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                                else:
                                    err_msg = 'Error in fetching Col number'
                                    local_tk.log.info('Error in fetching Col number')
                                    logger.print_on_console('Error in fetching Col number')
                        elif (lightning):
                            cell=webElement.find_element_by_xpath('//*[text()="'+text+'"]')
                            if len(cell)!=0:
                                tc=cell.find_elements_by_xpath('.//ancestor::th')
                                if len(tc)==0:
                                    tc=cell.find_elements_by_xpath('.//ancestor::td')
                                if(len(tc)!=0):
                                    tr=tc[0].find_elements_by_xpath('.//ancestor::tr')
                                    cols=tr[0].find_elements_by_xpath('.//th')
                                    cols+=tr[0].find_elements_by_xpath('.//td')
                                    for i in range(0,len(cols)):
                                        if cols[i]==tc[0]:
                                            col_number=i+1
                                            status=TEST_RESULT_PASS
                                            methodoutput=TEST_RESULT_TRUE
                                            break
                            local_tk.log.info('Got the result : %s',str(col_number))
                            logger.print_on_console('Got the result : ',str(col_number))
                        else:
                            js='var temp = fun(arguments[0], arguments[1]); return temp; function fun(table, str) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy, child;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (cell.innerText.indexOf(str)>= 0 && cell.innerText && cell.innerText.trim().length === str.length) return xx + cell.colSpan;             if (cell.children.length > 0) {                 for (var i = 0; i < cell.children.length; i++) {                     child = cell.children[i];   var sap=child.value || child.innerText;  var check_match=sap;                if (check_match && str === check_match.trim()) return xx + cell.colSpan; 					else{ 					var a=sap; 					if(a){ 					var b=a; 					if(b.indexOf(str)>=0 && b==str)return xx + cell.rowSpan; 					}	 				} 							 					                 }             }         }     }     return null; };'
                            col_number=local_tk.driver.execute_script(js,webElement,text)
                            if col_number:
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                        local_tk.log.info('Got the result : %s',str(col_number))
                        logger.print_on_console('Got the result : ',str(col_number))
                    except Exception as e:
                        local_tk.log.error(e)
                        #logger.print_on_console(e)
                        if container==None:
                            js='var temp = fun(arguments[0], arguments[1]); return temp; function fun(table, str) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy, child;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (cell.innerText.indexOf(str)>= 0 && cell.innerText && cell.innerText.trim().length === str.length) return xx + cell.colSpan;             if (cell.children.length > 0) {                 for (var i = 0; i < cell.children.length; i++) {                     child = cell.children[i];   var sap=child.value || child.innerText;  var check_match=sap;                if (check_match && str === check_match.trim()) return xx + cell.colSpan; 					else{ 					var a=sap; 					if(a){ 					var b=a; 					if(b.indexOf(str)>=0 && b==str)return xx + cell.rowSpan; 					}	 				} 							 					                 }             }         }     }     return null; };'
                            col_number=local_tk.driver.execute_script(js,webElement,text)
                            if col_number:
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                            local_tk.log.info('Got the result : %s',str(col_number))
                            logger.print_on_console('Got the result : ',str(col_number))
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                            err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                else:
                    local_tk.log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                    err_msg = ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                    logger.print_on_console(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
            else:
                err_msg = ERROR_CODE_DICT['MSG_ELEMENT_NOT_FOUND']
            return status,methodoutput,col_number,err_msg


        def getChildNodes(self,webElement):
            contents=None
            try:
                js="""var mytarget = arguments[0];
var mynodes = mytarget.childNodes;
var result = [];
if (typeof String.prototype.trim !== "function") {
    String.prototype.trim = function() {
        return this.replace(/^\\s+|\\s+$/g, "");
    }
}
recursfunc(mynodes);
return result.toString();

function recursfunc(mynodes) {
debugger;
    for (var i = 0; i < mynodes.length; i++) {
        if (mynodes[i].nodeName.toUpperCase() == \"#TEXT\") {             
            if ((mynodes[i].parentNode.nodeName.toUpperCase() != \"OPTION\") & (mynodes[i].parentNode.nodeName.toUpperCase() != \"SCRIPT\")) {
      			var myvalue = mynodes[i].nodeValue;                 
      			if (myvalue.trim().length > 0) {
                  if (result[result.length-1]!=myvalue)
                    result.push(myvalue);                 
                }             
    		}         
		} 
		else if (mynodes[i].nodeName.toUpperCase() == \"INPUT\") {
        	if (mynodes[i].type.toUpperCase() == \"RADIO\") {  
				if (mynodes[i].checked == true) {   
                	var myvalue = \"Selected\";                 
                } 
				else {
                	var myvalue = \"Unselected\";                 
                }             
			} 
            else if (mynodes[i].type.toUpperCase() == \"CHECKBOX\") {
            	if (mynodes[i].checked == true) {
              		var myvalue = \"Checked\";                 
                } 
				else {                     
                	var myvalue = \"Unchecked\";                 
                }             
			} 
            else if ((mynodes[i].type.toUpperCase() == \"BUTTON\") | (mynodes[i].type.toUpperCase() == \"SUBMIT\") | (mynodes[i].type.toUpperCase() == \"TEXT\")) {
            	var myvalue = mynodes[i].value;             
			} 
            else if (mynodes[i].type.toUpperCase() == \"IMAGE\") {
            	var myvalue = mynodes[i].title;                 
				if (myvalue.trim().length < 1) {
                	myvalue = mynodes[i].value;
                  	if (myvalue != undefined) {
                    	if (myvalue.trim().length < 1) {
                        	myvalue = \"Image\";                         
                        }                     
                    } 
                  	else {
                    	myvalue = \"Image\";                     
                    }                 
                }             
			}
            else { 
            	var myvalue=mynodes[i].value; 
            }             
            if (result[result.length-1]!=myvalue)
			    result.push(myvalue);         
		} 
        else if (mynodes[i].nodeName.toUpperCase() == \"IMG\") {
        	var myvalue = mynodes[i].title;             
			if (myvalue.trim().length < 1) {
            	myvalue = mynodes[i].value;                 
              	if (myvalue != undefined) {
                	if (myvalue.trim().length < 1) {
                    	myvalue = \"Image\";                     
                    }                 
                } 
              	else {
                	myvalue = \"Image\";                 
                }             
            }     
            if (result[result.length-1]!=myvalue)        
			    result.push(myvalue);         
		} 
        else if (mynodes[i].nodeName.toUpperCase() == \"TEXTAREA\") {
        	var myvalue = mynodes[i].value;    
            if (result[result.length-1]!=myvalue)         
			    result.push(myvalue);         
		} 
        else if (mynodes[i].nodeName.toUpperCase() == \"SELECT\") {
        	var myselect = mynodes[i].selectedOptions;             
			if (myselect != undefined | myselect != null) {
            	for (var j = 0; j < myselect.length; j++) {
                	var myvalue = mynodes[i].selectedOptions[j].textContent;
                    if (result[result.length-1]!=myvalue)
                  	    result.push(myvalue);                 
                }             
            } 
			else {
            	var myvalue = dropdowncallie(mynodes[i]);
                if (result[result.length-1]!=myvalue)
              	    result.push(myvalue);             
            }         
		} 
        else if ((mynodes[i].nodeName.toUpperCase() == \"I\")) {
        	var myvalue = mynodes[i].textContent;    
            if (result[result.length-1]!=myvalue)         
			    result.push(myvalue);         
		}         
        if (mynodes[i].hasChildNodes()) {
        	recursfunc(mynodes[i].childNodes);         
        }     
	} 
}  
function dropdowncallie(op) {
	var x = op.options[op.selectedIndex].text;
  	return x; 
};"""
                # js='var mytarget = arguments[0]; var mynodes = mytarget.childNodes; var result = []; if (typeof  String.prototype.trim  !== "function")  {       String.prototype.trim  =   function()  {             return  this.replace(/^\\s+|\\s+$/g,"");        } } recursfunc(mynodes); return result.toString();  function recursfunc(mynodes) {     for (var i = 0; i < mynodes.length; i++) {         if (mynodes[i].nodeName.toUpperCase() == \"#TEXT\") {             if ((mynodes[i].parentNode.nodeName.toUpperCase() != \"OPTION\") & (mynodes[i].parentNode.nodeName.toUpperCase() != \"SCRIPT\")) {                 var myvalue = mynodes[i].nodeValue;                 if (myvalue.trim().length > 0) {                     result.push(myvalue);                 }             }         } else if (mynodes[i].nodeName.toUpperCase() == \"INPUT\") {             if (mynodes[i].type.toUpperCase() == \"RADIO\") {                 if (mynodes[i].checked == true) {                     var myvalue = \"Selected\";                 } else {                     var myvalue = \"Unselected\";                 }             } else if (mynodes[i].type.toUpperCase() == \"CHECKBOX\") {                 if (mynodes[i].checked == true) {                     var myvalue = \"Checked\";                 } else {                     var myvalue = \"Unchecked\";                 }             } else if ((mynodes[i].type.toUpperCase() == \"BUTTON\") | (mynodes[i].type.toUpperCase() == \"SUBMIT\") | (mynodes[i].type.toUpperCase() == \"TEXT\")) {                 var myvalue = mynodes[i].value;             } else if (mynodes[i].type.toUpperCase() == \"IMAGE\") {                 var myvalue = mynodes[i].title;                 if (myvalue.trim().length < 1) {                     myvalue = mynodes[i].value;                     if (myvalue != undefined) {                         if (myvalue.trim().length < 1) {                             myvalue = \"Image\";                         }                     } else {                         myvalue = \"Image\";                     }                 }             }else{ var myvalue=mynodes[i].value; }             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \"IMG\") {             var myvalue = mynodes[i].title;             if (myvalue.trim().length < 1) {                 myvalue = mynodes[i].value;                 if (myvalue != undefined) {                     if (myvalue.trim().length < 1) {                         myvalue = \"Image\";                     }                 } else {                     myvalue = \"Image\";                 }             }             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \"TEXTAREA\") {             var myvalue = mynodes[i].value;             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \"SELECT\") {             var myselect = mynodes[i].selectedOptions;             if (myselect != undefined | myselect != null) {                 for (var j = 0; j < myselect.length; j++) {                     var myvalue = mynodes[i].selectedOptions[j].textContent;                     result.push(myvalue);                 }             } else {                 var myvalue = dropdowncallie(mynodes[i]);                 result.push(myvalue);             }         } else if ((mynodes[i].nodeName.toUpperCase() == \"I\")) {             var myvalue = mynodes[i].textContent;             result.push(myvalue);         }         if (mynodes[i].hasChildNodes()) {             recursfunc(mynodes[i].childNodes);         }     } }  function dropdowncallie(op) {     var x = op.options[op.selectedIndex].text;     return x; };'
                contents = browser_Keywords.local_bk.driver_obj.execute_script(js,webElement)
            except Exception as e:
                local_tk.log.error(e)
            return contents

        def getRowCountJs(self,webElement):
            js = 'var targetTable = arguments[0]; var rowCount = targetTable.rows; return rowCount.length;'
            row_count = browser_Keywords.local_bk.driver_obj.execute_script(js,webElement)
            return row_count

        def javascriptExecutor(self,webElement,row_num,col_num):
            remoteWebElement=None
            try:
                js='var temp = fun(arguments[0], arguments[2], arguments[1]); return temp;  function fun(table, x, y) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];    if (row.style!=undefined && row.style.display=="none")    {y++;continue;};     for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (xx <= x && x < xx + cell.colSpan && yyy <= y && y < yyy + cell.rowSpan) return cell;         }     }     return null; };'
                remoteWebElement=browser_Keywords.local_bk.driver_obj.execute_script(js,webElement,row_num,col_num)
            except Exception as e:
                local_tk.log.error(e)
            return remoteWebElement

        def getColoumnCountJs(self,webElement):
            js = 'var targetTable = arguments[0]; var columnCount = 0; var rows = targetTable.rows; if(rows.length > 0) { 	for (var i = 0; i < rows.length; i++) { 		var cells = rows[i].cells; 		var tempColumnCount = 0; 		for (var j = 0; j < cells.length; j++) { 			tempColumnCount += cells[j].colSpan; 		} 		if (tempColumnCount > columnCount) { 			columnCount = tempColumnCount; 		} 	} } return columnCount;'
            column_count = browser_Keywords.local_bk.driver_obj.execute_script(js,webElement)
            return column_count

        def getTooltip(self,webElement,row_num,col_num):
            contents=None
            try:
                #author : arpitha.b.v
                #commented javascript,because removed '\' in string appending of title attribute
               ## js = 'var temp = tooltip(arguments[0], arguments[1], arguments[2]); return temp;  function tooltip(table, row, col) {     var no_of_rows = table.rows.length;     var no_of_col = table.rows[row - 1].cells.length;     var ele = table.rows[row - 1];     var i, j, k, tp;     for (i = 0; i < no_of_rows; i++) {         for (j = 0; j < no_of_col; j++) {             if (i == row - 1 && j == col - 1) {                 if (ele.cells[col - 1].hasAttribute(\"title\")) {                     tp = ele.cells[col - 1].title;                 } else if (ele.cells[col - 1].children.length > 0) {                     for (k = 0; k < ele.cells[col - 1].children.length; k++) {                         finalele = recurseDomChildren(ele.cells[col - 1].children[k]);                         if (finalele != undefined && finalele != \"\") {                             if (finalele.hasAttribute(\"title\") && finalele != undefined) {                                 tp = finalele.title;                                 break;                             }                         }                     }                 } else {                     if (ele.hasAttribute(\"title\") && ele != undefined) {                         tp = ele.title;                     }                 }             }         }     }     return tp; };  function recurseDomChildren(start) {     var nodes, ele1;     if (start.hasAttribute(\"title\") && start != undefined) {         ele1 = start;         return ele1;     } else if (start.childNodes.length > 0) {         nodes = start.childNodes;         ele1 = loopNodeChildren(nodes);         if (ele1 != \"\") {             return ele1;         }     } }  function loopNodeChildren(nodes) {     var node, ele2;     for (var i = 0; i < nodes.length; i++) {         node = nodes[i];         if (node.childNodes.length > 0) {             ele2 = recurseDomChildren(node);             if (ele2 != \"\"  && ele2 != undefined) {               if(ele2.hasAttribute(\"title\")){                 break;               }             }         } else if (node.nodeType === 1) {             if (node.hasAttribute(\"title\") && node != undefined) {                 ele2 = node;                 break;             }         } else {             ele2 = \"\";         }     }     return ele2; };'
                js="""var temp = tooltip(arguments[0], arguments[1], arguments[2]); return temp; function tooltip(table, row, col) {     var no_of_rows = table.rows.length;     var no_of_col = table.rows[row - 1].cells.length;     var ele = table.rows[row - 1];     var i, j, k, tp;     for (i = 0; i < no_of_rows; i++) {         for (j = 0; j < no_of_col; j++) {             if (i == row - 1 && j == col - 1) {                 if (ele.cells[col - 1].hasAttribute("title")) {                           tp = ele.cells[col - 1].title;                     }                     else if (ele.cells[col - 1].children.length > 0) {                         for (k = 0; k < ele.cells[col - 1].children.length; k++) {                             finalele = recurseDomChildren(ele.cells[col - 1].children[k]);                             if (finalele != undefined && finalele != "") {                                                            if (finalele.hasAttribute("title") && finalele != undefined) {                                             tp = finalele.title;                                         break;                                     }                                 }                             }                         } else {                             if (ele.hasAttribute("title") && ele != undefined) {                                          tp = ele.title;                                 }                             }                         }                     }                 }                 return tp;             };              function recurseDomChildren(start) {                 var nodes, ele1;                 if (start.hasAttribute("title") && start != undefined) {                           ele1 = start;                         return ele1;                     }                     else if (start.childNodes.length > 0) {                         nodes = start.childNodes;                         ele1 = loopNodeChildren(nodes);                         if (ele1 != "") {                                      return ele1;                         }                     }                 }                  function loopNodeChildren(nodes) {                     var node, ele2;                     for (var i = 0; i < nodes.length; i++) {                         node = nodes[i];                         if (node.childNodes.length > 0) {                             ele2 = recurseDomChildren(node);                             if (ele2 != ""  && ele2 != undefined) {                                      if (ele2.hasAttribute("title")){                                                     break;                                     }                                 }                             }                             else if (node.nodeType === 1) {                                 if (node.hasAttribute("title") && node != undefined) {                                              ele2 = node;                                         break;                                     }                                 }                                 else {                                     ele2 = "";                                       }                             }                             return ele2;                         }; """
                contents = browser_Keywords.local_bk.driver_obj.execute_script(js,webElement,row_num,col_num)
            except Exception as e:
                local_tk.log.error(e)
            return contents

        def getElemntXpath(self,webElement):
            xpath=None
            try:
                js = 'function getElementXPath(elt) {var path = "";for (; elt && elt.nodeType == 1; elt = elt.parentNode){idx = getElementIdx(elt);xname = elt.tagName;if (idx >= 1){xname += "[" + idx + "]";}path = "/" + xname + path;}return path;}function getElementIdx(elt){var count = 1;for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling){if(sib.nodeType == 1 && sib.tagName == elt.tagName){count++;}}return count;}return getElementXPath(arguments[0]).toLowerCase();'
                xpath = browser_Keywords.local_bk.driver_obj.execute_script(js,webElement)
            except Exception as e:
                local_tk.log.error(e)
            return xpath

        def getInnerTable(self,webElement,input_val,*args):
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            web_element=None
            err_msg=None
            if((webElement is not None) and (input_val is not None)):
                try:
                    if(len(input_val) == 2):
                        local_tk.log.info('Input value is 2')
                        cell_row = input_val[0]
                        local_tk.log.info('cell row')
                        local_tk.log.info(cell_row)
                        input_val[1]=str(int(input_val[1])-1)
                        cell_col = input_val[1]
                        local_tk.log.info('cell_col')
                        local_tk.log.info(cell_col)
                        script ="""var temp = fun(arguments[0], arguments[1], arguments[2]); return temp;  function fun(table, x, y) {     row = table.rows[x];     cell = row.cells[y];     tableCheck = cell.getElementsByTagName('table'); if(tableCheck.length > 0){        console.log(tableCheck[0]);       return tableCheck[0];    }else{      return null; } }"""
                        web_element = browser_Keywords.local_bk.driver_obj.execute_script(script,webElement,cell_row,cell_col)
                        if( web_element.tag_name == 'table'):
                            logger.print_on_console('Inner table reference obtained')
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            web_element = None
                            err_msg = 'Table element not found'
                    elif(len(input_val) == 1):
                        local_tk.log.info('Input value is 1')
                        row_no = input_val[0]
                        local_tk.log.info('row_no')
                        local_tk.log.info(row_no)
                        script = """var ele = arguments[0]; var row = arguments[1]; var temp = fun(ele, row); return temp;  function fun(tableEle, rowNo) {     row = tableEle.rows[rowNo];     flag = false;     count = 0;     a = [];     eleCollection = row.getElementsByTagName('table');     if (eleCollection.length > 0) {         return eleCollection[0];     } else {         if (flag != true) {             child = tableEle.children;             ele = child[0];             trCount = ele.childElementCount;             for (i = rowNo; i < trCount; i++) {                 count++;                 if (count > 1) {                     row = a[1];                 }                 a = recursfunc(row);                 if (a[0] == true) {                     return a[1];                     break;                 }             }         }     }     return "null"; }  function recursfunc(innerTable) {     check = [];     chk = false;     firstRef = innerTable.nextElementSibling;     relativeRef = firstRef.getElementsByTagName('table');     if (relativeRef.length > 0) {         actual_ref = relativeRef[0];         flag = true;         chk = true;         check[0] = chk;         check[1] = actual_ref;         return check;     } else {         check[0] = chk;         check[1] = firstRef;         return check;     } } """
                        web_element = browser_Keywords.local_bk.driver_obj.execute_script(script,webElement,row_no)
                        if( web_element.tag_name == 'table'):
                            logger.print_on_console('Inner table reference obtained')
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            web_element = None
                            err_msg = 'Table element not found'
                    ##elif(len(input_val == 0)):
                    ##    script = """var ele = arguments[0]; var temp = fun(ele); console.log(temp); return temp;  function fun(tableEle) {     eleCollection = tableEle.getElementsByTagName('table');     if (eleCollection.length > 0) {         console.log(eleCollection.length);         return eleCollection[0];     }     return "null";     console.log("No Inner Table") };"""
                    ##    web_element = browser_Keywords.driver_obj.execute_script(script)
                except Exception as e:
                    local_tk.log.error(e)
                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            return status,methodoutput,web_element,err_msg


        """
        Match with Exact text

        """

        def selectByAbsoluteValue(self,webelement,input,*args):
            status=webconstants.TEST_RESULT_FAIL
            result=webconstants.TEST_RESULT_FALSE
            visibilityFlag=True
            verb = OUTPUT_CONSTANT
            err_msg=None
            if webelement is not None:
                if webelement.tag_name=='table':
                    if (input is not None) :
                        if len(input)==5:
                            dropVal=input[2]
                            row_num=int(input[0])
                            col_num=int(input[1])
                            inp_val = input[4]
                    if dropVal.lower()=='dropdown':
                        local_tk.driver=browser_Keywords.local_bk.driver_obj
                        local_tk.log.debug('got the driver instance from browser keyword')
                        visibleFlag=True
                        if visibleFlag==True:
                            try:
                                cell=self.javascriptExecutor(webelement,row_num,col_num)
                                element_list=cell.find_elements_by_xpath('.//*')
                                if len(list(element_list))>0:
                                    xpath=self.getElemntXpath(element_list[0])
                                    cell=browser_Keywords.local_bk.driver_obj.find_element_by_xpath(xpath)
                                try:
                                    local_tk.log.debug('checking for element not none')
                                    if(cell!=None):
                                        local_tk.log.debug('checking for element enabled')
                                        if cell.is_enabled():
                                            if len(inp_val.strip()) != 0:
                                                select = Select(cell)
                                                iList = select.options
                                                temp=[]
                                                for i in range (0,len(iList)):
                                                    internal_val = iList[i].text
                                                    temp.append(internal_val)
                                                if (inp_val in temp):
                                                    status=webconstants.TEST_RESULT_PASS
                                                    result=webconstants.TEST_RESULT_TRUE
                                                    local_tk.log.info('Values Match')
                                                else:
                                                    logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                                    local_tk.log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                                    err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                            else:
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                                local_tk.log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                except Exception as e:
                                    local_tk.log.error(e)
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                    err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
                            except Exception as e:
                                local_tk.log.error(e)
                                logger.print_on_console(ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION'])
                                err_msg=ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']
            return status,result,verb,err_msg
 


        def verticalScroll(self,webElement,input,*args):
            local_tk.driver=browser_Keywords.local_bk.driver_obj
            local_tk.log.debug('got the driver instance from browser keyword')
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            output_val=OUTPUT_CONSTANT
            visibleFlag=True
            err_msg=None
            if visibleFlag==True:
                try:
                    local_tk.log.debug('checking for element')
                    if webElement!=None:
                        if webElement.tag_name.lower() != 'table' and webElement.get_attribute('role') == 'grid':
                            direction = input[0]
                            try:
                                times = int(input[1])
                            except:
                                times = 0
                                err_msg='Invalid input: "times" should be a non-zero integer'
                                local_tk.log.error('Invalid input: "times" should be a non-zero integer')
                                logger.print_on_console('Invalid input: "times" should be a non-zero integer')
                            if times > 0:
                                if SYSTEM_OS == "Windows":
                                    user32 = windll.user32
                                    time.sleep(1)
                                    if direction.lower() == 'up':
                                        for i in range(times):
                                            user32.mouse_event(0x0800, None, None, 400, None)
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                    elif direction.lower() == 'down':
                                        for i in range(times):
                                            user32.mouse_event(0x0800, None, None, -400, None)
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                    else:
                                        err_msg='Direction given is incorrect'
                                        local_tk.log.error('Direction given is incorrect')
                                        logger.print_on_console('Direction given is incorrect')
                                else:
                                    if direction.lower() == 'down':
                                        times = (times * (-4))
                                        mouse = Controller()
                                        time.sleep(1)
                                        mouse.scroll(0, times)
                                        del mouse
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                    elif direction.lower() == 'up':
                                        times = (times * 4)
                                        mouse = Controller()
                                        time.sleep(1)
                                        mouse.scroll(0, times)
                                        del mouse
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                    else:
                                        err_msg='Direction given is incorrect'
                                        local_tk.log.error('Direction given is incorrect')
                                        logger.print_on_console('Direction given is incorrect')
                            else:
                                err_msg='Invalid input: "times" should be a non-zero integer'
                                local_tk.log.error('Invalid input: "times" should be a non-zero integer')
                                logger.print_on_console('Invalid input: "times" should be a non-zero integer')
                    else:
                        err_msg='Element not found'
                        local_tk.log.error('Element not found')
                        logger.print_on_console('Element not found')
                except Exception as e:
                    local_tk.log.error(e,exc_info=True)
                    logger.print_on_console("Error while scrolling")
                    err_msg = "Error while scrolling"
            else:
                local_tk.log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                err_msg = ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                logger.print_on_console(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
            return status,methodoutput,output_val,err_msg


        def horizontalScroll(self,webElement,input,*args):
            local_tk.driver=browser_Keywords.local_bk.driver_obj
            local_tk.log.debug('got the driver instance from browser keyword')
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            output_val=OUTPUT_CONSTANT
            visibleFlag=True
            err_msg=None
            if visibleFlag==True:
                try:
                    local_tk.log.debug('checking for element')
                    if webElement!=None:
                        if webElement.tag_name.lower() != 'table' and webElement.get_attribute('role') == 'grid':
                            direction = input[0]
                            try:
                                times = int(input[1])
                            except:
                                times = 0
                                err_msg='Invalid input: "times" should be a non-zero integer'
                                local_tk.log.error('Invalid input: "times" should be a non-zero integer')
                                logger.print_on_console('Invalid input: "times" should be a non-zero integer')
                            if times > 0:
                                if SYSTEM_OS == "Windows":
                                    user32 = windll.user32
                                    time.sleep(1)
                                    if direction.lower() == 'right':
                                        for i in range(times):
                                            user32.mouse_event(0x01000, None, None, 400, None)
                                            status=TEST_RESULT_PASS
                                            methodoutput=TEST_RESULT_TRUE
                                    elif direction.lower() == 'left':
                                        for i in range(times):
                                            user32.mouse_event(0x01000, None, None, -400, None)
                                            status=TEST_RESULT_PASS
                                            methodoutput=TEST_RESULT_TRUE
                                    else:
                                        err_msg='Direction given is incorrect'
                                        local_tk.log.error('Direction given is incorrect')
                                        logger.print_on_console('Direction given is incorrect')
                                else:
                                    if direction.lower() == 'left':
                                        times = (times * (-4))
                                        mouse = Controller()
                                        time.sleep(1)
                                        mouse.scroll(times,0)
                                        del mouse
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                    elif direction.lower() == 'right':
                                        times = (times * 4)
                                        mouse = Controller()
                                        time.sleep(1)
                                        mouse.scroll(times,0)
                                        del mouse
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                    else:
                                        err_msg='Direction given is incorrect'
                                        local_tk.log.error('Direction given is incorrect')
                                        logger.print_on_console('Direction given is incorrect')
                            else:
                                err_msg='Invalid input: "times" should be a non-zero integer'
                                local_tk.log.error('Invalid input: "times" should be a non-zero integer')
                                logger.print_on_console('Invalid input: "times" should be a non-zero integer')
                    else:
                        err_msg='Element not found'
                        local_tk.log.error('Element not found')
                        logger.print_on_console('Element not found')
                except Exception as e:
                    local_tk.log.error(e,exc_info=True)
                    logger.print_on_console("Error while scrolling")
                    err_msg = "Error while scrolling"
            else:
                local_tk.log.info(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
                err_msg = ERROR_CODE_DICT['ERR_HIDDEN_OBJECT']
                logger.print_on_console(ERROR_CODE_DICT['ERR_HIDDEN_OBJECT'])
            return status,methodoutput,output_val,err_msg

        def checkInputs(self, inputs):
            if len(inputs) == 4:
                if int(inputs[3]) <= 0:
                    return False
            return True