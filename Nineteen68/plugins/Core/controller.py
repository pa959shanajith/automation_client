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
import if_step
import for_step
import getparam
import jumpTo
import jumpBy
from teststepproperty import TestStepProperty
from generickeywordresult import GenericKeywordResult
import test_debug
import test
import handler
import os,sys
import logger
import json
from constants import *
import pause_execution
import dynamic_variable_handler
import reporting
import core_utils
from concurrent.futures import ThreadPoolExecutor
import threading
from datetime import datetime
import logging
import time
import platform
#index for iterating the teststepproperty for executor
i = 0
#Terminate Flag
terminate_flag=False
pause_flag=False
iris_flag = False
iris_constant_step = -1
break_point=-1
socket_object = None
thread_tracker = []
log = logging.getLogger("controller.py")


class TestThread(threading.Thread):
    """Test Worker Thread Class."""
    #----------------------------------------------------------------------
    def __init__(self,browser,mythread):
        """Init Worker Thread Class."""
        logger.print_on_console( 'Browser number: ',browser)
        log.debug('Browser number:  %d',browser)
        threading.Thread.__init__(self)
        self.browser = browser
        self.thread=mythread
        self.start()    # start the thread
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        try:
            time.sleep(2)
            con = Controller()
            con.conthread=self.thread
            status = con.invoke_controller(EXECUTE,'',con.conthread,self.browser)
            if status==TERMINATE:
                logger.print_on_console( '---------Termination Completed-------')
            else:
                logger.print_on_console('***SUITE EXECUTION COMPLETED***')
        except Exception as m:
            log.error(m)


class Controller():
    generic_dispatcher_obj = None
    mobile_web_dispatcher_obj = None
    web_dispatcher_obj = None
    oebs_dispatcher_obj = None
    webservice_dispatcher_obj = None
    outlook_dispatcher_obj = None
    desktop_dispatcher_obj = None
    sap_dispatcher_obj = None
    mobile_app_dispatcher_obj = None
    mainframe_dispatcher_obj = None
    system_dispatcher_obj = None
    def __init__(self):
        self.get_all_the_imports(CORE)
        self.__load_generic()
        self.cur_dir= os.getcwd()
        self.previous_step=''
        self.verify_dict={'web':VERIFY_EXISTS,
        'desktopjava':VERIFY_VISIBLE,'sap':VERIFY_EXISTS,'desktop':VERIFY_EXISTS}
        self.dynamic_var_handler_obj=dynamic_variable_handler.DynamicVariables()
        self.status=TEST_RESULT_FAIL
        self.scenario_start_time=''
        self.scenario_end_time=''
        self.scenario_ellapsed_time=''
        self.reporting_obj=reporting.Reporting()
        self.conthread=None
        self.action=None
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

    def __load_generic(self):
        try:
            if self.generic_dispatcher_obj==None:
                self.get_all_the_imports('ImageProcessing')
                self.get_all_the_imports('Generic')
                import generic_dispatcher
                self.generic_dispatcher_obj = generic_dispatcher.GenericKeywordDispatcher()
        except Exception as e:
            logger.print_on_console('Error loading Generic plugin')
            log.error(e)

    def __load_mobile_web(self):
        try:
            if self.mobile_web_dispatcher_obj==None:
                import platform
                if platform.system() == 'Darwin':
                    self.get_all_the_imports('Mobility/MobileWeb')
                else:
                    self.get_all_the_imports('Mobility')
                import web_dispatcher_MW
                self.mobile_web_dispatcher_obj = web_dispatcher_MW.Dispatcher()
                self.mobile_web_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading MobileWeb plugin')
            log.error(e)

    def __load_mobile_app(self):
        try:
            if self.mobile_app_dispatcher_obj==None:
                import platform
                if platform.system()=='Darwin':
                    self.get_all_the_imports('Mobility/MobileApp')
                else:
                    self.get_all_the_imports('Mobility')
                import mobile_app_dispatcher
                self.mobile_app_dispatcher_obj = mobile_app_dispatcher.MobileDispatcher()
                self.mobile_app_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading MobileApp plugin')
            log.error(e)

    def __load_webservice(self):
        try:
            self.get_all_the_imports('WebServices')
            import websevice_dispatcher
            self.webservice_dispatcher_obj = websevice_dispatcher.Dispatcher()
        except Exception as e:
            logger.print_on_console('Error loading Web services plugin')
            log.error(e)

    def __load_oebs(self):
        try:
            self.get_all_the_imports('Oebs')
            if iris_flag:
                self.get_all_the_imports('IRIS')
            import oebs_dispatcher
            self.oebs_dispatcher_obj = oebs_dispatcher.OebsDispatcher()
            self.oebs_dispatcher_obj.exception_flag=self.exception_flag
            self.oebs_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading OEBS plugin')
            log.error(e)

    def __load_web(self):
        try:
##            self.get_all_the_imports('ImageProcessing')
            self.get_all_the_imports('WebScrape')
            self.get_all_the_imports('Web')
            if iris_flag:
                self.get_all_the_imports('IRIS')
            import web_dispatcher
            self.web_dispatcher_obj = web_dispatcher.Dispatcher()
            self.web_dispatcher_obj.exception_flag=self.exception_flag
            self.web_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading Web plugin')
            log.error(e)

    def __load_desktop(self):
        try:
            self.get_all_the_imports('Desktop')
            if iris_flag:
                self.get_all_the_imports('IRIS')
            import desktop_dispatcher
            self.desktop_dispatcher_obj = desktop_dispatcher.DesktopDispatcher()
            self.desktop_dispatcher_obj.exception_flag=self.exception_flag
            self.desktop_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading Desktop plugin')
            log.error(e)

    def __load_sap(self):
        try:
            self.get_all_the_imports('SAP')
            if iris_flag:
                self.get_all_the_imports('IRIS')
            import sap_dispatcher
            self.sap_dispatcher_obj = sap_dispatcher.SAPDispatcher()
            self.sap_dispatcher_obj.exception_flag=self.exception_flag
            self.sap_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading SAP plugin')
            log.error(e)

    def __load_mainframe(self):
        try:
            self.get_all_the_imports('Mainframe')
            import mainframe_dispatcher
            self.mainframe_dispatcher_obj = mainframe_dispatcher.MainframeDispatcher()
            self.mainframe_dispatcher_obj.exception_flag=self.exception_flag
            self.mainframe_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading Mainframe plugin')
            log.error(e)

    def __load_system(self):
        try:
            self.get_all_the_imports('System')
            import system_dispatcher
            self.system_dispatcher_obj = system_dispatcher.SystemDispatcher()
            self.system_dispatcher_obj.exception_flag=self.exception_flag
            self.system_dispatcher_obj.action=self.action
        except Exception as e:
            logger.print_on_console('Error loading System plugin')
            log.error(e)


    def dangling_status(self,index):
        step=handler.tspList[index]
        return step.executed

    def check_dangling(self,tsp,index):
        status=True
        errormsg=""
        if tsp.__class__.__name__.lower() in [IF,FOR,GETPARAM]:
            info_dict=tsp.info_dict
            if info_dict is not None:
                if tsp.name.lower() in [ENDFOR,ENDLOOP]:
                    index=info_dict[0].keys()[0]
                    status=self.dangling_status(index)
                if tsp.name.lower() in [IF,ELSE_IF,ELSE,ENDIF]:
                    if tsp.name.lower() in [IF]:
                        status= info_dict[-1].values()[0].lower() == ENDIF
                        if not(status):
                            errormsg="Execution Terminated : Dangling if/for/getparam in testcase"
                    elif tsp.name.lower() in [ELSE_IF,ELSE]:
                        status1= info_dict[-1].values()[0] == ENDIF
                        status2= info_dict[0].keys()[0] != index
                        status = status1 and status2
                        if not(status1) and status2:
                            errormsg="Execution Terminated : Dangling if/for/getparam in testcase"
                    elif tsp.name.lower() in [ENDIF]:
                        index=info_dict[-1].keys()[0]
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
        global terminate_flag,pause_flag,iris_constant_step
        terminate_flag=pause_flag=False
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
        tsp = handler.tspList[index]
        testcase_details_orig=tsp.testcase_details
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
                logger.print_on_console('Step number is : ',tsp.stepnum)
                log.info('Step number is : '+str(tsp.stepnum))
                if ignore_stat:
                    teststepproperty = handler.tspList[index]
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
                        if tsp.name=='verifyValues' or tsp.name.lower()=='verifytextiris':
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
##            self.reporting_obj.generate_report_step(tsp,self.status,tsp.name+' EXECUTED and the result is  '+self.status,ellapsed_time,keyword_flag,result[3])
            if statusflag:
                self.reporting_obj.generate_report_step(tsp,'',self,ellapsed_time,keyword_flag,result,ignore_stat,inpval)
            else:
                self.reporting_obj.generate_report_step(tsp,self.status,self,ellapsed_time,keyword_flag,result,ignore_stat,inpval)
            if tsp.name.lower()=='verifyvalues' or tsp.name.lower()=='verifytextiris':
                tsp.testcase_details=testcase_details_orig

##      Issue #160
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
            if len(inpval)>1 and keyword.lower() in [COPY_VALUE,MODIFY_VALUE,CREATE_DYN_VARIABLE]:
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
        if tsp.name.lower()=='verifytextiris':
            display_keyword_response=result[1]
		#To Handle dynamic variables of DB keywords
        if tsp.name.lower() in DATABASE_KEYWORDS:
            if keyword_response != []:
                display_keyword_response='DB data fetched'
        if(tsp.apptype.lower() == 'webservice' and tsp.name.lower() == 'executerequest'):
            if len(display_keyword_response) == 2:
                logger.print_on_console('Response Header: \n',display_keyword_response[0])
                #data size check
                if self.core_utilsobject.getdatasize(display_keyword_response[1],'mb') < 10:
                    if 'soap:Envelope' in display_keyword_response[1]:
                        from lxml import etree
                        root = etree.fromstring(display_keyword_response[1])
                        respBody = etree.tostring(root,pretty_print=True)
                        logger.print_on_console('Response Body: \n',respBody,'\n')
                    else:
                        logger.print_on_console('NON SOAP XML')
                        logger.print_on_console('Response Body: \n',display_keyword_response[1],'\n')
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
                        logger.print_on_console('Result obtained is ',",".join([str(display_keyword_response[i])
                        if not isinstance(display_keyword_response[i],basestring) else display_keyword_response[i] for i in range(len(display_keyword_response))]))
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
                else:
                    logger.print_on_console('Result obtained is ',",".join([str(display_keyword_response[i])
                    if not isinstance(display_keyword_response[i],basestring) else display_keyword_response[i] for i in range(len(display_keyword_response))]))
            else:
                logger.print_on_console('Result obtained exceeds max. Limit, please use writeToFile keyword.')
        log.info('Result obtained is: ')
        log.info(display_keyword_response)
        """if tsp.apptype.lower()=='desktop' or tsp.apptype.lower()=='sap' or tsp.apptype.lower()=='desktopjava' or (tsp.cord!='' and tsp.cord!=None):"""
        if result[2]!='9cc33d6fe25973868b30f4439f09901a' and tsp.name.lower()!='verifytextiris':
            logger.print_on_console('Result obtained is: ',result[2])
        elif result:
            logger.print_on_console('Result obtained is: ',result[1])
        if tsp.apptype.lower()=='generic' and (tsp.name.lower()=='savetoclipboard' or tsp.name.lower()=='getfromclipboard'):
            if result[2]!='9cc33d6fe25973868b30f4439f09901a':
                logger.print_on_console('Result obtained is: ',result[2])
            elif result:
                logger.print_on_console('Result obtained is: ',result[1])
        if len(output)>0 and output[0] != '':
            self.dynamic_var_handler_obj.store_dynamic_value(output[0],keyword_response,tsp.name)
        if len(output)>1:
            self.dynamic_var_handler_obj.store_dynamic_value(output[1],result[1],tsp.name)

    def keywordinvocation(self,index,inpval,*args):
        global socket_object,iris_constant_step
        configvalues = self.configvalues
        try:
            import time
            time.sleep(int(configvalues['stepExecutionWait']))
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
            teststepproperty = handler.tspList[index]
            keyword=teststepproperty.name
            #Custom object implementation for Web
            if teststepproperty.objectname==CUSTOM:
                if self.verify_exists==False:
                    previous_step=handler.tspList[index-1]
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
                teststepproperty_prev = handler.tspList[index-1]
                if teststepproperty_prev.name.lower()!=DRAG:
                    teststepproperty.execute_flag=False
                    result=list(result)
                    result[3]='Drag Keyword is missing'
            elif keyword.lower()==DRAG:
                log.debug('Drag keyword encountered')
                if(index+1)<len(handler.tspList):
                    teststepproperty_next = handler.tspList[index+1]
                    if teststepproperty_next.name.lower()!=DROP:
                        teststepproperty.execute_flag=False
                        result=list(result)
                        result[3]='Drop Keyword is missing'
            #Checking for test step with constant iris object
            if(teststepproperty.cord != '' and teststepproperty.cord != None):
                if (teststepproperty.objectname.split(';')[-1] == 'constant' and keyword.lower() == 'verifyexistsiris'):
                    iris_constant_step = index
                elif iris_constant_step!=-1:
                    tsp = handler.tspList[iris_constant_step]
                    obj_props = tsp.objectname.split(';')
                    coords = [obj_props[2],obj_props[3],obj_props[4],obj_props[5]]
                    teststepproperty.custom_flag = True
                    teststepproperty.parent_xpath = {'cord': tsp.cord, 'coordinates': coords}
            #get the output varible from the teststep property
            if teststepproperty.execute_flag:
                #Check the apptype and pass to perticular module
                if teststepproperty.apptype.lower() == APPTYPE_GENERIC:
                    #Generic apptype module call

                    if self.generic_dispatcher_obj == None:
                        self.__load_generic()
                    result = self.invokegenerickeyword(teststepproperty,self.generic_dispatcher_obj,inpval)

                elif teststepproperty.apptype.lower() == APPTYPE_SYSTEM:
                    #System apptype module call
                    if self.system_dispatcher_obj == None:
                        self.__load_system()
                    result = self.invokesystemkeyword(teststepproperty,self.system_dispatcher_obj,inpval)

                elif teststepproperty.apptype.lower() == APPTYPE_WEB:
                    #Web apptype module call
                    if self.web_dispatcher_obj == None:
                        self.__load_web()
                    result = self.invokewebkeyword(teststepproperty,self.web_dispatcher_obj,inpval,args[0],iris_flag)
                elif teststepproperty.apptype.lower() == APPTYPE_MOBILE:
                    #MobileWeb apptype module call
                    if self.mobile_web_dispatcher_obj == None:
                        self.__load_mobile_web()
                    result = self.invokemobilekeyword(teststepproperty,self.mobile_web_dispatcher_obj,inpval,args[0])
                elif teststepproperty.apptype.lower() == APPTYPE_MOBILE_APP:
                    #MobileApp apptype module call
                    if self.mobile_app_dispatcher_obj==None:
                        self.__load_mobile_app()
                    result = self.invokemobileappkeyword(teststepproperty,self.mobile_app_dispatcher_obj,inpval,args[0])
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
##            logger.print_on_console( 'Result in methodinvocation : ', teststepproperty.name,' : ',temp_result)
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
            logger.print_on_console(keyword+' executed and the status is '+self.keyword_status+'\n')
            log.info(keyword+' executed and the status is '+self.keyword_status+'\n')
            #Checking for stop keyword
            if teststepproperty.name.lower()==STOP:
                ## Issue #160
                index=STOP
            return index,result
        else:
            return index,TERMINATE

    def executor(self,tsplist,action,last_tc_num,debugfrom_step,mythread):
        i=0
        status=True
        self.scenario_start_time=datetime.now()
        start_time_string=self.scenario_start_time.strftime(TIME_FORMAT)
        logger.print_on_console('Scenario Execution start time is : '+start_time_string,'\n')
        global pause_flag
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
                        logger.print_on_console('Terminating the execution')
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
                logger.print_on_console('Terminating the execution')
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
        self.reporting_obj.build_overallstatus(self.scenario_start_time,self.scenario_end_time,self.scenario_ellapsed_time)
        logger.print_on_console('Step Elapsed time is : ',str(self.scenario_ellapsed_time))
        return status

    def invokegenerickeyword(self,teststepproperty,dispatcher_obj,inputval):
        res = dispatcher_obj.dispatcher(teststepproperty,self.wx_object,self.conthread,*inputval)
        return res

    def invokesystemkeyword(self,teststepproperty,dispatcher_obj,inputval):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval)
        return res

    def invokeoebskeyword(self,teststepproperty,dispatcher_obj,inputval,iris_flag):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,iris_flag)
        return res

    def invokewebservicekeyword(self,teststepproperty,dispatcher_obj,inputval,socket_object):
        keyword = teststepproperty.name
        if keyword.lower() == 'settagvalue' or keyword.lower() == 'settagattribute':
            if handler.ws_templates_dict.has_key(teststepproperty.testscript_name):
                handler.ws_template=handler.ws_templates_dict[teststepproperty.testscript_name]
            else:
                handler.ws_template=''
        res = dispatcher_obj.dispatcher(teststepproperty,socket_object,*inputval)
        return res

    def invokewebkeyword(self,teststepproperty,dispatcher_obj,inputval,reporting_obj,iris_flag):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.reporting_obj,iris_flag)
        return res

    def invokemobilekeyword(self,teststepproperty,dispatcher_obj,inputval,reporting_obj):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.reporting_obj)
        return res

    def invokemobileappkeyword(self,teststepproperty,dispatcher_obj,inputval,reporting_obj):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.reporting_obj)
        return res

    def invokeDesktopkeyword(self,teststepproperty,dispatcher_obj,inputval,iris_flag):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,iris_flag)
        return res

    def invokeSAPkeyword(self,teststepproperty,dispatcher_obj,inputval,iris_flag):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,iris_flag)
        return res

    def invokemainframekeyword(self,teststepproperty,dispatcher_obj,inputval):
        res = dispatcher_obj.dispatcher(teststepproperty,inputval)
        return res

    def get_all_the_imports(self,plugin_path):
        path= os.environ["NINETEEN68_HOME"] + '/Nineteen68/plugins/'+plugin_path
        sys.path.append(path)
        for root, dirs, files in os.walk(path):
            for d in dirs:
                p = path + '/' + d
                sys.path.append(p)

    def invoke_debug(self,mythread,runfrom_step,json_data):
        status=COMPLETED
        global break_point
        obj = handler.Handler()
        self.action=DEBUG
        handler.tspList=[]
        scenario=[json_data]
        print( '=======================================================================================================')
        log.info('***DEBUG STARTED***')
        logger.print_on_console('***DEBUG STARTED***')
        print( '=======================================================================================================')
        for d in scenario:
            flag,browser_type,last_tc_num,testcase_empty_flag,empty_testcase_names=obj.parse_json(d)
            if flag == False:
                break
            print '\n'
            tsplist = obj.read_step()
            for k in range(len(tsplist)):
                if tsplist[k].name.lower() == 'openbrowser':
                    if tsplist[k].apptype.lower()=='web':
                        if not (IGNORE_THIS_STEP in tsplist[k].inputval[0].split(';')):
                            tsplist[k].inputval = browser_type
        if flag:
            if runfrom_step > 0 and runfrom_step <= tsplist[len(tsplist)-1].stepnum:
                self.conthread=mythread
                status = self.executor(tsplist,DEBUG,last_tc_num,runfrom_step,mythread)
            else:
                logger.print_on_console( 'Invalid step number!! Please provide run from step number from 1 to ',tsplist[len(tsplist)-1].stepnum,'\n')
                log.info('Invalid step number!! Please provide run from step number')
        else:
            print 'Invalid script'
        print( '=======================================================================================================')
        log.info('***DEBUG COMPLETED***')
        logger.print_on_console('***DEBUG COMPLETED***')
        print( '=======================================================================================================')
        #clearing of dynamic variables
        obj.clearList(self)
        #clearing dynamic variables at the end of execution to support dynamic variable at the scenario level
        obj.clear_dyn_variables()
        return status

    def invoke_execution(self,mythread,json_data,socketIO,wxObject,configvalues,qc_soc):
        global terminate_flag
        qc_url=''
        qc_password=''
        qc_username=''

        obj = handler.Handler()
        status=COMPLETED
        condition_check_flag = False
        testcase_empty_flag = False
        info_msg=''
##        t = test.Test()
##        suites_list,flag = t.gettsplist()
        #Getting all the details by parsing the json_data
        suiteId_list,suite_details,browser_type,scenarioIds,suite_data,execution_id,condition_check,dataparam_path=obj.parse_json_execute(json_data)
        self.action=EXECUTE
        log.info( 'No  of Suites : '+str(len(suiteId_list)))
        logger.print_on_console('No  of Suites : ',len(suiteId_list))
        j=1
        #Iterate through the suites-list
        for suite,suite_id,suite_id_data in zip(suite_details,suiteId_list,suite_data):
            #EXECUTION GOES HERE
            status = False
            flag=True
            if terminate_flag:
                status=TERMINATE
##                break
            log.info('---------------------------------------------------------------------')
            print( '=======================================================================================================')
            log.info('***SUITE '+str( j) +' EXECUTION STARTED***')
            logger.print_on_console('***SUITE ', j ,' EXECUTION STARTED***')
            log.info('-----------------------------------------------')
            print( '=======================================================================================================')
            do_not_execute = False
            #Check for the disabled scenario
            if not (do_not_execute) :
                i=0
                 #Logic to Execute each suite for each of the browser
                for browser in browser_type[suite_id]:
                    #Logic to iterate through each scenario in the suite
                    for scenario,scenario_id,condition_check_value,dataparam_path_value in zip(suite_id_data,scenarioIds[suite_id],condition_check[suite_id],dataparam_path[suite_id]):
                        execute_flag=True
                        con =Controller()
                        con.configvalues=configvalues
                        con.exception_flag=self.exception_flag
                        con.wx_object=wxObject
                        handler.tspList=[]
                        #condition check for scenario execution and reporting for condition check
                        if not(condition_check_flag):
                             #check for temrinate flag before printing loggers
                            if not(terminate_flag):
                                print( '=======================================================================================================')
                                logger.print_on_console( '***Scenario ' ,(i  + 1 ) ,' execution started***')
                                print( '=======================================================================================================')
                                log.info('***Scenario '  + str((i  + 1 ) ) + ' execution started***')
                            if(len(scenario)==3 and len(scenario['qcdetails'])==7):
                                qc_details_creds=scenario['qccredentials']
                                qc_username=qc_details_creds['qcusername']
                                qc_password=qc_details_creds['qcpassword']
                                qc_url=qc_details_creds['qcurl']
                                qc_sceanrio_data=scenario['qcdetails']
                                qc_domain=qc_sceanrio_data['qcdomain']
                                qc_project=qc_sceanrio_data['qcproject']
                                qc_folder=qc_sceanrio_data['qcfolderpath']
                                qc_tsList=qc_sceanrio_data['qctestset']
                                qc_testrunname=qc_sceanrio_data['qctestcase']

                            #Iterating through each test case in the scenario
                            for d in [eval(scenario[scenario_id])]:
                                #check for temrinate flag before parsing tsp list
                                if terminate_flag:
                                    break
                                flag,browser_temp,last_tc_num,testcase_empty_flag,empty_testcase_names=obj.parse_json(d,dataparam_path_value)

                                if flag == False:
                                    break
                                print '\n'
                                if (True in testcase_empty_flag):
                                    info_msg=str("Scenario cannot be executed, since the following testcases are empty: "+','.join(empty_testcase_names))
                                    logger.print_on_console(info_msg)
                                    log.info(info_msg)
                                    status = TERMINATE
                                    execute_flag=False
                                else:
                                    tsplist = handler.tspList
                                    if len(tsplist)==0:
                                        continue
                                    for k in range(len(tsplist)):
                                        if tsplist[k].name.lower() == 'openbrowser':
                                            if tsplist[k].apptype.lower()=='web':
                                                if not (IGNORE_THIS_STEP in tsplist[k].inputval[0].split(';')):
                                                        tsplist[k].inputval = [browser]
                            if flag and execute_flag :
                                #check for temrinate flag before execution
                                tsplist = obj.read_step()
                                if not(terminate_flag):
                                    con.action=EXECUTE
                                    con.conthread=mythread
                                    con.tsp_list=tsplist
                                    status = con.executor(tsplist,EXECUTE,last_tc_num,1,con.conthread)
                                    print( '=======================================================================================================')
                                    logger.print_on_console( '***Scenario' ,(i  + 1 ) ,' execution completed***')
                                    print( '=======================================================================================================')
                            if execute_flag:
                                #Saving the report for the scenario
                                logger.print_on_console( '***Saving report of Scenario' ,(i  + 1 ),'***')
                                log.info( '***Saving report of Scenario' +str(i  + 1 )+'***')
                                os.chdir(self.cur_dir)
                                filename='Scenario'+str(i  + 1)+'.json'
                                con.reporting_obj.save_report_json(filename)
                                socketIO.emit('result_executeTestSuite',self.getreport_data(suite_id,scenario_id,con,execution_id))
                                obj.clearList(con)
                                i+=1
                                #logic for condition check
                                report_json=con.reporting_obj.report_json[OVERALLSTATUS]
                                if len(scenario['qcdetails'])==7 and (qc_url!='' and qc_password!='' and  qc_username!=''):
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
                                        qc_status['qc_domain']=qc_domain
                                        qc_status['qc_project']=qc_project
                                        qc_status['qc_folder']=qc_folder
                                        qc_status['qc_tsList']=qc_tsList
                                        qc_status['qc_testrunname']=qc_testrunname
                                        qc_status['qc_update_status'] = qc_update_status
                                        logger.print_on_console('****Updating QCDetails****')
                                        if qc_soc is not None:
                                            data_to_send = json.dumps(qc_status).encode('utf-8')
                                            data_to_send+='#E&D@Q!C#'
                                            qc_soc.send(data_to_send)
                                            data_stream= qc_soc.recv(1024)
                                            server_data = data_stream[:data_stream.find('#E&D@Q!C#')]
                                            parsed_data = json.loads(server_data.decode('utf-8'))
                                            if parsed_data['QC_UpdateStatus']:
                                                logger.print_on_console('****Updated QCDetails****')
                                            else:
                                                logger.print_on_console('****Failed to Update QCDetails****')
                                        else:
                                            logger.print_on_console('****Failed to Update QCDetails****')
                                    except Exception as e:
                                        logger.print_on_console('Error in Updating Qc details')

                                #Check is made to fix issue #401
                                if len(report_json)>0:
                                    overall_status=report_json[0]['overallstatus']
                                    if(condition_check_value==1):
                                        if(overall_status==TEST_RESULT_PASS):
                                            continue
                                        else:
                                            condition_check_flag = True
                                            logger.print_on_console('Condition Check: Terminated by program ')
                            elif (True in testcase_empty_flag):
                                logger.print_on_console( '***Saving report of Scenario' ,(i  + 1 ),'***')
                                log.info( '***Saving report of Scenario' +str(i  + 1 )+'***')
                                os.chdir(self.cur_dir)
                                filename='Scenario'+str(i  + 1)+'.json'
                                con.reporting_obj.save_report_json_conditioncheck_testcase_empty(filename,info_msg)
                                socketIO.emit('result_executeTestSuite',self.getreport_data_conditioncheck_testcase_empty(suite_id,scenario_id,con,execution_id))
                                obj.clearList(con)
                                i+=1
                        else:
                            logger.print_on_console( '***Saving report of Scenario' ,(i  + 1 ),'***')
                            log.info( '***Saving report of Scenario' +str(i  + 1 )+'***')
                            os.chdir(self.cur_dir)
                            filename='Scenario'+str(i  + 1)+'.json'
                            con.reporting_obj.save_report_json_conditioncheck(filename)
                            socketIO.emit('result_executeTestSuite',self.getreport_data_conditioncheck(suite_id,scenario_id,con,execution_id))
                            obj.clearList(con)
                            i+=1
                            #logic for condition check
                            report_json=con.reporting_obj.report_json[OVERALLSTATUS]
            log.info('---------------------------------------------------------------------')
            print( '=======================================================================================================')
            log.info('***SUITE '+ str(j) +' EXECUTION COMPLETED***')
            #clearing dynamic variables at the end of execution to support dynamic variable at the scenario level
            obj.clear_dyn_variables()
            logger.print_on_console('***SUITE ', j ,' EXECUTION COMPLETED***')
            log.info('-----------------------------------------------')
            print( '=======================================================================================================')
            j=j+1
        if status==TERMINATE:
            print( '=======================================================================================================')
            logger.print_on_console( '***Terminating the Execution***')
            print( '=======================================================================================================')

        return status

    #Building of Dictionary to send back toserver to save the data
    def getreport_data(self,testsuite_id,scenario_id,con,execution_id):
        obj={'testsuiteId':testsuite_id,
        'scenarioId':scenario_id,
        'reportData':con.reporting_obj.report_json,
        'executionId':execution_id}
        return obj

    #Building of Dictionary to send back toserver to save the data for condition check
    def getreport_data_conditioncheck(self,testsuite_id,scenario_id,con,execution_id):
        obj={'testsuiteId':testsuite_id,
        'scenarioId':scenario_id,
        'reportData':con.reporting_obj.report_json_condition_check,
        'executionId':execution_id}
        return obj

    #Building of Dictionary to send back toserver to save the data for condition check for testcase empty
    def getreport_data_conditioncheck_testcase_empty(self,testsuite_id,scenario_id,con,execution_id):
        obj={'testsuiteId':testsuite_id,
        'scenarioId':scenario_id,
        'reportData':con.reporting_obj.report_json_condition_check_testcase_empty,
        'executionId':execution_id}
        return obj

    def invoke_controller(self,action,mythread,debug_mode,runfrom_step,json_data,wxObject,socketIO,qc_soc,*args):
        status = COMPLETED
        global terminate_flag,break_point,pause_flag,socket_object
        self.conthread=mythread
        self.clear_data()
        socket_object = socketIO
        #Logic to make sure that logic of usage of existing driver is not applicable to execution
        if self.web_dispatcher_obj != None:
            self.web_dispatcher_obj.action=action
        self.debug_choice=wxObject.choice
        if action.lower()==EXECUTE:
            self.execution_mode=SERIAL
            #Parallel Execution
            ##obj=handler.Handler()
            ##kill_process()
            ##if execution_mode.lower() == PARALLEL:
            ##    status=self.invoke_execution(mythread,json_data)
            if self.execution_mode.lower() == SERIAL:
                status=self.invoke_execution(mythread,json_data,socketIO,wxObject,self.configvalues,qc_soc)
        elif action.lower()==DEBUG:
            self.debug_mode=debug_mode
            self.wx_object=wxObject
            status=self.invoke_debug(mythread,runfrom_step,json_data)
        if status != TERMINATE:
            status=COMPLETED
        return status
    def invoke_parralel_exe(self,action,input_breakpoint,mythread):
        #create a ThreadPoolExecutor to perform parallel execution
        executor = ThreadPoolExecutor(max_workers=len(browsers))
        #create Future object of  size number of browsers selected
        for browser in range(len(browsers)):
            #create a future object and start execution
            future = executor.submit(TestThread(browsers[browser],mythread))
            #Store the future object to track in future
            thread_tracker.append(future)
            time.sleep(2)
        #Get the length of thread_tracker
        size = len(thread_tracker)
        task_counter = 0
        while True:
            if thread_tracker[0].done():
                task_counter = task_counter + 1
                if size == task_counter:
                    if  TERMINATE:
                        logger.print_on_console( 'Update the result json as terminate')
                    else:
                        logger.print_on_console( 'Update the result json as complete')
                executor.shutdown()
                break
        logger.print_on_console ('Parallel execution completed')

    def step_execution_status(self,teststepproperty):
        #325 : Report - Skip status in report by providing value 0 in the output column in testcase grid is not handled.
        outputstring = teststepproperty.outputval
        nostatusflag = False
        if len(outputstring) > 0  and outputstring != None:
            if (outputstring.find(';') > 0):
                index = outputstring.rfind(';')
                if outputstring[index + 1:] == STEPSTATUS_INREPORTS_ZERO:
                    nostatusflag = True
            elif outputstring== STEPSTATUS_INREPORTS_ZERO:
                nostatusflag = True
        return nostatusflag


def kill_process():
    import tempfile
    import psutil
    import os,shutil
    if platform.system() == 'Darwin':
        try:
            import browserops_MW
            browserops_MW.driver.quit()
        except Exception as e:
            logger.print_on_console('Error in stopping scraping driver as driver is already closed')
            log.error(e)

        try:
            import browser_Keywords_MW
            browser_Keywords_MW.driver_obj.quit()
        except Exception as e:
            logger.print_on_console('Error in stopping browser driver as driver is already closed')
            log.error(e)

        try:
            import install_and_launch
            install_and_launch.driver.quit()
        except Exception as e:
            logger.print_on_console('Error in stopping application driver as driver is already closed')
            log.error(e)

        try:
            os.system("killall -9 Safari")
            os.system("killall -9 safaridriver")
            os.system("killall -9 node")
        except Exception as e:
            logger.print_on_console('Exception in stopping server')
            log.error(e)
        log.info('Stale processes killed')
        logger.print_on_console('Stale processes killed')
    else:
        try:
            import win32com.client
            my_processes = ['chromedriver.exe','IEDriverServer.exe','IEDriverServer64.exe','CobraWinLDTP.exe','phantomjs.exe','geckodriver.exe']
            wmi=win32com.client.GetObject('winmgmts:')
            for p in wmi.InstancesOf('win32_process'):
                if p.Name in my_processes:
                    os.system("TASKKILL /F /IM " + p.Name )
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
            log.info('Stale processes killed')
            logger.print_on_console( 'Stale processes killed')
        except Exception as e:
            log.error(e)

        try:
            import browser_Keywords
            pidset = browser_Keywords.pid_set
            ##processes = psutil.net_connections()
            for pid in pidset:
                log.info( 'Pid Found' )
                log.info(pid)
                os.system("TASKKILL /F /PID " + str(pid))
            browser_Keywords.pid_set.clear()
        except Exception as e:
            log.error(e)
        try:
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
        except Exception as e:
            log.error('Error while deleting file/folder')
            log.error(e)
