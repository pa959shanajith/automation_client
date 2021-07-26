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
import constant_variable_handler
from constants import *
import logging
import core_utils


log = logging.getLogger('dynamic_variable.py')

class DynamicVariables:

    def __init__(self):
        self.dyn_obj=dynamic_variable_handler.DynamicVariables()
        self.const_var_obj=constant_variable_handler.ConstantVariables()
        dynamic_variable_handler.local_dynamic.dynamic_variable_map['{newline}']='\n'
        dynamic_variable_handler.local_dynamic.dynamic_variable_map['{tab}']='\t'


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
                    if not(variable in dynamic_variable_handler.local_dynamic.dynamic_variable_map):
                        #Add the variable to the map with the given value
                        dynamic_variable_handler.local_dynamic.dynamic_variable_map[variable]=value
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        log.info('Variable created is: ')
                        log.info(variable)
                        log.info('Value : ')
                        log.info(value)
                        logger.print_on_console('Variable created is ',str(variable),' = ',str(value))
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
                # value=coreutilsobj.get_UTF_8(value)
                #Check if the given variable to be modified is dynamic or not
                log.debug('Check if the given variable to be modified is dynamic or not')
                res=self.dyn_obj.check_for_dynamicvariables(variable)
                if res==TEST_RESULT_TRUE:
                    #Check if the variable already exists
                    log.debug('Check if the variable already exists')
                    if variable in dynamic_variable_handler.local_dynamic.dynamic_variable_map:
                        #Get the old value of the variable
                        log.debug('Get the old value of the variable')
                        oldvalue=self.dyn_obj.get_dynamic_value(variable)
                        # #Check if the value to be updated is also dynamic and get its value
                        # log.debug('Check if the value to be updated is also dynamic and get its value')
                        # if self.dyn_obj.check_for_dynamicvariables(value)==TEST_RESULT_PASS:
                        #     value=self.dyn_obj.get_dynamic_value(value)
                        #Modify the given variable with the new value
                        log.debug('Modify the given variable with the new value')
                        dynamic_variable_handler.local_dynamic.dynamic_variable_map[variable]=value
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        log.debug('Variable modified: Old value ',str(variable),' = ',str(oldvalue),' New value ',str(variable),' = ',str(value))
                        logger.print_on_console('Variable modified: Old value ',str(variable),' = ',str(oldvalue),' New value ',str(variable),' = ',str(value))
                    else:
                        err_msg=ERROR_CODE_DICT['ERR_DYNVAR']
                elif self.const_var_obj.check_for_constantvariables(variable)==TEST_RESULT_TRUE:
                    #checks if the variable is constant varaible ex: _a_;{b}
                    err_msg="Invalid input! Constant variable cannot be modified"
                else:
                   err_msg=INVALID_INPUT
            else:
               err_msg=INVALID_INPUT
            if err_msg is not None:
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
                    self.dyn_obj.store_dynamic_value(variable,value,"copyvalue")
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                    log.debug('Variable copied is ' + str(variable) + ' = ' + str(value))
                    logger.print_on_console('Variable copied is ',str(variable),' = ',str(value))
                elif self.const_var_obj.check_for_constantvariables(variable)==TEST_RESULT_TRUE:
                    #checks if the variable is constant variable ex: _a_
                    if variable not in constant_variable_handler.local_constant.constant_variable_map:
                        #checks if the constant variable exists or not
                        self.const_var_obj.store_constant_value(variable,value,"copyvalue")
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        log.debug('Variable copied is ' + str(variable) + ' = ' + str(value))
                        logger.print_on_console('Variable copied is ',str(variable),' = ',str(value))
                    else:
                        err_msg="Invalid input! Constant variable cannot be modified"
                else:
                   err_msg=INVALID_INPUT
            else:
               err_msg=INVALID_INPUT
            if err_msg is not None:
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured while copying value")
            err_msg=INPUT_ERROR
        return status,methodoutput,output_res,err_msg


    def delete_dyn_value(self,*args):
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
                errors= {"invalid_input_error":"","dynamic_variable_error":""}
                for i in range (len(values)):
                    error_message = None
                    variable=values[i]
                    if not(variable is None or variable is ''):
                        coreutilsobj=core_utils.CoreUtils()
                        variable=coreutilsobj.get_UTF_8(variable)
                        #Check if the given variable to be modified is dynamic or not
                        log.debug('Check if the given variable to be modified is dynamic or not')
                        res=self.dyn_obj.check_for_dynamicvariables(variable)
                        if res==TEST_RESULT_TRUE:
                            #Check if the variable already exists
                            log.debug('Check if the variable already exists')
                            if variable in dynamic_variable_handler.local_dynamic.dynamic_variable_map:
                                value=dynamic_variable_handler.local_dynamic.dynamic_variable_map.pop(variable)
                                log.debug('Variable deleted is ',variable,' = ',value)
                                logger.print_on_console('Variable deleted is ',variable,' = ',value)
                            else:
                                error_message=ERROR_CODE_DICT['ERR_DYNVAR']
                                errors["dynamic_variable_error"]+=str(variable)+", "
                        else:
                            error_message=INVALID_INPUT
                            errors["invalid_input_error"]+=str(variable)+", "
                    else:
                        error_message=INVALID_INPUT
                        errors["invalid_input_error"]+=str(variable)+", "
                    if error_message is not None:
                        log.error(error_message)
                        logger.print_on_console(error_message)
                if errors["dynamic_variable_error"]!="":
                    err_msg = errors["dynamic_variable_error"][:-2]+": variables doesnot exists.;"
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