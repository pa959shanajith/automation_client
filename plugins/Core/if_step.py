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

log = logging.getLogger('if_step.py')

class If():
    """Object instantiation of 'for' object"""
    def __init__(self,index,name,inputval,outputval,stepnum,testscript_name,info_dict,executed,apptype,additionalinfo,testcase_num,remark,testcase_details):
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
        self.testcase_num=testcase_num
        self.remarks=remark
        self.testcase_details=testcase_details

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

            #Check is made when elseIf is encountered to ensure it is to be executed or not
            if self.name.lower() == ELSE_IF:
                step=handler.local_handler.tspList[list(start_step.keys())[0]]
                #This check is to make sure that if the previous if/elseIf is already exeucted then do not execute next elseIf/else blocks
                #Hence ,it should  send the index after 'endIf' step
                if step.status==True:
                    self.parent_id=reporting_obj.get_pid()
                    return list(last_target.keys())[0]

            logger.print_on_console('Encountered :'+self.name+'\n')
            if len(input)>2 and input[2] is not None:
                logger.print_on_console('Input expression is',input[2])
            else:
                logger.print_on_console('Input expression is',input[0])
            res=INVALID
            if input[1] is not None:
                errs=input[1].split('\n')
                if errs[-1]=='':
                    errs=errs[:-1]
                for err in errs:
                    logger.print_on_console(err+'\n')
            else:
                logical_eval_obj=Logical_eval()
                res=logical_eval_obj.eval_expression(input[0])
                if len(res)>1:
                    logger.print_on_console(self.name+': '+res[1]+'\n')
                res=res[0]
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
                self.status=False
                logger.print_on_console('Invalid conditional expression\n')
                return list(last_target.keys())[0]
            else:
                self.status=False
                return list(next_target.keys())[0]



        #block to execute else part
        elif self.name.lower() in [ELSE]:
            self.step_description='Encountered :'+self.name
            step=handler.local_handler.tspList[list(start_step.keys())[0]]
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
                return list(last_target.keys())[0]

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
        try:
            if SYSTEM_OS == "Windows":
                result=satisfiable(expression)
                if type(result)==dict:
                    for res in result.keys():
                        status=result[res]
                        return [status]
                else:
                    return [False]
            else:
                status = eval(expression)
                return [status]
        except Exception as e:
            if e.__class__.__name__=='TypeError':
                return [INVALID,str(e)]
            return [INVALID]


