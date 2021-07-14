#-------------------------------------------------------------------------------
# Name:        constant_variable_handler
# Purpose:
#
# Author:      sathwik.p
#
# Created:     05-07-2021
# Copyright:   (c) sathwik.p 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from collections import OrderedDict
from constants import *
import re
import logging
import threading
local_constant = threading.local()

class ConstantVariables:
    def __init__(self):
        local_constant.constant_variable_map=OrderedDict()
        local_constant.log = logging.getLogger('constant_variable_handler.py')

    #To Check if the given pattern of the variable matches '_a_'
    def check_for_constantvariables(self,outputval):
        #checks whether the given variable is constant or not
        status = TEST_RESULT_FALSE
        if outputval != None and outputval != '':
            if '_' in outputval[0] and '_' in outputval[-1]:
                var_list=re.findall(r"_(.*)_",outputval)
                if len(var_list)>0:
                    status = TEST_RESULT_TRUE
        return status

    #To get the value of given constant variable
    def get_constant_value(self,variable):
        #returns the value of the constant variable if it exists otherwise returns None
        value=None
        if variable in local_constant.constant_variable_map:
            value=local_constant.constant_variable_map.get(variable)
        return value

    #To Store the output from keyword as an array if it is multiple values
    def store_as_array(self,variable,value):
        variable=variable[0:len(variable)-1]
        if len(value)>0 and not(isinstance(value[0],list)):
            for i in range(len(value)):
                local_constant.constant_variable_map[variable+'['+str(i)+']_']=value[i]
        else:
            for i in range(len(value)):
                for j in range(len(value[i])):
                    local_constant.constant_variable_map[variable+'['+str(i)+']['+str(j)+']_']=value[i][j]

    #To Store the output from keyword
    def store_constant_value(self,output_var,output_value,keyword):
        if self.check_for_constantvariables(output_var)==TEST_RESULT_TRUE:
            if isinstance(output_value,list):
                if not(keyword.lower() in DATABASE_KEYWORDS):
                    local_constant.constant_variable_map[output_var]=output_value
                    self.store_as_array(output_var,output_value)
                else:
                    output_value.append(output_var)
                    local_constant.constant_variable_map[DB_VAR]=output_value
            else:
                local_constant.constant_variable_map[output_var]=output_value