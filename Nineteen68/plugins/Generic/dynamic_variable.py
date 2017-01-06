#-------------------------------------------------------------------------------
# Name:        dynamic_variable
# Purpose:
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
import Exceptions
from constants import *
from loggermessages import *
import logging


log = logging.getLogger('dynamic_variable.py')

class DynamicVariables:

    def __init__(self):
        self.dyn_obj=dynamic_variable_handler.DynamicVariables()


    def create_dynamic_variable(self,variable,value):
        log.info(KEYWORD_EXECUTION_STARTED)
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        error_msg=None
        output_res=MD5_TEMP_RES
        try:
            log.debug('reding the inputs')
            if not(variable is None or value is None or variable is '' or value is ''):
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
                        log.debug('Variable created is '+str(variable)+'='+str(value))
                        logger.print_on_console('Variable created is '+str(variable)+'='+str(value))
                    else:
                        log.error('Variable already exists')
                        logger.print_on_console('Variable already exists')
            else:
                log.error('Invalid input')
                logger.print_on_console('Invalid input')


        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output_res,error_msg

    def modify_value(self,variable,value):
        log.info(KEYWORD_EXECUTION_STARTED)
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        error_msg=None
        output_res=MD5_TEMP_RES
        try:
            log.debug('reding the inputs')
            if not(variable is None or value is None or variable is '' or value is ''):
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
                        log.debug('Variable modified: Old value '+str(variable)+'='+str(oldvalue)+'New value '+str(variable)+'='+str(value))
                        logger.print_on_console('Variable modified: Old value '+str(variable)+'='+str(oldvalue)+'New value '+str(variable)+'='+str(value))
                    else:
                        log.error('Variable does not exists')
                        logger.print_on_console('Variable does not exists')
            else:
                log.error('Invalid input')
                logger.print_on_console('Invalid input')


        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output_res,error_msg

    def copy_value(self,variable,value):
        log.info(KEYWORD_EXECUTION_STARTED)
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        error_msg=None
        output_res=MD5_TEMP_RES
        try:
            log.debug('reding the inputs')
            if not(variable is None or value is None or variable is '' or value is ''):
                #Check if the given variable to be modified is dynamic or not
                log.debug('Check if the given variable to be modified is dynamic or not')
                res=self.dyn_obj.check_for_dynamicvariables(variable)
                if res==TEST_RESULT_TRUE:
                    #Check if the variable already exists
                    log.debug('Check if the variable already exists')
                    if not(dynamic_variable_handler.dynamic_variable_map.has_key(variable)):

                        #Check if the value to be updated is dynamic and get its value
                        log.debug('Check if the value to be updated is dynamic and get its value')
                        if self.dyn_obj.check_for_dynamicvariables(value)==TEST_RESULT_TRUE:
                            value=self.dyn_obj.get_dynamic_value(value)
                            #Add the variable to the map with the given value
                            dynamic_variable_handler.dynamic_variable_map[variable]=value
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                            log.debug('Variable copied is '+str(variable)+'='+str(value))
                            logger.print_on_console('Variable copied is '+str(variable)+'='+str(value))
                        else:
                            log.debug('Invalid Input: 2nd input should be dynamic variable')
                            logger.print_on_console('Invalid Input: 2nd input should be dynamic variable')

                    else:
                        log.error('Variable already exists')
                        logger.print_on_console('Variable already exists')
                else:
                    log.error('Invalid input')
                    logger.print_on_console('Invalid input')

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output_res,error_msg


    def delete_dyn_value(self,variable):
        log.info(KEYWORD_EXECUTION_STARTED)
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        error_msg=None
        output_res=MD5_TEMP_RES
        try:
            log.debug('reding the inputs')
            if not(variable is None or variable is ''):
                #Check if the given variable to be modified is dynamic or not
                log.debug('Check if the given variable to be modified is dynamic or not')
                res=self.dyn_obj.check_for_dynamicvariables(variable)
                if res==TEST_RESULT_TRUE:
                    #Check if the variable already exists
                    log.debug('Check if the variable already exists')
                    if dynamic_variable_handler.dynamic_variable_map.has_key(variable):
                        value=dynamic_variable_handler.dynamic_variable_map.pop(variable)
                        log.debug('Variable deleted is '+str(variable)+'='+str(value))
                        logger.print_on_console('Variable deleted is '+str(variable)+'='+str(value))
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        log.error('Variable does not exists')
                        logger.print_on_console('Variable does not exists')
                else:
                    log.error('Invalid input')
                    logger.print_on_console('Invalid input')
                    error_msg='Invalid input'

        except Exception as e:
             log.error(e)
             logger.print_on_console(e)
             error_msg=e
        return status,methodoutput,output_res,error_msg





