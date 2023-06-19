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
from text_keywords_sap import Text_Keywords
#-----------------------------------------------------Module Imports

class Table_keywords():

    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()
        self.rk = Radio_Checkbox_keywords()
        self.tk = Text_Keywords()

    def getXpath(self, sap_id, elem, row, col):
        try:
            cell = elem.GetCell(row, col)
            cell_id = cell.id.split('/')
            cell_xpath = sap_id + '/' + cell_id[-1]
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Not able to get cell_xpath' )
        return cell, cell_xpath


    def getRowCount(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id ):
                elem = ses.FindById(id)
                value = elem.RowCount
                status = sap_constants.TEST_RESULT_PASS
                result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in getRowCount' )
        return status, result, value, err_msg


    def getColumnCount(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        result = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id ):
                elem = ses.FindById(id)
                value = elem.Columns.Length
                status = sap_constants.TEST_RESULT_PASS
                result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in getColumnCount' )
        return status, result, value, err_msg


    def getColNumByText(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id ):
                colText = input_val[0]
                elem = ses.FindById(id)
                no_of_cols = elem.Columns.Length
                no_of_rows = elem.RowCount
                for i in range(-1, no_of_rows):
                    for j in range(-1, no_of_cols):
                        cell = None
                        try:
                            cell = elem.GetCell(i,j)
                        except:
                            pass
                        if (cell and colText in cell.text ):
                            value = j+1
                            flag = True
                            break
                    if ( flag ):
                        break
                if ( not flag ):
                    value = ''
                    err_msg = 'No matching text found in the table'
                else:
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in getColNumByText' )
        return status, result, value, err_msg



    def getRowNumByText(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id ):
                elem = ses.FindById(id)
                rowText = input_val[0]
                no_of_cols = elem.Columns.Length
                no_of_rows = elem.RowCount
                for i in range(0, no_of_rows):
                    for j in range(0, no_of_cols):
                        try:
                            cell = elem.GetCell(i,j)
                        except:
                            break
                        if ( rowText in cell.text ):
                            value = i + 1
                            flag = True
                            break
                    if ( flag ):
                        break
                if ( not flag ):
                    value = ''
                    err_msg = 'No matching text found in the table'
                else:
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in getRowNumByText' )
        return status, result, value, err_msg



    def getCellValue(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id ):
                row = int(input_val[0]) - 1
                col = int(input_val[1]) - 1
                if ( row < 0 or col < 0 ):
                    err_msg = 'Index value of row or column is negative'
                else:
                    elem = ses.FindById(id)
                    value = elem.GetCell(row, col).text
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in getCellValue' )
        return status, result, value, err_msg



    def verifyCellValue(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id ):
                elem = ses.FindById(id)
                row = int(input_val[0]) - 1
                col = int(input_val[1]) - 1
                cell_value = input_val[2]
                if ( row >= 0 and col >= 0 ):
                    if ( elem.GetCell(row, col).text == cell_value ):
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = 'Cell value and Input value do not Match'
                else:
                    err_msg = 'Index value of row or column is negative'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in verifyCellValue' )
        return status, result, value, err_msg



    def verifyTextExists(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id ):
                elem = ses.FindById(id)
                text = input_val[0]
                no_of_cols = elem.Columns.Length
                no_of_rows = elem.RowCount
                for i in range(0, no_of_rows):
                    for j in range(0, no_of_cols):
                        try:
                            cell = elem.GetCell(i,j)
                        except:
                            break
                        if ( cell.text == text ):
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                            break
                    if ( result != sap_constants.TEST_RESULT_FALSE ):
                        break
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in verifyTextExists' )
        return status, result, value, err_msg



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


    # def selectValueByIndex(self, sap_id, url, input_val, *args):
    #     status = sap_constants.TEST_RESULT_FAIL
    #     result = sap_constants.TEST_RESULT_FALSE
    #     """Object type is dropdown and lists. For SAP, we only have dropdowns."""
    #     value = OUTPUT_CONSTANT
    #     err_msg = None
    #     try:
    #         self.lk.setWindowToForeground(sap_id)
    #         id,ses = self.uk.getSapElement(sap_id)
    #         if ( id ):
    #             row = int(input_val[0])-1
    #             col = int(input_val[1])-1
    #             object_type_input = ses.FindById(id).type
    #             elem = ses.FindById(id)
    #             cell ,cell_xpath = self.getXpath(sap_id,elem,row,col)
    #             if ( cell.__getattr__("type") == object_type_input ):
    #                 err_msg = 'Error: Type Mismatch'
    #             else:
    #                 dk = Dropdown_Keywords()
    #                 text = input_val[2]
    #                 status,result,value,err_msg = dk.selectValueByIndex(cell_xpath, url, text)
    #         else:
    #             err_msg = sap_constants.ELELMENT_NOT_FOUND
    #         if ( err_msg ):
    #             log.info(err_msg)
    #             logger.print_on_console(err_msg)
    #     except Exception as e:
    #        err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
    #        log.error(err_msg)
    #        logger.print_on_console('Error occured in selectValueByText')
    #     return status,result,value,err_msg


    def selectValueByText(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        """Object type is dropdown and lists. For SAP, we only have dropdowns."""
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            self.lk.setWindowToForeground(sap_id)
            id,ses = self.uk.getSapElement(sap_id)
            if ( id ):
                row = int(input_val[0])-1
                col = int(input_val[1])-1
                object_type_input = ses.FindById(id).type
                elem = ses.FindById(id)
                cell, cell_xpath = self.getXpath(sap_id, elem, row, col)
                if ( cell.__getattr__("type") == object_type_input ):
                    err_msg = 'Error: Type Mismatch'
                else:
                    dk = Dropdown_Keywords()
                    text = input_val[2]
                    status, result, value, err_msg = dk.selectValueByText(cell_xpath, text)
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in selectValueByText' )
        return status, result, value, err_msg



    def getSelected(self, sap_id, input_val, *args):

        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        """Object type is dropdown and lists. For SAP, we only have dropdowns."""
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id ):
                object_type_input = ses.FindById(id).type
                row = int(input_val[0])-1
                col = int(input_val[1])-1
                elem = ses.FindById(id)
                cell, cell_xpath = self.getXpath(sap_id, elem, row, col)
                if ( cell.__getattr__("type") == object_type_input ):
                    err_msg = 'Error: Type Mismatch'
                else:
                    dk = Dropdown_Keywords()
                    status, result, value, err_msg = dk.getSelected(cell_xpath)
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in getSelected' )
        return status, result, value, err_msg


    def getStatus(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id ):
                row = int(input_val[0])-1
                col = int(input_val[1])-1
                object_type_input = ses.FindById(id).type
                elem = ses.FindById(id)
                cell, cell_xpath = self.getXpath(sap_id, elem, row, col)
                if ( cell.__getattr__("type") == object_type_input ):
                    err_msg = 'Error: Type Mismatch'
                else:
                    object_type_input = cell.__getattr__("type")
                    if ( object_type_input == "GuiRadioButton" or object_type_input == "GuiCheckBox" ):
                        status, result, value, err_msg = self.rk.get_status(cell_xpath)
                    else:
                        err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in getStatus' )
        return status, result, value, err_msg


    def selectRow(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id ):
                rowNum = int(input_val[0])-1
                elem = ses.FindById(id)
                rows = elem.Rows
                row_to_select = rows[rowNum]
                if ( row_to_select.Selectable == True ):
                    row_to_select.selected = True
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in selectRow' )
        return status, result, value, err_msg

    def selectColumn(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                colNum = int(input_val[0])-1
                elem = ses.FindById(id)
                columns = elem.Columns
                column_to_select = columns[colNum]
                if( elem.ColSelectMode != 0 ):
                    column_to_select.selected = True
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else : err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else : err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in selectColumn' )
        return status, result, value, err_msg


    def unselectRow(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id ):
                rowNum = int(input_val[0])-1
                elem = ses.FindById(id)
                rows = elem.Rows
                row_to_select = rows[rowNum]
                if ( row_to_select.Selectable == True ):
                    row_to_select.selected = False
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in unselectRow' )
        return status, result, value, err_msg

    def unselectColumn(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                colNum = int(input_val[0])-1
                elem = ses.FindById(id)
                columns = elem.Columns
                column_to_select = columns[colNum]
                if( elem.ColSelectMode != 0 ):
                    column_to_select.selected = True
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else : err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else : err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in unselectColumn' )
        return status, result, value, err_msg


    def setCellText(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id ):
                row = int(input_val[0]) - 1
                col = int(input_val[1]) - 1
                elem = ses.FindById(id)
                cell, cell_xpath = self.getXpath(sap_id, elem, row, col)
                status, result, value, err_code = self.tk.setText(cell_xpath, [input_val[2]])
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in setCellText' )
        return status, result, value, err_msg