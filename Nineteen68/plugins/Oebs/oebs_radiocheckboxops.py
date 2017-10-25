#-------------------------------------------------------------------------------
# Name:        oebs_radiocheckboxops.py
# Purpose:     This file contains the script to perform actions on radio button and checkbox Objects.
#
# Author:      sushma.p
#
# Created:     24-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import oebs_key_objects
import oebs_mouseops
import logging
import oebs_serverUtilities
from oebs_utilops import UtilOperations
import time
from oebs_msg import *

log = logging.getLogger('oebs_radiocheckboxops.py')

class RadioCheckboxOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()
        self.utilops_obj=UtilOperations()

    #Method to select radio button
    def selectradiobutton(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            objstates = curaccinfo.states
            log.debug('Received Object Context',DEF_SELECTRADIOBUTTON)
            x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
            y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
            #visibility check for scrollbar
            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
                #check for object enabled
                if 'enabled' in objstates:
                    if 'checked' in objstates:
                        log.debug('%s',MSG_OBJECTSELECTED)
                        oebs_key_objects.custom_msg.append(MSG_OBJECTSELECTED)
                    else:
                        oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                        time.sleep(2)
                        verifyresponse = MSG_TRUE
                        keywordresult=MSG_PASS
                else:
                   log.debug('MSG:%s',MSG_DISABLED_OBJECT)
                   oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Result %s',verifyresponse)
        log.debug('Status %s',keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to select checkbox
    def selectcheckbox(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            objstates = curaccinfo.states
            log.debug('Received Object Context',DEF_SELECTCHECKBOX)
            x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
            y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
            #Visibility check for scrollbar
            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
            #check for object enabled
                if 'enabled' in objstates:
                    if 'checked' in objstates:
                        log.debug('%s',MSG_OBJECTSELECTED)
                        oebs_key_objects.custom_msg.append(MSG_OBJECTSELECTED)
                    else:
                        oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                        time.sleep(2)
                        curaccinfo = acc.getAccessibleContextInfo()
                        objstates = curaccinfo.states
                        if 'checked' in objstates:
                            verifyresponse = MSG_TRUE
                            keywordresult=MSG_PASS
                        else:
                            log.debug('%s',MSG_OBJECT_READONLY)
                            oebs_key_objects.custom_msg.append(MSG_OBJECT_READONLY)
                else:
                    log.debug('%s',MSG_DISABLED_OBJECT)
                    oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Result %s',verifyresponse)
        log.debug('Status %s',keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

    #Method to un-select checkbox
    def unselectcheckbox(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            objstates = curaccinfo.states
            log.debug('Received Object Context',DEF_UNSELECTCHECKBOX)
            x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
            y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
            #Visibility check for scrollbar
            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
                #check for object enabled
                if 'enabled' in objstates:
                    if 'checked' in objstates:
                        oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                        time.sleep(2)
                        curaccinfo = acc.getAccessibleContextInfo()
                        objstates = curaccinfo.states
                        if 'checked' in objstates:
                            log.debug('%s',MSG_OBJECT_READONLY)
                            oebs_key_objects.custom_msg.append(MSG_OBJECT_READONLY)
                        else:
                            verifyresponse = MSG_TRUE
                            keywordresult=MSG_PASS
                    else:
                        oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                        time.sleep(2)
                        curaccinfo = acc.getAccessibleContextInfo()
                        objstates = curaccinfo.states
                        if 'checked' in objstates:
                            oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                            log.debug('%s',MSG_OBJECTUNSELECTED)
                            oebs_key_objects.custom_msg.append(MSG_OBJECTUNSELECTED)
                        else:
                            log.debug('%s',MSG_OBJECT_READONLY)
                            oebs_key_objects.custom_msg.append(MSG_OBJECT_READONLY)
                else:
                    log.debug('Object is disabled',MSG_DISABLED_OBJECT)
                    oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Result %s',verifyresponse)
        log.debug('Status %s',keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    def getstatus(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordResult to FAIL
        keywordresult=MSG_FAIL
        keywordresponse = ''
        flag = ''
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_GETSTATUS)
            objstates = curaccinfo.states
            radiocheckboxrole = curaccinfo.role
            if radiocheckboxrole == 'check box':
                if 'checked' in objstates:
                    keywordresult=MSG_PASS
                    flag = 'Checked'
                    keywordresponse = flag
                    oebs_key_objects.custom_msg.append("MSG_RESULT_IS")
                else:
                    keywordresult=MSG_PASS
                    flag = 'UnChecked'
                    keywordresponse = flag
                    oebs_key_objects.custom_msg.append("MSG_RESULT_IS")
            elif radiocheckboxrole == 'radio button':
                if 'checked' in objstates:
                    keywordresult=MSG_PASS
                    flag = 'Selected'
                    keywordresponse = flag
                    oebs_key_objects.custom_msg.append("MSG_RESULT_IS")
                else:
                    keywordresult=MSG_PASS
                    flag = 'UnSelected'
                    keywordresponse = flag
                    oebs_key_objects.custom_msg.append("MSG_RESULT_IS")
            elif radiocheckboxrole == 'push button':
                    flag=objstates
                    keywordresult=MSG_PASS
                    keywordresponse = flag
                    oebs_key_objects.custom_msg.append("MSG_RESULT_IS")
        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Result %s',keywordresponse)
        log.debug('Status %s',keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(keywordresponse))

