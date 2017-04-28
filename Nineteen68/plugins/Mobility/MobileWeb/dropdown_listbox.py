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
import  browser_Keywords
import webconstants
from utilweb_operations import UtilWebKeywords
import logger
import radio_checkbox_operations
import logging

from constants import *
log = logging.getLogger('dropdown_listbox.py')
class DropdownKeywords():

    def __init__(self):
        self.radioKeywordsObj=radio_checkbox_operations.RadioCheckboxKeywords()

    def selectValueByIndex(self,webelement,input,*args):
        """
        def : selectValueByIndex
        purpose : to select dropdown/listbox values based on index
        param  : webelement,list
        return : bool
        """
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
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

                if ((webelement.is_enabled()) and webelement.is_displayed()):
                    log.debug(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                    log.debug(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                    if (input is not None) :
                        if index == None:
                            index = input[0]
                        if len(index.strip()) != 0:
                            input_val = int(index)
                            #Issue fix ALM 131: ICE-Test Case: List and Dropdown -> "selectValueByIndex" is starting from index 1 instead of index 0
##                            input_val = input_val - 1
                            log.info('Input value obtained')
                            log.info(input_val)
                            select = Select(webelement)
                            iList = select.options
                            iListSize = len(iList)
##                            input_val=input_val-1
                            if(input_val < iListSize):
                                for i in range(0,iListSize):
                                    if(input_val == i):
##                                        if (isinstance(browser_Keywords.driver_obj,webdriver.Firefox)):
##                                            iList[i].click()
##                                        else:
                                        select.select_by_index(input_val)
                                        status=webconstants.TEST_RESULT_PASS
                                        result=webconstants.TEST_RESULT_TRUE
                                        log.info(STATUS_METHODOUTPUT_UPDATE)
##                                    else:
##                                      logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
##                                      log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
##                                      err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                            else:
                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    else:
                        log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                else:
                    log.info('Element is not enabled or dispalyed')
                    err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
        except Exception as e:
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
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        visibilityFlag=True
        iListSize = None
        err_msg=None
        if webelement is not None:
            log.info('Recieved web element from the web dispatcher')
            if webelement.is_displayed():
                log.debug(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                try:
                    select = Select(webelement)
                    iList = select.options
                    iListSize = len(iList)
                    log.info('Count of dropdown/listbox')
                    log.info(iListSize)
                    logger.print_on_console('Count obtained is',iListSize)
                    if (iListSize > 0):
                        status=webconstants.TEST_RESULT_PASS
                        result=webconstants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                except Exception as e:
                    log.error(e)

                    logger.print_on_console(e)
                log.info(RETURN_RESULT)
            else:
                log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
                err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
        return status,result,str(iListSize),err_msg

    def selectValueByText(self,webelement,input,*args):
        """
        def : selectValueByText
        purpose : to select dropdown/listbox values based on index
        param  : webelement,list
        return : bool
        """
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        verb = OUTPUT_CONSTANT
        err_msg=None
        if webelement is not None:
            if webelement.tag_name=='table':
                    if len(input)==5:
                        webelement=self.radioKeywordsObj.getActualElement(webelement,input)
            if ((webelement.is_enabled()) and webelement.is_displayed()):
                try:
                    if (input is not None) :
##                        if not(visibilityFlag and isvisble):
                        if len(input)==1:
                            inp_val = input[0]
                            log.info('Input value obtained')
                            log.info(inp_val)
                        elif len(input)==5:
                            inp_val = input[4]
                            log.info('Input value obtained')
                            log.info(inp_val)
                        if len(inp_val.strip()) != 0:
                            select = Select(webelement)
                            iList = select.options
                            flag = False
                            for i in range (0,len(iList)):
                                if iList[i].text == inp_val:
                                    flag = True
                            if(flag):
                                select.select_by_visible_text(inp_val)
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
                err_msg = 'Element is not displayed or enabled '
                logger.print_on_console('Element is not displayed or enabled ')
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
        return status,result,verb,err_msg

## defect 360
    def verifySelectedValue(self,webelement,input,*args):
        """
        def : verifySelectedValue
        purpose : to verify default/current selected value in dropdown/listbox
        param  : webelement,list
        return : bool
        """
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            log.info('Recieved web element from the web dispatcher')
            if webelement.is_displayed():
                log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                try:
                    if ((input is not None) and (len(input) == 1)) :
##                        if not(visibilityFlag and isvisble):
                        select = Select(webelement)
                        first_value = select.first_selected_option.text
                        inp_val = input[0]
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
        visibilityFlag=True
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            log.info('Recieved web element from the web dispatcher')
            if webelement.is_displayed():
                log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                try:
                    if ((input is not None) and (len(input) == 1)) :
                        log.info('Input is not none')
##                        if not(visibilityFlag and isvisble):
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
        return status,result,verb,err_msg

    def verifyAllValues(self,webelement,input,*args):
        """
        def : verifyAllValues
        purpose : to verify all objects in dropdown/listbox
        param  : webelement,list
        return : bool
        """

        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if input is not None:
                log.info('Input is not none')
                if webelement is not None:
                    log.info('Recieved web element from the web dispatcher')
                    if webelement.is_displayed():
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

            else:
                err_msg='Provided input not present in element'
                logger.print_on_console(err_msg)
                log.error(err_msg)

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        return status,result,verb,err_msg

    def selectMultipleValuesByIndexes(self,webelement,input,*args):
        """
        def : selectMultipleValuesByIndexes
        purpose : to select multiple values in dropdown/listbox based on index
        param  : webelement,list
        return : bool
        """
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if input is not None:
                if len(input) == 1:
                    if len(input[0].strip()) != 0:
                        log.info('Input is not none')
                        if webelement is not None:
                            log.info('Recieved web element from the web dispatcher')
                            if ((webelement.is_enabled()) and webelement.is_displayed()):
                                log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                                log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                                count= len(input)
                                log.info('count is')
                                log.info(count)
                                select = Select(webelement)
                                iList = select.options
                                iListSize = len(iList)
                                log.info('iListSize is')
                                log.info(iListSize)
                                flag = False
                                for x in range(0,count):
                                    if int(input[x]) <= iListSize:
                                        for i in range(0,iListSize):
                                            input_val_temp = input[x]
                                            input_val = int(input_val_temp)
                                            if( input_val == i):
                                                if (isinstance(browser_Keywords.driver_obj,webdriver.Firefox)):
                                                    iList[i].click()
                                                else:
                                                    select.select_by_index(input_val)
                                    else:
                                        flag = True
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                        log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                        break;
                                if (not flag):
                                    status=webconstants.TEST_RESULT_PASS
                                    result=webconstants.TEST_RESULT_TRUE
                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                else:
                    log.info('Input is not none')
                    if webelement is not None:
                            log.info('Recieved web element from the web dispatcher')
                            if ((webelement.is_enabled()) and webelement.is_displayed()):
                                log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                                log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                                count= len(input)
                                log.info('count is')
                                log.info(count)
                                select = Select(webelement)
                                iList = select.options
                                iListSize = len(iList)
                                log.info('iListSize is')
                                log.info(iListSize)

                                flag = False
                                for x in range(0,count):
                                    if int(input[x]) <= iListSize:
                                        for i in range(0,iListSize):
                                            input_val_temp = input[x]
                                            input_val = int(input_val_temp)
                                            if( input_val == i):
##                                                if (isinstance(browser_Keywords.driver_obj,webdriver.Firefox)):
##                                                    iList[i].click()
##                                                else:
                                                    select.select_by_index(input_val)
                                            else:

                                                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                                log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']

                                    else:
                                        flag = True
                                        logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                        log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                                        break;
                                if (not flag):
                                    status=webconstants.TEST_RESULT_PASS
                                    result=webconstants.TEST_RESULT_TRUE
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
        visibilityFlag=True
        output = None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if webelement is not None:
                log.info('Recieved web element from the web dispatcher')
                if webelement.tag_name=='table':
                    webelement=self.radioKeywordsObj.getActualElement(webelement,input)
                if webelement.is_displayed():
                    log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                    select = Select(webelement)
                    index = select.all_selected_options
                    log.info('Index value')
                    log.info(index)
                    if (len(index) == '1'):
                        output = select.all_selected_options[i].text
                        str(output)
                        logger.print_on_console(output)
                        status=webconstants.TEST_RESULT_PASS
                        result=webconstants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                    else:
                        temp = []
                        for x in range(0,len(index)):
                            out = select.all_selected_options[x].text
                            value = str(out)
                            temp.append(value)
                        output = ';'.join(temp)
                        logger.print_on_console(output)

                        if len(temp)>1:
                            output=temp
                        else:
                            output = value
                        status=webconstants.TEST_RESULT_PASS
                        result=webconstants.TEST_RESULT_TRUE
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                else:
                    logger.print_on_console('Element is not displayed')
                    log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
                    err_msg = ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED']
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        return status, result, output ,err_msg


    def selectMultipleValuesByText(self,webelement,input,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            log.info('Recieved web element from the web dispatcher')
            if ((webelement.is_enabled()) and webelement.is_displayed()):
                log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                try:
                    count = len(input)
                    log.info('count value is')
                    log.info(count)
                    if len(input) == 1:
                        if len(input[0].strip()) != 0:
                            select = Select(webelement)
                            iList = select.options
                            iListSize = len(iList)

                            counter = 0
                            for x in range(0,count):
                                flag = False
                                for i in range(0,len(iList)):
                                     if iList[i].text == input[x] :
                                        flag = True
                                if(flag):
                                    input_val = input[x]
                                    log.info('Input value obtained')
                                    log.info(input_val)
                                    select.select_by_visible_text(input_val)
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
                    else:
                        select = Select(webelement)
                        iList = select.options
                        iListSize = len(iList)
                        counter = 0
                        for x in range(0,count):
                            flag = False
                            for i in range(0,len(iList)):
                                 if iList[i].text == input[x] :
                                    flag = True
                            if(flag):
                                input_val = input[x]
                                log.info('Input value obtained')
                                log.info(input_val)
                                select.select_by_visible_text(input_val)
                                counter = counter + 1

                        if counter == count :
                            status=webconstants.TEST_RESULT_PASS
                            result=webconstants.TEST_RESULT_TRUE
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                        else:
                            logger.print_on_console(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                            log.info(ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH'])
                            err_msg = ERROR_CODE_DICT['ERR_VALUES_DOESNOT_MATCH']

                except Exception as e:
                    log.error(e)

                    logger.print_on_console(e)
            else:
                err_msg = 'Element is not displayed or enabled '
                logger.print_on_console('Element is not displayed or enabled ')
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
        return status,result,verb,err_msg

    def getMultipleValuesByIndexes(self,webelement,input,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        output = None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if input is not None:
                 if len(input) == 1:
                        if len(input[0].strip()) != 0:
                            log.info('Input is not none')
                            if webelement is not None:
                                log.info('Recieved web element from the web dispatcher')
                                log.debug(webelement)
                                if webelement.is_displayed():
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
                                            break;
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
                 else:
                    log.info('Input is not none')
                    if webelement is not None:
                        log.info('Recieved web element from the web dispatcher')
                        log.debug(webelement)
                        if webelement.is_displayed():
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
                                    break;
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
        return status,result,output,err_msg

    def selectAllValues(self,webelement,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            log.info('Recieved web element from the web dispatcher')
            log.debug(webelement)
            if ((webelement.is_enabled()) and webelement.is_displayed()):
                log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                try:
                    select = Select(webelement)
                    iList = select.options
                    iListSize = len(iList)
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
                err_msg = 'Element is not displayed or enabled '
                logger.print_on_console('Element is not displayed or enabled ')
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
        return status,result,verb,err_msg

    def getValueByIndex(self,webelement,input,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        output = None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            log.info('Recieved web element from the web dispatcher')
            log.debug(webelement)
            if webelement.is_displayed():
                log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                try:
                    if input is not None:
##                        if not(visibilityFlag and isvisble):
                        if len(input[0].strip()) != 0:
                            input_val = int(input[0])
                            select = Select(webelement)
                            iList = select.options
                            iListSize = len(iList)
                            if(input_val < iListSize):
                                for i in range(0,iListSize):
                                    if(input_val == i):
                                        output=select.options[input_val].text
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
        return status,result,output,err_msg

    def verifyValuesExists(self,webelement,input,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if input is not None:
                log.debug('Input is not none')
                if webelement is not None:
                    log.info('Recieved web element from the web dispatcher')
                    log.debug(webelement)
                    if webelement.is_displayed():
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
                            internal_val = select.options[x].text
                            str(internal_val)
                            temp.append(internal_val)
                        log.debug('temp value obtained')
                        log.debug(temp)
                        count = 0
                        for y in range(0,inp_val_len):
                            input_temp = input[y]
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
        visibilityFlag=True
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            log.info('Recieved web element from the web dispatcher')
            if webelement.is_displayed():
                log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                try:
                    if (input is not None) :
##                        if not(visibilityFlag and isvisble):
                        select = Select(webelement)
                        all_value = select.all_selected_options
                        len_all_values = len(all_value)
                        inp_val_len = len(input)
                        temp = []
                        flag = True
                        for x in range(0,len_all_values):
                            internal_val = all_value[x].text
                            temp.append(internal_val)
                        log.info('temp value')
                        log.info(temp)
                        for y in range(0,inp_val_len):
                            input_val = input[y]
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
        return status,result,verb,err_msg


    def deselectAll(self,webelement,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        verb = OUTPUT_CONSTANT
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if webelement is not None:
            log.info('Recieved web element from the web dispatcher')
            log.debug(webelement)
            if ((webelement.is_enabled()) and webelement.is_displayed()):
                log.info(ERROR_CODE_DICT['MSG_OBJECT_ENABLED'])
                log.info(ERROR_CODE_DICT['MSG_OBJECT_DISPLAYED'])
                try:
                    select = Select(webelement)
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
                err_msg = 'Element is not displayed or enabled '
                logger.print_on_console('Element is not displayed or enabled ')
                log.info(ERROR_CODE_DICT['ERR_OBJECT_DISABLED'])
                log.info(ERROR_CODE_DICT['MSG_OBJECT_NOT_DISPLAYED'])
        return status,result,verb,err_msg
