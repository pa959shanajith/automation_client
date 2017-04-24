#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sakshi.goyal
#
# Created:     06-04-2017
# Copyright:   (c) sakshi.goyal 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import win32com.client
import logger

import sap_constants
import time
from constants import *
from text_keywords_sap import Text_Keywords

import logging
import logging.config
log = logging.getLogger('table_keywords.py')
#-----------------------------------------------------Module Imports
from launch_keywords import Launch_Keywords
from button_link_keywords_sap import ButtonLinkKeyword
from dropdown_keywords import Dropdown_Keywords
from radio_checkbox_keywords_sap import Radio_Checkbox_keywords
#-----------------------------------------------------Module Imports

class Table_keywords():

    def getXpath(elem,row,col):
        try:
            cell = elem.GetCell(row, col)
            cell_id = cell.id.split('/')
            cell_xpath = sap_id + '/' + cell_id[-1]
        except Exception as e:
            log.error('Error occured',e)
            logger.print_on_console('was not able to get cell_xpath')
        return cell,cell_xpath



    def setFocus(self, sap_id, *args):
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            elem.SetFocus()
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def getRowCount(self, sap_id, *args):
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            value = elem.RowCount
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def getColumnCount(self, sap_id, *args):
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        result = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            value = elem.Columns.Length
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def mouseHover(self, sap_id,url, input_val,*args):
        row=input_val[0]
        col=input_val[1]
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            elem.GetCell(row, col).SetFocus()
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def getColNumByText(self, sap_id,url, input_val,*args):
        colName=input_val[0]
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            cols = elem.Columns
            for i in range(0, cols.Count):
                if (cols(i).Title == colName):
                    value = i
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                    break
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def getRowNumByText(self, sap_id,url, input_val,*args):
        rowText=input_val[0]
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            no_of_cols = elem.Columns.Length
            no_of_rows = elem.RowCount
            for i in range(0, no_of_rows):
                for j in range(0, no_of_cols):
                    if(id.GetCell(i,j).text == rowText):
                        value = i
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
                        break
                if(result != None):
                    break
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def getCellValue(self, sap_id,url, input_val,*args):
        row=input_val[0]
        col=input_val[1]
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            value = elem.GetCell(row, col).text
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def verifyCellValue(self, sap_id,url, input_val,*args):
        row=input_val[0]
        col=input_val[1]
        cell_value=input_val[2]

        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            if(elem.GetCell(row, col).text == cell_value):
                status=sap_constants.TEST_RESULT_PASS
                result=sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def verifyTextExists(self, sap_id,url, input_val,*args):
        text=input_val[0]
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            no_of_cols = elem.Columns.Length
            no_of_rows = elem.RowCount
            for i in range(0, no_of_rows):
                for j in range(0, no_of_cols):
                    if(ses.FindById(id).GetCell(i,j).text == text):
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
                        break
                if(result != sap_constants.TEST_RESULT_FALSE):
                    break
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG

        return status,result,value,err_msg



    def cellClick(self, sap_id,url, input_val,*args):
        row=input_val[0]
        col=input_val[1]
        text=input_val[2]
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        rk=Radio_Checkbox_keywords()
        bk =ButtonLinkKeyword()
        dk = Dropdown_Keywords()
        url=''#dummy variable
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            object_type_input = ses.FindById(id).type
            elem=ses.FindById(id)
            tabk=Table_keywords()
            cell ,cell_xpath =tabk.getXpath(elem,row,col)
            if(cell.__getattr__("type") != object_type_input):
                print "Error: Type Mismatch"
            else:
                if(object_type_input == "GuiTextField" or object_type_input == "GuiCTextField"):
                    cell.setFocus()
                    result = True
                if(object_type_input == "GuiCheckBox"):
                    status,result,isSelected,err_msg = rk.checkbox_getStatus(cell_xpath)
                    if(isSelected == sap_constants.CHECKED_CHECK):
                        status,result,value,err_msg = rk.select_checkbox(cell_xpath)
                    else:
                        status,result,value,err_msg = rk.unselect_checkbox(cell_xpath)

                if(object_type_input == "GuiRadioButton"):
                    status,result,value,err_msg = rk.select_radiobutton(cell_xpath)

                if(object_type_input == "GuiButton"):
                    status,result,value,err_msg = bk.click(cell_xpath)

                if(object_type_input == "GuiComboBox"):
                    if( text != None or text != ''):
                        status,result,value,err_msg = dk.selectValueByText(cell_xpath,url, text)
                    else:
                        logger.print_on_console('Text is not Entered to perform this action')
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def selectValueByIndex(self, sap_id,url, input_val,*args):
        row=input_val[0]
        col=input_val[1]
        index=input_val[2]
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        dk = Dropdown_Keywords()
        url=''#dummy variable
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        """Object type is dropdown and lists. For SAP, we only have dropdowns."""
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            object_type_input = ses.FindById(id).type
            elem=ses.FindById(id)
            tabk=Table_keywords()
            cell ,cell_xpath =tabk.getXpath(elem,row,col)
            if(cell.__getattr__("type") != object_type_input):
                print "Error: Type Mismatch"
            else:
                value = dk.selectValueByIndex(cell_xpath,url, index)
                status=sap_constants.TEST_RESULT_PASS
                result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def selectValueByText(self, sap_id, url,input_val,*args):
        row=input_val[0]
        col=input_val[1]
        text= input_val[2]
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        dk = Dropdown_Keywords()
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        """Object type is dropdown and lists. For SAP, we only have dropdowns."""
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            object_type_input = ses.FindById(id).type
            elem=ses.FindById(id)
            tabk=Table_keywords()
            cell ,cell_xpath =tabk.getXpath(elem,row,col)
            if(cell.__getattr__("type") != object_type_input):
                print "Error: Type Mismatch"
            else:
                result = dk.selectValueByText(cell_xpath,url, text)
                status=sap_constants.TEST_RESULT_PASS
                result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def getSelected(self, sap_id,url, input_val,*args):
        row=input_val[0]
        col=input_val[1]
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        dk = Dropdown_Keywords()
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        """Object type is dropdown and lists. For SAP, we only have dropdowns."""
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            object_type_input = ses.FindById(id).type
            elem=ses.FindById(id)
            tabk=Table_keywords()
            cell ,cell_xpath =tabk.getXpath(elem,row,col)
            if(cell.__getattr__("type") != object_type_input):
                print "Error: Type Mismatch"
            else:
                status,result,value,err_msg = dk.getSelected(cell_xpath)
                #status=sap_constants.TEST_RESULT_PASS
                #result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def getStatus(self, sap_id, url,input_val,*args):
        row=input_val[0]
        col=input_val[1]
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        rk=Radio_Checkbox_keywords()
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            object_type_input = ses.FindById(id).type
            elem=ses.FindById(id)
            tabk=Table_keywords()
            cell ,cell_xpath =tabk.getXpath(elem,row,col)
            if(cell.__getattr__("type") != object_type_input):
                print "Error: Type Mismatch"
            else:
                if(object_type_input == "GuiRadioButton" or object_type_input == "GuiCheckBox" ):
                    if(object_type_input == "GuiRadioButton"):
                        status,result,value,err_msg = rk.getStatus(cell_xpath)
                    elif(object_type_input == "GuiCheckBox"):
                        status,result,value,err_msg = rk.getStatus(cell_xpath)
                    #status=sap_constants.TEST_RESULT_PASS
                    #result=sap_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Element state does not allow to perform the operation')
                    err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def getCellToolTip(self, sap_id, url,input_val,*args):
        row=input_val[0]
        col=input_val[1]
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        """Object type is dropdown and lists. For SAP, we only have dropdowns."""
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            tabk=Table_keywords()
            cell ,cell_xpath =tabk.getXpath(elem,row,col)
            value = tk.getTooltipText(cell_xpath)
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def tableCell_click(self, sap_id,*args):
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            elem.SetFocus()
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def tableCell_doubleClick(self, sap_id,*args):
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            elem.SetFocus()
            i = elem.index('wnd')
            wndId = elem[:i+6]
            element = ses.FindById(wndId)
            value = ok.Object_Keywords().sendFunctionKeys(ses, element, "F2")
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def selectRow(self, sap_id,url, input_val,*args):
        rowNum=input_val[0]
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            rows = elem.Rows
            row_to_select = rows[rowNum]
            if(row_to_select.Selectable == True):
                row_to_select.selected = True
                status=sap_constants.TEST_RESULT_PASS
                result=sap_constants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Element state does not allow to perform the operation')
                err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def unselectRow(self, sap_id,url, input_val,*args):
        rowNum=input_val[0]
        tk=Text_Keywords()
        id,ses=tk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            rows = elem.Rows
            row_to_select = rows[rowNum]
            if(row_to_select.Selectable == True):
                row_to_select.selected = False
                status=sap_constants.TEST_RESULT_PASS
                result=sap_constants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('Element state does not allow to perform the operation')
                err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg


