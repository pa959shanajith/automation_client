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
from oebs_constants import *
import logger

log = logging.getLogger('oebs_radiocheckboxops.py')

class RadioCheckboxOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()
        self.utilops_obj=UtilOperations()

    #Method to select radio button
    def selectradiobutton(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
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
                        logger.print_on_console(MSG_OBJECTSELECTED)
                        status=TEST_RESULT_PASS
                    else:
                        oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                        time.sleep(2)
                        methodoutput = TEST_RESULT_TRUE
                        status=TEST_RESULT_PASS
                else:
                    err_msg = MSG_DISABLED_OBJECT
                    log.debug('MSG:%s',err_msg)
                    logger.print_on_console(err_msg)
            else:
                err_msg = MSG_ELEMENT_NOT_VISIBLE
                log.debug('MSG:%s',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_select_radiobutton']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Result %s',methodoutput)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to select checkbox
    def selectcheckbox(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
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
                        methodoutput = TEST_RESULT_TRUE
                        status=TEST_RESULT_PASS
                    else:
                        oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                        time.sleep(2)
                        curaccinfo = acc.getAccessibleContextInfo()
                        objstates = curaccinfo.states
                        if 'checked' in objstates:
                            methodoutput = TEST_RESULT_TRUE
                            status=TEST_RESULT_PASS
                        else:
                            err_msg = MSG_OBJECT_READONLY
                            log.debug('%s',err_msg)
                            logger.print_on_console(err_msg)
                else:
                    err_msg = MSG_DISABLED_OBJECT
                    log.debug('%s',err_msg)
                    logger.print_on_console(err_msg)
            else:
                err_msg = MSG_ELEMENT_NOT_VISIBLE
                log.debug('MSG:%s',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_select_checkbox']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Result %s',methodoutput)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to un-select checkbox
    def unselectcheckbox(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
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
                            err_msg = MSG_OBJECT_READONLY
                            log.debug('%s',err_msg)
                            logger.print_on_console(err_msg)
                        else:
                            methodoutput = TEST_RESULT_TRUE
                            status=TEST_RESULT_PASS
                    else:
                        methodoutput = TEST_RESULT_TRUE
                        status=TEST_RESULT_PASS
                else:
                    err_msg = MSG_DISABLED_OBJECT
                    log.debug('Object is disabled',err_msg)
                    logger.print_on_console(err_msg)
            else:
                err_msg = MSG_ELEMENT_NOT_VISIBLE
                log.debug('MSG:%s',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_unselect_checkbox']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Result %s',methodoutput)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    def getstatus(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = ''
        output_res = OUTPUT_CONSTANT
        err_msg = None
        flag = ''
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_GETSTATUS)
            objstates = curaccinfo.states
            radiocheckboxrole = curaccinfo.role
            if radiocheckboxrole == 'check box':
                if 'checked' in objstates:
                    status=TEST_RESULT_PASS
                    flag = 'Checked'
                    methodoutput = flag
                else:
                    status=TEST_RESULT_PASS
                    flag = 'UnChecked'
                    methodoutput = flag
            elif radiocheckboxrole == 'radio button':
                if 'checked' in objstates:
                    status=TEST_RESULT_PASS
                    flag = 'Selected'
                    methodoutput = flag
                else:
                    status=TEST_RESULT_PASS
                    flag = 'UnSelected'
                    methodoutput = flag
            elif radiocheckboxrole == 'push button':
                    flag=objstates
                    status=TEST_RESULT_PASS
                    methodoutput = flag
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_status']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Result %s',methodoutput)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

