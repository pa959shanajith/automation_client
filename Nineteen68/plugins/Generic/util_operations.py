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


class UtilOperations:

    def type_cast(self,input,to_type,*args):
        """
        def : create_folder
        purpose : creates the all the intermediate folders in the given path
        param : inputpath,folder_name
        return : bool

        """
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        input=str(input)
        to_type=str(to_type)
        fmt_type=None
        output=None
        logger.log('Input is '+input+' type to be converted is '+to_type)

        if not (input is None or input is '' or to_type is None or to_type is ''):
            try:
                if len(args)>0 and (args[0] is not None or args[0] != ''):
                    fmt_type=args[0]
                to_type=to_type.strip().lower()
                import numpy as np
                if to_type=='string':
                    output=input
                elif to_type=='int':
                    output=float(input)
                    if fmt_type!=None and fmt_type.strip().lower()=='roundoff':
                        output=round(output)
                    else:
                        output=int(output)
                elif to_type=='float':
                    output=np.float32(input)

                elif to_type=='double':
                    output=np.float64(input)
                elif to_type=='date':
                    #Supported date formats are
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
                            logger.log('Invalid date format')
                else:
                    logger.log('Please provide valid data type for conversion ')


                methodoutput=TEST_RESULT_TRUE
                status=TEST_RESULT_PASS
                logger.log('Result is ',output)
            except ValueError as e:
                logger.log('Invalid input format')
        else:
            logger.log(generic_constants.INVALID_INPUT)
        return status,methodoutput,output

    def verify_file_images(self,file1,file2):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if file1 != None and file2 != None and file1 != '' and file2 != '' and os.path.exists(file1) and os.path.exists(file2) :
                from PIL import Image
                img1 = Image.open(file1)
                img2 = Image.open(file2)
                if img1==img2:
                    logger.log('Images comparision is Pass')
                    methodoutput=TEST_RESULT_TRUE
                    status=TEST_RESULT_PASS
                else:
                    logger.log('Images comparision is Fail')
            else:
                logger.log('Invalid Input files')
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def verify_values(self,input1,input2):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if input1 != None and input2 != None and input1 != '' and input2 != '' :
                from PIL import Image
                input1=str(input1).replace('\n','').replace('\r','')
                input2=str(input2).replace('\n','').replace('\r','')
                if input1==input2:
                    logger.log('Values are equal')
                    methodoutput=TEST_RESULT_TRUE
                    status=TEST_RESULT_PASS
                else:
                    logger.log('Values are not equal')
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def stop(self,*args):
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        logger.log('Stopping the Execution')
        import handler
        output=len(handler.tspList)
        return status,methodoutput,output





