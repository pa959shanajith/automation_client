#-------------------------------------------------------------------------------
# Name:        handler
# Purpose:
#
# Author:      sushma.p
#
# Created:     18-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import json
from teststepproperty import TestStepProperty
from for_step import For
from if_step import If
from getparam_step import GetParam
from collections import OrderedDict
import constants
import logger

tspList=[]

copy_for_keywords=OrderedDict()
for_keywords=OrderedDict()

copy_condition_keywords=OrderedDict()
condition_keywords=OrderedDict()

copy_getparam_keywords=OrderedDict()
getparam_keywords=OrderedDict()

for_array=[constants.FOR,constants.ENDFOR]

if_endIf=[constants.IF,constants.ENDIF]
if_array=[constants.IF,constants.ELSE_IF,constants.ELSE,constants.ENDIF]

get_param=[constants.GETPARAM,constants.STARTLOOP,constants.ENDLOOP]

for_info={}
if_info={}
get_param_info={}

start_end_dict={constants.ENDFOR:[constants.FOR],
                constants.ENDIF:[constants.IF,constants.ELSE_IF,constants.ELSE],
                constants.ELSE_IF:[constants.IF,constants.ELSE_IF],
                constants.ELSE:[constants.IF,constants.ELSE_IF],
                constants.GETPARAM:[constants.STARTLOOP],
                constants.STARTLOOP:[constants.ENDLOOP]}


class Handler():

    def parse_json(self,test_data):
        logger.log('parse')
        json_string = json.dumps(test_data)
        new_obj = json.loads(json_string)
        if len(new_obj)==1:
            json_data=new_obj[0]
        testcase=json_data['testcase']
        comments=testcase[len(testcase)-1]['comments']
        testscript_name=json_data['testscript_name']
        self.create_list(testcase,testscript_name)

    def validate(self,start,end):
        return end in start_end_dict[start]

    def insert_into_fordict(self,keyword_index,keyword,start_index):
        if start_index is not None:
            for_info[start_index]=[{keyword_index:keyword}]
            for_info[(keyword_index,keyword)]=[{start_index[0]:start_index[1]}]
            for_keywords.popitem()
        else:
            for_info[(keyword_index,keyword)]=None

    def insert_into_getParamdict(self,keyword_index,keyword,start_index):
        if start_index is not None:
            if not(start_index[1] == constants.ENDLOOP and keyword==constants.ENDLOOP):
                if get_param_info.has_key(start_index) and get_param_info[start_index] is not None and (start_index != {keyword_index:keyword}):
                    get_param_info[start_index].append({keyword_index:keyword})
                else:
                    get_param_info[start_index]=[{keyword_index:keyword}]
        else:
            if_info[(keyword_index,keyword)]=None

    def insert_into_ifdict(self,keyword_index,keyword,start_index):
        if start_index is not None:
            if not(start_index[1] == constants.ENDIF and keyword==constants.ENDIF):
                if if_info.has_key(start_index) and if_info[start_index] is not None and (start_index != {keyword_index:keyword}):
                    if_info[start_index].append({keyword_index:keyword})
                else:
                    if_info[start_index]=[{keyword_index:keyword}]
        else:
            if_info[(keyword_index,keyword)]=None


    def for_index(self,keyword,keyword_index):
        flag=True
        if len(for_keywords) != 0:
            start_index=for_keywords.items()[-1]
            if start_end_dict.has_key(keyword):
                self.insert_into_fordict(keyword_index,keyword,start_index)
        else:
            self.insert_into_fordict(keyword_index,keyword,None)
        return flag

    def if_index(self,keyword,keyword_index):
        flag=True
        if len(condition_keywords)>0:
            start_index=condition_keywords.items()[-1]
            if not (keyword in if_endIf) and self.validate(keyword,start_index[1]):
                self.insert_into_ifdict(keyword_index,keyword,start_index)
            elif keyword==constants.ENDIF:
                #insert 'endIf' key to dict
                self.insert_into_ifdict(keyword_index,keyword,None)
                #mapping 'if' and 'endIf'
                if start_index[1]==constants.IF:
                    self.insert_into_ifdict(keyword_index,keyword,start_index)
                    self.insert_into_ifdict(start_index[0],start_index[1],(keyword_index,keyword))
                #mapping 'endIf' to it's respective steps while backtracking
                while(start_index[1]!=constants.IF):
                    if (len(condition_keywords)>0):
                        start_index=condition_keywords.items()[-1]
                        self.insert_into_ifdict(keyword_index,keyword,start_index)
                        self.insert_into_ifdict(start_index[0],start_index[1],(keyword_index,keyword))
                        condition_keywords.popitem()
                    else:
                        logger.log('IF is missing: Invalid script ')
                        flag=False
                        break
            else:
                logger.log('Invalid syntax')
                flag=False
        else:
            self.insert_into_ifdict(keyword_index,keyword,None)
        return flag

    def getparam_index(self,keyword,keyword_index):
        flag=True
        if len(getparam_keywords)>0:
            start_index=getparam_keywords.items()[-1]
            if keyword==constants.ENDLOOP:
                #insert 'endLoop' key to dict
                self.insert_into_getParamdict(keyword_index,keyword,None)
                #mapping 'getparam' and 'endloop'
                if start_index[1]==constants.GETPARAM:
                    self.insert_into_getParamdict(keyword_index,keyword,start_index)
                    self.insert_into_getParamdict(start_index[0],start_index[1],(keyword_index,keyword))
                #mapping 'endloop' to it's respective steps while backtracking
                while(start_index[1]!=constants.GETPARAM):
                    if (len(getparam_keywords)>0):
                        start_index=getparam_keywords.items()[-1]
                        self.insert_into_getParamdict(keyword_index,keyword,start_index)
                        self.insert_into_getParamdict(start_index[0],start_index[1],(keyword_index,keyword))
                        getparam_keywords.popitem()
                    else:
                        logger.log('Getparam is missing: Invalid script ')
                        flag=False
                        break
        else:
            self.insert_into_getParamdict(keyword_index,keyword,None)
        return flag

    def find_start_index(self,keyword,keyword_index,flag):
        if flag==1:
            return self.for_index(keyword,keyword_index)
        elif flag==2:
            return self.if_index(keyword,keyword_index)
        elif flag==3:
            return self.getparam_index(keyword,keyword_index)



    def parse_condition(self,testcase):
        flag=True
        for x in range(0,len(testcase)):
            step=testcase[x]
            keyword=step['keywordVal'].lower()
            outputval=step['outputVal'].strip()
            outputArray=outputval.split(';')
            if not (len(outputArray)>=1 and not(outputval.endswith('##;')) and outputval.split(';') and '##' in outputArray[len(outputArray)-1] ):
                logger.log(keyword)

                #getting 'for' info
                if keyword in for_array:
                    flag=self.find_start_index(keyword,x,1)
                    if flag==False:
                        return flag
                    if keyword in start_end_dict.values():
                        for_keywords[x]=keyword
                    copy_for_keywords[x]=keyword

                #getting 'if' info
                elif keyword in if_array:
                    flag=self.find_start_index(keyword,x,2)
                    if flag==False:
                        return flag
                    condition_keywords[x]=keyword
                    copy_condition_keywords[x]=keyword

                #getting 'getParam' info
                elif keyword in get_param:
                    flag=self.find_start_index(keyword,x,3)
                    if flag==False:
                        return flag
##                        break;
                    getparam_keywords[x]=keyword
                    copy_getparam_keywords[x]=keyword
            else:
                logger.log('Commented step '+str(step['stepNo']))
        return flag



    def create_step(self,index,keyword,apptype,inputval,objectname,outputval,stepnum,url,custname,testscript_name):
        key=(index,keyword)
        if keyword in for_array:
            tsp_step=For(index,keyword,inputval,outputval,stepnum,testscript_name,for_info[key],False)
        elif keyword in if_array:
            if if_info.has_key(key):
                tsp_step=If(index,keyword,inputval,outputval,stepnum,testscript_name,if_info[key],False)
            else:
                logger.log("'endIf' keyword missing in script:"+str(testscript_name))
                return False
        elif keyword in get_param:
            tsp_step=GetParam(index,keyword,inputval,outputval,stepnum,testscript_name,get_param_info[key],False)
        else:
            tsp_step=TestStepProperty(keyword,apptype,inputval,objectname,outputval,stepnum,url,custname,testscript_name)
        tsp_step.print_step()
        return tsp_step

    def extract_field(self,step,index,testscript_name):
        keyword=step['keywordVal'].lower()
        apptype=step['appType']
        inputval=step['inputVal']
        objectname=step['objectName']
        outputval=step['outputVal'].strip()
        stepnum=step['stepNo']
        url=step['url']
        custname=step['custname']
        outputArray=outputval.split(';')
        if not (len(outputArray)>=1 and not(outputval.endswith('##;')) and outputval.split(';') and '##' in outputArray[len(outputArray)-1] ):
            return self.create_step(index,keyword,apptype,inputval,objectname,outputval,stepnum,url,custname,testscript_name)
        return None


    def create_list(self,testcase,testscript_name):
        testcase.pop()
        flag=self.parse_condition(testcase)
        self.print_dict(if_info)
        for x in testcase:
            step=self.extract_field(x,testcase.index(x),testscript_name)
            if step is not None and step == True:
                tspList.append(step)
            elif step == False:
                break


    def print_dict(self,d):
        for k, v in d.items():
            print(k,':', v)

