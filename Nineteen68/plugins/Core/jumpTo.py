#-------------------------------------------------------------------------------
# Name:        module1
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
import constants
from  constants import *
import logging


log = logging.getLogger('jumpTo.py')

# Handles JumpTo keyword
class  JumpTo():

    def __init__(self,index,name,inputval,outputval,stepnum,testscript_name,executed,apptype,additionalinfo):
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

    def print_step(self):
        logger.print_on_console(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name)

    # returns jumpTo index of step to executed by taking the script name as parameter
    def invoke_jumpto(self,input,reporting_obj,counter):
        log.info('JumpTo Execution Started')
        return_value=self.index+1
        try:
            log.debug('Get the tsp list')
            tspList=handler.tspList
            flag=False
            i=-1
            log.debug('Searching for Test script name in tsp list')
            for tsp in tspList:
                i+=1
                inputVal=input[0]
                if inputVal==tsp.testscript_name:
                    flag=True
                    log.debug('Found  target index in tsp list')
                    logger.print_on_console('Target index ' +str(i))
                    return_value=i
                    self.status=True
                    no_Of_Test_steps=self.getNoOfStepsInTestScript(i,tsp.testscript_name,handler.tspList)
                    break
            if(flag==False):
                logger.print_on_console('Test script name not found')
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)


        #Reporting part
        self.step_description='JumpTo executed and the result is '+ str(self.status)
        self.parent_id=reporting_obj.get_pid()
        reporting_obj.name=self.name
        #Reporting part ends
        return return_value,no_Of_Test_steps


    # returns no of steps inside the test script
    def getNoOfStepsInTestScript(self,current_index,actual_testscript_name,tspList):
        return_value=None
        try:
            j=current_index
            for abc in range(j,len(tspList)):
##            while True:
                if tspList[abc].testscript_name==actual_testscript_name:
                    j=j+1
                    continue
##                elif j==len(tspList):
##                    break
                else:
                    break

            return_value=j
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        return return_value
