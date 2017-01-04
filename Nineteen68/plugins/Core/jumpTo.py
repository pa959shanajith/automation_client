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
import Exceptions
import constants

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
    def invoke_jumpto(self,reporting_obj):
        return_value=self.index+1
        try:
            tspList=handler.tspList
            flag=False
            i=-1
            for tsp in tspList:
                i+=1
                inputVal=input[0]
                if inputVal==tsp.testscript_name:
                    flag=True
                    logger.print_on_console('Target index ' +str(i))
                    return_value=i
                    self.status=True
            if(flag==False):
                logger.print_on_console('Test script name not found')
        except Exception as e:
            Exceptions.error(e)

        #Reporting part
        self.step_description='JumpTo executed and the result is '+self.status
        self.parent_id=reporting_obj.get_pid()
        #Reporting part ends
        return self.index+1

