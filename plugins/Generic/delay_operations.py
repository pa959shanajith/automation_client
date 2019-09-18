#-------------------------------------------------------------------------------
# Name:        delay_operations.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     10-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
import pause_display_operation
import logging
from constants import *
import core_utils
import dynamic_variable_handler
import time
import readconfig
log = logging.getLogger('delay_operations.py')

class Delay_keywords:

    def wait(self,input):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if not(input is None or input is ''):
                input=int(input)
                log.info('Wait for :' + str(input) + 'seconds')
                logger.print_on_console('Wait for :' , str(input) , 'seconds')
                time.sleep(input)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            else:
                log.error(INVALID_INPUT)
                err_msg=INVALID_INPUT
                logger.print_on_console(INVALID_INPUT)
        except ValueError:
            err_msg = INVALID_INPUT+". Only numbers are allowed"
            log.error(err_msg)
            logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error occurred for during wait"
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def pause(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            o = pause_display_operation.PauseAndDisplay()
            o.execute(args[-2],args[-1])
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            err_msg = "Error occurred for during pause"
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def display_variable_value(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        display_input=''
        configvalues = readconfig.readConfig().readJson()
        if(configvalues['displayVariableTimeOut']=='0'):
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
            logger.debug("Ignoring this step as DisplayVariableTimeout is 0")
            return status,methodoutput,output,err_msg,display_input
        else:
            try:
                if not (args is None or args is ''):
                    input_list=list(args)
                    index=input_list.index(';')
                    values=input_list[0:index]
                    variables=input_list[index+1:len(input_list)]
                    flag_invalid_syntax=False

                    #st_check = getparam.GetParam()
                    for x, y in zip(variables, values):
                        coreutilsobj=core_utils.CoreUtils()
                        y=coreutilsobj.get_UTF_8(y)
                        x=coreutilsobj.get_UTF_8(x)
    ##                  if type(x)==unicode or type(x)==str:
    ##                        x=str(x)
    ##                        changes to fix issue:304-Generic : getData keyword:  Actual data  is not getting stored in dynamic variable instead "null" is stored.
    ##                  changes done by jayashree.r
    ##                  if y == 'None' or y == None:
                        if y == None:
                            y = 'null'
                        if not((x.startswith('{') and x.endswith('}')) or (x.startswith('|') and x.endswith('|'))):
                            flag_invalid_syntax=True

                        elif x.startswith('|') and x.endswith('|') and x.count('|')!=2:
                            y=""
                            logger.print_on_console("Static variable doesn't exist")

                        if not isinstance(y,str):
                            if str(type(y))=="<class 'selenium.webdriver.remote.webelement.WebElement'>":
                                y = "WebElement"
                            y=str(y)
    ##                    display_input+=x+' = '+(y if type(y)==str else repr(y))+'\n'

                        display_input+=x+' = '+y+'\n'
                    if not (flag_invalid_syntax):
                        o = pause_display_operation.PauseAndDisplay()
                        o.display_value(display_input,args[-2],args[-1])
                        logger.print_on_console('Result is ',display_input)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
                else:
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg,display_input
