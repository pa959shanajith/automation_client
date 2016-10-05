#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     03-10-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import datetime
import logger
import generic_constants
##from datetime import datetime
from datetime import timedelta
import Exceptions

class DateOperation:
    def getCurrentDate(self,input):
        """
        def : getCurrentDate
        purpose : to retreieve current date in given format
        param  : string
        return : string
        """
        try:
            if not (input is None and input is ''):
                ret_format = self.__validate(input)
                if ret_format != -1:
                    cur_date = datetime.datetime.now()
                    output = cur_date.strftime(ret_format)
                    logger.log(output)
                    return output
                else:
                    logger.log('Format not supported')
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False


    def getCurrentTime(self,input):
        """
        def : getCurrentTime
        purpose : to retreieve current time in given format
        param  : string
        return : string
        """
        try:
            if not (input is None and input is ''):
                ret_format = self.__validate(input)
                if ret_format != -1:
                    cur_time = datetime.datetime.now()
                    output = cur_time.strftime(ret_format)
                    logger.log(output)
                    return output
                else:
                    logger.log('Format not supported')
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def getCurrentDateAndTime(self,input):
        """
        def : getCurrentDateAndTime
        purpose : to retreieve current date and time in given format
        param  : string
        return : string
        """
        try:
            if not (input is None and input is ''):
                ret_format = self.__validate(input)
                if ret_format != -1:
                    cur_date_time = datetime.datetime.now()
                    output = cur_date_time.strftime(ret_format)
                    logger.log(output)
                    return output
                else:
                    logger.log('Format not supported')
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def dateDifference(self,input_date, date_or_count ,date_format):
        """
        def : dateDifference
        purpose : finds the differce between two dates or date and count
        param  : string,string,string
        return : string
        """
        try:
            if not (input_date is None and input_date is ''):
                if not (date_or_count is None and date_or_count is ''):
                    if not (date_format is None and date_format is ''):
                        ret_inp_format = self.__validate(date_format)
                        if ret_inp_format != -1:
                            if(len(input_date) == len(date_or_count)):
                                    date1 = datetime.datetime.strptime(input_date, ret_inp_format)
                                    date2 = datetime.datetime.strptime(date_or_count, ret_inp_format)
                                    output = abs((date2 - date1).days)
                                    logger.log(output)
                                    return output
                            else:
                                count = datetime.datetime.strptime(input_date, ret_inp_format)
                                days = int(date_or_count)
                                temp = count - timedelta(days = days)
                                output = temp.strftime(ret_inp_format)
                                logger.log(output)
                                return output
                        else:
                            logger.log('Format not supported')
                    else:
                        logger.log(generic_constants.INVALID_INPUT)
                    return False
        except Exception as e:
            Exceptions.error(e)
            return False



    def dateAddition(self,input_date, date_or_count ,date_format):
        """
        def : dateAddition
        purpose : finds the date when date and count are added
        param  : string,string,string
        return : string
        """
        try:
            if not (input_date is None and input_date is ''):
                if not (date_or_count is None and date_or_count is ''):
                        if not (date_format is None and date_format is ''):
                            ret_inp_format = self.__validate(date_format)
                            if ret_inp_format != -1:
                                    count = datetime.datetime.strptime(input_date, ret_inp_format)
                                    days = int(date_or_count)
                                    temp = count + timedelta(days = days)
                                    output = temp.strftime(ret_inp_format)
                                    logger.log(output)
                                    return output
                            else:
                                logger.log('Format not supported')

        except Exception as e:
            Exceptions.error(e)
            return False



    def changeDateFormat(self,inp_date,inp_date_format,out_format):
        """
        def : changeDateFormat
        purpose : converts date from one format to other
        param  : string,string,string
        return : string
        """
        try:
            if not (inp_date is None and inp_date is ''):
                 if not (inp_date_format is None and inp_date_format is ''):
                    if not (out_format is None and out_format is ''):
                        ret_inp_format = self.__validate(inp_date_format)
                        ret_out_format = self.__validate(out_format)
                        if ret_inp_format != -1:
                            if ret_out_format != -1:
                                output=datetime.datetime.strptime(inp_date, ret_inp_format).strftime(ret_out_format)
                                logger.log(output)

                        else:
                            logger.log('Format not supported')
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def dateCompare(self, input_from , input_to , input_format):
        """
        def : dateCompare
        purpose : compare if two dates are equal or not
        param  : string,string,string
        return : boolean
        """
        try:
            if not (input_from is None and input_from is ''):
                 if not (input_to is None and input_to is ''):
                    if not (input_format is None and input_format is ''):
                        ret_inp_format = self.__validate(input_format)
                        if ret_inp_format != -1:
                            date1 = datetime.datetime.strptime(input_from, ret_inp_format )
                            date2 = datetime.datetime.strptime(input_to, ret_inp_format )
                            if date1 == date2:
                                logger.log(date1 == date2)
                                return True
                            else:
                                return False
                        else:
                            logger.log('Format not supported')
            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def __validate(self,input):
        try:
            dict={'dd/MM/yyyy': '%d/%m/%Y',
            'MM/dd/yyyy': '%m/%d/%Y',
            'dd/MMM/yyyy': '%d/%b/%Y',
            'MMM/dd/yyyy':'%b/%d/%Y',
            'HH:mm:ss' : '%H:%M:%S',
            'dd/MM/yyyy HH:mm:ss' :'%d/%m/%Y %H:%M:%S',
            'MM/dd/yyyy HH:mm:ss' : '%m/%d/%Y %H:%M:%S',
            'dd/MMM/yyyy HH:mm:ss' : '%d/%b/%Y %H:%M:%S',
            'MMM/dd/yyyy HH:mm:ss' :'%b/%d/%Y %H:%M:%S'

            }
            if(input in dict):
                date_format = dict.get(input)
    ##            logger.log(date_format)
                return date_format
            else:
                return -1
        except Exception as e:
            Exceptions.error(e)


##obj =DateOperation()
##obj.getCurrentDate("dd/MMM/yyyy")
##obj.getCurrentTime("HH:mm:ss")
##obj.getCurrentDateAndTime("dd/MMM/yyyy HH:mm:ss")
##obj.changeDateFormat("03/10/2016","dd/MM/yyyy","MMM/dd/yyyy")
##obj.dateCompare("03/10/2016","03/10/2016","dd/MM/yyyy")
##obj.validate("dd/MMMM/yyyy")
##obj.dateDifference("03/10/2016","8893","dd/MM/yyyy")
##obj.dateDifference("03/10/2016","29/05/1992","dd/MM/yyyy")
##obj.dateAddition("29/05/1992","8893","dd/MM/yyyy")

