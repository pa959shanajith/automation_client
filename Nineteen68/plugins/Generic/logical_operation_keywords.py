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

import logger
from constants import *

import logging


log = logging.getLogger('logical_operation_keywords.py')
class logical_eval():

    def eval_expression(self,expression,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_res=OUTPUT_CONSTANT
        log.debug('reading the inputs')
        if len(expression==2):
            expression=expression[0]+expression[1]+expression[2]
            logger.print_on_console('input expression is'+expression)
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
                            logger.print_on_console('result obtained'+status)
                else:
                    log.info('Expression evaluation failed')
            except Exception as e:
                log.error(e)
                logger.print_on_console(e)
                err_msg=INPUT_ERROR
        else:
            log.error('invalid expression')
        return status,methodoutput,output_res,err_msg


