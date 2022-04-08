#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     24-10-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import subprocess
import generic_constants
import os
import logger
from constants import *

import logging


log = logging.getLogger('batch_operation_keyword.py')


class BatchOperationKeyword():

    def executeFile(self, filePath):
        #logger.print_on_console('Executing keyword : executeFile')
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        err_msg = None
        output_res = OUTPUT_CONSTANT
        try:
            log.debug('reading the inputs')
            filename, file_ext = os.path.splitext(filePath)
            if file_ext in generic_constants.BATCH_FILE_TYPE or file_ext in generic_constants.EXE_FILE_TYPE:
                log.debug('executing .bat or .exe file')
                logger.print_on_console('executing .bat or .exe file')
                p = subprocess.Popen(filePath, cwd=os.path.dirname(filePath), creationflags=subprocess.CREATE_NEW_CONSOLE)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            elif file_ext in generic_constants.VBS_FILE_TYPE:
                log.debug('executing .vbs file')
                logger.print_on_console('executing .vbs file')
                os.chdir(os.path.dirname(filePath))
                os.startfile(filePath)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            else:
                log.debug('Invalid file format')
                logger.print_on_console(generic_constants.INVALID_FILE_FORMAT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=INPUT_ERROR
        return status, methodoutput, output_res, err_msg
