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
        try:
            datalength = sys.getsizeof(inputdata)
            log.info('Data size in bytes:')
            log.info(datalength)
            kilobytes = datalength/1024
            if memoryformat == 'kb':
                datalength = kilobytes
                log.info('Data size is: %s',str(datalength))
            elif memoryformat == 'mb':
                datalength = kilobytes/1024
                log.info('Data size is: %s',str(datalength))
            else:
                log.info('Data size is: %s',str(datalength))
            return datalength
        except Exception as e:
            log.info(e)

    #definition to convert to UTF-8 format when input is not within ascii 128
    def get_UTF_8(self,value):
        try:
            if not isinstance(value,int):
                if isinstance(value, list):
                    for eachvalue in value:
                        if not isinstance(eachvalue,unicode):
                            if not all(ord(c) < 128 for c in eachvalue):
                                value.append(eachvalue.decode('utf-8'))
                else:
                    if not isinstance(value,unicode):
                        if not all(ord(c) < 128 for c in value):
                            value = value.decode('utf-8')
            return value
        except Exception as e:
            log.info(e)
            


