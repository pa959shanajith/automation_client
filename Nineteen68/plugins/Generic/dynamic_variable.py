#-------------------------------------------------------------------------------
# Name:        dynamic_variable
# Purpose:     To display variable and pause window
#
# Author:      sushma.p
#
# Created:     08-12-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
from constants import *
import dynamic_variable_handler

from constants import *
import logging
import core_utils


log = logging.getLogger('dynamic_variable.py')

class DynamicVariables:

    def __init__(self):
        self.dyn_obj=dynamic_variable_handler.DynamicVariables()


    def create_dynamic_variable(self,variable,value):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_res=OUTPUT_CONSTANT
        try:
            coreutilsobj=core_utils.CoreUtils()
            log.debug('Reading the inputs in create_dynamic_variable')
            if not(variable is None or value is None or variable is '' or value is ''):
                variable=coreutilsobj.get_UTF_8(variable)
                value=coreutilsobj.get_UTF_8(value)
                #Check if the given variable to be created is dynamic or not
                log.debug('Check if the given variable to be created is dynamic or not')
                res=self.dyn_obj.check_for_dynamicvariables(variable)
                if res==TEST_RESULT_TRUE:
                    #Check if the variable already exists
                    if not(dynamic_variable_handler.dynamic_variable_map.has_key(variable)):
                        #Add the variable to the map with the given value
                        dynamic_variable_handler.dynamic_variable_map[variable]=value
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
##                        log.info('Variable created is '+str(variable)+'='+str(value))
                        log.info('Variable created is: ')
                        log.info(variable)
                        log.info('Value : ')
                        log.info(value)
                        logger.print_on_console('Variable created is ',variable,' = ',value)
##                        logger.print_on_console('Variable created is '+str(variable)+'='+str(value))
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_DYNVAR_ALREADY_EXISTS']
                        log.error(err_msg)
                        logger.print_on_console(err_msg)
            else:
                err_msg=INVALID_INPUT
                log.error(err_msg)
                logger.print_on_console(err_msg)

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=INPUT_ERROR
        return status,methodoutput,output_res,err_msg

    def modify_value(self,variable,value):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_res=OUTPUT_CONSTANT
        try:
            log.debug('Reading the inputs in modify_value')
            coreutilsobj=core_utils.CoreUtils()
            if not(variable is None or value is None or variable is '' or value is ''):
                variable=coreutilsobj.get_UTF_8(variable)
                value=coreutilsobj.get_UTF_8(value)
                #Check if the given variable to be modified is dynamic or not
                log.debug('Check if the given variable to be modified is dynamic or not')
                res=self.dyn_obj.check_for_dynamicvariables(variable)
                if res==TEST_RESULT_TRUE:
                    #Check if the variable already exists
                    log.debug('Check if the variable already exists')
                    if dynamic_variable_handler.dynamic_variable_map.has_key(variable):
                        #Get the old value of the variable
                        log.debug('Get the old value of the variable')
                        oldvalue=self.dyn_obj.get_dynamic_value(variable)
                        #Check if the value to be updated is also dynamic and get its value
                        log.debug('Check if the value to be updated is also dynamic and get its value')
                        if self.dyn_obj.check_for_dynamicvariables(value)==TEST_RESULT_PASS:
                            value=self.dyn_obj.get_dynamic_value(value)
                        #Modify the given variable with the new value
                        log.debug('Modify the given variable with the new value')
                        dynamic_variable_handler.dynamic_variable_map[variable]=value
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        log.debug('Variable modified: Old value ',variable,' = ',oldvalue,' New value ',variable,' = ',value)
                        logger.print_on_console('Variable modified: Old value ',variable,' = ',oldvalue,' New value ',variable,' = ',value)
##                        log.debug('Variable modified: Old value '+str(variable)+'='+str(oldvalue)+'New value '+str(variable)+'='+str(value))
##                        logger.print_on_console('Variable modified: Old value '+str(variable)+'='+str(oldvalue)+'New value '+str(variable)+'='+str(value))
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_DYNVAR']
                        log.error(err_msg)
                        logger.print_on_console(err_msg)
            else:
               err_msg=INVALID_INPUT
               log.error(err_msg)
               logger.print_on_console(err_msg)

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=INPUT_ERROR
        return status,methodoutput,output_res,err_msg

    def copy_value(self,variable,value):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_res=OUTPUT_CONSTANT
        try:
            log.debug('Reading the inputs in copy_value')
            if not(variable is None or value is None or variable is '' or value is ''):
                coreutilsobj=core_utils.CoreUtils()
                variable=coreutilsobj.get_UTF_8(variable)
                #Check if the given variable to be modified is dynamic or not
                log.debug('Check if the given variable to be modified is dynamic or not')
                res=self.dyn_obj.check_for_dynamicvariables(variable)
                if res==TEST_RESULT_TRUE:
                    #Fixing issue #123(ALM) check for the variable if it already exists is removed
##                    #Check if the variable already exists
##                    log.debug('Check if the variable already exists')
##                    if not(dynamic_variable_handler.dynamic_variable_map.has_key(variable)):

                    #Check if the value to be updated is dynamic and get its value
                    log.debug('Check if the value to be updated is dynamic and get its value')
                    value=coreutilsobj.get_UTF_8(value)
                    if self.dyn_obj.check_for_dynamicvariables(value)==TEST_RESULT_TRUE:
                        value=self.dyn_obj.get_dynamic_value(value)
                        #Add the variable to the map with the given value
                        dynamic_variable_handler.dynamic_variable_map[variable]=value
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        log.debug('Variable copied is ',variable,' = ',value)
                        logger.print_on_console('Variable copied is ',variable,' = ',value)
##                        log.debug('Variable copied is '+str(variable)+'='+str(value))
##                        logger.print_on_console('Variable copied is '+str(variable)+'='+str(value))
                    else:
                        log.debug('Invalid Input: 2nd input should be dynamic variable')
                        logger.print_on_console('Invalid Input: 2nd input should be dynamic variable')

##                    else:
##                        err_msg=ERROR_CODE_DICT['ERR_DYNVAR']
##                        log.error(err_msg)
##                        logger.print_on_console(err_msg)
                else:
                    err_msg=INVALID_INPUT
                    log.error(err_msg)
                    logger.print_on_console(err_msg)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=INPUT_ERROR
        return status,methodoutput,output_res,err_msg


    def delete_dyn_value(self,variable):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_res=OUTPUT_CONSTANT
        try:
            log.debug('reding the inputs')
            if not(variable is None or variable is ''):
                coreutilsobj=core_utils.CoreUtils()
                variable=coreutilsobj.get_UTF_8(variable)
                #Check if the given variable to be modified is dynamic or not
                log.debug('Check if the given variable to be modified is dynamic or not')
                res=self.dyn_obj.check_for_dynamicvariables(variable)
                if res==TEST_RESULT_TRUE:
                    #Check if the variable already exists
                    log.debug('Check if the variable already exists')
                    if dynamic_variable_handler.dynamic_variable_map.has_key(variable):
                        value=dynamic_variable_handler.dynamic_variable_map.pop(variable)
##                        log.debug('Variable deleted is '+str(variable)+'='+str(value))
##                        logger.print_on_console('Variable deleted is '+str(variable)+'='+str(value))
                        log.debug('Variable deleted is ',variable,' = ',value)
                        logger.print_on_console('Variable deleted is ',variable,' = ',value)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_DYNVAR']
                        log.error(err_msg)
                        logger.print_on_console(err_msg)
                else:
                    err_msg=INVALID_INPUT
                    log.error(err_msg)
                    logger.print_on_console(err_msg)

        except Exception as e:
             log.error(e)
             logger.print_on_console(e)
             err_msg=INPUT_ERROR
        return status,methodoutput,output_res,err_msg





