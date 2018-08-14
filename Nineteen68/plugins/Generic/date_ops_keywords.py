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
import calendar
import logger
import generic_constants
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import logging

from constants import *
log = logging.getLogger('date_ops_keywords.py')

class DateOperation:
    def getCurrentDate(self,input):
        """
        def : getCurrentDate
        purpose : to retreieve current date in given format
        param  : string
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg=None
        try:
            if not (input is None or input is ''):
                ret_format = self.validate(input)
                if ret_format != -1:
                    cur_date = datetime.datetime.now()
                    output = cur_date.strftime(ret_format)
                    logger.print_on_console('Output is :' ,output)
                    status=generic_constants.TEST_RESULT_PASS
                    result=generic_constants.TEST_RESULT_TRUE
                else:
                    #logger.print_on_console('Format not supported')
                    #err_msg = 'Format not supported'
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            else:
                #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            log.error(e)
            err_msg=generic_constants.ERR_MSG1+' getCurrentDate'
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg


    def getCurrentTime(self,input):
        """
        def : getCurrentTime
        purpose : to retreieve current time in given format
        param  : string
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg = None
        try:
            if not (input is None or input is ''):
                ret_format = self.validate(input)
                if ret_format != -1:
                    cur_time = datetime.datetime.now()
                    output = cur_time.strftime(ret_format)
                    logger.print_on_console('Output is :' ,output)
                    log.info('output is')
                    log.info(output)
                    status=generic_constants.TEST_RESULT_PASS
                    result=generic_constants.TEST_RESULT_TRUE
                else:
                    #logger.print_on_console('Format not supported')
                    #err_msg = 'Format not supported'
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            else:
                #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            log.error(e)
            err_msg=generic_constants.ERR_MSG1+' getCurrentTime'
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def getCurrentDateAndTime(self,input):
        """
        def : getCurrentDateAndTime
        purpose : to retreieve current date and time in given format
        param  : string
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg = None
        try:
            if not (input is None or input is ''):
                ret_format = self.validate(input)
                if ret_format != -1:
                    cur_date_time = datetime.datetime.now()
                    output = cur_date_time.strftime(ret_format)
                    logger.print_on_console('Output is :' ,output)
                    log.info('output is')
                    log.info(output)
                    status=generic_constants.TEST_RESULT_PASS
                    result=generic_constants.TEST_RESULT_TRUE
                else:
                    #logger.print_on_console('Format not supported')
                    #err_msg = 'Format not supported'
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            else:
                #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            log.error(e)
            err_msg=generic_constants.ERR_MSG1+' getCurrentDateAndTime'
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def dateDifference(self,input_date, date_or_count ,date_format):
        """
        def : dateDifference
        purpose : finds the differce between two dates or date and count
        param  : string,string,string
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg = None
        try:
            if not (input_date is None or input_date is ''):
                if not (date_or_count is None or date_or_count is ''):
                    if not (date_format is None or date_format is ''):
                        ret_inp_format = self.validate(date_format)
                        if ret_inp_format != -1:
                            if(len(input_date) == len(date_or_count)):
                                date1 = datetime.datetime.strptime(input_date, ret_inp_format)
                                date2 = datetime.datetime.strptime(date_or_count, ret_inp_format)
                                output = abs((date2 - date1).days)
                                logger.print_on_console('Output is :' ,output)
                                log.info('output is')
                                log.info(output)
                                status=generic_constants.TEST_RESULT_PASS
                                result=generic_constants.TEST_RESULT_TRUE
                            else:
                                count = datetime.datetime.strptime(input_date, ret_inp_format)
                                days = int(date_or_count)
                                temp = count - timedelta(days = days)
                                output = temp.strftime(ret_inp_format)
                                logger.print_on_console('Output is :' ,output)
                                log.info('output is')
                                log.info(output)
                                status=generic_constants.TEST_RESULT_PASS
                                result=generic_constants.TEST_RESULT_TRUE
                        else:
                            #logger.print_on_console('Format not supported')
                             #err_msg = 'Format not supported'
                            err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    else:
                        #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                else:
                    #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            else:
                #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            log.error(e)
            err_msg=generic_constants.ERR_MSG1+' dateDifference'
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def dateAddition(self,input_date, date_or_count ,date_format):
        """
        def : dateAddition
        purpose : finds the date when date and count are added
        param  : string,string,string
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg = None
        try:
            if not (input_date is None or input_date is ''):
                if not (date_or_count is None or date_or_count is ''):
                    if not (date_format is None or date_format is ''):
                        ret_inp_format = self.validate(date_format)
                        if ret_inp_format != -1:
                                count = datetime.datetime.strptime(input_date, ret_inp_format)
                                days = int(date_or_count)
                                temp = count + timedelta(days = days)
                                output = temp.strftime(ret_inp_format)
                                logger.print_on_console('Output is :' ,output)
                                log.info('output is')
                                log.info(output)
                                status=generic_constants.TEST_RESULT_PASS
                                result=generic_constants.TEST_RESULT_TRUE
                        else:
                            #logger.print_on_console('Format not supported')
                    #err_msg = 'Format not supported'
                             err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    else:
                        #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                else:
                   # logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            else:
                #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']

        except Exception as e:
            log.error(e)
            err_msg=generic_constants.ERR_MSG1+' dateAddition'
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg


    def monthAddition(self,input_date, date_or_count ,date_format):
        """
        author : arpitha.b.v
        def : monthAddition
        purpose : addition of months
        param  : string,string,string
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg = None
        try:
            if not (input_date is None or input_date is ''):
                if not (date_or_count is None or date_or_count is ''):
                    if not (date_format is None or date_format is ''):
                        ret_inp_format = self.validate(date_format)
                        if ret_inp_format != -1:
                                count = datetime.datetime.strptime(input_date, ret_inp_format)
                                temp = count+relativedelta(months=+int(date_or_count))
                                count = datetime.datetime.strptime(input_date, ret_inp_format)
                                monthVal=int(date_or_count)
                                temp = count + relativedelta(months = + monthVal)
                                output = temp.strftime(ret_inp_format)
                                logger.print_on_console('Output is :' ,output)
                                log.info('output is')
                                log.info(output)
                                status=generic_constants.TEST_RESULT_PASS
                                result=generic_constants.TEST_RESULT_TRUE
                        else:
                            #logger.print_on_console('Format not supported')
                    #err_msg = 'Format not supported'
                             err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    else:
                        #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                else:
                   # logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            else:
                #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']

        except Exception as e:
            log.error(e)
            err_msg=generic_constants.ERR_MSG1+' monthAddition'
        if err_msg!=None:
            import traceback
            traceback.print_exc()
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def yearAddition(self,input_date, date_or_count ,date_format):
        """
        author : arpitha.b.v
        def : yearAddition
        purpose : addition of years
        param  : string,string,string
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg = None
        try:
            if not (input_date is None or input_date is ''):
                if not (date_or_count is None or date_or_count is ''):
                    if not (date_format is None or date_format is ''):
                        ret_inp_format = self.validate(date_format)
                        if ret_inp_format != -1:
                                count = datetime.datetime.strptime(input_date, ret_inp_format)
                                temp = count+relativedelta(months=+int(date_or_count))
                                count = datetime.datetime.strptime(input_date, ret_inp_format)
                                yearVal=int(date_or_count)
                                temp = count + relativedelta(years = + yearVal)
                                output = temp.strftime(ret_inp_format)
                                logger.print_on_console('Output is :' ,output)
                                log.info('output is')
                                log.info(output)
                                status=generic_constants.TEST_RESULT_PASS
                                result=generic_constants.TEST_RESULT_TRUE
                        else:
                            #logger.print_on_console('Format not supported')
                    #err_msg = 'Format not supported'
                             err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    else:
                        #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                else:
                   # logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            else:
                #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']

        except Exception as e:
            log.error(e)
            err_msg=generic_constants.ERR_MSG1+' yearAddition'
        if err_msg!=None:
            import traceback
            traceback.print_exc()
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def changeDateFormat(self,inp_date,inp_date_format,out_format):
        """
        def : changeDateFormat
        purpose : converts date from one format to other
        param  : string,string,string
        return : string
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg = None
        try:
            if not (inp_date is None or inp_date is ''):
                 if not (inp_date_format is None or inp_date_format is ''):
                    if not (out_format is None or out_format is ''):
                        ret_inp_format = self.validate(inp_date_format)
                        ret_out_format = self.validate(out_format)
                        if ret_inp_format != -1:
                            if ret_out_format != -1:
                                output=datetime.datetime.strptime(inp_date, ret_inp_format).strftime(ret_out_format)
                                logger.print_on_console('Output is :' ,output)
                                log.info('output is')
                                log.info(output)
                                status=generic_constants.TEST_RESULT_PASS
                                result=generic_constants.TEST_RESULT_TRUE
                        else:
                           #logger.print_on_console('Format not supported')
                    #err_msg = 'Format not supported'
                           err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                    else:
                        #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                 else:
                    #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            else:
               # logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            log.error(e)
            err_msg=generic_constants.ERR_MSG1+' changeDateFormat'
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,output,err_msg

    def dateCompare(self, input_from , input_to=None , input_format=None):
        """
        def : dateCompare
        purpose : compare if two dates are equal or not
        param  : string,string,string(if 3rd param is none then by default format id dd/MM/YYYY)
        return : boolean
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        err_msg = None
        verb = OUTPUT_CONSTANT
        try:
            if not (input_from is None or input_from is ''):
#                try:
#                    if '==' in input_from:
#                        input_to=input_from.split('==')[1]
#                        input_from = input_from.split('==')[0]
#                except Exception as e:
#                    log.error(e)
#                    print '*****error1*****'
                if not (input_to is None or input_to is ''):
                    if  (input_format is None):
                        date1 = datetime.datetime.strptime(input_from, generic_constants.DATE_FORMAT )
                        date2 = datetime.datetime.strptime(input_to, generic_constants.DATE_FORMAT )
                        if date1 == date2:
                            log.info('date1 == date2')
                            log.info(date1 == date2)
                            status=generic_constants.TEST_RESULT_PASS
                            result=generic_constants.TEST_RESULT_TRUE
                        else:
                            status=generic_constants.TEST_RESULT_FAIL
                            result=generic_constants.TEST_RESULT_FALSE
                    else:
                        ret_inp_format = self.validate(input_format)
                        if ret_inp_format != -1:
                            date1 = datetime.datetime.strptime(input_from, ret_inp_format )
                            date2 = datetime.datetime.strptime(input_to, ret_inp_format )
                            if date1 == date2:
                                log.info('date1 == date2')
                                log.info(date1 == date2)
                                status=generic_constants.TEST_RESULT_PASS
                                result=generic_constants.TEST_RESULT_TRUE
                            else:
                                status=generic_constants.TEST_RESULT_FAIL
                                result=generic_constants.TEST_RESULT_FALSE
                        else:
                            #logger.print_on_console('Format not supported')
                    #err_msg = 'Format not supported'
                              err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                else:
                    #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            else:
                #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
            log.error(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,verb,err_msg

    def validate(self,input):
        try:
            dict={'dd/MM/yyyy': '%d/%m/%Y',
            'MMMM dd, yyyy': '%B %d, %Y',
            'MM/dd/yyyy': '%m/%d/%Y',
            'yyMMdd': '%y%m%d',
            'yyyy/MM/dd': '%Y/%m/%d',
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
                return date_format
            else:
                return -1
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)


##obj =DateOperation()
##obj.getCurrentDate("dd/MMM/yyyy")
##obj.getCurrentTime("HH:mm:ss")
##obj.getCurrentDateAndTime("dd/MMM/yyyy HH:mm:ss")
##obj.changeDateFormat("03/10/2016","dd/MM/yyyy","MMM/dd/yyyy")
##obj.dateCompare("03/10/2016","03/11/2016")
##obj.dateCompare("03/10/2016","03/10/2016", "dd/MM/yyyy")
##obj.validate("dd/MMMM/yyyy")
##obj.dateDifference("03/10/2016","8893","dd/MM/yyyy")
##obj.dateDifference("03/10/2016","29/05/1992","dd/MM/yyyy")
##obj.dateAddition("29/05/1992","8893","dd/MM/yyyy")
