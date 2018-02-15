#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     08-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from selenium.webdriver.support.ui import Select
from selenium import webdriver
import browser_Keywords
import webconstants
import  utilweb_operations
import logger
import radio_checkbox_operations
import core_utils
import logging
import platform
import readconfig
from sendfunction_keys import SendFunctionKeys
from constants import *
log = logging.getLogger('dropdown_listbox.py')
class DropdownKeywords():

    def __init__(self):
        self.radioKeywordsObj=radio_checkbox_operations.RadioCheckboxKeywords()
        self.util = utilweb_operations.UtilWebKeywords()
    def selectValueByIndex(self,webelement,input,*args):
        """
        def : selectValueByIndex
        purpose : to select dropdown/listbox values based on index
        param  : webelement,list
        return : bool
        """
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        index = None
        try:
            if webelement is not None:
                log.info('Recieved web element from the web dispatcher')
                if webelement.tag_name=='table':
                        webelement=self.radioKeywordsObj.getActualElement(webelement,input)
                        index = input[4]

                if ((webelement.is_enabled())):
                    if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                        # performing js code
                        log.debug('element is invisible, performing js code')
                        if (input is not None) :
                            if index == None:
                                index = input[0]
                            if len(index.strip()) != 0:
                                input_val = int(index)
                                #Issue fix ALM 131: ICE-Test Case: List and Dropdown -> "selectValueByIndex" is starting from index 1 instead of index 0
                                ##input_val = input_val - 1
                                log.info('Input value obtained')
                                log.info(input_val)
                                select = Select(webelement)
                                iList = select.options
                                #print iList
                                iListSize = len(iList)
                                ##input_val=input_val-1
                                if(input_val < iListSize):
                                    for i in range(0,iListSize):
                                        if(input_val == i):
                                            sValue =  browser_Keywords.driver_obj.execute_script("""return arguments[0].options[arguments[1]].text""", webelement,input_val)
                                            browser_Keywords.driver_obj.execute_script("""arguments[0].focus()""",webelement)
                                            from pyrobot import Robot
                                            robot = Robot()
                                            robot.type_string(str(sValue).strip())
                                            status=webconstants.TEST_RESULT_PASS
                                            result=webconstants.TEST_RESULT_TRUE
                                            log.info(STATUS_METHODOUTPUT_UPDATE)
                                else:
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                    log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']

                    else:
                        if (self.util.is_visible(webelement)):
                            # performing selenium code
                            log.debug('element is visible, performing selenium code')
                            if (input is not None):
                                if index == None:
                                    index = input[0]
                                if len(index.strip()) != 0:
                                    input_val = int(index)
                                    # Issue fix ALM 131: ICE-Test Case: List and Dropdown -> "selectValueByIndex" is starting from index 1 instead of index 0
                                    ##                            input_val = input_val - 1
                                    log.info('Input value obtained')
                                    log.info(input_val)
                                    select = Select(webelement)
                                    iList = select.options
                                    iListSize = len(iList)
                                    ##                            input_val=input_val-1
                                    if (input_val < iListSize):
                                        for i in range(0, iListSize):
                                            if (input_val == i):
                                                if (isinstance(browser_Keywords.driver_obj, webdriver.Firefox)):
                                                    iList[i].click()
                                                elif platform.system() == 'Darwin':
                                                    scroll = """arguments[0].scrollIntoView()"""
                                                    browser_Keywords.driver_obj.execute_script(scroll, webelement)
                                                    jstext = """for (var j = 0; j < arguments[1].length; j++) {for (var i = 0; i < arguments[0].length; i++) {if ( i == arguments[1][j]) {arguments[0][i].selected = true;}}}"""
                                                    browser_Keywords.driver_obj.execute_script(jstext, webelement, input)
                                                else:
                                                    select.select_by_index(input_val)
                                                status = webconstants.TEST_RESULT_PASS
                                                result = webconstants.TEST_RESULT_TRUE
                                                log.info(STATUS_METHODOUTPUT_UPDATE)
                                    else:
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                        log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                else:
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                    log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        else:
                            err_msg = 'Element is not displayed'
                            logger.print_on_console('Element is not displayed')
                            log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])

                else:
                    err_msg = ERROR_CODE_DICT['ERR_OBJECT_DISABLED']
                    log.info(err_msg)

        except Exception as e:
            import traceback
            print (traceback.format_exc(()))
            log.error(e)
            logger.print_on_console(e)
        log.info(RETURN_RESULT)

        return status,result,verb,err_msg



    def getCount(self,webelement,*args):
        """
        def : getCount
        purpose : to retrieve number of objects in dropdown/listbox
        param  : webelement
        return : string
        """
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output = None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            ##if ((webelement.is_enabled())):
            log.info('Recieved web element from the web dispatcher')
            if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                # performing js code
                log.debug('element is invisible, performing js code')
                try:
                    totalcount = browser_Keywords.driver_obj.execute_script("""return arguments[0].childElementCount""",webelement)
                    log.info('totalcount is')
                    log.info(totalcount)
                    if totalcount is not None:
                        output = str(totalcount)
                        status = webconstants.TEST_RESULT_PASS
                        result = webconstants.TEST_RESULT_TRUE
                        logger.print_on_console('Result obtained is: ',output)
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                except Exception as e:
                    log.error(e)
                    logger.print_on_console(e)
            else:
                if self.util.is_visible(webelement):
                    # performing selenium code
                    log.debug('element is visible, performing selenium code')
                    log.debug(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                    try:
                        select = Select(webelement)
                        iList = select.options
                        iListSize = len(iList)
                        log.info('Count of dropdown/listbox')
                        log.info(iListSize)
                        if (iListSize >= 0):
                            output = str(iListSize)
                            status=webconstants.TEST_RESULT_PASS
                            result=webconstants.TEST_RESULT_TRUE
                            logger.print_on_console('Result obtained is: ',output)
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                    except Exception as e:
                        log.error(e)
                        logger.print_on_console(e)
                    log.info(RETURN_RESULT)
                else:
                    logger.print_on_console('Element is not displayed')
                    log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
                    err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
            ##else:
                ##err_msg = 'Element is not enabled '
                ##logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                ##log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,output,err_msg

    """
    Helper function used in selectValueByText keyword
    """
    def getText(self,webelement,text):
        js = """for(var i=0; i<arguments[0].options.length; i++) {if (arguments[0].options[i].text.indexOf(arguments[1]) > -1) {return arguments[0].options[i].text;}}return 'nOtFoUnd';"""
        value = browser_Keywords.driver_obj.execute_script(js,webelement,text)
        if value == 'nOtFoUnd':
            return None
        return value

    def selectValueByText(self,webelement,input,*args):
        """
        def : selectValueByText
        purpose : to select dropdown/listbox values based on index
        param  : webelement,list
        return : bool
        """
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        if webelement is not None:
            if webelement.tag_name=='table':
                    if len(input)==5:
                        dropVal=input[2]
                        ##webelement=self.radioKeywordsObj.getActualElement(webelement,input)
                        """
                        author :arpitha
                        changes made for multiple dropdowns present in the table.
                        Date :12-05-2017
                        """
                        if dropVal.lower()=='dropdown':
                            ## webelement1=self.jsExecutorForMultipleDropdown(webelement,input)
                            ##New javascript was not providing the accurate element still keeping the if else condition for future checks if any
                            webelement=self.radioKeywordsObj.getActualElement(webelement,input)
                        else:
                            webelement=self.radioKeywordsObj.getActualElement(webelement,input)
            if ((webelement.is_enabled())):
                if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                    #performing js code
                    log.debug('element is invisible, performing js code')
                    try:
                        if (input is not None):
                            if len(input)==1:
                                inp_val = input[0]
                                log.info('Input value obtained')
                                log.info(inp_val)
                            elif len(input)==2:
                                inp_val = input[0]
                                log.info('Input value obtained')
                                log.info(inp_val)
                            elif len(input)==5:
                                inp_val = input[4]
                                log.info('Input value obtained')
                                log.info(inp_val)
                            coreutilsobj=core_utils.CoreUtils()
                            inp_val=coreutilsobj.get_UTF_8(inp_val)
                            if (inp_val is not None):
                                if len(inp_val.strip()) != 0:
                                    select = Select(webelement)
                                    iList = select.options
                                    flag = False
                                    data_list = []
                                    for i in range (0,len(iList)):
                                        values =iList[i].text.lower()
                                        if inp_val.lower() in values:
                                            data_list.append(iList[i].text)
                                    if len(data_list)>0:
                                        if len(input)==2:
                                            if int(input[1])< len(data_list) and int(input[1])>=0:
                                                index_val =int(input[1])
                                                inp_val = data_list[index_val]
                                                flag = True
                                            else:
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                        else:
                                            inp_val = data_list[0]
                                            flag = True
                                    else:
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                        log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                    if(flag):
                                        sValue = self.getText(webelement,inp_val)
                                        if sValue is not None:
                                            browser_Keywords.driver_obj.execute_script("""arguments[0].focus()""",webelement)
                                            from pyrobot import Robot
                                            robot = Robot()
                                            robot.type_string(str(sValue).strip())
                                            status = webconstants.TEST_RESULT_PASS
                                            result = webconstants.TEST_RESULT_TRUE
                                            log.info(STATUS_METHODOUTPUT_UPDATE)

                                    else:
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                        log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                        err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                else:
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                    log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                    err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    except Exception as e:
                        log.error(e)
                        from selenium.common.exceptions import NoSuchElementException
                        if type(e) == NoSuchElementException:
                           err_msg = str(e)

                        logger.print_on_console(e)
                else:
                    if (self.util.is_visible(webelement)):
                        # performing selenium code
                        log.debug('element is visible, performing selenium code')
                        try:
                            if (input is not None):
                                if len(input) == 1:
                                    inp_val = input[0]
                                    log.info('Input value obtained')
                                    log.info(inp_val)
                                elif len(input) == 2:
                                    inp_val = input[0]
                                    log.info('Input value obtained')
                                    log.info(inp_val)
                                elif len(input) == 5:
                                    inp_val = input[4]
                                    log.info('Input value obtained')
                                    log.info(inp_val)
                                coreutilsobj = core_utils.CoreUtils()
                                inp_val = coreutilsobj.get_UTF_8(inp_val)
                                if (inp_val is not None):
                                    if len(inp_val.strip()) != 0:
                                        select = Select(webelement)
                                        iList = select.options
                                        flag = False
                                        data_list = []
                                        for i in range(0, len(iList)):
                                            values = iList[i].text.lower()
                                            if inp_val.lower() in values:
                                                data_list.append(iList[i].text)
                                        if len(data_list) > 0:
                                            if len(input) == 2:
                                                if int(input[1]) < len(data_list) and int(input[1]) >= 0:
                                                    index_val = int(input[1])
                                                    inp_val = data_list[index_val]
                                                    flag = True
                                                else:
                                                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                                    log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                            else:
                                                inp_val = data_list[0]
                                                flag = True
                                        else:
                                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                        if (flag):
                                            import platform
                                            if platform.system() == 'Darwin':
                                                input_list = [inp_val]
                                                scroll = """arguments[0].scrollIntoView()"""
                                                browser_Keywords.driver_obj.execute_script(scroll, webelement)
                                                jstext = """for (var j = 0; j < arguments[1].length; j++) {for (var i = 0; i < arguments[0].length; i++) {if (arguments[0][i].innerHTML == arguments[1][j]) {arguments[0][i].selected = true;}}}"""
                                                browser_Keywords.driver_obj.execute_script(jstext, webelement, input_list)
                                            else:
                                                select.select_by_visible_text(inp_val)
                                            status = webconstants.TEST_RESULT_PASS
                                            result = webconstants.TEST_RESULT_TRUE
                                            log.info(STATUS_METHODOUTPUT_UPDATE)
                                        else:
                                            logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                            log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                            err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                    else:
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                        log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                        err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                else:
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                    log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        except Exception as e:
                            log.error(e)
                            from selenium.common.exceptions import NoSuchElementException
                            if type(e) == NoSuchElementException:
                                err_msg = str(e)
                            logger.print_on_console(e)
                    else:
                        logger.print_on_console('Element is not displayed')
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
                        err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
            else:
                err_msg = 'Element is not enabled '
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,verb,err_msg

    """
    author :arpitha
    changes made for multiple dropdowns present in the table.
    Date :12-05-2017
    """
    def jsExecutorForMultipleDropdown(self,webElement,input):
        remoteWebElement=None
        row_num=input[0]
        col_num=input[1]
        try:
            js="""var temp = fun(arguments[0], arguments[2], arguments[1]); return temp; function fun(table, x, y) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy,sVal;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;			             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }			             if (xx <= x && x < xx + cell.colSpan && yyy <= y && y < yyy + cell.rowSpan)              if(cell.children[0].type=='select-one'){                 sVal=cell.children[0]; 				return sVal; 		} 		else{               return cell; 		}         }     }     return null; };"""
            remoteWebElement=browser_Keywords.driver_obj.execute_script(js,webElement,row_num,col_num)
        except Exception as e:
            log.error(e)
        return remoteWebElement


    def verifySelectedValue(self,webelement,input,*args):
        """
        def : verifySelectedValue
        purpose : to verify default/current selected value in dropdown/listbox
        param  : webelement,list
        return : bool
        """
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None :
            if ((webelement.is_enabled())):
                log.info('Recieved web element from the web dispatcher')
                if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                    # performing js code
                    log.debug('element is invisible, performing js code')
                    try:
                        if ((input is not None) and (len(input) == 1) and input[0] != '') :
                            first_value = None
                            if browser_Keywords.driver_obj is not None and isinstance(browser_Keywords.driver_obj, webdriver.Ie):
                                count = browser_Keywords.driver_obj.execute_script("""return arguments[0].childElementCount""",webelement)
                                for i in range(count):
                                    if browser_Keywords.driver_obj.execute_script("""return arguments[0].options[arguments[1]].selected""",webelement,i):
                                        first_value = browser_Keywords.driver_obj.execute_script("""return arguments[0].options[arguments[1]].text""",webelement,i)
                                        break
                            else:
                                optionlist = browser_Keywords.driver_obj.execute_script("""return arguments[0].selectedOptions""",webelement)
                                first_value = browser_Keywords.driver_obj.execute_script("""return arguments[0].text""",optionlist[0])

                            inp_val = input[0]
                            coreutilsobj=core_utils.CoreUtils()
                            inp_val=coreutilsobj.get_UTF_8(inp_val)
                            if (first_value is not None and first_value == inp_val):
                                status=webconstants.TEST_RESULT_PASS
                                result=webconstants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INPUT_MISS_MATCH'])
                                log.info(ERROR_CODE_DICT['ERR_INPUT_MISS_MATCH'])
                                err_msg = ERROR_CODE_DICT['ERR_INPUT_MISS_MATCH']
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    except Exception as e:
                        log.error(e)

                        logger.print_on_console(e)
                else:
                    if (self.util.is_visible(webelement)):
                        # performing selenium code
                        log.debug('element is visible, performing selenium code')
                        try:
                            if ((input is not None) and (len(input) == 1) and input[0] != '') :
                                select = Select(webelement)
                                first_value = select.first_selected_option.text
                                inp_val = input[0]
                                coreutilsobj=core_utils.CoreUtils()
                                inp_val=coreutilsobj.get_UTF_8(inp_val)
                                if (first_value == inp_val):
                                    status=webconstants.TEST_RESULT_PASS
                                    result=webconstants.TEST_RESULT_TRUE
                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                                else:
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_INPUT_MISS_MATCH'])
                                    log.info(ERROR_CODE_DICT['ERR_INPUT_MISS_MATCH'])
                                    err_msg = ERROR_CODE_DICT['ERR_INPUT_MISS_MATCH']
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        except Exception as e:
                            log.error(e)
                            logger.print_on_console(e)
                    else:
                        logger.print_on_console('Element is not displayed')
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
                        err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
            else:
                err_msg = 'Element is not enabled '
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,verb,err_msg

    def verifySelectedValues(self,webelement,input,*args):
        """
        def : verifySelectedValue
        purpose : to verify default/current selected value in dropdown/listbox
        param  : webelement,list
        return : bool
        """
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            if ((webelement.is_enabled())):
                log.info('Recieved web element from the web dispatcher')
                if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                    try:
                        # performing js code
                        log.debug('element is invisible, performing js code')
                        if (input is not None and input[0] != ''):
                            selectedvalues = []
                            if browser_Keywords.driver_obj is not None and isinstance(browser_Keywords.driver_obj,webdriver.Ie):
                                count = browser_Keywords.driver_obj.execute_script("""return arguments[0].childElementCount""", webelement)
                                for i in range(count):
                                    if browser_Keywords.driver_obj.execute_script("""return arguments[0].options[arguments[1]].selected""", webelement, i):
                                        selectedvalues.append(browser_Keywords.driver_obj.execute_script("""return arguments[0].options[arguments[1]].text""",webelement,i))
                            else:
                                optionlist = browser_Keywords.driver_obj.execute_script("""return arguments[0].selectedOptions""", webelement)
                                for element in optionlist:
                                    selectedvalues.append(browser_Keywords.driver_obj.execute_script("""return arguments[0].text""",element))
                            selectedmatch = True
                            coreutilsobj = core_utils.CoreUtils()
                            for input_val in input:
                                input_val = coreutilsobj.get_UTF_8(input_val)
                                if input_val not in selectedvalues:
                                    selectedmatch = False
                                    break
                            if selectedmatch:
                                status = webconstants.TEST_RESULT_PASS
                                result = webconstants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                logger.print_on_console(err_msg)
                                log.error(err_msg)
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    except Exception as e:
                        log.error(e)

                        logger.print_on_console(e)
                else:
                    try:
                        # performing selenium code
                        log.debug('element is visible, performing selenium code')
                        if (input is not None and input[0] != ''):
                            select = Select(webelement)
                            all_value = select.all_selected_options
                            len_all_values = len(all_value)
                            inp_val_len = len(input)
                            temp = []
                            flag = True
                            for x in range(0, len_all_values):
                                internal_val = all_value[x].text
                                temp.append(internal_val)
                            log.info('temp value')
                            log.info(temp)
                            for y in range(0, inp_val_len):
                                input_val = input[y]
                                coreutilsobj = core_utils.CoreUtils()
                                input_val = coreutilsobj.get_UTF_8(input_val)
                                if (input_val in temp):
                                    temp.remove(input_val)
                                else:
                                    flag = False
                                    break

                            if (len(temp) == 0 and flag == True):
                                status = webconstants.TEST_RESULT_PASS
                                result = webconstants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                logger.print_on_console(err_msg)
                                log.error(err_msg)
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    except Exception as e:
                        log.error(e)

                        logger.print_on_console(e)
            else:
                err_msg = 'Element is not enabled '
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,verb,err_msg



    def verifyCount(self,webelement,input,*args):
        """
        def : verifyCount
        purpose : to verify number of objects in dropdown/listbox
        param  : webelement,list
        return : bool
        """
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            if ((webelement.is_enabled())):
                log.info('Recieved web element from the web dispatcher')
                if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                    try:
                        # performing js code
                        log.debug('element is invisible, performing js code')
                        if ((input is not None) and (len(input) == 1) and input[0] != ''):
                            log.info('Input is not none')
                            input_val = int(input[0])
                            totalcount = browser_Keywords.driver_obj.execute_script("""return arguments[0].childElementCount""", webelement)
                            log.info('totalcount is')
                            log.info(totalcount)
                            totalcount = int(totalcount)
                            if totalcount is not None and totalcount == input_val:
                                status = webconstants.TEST_RESULT_PASS
                                result = webconstants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                logger.print_on_console('Count mismatched')
                                log.info('Count mismatched')
                                err_msg = 'Count mismatched'
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    except Exception as e:
                        log.error(e)
                        logger.print_on_console(e)
                else:
                    if self.util.is_visible(webelement):
                        # performing selenium code
                        log.debug('element is visible, performing selenium code')
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                        try:
                            if ((input is not None) and (len(input) == 1) and input[0] != '') :
                                log.info('Input is not none')
                                select = Select(webelement)
                                iList = select.options
                                iListSize = len(iList)
                                logger.print_on_console(iListSize)
                                input_val = int(input[0])
                                if (iListSize == input_val):
                                    status=webconstants.TEST_RESULT_PASS
                                    result=webconstants.TEST_RESULT_TRUE
                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                                else:
                                    logger.print_on_console('Count mismatched')
                                    log.info('Count mismatched')
                                    err_msg = 'Count mismatched'
                                    logger.print_on_console(EXPECTED,input_val)
                                    log.info(EXPECTED)
                                    log.info(input)
                                    logger.print_on_console(ACTUAL,iListSize)
                                    log.info(ACTUAL)
                                    log.info(iListSize)
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        except Exception as e:
                            log.error(e)
                            logger.print_on_console(e)
                    else:
                        logger.print_on_console('Element is not displayed')
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
                        err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
            else:
                err_msg = 'Element is not enabled '
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,verb,err_msg

    def getAllValues(self,webelement,input,*args):
        """
        author : arpitha.b.v
        def :getAllValues
        purpose: to get All values present in the dropdown.
        param: webelement,list
        return : All dropdown values
        """
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output = None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            log.info('Recieved web element from the web dispatcher')
            ##if ((webelement.is_enabled())):
            if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                try:
                    # performing js code
                    log.debug('element is invisible, performing js code')
                    if input is not None:
                        alloptions = []
                        if browser_Keywords.driver_obj is not None and isinstance(browser_Keywords.driver_obj,
                                                                                  webdriver.Ie):
                            count = browser_Keywords.driver_obj.execute_script(
                                """return arguments[0].childElementCount""", webelement)
                            for i in range(count):
                                alloptions.append(browser_Keywords.driver_obj.execute_script(
                                    """return arguments[0].options[arguments[1]].text""", webelement, i))
                        else:
                            optionlist = browser_Keywords.driver_obj.execute_script(
                                """return arguments[0].options""", webelement)
                            for element in optionlist:
                                alloptions.append(
                                    browser_Keywords.driver_obj.execute_script("""return arguments[0].text""",
                                                                               element))
                        if len(input)!=0 and input[0] == "1":
                            for i in range(len(alloptions)):
                                alloptions[i] = alloptions[i].strip()
                        output = alloptions
                        if len(output) != 0:
                            status = webconstants.TEST_RESULT_PASS
                            result = webconstants.TEST_RESULT_TRUE
                            logger.print_on_console(output)
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                        else:
                            err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                            logger.print_on_console(err_msg)
                            log.error(err_msg)
                    else:
                        err_msg = 'Provided input not present in element'
                        logger.print_on_console(err_msg)
                        log.error(err_msg)
                except Exception as e:
                    log.error(e)
                    logger.print_on_console(e)
            else:
                try:
                    if input is not None:
                        log.info('Input is not none')
                        if self.util.is_visible(webelement):
                            # performing selenium code
                            log.debug('element is visible, performing selenium code')
                            log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                            select = Select(webelement)
                            option_len = select.options
                            opt_len = len(option_len)
                            inp_val_len = len(input)
                            log.info('inp_val_len')
                            log.info(inp_val_len)
                            temp = []
                            flag = True
                            for x in range(0,opt_len):
                                internal_val = select.options[x].text
                                if len(input)!=0 and input[0] == "1":
                                    internal_val= select.options[x].text.strip()
                                temp.append(internal_val)
                            log.info('temp value')
                            log.info(temp)
                            output=temp
                            if(len(temp) != 0 ):
                                status=webconstants.TEST_RESULT_PASS
                                result=webconstants.TEST_RESULT_TRUE
                                logger.print_on_console(output)
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                logger.print_on_console(err_msg)
                                log.error(err_msg)
                        else:
                            err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
                            logger.print_on_console(err_msg)
                            log.error(err_msg)

                    else:
                        err_msg='Provided input not present in element'
                        logger.print_on_console(err_msg)
                        log.error(err_msg)
                except Exception as e:
                    log.error(e)
                    logger.print_on_console(e)
            ##else:
                ##err_msg = 'Element is not enabled '
                ##logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                ##log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,output,err_msg

    def verifyAllValues(self,webelement,input,*args):
        """
        def : verifyAllValues
        purpose : to verify all objects in dropdown/listbox
        param  : webelement,list
        return : bool
        """

        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            if ((webelement.is_enabled())):
                log.info('Recieved web element from the web dispatcher')
                if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                    try:
                        # performing js code
                        log.debug('element is invisible, performing js code')
                        log.info("length of input is:")
                        log.info(len(input))
                        if input is not None and input[0] != '':
                            alloptions = []
                            if browser_Keywords.driver_obj is not None and isinstance(browser_Keywords.driver_obj,
                                                                                      webdriver.Ie):
                                count = browser_Keywords.driver_obj.execute_script(
                                    """return arguments[0].childElementCount""", webelement)
                                for i in range(count):
                                    alloptions.append(browser_Keywords.driver_obj.execute_script(
                                            """return arguments[0].options[arguments[1]].text""", webelement, i))
                            else:
                                optionlist = browser_Keywords.driver_obj.execute_script(
                                    """return arguments[0].options""", webelement)
                                for element in optionlist:
                                    alloptions.append(
                                        browser_Keywords.driver_obj.execute_script("""return arguments[0].text""",
                                                                                   element))
                            allmatch = True
                            coreutilsobj = core_utils.CoreUtils()
                            for input_val in input:
                                input_val = coreutilsobj.get_UTF_8(input_val)
                                if input_val not in alloptions:
                                    allmatch = False
                                    break
                            if allmatch:
                                status = webconstants.TEST_RESULT_PASS
                                result = webconstants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                logger.print_on_console(err_msg)
                                log.error(err_msg)
                        elif input[0]=='':
                           logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                           log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                           err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']

                        else:
                            err_msg='Provided input not present in element'
                            logger.print_on_console(err_msg)
                            log.error(err_msg)

                    except Exception as e:
                        log.error(e)
                        logger.print_on_console(e)
                else:
                    try:
                        if input is not None and input[0] != '':
                            log.info('Input is not none')
                            if self.util.is_visible(webelement):
                                # performing selenium code
                                log.debug('element is visible, performing selenium code')
                                log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                                select = Select(webelement)
                                option_len = select.options
                                opt_len = len(option_len)
                                inp_val_len = len(input)
                                log.info('inp_val_len')
                                log.info(inp_val_len)
                                temp = []
                                flag = True
                                for x in range(0,opt_len):
                                    internal_val = select.options[x].text
                                    temp.append(internal_val)
                                log.info('temp value')
                                log.info(temp)
                                for y in range(0,inp_val_len):
                                    input_val = input[y]
                                    coreutilsobj=core_utils.CoreUtils()
                                    input_val=coreutilsobj.get_UTF_8(input_val)
                                    if (input_val in temp):
                                        temp.remove(input_val)
                                    else:
                                        flag = False
                                        break

                                if(len(temp) ==  0 and flag == True):
                                    status=webconstants.TEST_RESULT_PASS
                                    result=webconstants.TEST_RESULT_TRUE
                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                                else:
                                    err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                    logger.print_on_console(err_msg)
                                    log.error(err_msg)

                            else:
                                err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
                                logger.print_on_console(err_msg)
                                log.error(err_msg)
                        elif input[0]=='':
                           logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                           log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                           err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']

                        else:
                            err_msg='Provided input not present in element'
                            logger.print_on_console(err_msg)
                            log.error(err_msg)

                    except Exception as e:
                        log.error(e)
                        logger.print_on_console(e)
            else:
                err_msg = 'Element is not enabled '
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,verb,err_msg

    def selectMultipleValuesByIndexes(self,webelement,input,*args):
        """
                def : selectMultipleValuesByIndexes
                purpose : to select multiple values in dropdown/listbox based on index
                param  : webelement,list
                return : bool
        """
        status = webconstants.TEST_RESULT_FAIL
        result = webconstants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            if ((webelement.is_enabled())):
                log.info('Recieved web element from the web dispatcher')
                if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                    try:
                        # performing js code
                        log.debug('element is invisible, performing js code')
                        if input is not None and len(input) != 0:
                                flag = False
                                log.info('userinput count is')
                                log.info(len(input))
                                totalcount = browser_Keywords.driver_obj.execute_script("""return arguments[0].childElementCount""",webelement)
                                log.info('totalcount is')
                                log.info(totalcount)
                                for inputindex in input:
                                    if inputindex is not None:
                                        inputindex = int(inputindex)
                                        if inputindex < totalcount:
                                            browser_Keywords.driver_obj.execute_script("""arguments[0].options[arguments[1]].selected=true""",webelement,inputindex)
                                        else:
                                            flag = True
                                            log.info("One of the provided index is invalid")
                                            break
                                    else:
                                        flag = True
                                        log.info("One of the provided index is invalid (None)")
                                        break
                                if (not flag):
                                    status = webconstants.TEST_RESULT_PASS
                                    result = webconstants.TEST_RESULT_TRUE
                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    except Exception as e:
                        log.error(e)
                        logger.print_on_console(e)
                else:
                    try:
                        if input is not None and len(input) != 0:
                                if (self.util.is_visible(webelement)):
                                    # performing selenium code
                                    log.debug('element is visible, performing selenium code')
                                    log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                                    log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                                    count = len(input)
                                    log.info('count is')
                                    log.info(count)
                                    select = Select(webelement)
                                    iList = select.options
                                    iListSize = len(iList)
                                    log.info('iListSize is')
                                    log.info(iListSize)
                                    flag = False
                                    if platform.system() == 'Darwin':
                                        input_list = [input]
                                        scroll = """arguments[0].scrollIntoView()"""
                                        browser_Keywords.driver_obj.execute_script(scroll, webelement)
                                        jstext = """for (var j = 0; j < arguments[1].length; j++) {for (var i = 0; i < arguments[0].length; i++) {if ( i == arguments[1][j]) {arguments[0][i].selected = true;}}}"""
                                        browser_Keywords.driver_obj.execute_script(jstext, webelement, input_list)
                                    else:
                                        for index in input:
                                            inputindex = int(index)
                                            if(inputindex != None and inputindex <= iListSize):
                                                if (isinstance(browser_Keywords.driver_obj, webdriver.Firefox)):
                                                    iList[inputindex].click()
                                                else:
                                                    select.select_by_index(inputindex)
                                            else:
                                                flag = True
                                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                                break
                                    if (not flag):
                                        status = webconstants.TEST_RESULT_PASS
                                        result = webconstants.TEST_RESULT_TRUE
                                        log.info(STATUS_METHODOUTPUT_UPDATE)
                                else:
                                    err_msg = 'Element is not displayed or enabled '
                                    logger.print_on_console('Element is not displayed or enabled ')
                                    log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                                    log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    except Exception as e:
                        log.error(e)
                        logger.print_on_console(e)
            else:
                err_msg = 'Element is not enabled '
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,verb,err_msg

    def getSelected(self,webelement,input,*args):
        """
        def : getSelected
        purpose : to retrieve all selected objects in dropdown/listbox
        param  : webelement,list
        return : bool
        """
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output = None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            ##if ((webelement.is_enabled())):
            log.info('Recieved web element from the web dispatcher')
            if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                try:
                    # performing js code
                    log.debug('element is invisible, performing js code')
                    if webelement.tag_name=='table':
                        if ((webelement.is_enabled())):
                            webelement=self.radioKeywordsObj.getActualElement(webelement,input)
                        else:
                            err_msg = 'Element is not enabled '
                            logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                            log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                    selectedvalues = []
                    if browser_Keywords.driver_obj is not None and isinstance(browser_Keywords.driver_obj,webdriver.Ie):
                        count = browser_Keywords.driver_obj.execute_script("""return arguments[0].childElementCount""", webelement)
                        for i in range(count):
                            if browser_Keywords.driver_obj.execute_script(
                                    """return arguments[0].options[arguments[1]].selected""", webelement, i):
                                value=browser_Keywords.driver_obj.execute_script(
                                    """return arguments[0].options[arguments[1]].text""", webelement, i)
                                if input[0] == "1":
                                    value = value.strip()
                                selectedvalues.append(value)
                    else:
                        optionlist = browser_Keywords.driver_obj.execute_script(
                            """return arguments[0].selectedOptions""", webelement)
                        for element in optionlist:
                            value = browser_Keywords.driver_obj.execute_script("""return arguments[0].text""",element)
                            if input[0] == "1":
                                value = value.strip()
                            selectedvalues.append(value)
                    output = selectedvalues
                    logger.print_on_console('Result obtained is: ',output)
                    status = webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                except Exception as e:
                    log.error(e)
                    logger.print_on_console(e)
            else:
                try:
                    if webelement.tag_name == 'table':
                        if ((webelement.is_enabled())):
                            webelement = self.radioKeywordsObj.getActualElement(webelement, input)
                        else:
                            err_msg = 'Element is not enabled '
                            logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                            log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                    if self.util.is_visible(webelement):
                        # performing selenium code
                        log.debug('element is visible, performing selenium code')
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                        select = Select(webelement)
                        index = select.all_selected_options
                        log.info('Index value')
                        log.info(index)
                        temp = []
                        for x in range(0, len(index)):
                            value = select.all_selected_options[x].text
                            if len(input)==1:
                                if input[0] == "1":
                                    value = value.strip()
                            temp.append(value)
                        output = ';'.join(temp)
                        if len(temp) > 1:
                            output = temp
                        else:
                            output = value
                        logger.print_on_console('Result obtained is: ',output)
                        status = webconstants.TEST_RESULT_PASS
                        result = webconstants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        logger.print_on_console('Element is not displayed')
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
                        err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
                except Exception as e:
                    log.error(e)
                    logger.print_on_console(e)
            ##else:
                ##err_msg = 'Element is not enabled '
                ##logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                ##log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status, result, output ,err_msg


    def selectMultipleValuesByText(self,webelement,input,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            if ((webelement.is_enabled())):
                log.info('Recieved web element from the web dispatcher')
                if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                    try:
                        # performing js code
                        log.debug('element is invisible, performing js code')
                        count = len(input)
                        log.info('length of input is')
                        log.info(count)
                        if len(input) != 0:
                            alloptions = browser_Keywords.driver_obj.execute_script("""return arguments[0].options""",webelement)
                            optionstext = []
                            for option in alloptions:
                                optionstext.append(browser_Keywords.driver_obj.execute_script("""return arguments[0].text""",option))
                            counter = 0
                            coreutilsobj = core_utils.CoreUtils()
                            for userinput in input:
                                userinput = coreutilsobj.get_UTF_8(userinput)
                                if userinput is not None and len(userinput)>0 and userinput in optionstext:
                                    index = optionstext.index(userinput)
                                    if index is not None:
                                        browser_Keywords.driver_obj.execute_script("""arguments[0].options[arguments[1]].selected=true""",webelement,index)
                                        counter = counter + 1
                            if counter == count :
                                status=webconstants.TEST_RESULT_PASS
                                result=webconstants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']

                    except Exception as e:
                        log.error(e)
                        logger.print_on_console(e)
                else:
                    if (self.util.is_visible(webelement)):
                        # performing selenium code
                        log.debug('element is visible, performing selenium code')
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                        try:
                            count = len(input)
                            log.info('length of input is')
                            log.info(count)
                            if len(input) != 0:
                                select = Select(webelement)
                                iList = select.options
                                iListSize = len(iList)
                                if platform.system() == 'Darwin':
                                    jscount = 0
                                    scroll = """arguments[0].scrollIntoView()"""
                                    browser_Keywords.driver_obj.execute_script(scroll, webelement)
                                    jstext = """for (var j = 0; j < arguments[1].length; j++) {for (var i = 0; i < arguments[0].length; i++) {if (arguments[0][i].innerHTML == arguments[1][j]) {arguments[0][i].selected = true;}}}"""
                                    browser_Keywords.driver_obj.execute_script(jstext, webelement, input)
                                    items = select.options
                                    for i in items:
                                        if i.is_selected():
                                            jscount = jscount + 1
                                    if jscount == count:
                                        status = webconstants.TEST_RESULT_PASS
                                        result = webconstants.TEST_RESULT_TRUE
                                        log.info(STATUS_METHODOUTPUT_UPDATE)
                                    else:
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                        log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                        err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                                else:
                                    counter = 0
                                    options = []
                                    coreutilsobj = core_utils.CoreUtils()
                                    for i in range(len(iList)):
                                        options.append(iList[i].text)
                                    for x in input:
                                        userinput = coreutilsobj.get_UTF_8(x)
                                        if (userinput is not None and len(userinput)>0 and userinput in options):
                                            select.select_by_visible_text(userinput)
                                            counter = counter + 1

                                    if counter == count:
                                        status = webconstants.TEST_RESULT_PASS
                                        result = webconstants.TEST_RESULT_TRUE
                                        log.info(STATUS_METHODOUTPUT_UPDATE)
                                    else:
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                        log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                        err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']

                        except Exception as e:
                            log.error(e)
                            logger.print_on_console(e)
                    else:
                        err_msg = 'Element is not displayed'
                        logger.print_on_console('Element is not displayed')
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
            else:
                err_msg = 'Element is not enabled '
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,verb,err_msg

    def getMultipleValuesByIndexes(self,webelement,input,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output = None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            ##if ((webelement.is_enabled())):
            log.info('Recieved web element from the web dispatcher')
            if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                try:
                    # performing js code
                    log.debug('element is invisible, performing js code')
                    if input is not None and len(input) != 0:
                        flag = False
                        resultoptions = []
                        log.info('userinput count is')
                        log.info(len(input))
                        totalcount = browser_Keywords.driver_obj.execute_script("""return arguments[0].childElementCount""", webelement)
                        log.info('totalcount is')
                        log.info(totalcount)
                        for inputindex in input:
                            if inputindex is not None:
                                inputindex = int(inputindex)
                                if inputindex < totalcount:
                                    resultoptions.append(str(browser_Keywords.driver_obj.execute_script("""return arguments[0].options[arguments[1]].text""", webelement,inputindex)))
                                else:
                                    flag = True
                                    log.info("One of the provided index is invalid")
                                    break
                            else:
                                flag = True
                                log.info("One of the provided index is invalid (None)")
                                break
                        if (not flag):
                            output = resultoptions
                            logger.print_on_console(output)
                            status = webconstants.TEST_RESULT_PASS
                            result = webconstants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                except Exception as e:
                    log.error(e)
                    logger.print_on_console(e)
            else:
                try:
                    if input is not None and len(input) != 0:
                        if self.util.is_visible(webelement):
                            # performing selenium code
                            log.debug('element is visible, performing selenium code')
                            log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                            count = len(input)
                            log.info('count is')
                            log.info(count)
                            select = Select(webelement)
                            iList = select.options
                            iListSize = len(iList)
                            temp = []
                            flag = False
                            for x in range(0,count):
                                if int(input[x]) <= iListSize:
                                    input_val_temp = input[x]
                                    input_val = int(input_val_temp)
                                    out=select.options[input_val].text
                                    value = str(out)
                                    temp.append(value)
                                else:
                                    flag = True
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                    log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                    break
                            if(not flag):
                                output = ';'.join(temp)
                                logger.print_on_console(output)
                                output=temp
                                status=webconstants.TEST_RESULT_PASS
                                result=webconstants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                        else:
                            logger.print_on_console('Element is not displayed')
                            log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
                            err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
                    else:
                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                except Exception as e:
                    log.error(e)
                    logger.print_on_console(e)
            ##else:
                ##err_msg = 'Element is not enabled '
                ##logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                ##log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,output,err_msg

    def selectAllValues(self,webelement,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            if ((webelement.is_enabled())):
                log.info('Recieved web element from the web dispatcher')
                if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                    try:
                        # performing js code
                        log.debug('element is invisible, performing js code')
                        alloptionscount = browser_Keywords.driver_obj.execute_script("""return arguments[0].childElementCount""",webelement)
                        for i in range(alloptionscount):
                            browser_Keywords.driver_obj.execute_script("""arguments[0].options[arguments[1]].selected=true""",webelement,i)
                        status = webconstants.TEST_RESULT_PASS
                        result = webconstants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    except Exception as e:
                        log.error(e)
                        logger.print_on_console(e)
                else:
                    if (self.util.is_visible(webelement)):
                        # performing selenium code
                        log.debug('element is visible, performing selenium code')
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                        try:
                            select = Select(webelement)
                            iList = select.options
                            iListSize = len(iList)
                            if platform.system()=='Darwin':
                                size=0
                                scroll = """arguments[0].scrollIntoView()"""
                                browser_Keywords.driver_obj.execute_script(scroll, webelement)
                                jsall = """for (var i = 0; i < arguments[0].length; i++) {arguments[0][i].selected = true;}"""
                                browser_Keywords.driver_obj.execute_script(jsall, webelement)
                                items = select.options
                                for i in items:
                                    if i.is_selected():
                                        size = size + 1
                                if (size == iListSize):
                                    status = webconstants.TEST_RESULT_PASS
                                    result = webconstants.TEST_RESULT_TRUE
                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                for i in range(0,iListSize):
                                    check = select.options[i].is_selected()
                                    if(check == False):
                                        to_select = select.options[i].text
                                        select.select_by_visible_text(to_select)
                                wlist = select.all_selected_options
                                size = len(wlist)
                                log.debug('size is')
                                log.debug(size)
                                log.debug('iListSize is')
                                log.debug(iListSize)
                                if(size == iListSize):
                                    status=webconstants.TEST_RESULT_PASS
                                    result=webconstants.TEST_RESULT_TRUE
                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                        except Exception as e:
                            log.error(e)
                            logger.print_on_console(e)
                    else:
                        logger.print_on_console('Element is not displayed')
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
                        err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
            else:
                err_msg = 'Element is not enabled '
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,verb,err_msg

    def getValueByIndex(self,webelement,input,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        output = None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            ##if ((webelement.is_enabled())):
            log.info('Recieved web element from the web dispatcher')
            if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                try:
                    # performing js code
                    log.debug('element is invisible, performing js code')
                    if input is not None and len(input[0].strip()) != 0:
                        alloptionscount = browser_Keywords.driver_obj.execute_script("""return arguments[0].childElementCount""", webelement)
                        input_val = int(input[0])
                        if input_val < alloptionscount:
                            output = browser_Keywords.driver_obj.execute_script("""return arguments[0].options[arguments[1]].text""",webelement,input_val)
                            if output is not None:
                                status = webconstants.TEST_RESULT_PASS
                                result = webconstants.TEST_RESULT_TRUE
                                logger.print_on_console('Result obtained is: ',output)
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    else:
                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                except Exception as e:
                    log.error(e)
                    logger.print_on_console(e)
            else:
                if self.util.is_visible(webelement):
                    # performing selenium code
                    log.debug('element is visible, performing selenium code')
                    log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                    try:
                        if input is not None:
                            if len(input[0].strip()) != 0:
                                input_val = int(input[0])
                                select = Select(webelement)
                                iList = select.options
                                iListSize = len(iList)
                                if(input_val < iListSize):
                                    for i in range(0,iListSize):
                                        if(input_val == i):
                                            output=select.options[input_val].text
                                            if input[0] == "1":
                                                output=select.options[input_val].text.strip()
                                            status=webconstants.TEST_RESULT_PASS
                                            result=webconstants.TEST_RESULT_TRUE
                                            logger.print_on_console('Result obtained is: ',output)
                                            log.info(STATUS_METHODOUTPUT_UPDATE)
                                else:
                                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                    log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    except Exception as e:
                        log.error(e)
                        logger.print_on_console(e)
                else:
                    logger.print_on_console('Element is not displayed')
                    log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
                    err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
            ##else:
                ##err_msg = 'Element is not enabled '
                ##logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                ##log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,output,err_msg

    def verifyValuesExists(self,webelement,input,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            if ((webelement.is_enabled())):
                log.info('Recieved web element from the web dispatcher')
                if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                    try:
                        # performing js code
                        log.debug('element is invisible, performing js code')
                        if input is not None and len(input) !=0:
                            log.debug('Input is not none')
                            count = len(input)
                            log.info('length of input is')
                            log.info(count)
                            alloptions = browser_Keywords.driver_obj.execute_script("""return arguments[0].options""",webelement)
                            optionstext = []
                            for option in alloptions:
                                optionstext.append(
                                    browser_Keywords.driver_obj.execute_script("""return arguments[0].text""", option).strip())
                            counter = 0
                            coreutilsobj = core_utils.CoreUtils()
                            for userinput in input:
                                userinput = coreutilsobj.get_UTF_8(userinput).strip()
                                if userinput is not None and userinput in optionstext:
                                    counter = counter + 1
                                else:
                                    break
                            if counter == count:
                                status = webconstants.TEST_RESULT_PASS
                                result = webconstants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                                err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    except Exception as e:
                        log.error(e)
                        logger.print_on_console(e)
                else:
                    try:
                        if input is not None:
                            log.debug('Input is not none')
                            if self.util.is_visible(webelement):
                                # performing selenium code
                                log.debug('element is visible, performing selenium code')
                                log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                                select = Select(webelement)
                                option_len = select.options
                                opt_len = len(option_len)
                                inp_val_len = len(input)
                                log.info('length of input value')
                                log.info(inp_val_len)
                                temp = []
                                flag = True
                                for x in range(0,opt_len):
                                    internal_val = select.options[x].text.strip()
                                    temp.append(internal_val)
                                log.debug('temp value obtained')
                                log.debug(temp)
                                count = 0
                                for y in range(0,inp_val_len):
                                    input_temp = input[y].strip()
                                    if (input_temp in temp):
                                        count+=1
                                    else:
                                        flag = False
                                if(not(flag == False)):
                                    status=webconstants.TEST_RESULT_PASS
                                    result=webconstants.TEST_RESULT_TRUE
                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                                else:
                                    logger.print_on_console('Inputs does not match')
                            else:
                                logger.print_on_console('Element is not displayed')
                                log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
                                err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    except Exception as e:
                        log.error(e)
                        logger.print_on_console(e)
            else:
                err_msg = 'Element is not enabled '
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,verb,err_msg

    def deselectAll(self,webelement,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            if ((webelement.is_enabled())):
                log.info('Recieved web element from the web dispatcher')
                log.debug(webelement)
                if not (self.util.is_visible(webelement)) and readconfig.readConfig().readJson()['ignoreVisibilityCheck'].strip().lower() == "yes":
                    try:
                        # performing js code
                        log.debug('element is invisible, performing js code')
                        alloptionscount = browser_Keywords.driver_obj.execute_script("""return arguments[0].childElementCount""", webelement)
                        for i in range(alloptionscount):
                            browser_Keywords.driver_obj.execute_script("""arguments[0].options[arguments[1]].selected=false""", webelement, i)
                        status = webconstants.TEST_RESULT_PASS
                        result = webconstants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    except Exception as e:
                        log.error(e)
                        logger.print_on_console(e)
                else:
                    if (self.util.is_visible(webelement)):
                        # performing selenium code
                        log.debug('element is visible, performing selenium code')
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                        log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                        try:
                            select = Select(webelement)
                            if platform.system() == 'Darwin':
                                scroll = """arguments[0].scrollIntoView()"""
                                browser_Keywords.driver_obj.execute_script(scroll, webelement)
                                jsdeselect = """for (var i = 0; i < arguments[0].length; i++) {arguments[0][i].selected = false;}"""
                                browser_Keywords.driver_obj.execute_script(jsdeselect, webelement)
                            else:
                                select.deselect_all()
                            check = select.all_selected_options
                            log.debug('value given by select.all_selected_options')
                            log.debug(check)
                            if(len(check) == 0):
                                status=webconstants.TEST_RESULT_PASS
                                result=webconstants.TEST_RESULT_TRUE
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                        except Exception as e:
                            log.error(e)
                            logger.print_on_console(e)
                    else:
                        err_msg = 'Element is not displayed'
                        logger.print_on_console('Element is not displayed')
                        log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
            else:
                err_msg = 'Element is not enabled '
                logger.print_on_console(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
        return status,result,verb,err_msg

    def selectByAbsoluteValue(self,webelement,input,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        verb = OUTPUT_CONSTANT
        err_msg=None
        if webelement is not None:
            if (input is not None) :
                if len(input)==5:
                    if webelement.tag_name=='table':
                        dropVal=input[2]
                        row_num=int(input[0])-1
                        col_num=int(input[1])-1
                        inp_val = input[4]
                        try:
                            if dropVal.lower()=='dropdown':
                                driver=browser_Keywords.driver_obj
                                log.debug('got the driver instance from browser keyword')
                                visibleFlag=True
                                if visibleFlag==True:
                                    from table_keywords import TableOperationKeywords
                                    tableops = TableOperationKeywords()
                                    cell=tableops.javascriptExecutor(webelement,row_num,col_num)
                                    element_list=cell.find_elements_by_xpath('.//*')
                                    if len(list(element_list))>0:
                                        xpath=tableops.getElemntXpath(element_list[0])
                                        cell=browser_Keywords.driver_obj.find_element_by_xpath(xpath)
                                        log.debug('checking for element not none')
                                        if(cell!=None):
                                            log.debug('checking for element enabled')
                                            if cell.is_enabled():
                                                if len(inp_val.strip()) != 0:
                                                    select = Select(cell)
                                                    iList = select.options
                                                else:
                                                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                                    log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                    else:
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                        log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        except Exception as e:
                            log.error(e)

                            logger.print_on_console(e)
                            err_msg=e
                elif (len(input) == 1):
                    if input[0] != '':
                        try:
                            inp_val = input[0]
                            log.info('Input value obtained')
                            log.info(inp_val)
                            coreutilsobj=core_utils.CoreUtils()
                            inp_val=coreutilsobj.get_UTF_8(inp_val)
                            if len(inp_val.strip()) != 0:
                                select = Select(webelement)
                                iList = select.options
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        except Exception as e:
                            log.error(e)
                            logger.print_on_console(e)
                            err_msg=e
                    else:
                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                else:
                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                    log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                try:
                    if inp_val !='':
                        temp=[]
                        for i in range (0,len(iList)):
                            internal_val = iList[i].text
                            temp.append(internal_val)
                        if (inp_val in temp):
                            select.select_by_visible_text(inp_val)
                            status=webconstants.TEST_RESULT_PASS
                            result=webconstants.TEST_RESULT_TRUE
                            log.info('Values Match')
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                            log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                            err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']
                    else:
                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']

                except Exception as e:
                    log.error(e)
                    logger.print_on_console(e)
                    err_msg=e
        return status,result,verb,err_msg


