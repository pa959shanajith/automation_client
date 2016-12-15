#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     09-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from pyrobot import Robot
from generic_constants import *
from constants import *
import logger
import Exceptions
import time
class SendFunctionKeys:

    def sendfunction_keys(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            input=str(input)
            if not(input is None or input is ''):
                count=self.get_args(args)
                if count == 'type':
                    self.type(input)
                else:
                    if '+' in input:
                        keys_list=input.split('+')
                        self.press_multiple_keys(keys_list,count)

                    else:
                        self.execute_key(input,count)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
            else:
                logger.log('Invalid input')

        except Exception as e:
            logger.log('Invalid input')
            Exceptions.error(e)
        return status,methodoutput

    def execute_key(self,key,count):
        for x in range(count):
            robot=Robot()
            robot.press_and_release(key)

    def press_multiple_keys(self,keys_list,count):
        for x in range(count):
            for key in keys_list:
                self.press_key(key)
            for key in keys_list:
                self.release_key(key)



    def type(self,input):
        robot=Robot()
        robot.type_string(input,1)


    def press_key(self,key):
        robot=Robot()
        robot.key_press(key)

    def release_key(self,key):
        robot=Robot()
        robot.key_release(key)

    def get_args(self,args):
        if len(args)>0 :
            var=args[0]
            if var is not None or var != '' and var in DYNAMIC_STATIC:
##            if (var.startswith('|') and var.endswith('|')) or (var.startswith('{') and var.endswith('}')):
##            if args[0] in DYNAMIC_STATIC:
                return 'type'
            else:
                return int(args[0])
        else:
            return 1




