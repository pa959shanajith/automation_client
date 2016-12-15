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

from oebs_msg import *
import oebs_key_objects
import oebs_serverUtilities
import time
import logging
import oebs_mouseops
from oebs_utilops import UtilOperations
from oebs_keyboardops import KeywordOperations

class DropdownListboxOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()
        self.utilops_obj=UtilOperations()
        self.keyboardops_obj=KeywordOperations()

    #Method to get dropdown/listbox values of given Object/XPATH
    def getselected(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult = MSG_FAIL
        #this is the response obtained from the keyword
        keywordresponse=''
        selectedvalue = []
        try:
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_DROPDOWNLISTBOX,DEF_GETSELECTED)
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
                        selectedvalue.append(childcontextinfo.name)
                        keywordresult=MSG_PASS
            #check for listbox
            elif charinfo.role == 'list':
                #calling getselected def to get all selected values in list
                selectedvalue = self.getselectedlist(acc)
                keywordresult = MSG_PASS
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_GETSELECTED,MSG_INVALID_INPUT,MSG_INVALID_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_OBJECT")
            outputsize = len(selectedvalue)
            for i in range(outputsize):
                if outputsize == 1:
                    if charinfo.role == 'list':
                        keywordresponse=selectedvalue[i]
                        keywordresponse = keywordresponse + ';'
                    else:
                        keywordresponse=selectedvalue[i]
                else:
                    keywordresponse=keywordresponse + selectedvalue[i]
                    if i < outputsize - 1:
                        keywordresponse = keywordresponse + ';'
            if keywordresult == MSG_PASS:

                if(len(selectedvalue)>1):
                    oebs_key_objects.custom_msg.append("MSG_RESULT_IS")
                else:
                    oebs_key_objects.custom_msg.append("MSG_RESULT_IS")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_GETSELECTED,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_GETSELECTED,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_GETSELECTED,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(selectedvalue)


    #Method to verify dropdown selected value of given Object/XPATH
    def verifyselectedvalue(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        selectedvalue = []
        #sets the verifyresponse to FALSE
        verifyresponse = MSG_FALSE
        try:
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_DROPDOWNLISTBOX,DEF_VERIFYSELECTEDVALUE)
            #check for dropdown
            if charinfo.role == 'combo box':
                childAcc = self.utilities_obj.looptolist(acc)
                selectedvalue = self.getselectedlist(childAcc)
                inputValue = oebs_key_objects.keyword_input
                if selectedvalue == inputValue:
                    keywordresult=MSG_PASS
                    verifyresponse=MSG_TRUE
            #check for listbox
            elif charinfo.role == 'list':
                inputValue = oebs_key_objects.keyword_input
                #calling getselected def to get all selected values in list
                selectedvalue = self.getselectedlist(acc)
                #verifys selected values with given input
                if selectedvalue == inputValue:
                    keywordresult=MSG_PASS
                    verifyresponse=MSG_TRUE
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYSELECTEDVALUE,MSG_INVALID_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_OBJECT")
            if keywordresult == MSG_FAIL:
                oebs_key_objects.custom_msg.append(MSG_VERIFYFAIL)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYSELECTEDVALUE,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYSELECTEDVALUE,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYSELECTEDVALUE,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to getcount of dropdown/listbox
    def getcount(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        var = []
        keywordresponse=''
        countvalue = ''
        try:
            verifyresponse = MSG_FALSE
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_DROPDOWNLISTBOX,DEF_GETCOUNT)
            countvalue = charinfo.childrenCount
            logging.debug('FILE: %s , DEF: %s MSG: children count: %s',OEBS_DROPDOWNLISTBOX,DEF_GETCOUNT,countvalue)
            oebs_key_objects.custom_msg.append("MSG_RESULT_IS")
            keywordresult=MSG_PASS
            keywordresponse=str(countvalue)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_GETCOUNT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_GETCOUNT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_GETCOUNT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(keywordresponse))

    #Method to verify count value of dropdown/listbox
    def verifycount(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        #sets the verifyresponse to FALSE
        verifyresponse = MSG_FALSE
        try:
            if len(oebs_key_objects.keyword_input) == 1:
                inputVal=oebs_key_objects.keyword_input[0]
                charinfo = acc.getAccessibleContextInfo()
                logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_DROPDOWNLISTBOX,DEF_VERIFYCOUNT)
                countvalue = charinfo.childrenCount
                if countvalue == int(inputVal):
                    keywordresult=MSG_PASS
                    verifyresponse = MSG_TRUE
                else:
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYCOUNT,MSG_INVALID_INPUT)
                    oebs_key_objects.custom_msg.append(MSG_VERIFYFAIL)
            else:
                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYCOUNT,MSG_INVALID_NOOF_INPUT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYCOUNT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYCOUNT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYCOUNT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to verify all values of dropdown/listbox
    def verifyallvalues(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult = MSG_FAIL
        #sets the verifyresponse to FALSE
        verifyresponse = MSG_FALSE
        outputvalues = []
        inputValues = oebs_key_objects.keyword_input
        try:
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_DROPDOWNLISTBOX,DEF_VERIFYALLVALUES)
            #check for dropdown
            if charinfo.role == 'combo box':
                #calling getvaluesdropdown def to get all values in dropdown
                    generatedvalues  = self.getvaluesdropdown(acc)
                    if generatedvalues == inputValues:
                        keywordresult=MSG_PASS
                        verifyresponse = MSG_TRUE
            #check for listbox
            elif charinfo.role == 'list':
                #calling getvalueslist def to get all values in list
                listvalues = self.getvalueslist(acc)
                if listvalues == inputValues:
                        keywordresult=MSG_PASS
                        verifyresponse =MSG_TRUE
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYALLVALUES,MSG_INVALID_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_OBJECT")
            if keywordresult == MSG_FAIL:
                oebs_key_objects.custom_msg.append(MSG_VERIFYFAIL)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYALLVALUES,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYALLVALUES,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYALLVALUES,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

    #Method to verify given values present in list/dropdown
    def verifyvaluesexists(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult = MSG_FAIL
        #sets the verifyresponse to FALSE
        verifyresponse = MSG_FALSE
        flag = 0
        outputvalues = []
        try:
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_DROPDOWNLISTBOX,DEF_VERIFYVALUESEXISTS)
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
                            keywordresult=MSG_PASS
                            verifyresponse = MSG_TRUE
                        else:
                            keywordresult=MSG_FAIL
                            verifyresponse = MSG_FALSE
                #check for listbox
                elif charinfo.role == 'list':
                    #calling getvalueslist def to get all values in list
                    listvalues = self.getvalueslist(acc)
                    inputlength = len(inputValues)
                    for i in range(0,inputlength):
                        if inputValues[i] in listvalues:
                            flag+=1;
                            keywordresult=MSG_PASS
                            verifyresponse = MSG_TRUE

                        if(flag==inputlength):
                            keywordresult=MSG_PASS
                            verifyresponse = MSG_TRUE
                        else:
                            keywordresult=MSG_FAIL
                            verifyresponse = MSG_FALSE
                else:
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_BUTTONOPS,DEF_VERIFYVALUESEXISTS,MSG_INVALID_INPUT)
                if keywordresult == MSG_FAIL:
                    oebs_key_objects.custom_msg.append(MSG_VERIFYFAIL)
            else:
                oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYVALUESEXISTS,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYVALUESEXISTS,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYVALUESEXISTS,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to get selected values for listbox
    def getselectedlist(self,acc):
        selectedvalue = []
        charinfo = acc.getAccessibleContextInfo()
        count = charinfo.childrenCount
        if charinfo.role == 'list':
            for num in range(0, count) :
                childAcc = acc.getAccessibleChildFromContext(num)
                acccontext = childAcc.getAccessibleContextInfo()
                state = acccontext.states
                if 'selected' in state:
                       value = acccontext.name
                       selectedvalue.append(str(value))
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
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            accinfo=acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_DROPDOWNLISTBOX,DEF_VERIFYSELECTEDVALUES)
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
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                else:
                    verifyresponse = MSG_FALSE
                if keywordresult == MSG_FAIL:
                    oebs_key_objects.custom_msg.append(MSG_VERIFYFAIL)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYSELECTEDVALUES,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYSELECTEDVALUES,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_VERIFYSELECTEDVALUES,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to get the values of the given Object location by passing their indexes
    def getmultiplevaluesbyindexes(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        #this is the response obtained from the keyword
        keywordresponse=''
        output_list=None
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_DROPDOWNLISTBOX,DEF_GETMULTIPLEVALUESBYINDEXES)
            if 'multiselectable' in curaccinfo.states:
                valueslength = len(oebs_key_objects.keyword_input)
                if valueslength >=  1:
                    output_list=[]
                    for index in range (valueslength):
                        i = oebs_key_objects.keyword_input[index]
                        actualelement=acc.getAccessibleChildFromContext(int(i))
                        elementcontext=actualelement.getAccessibleContextInfo()
                        if index == 0:
                            keywordresponse=elementcontext.name
                            keywordresponse=keywordresponse + ';'

                        else:
                            keywordresponse=keywordresponse + elementcontext.name
                            if(index !=valueslength-1):
                             keywordresponse=keywordresponse + ';'
                        output_list.append(elementcontext.name)
                    keywordresult=MSG_PASS
                else:
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_GETMULTIPLEVALUESBYINDEXES,MSG_INVALID_INPUT)
                    oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
            else:
                logging.debug('FILE: %s , DEF: %s MSG: Not a List',OEBS_DROPDOWNLISTBOX,DEF_GETMULTIPLEVALUESBYINDEXES)
                oebs_key_objects.custom_msg.append('Not a List.')
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_GETMULTIPLEVALUESBYINDEXES,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_GETMULTIPLEVALUESBYINDEXES,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_GETMULTIPLEVALUESBYINDEXES,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(output_list)


    def selectvaluebyindex(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        #this is the response obtained from the keyword
        verifyresponse=MSG_FALSE
        try:
            #gets the entire context information
            currinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX)
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
                    logging.debug('FILE: %s , DEF: %s MSG: Specified text %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX,childindex)
                    if (int(childindex) < int(children)) and (int(childindex) >= 0):
                        if currinfo.role =='combo box':
                            x_coor = int(currinfo.x + (0.5 * currinfo.width))
                            y_coor = int(currinfo.y + (0.5 * currinfo.height))
                            #Visibility check for scrollbar
                            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
                                oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                                acc = self.utilities_obj.looptolist(acc)
                                currinfo=acc.getAccessibleContextInfo()
                                if currinfo.accessibleAction == 1:
                                    acc.addAccessibleSelectionFromContext(int(childindex))
                                    keywordresult = MSG_PASS
                                    verifyresponse = MSG_TRUE
                                    logging.debug('FILE: %s , DEF: %s MSG: Value is selected',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX)
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
                                                self.keyboardops_obj.KeyboardOperation('keypress','A_UP')
                                            requiredcontext=self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]")
                                            listObj = self.utilities_obj.looptolist(requiredcontext)
                                            childobj=listObj.getAccessibleChildFromContext(int(childindex))
                                            childcontext=childobj.getAccessibleContextInfo()
                                            if 'selected' in childcontext.states:
                                                keywordresult = MSG_PASS
                                                verifyresponse = MSG_TRUE
                                            logging.debug('FILE: %s , DEF: %s MSG: Value is selected',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX)
                                        elif currentselection<childindex:
                                            moveloc=childindex-currentselection
                                            for index in range(int(moveloc)):
                                                self.keyboardops_obj.KeyboardOperation('keypress','A_DOWN')
                                                time.sleep(0.1)
                                            requiredcontext=self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]")
                                            listObj = self.utilities_obj.looptolist(requiredcontext)
                                            childobj=listObj.getAccessibleChildFromContext(int(childindex))
                                            childcontext=childobj.getAccessibleContextInfo()
                                            if 'selected' in childcontext.states:
                                                keywordresult = MSG_PASS
                                                verifyresponse = MSG_TRUE
                                            logging.debug('FILE: %s , DEF: %s MSG: Value is selected',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX)
                                    else:
                                        keywordresult = MSG_PASS
                                        verifyresponse = MSG_TRUE
                                        logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX,MSG_INVALID_NOOF_INPUT)
                                    logging.debug('FILE: %s , DEF: %s MSG: Value is selected',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX)
                                #combo box is revert back with below code
                                self.keyboardops_obj.KeyboardOperation('keypress','ENTER')
                                time.sleep(0.4)
                                labelobj1=acc.getAccessibleChildFromContext(childindex)
                                labelcontext1=labelobj1.getAccessibleContextInfo()
                                if 'selected' in labelcontext1.states:
                                    oebs_key_objects.custom_msg.append(MSG_OBJECT_SELECTABLE)
                                    keywordresult = MSG_PASS
                                    verifyresponse = MSG_TRUE
                                else:
                                    oebs_key_objects.custom_msg.append(MSG_OBJECT_READONLY)
                                    keywordresult = MSG_FAIL
                                    verifyresponse = MSG_FALSE
                            else:
                                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX,MSG_ELEMENT_NOT_VISIBLE)
                                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
                        else:
                            if currinfo.accessibleAction == 1:
                                acc.addAccessibleSelectionFromContext(int(childindex))
                                keywordresult = MSG_PASS
                                verifyresponse = MSG_TRUE
                                logging.debug('FILE: %s , DEF: %s MSG: Value is selected',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX)
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
                                                self.keyboardops_obj.KeyboardOperations('keypress','A_UP')
                                                time.sleep(0.1)
                                            requiredcontext=self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]")
                                            listObj = self.utilities_obj.looptolist(requiredcontext)
                                            childobj=listObj.getAccessibleChildFromContext(int(childindex))
                                            childcontext=childobj.getAccessibleContextInfo()
                                            if 'selected' in childcontext.states:
                                                keywordresult = MSG_PASS
                                                verifyresponse = MSG_TRUE
                                            logging.debug('FILE: %s , DEF: %s MSG: Value is selected',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX)
                                        elif currentselection<childindex:
                                            moveloc=childindex-currentselection
                                            for index in range(int(moveloc)):
                                                self.keyboardops_obj.KeyboardOperation('keypress','A_DOWN')
                                                time.sleep(0.1)
                                            requiredcontext=self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]")
                                            listObj = self.utilities_obj.looptolist(requiredcontext)
                                            childobj=listObj.getAccessibleChildFromContext(int(childindex))
                                            childcontext=childobj.getAccessibleContextInfo()
                                            if 'selected' in childcontext.states:
                                                keywordresult = MSG_PASS
                                                verifyresponse = MSG_TRUE
                                            logging.debug('FILE: %s , DEF: %s MSG: Value is selected',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX)
                                    else:
                                        keywordresult = MSG_PASS
                                        verifyresponse = MSG_TRUE
                                        logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX,MSG_INVALID_NOOF_INPUT)
                                else:
                                    logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX,MSG_ELEMENT_NOT_VISIBLE)
                                    oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
                    else:
                        logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX,MSG_INVALID_NOOF_INPUT)
                        oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
                else:
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX,MSG_INVALID_INPUT)
                    oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX,MSG_INVALID_NOOF_INPUT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYINDEX,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

    #Method to returns text of the given Object location
    def getvaluebyindex(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresponse = ''
        keywordresult=MSG_FAIL
        try:
            charinfo = acc.getAccessibleContextInfo()
            accinfo=self.utilities_obj.looptolist(acc)
            listcontxtInfo=accinfo.getAccessibleContextInfo()
            #enhancement for defect fix_1001
            #if (int(oebs_key_objects.keyword_input[0]) < listcontxtInfo.childrenCount and oebs_key_objects.keyword_input[0] >= 0):
            if(oebs_key_objects.keyword_input[0] != ''):
                if(int(oebs_key_objects.keyword_input[0]) > listcontxtInfo.childrenCount or int(oebs_key_objects.keyword_input[0]) < 0):
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_GETVALUEBYINDEX,MSG_INVALID_INPUT)
                    oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
                else:
                    childinfo=accinfo.getAccessibleChildFromContext(int(oebs_key_objects.keyword_input[0]))
                    childcontxt=childinfo.getAccessibleContextInfo()
                    keywordresult=MSG_PASS
                    keywordresponse=childcontxt.name
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_GETVALUEBYINDEX,MSG_INVALID_INPUT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_GETVALUEBYINDEX,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_GETVALUEBYINDEX,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_GETVALUEBYINDEX,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(keywordresponse))

    #Method to selects all text of the given Object location
    def selectallvalues(self,acc):
        del oebs_key_objects.custom_msg[:]
        verifyresponse = MSG_FALSE
        keywordresult=MSG_FAIL
        try:
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_DROPDOWNLISTBOX,DEF_SELECTALLVALUES)
            curaccinfo=acc.getAccessibleContextInfo()
            if(curaccinfo.role == 'list' and 'multiselectable' in curaccinfo.states):
                getAcceess=acc.selectAllAccessibleSelectionFromContext()
                verifyresponse = MSG_TRUE
                keywordresult=MSG_PASS
            else:
                oebs_key_objects.custom_msg.append(MSG_SINGLESELECTION_LIST)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTALLVALUES,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTALLVALUES,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTALLVALUES,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

    #Method to deselects all text of the given Object location
    def deselectall(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        #this is the response obtained from the keyword
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            currinfo = acc.getAccessibleContextInfo()
            if(currinfo.role == 'list' and 'multiselectable' in currinfo.states):
                values = currinfo.childrenCount
                for index in range(int(values)):
                    getAcceess=acc.removeAccessibleSelectionFromContext(index)
                verifyresponse = MSG_TRUE
                keywordresult=MSG_PASS
            else:
                oebs_key_objects.custom_msg.append(MSG_SINGLESELECTION_LIST)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_DESELECTALL,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_DESELECTALL,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_DESELECTALL,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

    #Method to selects multiple text of the given Object location providing thier indexes
    def selectmultiplevaluesbyindexes(self,acc):
        del oebs_key_objects.custom_msg[:]
        verifyresponse = MSG_FALSE
        keywordresult=MSG_FAIL
        try:
            #gets the entire context information
            contextinfo=acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_DROPDOWNLISTBOX,DEF_SELECTMULTIPLEVALUESBYINDEXES)
            childrennames=[]

            # code to deselect all selected values, fix for defect:1132
            children=contextinfo.childrenCount
            for index in range(int(children)):
                getAcceess=acc.removeAccessibleSelectionFromContext(index)

            if len(oebs_key_objects.keyword_input) > 0:
                for index in range(len(oebs_key_objects.keyword_input)):
                    if (oebs_key_objects.keyword_input[index] != None) and (oebs_key_objects.keyword_input[index] != ''):
                        childrennames.append(oebs_key_objects.keyword_input[index])
                    if(int(childrennames[index]) < int(contextinfo.childrenCount)):
                        acc.addAccessibleSelectionFromContext(int(childrennames[index]))
                        verifyresponse=MSG_TRUE
                        keywordresult=MSG_PASS
                    else:
                        logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTMULTIPLEVALUESBYINDEXES,MSG_INVALID_INPUT)
                        verifyresponse = MSG_FALSE
                        keywordresult=MSG_FAIL
                        break
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTMULTIPLEVALUESBYINDEXES,MSG_INVALID_INPUT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTMULTIPLEVALUESBYINDEXES,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTMULTIPLEVALUESBYINDEXES,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTMULTIPLEVALUESBYINDEXES,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    def selectvaluebytext(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        #this is the response obtained from the keyword
        verifyresponse=MSG_FALSE
        try:
            #gets the entire context information
            currinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT)
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
                    logging.debug('FILE: %s , DEF: %s MSG: Specified text %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT,childname)
                    if currinfo.role == 'combo box':
                        x_coor = int(currinfo.x + (0.5 * currinfo.width))
                        y_coor = int(currinfo.y + (0.5 * currinfo.height))
                        #Visibility check for scrollbar
                        if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
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
                                        keywordresult = MSG_PASS
                                        verifyresponse = MSG_TRUE
                                        logging.debug('FILE: %s , DEF: %s MSG: Value selected is %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT,fetchedname)
                                        break
                                    else:
                                        logging.debug('FILE: %s , DEF: %s MSG: Value Does not exist',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT)
                                        oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
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
                                    keywordresult = MSG_PASS
                                    verifyresponse = MSG_TRUE
                                    self.keyboardops_obj.KeyboardOperation('keypress','HOME')
                                    for num in range(elementPos):
                                        self.keyboardops_obj.KeyboardOperation('keypress','A_DOWN')
                                        time.sleep(0.1)
                                    requiredcontext=self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]")
                                    listObj = self.utilities_obj.looptolist(requiredcontext)
                                    childobj=listObj.getAccessibleChildFromContext(int(elementPos))
                                    childcontext=childobj.getAccessibleContextInfo()
                                    if 'selected' in childcontext.states:
                                        keywordresult = MSG_PASS
                                        verifyresponse = MSG_TRUE
                                    logging.debug('FILE: %s , DEF: %s MSG: Value is selected',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT)
                                else:
                                    logging.debug('FILE: %s , DEF: %s MSG: Value Does not exist',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT)
                            #combo box is revert back with below code
                            self.keyboardops_obj.KeyboardOperation('keypress','ENTER')
                            time.sleep(0.4)
                            labelobj1=acc.getAccessibleChildFromContext(elementPos)
                            labelcontext1=labelobj1.getAccessibleContextInfo()
                            if 'selected' in labelcontext1.states:
                                oebs_key_objects.custom_msg.append(MSG_OBJECT_SELECTABLE)
                                keywordresult = MSG_PASS
                                verifyresponse = MSG_TRUE
                            else:
                                oebs_key_objects.custom_msg.append(MSG_OBJECT_READONLY)
                                keywordresult = MSG_FAIL
                                verifyresponse = MSG_FALSE
                        else:
                                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_SETTEXT,MSG_ELEMENT_NOT_VISIBLE)
                                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
                    else:
                        if currinfo.accessibleAction == 1:
                            acc.addAccessibleSelectionFromContext(int(childindex))
                            keywordresult = MSG_PASS
                            verifyresponse = MSG_TRUE
                            logging.debug('FILE: %s , DEF: %s MSG: Value is selected',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT)
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
                                                self.keyboardops_obj.KeyboardOperation('keypress','A_UP')
                                                time.sleep(0.1)
                                            requiredcontext=self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]")
                                            listObj = self.utilities_obj.looptolist(requiredcontext)
                                            childobj=listObj.getAccessibleChildFromContext(int(elementPos))
                                            childcontext=childobj.getAccessibleContextInfo()
                                            if 'selected' in childcontext.states:
                                                keywordresult = MSG_PASS
                                                verifyresponse = MSG_TRUE
                                            logging.debug('FILE: %s , DEF: %s MSG: Value is selected',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT)
                                        elif currentselection<elementPos:
                                            moveloc=elementPos-currentselection
                                            for index in range(int(moveloc)):
                                                self.keyboardops_obj.KeyboardOperation('keypress','A_DOWN')
                                                time.sleep(0.1)
                                            requiredcontext=self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]")
                                            listObj = self.utilities_obj.looptolist(requiredcontext)
                                            childobj=listObj.getAccessibleChildFromContext(int(elementPos))
                                            childcontext=childobj.getAccessibleContextInfo()
                                            if 'selected' in childcontext.states:
                                                keywordresult = MSG_PASS
                                                verifyresponse = MSG_TRUE
                                            logging.debug('FILE: %s , DEF: %s MSG: Value is selected',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT)
                                    else:
                                        keywordresult = MSG_PASS
                                        verifyresponse = MSG_TRUE
                                        logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT,MSG_INVALID_NOOF_INPUT)
                                else:
                                    logging.debug('FILE: %s , DEF: %s MSG: Value Does not exist',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT)
                                    oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
                            else:
                                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_SETTEXT,MSG_ELEMENT_NOT_VISIBLE)
                                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
                else:
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT,MSG_INVALID_INPUT)
                    oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT,MSG_INVALID_NOOF_INPUT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_NO_INPUT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTVALUEBYTEXT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    def selectmultiplevaluesbytext(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        #this is the response obtained from the keyword
        verifyresponse=MSG_FALSE
        try:
            #gets the entire context information
            currinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_DROPDOWNLISTBOX,DEF_SELECTMULTIPLEVALUEBYTEXT)
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
                for index in range(children):
                    childacc = acc.getAccessibleChildFromContext(int(index))
                    childcontext = childacc.getAccessibleContextInfo()
                    fetchedname = childcontext.name
                    if fetchedname in childrennames:
                        acc.addAccessibleSelectionFromContext(index)
                        childrenselected = childrenselected + 1
                if childrenselected == len(childrennames):
                    keywordresult = MSG_PASS
                    verifyresponse = MSG_TRUE
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTMULTIPLEVALUEBYTEXT,MSG_INVALID_NOOF_INPUT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTMULTIPLEVALUEBYTEXT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTMULTIPLEVALUEBYTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_DROPDOWNLISTBOX,DEF_SELECTMULTIPLEVALUEBYTEXT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))
