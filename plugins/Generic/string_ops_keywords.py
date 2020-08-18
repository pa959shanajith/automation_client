#-------------------------------------------------------------------------------
# Name:        string_ops_keywords.py
# Purpose:
#
# Author:      rakesh.v
#
# Created:     30-09-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import string
import random
import re
import logger
import generic_constants
import core_utils
from constants import SYSTEM_OS
import subprocess
from unidecode import unidecode
from constants import *
if SYSTEM_OS == "Windows":
    import win32clipboard
import logging
log = logging.getLogger('string_ops_keywords.py')

class StringOperation:
    def toLowerCase(self,input):
        """
        def : toLowerCase
        purpose : converts upper case string to lower case
        param  : string to be converted
        return : string with lower case
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        try:
            if  not (input is None or input is ''):
                output=''
                for char in input:
                    notenglish=False
                    if not (ord(char) >= 65 and ord(char) <= 122):
                        notenglish = True
                    if not (notenglish):
                        output = output+char.lower()
                    else:
                        output=output+char
    ##                logger.print_on_console('Result : ',output)
                coreutilsobj=core_utils.CoreUtils()
                output=coreutilsobj.get_UTF_8(output)
##                output = input.lower()
##                logger.print_on_console('Result : ',output)
                log.info('Result : ')
                log.info(output)
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
            else:
                #log.error(INVALID_INPUT)
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                #logger.print_on_console(INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def toUpperCase(self,input):
        """
        def : toUpperCase
        purpose : converts upper case string to upper case
        param  : string to be converted
        return : string with upper case
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        try:
            if not (input is None or input is ''):
                output=''
                for char in input:
                    notenglish=False
                    if not (ord(char) >= 65 and ord(char) <= 122):
                        notenglish = True
                    if not (notenglish):
                        output = output+char.upper()
                    else:
                        output=output+char
##                logger.print_on_console('Result : ',output)
                coreutilsobj=core_utils.CoreUtils()
                output=coreutilsobj.get_UTF_8(output)
                log.info('Result : ')
                log.info(output)
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
            else:
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                #logger.print_on_console(INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def trim(self, input):
        """
        def : trim
        purpose : remove leading and trailing space
        param  : string to be trim
        return : string with removed spaces
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        try:
            if not (input is None or input is ''):
                output = input.strip()
##                logger.print_on_console('Result : ',output)
                log.info('Result : ')
                log.info(output)
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
            else:
                #log.error(INVALID_INPUT)
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                #logger.print_on_console(INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def left(self, actual_string,index):
        """
        def : left
        purpose : to find only left character of string
        param  : string and index position
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        try:
            if not (actual_string is None or actual_string is ''):
                if not (index is None or index is ''):
                    coreutilsobj=core_utils.CoreUtils()
                    actual_string=coreutilsobj.get_UTF_8(actual_string)
                    index_toint = int(index)
                    output = actual_string[:index_toint]
##                    logger.print_on_console('Result : ',output)
                    output=coreutilsobj.get_UTF_8(output)
                    log.info('Result : ')
                    log.info(output)
                    status=generic_constants.TEST_RESULT_PASS
                    result=generic_constants.TEST_RESULT_TRUE
                else:
                    #log.error(INVALID_INPUT)
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    #logger.print_on_console(INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def right(self, actual_string,index):
        """
        def : right
        purpose : to find only right character of string
        param  : string and index position
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        try:
            if not (actual_string is None or actual_string is ''):
                if not (index is None or index is ''):
                    coreutilsobj=core_utils.CoreUtils()
                    index_toint = int(index)
                    if index_toint > 0:
                        actual_string=coreutilsobj.get_UTF_8(actual_string)
                        output = actual_string[-index_toint:]
##                        logger.print_on_console('Result : ',output)
                        output=coreutilsobj.get_UTF_8(output)
                        log.info('Result : ')
                        log.info(output)
                        status=generic_constants.TEST_RESULT_PASS
                        result=generic_constants.TEST_RESULT_TRUE
                    else:
                        #log.error(INVALID_INPUT)
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        #logger.print_on_console(INVALID_INPUT)
                else:
                    #log.error(INVALID_INPUT)
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    #logger.print_on_console(INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def mid(self,input):
        """
        def : mid
        purpose : to find middle character in a string
        param  : string
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        try:
            if not (input is None or input is ''):
                coreutilsobj=core_utils.CoreUtils()
                input=coreutilsobj.get_UTF_8(input)
                output = coreutilsobj.get_UTF_8(input[int(len(input)/2)])
                #logger.print_on_console('Result: '+str(output))
                log.info('Result:')
                log.info(output)
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
            else:
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            log.error(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def getStringLength(self, input):
        """
        def : getStringLength
        purpose : to find length of the string
        param  : string
        return : length
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        try:
            if input is not None :
                output = len(input)
                logger.print_on_console('Result obtained is: ',output)
                log.info('Result obtained is:')
                log.info(output)
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
            else:
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def find(self, actual_string,to_find):
        """
        def : find
        purpose : to find if string conatins another string
        param  : string , string
        return : integers or list of integers
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        position=[]
        try:
            if not (actual_string is None or actual_string is ''):
                if not (to_find is None or to_find is ''):
                    coreutilsobj=core_utils.CoreUtils()
                    actual_string=coreutilsobj.get_UTF_8(actual_string)
                    actual_string=unidecode(actual_string)
                    to_find=coreutilsobj.get_UTF_8(to_find)
                    #output_val = actual_string.find(to_find)
                    position = [i+1 for i in range(len(actual_string)) if actual_string.startswith(to_find, i)]
                    output_val = len(position)
                    if len(position) == 1: position=position[0]
                    if(output_val == 0):
                        logger.print_on_console('The Original String is:',actual_string ,' and ' , actual_string , ' does not Contain ', to_find )
                    else:
                        log.info('Result : ')
                        log.info(output_val)
                        status=generic_constants.TEST_RESULT_PASS
                        result=generic_constants.TEST_RESULT_TRUE
                        output=position
            else:
                #log.error(INVALID_INPUT)
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                #logger.print_on_console(INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def replace(self, actual_string, to_be_replaced , value ):
        """
        def : replace
        purpose : to replace certain character in a string
        param  : string , string , string
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        try:
            if not (actual_string is None or actual_string is ''):
                if not (to_be_replaced is None):
                    if not (value is None):
                        coreutilsobj=core_utils.CoreUtils()
                        actual_string=coreutilsobj.get_UTF_8(actual_string)
                        actual_string=unidecode(actual_string)
                        to_be_replaced=coreutilsobj.get_UTF_8(to_be_replaced)
                        value=coreutilsobj.get_UTF_8(value)
                        if (actual_string not in to_be_replaced):
                            output =  actual_string.replace(to_be_replaced,value)
##                            logger.print_on_console('Result : ',output)
                            log.info('Result : ')
                            log.info(output)
                            status=generic_constants.TEST_RESULT_PASS
                            result=generic_constants.TEST_RESULT_TRUE
                        else:
                            logger.print_on_console("Input Value ",actual_string," does not contain ",to_be_replaced);
                    else:
                        #log.error(INVALID_INPUT)
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                        #logger.print_on_console(INVALID_INPUT)
                else:
                    #log.error(INVALID_INPUT)
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    #logger.print_on_console(INVALID_INPUT)
            else:
##                log.error(INVALID_INPUT)
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
##                logger.print_on_console(INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def split(self,input,character):
        """
        def : split
        purpose : to splict string based on character
        param  : string , string
        return : multidimensional array
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        try:
            if not (input is None or input is ''):
                if not (character is None):
                    coreutilsobj=core_utils.CoreUtils()
                    input=coreutilsobj.get_UTF_8(input)
                    input=unidecode(input)
                    character=coreutilsobj.get_UTF_8(character)
                    output = input.split(character)
##                    logger.print_on_console('Result : ',output)
                    log.info('Result : ')
                    log.info(output)
                    status=generic_constants.TEST_RESULT_PASS
                    result=generic_constants.TEST_RESULT_TRUE
                else:
                    #log.error(INVALID_INPUT)
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    #logger.print_on_console(INVALID_INPUT)
            else:
                #log.error(INVALID_INPUT)
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                #logger.print_on_console(INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def concatenate(self,*args):
        """
        def : concatenate
        purpose : to concatenate string
        param  : *args
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        try:
            input_vals = args
            len_input_val = len(input_vals)
            if len_input_val >= 2:
##                output = ''.join(input_vals)
                output=''
                coreutilsobj=core_utils.CoreUtils()
                for eachvalue in input_vals:
                    eachvalue=coreutilsobj.get_UTF_8(eachvalue)
                    eachvalue=unidecode(eachvalue)
                    output=output+eachvalue
                logger.print_on_console('Result : ',output)
                log.info('Output is')
                log.info(output)
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
            else:
                #log.error(INVALID_INPUT)
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                #logger.print_on_console(INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def getSubString(self,actual_string,index):
        """
        def : getSubString
        purpose : to get a substring based on index
        param  : string , string
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        index=str(index)
        try:
            if not (actual_string is None or actual_string is ''):
                coreutilsobj=core_utils.CoreUtils()
                actual_string=coreutilsobj.get_UTF_8(actual_string)
                actual_string=unidecode(actual_string)
                if not (index is None or index is ''):
                    ran = '-'
                    if(ran in index):
                        val = index.split('-')
                        low_range = val[0]
                        low_range = int(low_range)
                        high_range = val[1]
                        high_range = int(high_range)
                        output = actual_string[low_range:high_range]
                        logger.print_on_console('Result : ',output)
                        log.info('Result : ')
                        log.info(output)
                        status=generic_constants.TEST_RESULT_PASS
                        result=generic_constants.TEST_RESULT_TRUE
                    else:
                        to_int_index = int(index)
                        output = actual_string[to_int_index:]
                        logger.print_on_console('Result : ',output)
                        log.info('Result : ')
                        log.info(output)
                        status=generic_constants.TEST_RESULT_PASS
                        result=generic_constants.TEST_RESULT_TRUE
                else:
                    #log.error(INVALID_INPUT)
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    #logger.print_on_console(INVALID_INPUT)
            else:
                #log.error(INVALID_INPUT)
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                #logger.print_on_console(INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def stringGeneration(self,data_type,data_length):
        """
        def : stringGeneration
        purpose : to generate random digits or character
        param  : string , string
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        try:
            if not (data_type is None or data_type is ''):
                if not (data_length is None or data_length is ''):
                    data_length_int = int(data_length)
                    if(data_length_int > 0):
                        data_type=data_type.lower()
                        if (data_type == 'char'):
                            output = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(data_length_int))
##                            logger.print_on_console('Result : ',output)
                            log.info('Result : ')
                            log.info(output)
                            status=generic_constants.TEST_RESULT_PASS
                            result=generic_constants.TEST_RESULT_TRUE
                        elif (data_type == 'num'):
                            while True:
                                output = ''.join(random.choice(string.digits) for i in range(data_length_int))
                                if data_length_int==1: break
                                elif data_length_int>1 and output[0]!='0': break
##                            logger.print_on_console('Result : ',output)
                            log.info('Result : ')
                            log.info(output)
                            status=generic_constants.TEST_RESULT_PASS
                            result=generic_constants.TEST_RESULT_TRUE
                    else:
                        #log.error(generic_constants.INP_VAL_EXCEEDS)
                        err_msg=generic_constants.INP_VAL_EXCEEDS
                        #logger.print_on_console(generic_constants.INP_VAL_EXCEEDS)
                else:
                    #log.error(INVALID_INPUT)
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    #logger.print_on_console(INVALID_INPUT)
            else:
                #log.error(INVALID_INPUT)
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
##                logger.print_on_console(INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def save_to_clip_board(self,input_val,*args):
        """
        def : save_to_clip_board
        purpose : to save data on clipboard
        param  : string
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            if SYSTEM_OS == "Windows":
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(input_val)
                win32clipboard.CloseClipboard()
                status=generic_constants.TEST_RESULT_PASS
            elif SYSTEM_OS == "Darwin":
                p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
                p.stdin.write(input_val)
                p.stdin.close()
                retcode = p.wait()
                if str(retcode)=="0":
                    status=generic_constants.TEST_RESULT_PASS
            result=generic_constants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg="Error while saving data to clipboard"
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def get_from_clip_board(self,*args):
        """
        def : get_from_clip_board
        purpose : to get data from clipboard
        param  : *args
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        try:
            if SYSTEM_OS == "Windows":
                win32clipboard.OpenClipboard()
                output = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                status=generic_constants.TEST_RESULT_PASS
            elif SYSTEM_OS == "Darwin":
                p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
                retcode = p.wait()
                output = p.stdout.read()
                if str(retcode)=="0":
                    status=generic_constants.TEST_RESULT_PASS
            result=generic_constants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg="Error while saving data to clipboard"
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return status,result,output,err_msg
