#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     10-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
import Exceptions
import pause_display_operation
from constants import *

class Delay_keywords:

    def wait(self,input):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            import time
            if not(input is None and input is ''):
                input=int(input)
                logger.log('wait method started')
                time.sleep(input)
                logger.log('wait method completed')
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def pause(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            pause_display_operation.execute()
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def display_variable_value(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
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
            Exceptions.error(e)
        return status,methodoutput


