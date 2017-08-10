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
import core_utils
dynamic_variable_map=OrderedDict()
import logging
log = logging.getLogger('dynamic_variable_handler.py')

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
        coreutilsobj=core_utils.CoreUtils()
        input_var=coreutilsobj.get_UTF_8(input_var)
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
                temp_value=self.get_dynamic_value(input_var)
                if temp_value is None:
                    actual_value=temp_value
                else:
                    if not isinstance(temp_value,unicode):
                        if actual_value is not None:
                            actual_value=actual_value.replace(input_var,str(temp_value))
                    else:
                        if actual_value is not None:
                            actual_value=actual_value.replace(input_var,temp_value)
                ###Logic to replace dynamic variable values for keywords other than IF and  Evaluate
                ##if keyword not in [EVALUATE,IF,ELSE_IF]:
                ##    data=input_var[1:-1]
                ##    data='{'+data+'}'
                ##    temp_value=self.get_dynamic_value(data)
                ##    if temp_value is None:
                ##        actual_value=temp_value
                ##    else:
                ##        if not isinstance(temp_value,unicode):
                ##            if actual_value is not None:
                ##                actual_value=actual_value.replace(data,str(temp_value))
                ##        else:
                ##            if actual_value is not None:
                ##                actual_value=actual_value.replace(data,temp_value)
                ##
                ##else:
                ##     #Logic to replace dynamic variable values for keywords IF and  Evaluate
                ##     #since input does not contain ';' and input will be expression
                ##    var_list=re.findall("\{(.*?)\}",input_var)
                ##    for data in var_list:
                ##        data='{'+data+'}'
                ##        temp_value=self.get_dynamic_value(data)
                ##        if temp_value is None:
                ##            actual_value=temp_value
                ##        else:
                ##            if not isinstance(temp_value,unicode):
                ##                if actual_value is not None:
                ##                    actual_value=actual_value.replace(data,str(temp_value))
                ##            else:
                ##                if actual_value is not None:
                ##                    actual_value=actual_value.replace(data,temp_value)

        return actual_value

    #To Store the output from keyword as an array if it is multiple values
    def store_as_array(self,variable,value):
        if not(isinstance(value[0],list)):
            variable=variable[0:len(variable)-1]
            for i in range(len(value)):
                dynamic_variable_map[variable+'['+str(i)+']}']=value[i]
        else:
            variable=variable[0:len(variable)-1]
            for i in range(len(value)):
                p=i+1
                for j in range(len(value[i])):
                    q=j+1
                    dynamic_variable_map[variable+'['+str(p)+']['+str(q)+']}']=value[i][j]


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
                if not isinstance(replacestring,basestring):
                    replacestring = str(replacestring)
                inputvar = inputvar.replace(nested_variable[i],replacestring)
                value=inputvar

        return value

    #To simplify expression for IF, ELSEIF and EVALUATE keywords
    def simplify_expression(self,input_var,keyword,con_obj):
        if len(re.findall(IGNORE_THIS_STEP,input_var))!=0:
            return [input_var,IGNORE_THIS_STEP]
        k=-1
        if keyword.lower() in [IF,ELSE_IF]:
            k=1
        elif keyword.lower() == EVALUATE:
            k=2
            input_var='('+input_var+')'
        else:
            return [INVALID,None]
        log.debug('___INPUT: ',input_var)
        disp_expression=''
        invalid_flag=False
        invalid_msg=''
        if not(input_var[0]=='(' and input_var[-1]==')'):
            invalid_msg=keyword+': Expression must be enclosed within "(" and ")"\n'
            log.error(keyword+': Expression must be enclosed within "(" and ")"')
            return [input_var,invalid_msg]
        if k==1:
            input_list=input_var.split(';')
            if len(input_list)<3:
                invalid_msg=keyword+': Expression must have atleast 1 operator and 2 operands for comparision\n'
                log.error(keyword+': Expression must have atleast 1 operator and 2 operands for comparision')
                return [input_var,invalid_msg]
            for e in input_list:
                if e.replace('(','').strip()=='' or e.replace(')','').strip()=='' or e.replace('(','').replace(')','').strip()=='':
                    invalid_flag=True
                    invalid_msg=keyword+': Expression must have atleast two operands present for comparision\n'
                    log.error(keyword+': Expression must have atleast two operands present for comparision')
            for i in range(len(input_list)):
                input_list[i]=input_list[i].strip()
            log.debug('Stage 0: ',input_list)
            exp=';'.join(input_list)
            exp=re.sub(r'[)][\s]*AND[\s]*[(]', ')and(',exp)
            exp=re.sub(r'[)][\s]*OR[\s]*[(]', ')or(',exp)
            exp=re.sub(r'[\s]*NOT[\s]*[(]', 'not(',exp)
            exp=exp.replace(";>=;","$~>=~$").replace(";<=;","$~<=~$").replace(";==;","$~==~$").replace(";!=;","$~!=~$").replace(";>;","$~>~$").replace(";<;","$~<~$")
        elif k==2:
            exp=input_var
            exp=re.sub(r'[\s]*\+[\s]*', '$~+~$',exp)
            exp=re.sub(r'[\s]*\-[\s]*', '$~-~$',exp)
            exp=re.sub(r'[\s]*\*[\s]*', '$~*~$',exp)
            exp=re.sub(r'[\s]*\/[\s]*', '$~/~$',exp)
            exp=re.sub(r'[\s]*\^[\s]*', '$~^~$',exp)
            ##exp=re.sub(r'[(][\s]*[(]', '((',exp)
            ##exp=re.sub(r'[)][\s]*[)]', '))',exp)
            exp=exp.replace('+~$(','+(').replace('-~$(','-(').replace('*~$(','*(').replace('/~$(','/(').replace('^~$(','^(').replace(')$~+',')+').replace(')$~-',')-').replace(')$~*',')*').replace(')$~/',')/').replace(')$~^',')^')
        exp=re.sub(r'[(][\s]*', '(',exp)
        exp=re.sub(r'[\s]*[)]', ')',exp)
        log.debug('Stage 1: ',exp)
        dv_flag=i=0
        try:
            while i < len(exp)-1:
                if (exp[i]=='{' and exp[i-1]=='$') or (exp[i]=='{' and exp[i-1]=='('):
                    dv_flag+=1
                elif (exp[i]=='}' and exp[i+1]=='$') or (exp[i]=='}' and exp[i+1]==')'):
                    dv_flag-=1
                if dv_flag!=0:
                    i+=1
                    continue
                if exp[i]=='(' and exp[i+1]!='(' and exp[i+1]!=')' and exp[i+1:i+5]!='not(':
                    exp=exp[0:i+1]+"~$"+exp[i+1:]
                    i+=2
                elif exp[i+1]==')' and exp[i]!='(' and exp[i]!=')':
                    exp=exp[0:i+1]+"$~"+exp[i+1:]
                    i+=2
                i+=1
            log.debug('Stage 2: ',exp)
            inp_err_list=exp.split('~')
            exp=exp.split('~')
            dv_dict=dict()
            log.debug('Stage 3: ',exp)
            for i in range(len(exp)):
                if exp[i][0]=='$' and exp[i][-1]!='$':
                    inp_err_list[i]=inp_err_list[i][1:]
                    invalid_msg+=keyword+': Special Characters "(", ")" and ";" should be passed through dynamic variables\n'
                    log.error(keyword+': Special Characters "(", ")" and ";" should be passed through dynamic variables')
                    invalid_flag=True
                elif exp[i][0]!='$' and exp[i][-1]=='$':
                    inp_err_list[i]=inp_err_list[i][:-1]
                    invalid_msg+=keyword+': Special Characters "(", ")" and ";" should be passed through dynamic variables\n'
                    invalid_flag=True
                elif exp[i][0]=='$' and exp[i][-1]=='$':
                    inp_err_list[i]=exp[i]=exp[i][1:-1]
                    if len(exp[i])==0:
                        continue
                    if exp[i][0]=='{' and exp[i][-1]=='}':
                        if not dv_dict.has_key(exp[i]):
                            dv_dict[exp[i]]=self.replace_dynamic_variable(exp[i],keyword,con_obj)
                        inp_err_list[i]=exp[i]=dv_dict[exp[i]]
                        if exp[i] is None:
                            exp[i]='null'
                    try:
                        if type(exp[i]) is int or type(exp[i]) is float:
                            exp[i]=str(exp[i])
                        else:
                            tmp=float(exp[i])
                    except Exception as e:
                        if k==2:
                            invalid_msg+=keyword+': Only numbers are allowed in expression\n'
                            invalid_flag=True
                            inp_err_list[i]=' "'+exp[i]+'" '
                        exp[i]="'"+exp[i].replace("\\","\\\\").replace("'","\\'")+"'"
            log.debug('Stage 4: ',exp)
        except Exception as e:
            log.error(e)
            return [input_var,e]

        ## Issue #156 None is getting stored in dynamic variable instead of null if no value is assigned
        none_count=0
        for e in inp_err_list:
            if e is None:
                e='null'
                none_count+=1
            disp_expression=disp_expression+str(e)

        exp=''.join(exp)
        if k==2:
            exp=exp[1:-1]
            disp_expression=disp_expression[1:-1]
        if none_count>0:
            invalid_msg+=keyword+': Null values not allowed in expression'
            log.error(keyword+': Null values not allowed in expression')
            return [disp_expression,invalid_msg]
        ## Fix of Issue #156 Ends here

        if invalid_flag:
            return [disp_expression,invalid_msg]
        log.debug('__OUTPUT: ',exp)
        return [exp,None,disp_expression]


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
