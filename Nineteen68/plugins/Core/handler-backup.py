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



"""List to store the test steps"""
tspList=[]

"""global index used in parse_condition method"""
tspIndex=-1

"""global index used in create_list method"""
tspIndex2=-1

"""Dict to store the for,endfor keywords"""
copy_for_keywords=OrderedDict()
for_keywords=OrderedDict()

"""Dict to store the if,elseIf,else,endIf keywords"""
copy_condition_keywords=OrderedDict()
condition_keywords=OrderedDict()

"""Dict to store the getparam,startloop,endloop keywords"""
copy_getparam_keywords=OrderedDict()
getparam_keywords=OrderedDict()

"""List containing for,endfor constants"""
for_array=[constants.FOR,constants.ENDFOR]

"""List containing if,endif constants"""
if_endIf=[constants.IF,constants.ENDIF]

"""List containing if,elseif,else,endif constants"""
if_array=[constants.IF,constants.ELSE_IF,constants.ELSE,constants.ENDIF]

"""List containing getparam,startloop,endloop constants"""
get_param=[constants.GETPARAM,constants.STARTLOOP,constants.ENDLOOP]

"""Dict to store the start-end of for info"""
for_info={}
"""Dict to store the start-end of if info"""
if_info={}
"""Dict to store the start-end of getparam info"""
get_param_info={}

"""Dict to store information about the possible start of each conditional keyword"""
start_end_dict={constants.ENDFOR:[constants.FOR],
                constants.ENDIF:[constants.IF,constants.ELSE_IF,constants.ELSE],
                constants.ELSE_IF:[constants.IF,constants.ELSE_IF],
                constants.ELSE:[constants.IF,constants.ELSE_IF],
                constants.GETPARAM:[constants.STARTLOOP],
                constants.STARTLOOP:[constants.ENDLOOP]}

class Handler():

    def parse_json(self,test_data):
        """
        def : parse_json
        purpose : parses the given json and passes it to create list
        param : test_data (json list)
        return : None

        """
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
        """
        def : validate
        purpose : validates whether the start and end is proper based on 'start_end_dict' info
        param : start,end keywords
        return : bool

        """
        return end in start_end_dict[start]

    def insert_into_fordict(self,keyword_index,keyword,start_index):
        """
        def : insert_into_fordict
        purpose : inserts the '(indexOfFor,for)' as 'key' and its respective endfor step as value 'indexofEndfor:endfor' and vice versa
        param : keyword_index,keyword,start_index
        return :

        """
        if start_index is not None:
            for_info[start_index]=[{keyword_index:keyword}]
            for_info[(keyword_index,keyword)]=[{start_index[0]:start_index[1]}]
            for_keywords.popitem()
        else:
            for_info[(keyword_index,keyword)]=None

    def insert_into_getParamdict(self,keyword_index,keyword,start_index):
        """
        def : insert_into_getParamdict
        purpose : inserts the '(indexOfgetParam,for)' as 'key' and its respective startLoop and endLoop as values and vice versa
        param : keyword_index,keyword,start_index
        return :

        """
        if start_index is not None:
            if not(start_index[1] == constants.ENDLOOP and keyword==constants.ENDLOOP):
                if get_param_info.has_key(start_index) and get_param_info[start_index] is not None and (start_index != {keyword_index:keyword}):
                    get_param_info[start_index].append({keyword_index:keyword})
                else:
                    get_param_info[start_index]=[{keyword_index:keyword}]
        else:
            if_info[(keyword_index,keyword)]=None

    def insert_into_ifdict(self,keyword_index,keyword,start_index):
        """
        def : insert_into_ifdict
        purpose : inserts the '(indexOfif,If)' as 'key' and its immediate end and its respective endIf step as values and vice versa
        param : keyword_index,keyword,start_index
        return :

        """
        if start_index is not None:
            if not(start_index[1] == constants.ENDIF and keyword==constants.ENDIF):
                if if_info.has_key(start_index) and if_info[start_index] is not None and (start_index != {keyword_index:keyword}):
                    if_info[start_index].append({keyword_index:keyword})
                else:
                    if_info[start_index]=[{keyword_index:keyword}]
        else:
            if_info[(keyword_index,keyword)]=None


    def for_index(self,keyword,keyword_index):
        """
        def : for_index
        purpose : finds the last value in 'for_keywords' dict, if it is 'endfor' then calls insert_into_fordict method
        param : keyword_index,keyword,start_index
        return : bool

        """
        flag=True
        if len(for_keywords) != 0:
            start_index=for_keywords.items()[-1]
            if start_end_dict.has_key(keyword):
                self.insert_into_fordict(keyword_index,keyword,start_index)
        else:
            self.insert_into_fordict(keyword_index,keyword,None)
        return flag

    def if_index(self,keyword,keyword_index):
        """
        def : if_index
        purpose : finds the last value in 'condition_keywords' dict, if it is valid 'end step', calls insert_into_ifdict method
        param : keyword_index,keyword,start_index
        return : bool

        """
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
            elif keyword==constants.IF:
                self.insert_into_ifdict(keyword_index,keyword,None)

        else:
            self.insert_into_ifdict(keyword_index,keyword,None)
        return flag

    def getparam_index(self,keyword,keyword_index):
        """
        def : getparam_index
        purpose : finds the last value in 'getparam_keywords' dict, if it is valid 'end step', calls insert_into_getParamdict method
        param : keyword_index,keyword,start_index
        return : bool

        """
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
        """
        def : find_start_index
        purpose : calls respective method to find the start step of the given keyword
        param : keyword_index,keyword,start_index
        return : bool

        """
        if flag==1:
            return self.for_index(keyword,keyword_index)
        elif flag==2:
            return self.if_index(keyword,keyword_index)
        elif flag==3:
            return self.getparam_index(keyword,keyword_index)



    def parse_condition(self,testcase):
        """
        def : parse_condition
        purpose : parses entire testcript json to map the corresponding start and end of if,for,getparam
        param : keyword_index,keyword,start_index
        return : bool

        """
        flag=True

        for x in range(0,len(testcase)):
            global tspIndex
            tspIndex+=1
            step=testcase[x]

            keyword=step['keywordVal']
            outputval=step['outputVal'].strip()
            outputArray=outputval.split(';')
            if not (len(outputArray)>=1 and not(outputval.endswith('##;')) and outputval.split(';') and '##' in outputArray[len(outputArray)-1] ):
                logger.log(str(x)+' '+keyword)
                keyword=keyword.lower()

                #getting 'for' info
                if keyword in for_array:
                    flag=self.find_start_index(keyword,tspIndex,1)
                    if flag==False:
                        return flag
                    if keyword in start_end_dict.values():
                        for_keywords[tspIndex]=keyword
                    copy_for_keywords[tspIndex]=keyword

                #getting 'if' info
                elif keyword in if_array:
                    flag=self.find_start_index(keyword,tspIndex,2)
                    if flag==False:
                        return flag
                    condition_keywords[tspIndex]=keyword
                    copy_condition_keywords[tspIndex]=keyword

                #getting 'getParam' info
                elif keyword in get_param:
                    flag=self.find_start_index(keyword,tspIndex,3)
                    if flag==False:
                        return flag
                    getparam_keywords[tspIndex]=keyword
                    copy_getparam_keywords[tspIndex]=keyword
            else:
                logger.log('Commented step '+str(step['stepNo']))
        return flag



    def create_step(self,index,keyword,apptype,inputval,objectname,outputval,stepnum,url,custname,testscript_name):
        """
        def : create_step
        purpose : creates an object of each step
        param : keyword_index,keyword,start_index
        return : object

        """
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
            tsp_step=TestStepProperty(keyword,index,apptype,inputval,objectname,outputval,stepnum,url,custname,testscript_name)
        return tsp_step

    def extract_field(self,step,index,testscript_name):
        """
        def : extract_field
        purpose : extracts the value of each key present in test step json
        param : test_step,index,testscript_name
        return : object/None

        """
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
        """
        def : create_list
        purpose : appends each test case step into gloabl tsplist
        param : test_step,index,testscript_name
        return :

        """
        #popping the comments key in testcase before parsing
        testcase.pop()
        flag=self.parse_condition(testcase)
        for x in testcase:
            global tspIndex2
            tspIndex2+=1
            step=self.extract_field(x,tspIndex2,testscript_name)
            if step is not None and step != False:
                tspList.append(step)
            elif step == False:
                break




    def read_step(self):
        """
        def : read_step
        purpose : prints the global tsp list
        param : dict
        return :

        """
        self.print_dict(if_info)
        logger.log('TSP list\n')
        for x in tspList:
            x.print_step()
            logger.log('\n')

    def print_dict(self,d):
        """
        def : print_dict
        purpose : utility method to print the dictionary
        param : dict
        return :

        """
        for k, v in d.items():
            print(k,':', v)

