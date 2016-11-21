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
from constants import *
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
        self.status=False
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
        start_step=self.info_dict[0]
        next_target=self.info_dict[1]
        if len(self.info_dict)>2:
            last_target=self.info_dict[2]
        else:
            last_target=next_target

        next_index=index+1
        #block to execute if,elseIf part
        if self.name.lower() in [IF,ELSE_IF]:

            #Check is made when elseIf is encountered to ensure it is to be executed or not
            if self.name.lower() == ELSE_IF:
                step=handler.tspList[start_step.keys()[0]]
                if step.status==True:
                    return last_target.keys()[0]

            logger.log('Encountered :'+self.name+'\n')
            logical_eval_obj=Logical_eval()
            input_expression=self.inputval
            logger.log('Input_expression is '+input_expression)
            res=logical_eval_obj.eval_expression(input_expression)
            logger.log(self.name+': Condition is '+str(res)+'\n')


            if res==True:
                self.status=True
                logger.log('***Started executing:'+self.name+'***\n')
                return self.index+1
            elif res==INVALID:
                logger.log('Invalid conditional expression\n')
                return last_target.keys()[0]
            else:
                return next_target.keys()[0]



        #block to execute else part
        elif self.name.lower() in [ELSE]:
            step=handler.tspList[start_step.keys()[0]]
            if step.status==False:
                logger.log('***Started executing:'+self.name+'***\n')
                return self.index+1
            else:
                return last_target.keys()[0]

        #block to execute endIf
        else:
            logger.log('Encountered :'+self.name+'\n')
            logger.log('***If execution completed ***\n')
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
            return INVALID


