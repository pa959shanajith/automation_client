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

class BatchOperationKeyword():
    status=False
    def executeFile(self, filePath):
        try:
            filename,file_ext=os.path.splitext(filePath)
            if file_ext in generic_constants.BATCH_FILE_TYPE:
                logger.log('executing .bat file')
                p = subprocess.Popen(filePath, creationflags=subprocess.CREATE_NEW_CONSOLE)
                status=True
                return status
            elif file_ext in generic_constants.VBS_FILE_TYPE:
                logger.log('executing .vbs file')
                os.system(filePath)
                status=True
            else:
                logger.log(generic_constants.INVALID_FILE_FORMAT)
        except Exception as e:
            Exceptions.error(e)
        return status

