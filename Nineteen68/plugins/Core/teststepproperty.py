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

class TestStepProperty():

    def __init__(self,keyword,apptype,inputval,objectname,outputval,stepnum,url,custname,testscriptname):
        self.keyword=keyword
        self.apptype=apptype
        self.inputval=inputval
        self.objectname=objectname
        self.outputval=outputval
        self.stepnum=stepnum
        self.url=url
        self.custname=custname
        self.testscriptname=testscriptname

    def print_step(self):
##        print step.keyword,step.apptype,step.inputval,step.objectname,step.outputval,step.stepnum,step.url,step.custname,step.testscriptname+'\n'
        print self.stepnum,self.keyword,self.apptype,self.inputval,self.objectname,self.outputval,self.url,self.custname,self.testscriptname+'\n'











