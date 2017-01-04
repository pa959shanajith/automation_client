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


    def invoke_jumpby(self,input,reporting_obj):
        try:
            index=int(self.index)
            stepToJump=int(input[0])
            tspList=handler.tspList
            jumpByStepNum=-1


            if (stepToJump > 0) :
                jumpByStepNum = index + 1+ stepToJump
            elif (stepToJump==0):
                logger.print_on_console('ERR_JUMPBY_CAN''T_BE_0')
            else:
				jumpByStepNum = index - 1+ stepToJump


            if jumpByStepNum<0:
                logger.print_on_console('Invalid Input')
                jumpByStepNum=-1

            elif jumpByStepNum<len(tspList):
                flag=self.__validate_jumpbystep(jumpByStepNum)
                self.status=True

            else:
                jumpByStepNum=-1
                logger.print_on_console('ERR_JUMPY_STEP_DOESN''T_EXISTS')

        except Exception as e:
            Exceptions.error(e)

        #Reporting part
        self.step_description='JumpBy executed and the result is '+self.status
        self.parent_id=reporting_obj.get_pid()
        #Reporting part ends
        return jumpByStepNum


    def __validate_jumpbystep(self,input):
        import handler
        condition_list= handler.condition_keywords.keys()
        number=min(condition_list, key=lambda x:abs(x-self.index))




