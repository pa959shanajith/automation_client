#-------------------------------------------------------------------------------
# Name:        util_operations
# Purpose:
#
# Author:      sushma.p
#
# Created:     06-12-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import os
import logger
from generic_constants import *
import Exceptions
import file_operations
from constants import *
from loggermessages import *
import logging

log = logging.getLogger('util_operations.py')
class UtilOperations:

    def type_cast(self,input,to_type,*args):
        """
        def : create_folder
        purpose : creates the all the intermediate folders in the given path
        param : inputpath,folder_name
        return : bool

        """
        log.info(KEYWORD_EXECUTION_STARTED)
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        log.debug('reading the inputs')
        input=str(input)
        to_type=str(to_type)
        fmt_type=None
        output=None
        error_msg=None
        log.info('Input is '+input+' type to be converted is '+to_type)
        logger.print_on_console('Input is '+input+' type to be converted is '+to_type)

        if not (input is None or input is '' or to_type is None or to_type is ''):
            try:
                if len(args)>0 and (args[0] is not None or args[0] != ''):
                    fmt_type=args[0]
                to_type=to_type.strip().lower()
                import numpy as np
                if to_type=='string':
                    log.debug('converting into string')
                    output=input
                elif to_type=='int':
                    log.debug('converting into int')
                    output=float(input)
                    if fmt_type!=None and fmt_type.strip().lower()=='roundoff':
                        output=round(output)
                    else:
                        output=int(output)
                elif to_type=='float':
                    log.debug('converting into float')
                    output=np.float32(input)

                elif to_type=='double':
                    log.debug('converting into double')
                    output=np.float64(input)
                elif to_type=='date':
                    #Supported date formats are
                    log.debug('converting into date format')
                    sprtd_date1 = "([MM]|[dd]){2}[/|-|,]([MM]|[dd]){2}[/|-|.][y]{4}"
                    sprtd_date2 = "([dd]){2}[/|-|,]([MMM]){3}[/|-|,][y]{4}"
                    sprtd_date3 = "([MMM]){3}[/|-|,]([dd]){2}[/|-|,][y]{4}"
                    if fmt_type != None and fmt_type != '':
                        import re
                        flag=False
                        if re.match((sprtd_date1),fmt_type) != None or re.match((sprtd_date2),fmt_type) != None or re.match((sprtd_date3),fmt_type) != None :
                            flag=True

                        if flag:
                            import date_ops_keywords
                            import datetime
                            obj=date_ops_keywords.DateOperation()
                            fmt_type=obj.validate(fmt_type)
                            if (',' in input or '/' in input or '-' in input):
                                input=input.replace(',','/').replace('-','/')
                                if fmt_type!=-1:
                                    output=datetime.datetime.strptime(input, fmt_type).strftime(fmt_type)
                            else:
                                if fmt_type!=-1:
                                    tempDate = datetime.datetime(1900, 1, 1)
                                    deltaDays = datetime.timedelta(days=int(float(input))-2)
                                    date_output = (tempDate + deltaDays )
                                    output= date_output.strftime(fmt_type)

                        else:
                            log.error('Invalid date format')
                            logger.print_on_console('Invalid date format')
                else:
                    log.error('Please provide valid data type for conversion ')
                    logger.print_on_console('Please provide valid data type for conversion ')


                methodoutput=TEST_RESULT_TRUE
                status=TEST_RESULT_PASS
                log.info('Result is ',output)
                logger.print_on_console('Result is ',output)
            except Exception as e:
                log.error(e)
                logger.print_on_console(e)
                error_msg=e
        else:
            log.error(generic_constants.INVALID_INPUT)
            logger.print_on_console(generic_constants.INVALID_INPUT)
        return status,methodoutput,output,error_msg

    def verify_file_images(self,file1,file2):
        log.info(KEYWORD_EXECUTION_STARTED)
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=MD5_TEMP_RES
        error_msg=None
        try:
            log.debug('reading the inputs')
            if file1 != None and file2 != None and file1 != '' and file2 != '' and os.path.exists(file1) and os.path.exists(file2) :
                from PIL import Image
                img1 = Image.open(file1)
                img2 = Image.open(file2)
                log.debug('comparing the images')
                if img1==img2:
                    log.debug('Images comparision is Pass')
                    logger.print_on_console('Images comparision is Pass')
                    methodoutput=TEST_RESULT_TRUE
                    status=TEST_RESULT_PASS
                else:
                    log.debug('Images comparision is Fail')
                    logger.print_on_console('Images comparision is Fail')
            else:
                log.error('Invalid Input files')
                logger.print_on_console('Invalid Input files')
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output,error_msg

    def verify_values(self,input1,input2):
        log.info(KEYWORD_EXECUTION_STARTED)
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=MD5_TEMP_RES
        error_msg=None
        try:
            log.debug('reading the inputs')
            if input1 != None and input2 != None and input1 != '' and input2 != '' :
                from PIL import Image
                input1=str(input1).replace('\n','').replace('\r','')
                input2=str(input2).replace('\n','').replace('\r','')
                if input1==input2:
                    log.debug('Values are equal')
                    logger.print_on_console('Values are equal')
                    methodoutput=TEST_RESULT_TRUE
                    status=TEST_RESULT_PASS
                else:
                    log.error('Values are not equal')
                    logger.print_on_console('Values are not equal')
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output,error_msg

    def stop(self,*args):
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        log.info('Stopping the Execution')
        logger.print_on_console('Stopping the Execution')
        log.debug('Stopping the Execution')
        import handler
        output=len(handler.tspList)
        return status,methodoutput,output





