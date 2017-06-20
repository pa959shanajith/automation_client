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
import logger
import generic_constants

import logging
from constants import *
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
        output=OUTPUT_CONSTANT
        try:
            if  not (input is None or input is ''):
                output = input.lower()
                logger.print_on_console('Result : ',output)
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
        output=OUTPUT_CONSTANT
        try:
            if not (input is None or input is ''):
                output = input.upper()
                logger.print_on_console('Result : ',output)
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
        output=OUTPUT_CONSTANT
        try:
            if not (input is None or input is ''):
                output = input.strip()
                logger.print_on_console('Result : ',output)
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
        output=OUTPUT_CONSTANT
        try:
            if not (actual_string is None or actual_string is ''):
                if not (index is None or index is ''):
                    index_toint = int(index)
                    output = actual_string[:index_toint]
                    logger.print_on_console('Result : ',output)
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
        output=OUTPUT_CONSTANT
        try:
            if not (actual_string is None or actual_string is ''):
                if not (index is None or index is ''):
                    index_toint = int(index)
                    if index_toint > 0:
                        output = actual_string[-index_toint:]
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
        output=OUTPUT_CONSTANT
        try:
            if not (input is None or input is ''):
                input_len = len(input)
                if (input_len % 2 == 0):
                    even_inp = input_len/2
                    output = input[even_inp]
                    logger.print_on_console('Result : ',output)
                    log.info('Result : ')
                    log.info(output)
                    status=generic_constants.TEST_RESULT_PASS
                    result=generic_constants.TEST_RESULT_TRUE
                else:
                    odd_inp = input_len/2
                    output = input[odd_inp]
                    logger.print_on_console('Result : ',output)
                    log.info('Result : ')
                    log.info(output)
                    status=TEST_RESULT_PASS
                    result=TEST_RESULT_TRUE
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
        output=OUTPUT_CONSTANT
        try:
            if not (input is None or input is ''):
                output = len(input)
                logger.print_on_console('Result : ',output)
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

    def find(self, actual_string,to_find):
        """
        def : find
        purpose : to find if string conatins another string
        param  : string , string
        return : boolean
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            if not (actual_string is None or actual_string is ''):
                if not (to_find is None or to_find is ''):
                    output_val = actual_string.find(to_find)
                    if(output_val == -1):
                        logger.print_on_console('The Original String is:',actual_string ,'and' , actual_string , 'does not Contain', to_find )
                    else:
                        log.info('Result : ')
                        log.info(output_val)
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
        output=OUTPUT_CONSTANT
        try:
            if not (actual_string is None or actual_string is ''):
                if not (to_be_replaced is None):
                    if not (value is None):
                        if (actual_string not in to_be_replaced):
                            output =  actual_string.replace(to_be_replaced,value)
                            logger.print_on_console('Result : ',output)
                            log.info('Result : ')
                            log.info(output)
                            status=generic_constants.TEST_RESULT_PASS
                            result=generic_constants.TEST_RESULT_TRUE
                        else:
                            logger.print_on_console("Input Value " + actual_string+ " does not contain " + to_be_replaced);
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
        output=OUTPUT_CONSTANT
        try:
            if not (input is None or input is ''):
                if not (character is None):
                    output = input.split(character)
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
        output=OUTPUT_CONSTANT
        try:
            input_vals = args
            len_input_val = len(input_vals)
            if len_input_val >= 2:
                output = ''.join(input_vals)
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
        output=OUTPUT_CONSTANT
        try:
            if not (actual_string is None or actual_string is ''):
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
        output=OUTPUT_CONSTANT
        try:
            if not (data_type is None or data_type is ''):
                if not (data_length is None or data_length is ''):
                    data_length_int = int(data_length)
                    if(data_length_int > 0):
                        data_type=data_type.lower()
                        if (data_type == 'char'):
                            output = ''.join(random.choice(string.lowercase + string.uppercase) for i in range(data_length_int))
                            logger.print_on_console('Result : ',output)
                            log.info('Result : ')
                            log.info(output)
                            status=generic_constants.TEST_RESULT_PASS
                            result=generic_constants.TEST_RESULT_TRUE
                        elif (data_type == 'num'):
                            output = ''.join(random.choice(string.digits) for i in range(data_length_int))
                            logger.print_on_console('Result : ',output)
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

##obj =StringOperation()
##obj.toLowerCase('RAkESH')
##obj.toUpperCase('raKesh')
##obj.concatenate("I am ","Rakesh","SV")
##obj.trim(' Rake  ')
##obj.getStringLength('RAKESH')
##obj.replace("Rakesh","esh"," ")
##obj.split("Rak esh"," ")
##obj.getSubString("hello","1")
##obj.getSubString("RAKESH","5-6")
##obj.find("Rakesh","z")
##obj.left("Rakesh SV","7")
##obj.right("RakeshSV",7)
##obj.getStringLength("\"\"")
##obj.stringGeneration('char','1')




