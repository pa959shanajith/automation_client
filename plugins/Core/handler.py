#-------------------------------------------------------------------------------
# Name:        handler.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     18-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import json
import jumpBy
import jumpTo
from teststepproperty import TestStepProperty
import if_step
import for_step
import re
import getparam
from collections import OrderedDict
import constants
import logger
import logging
from core_utils import CoreUtils
import threading
from aws_keywords import *
local_handler = threading.local()



"""List to store the test steps"""
##tspList=[]

"""global index used in parse_condition method"""
##tspIndex=-1

"""global index used in create_list method"""
##tspIndex2=-1

"""Dict to store the for,endfor keywords"""
##copy_for_keywords=OrderedDict()
##for_keywords=OrderedDict()

"""Dict to store the if,elseIf,else,endIf keywords"""
##copy_condition_keywords=OrderedDict()
##condition_keywords=OrderedDict()

"""Dict to store the getparam,startloop,endloop keywords"""
##copy_getparam_keywords=OrderedDict()
##getparam_keywords=OrderedDict()

"""List containing for,endfor constants"""
##for_array=[constants.FOR,constants.ENDFOR]

"""List containing if,endif constants"""
##if_endIf=[constants.IF,constants.ENDIF]

"""List containing if,elseif,else,endif constants"""
##if_array=[constants.IF,constants.ELSE_IF,constants.ELSE,constants.ENDIF]

"""List containing getparam,startloop,endloop constants"""
##get_param=[constants.GETPARAM,constants.STARTLOOP,constants.ENDLOOP]

"""List to store the object of nested if info"""
##cond_nest_info=[]

"""Dict to store the start-end of for info"""
##for_info=OrderedDict()

"""Dict to store the start-end of if info"""

##if_info=OrderedDict()
"""Dict to store the start-end of getparam info"""
##get_param_info=OrderedDict()

"""Dict to store information about the possible start of each conditional keyword"""
##start_end_dict={constants.ENDFOR:[constants.FOR],
##                constants.FOR:[constants.ENDFOR],
##                constants.IF:[constants.ENDIF,constants.ELSE_IF,constants.ELSE],
##                constants.ENDIF:[constants.IF,constants.ELSE_IF,constants.ELSE],
##                constants.ELSE_IF:[constants.IF,constants.ELSE_IF],
##                constants.ELSE:[constants.IF,constants.ELSE_IF],
##                constants.GETPARAM:[constants.STARTLOOP],
##                constants.STARTLOOP:[constants.ENDLOOP]}

##ws_template=''
##ws_templates_dict={}
##testcasename = ''

##dynamic_variable_map=OrderedDict()
##log = logging.getLogger('handler.py')


class Handler():

    def __init__(self):
        global local_handler
        self.utils_obj=CoreUtils()
        local_handler.log = logging.getLogger('handler.py')
        local_handler.testcasename = ''
        local_handler.ws_templates_dict = {}
        local_handler.ws_template = ''
        local_handler.start_end_dict = {constants.ENDFOR:[constants.FOR],
                                      constants.FOR:[constants.ENDFOR],
                                      constants.ENDIF:[constants.IF,constants.ELSE_IF,constants.ELSE],
                                      constants.ELSE_IF:[constants.IF,constants.ELSE_IF],
                                      constants.ELSE:[constants.IF,constants.ELSE_IF],
                                      constants.GETPARAM:[constants.STARTLOOP],
                                      constants.STARTLOOP:[constants.ENDLOOP]}
        local_handler.get_param_info = OrderedDict()
        local_handler.if_info = OrderedDict()
        local_handler.for_info = OrderedDict()
        local_handler.cond_nest_info = []
        local_handler.get_param = [constants.GETPARAM,constants.STARTLOOP,constants.ENDLOOP]
        local_handler.if_array = [constants.IF,constants.ELSE_IF,constants.ELSE,constants.ENDIF]
        local_handler.if_endIf = [constants.IF,constants.ENDIF]
        local_handler.for_array = [constants.FOR,constants.ENDFOR]
        local_handler.getparam_keywords = OrderedDict()
        local_handler.copy_getparam_keywords = OrderedDict()
        local_handler.condition_keywords = OrderedDict()
        local_handler.copy_condition_keywords = OrderedDict()
        local_handler.for_keywords = OrderedDict()
        local_handler.copy_for_keywords = OrderedDict()
        local_handler.tspIndex2 = -1
        local_handler.tspIndex = -1
        local_handler.tspList = []
        local_handler.awsKeywords = {}
        local_handler.paramData={}

    def parse_json(self,test_data,data_param_path=None):
        """
        def : parse_json
        purpose : parses the given json and passes it to create list
        param : test_data (json list)
        return : None
        """
        local_handler.log.debug('Parsing')
        local_handler.log.debug('-------------------------')
        local_handler.log.debug('TSP list')
        local_handler.log.debug('-------------------------')
        json_string = json.dumps(test_data)
        new_obj = json.loads(json_string)
        script=[]
        testcasename_list=[]
        testcase_empty_flag = []
        empty_testcase_names=[]
        browser_type=[]
        datatables=[]
        extract_path = None
        if(data_param_path is not None and data_param_path != ''):
            data_param_path_temp = str(data_param_path)
            extract_path = [data_param_path_temp]
        #Iterating through json array
        appType=None
        for json_data in new_obj:
            #if json_data.has_key('template'):
                #ws_template=json_data['template']
            if 'testcase' in json_data:
                testcase=json_data['testcase']
                try:
                #Empty testcase scenerio not terminating fix Bug #246 (Himanshu)
                    if (len(testcase)==0 or testcase=='[]' or testcase=='' or testcase=='null'):
                        logger.print_on_console('Testcase is empty')
                        local_handler.log.info('Testcase is empty')
                        testcase_empty_flag.append(True)
                        if 'testcasename' in json_data:
                            empty_testcase_names.append(json_data['testcasename'])
                        continue
                except Exception as e:
                    local_handler.log.error(e)
                appType=None
                if('apptype' in json_data and json_data['apptype']=="MobileApp"):
                    local_handler.awsKeywords[json_data["testcasename"]]=set()
                    appType="MobileApp"
                script.append(testcase)
            # Checking if the testcase has key 'testscript_name' or 'testcasename'
            # adding the template to dict if available
            if 'testscript_name' in json_data:
                testscript_name=json_data['testscript_name']
                if 'template' in json_data:
                    local_handler.ws_templates_dict[testscript_name]=json_data['template']
                else:
                    local_handler.ws_templates_dict[testscript_name]=""
            elif 'testcasename' in json_data:
                testscript_name=json_data['testcasename']
                if 'template' in json_data:
                    local_handler.ws_templates_dict[testscript_name]=json_data['template']
                else:
                    local_handler.ws_templates_dict[testscript_name]=""
            local_handler.testcasename =testscript_name
            testcasename_list.append(testscript_name)
            if 'browsertype' in json_data:
                browser_type=json_data['browsertype']
            elif 'browserType' in json_data:
                browser_type=json_data['browserType']
            
            if 'datatables' in json_data:
                if len(json_data['datatables']): 
                    if not len(datatables):
                        # loop through all the datatables present testcase and append to datatables
                        for dt_index in range(len(json_data['datatables'])):
                            datatables.append(json_data['datatables'][dt_index])
            
        if not len(datatables):
                datatables=[]

        flag=self.create_list(script,testcasename_list,extract_path,appType)
        return flag,browser_type,len(script),datatables,testcase_empty_flag,empty_testcase_names


    def parse_json_execute(self,test_data):
        """
        def : parse_json
        purpose : parses the given json and passes it to create list
        param : test_data (json list)
        return : None
        """
        logger.print_on_console('Parsing')
        new_obj = json.loads(json.dumps(test_data))
        suite_data=[]
        scenarioIds={}
        browser_type={}
        dataparam_path={}
        report_type = "functionalTesting"
        condition_check={}
        #Iterating through json array
        try:
            suite_details=new_obj['suitedetails']
            suiteId_list=new_obj['testsuiteIds']
            batch_id=new_obj['batchId']
            execution_ids=new_obj['executionIds']
            exec_mode=new_obj['exec_mode']
            if 'integration' in new_obj:
                qc_creds=new_obj['integration']
            else:
                qc_creds={ "alm": { "url": "", "username": "", "password": "" },
                           "qtest": { "url": "", "username": "", "password": "", "qteststeps": "" },
                           "zephyr": { "url": "", "username": "", "password": "" }}
            if 'reportType' in new_obj: report_type = new_obj['reportType']
            for json_data,suite_id in zip(suite_details,suiteId_list):
                for i in json_data[suite_id]:
                    i["apptype"] = new_obj['apptype']
                suite_data.append(json_data[suite_id])
                if 'scenarioIds' in json_data:
                    scenarioIds[suite_id]=json_data['scenarioIds']
                if 'browserType' in json_data:
                    browser_type[suite_id]=json_data['browserType']
                if 'condition' in json_data:
                    condition_check[suite_id]=json_data['condition']
                if 'dataparampath' in json_data:
                    dataparam_path[suite_id]=json_data['dataparampath']
        except Exception as e:
            local_handler.log.error("Error while parsing data")
            local_handler.log.error(e,exc_info=True)
        return suiteId_list,suite_details,browser_type,scenarioIds,suite_data,execution_ids,batch_id,condition_check,dataparam_path,exec_mode,qc_creds,report_type

    def validate(self,start,end):
        """
        def : validate
        purpose : validates whether the start and end is proper based on 'start_end_dict' info
        param : start,end keywords
        return : bool
        """
        return end in local_handler.start_end_dict[start]

    def insert_into_fordict(self,keyword_index,keyword,start_index):
        """
        def : insert_into_fordict
        purpose : inserts the '(indexOfFor,for)' as 'key' and its respective endfor step as value 'indexofEndfor:endfor' and vice versa
        param : keyword_index,keyword,start_index
        return :
        """
        if start_index is not None:
            local_handler.for_info[start_index]=[{keyword_index:keyword}]
            local_handler.for_info[(keyword_index,keyword)]=[{start_index[0]:start_index[1]}]
            local_handler.for_keywords.popitem()
        else:
            local_handler.for_info[(keyword_index,keyword)]=None

    def insert_into_getParamdict(self,keyword_index,keyword,start_index):
        """
        def : insert_into_getParamdict
        purpose : inserts the '(indexOfgetParam,getparam)' as 'key' and its respective startLoop and endLoop as values and vice versa
        param : keyword_index,keyword,start_index
        return :
        """
        if start_index is not None:
            if not(start_index[1] == constants.ENDLOOP and keyword==constants.ENDLOOP):
                if start_index in local_handler.get_param_info and local_handler.get_param_info[start_index] is not None and (start_index != {keyword_index:keyword}):
                    local_handler.get_param_info[start_index].append({keyword_index:keyword})
                else:
                    local_handler.get_param_info[start_index]=[{keyword_index:keyword}]
        else:
            local_handler.get_param_info[(keyword_index,keyword)]=None

    def insert_into_ifdict(self,keyword_index,keyword,start_index):
        """
        def : insert_into_ifdict
        purpose : inserts the '(indexOfif,If)' as 'key' and its immediate end and its respective endIf step as values and vice versa
        param : keyword_index,keyword,start_index
        return :
        """
        if start_index is not None:
            if not(start_index[1] == constants.ENDIF and keyword==constants.ENDIF):
                if start_index in local_handler.if_info and local_handler.if_info[start_index] is not None and (start_index != {keyword_index:keyword}):
                    local_handler.if_info[start_index].append({keyword_index:keyword})
                else:
                    local_handler.if_info[start_index]=[{keyword_index:keyword}]
        else:
            local_handler.if_info[(keyword_index,keyword)]=None


    def for_index(self,keyword,keyword_index):
        """
        def : for_index
        purpose : finds the last value in 'for_keywords' dict, if it is 'endfor' then calls insert_into_fordict method
        param : keyword_index,keyword,start_index
        return : bool
        """
        flag=True

        if len(local_handler.for_keywords) != 0:
            start_index=list(local_handler.for_keywords.items())[-1]
            # if keyword == constants.ENDFOR and self.validate(keyword,start_index[1]):
            if keyword == constants.ENDFOR:
                self.insert_into_fordict(keyword_index,keyword,start_index)
            elif keyword== constants.ENDFOR:
                local_handler.log.error('For is missing: Invalid testcase ')
                logger.print_on_console('For is missing: Invalid testcase ')
                flag=False
            elif keyword==constants.FOR:
                self.insert_into_fordict(keyword_index,keyword,None)
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
        if len(local_handler.condition_keywords)>0:
            start_index=list(local_handler.condition_keywords.items())[-1]
            if not (keyword in local_handler.if_endIf) and self.validate(keyword,start_index[1]):
                self.insert_into_ifdict(keyword_index,keyword,start_index)
                #New change to insert even the satrt of the keyword
                self.insert_into_ifdict(start_index[0],start_index[1],(keyword_index,keyword))
            elif keyword==constants.ENDIF:
                whileflag=False
                #insert 'endIf' key to dict
                self.insert_into_ifdict(keyword_index,keyword,None)
                #mapping 'if' and 'endIf'
                if start_index[1]==constants.IF:
                    self.insert_into_ifdict(keyword_index,keyword,start_index)
                    self.insert_into_ifdict(start_index[0],start_index[1],(keyword_index,keyword))
                #mapping 'endIf' to it's respective steps while backtracking
                while(start_index[1]!=constants.IF):
                    whileflag=True
                    if (len(local_handler.condition_keywords)>0):
                        start_index=list(local_handler.condition_keywords.items())[-1]
                        self.insert_into_ifdict(keyword_index,keyword,start_index)
                        self.insert_into_ifdict(start_index[0],start_index[1],(keyword_index,keyword))
                        local_handler.condition_keywords.popitem()
                        flag=constants.ENDIF
                    else:
                        local_handler.log.error('IF is missing: Invalid Testcase ')
                        logger.print_on_console('IF is missing: Invalid script ')
                        flag=False
                        break
                #To fix issue with nested if blocks (without containing elseif/else blocks)
                if(start_index[1]==constants.IF and not(whileflag)):
                    local_handler.condition_keywords.popitem()
                    flag=constants.ENDIF

            elif keyword==constants.IF:
                # self.insert_into_ifdict(keyword_index,keyword,None)
                # New change to Map 'if' to 'if'
                self.insert_into_ifdict(keyword_index,keyword,(keyword_index,keyword))
        else:
            self.insert_into_ifdict(keyword_index,keyword,(keyword_index,keyword))
        return flag

    def getparam_index(self,keyword,keyword_index):
        """
        def : getparam_index
        purpose : finds the last value in 'getparam_keywords' dict, if it is valid 'end step', calls insert_into_getParamdict method
        param : keyword_index,keyword,start_index
        return : bool
        """
        flag=True
        if len(local_handler.getparam_keywords)>0:
            start_index=list(local_handler.getparam_keywords.items())[-1]
            if keyword==constants.ENDLOOP:
                #insert 'endLoop' key to dict
                self.insert_into_getParamdict(keyword_index,keyword,None)
                #mapping 'getparam' and 'endloop'
                if start_index[1]==constants.GETPARAM:
                    self.insert_into_getParamdict(keyword_index,keyword,start_index)
                    self.insert_into_getParamdict(start_index[0],start_index[1],(keyword_index,keyword))
                #mapping 'endloop' to it's respective steps while backtracking
                while(start_index[1]!=constants.GETPARAM):
                    if (len(local_handler.getparam_keywords)>0):
                        start_index=list(local_handler.getparam_keywords.items())[-1]
                        self.insert_into_getParamdict(keyword_index,keyword,start_index)
                        self.insert_into_getParamdict(start_index[0],start_index[1],(keyword_index,keyword))
                        local_handler.getparam_keywords.popitem()
                    else:
                        local_handler.log.error('Getparam is missing: Invalid testcase ')
                        logger.print_on_console('Getparam is missing: Invalid testcase ')
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



    def parse_condition(self,testcase,testscript_name,aws_flag=False):
        """
        def : parse_condition
        purpose : parses entire testcript json to map the corresponding start and end of if,for,getparam
        param : testcase,testscript_name,aws_flag
        return : bool
        """
        flag=True
        for x in range(0,len(testcase)):
            step=testcase[x]
            keyword=step['keywordVal']
            outputArray=step['outputVal'].strip().split(';')
            if not (len(outputArray)>=1 and  '##' == outputArray[-1] ):
                logger.print_on_console('keyword: '+keyword)
                local_handler.log.info('keyword: '+keyword)
                local_handler.log.debug(str(x)+'keyword: '+keyword)
                keyword=keyword.lower()
                if aws_flag:
                    if(keyword not in aws_supported_keywords):
                        local_handler.awsKeywords[testscript_name].add(step['keywordVal'])

                local_handler.tspIndex+=1

                #getting 'for' info
                if keyword in local_handler.for_array:
                    flag=self.find_start_index(keyword,local_handler.tspIndex,1)
                    if flag==False:
                        return flag
                    if keyword==constants.FOR:
                        local_handler.for_keywords[local_handler.tspIndex]=keyword
                    local_handler.copy_for_keywords[local_handler.tspIndex]=keyword

                #getting 'if' info
                elif keyword in local_handler.if_array:
                    flag=self.find_start_index(keyword,local_handler.tspIndex,2)
                    if flag==False:
                        return flag
                    if flag!=constants.ENDIF:
                        local_handler.condition_keywords[local_handler.tspIndex]=keyword
                    local_handler.copy_condition_keywords[local_handler.tspIndex]=keyword

                #getting 'getParam' info
                elif keyword in local_handler.get_param:
                    flag=self.find_start_index(keyword,local_handler.tspIndex,3)
                    if flag==False:
                        return flag
                    local_handler.getparam_keywords[local_handler.tspIndex]=keyword
                    local_handler.copy_getparam_keywords[local_handler.tspIndex]=keyword
            else:
                logger.print_on_console('Commented step '+str(step['stepNo']))
        return flag

    def create_step(self,index,keyword,apptype,inputval,objectname,identifiers,outputval,stepnum,url,custname,testscript_name,additionalinfo,i,remark,testcase_details,cord,original_device_height,original_device_width,top,left,width,height,extract_path=None):
        """
        def : create_step
        purpose : creates an object of each step
        param : keyword_index,keyword,start_index
        return : object
        """
        key_lower=keyword.lower()
        key=(index,key_lower)
        tsp_step=None
        try:
            #block which creates the step of instances of (for,endFor)
            if key_lower in local_handler.for_array:
                if not(key in local_handler.for_info):
                    self.insert_into_fordict(index,key_lower,None)
                    local_handler.log.error('Dangling if/for/getparam in testcase: '+str(testscript_name))
                    # logger.print_on_console('Dangling if/for/getparam in testcase: '+str(testscript_name))
                tsp_step=for_step.For(index,keyword,inputval,outputval,stepnum,testscript_name,local_handler.for_info[key],False,apptype,additionalinfo,i,remark,testcase_details)

            #block which creates the step of instances (if,elseIf,else,endIf)
            elif key_lower in local_handler.if_array:
                if not(key in local_handler.if_info):
                    self.insert_into_ifdict(index,key_lower,None)
                    local_handler.log.error('Dangling if/for/getparam in testcase: '+str(testscript_name))
                    # logger.print_on_console('Dangling if/for/getparam in testcase: '+str(testscript_name))

                tsp_step=if_step.If(index,keyword,inputval,outputval,stepnum,testscript_name,local_handler.if_info[key],False,apptype,additionalinfo,i,remark,testcase_details)

            #block which creates the step of instances of (getparam,startloop,endloop)
            elif key_lower in local_handler.get_param:
                if not(key in local_handler.get_param_info):
                    self.insert_into_getParamdict(index,key_lower,None)
                    local_handler.log.error('Dangling if/for/getparam in testcase: '+str(testscript_name))
                    # logger.print_on_console('Dangling if/for/getparam in testcase: '+str(testscript_name))

                if(extract_path==None):
                    tsp_step=getparam.GetParam(index,keyword,inputval,outputval,stepnum,testscript_name,local_handler.get_param_info[key],False,apptype,additionalinfo,i,remark,testcase_details)
                else:
                    tsp_step=getparam.GetParam(index,keyword,extract_path,outputval,stepnum,testscript_name,local_handler.get_param_info[key],False,apptype,additionalinfo,i,remark,testcase_details)

            #block which creates the step of instances of (jumpBy)
            elif key_lower == constants.JUMP_BY:
                tsp_step=jumpBy.JumpBy(index,keyword,inputval,outputval,stepnum,testscript_name,False,apptype,additionalinfo,i,remark,testcase_details)

            #block which creates the step of instances of (jumpTo)
            elif key_lower == constants.JUMP_TO:
                tsp_step=jumpTo.JumpTo(index,keyword,inputval,outputval,stepnum,testscript_name,False,apptype,additionalinfo,i,remark,testcase_details)

            #block which creates the step of instances of (Keywords)
            else:
                #Implementation of Decryption of Xpath and url
                #Currenlty implemented only for WEB and MobileWeb apptype
                if(apptype.lower() == constants.APPTYPE_WEB or apptype.lower() == constants.APPTYPE_MOBILE ):
                    try:
                        #Handling url of pages having iframes and frames
                        if len(url.strip())!=0 and (not ("https" in url or "http" in url)) and not re.match('\d[if]\/',url):
                            url_dec=self.utils_obj.scrape_unwrap(url)
                            if url is not None: url = url_dec
                        if(objectname.strip() != '' and not(objectname.startswith('@')) and len(objectname.split(';')) == 3):
                            xpath_string=objectname.split(';')
                            left_part=self.utils_obj.scrape_unwrap(xpath_string[0])
                            right_part=self.utils_obj.scrape_unwrap(xpath_string[2])
                            if left_part is not None and right_part is not None:
                                objectname = left_part+';'+xpath_string[1]+';'+right_part
                    except Exception as e:
                        local_handler.log.error(e)
                tsp_step=TestStepProperty(keyword,index,apptype,inputval,objectname,identifiers,outputval,stepnum,url,custname,testscript_name,additionalinfo,i,remark,testcase_details,cord,original_device_height,original_device_width,top,left,width,height)
        except Exception as e:
            logger.print_on_console(e)
            local_handler.log.error(e)
        return tsp_step

    def extract_field(self,step,index,testscript_name,i,extract_path = None):
        """
        def : extract_field
        purpose : extracts the value of each key present in test step json
        param : test_step,index,testscript_name
        return : object/None
        """
        keyword=step['keywordVal']
        apptype=step['appType']
        inputval=step['inputVal']
        objectname=step['objectName']
        if 'identifier' in step:
            identifiers=step['identifier']
        else:
            identifiers = ''
        outputval=step['outputVal'].strip()
        stepnum=step['stepNo']
        url=step['url']
        custname=step['custname']

        if 'original_device_height' in step and 'original_device_width' in step:
            original_device_height = step['original_device_height']
            original_device_width = step['original_device_width']
        else:
            original_device_height = None
            original_device_width = None
        if('cord' in step):
            cord=step['cord']
        else:
            cord=None
        remark=''
        testcase_details=''
        if 'remarks' in step:
            remark=step['remarks']
        if 'addTestCaseDetailsInfo' in step:
            testcase_details=step['addTestCaseDetailsInfo']
        
        if 'top' in step:
            top = step['top']
        else:
            top = None

        if 'left' in step:
            left = step['left']
        else:
            left = None

        if 'width' in step:
            width = step['width']
        else:
            width = None

        if 'height' in step:
            height = step['height']
        else:
            height = None

        additionalinfo = ''
        outputArray=outputval.split(';')
        #check if the step is commented before adding to the tsplist
        if not (len(outputArray)>=1 and  '##' == outputArray[-1] ):
            local_handler.tspIndex2+=1
            return self.create_step(local_handler.tspIndex2,keyword,apptype,inputval,objectname,identifiers,outputval,stepnum,url,custname,testscript_name,additionalinfo,i,remark,testcase_details,cord, original_device_height, original_device_width,top,left,width,height,extract_path)
        return None


    def create_list(self,testcase,testscript_name,extract_path= None,appType=None):
        """
        def : create_list
        purpose : appends each test case step into gloabl tsplist
        param : test_step,index,testscript_name
        return :

        """
        #popping the comments key in testcase json before parsing if it has
        #To fix the UAT defect #3390:
        #If We are giving the start loop in one script and end loop in another script it?s not working.
        #In First for loop, complete json data is parsed to build info_dict of getparam,for,if and in second for loop creation of
        #each step is done
        #Earlier the whole process was done for single testcase at a time, now it's done for entire scenario at once
        aws_flag=False
        if appType is not None : aws_flag=True
        testcase_copy=[]
        for i in range(len(testcase)):
            try:
                d=eval(testcase[i])
            except:
                d=testcase[i]
            if len(d)>0 and 'comments' in d[len(d)-1]:
                d.pop()
            testcase_copy.append(d)
            self.parse_condition(d,testscript_name[i],aws_flag)

        for i in range(len(testcase_copy)):
            for x in testcase_copy[i]:
                step=self.extract_field(x, local_handler.tspIndex2, testscript_name[i], i+1, extract_path)
                if step is not None and step != False:
                    local_handler.tspList.append(step)
                elif step == False:
                    return step
        return True

    def read_step(self):
        """
        def : read_step
        purpose : prints the global tsp list
        param : dict
        return :
        """
        local_handler.log.info('Printing each step in TSP')
        local_handler.log.info('-------------------------')
        local_handler.log.info('TSP list')
        local_handler.log.info('-------------------------')
        for x in local_handler.tspList:
            x.print_step()
            # logger.print_on_console('\n')
        return local_handler.tspList

    def print_dict(self,d):
        """
        def : print_dict
        purpose : utility method to print the dictionary
        param : dict
        return :
        """
        if len(d)==0:
            print(d,' is empty')
        for k, v in list(d.items()):
            print((k,':', v))

    def clearList(self,con):
        """
        def : clearList
        purpose : Reset all global variables after the execution of each Scenario
        param : dict
        return :
        """
        global local_handler
        import dynamic_variable_handler
        del local_handler.tspList[:]
        del local_handler.cond_nest_info[:]
        local_handler.tspIndex=-1
        local_handler.tspIndex2=-1
        local_handler.copy_for_keywords.clear()
        local_handler.for_keywords.clear()
        local_handler.copy_condition_keywords.clear()
        local_handler.condition_keywords.clear()
        local_handler.copy_getparam_keywords.clear()
        local_handler.getparam_keywords.clear()
        local_handler.for_info.clear()
        local_handler.if_info.clear()
        local_handler.get_param_info.clear()
        local_handler.ws_template=''
        local_handler.ws_templates_dict.clear()
        #dynamic_variable_handler.dynamic_variable_map.clear()
        if con.oebs_dispatcher_obj != None:
            con.oebs_dispatcher_obj.clear_oebs_window_name()
            # dynamic_variable_handler.dynamic_variable_map.clear()

    def clear_dyn_variables(self):
        import dynamic_variable_handler
        dynamic_variable_handler.local_dynamic.dynamic_variable_map.clear()

    def clear_const_variables(self):
        import constant_variable_handler
        constant_variable_handler.local_constant.constant_variable_map.clear()
