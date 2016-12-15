#-------------------------------------------------------------------------------
# Name:        dynamic_handler
# Purpose:
#
# Author:      sushma.p
#
# Created:     09-12-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger
import Exceptions
from collections import OrderedDict
from constants import *

dynamic_variable_map=OrderedDict()

class DynamicVariables:

    #To replace the dynamic vraiable by it's actual value
    def replace_dynamic_variable(self,input_var,keyword):
        actual_value=input_var
        if not(keyword in DYNAMIC_KEYWORDS):

            status,nested_var=self.check_dynamic_inside_dynamic(input_var)
            if status==TEST_RESULT_TRUE:
                value=self.get_nestedDyn_value(nested_var,input_var)
                actual_value=value
                if self.check_for_dynamicvariables(value)==TEST_RESULT_TRUE:
                    actual_value=self.get_dynamic_value(value)

            elif  self.check_for_dynamicvariables(input_var)==TEST_RESULT_TRUE:
                actual_value=self.get_dynamic_value(input_var)
        return actual_value

    #To Store the output from keyword as an array if it is multiple values
    def store_as_array(self,variable,value):
        variable=variable[0:len(variable)-1]
        for i in range(len(value)):
            dynamic_variable_map[variable+'['+str(i)+']}']=value[i]


     #To Store the output from keyword as an array if it is single value
    def store_dynamic_value(self,output_var,output_value):

        if self.check_for_dynamicvariables(output_var)==TEST_RESULT_TRUE:
            if isinstance(output_value,list):
                self.store_as_array(output_var,output_value)
            else:
                dynamic_variable_map[output_var]=output_value

     #To Check if the given pattern of the variable matches '{a}'
    def check_for_dynamicvariables(self,outputval):
        #checks whether the given variable is dynamic or not
        status = TEST_RESULT_FALSE
        if outputval != None and outputval != '':
            if outputval.startswith('{') and outputval.endswith('}'):
                status = TEST_RESULT_TRUE
        return status

    #To get the value of given dynamic variable
    def get_dynamic_value(self,variable):
        #returns the value of the dynamic variable if it exists otherwise returns None
        value=None
        if dynamic_variable_map.has_key(variable):
            value=dynamic_variable_map.get(variable)
        return value

     #To Check if the given pattern of the variable matches '{a[{b}]}'
    def check_dynamic_inside_dynamic(self,inputvar):
        #checks whether the given variable is contains another dynamic inside it
        status = TEST_RESULT_FALSE
        nested_variable=None
        if (inputvar.startswith('{') and inputvar.endswith('}')) or (inputvar.count('{') > 0 and inputvar.count('}') > 0):
            import re
            pattern = '\\[(.*?)\\]'
            regularexp = re.compile(pattern)
            nested_variable = regularexp.findall(inputvar)
            if len(nested_variable) > 0 :
                status = TEST_RESULT_TRUE
        return status,nested_variable

     #To get the value of the nested dynamic variable Eg ({b} value in '{a[{b}]}')
    def get_nestedDyn_value(self,nested_variable,inputvar):
        #gets the value of nested dynamic variable if it exists
        value = None
        if len(nested_variable) > 0 :
            for i in range(len(nested_variable)):
                #Check if the nested variable is again a dynamic variable or actual value
                replacestring=nested_variable[i]
                if self.check_for_dynamicvariables(nested_variable[i])==TEST_RESULT_TRUE:
                    if dynamic_variable_map.has_key(nested_variable[i]):
                        replacestring = dynamic_variable_map.get(nested_variable[i])

                inputvar = inputvar.replace(nested_variable[i],replacestring)
                value=inputvar

        return value

##
##obj=DynamicVariables()
##dynamic_variable_map['{a}']='0'
##dynamic_variable_map['{b}']='1'
##dynamic_variable_map['{c[0]}']='3333'
##dynamic_variable_map['{c[0][1]}']='10101'
##print '{a} is dynamic variable :',obj.check_for_dynamicvariables('{a}')
##print '{a}= ',obj.get_dynamic_value('{a}')
##status,nested_var1=  obj.check_dynamic_inside_dynamic('{c[{a}]}')
##status,nested_var= obj.check_dynamic_inside_dynamic('{c}')
##value= obj.get_nestedDyn_value(nested_var1,'{c[{a}]}')
##print '{c[{a}]} ',obj.get_dynamic_value(value)
##status,nested_var1=  obj.check_dynamic_inside_dynamic('{c[{a}][{b}]}')
##print '{c[{a}][{b}]} FIRST ',status,nested_var1
##nested_var= obj.get_nestedDyn_value(nested_var1,'{c[{a}][{b}]}')
##print 'nested_var----- ',nested_var
##print '{c[{a}][{b}]} SECOND ',obj.get_dynamic_value(nested_var)
##print '-------------------'
##print dynamic_variable_map
##print '------------------'
