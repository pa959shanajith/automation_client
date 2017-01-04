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

##import selenium
import Exceptions
from selenium.webdriver.support.ui import Select
##import browser_Keywords
import webconstants
from utilweb_operations import UtilWebKeywords
import logger
import radio_checkbox_operations
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
        if webelement is not None:
            if webelement.tag_name=='table':
                    webelement=self.radioKeywordsObj.getActualElement(webelement,input)
            if ((webelement.is_enabled()) and webelement.is_displayed()):
                try:
                    if (input is not None) :
                        input_val = int(input[0])
                        select = Select(webelement)
                        iList = select.options
                        iListSize = len(iList)
                        input_val=input_val-1
                        if(input_val < iListSize):
                            for i in range(0,iListSize):
                                if(input_val == i):
                                    select.select_by_index(input_val)
                                    status=webconstants.TEST_RESULT_PASS
                                    result=webconstants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Invalid input')
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.print_on_console('Element is not enabled or dispalyed')
        return status,result

    def getCount(self,webelement,*args):
        """
        def : getCount
        purpose : to retrieve number of objects in dropdown/listbox
        param  : webelement
        return : string
        """
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        iListSize = None
        if webelement is not None:
            if webelement.is_displayed():
                try:
                    select = Select(webelement)
                    iList = select.options
                    iListSize = len(iList)
                    logger.print_on_console(iListSize)
                    if (iListSize > 0):
                        status=webconstants.TEST_RESULT_PASS
                        result=webconstants.TEST_RESULT_TRUE
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.print_on_console('Element is not dispalyed')
        return status,result,str(iListSize)

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
                        elif len(input)==5:
                            inp_val = input[4]
                        select = Select(webelement)
                        select.select_by_visible_text(inp_val)
                        status=webconstants.TEST_RESULT_PASS
                        result=webconstants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Invalid input')
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.print_on_console('Element is not enabled or dispalyed')
        return status,result

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
        if webelement is not None:
            if webelement.is_displayed():
                try:
                    if ((input is not None) and (len(input) == 1)) :
##                        if not(visibilityFlag and isvisble):
                        select = Select(webelement)
                        first_value = select.first_selected_option.text
                        inp_val = input[0]
                        if (first_value == inp_val):
                            status=webconstants.TEST_RESULT_PASS
                            result=webconstants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Invalid input')
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.print_on_console('Element is not dispalyed')
        return status,result

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
        if webelement is not None:
            if webelement.is_displayed():
                try:
                    if ((input is not None) and (len(input) == 1)) :
##                        if not(visibilityFlag and isvisble):
                        select = Select(webelement)
                        iList = select.options
                        iListSize = len(iList)
                        logger.print_on_console(iListSize)
                        input_val = int(input[0])
                        if (iListSize == input_val):
                            status=webconstants.TEST_RESULT_PASS
                            result=webconstants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Invalid input')
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.print_on_console('Element is not dispalyed')
        return status,result

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
        try:
            if input is not None:
                if webelement is not None:
                    if webelement.is_displayed():
                        select = Select(webelement)
                        option_len = select.options
                        opt_len = len(option_len)
                        inp_val_len = len(input)
                        temp = []
                        flag = True
                        for x in range(0,opt_len):
                            internal_val = select.options[x].text
                            temp.append(internal_val)

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
                    else:
                        logger.print_on_console('Element is not dispalyed')
            else:
                logger.print_on_console('Provided input not present in element')

        except Exception as e:
            Exceptions.error(e)
        return status,result

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
        try:
            if input is not None:
                if webelement is not None:
                    if ((webelement.is_enabled()) and webelement.is_displayed()):
                        count= len(input)
                        select = Select(webelement)
                        iList = select.options
                        iListSize = len(iList)
                        for x in range(0,count):
                            input_val_temp = input[x]
                            input_val = int(input_val_temp)
                            select.select_by_index(input_val)
                        status=webconstants.TEST_RESULT_PASS
                        result=webconstants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Element is not enabled or displayed')
            else:
                logger.print_on_console('Invalid input')
        except Exception as e:
            Exceptions.error(e)
        return status,result

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
        try:
            if webelement is not None:
                if webelement.tag_name=='table':
                    webelement=self.radioKeywordsObj.getActualElement(webelement,input)
                if webelement.is_displayed():
                    select = Select(webelement)
                    index = select.all_selected_options
                    if (len(index) == '1'):
                        output = select.all_selected_options[i].text
                        str(output)
                        logger.print_on_console(output)
                        status=webconstants.TEST_RESULT_PASS
                        result=webconstants.TEST_RESULT_TRUE
                    else:
                        temp = []
                        for x in range(0,len(index)):
                            out = select.all_selected_options[x].text
                            value = str(out)
                            temp.append(value)
                        output = ';'.join(temp)
                        logger.print_on_console(output)
                        output=temp
                        status=webconstants.TEST_RESULT_PASS
                        result=webconstants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Element is not displayed')
        except Exception as e:
            Exceptions.error(e)
        return status, result, output


    def selectMultipleValuesByText(self,webelement,input,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        if webelement is not None:
            if ((webelement.is_enabled()) and webelement.is_displayed()):
                try:
                    count = len(input)
                    select = Select(webelement)
                    iList = select.options
                    iListSize = len(iList)
                    for x in range(0,count):
                        input_val = input[x]
                        select.select_by_visible_text(input_val)

                    status=webconstants.TEST_RESULT_PASS
                    result=webconstants.TEST_RESULT_TRUE
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.print_on_console('Element is not enabled or displayed')
        return status,result

    def getMultipleValuesByIndexes(self,webelement,input,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        output = None
        try:
            if input is not None:
                if webelement is not None:
                    if webelement.is_displayed():
                        count = len(input)
                        select = Select(webelement)
                        iList = select.options
                        iListSize = len(iList)
                        temp = []
                        for x in range(0,count):
                            input_val_temp = input[x]
                            input_val = int(input_val_temp)
                            out=select.options[input_val].text
                            value = str(out)
                            temp.append(value)
                        output = ';'.join(temp)
                        logger.print_on_console(output)
                        output=temp
                        status=webconstants.TEST_RESULT_PASS
                        result=webconstants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Element is not displayed')
            else:
                logger.print_on_console('Invalid input')
        except Exception as e:
            Exceptions.error(e)
        return status,result,output

    def selectAllValues(self,webelement,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        if webelement is not None:
            if ((webelement.is_enabled()) and webelement.is_displayed()):
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
                    if(size == iListSize):
                        status=webconstants.TEST_RESULT_PASS
                        result=webconstants.TEST_RESULT_TRUE
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.print_on_console('Element is not enabled or displayed')
        return status,result

    def getValueByIndex(self,webelement,input,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        output = None
        if webelement is not None:
            if webelement.is_displayed():
                try:
                    if input is not None:
##                        if not(visibilityFlag and isvisble):
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
                    else:
                        logger.print_on_console('Invalid input')
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.print_on_console('Element is not displayed')
        return status,result,output

    def verifyValuesExists(self,webelement,input,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        try:
            if input is not None:
                if webelement is not None:
                    if webelement.is_displayed():
                        select = Select(webelement)
                        option_len = select.options
                        opt_len = len(option_len)
                        inp_val_len = len(input)
                        temp = []
                        flag = True
                        for x in range(0,opt_len):
                            internal_val = select.options[x].text
                            str(internal_val)
                            temp.append(internal_val)
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
                        else:
                            logger.print_on_console('Inputs does not match')
                    else:
                        logger.print_on_console('Element is not displayed')
            else:
                logger.print_on_console('Invalid input')
        except Exception as e:
            Exceptions.error(e)
        return status,result

    def deselectAll(self,webelement,*args):
        status=webconstants.TEST_RESULT_FAIL
        result=webconstants.TEST_RESULT_FALSE
        visibilityFlag=True
        if webelement is not None:
            if ((webelement.is_enabled()) and webelement.is_displayed()):
                try:
                    select = Select(webelement)
                    select.deselect_all()
                    check = select.all_selected_options
                    if(len(check) == 0):
                        status=webconstants.TEST_RESULT_PASS
                        result=webconstants.TEST_RESULT_TRUE
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.print_on_console('Element is not displayed or enabled ')
        return status,result
