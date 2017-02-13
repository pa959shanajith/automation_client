#-------------------------------------------------------------------------------
# Name:        jumpBy.py
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     03-11-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import handler
import logger

from  constants import *

import logging


log = logging.getLogger('jumpBy.py')


class  JumpBy():
    def __init__(self,index,name,inputval,outputval,stepnum,testscript_name,executed,apptype,additionalinfo,testcase_num):
        self.index=index
        self.name=name
        self.inputval=inputval
        self.testscript_name=testscript_name
        self.outputval=outputval
        self.stepnum=stepnum
        self.executed=executed
        self.apptype=apptype
        self.additionalinfo=additionalinfo
        self.parent_id=0
        self.step_description=''
        self.status=False
        self.testcase_num=testcase_num

    def print_step(self):
        log.info(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name)


    def invoke_jumpby(self,input,reporting_obj):
        log.info('JumpBy Execution Started')
        try:
            log.debug('Reading the inputs')
            index=int(self.index)
            stepToJump=int(input[0])
            tspList=handler.tspList
            jumpByStepNum=-1

            log.debug('Finding out the step number to jump')
            scenario=None
            if (stepToJump > 0) :
                jumpByStepNum = index + 1+ stepToJump
                scenario='positive'
            elif (stepToJump==0):
                logger.print_on_console('ERR_JUMPBY_CAN''T_BE_0')
                log.error('ERR_JUMPBY_CAN''T_BE_0')
            else:
                scenario='negative'
                jumpByStepNum = index - 1+ stepToJump



            if jumpByStepNum<0:

                logger.print_on_console('JumpTo for negitive step  number is not allowed')
                log.error('JumpTo for negitive step  number is not allowed')
                jumpByStepNum=-1

            if jumpByStepNum<len(tspList):
                flag,error=self.__validate_jumpbystep(jumpByStepNum,scenario)
                if(flag):
                    logger.print_on_console('Encountered jumpBy ',str(stepToJump))
                    log.info('Encountered jumpBy '+str(stepToJump))
                    self.status=True
                else:
                    logger.print_on_console(error)
                    jumpByStepNum=TERMINATE

            else:
                jumpByStepNum=-1
                logger.print_on_console('ERR_JUMPY_STEP_DOESN''T_EXISTS')
                log.error('ERR_JUMPY_STEP_DOESN''T_EXISTS')

        except Exception as e:
             log.error(e)
             logger.print_on_console(e)


        #Reporting part
        self.step_description='JumpBy executed and the result is '+str(self.status)
        logger.print_on_console('JumpBy executed and the result is '+str(self.status))
        log.info('JumpBy executed and the result is '+str(self.status))
        self.parent_id=reporting_obj.get_pid()
        reporting_obj.name=self.name
        #Reporting part ends
        return jumpByStepNum


        #Reporting part
        self.step_description='JumpBy executed and the result is '+str(self.status)
        logger.print_on_console('JumpBy executed and the result is '+str(self.status))
        log.info('JumpBy executed and the result is '+self.status)
        self.parent_id=reporting_obj.get_pid()
        reporting_obj.name=self.name
        #Reporting part ends
        return jumpByStepNum


    def __validate_jumpbystep(self,jumpByStepNum,scenario):

        invalid_keyword_list=[STARTLOOP,ELSE_IF,ELSE]
        import handler
        try:
            condition_list= handler.copy_condition_keywords.keys()
            number=min(condition_list, key=lambda x:abs(x-self.index))
            if scenario=='positive':
                if jumpByStepNum>number:
                    return False,'Invalid Jump In If'
            if scenario=='negative':
                if jumpByStepNum<number:
                    return False,'Invalid Jump In If'
            elif handler.tspList[jumpByStepNum].name.lower()==STARTLOOP:
                    return False, 'Jump By The given step is not allowed'
        except Exception as e:
            log.error(e)
        return True,''




