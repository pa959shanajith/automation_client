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
                if ( elem.type == 'GuiShell' and elem.SubType == 'GridView' ):# check for shell gridview
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
                elif ( elem.type == 'GuiShell' and elem.SubType == 'Toolbar' ): # check for shell Toolbar
                    count = elem.ButtonCount
                    btn_id = None
                    btn_type = None
                    #---------------------------info for buttons
                    info_list=[]
                    for i in range(0,count):
                        info_list.append(elem.GetButtonTooltip(i).lower().strip())
                    log.info("Toolbar(shell) Buttons avaliable are : "+str(info_list))
                    del info_list
                    #---------------------------info for buttons
                    for i in range(0,count):
                        if ( elem.GetButtonTooltip(i).lower().strip() == str(input_val[0]).strip().lower() ):
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
                            if ( len(input_val) >= 2 ):
                                elem.PressContextButton(btn_id)
##                                self.menuItem_list=input_val[1:]
##                                self.count = 0
##                                def recq_call(elem, menuItem):
##                                    print('1', elem, menuItem)
##                                    try:
##                                        print(elem.CurrentContextMenu())
##                                    except:
##                                        pass
##                                    temp_elem = elem.SelectContextMenuItemByText(menuItem)
##                                    self.count = self.count + 1
##                                    print(count)
##                                    print(len(self.menuItem_list))
##                                    if count == len(self.menuItem_list):
##                                        return
##                                    else:
##                                        recq_call(temp_elem,self.menuItem_list[self.count])
##                                recq_call(elem,self.menuItem_list[self.count])
                                menuItem = str(input_val[1]).strip()
##                                elem.PressContextButton(btn_id)
                                elem.SelectContextMenuItemByText(menuItem)
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            else:
                                err_msg = sap_constants.INVALID_INPUT
                    else:
                        err_msg = 'Unable to press button / button does not exist'
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