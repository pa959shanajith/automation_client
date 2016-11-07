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
import Exceptions

class BatchOperationKeyword():

    def executeFile(self, filePath):
        status=False
        try:
            filename,file_ext=os.path.splitext(filePath)
            if file_ext in generic_constants.BATCH_FILE_TYPE or  file_ext in generic_constants.EXE_FILE_TYPE:
                logger.log('executing .bat or .exe file')
                p = subprocess.Popen(filePath,cwd=os.path.dirname(filePath), creationflags=subprocess.CREATE_NEW_CONSOLE)
                status=True
                return status
            elif file_ext in generic_constants.VBS_FILE_TYPE:
                logger.log('executing .vbs file')
                os.chdir(os.path.dirname(filePath))
                os.startfile(filePath)
                status=True
            else:
                logger.log(generic_constants.INVALID_FILE_FORMAT)
        except Exception as e:
            Exceptions.error(e)
        return status

