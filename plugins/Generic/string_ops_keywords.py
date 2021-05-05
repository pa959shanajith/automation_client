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

    def find(self, input):
        """
        def : find
        purpose : to find if string conatins another string
        param  : string , string, wildcard option(if required)
        return : integers or list of integers
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        position=[]
        wildcard_find = False
        actual_string = input[0]
        to_find = input[1]
        to_find_d = to_find
        wildcard_option = input[2].lower() if(len(input) == 3) else ""
        if (wildcard_option != ""):
            if (wildcard_option == 'wildcard'):
                tf_single_count=to_find.count('?')
                tf_mul_count=to_find.count('*')
                if tf_single_count>=1 or tf_mul_count>=1:
                    wildcard_find = True
        try:
            if not (actual_string is None or actual_string is ''):
                if not (to_find is None or to_find is ''):
                    if (wildcard_find == True):
                        if len(to_find)-1<= len(actual_string):
                            position=self.find_wildcard(actual_string,to_find)
                            position=list(set(position))
                            position.sort()
                            output_val = len(position)
                            if len(position) == 1: position=position[0]
                            if(output_val == 0):
                                output='false'
                                logger.print_on_console('The Original String is ',actual_string ,' and ' , actual_string , ' does not Contain ', to_find_d )
                            else:
                                log.info('Result : ')
                                log.info(output_val)
                                status=generic_constants.TEST_RESULT_PASS
                                result=generic_constants.TEST_RESULT_TRUE
                                output=position
                        else:
                            output='false'
                            logger.print_on_console('The Original String is ',actual_string ,' and ' , actual_string , ' does not Contain ', to_find_d )      
                    elif wildcard_option == "":
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
                                output='false'
                            else:
                                log.info('Result : ')
                                log.info(output_val)
                                status=generic_constants.TEST_RESULT_PASS
                                result=generic_constants.TEST_RESULT_TRUE
                                output=position
                    else:
                        output='false'
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
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
            if len_input_val >= 2 and not None in input_vals:
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
                output = output.replace('\x00','') if output else None
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

    def find_wildcard(self,actual_string,to_find):
        """
        def : find_wildcard
        purpose : finds the to_find with wildcard in the actualstring
        param  : actual_string, to_find
        return : postion of where the string is found
        """
        pos=[]
        position=[]
        actual_string_list=[]
        find_string_list=[]
        to_find_list=[]
        wildcard_search=False
        string_search=False
        mix_char=False
        last_wildcard_search=False
        first_wc=to_find[0]
        last_wc=to_find[-1]
        try:
            import re
            tf_split=re.split(r'[?*]',to_find)
            tf_single_count=to_find.count('?')
            tf_mul_count=to_find.count('*')
            if tf_single_count>=1 and tf_mul_count>=1:
                mix_char=True
            elif '?' in  to_find and '*' in to_find:
                mix_char=True
            if first_wc == "?" or first_wc == "*":
                if len(to_find)<= len(actual_string):
                    if tf_single_count==len(to_find)-1:
                        wildcard_search=True
                    elif tf_single_count==1 or tf_mul_count==1:
                        wildcard_search=True
                    else:
                        for i in range(len(actual_string)):
                            if i == 0 and actual_string[i]==tf_split[-1]:
                                find_string_list.append(i)
                            elif actual_string[i]==tf_split[-1]:
                                find_string_list.append(i+1)
                        for j in range(len(find_string_list)):
                            if j<len(find_string_list) and find_string_list[j]==0:
                                a_spl=actual_string[:find_string_list[j]]
                                actual_string_list.append(a_spl)
                            elif j<len(find_string_list):
                                f_i=find_string_list[j]-1
                                a_spl=actual_string[:f_i]
                                actual_string_list.append(a_spl)
                            else:
                                break
                        string_search=True         
                else:
                    logger.print_on_console('The Original String is ',actual_string ,' and ' , actual_string , ' does not Contain ', to_find)
            elif last_wc == "?" or last_wc == "*":
                if len(tf_split[0])>1:
                    if last_wc=="*":
                        pos = [i+1 for i in range(len(actual_string)) if actual_string.startswith(tf_split[0], i)]
                        position.extend(pos)
                    else:
                        last_wildcard_search=True
                else:
                    if tf_single_count!=1 and tf_single_count>0:
                        wildcard_search=True
                    elif tf_mul_count!=1 and tf_mul_count>0:
                        wildcard_search=True
                    else:
                        if actual_string.find(tf_split[0])==len(actual_string)-1:
                            wildcard_search=True
                        else:
                            for i in range(len(actual_string)):
                                if i == 0 and actual_string[i]==tf_split[0]:
                                    find_string_list.append(i)
                                elif actual_string[i]==tf_split[0]:
                                    find_string_list.append(i+1)
                            for j in range(len(find_string_list)):
                                if j<len(find_string_list) and find_string_list[j]==0:
                                    a_spl=actual_string[find_string_list[j]:]
                                    actual_string_list.append(a_spl)
                                elif j<len(find_string_list):
                                    f_i=find_string_list[j]-1
                                    a_spl=actual_string[f_i:]
                                    actual_string_list.append(a_spl)
                                else:
                                    break
                            string_search=True
            else:
                if len(tf_split[0])>1:
                    wildcard_search=True
                else:
                    tf_string="".join(tf_split)
                    if (tf_single_count!=1 and tf_single_count>0) and mix_char==False:
                        wildcard_search=True
                    elif (tf_mul_count!=1 and tf_mul_count>0) and mix_char==False:
                        if len(tf_split)==tf_split.count(tf_split[0]):
                            for i in range(len(actual_string)):
                                if i == 0 and actual_string[i]==tf_split[0]:
                                    find_string_list.append(i)
                                elif actual_string[i]==tf_split[0]:
                                    find_string_list.append(i+1)
                            for j in range(len(find_string_list)):
                                if j<len(find_string_list)-2 and find_string_list[j]==0:
                                    a_spl=actual_string[find_string_list[j]:find_string_list[j+2]]
                                    actual_string_list.append(a_spl)
                                elif j<len(find_string_list)-2:
                                    f_i=find_string_list[j]-1
                                    if j!=len(find_string_list)-1:
                                        a_spl=actual_string[f_i:find_string_list[j+2]]
                                        actual_string_list.append(a_spl)
                                else:
                                    break
                            string_search=True
                        elif (tf_split.count(tf_split[0])>1 and tf_split[0]!=tf_split[-1]):
                            first_char_count = tf_split.count(tf_split[0])
                            to_find_lc_index = actual_string.find(tf_split[-1])
                            for i in range(len(actual_string)):
                                if i == 0 and actual_string[i]==tf_split[0]:
                                    find_string_list.append(i)
                                elif actual_string[i]==tf_split[0]:
                                    find_string_list.append(i+1)
                            for j in range(len(find_string_list)):
                                if j<len(find_string_list) and find_string_list[j]==0:
                                    tfli=to_find_lc_index+1
                                    a_spl=actual_string[find_string_list[j]:tfli]
                                    actual_string_list.append(a_spl)
                                elif j<len(find_string_list):
                                    tfli=to_find_lc_index+1
                                    f_i=find_string_list[j]-1
                                    a_spl=actual_string[f_i:tfli]
                                    actual_string_list.append(a_spl)
                                else:
                                    break
                            for item in actual_string_list[:]:
                                if not(item.count(tf_split[0])>=first_char_count):
                                    actual_string_list.remove(item)
                            string_search=True     
                        else:
                            wildcard_search=True
                    elif (tf_single_count==1 and mix_char==False):
                        wildcard_search=True
                    elif (tf_mul_count==1 and mix_char==False):
                        for i in range(len(actual_string)):
                            if i == 0 and actual_string[i]==tf_split[0]:
                                find_string_list.append(i)
                            elif actual_string[i]==tf_split[0]:
                                find_string_list.append(i+1)
                        if tf_split[0]!=tf_split[-1]:
                            to_find_lc_index = actual_string.find(tf_split[-1])
                            if (tf_string == actual_string):
                                for j in range(len(find_string_list)):
                                    if j<len(find_string_list) and find_string_list[j]==0:
                                        tfli=to_find_lc_index+1
                                        a_spl=actual_string[find_string_list[j]:tfli]
                                        actual_string_list.append(a_spl)
                                    elif j<len(find_string_list):
                                        tfli=to_find_lc_index+1
                                        f_i=find_string_list[j]-1
                                        a_spl=actual_string[f_i:tfli]
                                        actual_string_list.append(a_spl)
                                    else:
                                        break
                                string_search=True
                            elif (to_find_lc_index<len(actual_string)-1 and actual_string[to_find_lc_index]==actual_string[to_find_lc_index+1]):
                                for j in range(len(find_string_list)):
                                    if j<len(find_string_list) and find_string_list[j]==0:
                                        tfli=to_find_lc_index+1
                                        a_spl=actual_string[find_string_list[j]:tfli]
                                        actual_string_list.append(a_spl)
                                    elif j<len(find_string_list):
                                        tfli=to_find_lc_index+1
                                        f_i=find_string_list[j]-1
                                        a_spl=actual_string[f_i:tfli]
                                        actual_string_list.append(a_spl)
                                    else:
                                        break
                                string_search=True
                            else:
                                for i in range(len(actual_string)):
                                    if i == 0 and actual_string[i]==tf_split[-1]:
                                        to_find_list.append(i)
                                    elif actual_string[i]==tf_split[-1]:
                                        to_find_list.append(i+1)
                                for i in range(len(to_find_list)):
                                    for j in range(len(find_string_list)):
                                        if i<=j:
                                            if j<len(find_string_list) and find_string_list[j]==0:
                                                a_spl=actual_string[find_string_list[j]:to_find_list[i]]
                                                actual_string_list.append(a_spl)
                                            elif j<len(find_string_list):
                                                f_i=find_string_list[j]-1
                                                # if j!=len(find_string_list)-1:
                                                a_spl=actual_string[f_i:to_find_list[i]]
                                                actual_string_list.append(a_spl)
                                            else:
                                                break
                                string_search=True
                        else:
                            for j in range(len(find_string_list)):
                                if j<len(find_string_list) and find_string_list[j]==0:
                                    a_spl=actual_string[find_string_list[j]:find_string_list[j+1]]
                                    actual_string_list.append(a_spl)
                                elif j<len(find_string_list):
                                    f_i=find_string_list[j]-1
                                    if j!=len(find_string_list)-1:
                                        a_spl=actual_string[f_i:find_string_list[j+1]]
                                        actual_string_list.append(a_spl)
                                else:
                                    break
                            string_search=True
                    elif mix_char:
                        for i in range(len(actual_string)):
                            if i == 0 and actual_string[i]==tf_split[0]:
                                find_string_list.append(i)
                            elif actual_string[i]==tf_split[0]:
                                find_string_list.append(i+1)
                        if tf_split[0]!=tf_split[-1]:
                            to_find_lc_index = actual_string.find(tf_split[-1])
                            for j in range(len(find_string_list)):
                                if j<len(find_string_list) and find_string_list[j]==0:
                                    tfli=to_find_lc_index+1
                                    a_spl=actual_string[find_string_list[j]:]
                                    actual_string_list.append(a_spl)
                                elif j<len(find_string_list):
                                    tfli=to_find_lc_index+1
                                    f_i=find_string_list[j]-1
                                    a_spl=actual_string[f_i:]
                                    actual_string_list.append(a_spl)
                                else:
                                    break
                            string_search=True
                        elif len(tf_split)==tf_split.count(tf_split[0]):
                            wildcard_search=True
                        else:
                            for j in range(len(find_string_list)):
                                if j<len(find_string_list) and find_string_list[j]==0:
                                    a_spl=actual_string[find_string_list[j]:find_string_list[j+1]]
                                    actual_string_list.append(a_spl)
                                elif j<len(find_string_list):
                                    f_i=find_string_list[j]-1
                                    if j!=len(find_string_list)-1:
                                        a_spl=actual_string[f_i:find_string_list[j+1]]
                                        actual_string_list.append(a_spl)
                                else:
                                    break
                            string_search=True
                        for a in actual_string_list[:]:
                            to_find = to_find.replace('?','.')
                            to_find = to_find.replace('*','.+')
                            pattern = re.compile(r"\b{}".format(to_find))
                            match = pattern.search(a)
                            if (match==None):
                                actual_string_list.remove(a)
            if wildcard_search==True:
                to_find_d = to_find
                to_find = to_find.replace('?','.')
                to_find = to_find.replace('*','.+')
                if to_find.count('.')>0:
                    if to_find != '':
                        pattern = re.compile(r"{}".format(to_find))
                        match = pattern.search(actual_string)
                        if match:
                            pos = [i+1 for i in range(len(actual_string)) if actual_string.startswith(match.group(), i)]
                            position.extend(pos)
            elif string_search==True:
                for z in actual_string_list:
                    if z != '':
                        pattern = re.compile(r"{}".format(z))
                        match = pattern.search(actual_string)
                        if match:
                            pos = [i+1 for i in range(len(actual_string)) if actual_string.startswith(match.group(), i)]
                            position.extend(pos)
                            continue
                        else:
                            logger.print_on_console('The Original String is ',actual_string ,' and ' , actual_string , ' does not Contain ', to_find_d)
            elif last_wildcard_search==True:
                to_find_d=to_find
                to_find = to_find.replace('?','.')
                to_find = to_find.replace('*','.+')
                if to_find.count('.')>0:
                    if to_find != '':
                        pattern = re.compile(r"{}".format(to_find))
                        match = pattern.findall(actual_string)
                        if match:
                            for m in match:
                                pos = [i+1 for i in range(len(actual_string)) if actual_string.startswith(m, i)]
                                position.extend(pos)
        except Exception as e:
            err_msg="Error occured in wildcard find"
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return position
                
