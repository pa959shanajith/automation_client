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
from oebs_constants import *
import logger
import oebs_key_objects
import oebsServer
import oebs_serverUtilities
import logging
import oebs_mouseops
import oebs_keyboardops
from oebs_keyboardops import KeywordOperations
import time

log = logging.getLogger('oebs_internalframeops.py')

class InternalFrameOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()


    def closeframe(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
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
                        methodoutput = TEST_RESULT_TRUE
                        status=TEST_RESULT_PASS
                    else:
                        err_msg = MSG_DISABLED_OBJECT
                        log.debug('Object Disabled',err_msg)
                        logger.print_on_console(err_msg)
            else:
                err_msg = MSG_DISABLED_OBJECT
                log.debug('Object Disabled',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_close_frame']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',status)
        log.debug('Status: %s',status)
        return status,methodoutput,output_res,err_msg

    def togglemaximize(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_TOGGLEMAXIMIZE)
            objstates = charinfo.states
            if 'enabled' in objstates:
                accessibleactionsinfo = acc.getAccessibleActions()
                found = False
                actioncount = accessibleactionsinfo.actionsCount
                for i in range(actioncount):
                    actiontext = accessibleactionsinfo.actionInfo[i].name
                    if(str(actiontext) == 'Toggle Maximized'):
                        found = True
                        acc.doAccessibleActions(i,'Toggle Maximized')
                        methodoutput = TEST_RESULT_TRUE
                        status=TEST_RESULT_PASS
                if not found:
                    err_msg = MSG_DISABLED_OBJECT
                    log.debug('Object Disabled',err_msg)
                    logger.print_on_console(err_msg)
            else:
                err_msg = MSG_DISABLED_OBJECT
                log.debug('Object Disabled',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_toggle_maxamize']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',status)
        log.debug('Status: %s',status)
        return status,methodoutput,output_res,err_msg

    def toggleminimize(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_TOGGLEMINIMIZE)
            objstates = charinfo.states
            keywordop_obj=KeywordOperations()
            if 'enabled' in objstates :
                from oebs_utilops import UtilOperations
                obj=UtilOperations()
                accessibleactionsinfo = acc.getAccessibleActions()
                actioncount = accessibleactionsinfo.actionsCount
                for i in range(actioncount):
                    found = False
                    actiontext = accessibleactionsinfo.actionInfo[i].name
                    if(str(actiontext) == 'Toggle Minimized'):
                        found = True
                        obj.rightclick(acc)
                        if('iconified' in objstates):
                            keywordop_obj.keyboard_operation('keypress','R')
                        else:
                            for i in range(0,4):
                                keywordop_obj.keyboard_operation('keypress','A_DOWN')
                            keywordop_obj.keyboard_operation('keypress','ENTER')
                        methodoutput = TEST_RESULT_TRUE
                        status=TEST_RESULT_PASS
                if not found:
                    err_msg = ERROR_CODE_DICT['err_minimize']
                    log.debug('Object Disabled',err_msg)
                    logger.print_on_console(err_msg)
            else:
                err_msg = MSG_DISABLED_OBJECT
                log.debug('Object Disabled',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_toggle_minimize']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',status)
        log.debug('Status: %s',status)
        return status,methodoutput,output_res,err_msg
