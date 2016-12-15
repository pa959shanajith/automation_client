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


    def print_step(self):
        logger.log(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+str(self.info_dict))

    def invokeFor(self,input):
        global iteration_count


        #block to execute endFor
        if self.name.lower() == constants.ENDFOR:
            logger.log('\nEncountered :'+self.name+'\n')
            self.executed=True
            index=self.getEndfor()
            logger.log('***For: Iteration '+str(iteration_count)+' completed***\n\n')
            return index

        #block to execute for
        if self.name==constants.FOR:
            endForNum = self.info_dict[0].keys()[0]
            try:
                inputval = int(input[0])
            except ValueError:
                logger.log('\nEncountered :'+self.name+'\n')
                logger.log('Invalid for count '+input[0]+'\n')
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
                else:
                    logger.log('\nEncountered :'+self.name+'\n')
                    self.executed=True
                    iteration_count=self.count
                    logger.log('***For: Iteration '+str(self.count)+ ' started***')

            return forIndex

    def getEndfor(self):
        index=None
        if self.info_dict is not None:
            index= self.info_dict[0].keys()[0]
        return index



