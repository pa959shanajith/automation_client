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

log = logging.getLogger('oebs_utilops.py')

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
            log.debug('Received Object Context',DEF_SETFOCUS)
            x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
            y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
            log.debug('Formula Created',DEF_SETFOCUS)
            #Visibility check for scrollbar
            if(self.getObjectVisibility(acc,x_coor,y_coor)):
                if ('showing' or 'focusable') in curaccinfo.states:
                    oebs_mouseops.MouseOperation('move',x_coor,y_coor)
                    keywordresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                    log.debug('%s %s',MSG_RESULT_IS,keywordresult)
                else:
                    log.debug('%s %s',MSG_RESULT_IS,keywordresult)
                    oebs_key_objects.custom_msg.append(MSG_INVALID_OBJECT)
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Status %s',keywordresult)
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
                log.debug('%s',keywordresult)
            else:
                log.debug('%s %s',DEF_DRAG)
                oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)
                verifyresponse = MSG_FALSE
                keywordresult = MSG_FAIL
                log.debug('%s',keywordresult)



        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status: %s',keywordresult)
        log.debug('Status: %s',keywordresult)
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
                log.debug('%s',keywordresult)
            else:
                log.debug('%s %s',DEF_DROP)
                oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)
                verifyresponse = MSG_FALSE
                keywordresult = MSG_FAIL
                log.debug('%s',keywordresult)

        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status: %s',keywordresult)
        log.debug('Status: %s',keywordresult)
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
            log.debug('Received Object Context',DEF_VERIFYENABLED)
            objstates = curaccinfo.states
            if 'enabled' in objstates:
                verifyresponse = MSG_TRUE
                keywordresult = MSG_PASS
                log.debug('%s',keywordresult)
            else:
                log.debug('%s %s',DEF_VERIFYENABLED)
                oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)
                verifyresponse = MSG_FALSE
                keywordresult = MSG_FAIL
                log.debug('%s',keywordresult)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Status %s',keywordresult)
        log.debug('Verify Response %s',str(verifyresponse))
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
            log.debug('Received Object Context',DEF_VERIFYDISABLED)
            objstates = curaccinfo.states
            if 'enabled' in objstates:
                verifyresponse = MSG_FALSE
                keywordresult = MSG_FAIL
                log.debug('%s',keywordresult)
                oebs_key_objects.custom_msg.append(MSG_OBJECT_ENABLED)
            else:
                verifyresponse = MSG_TRUE
                keywordresult= MSG_PASS
                log.debug('%s',keywordresult)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Status %s',keywordresult)
        log.debug('Verify Response %s',str(verifyresponse))
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
            log.debug('Received Object Context',DEF_VERIFYVISIBLE)
            objstates = curaccinfo.states
            x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
            y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
            #Visibility check for scrollbar
            if(self.getObjectVisibility(acc,x_coor,y_coor)):
                if 'visible' in objstates:
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                    log.debug('%s',keywordresult)
                else:
                    verifyresponse = MSG_FALSE
                    keywordresult=MSG_FAIL
                    oebs_key_objects.custom_msg.append(MSG_HIDDEN_OBJECT)
                    log.debug('%s',keywordresult)
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Status %s',keywordresult)
        log.debug('Verify Response %s',str(verifyresponse))
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
            log.debug('Received Object Context',DEF_VERIFYHIDDEN)
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
                    log.debug('%s',keywordresult)
                    oebs_key_objects.custom_msg.append(MSG_OBJECT_VISIBLE)
                else:
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                    log.debug('%s',keywordresult)
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
                verifyresponse = MSG_TRUE
                keywordresult=MSG_PASS

        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Status %s',keywordresult)
        log.debug('Verify Response %s',str(verifyresponse))
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
            log.debug('Received Object Context',DEF_VERIFYREADONLY)
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
                        self.keyboardops.keyboard_operation('keypress','A_DOWN')
                        time.sleep(0.1)
                        requiredcontext=self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]")
                        listObj = self.utilities_obj.looptolist(requiredcontext)
                        childobj=listObj.getAccessibleChildFromContext(int(childindex))
                        childcontext=childobj.getAccessibleContextInfo()
                        if 'selected' in childcontext.states:
                            keywordresult = MSG_PASS
                            verifyresponse = MSG_TRUE
                        self.keyboardops.keyboard_operation('keypress','ENTER')
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
                            self.keyboardops.keyboard_operation('keypress','A_UP')
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
                        log.debug('MSG:%s',DEF_VERIFYREADONLY,MSG_ELEMENT_NOT_VISIBLE)
                        oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
                else:
                    oebs_key_objects.custom_msg.append(MSG_OBJECT_SELECTABLE)
            elif 'enabled' in objstates:
                if 'editable' in objstates:
                    log.debug('%s',DEF_VERIFYREADONLY,keywordresult)
                    oebs_key_objects.custom_msg.append(MSG_OBJECT_EDITABLE)
                else:
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                    log.debug('%s',DEF_VERIFYREADONLY,keywordresult)
            else:
                log.debug('Object Disabled',DEF_VERIFYREADONLY,MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',DEF_VERIFYREADONLY,e)
            log.debug('Status %s',DEF_VERIFYREADONLY,keywordresult)
        log.debug('Status %s',DEF_VERIFYREADONLY,keywordresult)
        log.debug('Verify Response %s',DEF_VERIFYREADONLY,str(verifyresponse))
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
            log.debug('Received Object Context',DEF_GETTOOLTIPTEXT)
            keywordresponse = curaccinfo.description
            keywordresult = MSG_PASS
            oebs_key_objects.custom_msg.append("MSG_RESULT_IS")
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',DEF_GETTOOLTIPTEXT,e)
            log.debug('Status %s',DEF_GETTOOLTIPTEXT,keywordresult)
        log.debug('Status %s',DEF_GETTOOLTIPTEXT,keywordresult)
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
            log.debug('Received Object Context',DEF_VERIFYTOOLTIPTEXT)
            if len(oebs_key_objects.keyword_input) == 1:
                text=oebs_key_objects.keyword_input[0]
               # oebs_key_objects.custom_msg.append(str('User Input: ' + text))
                tooltiptext = curaccinfo.description
                if text == tooltiptext:
                    verifyresponse = MSG_TRUE
                    keywordresult = MSG_PASS
                else:
                    log.debug('MSG:%s',DEF_VERIFYTOOLTIPTEXT,MSG_INVALID_INPUT)
                   # oebs_key_objects.custom_msg.append(str('Verification failed \'' + tooltiptext + '\' not equal to \''+text+"\'."))
            else:
                log.debug('%s',DEF_VERIFYTOOLTIPTEXT,MSG_INVALID_INPUT)
                oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',DEF_VERIFYTOOLTIPTEXT,e)
            log.debug('Status %s',DEF_VERIFYTOOLTIPTEXT,keywordresult)
        log.debug('Status %s',DEF_VERIFYTOOLTIPTEXT,keywordresult)
        log.debug('Verify Response %s',DEF_VERIFYTOOLTIPTEXT,str(verifyresponse))
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
            log.debug('Received Object Context',DEF_VERIFYEXISTS)
            if('showing' in curaccinfo.states and 'visible' in curaccinfo.states):
                verifyresponse = MSG_TRUE
                keywordresult = MSG_PASS
            else:
                log.debug('%s',DEF_VERIFYEXISTS,MSG_INVALID_INPUT)
                oebs_key_objects.custom_msg.append(MSG_HIDDEN_OBJECT)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',DEF_VERIFYEXISTS,e)
            log.debug('Status %s',DEF_VERIFYEXISTS,keywordresult)
        log.debug('Status %s',DEF_VERIFYEXISTS,keywordresult)
        log.debug('Verify Response %s',DEF_VERIFYEXISTS,str(verifyresponse))
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
                log.debug('Received Object Context',DEF_VERIFYDOESNOTEXISTS)
                if(acc):
                    log.debug('%s',DEF_VERIFYDOESNOTEXISTS,MSG_ELEMENT_EXIST)
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
            log.error('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Status %s',DEF_VERIFYDOESNOTEXISTS,keywordresult)
        log.debug('Verify Response %s',DEF_VERIFYDOESNOTEXISTS,str(verifyresponse))
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
            log.debug('Received Object Context',DEF_RIGHTCLICK)
            objstates = charinfo.states
            #x_coor = int(charinfo.x + (0.5 * charinfo.width))
            #y_coor = int(charinfo.y + (0.5 * charinfo.height))
            x_coor = int(charinfo.x + 25)
            y_coor = int(charinfo.y + 10)
            #Visibility check for scrollbar
            if(self.getObjectVisibility(acc,x_coor,y_coor)):
            #check for object enabled
                if 'enabled' in objstates:
                	log.debug('RightClick Happens on :%s , %s',x_coor,y_coor)
                	oebs_mouseops.MouseOperation('rightclick',x_coor,y_coor)
                	log.debug('RightClick Successful',DEF_RIGHTCLICK)
                	verifyresponse = MSG_TRUE
                	keywordresult=MSG_PASS
                else:
                    log.debug('Object Disabled',MSG_DISABLED_OBJECT)
                    oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status: %s',keywordresult)
        log.debug('Status: %s',keywordresult)
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
            log.debug('Received Object Context',DEF_SWITCHTOFRAME)
            failflag = -1
            if len(oebs_key_objects.keyword_input) == 1:
                #checks if the text is empty
                if (oebs_key_objects.keyword_input[0] != ''):
                    framename = oebs_key_objects.keyword_input[0]
                    log.debug('%s is the frame name.',framename)
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
                            log.debug('MSG:%s',MSG_INVALID_INPUT)
                            oebs_key_objects.custom_msg.append("Switch to Frame Failed.")
                        elif failflag == -1 :
                            log.debug('MSG:%s',MSG_INVALID_INPUT)
                            oebs_key_objects.custom_msg.append("Switch to Frame Failed.")
                            oebs_mouseops.MouseOperation('click',x_coormenu,y_coormenu)
                        elif failflag == 0:
                            #sets the verifyresponse to TRUE
                            verifyresponse = MSG_TRUE
                            #sets the keywordresult to pass
                            keywordresult=MSG_PASS
                        else:
                            log.debug('MSG:%s',MSG_INVALID_INPUT)
                            oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)
                    else:
                        log.debug('MSG:%s',MSG_INVALID_NOOF_INPUT)
                        oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)
                else:
                    log.debug('MSG:%s',MSG_INVALID_NOOF_INPUT)
                    oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Status %s',keywordresult)
        log.debug('Verify Response %s',str(verifyresponse))
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
            log.debug('Received Object Context',DEF_SENDFUNCTIONKEYS)
            string = oebs_key_objects.keyword_input[0]
            for i in range(len(string)):
                if string[i].isalpha():
                    if string[i].isupper():
                        self.keyboardops.keyboard_operation('keypress','CAPSLOCK')
                        self.keyboardops.keyboard_operation('keypress',string[i])
                        self.keyboardops.keyboard_operation('keypress','CAPSLOCK')

                        keywordresult = MSG_PASS
                        verifyresponse = MSG_TRUE
                    else:
                        val = string[i].upper()
                        self.keyboardops.keyboard_operation('keypress','TAB')
                        keywordresult = MSG_PASS
                        verifyresponse = MSG_TRUE
                elif string[i].isdigit():
                    self.keyboardops.keyboard_operation('keypress',string[i])
                    keywordresult = MSG_PASS
                    verifyresponse = MSG_TRUE
                else:
                    if string[i] in oebs_constants.SENDFUNCTION_KEYS_DICT:
                        self.keyboardops.keyboard_operation('keydown','SHIFT')
                        self.keyboardops.keyboard_operation('keypress',oebs_constants.SENDFUNCTION_KEYS_DICT[string[i]])
                        self.keyboardops.keyboard_operation('keyup','SHIFT')
                        keywordresult = MSG_PASS
                        verifyresponse = MSG_TRUE
        except Exception as e:
            self.utilities_obj.cleardata()
            log.error('%s',e)
            log.debug('Status %s',keywordresult)
            oebs_key_objects.custom_msg.append(str(e))
        log.debug('Status %s',keywordresult)
        log.debug('Verify Response %s',str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

