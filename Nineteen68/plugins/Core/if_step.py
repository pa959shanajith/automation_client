#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     21-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger
class If():

    """Object instantiation of 'for' object"""
    def __init__(self,index,name,inputval,outputval,step_num,testscript_name,info_dict,executed):
        self.index=index
        self.name=name
        self.inputval=inputval
        self.info_dict=info_dict
        self.testscript_name=testscript_name
        self.outputval=outputval
        self.step_num=step_num
        self.executed=executed

    def print_step(self):
        logger.log('Stepno:'+str(self.step_num)+'keyword:'+self.name+'Inputval:'+str(self.inputval)+'OutputVal:'+self.outputval+'testscript_name:'+self.testscript_name+'Info_dict'+str(self.info_dict)+'\n')
