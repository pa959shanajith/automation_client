#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:
# Copyright:   (c) sushma.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import logging
##import testcase_compile
dynamic_variable_map = {}

from testmobile_constants import *
log = logging.getLogger('generic_operations.py')

class GenericOperations:
    """Basis for all tests."""


    def wait(self,timeout,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            log.info(timeout)
            time.sleep(int(timeout))
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE

        except Exception as e:
            log.error(e)
        return status,methodoutput,output,err_msg


    def check_and_replace_dynamicvariables(self,inputval,keyword=None):
        #checks whether the given variable is dynamic or not
        value=inputval[0].split(';')
        for i in range(len(value)):
            if value[i].startswith('{') and value[i].endswith('}'):
                if value[i] in dynamic_variable_map:
                    value[i]=dynamic_variable_map[value[i]]
        return value



    # def replace_dynamic_variable(self,input_var,keyword):
    #     coreutilsobj=core_utils.CoreUtils()
    #     input_var=coreutilsobj.get_UTF_8(input_var)
    #     actual_value=input_var
    #     if not(keyword.lower() in DYNAMIC_KEYWORDS):
    #         status,nested_var=self.check_dynamic_inside_dynamic(input_var)
    #         if status==TEST_RESULT_TRUE:
    #             value=self.get_nestedDyn_value(nested_var,input_var)
    #             actual_value=value
    #             if self.check_for_dynamicvariables(value,keyword)==TEST_RESULT_TRUE:
    #                 actual_value=self.get_dynamic_value(value)


    #         elif self.check_for_dynamicvariables(input_var,keyword)==TEST_RESULT_TRUE:
    #             temp_value=self.get_dynamic_value(input_var)
    #             if temp_value is None:
    #                 actual_value=temp_value
    #             else:
    #                 try:
    #                     dyn_data=temp_value.tag_name
    #                 except:
    #                     dyn_data=''
    #                 if not ((isinstance(temp_value,str))or (dyn_data !='')):
    #                     if actual_value is not None:
    #                         actual_value=actual_value.replace(input_var,str(temp_value))
    #                 else:
    #                     if actual_value is not None:
    #                         if dyn_data !='':
    #                             actual_value=temp_value
    #                         else:
    #                             actual_value=actual_value.replace(input_var,temp_value)
    #     else:
    #         status,nested_var=self.check_dynamic_inside_dynamic(input_var)
    #         if status==TEST_RESULT_TRUE:
    #             actual_value=self.get_nestedDyn_value(nested_var,input_var)
    #     return actual_value


    def get_UTF_8(self,value):
        try:
            if isinstance(value,str) or isinstance(value, list):
                if isinstance(value, list):
                    for eachvalue in value:
                        if not isinstance(eachvalue,str):
                            if not all(ord(c) < 128 for c in eachvalue):
                                value.append(eachvalue.decode('utf-8'))
                else:
                    if not isinstance(value,str):
                        if not all(ord(c) < 128 for c in value):
                            value = value.decode('utf-8')
            return value
        except Exception as e:
            log.info(e)


    def store_dynamic_value(self,output_var,output_value,keyword):
        if output_var.startswith('{') and output_var.endswith('}'):
                dynamic_variable_map[output_var]=output_value


    def create_dynamic_variable(self,variable,value):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_res=OUTPUT_CONSTANT
        try:

            if not(variable is None or value is None or variable is '' or value is ''):
                variable=coreutilsobj.get_UTF_8(variable)
                value=coreutilsobj.get_UTF_8(value)
                #Check if the given variable to be created is dynamic or not
                log.debug('Check if the given variable to be created is dynamic or not')
                res=self.dyn_obj.check_for_dynamicvariables(variable)
                if res==TEST_RESULT_TRUE:
                    #Check if the variable already exists
                    if not(variable in dynamic_variable_map):
                        #Add the variable to the map with the given value
                        dynamic_variable_map[variable]=value
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
##                        log.info('Variable created is '+str(variable)+'='+str(value))
                        log.info('Variable created is: ')
                        log.info(variable)
                        log.info('Value : ')
                        log.info(value)

##                        logger.print_on_console('Variable created is '+str(variable)+'='+str(value))
                    else:
                        err_msg='ERR_DYNVAR_ALREADY_EXISTS'
                        log.error(err_msg)

            else:
                err_msg="INVALID_INPUT"
                log.error(err_msg)


        except Exception as e:
            log.error(e)
            err_msg="INPUT_ERROR"
        return status,methodoutput,output_res,err_msg


