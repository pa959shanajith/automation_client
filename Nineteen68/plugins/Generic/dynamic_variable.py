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
import dynamic_handler
import Exceptions

class DynamicVariables:

    def __init__(self):
        self.dyn_obj=dynamic_handler.DynamicVariables()


    def create_dynamic_variable(self,variable,value):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if not(variable is None or value is None or variable is '' or value is ''):
                #Check if the given variable to be created is dynamic or not
                res=self.dyn_obj.check_for_dynamicvariables(variable)
                if res==TEST_RESULT_TRUE:
                    #Check if the variable already exists
                    if not(dynamic_handler.dynamic_variable_map.has_key(variable)):
                        #Add the variable to the map with the given value
                        dynamic_handler.dynamic_variable_map[variable]=value
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        logger.log('Variable created is '+str(variable)+'='+str(value))
                    else:
                        logger.log('Variable already exists')
            else:
                logger.log('Invalid input')


        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def modify_value(self,variable,value):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if not(variable is None or value is None or variable is '' or value is ''):
                #Check if the given variable to be modified is dynamic or not
                res=self.dyn_obj.check_for_dynamicvariables(variable)
                if res==TEST_RESULT_TRUE:
                    #Check if the variable already exists
                    if dynamic_handler.dynamic_variable_map.has_key(variable):
                        #Get the old value of the variable
                        oldvalue=self.dyn_obj.get_dynamic_value(variable)
                        #Check if the value to be updated is also dynamic and get its value
                        if self.dyn_obj.check_for_dynamicvariables(value)==TEST_RESULT_PASS:
                            value=self.dyn_obj.get_dynamic_value(value)
                        #Modify the given variable with the new value
                        dynamic_handler.dynamic_variable_map[variable]=value
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                        logger.log('Variable modified: Old value '+str(variable)+'='+str(oldvalue)+'New value '+str(variable)+'='+str(value))
                    else:
                        logger.log('Variable does not exists')
            else:
                logger.log('Invalid input')


        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def copy_value(self,variable,value):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if not(variable is None or value is None or variable is '' or value is ''):
                #Check if the given variable to be modified is dynamic or not
                res=self.dyn_obj.check_for_dynamicvariables(variable)
                if res==TEST_RESULT_TRUE:
                    #Check if the variable already exists
                    if not(dynamic_handler.dynamic_variable_map.has_key(variable)):

                        #Check if the value to be updated is dynamic and get its value
                        if self.dyn_obj.check_for_dynamicvariables(value)==TEST_RESULT_TRUE:
                            value=self.dyn_obj.get_dynamic_value(value)
                            #Add the variable to the map with the given value
                            dynamic_handler.dynamic_variable_map[variable]=value
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                            logger.log('Variable copied is '+str(variable)+'='+str(value))
                        else:
                            logger.log('Invalid Input: 2nd input should be dynamic variable')

                    else:
                        logger.log('Variable already exists')
                else:
                    logger.log('Invalid input')

        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput


    def delete_dyn_value(self,variable):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if not(variable is None or variable is ''):
                #Check if the given variable to be modified is dynamic or not
                res=self.dyn_obj.check_for_dynamicvariables(variable)
                if res==TEST_RESULT_TRUE:
                    #Check if the variable already exists
                    if dynamic_handler.dynamic_variable_map.has_key(variable):
                        value=dynamic_handler.dynamic_variable_map.pop(variable)
                        logger.log('Variable deleted is '+str(variable)+'='+str(value))
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        logger.log('Variable does not exists')
                else:
                    logger.log('Invalid input')

        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput





