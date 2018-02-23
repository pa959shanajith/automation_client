#-------------------------------------------------------------------------------
# Name:         SAP_Shell_keywords
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
from sap_launch_keywords import Launch_Keywords
import logging
global nodeList
log = logging.getLogger("sap_shell_keywords.py")

class Shell_Keywords():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk =Launch_Keywords()
        self.nodeList=[]

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
            log.error(e)
            logger.print_on_console('Error occured in GETROWCOUNT')
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
            log.error(e)
            logger.print_on_console('Error occured in GETCOLUMNCOUNT')
        return status,result,value,err_msg

    def selectRows(self, sap_id,input_val,*args):
            self.lk.setWindowToForeground(sap_id)
            id,ses=self.uk.getSapElement(sap_id)
            status=sap_constants.TEST_RESULT_FAIL
            result=sap_constants.TEST_RESULT_FALSE
            err_msg=None
            row=[]
            #-------to handle multiple inputs
            if len(input_val)>1:
               for i in range(0,len(input_val)):
                    rows =int(input_val[i])-1
                    row.append(rows)
               rowpos= ','.join(map(str,row))
            else:
                row=int(input_val[0])-1
                rowpos=str(row)
            #-------to handle multiple inputs
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
                log.error(e)
                logger.print_on_console('Error occured in SELECTROWS')
            return status,result,value,err_msg

    def toolBarActionKeys(self, sap_id,input_val,*args):
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
                log.error(e)
                logger.print_on_console('Error occured in ToolbarActionKeys')
            return status,result,value,err_msg

    def getCellText(self, sap_id,input_val,*args):
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
                            for i in range(0,imax):
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
                log.error(e)
                logger.print_on_console('Error occured in GetCellText')
            return status,result,value,err_msg

    def pressToolBarButton(self, sap_id,input_val,*args):
            self.lk.setWindowToForeground(sap_id)
            id,ses=self.uk.getSapElement(sap_id)
            status=sap_constants.TEST_RESULT_FAIL
            result=sap_constants.TEST_RESULT_FALSE
            err_msg=None
            text=input_val[0]
            value=OUTPUT_CONSTANT
            elem = ses.FindById(id)
            try:
                rowcount = elem.rowCount
                ele_type = "GuiGridControl"
            except Exception as e:
                ele_type = "GuiToolbarControl"
            try:
                if(id != None):
                    if(elem.type == 'GuiShell'):
                        if(ele_type == "GuiGridControl"):
                            try:
                                #-------------------------------store the tooltips of the grid buttons
                                if elem.rowCount!=0:
                                    lim=elem.ToolbarButtonCount
                                    for x in range (0,lim):
                                         a=elem.GetToolbarButtonTooltip(x)
                                         if text.strip().lower()==str(a).strip().lower():
                                            elmID=elem.GetToolbarButtonId(x)
                                            if((elem.GetToolbarButtonType(x) == "Menu" or "ButtonAndMenu") and len(input_val)>1):
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
                        elif(ele_type == "GuiToolbarControl"):
                            count = elem.ButtonCount
                            btn_id = None
                            for i in range(0,count):
                                if(elem.GetButtonTooltip(i).lower() == text.strip().lower()):
                                    btn_id = elem.GetButtonId(i)
                                    btn_type = elem.GetButtonType(i)
                                    break
                            if(btn_id != None):
                                if(btn_type == "Button"):
                                    if(len(input_val)>1):
                                        logger.print_on_console('Extra input not required')
                                    elem.pressButton(btn_id)
                                else:
                                    menuItem = str(input_val[1]).strip()
                                    elem.PressContextButton(btn_id)
                                    elem.SelectContextMenuItemByText(menuItem)
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            else:
                                logger.print_on_console('Unable to press button / button does not exist')
                                err_msg = sap_constants.ERROR_MSG
                    else:
                        logger.print_on_console('Element is not a shell object')
                        err_msg = sap_constants.ERROR_MSG
                else:
                      logger.print_on_console('element not present on the page where operation is trying to be performed')
                      err_msg = sap_constants.ERROR_MSG
            except Exception as e:
                err_msg = sap_constants.ERROR_MSG
                log.error(e)
                logger.print_on_console('Error occured in PressToolbarButton')
            return status,result,value,err_msg

    def clickCell(self, sap_id,input_val,*args):
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
                            for i in range(0,imax):
                                b=elem.columnorder(i)
                                bList.append(b)
                            #----------------------------------function to append columnorder
                            if index>=0 and row >=0:
                                column=str(bList[index])
                                try:
                                    elem.Click(row,column)
                                except:
                                    elem.setCurrentCell(row,column)
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
                log.error(e)
                logger.print_on_console('Error occured in ClickCell')
            return status,result,value,err_msg

    def doubleClickCell(self, sap_id,input_val,*args):
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
                            for i in range(0,imax):
                                b=elem.columnorder(i)
                                bList.append(b)
                            #----------------------------------function to append columnorder
                            if index>=0 and row >=0:
                                column=str(bList[index])
                                elem.DoubleClick(row,column)
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
                log.error(e)
                logger.print_on_console('Error occured in DoubleClickCell')
            return status,result,value,err_msg

    def selectTreeNode(self, sap_id,input_val,*args):
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        elem = ses.FindById(id)
        node = ''
        try:
            if(id != None):
                if(elem.type == 'GuiShell' and elem.SubType == 'Tree'):
                    for i in range(0,len(input_val)):
                        if(i==0):
                            node = elem.TopNode
                            try:
                                while (elem.GetNodeTextByKey(node)).lower() != input_val[i].lower():
                                    node = elem.GetNextNodeKey(node)
                            except:
                                pass
                            self.expandTree(elem,node)
                        else:
                            child_nodes = elem.GetSubNodesCol(node)
                            j = 0
                            try:
                                node = child_nodes[j]
                                while (elem.GetNodeTextByKey(child_nodes[j])).lower() != input_val[i].lower():
                                    node = elem.GetNextNodeKey(child_nodes[j])
                                    j = j + 1
                            except:
                                pass
                            self.expandTree(elem,node)
                    if(elem.GetNodeTextByKey(node) == input_val[len(input_val)-1]):
                        elem.DoubleClickNode(node)
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Invalid input')
                        err_msg = sap_constants.ERROR_MSG
                else:
                    logger.print_on_console('Element is not a tree object')
                    err_msg = sap_constants.ERROR_MSG
            else:
                logger.print_on_console('Element not present on the page where operation is trying to be performed')
                err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            log.error(e)
            logger.print_on_console('Error occured in SelectTreeNode')
        self.colapseTree(elem)
        return status,result,value,err_msg

    def getNodeNameByIndex(self,sap_id,input_val,*args):
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        elem = ses.FindById(id)
        node = ''
        flag = True
        try:
            if(id != None):
                if(elem.type == 'GuiShell' and elem.SubType == 'Tree'):
                    for i in range(0,len(input_val)):
                        count = int(input_val[i])
                        if(i==0):
                            node = elem.TopNode
                            c = self.getFirstLevelNodeCount(elem)
                            if(count>c):
                                flag = False
                                break
                            try:
                                while (count-1):
                                    node = elem.GetNextNodeKey(node)
                                    count = count - 1
                            except:
                                pass
                            self.expandTree(elem,node)
                        else:
                            child_nodes = elem.GetSubNodesCol(node)
                            if(count>len(child_nodes)):
                                flag = False
                                break
                            j = 0
                            try:
                                node = child_nodes[j]
                                while (count-1):
                                    node = elem.GetNextNodeKey(child_nodes[j])
                                    count = count - 1
                                    j = j + 1
                            except Exception as e:
                                pass
                            self.expandTree(elem,node)
                    if(flag):
                        value = elem.GetNodeTextByKey(node)
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Invalid input')
                        err_msg = sap_constants.ERROR_MSG
                else:
                    logger.print_on_console('Element is not a tree object')
                    err_msg = sap_constants.ERROR_MSG
            else:
                logger.print_on_console('Element not present on the page where operation is trying to be performed')
                err_msg = sap_constants.ERROR_MSG
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            log.error(e)
            logger.print_on_console('Error occured in GetNodeNameByIndex')
        self.colapseTree(elem)
        return status,result,value,err_msg


    def getFirstLevelNodeCount(self, tree):
        c = 1
        n = tree.TopNode
        while True:
            try:
                n = tree.GetNextNodeKey(n)
                c = c + 1
            except:
                break
        return c

    def expandTree(self,tree,node):
        if tree.IsFolder(node)==True:
            if tree.IsFolderExpandable(node)==True:
                if tree.IsFolderExpanded(node)!=True:
                    try:
                        tree.ExpandNode(node)
                        self.nodeList.append(node)
                    except:
                        pass

    def colapseTree(self,tree):
        try:
            for i in self.nodeList:
                tree.CollapseNode(i)
        except:
            import traceback
            traceback.print_exc()