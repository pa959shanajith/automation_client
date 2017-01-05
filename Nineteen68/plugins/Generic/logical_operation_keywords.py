#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     26-10-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from sympy.logic.inference import satisfiable
import Exceptions
import logger
from constants import *
from loggermessages import *
import logging


log = logging.getLogger('logical_operation_keywords.py')
class logical_eval():

    def eval_expression(self,expression,*args):
        log.info(KEYWORD_EXECUTION_STARTED)
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        error_msg=None
        output_res=MD5_TEMP_RES
        log.debug('reading the inputs')
        if len(expression==2):
            expression=expression[0]+expression[1]+expression[2]
            expression=expression.replace('AND','and').replace('OR','or').replace('NOT','not')
            try:
                logger.print_on_console('Evaluationg the expression')
                result=satisfiable(expression)
                if type(result)==dict:
                    for res in result.iterkeys():
                        status=result[res]
                        log.debug('Got the result : %s', status)
                        if status==True:
                            log.debug('Got the result : %s', status)
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                else:
                    log.info('Expression evaluation failed')
            except Exception as e:
                log.error(e)
                
                logger.print_on_console(e)
                error_msg=e
        else:
            log.error('invalid expression')

        return status,methodoutput,output_res,error_msg


