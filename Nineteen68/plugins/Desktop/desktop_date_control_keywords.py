#-------------------------------------------------------------------------------
# Name:        date_control_keywords.py
# Purpose:     operations to perform date operation on the desktop application
#              Operations supported are setDate, getDate
# Author:      wasimakram.sutar,anas.ahmed
#
# Created:     16/06/2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import desktop_launch_keywords
import logger
from desktop_editable_text import Text_Box
import desktop_constants
import desktop_editable_text
import time
from constants import *
editable_text=desktop_editable_text.Text_Box()

import logging
log = logging.getLogger('desktop_date_control_keywords.py')


month_dict1 = {'JAN' : 1,
              'FEB':2,
              'MAR' : 3,
              'APR':4,
              'MAY' : 5,
              'JUN':6,
              'JUL' : 7,
              'AUG':8,
              'SEP' : 9,
              'OCT':10,
              'NOV' : 11,
              'DEC':12
                }


month_dict2 = { 1 :'JAN',
                2 :'FEB',
                3 : 'MAR' ,
                4 :'APR',
                5 :'MAY',
                6 : 'JUN',
                7 : 'JUL',
                8 : 'AUG',
                9 : 'SEP',
                10 : 'OCT',
                11 : 'NOV',
                12 : 'DEC'
                }
class DateControlKeywords():
    """
        def : setDate
        purpose : set The given date in a DatePicker
        param  : string
        return : string
        """
    def setDate(self,element,parent,input_val, *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if len(input_val) == 2:
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check and element.friendly_class_name() == 'DateTimePicker'):
                    log.info('Parent matched')
                    if(element.is_enabled()):
                        input_date = input_val[0]
                        date_format = input_val[1]
                        valid_date_format = self.validate(date_format)
                        if valid_date_format != -1:
                            split_date = input_date.split('/')
                            if len(split_date) == 3:
                                first_val = split_date[0]
                                second_val = split_date[1]
                                third_val = split_date[2]
                                flag = False
                                day = ''
                                month = ''
                                year = ''
                                try:
                                    if valid_date_format== 1:
                                        day = int(first_val)
                                        month = int(second_val)
                                        year = int(third_val)
                                    elif valid_date_format== 2:
                                        month = int(first_val)
                                        day = int(second_val)
                                        year = int(third_val)
                                    elif valid_date_format== 3:
                                        day = int(first_val)
                                        month = month_dict1[second_val]
                                        year = int(third_val)
                                    elif valid_date_format== 4:
                                        month = month_dict1[first_val]
                                        day = int(second_val)
                                        year = int(third_val)
                                    if isinstance(day,int) and isinstance(month,int) and isinstance(year,int) and day > 0 and month > 0 and year >0:
                                        flag = True

                                    if flag:
                                        element.SetTime(year, month, 0, day, 0, 0, 0, 0)
                                        status = desktop_constants.TEST_RESULT_PASS
                                        result = desktop_constants.TEST_RESULT_TRUE
                                        log.info(STATUS_METHODOUTPUT_UPDATE)
                                    else:
                                        log.info('Input date should contain day,month and year')
                                        logger.print_on_console('Input date should contain day,month and year')
                                        err_msg = 'Input date should contain day,month and year'
                                except Exception as e:
                                    log.error(e)
                                    logger.print_on_console(e)
                        else:
                            log.info('Invalid Date format: Please provide the valid date format')
                            logger.print_on_console('Invalid Date format: Please provide the valid date format')
                            err_msg = 'Invalid Date format: Please provide the valid date format'
                    else:
                        log.info('Date picker control state does not allow to perform the operation')
                        logger.print_on_console('Date picker control  state does not allow to perform the operation')
                        err_msg = 'Date picker control state does not allow to perform the operation'
                else:
                   log.info('Date picker control  not present on the Application where operation is trying to be performed')
                   logger.print_on_console('Date picker control  not present on the Application where operation is trying to be performed')
                   err_msg='Date picker control l not present on the Application where operation is trying to be performed'
            else:
               log.info('Invalid input : Please provide input date and the date format')
               logger.print_on_console('Invalid input : Please provide input date and the date format')
               err_msg='Invalid input : Please provide input date and the date format'
        except Exception as exception:
            import traceback
            traceback.print_exc()
            log.error(exception)
            logger.print_on_console(exception)


        return status,result,verb,err_msg

    def getDate(self,element,parent,input_val, *args):
        """
        def : getDate
        purpose : get The date in the specified format
        param  : string
        return : string
        """
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        items=[]
        try:
            if len(input_val) == 1:
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(element,parent)
                log.debug('Parent of element while scraping')
                log.debug(parent)
                log.debug('Parent check status')
                log.debug(check)
                if (check and element.friendly_class_name() == 'DateTimePicker'):
                    log.info('Parent matched')
                    date_format = input_val[0]
                    valid_date_format = self.validate(date_format)
                    if valid_date_format != -1:
                        date_obj = element.GetTime()
                        res = ''
                        try:
                            if date_obj is not None:
                                if valid_date_format== 1:
                                    day = date_obj.wDay
                                    month = date_obj.wMonth
                                    year = date_obj.wYear
                                    res = str(day) + '/' + str(month) + '/' + str(year)
                                    flag = True
                                elif valid_date_format== 2:
                                    month = date_obj.wMonth
                                    day = date_obj.wDay
                                    year = date_obj.wYear
                                    res = str(month) + '/' + str(day) + '/' + str(year)
                                    flag = True
                                elif valid_date_format== 3:
                                    day = date_obj.wDay
                                    month = month_dict2[date_obj.wMonth]
                                    year = date_obj.wYear
                                    res = str(day) + '/' + str(month) + '/' + str(year)
                                    flag = True
                                elif valid_date_format== 4:
                                    month = month_dict2[date_obj.wMonth]
                                    day = date_obj.wDay
                                    year = date_obj.wYear
                                    res = str(month) + '/' + str(day) + '/' + str(year)
                                    flag = True


                                if flag:
                                    verb = res
                                    status = desktop_constants.TEST_RESULT_PASS
                                    result = desktop_constants.TEST_RESULT_TRUE
                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                        except Exception as e:
                            print e
                            import traceback
                            traceback.print_exc()
                            log.error(e)
                            logger.print_on_console(e)
                    else:
                        log.info('Invalid Date format: Please provide the valid date format')
                        logger.print_on_console('Invalid Date format: Please provide the valid date format')
                        err_msg = 'Invalid Date format: Please provide the valid date format'

                else:
                   log.info('Date picker control  not present on the Application where operation is trying to be performed')
                   logger.print_on_console('Date picker control  not present on the Application where operation is trying to be performed')
                   err_msg='Date picker control l not present on the Application where operation is trying to be performed'
            else:
               log.info('Invalid input : Please provide input date and the date format')
               logger.print_on_console('Invalid input : Please provide input date and the date format')
               err_msg='Invalid input : Please provide input date and the date format'
        except Exception as exception:
            import traceback
            traceback.print_exc()
            log.error(exception)
            logger.print_on_console(exception)


        return status,result,verb,err_msg


    def validate(self,input_format):
        try:
            date_format_supported = {'dd/MM/yyyy' : 1,
                        'MM/dd/yyyy':2,
                        'dd/MMM/yyyy' : 3,
                        'MMM/dd/yyyy' : 4}
            if(input_format in date_format_supported):
                date_format = date_format_supported.get(input_format)
                return date_format
            else:
                return -1
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)

