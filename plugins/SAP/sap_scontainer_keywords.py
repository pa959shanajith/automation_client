#-------------------------------------------------------------------------------
# Name:       sap_scontainer_keywords
# Purpose:    Module for textbox keywords
#
#Author:      anas.ahmed1
#
# Created:     06-05-2020
# Copyright:   (c) anas.ahmed 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sap_constants
from constants import *
import logger
from encryption_utility import AESCipher
from saputil_operations import SapUtilKeywords
from sap_launch_keywords import Launch_Keywords
import sap_highlight
import pywinauto
import logging
log = logging.getLogger('sap_scontainer_keywords.py')

class SContainer_Keywords():

    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()
        self.tableType = None

    def getRowCount(self, sap_id, *args):
        """
        This function returns the total number of rows for the simple container
        Input : N/A
        Output : Number of rows
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                #elem = ses.FindById(id)
                if ( ses.FindById(id).type == 'GuiSimpleContainer' ):
                    """check if elem is steploop"""
                    if( ses.FindById(id).IsStepLoop == True ):
                        log.info("Element is a Step Loop")
                        value = ses.FindById(id).LoopRowCount
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        log.info("Element is Not a Step Loop")
                        table = self.createCustomTable(ses.FindById(id))
                        value=len(table)
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
            logger.print_on_console( 'Error occured in getRowCount' )
        return status, result, value, err_msg

    def getColCount(self, sap_id, *args):
        """
        This function returns the total number of columns for the simple container
        Input : N/A
        Output : Number of columns
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( ses.FindById(id).type == 'GuiSimpleContainer' ):
                    """check if elem is steploop"""
                    if( ses.FindById(id).IsStepLoop == True ):
                        log.info("Element is a Step Loop")
                        value = ses.FindById(id).LoopColCount
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        log.info("Element is Not a Step Loop")
                        table = self.createCustomTable(ses.FindById(id))
                        value=len(table[0])
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
            logger.print_on_console( 'Error occured in getColCount' )
        return status, result, value, err_msg

    def getTypeOfCell(self, sap_id, input_val, *args):
        """
        This function returns the GUI type of the cell of the simple container
        Input : Row;Column
        Output : GUI Type
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                row = int(input_val[0])-1
                col = int(input_val[1])-1
                if ( ses.FindById(id).type == 'GuiSimpleContainer' ):
                    elem = self.getElementFromCell(self.createCustomTable(ses.FindById(id)),row,col)
                    value = elem.Type
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                    pass
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except ValueError as v:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(v)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in getTextOfCell : Invalid Row or Column number' )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in getTextOfCell' )
        return status, result, value, err_msg

    def getTextOfCell(self, sap_id, input_val, *args):
        """
        This function returns the cell Text of the simple container
        Input : Row;Column
        Output : Text
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                row = int(input_val[0])-1
                col = int(input_val[1])-1
                if ( ses.FindById(id).type == 'GuiSimpleContainer' ):
                    elem = self.getElementFromCell(self.createCustomTable(ses.FindById(id)),row,col)
                    value = elem.Text
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                    pass
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except ValueError as v:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(v)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in getTextOfCell : Invalid Row or Column number' )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in getTextOfCell' )
        return status, result, value, err_msg

    def verifyTextOfCell(self, sap_id, input_val, *args):
        """
        This function returns boolean value(True/False) based on the verification of text  the simple-container cell against the input
        Input : Row;Column;Input Text;Selective(optional)
        Output : Boolean Value
        Note: passing selective as the 4th variable will resulting in partial verification
        (i.e. it will match the input text with a part of the cell text)
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                row = int(input_val[0])-1
                col = int(input_val[1])-1
                if ( ses.FindById(id).type == 'GuiSimpleContainer' ):
                    elem = self.getElementFromCell(self.createCustomTable(ses.FindById(id)),row,col)
                    if ( elem.Text == input_val[2] ):
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    if(len(input_val)==4 and input_val[3].lower()=='selective'):
                        if (str(input_val[2]) in elem.Text):
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except ValueError as v:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(v)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in verifyTextOfCell : Invalid Row or Column number' )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in verifyTextOfCell' )
        return status, result, value, err_msg

    def clickOnCell(self, sap_id, input_val, *args):
        """
        This function returns boolean value, performs a mouse-click on the simple-container cell
        Input : Row;Column
        Output : Boolean Value
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                row = int(input_val[0])-1
                col = int(input_val[1])-1
                if ( ses.FindById(id).type == 'GuiSimpleContainer' ):
                    elem = self.getElementFromCell(self.createCustomTable(ses.FindById(id)),row,col)
                    left =  elem.__getattr__("ScreenLeft")
                    width = elem.__getattr__("Width")
                    x = left + width/2
                    top =  elem.__getattr__("ScreenTop")
                    height = elem.__getattr__("Height")
                    y = top + height/2
                    pywinauto.mouse.click(button = 'left', coords = (int(x), int(y)))
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except ValueError as v:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(v)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in clickOnCell : Invalid Row or Column number' )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in clickOnCell' )
        return status, result, value, err_msg

    def doubleClickOnCell(self, sap_id, input_val, *args):
        """
        This function returns boolean value, performs a mouse-double click on the simple-container cell
        Input : Row;Column
        Output : Boolean Value
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                row = int(input_val[0])-1
                col = int(input_val[1])-1
                if ( ses.FindById(id).type == 'GuiSimpleContainer' ):
                    elem = self.getElementFromCell(self.createCustomTable(ses.FindById(id)),row,col)
                    left =  elem.__getattr__("ScreenLeft")
                    width = elem.__getattr__("Width")
                    x = left + width/2
                    top =  elem.__getattr__("ScreenTop")
                    height = elem.__getattr__("Height")
                    y = top + height/2
                    pywinauto.mouse.double_click(button = 'left', coords = (int(x), int(y)))
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except ValueError as v:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(v)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in doubleClickOnCell : Invalid Row or Column number' )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in doubleClickOnCell' )
        return status, result, value, err_msg

    def rightClickOnCell(self, sap_id, input_val, *args):
        """
        This function returns boolean value, performs a mouse-right click on the simple-container cell
        Input : Row;Column
        Output : Boolean Value
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                row = int(input_val[0])-1
                col = int(input_val[1])-1
                if ( ses.FindById(id).type == 'GuiSimpleContainer' ):
                    elem = self.getElementFromCell(self.createCustomTable(ses.FindById(id)),row,col)
                    left =  elem.__getattr__("ScreenLeft")
                    width = elem.__getattr__("Width")
                    x = left + width/2
                    top =  elem.__getattr__("ScreenTop")
                    height = elem.__getattr__("Height")
                    y = top + height/2
                    pywinauto.mouse.right_click(coords = (int(x), int(y)))
                    status = sap_constants.TEST_RESULT_PASS
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except ValueError as v:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(v)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in rightClickOnCell : Invalid Row or Column number' )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in rightClickOnCell' )
        return status, result, value, err_msg

    def setCellFocus(self, sap_id, input_val, *args):
        """
        This function returns boolean value, performs a highlighted focus  on the simple-container cell
        Input : Row;Column
        Output : Boolean Value
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                row = int(input_val[0])-1
                col = int(input_val[1])-1
                highligh_obj = sap_highlight.highLight()
                if ( ses.FindById(id).type == 'GuiSimpleContainer' ):
                    elem = self.getElementFromCell(self.createCustomTable(ses.FindById(id)),row,col)
                    try:
                        #--------------------------------mouse will move over to the middle of the element and click
                        left = elem.__getattr__("ScreenLeft")
                        width = elem.__getattr__("Width")
                        x = left + width / 2
                        top = elem.__getattr__("ScreenTop")
                        height = elem.__getattr__("Height")
                        y = top + height / 2
                        pywinauto.mouse.move(coords=(int(x), int(y)))
                    except Exception as e:
                        err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
                    highligh_obj.draw_outline(elem)
                    elem.SetFocus()
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except ValueError as v:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(v)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in setCellFocus : Invalid Row or Column number' )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in setCellFocus' )
        return status, result, value, err_msg

#------------------------------------------------Supplimentary Simple Container methods----------------------------------------------------------------

    def createCustomTable(self,elem):
        """
        Rules for custom table
        1.With Headers
            - have lables as headers, then everthing is in scontainers
        2.Without Headers
            - have everything in scontainers
        3.Steploop Containers.
            - all items in this container are not in scontainers
        4.Without Headers Type 2
            - has everything in a single scontainers, inconsistant with rows and columns.
        """
        flag_h = False
        flag_s = False
        sL_flag = False
        self.tableType = None
        if( elem.IsStepLoop == True ):
            sL_flag = True
        ch = list(elem.children)
        hList = []
        rList = []
        for c in ch:
            if( c.Type == 'GuiSimpleContainer' ):
                flag_s=True
                #its a header container

        def getColNum(element):
            """Returs column value if present in element ID"""
            col = None
            eid = element.Id
            num=eid[eid.rindex('/'):][eid[eid.rindex('/'):].index('[')+1:eid[eid.rindex('/'):].index(']')]
            col=num.split(',')[0]
            #check if col exists and is a number
            try:
                int(col)
                if(int(col)==0 and len(col)):log.debug(('Element id has no col value'))
            except:log.error('Element id has no col value')
            del eid,num
            return col
        def getRowNum(element):
            """Returs row value if present in element ID"""
            row = None
            eid = element.Id
            num=eid[eid.rindex('/'):][eid[eid.rindex('/'):].index('[')+1:eid[eid.rindex('/'):].index(']')]
            row=num.split(',')[1]
            #check if row exists and is a number
            try:
                int(row)
                if(int(row)==0 and len(row)):log.debug(('Element id has no row value'))
            except:log.error('Element id has no row value')
            del eid,num
            return row
        def reArrangeRows(row_list):
            """
            This function is to arrange rList in order as in SAPGUI 730 , the scontainers are populated haphazardly
            There are 3 ways to arrange 1.row number 2.last index in name 3.Top/ScreenTop
            Input : rList (its a list of rows within a simple container)
            Output : rList (arranged list)
            """
            tempList = []
            properList = []
            for r in row_list:
                rNum = getRowNum(r)
                tempList.append(int(rNum))
            tempList.sort() #also sorted(tempList)
            for t in tempList:
                for r in row_list:
                    rNum = getRowNum(r)
                    if ( int(rNum) == t ):
                        properList.append(r)
            del tempList, row_list, rNum, t, r
            return properList

        if (flag_s == True and sL_flag == False):
            #set headers
            #header elements are not simple containers any element is a header
            for c in ch:
                if( c.Type != 'GuiSimpleContainer' ):
                    hList.append(c) #adds to header list
                elif(c.Type == 'GuiSimpleContainer'):
                    flag_h=True
                    break# breaks loop as headers are over

            for c in ch:
                if( c.Type == 'GuiSimpleContainer' ):
                    rList.append(c) #adds to header list

            rList = reArrangeRows(rList)

            if ( flag_h == True ):
                """Checks if the objects have inconsistant column headers"""
                for i in range(0,len(rList)):
                    if (len(hList) != len(list(rList[0].children)) ):
                        flag_h = False


            if ( flag_h == True ):
                """
                Identified as a header table
                Assumptions : number of columns at are uniform compared to each row
                """
                logger.print_on_console( 'Table is of type : Header table' )
                self.tableType = 1
                #create header reference List
                refList=[] # list of header col values, will be referenced for other cell assignments
                for i in range(0,len(hList)):
                    helem = hList[i]
                    col=getColNum(helem)
                    refList.append(col)

                tableObj = []
                tableObj.append(hList)
                for r in rList:
                    rListItems = list(r.children)
                    newrList=[]
                    for i in range(0,len(rListItems)):
                        Item_col=getColNum(rListItems[i])
                        if refList[i]==Item_col:
                            newrList.append(rListItems[i])
                        else:
                            for j in range(i,len(rListItems)):
                                if refList[j]==Item_col:
                                    newrList.append(rListItems[i])
                                else:
                                    newrList.append(None)
                    tableObj.append(newrList)
                #del newrList,rListItems,Item_col,refList,col,helem
            else:
                """
                Identified as a header-deficient table
                Assumptions : number of columns at are non-uniform compared to each row
                """
                logger.print_on_console( 'Table is of type : Header-deficient table - type1' )
                logger.print_on_console( 'Warning! : This type of table has inconsistancy with column positions' )
                self.tableType = 2
                tableObj = []
                tableObj.append(hList)
                for r in rList:
                    rListItems = list(r.children)
                    newrList=[]
                    for i in range(0,len(rListItems)):
                            newrList.append(rListItems[i])
                    tableObj.append(newrList)
                del newrList,rListItems

        elif( not flag_h and not sL_flag and not flag_s):
            """
                Identified as a header-deficient table - type2
                Assumptions : number of columns at are non-uniform compared to each row, and there are no neaders and all elements are within a scontainer
            """
            logger.print_on_console( 'Table is of type : Header-deficient table - type2' )
            logger.print_on_console( 'Warning! : This type of table has inconsistancy with column positions' )
            self.tableType = 4
            tableObj=[]
            rHList =[]
            for i in range(0,len(ch)):
                r1=r2=rPrev=None
                r1 = getRowNum(ch[i])
                try:r2 = getRowNum(ch[i+1])
                except Exception as e: log.info('Exception at r2:',e)
                try : rPrev = getRowNum(ch[i-1])
                except Exception as e: log.info('Exception at rPrev:',e)
                if(r1 == r2):
                    rHList.append(ch[i])
                elif( (r2 and r1!=r2) or (r1 and not(r2)) ):
                    if (r1 == rPrev):
                        rHList.append(ch[i])
                        tableObj.append(rHList)
                        rHList=[]
                    else:
                        tableObj.append(rHList)
                        rHList=[]
                        rHList.append(ch[i])
                        tableObj.append(rHList)
            del rHList,r1,r2,rPrev

        elif ( sL_flag == True ):
            """
                Identified as a step-loop table
                Assumptions : 1.number of columns at are non-uniform compared to each row
                              2.Headers are absent
            """
            logger.print_on_console( 'Table is of type : Step-Loop table' )
            self.tableType = 3
            rc = elem.LoopRowCount
            cc = elem.LoopColCount
            allChildren = list(elem.Children)
            tableObj =[]
            ai=0
            for r in range(0,rc):
                Larray = []
                for c in range(0,cc):
                    Larray.append(allChildren[ai])
                    ai=ai+1
                tableObj.append(Larray)
            del ai,rc,cc,allChildren,Larray

        if(len(tableObj) == 0):
            log.error( 'Unable to create table' )
            logger.print_on_console( 'Unable to create table' )
        #deleting all variables to avoid memory leackage
        del sL_flag,flag_h,flag_s,hList,rList
        return tableObj

    def getElementFromCell(self,table,row,col):
        """
        This function returns the element from the table
        Input: table(from createCustomTable), row, column
        Output: SAP object(element) at position <row,column> of the table
        """
        elem = None
        try:
            elem = table[row][col]
            if(elem is None):
                log.info('Element at position ' + str(row + 1) + ',' + str(col + 1) + ' is NoneType')
                logger.print_on_console( 'Element at position ' + str(row + 1) + ',' + str(col + 1) + ' is NoneType' )
        except Exception as e:
            log.error(e)
            log.info('Element at position ' + str(row + 1) + ',' + str(col + 1) + ' not found')
            logger.print_on_console( 'Element at position ' + str(row + 1) + ',' + str(col + 1) + ' not found' )
        del table,row,col
        return elem



