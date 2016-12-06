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
        self.count=0,
        self.additionalinfo = additionalinfo


    def print_step(self):
        logger.log(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+str(self.info_dict))

    def invokeFor(self):
        obj=controller.Controller()

        #block to execute endFor
        if self.name.lower() == constants.ENDFOR:
            self.executed=True
            index=self.getEndfor()
            logger.log('***For: Iteration completed***\n\n')
            return index

        #block to execute for
        if self.name==constants.FOR:
            logger.log('Encountered :'+self.name+'\n')
            endForNum = self.info_dict[0].keys()[0]
            try:
                inputval = int(self.inputval[0])
            except ValueError:
                logger.log('Invalid for count '+self.inputval[0]+'\n')
                self.executed=False
                forIndex=endForNum+1
                return forIndex

            forIndex = self.index+1;
            if (inputval > 0 and inputval != 0):
                self.count=self.count+1

                if not(self.count<= inputval):
                    self.count=0
                    self.executed=False
                    forIndex=endForNum+1
                else:
                    self.executed=True
                    logger.log('***For: Iteration '+str(self.count)+ ' started***')

            return forIndex

    def getEndfor(self):
        index=None
        if self.info_dict is not None:
            index= self.info_dict[0].keys()[0]
        return index



