#-------------------------------------------------------------------------------
# Name:        module1
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
import Exceptions
class StringOperation:
    def toLowerCase(self,input):
        """
        def : toLowerCase
        purpose : converts upper case string to lower case
        param  : string to be converted
        return : string with lower case
        """
        try:
            if not (input is None and input is ''):
                output = input.lower()
                logger.log(output)
                return output
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False


    def toUpperCase(self,input):
        """
        def : toUpperCase
        purpose : converts lower case string to upper case
        param  : string to be converted
        return : string with upper case
        """
        try:
            if not (input is None and input is ''):
                output = input.upper()
                logger.log(output)
                return output
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def trim(self, input):
        """
        def : trim
        purpose : remove leading and trailing space
        param  : string to be trim
        return : string with removed spaces
        """
        try:
            if not (input is None and input is ''):
                output = input.strip()
                logger.log(output)
                return output
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def left(self, actual_string,index):
        """
        def : left
        purpose : to find only left character of string
        param  : string and index position
        return : string
        """
        try:
            if not (actual_string is None and actual_string is ''):
                if not (index is None and index is ''):
                    index_toint = int(index)
                    output = actual_string[:index_toint]
                    logger.log(output)
                    return output
                else:
                    logger.log(generic_constants.INVALID_INPUT)
                    return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def right(self, actual_string,index):
        """
        def : right
        purpose : to find only right character of string
        param  : string and index position
        return : string
        """
        try:
            if not (actual_string is None and actual_string is ''):
                if not (index is None and index is ''):
                    index_toint = int(index)
                    if index_toint > 0:
                        output = actual_string[-index_toint:]
                        logger.log(output)
                        return output
                    else:
                        logger.log(generic_constants.INVALID_INPUT)
                else:
                    logger.log(generic_constants.INVALID_INPUT)
                    return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def mid(self,input):
        """
        def : mid
        purpose : to find middle character in a string
        param  : string
        return : string
        """
        try:
            if not (input is None and input is ''):
                input_len = len(input)
                if (input_len % 2 == 0):
                    even_inp = input_len/2
                    output = input[even_inp]
                    logger.log(output)
                    return True
                else:
                    odd_inp = input_len/2
                    output = input[odd_inp]
                    logger.log(output)
                    return True
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def getStringLength(self, input):
        """
        def : getStringLength
        purpose : to find length of the string
        param  : string
        return : length
        """
        try:
            if not (input is None and input is ''):
                output = len(input)
                logger.log(output)
                return output
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def find(self, actual_string,to_find):
        """
        def : find
        purpose : to find if string conatins another string
        param  : string , string
        return : boolean
        """
        try:
            if not (actual_string is None and actual_string is ''):
                if not (to_find is None and to_find is ''):
                    output = actual_string.find(to_find)
                    if(output == -1):
                        return False
                    else:
                        return True
        except Exception as e:
            Exceptions.error(e)
            return False

    def replace(self, actual_string, to_be_replaced , value ):
        """
        def : replace
        purpose : to replace certain character in a string
        param  : string , string , string
        return : string
        """
        try:
            if not (actual_string is None and actual_string is ''):
                if not (to_be_replaced is None):
                    if not (value is None):
                        if (actual_string not in to_be_replaced):
                            output =  actual_string.replace(to_be_replaced,value)
                            logger.log(output)
                            return output
                        else:
                            logger.log("Input Value " + actual_string+ " does not contain " + to_be_replaced);
                            return False
                    else:
                        logger.log(generic_constants.INVALID_INPUT)
                        return False
                else:
                    logger.log(generic_constants.INVALID_INPUT)
                    return False
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def split(self,input,character):
        """
        def : split
        purpose : to splict string based on character
        param  : string , string
        return : multidimensional array
        """
        try:
            if not (input is None and input is ''):
                if not (character is None):
                    output = input.split(character)
                    logger.log(output)
                    return True
                else:
                    logger.log(generic_constants.INVALID_INPUT)
                    return False
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def concatenate(self,input1,input2):
        """
        def : concatenate
        purpose : to concatenate two string
        param  : string , string
        return : string
        """
        try:
            if not (input1 is None and input1 is ''):
                if not (input2 is None and input2 is ''):
                    output = input1 + input2
                    logger.log(output)
                    return output
                else:
                    logger.log(generic_constants.INVALID_INPUT)
                    return False
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def getSubString(self,actual_string,index):
        """
        def : getSubString
        purpose : to get a substring based on index
        param  : string , string
        return : string
        """
        try:
            if not (actual_string is None and actual_string is ''):
                if not (index is None and index is ''):
                    ran = '-'
                    if(ran in index):
                        val = index.split('-')
                        low_range = val[0]
                        low_range = int(low_range)
                        high_range = val[1]
                        high_range = int(high_range)
                        output = actual_string[low_range:high_range]
                        logger.log(output)
                        return output
                    else:
                        to_int_index = int(index)
                        output = actual_string[to_int_index:]
                        logger.log(output)
                        return output
                else:
                    logger.log(generic_constants.INVALID_INPUT)
                    return False
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def stringGeneration(self,data_type,data_length):
        """
        def : stringGeneration
        purpose : to generate random digits or character
        param  : string , string
        return : string
        """
        try:
            if not (data_type is None and data_type is ''):
                if not (data_length is None and data_length is ''):
                    data_length_int = int(data_length)
                    if(data_length_int > 0):
                        data_type=data_type.lower()
                        if (data_type == 'char'):
                            output = ''.join(random.choice(string.lowercase + string.uppercase) for i in range(data_length_int))
                            logger.log(output)
                            return output
                        elif (data_type == 'num'):
                            output = ''.join(random.choice(string.digits) for i in range(data_length_int))
                            logger.log(output)
                            return output
                    else:
                        logger.log(generic_constants.INP_VAL_EXCEEDS)
                        return False
                else:
                    logger.log(generic_constants.INVALID_INPUT)
                    return False
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

##obj =StringOperation()
##obj.toLowerCase('RAkESH')
##obj.toUpperCase('raKesh')
##obj.concatenate("I am "," Rakesh")
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




