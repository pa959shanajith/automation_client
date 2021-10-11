#-------------------------------------------------------------------------------
# Name:        oebs_tableops.py
# Purpose:     keywords in this script are used to perform table operation.
#
# Author:      sushma.p
#
# Created:     24-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------

import oebs_key_objects
import logging
import oebs_serverUtilities
from oebs_constants import *
import oebs_mouseops
import logger
log = logging.getLogger('oebs_tableops.py')

class TableOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()

    #Method to get row count of a table
    def getrowcount(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = ''
        output_res = OUTPUT_CONSTANT
        err_msg = None
        rowcount = ''
        try:
                log.debug('Received Object Context',DEF_GETROWCOUNT)
                #gets the accessible table information
                curaccinfo=acc.getAccessibleContextInfo()
                childrencount=curaccinfo.childrenCount
                for count in range (childrencount):
                    tablechild=acc.getAccessibleChildFromContext(count)
                    tablechildcontext=tablechild.getAccessibleContextInfo()
                    if(tablechildcontext.role =='row header'):
                        status=TEST_RESULT_PASS
                        methodoutput = str(tablechildcontext.childrenCount+1)
                        break
                    elif tablechildcontext.role == 'label':
                        parentacc = acc.getAccessibleParentFromContext()
                        parentinfo = parentacc.getAccessibleContextInfo()
                        if parentinfo.role == 'viewport':
                            tableinfo = acc.getAccessibleTableInfo()
                            rowcount = tableinfo.rowCount
                            status=TEST_RESULT_PASS
                            methodoutput = str(rowcount)
                            break
                        elif parentinfo.role == 'table':
                            curaccinfo=parentacc.getAccessibleContextInfo()
                            childrencount=curaccinfo.childrenCount
                            for count in range (childrencount):
                                tablechild=parentacc.getAccessibleChildFromContext(count)
                                tablechildcontext=tablechild.getAccessibleContextInfo()
                                if(tablechildcontext.role =='row header'):
                                    status=TEST_RESULT_PASS
                                    methodoutput = str(tablechildcontext.childrenCount)
                                    break
                            break
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_row_count']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to get column count of a table
    def getcolumncount(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = ''
        output_res = OUTPUT_CONSTANT
        err_msg = None
        columncount = ''
        try:
                log.debug('Received Object Context',DEF_GETCOLUMNCOUNT)
                #gets the accessible table information
                curaccinfo=acc.getAccessibleContextInfo()
                childrencount=curaccinfo.childrenCount
                for count in range (childrencount):
                    tablechild=acc.getAccessibleChildFromContext(count)
                    tablechildcontext=tablechild.getAccessibleContextInfo()
                    if(tablechildcontext.role =='column header'):
                        status=TEST_RESULT_PASS
                        methodoutput = str(tablechildcontext.childrenCount)
                        break
                    elif tablechildcontext.role == 'label':
                        parentacc = acc.getAccessibleParentFromContext()
                        parentinfo = parentacc.getAccessibleContextInfo()
                        if parentinfo.role == 'viewport':
                            tableinfo = acc.getAccessibleTableInfo()
                            columncount = tableinfo.columnCount
                            status=TEST_RESULT_PASS
                            methodoutput = str(columncount)
                            break
                        elif parentinfo.role == 'table':
                            curaccinfo=parentacc.getAccessibleContextInfo()
                            childrencount=curaccinfo.childrenCount
                            for count in range (childrencount):
                                tablechild=parentacc.getAccessibleChildFromContext(count)
                                tablechildcontext=tablechild.getAccessibleContextInfo()
                                if(tablechildcontext.role =='column header'):
                                    status=TEST_RESULT_PASS
                                    methodoutput = str(tablechildcontext.childrenCount)
                                    break
                            break
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_column_count']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to get cell value of given Object/XPATH
    def getcellvaluejava(self,acc):
        del oebs_key_objects.custom_msg[:]
            #this is the response obtained from the keyword
        methodoutput=''
        try:
            log.debug('Received Object Context',DEF_GETCELLVALUEJAVA)
            if(oebs_key_objects.keyword_input[0] =='1'):
                parentcontext=self.getparent(acc)
                methodoutput=self.getheader(parentcontext)
            else:
                #gets the inputs which user has passed and subtracting 1 or 2 to match the values which user passes with the table index as table index starts with 0
                rowinput=int(oebs_key_objects.keyword_input[0])-2
                coulmninput=int(oebs_key_objects.keyword_input[1])-1
                self.getrowcount(acc)
                #gets the output from getrowcount method
                actualrowcount = int(oebs_key_objects.keyword_output[1])
                tablecontextinfo=acc.getAccessibleTableInfo()
                self.getcolumncount(acc)
                #gets the output from getcoulmncount method
                actualcoulmncount = int(oebs_key_objects.keyword_output[1])
                if( rowinput    <   actualrowcount  and rowinput >= 0 and coulmninput <   actualcoulmncount  and coulmninput >= 0 ):
                    cellinfo=acc.getAccessibleTableCellInfo(rowinput,coulmninput)
                    index=cellinfo.index
                    contextinfo=acc.getAccessibleChildFromContext(index)
                    cellcontextinfo=contextinfo.getAccessibleContextInfo()
                    if(cellcontextinfo.role == 'label'):
                        methodoutput=cellcontextinfo.name
                else:
                    log.debug('%s',MSG_INVALID_NOOF_INPUT)
                    logger.print_on_console(MSG_INVALID_NOOF_INPUT)
                    oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_cell_value']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
        return methodoutput

    def getcellvalueOebs(self,acc):
        methodoutput=''
        try:
            log.debug('Received Object Context',DEF_GETCELLVALUEOEBS)
            parentinfo=acc.getAccessibleParentFromContext()
            parentcontext=parentinfo.getAccessibleContextInfo()
            childinfo=acc.getAccessibleChildFromContext(0)
            childcontext=childinfo.getAccessibleContextInfo()
            if(parentcontext.role == 'table' and childcontext.role== 'label' ):
                rowinput=int(oebs_key_objects.keyword_input[0])-1
                coulmninput=int(oebs_key_objects.keyword_input[1])-1
                self.getrowcount(acc)
                actualrowcount = int(oebs_key_objects.keyword_output[1])
                self.getcolumncount(acc)
                actualcoulmncount = int(oebs_key_objects.keyword_output[1])
                if( rowinput    <   actualrowcount  and rowinput >= 0 and coulmninput <   actualcoulmncount  and coulmninput >= 0 ):
                    index = (rowinput*actualcoulmncount)+coulmninput
                    innertablechild=acc.getAccessibleChildFromContext(index)
                    innertablechildcontext=innertablechild.getAccessibleContextInfo()
                    methodoutput=innertablechildcontext.name
                else:
                    log.debug('%s',MSG_INVALID_NOOF_INPUT)
                    oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)

            elif(childcontext.role== 'table'):
                if(oebs_key_objects.keyword_input[0] =='1'):
                    parentcontext=self.getparent(acc)
                    if(parentcontext):
                        methodoutput=self.getheader(parentcontext)
                    else:
                        methodoutput=self.getheader(acc)
                else:
                    rowinput=int(oebs_key_objects.keyword_input[0])-2
                    coulmninput=int(oebs_key_objects.keyword_input[1])-1
                    self.getrowcount(acc)
                    actualrowcount = int(oebs_key_objects.keyword_output[1])
                    self.getcolumncount(acc)
                    actualcoulmncount = int(oebs_key_objects.keyword_output[1])
                    curaccinfo=acc.getAccessibleContextInfo()
                    childrencount=curaccinfo.childrenCount
                    for count in range (childrencount):
                        tablechild=acc.getAccessibleChildFromContext(count)
                        tablechildcontext=tablechild.getAccessibleContextInfo()
                        if(tablechildcontext.role =='table'):
                            if( rowinput    <   actualrowcount  and rowinput >= 0 and coulmninput <   actualcoulmncount  and coulmninput >= 0 ):
                                index = (rowinput*actualcoulmncount)+coulmninput
                                innertablechild=tablechild.getAccessibleChildFromContext(index)
                                innertablechildcontext=innertablechild.getAccessibleContextInfo()
                                methodoutput=innertablechildcontext.name
                            else:
                                log.debug('%s',MSG_INVALID_NOOF_INPUT)
                                logger.print_on_console(MSG_INVALID_NOOF_INPUT)
                                oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)
                        break
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_cell_value']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
        return methodoutput


    def getcellvalue(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = ''
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
                log.debug('Received Object Context',DEF_GETCELLVALUE)
                #gets the accessible table information
                curaccinfo=acc.getAccessibleContextInfo()
                childrencount=curaccinfo.childrenCount
                for count in range (childrencount):
                    tablechild=acc.getAccessibleChildFromContext(count)
                    tablechildcontext=tablechild.getAccessibleContextInfo()
                    #
                    if(tablechildcontext.role =='row header' or tablechildcontext.role =='column header'):
                        result=self.getcellvalueOebs(acc)
                        if(result):
                                if'value' in result:
                                    splitval=result.split("value",1)[1]
                                    if 'is' in splitval:
                                        splitval=splitval.split("is",1)[1]
                                elif 'Column' in result:
                                    splitval=result.split("Column",1)[0]
                        methodoutput=splitval.strip()
                        status=TEST_RESULT_PASS
                        break
                    elif tablechildcontext.role == 'label':
                        parentacc = acc.getAccessibleParentFromContext()
                        parentinfo = parentacc.getAccessibleContextInfo()
                        if parentinfo.role == 'viewport':
                            methodoutput = self.getcellvaluejava(acc)
                            if(methodoutput):
                                status=TEST_RESULT_PASS
                            break
                        elif parentinfo.role == 'table':
                            result = self.getcellvalueOebs(acc)
                            if(result):
                                if'value' in result:
                                    splitval=result.split("value",1)[1]
                                    if 'is' in splitval:
                                        splitval=splitval.split("is",1)[1]
                                elif 'Column' in result:
                                    splitval=result.split("Column",1)[0]
                            methodoutput=splitval.strip()
                            status=TEST_RESULT_PASS
                            break
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_cell_value']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg


    #Method to verify cell value of given Object/XPATH with actual present in application
    def verifycellvalue(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            log.debug('Received Object Context',DEF_VERIFYCELLVALUE)
            #getting cell value using getCellValue method
            inputcellvalue = oebs_key_objects.keyword_input[2]
            self.getcellvalue(acc)
            fetchedcellvalue = oebs_key_objects.keyword_output[1]
            if inputcellvalue == fetchedcellvalue:
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_cell_value']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to cell click of given Object/XPATH with actual present in application
    def cellclick(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            log.debug('Received Object Context',DEF_CELLCLICK)
            #getting cell value using getCellValue method
            #inputcellvalue = oebs_key_objects.keyword_input[2]
            curaccinfo=acc.getAccessibleContextInfo()
            childrencount=curaccinfo.childrenCount
            for count in range (childrencount):
                    tablechild=acc.getAccessibleChildFromContext(count)
                    tablechildcontext=tablechild.getAccessibleContextInfo()
                    if(tablechildcontext.role =='row header' or tablechildcontext.role =='column header'):

                        result=self.cellclickoebs(acc)
                        if(result):
                            methodoutput=TEST_RESULT_TRUE
                            status=TEST_RESULT_PASS
                        break
                    elif tablechildcontext.role == 'label':
                        parentacc = acc.getAccessibleParentFromContext()
                        parentinfo = parentacc.getAccessibleContextInfo()
                        if parentinfo.role == 'viewport':
                            methodoutput = getcellvaluejava(acc)
                            if(methodoutput):
                                status=TEST_RESULT_PASS
                            break
                        elif parentinfo.role == 'table':
                            result =self.cellclickoebs(acc)
                            if(result):
                                methodoutput=TEST_RESULT_TRUE
                                status=TEST_RESULT_PASS
                            break
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_cell_click']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    def getparent(self,acc):
        parentcon=acc.getAccessibleParentFromContext()
        parentcontextinfo=parentcon.getAccessibleContextInfo()
        if(parentcontextinfo.role == 'viewport'):
            c=parentcon.getAccessibleParentFromContext()
            d=c.getAccessibleContextInfo()
            if(d.role == 'scroll pane'):
                return c
        if(parentcontextinfo.role == 'table'):
            d=parentcon.getAccessibleContextInfo()
            return d

    #Method to cell click of OEBS table
    def cellclickoebs(self,acc):
        #  methodoutput=''
        methodoutput = TEST_RESULT_FALSE
        status=TEST_RESULT_FAIL
        try:
            log.debug('Received Object Context',DEF_CELLCLICK)
            parentinfo=acc.getAccessibleParentFromContext()
            parentcontext=parentinfo.getAccessibleContextInfo()
            childinfo=acc.getAccessibleChildFromContext(0)
            childcontext=childinfo.getAccessibleContextInfo()
            if(parentcontext.role == 'table' and childcontext.role== 'label' ):
                rowinput=int(oebs_key_objects.keyword_input[0])-1
                coulmninput=int(oebs_key_objects.keyword_input[1])-1
                self.getrowcount(acc)
                actualrowcount = int(oebs_key_objects.keyword_output[1])
                self.getcolumncount(acc)
                actualcoulmncount = int(oebs_key_objects.keyword_output[1])
                if( rowinput    <   actualrowcount  and rowinput >= 0 and coulmninput <   actualcoulmncount  and coulmninput >= 0 ):
                    index = (rowinput*actualcoulmncount)+coulmninput
                    childrencount = parentcontext.childrenCount
                    for count in range(childrencount):
                        tablechildclick = parentinfo.getAccessibleChildFromContext(count)
                        tablechildcontextclickinfo=tablechildclick.getAccessibleContextInfo()
                        if(tablechildcontextclickinfo.role =='column header'):

                            columncontext = parentinfo.getAccessibleChildFromContext(count)
                            columncontextinfo = columncontext.getAccessibleContextInfo()

                            childcolumncontext = columncontext.getAccessibleChildFromContext(coulmninput)
                            childcolumncontextinfo = childcolumncontext.getAccessibleContextInfo()
                            columnx = childcolumncontextinfo.x
                            columny = childcolumncontextinfo.y
                            columnheight = childcolumncontextinfo.height
                            columnwidth = childcolumncontextinfo.width

                        elif (tablechildcontextclickinfo.role =='row header'):

                            rowcontext = parentinfo.getAccessibleChildFromContext(2)
                            rowcontextinfo = rowcontext.getAccessibleContextInfo()

                            childrowcontext = rowcontext.getAccessibleChildFromContext(rowinput)
                            childrowcontextinfo = childrowcontext.getAccessibleContextInfo()
                            rowx = childrowcontextinfo.x
                            rowy = childrowcontextinfo.y
                            rowheight = childrowcontextinfo.height
                            rowwidth = childrowcontextinfo.width

                    x_coor = (columnx+(columnx+columnwidth))/2
                    y_coor = (rowy+(rowy+rowheight))/2
                    parent_x = parentcontext.x
                    parent_y = parentcontext.y
                    parent_height = parentcontext.height
                    parent_width = parentcontext.width
                    if((x_coor > parent_x and x_coor<(parent_x + parent_width)) and (y_coor>parent_y and y_coor<(parent_y+parent_height))):
                        oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                        methodoutput=TEST_RESULT_TRUE
                else:
                    log.debug('%s',MSG_INVALID_NOOF_INPUT)
                    oebs_key_objects.custom_msg.append(MSG_INVALID_NOOF_INPUT)
                    logger.print_on_console(MSG_INVALID_NOOF_INPUT)
            elif(childcontext.role== 'table'):
                if(oebs_key_objects.keyword_input[0] =='1'):
                    parentcontext=getparent(acc)
                    if(parentcontext):
                        methodoutput=getclickheader(parentcontext)
                    else:
                        methodoutput=getclickheader(acc)
                else:
                    rowinput=int(oebs_key_objects.keyword_input[0])-2
                    coulmninput=int(oebs_key_objects.keyword_input[1])-1
                    getrowcount(acc)
                    actualrowcount = int(oebs_key_objects.keyword_output[1])
                    getcolumncount(acc)
                    actualcoulmncount = int(oebs_key_objects.keyword_output[1])
                    curaccinfo=acc.getAccessibleContextInfo()
                    childrencount=curaccinfo.childrenCount
                    for count in range (childrencount):
                        tablechild=acc.getAccessibleChildFromContext(count)
                        tablechildcontext=tablechild.getAccessibleContextInfo()
                        if(tablechildcontext.role =='table'):
                            if( rowinput    <   actualrowcount  and rowinput >= 0 and coulmninput <   actualcoulmncount  and coulmninput >= 0 ):
                                index = (rowinput*actualcoulmncount)+coulmninput
                                for count in range (childrencount):
                                    tablechildclick = acc.getAccessibleChildFromContext(count)
                                    tablechildcontextclickinfo=tablechildclick.getAccessibleContextInfo()
                                    if(tablechildcontextclickinfo.role =='column header'):

                                        columncontext = acc.getAccessibleChildFromContext(count)
                                        columncontextinfo = columncontext.getAccessibleContextInfo()

                                        childcolumncontext = columncontext.getAccessibleChildFromContext(coulmninput)
                                        childcolumncontextinfo = childcolumncontext.getAccessibleContextInfo()
                                        columnx = childcolumncontextinfo.x
                                        columny = childcolumncontextinfo.y
                                        columnheight = childcolumncontextinfo.height
                                        columnwidth = childcolumncontextinfo.width

                                    elif (tablechildcontextclickinfo.role =='row header'):

                                        rowcontext = acc.getAccessibleChildFromContext(2)
                                        rowcontextinfo = rowcontext.getAccessibleContextInfo()

                                        childrowcontext = rowcontext.getAccessibleChildFromContext(rowinput)
                                        childrowcontextinfo = childrowcontext.getAccessibleContextInfo()
                                        rowx = childrowcontextinfo.x
                                        rowy = childrowcontextinfo.y
                                        rowheight = childrowcontextinfo.height
                                        rowwidth = childrowcontextinfo.width

                                x_coor = (columnx+(columnx+columnwidth))/2
                                y_coor = (rowy+(rowy+rowheight))/2

                                parent_x = childcontext.x
                                parent_y = childcontext.y
                                parent_height = childcontext.height
                                parent_width = childcontext.width
                                if((x_coor > parent_x and x_coor<(parent_x + parent_width)) and (y_coor>parent_y and y_coor<(parent_y+parent_height))):
                                    oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                                    log.debug('Click Successful',DEF_CLICK)
                                    methodoutput = TEST_RESULT_TRUE
                                    status=TEST_RESULT_PASS
                            else:
                                log.debug('%s',MSG_INVALID_NOOF_INPUT)
                                logger.print_on_console(MSG_INVALID_NOOF_INPUT)
                                oebs_key_objects.custom_msg.append(MSG_INVALID_NOOF_INPUT)
                        break
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_cell_click']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
        return methodoutput

    #Method to click table header
    def getclickheader(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        del oebs_key_objects.custom_msg[:]
        result=''
        contextinfo=acc.getAccessibleContextInfo()
        for index in range (contextinfo.childrenCount):
            childcon=acc.getAccessibleChildFromContext(index)
            childinfo=childcon.getAccessibleContextInfo()
            if(childinfo.role == 'viewport' and index == (contextinfo.childrenCount - 1)):
                viewportchildinfo=childcon.getAccessibleChildFromContext(0)
                viewportchild=viewportchildinfo.getAccessibleContextInfo()
                coulmninput=int(oebs_key_objects.keyword_input[1])-1
                if(coulmninput < (viewportchild.childrenCount) and coulmninput >= 0):
                    panelchildinfo=viewportchildinfo.getAccessibleChildFromContext(coulmninput)
                    info=panelchildinfo.getAccessibleContextInfo()
                    result=info.name
                else:
                    log.debug('%s',MSG_INVALID_OBJECT)
                    oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)
                    logger.print_on_console(MSG_INVALID_INPUT)
                break
            elif(childinfo.role =='table'):
                parentacc = acc.getAccessibleContextInfo()
                if(parentacc.role == 'table'):
                    for count in range(parentacc.childrenCount):
                        var = acc.getAccessibleChildFromContext(count)
                        varcontext = var.getAccessibleContextInfo()
                        if(varcontext.role == 'column header'):
                            coulmninput=int(oebs_key_objects.keyword_input[1])-1
                            viewportchildinfo=var.getAccessibleChildFromContext(coulmninput)
                            info=viewportchildinfo.getAccessibleContextInfo()
                            columnheaderx = info.x
                            columnheadery = info.y
                            columnheaderheight = info.height
                            columnheaderwidth = info.width
                            x_coor = (columnheaderx+(columnheaderx+columnheaderwidth))/2
                            y_coor = (columnheadery+(columnheadery+columnheaderheight))/2
                            if((x_coor > columnheaderx and x_coor<(columnheaderx + columnheaderwidth)) and (y_coor>columnheadery and y_coor<(columnheadery+columnheaderheight))):
                                oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                                methodoutput = TEST_RESULT_TRUE
                                status=TEST_RESULT_PASS


                else:
                    coulmninput=int(oebs_key_objects.keyword_input[1])-1
                    viewportchildinfo=childcon.getAccessibleChildFromContext(coulmninput)
                    info=viewportchildinfo.getAccessibleContextInfo()
                    columnheaderx = info.x
                    columnheadery = info.y
                    columnheaderheight = info.height
                    columnheaderwidth = info.width
                    x_coor = (columnheaderx+(columnheaderx+columnheaderwidth))/2
                    y_coor = (columnheadery+(columnheadery+columnheaderheight))/2
                    if((x_coor > columnheaderx and x_coor<(columnheaderx + columnheaderwidth)) and (y_coor>columnheadery and y_coor<(columnheadery+columnheaderheight))):
                        oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                        methodoutput = TEST_RESULT_TRUE
                        status=TEST_RESULT_PASS

                break
        return methodoutput


    def getheader(self,acc):
        del oebs_key_objects.custom_msg[:]
        result=''
        contextinfo=acc.getAccessibleContextInfo()
        for index in range (contextinfo.childrenCount):
            childcon=acc.getAccessibleChildFromContext(index)
            childinfo=childcon.getAccessibleContextInfo()
            if(childinfo.role == 'viewport' and index == (contextinfo.childrenCount - 1)):
                viewportchildinfo=childcon.getAccessibleChildFromContext(0)
                viewportchild=viewportchildinfo.getAccessibleContextInfo()
                coulmninput=int(oebs_key_objects.keyword_input[1])-1
                if(coulmninput < (viewportchild.childrenCount) and coulmninput >= 0):
                    panelchildinfo=viewportchildinfo.getAccessibleChildFromContext(coulmninput)
                    info=panelchildinfo.getAccessibleContextInfo()
                    result=info.name
                else:
                    log.debug('%s',MSG_INVALID_OBJECT)
                    logger.print_on_console(MSG_INVALID_INPUT)
                    oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)
                break
            elif(childinfo.role =='table'):
                parentacc = acc.getAccessibleContextInfo()
                if(parentacc.role == 'table'):
                    for count in range(parentacc.childrenCount):
                        var = acc.getAccessibleChildFromContext(count)
                        varcontext = var.getAccessibleContextInfo()
                        if(varcontext.role == 'column header'):
                            coulmninput=int(oebs_key_objects.keyword_input[1])-1
                            viewportchildinfo=var.getAccessibleChildFromContext(coulmninput)
                            info=viewportchildinfo.getAccessibleContextInfo()
                            result=info.name


                else:
                    coulmninput=int(oebs_key_objects.keyword_input[1])-1
                    viewportchildinfo=childcon.getAccessibleChildFromContext(coulmninput)
                    info=viewportchildinfo.getAccessibleContextInfo()
                    result=info.name
                break
        return result
