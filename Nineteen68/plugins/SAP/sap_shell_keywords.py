#-------------------------------------------------------------------------------
# Name:         SAP_Shell_keywords
# Purpose:      Handling SAP-Shell elements
#
# Author:       anas.ahmed1
#
# Created:      15-06-2017
# Copyright:    (c) anas.ahmed1 2017
# Licence:      <your licence>
#-------------------------------------------------------------------------------
import sap_constants
from constants import *
import logger
from saputil_operations import SapUtilKeywords
from sap_launch_keywords import Launch_Keywords
import logging
log = logging.getLogger("sap_shell_keywords.py")

class Shell_Keywords():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()
        #self.nodeList = []

    def get_rowCount(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' ):
                    value = elem.rowCount
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                    log.debug( 'Get Shell Row Count => Row Count is : ' + str(value) )
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str( e )
            log.error( err_msg )
            logger.print_on_console( 'Error occured in GETROWCOUNT' )
        return status, result, value, err_msg

    def get_colCount(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' ):
                    value = elem.columnCount
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                    log.debug( 'Get Shell Column Count => Column Count is : ' + str(value) )
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str( e )
            log.error( err_msg )
            logger.print_on_console( 'Error occured in GETCOLUMNCOUNT' )
        return status, result, value, err_msg

    def getRowColByText(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        colOrder = []
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' ):
                    checkVal = input_val[0]
                    row_count = elem.rowCount
                    col_count = elem.columnCount
                    for col in range(col_count):
                        colOrder.append(elem.columnorder(col))
                    data = {}
                    cnt = 0
                    for row in range(row_count):
                        dataRow = {}
                        for col in range(col_count):
                            valFromTable = elem.getCellValue(row, colOrder[col])
                            if ( checkVal == valFromTable ):
                                dataRow['Row'] = str(row + 1)
                                dataRow['Col'] = str(col + 1)
                                cnt = cnt + 1
                                data[cnt] = dataRow
                    value = data
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                    if ( len(value) == 0 ):
                        err_msg = 'No matching text found in shell'
                    else:
                        log.debug('Get Shell Row Column By Text => Value is :' + str( value ))
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occoured in RowColumnNumberByText' )
        return status, result, value, err_msg

    def selectRows(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        row = []
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' ):
                    #-------to handle multiple inputs
                    if ( len( input_val ) > 1 ):
                       for i in range(0,len(input_val)):
                            rows = int(input_val[i])-1
                            row.append(rows)
                       rowpos = ','.join(map(str,row))
                    else:
                        row = int(input_val[0])-1
                        rowpos = str(row)
                    #-------to handle multiple inputs
                    if ( elem.rowCount != 0 ):
                        elem.selectedRows=rowpos
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error(e)
            logger.print_on_console( 'Error occured in SELECTROWS' )
        return status, result, value, err_msg

    def toolBarActionKeys(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' ):
                    if ( elem.rowCount != 0 ):
                        action = input_val[0]
                        elem.pressButton(unicode(action, "utf-8"))
                        status = TEST_RESULT_PASS
                        result = TEST_RESULT_TRUE
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error(err_msg)
            logger.print_on_console( 'Error occured in toolBarActionKeys' )
        return status, result, value, err_msg

    def getCellText(self, sap_id,input_val,*args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        bList = []
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            d1,d2,imax,d3 = self.get_colCount(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' ):
                    row = int(input_val[0])-1
                    index = int(input_val[1])-1
                    if ( elem.rowCount != 0 ):
                        #----------------------------------function to append columnorder
                        for i in range(0,imax):
                            b=elem.columnorder(i)
                            bList.append(b)
                        #----------------------------------function to append columnorder
                        if ( index >= 0 and row >= 0 ):
                            column = str(bList[index])
                            value = elem.getCellValue(row, column)
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = 'Row and column values are incorrect'
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console('Error occured in GetCellText')
        return status, result, value, err_msg

    def pressToolBarButton(self, sap_id,input_val,*args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                try:
                    rowcount = elem.rowCount
                    ele_type = "GuiGridControl"
                except Exception as e:
                    ele_type = "GuiToolbarControl"
                if ( elem.type == 'GuiShell' ):
                    if ( ele_type == "GuiGridControl" ):
                        try:
                            #-------------------------------store the tooltips of the grid buttons
                            lim = elem.ToolbarButtonCount
                            for x in range (0,lim):
                                 a = elem.GetToolbarButtonTooltip(x)
                                 if ( str(input_val[0]).strip().lower() == str(a).strip().lower() ):
                                    elmID = elem.GetToolbarButtonId(x)
                                    if ( (elem.GetToolbarButtonType(x) == "Menu" or "ButtonAndMenu") and len(input_val) > 1 ):
                                        menuItem = str(input_val[1]).strip()
                                        elem.PressToolbarContextButton(elmID)
                                        elem.SelectContextMenuItemByText(menuItem)
                                    else:
                                        elem.PressToolbarButton(elmID)
                                    status = sap_constants.TEST_RESULT_PASS
                                    result = sap_constants.TEST_RESULT_TRUE
                                    break
                            #-------------------------------store the tooltips of the grid buttons
                        except Exception as e:
                            logger.print_on_console('Unable to press button / button does not exist')
                            err_msg = sap_constants.ERROR_MSG
                    elif ( ele_type == "GuiToolbarControl" ):
                        count = elem.ButtonCount
                        btn_id = None
                        for i in range(0,count):
                            if ( elem.GetButtonTooltip(i).lower() == str(input_val[0]).strip().lower() ):
                                btn_id = elem.GetButtonId(i)
                                btn_type = elem.GetButtonType(i)
                                break
                        if ( btn_id ):
                            if ( btn_type == "Button" or (btn_type == "ButtonAndMenu" and len(input_val) == 1) ):
                                if ( len(input_val) > 1 ):
                                    log.info('Extra input not required')
                                    logger.print_on_console('Extra input not required')
                                elem.pressButton(btn_id)
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            else:
                                if ( len(input_val) == 2 ):
                                    menuItem = str(input_val[1]).strip()
                                    elem.PressContextButton(btn_id)
                                    elem.SelectContextMenuItemByText(menuItem)
                                    status = sap_constants.TEST_RESULT_PASS
                                    result = sap_constants.TEST_RESULT_TRUE
                                else:
                                    err_msg = sap_constants.INVALID_INPUT
                        else:
                            err_msg = 'Unable to press button / button does not exist'
                    else:
                        err_msg = 'Unsupported element type'
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND

        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in PressToolbarButton' )
        return status,result,value,err_msg

    def clickCell(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None

        value = OUTPUT_CONSTANT
        bList = []
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                d1,d2,imax,d3 = self.get_colCount(sap_id)
                if ( elem.type == 'GuiShell' ):
                    row = int(input_val[0])-1
                    index = int(input_val[1])-1
                    if ( elem.rowCount != 0 ):
                        #----------------------------------function to append columnorder
                        for i in range(0,imax):
                            b=elem.columnorder(i)
                            bList.append(b)
                        #----------------------------------function to append columnorder
                        if ( index >= 0 and row >= 0 ):
                            column = str(bList[index])
                            try:
                                elem.Click(row,column)
                            except:
                                elem.setCurrentCell(row,column)
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = 'Row and column values are incorrect'
                    else:
                        err_msg = 'Element has zero row count'
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in ClickCell' )
        return status,result,value,err_msg

    def setCellText(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_value = None
        value = OUTPUT_CONSTANT
        bList = []
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                d1, d2, imax, d3 = self.get_colCount(sap_id)
                if ( elem.type == 'GuiShell' ):
                    val = str(input_val[2])
                    row = int(input_val[0]) - 1
                    index = int(input_val[1]) - 1
                    if ( elem.rowCount != 0 ):
                        #----------------------------------function to append columnorder
                        for i in range(0,imax):
                            b = elem.columnorder(i)
                            bList.append(b)
                        #----------------------------------function to append columnorder
                        if ( index >= 0  and  row >= 0):
                            column = str(bList[index])
                            if ( elem.GetCellChangeable(row, column)) :
                                elem.ModifyCell(row, column,val)
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            else:
                                err_msg = 'Element is not changable'
                        else:
                            err_msg = 'Out of bounds exception'
                    else:
                        err_msg = 'Element has zero row count'
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in setCellText' )
        return status,result,value,err_msg

    def setShellText(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' ):
                    elem.text = input_val[0]
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console('Error occured in setShellText')
        return status, result, value, err_msg

    def doubleClickCell(self, sap_id, input_val,*args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        bList = []
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                d1,d2,imax,d3 = self.get_colCount(sap_id)
                if ( elem.type == 'GuiShell' ):
                    row = int(input_val[0]) - 1
                    index = int(input_val[1]) - 1
                    if ( elem.rowCount != 0 ):
                        #----------------------------------function to append columnorder
                        for i in range(0, imax):
                            b = elem.columnorder(i)
                            bList.append(b)
                        #----------------------------------function to append columnorder
                        if ( index >= 0 and row >= 0 ):
                            column = str(bList[index])
                            elem.DoubleClick(row,column)
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = 'Row and column values are incorrect'
                    else:
                        err_msg = 'Element has zero row count'
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in DoubleClickCell' )
        return status, result, value, err_msg

    def selectAllRows(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' and elem.SubType == 'GridView' ):
                    elem.SelectAll()
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in selectAllRows' )
        return status, result, value, err_msg

    def unselectAllSelections(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if (elem.type == 'GuiShell' and elem.SubType == 'GridView'):
                    elem.clearSelection()
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in unselectAllSelections' )
        return status, result, value, err_msg

    def scrollToRowNumber(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' and elem.SubType == 'GridView' ):
                    rowNum = int(input_val[0])
                    rowNum = rowNum - 1  # rowNum Starts From 0
                    if ( rowNum >= -1 ):
                        if ( rowNum == -1 or rowNum >= elem.rowCount ):  # end
                            end = elem.rowCount - elem.VisibleRowCount + 1
                            elem.FirstVisibleRow = end
                            value = end
                        else:
                            elem.FirstVisibleRow = rowNum
                            value = rowNum
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = 'Invalid input'
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in scrollToRowNumber' )
        return status, result, value, err_msg

    def getCellColor(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        bList = []
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' ):
                    if ( elem.rowCount != 0 ):
                        d1, d2, imax, d3 = self.get_colCount(sap_id)
                        row = int(input_val[0]) - 1
                        index = int(input_val[1]) - 1
                        if ( index >= 0 and row >= 0 ):
                            # ----------------------------------function to append columnorder
                            for i in range(0, imax):
                                b = elem.columnorder(i)
                                bList.append(b)
                            # ----------------------------------function to append columnorder
                            column = str(bList[index])
                            value = str(elem.getCellColor(row, column))
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = 'Invalid index'
                    else:
                        err_msg = 'Invalid row count'
                else:
                    err_msg = 'Element is not a shell object'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console('Error occured in getCellColor')
        return status, result, value, err_msg

    #TREE
    #---------------------------------------------------------------------------shell tree suppliment functions

    def tree_Type(self, elem):
        tree_type = None
        try:
            tree_type = elem.GetTreeType()
            if ( tree_type == 0 ):
                log.debug( 'Simple Tree' )
            elif ( tree_type == 1 ):
                log.debug( 'List Tree' )
            elif ( tree_type == 2 ):
                log.debug( 'Column Tree' )
        except Exception as e:
            log.error( e )
        return tree_type

    def treeTraverse(self, elem , input_val, column_data):
        treeType = self.tree_Type(elem)
        flag = False
        #-----------------------------------------------------------------------
        #-----------------------------------------------------------------------
        if ( not( column_data ) ):
            #list tree and simple
            cflag = True
            for i in range(0, len(input_val)):
                if ( i == 0 ):
                    node = elem.TopNode
                    try:
                        if ( input_val[i].isdigit() ):
                            count = int( input_val[i] )
                            c = self.getFirstLevelNodeCount(elem)
                            if ( count > c ):
                                cflag = False
                                break
                            try:
                                while ( count - 1 ):
                                    node = elem.GetNextNodeKey(node)
                                    count = count - 1
                            except:
                                pass
                        else:
                            try:
                                txt = self.getTextofNode(elem, node)
                                while txt.lower() != input_val[i].lower():
                                    node = elem.GetNextNodeKey(node)
                                    txt = self.getTextofNode(elem, node)
                            except:
                                pass
                    except:
                        pass
                else:
                    self.expandTree(elem, node)
                    child_nodes = elem.GetSubNodesCol(node)
                    try:
                        if ( input_val[i].isdigit() ):
                            count = int( input_val[i] )
                            if ( count > len(child_nodes) ):
                                cflag = False
                                break
                            try:
                                node = child_nodes[0]
                                while (count - 1):
                                    node = elem.GetNextNodeKey(node)
                                    count = count - 1
                            except:
                                pass
                        else:
                            try:
                                node = child_nodes[0]
                                txt = self.getTextofNode(elem, node)
                                while txt.lower() != input_val[i].lower():
                                    node = elem.GetNextNodeKey(node)
                                    txt = self.getTextofNode(elem, node)
                            except:
                                pass
                    except:
                        pass
            txt = self.getTextofNode(elem, node)
            if ( not ( input_val[len(input_val) - 1].isdigit() ) ):
                if ( txt.lower() == input_val[len(input_val) - 1].lower() ):
                    flag = True
            elif ( cflag ):
                flag = True
        #-----------------------------------------------------------------------
        #-----------------------------------------------------------------------
        elif ( column_data and treeType == 2 ):
            #column
            if ( column_data ):
                verifyColVal = ( len(column_data) >= 1 ) and ( elem.GetTreeType() == 2 )
                if ( verifyColVal ):
                    columnNames = elem.GetColumnNames()
                    titles = [elem.GetColumnTitleFromName(col) for col in columnNames if col]
                for i in range(0, len(input_val)):
                    # ----------------- Loop iteration initialization - Start -----------------------
                    nText = input_val[i]
                    colCheck = False
                    check = False
                    if ( verifyColVal and len(column_data[i]) == 2 ):  # @add Code for Case When Value is Missing
                        colCheck = True
                        col_count = len(titles)
                        col_no = column_data[i][0].strip()
                        if ( col_no.isdigit() ):
                            col_no = int(col_no)
                            if ( col_no > col_count ):
                                err_msg = "Tree Traverse : Column Number specified exceeds the number of columns present in the tree"
                                log.debug( err_msg )
                                log.error( err_msg )
                                return None
                            col_no = col_no - 1
                        else:
                            try:
                                col_no = titles.index(col_no)
                            except ValueError:
                                err_msg = 'Column not found'
                                logger.print_on_console( err_msg )
                                return None
                        col_val = column_data[i][1]
                    # Top Node - Either Inside a Parent or node without a Parent
                    if ( i == 0 ):
                        node = self.getFirstRootNode(elem)
                    else:
                        child_nodes = elem.GetSubNodesCol(node)
                        try:
                            node = child_nodes[0]
                        except Exception as e:
                            log.error( sap_constants.ERROR_MSG + ' : ' + str(e) )
                            log.debug( 'Tree Traverse : No further Children found' )
                            return None
                    self.expandTree(elem, node)
                    #----------------- Loop iteration initialization - End --------------------------
                # check, node, col_no, col_val, col_count, col_check, nText - initialized
                try:
                    if ( colCheck ):
                        columnText = elem.getItemText(node, elem.GetColumnNames()[col_no])
                        check = (columnText.lower() != col_val.lower())

                    if ( nText.isdigit() ):
                        # Part1 - When node index is provided
                        log.debug('Moving to node Number : ' + str(nText))
                        try:
                            for i in range(int(nText) - 1):
                                node = elem.GetNextNodeKey(node)
                        except Exception as e:
                            err_msg = 'Invalid index'
                            log.error( err_msg )
                            log.error( sap_constants.ERROR_MSG + ' : ' + str(e) )
                            logger.print_on_console( err_msg )
                            return None

                        if ( colCheck ):
                            columnText = elem.getItemText(node, elem.GetColumnNames()[col_no])
                            check = columnText.lower() != col_val.lower()
                    else:
                        # Part2 - When node text is provided
                        txt = self.getTextofNode(elem, node)
                        while txt.lower() != nText.lower() or check:
                            try:
                                node = elem.GetNextNodeKey(node)
                                txt = self.getTextofNode(elem, node)
                            except Exception as e:
                                """
                                    Exception will be raised when looping through current level is going on
                                    and the required node is not found so it is definetely a failed case.
                                """
                                err_msg = 'Node not found'
                                log.error( sap_constants.ERROR_MSG + ' : ' + str(e) )
                                log.debug( 'Node with Text = ' + nText + " not found" )
                                logger.print_on_console( err_msg )
                                return None
                            if ( colCheck ):
                                columnText = elem.getItemText(node, elem.GetColumnNames()[col_no])
                                check = (columnText.lower() != col_val.lower())
                        log.debug( 'Moving to node with text : ' + str(txt) )
                    self.expandTree(elem, node)
                except:  # @update code - as exceptions are already handled inside this try check if it is needed for unexpected exceptions or move exceptions that are handled
                    # inside here itself
                    pass
                 # Final Verification of Leaf Node
                txtCheck = True
                """
                   If Leaf Node is an index and node is found at that index then it is assumed that node is correct
                   and if Lead Node is a text then compare the text of the lead provided and actual text.
                """
                if ( not nText.isdigit() ):
                    txt = self.getTextofNode(elem, node)
                    txtCheck = txt.lower() == input_val[len(input_val) - 1].lower()
                if ( verifyColVal ):
                    if ( txtCheck and not check ):
                        flag = True
                    else:
                        flag = False
        #-----------------------------------------------------------------------
        if ( flag ):
            return node
        else:
            return None

    def getTextofNode(self, elem, node):
        txt = None
        if ( elem.GetTreeType() == 2 ):  # @add - add more conditions based on tree types
           cols = elem.GetColumnNames()
           for col in cols:
               txt = elem.GetItemText(node, col)
               if ( txt ):
                   return txt
        else:
            txt = elem.GetNodeTextByKey(node)
        return txt


    def getSelectedNodes(self, elem):
        nodes = []
        if ( elem.GetTreeType() == 2 ):  # @add - add more conditions based on tree types
            nodes = [elem.SelectedItemNode()]
        else:
            nodes = elem.GetSelectedNodes()
        return nodes

    def singleSelectNode(self, elem, node):
        if ( elem.GetTreeType() == 2 ):  # @add - add more conditions based on tree types
            elem.SelectItem(node, elem.GetColumnNames()[0])
        else:
            elem.SelectNode(node)
        return

    def getFirstLevelNodeCount(self, tree):
        c = 1
        n = self.getFirstRootNode(tree)
        while True:
            try:
                n = tree.GetNextNodeKey(n)
                c = c + 1
            except:
                break
        return c

    def expandTree(self, tree, node):
        if ( self.isFolder(tree, node) ):
            if ( tree.IsFolderExpanded(node) != True ):
                try:
                    tree.ExpandNode(node)
                except:
                    pass

    def isFolder(self, tree, node):
        return True if(tree.IsFolder(node) == True or tree.isFolderExpandable(node) == True or tree.GetNodeChildrenCount(node) > 0) else False

    def recursiveCollapseNode(self, tree, node):
        nodes = tree.GetSubNodesCol(node)
        if ( len(nodes) == 0 ):
            return
        for node in nodes:
            if ( self.isFolder(tree, node) and tree.isFolderExpanded(node) ):
                self.recursiveCollapseNode(tree, node)
                tree.CollapseNode(node)

    def getFirstRootNode(self, tree):
        root = tree.TopNode
        while True:
            try:
               parent = tree.GetParent(root)
               if ( parent ):
                   root = parent
               else:
                   break
            except:
                break
        while True:
            try:
                previous = tree.GetPreviousNodeKey(root)
                root = previous
            except:
                break
        return root

    def colData(self, column_data, len_input):
        newL = []
        if ( column_data ) :
            for i in range( 0, len_input - 1 ):
                newL.append([])
            newL.append(column_data)
        else:
            newL = None
        return newL

    #---------------------------------------------------------------------------shell tree suppliment functions
    #---------------------------------------------------------------------------shell tree keywords
    """Keywords : 1.verifyTreePath 2.selectTreeElement 3.getTreeNodeText 4.getTreeNodeCount 5.singleSelectParentOfSelected
    6.collapseTree 7.getColValueCorrToSelectedNode 8.selectTreeNode 9.getNodeNameByIndex """
    def verifyTreePath(self, sap_id, input_val, *args):
        """
            :param sap_id: Object Id of element
            :param input_val: Path to the Node from Top [A<str>; B<str>; C<str>]
            :param column_data: Array of Array containing Column information specific to node
            [['Column_Name<String>','Column_Value<String>'], [Column_Number<int>, Column_Value<String>]]
        """
        #-------------------to split input variables
        index = []
        column_data = None
        for i in range(0,len(input_val)):
            if ( input_val[i] == '<>' ):
                index.append(i)
        if ( index ):
            input_val = input_val[:index[0]]
            column_data = self.colData(input_val[index[0] + 1:],len(input_val))
        #-------------------to split input variables
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        node = None
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    node = self.treeTraverse(elem, input_val, column_data)
                    if ( node ):
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = "Verification Failed for the path specified in the Tree"
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
            logger.print_on_console( 'Error occured in VerifyTreePath' )
        return status, result, value, err_msg

    def selectTreeElement(self, sap_id, input_val, *args):
        '''
            :param sap_id: Object Id of SAP element
            :param input_val: Path From Root node to the desired Node. for example - [A,B,C]
            :param column_data: Array of Array containing Column information specific to node
            [['Column_Name<String>','Column_Value<String>'], [Column_Number<int>, Column_Value<String>]]
            :param isDoubleClick: 0 or 1 Indicating whether to double click or not
            :param item: item in Node (row) to double click
            :param args:
        '''
        #-------------------to split input variables
        isDoubleClick=0
        item=None
        column_data = None
        index=[]
        for i in range(0,len(input_val)):
            if ( input_val[i] == '<>' ):
                index.append(i)
        if ( index ):
            if ( len(index) == 1 ):
                input_val = input_val[:index[0]]
                column_data = self.colData(input_val[index[0] + 1:],len(input_val))
            elif ( len(index) == 2 ):
                isDoubleClick = input_val[index[1]+1:][0]
                input_val = input_val[:index[0]]
                column_data = self.colData(input_val[index[0] + 1:index[1]],len(input_val))
            elif ( len(index) == 3 ):
                item = input_val[index[2]+1:][0]
                isDoubleClick = input_val[index[1]+1:index[2]][0]
                input_val = input_val[:index[0]]
                column_data = self.colData(input_val[index[0] + 1:index[1]],len(input_val))
        #-------------------to split input variables

        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        node = None
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                elem.UnselectAll()
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    node = self.treeTraverse(elem, input_val, column_data)
                    if ( node ):
                        isDoubleClick = int( isDoubleClick )
                        if ( item ):  # Selection When Item is there
                            check = False
                            if ( item.isdigit() ):  # Item is Column Number or Item Index
                                # @add Code - Add Condition of selecting last item when item_no is 0
                                item = int(item)
                                if ( item > 0 ):
                                    tree_type = elem.GetTreeType()
                                    item_id = None
                                    if ( tree_type == 1 ):  # List Tree
                                        log.debug('Operation on item in list at index : ' + str(item))
                                        item_count = elem.GetListTreeNodeItemCount(node)
                                        item_id = item
                                    elif ( tree_type == 2 ):  # Column Tree
                                        columns = elem.GetColumnNames()
                                        item_count = len(columns)
                                        item_id = columns[item - 1]
                                        log.debug('Operation on item at column index : ' + str(item))
                                    check = (item <= item_count)
                                else:
                                    err_msg = 'Invalid Item'
                                    log.debug( err_msg )
                            else:  # Item is Column Name
                                # To get Item ID when item is not a digit but column name
                                columns = elem.GetColumnNames()
                                column_titles = [elem.GetColumnTitleFromName(col) for col in columns]
                                try:
                                    item_id = columns[column_titles.index(item)]
                                    check = True
                                    logger.debug( 'Operation on item with column name : ' + str(item) )
                                except ValueError:
                                    err_msg = 'Column not found'
                                    log.debug( err_msg )
                            if ( check ):
                                if elem.GetItemType(node, item_id) == 5:
                                    elem.clickLink(node, item_id)
                                else:
                                    elem.DoubleClickItem(node, item_id)
                                elem.SelectItem(node, item_id)
                            else:
                                err_msg = 'Invalid item'
                                log.debug( err_msg )
                        else:
                            # SomeNodes with GetItemType = 2 does not work for Double Click But With SelectedNode
                            # Selection and Double Click Both Operation so as to Select and DoubleClick in cases where Double Click Works and where selected Work
                            elem.SelectNode(node)
                            if ( isDoubleClick ):
                                elem.DoubleClickNode(node)
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = sap_constants.INVALID_INPUT
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in SelectTreeElement' )
        return status, result, value, err_msg

    def getTreeNodeText(self, sap_id, input_val, *args):
        '''
            :param sap_id: Object Id of SAP element
            :param input_val: Path From Root node to the desired Node. for example - [A,B,C]
            :param column_data: Array of Array containing Column information specific to node
            [['Column_Name<String>','Column_Value<String>'], [Column_Number<int>, Column_Value<String>]]
            :param item: item in Node (row) to double click
            :param args:
        '''
        #-------------------to split input variables
        item = None
        column_data = None
        index = []
        for i in range( 0,len(input_val) ):
            if ( input_val[i] == '<>' ):
                index.append(i)
        if ( index ):
            if ( len(index) == 1 ):
                input_val = input_val[:index[0]]
                column_data = self.colData(input_val[index[0] + 1:],len(input_val))
            elif ( len(index) == 2 ):
                item = input_val[index[1]+1:][0]
                input_val = input_val[:index[0]]
                column_data = self.colData(input_val[index[0] + 1:index[1]],len(input_val))
        #-------------------to split input variables
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        node = None
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                elem.UnselectAll()
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    node = self.treeTraverse(elem, input_val, column_data)
                    if ( node ):
                        if ( item ):  # Selection When Item is there
                            check = False
                            if ( item.isdigit() ):  # Item is Column Number or Item Index
                                # @add Code - Add Condition of selecting last item when item_no is 0
                                item = int(item)
                                if ( item > 0 ):
                                    tree_type = elem.GetTreeType()
                                    item_id = None
                                    if ( tree_type == 1 ):  # List Tree
                                        log.debug( 'Operation on item in list at index : ' + str(item) )
                                        item_count = elem.GetListTreeNodeItemCount(node)
                                        item_id = item
                                    elif ( tree_type == 2 ):  # Column Tree
                                        columns = elem.GetColumnNames()
                                        item_count = len(columns)
                                        item_id = columns[item - 1]
                                        log.debug('Operation on item at column index : ' + str(item))
                                    check = (item <= item_count)
                                else:
                                    err_msg = 'Invalid item'
                                    log.debug( err_msg )
                            else:  # Item is Column Name
                                # To get Item ID when item is not a digit but column name
                                columns = elem.GetColumnNames()
                                column_titles = [elem.GetColumnTitleFromName(col) for col in columns]
                                try:
                                    item_id = columns[column_titles.index(item)]
                                    check = True
                                    log.debug('Operation on item with column name : ' + str(item))
                                except ValueError:
                                    err_msg = 'Column not found'
                                    log.debug( err_msg )
                            if ( check ):
                                value = elem.GetItemText(node, item_id)
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            else:
                                err_msg = 'Invalid item'
                                log.debug( err_msg )
                        else:
                            value = self.getTextofNode(elem, node)
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = sap_constants.INVALID_INPUT
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in GetTreeNodeText' )
        return status, result, value, err_msg

    def getTreeNodeCount(self, sap_id, input_val, *args):
        '''
                   :param sap_id: Object Id of SAP element
                   :param input_val: Path From Root node to the desired Node. for example - [A,B,C]
                   :param column_data: Array of Array containing Column information specific to node
                   [['Column_Name<String>','Column_Value<String>'], [Column_Number<int>, Column_Value<String>]]
                   :param item: item in Node (row) to double click
                   :param args:
               '''
        #-------------------to split input variables
        index = []
        column_data = None
        for i in range( 0,len(input_val) ):
            if ( input_val[i] == '<>' ):
                index.append(i)
        if ( index ):
            input_val = input_val[:index[0]]
            column_data = self.colData(input_val[index[0] + 1:],len(input_val))
        #-------------------to split input variables
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        node = None
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                elem.UnselectAll()
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    if ( not( input_val[0] ) ):
                        value = self.getFirstLevelNodeCount(elem)
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        node = self.treeTraverse(elem, input_val, column_data)
                        if ( node ):
                            if ( self.isFolder(elem, node) ):
                                self.expandTree(elem,node)
                                child_nodes = elem.GetSubNodesCol(node)
                                value = len(child_nodes)
                            else:
                                value = 0
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = sap_constants.INVALID_INPUT
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in GetTreeNodeCount' )
        return status, result, value, err_msg

    def singleSelectParentOfSelected(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    nodes = self.getSelectedNodes(elem)
                    if ( nodes is not None ):
                        if ( len(nodes) == 1 ):
                            try:
                                parent = elem.GetParent(nodes[0])
                                self.singleSelectNode(elem, parent)
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            except Exception as e:
                                log.error(e)
                                err_msg = 'Parent not found'
                        else:
                            err_msg = 'Multiple selection not allowed'
                    else:
                        err_msg = 'Rows not found'
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in singleSelectParentOfSelected' )
        return status, result, value, err_msg

    def collapseTree(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    count = self.getFirstLevelNodeCount(elem)
                    for index in range(count):
                        if ( index == 0 ):
                            n = self.getFirstRootNode(elem)
                        else:
                            n = elem.GetNextNodeKey(n)
                        if ( self.isFolder(elem, n) and elem.isFolderExpanded(n) ):
                            log.debug( "Recursively Collapsing Parent Node at index - "+str(index) )
                            self.recursiveCollapseNode(elem, n)
                            elem.CollapseNode(n)
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in CollapseTree' )
        return status, result, value, err_msg

    def getColValueCorrToSelectedNode(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    if ( elem.GetTreeType() == 2 ):
                        node = elem.SelectedItemNode()
                        if ( node ):
                            try:
                                colNumber = int(input_val[0])
                                columns = elem.GetColumnNames()
                                if ( colNumber <= len(columns) ):
                                    colNumber = colNumber - 1
                                    value = elem.GetItemText(node, columns[colNumber])
                                    status = sap_constants.TEST_RESULT_PASS
                                    result = sap_constants.TEST_RESULT_TRUE
                                    log.debug( 'Get Column Text From Selected Column => Value is: ' + str(value) )
                                else:
                                    err_msg = 'Col Index Out of Range'
                            except Exception as e:
                                log.error(e)
                                err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
                        else:
                            err_msg = 'No Item Selected'
                    else:
                        err_msg = 'Not a Column Tree'
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in GetColValueCorrToSelectedNode' )
        return status, result, value, err_msg

    def selectTreeNode(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        node = None
        in_flag = False
        additional_data = None
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                elem.UnselectAll()
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    node = self.treeTraverse(elem, input_val, additional_data)
                    if ( node ):
                        # Some Nodes with GetItemType = 2 does not work for Double Click But With SelectedNode
                        # Selection and Double Click Both Operation so as to Select and DoubleClick in cases where DoubleClickNode works so will SelectedNode
                        try:
                            elem.SelectNode(node)
                            elem.DoubleClickNode(node)
                            in_flag = True
                        except:
                            elem.DoubleClickNode(node)
                            in_flag = True
                        if ( in_flag == True ):
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = sap_constants.INVALID_INPUT
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in SelectTreeNode' )
        return status,result,value,err_msg

    def getNodeNameByIndex(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        node = None
        flag = True
        try:
            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    for i in range(0,len(input_val)):
                        count = int(input_val[i])
                        if ( i == 0 ):
                            node = elem.TopNode
                            c = self.getFirstLevelNodeCount(elem)
                            if ( count > c ):
                                flag = False
                                break
                            try:
                                while ( count - 1 ):
                                    node = elem.GetNextNodeKey(node)
                                    count = count - 1
                            except:
                                pass
                        else:
                            self.expandTree(elem,node)
                            child_nodes = elem.GetSubNodesCol(node)
                            if ( count > len(child_nodes) ):
                                flag = False
                                break
                            try:
                                node = child_nodes[0]
                                while (count - 1):
                                    node = elem.GetNextNodeKey(node)
                                    count = count - 1
                            except Exception as e:
                                pass
                    if ( flag ):
                        value = elem.GetNodeTextByKey(node)
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = sap_constants.INVALID_INPUT
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in GetNodeNameByIndex' )
        return status, result, value, err_msg