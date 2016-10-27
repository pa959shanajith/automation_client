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
import oebs_utilops
import time


class InternalFrameOperations:
    def closeframe(self,acc):
        del oebs_key_objects.custom_msg[:]
     	#sets the keywordResult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_INTERNALFRAMEOPS,DEF_CLOSEFRAME)
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
                        logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_INTERNALFRAMEOPS,DEF_CLOSEFRAME,MSG_DISABLED_OBJECT)
                        oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")


            else:
                logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_INTERNALFRAMEOPS,DEF_CLOSEFRAME,MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")

        except Exception as e:
            oebs_serverUtilities.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_INTERNALFRAMEOPS,DEF_CLOSEFRAME,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_INTERNALFRAMEOPS,DEF_CLOSEFRAME,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_INTERNALFRAMEOPS,DEF_CLOSEFRAME,keywordresult)
        # response is sent to the client
        oebs_serverUtilities.cleardata()
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
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMAXIMIZE)
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
                        logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMAXIMIZE,MSG_DISABLED_OBJECT)
                        oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")
            else:
                logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMAXIMIZE,MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")

        except Exception as e:
            oebs_serverUtilities.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMAXIMIZE,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMAXIMIZE,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMAXIMIZE,keywordresult)
        # response is sent to the client
        oebs_serverUtilities.cleardata()
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
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMINIMIZE)
            objstates = charinfo.states
            if 'enabled' in objstates:
                accessibleactionsinfo = acc.getAccessibleActions()
                actioncount = accessibleactionsinfo.actionsCount
                if('iconified' in objstates):
                    for i in range(actioncount):
                        actiontext = accessibleactionsinfo.actionInfo[i].name
                        if(str(actiontext) == 'Toggle Minimized'):
                            oebs_utilops.rightclick(acc)
                            oebs_keyboardops.KeyboardOperation('keypress','R')
                            verifyresponse = MSG_TRUE
                            keywordresult=MSG_PASS
                        else:
                            logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMINIMIZE,MSG_DISABLED_OBJECT)
                            oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")

                else:
                    for i in range(actioncount):
                        actiontext = accessibleactionsinfo.actionInfo[i].name
                        if(str(actiontext) == 'Toggle Minimized'):
                            oebs_utilops.rightclick(acc)
                            for i in range(0,4):
                                oebs_keyboardops.KeyboardOperation('keypress','A_DOWN')
                            oebs_keyboardops.KeyboardOperation('keypress','ENTER')
                            verifyresponse = MSG_TRUE
                            keywordresult=MSG_PASS
                        else:
                            logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMINIMIZE,MSG_DISABLED_OBJECT)
                            oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")

            else:
                logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMINIMIZE,MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")

        except Exception as e:
            oebs_serverUtilities.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMINIMIZE,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMINIMIZE,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMINIMIZE,keywordresult)
        # response is sent to the client
        oebs_serverUtilities.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))
