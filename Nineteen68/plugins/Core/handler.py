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
import getparam
from collections import OrderedDict
import constants
import logger
import logging
from core_utils import CoreUtils



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

"""List to store the object of nested if info"""
cond_nest_info=[]

"""Dict to store the start-end of for info"""
for_info=OrderedDict()

"""Dict to store the start-end of if info"""

if_info=OrderedDict()
"""Dict to store the start-end of getparam info"""
get_param_info=OrderedDict()

"""Dict to store information about the possible start of each conditional keyword"""
start_end_dict={constants.ENDFOR:[constants.FOR],
                constants.FOR:[constants.ENDFOR],
##                constants.IF:[constants.ENDIF,constants.ELSE_IF,constants.ELSE],
                constants.ENDIF:[constants.IF,constants.ELSE_IF,constants.ELSE],
                constants.ELSE_IF:[constants.IF,constants.ELSE_IF],
                constants.ELSE:[constants.IF,constants.ELSE_IF],
                constants.GETPARAM:[constants.STARTLOOP],
                constants.STARTLOOP:[constants.ENDLOOP]}

ws_template=''
ws_templates_dict={}
testcasename = ''

##dynamic_variable_map=OrderedDict()
log = logging.getLogger('handler.py')


class Handler():

    def __init__(self):
        self.utils_obj=CoreUtils()

    def parse_json(self,test_data,data_param_path=None):
        """
        def : parse_json
        purpose : parses the given json and passes it to create list
        param : test_data (json list)
        return : None

        """
##        import  ftfy
        global ws_template
        global ws_templates_dict
        log.debug('Parsing')
        log.debug('-------------------------')
        log.debug('TSP list')
        log.debug('-------------------------')
        json_string = json.dumps(test_data)
        new_obj = json.loads(json_string)
        script=[]
        testcasename_list=[]
        testcase_empty_flag = []
        empty_testcase_names=[]
        browser_type=[]
        extract_path = []
        if(data_param_path is not None and data_param_path != ''):
            data_param_path_temp = str(data_param_path)
            extract_path.append(data_param_path_temp)
        #Iterating through json array
        for json_data in new_obj:
            #if json_data.has_key('template'):
                #ws_template=json_data['template']
            if json_data.has_key('testcase'):
                testcase=json_data['testcase']
                try:
                #Empty testcase scenerio not terminating fix Bug #246 (Himanshu)
                    if (len(testcase)==0 or testcase=='[]' or testcase=='' or testcase=='null'):
                        logger.print_on_console('Testcase is empty')
                        log.info('Testcase is empty')
                        testcase_empty_flag.append(True)
                        if json_data.has_key('testcasename'):
                            empty_testcase_names.append(json_data['testcasename'])
                        continue
                except Exception as e:
                    log.error(e)

                #passing test case value to ftfy module to handle special charcter
##                if(type(testcase) == 'unicode'):
##                    temp_testcase = ftfy.fix_text(testcase)
##                    script.append(temp_testcase)
##                else:
##                script.append(testcase)
                script.append(testcase)
            if json_data.has_key('comments'):
                comments=json_data['comments']
            #Checking if the testcase has key 'testscript_name' or 'testcasename'
            #adding the template to dict if available
            if json_data.has_key('testscript_name'):
                testscript_name=json_data['testscript_name']
                if json_data.has_key('template'):
                    ws_templates_dict[testscript_name]=json_data['template']
                else:
                    ws_templates_dict[testscript_name]=""
            elif json_data.has_key('testcasename'):
                testscript_name=json_data['testcasename']
                if json_data.has_key('template'):
                    ws_templates_dict[testscript_name]=json_data['template']
                else:
                    ws_templates_dict[testscript_name]=""
            global testcasename
            testcasename =testscript_name
            testcasename_list.append(testscript_name)
            if json_data.has_key('browsertype'):
                browser_type=json_data['browsertype']
            elif json_data.has_key('browserType'):
                browser_type=json_data['browserType']
        if(data_param_path is None or data_param_path == ''):
            flag=self.create_list(script,testcasename_list)
        else:
            flag=self.create_list(script,testcasename_list,extract_path)
        return flag,browser_type,len(script),testcase_empty_flag,empty_testcase_names


    def parse_json_execute(self,test_data):
        """
        def : parse_json
        purpose : parses the given json and passes it to create list
        param : test_data (json list)
        return : None

        """
        logger.print_on_console('Parsing')
        json_string = json.dumps(test_data)
        new_obj = json.loads(json_string)
        suite_data=[]
        scenarioIds={}
        browser_type={}
        dataparam_path={}
        condition_check={}
        suiteId_list=[]
        suite_details=[]
        execution_id=[]
        #Iterating through json array

        try:
            #Getting suite_data
            suite_details=new_obj['suitedetails']
            #Getting suite_ids
            suiteId_list=new_obj['testsuiteIds']
            execution_id=new_obj['executionId']
            for json_data,suite_id in zip(suite_details,suiteId_list):
                if type(suite_id)==unicode:
                    suite_id=str(suite_id)

                suite_data.append(json_data[suite_id])
                if json_data.has_key('scenarioIds'):
                    scenarioIds[suite_id]=json_data['scenarioIds']

                if json_data.has_key('browserType'):
                    browser_type[suite_id]=json_data['browserType']

                if json_data.has_key('condition'):
                    condition_check[suite_id]=json_data['condition']

                if json_data.has_key('dataparampath'):
                    dataparam_path[suite_id]=json_data['dataparampath']
        except Exception as e:
            print e
        return suiteId_list,suite_details,browser_type,scenarioIds,suite_data,execution_id,condition_check,dataparam_path

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
        purpose : inserts the '(indexOfgetParam,getparam)' as 'key' and its respective startLoop and endLoop as values and vice versa
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
            get_param_info[(keyword_index,keyword)]=None

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
##            if keyword == constants.ENDFOR and self.validate(keyword,start_index[1]):
            if keyword == constants.ENDFOR:
                self.insert_into_fordict(keyword_index,keyword,start_index)
            elif keyword== constants.ENDFOR:
                log.error('For is missing: Invalid testcase ')
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
        if len(condition_keywords)>0:
            start_index=condition_keywords.items()[-1]
            if not (keyword in if_endIf) and self.validate(keyword,start_index[1]):
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
                    if (len(condition_keywords)>0):
                        start_index=condition_keywords.items()[-1]
                        self.insert_into_ifdict(keyword_index,keyword,start_index)
                        self.insert_into_ifdict(start_index[0],start_index[1],(keyword_index,keyword))
                        condition_keywords.popitem()
                        flag=constants.ENDIF
                    else:
                        log.error('IF is missing: Invalid Testcase ')
                        logger.print_on_console('IF is missing: Invalid script ')
                        flag=False
                        break
                #To fix issue with nested if blocks (without containing elseif/else blocks)
                if(start_index[1]==constants.IF and not(whileflag)):
                    condition_keywords.popitem()
                    
            elif keyword==constants.IF:
##                self.insert_into_ifdict(keyword_index,keyword,None)
                  #New change to Map 'if' to 'if'
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
                        log.error('Getparam is missing: Invalid testcase ')
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



    def parse_condition(self,testcase):
        """
        def : parse_condition
        purpose : parses entire testcript json to map the corresponding start and end of if,for,getparam
        param : keyword_index,keyword,start_index
        return : bool

        """
        flag=True

        for x in range(0,len(testcase)):
            step=testcase[x]

            keyword=step['keywordVal']
            outputval=step['outputVal'].strip()
            outputArray=outputval.split(';')
            if not (len(outputArray)>=1 and not(outputval.endswith('##;')) and outputval.split(';') and '##' in outputArray[len(outputArray)-1] ):
                logger.print_on_console('keyword: '+keyword)
                log.info('keyword: '+keyword)
                log.debug(str(x)+'keyword: '+keyword)
                keyword=keyword.lower()
                global tspIndex
                tspIndex+=1

                #getting 'for' info
                if keyword in for_array:
                    flag=self.find_start_index(keyword,tspIndex,1)
                    if flag==False:
                        return flag
                    if keyword==constants.FOR:
                        for_keywords[tspIndex]=keyword
                    copy_for_keywords[tspIndex]=keyword

                #getting 'if' info
                elif keyword in if_array:
                    flag=self.find_start_index(keyword,tspIndex,2)
                    if flag==False:
                        return flag
                    if flag!=constants.ENDIF:
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
                logger.print_on_console('Commented step '+str(step['stepNo']))
        return flag



    def create_step(self,index,keyword,apptype,inputval,objectname,outputval,stepnum,url,custname,testscript_name,additionalinfo,i,remark,testcase_details,cord,extract_path=None):
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
            if key_lower in for_array:
                if not(for_info.has_key(key)):
                    self.insert_into_fordict(index,key_lower,None)
                    log.error('Dangling if/for/getparam in testcase: '+str(testscript_name))
##                    logger.print_on_console('Dangling if/for/getparam in testcase: '+str(testscript_name))
                tsp_step=for_step.For(index,keyword,inputval,outputval,stepnum,testscript_name,for_info[key],False,apptype,additionalinfo,i,remark,testcase_details)

            #block which creates the step of instances (if,elseIf,else,endIf)
            elif key_lower in if_array:
                if not(if_info.has_key(key)):
                    self.insert_into_ifdict(index,key_lower,None)
                    log.error('Dangling if/for/getparam in testcase: '+str(testscript_name))
##                    logger.print_on_console('Dangling if/for/getparam in testcase: '+str(testscript_name))

                tsp_step=if_step.If(index,keyword,inputval,outputval,stepnum,testscript_name,if_info[key],False,apptype,additionalinfo,i,remark,testcase_details)

            #block which creates the step of instances of (getparam,startloop,endloop)
            elif key_lower in get_param:
                if not(get_param_info.has_key(key)):
                    self.insert_into_getParamdict(index,key_lower,None)
                    log.error('Dangling if/for/getparam in testcase: '+str(testscript_name))
##                    logger.print_on_console('Dangling if/for/getparam in testcase: '+str(testscript_name))

                if(extract_path==None):
                    tsp_step=getparam.GetParam(index,keyword,inputval,outputval,stepnum,testscript_name,get_param_info[key],False,apptype,additionalinfo,i,remark,testcase_details)
                else:
                    tsp_step=getparam.GetParam(index,keyword,extract_path,outputval,stepnum,testscript_name,get_param_info[key],False,apptype,additionalinfo,i,remark,testcase_details)

            #block which creates the step of instances of (jumpBy)
            elif key_lower == constants.JUMP_BY:
                tsp_step=jumpBy.JumpBy(index,keyword,inputval,outputval,stepnum,testscript_name,False,apptype,additionalinfo,i,remark,testcase_details)

            #block which creates the step of instances of (jumpTo)
            elif key_lower == constants.JUMP_TO:
                tsp_step=jumpTo.JumpTo(index,keyword,inputval,outputval,stepnum,testscript_name,False,apptype,additionalinfo,i,remark,testcase_details)

            #block which creates the step of instances of (Keywords)
            else:
                #Implementation of Decryption of Xpath and url
                #Currenlty implemented only for WEB apptype
                if(apptype.lower() == constants.APPTYPE_WEB):
                    try:
                        if len(url.strip())!=0:
                            url=self.utils_obj.scrape_unwrap(url)
                        if(objectname.strip() != '' and not(objectname.startswith('@'))):
                            xpath_string=objectname.split(';')
                            left_part=self.utils_obj.scrape_unwrap(xpath_string[0])
                            right_part=self.utils_obj.scrape_unwrap(xpath_string[2])
                            objectname = left_part+';'+xpath_string[1]+';'+right_part
                    except Exception as e:
                        log.error(e)
                tsp_step=TestStepProperty(keyword,index,apptype,inputval,objectname,outputval,stepnum,url,custname,testscript_name,additionalinfo,i,remark,testcase_details,cord)
        except Exception as e:
            logger.print_on_console(e)
            log.error(e)
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
        outputval=step['outputVal'].strip()
        stepnum=step['stepNo']
        url=step['url']
        custname=step['custname']
        if(step.has_key('cord')): 
            cord=step['cord']
        else:
            cord=None
        remark=''
        testcase_details=''
        if 'remarks' in step:
            remark=step['remarks']
        if 'addTestCaseDetailsInfo' in step:
            testcase_details=step['addTestCaseDetailsInfo']

        additionalinfo = ''
        outputArray=outputval.split(';')
        #check if the step is commented before adding to the tsplist
        if not (len(outputArray)>=1 and not(outputval.endswith('##;')) and outputval.split(';') and '##' in outputArray[len(outputArray)-1] ):
            global tspIndex2
            tspIndex2+=1
            return self.create_step(tspIndex2,keyword,apptype,inputval,objectname,outputval,stepnum,url,custname,testscript_name,additionalinfo,i,remark,testcase_details,cord,extract_path)
        return None


    def create_list(self,testcase,testscript_name,extract_path= None):
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
        testcase_copy=[]
        for i in range(len(testcase)):
            try:
                d=eval(testcase[i])
            except Exception as e:
                d=testcase[i]
            if len(d)>0 and d[len(d)-1].has_key('comments'):
                d.pop()
            testcase_copy.append(d)
            flag=self.parse_condition(d)

        for i in range(len(testcase_copy)):
            for x in testcase_copy[i]:
                if extract_path == None:
                    step=self.extract_field(x,tspIndex2,testscript_name[i],i+1)
                else:
                    step=self.extract_field(x,tspIndex2,testscript_name[i],i+1,extract_path)
                if step is not None and step != False:
                    tspList.append(step)
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
        log.info('Printing each step in TSP')
        log.info('-------------------------')
        log.info('TSP list')
        log.info('-------------------------')
        for x in tspList:
            x.print_step()
##            logger.print_on_console('\n')
        return tspList

    def print_dict(self,d):
        """
        def : print_dict
        purpose : utility method to print the dictionary
        param : dict
        return :

        """
        if len(d)==0:
            print d,' is empty'
        for k, v in d.items():
            print(k,':', v)

    def clearList(self,con):
        """
        def : clearList
        purpose : Reset all global variables after the execution of each Scenario
        param : dict
        return :

        """
        import dynamic_variable_handler
        del tspList[:]
        del cond_nest_info[:]
        global tspIndex,tspIndex2,copy_for_keywords,for_keywords,copy_condition_keywords,condition_keywords,copy_getparam_keywords                        ,getparam_keywords,for_info,if_info,get_param_info
        tspIndex=-1
        tspIndex2=-1
        copy_for_keywords.clear()
        for_keywords.clear()
        copy_condition_keywords.clear()
        condition_keywords.clear()
        copy_getparam_keywords.clear()
        getparam_keywords.clear()
        for_info.clear()
        if_info.clear()
        get_param_info.clear()
        ws_template=''
        global ws_templates_dict
        ws_templates_dict.clear();
        #dynamic_variable_handler.dynamic_variable_map.clear()
        if con.oebs_dispatcher_obj != None:
            con.oebs_dispatcher_obj.clear_oebs_window_name()
            	##        dynamic_variable_handler.dynamic_variable_map.clear()
    def clear_dyn_variables(self):
        import dynamic_variable_handler
        dynamic_variable_handler.dynamic_variable_map.clear()
