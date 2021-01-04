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
import logger
import json
from constants import *
import dynamic_variable_handler
import reporting
import core_utils
import recording
from logging.handlers import TimedRotatingFileHandler
local_cont = threading.local()
#index for iterating the teststepproperty for executor
##i = 0
terminate_flag=False
manual_terminate_flag=False
pause_flag=False
iris_flag = True
iris_constant_step = -1
socket_object = None
saucelabs_count = 0
# test_case_number = 0
log = logging.getLogger("controller.py")
status_percentage = {TEST_RESULT_PASS:0,TEST_RESULT_FAIL:0,TERMINATE:0,"total":0}
process_ids = []
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
        local_cont.generic_dispatcher_obj = None
        local_cont.test_case_number = 0
        self.action=None
        core_utils.get_all_the_imports(CORE)
        self.cur_dir= os.getcwd()
        self.previous_step=''
        self.verify_dict={'web':VERIFY_EXISTS,
        'oebs':VERIFY_VISIBLE,'sap':VERIFY_EXISTS,'desktop':VERIFY_EXISTS,'mobileweb':VERIFY_EXISTS}
        self.dynamic_var_handler_obj=dynamic_variable_handler.DynamicVariables()
        self.status=TEST_RESULT_FAIL
        self.scenario_start_time=''
        self.scenario_end_time=''
        self.scenario_ellapsed_time=''
        self.reporting_obj=reporting.Reporting()
        self.conthread=None
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
        self.__load_generic()

    def __load_generic(self):
        try:
            if local_cont.generic_dispatcher_obj==None:
                core_utils.get_all_the_imports('Generic')
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
                else:
                    core_utils.get_all_the_imports('Mobility')
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
                else:
                    core_utils.get_all_the_imports('Mobility')
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
            if iris_flag:
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
            if iris_flag:
                core_utils.get_all_the_imports('IRIS')
            import web_dispatcher
            local_cont.web_dispatcher_obj = web_dispatcher.Dispatcher()
            local_cont.web_dispatcher_obj.exception_flag=self.exception_flag
            local_cont.web_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading Web plugin')
            log.error(e)

    def __load_desktop(self):
        try:
            core_utils.get_all_the_imports('Desktop')
            if iris_flag:
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
            if iris_flag:
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

    def methodinvocation(self,index,*args):
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
                        logger.print_on_console('Step Execution start time is : '+start_time_string)
                        log.info('Step Execution start time is : '+start_time_string)
                        index,result = self.keywordinvocation(index,inpval,self.reporting_obj,*args)
                        if tsp.name.lower()=='verifytextiris':
                            #testcase_details_orig=tsp.testcase_details
                            testcase_details=tsp.testcase_details
                            if testcase_details=='':
                                testcase_details={'actualResult_pass':'','testcaseDetails':'','actualResult_fail':''}
                            elif type(testcase_details)==str:
                                testcase_details=ast.literal_eval(testcase_details)
                            new_array=result[2]
                            if new_array[0]==None:
                                new_array[0]='null'
                            if new_array[1]==None:
                                new_array[1]='null'
                            if new_array[0]=='':
                                new_array[0]='  '
                            if new_array[1]=='':
                                new_array[1]='  '
                            testcase_details['testcaseDetails']=new_array[1]
                            testcase_details['actualResult_pass']=new_array[0]
                            testcase_details['actualResult_fail']=new_array[0]
                            tsp.testcase_details=testcase_details

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
                                index = tsp.performdataparam(inpval,self,self.reporting_obj)
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
        if ignore_stat:
            statusflag=True
        if keyword_flag:
            end_time = datetime.now()
            end_time_string=end_time.strftime(TIME_FORMAT)
            logger.print_on_console('Step Execution end time is : '+end_time_string)
            ellapsed_time=end_time-start_time
            logger.print_on_console('Step Elapsed time is : ',str(ellapsed_time)+'\n')
            #Changing the overallstatus of the scenario if it's Fail or Terminate
            if self.status == TEST_RESULT_FAIL :
                if not statusflag:
                    self.reporting_obj.overallstatus=self.status
            elif self.status == TERMINATE:
                self.reporting_obj.overallstatus=self.status
        if self.action==EXECUTE:
            # self.reporting_obj.generate_report_step(tsp,self.status,tsp.name+' EXECUTED and the result is  '+self.status,ellapsed_time,keyword_flag,result[3])
            if statusflag:
                self.reporting_obj.generate_report_step(tsp,'',self,ellapsed_time,keyword_flag,result,ignore_stat,inpval)
            else:
                self.reporting_obj.generate_report_step(tsp,self.status,self,ellapsed_time,keyword_flag,result,ignore_stat,inpval)
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
        inpval = []
        input_list = input[0].split(SEMICOLON)
        if IGNORE_THIS_STEP in input_list:
            ignore_status=True
        if keyword.lower() in [IF,ELSE_IF,EVALUATE]:
            inpval=self.dynamic_var_handler_obj.simplify_expression(input,keyword,self)
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
            if keyword.lower() not in [CREATE_DYN_VARIABLE]:
                inpval[0]=self.dynamic_var_handler_obj.replace_dynamic_variable(inpval[0],keyword,self)
            if len(inpval)>1 and keyword.lower() in [COPY_VALUE,MODIFY_VALUE]:
                inpval[1]=self.dynamic_var_handler_obj.replace_dynamic_variable(inpval[1],'',self)
        else:
            if keyword.lower() in WS_KEYWORDS or keyword.lower() == 'navigatetourl':
                input_list=[input[0]]
            for x in input_list:
                if STATIC_NONE in x:
                    x=None
                else:
                    #To Handle dynamic variables of DB keywords,controller object is sent to dynamicVariableHandler
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
                        exception_list = ['getxmlblockdata','findimageinpdf','comparepdfs','getallvalues']
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
        if tsp.apptype.lower()=='generic' and (tsp.name.lower()=='savetoclipboard' or tsp.name.lower()=='getfromclipboard'):
            if result[2]!='9cc33d6fe25973868b30f4439f09901a':
                logger.print_on_console('Result obtained is: ',result[2])
            elif result:
                logger.print_on_console('Result obtained is: ',result[1])
        if tsp.name.lower()=='find':
            keyword_response=result[1]
            result = result[:1] + (result[2],) + result[2:]
        if len(output)>0 and output[0] != '':
            self.dynamic_var_handler_obj.store_dynamic_value(output[0],keyword_response,tsp.name)
        if len(output)>1:
            self.dynamic_var_handler_obj.store_dynamic_value(output[1],result[1],tsp.name)

    def keywordinvocation(self,index,inpval,*args):
        global socket_object,iris_constant_step,status_percentage
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
                    result = self.invokewebkeyword(teststepproperty,local_cont.web_dispatcher_obj,inpval,args[0],iris_flag)
                elif teststepproperty.apptype.lower() == APPTYPE_MOBILE:
                    #MobileWeb apptype module call
                    if self.mobile_web_dispatcher_obj == None:
                        self.__load_mobile_web()
                    result = self.invokemobilekeyword(teststepproperty,self.mobile_web_dispatcher_obj,inpval,args[0])
                elif teststepproperty.apptype.lower() == APPTYPE_MOBILE_APP:
                    #MobileApp apptype module call
                    if self.mobile_app_dispatcher_obj==None:
                        self.__load_mobile_app()
                    result = self.invokemobileappkeyword(teststepproperty,self.mobile_app_dispatcher_obj,inpval,args[0], iris_flag)
                elif teststepproperty.apptype.lower() == APPTYPE_WEBSERVICE:
                    #Webservice apptype module call
                    if self.webservice_dispatcher_obj == None:
                        self.__load_webservice()
                    result = self.invokewebservicekeyword(teststepproperty,self.webservice_dispatcher_obj,inpval,socket_object)
                elif teststepproperty.apptype.lower() == APPTYPE_DESKTOP:
                    #Desktop apptype module call
                    if self.desktop_dispatcher_obj == None:
                        self.__load_desktop()
                    result = self.invokeDesktopkeyword(teststepproperty,self.desktop_dispatcher_obj,inpval,iris_flag)
                    #----------------------------------------------------------------------------------------------SAP change
                elif teststepproperty.apptype.lower() == APPTYPE_SAP:
                    #SAP apptype module call
                    if self.sap_dispatcher_obj == None:
                        self.__load_sap()
                    result = self.invokeSAPkeyword(teststepproperty,self.sap_dispatcher_obj,inpval,iris_flag)
                #----------------------------------------------------------------------------------------------SAP change
                elif teststepproperty.apptype.lower() == APPTYPE_DESKTOP_JAVA:
                    #OEBS apptype module call
                    if self.oebs_dispatcher_obj == None:
                        self.__load_oebs()
                    result = self.invokeoebskeyword(teststepproperty,self.oebs_dispatcher_obj,inpval,iris_flag)
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
                    result = self.invokepdfkeyword(teststepproperty,self.pdf_dispatcher_obj,inpval,iris_flag)
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
            log.info(result)
            self.keyword_status=TEST_RESULT_FAIL
            if result!=TERMINATE:
                self.store_result(result,teststepproperty)
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
            if(self.keyword_status=='Pass'): setcolor="GREEN"
            elif(self.keyword_status=='Fail') : setcolor="RED"
            logger.print_on_console(keyword+' executed and the status is '+self.keyword_status+'\n',color=setcolor)
            log.info(keyword+' executed and the status is '+self.keyword_status+'\n')
            #Checking for stop keyword
            if teststepproperty.name.lower()==STOP:
                ## Issue #160
                index=STOP
            return index,result
        else:
            return index,TERMINATE

    def executor(self,tsplist,action,last_tc_num,debugfrom_step,mythread,*args):
        global status_percentage
        status_percentage = {TEST_RESULT_PASS:0,TEST_RESULT_FAIL:0,TERMINATE:0,"total":0}
        i=0
        status=True
        self.scenario_start_time=datetime.now()
        start_time_string=self.scenario_start_time.strftime(TIME_FORMAT)
        logger.print_on_console('Scenario Execution start time is : '+start_time_string,'\n')
        global pause_flag
        if local_cont.generic_dispatcher_obj is not None and local_cont.generic_dispatcher_obj.action is None:
            local_cont.generic_dispatcher_obj.action=action
        while (i < len(tsplist)):
            #Check for 'terminate_flag' before execution
            if not(terminate_flag):
                #Check for 'pause_flag' before execution
                if pause_flag:
                    self.pause_execution()
                self.last_tc_num=last_tc_num
                self.debugfrom_step=debugfrom_step
                try:
                    i = self.methodinvocation(i)
                    if i== TERMINATE:
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
        return status,status_percentage

    def invokegenerickeyword(self,teststepproperty,dispatcher_obj,inputval):
        res = dispatcher_obj.dispatcher(teststepproperty,self.wx_object,self.conthread,*inputval)
        return res

    def invokesystemkeyword(self,teststepproperty,dispatcher_obj,inputval):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval)
        return res

    def invokeoebskeyword(self,teststepproperty,dispatcher_obj,inputval,iris_flag):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,iris_flag,self.conthread)
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

    def invokewebkeyword(self,teststepproperty,dispatcher_obj,inputval,reporting_obj,iris_flag):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.reporting_obj,iris_flag,self.wx_object,self.conthread)
        return res

    def invokemobilekeyword(self,teststepproperty,dispatcher_obj,inputval,reporting_obj):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.reporting_obj,self.conthread)
        return res

    def invokemobileappkeyword(self,teststepproperty,dispatcher_obj,inputval,reporting_obj, iris_flag):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.reporting_obj, iris_flag,self.conthread)
        return res

    def invokeDesktopkeyword(self,teststepproperty,dispatcher_obj,inputval,iris_flag):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,iris_flag,self.conthread)
        return res

    def invokeSAPkeyword(self,teststepproperty,dispatcher_obj,inputval,iris_flag):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,iris_flag,self.conthread)
        return res

    def invokemainframekeyword(self,teststepproperty,dispatcher_obj,inputval):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.conthread)
        return res

    def invokepdfkeyword(self, teststepproperty, dispatcher_obj,inputval,iris_flag):
        res = dispatcher_obj.dispatcher(teststepproperty, inputval, iris_flag)
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
        for testcase in scenario:
            flag,browser_type,last_tc_num,testcase_empty_flag,empty_testcase_names=obj.parse_json(testcase)
            if flag == False:
                break
            print('\n')
            tsplist = obj.read_step()
            for k in range(len(tsplist)):
                if tsplist[k].name.lower() == 'openbrowser' and tsplist[k].apptype.lower()=='web' and (IGNORE_THIS_STEP not in tsplist[k].inputval[0].split(';')):
                    tsplist[k].inputval = browser_type
        if flag:
            if runfrom_step > 0 and runfrom_step <= tsplist[len(tsplist)-1].stepnum:
                self.conthread=mythread
                status,status_percentage = self.executor(tsplist,DEBUG,last_tc_num,runfrom_step,mythread)
            else:
                logger.print_on_console( 'Invalid step number!! Please provide run from step number from 1 to ',tsplist[len(tsplist)-1].stepnum,'\n')
                log.info('Invalid step number!! Please provide run from step number')
        else:
            logger.print_on_console('Invalid script')
        temp={}
        if (handler.local_handler.awsKeywords):
            for k,v in handler.local_handler.awsKeywords.items():
                if list(v) != []:
                    temp[k]=list(v)
            handler.local_handler.awsKeywords=temp
            if (handler.local_handler.awsKeywords):
                logger.print_on_console("***Following Testcases are not AWS Compatible because of the following keywords :***")
                log.info("***Following Testcases are not AWS Compatible because of the following keywords :***")
                for k,v in handler.local_handler.awsKeywords.items():
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
        return status

    def invoke_execution(self,mythread,json_data,socketIO,wxObject,configvalues,qcObject,qtestObject,zephyrObject,aws_mode):
        global terminate_flag,status_percentage,saucelabs_count
        qc_url=''
        qc_password=''
        qc_username=''
        zephyr_accNo=''
        zephyr_secKey=''
        zephyr_acKey=''        
        con = Controller()
        obj = handler.Handler()
        status=COMPLETED
        aws_tsp=[]
        aws_scenario=[]
        step_results=[]
        scen_id=[]
        condition_check_flag = False
        testcase_empty_flag = False
        count = 0
        info_msg=''
        # t = test.Test()
        # suites_list,flag = t.gettsplist()
        #Getting all the details by parsing the json_data
        suiteId_list,suite_details,browser_type,scenarioIds,suite_data,execution_ids,batch_id,condition_check,dataparam_path,self.execution_mode,qc_creds=obj.parse_json_execute(json_data)
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
            flag=True
            if terminate_flag:
                status=TERMINATE
            log.info('---------------------------------------------------------------------')
            print('=======================================================================================================')
            log.info('***SUITE '+str(suite_idx) +' EXECUTION STARTED***')
            logger.print_on_console('***SUITE ', str(suite_idx) ,' EXECUTION STARTED***')
            log.info('---------------------------------------------------------------------')
            print('=======================================================================================================')
            do_not_execute = False
            #Check for the disabled scenario
            if not (do_not_execute):
                if aws_mode:
                    pytest_files=[]
                 #Logic to Execute each suite for each of the browser
                for browser in browser_type[suite_id]:
                    sc_idx = 0
                    condition_check_flag = False
                    #Logic to iterate through each scenario in the suite
                    for scenario,scenario_id,condition_check_value,dataparam_path_value in zip(suite_id_data,scenarioIds[suite_id],condition_check[suite_id],dataparam_path[suite_id]):
                        execute_flag=True
                        con.reporting_obj=reporting.Reporting()
                        con.configvalues=configvalues
                        con.exception_flag=self.exception_flag
                        con.wx_object=wxObject
                        handler.local_handler.tspList=[]
                        execute_result_data = {
                            'testsuiteId': suite_id,
                            'scenarioId': scenario_id,
                            'batchId': batch_id,
                            'executionId': execution_ids[suite_idx-1],
                            'reportData': None}
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
                            if(qc_creds["alm"]["url"] != "" and len(scenario["qcdetails"]) != 0):
                                qc_username=qc_creds['alm']['username']
                                qc_password=qc_creds['alm']['password']
                                qc_url=qc_creds['alm']['url']
                                qc_sceanrio_data=scenario['qcdetails'][integ]
                                integ += 1
                            # if('integrationType' in qc_creds and qc_creds['integrationType'] == 'qTest'):
                            if(qc_creds["qtest"]["url"] != "" and len(scenario["qcdetails"]) != 0):
                                qtest_username=qc_creds["qtest"]["username"]
                                qtest_password=qc_creds["qtest"]["password"]
                                qtest_url=qc_creds["qtest"]["url"]
                                qtest_stepsup=qc_creds["qtest"]["qteststeps"]
                                qc_sceanrio_data=scenario['qcdetails'][integ]
                                integ += 1
                                qtest_project=qc_sceanrio_data['qtestproject']
                                qtest_projectid=qc_sceanrio_data['qtestprojectid']
                                qtest_suite=qc_sceanrio_data['qtestsuite']
                                qtest_suiteid=qc_sceanrio_data['qtestsuiteid']
                            # if('integrationType' in qc_creds and qc_creds['integrationType'] == 'Zephyr'):
                            if(qc_creds["zephyr"]["accountid"] != "" and len(scenario["qcdetails"]) != 0):
                                zephyr_acKey=qc_creds["zephyr"]["accesskey"]
                                zephyr_secKey=qc_creds["zephyr"]["secretkey"]
                                zephyr_accNo=qc_creds["zephyr"]["accountid"]
                                zephyr_sceanrio_data=scenario['qcdetails'][integ]
                                integ += 1
                                zephyr_cycleid=zephyr_sceanrio_data['cycleid']
                                zephyr_projectid=zephyr_sceanrio_data['projectid']
                                zephy_versionid=zephyr_sceanrio_data['versionid']
                                zephy_testid=zephyr_sceanrio_data['testid']  
                                zephy_issueid=zephyr_sceanrio_data['issueid']                       
                                
                            #Iterating through each test case in the scenario
                            for testcase in [eval(scenario[scenario_id])]:
                                #check for temrinate flag before parsing tsp list
                                if terminate_flag:
                                    break
                                flag,_,last_tc_num,testcase_empty_flag,empty_testcase_names=obj.parse_json(testcase,dataparam_path_value)
                                if flag == False:
                                    break
                                print('\n')
                                if (True in testcase_empty_flag):
                                    if(condition_check_value==1):
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
                            if execution_env == 'saucelabs':
                                self.__load_web()
                                import script_generator
                                scenario_name=json_data['suitedetails'][suite_idx-1]["scenarioNames"][sc_idx]
                                if not terminate_flag:
                                    saucelabs_obj=script_generator.SauceLabs_Operations(scenario_name,str(saucelabs_count))
                                    status=saucelabs_obj.complie_TC(tsplist,scenario_name,browser,str(saucelabs_count),execute_result_data,socketIO)
                                if status==TERMINATE:
                                    terminate_flag=True
                                    msg='***Scenario'+str(sc_idx+ 1)+': '+scenario_name+' is Terminated ***'
                                    logger.print_on_console(msg)
                                else:
                                    print('=======================================================================================================')
                                    logger.print_on_console( '***Scenario' ,str(sc_idx + 1) ,' execution completed***')
                                    print('=======================================================================================================')
                                saucelabs_count += 1
                                sc_idx += 1
                                execute_flag=False
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
                                    status,status_percentage = con.executor(tsplist,EXECUTE,last_tc_num,1,con.conthread,video_path)
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
                                    if con.reporting_obj.report_json[ROWS]==[] and con.reporting_obj.report_json[OVERALLSTATUS]==[]:
                                        con.reporting_obj.add_to_reporting_obj()
                                status_percentage["s_index"]=suite_idx-1
                                status_percentage["index"]=sc_idx
                                con.reporting_obj.user_termination=manual_terminate_flag
                                con.reporting_obj.save_report_json(filename,json_data,status_percentage)
                                execute_result_data["reportData"] = con.reporting_obj.report_json
                                socketIO.emit('result_executeTestSuite', execute_result_data)
                                obj.clearList(con)
                                sc_idx += 1
                                #logic for condition check
                                report_json=con.reporting_obj.report_json[OVERALLSTATUS]

                                #Check is made to fix issue #401
                                if len(report_json)>0:
                                    overall_status=report_json[0][OVERALLSTATUS]
                                    if(condition_check_value==1):
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
                                socketIO.emit('result_executeTestSuite', execute_result_data)
                                obj.clearList(con)
                                sc_idx += 1
                                report_json=con.reporting_obj.report_json_condition_check_testcase_empty[OVERALLSTATUS]
                            # if integration_type!="qTest" and integration_type!="Zephyr" and len(scenario['qcdetails'])==10 and (qc_url!='' and qc_password!='' and  qc_username!=''):
                            if  len(scenario['qcdetails'])!=0 and qc_creds['alm']['url'] != '':
                                if type(qc_sceanrio_data) is not list:
                                    qc_domain=qc_sceanrio_data['qcdomain']
                                    qc_project=qc_sceanrio_data['qcproject']
                                    qc_folder=qc_sceanrio_data['qcfolderpath']
                                    qc_tsList=qc_sceanrio_data['qctestset']
                                    qc_testrunname=qc_sceanrio_data['qctestcase']
                                    qc_status_over=report_json[0]
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
                                        qc_tsList=qc_sceanrio_data[i]['qctestset']
                                        qc_testrunname=qc_sceanrio_data[i]['qctestcase']
                                        qc_status_over=report_json[0]
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
                            if len(scenario['qcdetails'])!=0 and qc_creds['qtest']['url'] != '':
                                qtest_status_over=report_json[0]
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

                            # if (integration_type=="Zephyr" and zephyr_accNo!='' and zephyr_secKey!='' and  zephyr_acKey!=''):
                            if len(scenario['qcdetails'])!=0 and qc_creds['zephyr']['accountid'] != '':
                                zephyr_status_over=report_json[0]
                                try:
                                    zephyr_status = {}
                                    zephyr_status['zephyraction']='zephyrupdate'
                                    zephyr_status['cycleId']=zephyr_cycleid
                                    zephyr_status['testId']=zephy_testid
                                    zephyr_status['issueId']=zephy_issueid
                                    zephyr_status['projectId']=zephyr_projectid
                                    zephyr_status['versionId']=zephy_versionid
                                    zephyr_status['zephyr_accNo']=zephyr_accNo
                                    zephyr_status['zephyr_acKey']=zephyr_acKey
                                    zephyr_status['zephyr_secKey']=zephyr_secKey
                                    zephyr_update_status=zephyr_status_over['overallstatus']
                                    zephyr_status['status']={}
                                    if(zephyr_update_status.lower()=='pass'):
                                        zephyr_status['status']['id']='1'
                                    elif(zephyr_update_status.lower()=='fail'):
                                        zephyr_status['status']['id']='2'
                                    elif(zephyr_update_status.lower()=='terminate'):
                                        zephyr_status['status']['id']='5'
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
                            socketIO.emit('result_executeTestSuite', execute_result_data)
                            obj.clearList(con)
                            sc_idx += 1
                            #logic for condition check
                            report_json=con.reporting_obj.report_json[OVERALLSTATUS]
                        time.sleep(1)
            if aws_mode and not terminate_flag:
                tc_obj.make_zip(pytest_files)
                execution_status,step_results=self.aws_obj.run_aws_android_tests()
                self.aws_report(aws_tsp,aws_scenario,step_results,suite_idx,execute_result_data,con.reporting_obj,json_data,socketIO)
                if not(execution_status):
                    status=TERMINATE
            log.info('---------------------------------------------------------------------')
            print('=======================================================================================================')
            log.info('***SUITE '+ str(suite_idx) +' EXECUTION COMPLETED***')
            #clearing dynamic variables at the end of execution to support dynamic variable at the scenario level
            obj.clear_dyn_variables()
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
            obj_reporting.overallstatus_array=[]
            obj_reporting.overallstatus=TEST_RESULT_PASS
            obj_reporting.report_json[ROWS]=obj_reporting.report_string
            obj_reporting.report_json[OVERALLSTATUS]=obj_reporting.overallstatus_array
            tc_aws=aws_tsp[sc_idx]
            os.chdir(self.cur_dir)
            filename='Scenario'+str(sc_idx+1)+'.json'
            for tsp in tc_aws:
                if tsp.name=='LaunchApplication':
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

    def invoke_controller(self,action,mythread,debug_mode,runfrom_step,json_data,root_obj,socketIO,qc_soc,qtest_soc,zephyr_soc,*args):
        status = COMPLETED
        global socket_object
        self.conthread=mythread
        self.clear_data()
        wxObject = root_obj.cw
        socket_object = socketIO
        #Logic to make sure that logic of usage of existing driver is not applicable to execution
        if local_cont.web_dispatcher_obj != None:
            local_cont.web_dispatcher_obj.action=action
        if action==EXECUTE:
            if len(args)>0:
                aws_mode=args[0]
            self.execution_mode = json_data['exec_mode'].lower()
            kill_process()
            if self.execution_mode == SERIAL:
                status=self.invoke_execution(mythread,json_data,socketIO,wxObject,self.configvalues,qc_soc,qtest_soc,zephyr_soc,aws_mode)
            elif self.execution_mode == PARALLEL:
                status = self.invoke_parralel_exe(mythread,json_data,socketIO,wxObject,self.configvalues,qc_soc,qtest_soc,zephyr_soc,aws_mode)
        elif action==DEBUG:
            self.debug_choice=wxObject.choice
            self.debug_mode=debug_mode
            self.wx_object=wxObject
            status=self.invoke_debug(mythread,runfrom_step,json_data)
        if status != TERMINATE:
            status=COMPLETED
        return status

    def invoke_parralel_exe(self,mythread,json_data,socketIO,wxObject,configvalues,qc_soc,qtest_soc,zephyr_soc,aws_mode):
        try:
            import copy
            browsers_data = json_data['suitedetails'][0]['browserType']
            jsondata_dict = {}
            th={}
            log1 = logging.getLogger("controller.py") #Disable loggers from imported modules
            if(log1.handlers):
                log1.handlers.clear()
            for i in range (len(browsers_data)):
                jsondata_dict[i] = copy.deepcopy(json_data)
                for j in range(len(jsondata_dict[i]['suitedetails'])):
                    jsondata_dict[i]['suitedetails'][j]['browserType'] = [browsers_data[i]]
                thread_name = "test_thread_browser" + str(browsers_data[i])
                th[i] = threading.Thread(target = self.invoke_execution, name = thread_name, args = (mythread,jsondata_dict[i],socketIO,wxObject,configvalues,qc_soc,qtest_soc,zephyr_soc,aws_mode))
                self.seperate_log(th[i], browsers_data[i]) #function that creates different logs for each browser
                th[i].start()
            for i in th:
                th[i].join()
            for i in th:
                while th[i].is_alive(): pass
        except Exception as e:
            logger.print_on_console("Exception in Parallel Execution")
            log.error("Exception in Parallel Execution. Error: " + str(e))
        if not(terminate_flag):
            status = COMPLETED
        return status
        
    def seperate_log(self, cur_thread, id):
        try:
            log = logging.getLogger("controller.py")
            browser_name = {'1':'Chrome', '2':'FireFox', '3':'IE', '6': 'Safari', '7':'EdgeLegacy', '8':'EdgeChromium'}
            log_filepath = os.path.normpath(os.path.dirname(self.configvalues["logFile_Path"]) + os.sep + 'TestautoV2_Parallel_' + str(browser_name[id]) + '.log').replace("\\","\\\\")
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
    import os,shutil
    if SYSTEM_OS == 'Darwin':
        try:
            import browser_Keywords_MW
            browser_Keywords_MW.driver_obj.quit()
        except ImportError: pass
        except Exception as e:
            logger.print_on_console('Error in stopping scraping driver as driver is already closed')
            log.error(e)


        try:
            import install_and_launch
            install_and_launch.driver.quit()
        except ImportError: pass
        except Exception as e:
            logger.print_on_console('Error in stopping application driver as driver is already closed')
            log.error(e)

        try:
            import browser_Keywords
            del browser_Keywords.drivermap[:]
            if hasattr(browser_Keywords.local_bk, 'driver_obj'):
                if (browser_Keywords.local_bk.driver_obj):
                    browser_Keywords.local_bk.driver_obj = None
            if hasattr(browser_Keywords.local_bk, 'pid_set'):
                if (browser_Keywords.local_bk.pid_set):
                    del browser_Keywords.local_bk.pid_set[:]
        except Exception as e:
            log.error(e)

        try:
            # os.system("killall -9 Safari")
                # This kills all instances of safari browser even if it is not opened by Avo Assure.
                # Issue when Avo Assure is opened in Safari browser
            for id in process_ids:
                os.system("kilall -9 " + id)
            # os.system("killall -9 safaridriver")
            # os.system("killall -9 node_appium")
            # os.system("killall -9 xcodebuild")
            # os.system("killall -9 chromedriver")
            # os.system("killall -9 geckodriver")
        except Exception as e:
            logger.print_on_console('Exception in stopping server')
            log.error(e)
        log.info('Stale processes killed')
        logger.print_on_console('Stale processes killed')
    else:
        try:
            import win32com.client
            for id in process_ids:
                os.system("TASKKILL /F /T /PID " + str(id))
                process_ids.remove(id)
            # my_processes = ['msedgedriver.exe','MicrosoftWebDriver.exe','MicrosoftEdge.exe','chromedriver.exe','IEDriverServer.exe','IEDriverServer64.exe','CobraWinLDTP.exe','phantomjs.exe','geckodriver.exe']
            # wmi=win32com.client.GetObject('winmgmts:')
            # for p in wmi.InstancesOf('win32_process'):
            #     if p.pid in process_ids:
            #         os.system("TASKKILL /F /T /IM " + p.pid)
        except Exception as e:
            log.error(e)

        try:
            import browser_Keywords_MW
            del browser_Keywords_MW.drivermap[:]
            if hasattr(browser_Keywords_MW, 'driver_obj'):
                if (browser_Keywords_MW.driver_obj):
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
                    os.system("TASKKILL /F /T /PID " + str(line.pid))
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
