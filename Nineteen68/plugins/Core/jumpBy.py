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
class  JumpBy():
    def __init__(self,index,name,inputval,outputval,stepnum,testscript_name,executed,apptype):
        self.index=index
        self.name=name
        self.inputval=inputval[0]
        self.testscript_name=testscript_name
        self.outputval=outputval
        self.stepnum=stepnum
        self.executed=executed
        self.apptype=apptype

    def print_step(self):
        logger.log(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name)


    def invoke_jumpby(self):
        try:
            index=int(self.index)
            stepToJump=int(self.inputval)
            tspList=handler.tspList

            if (stepToJump > 0) :
                jumpByStepNum = index + 1+ stepToJump
            elif (stepToJump==0):
                logger.log('ERR_JUMPBY_CAN''T_BE_0')
                return -1
            else:
				jumpByStepNum = index - 1+ stepToJump


            if jumpByStepNum<0:
                logger.log('Invalid Input')

            elif jumpByStepNum<len(tspList):
                flag=self.__validate_jumpbystep(jumpByStepNum)
                return jumpByStepNum
            else:
                logger.log('ERR_JUMPY_STEP_DOESN''T_EXISTS')

        except Exception as e:
            Exceptions.error(e)
        return -1


    def __validate_jumpbystep(self,input):
        import handler
        print 'JUMPPPPP',input
        condition_list= handler.condition_keywords.keys()
        number=min(condition_list, key=lambda x:abs(x-self.index))
##        start_index=
##        if condition_list[0] < self.index < condition_list[1]:

##        if get_step.name==constants.IF or index<keys:
##            return True



