#-------------------------------------------------------------------------------
# Name:        for_step.py
# Purpose:
#
# Author:      rakesh.v
#
# Created:     04-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
import constants
##iteration_count={}
import logging
log = logging.getLogger('for_step.py')
import threading
local_for = threading.local()

class For():

    """Object instantiation of 'for,endfor' object"""
    def __init__(self,index,name,inputval,outputval,stepnum,testscript_name,info_dict,executed,apptype,additionalinfo,testcase_num,remark,testcase_details):
        self.index=index
        self.name=name
        self.inputval=inputval
        self.info_dict=info_dict
        self.testscript_name=testscript_name
        self.outputval=outputval
        self.stepnum=stepnum
        self.executed=executed
        self.status=constants.TEST_RESULT_PASS
        self.apptype=apptype
        self.count=0
        self.additionalinfo = additionalinfo
        self.parent_id=0
        self.step_description=''
        self.testcase_num=testcase_num
        self.remarks=remark
        self.testcase_details=testcase_details
        local_for.iteration_count={}


    def print_step(self):
        log.info(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+str(self.info_dict))

    def add_report_step(self,reporting_obj,step_description):
        #Reporting part
        self.step_description=step_description
        self.parent_id=reporting_obj.get_pid()
        reporting_obj.pop_pid()
        reporting_obj.remove_nested_flag()
        #Reporting part ends

    def add_report_step_iteration(self,reporting_obj,step_description):
        #Reporting part
        self.step_description=step_description
        self.parent_id=reporting_obj.get_pid()
        reporting_obj.add_pid(self.name)
        #Reporting part ends

    def add_report_step_for(self,reporting_obj,step_description):
        #Reporting part
        self.step_description=step_description
        self.parent_id=reporting_obj.get_pid()
        reporting_obj.add_pid(self.name)
        reporting_obj.generate_report_step(self,'',step_description,'3.00',False)
        #Reporting part ends

    def invalid_for_input(self,endForNum,inputval,reporting_obj):
        logger.print_on_console('\nEncountered :'+self.name+'\n')
        logger.print_on_console('Invalid for count '+inputval+'\n')
        #Reporting part
        self.step_description='Encountered :'+self.name+' Invalid for count '+inputval
        reporting_obj.name=constants.ENDFOR
        self.add_report_step(reporting_obj,constants.ENDFOR_DESCRIPTION)
        #Reporting part ends
        self.executed=False
        self.status=constants.TEST_RESULT_FAIL
        forIndex=endForNum+1
        return forIndex



    def invokeFor(self,input,reporting_obj):
        global local_for

        #block to execute endFor
        if self.name.lower() == constants.ENDFOR:
            logger.print_on_console('\nEncountered :'+self.name+'\n')
            self.executed=True
            index=self.getEndfor()
            logger.print_on_console('***For: Iteration '+str(local_for.iteration_count[index])+' completed***\n')
            log.info('***For: Iteration '+str(local_for.iteration_count[index])+' completed***\n')
            #Reporting part
            self.add_report_step(reporting_obj,'Iteration: '+str(local_for.iteration_count[index])+' executed')
            #Reporting part ends

            return index


        #block to execute for
        if self.name.lower()==constants.FOR:

            endForNum = list(self.info_dict[0].keys())[0]
            inputval=input[0]
            try:
                if(int(input[0]) <= 0):
                    forIndex=self.invalid_for_input(endForNum,inputval,reporting_obj)
                    local_for.iteration_count[self.index]=0
                    return forIndex
                else:
                   inputval = int(input[0])
                   local_for.iteration_count[self.index]=0
            except ValueError:
                forIndex=self.invalid_for_input(endForNum,inputval,reporting_obj)
                local_for.iteration_count[self.index]=0
                return forIndex


            forIndex = self.index+1;
            if (inputval > 0 and inputval != 0):
                self.count=self.count+1

                if not(self.count<= inputval):
                    local_for.iteration_count[self.index]=0
                    self.count=0
                    self.executed=False
                    forIndex=endForNum+1

                    #Reporting part
                    reporting_obj.name=constants.ENDFOR
                    self.add_report_step(reporting_obj,constants.ENDFOR_DESCRIPTION)
                    #Reporting part ends


                else:
                    if self.count==1:
                        logger.print_on_console('\nEncountered :'+self.name+'\n')
                        #Reporting part
                        self.add_report_step_for(reporting_obj,'Execute the steps in the loop for the given count '+str(inputval))
                        #Reporting part ends
                    self.executed=True
                    local_for.iteration_count[self.index]=self.count
                    logger.print_on_console('***For: Iteration '+str(self.count)+ ' started***')
                    log.info('***For: Iteration '+str(self.count)+ ' started***')

                    #Reporting part
                    self.add_report_step_iteration(reporting_obj,'Iteration '+str(local_for.iteration_count[self.index])+' started')
                    #Reporting part ends
            else:
                forIndex=self.invalid_for_input(endForNum,inputval,reporting_obj)
                local_for.iteration_count[self.index]=0

            return forIndex

    def getEndfor(self):
        index=None
        if self.info_dict is not None:
            index= list(self.info_dict[0].keys())[0]
        return index



