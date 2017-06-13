#-------------------------------------------------------------------------------
# Name:        dynamic_variable_handler
# Purpose:
#
# Author:      sushma.p
#
# Created:     09-12-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger

from collections import OrderedDict
from constants import *
import re
dynamic_variable_map=OrderedDict()

class DynamicVariables:

	#TO ftech the value form Data base
    def getDBdata(self,inp_value,con_obj):
        res=False
        dyn_value=None
        variable=re.findall("\{(.*?)\[",inp_value)
        if len(variable)>0 and variable[0] != '' and dynamic_variable_map.has_key(DB_VAR):
            dbvalue=dynamic_variable_map[DB_VAR]
            temp_dbvalue=re.findall("\{(.*?)\[",dbvalue[-1])
            #To Fix issue with displaying/Fetching of Databse values
            if len(temp_dbvalue)==0:
                temp_dbvalue.append(dbvalue[-1])
            else:
                temp_dbvalue[0]='{'+temp_dbvalue[0]+'}'
            if dbvalue!=None and temp_dbvalue[0]=='{'+variable[0]+'}':
                  #Dynamic variable is sent to DB keyword 'fetch_data' to get the cell value present in given row and col of DB
                dbvalue[-1]=inp_value
                dyn_value=con_obj.generic_dispatcher_obj.fetch_data(dbvalue)
                res=True
        return res,dyn_value

    #To replace the dynamic vraiable by it's actual value
    def replace_dynamic_variable(self,input_var,keyword,con_obj):
        actual_value=input_var
        if not(keyword in DYNAMIC_KEYWORDS):
            status,nested_var=self.check_dynamic_inside_dynamic(input_var)
            if status==TEST_RESULT_TRUE:
                value=self.get_nestedDyn_value(nested_var,input_var)
                actual_value=value
                if self.check_for_dynamicvariables(value)==TEST_RESULT_TRUE:
                    actual_value=self.get_dynamic_value(value)
                    if actual_value==None:
                        db_result=self.getDBdata(value,con_obj)
                        actual_value=db_result[1]

            elif self.check_for_dynamicvariables(input_var)==TEST_RESULT_TRUE:
                var_list=re.findall("\{(.*?)\}",input_var)
                for data in var_list:
                    data='{'+data+'}'
                    temp_value=self.get_dynamic_value(data)
                    #changes to fix issue:304-Generic : getData keyword:  Actual data  is not getting stored in dynamic variable instead "null" is stored.
                    #changes done by jayashree.r
                    if temp_value is None:
                    	actual_value=temp_value
                    else:
                        if not isinstance(temp_value,unicode):
                     	  actual_value=actual_value.replace(data,str(temp_value))
                        else:
                            actual_value=actual_value.replace(data,temp_value)
        return actual_value

    #To Store the output from keyword as an array if it is multiple values
    def store_as_array(self,variable,value):
        variable=variable[0:len(variable)-1]
        for i in range(len(value)):
            dynamic_variable_map[variable+'['+str(i)+']}']=value[i]


     #To Store the output from keyword as an array if it is single value
    def store_dynamic_value(self,output_var,output_value,keyword):

        if self.check_for_dynamicvariables(output_var)==TEST_RESULT_TRUE:
            if isinstance(output_value,list):
                if not(keyword.lower() in DATABASE_KEYWORDS):
                    self.store_as_array(output_var,output_value)
                else:
                    output_value.append(output_var)
                    dynamic_variable_map[DB_VAR]=output_value
            else:
                dynamic_variable_map[output_var]=output_value

     #To Check if the given pattern of the variable matches '{a}'
    def check_for_dynamicvariables(self,outputval):
        #checks whether the given variable is dynamic or not
        status = TEST_RESULT_FALSE
        if outputval != None and outputval != '':
            if outputval.startswith('{') and outputval.endswith('}'):
                status = TEST_RESULT_TRUE
            elif '{' in outputval and '}' in outputval:
                var_list=re.findall("\{(.*?)\}",outputval)
                if len(var_list)>0:
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
