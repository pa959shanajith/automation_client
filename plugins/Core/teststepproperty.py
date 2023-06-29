#-------------------------------------------------------------------------------
# Name:        teststepproperty.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     18-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
import logging
import constants

log = logging.getLogger('teststepproperty.py')
class TestStepProperty(): 

    def __init__(self,name,index,apptype,inputval,objectname,identifiers,outputval,stepnum,url,custname,testscript_name,additionalinfo,testcase_num,remark,testcase_details,cord,original_device_height,original_device_width,top,left,width,height):
        self.name=name
        self.index=index
        self.apptype=apptype
        self.inputval=inputval
        self.objectname=objectname
        self.identifiers=identifiers
        self.outputval=outputval
        self.stepnum=stepnum
        self.url=url
        self.custname=custname
        self.testscript_name=testscript_name
        self.additionalinfo = additionalinfo
        self.parent_xpath=''
        self.custom_flag=False
        self.execute_flag=True
        self.keyword_status=constants.TEST_RESULT_FAIL
        self.testcase_num=testcase_num
        self.remarks=remark
        self.testcase_details=testcase_details
        self.cord=cord
        self.original_device_height = original_device_height
        self.original_device_width = original_device_width
        self.browser_type = None
        self.top = top
        self.left = left
        self.width = width
        self.height = height
    def print_step(self):
        log.info(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+self.apptype)









