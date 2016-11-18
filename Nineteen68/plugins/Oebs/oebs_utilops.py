#-------------------------------------------------------------------------------
# Name:        oebs_utilops.py
# Purpose:     keywords in this script enables to perform action on text Objects.
#
# Author:      sushma.p
#
# Created:     24-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from oebs_msg import *
import oebs_key_objects
import oebs_serverUtilities
import logging
import oebs_mouseops
from oebs_keyboardops import KeywordOperations
import time
import oebs_constants
global activeframes
activeframes=[]

class UtilOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()
        self.keyboardops=KeywordOperations()

    #Method to setfocus on the User given Object
    def setfocus(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        keywordresponse=MSG_FALSE
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_UTILOPS,DEF_SETFOCUS)
            x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
            y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
            logging.debug('FILE: %s , DEF: %s MSG: Formula Created',OEBS_UTILOPS,DEF_SETFOCUS)
            #Visibility check for scrollbar
            if(self.getObjectVisibility(acc,x_coor,y_coor)):
                if ('showing' or 'focusable') in curaccinfo.states:
                    oebs_mouseops.MouseOperation('move',x_coor,y_coor)
                    keywordresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                    logging.debug('FILE: %s , DEF: %s MSG: %s %s',OEBS_UTILOPS,DEF_SETFOCUS,MSG_RESULT_IS,keywordresult)
                else:
                    logging.debug('FILE: %s , DEF: %s MSG: %s %s',OEBS_UTILOPS,DEF_SETFOCUS,MSG_RESULT_IS,keywordresult)
                    oebs_key_objects.custom_msg.append("ERR_INVALID_OBJECT")
            else:
                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_UTILOPS,DEF_SETFOCUS,MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_SETFOCUS,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_SETFOCUS,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_SETFOCUS,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(keywordresponse))

    def drag(self,acc):
        print
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            curaccinfo = acc.getAccessibleContextInfo()
            objstates = curaccinfo.states
            if 'enabled' in objstates:
                x1 = curaccinfo.x
                y1 = curaccinfo.y
                width = curaccinfo.width
                height = curaccinfo.height
                x2 = x1 + width
                y2 = y1 + height
                x_cor = (x1+x2)/2
                y_cor = (y1+y2)/2
                oebs_mouseops.MouseOperation('hold',x_cor,y_cor)
                verifyresponse = MSG_TRUE
                keywordresult = MSG_PASS
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_DRAG,keywordresult)
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s %s',OEBS_UTILOPS,DEF_DRAG)
                oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")
                verifyresponse = MSG_FALSE
                keywordresult = MSG_FAIL
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_DRAG,keywordresult)



        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_BUTTONOPS,DEF_CLICK,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_BUTTONOPS,DEF_CLICK,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_BUTTONOPS,DEF_CLICK,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

    def drop(self,acc):
        print
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            curaccinfo = acc.getAccessibleContextInfo()
            objstates = curaccinfo.states
            if 'enabled' in objstates:
                x1 = curaccinfo.x
                y1 = curaccinfo.y
                width = curaccinfo.width
                height = curaccinfo.height
                x2 = x1 + width
                y2 = y1 + height
                x_cor = (x1+x2)/2
                y_cor = (y1+y2)/2

                oebs_mouseops.MouseOperation('slide',x_cor,y_cor)
                oebs_mouseops.MouseOperation('release',x_cor,y_cor)



                verifyresponse = MSG_TRUE
                keywordresult = MSG_PASS
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_DROP,keywordresult)
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s %s',OEBS_UTILOPS,DEF_DROP)
                oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")
                verifyresponse = MSG_FALSE
                keywordresult = MSG_FAIL
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_DROP,keywordresult)

        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_BUTTONOPS,DEF_CLICK,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_BUTTONOPS,DEF_CLICK,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_BUTTONOPS,DEF_CLICK,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to check given object is enabled
    def verifyenabled(self,acc):
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_UTILOPS,DEF_VERIFYENABLED)
            objstates = curaccinfo.states
            if 'enabled' in objstates:
                verifyresponse = MSG_TRUE
                keywordresult = MSG_PASS
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYENABLED,keywordresult)
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s %s',OEBS_UTILOPS,DEF_VERIFYENABLED)
                oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")
                verifyresponse = MSG_FALSE
                keywordresult = MSG_FAIL
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYENABLED,keywordresult)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYENABLED,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYENABLED,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYENABLED,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Verify Response %s',OEBS_UTILOPS,DEF_VERIFYENABLED,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to check given object is disabled
    def verifydisabled(self,acc):
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_UTILOPS,DEF_VERIFYDISABLED)
            objstates = curaccinfo.states
            if 'enabled' in objstates:
                verifyresponse = MSG_FALSE
                keywordresult = MSG_FAIL
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYDISABLED,keywordresult)
                oebs_key_objects.custom_msg.append("ERR_OBJECT_ENABLED")
            else:
                verifyresponse = MSG_TRUE
                keywordresult= MSG_PASS
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYDISABLED,keywordresult)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYDISABLED,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYDISABLED,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYDISABLED,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Verify Response %s',OEBS_UTILOPS,DEF_VERIFYDISABLED,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

    #Method to check given object is visible
    def verifyvisible(self,acc):
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_UTILOPS,DEF_VERIFYVISIBLE)
            objstates = curaccinfo.states
            x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
            y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
            #Visibility check for scrollbar
            if(self.getObjectVisibility(acc,x_coor,y_coor)):
                if 'visible' in objstates:
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYVISIBLE,keywordresult)
                else:
                    verifyresponse = MSG_FALSE
                    keywordresult=MSG_FAIL
                    oebs_key_objects.custom_msg.append("ERR_HIDDEN_OBJECT")
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYVISIBLE,keywordresult)
            else:
                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_UTILOPS,DEF_VERIFYVISIBLE,MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYVISIBLE,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYVISIBLE,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYVISIBLE,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Verify Response %s',OEBS_UTILOPS,DEF_VERIFYVISIBLE,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

    #Method to check given object is hidden
    def verifyhidden(self,acc):
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_UTILOPS,DEF_VERIFYHIDDEN)
            objstates = curaccinfo.states
            x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
            y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
            #Visibility check for scrollbar
            print 'Visibility',self.getObjectVisibility(acc,x_coor,y_coor)
            if(self.getObjectVisibility(acc,x_coor,y_coor)):
                print objstates
                if 'visible' and 'showing' in objstates:
                    verifyresponse = MSG_FALSE
                    keywordresult=MSG_FAIL
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYHIDDEN,keywordresult)
                    oebs_key_objects.custom_msg.append("ERR_OBJECT_VISIBLE")
                else:
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYHIDDEN,keywordresult)
            else:
                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_UTILOPS,DEF_VERIFYHIDDEN,MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
                verifyresponse = MSG_TRUE
                keywordresult=MSG_PASS

        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYHIDDEN,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYHIDDEN,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYHIDDEN,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Verify Response %s',OEBS_UTILOPS,DEF_VERIFYHIDDEN,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to check given object is verifyreadonly
    def verifyreadonly(self,acc):
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            currinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_UTILOPS,DEF_VERIFYREADONLY)
            objstates = currinfo.states
            children=''
            if(currinfo.role =='list'):
                children = currinfo.childrenCount
            else:
                listObj = self.utilities_obj.looptolist(acc)
                listContext = listObj.getAccessibleContextInfo()
                children=listContext.childrenCount
            childindex = 1
            if currinfo.role =='combo box':
                x_coor = int(currinfo.x + (0.5 * currinfo.width))
                y_coor = int(currinfo.y + (0.5 * currinfo.height))
                #oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                acc = self.utilities_obj.looptolist(acc)
                currinfo=acc.getAccessibleContextInfo()
                currentselection=0
                for selected in range(children):
                    labelobj=acc.getAccessibleChildFromContext(selected)
                    labelcontext=labelobj.getAccessibleContextInfo()
                    if 'selected' in labelcontext.states:
                        currentselection=labelcontext.indexInParent
                if currentselection == 0:
                    #x_coor = int(currinfo.x + (0.5 * currinfo.width))
                    #y_coor = int(currinfo.y + (0.5 * currinfo.height))
                    #Visibility check for scrollbar

                    if(self.getObjectVisibility(acc,x_coor,y_coor)):
                        oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                        oebs_keyboardops.KeyboardOperation('keypress','A_DOWN')
                        time.sleep(0.1)
                        requiredcontext=self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]")
                        listObj = self.utilities_obj.looptolist(requiredcontext)
                        childobj=listObj.getAccessibleChildFromContext(int(childindex))
                        childcontext=childobj.getAccessibleContextInfo()
                        if 'selected' in childcontext.states:
                            keywordresult = MSG_PASS
                            verifyresponse = MSG_TRUE
                        oebs_keyboardops.KeyboardOperation('keypress','ENTER')
                        time.sleep(0.4)
                        for selected in range(children):
                            labelobj=acc.getAccessibleChildFromContext(selected)
                            labelcontext=labelobj.getAccessibleContextInfo()
                            if 'selected' in labelcontext.states:
                                currentselection=labelcontext.indexInParent
                        if currentselection == 0:
                            oebs_key_objects.custom_msg.append(MSG_OBJECT_READONLY)
                            keywordresult = MSG_PASS
                            verifyresponse = MSG_TRUE
                        else:
                            oebs_keyboardops.KeyboardOperation('keypress','A_UP')
                            time.sleep(0.1)
                            requiredcontext=self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]")
                            listObj = self.utilities_obj.looptolist(requiredcontext)
                            childobj=listObj.getAccessibleChildFromContext(int(childindex))
                            childcontext=childobj.getAccessibleContextInfo()
                            if 'selected' in childcontext.states:
                                keywordresult = MSG_PASS
                                verifyresponse = MSG_TRUE
                            oebs_key_objects.custom_msg.append(MSG_OBJECT_SELECTABLE)
                    else:
                        logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_UTILOPS,DEF_VERIFYREADONLY,MSG_ELEMENT_NOT_VISIBLE)
                        oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
                else:
                    oebs_key_objects.custom_msg.append(MSG_OBJECT_SELECTABLE)
            elif 'enabled' in objstates:
                if 'editable' in objstates:
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYREADONLY,keywordresult)
                    oebs_key_objects.custom_msg.append(MSG_OBJECT_EDITABLE)
                else:
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYREADONLY,keywordresult)
            else:
                logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_UTILOPS,DEF_VERIFYREADONLY,MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYREADONLY,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYREADONLY,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYREADONLY,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Verify Response %s',OEBS_UTILOPS,DEF_VERIFYREADONLY,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

    #Method to get tool tip text
    def gettooltiptext(self,acc):
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult = MSG_FAIL
        keywordresponse=''
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_UTILOPS,DEF_GETTOOLTIPTEXT)
            keywordresponse = curaccinfo.description
            keywordresult = MSG_PASS
            oebs_key_objects.custom_msg.append("MSG_RESULT_IS")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_GETTOOLTIPTEXT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_GETTOOLTIPTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_GETTOOLTIPTEXT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(keywordresponse))

    #Method to verify tool tip text
    def verifytooltiptext(self,acc):
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_UTILOPS,DEF_VERIFYTOOLTIPTEXT)
            if len(oebs_key_objects.keyword_input) == 1:
                text=oebs_key_objects.keyword_input[0]
               # oebs_key_objects.custom_msg.append(str('User Input: ' + text))
                tooltiptext = curaccinfo.description
                if text == tooltiptext:
                    verifyresponse = MSG_TRUE
                    keywordresult = MSG_PASS
                else:
                    logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_UTILOPS,DEF_VERIFYTOOLTIPTEXT,MSG_INVALID_INPUT)
                   # oebs_key_objects.custom_msg.append(str('Verification failed \'' + tooltiptext + '\' not equal to \''+text+"\'."))
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYTOOLTIPTEXT,MSG_INVALID_INPUT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYTOOLTIPTEXT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYTOOLTIPTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYTOOLTIPTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Verify Response %s',OEBS_UTILOPS,DEF_VERIFYTOOLTIPTEXT,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to verify exists
    def verifyexists(self,acc):
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_UTILOPS,DEF_VERIFYEXISTS)
            if('showing' in curaccinfo.states and 'visible' in curaccinfo.states):
                verifyresponse = MSG_TRUE
                keywordresult = MSG_PASS
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYEXISTS,MSG_INVALID_INPUT)
                oebs_key_objects.custom_msg.append("ERR_HIDDEN_OBJECT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYEXISTS,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYEXISTS,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYEXISTS,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Verify Response %s',OEBS_UTILOPS,DEF_VERIFYEXISTS,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to verify does not exists
    def verifydoesnotexists(self,acc):
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            if(str(acc)!='fail'):
                curaccinfo = acc.getAccessibleContextInfo()
                logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_UTILOPS,DEF_VERIFYDOESNOTEXISTS)
                if(acc):
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYDOESNOTEXISTS,MSG_ELEMENT_EXIST)
                    oebs_key_objects.custom_msg.append(MSG_ELEMENT_EXIST)
                else:
                    verifyresponse = MSG_TRUE
                    keywordresult = MSG_PASS
            else:
                verifyresponse = MSG_TRUE
                keywordresult = MSG_PASS
        except Exception as e:
            verifyresponse = MSG_TRUE
            keywordresult = MSG_PASS
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_VERIFYDOESNOTEXISTS,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYDOESNOTEXISTS,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_VERIFYDOESNOTEXISTS,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Verify Response %s',OEBS_UTILOPS,DEF_VERIFYDOESNOTEXISTS,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to perform rightclick operation
    def rightclick(self,acc):
        del oebs_key_objects.custom_msg[:]
     	#sets the keywordResult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_UTILOPS,DEF_RIGHTCLICK)
            objstates = charinfo.states
            #x_coor = int(charinfo.x + (0.5 * charinfo.width))
            #y_coor = int(charinfo.y + (0.5 * charinfo.height))
            x_coor = int(charinfo.x + 25)
            y_coor = int(charinfo.y + 10)
            #Visibility check for scrollbar
            if(self.getObjectVisibility(acc,x_coor,y_coor)):
            #check for object enabled
                if 'enabled' in objstates:
                	logging.debug('FILE: %s , DEF: %s MSG: RightClick Happens on :%s , %s',OEBS_UTILOPS,DEF_RIGHTCLICK,x_coor,y_coor)
                	oebs_mouseops.MouseOperation('rightclick',x_coor,y_coor)
                	logging.debug('FILE: %s , DEF: %s MSG: RightClick Successful',OEBS_UTILOPS,DEF_RIGHTCLICK)
                	verifyresponse = MSG_TRUE
                	keywordresult=MSG_PASS
                else:
                    logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_UTILOPS,DEF_RIGHTCLICK,MSG_DISABLED_OBJECT)
                    oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")
            else:
                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_UTILOPS,DEF_RIGHTCLICK,MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_RIGHTCLICK,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_UTILOPS,DEF_RIGHTCLICK,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_UTILOPS,DEF_RIGHTCLICK,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #definition for switching from one internal frame to another
    def switchtoframe(self,acc):
        global activeframes
        activeframes=[]
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            framecontext=acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_UTILOPS,DEF_SWITCHTOFRAME)
            failflag = -1
            if len(oebs_key_objects.keyword_input) == 1:
                #checks if the text is empty
                if (oebs_key_objects.keyword_input[0] != ''):
                    framename = oebs_key_objects.keyword_input[0]
                    logging.debug('FILE: %s , DEF: %s MSG: %s is the frame name.',OEBS_UTILOPS,DEF_SWITCHTOFRAME,framename)
                    menuobj=self.utilities_obj.menugenerator(acc)
                    self.getactiveframes(acc)
                    activeframelist=[]
                    for activeframeindex in range(len(activeframes)):
                        if  str(activeframes[activeframeindex]).startswith(framename):
                            activeframelist.append(activeframes[activeframeindex])
                    activeframelist=list(reversed(activeframelist))
                    if(len(activeframelist) !=0):
                        menubarcontext=menuobj.getAccessibleContextInfo()
                        for childindex in range(menubarcontext.childrenCount):
                            menuchildobj = menuobj.getAccessibleChildFromContext(childindex)
                            menuchildcontext=menuchildobj.getAccessibleContextInfo()
                            if 'window' in str(menuchildcontext.name).lower():
                                x_coormenu = int(menuchildcontext.x + (0.5 * menuchildcontext.width))
                                y_coormenu = int(menuchildcontext.y + (0.5 * menuchildcontext.height))
                                oebs_mouseops.MouseOperation('click',x_coormenu,y_coormenu)
                                time.sleep(2)
                                menuchildcontext=menuchildobj.getAccessibleContextInfo()
                                for windowchildren in range (menuchildcontext.childrenCount):
                                    windowobj=menuchildobj.getAccessibleChildFromContext(windowchildren)
                                    windowcontext=windowobj.getAccessibleContextInfo()
                                    if len(windowcontext.name) != 0:
                                        if str(activeframelist[0]) in windowcontext.name:
                                            x_coor = int(windowcontext.x + (0.5 * windowcontext.width))
                                            y_coor = int(windowcontext.y + (0.5 * windowcontext.height))
                                            oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                                            failflag = 0
                                            break
                                        else:
                                            failflag = 1
                                else:
                                    if failflag != 0:
                                        failflag = -1
                        if failflag == 1 :
                            logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_UTILOPS,DEF_SWITCHTOFRAME,MSG_INVALID_INPUT)
                            oebs_key_objects.custom_msg.append("Switch to Frame Failed.")
                        elif failflag == -1 :
                            logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_UTILOPS,DEF_SWITCHTOFRAME,MSG_INVALID_INPUT)
                            oebs_key_objects.custom_msg.append("Switch to Frame Failed.")
                            oebs_mouseops.MouseOperation('click',x_coormenu,y_coormenu)
                        elif failflag == 0:
                            #sets the verifyresponse to TRUE
                            verifyresponse = MSG_TRUE
                            #sets the keywordresult to pass
                            keywordresult=MSG_PASS
                        else:
                            logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_UTILOPS,DEF_SWITCHTOFRAME,MSG_INVALID_INPUT)
                            oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
                    else:
                        logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_UTILOPS,DEF_SWITCHTOFRAME,MSG_INVALID_NOOF_INPUT)
                        oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
                else:
                    logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_UTILOPS,DEF_SWITCHTOFRAME,MSG_INVALID_NOOF_INPUT)
                    oebs_key_objects.custom_msg.append("ERR_INVALID_NO_INPUT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_SWITCHTOFRAME,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_SWITCHTOFRAME,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_SWITCHTOFRAME,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Verify Response %s',OEBS_UTILOPS,DEF_SWITCHTOFRAME,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))



    def getactiveframes(self,frameobj):
        framecontext=frameobj.getAccessibleContextInfo()
        for index in range(framecontext.childrenCount):
            elementobj=frameobj.getAccessibleChildFromContext(index)
            elementcontext=elementobj.getAccessibleContextInfo()
            if elementcontext.role == 'desktop pane':
                for desktopindex in range(elementcontext.childrenCount):
                    desktopchildobj = elementobj.getAccessibleChildFromContext(desktopindex)
                    desktopchildcontext=desktopchildobj.getAccessibleContextInfo()
                    if 'visible' and 'showing' in desktopchildcontext.states:
                        global activeframes
                        activeframes.append(desktopchildcontext.name)
                break
            else:
                self.getactiveframes(elementobj)

    #Visibility check for scrollbar
    def getObjectVisibility(self,acc,x_coor,y_coor):
        try:
            localacc = self.viewportacc(acc)
            if(localacc):
                curaccinfo1 = localacc.getAccessibleContextInfo()
                x1_coor = curaccinfo1.x
                y1_coor = curaccinfo1.y
                x2_coor = curaccinfo1.x+curaccinfo1.width
                y2_coor = curaccinfo1.y+curaccinfo1.height
                if(( x_coor > x1_coor and x_coor < x2_coor)and(y_coor > y1_coor and y_coor < y2_coor)):
                    return True
                else:
                    return False
            else:
                return True

        except Exception as e:
            return True


    #parent access context
    def viewportacc(self,acc):
        global accontext
        count = 0
        accontext = ''
        parentacc = acc.getAccessibleParentFromContext()
        if(parentacc):
            parentinfo = parentacc.getAccessibleContextInfo()

            if(parentinfo.role == 'viewport'):
                #global accContext
                accontext = parentacc
                count+=1
            if(count==0):
                self.viewportacc(parentacc)
        return accontext


    #Method for send function keys
    def sendfunctionkeys(self,acc):
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_UTILOPS,DEF_SENDFUNCTIONKEYS)
            string = oebs_key_objects.keyword_input[0]
            for i in range(len(string)):
                if string[i].isalpha():
                    if string[i].isupper():
                        oebs_keyboardops.KeyboardOperation('keypress','CAPSLOCK')
                        oebs_keyboardops.KeyboardOperation('keypress',string[i])
                        oebs_keyboardops.KeyboardOperation('keypress','CAPSLOCK')
                        keywordresult = MSG_PASS
                        verifyresponse = MSG_TRUE
                    else:
                        val = string[i].upper()
                        oebs_keyboardops.KeyboardOperation('keypress',val)
                        keywordresult = MSG_PASS
                        verifyresponse = MSG_TRUE
                elif string[i].isdigit():
                    oebs_keyboardops.KeyboardOperation('keypress',string[i])
                    keywordresult = MSG_PASS
                    verifyresponse = MSG_TRUE
                else:
                    if string[i] in oebs_constants.SENDFUNCTION_KEYS_DICT:
                        oebs_keyboardops.KeyboardOperation('keydown','SHIFT')
                        oebs_keyboardops.KeyboardOperation('keypress',oebs_constants.SENDFUNCTION_KEYS_DICT[string[i]])
                        oebs_keyboardops.KeyboardOperation('keyup','SHIFT')
                        keywordresult = MSG_PASS
                        verifyresponse = MSG_TRUE
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_UTILOPS,DEF_SENDFUNCTIONKEYS,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_SENDFUNCTIONKEYS,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_UTILOPS,DEF_SENDFUNCTIONKEYS,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Verify Response %s',OEBS_UTILOPS,DEF_SENDFUNCTIONKEYS,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

