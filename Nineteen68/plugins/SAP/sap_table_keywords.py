#-------------------------------------------------------------------------------
# Name:        SAP_Table_keywords
# Purpose:     To perform Actions of SAP Table objects
#
# Author:      anas.ahmed,sakshi.goyal
#
# Created:     06-04-2017
# Copyright:   (c) anas.ahmed 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger
import sap_constants
from constants import *
from saputil_operations import SapUtilKeywords
import logging
import logging.config
log = logging.getLogger('sap_table_keywords.py')
#-----------------------------------------------------Module Imports
from sap_launch_keywords import Launch_Keywords
from sap_dropdown_keywords import Dropdown_Keywords
from radio_checkbox_keywords_sap import Radio_Checkbox_keywords
#-----------------------------------------------------Module Imports

class Table_keywords():

    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()
        self.rk = Radio_Checkbox_keywords()

    def getXpath(self,sap_id,elem,row,col):
        try:
            cell = elem.GetCell(row, col)
            cell_id = cell.id.split('/')
            cell_xpath = sap_id + '/' + cell_id[-1]
        except Exception as e:
            log.error('Error occured',e)
            logger.print_on_console('Not able to get cell_xpath')
        return cell,cell_xpath


    def getRowCount(self, sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
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
            logger.print_on_console("Error occured in getRowCount")
        return status,result,value,err_msg


    def getColumnCount(self, sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
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
            logger.print_on_console("Error occured in getColumnCount")
        return status,result,value,err_msg


    def getColNumByText(self, sap_id, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        colText=input_val[0]
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            no_of_cols = elem.Columns.Length
            no_of_rows = elem.RowCount
            for i in range(-1, no_of_rows):
                for j in range(-1, no_of_cols):
                    try:
                        cell = elem.GetCell(i,j)
                    except:
                        break
                    if(colText in elem.GetCell(i,j).text):
                        value = j+1
                        break
                    else:
                        value =''
                if(value != ''):
                    break
            if(value == ''):
                logger.print_on_console('No matching text found in the table')
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console("Error occured in getColNumByText")
        return status,result,value,err_msg



    def getRowNumByText(self, sap_id, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        rowText=input_val[0]
        id,ses=self.uk.getSapElement(sap_id)
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
                    try:
                        cell = elem.GetCell(i,j)
                    except:
                        break
                    if(rowText in cell.text):
                        value = i+1
                        break
                    else:
                        value =''
                if(value != ''):
                    break
            if(value==''):
                logger.print_on_console('No matching text found in the table')
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console("Error occured in getRowNumByText")
        return status,result,value,err_msg



    def getCellValue(self, sap_id, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-1
        col=int(input_val[1])-1
        id,ses=self.uk.getSapElement(sap_id)
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
            logger.print_on_console("Error occured in getCellValue")
        return status,result,value,err_msg



    def verifyCellValue(self, sap_id, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-1
        col=int(input_val[1])-1
        cell_value=input_val[2]

        id,ses=self.uk.getSapElement(sap_id)
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
            logger.print_on_console("Error occured in verifyCellValue")
        return status,result,value,err_msg



    def verifyTextExists(self, sap_id, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        text=input_val[0]
        id,ses=self.uk.getSapElement(sap_id)
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
                    try:
                        cell = elem.GetCell(i,j)
                    except:
                        break
                    if(cell.text == text):
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
                        break
                if(result != sap_constants.TEST_RESULT_FALSE):
                    break
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console("Error occured in verifyTextExists")
        return status,result,value,err_msg



##    def cellClick(self, sap_id,url, input_val,*args):
##        self.lk.setWindowToForeground(sap_id)
##        row=int(input_val[0])-2
##        col=int(input_val[1])-2
##        text=input_val[2]
##        id,ses=self.uk.getSapElement(sap_id)
##        rk=Radio_Checkbox_keywords()
##        bk =ButtonLinkKeyword()
##        dk = Dropdown_Keywords()
##        url=''#dummy variable
##        status = sap_constants.TEST_RESULT_FAIL
##        result = sap_constants.TEST_RESULT_FALSE
##        value = OUTPUT_CONSTANT
##        err_msg=None
##        try:
##            object_type_input = ses.FindById(id).type
##            elem=ses.FindById(id)
##            cell ,cell_xpath =self.getXpath(sap_id,elem,row,col)
##            if(cell.__getattr__("type") != object_type_input):
##                print "Error: Type Mismatch"
##            else:
##                if(object_type_input == "GuiTextField" or object_type_input == "GuiCTextField"):
##                    cell.setFocus()
##                    result = True
##                if(object_type_input == "GuiCheckBox"):
##                    status,result,isSelected,err_msg = rk.checkbox_getStatus(cell_xpath)
##                    if(isSelected == sap_constants.CHECKED_CHECK):
##                        status,result,value,err_msg = rk.select_checkbox(cell_xpath)
##                    else:
##                        status,result,value,err_msg = rk.unselect_checkbox(cell_xpath)
##
##                if(object_type_input == "GuiRadioButton"):
##                    status,result,value,err_msg = rk.select_radiobutton(cell_xpath)
##
##                if(object_type_input == "GuiButton"):
##                    status,result,value,err_msg = bk.click(cell_xpath)
##
##                if(object_type_input == "GuiComboBox"):
##                    if( text != None or text != ''):
##                        status,result,value,err_msg = dk.selectValueByText(cell_xpath,url, text)
##                    else:
##                        logger.print_on_console('Text is not Entered to perform this action')
##        except Exception as e:
##            log.error('Error occured',e)
##            err_msg = sap_constants.ERROR_MSG
##        return status,result,value,err_msg


    def selectValueByText(self, sap_id, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-1
        col=int(input_val[1])-1
        text= input_val[2]
        id,ses=self.uk.getSapElement(sap_id)
        dk = Dropdown_Keywords()
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        """Object type is dropdown and lists. For SAP, we only have dropdowns."""
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            object_type_input = ses.FindById(id).type
            elem=ses.FindById(id)
            cell ,cell_xpath =self.getXpath(sap_id,elem,row,col)
            if(cell.__getattr__("type") == object_type_input):
                logger.print_on_console("Error: Type Mismatch")
            else:
                result = dk.selectValueByText(cell_xpath,text)
                status=sap_constants.TEST_RESULT_PASS
                result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console("Error occured in selectValueByText")
        return status,result,value,err_msg



    def getSelected(self, sap_id, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-1
        col=int(input_val[1])-1
        id,ses=self.uk.getSapElement(sap_id)
        dk = Dropdown_Keywords()
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        """Object type is dropdown and lists. For SAP, we only have dropdowns."""
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            object_type_input = ses.FindById(id).type
            elem=ses.FindById(id)
            cell ,cell_xpath =self.getXpath(sap_id,elem,row,col)
            if(cell.__getattr__("type") == object_type_input):
                logger.print_on_console("Error: Type Mismatch")
            else:
                status,result,value,err_msg = dk.getSelected(cell_xpath)
                #status=sap_constants.TEST_RESULT_PASS
                #result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console("Error occured in getSelected")
        return status,result,value,err_msg


    def getStatus(self, sap_id,input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-1
        col=int(input_val[1])-1
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            object_type_input = ses.FindById(id).type
            elem=ses.FindById(id)
            cell ,cell_xpath =self.getXpath(sap_id,elem,row,col)
            if(cell.__getattr__("type") == object_type_input):
                logger.print_on_console("Error: Type Mismatch")
            else:
                object_type_input=cell.__getattr__("type")
                if(object_type_input == "GuiRadioButton" or object_type_input == "GuiCheckBox" ):
                    status,result,value,err_msg = self.rk.get_status(cell_xpath)
                else:
                    logger.print_on_console('Element state does not allow to perform the operation')
                    err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console("Error occured in getStatus")
        return status,result,value,err_msg


    def selectRow(self, sap_id, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        rowNum=int(input_val[0])-1
        id,ses=self.uk.getSapElement(sap_id)
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
            logger.print_on_console("Error occured in selectRow")
        return status,result,value,err_msg



    def unselectRow(self, sap_id, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        rowNum=int(input_val[0])-1
        id,ses=self.uk.getSapElement(sap_id)
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
            logger.print_on_console("Error occured in unselectRow")
        return status,result,value,err_msg


