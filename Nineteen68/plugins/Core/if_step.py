#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     21-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger
from sympy.logic.inference import satisfiable
import Exceptions
import logger
import handler
import constants
import controller


class If():
    """Object instantiation of 'for' object"""
    def __init__(self,index,name,inputval,outputval,stepnum,testscript_name,info_dict,executed,apptype):
        self.index=index
        self.name=name
        self.inputval=inputval[0]
        self.info_dict=info_dict
        self.testscript_name=testscript_name
        self.outputval=outputval
        self.stepnum=stepnum
        self.executed=executed
        self.apptype=apptype

    def print_step(self):
        logger.log(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+str(self.info_dict))



    def invoke_condtional_keyword(self):

        """
        def : invoke_condtional_keyword
        purpose : executes if,elseIf,else,endIf keyword
        param :
        return :

        """

        self.executed=True
        index=self.index
        end_info=self.info_dict
        next_target=self.info_dict[0]
        if len(self.info_dict)>1:
            last_target=self.info_dict[1]
        else:
            last_target=next_target

        next_index=index+1
        if self.name.lower() in [constants.IF,constants.ELSE_IF]:
            logical_eval_obj=Logical_eval()
            input_expression=self.inputval
            logger.log('Input_expression is '+input_expression)
            res=logical_eval_obj.eval_expression(input_expression)
            logger.log('Condition is '+str(res))
            if res==True:
                logger.log('Started executing:'+self.name)
                return self.execution(next_index,next_target,last_target)
            elif res==constants.INVALID:
                logger.log('Invalid conditional expression')
                return last_target.keys()[0]
            else:
                return next_target.keys()[0]
        elif self.name.lower() in [constants.ELSE]:
            logger.log('Executing:'+self.name)
            return self.execution(next_index,next_target,last_target)

        else:
            logger.log('Encountered:'+self.name)
            return next_index

    def execution(self,next_index,next_target,last_target):
        obj=controller.Controller()
        while (next_index<next_target.keys()[0]):
            next_index=obj.methodinvocation(next_index)
        if next_index==next_target.keys()[0]:
            next_index=last_target.keys()[0]
        return next_index


class Logical_eval():

    def eval_expression(self,expression):
        expression=str(expression)
        expression=expression.replace('AND','and').replace('OR','or').replace('NOT','not')
        try:
            result=satisfiable(expression)
            if type(result)==dict:
                for res in result.iterkeys():
                    status=result[res]
                    return status
            else:
                return False
        except Exception as e:
            Exceptions.error(e)
            return constants.INVALID


