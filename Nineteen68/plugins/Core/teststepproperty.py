#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     18-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
class TestStepProperty():

    def __init__(self,name,index,apptype,inputval,objectname,outputval,stepnum,url,custname,testscript_name,additionalinfo):
        self.name=name
        self.index=index
        self.apptype=apptype
        self.inputval=inputval
        self.objectname=objectname
        self.outputval=outputval
        self.stepnum=stepnum
        self.url=url
        self.custname=custname
        self.testscript_name=testscript_name
        self.additionalinfo = additionalinfo

    def print_step(self):
        logger.log(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+self.apptype)










