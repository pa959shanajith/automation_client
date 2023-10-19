#-------------------------------------------------------------------------------
# Name:        controller.py
# Purpose:
#
# Author:      wasimakram.sutar,sushma.p,rakesh.v
#
# Created:     02-11-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from concurrent.futures import ThreadPoolExecutor
import threading
from datetime import datetime
import logging
import time
import platform
import if_step
import for_step
import getparam
import jumpTo
import jumpBy
from teststepproperty import TestStepProperty
import handler
import os,sys
import re
import wx
import subprocess
import logger
import json
from constants import *
import dynamic_variable_handler
import constant_variable_handler
import reporting
import core_utils
import recording
from logging.handlers import TimedRotatingFileHandler
import shutil
import requests
local_cont = threading.local()
import cicd_core
from retryapis_cicd import Retryrequests
#index for iterating the teststepproperty for executor
##i = 0
terminate_flag=False
manual_terminate_flag=False
pause_flag=False
iris_constant_step = -1
socket_object = None
saucelabs_count = 0
browserstack_count = 0
# test_case_number = 0
log = logging.getLogger("controller.py")
status_percentage = {TEST_RESULT_PASS:0,TEST_RESULT_FAIL:0,TERMINATE:0,"total":0}
process_ids = []
screen_testcase_map= {}
class ThreadLogFilter(logging.Filter):
    """
    This filter only show log entries for specified thread name
    """

    def __init__(self, thread_name, *args, **kwargs):
        logging.Filter.__init__(self, *args, **kwargs)
        self.thread_name = thread_name

    def filter(self, record):
        return record.threadName == self.thread_name
class Controller():
    mobile_web_dispatcher_obj = None
    oebs_dispatcher_obj = None
    webservice_dispatcher_obj = None
    outlook_dispatcher_obj = None
    desktop_dispatcher_obj = None
    sap_dispatcher_obj = None
    mobile_app_dispatcher_obj = None
    mainframe_dispatcher_obj = None
    system_dispatcher_obj = None
    pdf_dispatcher_obj = None

    def __init__(self):
        global local_cont
        local_cont.web_dispatcher_obj = None
        local_cont.accessibility_testing_obj = None
        local_cont.generic_dispatcher_obj = None
        local_cont.test_case_number = 0
        local_cont.module_stop=False
        self.action=None
        core_utils.get_all_the_imports(CORE)
        self.cur_dir= os.getcwd()
        self.previous_step=''
        self.verify_dict={'web':VERIFY_EXISTS,
        'oebs':VERIFY_VISIBLE,'sap':VERIFY_EXISTS,'desktop':VERIFY_EXISTS,'mobileweb':VERIFY_EXISTS}
        self.dynamic_var_handler_obj=dynamic_variable_handler.DynamicVariables()
        self.constant_var_handler_obj=constant_variable_handler.ConstantVariables()
        self.status=TEST_RESULT_FAIL
        self.scenario_start_time=''
        self.scenario_end_time=''
        self.scenario_ellapsed_time=''
        self.reporting_obj=reporting.Reporting()
        self.conthread=None
        self.active_scheme=""
        self.change_power_option=""
        self.powerscheme_location=""
        self.one_power_option=False
        self.counter=[]
        self.jumpto_previousindex=[]
        self.verify_exists=False
        self.debug_mode=False
        self.debug_choice='Normal'
        self.last_tc_num=1
        self.debugfrom_step=1
        self.configvalues={}
        self.core_utilsobject = core_utils.CoreUtils()
        self.exception_flag=None
        local_cont.i = 0
        self.execution_mode = None
        self.runfrom_step_range_input=[]
        self.tc_name_list=[]
        self.constant_var_exists=False
        self.__load_generic()

    def __load_generic(self):
        try:
            if local_cont.generic_dispatcher_obj==None:
                core_utils.get_all_the_imports('Generic')
                core_utils.get_all_the_imports('IRIS')
                import generic_dispatcher
                local_cont.generic_dispatcher_obj = generic_dispatcher.GenericKeywordDispatcher()
        except Exception as e:
            logger.print_on_console('Error loading Generic plugin')
            log.error(e,exc_info=True)

    def __load_pdf(self):
        try:
            if self.pdf_dispatcher_obj==None:
                core_utils.get_all_the_imports('PDF')
                import pdf_dispatcher
                self.pdf_dispatcher_obj = pdf_dispatcher.PDFDispatcher()
        except Exception as e:
            logger.print_on_console('Error loading PDF plugin')
            log.error(e,exc_info=True)

    def __load_mobile_web(self):
        try:
            if self.mobile_web_dispatcher_obj==None:
                if SYSTEM_OS == 'Darwin':
                    core_utils.get_all_the_imports('Mobility/MobileWeb')
                    core_utils.get_all_the_imports('Saucelabs')
                else:
                    core_utils.get_all_the_imports('Mobility')
                    core_utils.get_all_the_imports('Saucelabs')
                import web_dispatcher_MW
                self.mobile_web_dispatcher_obj = web_dispatcher_MW.Dispatcher()
                self.mobile_web_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading MobileWeb plugin')
            log.error(e,exc_info=True)

    def __load_mobile_app(self):
        try:
            if self.mobile_app_dispatcher_obj==None:
                if SYSTEM_OS=='Darwin':
                    core_utils.get_all_the_imports('Mobility/MobileApp')
                    core_utils.get_all_the_imports('Mobility/iris_mobile')
                else:
                    core_utils.get_all_the_imports('Mobility')
                    core_utils.get_all_the_imports('Saucelabs')
                import mobile_app_dispatcher
                self.mobile_app_dispatcher_obj = mobile_app_dispatcher.MobileDispatcher()
                self.mobile_app_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading MobileApp plugin')
            log.error(e,exc_info=True)

    def __load_webservice(self):
        try:
            core_utils.get_all_the_imports('WebServices')
            import websevice_dispatcher
            self.webservice_dispatcher_obj = websevice_dispatcher.Dispatcher()
        except Exception as e:
            logger.print_on_console('Error loading Web services plugin')
            log.error(e)

    def __load_oebs(self):
        try:
            core_utils.get_all_the_imports('Oebs')
            core_utils.get_all_the_imports('IRIS')
            import oebs_dispatcher
            self.oebs_dispatcher_obj = oebs_dispatcher.OebsDispatcher()
            self.oebs_dispatcher_obj.exception_flag=self.exception_flag
            self.oebs_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading OEBS plugin')
            log.error(e)

    def __load_web(self):
        try:
            # core_utils.get_all_the_imports('ImageProcessing')
            core_utils.get_all_the_imports('WebScrape')
            core_utils.get_all_the_imports('Web')
            core_utils.get_all_the_imports('Saucelabs')
            core_utils.get_all_the_imports('Browserstack')
            core_utils.get_all_the_imports('IRIS')
            import web_dispatcher
            import web_accessibility_testing
            local_cont.web_dispatcher_obj = web_dispatcher.Dispatcher()
            local_cont.web_dispatcher_obj.exception_flag=self.exception_flag
            local_cont.web_dispatcher_obj.action=self.action
            local_cont.accessibility_testing_obj = web_accessibility_testing.Web_Accessibility_Testing()
        except Exception as e:
            logger.print_on_console('Error loading Web plugin')
            log.error(e)

    def __load_desktop(self):
        try:
            core_utils.get_all_the_imports('Desktop')
            core_utils.get_all_the_imports('IRIS')
            import desktop_dispatcher
            self.desktop_dispatcher_obj = desktop_dispatcher.DesktopDispatcher()
            self.desktop_dispatcher_obj.exception_flag=self.exception_flag
            self.desktop_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading Desktop plugin')
            log.error(e)

    def __load_sap(self):
        try:
            core_utils.get_all_the_imports('SAP')
            core_utils.get_all_the_imports('IRIS')
            import sap_dispatcher
            self.sap_dispatcher_obj = sap_dispatcher.SAPDispatcher()
            self.sap_dispatcher_obj.exception_flag=self.exception_flag
            self.sap_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading SAP plugin')
            log.error(e)

    def __load_mainframe(self):
        try:
            core_utils.get_all_the_imports('Mainframe')
            import mainframe_dispatcher
            self.mainframe_dispatcher_obj = mainframe_dispatcher.MainframeDispatcher()
            self.mainframe_dispatcher_obj.exception_flag=self.exception_flag
            self.mainframe_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading Mainframe plugin')
            log.error(e)

    def __load_system(self):
        try:
            core_utils.get_all_the_imports('System')
            import system_dispatcher
            self.system_dispatcher_obj = system_dispatcher.SystemDispatcher()
            self.system_dispatcher_obj.exception_flag=self.exception_flag
            self.system_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading System plugin')
            log.error(e,exc_info=True)


    def __load_aws(self):
        try:
            core_utils.get_all_the_imports('AWS/src')

        except Exception as e:
            logger.print_on_console('Error loading AWS plugin')
            log.error(e)
    def dangling_status(self,index):
        step=handler.local_handler.tspList[index]
        return step.executed

    def check_dangling(self,tsp,index):
        status=True
        errormsg=""
        if tsp.__class__.__name__.lower() in [IF,FOR,GETPARAM]:
            info_dict=tsp.info_dict
            if info_dict is not None:
                if tsp.name.lower() in [ENDFOR,ENDLOOP]:
                    index=list(info_dict[0].keys())[0]
                    status=self.dangling_status(index)
                if tsp.name.lower() in [IF,ELSE_IF,ELSE,ENDIF]:
                    if tsp.name.lower() in [IF]:
                        status= list(info_dict[-1].values())[0].lower() == ENDIF
                        if not(status):
                            errormsg="Execution Terminated : Dangling if/for/getparam in testcase"
                    elif tsp.name.lower() in [ELSE_IF,ELSE]:
                        status1= list(info_dict[-1].values())[0] == ENDIF
                        status2= list(info_dict[0].keys())[0] != index
                        status = status1 and status2
                        if not(status1) and status2:
                            errormsg="Execution Terminated : Dangling if/for/getparam in testcase"
                    elif tsp.name.lower() in [ENDIF]:
                        index=list(info_dict[-1].keys())[0]
                        status=self.dangling_status(index)
            else:
                status=False
                if tsp.name.lower() == FOR:
                    errormsg="Execution Terminated : Dangling if/for/getparam in testcase"
            if tsp.name.lower()==ENDLOOP and len(info_dict)<2:
                status=False
        if not(status) and len(errormsg)>0:
            logger.print_on_console(errormsg+' in '+tsp.testscript_name+'\n')
            log.error(errormsg+' in '+tsp.testscript_name)
        elif not(status):
            logger.print_on_console('Dangling: '+tsp.name +' in '+tsp.testscript_name+'\n')
            log.error('Dangling: '+tsp.name +' in '+tsp.testscript_name)
        return status

    def __print_details(self,tsp,input,inpval):
        keyowrd='Keyword : '+tsp.name
        input_val='Input :'+str(input)
        output='Output :'+tsp.outputval
        apptype='Apptype : '+str(tsp.apptype)
        log.info(keyowrd)
        log.info(input_val)
        log.info(output)
        log.info(apptype)
        for i in range(len(inpval)):
            log.info('Input: '+str(i + 1)+ '= '+repr(inpval[i]))

    def clear_data(self):
        global terminate_flag,manual_terminate_flag,pause_flag,iris_constant_step
        terminate_flag=manual_terminate_flag=pause_flag=False
        iris_constant_step = -1

    def resume_execution(self):
        global pause_flag
        logger.print_on_console('=======Resuming=======')
        log.info('=======Resuming=======')
        self.conthread.paused = False
        pause_flag=False
        # Notify so thread will wake after lock released
        try:
            self.conthread.pause_cond.notify()
            # Now release the lock
            self.conthread.pause_cond.release()
        except Exception as e:
            log.error('Debug is not paused to Resume')
            logger.print_on_console('Debug is not paused to Resume')
            log.error(e)

    def pause_execution(self):
        logger.print_on_console('=======Pausing=======')
        log.info('=======Pausing=======')
        self.conthread.paused=True
        self.conthread.pause_cond.acquire()
        with self.conthread.pause_cond:
            while self.conthread.paused:
                self.conthread.pause_cond.wait()


    def methodinvocation(self,index,execution_env,datatables=[],execute_result_data={},*args):
        global pause_flag
        result=(TEST_RESULT_FAIL,TEST_RESULT_FALSE,OUTPUT_CONSTANT,None)
		#COmapring breakpoint with the step number of tsp instead of index - (Sushma)
        tsp = handler.local_handler.tspList[index]
        testcase_details_orig=tsp.testcase_details
        if local_cont.test_case_number != tsp.testcase_num and tsp.testscript_name:
            local_cont.test_case_number = tsp.testcase_num
            log.info('---------------------------------------------------------------------')
            print('-------------------------------------------------------------------------------------------------------')
            logger.print_on_console('***Test case name: '+str(tsp.testscript_name)+'***')
            log.info('***Test case name: '+str(tsp.testscript_name)+'***')
            print('-------------------------------------------------------------------------------------------------------')
            log.info('---------------------------------------------------------------------')
        #logic to handle step by step debug
        if self.debug_mode and tsp.testcase_num==self.last_tc_num:
            #logic to handle run from setp debug
            if self.debug_choice=='RunfromStep' and self.debugfrom_step>0 and tsp.stepnum < self.debugfrom_step :
                return index +1
            pause_flag=True
        keyword_flag=True
        ignore_stat=False
        inpval=[]
        start_time = datetime.now()
        #Check for 'terminate_flag' before execution
        if not(terminate_flag):
            #Check for 'pause_flag' before executionee
            if pause_flag:
                self.pause_execution()
            if(self.check_dangling(tsp,index)):
                input = tsp.inputval[0]
                #Logic to split input and handle dynamic variables
                rawinput = tsp.inputval
                if len(args) > 0:
                    rawinput = args[0]
                inpval,ignore_stat=self.split_input(rawinput,tsp.name)
                if tsp.name.lower() not in [FOR,ENDFOR] :
                    #Print the details of keyword
                    self.__print_details(tsp,input,inpval)
                #Calculating Start time
                logger.print_on_console('Step number is : ',str(tsp.stepnum))
                log.info('Step number is : '+str(tsp.stepnum))
                if ignore_stat:
                    teststepproperty = handler.local_handler.tspList[index]
                    keyword=teststepproperty.name
                    logger.print_on_console('Step Skipped : Encountered ignore step instruction for the keyword : ',keyword)
                    index=index+1
                else:
                    if tsp != None and isinstance(tsp,TestStepProperty) :
                        log.info( "----Keyword :"+str(tsp.name)+' execution Started----')
                        start_time = datetime.now()
                        start_time_string=start_time.strftime(TIME_FORMAT)
                        log.info('Step Execution start time is : '+start_time_string)
                        index,result = self.keywordinvocation(index,inpval,self.reporting_obj,execution_env,*args)
                    else:
                        keyword_flag=False
                        start_time = datetime.now()
                        if len(tsp.inputval[0].strip())==0 and tsp.name.lower().strip() in [IF,ELSE_IF,FOR,GETPARAM]:
                            logger.print_on_console('Input value for '+tsp.name+' cannot be empty')
                            index = TERMINATE
                        else:
                            if tsp != None and isinstance(tsp,if_step.If):
                                index = tsp.invoke_condtional_keyword(inpval,self.reporting_obj)
                            elif tsp != None and isinstance(tsp,for_step.For):
                                index = tsp.invokeFor(inpval,self.reporting_obj)
                            elif tsp != None and isinstance(tsp,getparam.GetParam):
                                index = tsp.performdataparam(inpval,self,self.reporting_obj,execution_env,datatables)
                            elif tsp != None and isinstance(tsp,jumpBy.JumpBy):
                                index = tsp.invoke_jumpby(inpval,self.reporting_obj)
                            elif tsp != None and isinstance(tsp,jumpTo.JumpTo):
                                self.jumpto_previousindex.append(index+1)
                                index,counter = tsp.invoke_jumpto(inpval,self.reporting_obj,self.counter)
                                self.counter.append(counter)
            else:
                index= TERMINATE
                self.status=index
        else:
            index= TERMINATE
            self.status=index
        ellapsed_time=''
        statusflag = self.step_execution_status(tsp)
        if tsp.name.lower() == "getparam" and tsp.step_description.lower() == DATA_PARAMETERIZATION_FAILED:
            self.reporting_obj.overallstatus = TEST_RESULT_FAIL
            status_percentage["total"] += 2
            status_percentage["Fail"] += 2
        if ignore_stat:
            statusflag=True
        if keyword_flag:
            end_time = datetime.now()
            end_time_string=end_time.strftime(TIME_FORMAT)
            log.info('Step Execution end time is : '+end_time_string)
            ellapsed_time=end_time-start_time
            log.info('Step Elapsed time is : '+str(ellapsed_time)+"\n")
            #Changing the overallstatus of the scenario if it's Fail or Terminate
            if self.status == TEST_RESULT_FAIL :
                if not statusflag:
                    self.reporting_obj.overallstatus=self.status
            elif self.status == TERMINATE:
                self.reporting_obj.overallstatus=self.status
        if self.action==EXECUTE:
            # self.reporting_obj.generate_report_step(tsp,self.status,tsp.name+' EXECUTED and the result is  '+self.status,ellapsed_time,keyword_flag,result[3])
            if statusflag:
                # self.reporting_obj.generate_report_step(tsp,'',self,ellapsed_time,keyword_flag,result,ignore_stat,inpval)
                #added value to store ids in reportitem collection
                self.reporting_obj.generate_report_step(tsp,'',self,ellapsed_time,keyword_flag,result,ignore_stat,inpval,execute_result_data=execute_result_data)
            else:
                # self.reporting_obj.generate_report_step(tsp,self.status,self,ellapsed_time,keyword_flag,result,ignore_stat,inpval)
                self.reporting_obj.generate_report_step(tsp,self.status,self,ellapsed_time,keyword_flag,result,ignore_stat,inpval,execute_result_data=execute_result_data)
            if tsp.name.lower()=='verifyvalues' or tsp.name.lower()=='verifytextiris':
                tsp.testcase_details=testcase_details_orig

        # Issue #160
        if index==STOP:
            return index
        if len(self.counter)>0 and self.counter[-1]>-1 and self.counter[-1]-index==0:
            return JUMP_TO
        return index

    def split_input(self,input,keyword):
        ignore_status = False
        const_var=False
        inpval = []
        input_list = input[0].split(SEMICOLON)
        if IGNORE_THIS_STEP in input_list:
            ignore_status=True
        if keyword.lower() in [IF,ELSE_IF,EVALUATE]:
            inpval=self.dynamic_var_handler_obj.simplify_expression(input,keyword,self)
        elif keyword.lower() in CONSTANT_KEYWORDS:
            if STATIC_NONE in input[0]:
                input[0]=input[0].replace(STATIC_NONE,'')
            string=input[0]
            index=string.find(';')
            if index >-1:
                inpval.append(string[0:index])
                inpval.append(string[index+1:len(string)])
            elif string != '':
                inpval.append(string)
            if keyword.lower() == CREATE_CONST_VARIABLE and len(inpval)>1:
                #createConstVariable ex: _a_;{a}
                const_var=self.constant_var_handler_obj.check_for_constantvariables(inpval[1])
                if const_var!=TEST_RESULT_TRUE:
                    #check if the inputval[1] is constant variable or not,
                    #createConstVariable ex: _a_;{a}
                    inpval[1]=self.dynamic_var_handler_obj.replace_dynamic_variable(inpval[1],'',self)
                else:
                    #createConstVariable ex: _a_;_b_  (_b_ is already created)
                    inpval[1]=self.constant_var_handler_obj.get_constant_value(inpval[1])
        elif keyword.lower() in DYNAMIC_KEYWORDS:
            if STATIC_NONE in input[0]:
                input[0]=input[0].replace(STATIC_NONE,'')
            string=input[0]
            index=string.find(';')
            if index >-1:
                inpval.append(string[0:index])
                inpval.append(string[index+1:len(string)])
            elif string != '':
                inpval.append(string)
            if keyword.lower() != CREATE_DYN_VARIABLE:
                const_var=self.constant_var_handler_obj.check_for_constantvariables(inpval[0])
                #check if the inputval[0] is constant variable or not,
                #ex: COPY_VALUE->_a_;{a}
                if const_var!=TEST_RESULT_TRUE:
                    inpval[0]=self.dynamic_var_handler_obj.replace_dynamic_variable(inpval[0],keyword,self)
            if len(inpval)>1 and keyword.lower() in [COPY_VALUE,MODIFY_VALUE,CREATE_DYN_VARIABLE]:
                exch = keyword.lower() == COPY_VALUE
                const_var=self.constant_var_handler_obj.check_for_constantvariables(inpval[1])
                if const_var==TEST_RESULT_TRUE:
                    #to get the value of constantVarible,
                    inpval[1]=self.constant_var_handler_obj.get_constant_value(inpval[1])
                inpval[1]=self.dynamic_var_handler_obj.replace_dynamic_variable(inpval[1],'',self,no_exch_val=exch)
        else:
            if keyword.lower() in WS_KEYWORDS or keyword.lower() == 'navigatetourl':
                input_list=[input[0]]
            for x in input_list:
                if STATIC_NONE in x:
                    x=None
                else:
                    # To Handle dynamic variables of DB keywords,controller object is sent to dynamicVariableHandler
                    const_var=self.constant_var_handler_obj.check_for_constantvariables(x)
                    #to get the value of constantVariable, ex:displayVariableValue
                    if const_var==TEST_RESULT_TRUE:
                        #ex:displayVariableValue _a_
                        x=self.constant_var_handler_obj.get_constant_value(x)
                    else:
                        x=self.dynamic_var_handler_obj.replace_dynamic_variable(x,keyword,self)
                inpval.append(x)
        return inpval,ignore_status

    def store_result(self,result_temp,tsp):
        output=tsp.outputval.split(SEMICOLON)
        result=result_temp
        if len(result)>4:
            result=result_temp[0:-1]
        keyword_response=result[-2]
        if result[-2] == OUTPUT_CONSTANT:
            keyword_response=result[-3]
        display_keyword_response=keyword_response
        if len(result_temp)>4:
            tsp.additionalinfo=result_temp[-1]
        elif result_temp[2] != OUTPUT_CONSTANT:
            tsp.additionalinfo=result_temp[2]
            display_keyword_response=result_temp[2]
        if tsp.name.lower()=='verifyvalues':
            display_keyword_response=[result[1]]
        elif tsp.name.lower()=='verifytextiris':
            display_keyword_response=result[1]
        elif tsp.name.lower()=='find':
            keyword_response=result[1]
		#To Handle dynamic variables of DB keywords
        if tsp.name.lower() in DATABASE_KEYWORDS:
            if keyword_response != []:
                display_keyword_response='DB data fetched'
        if(tsp.apptype.lower() == 'webservice' and tsp.name.lower() == 'executerequest'):
            if len(display_keyword_response) == 2:
                logger.print_on_console('Response Header: \n',display_keyword_response[0])
                #data size check
                if self.core_utilsobject.getdatasize(display_keyword_response[1],'mb') < 10:
                    from bs4 import BeautifulSoup
                    if 'soap:Envelope' in display_keyword_response[1]:
                        #root = BeautifulSoup(display_keyword_response[1][2:-1], "xml").prettify()
                        root = BeautifulSoup(display_keyword_response[1], "xml").prettify()
                        respBody = root.replace("\n",' ')
                        logger.print_on_console('Response Body: \n',respBody,'\n')
                    else:
                        logger.print_on_console('NON SOAP XML')
                        logger.print_on_console('Response Body: \n',display_keyword_response[1].replace("\\n","\n").replace("\\r","\r").replace("\\t","\t"),'\n')
                        #logger.print_on_console('Response Body: \n',display_keyword_response[1][2:-1].replace("\\n","\n").replace("\\r","\r").replace("\\t","\t"),'\n')
                else:
                    logger.print_on_console('Response Body exceeds max. Limit, please use writeToFile keyword.')
                    log.info('Result obtained is: ')
                    log.info(display_keyword_response)
            elif(len(display_keyword_response) == 1):
                logger.print_on_console('Response Header: ',display_keyword_response[0])
            else:
                #data size check
                if self.core_utilsobject.getdatasize(display_keyword_response,'mb') < 10:
                    if not isinstance(display_keyword_response,list):
                        logger.print_on_console('Result obtained is ',display_keyword_response)
                    else:
                        logger.print_on_console('Result obtained is ',",".join([str(display_keyword_response[local_cont.i])
                        if not isinstance(display_keyword_response[local_cont.i],str) else display_keyword_response[local_cont.i] for local_cont.i in range(len(display_keyword_response))]))
                else:
                    logger.print_on_console('Result obtained exceeds max. Limit, please use writeToFile keyword.')
        else:
            #data size check
            if self.core_utilsobject.getdatasize(display_keyword_response,'mb') < 10:
                if not isinstance(display_keyword_response,list):
                    if tsp.name.lower() == 'getindexcount':
                        if '@' in str(display_keyword_response):
                            row,col=display_keyword_response.split('@')
                            logger.print_on_console("The index count for the dynamic variable is " + "Row: "+str(row) + " and Column: "+str(col))
                        else:
                            logger.print_on_console('Result obtained is ',display_keyword_response)
                    elif tsp.apptype.lower()=='system':
                        if result[2]!=OUTPUT_CONSTANT :
                            logger.print_on_console('Result obtained is: ',result[2])
                        elif result:
                            logger.print_on_console('Result obtained is: ',result[1])
                    elif tsp.name.lower() == "find":
                        logger.print_on_console('Result obtained is: ',result[2])
                else:
                    if tsp.apptype.lower()=='system':
                        if result[2]!=OUTPUT_CONSTANT :
                            logger.print_on_console('Result obtained is: ',result[2])
                        elif result:
                            logger.print_on_console('Result obtained is: ',result[1])
                    else:
                        keyword_lower = tsp.name.lower()
                        #list containing keywords that should not print output on console, add keyword here to stop printing
                        #Fix for #17330 Addition of getAllValues in exception_list
                        exception_list = ['getxmlblockdata','findimageinpdf','comparepdfs','getallvalues','getcontent']
                        if (tsp.apptype.lower()!='desktop' and keyword_lower not in exception_list) : logger.print_on_console('Result obtained is ',",".join([str(display_keyword_response[local_cont.i])
                        if not isinstance(display_keyword_response[local_cont.i],str) else display_keyword_response[local_cont.i] for local_cont.i in range(len(display_keyword_response))]))
            else:
                logger.print_on_console('Result obtained exceeds max. Limit, please use writeToFile keyword.')
        log.info('Result obtained is: '+str(display_keyword_response))
        if tsp.apptype.lower()=='desktop' or tsp.apptype.lower()=='sap' or tsp.apptype.lower()=='oebs' or (tsp.cord!='' and tsp.cord!=None):
            if result[2]!='9cc33d6fe25973868b30f4439f09901a' and tsp.name.lower()!='verifytextiris':
                logger.print_on_console('Result obtained is: ',result[2])
            elif result:
                logger.print_on_console('Result obtained is: ',result[1])
        if tsp.apptype.lower()=='generic' and (tsp.name.lower()=='savetoclipboard' or tsp.name.lower()=='getfromclipboard' or tsp.name.lower() == 'getkeystatus'):
            if result[2]!='9cc33d6fe25973868b30f4439f09901a':
                logger.print_on_console('Result obtained is: ',result[2])
            elif result:
                logger.print_on_console('Result obtained is: ',result[1])
        if tsp.name.lower()=='find':
            keyword_response=result[1]
            result = result[:1] + (result[2],) + result[2:]
        if len(output)>0 and output[0] != '':
            const_var=self.constant_var_handler_obj.check_for_constantvariables(output[0])
            #checks if the output variable is a constant variable or not
            if const_var==TEST_RESULT_TRUE:
                if output[0] in constant_variable_handler.local_constant.constant_variable_map:
                    #checks if the output variable(constant variable) is assigned with a value
                    if tsp.name in FILEPATH_OUTPUT_FIELD_KEYWORDS:
                        cosnt_val=constant_variable_handler.local_constant.constant_variable_map[output[0]]
                        file_path = cosnt_val.split(";")[0]
                        if not(os.path.exists(file_path)):
                            self.constant_var_exists=True
                            err_msg="Error: Constant variable cannot be modified!"
                            logger.print_on_console(err_msg)
                            log.debug(err_msg)
                    else:
                        self.constant_var_exists=True
                        err_msg="Error: Constant variable cannot be modified!"
                        logger.print_on_console(err_msg)
                        log.debug(err_msg)
                else:
                    #in the current step if _a_ is used in output and _a_ is not created, then _a_ should be created and the response of the keyword should be written to _a_
                    self.constant_var_handler_obj.store_constant_value(output[0],keyword_response,tsp.name)
            else:
                self.dynamic_var_handler_obj.store_dynamic_value(output[0],keyword_response,tsp.name)
        if len(output)>1:
            self.dynamic_var_handler_obj.store_dynamic_value(output[1],result[1],tsp.name)

    def keywordinvocation(self,index,inpval,*args):
        global socket_object, iris_constant_step, status_percentage
        self.constant_var_exists=False
        configvalues = self.configvalues
        try:
            time.sleep(float(configvalues['stepExecutionWait']))
        except Exception as e:
            log.error('stepExecutionWait should be a integer, please change it in config.json')
            logger.print_on_console('stepExecutionWait should be a integer, please change it in config.json')
            log.error(e)
        result=(TEST_RESULT_FAIL,TEST_RESULT_FALSE,OUTPUT_CONSTANT,None)
        #Check for 'terminate_flag' before execution
        if not(terminate_flag):
            #Check for 'pause_flag' before execution
            if pause_flag:
                self.pause_execution()
            teststepproperty = handler.local_handler.tspList[index]
            keyword=teststepproperty.name
            #Custom object implementation for Web
            if teststepproperty.objectname==CUSTOM:
                if self.verify_exists==False:
                    previous_step=handler.local_handler.tspList[index-1]
                    apptype=previous_step.apptype.lower()
                    if  apptype in self.verify_dict and previous_step.name.lower()==self.verify_dict[apptype]:
                        self.previous_step=previous_step
                        teststepproperty.custom_flag=True
                        self.verify_exists=True
                    else:
                        apptype=teststepproperty.apptype.lower()
                        logger.print_on_console('ERR_CUSTOM_VERIFYEXISTS: Previous step ',self.verify_dict[apptype],' is missing')
                if self.verify_exists==True:
                    teststepproperty.custom_flag=True
                    teststepproperty.parent_xpath=self.previous_step.objectname
                    teststepproperty.url=self.previous_step.url
            #Fixed OEBS custom reference defect #398
            elif keyword.lower() in [VERIFY_EXISTS,VERIFY_VISIBLE] and self.verify_exists:
                self.verify_exists=False
            #Checking of  Drag and Drop keyowrds Issue #115 in Git
            if teststepproperty.name.lower()==DROP:
                log.debug('Drop keyword encountered')
                teststepproperty_prev = handler.local_handler.tspList[index-1]
                if teststepproperty_prev.name.lower()!=DRAG:
                    teststepproperty.execute_flag=False
                    result=list(result)
                    result[3]='Drag Keyword is missing'
            elif keyword.lower()==DRAG:
                log.debug('Drag keyword encountered')
                if(index+1)<len(handler.local_handler.tspList):
                    teststepproperty_next = handler.local_handler.tspList[index+1]
                    if teststepproperty_next.name.lower()!=DROP:
                        teststepproperty.execute_flag=False
                        result=list(result)
                        result[3]='Drop Keyword is missing'
            #Checking for test step with constant iris object
            if(teststepproperty.cord != '' and teststepproperty.cord != None):
                if (teststepproperty.objectname.split(';')[-1] == 'constant' and keyword.lower() == 'verifyexistsiris'):
                    iris_constant_step = index
                elif iris_constant_step!=-1:
                    tsp = handler.local_handler.tspList[iris_constant_step]
                    obj_props = tsp.objectname.split(';')
                    coords = [obj_props[2],obj_props[3],obj_props[4],obj_props[5]]
                    teststepproperty.custom_flag = True
                    teststepproperty.parent_xpath = {'cord': tsp.cord, 'coordinates': coords}
            #get the output varible from the teststep property
            if teststepproperty.execute_flag:
                #Check the apptype and pass to perticular module
                if teststepproperty.apptype.lower() == APPTYPE_GENERIC:
                    #Generic apptype module call

                    if local_cont.generic_dispatcher_obj == None:
                        self.__load_generic()
                    result = self.invokegenerickeyword(teststepproperty,local_cont.generic_dispatcher_obj,inpval)

                elif teststepproperty.apptype.lower() == APPTYPE_SYSTEM:
                    #System apptype module call
                    if self.system_dispatcher_obj == None:
                        self.__load_system()
                    result = self.invokesystemkeyword(teststepproperty,self.system_dispatcher_obj,inpval)

                elif teststepproperty.apptype.lower() == APPTYPE_WEB:
                    #Web apptype module call
                    if local_cont.web_dispatcher_obj == None:
                        self.__load_web()
                    result = self.invokewebkeyword(teststepproperty,local_cont.web_dispatcher_obj,inpval,args[0],args[1])
                elif teststepproperty.apptype.lower() == APPTYPE_MOBILE:
                    #MobileWeb apptype module call
                    if self.mobile_web_dispatcher_obj == None:
                        self.__load_mobile_web()
                    result = self.invokemobilekeyword(teststepproperty,self.mobile_web_dispatcher_obj,inpval,args[0],args[1])
                elif teststepproperty.apptype.lower() == APPTYPE_MOBILE_APP:
                    #MobileApp apptype module call
                    if self.mobile_app_dispatcher_obj==None:
                        self.__load_mobile_app()
                    result = self.invokemobileappkeyword(teststepproperty,self.mobile_app_dispatcher_obj,inpval,args[0],args[1])
                elif teststepproperty.apptype.lower() == APPTYPE_WEBSERVICE:
                    #Webservice apptype module call
                    if self.webservice_dispatcher_obj == None:
                        self.__load_webservice()
                    result = self.invokewebservicekeyword(teststepproperty,self.webservice_dispatcher_obj,inpval,socket_object)
                elif teststepproperty.apptype.lower() == APPTYPE_DESKTOP:
                    #Desktop apptype module call
                    if self.desktop_dispatcher_obj == None:
                        self.__load_desktop()
                    result = self.invokeDesktopkeyword(teststepproperty,self.desktop_dispatcher_obj,inpval)
                    #----------------------------------------------------------------------------------------------SAP change
                elif teststepproperty.apptype.lower() == APPTYPE_SAP:
                    #SAP apptype module call
                    if self.sap_dispatcher_obj == None:
                        self.__load_sap()
                    result = self.invokeSAPkeyword(teststepproperty,self.sap_dispatcher_obj,inpval)
                #----------------------------------------------------------------------------------------------SAP change
                elif teststepproperty.apptype.lower() == APPTYPE_DESKTOP_JAVA:
                    #OEBS apptype module call
                    if self.oebs_dispatcher_obj == None:
                        self.__load_oebs()
                    result = self.invokeoebskeyword(teststepproperty,self.oebs_dispatcher_obj,inpval)
            #----------------------------------------------------------------------------------------------Mainframe change
                elif teststepproperty.apptype.lower() == APPTYPE_MAINFRAME:
                    #Mainframe apptype module call
                    if self.mainframe_dispatcher_obj == None:
                        self.__load_mainframe()
                    result = self.invokemainframekeyword(teststepproperty,self.mainframe_dispatcher_obj,inpval)
                #----------------------------------------------------------------------------------------------Mainframe change
                elif teststepproperty.apptype.lower() == APPTYPE_PDF:
                    #pdf apptype module call
                    if self.pdf_dispatcher_obj == None:
                        self.__load_pdf()
                    result = self.invokepdfkeyword(teststepproperty,self.pdf_dispatcher_obj,inpval)
			#Fixed issue num #389 (Taiga)
            temp_result=result
            if result!=TERMINATE:
                temp_result=list(result)
                if  len(temp_result)>2 and temp_result[2]==OUTPUT_CONSTANT:
                    temp_result[2]=None
                if len(temp_result)>4:
                    temp_result=temp_result[0:-1]
            if pause_flag:
                self.pause_execution()
            # logger.print_on_console( 'Result in methodinvocation : ', teststepproperty.name,' : ',temp_result)
            log.info('Result in methodinvocation : '+ str(teststepproperty.name)+' : ')
            if keyword != 'secureGetData':
                log.info(result)
            self.keyword_status=TEST_RESULT_FAIL
            if result!=TERMINATE:
                self.store_result(result,teststepproperty)
                if self.constant_var_exists:
                    #if the output variable(constant variable) is assigned with a value and still constantVariable is used in output
                    temp_re=list(result)
                    temp_re[0]=TEST_RESULT_FAIL
                    temp_re[1]=TEST_RESULT_FALSE
                    result=tuple(temp_re)
                self.status=result[0]
                index+=1
                self.keyword_status=self.status
            else:
                index=result
                self.status=result
            #Fixing issue #382
            if teststepproperty.outputval.split(";")[-1].strip() != STEPSTATUS_INREPORTS_ZERO:
                status_percentage[self.keyword_status]+=1
                status_percentage["total"]+=1
            kwargs = {}
            if(self.keyword_status=='Pass'): kwargs["setcolor"]="GREEN"
            elif(self.keyword_status=='Fail') : kwargs["setcolor"]="RED"
            keyword = str(teststepproperty.name)
            cicd_mode = cicd_core.iscicd
            if cicd_mode and keyword == 'displayVariableValue':
                logger.print_on_console(keyword +':  '+ teststepproperty.additionalinfo, **kwargs)
                logger.print_on_console(keyword +' executed and the status is Pass' + '\n', **kwargs)
                log.info(keyword +':  '+ teststepproperty.additionalinfo)
                log.info(keyword +' executed and the status is pass'+'\n')
            else:
                logger.print_on_console(keyword+' executed and the status is '+self.keyword_status+'\n',**kwargs)
                log.info(keyword+' executed and the status is '+self.keyword_status+'\n')
            #Checking for stop keyword
            # CR #22650 stop keyword enhancement
            # 1. when input is 'testcase' stop the current testcase execution and jump to next teststep of next testcase.
            #    1.a :  assign index to prev_index and reduce the index value as its incremented already
            #    1.b : Find the starting index of next testcase and assign it to index by checking testcase_name
            #    1.b : if index+1 hasnt changed implies that there are no further testcase in that scenario. so make index= STOP
            # 2. when input is 'module' stop the current module and move to next module if its batch execution.
            #   2.a : set module_stop=True. which asks to stop looping through the scenarios of the current module and move to next module if present
            # 3. when input is 'scenario' assign STOP to index and stop the sceanrio execution and move to next scenario if present
            if teststepproperty.name.lower() == STOP and self.status == 'Pass':
                ## Issue #160
                # index = STOP
                if self.action.lower() == 'debug':
                    index = STOP
                else:
                    if teststepproperty.inputval[0].lower() == 'testcase':
                        prev_index = index
                        index -= 1
                        teststepproperty_name = teststepproperty.testscript_name
                        for i in range(index, len(handler.local_handler.tspList)):
                            if teststepproperty_name != handler.local_handler.tspList[i].testscript_name:
                                index = handler.local_handler.tspList[i].index
                                break
                        if (index + 1) == prev_index:
                            index = STOP
                    elif teststepproperty.inputval[0].lower() == 'module':
                        local_cont.module_stop = True
                        index = STOP
                    else:
                        index = STOP
            return index,result
        else:
            return index,TERMINATE

    def executor(self,tsplist,action,last_tc_num,debugfrom_step,mythread,execution_env,*args,datatables=[], accessibility_testing = False,execute_result_data={}):
        global status_percentage, screen_testcase_map
        status_percentage = {TEST_RESULT_PASS:0,TEST_RESULT_FAIL:0,TERMINATE:0,"total":0}
        i=0
        status=True
        accessibility_reports = []
        self.scenario_start_time=datetime.now()
        start_time_string=self.scenario_start_time.strftime(TIME_FORMAT)
        logger.print_on_console('Scenario Execution start time is : '+start_time_string,'\n')
        global pause_flag
        if(action != DEBUG):
            hn = execution_env['handlerno']
            log.root.handlers[hn].createTspObj(execution_env['scenario_id'],execution_env['browser'])
        if local_cont.generic_dispatcher_obj is not None and local_cont.generic_dispatcher_obj.action is None:
            local_cont.generic_dispatcher_obj.action=action
        #Check for 'run from step' with range as input
        last_step_val = len(tsplist)
        if self.runfrom_step_range_input:
            last_step_val=self.runfrom_step_range_input[-1]
        while (i < len(tsplist)):
            #Check for 'terminate_flag' before execution
            if not(terminate_flag):
                if tsplist[i].testcase_num == last_tc_num:
                    if mythread.cw and mythread.cw.debugwindow is not None:
                        wx.CallAfter(mythread.cw.debugwindow.Show)
                    if self.runfrom_step_range_input:
                        #checks if the current step num is greater than ending range of run from step, to Run till the ending range of run from step
                        if tsplist[i].stepnum > last_step_val: break
                #Check for 'pause_flag' before execution
                if pause_flag:
                    self.pause_execution()
                self.last_tc_num=last_tc_num
                self.debugfrom_step=debugfrom_step
                try:
                    index = i
                    # if(action != DEBUG):    
                    #     log.root.handlers[hn].starttsp(tsplist[index],execution_env['scenario_id'],execution_env['browser'])
                    
                    # Added data to insert ids in the reportitem collection
                    # i = self.methodinvocation(i,execution_env,datatables)
                    i = self.methodinvocation(i,execution_env,datatables,execute_result_data=execute_result_data)
                    # if(action != DEBUG):
                    #     log.root.handlers[hn].stoptsp(tsplist[index],execution_env['scenario_id'],execution_env['browser'])
                    #Check wether accessibility testing has to be executed
                    if accessibility_testing and (index + 1 >= len(tsplist) or (tsplist[index].testscript_name != tsplist[index + 1].testscript_name and screen_testcase_map[tsplist[index].testscript_name]['screenid'] != screen_testcase_map[tsplist[index + 1].testscript_name]['screenid'])):
                        if local_cont.accessibility_testing_obj is None: self.__load_web()
                        import browser_Keywords
                        script_info =  screen_testcase_map[tsplist[index].testscript_name]
                        #Check if browser is present or not
                        if hasattr(browser_Keywords.local_bk, 'driver_obj') and browser_Keywords.local_bk.driver_obj is not None and len(script_info['accessibility_parameters']) > 0:
                            acc_result = local_cont.accessibility_testing_obj.runCrawler(browser_Keywords.local_bk.driver_obj, script_info, screen_testcase_map["executionid"], index)
                            #Check if accessibility Testing was successful
                            if acc_result and acc_result["status"] != "fail":
                                accessibility_reports.append(acc_result)
                    if i == TERMINATE:
                        #Changing the overallstatus of the report_obj to Terminate - (Sushma)
                        self.reporting_obj.overallstatus=TERMINATE
                        status_percentage[TERMINATE]+=1
                        status_percentage["total"]+=1
                        logger.print_on_console('Terminating the execution',color="YELLOW")
                        status=i
                        break
                    ## Issue #160
                    elif i==STOP:
                        log.info('Encountered STOP keyword')
                        break
                    elif i==JUMP_TO:
                        i=self.jumpto_previousindex[-1]
                        if len(self.jumpto_previousindex)>0 and len(self.counter)>0:
                            self.jumpto_previousindex.pop()
                            self.counter.pop()
                except Exception as e:
                    log.error(e,exc_info=True)
                    logger.print_on_console("Error encountered during Execution")
                    status=False
                    i=i+1
            else:
                logger.print_on_console('Terminating the execution',color="YELLOW")
                #Changing the overallstatus of the report_obj to Terminate - (Sushma)
                self.reporting_obj.overallstatus=TERMINATE
                status=TERMINATE
                break
        self.scenario_end_time=datetime.now()
        end_time_string=self.scenario_end_time.strftime(TIME_FORMAT)
        logger.print_on_console('Scenario Execution end time is : '+end_time_string)
        self.scenario_ellapsed_time=self.scenario_end_time-self.scenario_start_time
        if terminate_flag:
            #Indication of user_termination to report_obj to add a proper description in report - (Sushma)
            self.reporting_obj.user_termination=True
            status_percentage[TERMINATE]+=1
            status_percentage["total"]+=1
        ##send path to build overall status
        video_path = args[0] if (args and args[0]) else ''
        self.reporting_obj.build_overallstatus(self.scenario_start_time,self.scenario_end_time,self.scenario_ellapsed_time,video_path)
        logger.print_on_console('Step Elapsed time is : ',str(self.scenario_ellapsed_time))
        return status,status_percentage,accessibility_reports

    def invokegenerickeyword(self,teststepproperty,dispatcher_obj,inputval):
        res = dispatcher_obj.dispatcher(teststepproperty,self.wx_object,self.conthread,*inputval)
        return res

    def invokesystemkeyword(self,teststepproperty,dispatcher_obj,inputval):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval)
        return res

    def invokeoebskeyword(self,teststepproperty,dispatcher_obj,inputval):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.conthread)
        return res

    def invokewebservicekeyword(self,teststepproperty,dispatcher_obj,inputval,socket_object):
        keyword = teststepproperty.name
        if keyword.lower() == 'settagvalue' or keyword.lower() == 'settagattribute':
            if teststepproperty.testscript_name in handler.local_handler.ws_templates_dict:
                handler.local_handler.ws_template=handler.local_handler.ws_templates_dict[teststepproperty.testscript_name]
            else:
                handler.local_handler.ws_template=''
        res = dispatcher_obj.dispatcher(teststepproperty,socket_object,*inputval)
        return res

    def invokewebkeyword(self,teststepproperty,dispatcher_obj,inputval,reporting_obj,execution_env):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.reporting_obj,self.wx_object,self.conthread,execution_env)
        # To Retry on driver exception
        if (res[3] == ERROR_CODE_DICT['ERR_WEB_DRIVER_EXCEPTION']) and (res[1] == 'False'):
            log.info('Retry on Driver Exception')
            res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.reporting_obj,self.wx_object,self.conthread,execution_env)
            log.info('Retry on Driver Exception Done!')
        return res

    def invokemobilekeyword(self,teststepproperty,dispatcher_obj,inputval,reporting_obj,execution_env):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.reporting_obj,self.conthread,execution_env)
        return res

    def invokemobileappkeyword(self,teststepproperty,dispatcher_obj,inputval,reporting_obj,execution_env):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.reporting_obj,self.conthread,execution_env)
        return res

    def invokeDesktopkeyword(self,teststepproperty,dispatcher_obj,inputval):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.conthread)
        return res

    def invokeSAPkeyword(self,teststepproperty,dispatcher_obj,inputval):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.conthread)
        return res

    def invokemainframekeyword(self,teststepproperty,dispatcher_obj,inputval):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.conthread)
        return res

    def invokepdfkeyword(self, teststepproperty, dispatcher_obj,inputval):
        res = dispatcher_obj.dispatcher(teststepproperty, inputval)
        return res

    def invoke_debug(self,mythread,runfrom_step,json_data):
        status=COMPLETED
        obj = handler.Handler()
        self.action=DEBUG
        handler.local_handler.tspList=[]
        scenario=[json_data]
        print('=======================================================================================================')
        log.info('***DEBUG STARTED***')
        logger.print_on_console('***DEBUG STARTED***')
        print('=======================================================================================================')
        if mythread.cw and mythread.cw.debugwindow is not None:
            wx.CallAfter(mythread.cw.debugwindow.Hide)
        for testcase in scenario:
            flag,browser_type,last_tc_num,datatables,_,_=obj.parse_json(testcase)
            if flag == False:
                break
            print('\n')
            tsplist = obj.read_step()
            for k in range(len(tsplist)):
                if tsplist[k].apptype.lower()=='web':
                    tsplist[k].browser_type = browser_type
                    if tsplist[k].name.lower() == 'openbrowser' and (IGNORE_THIS_STEP not in tsplist[k].inputval[0].split(';')):
                        tsplist[k].inputval = browser_type
        start_debug=False
        for z in range(len(testcase)):
            if "testcasename" in testcase[z]:
                tc_name=testcase[z]["testcasename"]
                self.tc_name_list.append(tc_name)
        if type(runfrom_step) != int:
            pattern = re.compile(r"[0-9]+-[0-9]+")
            match = pattern.search(runfrom_step)
            if match:
                self.runfrom_step_range_input = [int(sno) for sno in runfrom_step.split('-')]
                first_step_val, last_step_val = self.runfrom_step_range_input
                starting_val_end_range = first_step_val + 1
                if first_step_val > 0 and first_step_val <= tsplist[-1].stepnum:
                    if last_step_val > first_step_val and last_step_val <= tsplist[-1].stepnum:
                        testcase_details=testcase[-2]['testcase']
                        no_of_steps=(last_step_val-first_step_val)+1
                        comment_step_count=0
                        tdlist=testcase_details[first_step_val-1:last_step_val]
                        for i in tdlist:
                            outputArray=i['outputVal'].split(';')
                            if (len(outputArray)>=1 and  '##' == outputArray[-1]):
                                comment_step_count=comment_step_count+1
                        if comment_step_count<no_of_steps:
                            runfrom_step = first_step_val
                            start_debug = True
                        else:
                            status=TERMINATE
                            log.info('Steps are commented in the testcase for the given input for run from step')
                    else:
                        logger.print_on_console('Invalid step number!! Please provide ending range for run from step between ',starting_val_end_range,' to ',tsplist[-1].stepnum,'\n')
                        log.info('Invalid step number!! Please provide run from step number')
                else:
                    logger.print_on_console('Invalid step number!! Please provide starting range for run from step between 1 to ',tsplist[-1].stepnum,'\n')
                    log.info('Invalid step number!! Please provide run from step number')
            else:
                logger.print_on_console('Invalid step number!! Please provide valid input for run from step \n' )
                log.info('Invalid step number!! Please provide valid input for run from step')
        else:
            if runfrom_step > 0 and runfrom_step <= tsplist[-1].stepnum:
                start_debug = True
            else:
                logger.print_on_console('Invalid step number!! Please provide run from step number between 1 to ',tsplist[-1].stepnum,'\n')
                log.info('Invalid step number!! Please provide run from step number')
        if flag:
            if start_debug:
                self.conthread=mythread
                execution_env = {'env':'default'}
                status,_,_ = self.executor(tsplist,DEBUG,last_tc_num,runfrom_step,mythread,execution_env,datatables=datatables, accessibility_testing = False)
        else:
            logger.print_on_console('Invalid script')
        temp={}
        if (handler.local_handler.awsKeywords):
            for k,v in handler.local_handler.awsKeywords.items():
                if list(v) != []:
                    temp[k]=list(v)
            if (temp):
                logger.print_on_console("***Following Testcases are not AWS Compatible because of the following keywords :***")
                log.info("***Following Testcases are not AWS Compatible because of the following keywords :***")
                for k,v in temp.items():
                    logger.print_on_console(k,':',list(v))
                    log.info(k+':'+str(list(v)))
        print('=======================================================================================================')
        log.info('***DEBUG COMPLETED***')
        logger.print_on_console('***DEBUG COMPLETED***')
        print('=======================================================================================================')
        #clearing of dynamic variables
        obj.clearList(self)
        #clearing dynamic variables at the end of execution to support dynamic variable at the scenario level
        obj.clear_dyn_variables()
        #clearing dynamic variables at the end of execution to support constant variable at the scenario level
        obj.clear_const_variables()
        return status

    def invoke_execution(self,mythread,json_data,socketIO,wxObject,configvalues,qcObject,qtestObject,zephyrObject,azureObject,cicd_mode,aws_mode,browserno='0',threadName=''):
        global terminate_flag, status_percentage, browserstack_count,saucelabs_count, screen_testcase_map
        qc_url=''
        qc_password=''
        qc_username=''
        zephyr_password=''
        zephyr_username=''
        zephyr_url=''
        zephyr_apitoken=''
        zephyr_authtype=''

        azure_password=''
        azure_username=''
        azure_url=''

        con = Controller()
        obj = handler.Handler()
        status=COMPLETED
        aws_tsp=[]
        aws_scenario=[]
        step_results=[]
        scen_id=[]
        pytest_files=[]
        condition_check_flag = False
        testcase_empty_flag = False
        count = 0
        info_msg=''
        opts = mythread.main.opts
        # t = test.Test()
        # suites_list,flag = t.gettsplist()
        #Getting all the details by parsing the json_data
        suiteId_list,suite_details,browser_type,scenarioIds,suite_data,execution_ids,batch_id,condition_check,dataparam_path,self.execution_mode,qc_creds,report_type = obj.parse_json_execute(json_data)
        self.action=EXECUTE
        log.info( 'No  of Suites : '+str(len(suiteId_list)))
        logger.print_on_console('No  of Suites : ',str(len(suiteId_list)))
        headless_mode = str(configvalues['headless_mode'])=='Yes'
        if headless_mode:
            log.info('Execution in headless mode')
            logger.print_on_console('Execution in headless mode')
        suite_idx=1
        tc_obj=None
        self.aws_obj=None
        if aws_mode:
            self.__load_aws()
            from testcase_compile import TestcaseCompile
            from aws_operations import AWS_Operations
            cur_date=str(datetime.now()).replace(' ','_').replace('.','_').replace(':','_')
            tc_obj=TestcaseCompile(cur_date)
            self.aws_obj=AWS_Operations(cur_date)
        #Iterate through the suites-list
        for suite,suite_id,suite_id_data in zip(suite_details,suiteId_list,suite_data):
            #EXECUTION GOES HERE
            flag = True
            local_cont.module_stop = False
            if terminate_flag:
                status=TERMINATE
            log.info('---------------------------------------------------------------------')
            print('=======================================================================================================')
            log.info('***SUITE '+str(suite_idx) +' EXECUTION STARTED***')
            logger.print_on_console('***SUITE ', str(suite_idx) ,' EXECUTION STARTED***')
            log.info('---------------------------------------------------------------------')
            print('=======================================================================================================')
            exc_pass = True
            base_execute_data = {
                'batchId': batch_id,
                'executionId': execution_ids[suite_idx-1],
                'testsuiteId': suite_id,
                'projectname' : suite['projectname']
            }
            if cicd_mode:
                base_execute_data["event"] = "return_status_executeTestSuite"
                base_execute_data["configkey"] = opts.configkey
                base_execute_data["executionListId"] = opts.executionListId
                base_execute_data["agentname"] = opts.agentname
                base_execute_data['execReq'] = json_data
                server_url = 'https://' + opts.serverurl + ':' + opts.serverport + '/setExecStatus'
                data_dict = dict({"status" : "started",
                    'startTime': datetime.now().strftime(TIME_FORMAT),"exce_data" : base_execute_data})
                #res = requests.post(server_url,json=data_dict, verify=False)
                res = Retryrequests.retry_cicd_apis(self, server_url, data_dict)
                # #send response through API
            else:
                socketIO.emit("return_status_executeTestSuite", dict({"status": "started",
                    'startTime': datetime.now().strftime(TIME_FORMAT)}, **base_execute_data))
            execute_result_data = dict({'scenarioId': None, 'reportData': None}, **base_execute_data)
            if(self.execution_mode == PARALLEL):
                log_handler = logger.CustomHandler(self.execution_mode,base_execute_data,browserno)
                log_filter = ThreadLogFilter(threadName)
                log_handler.addFilter(log_filter)
            else:
                log_handler = logger.CustomHandler(self.execution_mode,base_execute_data)
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d %(message)s")
            log_handler.setFormatter(formatter)
            log.root.addHandler(log_handler)
            handlerno = len(log.root.handlers)-1
            if aws_mode:
                pytest_files=[]
                #Logic to Execute each suite for each of the browser
            for browser in browser_type[suite_id]:
                local_cont.module_stop = False
                sc_idx = 0
                condition_check_flag = False
                #Logic to iterate through each scenario in the suite
                for scenario,scenario_id,condition_check_value,dataparam_path_value in zip(suite_id_data,scenarioIds[suite_id],condition_check[suite_id],dataparam_path[suite_id]):
                    execute_flag=True
                    #check if accessibility parameters are present if not initialize empty array
                    if "accessibilityMap" in suite and scenario_id in suite['accessibilityMap']:
                        accessibility_parameters = suite['accessibilityMap'][scenario_id]
                        if len(accessibility_parameters) > 0 and isinstance(accessibility_parameters, list) and isinstance(accessibility_parameters[0], list) and len(accessibility_parameters[0]) > 0:
                            accessibility_parameters = accessibility_parameters[0]
                        else:
                            accessibility_parameters = []
                    else:
                        accessibility_parameters = []
                    con.reporting_obj=reporting.Reporting()
                    con.configvalues=configvalues
                    con.exception_flag=self.exception_flag
                    con.wx_object=wxObject
                    handler.local_handler.tspList=[]
                    accessibility_reports = []
                    execute_result_data['scenarioId'] = scenario_id
                    #condition check for scenario execution and reporting for condition check
                    if not(condition_check_flag):
                            #check for terminate flag before printing loggers
                        if not(terminate_flag):
                            print('=======================================================================================================')
                            logger.print_on_console( '***Scenario ' ,str(sc_idx + 1) ,' execution started***')
                            print('=======================================================================================================')
                            log.info('***Scenario '  + str(sc_idx + 1)+ ' execution started***')
                        # if('integrationType' not in qc_creds and len(scenario)==2 and len(scenario['qcdetails'])==10):

                        # if('integrationType' in qc_creds and qc_creds['integrationType'] == 'ALM'):
                        integ = 0
                        if("alm" in qc_creds and qc_creds["alm"]["url"] != "" and len(scenario["qcdetails"]) > integ and scenario['qcdetails'][integ][0]["type"] == "ALM"):
                            qc_username=qc_creds['alm']['username']
                            qc_password=qc_creds['alm']['password']
                            qc_url=qc_creds['alm']['url']
                            qc_sceanrio_data=scenario['qcdetails'][integ]
                            integ += 1
                        # if('integrationType' in qc_creds and qc_creds['integrationType'] == 'qTest'):
                        if("qtest" in qc_creds and qc_creds["qtest"]["url"] != "" and len(scenario["qcdetails"]) > integ and scenario['qcdetails'][integ]["type"] == "qTest"):
                            qtest_username=qc_creds["qtest"]["username"]
                            qtest_password=qc_creds["qtest"]["password"]
                            qtest_url=qc_creds["qtest"]["url"]
                            qtest_stepsup=qc_creds["qtest"]["qteststeps"]
                            qtest_sceanrio_data=scenario['qcdetails'][integ]
                            integ += 1
                            qtest_project=qtest_sceanrio_data['qtestproject']
                            qtest_projectid=qtest_sceanrio_data['qtestprojectid']
                            qtest_suite=qtest_sceanrio_data['qtestsuite']
                            qtest_suiteid=qtest_sceanrio_data['qtestsuiteid']
                        # if('integrationType' in qc_creds and qc_creds['integrationType'] == 'Zephyr'):
                        if("zephyr" in qc_creds and qc_creds["zephyr"]["url"] != "" and len(scenario["qcdetails"]) > integ and scenario['qcdetails'][integ]["type"] == "Zephyr"):
                            zephyr_url=qc_creds["zephyr"]["url"]
                            zephyr_username=qc_creds["zephyr"]["username"]
                            zephyr_password=qc_creds["zephyr"]["password"]
                            zephyr_apitoken=qc_creds["zephyr"]["apitoken"]
                            zephyr_authtype=qc_creds["zephyr"]["authtype"]
                            zephyr_sceanrio_data=scenario['qcdetails'][integ]
                            integ += 1
                            zephyr_releaseid=zephyr_sceanrio_data['releaseid']
                            zephyr_projectid=zephyr_sceanrio_data['projectid']
                            zephyr_treeid=zephyr_sceanrio_data['treeid']
                            zephy_testid=zephyr_sceanrio_data['testid']
                            if 'parentid' in zephyr_sceanrio_data: zephyr_parentid=zephyr_sceanrio_data['parentid']
                            else: zephyr_parentid=''

                        # Updating the azure variables to update the test case status
                        if("azure" in qc_creds and qc_creds["azure"]["url"] != "" and len(scenario["qcdetails"]) > integ and scenario['qcdetails'][integ]["type"] == "Azure" and 'TestCaseId' in scenario['qcdetails'][integ]):
                            azure_url=qc_creds["azure"]["url"]
                            azure_username=qc_creds["azure"]["username"]
                            azure_password=qc_creds["azure"]["password"]
                            # azure_apitoken=qc_creds["azure"]["apitoken"]
                            # azure_authtype=qc_creds["azure"]["authtype"]
                            azure_sceanrio_data=scenario['qcdetails'][integ]
                            integ += 1
                            azure_test_plan_id=azure_sceanrio_data['TestPlanId']
                            azure_test_suite_id=azure_sceanrio_data['TestSuiteId']
                            azure_test_case_id=azure_sceanrio_data['TestCaseId']
                            if 'parentid' in azure_sceanrio_data: azure_parentid=azure_sceanrio_data['parentid']
                            else: azure_parentid=''

                        #Iterating through each test case in the scenario
                        for testcase in [eval(scenario[scenario_id])]:
                            #For every unique screen in list of test cases, store screen data
                            for step in testcase:
                                step['apptype'] = scenario['apptype']
                                screen_testcase_map[step['testcasename']] = {}
                                screen_testcase_map[step['testcasename']]["screenname"] = step['screenname']
                                screen_testcase_map[step['testcasename']]["screenid"] = step['screenid']
                                screen_testcase_map[step['testcasename']]["cycleid"] = suite['cycleid']
                                screen_testcase_map[step['testcasename']]["releaseid"] = suite['releaseid']
                                screen_testcase_map[step['testcasename']]["cyclename"] = suite['cyclename']
                                screen_testcase_map["executionid"] = execute_result_data['executionId']
                                screen_testcase_map[step['testcasename']]['accessibility_parameters'] = accessibility_parameters
                                screen_testcase_map[step['testcasename']]['projectname'] = suite['projectname']
                            #check for temrinate flag before parsing tsp list
                            if terminate_flag:
                                break
                            flag,_,last_tc_num,datatables,testcase_empty_flag,empty_testcase_names=obj.parse_json(testcase,dataparam_path_value)
                            if flag == False:
                                break
                            print('\n')
                            if (True in testcase_empty_flag):
                                if(int(condition_check_value)==1):
                                    condition_check_flag = True
                                    logger.print_on_console('Condition Check: Terminated by program ')
                                info_msg=str("Scenario cannot be executed, since the following testcases are empty: "+','.join(empty_testcase_names))
                                logger.print_on_console(info_msg)
                                log.info(info_msg)
                                status = TERMINATE
                                execute_flag=False
                            else:
                                tsplist = handler.local_handler.tspList
                                if aws_mode:
                                    aws_tsp.append(tsplist)
                                if len(tsplist)==0:
                                    continue
                                if not(aws_mode):
                                    for k in range(len(tsplist)):
                                        if tsplist[k].name.lower() == 'openbrowser' and tsplist[k].apptype.lower()=='web' and (IGNORE_THIS_STEP not in tsplist[k].inputval[0].split(';')):
                                            tsplist[k].inputval = [browser]
                        if aws_mode:
                            compile_status=False
                            scen_id=scenario_id.split('"')
                            aws_scenario=aws_scenario+scen_id
                            scenario_name=json_data['suitedetails'][suite_idx-1]["scenarioNames"][sc_idx]
                            tsplist = handler.local_handler.tspList
                            if not terminate_flag:
                                compile_status,pytest_file=tc_obj.compile_tc(tsplist,sc_idx+1,scenario_name)
                            if compile_status:
                                pytest_files.append(pytest_file)
                                msg='***Scenario'+str(sc_idx + 1)+': '+scenario_name+' Compiled for AWS Execution***'
                                print(line_separator)
                                logger.print_on_console(msg)
                                print(line_separator)
                                log.info(line_separator)
                                log.info(msg)
                                log.info(line_separator)
                            else:
                                terminate_flag=True
                                msg='***Scenario'+str(sc_idx+ 1)+': '+scenario_name+' is Terminated ***'
                                logger.print_on_console(msg)
                                log.info(msg)
                                tsplist=[]
                            sc_idx+=1
                            execute_flag=False
                        execution_env = json_data.get('exec_env', 'default').lower()

                        if execution_env == 'browserstack':
                            # self.__load_web()
                            # import script_generator
                            scenario_name=json_data['suitedetails'][suite_idx-1]["scenarioNames"][sc_idx]
                            core_utils.get_all_the_imports('Browserstack')
                            import browserstack_web_keywords
                            s = ''
                            browserstack_details = {
                                'browserstack_username': json_data['browserstack_username'],
                                'browserstack_access_key': json_data['browserstack_access_key'],
                            }
                            if(json_data['apptype'] == 'Web'):
                                s=browserstack_web_keywords.Browserstack_config()
                                browserstack_details['osVersion'] = json_data['osVersion']
                                browserstack_details['os'] = json_data['os']
                                browserstack_details['browserName'] = json_data['browserName']
                                browserstack_details['browserVersion'] = json_data['browserVersion']

                            s.save_browserstackconf(browserstack_details)
                            execution_env = {'env': 'browserstack','browser':browser,'scenario': scenario_name,'scenario_id':scenario_id,'handlerno': handlerno}
                            now=datetime.now()

                        elif execution_env == 'saucelabs':
                            # self.__load_web()
                            # import script_generator
                            scenario_name=json_data['suitedetails'][suite_idx-1]["scenarioNames"][sc_idx]
                            import sauceclient
                            core_utils.get_all_the_imports('Saucelabs')
                            import web_keywords,web_keywords_MW,web_keywords_MA
                            s = ''
                            sauce_details = {
                                'sauce_username': json_data['sauce_username'],
                                'sauce_access_key': json_data['sauce_access_key'],
                                'remote_url': json_data['remote_url'],
                            }
                            if(json_data['apptype'] == 'Web'):
                                s=web_keywords.Sauce_Config()
                                sauce_details['version'] = json_data['browserVersion']
                                sauce_details['platform'] = json_data['platform']
                            elif json_data['apptype'] == 'MobileApp':
                                s=web_keywords_MA.Sauce_Config()
                                sauce_details['mobile'] = json_data['mobile']
                            else:
                                s=web_keywords_MW.Sauce_Config()
                                sauce_details['mobile'] = json_data['mobile']

                            s.save_sauceconf(sauce_details)
                            execution_env = {'env': 'saucelabs','browser':browser,'scenario': scenario_name,'scenario_id':scenario_id,'handlerno': handlerno}
                            now=datetime.now()
                            # if not terminate_flag:
                            #     saucelabs_obj=script_generator.SauceLabs_Operations(scenario_name,str(saucelabs_count))
                            #     status=saucelabs_obj.complie_TC(tsplist,scenario_name,browser,str(saucelabs_count),execute_result_data,socketIO)
                            # if status==TERMINATE:
                            #     terminate_flag=True
                            #     msg='***Scenario'+str(sc_idx+ 1)+': '+scenario_name+' is Terminated ***'
                            #     logger.print_on_console(msg)
                            # else:
                            #     print('=======================================================================================================')
                            #     logger.print_on_console( '***Scenario' ,str(sc_idx + 1) ,' execution completed***')
                            #     print('=======================================================================================================')
                            # saucelabs_count += 1
                            # sc_idx += 1
                            # execute_flag=False
                        else:
                            # For sauce labs / AWS pass browser and scenario_id in execution_env to push logs into NFS
                            execution_env = {'env':'default','browser':browser,'scenario_id':scenario_id,'handlerno':handlerno}
                        if flag and execute_flag :
                            #check for temrinate flag before execution
                            tsplist = obj.read_step()
                            if not(terminate_flag):
                                con.action=EXECUTE
                                con.conthread=mythread
                                con.tsp_list=tsplist
                                local_cont.test_case_number=0
                                #create a video path
                                video_path = ''
                                recorder_obj = recording.Recorder()
                                record_flag = str(configvalues['screen_rec']).lower()
                                #start screen recording
                                if (record_flag=='yes') and self.execution_mode == SERIAL and json_data['apptype'] == 'Web': video_path = recorder_obj.record_execution(json_data['suitedetails'][0])
                                # Added data to get ids to store in report items collection
                                # status,status_percentage,accessibility_reports = con.executor(tsplist,EXECUTE,last_tc_num,1,con.conthread,execution_env,video_path,datatables=datatables,accessibility_testing = True)
                                status,status_percentage,accessibility_reports = con.executor(tsplist,EXECUTE,last_tc_num,1,con.conthread,execution_env,video_path,datatables=datatables,accessibility_testing = True,execute_result_data = execute_result_data)
                                #end video
                                if (record_flag=='yes') and self.execution_mode == SERIAL and json_data['apptype'] == 'Web': recorder_obj.rec_status = False
                                print('=======================================================================================================')
                                logger.print_on_console( '***Scenario' ,str(sc_idx + 1) ,' execution completed***')
                                print('=======================================================================================================')
                                tsplistLen = len(tsplist)
                                del con.tsp_list
                                del tsplist
                        if execute_flag:
                            #Saving the report for the scenario
                            logger.print_on_console( '***Saving report of Scenario' ,str(sc_idx  + 1 ),'***')
                            log.info( '***Saving report of Scenario' +str(sc_idx + 1)+'***')
                            os.chdir(self.cur_dir)
                            filename='Scenario'+str(count + 1)+'.json'
                            count+=1
                            #check if user has manually terminated during execution, then check if the teststep data and overallstatus is [] if so poputale default values in teststep data and overallstatus
                            if terminate_flag:
                                if con.reporting_obj.report_json[ROWS]==[] and con.reporting_obj.report_json[OVERALLSTATUS]=={}:
                                    con.reporting_obj.add_to_reporting_obj()
                            status_percentage["s_index"]=suite_idx-1
                            status_percentage["index"]=sc_idx
                            con.reporting_obj.user_termination=manual_terminate_flag
                            con.reporting_obj.save_report_json(filename,json_data,status_percentage)
                            execute_result_data["reportData"] = con.reporting_obj.report_json
                            if len(accessibility_reports) > 0:
                                execute_result_data["accessibility_reports"] = accessibility_reports
                            execute_result_data['report_type'] = report_type
                            if execution_env['env'] == 'browserstack':
                                browser_num={'1':'googlechrome','2':'firefox','3':'iexplore','7':'microsoftedge','8':'microsoftedge'}
                                self.__load_web()
                                import browserstack_web_keywords
                                self.obj = browserstack_web_keywords.Browserstack_config()
                                self.obj.get_browserstackconf()
                                time.sleep(5)
                            elif execution_env['env'] == 'saucelabs':
                                browser_num={'1':'googlechrome','2':'firefox','3':'iexplore','7':'microsoftedge','8':'microsoftedge'}
                                self.__load_web()
                                import web_keywords
                                self.obj = web_keywords.Sauce_Config()
                                self.obj.get_sauceconf()
                                sc = self.obj.get_sauceclient()
                                j = self.obj.get_saucejobs(sc)
                                all_jobs=j.get_jobs(start=int(now.timestamp()),full=True)
                                time.sleep(5)
                                import constants
                                if constants.SCREENSHOT_PATH  not in ['screenshot_path', 'Disabled']:
                                    path = os.path.join(constants.SCREENSHOT_PATH,json_data['suitedetails'][0]['projectname'],json_data['suitedetails'][0]['releaseid'],json_data['suitedetails'][0]['cyclename'],datetime.now().strftime("%Y-%m-%d"))
                                    
                                    if not os.path.exists(path):
                                        os.makedirs(path)
                                    file_name = datetime.now().strftime("%Y%m%d%H%M%S")
                                    video_path = path+"ScreenRecording_"+file_name+".mp4"
                                    for i in range(0,len(all_jobs)):
                                        if(all_jobs[i]['browser']==browser_num[browser]):
                                            file_creations_status=j.get_job_asset_content(all_jobs[i]['id'],file_name,path)
                                    if len(all_jobs)!=0:
                                        execute_result_data['reportData']['overallstatus']['video']=video_path
                            if cicd_mode:
                                execute_result_data["event"] = "result_executeTestSuite"
                                execute_result_data["configkey"] = opts.configkey
                                execute_result_data["executionListId"] = opts.executionListId
                                execute_result_data["agentname"] = opts.agentname
                                execute_result_data['execReq'] = json_data
                                server_url = 'https://' + opts.serverurl + ':' + opts.serverport + '/setExecStatus'
                                data_dict = dict({"exce_data" : execute_result_data})
                                # res = requests.post(server_url,json=data_dict, verify=False)
                                res = Retryrequests.retry_cicd_apis(self, server_url, data_dict)
                            else:
                                socketIO.emit('result_executeTestSuite', execute_result_data)
                            obj.clearList(con)
                            sc_idx += 1
                            #logic for condition check
                            report_json=con.reporting_obj.report_json[OVERALLSTATUS]
                            #Check is made to fix issue #401
                            overall_status=report_json[OVERALLSTATUS] if len(report_json)>0 else TEST_RESULT_FAIL
                            if overall_status != TEST_RESULT_PASS: exc_pass = False
                            if(int(condition_check_value)==1):
                                if(overall_status==TEST_RESULT_PASS):
                                    continue
                                else:
                                    condition_check_flag = True
                                    logger.print_on_console('Condition Check: Terminated by program ')
                        elif (True in testcase_empty_flag):
                            logger.print_on_console( '***Saving report of Scenario' ,str(sc_idx + 1),'***')
                            log.info( '***Saving report of Scenario' +str(sc_idx + 1)+'***')
                            os.chdir(self.cur_dir)
                            filename='Scenario'+str(count + 1)+'.json'
                            count+=1
                            status_percentage["s_index"]=suite_idx-1
                            status_percentage["index"]=sc_idx
                            con.reporting_obj.user_termination=manual_terminate_flag
                            con.reporting_obj.save_report_json_conditioncheck_testcase_empty(filename,info_msg,json_data,status_percentage)
                            execute_result_data["reportData"] = con.reporting_obj.report_json_condition_check_testcase_empty
                            if cicd_mode:
                                execute_result_data["event"] = "result_executeTestSuite"
                                execute_result_data["configkey"] = opts.configkey
                                execute_result_data["executionListId"] = opts.executionListId
                                execute_result_data["agentname"] = opts.agentname
                                execute_result_data['execReq'] = json_data
                                server_url = 'https://' + opts.serverurl + ':' + opts.serverport + '/setExecStatus'
                                data_dict = dict({"exce_data" : execute_result_data})
                                # res = requests.post(server_url,json=data_dict, verify=False)  
                                res = Retryrequests.retry_cicd_apis(self, server_url, data_dict)                          
                            else:
                                socketIO.emit('result_executeTestSuite', execute_result_data)
                            obj.clearList(con)
                            sc_idx += 1
                            exc_pass = False
                            report_json=con.reporting_obj.report_json_condition_check_testcase_empty[OVERALLSTATUS]
                        integ=0
                        # if integration_type!="qTest" and integration_type!="Zephyr" and len(scenario['qcdetails'])==10 and (qc_url!='' and qc_password!='' and  qc_username!=''):
                        if  len(scenario["qcdetails"]) > integ and qc_creds['alm']['url'] != '' and scenario['qcdetails'][integ][0]["type"] == "ALM":
                            integ += 1
                            if type(qc_sceanrio_data) is not list:
                                qc_domain=qc_sceanrio_data['qcdomain']
                                qc_project=qc_sceanrio_data['qcproject']
                                qc_folder=qc_sceanrio_data['qcfolderpath']
                                qc_folderid=qc_sceanrio_data[i]['qcfolderid']
                                qc_tsList=qc_sceanrio_data['qctestset']
                                qc_testrunname=qc_sceanrio_data['qctestcase']
                                qc_status_over=report_json
                                qc_update_status=qc_status_over['overallstatus']
                                if(str(qc_update_status).lower()=='pass'):
                                    qc_update_status='Passed'
                                elif(str(qc_update_status).lower()=='fail'):
                                    qc_update_status='Failed'
                                else:
                                    qc_update_status='Not Completed'
                                try:
                                    qc_status = {}
                                    qc_status['qcaction']='qcupdate'
                                    qc_status['qcurl']=qc_url
                                    qc_status['qcusername']=qc_username
                                    qc_status['qcpassword']=qc_password
                                    qc_status['qc_domain']=qc_domain
                                    qc_status['qc_project']=qc_project
                                    qc_status['qc_folder']=qc_folder
                                    qc_status['qc_folderid']=qc_folderid
                                    qc_status['qc_tsList']=qc_tsList
                                    qc_status['qc_testrunname']=qc_testrunname
                                    qc_status['qc_update_status'] = qc_update_status
                                    logger.print_on_console('****Updating QCDetails****')
                                    if qcObject is not None:
                                        qc_status_updated = qcObject.update_qc_details(qc_status)
                                        if qc_status_updated:
                                            logger.print_on_console('****Updated QCDetails****')
                                        else:
                                            logger.print_on_console('****Failed to Update QCDetails****')
                                    else:
                                        logger.print_on_console('****Failed to Update QCDetails****')
                                except Exception as e:
                                    logger.print_on_console('Error in Updating Qc details')
                            else:
                                for i in range(len(qc_sceanrio_data)):
                                    qc_domain=qc_sceanrio_data[i]['qcdomain']
                                    qc_project=qc_sceanrio_data[i]['qcproject']
                                    qc_folder=qc_sceanrio_data[i]['qcfolderpath']
                                    qc_folderid=qc_sceanrio_data[i]['qcfolderid']
                                    qc_tsList=qc_sceanrio_data[i]['qctestset']
                                    qc_testrunname=qc_sceanrio_data[i]['qctestcase']
                                    qc_status_over=report_json
                                    qc_update_status=qc_status_over['overallstatus']
                                    if(str(qc_update_status).lower()=='pass'):
                                        qc_update_status='Passed'
                                    elif(str(qc_update_status).lower()=='fail'):
                                        qc_update_status='Failed'
                                    else:
                                        qc_update_status='Not Completed'
                                    try:
                                        qc_status = {}
                                        qc_status['qcaction']='qcupdate'
                                        qc_status['qcurl']=qc_url
                                        qc_status['qcusername']=qc_username
                                        qc_status['qcpassword']=qc_password
                                        qc_status['qc_domain']=qc_domain
                                        qc_status['qc_project']=qc_project
                                        qc_status['qc_folder']=qc_folder
                                        qc_status['qc_folderid']=qc_folderid
                                        qc_status['qc_tsList']=qc_tsList
                                        qc_status['qc_testrunname']=qc_testrunname
                                        qc_status['qc_update_status'] = qc_update_status
                                        logger.print_on_console('****Updating QCDetails****')
                                        if qcObject is not None:
                                            qc_status_updated = qcObject.update_qc_details(qc_status)
                                            if qc_status_updated:
                                                logger.print_on_console('****Updated QCDetails****')
                                            else:
                                                logger.print_on_console('****Failed to Update QCDetails****')
                                        else:
                                            logger.print_on_console('****Failed to Update QCDetails****')
                                    except Exception as e:
                                        logger.print_on_console('Error in Updating Qc details')
                        # if (integration_type=="qTest" and qc_url!='' and qc_password!='' and  qc_username!=''):
                        if len(scenario["qcdetails"]) > integ and qc_creds['qtest']['url'] != '' and scenario['qcdetails'][integ]["type"] == "qTest":
                            qtest_status_over=report_json
                            integ += 1
                            try:
                                qtest_status = {}
                                qtest_status['qtestaction']='qtestupdate'
                                qtest_status['qtest_project']=qtest_project
                                qtest_status['qtest_projectid']=qtest_projectid
                                qtest_status['qtest_suite']=qtest_suite
                                qtest_status['qtest_suiteid']=qtest_suiteid
                                qtest_status['user']=qtest_username
                                qtest_status['qtest_status_over'] = qtest_status_over
                                qtest_status['qtest_stepsup']=qtest_stepsup
                                qtest_status['qtesturl']=qtest_url
                                qtest_status['qtestusername']=qtest_username
                                qtest_status['qtestpassword']=qtest_password
                                qtest_status['steps']=[]
                                for i in con.reporting_obj.report_json['rows']:
                                    if 'Keyword' in i and i['Keyword'] == 'TestCase Name':
                                        pass
                                    elif 'Step' in i and i['Step'] == 'Terminated':
                                        pass
                                    else:
                                        if(i['status'].lower()=='pass'):
                                            qtest_status['steps'].append(601)
                                        elif(i['status'].lower()=='fail'):
                                            qtest_status['steps'].append(602)
                                        elif(i['status'].lower()=='terminate'):
                                            qtest_status['steps'].append(603)
                                        else:
                                            tsplistLen -= 1
                                logger.print_on_console('****Updating qTest Details****')
                                if qtestObject is not None:
                                    qtest_status_updated = qtestObject.update_qtest_run_details(qtest_status,tsplistLen)
                                    if qtest_status_updated:
                                        logger.print_on_console('****Updated qTest Details****')
                                    else:
                                        logger.print_on_console('****Failed to Update qTest Details****')
                                else:
                                    logger.print_on_console('****Failed to Update qTest Details****')
                            except Exception as e:
                                log.error('Error in Updating qTest details '+str(e))
                                logger.print_on_console('Error in Updating qTest details')
                        # if (integration_type=="Zephyr" and zephyr_password!='' and zephyr_username!='' and  zephyr_url!=''):
                        if len(scenario["qcdetails"]) > integ and qc_creds['zephyr']['url'] != '' and scenario['qcdetails'][integ]["type"] == "Zephyr":
                            zephyr_status_over=report_json
                            integ += 1
                            try:
                                zephyr_status = {}
                                zephyr_status['zephyraction']='zephyrupdate'
                                zephyr_status['releaseid']=zephyr_releaseid
                                zephyr_status['testid']=zephy_testid
                                zephyr_status['projectId']=zephyr_projectid
                                zephyr_status['treeid']=zephyr_treeid
                                zephyr_status['parentid']=zephyr_parentid
                                zephyr_status['zephyr_password']=zephyr_password
                                zephyr_status['zephyr_url']=zephyr_url
                                zephyr_status['zephyr_username']=zephyr_username
                                zephyr_status['zephyr_apitoken']=zephyr_apitoken
                                zephyr_status['zephyr_authtype']=zephyr_authtype
                                zephyr_update_status=zephyr_status_over['overallstatus']
                                if(zephyr_update_status.lower()=='pass'):
                                    zephyr_status['status']='1'
                                elif(zephyr_update_status.lower()=='fail'):
                                    zephyr_status['status']='2'
                                elif(zephyr_update_status.lower()=='terminate'):
                                    zephyr_status['status']='11'
                                logger.print_on_console('****Updating Zephyr Details****')
                                if zephyrObject is not None:
                                    zephry_update_status = zephyrObject.update_zephyr_test_details(zephyr_status)
                                    if zephry_update_status:
                                        logger.print_on_console('****Updated Zephyr Details****')
                                    else:
                                        logger.print_on_console('****Failed to Update Zephyr Details****')
                                else:
                                    logger.print_on_console('****Failed to Update Zephyr Details****')
                            except Exception as e:
                                log.error('Error in Updating Zephyr details '+str(e))
                                logger.print_on_console('Error in Updating Zephyr details')
                        
                        # Azure - Updating the scenario status to the azure test case
                        if len(scenario["qcdetails"]) > integ and 'azure' in qc_creds and qc_creds['azure']['url'] != '' and scenario['qcdetails'][integ]["type"] == "Azure" and 'TestCaseId' in scenario['qcdetails'][integ]:
                            azure_status_over=report_json
                            integ += 1
                            try:
                                azure_status = {}
                                azure_status['azureaction']='azureupdate'
                                azure_status['azurepat']=azure_password
                                azure_status['azureBaseUrl']=azure_url
                                azure_status['azure_username']=azure_username
                                azure_status['mapping_details'] = scenario['qcdetails'][integ-1]
                                azure_update_status=azure_status_over['overallstatus']
                                if(azure_update_status.lower()=='pass'):
                                    azure_status['status']='passed'
                                elif(azure_update_status.lower()=='fail'):
                                    azure_status['status']='failed'
                                elif(azure_update_status.lower()=='terminate'):
                                    azure_status['status']='failed'
                                logger.print_on_console('****Updating Azure Details****')
                                if azureObject is not None:
                                    azure_update_status = azureObject.update_azure_test_details(azure_status)
                                    if azure_update_status:
                                        logger.print_on_console('****Updated Azure Details****')
                                    else:
                                        logger.print_on_console('****Failed to Update Azure Details****')
                                else:
                                    logger.print_on_console('****Failed to Update Azure Details****')
                            except Exception as e:
                                log.error('Error in Updating Azure details '+str(e))
                                logger.print_on_console('Error in Updating Azure details')


                        if local_cont.module_stop:
                            break
                    else:
                        logger.print_on_console( '***Saving report of Scenario' ,str(sc_idx + 1),'***')
                        log.info( '***Saving report of Scenario' +str(sc_idx + 1)+'***')
                        os.chdir(self.cur_dir)
                        filename='Scenario'+str(count + 1)+'.json'
                        count+=1
                        status_percentage["s_index"]=suite_idx-1
                        status_percentage["index"]=sc_idx
                        con.reporting_obj.user_termination=manual_terminate_flag
                        con.reporting_obj.save_report_json_conditioncheck(filename,json_data,status_percentage)
                        execute_result_data["reportData"] = con.reporting_obj.report_json_condition_check
                        if cicd_mode:
                            execute_result_data["event"] = "result_executeTestSuite"
                            execute_result_data["configkey"] = opts.configkey
                            execute_result_data["executionListId"] = opts.executionListId
                            execute_result_data["agentname"] = opts.agentname
                            execute_result_data['execReq'] = json_data
                            server_url = 'https://' + opts.serverurl + ':' + opts.serverport + '/setExecStatus'
                            data_dict = dict({"exce_data" : execute_result_data})
                            # res = requests.post(server_url,json=data_dict, verify=False)
                            res = Retryrequests.retry_cicd_apis(self, server_url, data_dict)
                        else:
                            socketIO.emit('result_executeTestSuite', execute_result_data)
                        obj.clearList(con)
                        sc_idx += 1
                        exc_pass = False
                        #logic for condition check
                        report_json=con.reporting_obj.report_json[OVERALLSTATUS]
                    time.sleep(1)
            if aws_mode and not terminate_flag and not(True in testcase_empty_flag):
                tc_obj.make_zip(pytest_files)
                execution_status,step_results,config_stat=self.aws_obj.run_aws_android_tests()
                if execution_status and config_stat:
                    self.aws_report(aws_tsp,aws_scenario,step_results,suite_idx,execute_result_data,con.reporting_obj,json_data,socketIO)
                else:
                    logger.print_on_console( '***Saving report of Scenario' ,str(sc_idx + 1),'***')
                    log.info( '***Saving report of Scenario' +str(sc_idx + 1)+'***')
                    os.chdir(self.cur_dir)
                    filename='Scenario'+str(count + 1)+'.json'
                    count+=1
                    status_percentage["s_index"]=suite_idx-1
                    status_percentage["index"]=sc_idx
                    con.reporting_obj.user_termination=manual_terminate_flag
                    if not(config_stat):
                        info_msg=str("Error in Configuring AWS run")
                    logger.print_on_console(info_msg)
                    log.info(info_msg)
                    con.reporting_obj.save_report_json_conditioncheck_testcase_empty(filename,info_msg,json_data,status_percentage)
                    execute_result_data["reportData"] = con.reporting_obj.report_json_condition_check_testcase_empty
                    if cicd_mode :
                        execute_result_data["event"] = "result_executeTestSuite"
                        execute_result_data["configkey"] = opts.configkey
                        execute_result_data["executionListId"] = opts.executionListId
                        execute_result_data["agentname"] = opts.agentname
                        execute_result_data['execReq'] = json_data
                        server_url = 'https://' + opts.serverurl + ':' + opts.serverport + '/setExecStatus'
                        data_dict = dict({"exce_data" : execute_result_data})
                        # res = requests.post(server_url,json=data_dict, verify=False)
                        res = Retryrequests.retry_cicd_apis(self, server_url, data_dict)
                    else:
                        socketIO.emit('result_executeTestSuite', execute_result_data)
                    obj.clearList(con)
                    sc_idx += 1
                    exc_pass = False
                    report_json=con.reporting_obj.report_json_condition_check_testcase_empty[OVERALLSTATUS]
                if con.reporting_obj.overallstatus != 'Pass': exc_pass = False
                if not(execution_status):
                    status=TERMINATE
            temp={}
            if (handler.local_handler.awsKeywords):
                for k,v in handler.local_handler.awsKeywords.items():
                    if list(v) != []:
                        temp[k]=list(v)
                if (temp):
                    logger.print_on_console("***Following Testcases are not AWS Compatible because of the following keywords :***")
                    log.info("***Following Testcases are not AWS Compatible because of the following keywords :***")
                    for k,v in temp.items():
                        logger.print_on_console(k,':',list(v))
                        log.info(k+':'+str(list(v)))
            log.info('---------------------------------------------------------------------')
            print('=======================================================================================================')
            log.info('***SUITE '+ str(suite_idx) +' EXECUTION COMPLETED***')
            if status == TERMINATE: exc_pass = False
            if cicd_mode:
                base_execute_data["event"] = "return_status_executeTestSuite"
                base_execute_data["configkey"] = opts.configkey
                base_execute_data["executionListId"] = opts.executionListId
                base_execute_data["agentname"] = opts.agentname
                base_execute_data['execReq'] = json_data
                server_url = 'https://' + opts.serverurl + ':' + opts.serverport + '/setExecStatus'
                data_dict = dict({"status" : "finished", "executionStatus": exc_pass,
                    'endTime': datetime.now().strftime(TIME_FORMAT),"exce_data" : base_execute_data})
                # res = requests.post(server_url,json=data_dict, verify=False)
                res = Retryrequests.retry_cicd_apis(self, server_url, data_dict)
            else:
                socketIO.emit("return_status_executeTestSuite", dict({"status": "finished", "executionStatus": exc_pass,
                    "endTime": datetime.now().strftime(TIME_FORMAT)}, **base_execute_data))
            if not exc_pass:
                if status == TERMINATE and manual_terminate_flag:
                    mythread.test_status = 'userTerminate'
                elif status == TERMINATE:
                    mythread.test_status = 'programTerminate'
                else:
                    mythread.test_status = 'fail'
            #clearing dynamic variables at the end of execution to support dynamic variable at the scenario level
            obj.clear_dyn_variables()
            #clearing dynamic variables at the end of execution to support constant variable at the scenario level
            obj.clear_const_variables()
            logger.print_on_console('***SUITE ', str(suite_idx) ,' EXECUTION COMPLETED***')
            log.info('---------------------------------------------------------------------')
            print('=======================================================================================================')
            suite_idx += 1
        del con
        del obj
        if status==TERMINATE:
            print('=======================================================================================================')
            logger.print_on_console( '***Terminating the Execution***',color="YELLOW")
            print('=======================================================================================================')
        return status



    #generating report of AWS in Avo Assure by using AWS result(AWS device farm executed result present in test spec output.txt)
    def aws_report(self,aws_tsp,aws_scenario,step_results,suite_idx,execute_result_data,obj_reporting,json_data,socketIO):
        sc_idx=0
        idx_t=0
        list_time=[]
        tc_aws=[]
        inpval=[]
        keyword_flag=True
        ignore_stat=False
        try:
            path_file=os.environ['AVO_ASSURE_HOME']+os.sep+'output'
            os.chdir(path_file)
            f=open("step_result.txt","w")
            f.writelines(str(step_results))
            list_time=step_results[-1]
            del step_results[-1]
            list_time=eval(list_time)
            format_time='%Y-%m-%d %H:%M:%S.%f'
            for i in step_results:
                self.scenario_start_time=datetime.strptime(list_time[idx_t], format_time)
                status_percentage = {TEST_RESULT_PASS:0,TEST_RESULT_FAIL:0,TERMINATE:0,"total":0}
                pass_val=fail_val=0
                obj_reporting.report_string=[]
                obj_reporting.overallstatus_obj={}
                obj_reporting.overallstatus=TEST_RESULT_PASS
                obj_reporting.report_json[ROWS]=obj_reporting.report_string
                obj_reporting.report_json[OVERALLSTATUS]=obj_reporting.overallstatus_obj
                tc_aws=aws_tsp[sc_idx]
                os.chdir(self.cur_dir)
                filename='Scenario'+str(sc_idx+1)+'.json'
                for tsp in tc_aws:
                    if tsp.name=='launchApplication':
                        inpval = tsp.inputval[0].split(';')
                        result=['Pass',True,'9cc33d6fe25973868b30f4439f09901a',None]
                        self.status=result[0]
                        if result[0]=='Pass':
                            pass_val+=1
                            status_percentage["total"]+=1
                        else:
                            fail_val+=1
                            status_percentage["total"]+=1
                        ellapsed_time=''
                        obj_reporting.generate_report_step(tsp,self.status,self,ellapsed_time,keyword_flag,result,ignore_stat,inpval)
                        continue
                    else:
                        self.status=i[str(tsp.stepnum)][0]
                        if self.status=='Pass':
                            pass_val+=1
                            status_percentage["total"]+=1
                        elif self.status=='Fail':
                            fail_val+=1
                            status_percentage["total"]+=1
                            obj_reporting.overallstatus=self.status
                        inpval = tsp.inputval[0].split(';')
                        result=i[str(tsp.stepnum)]
                        ellapsed_time=''
                        obj_reporting.generate_report_step(tsp,self.status,self,ellapsed_time,keyword_flag,result,ignore_stat,inpval)
                        continue
                self.scenario_end_time=datetime.strptime(list_time[idx_t+1], format_time)
                self.scenario_ellapsed_time=self.scenario_end_time-self.scenario_start_time
                obj_reporting.build_overallstatus(self.scenario_start_time,self.scenario_end_time,self.scenario_ellapsed_time)
                status_percentage[TEST_RESULT_PASS]=pass_val
                status_percentage[TEST_RESULT_FAIL]=fail_val
                status_percentage["s_index"]=suite_idx-1
                status_percentage["index"]=sc_idx
                obj_reporting.user_termination=manual_terminate_flag
                obj_reporting.save_report_json(filename,json_data,status_percentage)
                execute_result_data["scenarioId"]=aws_scenario[sc_idx]
                execute_result_data["reportData"] = obj_reporting.report_json
                socketIO.emit('result_executeTestSuite', execute_result_data)
                sc_idx+=1
                idx_t+=1
        except Exception as e:
            logger.print_on_console("Exception in aws_report")
            log.error("Exception in aws_report. Error: " + str(e))

    def invoke_controller(self,action,mythread,debug_mode,runfrom_step,json_data,root_obj,socketIO,qc_soc,qtest_soc,zephyr_soc,azure_soc,cicd_mode,*args):
        status = COMPLETED
        global socket_object
        self.conthread=mythread
        self.clear_data()
        wxObject = root_obj.cw
        socket_object = socketIO
        configvalues = self.configvalues
        dis_sys_screenoff = str(configvalues['disable_screen_timeout']).lower() == 'yes'
        reset_sys_screenoff = False
        try:
            is_admin = core_utils.check_isadmin()
            #Logic to make sure that logic of usage of existing driver is not applicable to execution
            if local_cont.web_dispatcher_obj != None:
                local_cont.web_dispatcher_obj.action=action
            if action==EXECUTE:
                aws_mode = len(args)>0 and args[0]
                self.execution_mode = json_data['exec_mode'].lower()
                if configvalues['kill_stale'].lower() == 'yes': kill_process()
                if dis_sys_screenoff and is_admin and SYSTEM_OS == 'Windows':
                    self.disable_screen_timeout()
                    reset_sys_screenoff = True
                if self.execution_mode == SERIAL:
                    status=self.invoke_execution(mythread,json_data,socketIO,wxObject,self.configvalues,qc_soc,qtest_soc,zephyr_soc,azure_soc,aws_mode,cicd_mode)
                elif self.execution_mode == PARALLEL:
                    status = self.invoke_parralel_exe(mythread,json_data,socketIO,wxObject,self.configvalues,qc_soc,qtest_soc,zephyr_soc,azure_soc,aws_mode,cicd_mode)
                # Remove all the added custom handlers. Handler at 0 index is main one. So we start removing from 1st index.
                for _ in range(len(log.root.handlers)-1):
                    log.root.handlers[1].writeManifest()
                    log.root.removeHandler(log.root.handlers[1])
                shutil.rmtree(os.sep.join([os.getcwd(),'output','.logs',json_data['batchId']]), ignore_errors=True)
            elif action==DEBUG:
                if json_data[0]['testcasename'] == AVO_GENIUS: kill_process()
                self.debug_choice=wxObject.choice
                self.debug_mode=debug_mode
                self.wx_object=wxObject
                status=self.invoke_debug(mythread,runfrom_step,json_data)
            if status != TERMINATE:
                status=COMPLETED
        except Exception as e:
            logger.print_on_console("Exception in Invoke Controller")
            log.error("Exception in Invoke Controller", exc_info=True)
            status = TERMINATE
        finally:
            if reset_sys_screenoff:
                self.reset_screen_timeout()
        return status

    def disable_screen_timeout(self):
        try:
            log.info("Disable screen timeout process started")
            poweroptions_list=[]
            get_active_scheme_cmd = "powercfg -getactivescheme"
            power_cfg_active = subprocess.Popen(get_active_scheme_cmd, shell=True, stdout=subprocess.PIPE)
            power_active_scheme = power_cfg_active.stdout.read()
            power_active_scheme = power_active_scheme.decode()
            pattern = "GUID: [a-z,A-Z,0-9]*-?[a-z,A-Z,0-9]*-?[a-z,A-Z,0-9]*-?[a-z,A-Z,0-9]*-?[a-z,A-Z,0-9]*"
            result = re.findall(pattern, power_active_scheme)
            for i in result:
                temp = i.split(" ")
                if temp[-1] and len(temp[-1])==36:
                    self.active_scheme=temp[-1]
            powercgf_list_cmd = "powercfg -list"
            power_cfg_list = subprocess.Popen(powercgf_list_cmd, shell=True, stdout=subprocess.PIPE)
            power_scheme_list = power_cfg_list.stdout.read()
            power_scheme_list = power_scheme_list.decode()
            pattern = "GUID: [a-z,A-Z,0-9]*-?[a-z,A-Z,0-9]*-?[a-z,A-Z,0-9]*-?[a-z,A-Z,0-9]*-?[a-z,A-Z,0-9]*"
            result1 = re.findall(pattern, power_scheme_list)
            for i in result1:
                temp1 = i.split(" ")
                if temp1[-1] and len(temp1[-1])==36:
                    poweroptions_list.append(temp1[-1])
            if len(poweroptions_list)==1:
                duplicate_cmd="powercfg -duplicatescheme "+self.active_scheme
                subprocess.call(duplicate_cmd, shell=True)
                powercgf_list_cmd = "powercfg -list"
                power_cfg_list = subprocess.Popen(powercgf_list_cmd, shell=True, stdout=subprocess.PIPE)
                power_scheme_list = power_cfg_list.stdout.read()
                power_scheme_list = power_scheme_list.decode()
                pattern = "GUID: [a-z,A-Z,0-9]*-?[a-z,A-Z,0-9]*-?[a-z,A-Z,0-9]*-?[a-z,A-Z,0-9]*-?[a-z,A-Z,0-9]*"
                result2 = re.findall(pattern, power_scheme_list)
                poweroptions_list=[]
                for x in result2:
                    temp2 = x.split(" ")
                    if temp2[-1] and len(temp2[-1])==36:
                        poweroptions_list.append(temp2[-1])
                self.one_power_option=True
            for j in poweroptions_list:
                if j!=self.active_scheme:
                    self.change_power_option=j
                    break
            self.powerscheme_location=os.environ['AVO_ASSURE_HOME']+os.sep+'assets'+os.sep+'active_scheme.pow'
            export_cmd="powercfg -export "+self.powerscheme_location+" "+self.active_scheme
            subprocess.call(export_cmd, shell=True)
            powercfg_commands = ["powercfg /change standby-timeout-ac 0", "powercfg /change standby-timeout-dc 0", "powercfg /change monitor-timeout-ac 0", "powercfg /change monitor-timeout-dc 0", "powercfg /change hibernate-timeout-ac 0", "powercfg /change hibernate-timeout-dc 0"]
            for command in powercfg_commands:
                subprocess.call(command, shell=True)
            log.info("Disable screen timeout process completed")
        except Exception as e:
            logger.print_on_console("Exception in reset screen timeout")
            log.error("Exception in reset screen timeout. Error: " + str(e))

    def reset_screen_timeout(self):
        try:
            log.info("reset screen timeout process started")
            setactive_cmd="powercfg -setactive "+self.change_power_option
            subprocess.call(setactive_cmd, shell=True)
            deleteactive_cmd="powercfg -delete "+self.active_scheme
            subprocess.call(deleteactive_cmd, shell=True)
            import_cmd="powercfg -import "+self.powerscheme_location+" "+self.active_scheme
            subprocess.call(import_cmd, shell=True)
            os.remove(self.powerscheme_location)
            setactive_cmd="powercfg -setactive "+self.active_scheme
            subprocess.call(setactive_cmd, shell=True)
            if self.one_power_option:
                delete_duplicate_cmd="powercfg -delete "+self.change_power_option
                subprocess.call(delete_duplicate_cmd, shell=True)
            log.info("reset screen timeout process completed")
        except Exception as e:
            logger.print_on_console("Exception in reset screen timeout")
            log.error("Exception in reset screen timeout. Error: " + str(e))

    def invoke_parralel_exe(self,mythread,json_data,socketIO,wxObject,configvalues,qc_soc,qtest_soc,zephyr_soc,aws_mode,cicd_mode):
        try:
            import copy
            browsers_data = json_data['suitedetails'][0]['browserType']
            jsondata_dict = {}
            th={}
            log1 = logging.getLogger("controller.py") #Disable loggers from imported modules
            if(log1.handlers):
                log1.handlers.clear()
            if json_data['exec_env'].lower() =='saucelabs':
                self.__load_web()
                import web_keywords
                import sauceclient
                s=web_keywords.Sauce_Config()
                s.get_sauceconf()
                sc=s.get_sauceclient()
                a=sauceclient.Account(sc)
                maxlength=a.get_concurrency()['concurrency']['ancestor']['allowed']['overall']
                curlength=a.get_concurrency()['concurrency']['ancestor']['current']['overall']
                browserlength=maxlength-curlength
                if len(browsers_data) > browserlength:
                    browsers_data=browsers_data[:browserlength]
                    logger.print_on_console('Available Instance for Execution is ' + str(browserlength) + " browsers")
            for i in range (len(browsers_data)):
                jsondata_dict[i] = copy.deepcopy(json_data)
                for j in range(len(jsondata_dict[i]['suitedetails'])):
                    jsondata_dict[i]['suitedetails'][j]['browserType'] = [browsers_data[i]]
                thread_name = "test_thread_browser" + str(browsers_data[i])
                th[i] = threading.Thread(target = self.invoke_execution, name = thread_name, args = (mythread,jsondata_dict[i],socketIO,wxObject,configvalues,qc_soc,qtest_soc,zephyr_soc,cicd_mode,aws_mode,browsers_data[i],thread_name))
                self.seperate_log(th[i], browsers_data[i]) #function that creates different logs for each browser
                if SYSTEM_OS =='Linux': time.sleep(0.5)
                th[i].start()
            for i in th:
                th[i].join()
            for i in th:
                while th[i].is_alive(): pass
        except Exception as e:
            logger.print_on_console("Exception in Parallel Execution")
            log.error("Exception in Parallel Execution. Error: " + str(e))
        status = COMPLETED
        if terminate_flag:
            status = TERMINATE
        return status

    def seperate_log(self, cur_thread, id):
        try:
            log = logging.getLogger("controller.py")
            log_filepath = os.path.normpath(os.path.dirname(self.configvalues["logFile_Path"]) + os.sep + 'Avoclient_Parallel_' + str(BROWSER_NAME_LOG[id]) + '.log').replace("\\","\\\\")
            file1 = open(log_filepath, 'a+')
            file1.close()
            threadName = cur_thread.name #Get name of each thread
            log_handler = TimedRotatingFileHandler(log_filepath, 'midnight', 1, 5, None, False, False)
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d %(message)s")
            log_handler.setFormatter(formatter)
            log_filter = ThreadLogFilter(threadName)
            log_handler.addFilter(log_filter)
            log.addHandler(log_handler)
        except Exception as e:
            log.error(e)

    def step_execution_status(self,teststepproperty):
        #325 : Report - Skip status in report by providing value 0 in the output column in testcase grid is not handled.
        nostatusflag = False
        if teststepproperty.outputval.split(";")[-1].strip() == STEPSTATUS_INREPORTS_ZERO:
            nostatusflag=True
        return nostatusflag


def kill_process():
    import tempfile
    import psutil
    if SYSTEM_OS == 'Darwin':
        try:
            import browser_Keywords_MW
            if browser_Keywords_MW.driver_obj != None:
                browser_Keywords_MW.driver_obj.quit()
                browser_Keywords_MW.driver_obj = None
        except ImportError: pass
        except Exception as e:
            logger.print_on_console('Error in stopping mobile browser driver as driver is already closed')
            log.error(e)


        try:
            import android_scrapping
            if android_scrapping.driver != None:
                android_scrapping.driver.quit()
                android_scrapping.driver = None
        except ImportError: pass
        except Exception as e:
            logger.print_on_console('Error in stopping application driver as driver is already closed')
            log.error(e)

        try:
            import browser_Keywords
            for driver in browser_Keywords.drivermap:
                driver.quit()
            del browser_Keywords.drivermap[:]
            if hasattr(browser_Keywords.local_bk, 'driver_obj'):
                if (browser_Keywords.local_bk.driver_obj):
                    browser_Keywords.local_bk.driver_obj = None
            if hasattr(browser_Keywords.local_bk, 'pid_set'):
                if (browser_Keywords.local_bk.pid_set):
                    del browser_Keywords.local_bk.pid_set[:]
        except Exception as e:
            logger.print_on_console('Exception in stopping server')
            log.error(e)

        try:
            #os.system("killall -9 Safari")
            ## This kills all instances of safari browser even if it is not opened by Avo Assure.
            ## Issue when Avo Assure is opened in Safari browser
            #for id in process_ids:
            #    os.system("killall -9 " + str(id))
            #os.system("killall -9 safaridriver")
            os.system("killall -9 node_appium")
            os.system("killall -9 xcodebuild")
            #os.system("killall -9 chromedriver")
            #os.system("killall -9 geckodriver")
        except Exception as e:
            logger.print_on_console('Exception in stopping server')
            log.error(e)
        log.info('Stale processes killed')
        logger.print_on_console('Stale processes killed')
    elif SYSTEM_OS == 'Linux':
        stale_process_killed=False
        log.info("killing stale process in linux")
        try:
            import browser_Keywords
            if browser_Keywords.linux_drivermap != []:
                for brwdriver in browser_Keywords.linux_drivermap:
                    brwdriver.quit()
                del browser_Keywords.linux_drivermap[:]
            for driver in browser_Keywords.drivermap:
                driver.quit()
            del browser_Keywords.drivermap[:]
            if hasattr(browser_Keywords.local_bk, 'driver_obj'):
                if (browser_Keywords.local_bk.driver_obj):
                    browser_Keywords.local_bk.driver_obj = None
            if hasattr(browser_Keywords.local_bk, 'pid_set'):
                if (browser_Keywords.local_bk.pid_set):
                    del browser_Keywords.local_bk.pid_set[:]
            stale_process_killed=True
        except Exception as e:
            if isinstance(e,ModuleNotFoundError):
                logger.print_on_console('No stale process to kill')
                log.error(e,exc_info=True)
        if stale_process_killed:
            log.info('Stale process Killed')
            logger.print_on_console('Stale process killed')

    else:
        try:
            import browser_Keywords
            for driver in browser_Keywords.drivermap:
                driver.quit()
            del browser_Keywords.drivermap[:]
            if hasattr(browser_Keywords.local_bk, 'driver_obj'):
                if (browser_Keywords.local_bk.driver_obj):
                    browser_Keywords.local_bk.driver_obj = None
            if hasattr(browser_Keywords.local_bk, 'pid_set'):
                if (browser_Keywords.local_bk.pid_set):
                    del browser_Keywords.local_bk.pid_set[:]
        except Exception as e:
            log.error(e)
        tries = {}
        while(len(process_ids) > 0):
            try:
                id = process_ids.pop()
                if id in tries and tries[id] >= 3:
                    logger.print_on_console("Unable to kill process wit PID: " + str(id))
                    continue
                elif id in tries:
                    tries[id] += 1
                else:
                    tries[id] = 1
                process_ids.append(id)
                os.system("TASKKILL /F /T /PID " + str(id))
                process_ids.pop()
            except Exception as e:
                log.error(e)
            # my_processes = ['msedgedriver.exe','MicrosoftWebDriver.exe','MicrosoftEdge.exe','chromedriver.exe','IEDriverServer.exe','IEDriverServer64.exe','CobraWinLDTP.exe','phantomjs.exe','geckodriver.exe']
            # wmi=win32com.client.GetObject('winmgmts:')
            # for p in wmi.InstancesOf('win32_process'):
            #     if p.pid in process_ids:
            #         os.system("TASKKILL /F /T /IM " + p.pid)


        try:
            import browser_Keywords_MW
            del browser_Keywords_MW.drivermap[:]
            if hasattr(browser_Keywords_MW, 'driver_obj') and hasattr(browser_Keywords_MW, 'device_id'):
                adb=os.environ['ANDROID_HOME']+"\\platform-tools\\adb.exe"
                cmd = adb + ' -s '+ browser_Keywords_MW.device_id +' shell pm clear com.android.chrome '
                s = subprocess.check_output(cmd.split(),universal_newlines=True).strip()
                if (browser_Keywords_MW.driver_obj) and s =='Success':
                    browser_Keywords_MW.driver_obj = None
        except ImportError:pass
        except Exception as e:
            log.error(e)

        try:
            processes = psutil.net_connections()
            for line in processes:
                p =  line.laddr
                if p[1] == 4723:
                    log.info( 'Pid Found' )
                    log.info(line.pid)
                    os.system("TASKKILL /F /PID " + str(line.pid))
        except Exception as e:
            log.error(e)

        try:
            import browser_Keywords
            del browser_Keywords.drivermap[:]
            if hasattr(browser_Keywords.local_bk, 'driver_obj'):
                if (browser_Keywords.local_bk.driver_obj):
                    browser_Keywords.local_bk.driver_obj = None
            if hasattr(browser_Keywords.local_bk, 'pid_set'):
                if (browser_Keywords.local_bk.pid_set):
                    pidset = browser_Keywords.local_bk.pid_set
                    ##processes = psutil.net_connections()
                    for pid in pidset:
                        log.info( 'Pid Found' )
                        log.info(pid)
                        try:
                            os.system("TASKKILL /F /T /PID " + str(pid))
                        except Exception as e:
                            log.error(e)
                del browser_Keywords.local_bk.pid_set[:]
        except ImportError: pass
        except Exception as e:
            log.error(e,exc_info=True)
        time.sleep(3)
        try:
            folder = tempfile.gettempdir()
            profdir = ["~DF","scoped_dir","IE","chrome_","anonymous", "userprofile",
                        "seleniumSslSupport","webdriver-ie", "Low", "screenshot",
                        "_MEI", "CVR","tmp","jar_cache","DMI","~nsu","moz-","gen"]
            for the_file in os.listdir(folder):
                folderwithnum = ''

                try:
                    folderwithnum = int(the_file[0:3])
                except:
                    pass

                for name in profdir:
                    if the_file.startswith(name) or isinstance(folderwithnum,int):

                        try:
                            file_path = os.path.join(folder, the_file)
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                                break
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path,ignore_errors=True)
                                break
                        except:
                            pass

        except Exception as e:
            log.error('Error while deleting file/folder')
            log.error(e)

        log.info('Stale processes killed')
        logger.print_on_console( 'Stale processes killed')
