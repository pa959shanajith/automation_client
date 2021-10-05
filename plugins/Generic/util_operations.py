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

import file_operations
from constants import *
import core_utils
import logging
import ast
if SYSTEM_OS != 'Darwin':
    import win32api,win32con
if SYSTEM_OS == 'Darwin':
    import subprocess

log = logging.getLogger('util_operations.py')
class UtilOperations:

    def __init__(self):
    	#960 Imageverificaton (Himanshu)
        self.verify_image_obj=None
        self.__load_Image_processingobj()

    def __load_Image_processingobj(self):
        try:
            from verify_file_images import VerifyFileImages
            self.verify_image_obj=VerifyFileImages()
        except ImportError: pass
        except Exception as e:
            log.error(e)

    def check_input(self,input):
        """
        def : check_input
        purpose : input validation for typecast.
        param : input
        output : modified input
        """

        import re
        if len(re.sub("[0-9.,]","",input))!=0 or input.count('.') >=2:
            raise Exception('Please provide valid value for conversion')
        input =re.sub("[^0-9.]", "", input)
        return input

    def type_cast(self,input,to_type,*args):
        """
        def : create_folder
        purpose : creates the all the intermediate folders in the given path
        param : inputpath,folder_name
        return : bool

        """

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        log.debug('reading the inputs')
        if  not isinstance(input,str):
            input=str(input)
        to_type=str(to_type)
        fmt_type=None
        output=None
        err_msg=None
        casted_flag=False
        log.info('Input is '+input+' type to be converted is '+to_type)
        logger.print_on_console('Input is '+input+' type to be converted is '+to_type)
        if not (input is None or input is '' or to_type is None or to_type is ''):
            try:
                if len(args)>0 and (args[0] is not None or args[0] != ''):
                    fmt_type=args[0]
                to_type=to_type.strip().lower()
                if to_type=='string':
                    log.debug('converting into string')
                    output=input
                    casted_flag=True
                elif to_type=='int':
                    log.debug('converting into int')
                    input=self.check_input(input)
                    output=float(input)
                    if fmt_type!=None and fmt_type.strip().lower()=='roundoff':
                        output=round(output)
                    else:
                        output=int(output)
                    casted_flag = True
                elif to_type=='float':
                    log.debug('converting into float')
                    input=self.check_input(input)
                    output=float(input)
                    temp_var = output
                    output=str('{:.7f}'.format(float(output)))
                    for i in range(-1,-len(output)-1,-1):
                        if output[i] =='0':
                            temp_var = output[:i]
                        elif output[i]=='.':
                            output=output[:i+2]
                            break
                        else:
                            output=temp_var
                            break
                    output=float(output)
                    casted_flag = True
                elif to_type=='double':
                    log.debug('converting into double')
                    input=self.check_input(input)
                    output=float(input)
                    temp_var = output
                    output=str('{:.15f}'.format(float(output)))
                    for i in range(-1,-len(output)-1,-1):
                        if output[i] =='0':
                            temp_var = output[:i]
                        elif output[i]=='.':
                            output=output[:i+2]
                            break
                        else:
                            output=temp_var
                            break
                    output=float(output)
                    casted_flag = True
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
                            casted_flag=True
                        else:
                            log.error('Invalid date format')
                            logger.print_on_console('Invalid date format')
                else:
                    log.error('Please provide valid data type for conversion ')
                    logger.print_on_console('Please provide valid data type for conversion ')

                if casted_flag:
                    methodoutput=TEST_RESULT_TRUE
                    status=TEST_RESULT_PASS
                    log.info('Result is %s',output)
                    logger.print_on_console('Result is ',output)

            except Exception as e:
                log.error(e)
                logger.print_on_console(e)
                err_msg=INPUT_ERROR
        else:
            log.error(generic_constants.INVALID_INPUT)
            logger.print_on_console(generic_constants.INVALID_INPUT)
        return status,methodoutput,output,err_msg

    def verify_file_images(self,file1,file2):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            log.debug('reading the inputs')

            if file1 != None and file2 != None and file1 != '' and file2 != '' and os.path.exists(file1) and os.path.exists(file2) :
				#960 Imageverificaton added ssim and histogram algo. (Himanshu)
                #sending Image path instead of Images (Himanshu)
                #img1 = Image.open(file1)
                #img2 = Image.open(file2)
                log.debug('comparing the images')
                if self.verify_image_obj != None:
                	#Meaning user has advanced image processing plugin
                    if self.verify_image_obj.imagecomparison(file1,file2):
                        info_msg=ERROR_CODE_DICT['MSG_IMAGE_COMPARE_PASS']
                        log.info(info_msg)
                        logger.print_on_console(info_msg)
                        methodoutput=TEST_RESULT_TRUE
                        status=TEST_RESULT_PASS
                else:
                		#using MSE
                        from PIL import Image
                        import numpy as np

                        img1 = Image.open(file1)
                        img2 = Image.open(file2)
                        width1, height1 = img1.size
                        width2, height2 = img2.size
                        size=(min(width1,width2,1024),min(height1,height2,800))
                        if not(file1.split('.')[-1]=='jpg'):
                            img1 = img1.convert('RGB')
                            #print 'converted img 1'
                        if not(file2.split('.')[-1]=='jpg'):
                            img2 = img2.convert('RGB')
                            #print 'converted img 2'
                        img1 = img1.resize(size)
                        img2 = img2.resize(size)
                        imageA = np.asarray(img1)
                        imageB = np.asarray(img2)
                        err = np.sum((imageA.astype("float") - imageB.astype("float"))**2)
                        #print 'err: ',err
                        err /= float(size[0]*size[1]*3*255*255)
                        #print 'err %: ',err*100,'%'
                        if(err<0.0005):
                            info_msg=ERROR_CODE_DICT['MSG_IMAGE_COMPARE_PASS']
                            log.info(info_msg)
                            logger.print_on_console(info_msg)
                            methodoutput=TEST_RESULT_TRUE
                            status=TEST_RESULT_PASS
                        else:
                            err_msg=ERROR_CODE_DICT['ERR_IMAGE_COMPARE_FAIL']
            else:
                err_msg=ERROR_CODE_DICT['ERR_NO_IMAGE_SOURCE']
            if err_msg != None:
                logger.print_on_console(err_msg)
                log.error(err_msg)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=INPUT_ERROR
        return status,methodoutput,output,err_msg

    def image_similarity_percentage(self,file1,file2):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            log.debug('reading the inputs')
            if file1 != None and file2 != None and file1 != '' and file2 != '' and os.path.exists(file1) and os.path.exists(file2) :
				#960 Imageverificaton added ssim and histogram algo. (Himanshu)
                #sending Image path instead of Images (Himanshu)
                #img1 = Image.open(file1)
                #img2 = Image.open(file2)
                log.debug('comparing the images')
                if self.verify_image_obj != None:
                	#Meaning user has advanced image processing plugin
                    if self.verify_image_obj.imagecomparison(file1,file2):
                        info_msg=ERROR_CODE_DICT['MSG_IMAGE_COMPARE_PASS']
                        log.info(info_msg)
                        logger.print_on_console(info_msg)
                        methodoutput=TEST_RESULT_TRUE
                        status=TEST_RESULT_PASS
                else:
                		#using MSE
                        from PIL import Image
                        import numpy as np
                        img1 = Image.open(file1)
                        img2 = Image.open(file2)
                        width1, height1 = img1.size
                        width2, height2 = img2.size
                        size=(min(width1,width2,1024),min(height1,height2,800))
                        if not(file1.split('.')[-1]=='jpg'):
                            img1 = img1.convert('RGB')
                            #print 'converted img 1'
                        if not(file2.split('.')[-1]=='jpg'):
                            img2 = img2.convert('RGB')
                            #print 'converted img 2'
                        img1 = img1.resize(size)
                        img2 = img2.resize(size)
                        imageA = np.asarray(img1)
                        imageB = np.asarray(img2)
                        err = np.sum((imageA.astype("float") - imageB.astype("float"))**2)
                        #print 'err: ',err
                        err /= float(size[0]*size[1]*3*255*255)
                        #print 'err %: ',err*100,'%'
                        output = str((1-err)*100)
                        logger.print_on_console("Image similarity percentage is: "+str((1-err)*100)+"%")
                        methodoutput=TEST_RESULT_TRUE
                        status=TEST_RESULT_PASS
                        log.info('Result is %s',output)
                        logger.print_on_console('Result is ',output)
            else:
                err_msg=ERROR_CODE_DICT['ERR_NO_IMAGE_SOURCE']
            if err_msg != None:
                logger.print_on_console(err_msg)
                log.error(err_msg)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=INPUT_ERROR
        return status,methodoutput,output,err_msg

    def verify_values(self,input1,input2):
        #special language support defect #872 added support for non english characters using unicode (Himanshu)
        coreutilsobj=core_utils.CoreUtils()
        input1=coreutilsobj.get_UTF_8(input1)
        input2=coreutilsobj.get_UTF_8(input2)

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            log.debug('reading the inputs')
            if input1 != None and input2 != None and input1 != '' and input2 != '' :
                # input1=str(input1).replace('\n','').replace('\r','')
                # input2=str(input2).replace('\n','').replace('\r','')
                if '\xa0' in input1:
                    input1=input1.replace('\xa0', " ")
                if '\xa0' in input2:
                    input2 = input2.replace('\xa0', " ")
                    
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
            err_msg=INPUT_ERROR
        return status,methodoutput,output,err_msg

    def stop(self,stop_type=None):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        if stop_type == None or stop_type == '':
            status = TEST_RESULT_PASS
            methodoutput = TEST_RESULT_TRUE
            log.info('Execution Stopped')
            logger.print_on_console('Execution Stopped')
            log.debug('Execution Stopped')
            import handler
            output = len(handler.local_handler.tspList)
        elif stop_type.lower() in ['module', 'scenario', 'testcase']:
            status = TEST_RESULT_PASS
            methodoutput = TEST_RESULT_TRUE
            log.info('Execution Stopped')
            logger.print_on_console('Execution Stopped')
            log.debug('Execution Stopped')
            import handler
            output = len(handler.local_handler.tspList)
        else:
            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status, methodoutput, output, err_msg

    def getIndexCount(self,variable):
        try:
            status=TEST_RESULT_FAIL
            result=TEST_RESULT_FALSE
            err_msg=None
            output=None
            variable = ast.literal_eval(variable)
            if any(isinstance(el, list) for el in variable):
                output=str(len(variable))+'@'+str(len(variable[0]))
                status=TEST_RESULT_PASS
                result=TEST_RESULT_TRUE
                methodoutput=TEST_RESULT_TRUE
                logger.print_on_console("getIndexCount has performed for Two-Dimensional Array")
            elif isinstance(variable,list):
                output=len(variable)
                status=TEST_RESULT_PASS
                result=TEST_RESULT_TRUE
                methodoutput=TEST_RESULT_TRUE
                logger.print_on_console("getIndexCount has performed for One-Dimensional Array")
            else:
                logger.print_on_console("The Dynamic Varibale has OverWritten")
        except Exception as e:
            log.error(e)
            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def nullCheck(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        ncFlag=False
        try:
            if not (args is None or args is ''):
                input_list=list(args)
                y=input_list[0]
                if y == None or y == "null":
                    ncFlag = True
                    methodoutput = ncFlag
                    status=TEST_RESULT_PASS
                    status_msg = "Null value is present in the given input"
                    logger.print_on_console(status_msg)
                else:
                    err_msg = "Null value is not present in the given input"
            else:
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg="Error checking null value"
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def disableAnchorIris(self,*args):
        """
        Def : This function sets the global variables 'relativeCoordinates' and 'verifyFlag'
              defined in ./plugins/IRIS/iris_operation.py to []/ False and 'iris_constant_step' defined
              to ./plugins/Core/controller.py to -1 if they were set during runtime(basically if iris parent element
              is already set this keywords will unset the parent).
        Input : N/A
        Output : Boolean
        """
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        try:
            import iris_operations
            import controller
            if ( iris_operations.relativeCoordinates and iris_operations.verifyFlag and controller.iris_constant_step !=-1 ):
                iris_operations.relativeCoordinates = []
                iris_operations.verifyFlag = False
                controller.iris_constant_step = -1
                status=TEST_RESULT_PASS
                result=TEST_RESULT_TRUE
            else:
                err_msg = 'Unable to find iris anchor element'
        except Exception as e:
            err_msg="Error occurred in disableAnchorIris, Err Msg : " + str(e)
        if(err_msg):
            log.error( err_msg )
            logger.print_on_console(err_msg)
        return status, result, output, err_msg

    def getKeyStatus(self,*args):
        """
        Def : This function return the boolean value of NUM LOCK, CAPS LOCK and SCROLL LOCK
        Input : Input text(only allowed text: num/caps/scroll)
        Output : On/Off
        """
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        try:
            if SYSTEM_OS != 'Darwin':
                #windows
                if str(args[0]).lower() == 'num':
                    if win32api.GetKeyState(win32con.VK_NUMLOCK) : output = True
                    else: output = False
                elif str(args[0]).lower() == 'caps':
                    if win32api.GetKeyState(win32con.VK_CAPITAL) : output = True
                    else: output = False
                elif str(args[0]).lower() == 'scroll':
                    if win32api.GetKeyState(win32con.VK_SCROLL) : output = True
                    else: output = False
                else:
                    err_msg = 'Please specify a valid toggle key (caps/ num/ scroll)'
                    output = 'null'
            else:
                #mac-os
                #x=subprocess.check_output('xset q | grep LED', shell=True)[65]
                #if x==48 or x==50:
                    #caps = False
                    #if x == 48:
                        #num = False
                    #else:
                        #num = True
                #elif x==49 or x==51:
                    #caps = True
                    #if x == 49:
                        #num = False
                    #else:
                        #num = True
                if str(args[0]).lower() == 'num':
                    numStatus = subprocess.getoutput("xset q | grep Caps | tr -s ' ' | cut -d ' ' -f 9")
                    if numStatus == 'on': output = True
                    elif numStatus == 'off': output = False
                elif str(args[0]).lower() == 'caps':
                    capsStatus = subprocess.getoutput("xset q | grep Caps | tr -s ' ' | cut -d ' ' -f 5")
                    if capsStatus == 'on': output = True
                    elif capsStatus == 'off' : output = False
                elif str(args[0]).lower() == 'scroll':
                    scrollStatus = subprocess.getoutput("xset q | grep Caps | tr -s ' ' | cut -d ' ' -f 13")
                    if scrollStatus == 'on': output = True
                    elif scrollStatus == 'off' : output = False
                else:
                    err_msg = 'Please specify valid a toggle key (caps/ num/ scroll)'
                    output = 'null'
            status=TEST_RESULT_PASS
            result=TEST_RESULT_TRUE
        except Exception as e:
            err_msg="Error occurred in getKeyStatus, Err Msg : " + str(e)
        if(err_msg):
            log.error( err_msg )
            logger.print_on_console(err_msg)
        return status, result, output, err_msg
    def staticFetch(self,tspIndex,inp):
        import handler
        var = inp[1:len(str(inp))-1]
        path = handler.local_handler.paramData[var][0]
        return path
