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
from saputil_operations import SapUtilKeywords
import logging
import logging.config
log = logging.getLogger('table_keywords.py')
#-----------------------------------------------------Module Imports
from pyrobot import Robot
from launch_keywords import Launch_Keywords
from button_link_keywords_sap import ButtonLinkKeyword
from dropdown_keywords import Dropdown_Keywords
from radio_checkbox_keywords_sap import Radio_Checkbox_keywords
from element_keywords import ElementKeywords
#-----------------------------------------------------Module Imports

class Table_keywords():

    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()

    def getXpath(self,sap_id,elem,row,col):
        try:
            cell = elem.GetCell(row, col)
            cell_id = cell.id.split('/')
            cell_xpath = sap_id + '/' + cell_id[-1]
        except Exception as e:
            log.error('Error occured',e)
            logger.print_on_console('was not able to get cell_xpath')
        return cell,cell_xpath



    def setFocus(self, sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
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
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            value = elem.RowCount+1
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
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
            value = elem.Columns.Length+1
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def mouseHover(self, sap_id,url, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-2
        col=int(input_val[1])-2
        id,ses=self.uk.getSapElement(sap_id)
        w1,w2,wndname,w3=self.lk.getPageTitle()
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            cell = elem.GetCell(row, col)
            left =  cell.__getattr__("ScreenLeft")
            width = cell.__getattr__("Width")
            x = left + width/2
            top =  cell.__getattr__("ScreenTop")
            height = cell.__getattr__("Height")
            y= top + height/2
            rob =Robot(str(wndname))
            rob.set_mouse_pos( int(x), int(y))
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def getColNumByText(self, sap_id,url, input_val,*args):
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
            for i in range(0, no_of_rows):
                for j in range(0, no_of_cols):
                    if(colText in elem.GetCell(i,j).text):
                        value = j+2
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
        return status,result,value,err_msg



    def getRowNumByText(self, sap_id,url, input_val,*args):
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
                    if(rowText in elem.GetCell(i,j).text):
                        value = i+2
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
        return status,result,value,err_msg



    def getCellValue(self, sap_id,url, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-2
        col=int(input_val[1])-2
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
        return status,result,value,err_msg



    def verifyCellValue(self, sap_id,url, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-2
        col=int(input_val[1])-2
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
        return status,result,value,err_msg



    def verifyTextExists(self, sap_id,url, input_val,*args):
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



    def selectValueByIndex(self, sap_id,url, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-2
        col=int(input_val[1])-2
        index=input_val[2]
        id,ses=self.uk.getSapElement(sap_id)
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
            cell ,cell_xpath =self.getXpath(sap_id,elem,row,col)
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
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-2
        col=int(input_val[1])-2
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
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-2
        col=int(input_val[1])-2
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
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-2
        col=int(input_val[1])-2
        id,ses=self.uk.getSapElement(sap_id)
        rk=Radio_Checkbox_keywords()
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            object_type_input = ses.FindById(id).type
            elem=ses.FindById(id)
            cell ,cell_xpath =self.getXpath(sap_id,elem,row,col)
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
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-2
        col=int(input_val[1])-2
        ek=ElementKeywords()
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        """Object type is dropdown and lists. For SAP, we only have dropdowns."""
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            cell ,cell_xpath =self.getXpath(sap_id,elem,row,col)
            d1,d2,value,d3 = ek.getTooltipText(cell_xpath)
            if(value!=None or value!=Null):
                status=sap_constants.TEST_RESULT_PASS
                result=sap_constants.TEST_RESULT_TRUE
            else:
                logger.print_on_console('ToolTipText not avaliable for the element ')
                err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            log.error('Error occured',e)
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def tableCell_click(self, sap_id, url,input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-2
        col=int(input_val[1])-2
        id,ses=self.uk.getSapElement(sap_id)
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        w1,w2,wndname,w3=self.lk.getPageTitle()
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            cell ,cell_xpath =self.getXpath(sap_id,elem,row,col)
            left =  cell.__getattr__("ScreenLeft")
            width = cell.__getattr__("Width")
            x = left + width/2
            top =  cell.__getattr__("ScreenTop")
            height = cell.__getattr__("Height")
            y= top + height/2
            rob =Robot(str(wndname))
            rob.move_and_click( int(x), int(y),"Left")
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            import traceback
            traceback.print_exc()
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def tableCell_doubleClick(self, sap_id, url,input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        row=int(input_val[0])-2
        col=int(input_val[1])-2
        id,ses=self.uk.getSapElement(sap_id)
        w1,w2,wndname,w3=self.lk.getPageTitle()
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg=None
        try:
            elem=ses.FindById(id)
            cell ,cell_xpath =self.getXpath(sap_id,elem,row,col)
            left =  cell.__getattr__("ScreenLeft")
            width = cell.__getattr__("Width")
            x = left + width/2
            top =  cell.__getattr__("ScreenTop")
            height = cell.__getattr__("Height")
            y= top + height/2
            rob =Robot(str(wndname))
            rob.set_mouse_pos( int(x), int(y))
            rob.double_click_mouse("Left")
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error('Error occured',e)
            import traceback
            traceback.print_exc()
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg



    def selectRow(self, sap_id,url, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        rowNum=int(input_val[0])-2
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
        return status,result,value,err_msg



    def unselectRow(self, sap_id,url, input_val,*args):
        self.lk.setWindowToForeground(sap_id)
        rowNum=int(input_val[0])-2
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
        return status,result,value,err_msg


