#-------------------------------------------------------------------------------
# Name:        delay_operations.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     10-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
import pause_display_operation
import logging
from constants import *

log = logging.getLogger('delay_operations.py')

class Delay_keywords:

    def wait(self,input):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            import time
            if not(input is None and input is ''):
                input=int(input)
                log.info('Wait for :' + str(input) + 'seconds')
                logger.print_on_console('Wait for :' , str(input) , 'seconds')
                time.sleep(input)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            else:
                log.error(INVALID_INPUT)
                err_msg=INVALID_INPUT
                logger.print_on_console(INVALID_INPUT)
        except Exception as e:
            log.error(e)
            
            logger.print_on_console(e)
        return status,methodoutput,output,err_msg

    def pause(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            pause_display_operation.execute()
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            
            logger.print_on_console(e)
        return status,methodoutput,output,err_msg

    def display_variable_value(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            import time
            display_input=''
            input_list=list(args)
            index=input_list.index(';')
            values=input_list[0:index]
            variables=input_list[index+1:len(input_list)]
            for x, y in zip(variables, values):
                if type(x)==unicode or type(x)==str:
                    x=str(x)
                if type(y)==unicode or type(y)==str:
                    y=str(y)
                display_input+=x+' = '+(y if type(y)==str else repr(y))+'\n'
            pause_display_operation.display_value(display_input)
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            
            logger.print_on_console(e)
        return status,methodoutput,output,err_msg


