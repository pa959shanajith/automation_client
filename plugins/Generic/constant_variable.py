#-------------------------------------------------------------------------------
# Name:        constant_variable
# Purpose:     To create constant variable 
#
# Author:      sathwik.p
#
# Created:     05-07-2021
# Copyright:   (c) sathwik.p 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
from constants import *
import constant_variable_handler
from constants import *
import logging
import core_utils

log = logging.getLogger('constant_variable.py')

class ConstantVariables:

    def __init__(self):
        self.const_var_obj=constant_variable_handler.ConstantVariables()


    def create_constant_variable(self,variable, value):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_res=OUTPUT_CONSTANT
        try:
            coreutilsobj=core_utils.CoreUtils()
            log.debug('Reading the inputs in create_constant_variable')
            if not(variable is None or value is None or variable is '' or value is ''):
                variable=coreutilsobj.get_UTF_8(variable)
                value=coreutilsobj.get_UTF_8(value)
                #Check if the given variable to be created is constant or not
                log.debug('Check if the given variable to be created is constant or not')
                res=self.const_var_obj.check_for_constantvariables(variable)
                if res==TEST_RESULT_TRUE:
                    #Check if the variable already exists
                    if not(variable in constant_variable_handler.local_constant.constant_variable_map):
                        #Add the variable to the map with the given value
                        constant_variable_handler.local_constant.constant_variable_map[variable]=value
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        log.info('Variable created is: ')
                        log.info(variable)
                        log.info('Value : ')
                        log.info(value)
                        logger.print_on_console('Variable created is ',str(variable),' = ',str(value))
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_CONSVAR_ALREADY_EXISTS']
                        log.error(err_msg)
                        logger.print_on_console(err_msg)
                else:
                    err_msg=INVALID_INPUT
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

    def delete_const_variable(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_res=OUTPUT_CONSTANT
        values=[]
        try:
            if len(args)!= 0:
                if len(args)>1:
                    values.append(args[0])
                    values.extend(args[1].split(';'))
                else:
                    values.append(args[0])
                log.debug('Reading the inputs')
                errors= {"invalid_input_error":"","constant_variable_error":""}
                for i in range (len(values)):
                    error_message = None
                    variable=values[i]
                    if not(variable is None or variable is ''):
                        coreutilsobj=core_utils.CoreUtils()
                        variable=coreutilsobj.get_UTF_8(variable)
                        #Check if the given variable is constant or not
                        log.debug('Check if the given variable is constant or not')
                        res=self.const_var_obj.check_for_constantvariables(variable)
                        if res==TEST_RESULT_TRUE:
                            #Check if the variable already exists
                            log.debug('Check if the variable already exists')
                            if variable in constant_variable_handler.local_constant.constant_variable_map:
                                value=constant_variable_handler.local_constant.constant_variable_map.pop(variable)
                                log.debug('Variable deleted is ',variable,' = ',value)
                                logger.print_on_console('Variable deleted is ',variable,' = ',value)
                            else:
                                error_message=ERROR_CODE_DICT['ERR_CONVAR']
                                errors["constant_variable_error"]+=str(variable)+", "
                        else:
                            error_message=INVALID_INPUT
                            errors["invalid_input_error"]+=str(variable)+", "
                    else:
                        error_message=INVALID_INPUT
                        errors["invalid_input_error"]+=str(variable)+", "
                    if error_message is not None:
                        log.error(error_message)
                        logger.print_on_console(error_message)
                if errors["constant_variable_error"]!="":
                    err_msg = errors["constant_variable_error"][:-2]+": variables doesnot exists.;"
                if errors["invalid_input_error"]!="":
                    if err_msg is None:
                        err_msg = errors["invalid_input_error"][:-2] + ": Invalid Inputs. Please provide valid inputs.;"
                    else:
                        err_msg = err_msg + errors["invalid_input_error"][:-2] + ": Invalid Inputs. Please provide valid inputs.;"
                if not err_msg:
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
            else:
                err_msg=INVALID_INPUT
                logger.print_on_console(err_msg)
                log.error(err_msg)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=INPUT_ERROR
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
        return status,methodoutput,output_res,err_msg

    