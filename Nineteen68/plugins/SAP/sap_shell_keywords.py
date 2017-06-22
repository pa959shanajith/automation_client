#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:      Handling SAP-Shell elements
#
# Author:      anas.ahmed1
#
# Created:     15-06-2017
# Copyright:   (c) anas.ahmed1 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sap_constants
from constants import *
import logger
import time
from saputil_operations import SapUtilKeywords
from launch_keywords import Launch_Keywords

class Shell_Keywords():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk =Launch_Keywords()

    def get_children(self, sap_id,url,input_val, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        pos=input_val[0]
        print'pos is ============',pos
        elem = ses.FindById(id)
        try:
            if(id != None):
                    if(elem.type == 'GuiShell'):
                        try:
                            print'object is ==========================shell'
                            print 'name is ===========================',elem.Text
                            print 'width is ==========================',elem.Width
                            print 'height is =========================',elem.Height
                            print 'row is =========================',elem.rowCount
                            print 'col is =========================',elem.columnCount
                            #elem.selectedColumns="2"
                            print 'val is =========================',elem.pressButton(" Details ")
                            print 'val is =========================',elem.getCellValue
                            try:
                                print'========================================,',ses.SelectContextMenuItem
                                print"strp1------------------"
                                elem.SelectContextMenuItemByPosition(pos).Text
                                print '======================================'
                                ses.SelectContextMenuItemByPosition(pos).Text
                                print'step2========================'
                                ses.SelectContextMenuItemByPosition(pos).Text
                                print'step3========================'
                            except Exception as e:
                                print '================',e
                        except Exception as e:
                            print 'error is ===========================',e
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                        value=ses.FindById(id).text

                    else:
                        logger.print_on_console('Element state does not allow to perform the operation')
                        err_msg = sap_constants.ERROR_MSG
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
                  err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            Exceptions.error(e)
            logger.print_on_console('Error occured in getText and is a :',e)
        return status,result,value,err_msg

    def get_rowCount(self, sap_id,*args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        elem = ses.FindById(id)
        try:
            if(id != None):
                if(elem.type == 'GuiShell'):
                    value=elem.rowCount
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Element is not a shell object')
                    err_msg = sap_constants.ERROR_MSG
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
                  err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            Exceptions.error(e)
            logger.print_on_console('Error occured in GETROWCOUNT and is a :',e)
        return status,result,value,err_msg

    def get_colCount(self, sap_id,*args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        elem = ses.FindById(id)
        try:
            if(id != None):
                if(elem.type == 'GuiShell'):
                    value=elem.columnCount
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Element is not a shell object')
                    err_msg = sap_constants.ERROR_MSG
            else:
                  logger.print_on_console('element not present on the page where operation is trying to be performed')
                  err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            Exceptions.error(e)
            logger.print_on_console('Error occured in GETCOLUMNCOUNT and is a :',e)
        return status,result,value,err_msg

    def selectRows(self, sap_id,url,input_val,*args):
            self.lk.setWindowToForeground(sap_id)
            id,ses=self.uk.getSapElement(sap_id)
            status=sap_constants.TEST_RESULT_FAIL
            result=sap_constants.TEST_RESULT_FALSE
            err_msg=None
            rowpos=input_val[0]
            value=OUTPUT_CONSTANT
            elem = ses.FindById(id)
            try:
                if(id != None):
                    if(elem.type == 'GuiShell'):
                        if elem.rowCount!=0:
                            elem.selectedRows=rowpos
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Element is not a shell object')
                        err_msg = sap_constants.ERROR_MSG
                else:
                      logger.print_on_console('element not present on the page where operation is trying to be performed')
                      err_msg = sap_constants.ERROR_MSG
            except Exception as e:
                err_msg = sap_constants.ERROR_MSG
                Exceptions.error(e)
                logger.print_on_console('Error occured in SELECTROWS and is a :',e)
                import traceback
                traceback.print_exc()
            return status,result,value,err_msg

    def readGridCells(self, sap_id,url,input_val,*args):
            self.lk.setWindowToForeground(sap_id)
            id,ses=self.uk.getSapElement(sap_id)
            status=sap_constants.TEST_RESULT_FAIL
            result=sap_constants.TEST_RESULT_FALSE
            err_msg=None
            text=input_val[0]
            value=OUTPUT_CONSTANT
            elem = ses.FindById(id)
            try:
                if(id != None):
                    if(elem.type == 'GuiShell'):
                        if elem.rowCount!=0:
                            for i in range(0,elem.rowCount):
                                for j in range(0,elem.columnCount):
                                    try:
                                        #grid=elem.getCellValue(str(i),str(j))
                                        grid=elem.GetCellValue(i, j).text
                                    except Exception as e:
                                        import traceback
                                        traceback.print_exc()
                                    if text in grid:
                                        elem.selectedRows=str(i)
                                        status = sap_constants.TEST_RESULT_PASS
                                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Element is not a shell object')
                        err_msg = sap_constants.ERROR_MSG
                else:
                      logger.print_on_console('element not present on the page where operation is trying to be performed')
                      err_msg = sap_constants.ERROR_MSG
            except Exception as e:
                err_msg = sap_constants.ERROR_MSG
                Exceptions.error(e)
                logger.print_on_console('Error occured in readGridCells and is a :',e)
                import traceback
                traceback.print_exc()
            return status,result,value,err_msg

    def toolBarActionKeys(self, sap_id,url,input_val,*args):
            self.lk.setWindowToForeground(sap_id)
            id,ses=self.uk.getSapElement(sap_id)
            status=sap_constants.TEST_RESULT_FAIL
            result=sap_constants.TEST_RESULT_FALSE
            err_msg=None
            action=input_val[0]
            value=OUTPUT_CONSTANT
            elem = ses.FindById(id)
            try:
                if(id != None):
                    if(elem.type == 'GuiShell'):
                        if elem.rowCount!=0:
                            try:
                                elem.pressButton(unicode(action,"utf-8"))
                            except Exception as e :
                                print e
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Element is not a shell object')
                        err_msg = sap_constants.ERROR_MSG
                else:
                      logger.print_on_console('element not present on the page where operation is trying to be performed')
                      err_msg = sap_constants.ERROR_MSG
            except Exception as e:
                err_msg = sap_constants.ERROR_MSG
                Exceptions.error(e)
                logger.print_on_console('Error occured in SELECTROWS and is a :',e)
                import traceback
                traceback.print_exc()
            return status,result,value,err_msg

    def getCellText(self, sap_id,url,input_val,*args):
            self.lk.setWindowToForeground(sap_id)
            id,ses=self.uk.getSapElement(sap_id)
            status=sap_constants.TEST_RESULT_FAIL
            result=sap_constants.TEST_RESULT_FALSE
            err_msg=None
            r_int=long(input_val[0])
            i_int=int(input_val[1])
            row=r_int-1
            index=i_int-1
            value=OUTPUT_CONSTANT
            elem = ses.FindById(id)
            d1,d2,imax,d3=self.get_colCount(sap_id)
            bList=[]
            try:
                if(id != None):
                    if(elem.type == 'GuiShell'):
                        if elem.rowCount!=0:
                            #----------------------------------function to append columnorder
                            for i in range(0,imax-1):
                                        b=elem.columnorder(i)
                                        bList.append(b)
                            #----------------------------------function to append columnorder
                            if index>=0 and row >=0:
                                column=str(bList[index])
                                value=elem.getCellValue(row,column)
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            else:
                                logger.print_on_console('Row and column values are incorrect')
                                err_msg = sap_constants.ERROR_MSG

                    else:
                        logger.print_on_console('Element is not a shell object')
                        err_msg = sap_constants.ERROR_MSG
                else:
                      logger.print_on_console('element not present on the page where operation is trying to be performed')
                      err_msg = sap_constants.ERROR_MSG
            except Exception as e:
                err_msg = sap_constants.ERROR_MSG
                Exceptions.error(e)
                logger.print_on_console('Error occured in GetCellText and is a :',e)
                import traceback
                traceback.print_exc()
            return status,result,value,err_msg