#-------------------------------------------------------------------------------
# Name:        oebs_dropdownlistboxops.py
# Purpose:     keywords in this script are used to perform dropdown and listbox operation.
#
# Author:      sushma.p
#
# Created:     24-10-2016
# Copyright:   (c) yesubabu.d,Shreeram.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from oebs_constants import *
import oebs_key_objects
import oebs_serverUtilities
import time
import logging
import logger
import oebs_mouseops
from oebs_utilops import UtilOperations
from oebs_keyboardops import KeywordOperations
import re

log = logging.getLogger('oebs_dropdownlistboxops.py')

class DropdownListboxOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()
        self.utilops_obj=UtilOperations()
        self.keyboardops_obj=KeywordOperations()

    #Method to get dropdown/listbox values of given Object/XPATH
    def getselected(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        selectedvalue = ''
        try:
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_GETSELECTED)
            #check for dropdown
            if charinfo.role == 'combo box':
                listcontext=self.utilities_obj.looptolist(acc)
                listcontextinfo=listcontext.getAccessibleContextInfo()
                listchildcount=listcontextinfo.childrenCount
                for index in range (listchildcount):
                    childcontext=listcontext.getAccessibleChildFromContext(index)
                    childcontextinfo=childcontext.getAccessibleContextInfo()
                    childstates=childcontextinfo.states
                    if 'selected' in childstates:
                        selectedvalue = childcontextinfo.name
                        output_res = selectedvalue
                        status=TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
            #check for listbox
            elif charinfo.role == 'list':
                #calling getselected def to get all selected values in list
                selectedvalue = self.getselectedlist(acc)
                output_res = selectedvalue
                status = TEST_RESULT_PASS
                methodoutput = TEST_RESULT_TRUE
            else:
                log.debug('%s',MSG_INVALID_INPUT)
                logger.print_on_console(MSG_INVALID_INPUT)
                err_msg = MSG_INVALID_OBJECT
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_selected']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to verify dropdown selected value of given Object/XPATH
    def verifyselectedvalue(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        selectedvalue = []
        try:
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_VERIFYSELECTEDVALUE)
            #check for dropdown
            if charinfo.role == 'combo box':
                childAcc = self.utilities_obj.looptolist(acc)
                selectedvalue = self.getselectedlist(childAcc)
                inputValue = oebs_key_objects.keyword_input
                # inputValue is a list
                if selectedvalue in inputValue:
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
            #check for listbox
            elif charinfo.role == 'list':
                inputValue = oebs_key_objects.keyword_input
                #calling getselected def to get all selected values in list
                selectedvalue = self.getselectedlist(acc)
                #verifys selected values with given input
                # inputValue is a list
                if selectedvalue in inputValue:
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
            else:
                log.debug('%s',MSG_INVALID_OBJECT)
                err_msg = MSG_INVALID_OBJECT
                logger.print_on_console(MSG_INVALID_OBJECT)
            if status == TEST_RESULT_FAIL:
                err_msg = MSG_VERIFYFAIL
                logger.print_on_console(MSG_VERIFYFAIL)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_selected']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to getcount of dropdown/listbox
    def getcount(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        countvalue = ''
        try:
            methodoutput = TEST_RESULT_FALSE
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_GETCOUNT)
            countvalue = charinfo.childrenCount
            log.debug('children count: %s',countvalue)
            status=TEST_RESULT_PASS
            methodoutput=str(countvalue)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            err_msg = ERROR_CODE_DICT['err_get_count']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to verify count value of dropdown/listbox
    def verifycount(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            if len(oebs_key_objects.keyword_input) == 1:
                inputVal=oebs_key_objects.keyword_input[0]
                charinfo = acc.getAccessibleContextInfo()
                log.debug('Received Object Context',DEF_VERIFYCOUNT)
                countvalue = charinfo.childrenCount
                if countvalue == int(inputVal):
                    status=TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
                else:
                    log.debug('%s',MSG_INVALID_INPUT)
                    logger.print_on_console(MSG_INVALID_INPUT)
                    err_msg = MSG_INVALID_INPUT
            else:
                log.debug('MSG:%s',MSG_INVALID_NOOF_INPUT)
                err_msg = MSG_INVALID_INPUT
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_count']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to verify all values of dropdown/listbox
    def verifyallvalues(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        inputValues = oebs_key_objects.keyword_input
        try:
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_VERIFYALLVALUES)
            #check for dropdown
            if charinfo.role == 'combo box':
                #calling getvaluesdropdown def to get all values in dropdown
                    generatedvalues  = self.getvaluesdropdown(acc)
                    if sorted(generatedvalues) == sorted(inputValues):
                        status=TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
            #check for listbox
            elif charinfo.role == 'list':
                #calling getvalueslist def to get all values in list
                listvalues = self.getvalueslist(acc)
                if len(inputValues) > 0 and str(listvalues) == inputValues[0]:
                        status=TEST_RESULT_PASS
                        methodoutput =TEST_RESULT_TRUE
            else:
                log.debug('%s',MSG_INVALID_OBJECT)
                err_msg = MSG_INVALID_OBJECT
                logger.print_on_console(err_msg)
            if status == TEST_RESULT_FAIL:
                err_msg = MSG_VERIFYFAIL
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            err_msg = ERROR_CODE_DICT['err_verify_all_values']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to verify given values present in list/dropdown
    def verifyvaluesexists(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        flag = 0
        try:
            log.debug('Received Object Context',DEF_VERIFYVALUESEXISTS)
            charinfo = acc.getAccessibleContextInfo()
            inputValues = oebs_key_objects.keyword_input
            if(len(inputValues) > 0 and inputValues[0] != ''):
                #check for dropdown
                if charinfo.role == 'combo box':
                    #calling getvaluesdropdown def to get all values in dropdown
                    generatedvalues  = self.getvaluesdropdown(acc)
                    inputlength = len(inputValues)
                    for i in range(0,inputlength):
                        if inputValues[i] in generatedvalues:
                            status=TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                        else:
                            status=TEST_RESULT_FAIL
                            methodoutput = TEST_RESULT_FALSE
                #check for listbox
                elif charinfo.role == 'list':
                    #calling getvalueslist def to get all values in list
                    listvalues = self.getvalueslist(acc)
                    inputlength = len(inputValues)
                    for i in range(0,inputlength):
                        if inputValues[i] in listvalues:
                            flag+=1
                            status=TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE

                        if(flag==inputlength):
                            status=TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                        else:
                            status=TEST_RESULT_FAIL
                            methodoutput = TEST_RESULT_FALSE
                else:
                    log.debug('%s',MSG_INVALID_INPUT)
                    err_msg = MSG_INVALID_INPUT
                    logger.print_on_console(err_msg)
                if status == TEST_RESULT_FAIL:
                    err_msg = MSG_VERIFYFAIL
                    logger.print_on_console(err_msg)
            else:
                err_msg = MSG_INVALID_INPUT
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            err_msg = ERROR_CODE_DICT['err_verify_values_exist']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to get selected values for listbox
    def getselectedlist(self,acc):
        selectedvalue = ''
        charinfo = acc.getAccessibleContextInfo()
        count = charinfo.childrenCount
        if charinfo.role == 'list':
            for num in range(0, count) :
                childAcc = acc.getAccessibleChildFromContext(num)
                acccontext = childAcc.getAccessibleContextInfo()
                state = acccontext.states
                if 'selected' in state:
                    selectedvalue = acccontext.name
                    break
        return selectedvalue

    #Method to get count for dropdown
    def count(self,acc):
        global countvalue
        charinfo = acc.getAccessibleContextInfo()
        for i in range(charinfo.childrenCount):
                    childacc = acc.getAccessibleChildFromContext(i)
                    contextInfo = childacc.getAccessibleContextInfo()
                    if contextInfo.role == 'list':
                        countvalue = str(contextInfo.childrenCount)
                        break
                    count(childacc)
        return countvalue

    #Method to get all values of drop down
    def getvaluesdropdown(self,acc):
        charinfo = self.utilities_obj.looptolist(acc)
        selectedvalue = []
        contextInfo = charinfo.getAccessibleContextInfo()
        if contextInfo.role == 'list':
            #global selectedvalue
            count1 = contextInfo.childrenCount
            for num in range(0, count1) :
                acctemp = charinfo.getAccessibleChildFromContext(num)
                acccontext = acctemp.getAccessibleContextInfo()
                state = acccontext.role
                if state=='label':
                    value = acccontext.name
                    selectedvalue.append(str(value))
        return selectedvalue

    #Method to get all values of listbox
    def getvalueslist(self,acc):
        selectedvalue = []
        #global selectedvalue
        contextInfo = acc.getAccessibleContextInfo()
        if contextInfo.role == 'list':
            count1 = contextInfo.childrenCount
            for num in range(0, count1) :
                childacc = acc.getAccessibleChildFromContext(num)
                acccontext = childacc.getAccessibleContextInfo()
                state = acccontext.role
                if state=='label':
                    value = acccontext.name
                    selectedvalue.append(str(value))
        return selectedvalue

    #method to verify whether given values are selected in listbox object
    def	verifyselectedvalues(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            accinfo=acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_VERIFYSELECTEDVALUES)
            if (accinfo.role == 'list') :
                count=0
                for num in range(0,accinfo.childrenCount):
                    for counter in range(0,len(oebs_key_objects.keyword_input)):
                        childinfo=acc.getAccessibleChildFromContext(num)
                        childcontextInfo=childinfo.getAccessibleContextInfo()
                        if (childcontextInfo.name == oebs_key_objects.keyword_input[counter]):
                            if('selected' in childcontextInfo.states):
                                count=count+1
                            else:
                                break
                if(count == len(oebs_key_objects.keyword_input)):
                    methodoutput = TEST_RESULT_TRUE
                    status=TEST_RESULT_PASS
                else:
                    methodoutput = TEST_RESULT_FALSE
                if status == TEST_RESULT_FAIL:
                    err_msg = MSG_VERIFYFAIL
                    logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            err_msg = ERROR_CODE_DICT['err_verify_selected_values']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to get the values of the given Object location by passing their indexes
    def getmultiplevaluesbyindexes(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        output_list=None
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_GETMULTIPLEVALUESBYINDEXES)
            if curaccinfo.role == 'list' and 'enabled' in curaccinfo.states:
                valueslength = len(oebs_key_objects.keyword_input)
                if valueslength >=  1:
                    output_list=[]
                    for index in range (valueslength):
                        i = oebs_key_objects.keyword_input[index]
                        actualelement=acc.getAccessibleChildFromContext(int(i))
                        elementcontext=actualelement.getAccessibleContextInfo()
                        if index == 0:
                            methodoutput=elementcontext.name
                            methodoutput=methodoutput + ';'

                        else:
                            methodoutput=methodoutput + elementcontext.name
                            if(index !=valueslength-1):
                                methodoutput=methodoutput + ';'
                        output_list.append(elementcontext.name)
                    status=TEST_RESULT_PASS
                else:
                    log.debug('%s',DEF_GETMULTIPLEVALUESBYINDEXES,MSG_INVALID_INPUT)
                    err_msg = MSG_INVALID_INPUT
                    logger.print_on_console(err_msg)
            else:
                log.debug('Not a List',DEF_GETMULTIPLEVALUESBYINDEXES)
                err_msg = ERROR_CODE_DICT['err_object']
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_multiple_index']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',DEF_GETMULTIPLEVALUESBYINDEXES,e)
            log.debug('Status %s',DEF_GETMULTIPLEVALUESBYINDEXES,status)
        log.debug('Status %s',DEF_GETMULTIPLEVALUESBYINDEXES,status)
        return status,output_list,output_res,err_msg

    def selectvaluebyindex(self,acc,*args):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            currinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context')
            children=''
            if(currinfo.role =='list'):
                children = currinfo.childrenCount
            else:
                listObj = self.utilities_obj.looptolist(acc)
                listContext = listObj.getAccessibleContextInfo()
                children=listContext.childrenCount
            if (len(oebs_key_objects.keyword_input) == 1) and (oebs_key_objects.keyword_input[0] != None):
                if (oebs_key_objects.keyword_input[0] != ''):
                    childindex = int(oebs_key_objects.keyword_input[0])
                    log.debug('Specified text %s',childindex)
                    if (int(childindex) < int(children)) and (int(childindex) >= 0):
                        if currinfo.role =='combo box':
                            x_coor = int(currinfo.x + (0.5 * currinfo.width))
                            y_coor = int(currinfo.y + (0.5 * currinfo.height))
                            if x_coor == -1 or y_coor == -1 and (args[0]['top'] != '' and args[0]['left'] != '' and args[0]['width'] != '' and args[0]['height'] != '' and args[0]['top'] != -1 and args[0]['left'] != -1 and args[0]['width'] != -1 and args[0]['height'] != -1):
                                x_coor = int(args[0]['left'] + (0.5 * args[0]['width']))
                                y_coor = int(args[0]['top'] + (0.5 * args[0]['height']))
                            #Visibility check for scrollbar
                            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
                                acc.doAccessibleActions(1, 'Toggle Drop Down')
                                for i in range(2):
                                    oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                                acc = self.utilities_obj.looptolist(acc)
                                currinfo=acc.getAccessibleContextInfo()
                                if currinfo.accessibleAction == 1:
                                    acc.addAccessibleSelectionFromContext(int(childindex))
                                    status = TEST_RESULT_PASS
                                    methodoutput = TEST_RESULT_TRUE
                                    log.debug('Value is selected')
                                else:
                                    currentselection=0
                                    for selected in range(children):
                                        labelobj=acc.getAccessibleChildFromContext(selected)
                                        labelcontext=labelobj.getAccessibleContextInfo()
                                        if 'selected' in labelcontext.states:
                                            currentselection=labelcontext.indexInParent
                                    if currentselection != childindex:
                                        moveloc=0
                                        if currentselection>childindex:
                                            moveloc=currentselection-childindex
                                            for index in range(int(moveloc)):
                                                self.keyboardops_obj.keyboard_operation('keypress','A_UP')
                                            requiredcontext, visible, active_parent = self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]",oebs_key_objects.object_type,args[0]['top'],args[0]['left'],args[0]['width'],args[0]['height'])
                                            listObj = self.utilities_obj.looptolist(requiredcontext)
                                            childobj=listObj.getAccessibleChildFromContext(int(childindex))
                                            childcontext=childobj.getAccessibleContextInfo()
                                            if 'selected' in childcontext.states:
                                                status = TEST_RESULT_PASS
                                                methodoutput = TEST_RESULT_TRUE
                                            log.debug('Value is selected')
                                        elif currentselection<childindex:
                                            moveloc=childindex-currentselection
                                            for index in range(int(moveloc)):
                                                self.keyboardops_obj.keyboard_operation('keypress','A_DOWN')
                                                time.sleep(0.1)
                                            requiredcontext, visible, active_parent = self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]",oebs_key_objects.object_type,args[0]['top'],args[0]['left'],args[0]['width'],args[0]['height'])
                                            listObj = self.utilities_obj.looptolist(requiredcontext)
                                            childobj=listObj.getAccessibleChildFromContext(int(childindex))
                                            childcontext=childobj.getAccessibleContextInfo()
                                            if 'selected' in childcontext.states:
                                                status = TEST_RESULT_PASS
                                                methodoutput = TEST_RESULT_TRUE
                                            log.debug('Value is selected')
                                    else:
                                        status = TEST_RESULT_PASS
                                        methodoutput = TEST_RESULT_TRUE
                                        if currentselection != childindex:
                                            logger.print_on_console(MSG_INVALID_NOOF_INPUT)
                                            log.debug('%s',MSG_INVALID_NOOF_INPUT)
                                    log.debug('Value is selected')
                                #combo box is revert back with below code
                                self.keyboardops_obj.keyboard_operation('keypress','ENTER')
                                time.sleep(0.4)
                                labelobj1=acc.getAccessibleChildFromContext(childindex)
                                labelcontext1=labelobj1.getAccessibleContextInfo()
                                if 'selected' in labelcontext1.states:
                                    status = TEST_RESULT_PASS
                                    methodoutput = TEST_RESULT_TRUE
                                else:
                                    if labelcontext1.x == -1 and labelcontext1.y == -1 and labelcontext1.width == -1 and labelcontext1.height == -1:
                                        oebs_key_objects.custom_msg.append(MSG_OBJECT_SELECTABLE)
                                        status = TEST_RESULT_PASS
                                        methodoutput = TEST_RESULT_TRUE
                                    else:
                                        err_msg = MSG_OBJECT_READONLY
                                        logger.print_on_console(err_msg)
                                        status = TEST_RESULT_FAIL
                                        methodoutput = TEST_RESULT_FALSE
                            else:
                                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                                err_msg = MSG_ELEMENT_NOT_VISIBLE
                                logger.print_on_console(err_msg)
                        else:
                            if currinfo.accessibleAction == 1 or currinfo.accessibleSelection == 1:
                                acc.addAccessibleSelectionFromContext(int(childindex))
                                status = TEST_RESULT_PASS
                                methodoutput = TEST_RESULT_TRUE
                                log.debug('Value is selected')
                            else:
                                labelcontext=''
                                currentselection=0
                                x_coor=int((currinfo.x + 5) + (currinfo.width * 0.5))
                                y_coor=int(currinfo.y + 5)
                                #Visibility check for scrollbar
                                if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
                                    oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                                    #time to get the context of the clicked value
                                    time.sleep(2)
                                    for selected in range(int(currinfo.childrenCount)):
                                        labelobj=acc.getAccessibleChildFromContext(selected)
                                        labelcontext=labelobj.getAccessibleContextInfo()
                                        if 'selected' in labelcontext.states:
                                            currentselection=labelcontext.indexInParent

                                    if currentselection != childindex:
                                        moveloc=0
                                        if currentselection>childindex:
                                            moveloc=currentselection-childindex
                                            for index in range(int(moveloc)):
                                                self.keyboardops_obj.keyboard_operation('keypress','A_UP')
                                                time.sleep(0.1)
                                            requiredcontext, visible, active_parent = self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]",oebs_key_objects.object_type,args[0]['top'],args[0]['left'],args[0]['width'],args[0]['height'])
                                            listObj = self.utilities_obj.looptolist(requiredcontext)
                                            childobj=listObj.getAccessibleChildFromContext(int(childindex))
                                            childcontext=childobj.getAccessibleContextInfo()
                                            if 'selected' in childcontext.states:
                                                status = TEST_RESULT_PASS
                                                methodoutput = TEST_RESULT_TRUE
                                            log.debug('Value is selected')
                                        elif currentselection<childindex:
                                            moveloc=childindex-currentselection
                                            for index in range(int(moveloc)):
                                                self.keyboardops_obj.keyboard_operation('keypress','A_DOWN')
                                                time.sleep(0.1)
                                            requiredcontext, visible, active_parent = self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]",oebs_key_objects.object_type,args[0]['top'],args[0]['left'],args[0]['width'],args[0]['height'])
                                            listObj = self.utilities_obj.looptolist(requiredcontext)
                                            childobj=listObj.getAccessibleChildFromContext(int(childindex))
                                            childcontext=childobj.getAccessibleContextInfo()
                                            if 'selected' in childcontext.states:
                                                status = TEST_RESULT_PASS
                                                methodoutput = TEST_RESULT_TRUE
                                            log.debug('Value is selected')
                                    else:
                                        status = TEST_RESULT_PASS
                                        methodoutput = TEST_RESULT_TRUE
                                        if currentselection != childindex:
                                            logger.print_on_console(MSG_INVALID_NOOF_INPUT)
                                            log.debug('%s',MSG_INVALID_NOOF_INPUT)
                                else:
                                    log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                                    err_msg = MSG_ELEMENT_NOT_VISIBLE
                                    logger.print_on_console(err_msg)
                    else:
                        err_msg = MSG_INVALID_NOOF_INPUT
                        log.debug('%s',MSG_INVALID_NOOF_INPUT)
                        logger.print_on_console(err_msg)
                else:
                    err_msg = MSG_INVALID_INPUT
                    log.debug('%s',err_msg)
                    logger.print_on_console(err_msg)
            else:
                err_msg = MSG_INVALID_NOOF_INPUT
                log.debug('%s',err_msg)
                logger.print_on_console(err_msg)    
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_select_value_index']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to returns text of the given Object location
    def getvaluebyindex(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            charinfo = acc.getAccessibleContextInfo()
            accinfo=self.utilities_obj.looptolist(acc)
            listcontxtInfo=accinfo.getAccessibleContextInfo()
            #enhancement for defect fix_1001
            #if (int(oebs_key_objects.keyword_input[0]) < listcontxtInfo.childrenCount and oebs_key_objects.keyword_input[0] >= 0):
            if(oebs_key_objects.keyword_input[0] != ''):
                if(int(oebs_key_objects.keyword_input[0]) > listcontxtInfo.childrenCount or int(oebs_key_objects.keyword_input[0]) < 0):
                    err_msg = MSG_INVALID_INPUT
                    log.debug('%s',err_msg)
                    logger.print_on_console(err_msg)
                else:
                    childinfo=accinfo.getAccessibleChildFromContext(int(oebs_key_objects.keyword_input[0]))
                    childcontxt=childinfo.getAccessibleContextInfo()
                    status=TEST_RESULT_PASS
                    methodoutput=childcontxt.name
            else:
                err_msg = MSG_INVALID_INPUT
                log.debug('%s',err_msg)
                logger.print_on_console(err_msg)   
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_value_index']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg



    #Added for the issue #8010
    def getallvalues(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_VERIFYALLVALUES)
            #check for dropdown
            if charinfo.role == 'combo box':
                #calling getvaluesdropdown def to get all values in dropdown
                    generatedvalues  = self.getvaluesdropdown(acc)
                    if len(generatedvalues)!=0:
                        status=TEST_RESULT_PASS
                        methodoutput = generatedvalues
            #check for listbox
            elif charinfo.role == 'list':
                #calling getvalueslist def to get all values in list
                listvalues = self.getvalueslist(acc)
                if len(listvalues)!=0:
                        status=TEST_RESULT_PASS
                        methodoutput = listvalues
            else:
                err_msg = MSG_INVALID_OBJECT
                log.debug('%s',err_msg)
                logger.print_on_console(err_msg)
            if status == TEST_RESULT_FAIL:
                err_msg = MSG_VERIFYFAIL
                logger.print_on_console(MSG_VERIFYFAIL)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_all_values']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to selects all text of the given Object location
    def selectallvalues(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            log.debug('Received Object Context')
            curaccinfo=acc.getAccessibleContextInfo()
            if(curaccinfo.role == 'list' and 'multiselectable' in curaccinfo.states):
                getAcceess=acc.selectAllAccessibleSelectionFromContext()
                methodoutput = TEST_RESULT_TRUE
                status=TEST_RESULT_PASS
            else:
                err_msg = MSG_SINGLESELECTION_LIST
                log.debug('%s',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_select_all_values']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to deselects all text of the given Object location
    def deselectall(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            currinfo = acc.getAccessibleContextInfo()
            if(currinfo.role == 'list' and 'multiselectable' in currinfo.states):
                values = currinfo.childrenCount
                for index in range(int(values)):
                    getAcceess=acc.removeAccessibleSelectionFromContext(index)
                methodoutput = TEST_RESULT_TRUE
                status=TEST_RESULT_PASS
            else:
                err_msg = MSG_SINGLESELECTION_LIST
                log.debug('%s',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_deselect_all']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to selects multiple text of the given Object location providing thier indexes
    def selectmultiplevaluesbyindexes(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            contextinfo=acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_SELECTMULTIPLEVALUESBYINDEXES)
            childrennames=[]

            # code to deselect all selected values, fix for defect:1132
            children=contextinfo.childrenCount
            for index in range(int(children)):
                getAcceess=acc.removeAccessibleSelectionFromContext(index)

            if len(oebs_key_objects.keyword_input) > 0 and contextinfo.role == 'list':
                if (len(oebs_key_objects.keyword_input) > 1 and 'multiselectable' in contextinfo.states) or len(oebs_key_objects.keyword_input) == 1:
                    for index in range(len(oebs_key_objects.keyword_input)):
                        if (oebs_key_objects.keyword_input[index] != None) and (oebs_key_objects.keyword_input[index] != ''):
                            childrennames.append(oebs_key_objects.keyword_input[index])
                        if(int(childrennames[index]) < int(contextinfo.childrenCount)):
                            acc.addAccessibleSelectionFromContext(int(childrennames[index]))
                            methodoutput=TEST_RESULT_TRUE
                            status=TEST_RESULT_PASS
                        else:
                            err_msg = MSG_INVALID_INPUT
                            log.debug('%s',err_msg)
                            logger.print_on_console(err_msg)
                            methodoutput = TEST_RESULT_FALSE
                            status=TEST_RESULT_FAIL
                            break
                else:
                    err_msg = MSG_SINGLESELECTION_LIST
                    logger.print_on_console(MSG_SINGLESELECTION_LIST)
                    status=TEST_RESULT_FAIL
            else:
                err_msg = MSG_INVALID_INPUT
                log.debug('%s',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_select_multiple_values']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    def selectvaluebytext(self,acc,*args):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            currinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_SELECTVALUEBYTEXT)
            children = ''
            listObj=''
            if(currinfo.role =='list'):
                children = currinfo.childrenCount
            else:
                listObj = self.utilities_obj.looptolist(acc)
                listContext = listObj.getAccessibleContextInfo()
                children=listContext.childrenCount

            if len(oebs_key_objects.keyword_input) == 1:
                if (oebs_key_objects.keyword_input[0] != None and oebs_key_objects.keyword_input[0] != ''):
                    childname = oebs_key_objects.keyword_input[0]
                    log.debug('Specified text %s',childname)
                    if currinfo.role == 'combo box':
                        x_coor = int(currinfo.x + (0.5 * currinfo.width))
                        y_coor = int(currinfo.y + (0.5 * currinfo.height))
                        if x_coor == -1 or y_coor == -1 and (args[0]['top'] != '' and args[0]['left'] != '' and args[0]['width'] != '' and args[0]['height'] != '' and args[0]['top'] != -1 and args[0]['left'] != -1 and args[0]['width'] != -1 and args[0]['height'] != -1):
                            x_coor = int(args[0]['left'] + (0.5 * args[0]['width']))
                            y_coor = int(args[0]['top'] + (0.5 * args[0]['height']))
                        #Visibility check for scrollbar
                        if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
                            acc.doAccessibleActions(1, 'Toggle Drop Down')
                            for i in range(2):
                                oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                            acc = self.utilities_obj.looptolist(acc)
                            currinfo=acc.getAccessibleContextInfo()
                            if currinfo.accessibleAction == 1:
                                for index in range(children):
                                    childacc = acc.getAccessibleChildFromContext(int(index))
                                    childcontext = childacc.getAccessibleContextInfo()
                                    fetchedname = childcontext.name
                                    if(childname == fetchedname):
                                        acc.addAccessibleSelectionFromContext(index)
                                        status = TEST_RESULT_PASS
                                        methodoutput = TEST_RESULT_TRUE
                                        log.debug('Value selected is %s',fetchedname)
                                        break
                                    else:
                                        log.debug('Value Does not exist',DEF_SELECTVALUEBYTEXT)
                                        err_msg = ERROR_CODE_DICT['err_value']
                                        logger.print_on_console(err_msg)
                            else:
                                elementPos=0
                                for index in range(children):
                                    listObj=acc.getAccessibleChildFromContext(index)
                                    labelContext=listObj.getAccessibleContextInfo()
                                    fetchedname=labelContext.name
                                    if(childname == fetchedname):
                                        break
                                    else:
                                        if index < int(children -1):
                                            elementPos=elementPos + 1
                                        else:
                                            elementPos=-1
                                if elementPos != -1:
                                    status = TEST_RESULT_PASS
                                    methodoutput = TEST_RESULT_TRUE
                                    self.keyboardops_obj.keyboard_operation('keypress','HOME')
                                    for num in range(elementPos):
                                        self.keyboardops_obj.keyboard_operation('keypress','A_DOWN')
                                        time.sleep(0.1)
                                    requiredcontext, visible, active_parent = self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]",oebs_key_objects.object_type,'','','','')
                                    listObj = self.utilities_obj.looptolist(requiredcontext)
                                    childobj=listObj.getAccessibleChildFromContext(int(elementPos))
                                    childcontext=childobj.getAccessibleContextInfo()
                                    if 'selected' in childcontext.states:
                                        status = TEST_RESULT_PASS
                                        methodoutput = TEST_RESULT_TRUE
                                    log.debug('Value is selected',DEF_SELECTVALUEBYTEXT)
                                else:
                                    log.debug('Value Does not exist',DEF_SELECTVALUEBYTEXT)
                                    err_msg = ERROR_CODE_DICT['err_value']
                                    logger.print_on_console(err_msg)
                            #combo box is revert back with below code
                            self.keyboardops_obj.keyboard_operation('keypress','ENTER')
                            time.sleep(0.4)
                            labelobj1=acc.getAccessibleChildFromContext(elementPos)
                            labelcontext1=labelobj1.getAccessibleContextInfo()
                            if 'selected' in labelcontext1.states:
                                oebs_key_objects.custom_msg.append(MSG_OBJECT_SELECTABLE)
                                status = TEST_RESULT_PASS
                                methodoutput = TEST_RESULT_TRUE
                            else:
                                if labelcontext1.x == -1 and labelcontext1.y == -1 and labelcontext1.width == -1 and labelcontext1.height == -1:
                                    oebs_key_objects.custom_msg.append(MSG_OBJECT_SELECTABLE)
                                    status = TEST_RESULT_PASS
                                    methodoutput = TEST_RESULT_TRUE
                                else:
                                    err_msg = MSG_OBJECT_READONLY
                                    logger.print_on_console(err_msg)
                                    status = TEST_RESULT_FAIL
                                    methodoutput = TEST_RESULT_FALSE
                        else:
                            err_msg = MSG_ELEMENT_NOT_VISIBLE
                            log.debug('MSG:%s',err_msg)
                            logger.print_on_console(err_msg)
                    else:
                        if currinfo.accessibleAction == 1 or currinfo.accessibleSelection == 1:
                            for index in range(children):
                                childacc = acc.getAccessibleChildFromContext(int(index))
                                childcontext = childacc.getAccessibleContextInfo()
                                fetchedname = childcontext.name
                                if(childname == fetchedname):
                                    acc.addAccessibleSelectionFromContext(index)
                                    status = TEST_RESULT_PASS
                                    methodoutput = TEST_RESULT_TRUE
                                    log.debug('Value selected is %s',fetchedname)
                                    break
                            else:
                                log.debug('Value Does not exist',DEF_SELECTVALUEBYTEXT)
                                err_msg = ERROR_CODE_DICT['err_value']
                                logger.print_on_console(err_msg)
                        else:
                            labelContext=''
                            elementPos=0
                            indexpos=0
                            fetchedname=''
                            x_coor=int((currinfo.x + 5) + (currinfo.width * 0.5))
                            y_coor=int(currinfo.y + 5)
                            #Visibility check for scrollbar
                            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
                                oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                                #time to get the context of the clicked value
                                time.sleep(2)
                                for index in range(children):
                                    listContext=acc.getAccessibleChildFromContext(index)
                                    labelContext=listContext.getAccessibleContextInfo()
                                    fetchedname=labelContext.name
                                    if(childname == fetchedname):
                                        break
                                    else:
                                        if index < int(children -1):
                                            elementPos=elementPos + 1
                                            indexpos=index
                                        else:
                                            elementPos=-1
                                            indexpos=index
                                currentselection=0
                                if elementPos != -1:
                                    for selected in range(int(currinfo.childrenCount)):
                                        labelobj=acc.getAccessibleChildFromContext(selected)
                                        labelcontext=labelobj.getAccessibleContextInfo()
                                        if 'selected' in labelcontext.states:
                                            currentselection=labelcontext.indexInParent
                                    if currentselection != elementPos:
                                        moveloc=0
                                        if currentselection>elementPos:
                                            moveloc=currentselection-elementPos
                                            for index in range(int(moveloc)):
                                                self.keyboardops_obj.keyboard_operation('keypress','A_UP')
                                                time.sleep(0.1)
                                            requiredcontext, visible, active_parent = self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]",oebs_key_objects.object_type,'','','','')
                                            listObj = self.utilities_obj.looptolist(requiredcontext)
                                            childobj=listObj.getAccessibleChildFromContext(int(elementPos))
                                            childcontext=childobj.getAccessibleContextInfo()
                                            if 'selected' in childcontext.states:
                                                status = TEST_RESULT_PASS
                                                methodoutput = TEST_RESULT_TRUE
                                            log.debug('Value is selected',DEF_SELECTVALUEBYTEXT)
                                        elif currentselection<elementPos:
                                            moveloc=elementPos-currentselection
                                            for index in range(int(moveloc)):
                                                self.keyboardops_obj.keyboard_operation('keypress','A_DOWN')
                                                time.sleep(0.1)
                                            requiredcontext, visible, active_parent = self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]",oebs_key_objects.object_type,'','','','')
                                            listObj = self.utilities_obj.looptolist(requiredcontext)
                                            childobj=listObj.getAccessibleChildFromContext(int(elementPos))
                                            childcontext=childobj.getAccessibleContextInfo()
                                            if 'selected' in childcontext.states:
                                                status = TEST_RESULT_PASS
                                                methodoutput = TEST_RESULT_TRUE
                                            log.debug('Value is selected',DEF_SELECTVALUEBYTEXT)
                                    else:
                                        status = TEST_RESULT_PASS
                                        methodoutput = TEST_RESULT_TRUE
                                        logger.print_on_console(MSG_INVALID_NOOF_INPUT)
                                        log.debug('%s',MSG_INVALID_NOOF_INPUT)
                                else:
                                    log.debug('Value Does not exist',DEF_SELECTVALUEBYTEXT)
                                    logger.print_on_console(MSG_INVALID_INPUT)
                                    err_msg = MSG_INVALID_INPUT
                            else:
                                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                                logger.print_on_console(MSG_ELEMENT_NOT_VISIBLE)
                                err_msg = MSG_ELEMENT_NOT_VISIBLE
                else:
                    log.debug('%s',MSG_INVALID_INPUT)
                    logger.print_on_console(MSG_INVALID_NOOF_INPUT)
                    err_msg = MSG_INVALID_INPUT
            else:
                log.debug('%s',MSG_INVALID_NOOF_INPUT)
                logger.print_on_console(MSG_INVALID_NOOF_INPUT)
                err_msg = MSG_INVALID_INPUT
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_select_value_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    def selectmultiplevaluesbytext(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            currinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_SELECTMULTIPLEVALUEBYTEXT)
            children = currinfo.childrenCount

            # code to deselect all selected values, fix for defect:1132
            for index in range(int(children)):
                getAcceess=acc.removeAccessibleSelectionFromContext(index)

            childrennames=[]
            for index in range(len(oebs_key_objects.keyword_input)):
                if (oebs_key_objects.keyword_input[index] != None) and (oebs_key_objects.keyword_input[index] != ''):
                    childrennames.append(oebs_key_objects.keyword_input[index])
            childrenselected=0
            if len(childrennames) != 0 :
                if (len(childrennames) > 1 and 'multiselectable' in currinfo.states) or len(childrennames) == 1:
                    for index in range(children):
                        childacc = acc.getAccessibleChildFromContext(int(index))
                        childcontext = childacc.getAccessibleContextInfo()
                        fetchedname = childcontext.name
                        if fetchedname in childrennames:
                            acc.addAccessibleSelectionFromContext(index)
                            childrenselected = childrenselected + 1
                    if childrenselected == len(childrennames):
                        status = TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
                    else:
                        err_msg = ERROR_CODE_DICT['err_multi_select']
                        logger.print_on_console(err_msg)
                        status=TEST_RESULT_FAIL
                else:
                    err_msg = MSG_SINGLESELECTION_LIST
                    logger.print_on_console(err_msg)
                    status=TEST_RESULT_FAIL
            else:
                log.debug('%s',MSG_INVALID_NOOF_INPUT)
                err_msg = MSG_INVALID_INPUT
                logger.print_on_console(MSG_INVALID_INPUT)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_select_multiple_value_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    def select_from_navigator(self, acc):
        """
        def : select_from_navigator
        purpose : select from navigator is used to select the screen from navigator.
        param  : inputs : 1. Heirarchy of the navigator items 
        return : pass,true / fail,false
        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            log.debug('Received Object Context',DEF_SELECTFROMNAVIGATOR)

            # minimizing all the opened navaigator child elements
            for childindex in range(acc.getAccessibleContextInfo().childrenCount):
                try:
                    listchildobjcontext = acc.getAccessibleChildFromContext(childindex)
                    listchildobj = listchildobjcontext.getAccessibleContextInfo()
                    if "-" in str(listchildobj.name).lower() and len(str(listchildobj.name)) > 0 and str(listchildobj.name)[0] == "-":
                        x_cord = listchildobj.x
                        y_cord = listchildobj.y
                        x_cord_width = x_cord + listchildobj.width
                        y_cord_width = y_cord + listchildobj.height
                        x_cordinate = (x_cord + x_cord_width) / 2
                        y_cordinate = (y_cord + y_cord_width) / 2
                        oebs_mouseops.MouseOperation('doubleClick', int(x_cordinate), int(y_cordinate))
                except Exception as e:
                    break

            if len(oebs_key_objects.keyword_input) > 0:
                global counter,flag1,flag2,last_index_clicked
                counter = 0
                flag1 = flag2 =  False
                last_index_clicked = -1
                # currinfo = acc.getAccessibleContextInfo()

                def search_in_navigator():
                    global counter,flag1,flag2,last_index_clicked
                    try:
                        for childindex in range(acc.getAccessibleContextInfo().childrenCount):
                            listchildobjcontext = acc.getAccessibleChildFromContext(childindex)
                            listchildobj = listchildobjcontext.getAccessibleContextInfo()
                            if oebs_key_objects.keyword_input[counter].lower() in str(listchildobj.name).lower() and childindex > last_index_clicked:
                                if len(str(listchildobj.name)) > 0 and str(listchildobj.name)[0] != "-":
                                    x_cord = listchildobj.x
                                    y_cord = listchildobj.y
                                    x_cord_width = x_cord + listchildobj.width
                                    y_cord_width = y_cord + listchildobj.height
                                    x_cordinate = (x_cord + x_cord_width) / 2
                                    y_cordinate = (y_cord + y_cord_width) / 2
                                    last_index_clicked = childindex
                                    oebs_mouseops.MouseOperation('doubleClick', int(x_cordinate), int(y_cordinate))
                                time.sleep(2)
                                flag1 = True
                                counter += 1
                                if counter < len(oebs_key_objects.keyword_input):
                                    search_in_navigator()
                                else:
                                    flag2 = True
                                    break
                            if flag2:
                                    break
                    except Exception as e:
                        err_msg = ERROR_CODE_DICT['err_select_navigator']
                        logger.print_on_console(err_msg)
                        log.error(err_msg)
                        log.debug('%s',e)
                        
                search_in_navigator()
                
                if flag1 == True and flag2 == True:
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
                elif flag1 != False or flag2 == False:
                    err_msg = ERROR_CODE_DICT['err_select_navigator']

            if err_msg:
                log.info(err_msg)
                logger.print_on_console (err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_select_navigator']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
        return status,methodoutput,output_res,err_msg