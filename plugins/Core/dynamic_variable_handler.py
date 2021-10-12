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
import constant_variable_handler
import re
import core_utils
##dynamic_variable_map=OrderedDict()
import logging
#log = logging.getLogger('dynamic_variable_handler.py')
import ast
import math
import threading
import json
import controller
local_dynamic = threading.local()

class DynamicVariables:
    def __init__(self):
        local_dynamic.dynamic_variable_map=OrderedDict()
        self.const_var_obj=constant_variable_handler.ConstantVariables()
        local_dynamic.log = logging.getLogger('dynamic_variable_handler.py')

	#TO ftech the value form Data base
    def getDBdata(self,inp_value,con_obj):
        res=False
        dyn_value=None
        variable=re.findall(r"\{(.*?)\[",inp_value)
        if len(variable)>0 and variable[0] != '' and DB_VAR in local_dynamic.dynamic_variable_map:
            dbvalue=local_dynamic.dynamic_variable_map[DB_VAR]
            temp_dbvalue=re.findall(r"\{(.*?)\[",dbvalue[-1])
            #To Fix issue with displaying/Fetching of Databse values
            if len(temp_dbvalue)==0:
                temp_dbvalue.append(dbvalue[-1])
            else:
                temp_dbvalue[0]='{'+temp_dbvalue[0]+'}'
            if dbvalue!=None and temp_dbvalue[0]=='{'+variable[0]+'}':
                  #Dynamic variable is sent to DB keyword 'fetch_data' to get the cell value present in given row and col of DB
                dbvalue[-1]=inp_value
                dyn_value=controller.local_cont.generic_dispatcher_obj.fetch_data(dbvalue)
                res=True
        return res,dyn_value

    #To replace the dynamic variable by it's actual value
    def replace_dynamic_variable(self,input_var,keyword,con_obj,no_exch_val=False):
        coreutilsobj=core_utils.CoreUtils()
        input_var=coreutilsobj.get_UTF_8(input_var)
        actual_value=input_var
        if not(keyword.lower() in DYNAMIC_KEYWORDS):
            status,nested_var=self.check_dynamic_inside_dynamic(input_var)
            if status==TEST_RESULT_TRUE:
                value=self.get_nestedDyn_value(nested_var,input_var)
                actual_value=value
                status_var=self.check_for_dynamicvariables(value,keyword)
                if status_var==TEST_RESULT_TRUE:
                    actual_value=self.get_dynamic_value(value)
                    if actual_value==None:
                        db_result=self.getDBdata(value,con_obj)
                        actual_value=db_result[1]
                elif status_var==TEST_RESULT_FALSE and keyword.lower()=='displayvariablevalue':
                    actual_value=None

            elif self.check_for_dynamicvariables(input_var,keyword)==TEST_RESULT_TRUE:
                temp_value=self.get_dynamic_value(input_var)
                if temp_value is None:
                    actual_value=temp_value
                elif actual_value is not None:
                    if hasattr(temp_value, "tag_name") or no_exch_val:
                        actual_value=temp_value
                    else:
                        if not isinstance(temp_value,str): temp_value = str(temp_value)
                        actual_value=actual_value.replace(input_var,temp_value)
        else:
            status,nested_var=self.check_dynamic_inside_dynamic(input_var)
            if status==TEST_RESULT_TRUE:
                actual_value=self.get_nestedDyn_value(nested_var,input_var)
        return actual_value

    #To Store the output from keyword as an array if it is multiple values
    def store_as_array(self,variable,value):
        variable=variable[0:len(variable)-1]
        if len(value)>0 and not(isinstance(value[0],list)):
            for i in range(len(value)):
                local_dynamic.dynamic_variable_map[variable+'['+str(i)+']}']=value[i]
        else:
            for i in range(len(value)):
                for j in range(len(value[i])):
                    local_dynamic.dynamic_variable_map[variable+'['+str(i)+']['+str(j)+']}']=value[i][j]


     #To Store the output from keyword as an array if it is single value
    def store_dynamic_value(self,output_var,output_value,keyword):
        if self.check_for_dynamicvariables(output_var,keyword,True)==TEST_RESULT_TRUE:
            if isinstance(output_value,list):
                if not(keyword.lower() in DATABASE_KEYWORDS):
                    local_dynamic.dynamic_variable_map[output_var]=output_value
                    self.store_as_array(output_var,output_value)
                else:
                    output_value.append(output_var)
                    local_dynamic.dynamic_variable_map[DB_VAR]=output_value
            else:
                local_dynamic.dynamic_variable_map[output_var]=output_value


     #To Check if the given pattern of the variable matches '{a}'
    def check_for_dynamicvariables(self,outputval,keyword=None,store_val=False):
        #checks whether the given variable is dynamic or not
        status = TEST_RESULT_FALSE
        json_flag=False
        if outputval != None and outputval != '':
            if (outputval.startswith('{') and outputval.endswith('}')) or (outputval.startswith('[') and outputval.endswith(']')) :
                try:
                    if type(outputval)==dict:
                        status = TEST_RESULT_FALSE
                        json_flag=True
                    elif keyword is not None and keyword.lower()=='getobject' and store_val:
                        json_flag=True
                        if(outputval.startswith('{{') and outputval.endswith('}}') and outputval[2:].find('{') <0 and outputval[2:-2].find('}')<0):
                            status = TEST_RESULT_TRUE
                        else:
                            err_msg=ERROR_CODE_DICT['INCORRECT_VARIABLE_FORMAT']
                            logger.print_on_console(err_msg)
                            local_dynamic.log.error(err_msg)
                    else:
                        #Changed the code as we are getting malformed string using ast.literal_eval for JSON
                        json.loads(outputval)
                        status = TEST_RESULT_FALSE
                        json_flag=True
                except Exception as e:
                    try:
                        value=ast.literal_eval(str(outputval))
                        if type(value)==set:
                            json_flag=False
                        else:
                            status = TEST_RESULT_FALSE
                            json_flag=True
                    except Exception as e:
                        local_dynamic.log.debug('Not a json input')
            if not(json_flag):
                if '{' in outputval and '}' in outputval:
                    var_list=re.findall(r"\{(.*?)\}",outputval)
                    if len(var_list)>0:
                        status = TEST_RESULT_TRUE
        return status

    #To get the value of given dynamic variable
    def get_dynamic_value(self,variable):
        #returns the value of the dynamic variable if it exists otherwise returns None

        value=None
        if variable in local_dynamic.dynamic_variable_map:
            value=local_dynamic.dynamic_variable_map.get(variable)
        return value

     #To Check if the given pattern of the variable matches '{a[{b}]}'
    def check_dynamic_inside_dynamic(self,inputvar):
        #checks whether the given variable is contains another dynamic inside it
        status = TEST_RESULT_FALSE
        nested_variable=None
        if (inputvar.startswith('{') and inputvar.endswith('}')) or (inputvar.count('{') > 0 and inputvar.count('}') > 0):
            try:
                if type(eval(inputvar))==list:
                    return status,nested_variable
            except Exception as e:
                pass
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
                    if nested_variable[i] in local_dynamic.dynamic_variable_map:
                        replacestring = local_dynamic.dynamic_variable_map.get(nested_variable[i])
                if not isinstance(replacestring,str):
                    replacestring = str(replacestring)
                inputvar = inputvar.replace(nested_variable[i],replacestring)
                value=inputvar

        return value

    #To simplify expression for IF, ELSEIF and EVALUATE keywords
    def simplify_expression(self,input_var,keyword,con_obj):
        k=-1
        if keyword.lower() in [IF,ELSE_IF]:
            k=1
            input_var=input_var[0]
        elif keyword.lower() == EVALUATE:
            k=2
            input_var='('+input_var[0]+')'
        else:
            return [INVALID,None]
        local_dynamic.log.debug('___INPUT: %s',input_var)
        disp_expression=''
        invalid_flag=False
        invalid_msg=''
        input_var=input_var.strip()
        #if input_var=='':
        #    return [input_var,ERROR_CODE_DICT['ERR_INVALID_INPUT']]
        if not(input_var.startswith('(') and input_var.endswith(')')):
            invalid_msg=keyword+': Expression must be enclosed within "(" and ")"\n'
            local_dynamic.log.error(keyword+': Expression must be enclosed within "(" and ")"')
            return [input_var,invalid_msg]
        if k==1:
            input_list=input_var.split(';')
            if len(input_list)<3:
                invalid_msg=keyword+': Expression must have atleast 1 operator and 2 operands for comparision\n'
                local_dynamic.log.error(keyword+': Expression must have atleast 1 operator and 2 operands for comparision')
                return [input_var,invalid_msg]
            for e in input_list:
                if e.replace('(','').strip()=='' or e.replace(')','').strip()=='' or e.replace('(','').replace(')','').strip()=='':
                    invalid_flag=True
                    invalid_msg=keyword+': Expression must have atleast two operands present for comparision\n'
                    local_dynamic.log.error(keyword+': Expression must have atleast two operands present for comparision')
            for i in range(len(input_list)):
                input_list[i]=input_list[i].strip()
            local_dynamic.log.debug('Stage 0: %s',input_list)
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
        local_dynamic.log.debug('Stage 1: %s',exp)
        dv_flag=i=0
        paran_cnt=0
        try:
            while i < len(exp)-1:
                if (exp[i]=='{' and exp[i-1]=='$') or (exp[i]=='{' and exp[i-1]=='('):
                    dv_flag+=1
                elif (exp[i]=='}' and exp[i+1]=='$') or (exp[i]=='}' and exp[i+1]==')'):
                    dv_flag-=1
                if dv_flag!=0:
                    i+=1
                    continue
                if exp[i]=='(':
                    paran_cnt+=1
                    if exp[i+1]!='(' and exp[i+1]!=')' and exp[i+1:i+5]!='not(':
                        exp=exp[0:i+1]+"~$"+exp[i+1:]
                        i+=2
                elif exp[i]==')':
                    paran_cnt-=1
                elif exp[i+1]==')' and exp[i]!='(' and exp[i]!=')':
                    exp=exp[0:i+1]+"$~"+exp[i+1:]
                    i+=2
                if paran_cnt==0:
                    paran_cnt=1000
                    invalid_flag=True
                    invalid_msg=keyword+': Expression must be enclosed within "(" and ")" and balanced\n'
                i+=1
            local_dynamic.log.debug('Stage 2: %s',exp)
            inp_err_list=exp.split('~')
            exp=exp.split('~')
            local_dynamic.log.debug('Stage 3: %s',exp)
            for i in range(len(exp)):
                if exp[i][0]=='$' and exp[i][-1]!='$':
                    inp_err_list[i]=inp_err_list[i][1:]
                    invalid_msg+=keyword+': Special Characters "(", ")" and ";" should be passed through dynamic variables\n'
                    local_dynamic.log.error(keyword+': Special Characters "(", ")" and ";" should be passed through dynamic variables')
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
                        inp_err_list[i]=exp[i]=self.replace_dynamic_variable(exp[i],keyword,con_obj)
                        if exp[i] is None:
                            exp[i]='null'
                    if exp[i][0]=='_' and exp[i][-1]=='_':
                        inp_err_list[i]=exp[i]=self.const_var_obj.get_constant_value(exp[i])
                        if exp[i] is None:
                            exp[i]='null'
                    inf_val = False
                    try:
                        if float(exp[i]) == math.inf:
                            inf_val = True
                            invalid_msg+=keyword+': Value provided in expression is too huge to evaluate\n'
                            invalid_flag=True
                            inp_err_list[i]=' "'+exp[i]+'" '
                            exp[i]="'"+exp[i].replace("\\","\\\\").replace("'","\\'")+"'"
                    except: pass
                    if not inf_val:
                        try:
                            if type(exp[i]) is int or type(exp[i]) is float:
                                exp[i]=str(exp[i])
                            else:
                                _=float(exp[i])
                        except Exception as e:
                            if k==2:
                                invalid_msg+=keyword+': Only numbers are allowed in expression\n'
                                invalid_flag=True
                                inp_err_list[i]=' "'+exp[i]+'" '
                            exp[i]="'"+exp[i].replace("\\","\\\\").replace("'","\\'")+"'"
            local_dynamic.log.debug('Stage 4: %s',exp)
        except Exception as e:
            local_dynamic.log.error(e)
            return [input_var,e]

        # Python3 issue fix. 020 is not a valid number
        for i in range(len(exp)):
            try:
                part = int(exp[i])
                exp[i] = str(part)
            except: pass

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
            local_dynamic.log.error(keyword+': Null values not allowed in expression')
            return [disp_expression,invalid_msg]
        ## Fix of Issue #156 Ends here

        if invalid_flag:
            return [disp_expression,invalid_msg]
        local_dynamic.log.debug('__OUTPUT: %s',exp)
        return [exp,None,disp_expression]
