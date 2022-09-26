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

from oebs_constants import *
import oebs_key_objects
import oebs_serverUtilities
import logging
import oebs_mouseops
from oebs_keyboardops import KeywordOperations
import time
import logger
global activeframes
import ast
import oebs_api
from oebs_utils import Utils
activeframes=[]

log = logging.getLogger('oebs_utilops.py')

class UtilOperations:

    def __init__(self):
        self.utilities_obj = oebs_serverUtilities.Utilities()
        self.keyboardops = KeywordOperations()
        self.utils_obj = Utils()

    #Method to setfocus on the User given Object
    def setfocus(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
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
                    acc.requestFocus()
                    methodoutput = TEST_RESULT_TRUE
                    status=TEST_RESULT_PASS
                    log.debug('%s %s',MSG_RESULT_IS,status)
                else:
                    log.debug('%s %s',MSG_RESULT_IS,status)
                    logger.print_on_console(MSG_INVALID_OBJECT)
                    err_msg = MSG_INVALID_OBJECT
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                logger.print_on_console(MSG_ELEMENT_NOT_VISIBLE)
                err_msg = MSG_ELEMENT_NOT_VISIBLE
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_set_focus']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    def drag(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
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
                if curaccinfo.role == "panel":
                    x_cor = x1
                    y_cor = y1
                oebs_mouseops.MouseOperation('hold',x_cor,y_cor)
                methodoutput = TEST_RESULT_TRUE
                status = TEST_RESULT_PASS
                log.debug('%s',status)
            else:
                log.debug('%s %s',DEF_DRAG)
                logger.print_on_console(MSG_DISABLED_OBJECT)
                err_msg = MSG_DISABLED_OBJECT
                methodoutput = TEST_RESULT_FAIL
                status = TEST_RESULT_FAIL
                log.debug('%s',status)

        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_drag']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',status)
        log.debug('Status: %s',status)
        return status,methodoutput,output_res,err_msg

    def drop(self,acc):
        err_msg = None
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
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

                methodoutput = TEST_RESULT_TRUE
                status = TEST_RESULT_PASS
                log.debug('%s',status)
            else:
                log.debug('%s %s',DEF_DROP)
                err_msg = MSG_DISABLED_OBJECT
                logger.print_on_console(MSG_DISABLED_OBJECT)
                methodoutput = TEST_RESULT_FAIL
                status = TEST_RESULT_FAIL
                log.debug('%s',status)

        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_drop']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',status)
        log.debug('Status: %s',status)
        return status, methodoutput, output_res, err_msg

    def mousehover(self,acc):
        status=TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
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
                #converting the float to int:
                x_cor = int(x_cor)
                y_cor = int(y_cor)
                #x_cor = x2
                #y_cor = y2
                print(x_cor)
                oebs_mouseops.MouseOperation('move',x_cor,y_cor)
                methodoutput = TEST_RESULT_TRUE
                status = TEST_RESULT_PASS
                log.debug('%s',status)
            else:
                log.debug('%s %s',DEF_DRAG)
                err_msg = MSG_DISABLED_OBJECT
                logger.print_on_console(MSG_DISABLED_OBJECT)
                methodoutput = TEST_RESULT_FAIL
                status = TEST_RESULT_FAIL
                log.debug('%s',status)

        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_mouse_hover']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',status)
        log.debug('Status: %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to check given object is enabled
    def verifyenabled(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_VERIFYENABLED)
            objstates = curaccinfo.states
            if 'enabled' in objstates:
                methodoutput = TEST_RESULT_TRUE
                status = TEST_RESULT_PASS
                log.debug('%s',status)
            else:
                log.debug('%s %s',DEF_VERIFYENABLED)
                err_msg = MSG_DISABLED_OBJECT
                logger.print_on_console(MSG_DISABLED_OBJECT)
                methodoutput = TEST_RESULT_FAIL
                status = TEST_RESULT_FAIL
                log.debug('%s',status)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_enabled']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        log.debug('Verify Response %s',str(methodoutput))
        return status,methodoutput,output_res,err_msg

    #Method to check given object is disabled
    def verifydisabled(self,acc):
        status=TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_VERIFYDISABLED)
            objstates = curaccinfo.states
            if 'enabled' in objstates:
                methodoutput = TEST_RESULT_FAIL
                status = TEST_RESULT_FAIL
                log.debug('%s',status)
                err_msg = MSG_OBJECT_ENABLED
            else:
                methodoutput = TEST_RESULT_TRUE
                status= TEST_RESULT_PASS
                log.debug('%s',status)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_disabled']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        log.debug('Verify Response %s',str(methodoutput))
        return status,methodoutput,output_res,err_msg

    #Method to check given object is visible
    def verifyvisible(self,acc):
        status=TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
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
                    methodoutput = TEST_RESULT_TRUE
                    status=TEST_RESULT_PASS
                    log.debug('%s',status)
                else:
                    methodoutput = TEST_RESULT_FAIL
                    status=TEST_RESULT_FAIL
                    err_msg = MSG_HIDDEN_OBJECT
                    logger.print_on_console(MSG_HIDDEN_OBJECT)
                    log.debug('%s',status)
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                logger.print_on_console(MSG_ELEMENT_NOT_VISIBLE)
                err_msg = MSG_ELEMENT_NOT_VISIBLE
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_visible']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        log.debug('Verify Response %s',str(methodoutput))
        return status,methodoutput,output_res,err_msg

    #Method to check given object is hidden
    def verifyhidden(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_VERIFYHIDDEN)
            objstates = curaccinfo.states
            x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
            y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
            #Visibility check for scrollbar
            if(self.getObjectVisibility(acc,x_coor,y_coor)):
                if 'visible' and 'showing' in objstates:
                    methodoutput = TEST_RESULT_FAIL
                    status=TEST_RESULT_FAIL
                    log.debug('%s',status)
                    err_msg = MSG_OBJECT_VISIBLE
                else:
                    methodoutput = TEST_RESULT_TRUE
                    status=TEST_RESULT_PASS
                    log.debug('%s',status)
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                err_msg = MSG_ELEMENT_NOT_VISIBLE
                logger.print_on_console(MSG_ELEMENT_NOT_VISIBLE)
                methodoutput = TEST_RESULT_TRUE
                status=TEST_RESULT_PASS

        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_hidden']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        log.debug('Verify Response %s',str(methodoutput))
        return status,methodoutput,output_res,err_msg

    #Method to check given object is verifyreadonly
    def verifyreadonly(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
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
                    if(self.getObjectVisibility(acc,x_coor,y_coor)):
                        oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                        self.keyboardops.keyboard_operation('keypress','A_DOWN')
                        time.sleep(0.1)
                        requiredcontext, visible, active_parent = self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]",oebs_key_objects.object_type)
                        listObj = self.utilities_obj.looptolist(requiredcontext)
                        childobj=listObj.getAccessibleChildFromContext(int(childindex))
                        childcontext=childobj.getAccessibleContextInfo()
                        if 'selected' in childcontext.states:
                            status = TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                        self.keyboardops.keyboard_operation('keypress','ENTER')
                        time.sleep(0.4)
                        for selected in range(children):
                            labelobj=acc.getAccessibleChildFromContext(selected)
                            labelcontext=labelobj.getAccessibleContextInfo()
                            if 'selected' in labelcontext.states:
                                currentselection=labelcontext.indexInParent
                        if currentselection == 0:
                            status = TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                        else:
                            self.keyboardops.keyboard_operation('keypress','A_UP')
                            time.sleep(0.1)
                            requiredcontext, visible, active_parent = self.utilities_obj.object_generator(oebs_key_objects.applicationname,oebs_key_objects.xpath,oebs_key_objects.keyword,"[\"\"]","[\"\"]",oebs_key_objects.object_type)
                            listObj = self.utilities_obj.looptolist(requiredcontext)
                            childobj=listObj.getAccessibleChildFromContext(int(childindex))
                            childcontext=childobj.getAccessibleContextInfo()
                            if 'selected' in childcontext.states:
                                status = TEST_RESULT_PASS
                                methodoutput = TEST_RESULT_TRUE
                            methodoutput = MSG_OBJECT_SELECTABLE
                    else:
                        log.debug('MSG:%s',DEF_VERIFYREADONLY,MSG_ELEMENT_NOT_VISIBLE)
                        logger.print_on_console(MSG_ELEMENT_NOT_VISIBLE)
                        err_msg = MSG_ELEMENT_NOT_VISIBLE
                else:
                    methodoutput = MSG_OBJECT_SELECTABLE
            elif 'enabled' in objstates:
                if 'editable' in objstates:
                    log.debug('%s',DEF_VERIFYREADONLY,status)
                    methodoutput = MSG_OBJECT_EDITABLE
                else:
                    methodoutput = TEST_RESULT_TRUE
                    status=TEST_RESULT_PASS
                    log.debug('%s',DEF_VERIFYREADONLY,status)
            else:
                log.debug('Object Disabled',DEF_VERIFYREADONLY,MSG_DISABLED_OBJECT)
                logger.print_on_console(MSG_DISABLED_OBJECT)
                err_msg = MSG_DISABLED_OBJECT
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_read_only']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',DEF_VERIFYREADONLY,e)
            log.debug('Status %s',DEF_VERIFYREADONLY,status)
        log.debug('Status %s',DEF_VERIFYREADONLY,status)
        log.debug('Verify Response %s',DEF_VERIFYREADONLY,str(methodoutput))
        return status,methodoutput,output_res,err_msg

    #Method to get tool tip text
    def gettooltiptext(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_GETTOOLTIPTEXT)
            methodoutput = curaccinfo.description
            status = TEST_RESULT_PASS
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_tooltip_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',DEF_GETTOOLTIPTEXT,e)
            log.debug('Status %s',DEF_GETTOOLTIPTEXT,status)
        log.debug('Status %s',DEF_GETTOOLTIPTEXT,status)
        return status,methodoutput,output_res,err_msg

    #Method to verify tool tip text
    def verifytooltiptext(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_VERIFYTOOLTIPTEXT)
            if len(oebs_key_objects.keyword_input) == 1:
                text=oebs_key_objects.keyword_input[0]
                # oebs_key_objects.custom_msg.append(str('User Input: ' + text))
                tooltiptext = curaccinfo.description
                if text == tooltiptext:
                    methodoutput = TEST_RESULT_TRUE
                    status = TEST_RESULT_PASS
                else:
                    log.debug('MSG:%s',DEF_VERIFYTOOLTIPTEXT,MSG_INVALID_INPUT)
                    logger.print_on_console(MSG_INVALID_INPUT)
                    err_msg = MSG_INVALID_INPUT
            else:
                log.debug('%s',DEF_VERIFYTOOLTIPTEXT,MSG_INVALID_INPUT)
                err_msg = MSG_INVALID_INPUT
                logger.print_on_console(MSG_INVALID_INPUT)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_tooltip_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',DEF_VERIFYTOOLTIPTEXT,e)
            log.debug('Status %s',DEF_VERIFYTOOLTIPTEXT,status)
        log.debug('Status %s',DEF_VERIFYTOOLTIPTEXT,status)
        log.debug('Verify Response %s',DEF_VERIFYTOOLTIPTEXT,str(methodoutput))
        return status,methodoutput,output_res,err_msg

    #Method to verify exists
    def verifyexists(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_VERIFYEXISTS)
            if('showing' in curaccinfo.states and 'visible' in curaccinfo.states):
                methodoutput = TEST_RESULT_TRUE
                status = TEST_RESULT_PASS
            else:
                log.debug('%s',DEF_VERIFYEXISTS,MSG_HIDDEN_OBJECT)
                logger.print_on_console(MSG_HIDDEN_OBJECT)
                err_msg = MSG_HIDDEN_OBJECT
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_exists']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',DEF_VERIFYEXISTS,e)
            log.debug('Status %s',DEF_VERIFYEXISTS,status)
        log.debug('Status %s',DEF_VERIFYEXISTS,status)
        log.debug('Verify Response %s',DEF_VERIFYEXISTS,str(methodoutput))
        return status,methodoutput,output_res,err_msg

    #Method to verify does not exists
    def verifydoesnotexists(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            if(str(acc)!='fail'):
                curaccinfo = acc.getAccessibleContextInfo()
                log.debug('Received Object Context',DEF_VERIFYDOESNOTEXISTS)
                if(acc):
                    log.debug('%s',DEF_VERIFYDOESNOTEXISTS,MSG_ELEMENT_EXIST)
                    err_msg = MSG_ELEMENT_EXIST
                else:
                    methodoutput = TEST_RESULT_TRUE
                    status = TEST_RESULT_PASS
            else:
                methodoutput = TEST_RESULT_TRUE
                status = TEST_RESULT_PASS
        except Exception as e:
            methodoutput = TEST_RESULT_TRUE
            status = TEST_RESULT_PASS
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_not_exists']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.error('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',DEF_VERIFYDOESNOTEXISTS,status)
        log.debug('Verify Response %s',DEF_VERIFYDOESNOTEXISTS,str(methodoutput))
        return status,methodoutput,output_res,err_msg

    #Method to perform rightclick operation
    def rightclick(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
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
                    methodoutput = TEST_RESULT_TRUE
                    status=TEST_RESULT_PASS
                else:
                    log.debug('Object Disabled',MSG_DISABLED_OBJECT)
                    logger.print_on_console(MSG_DISABLED_OBJECT)
                    err_msg = MSG_DISABLED_OBJECT
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                logger.print_on_console(MSG_ELEMENT_NOT_VISIBLE)
                err_msg = MSG_ELEMENT_NOT_VISIBLE
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_right_click']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',status)
        log.debug('Status: %s',status)
        return status,methodoutput,output_res,err_msg

    #definition for switching from one internal frame to another
    def switchtoframe(self,applicationname,objectname,keyword,inputs,outputs,object_type):
        global activeframes
        activeframes=[]
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #input sent from the user
            inputs = ast.literal_eval(str(inputs))
            inputs = [n for n in inputs]
            oebs_key_objects.keyword_input = []
            for index in range(len(inputs)):
                oebs_key_objects.keyword_input.append(inputs[index])
            oebs_key_objects.keyword_output = outputs.split(';')
            isjavares, hwnd = self.utils_obj.isjavawindow(applicationname)
            acc=oebs_api.JABContext(hwnd)
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
                                oebs_mouseops.MouseOperation('hold',x_coormenu,y_coormenu)
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
                            err_msg = "Switch to Frame Failed"
                        elif failflag == -1 :
                            log.debug('MSG:%s',MSG_INVALID_INPUT)
                            err_msg = "Switch to Frame Failed"
                            oebs_mouseops.MouseOperation('click',x_coormenu,y_coormenu)
                        elif failflag == 0:
                            #sets the methodoutput to TRUE
                            methodoutput = TEST_RESULT_TRUE
                            #sets the status to pass
                            status=TEST_RESULT_PASS
                        else:
                            log.debug('MSG:%s',MSG_INVALID_INPUT)
                            logger.print_on_console(MSG_INVALID_INPUT)
                            err_msg = MSG_INVALID_INPUT
                    else:
                        log.debug('MSG:%s',MSG_INVALID_INPUT)
                        logger.print_on_console(MSG_INVALID_INPUT)
                        err_msg = MSG_INVALID_INPUT
                else:
                    log.debug('MSG:%s',MSG_INVALID_NOOF_INPUT)
                    logger.print_on_console(MSG_INVALID_NOOF_INPUT)
                    err_msg = MSG_INVALID_INPUT
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_switch_frame']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        log.debug('Verify Response %s',str(methodoutput))
        return status,methodoutput,output_res,err_msg

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

    def internal_setfocus(self,acc):
        try:
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context','internal_setfocus')
            x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
            y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
            log.debug('Formula Created','internal_setfocus')
            #Visibility check for scrollbar
            if(self.getObjectVisibility(acc,x_coor,y_coor)):
                if ('showing' or 'focusable') in curaccinfo.states:
                    oebs_mouseops.MouseOperation('move',x_coor,y_coor)
                else:
                    log.error('Not focusable')
        except Exception as e:
            log.error(e)

    #Method for send function keys
    def sendfunctionkeys(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_SENDFUNCTIONKEYS)
            self.internal_setfocus(acc)
            string = str(oebs_key_objects.keyword_input[0])
            count=1
            if len(oebs_key_objects.keyword_input)>1:
                count=oebs_key_objects.keyword_input[1]
                try:
                    count=int(float(count))
                except Exception as e:
                    log.error(e)
                    err_msg = MSG_INVALID_FORMAT_INPUT
            if string!=None and string.strip() != '':
                for i in range(count):
                    import time
                    time.sleep(0.5)
                    res=self.keyboardops.keyboard_operation_sendfunctionkeys('keypress',string)
                    if res:
                        status = TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
            else:
                logger.print_on_console(MSG_INVALID_INPUT)
                err_msg = MSG_INVALID_INPUT

        #    for i in range(len(string)):
        #        if string[i].isalpha():
        #            if string[i].isupper():
        #                self.keyboardops.keyboard_operation('keypress','CAPSLOCK')
        #                self.keyboardops.keyboard_operation('keypress',string[i])
        #                self.keyboardops.keyboard_operation('keypress','CAPSLOCK')

        #                status = TEST_RESULT_PASS
        #                methodoutput = TEST_RESULT_TRUE
        #            else:
        #                val = string[i].upper()
        #                self.keyboardops.keyboard_operation('keypress',val)
        #                status = TEST_RESULT_PASS
        #                methodoutput = TEST_RESULT_TRUE
        #        elif string[i].isdigit():
        #            self.keyboardops.keyboard_operation('keypress',string[i])
        #            status = TEST_RESULT_PASS
        #            methodoutput = TEST_RESULT_TRUE
        #        else:
        #            if string[i] in oebs_constants.SENDFUNCTION_KEYS_DICT:
        #                self.keyboardops.keyboard_operation('keydown','SHIFT')
        #                self.keyboardops.keyboard_operation('keypress',oebs_constants.SENDFUNCTION_KEYS_DICT[string[i]])
        #                self.keyboardops.keyboard_operation('keyup','SHIFT')
        #                status = TEST_RESULT_PASS
        #                methodoutput = TEST_RESULT_TRUE
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_send_function']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        log.debug('Verify Response %s',str(methodoutput))
        return status,methodoutput,output_res,err_msg

    def select_menu(self,applicationname,objectname,keyword,inputs,outputs,object_type):
        """
        def : select_menu
        purpose : select menu is used to select the menu items.
        param  : inputs : 1. Heirarchy of the menu item 
        return : pass,true / fail,false
        """

        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FAIL
        output_res = OUTPUT_CONSTANT
        err_msg = None
        
        try:
            #input sent from the user
            inputs = ast.literal_eval(str(inputs))
            inputs = [n for n in inputs]
            oebs_key_objects.keyword_input = []
            for index in range(len(inputs)):
                oebs_key_objects.keyword_input.append(inputs[index])
            oebs_key_objects.keyword_output = outputs.split(';')
            isjavares, hwnd = self.utils_obj.isjavawindow(applicationname)
            acc=oebs_api.JABContext(hwnd)

            if len(oebs_key_objects.keyword_input) > 0:
                global counter,flag1,flag2
                counter = 0
                flag1 = flag2 =  False
                menuobj=self.utilities_obj.menugenerator(acc)

                def search_in_menu(menu_obj):
                    global counter,flag1,flag2
                    try:
                        menubarcontext=menu_obj.getAccessibleContextInfo()
                        for childindex in range(menubarcontext.childrenCount):
                            menuchildobj = menu_obj.getAccessibleChildFromContext(childindex)
                            menuchildcontext=menuchildobj.getAccessibleContextInfo()
                            if oebs_key_objects.keyword_input[counter].lower() not in str(menuchildcontext.name).lower():
                                flag1 = False
                            elif oebs_key_objects.keyword_input[counter].lower() in str(menuchildcontext.name).lower():
                                x_coormenu = int(menuchildcontext.x + (0.5 * menuchildcontext.width))
                                y_coormenu = int(menuchildcontext.y + (0.5 * menuchildcontext.height))
                                if menuchildcontext.role != 'menu item':
                                    oebs_mouseops.MouseOperation('hold',x_coormenu,y_coormenu)
                                else:
                                    oebs_mouseops.MouseOperation('hold',menuchildcontext.x + 10,y_coormenu)
                                time.sleep(2)
                                flag1 = True
                                counter += 1
                                if counter < len(oebs_key_objects.keyword_input):
                                    search_in_menu(menuchildobj)
                                else:
                                    if menuchildcontext.role != 'menu item':
                                        oebs_mouseops.MouseOperation('click',x_coormenu,y_coormenu)
                                    else:
                                        oebs_mouseops.MouseOperation('click',menuchildcontext.x + 10,y_coormenu)
                                    flag2 = True
                                    break
                            if flag2:
                                    break
                    except Exception as e:
                        err_msg = ERROR_CODE_DICT['err_select_menu']
                        logger.print_on_console(err_msg)
                        log.error(err_msg)
                        log.debug('%s',e)
                
                search_in_menu(menuobj)

                if flag1 == True and flag2 == True:
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
                elif flag1 != False or flag2 == False:
                    err_msg = ERROR_CODE_DICT['err_select_menu']

            if err_msg:
                log.info(err_msg)
                logger.print_on_console (err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_select_menu']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
        return status,methodoutput,output_res,err_msg