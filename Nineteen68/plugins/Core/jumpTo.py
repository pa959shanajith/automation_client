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

    def print_step(self):
        logger.log(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name)

    # returns jumpTo index of step to executed by taking the script name as parameter
    def invoke_jumpto(self):
        try:
            tspList=handler.tspList
            flag=False
            i=-1
            for tsp in tspList:
                i+=1
                inputVal=self.inputval[0]
                if inputVal==tsp.testscript_name:
                    flag=True
                    logger.log('Target index ' +str(i))
                    return i
            if(flag==False):
                logger.log('Test script name not found')
        except Exception as e:
            Exceptions.error(e)
        return self.index+1

