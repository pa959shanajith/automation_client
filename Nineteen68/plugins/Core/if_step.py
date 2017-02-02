#-------------------------------------------------------------------------------
# Name:        if_step.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     21-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from sympy.logic.inference import satisfiable

import logger
import handler
from constants import *
import reporting
import logging
import dynamic_variable_handler

log = logging.getLogger('if_step.py')

class If():
    """Object instantiation of 'for' object"""
    def __init__(self,index,name,inputval,outputval,stepnum,testscript_name,info_dict,executed,apptype,additionalinfo):
        self.index=index
        self.name=name
        self.inputval=inputval
        self.info_dict=info_dict
        self.testscript_name=testscript_name
        self.outputval=outputval
        self.stepnum=stepnum
        self.executed=executed
        self.status=False
        self.apptype=apptype
        self.additionalinfo = additionalinfo
        self.parent_id=0
        self.step_description=''

    def print_step(self):
        log.info(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+str(self.info_dict))



    def invoke_condtional_keyword(self,input,reporting_obj):

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
        #NO need to keep track of next targets when endIf is encountered
        if self.name.lower() != ENDIF:
            self.step_description='Encountered :'+self.name
            next_target=self.info_dict[1]
            if len(self.info_dict)>2:
                last_target=self.info_dict[2]
            else:
                last_target=next_target

        next_index=index+1
        #block to execute if,elseIf part
        if self.name.lower() in [IF,ELSE_IF]:


            input_expression=None
            #Check is made when elseIf is encountered to ensure it is to be executed or not
            if self.name.lower() == ELSE_IF:
                step=handler.tspList[start_step.keys()[0]]
                #This check is to make sure that if the previous if/elseIf is already exeucted then do not execute next elseIf/else blocks
                #Hence ,it should  send the index after 'endIf' step
                if step.status==True:
                    self.parent_id=reporting_obj.get_pid()
                    return last_target.keys()[0]

            logger.print_on_console('Encountered :'+self.name+'\n')
            logical_eval_obj=Logical_eval()
            input_expression=''
            if len(input)>=2:
                for exp in input:
                    input_expression=input_expression+exp
            else:
                logger.print_on_console('Invalid input')

            if '{' in input_expression and '}' in input_expression :
                import re
                dyn_var_list=re.findall("\{(.*?)\}", input_expression)
                if len(dyn_var_list)>0:
                    import string
                    for var in dyn_var_list:
                        value=dynamic_variable_handler.dynamic_variable_map['{'+var+'}']
                        input_expression=string.replace(input_expression,'{'+var+'}',value)
            logger.print_on_console('Input_expression is ',input_expression)
            res=logical_eval_obj.eval_expression(input_expression)
            logger.print_on_console(self.name+': Condition is '+str(res)+'\n')
            self.step_description='Encountered :'+self.name+ ' Condition is '+str(res)


            if res==True:
                #Reporting part
                self.parent_id=reporting_obj.get_pid()
                reporting_obj.add_pid(self.name)
                #Reporting part ends

                self.status=True
                logger.print_on_console('***Started executing:'+self.name+'***\n')
                return self.index+1
            elif res==INVALID:
                if self.name==IF:
                    self.parent_id=reporting_obj.get_pid()
                    reporting_obj.add_pid(self.name)

                logger.print_on_console('Invalid conditional expression\n')
                return last_target.keys()[0]
            else:
                return next_target.keys()[0]



        #block to execute else part
        elif self.name.lower() in [ELSE]:
            self.step_description='Encountered :'+self.name
            step=handler.tspList[start_step.keys()[0]]
            #This check is to make sure that if the previous if/elseIf is False ,only then enter the else block
            #else ,it should  send the index after 'endIf' step
            if step.status==False:

                #Reporting part
                self.parent_id=reporting_obj.get_pid()
                reporting_obj.add_pid(self.name)
                #Reporting part ends

                logger.print_on_console('***Started executing:'+self.name+'***\n')
                return self.index+1
            else:
                return last_target.keys()[0]

        #block to execute endIf
        else:
            #Reporting part
            self.parent_id=reporting_obj.get_pid()
            reporting_obj.pop_pid()
            reporting_obj.remove_nested_flag()
            self.step_description='Encountered :'+self.name
            #Reporting part ends

            logger.print_on_console('Encountered :'+self.name+'\n')
            logger.print_on_console('***If execution completed ***\n')
            return next_index



class Logical_eval():

    #Block to evaluate conditional expression
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


