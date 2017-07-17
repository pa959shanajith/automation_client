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
import json
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
        self.jumpByStepNum=-1

    def print_step(self):
        log.info(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name)


    def invoke_jumpby(self,input,reporting_obj):
        log.info('JumpBy Execution Started')
        try:
            log.debug('Reading the inputs')
            index=int(self.index)
            stepToJump=int(input[0])
            tspList=handler.tspList
            self.jumpByStepNum=-1

            log.debug('Finding out the step number to jump')
            scenario=None
            if (stepToJump > 0) :
                self.jumpByStepNum = index + 1+ stepToJump
                scenario='positive'
            elif (stepToJump==0):
                logger.print_on_console('ERR_JUMPBY_CAN''T_BE_0')
                log.error('ERR_JUMPBY_CAN''T_BE_0')
            else:
                scenario='negative'
                self.jumpByStepNum = index - 1+ stepToJump



            if self.jumpByStepNum<0:

                logger.print_on_console('JumpBy for negitive step  number is not allowed')
                log.error('JumpBy for negitive step  number is not allowed')
                self.jumpByStepNum=-1

            if self.jumpByStepNum<len(tspList):
                flag,error=self.__validate_jumpbystep(stepToJump)
                if(flag):
                    logger.print_on_console('Encountered jumpBy ',str(stepToJump))
                    log.info('Encountered jumpBy '+str(stepToJump))
                    self.status=True
                else:
                    for err in error:
                        logger.print_on_console(err)
                    self.jumpByStepNum=TERMINATE

            else:
                self.jumpByStepNum=index + 1
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
        return self.jumpByStepNum

    # Issue #153 and #167
    def __validate_jumpbystep(self,stepToJump):
        import handler
        try:
            if len(handler.cond_nest_info)==0:
            	handler.cond_nest_info = self.__generate_conditional_structure(handler.copy_condition_keywords)
            if handler.tspList[self.jumpByStepNum].name.lower()==STARTLOOP:
                return False, ['Jump By The given step is not allowed']
            else:
                t_obj=handler.cond_nest_info
                for item in t_obj:
                    if self.jumpByStepNum>=item['st'] and self.jumpByStepNum<=item['en']:
                        if self.index>item['st'] and self.index<item['en']:
                            t_obj=item['c']
                        else:
                            return False, ['Encountered jumpBy '+str(stepToJump),'Input error: please provide the valid input']
        except Exception as e:
            log.error(e)
        return True,['']

    def __generate_conditional_structure(self,condition_keywords):
        cn=0
        unix=1
        t_obj=[]
        t_obj.append({'p':-1,'c':[],'l':0})
        for idx,kw in condition_keywords.iteritems():
        	if kw=='if':
        		if cn==-1:
        			cn=0
        		else:
        			cn=unix-1
        		t_obj.append({'p':cn,'c':[],'l':t_obj[cn]['l']+1,'st':idx,'en':-1})
        		t_obj[cn]['c'].append(t_obj[unix])
        		unix+=1
        	if kw=='elseif' or kw=='else':
        		p_list=t_obj[cn]['c']
        		p_list[len(p_list)-1]['en']=idx-1
        		t_obj.append({'p':cn,'c':[],'l':t_obj[cn]['l']+1,'st':idx,'en':-1})
        		t_obj[cn]['c'].append(t_obj[unix])
        		unix+=1
        	if kw=='endif':
        		p_list=t_obj[cn]['c']
        		p_list[len(p_list)-1]['en']=idx-1
        		cn=t_obj[cn]['p']
       	return json.loads(json.dumps(t_obj[0]))['c']
