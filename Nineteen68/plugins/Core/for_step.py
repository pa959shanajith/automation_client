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
import controller
import constants
class For():

    """Object instantiation of 'for,endfor' object"""
    def __init__(self,index,name,inputval,outputval,stepnum,testscript_name,info_dict,executed,apptype):
        self.index=index
        self.name=name
        self.inputval=inputval[0]
        self.info_dict=info_dict
        self.testscript_name=testscript_name
        self.outputval=outputval
        self.stepnum=stepnum
        self.executed=executed
        self.apptype=apptype

    def print_step(self):
        logger.log(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+str(self.info_dict))

    def invokeFor(self):
        obj=controller.Controller()
        if self.name.lower() == constants.ENDFOR:
            index=self.getEndfor()
            return index

        if self.name==constants.FOR:
            endForNum = self.info_dict[0].keys()[0]
            inputval = int(self.inputval)
            forIndex = self.index+1;
            if (inputval > 0 and inputval != 0):
                j =0
                while (forIndex <= endForNum):
                    if forIndex != endForNum:
                        forIndex = obj.methodinvocation(forIndex)
                    else:
                        j+=1
                        if (j < inputval):
                            index=obj.methodinvocation(forIndex)
                            forIndex = index + 1
                        else:
                            return endForNum+1
            else:
                return endForNum+1



    def getEndfor(self):
        return self.info_dict[0].keys()[0]
