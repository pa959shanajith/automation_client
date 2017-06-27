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
import platform
if platform.system() != 'Darwin':
    from pyrobot import Robot
from generic_constants import *
from constants import *
import logger

import time
from constants import *

import logging


log = logging.getLogger('sendfunction_keys.py')
class SendFunctionKeys:

    def sendfunction_keys(self,input,*args):
        
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_res=OUTPUT_CONSTANT
        try:
            log.debug('reading the inputs')
            input=str(input)
            if not(input is None or input is ''):
                count=self.get_args(args)
                if count == 'type':
                    log.debug('sending the keys in input')
                    self.type(input)
                else:
                    if '+' in input:
                        keys_list=input.split('+')
                        log.debug('sending multiple  keys')
                        self.press_multiple_keys(keys_list,count)

                    else:
                        log.debug('sending the keys in input')
                        self.execute_key(input,count)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            else:
                log.debug('Invalid input')
##                logger.print_on_console('Invalid input')
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg

    def execute_key(self,key,count):
        for x in range(count):
            robot=Robot()
            log.debug('press and release the key', key)
            robot.press_and_release(key)

    def press_multiple_keys(self,keys_list,count):
        for x in range(count):
            for key in keys_list:
                self.press_key(key)
            for key in keys_list:
                self.release_key(key)



    def type(self,input):
        try:
            robot=Robot()
            robot.type_string(str(input),1)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=INPUT_ERROR


    def press_key(self,key):
        robot=Robot()
        log.debug('press  the key', key)
        robot.key_press(key)

    def release_key(self,key):
        robot=Robot()
        log.debug('releasing  the key', key)
        robot.key_release(key)

    def get_args(self,args):
        value=1
        if len(args)>0 :
            var=args[0]
            if var is not None or var != '':
                import re
                if (var.startswith('|') and var.endswith('|')) or (var.startswith('{') and var.endswith('}')):
                    value= 'type'
                elif re.match(('^\d+$'),var):
                    value=int(var)

        return value




