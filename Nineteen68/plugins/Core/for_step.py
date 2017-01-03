#-------------------------------------------------------------------------------
# Name:        module1
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
iteration_count=0

class For():

    """Object instantiation of 'for,endfor' object"""
    def __init__(self,index,name,inputval,outputval,stepnum,testscript_name,info_dict,executed,apptype,additionalinfo):
        self.index=index
        self.name=name
        self.inputval=inputval
        self.info_dict=info_dict
        self.testscript_name=testscript_name
        self.outputval=outputval
        self.stepnum=stepnum
        self.executed=executed
        self.apptype=apptype,
        self.count=0
        self.additionalinfo = additionalinfo
        self.parent_id=0
        self.step_description=''


    def print_step(self):
        logger.log(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+str(self.info_dict))

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

    def invokeFor(self,input,reporting_obj):
        global iteration_count


        #block to execute endFor
        if self.name.lower() == constants.ENDFOR:
            logger.log('\nEncountered :'+self.name+'\n')
            self.executed=True
            index=self.getEndfor()
            logger.log('***For: Iteration '+str(iteration_count)+' completed***\n\n')
            #Reporting part
            self.add_report_step(reporting_obj,'For: Iteration '+str(iteration_count)+' completed')
            #Reporting part ends

            return index

        #block to execute for
        if self.name==constants.FOR:


            endForNum = self.info_dict[0].keys()[0]
            try:
                inputval = int(input[0])
            except ValueError:
                logger.log('\nEncountered :'+self.name+'\n')
                logger.log('Invalid for count '+input[0]+'\n')
                #Reporting part
                self.step_description='Encountered :'+self.name+' Invalid for count '+input[0]
                #Reporting part ends
                self.executed=False
                forIndex=endForNum+1
                return forIndex
                iteration_count=0

            forIndex = self.index+1;
            if (inputval > 0 and inputval != 0):
                self.count=self.count+1

                if not(self.count<= inputval):
                    iteration_count=0
                    self.count=0
                    self.executed=False
                    forIndex=endForNum+1

                    #Reporting part
                    reporting_obj.name=constants.ENDFOR
                    self.add_report_step(reporting_obj,'EndFor: completed')
                    #Reporting part ends


                else:
                    if self.count==1:
                        logger.log('\nEncountered :'+self.name+'\n')
                        #Reporting part
                        self.add_report_step_for(reporting_obj,'Encountered :'+self.name)
                        #Reporting part ends
                    self.executed=True
                    iteration_count=self.count
                    logger.log('***For: Iteration '+str(self.count)+ ' started***')

                    #Reporting part
                    self.add_report_step_iteration(reporting_obj,'For: Iteration '+str(iteration_count)+' started')
                    #Reporting part ends

            return forIndex

    def getEndfor(self):
        index=None
        if self.info_dict is not None:
            index= self.info_dict[0].keys()[0]
        return index



