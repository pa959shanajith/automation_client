#-------------------------------------------------------------------------------
# Name:        oebs_scrollbarops.py
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
import time
import logger

log = logging.getLogger('oebs_scrollbarops.py')

class ScrollbarOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()

    def right(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_RIGHT)
            objstates = charinfo.states
            x1_cor = charinfo.x
            y1_cor = charinfo.y
            width = charinfo.width
            height = charinfo.height
            x2_cor = x1_cor+width
            y2_cor = y1_cor+height
            if len(oebs_key_objects.keyword_input) == 0 or oebs_key_objects.keyword_input[0]=='' or oebs_key_objects.keyword_input[0]==None or not oebs_key_objects.keyword_input[0].isdigit():
                err_msg = ERROR_CODE_DICT['invalid_input_scroll']
                log.info(err_msg)
                logger.print_on_console(err_msg)
            numofoperation = int(oebs_key_objects.keyword_input[0])
            if 'enabled' in objstates and not err_msg:
                    if(numofoperation > 0):
                        for i in range(numofoperation):
                            if(width>height):
                                x_cor = ((x2_cor-height)+x2_cor)/2
                                y_cor = (y1_cor+y2_cor)/2
                                oebs_mouseops.MouseOperation('click',int(x_cor),int(y_cor))
                                methodoutput = TEST_RESULT_TRUE
                                status=TEST_RESULT_PASS
                    else:
                        err_msg = MSG_INVALID_INPUT
                        log.debug('Invalid Input',err_msg)
                        logger.print_on_console(err_msg)
            elif not err_msg:
                err_msg = MSG_DISABLED_OBJECT
                log.debug('Object Disabled',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_right']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',status)
        log.debug('Status: %s',status)
        return status,methodoutput,output_res,err_msg

    def left(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_LEFT)
            objstates = charinfo.states
            x1_cor = charinfo.x
            y1_cor = charinfo.y
            width = charinfo.width
            height = charinfo.height
            x2_cor = x1_cor+width
            y2_cor = y1_cor+height
            if len(oebs_key_objects.keyword_input) == 0 or oebs_key_objects.keyword_input[0]=='' or oebs_key_objects.keyword_input[0]==None or not oebs_key_objects.keyword_input[0].isdigit():
                err_msg = ERROR_CODE_DICT['invalid_input_scroll']
                log.info(err_msg)
                logger.print_on_console(err_msg)
            numofoperation = int(oebs_key_objects.keyword_input[0])
            if 'enabled' in objstates and not err_msg:
                    if(numofoperation > 0):
                        for i in range(numofoperation):
                            if(width>height):
                                x_cor = ((x1_cor+height)+x1_cor)/2
                                y_cor = (y1_cor+y2_cor)/2
                                oebs_mouseops.MouseOperation('click',int(x_cor),int(y_cor))
                                methodoutput = TEST_RESULT_TRUE
                                status=TEST_RESULT_PASS
                    else:
                        err_msg = MSG_INVALID_INPUT
                        log.debug('Invalid Input',err_msg)
                        logger.print_on_console(err_msg)
            elif not err_msg:
                err_msg = MSG_DISABLED_OBJECT
                log.debug('Object Disabled',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_left']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',status)
        log.debug('Status: %s',status)
        return status,methodoutput,output_res,err_msg

    def up(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_UP)
            objstates = charinfo.states
            x1_cor = charinfo.x
            y1_cor = charinfo.y
            width = charinfo.width
            height = charinfo.height
            x2_cor = x1_cor+width
            y2_cor = y1_cor+height
            if len(oebs_key_objects.keyword_input) == 0 or oebs_key_objects.keyword_input[0]=='' or oebs_key_objects.keyword_input[0]==None or not oebs_key_objects.keyword_input[0].isdigit():
                err_msg = ERROR_CODE_DICT['invalid_input_scroll']
                log.info(err_msg)
                logger.print_on_console(err_msg)
            numofoperation = int(oebs_key_objects.keyword_input[0])
            if 'enabled' in objstates and not err_msg:
                    if(numofoperation > 0):
                        for i in range(numofoperation):
                            if(height>width):
                                x_cor = (x1_cor+x2_cor)/2
                                y_cor = (y1_cor+(y1_cor+width))/2
                                oebs_mouseops.MouseOperation('click',int(x_cor),int(y_cor))
                                methodoutput = TEST_RESULT_TRUE
                                status=TEST_RESULT_PASS

                    else:
                        err_msg = MSG_INVALID_INPUT
                        log.debug('Invalid Input',err_msg)
                        logger.print_on_console(err_msg)
            elif not err_msg:
                err_msg = MSG_DISABLED_OBJECT
                log.debug('Object Disabled',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_up']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',status)
        log.debug('Status: %s',status)
        return status,methodoutput,output_res,err_msg

    def down(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_DOWN)
            objstates = charinfo.states
            x1_cor = charinfo.x
            y1_cor = charinfo.y
            width = charinfo.width
            height = charinfo.height
            x2_cor = x1_cor+width
            y2_cor = y1_cor+height
            if len(oebs_key_objects.keyword_input) == 0 or oebs_key_objects.keyword_input[0]=='' or oebs_key_objects.keyword_input[0]==None or not oebs_key_objects.keyword_input[0].isdigit():
                err_msg = ERROR_CODE_DICT['invalid_input_scroll']
                log.info(err_msg)
                logger.print_on_console(err_msg)
            numofoperation = int(oebs_key_objects.keyword_input[0])
            if 'enabled' in objstates and not err_msg:
                if(numofoperation > 0):
                    for i in range(numofoperation):
                        if(height>width):
                            x_cor = (x1_cor+x2_cor)/2
                            y_cor = (y2_cor+(y2_cor-width))/2
                            oebs_mouseops.MouseOperation('click',int(x_cor),int(y_cor))
                            methodoutput = TEST_RESULT_TRUE
                            status=TEST_RESULT_PASS

                else:
                    err_msg = MSG_INVALID_INPUT
                    log.debug('Invalid Input',err_msg)
                    logger.print_on_console(err_msg)
            elif not err_msg:
                err_msg = MSG_DISABLED_OBJECT
                log.debug('Object Disabled',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_down']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',status)
        log.debug('Status: %s',status)
        return status,methodoutput,output_res,err_msg

