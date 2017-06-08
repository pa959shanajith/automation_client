#-------------------------------------------------------------------------------
# Name:        core_utils.py
# Purpose:		providing utility functions for the Core folder
#
# Author:      vishvas.a
#
# Created:     07-07-2017
# Copyright:   (c) vishvas.a 2017
# Licence:     <your licence>
#
#-------------------------------------------------------------------------------

import sys
import logging
log = logging.getLogger("core_utils.py")
class CoreUtils():

    #definition to fetch the data size in bytes/kilobytes/megabytes
    # sends data length in bytes if memoryformat not provided
    def getdatasize(self,inputdata,memoryformat):
        datalength = sys.getsizeof(inputdata)
        log.info('Data size in bytes:')
        log.info(datalength)
        kilobytes = datalength/1024
        if memoryformat == 'kb':
            datalength = kilobytes
            log.info('Data size is:',datalength)
        elif memoryformat == 'mb':
            datalength = kilobytes/1024
            log.info('Data size is:',datalength)
        else:
            log.info('Data size is:',datalength)
        return datalength