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

class logical_eval():

    def eval_expression(self,expression):
        expression=str(expression)
        expression=expression.replace('AND','and').replace('OR','or').replace('NOT','not')
        try:
            logger.log('Evaluationg the expression')
            result=satisfiable(expression)
            if type(result)==dict:
                for res in result.iterkeys():
                    status=result[res]
                    return status
            else:
                return False
        except Exception as e:
            Exceptions.error(e)




