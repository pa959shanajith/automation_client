#-------------------------------------------------------------------------------
# Name:        oebs_internalframeops.py
# Purpose:     keywords in this script enables to perform action on internalframe Objects.
#
# Author:      sushma.p
#
# Created:     24-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import oebs_api
import oebs_msg
from oebs_msg import *
import oebs_key_objects
import oebsServer
import oebs_serverUtilities
import logging
import oebs_mouseops
import oebs_keyboardops
from oebs_keyboardops import KeywordOperations
import oebs_utilops
import time

log = logging.getLogger('oebs_internalframeops.py')

class InternalFrameOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()


    def closeframe(self,acc):
        del oebs_key_objects.custom_msg[:]
     	#sets the keywordResult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_CLOSEFRAME)
            objstates = charinfo.states
            if 'enabled' in objstates:
                accessibleactionsinfo = acc.getAccessibleActions()
                actioncount = accessibleactionsinfo.actionsCount
                for i in range(actioncount):

                    actiontext = accessibleactionsinfo.actionInfo[i].name
                    if(str(actiontext) == 'Close Window'):
                        x1 = charinfo.x
                        x2 = charinfo.x + charinfo.width
                        y1 = charinfo.y
                        y2 = charinfo.y + charinfo.height
                        xcor = x2 - 10
                        ycor = y1 + 10
                        oebs_mouseops.MouseOperation('click',xcor,ycor)
                        verifyresponse = MSG_TRUE
                        keywordresult=MSG_PASS
                    else:
                        log.debug('Object Disabled',MSG_DISABLED_OBJECT)
                        oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)


            else:
                log.debug('Object Disabled',MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)

        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status: %s',keywordresult)
        log.debug('Status: %s',keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

    def togglemaximize(self,acc):
        del oebs_key_objects.custom_msg[:]
     	#sets the keywordResult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_TOGGLEMAXIMIZE)
            objstates = charinfo.states
            if 'enabled' in objstates:
                accessibleactionsinfo = acc.getAccessibleActions()
                actioncount = accessibleactionsinfo.actionsCount
                for i in range(actioncount):

                    actiontext = accessibleactionsinfo.actionInfo[i].name
                    if(str(actiontext) == 'Toggle Maximized'):
                        acc.doAccessibleActions(i,'Toggle Maximized')
                        verifyresponse = MSG_TRUE
                        keywordresult=MSG_PASS
                    else:
                        log.debug('Object Disabled',MSG_DISABLED_OBJECT)
                        oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)
            else:
                log.debug('Object Disabled',MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)

        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status: %s',keywordresult)
        log.debug('Status: %s',keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    def toggleminimize(self,acc):
        del oebs_key_objects.custom_msg[:]
     	#sets the keywordResult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_TOGGLEMINIMIZE)
            objstates = charinfo.states
            keywordop_obj=KeywordOperations()
            if 'enabled' in objstates:
                accessibleactionsinfo = acc.getAccessibleActions()
                actioncount = accessibleactionsinfo.actionsCount
                if('iconified' in objstates):
                    for i in range(actioncount):
                        actiontext = accessibleactionsinfo.actionInfo[i].name
                        if(str(actiontext) == 'Toggle Minimized'):
                            oebs_utilops.rightclick(acc)
                            keywordop_obj.KeyboardOperation('keypress','R')
                            verifyresponse = MSG_TRUE
                            keywordresult=MSG_PASS
                        else:
                            log.debug('Object Disabled',MSG_DISABLED_OBJECT)
                            oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)

                else:
                    for i in range(actioncount):
                        actiontext = accessibleactionsinfo.actionInfo[i].name
                        if(str(actiontext) == 'Toggle Minimized'):
                            oebs_utilops.rightclick(acc)
                            for i in range(0,4):
                                keywordop_obj.KeyboardOperation('keypress','A_DOWN')
                            keywordop_obj.KeyboardOperation('keypress','ENTER')
                            verifyresponse = MSG_TRUE
                            keywordresult=MSG_PASS
                        else:
                            log.debug('Object Disabled',MSG_DISABLED_OBJECT)
                            oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)

            else:
                log.debug('Object Disabled',MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)

        except Exception as e:
            self.utilities_obj.cleardata()
            log.debug('%s',e)
            log.debug('Status: %s',keywordresult)
        log.debug('Status: %s',keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))
