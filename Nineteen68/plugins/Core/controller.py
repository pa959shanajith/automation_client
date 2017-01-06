#-------------------------------------------------------------------------------
# Name:        controller.py
# Purpose:
#
# Author:      wasimakram.sutar
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
import test
import handler
import os,sys
import logger
from constants import *
import pause_execution
import dynamic_variable_handler
import reporting

from values_from_ui import *
from concurrent.futures import ThreadPoolExecutor
import threading
from datetime import datetime
import logging




#index for iterating the teststepproperty for executor
i = 0

#Terminate Flag
terminate_flag=False
pause_flag=False
break_point=-1

thread_tracker = []
log = logging.getLogger("controller.py")


class TestThread(threading.Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self,browser):
        """Init Worker Thread Class."""
        logger.print_on_console( 'Browser number: ',browser)
        log.debug('Browser number:  %d',browser)
        threading.Thread.__init__(self)
        self.browser = browser
        self.start()    # start the thread

    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        try:


            time.sleep(2)
            con = Controller()
            print 'Controller object created'

            status = con.invoke_controller('debug','',self.browser)
            if status==TERMINATE:
                print '---------Termination Completed-------'
            else:
                logger.print_on_console('***SUITE EXECUTION COMPLETED***')

        except Exception as m:
            print m



class Controller():

    generic_dispatcher_obj = None
    web_dispatcher_obj = None
    oebs_dispatcher_obj = None
    webservice_dispatcher_obj = None
    outlook_dispatcher_obj = None
    desktop_dispatcher_obj = None
    verify_exists=False

    def __init__(self):
        self.get_all_the_imports()
        self.__load_generic()
        self.__load_web()
        self.__load_webservice()
        self.__load_oebs()
        self.__load_outlook()
        self.__load_desktop()
        self.previous_step=''
        self.verify_dict={'web':VERIFY_EXISTS,
        'desktopjava':VERIFY_VISIBLE}
        self.dynamic_var_handler_obj=dynamic_variable_handler.DynamicVariables()
        self.status=TEST_RESULT_FAIL
        self.scenario_start_time=''
        self.scenario_end_time=''
        self.scenario_ellapsed_time=''
        self.reporting_obj=reporting.Reporting()

    def __load_generic(self):
        try:
            import generic_dispatcher
            self.generic_dispatcher_obj = generic_dispatcher.GenericKeywordDispatcher()
        except Exception as e:
            logger.print_on_console('')

    def __load_webservice(self):
        try:
            import websevice_dispatcher
            self.webservice_dispatcher_obj = websevice_dispatcher.Dispatcher()
        except Exception as e:
            logger.print_on_console('')

    def __load_oebs(self):
        try:
            import oebs_dispatcher
            self.oebs_dispatcher_obj = oebs_dispatcher.OebsDispatcher()
        except Exception as e:
            logger.print_on_console('')

    def __load_outlook(self):
        try:
            import outlookdispatcher
            self.outlook_dispatcher_obj = outlookdispatcher.Dispatcher()
        except Exception as e:
             logger.print_on_console('')

    def __load_web(self):
        try:
            import web_dispatcher
            self.web_dispatcher_obj = web_dispatcher.Dispatcher()
        except Exception as e:
             logger.print_on_console('')

    def __load_desktop(self):
        try:
            import desktop_dispatcher
            self.desktop_dispatcher_obj = desktop_dispatcher.DesktopDispatcher()
        except Exception as e:
            logger.print_on_console('')

    def dangling_status(self,index):
        step=handler.tspList[index]
        return step.executed

    def check_dangling(self,tsp,index):
        status=True
        if tsp.__class__.__name__.lower() in [IF,FOR,GETPARAM]:
            info_dict=tsp.info_dict
            if info_dict is not None:
                if tsp.name.lower() in [ENDFOR,ENDLOOP]:
                    index=info_dict[0].keys()[0]
                    status=self.dangling_status(index)

                if tsp.name.lower() in [IF,ELSE_IF,ELSE,ENDIF]:

                    if tsp.name.lower() in [IF]:
                        status= info_dict[-1].values()[0].lower() == ENDIF

                    elif tsp.name.lower() in [ELSE_IF,ELSE]:
                        status1= info_dict[-1].values()[0] == ENDIF
                        status2= info_dict[0].keys()[0] != index
                        status = status1 and status2

                    elif tsp.name.lower() in [ENDIF]:
                        index=info_dict[-1].keys()[0]
                        status=self.dangling_status(index)



            else:
                status=False
            if tsp.name.lower()==ENDLOOP and len(info_dict)<2:
                status=False

        if not(status):
            logger.print_on_console('Dangling: '+tsp.name +' in '+tsp.testscript_name+'\n')
            log.error('Dangling: '+tsp.name +' in '+tsp.testscript_name)
        return status

    def __print_details(self,tsp,input,inpval):
        keyowrd='Keyword : '+tsp.name
        input_val='Input :'+str(input)
        output='Output :'+tsp.outputval
        apptype='Apptype : '+str(tsp.apptype)
        logger.print_on_console(keyowrd)
        log.info(keyowrd)
        logger.print_on_console(input_val)
        log.info(input_val)
        logger.print_on_console(output)
        log.info(output)
        logger.print_on_console(apptype)
        log.info(apptype)
        for i in range(len(inpval)):
            logger.print_on_console('Input: ',i + 1 , '= ',inpval[i])



    def methodinvocation(self,index,*args):

        if break_point != -1 and break_point == index:
            index = BREAK_POINT
            return index
        tsp = handler.tspList[index]
        keyword_flag=True
        #Check for 'terminate_flag' before execution
        if not(terminate_flag):
            #Check for 'pause_flag' before executionee
            if pause_flag:
                pause_execution.execute(PAUSE)
            if(self.check_dangling(tsp,index)):

                input = tsp.inputval[0]
                addtionalinfo = tsp.additionalinfo



                if input.find(IGNORE_THIS_STEP) != -1 :
                    #Skip the current step execution
                    #update in the report
                    #increment the tsp index to point to next step and continue
                    index += 1

                else:
                    if addtionalinfo != None:
                        if addtionalinfo == IGNORE_THIS_STEP:
                            #Skip the current step execution
                            #update in the report
                            #increment the tsp index to point to next step and continue
                            index += 1

                #Logic to split input and handle dynamic variables
                rawinput = tsp.inputval
                if len(args) > 0:
                    rawinput = args[0]


                inpval=self.split_input(rawinput,tsp.name)
                if tsp.name.lower() not in [FOR,ENDFOR] :
                    #Print the details of keyword
                    self.__print_details(tsp,input,inpval)

                #Calculating Start time

                if tsp != None and isinstance(tsp,TestStepProperty) :
                    logger.print_on_console( "----Keyword :",tsp.name,' execution Started----\n')
                    start_time = datetime.now()
                    start_time_string=start_time.strftime(TIME_FORMAT)
                    logger.print_on_console('Step Execution start time is : '+start_time_string)
                    index,result = self.keywordinvocation(index,inpval,self.reporting_obj,*args)
                else:
                    keyword_flag=False
                    if tsp != None and isinstance(tsp,if_step.If):
                        index = tsp.invoke_condtional_keyword(inpval,self.reporting_obj)
                    elif tsp != None and isinstance(tsp,for_step.For):
                        index = tsp.invokeFor(inpval,self.reporting_obj)
                    elif tsp != None and isinstance(tsp,getparam.GetParam):
                        index = tsp.performdataparam(inpval,self,self.reporting_obj)
                    elif tsp != None and isinstance(tsp,jumpBy.JumpBy):
                        index = tsp.invoke_jumpby(inpval,self.reporting_obj)
                    elif tsp != None and isinstance(tsp,jumpTo.JumpTo):
                        index = tsp.invoke_jumpto(inpval,self.reporting_obj)



            else:

                index= TERMINATE
        else:
            index= TERMINATE



        ellapsed_time=''
        if keyword_flag:
            end_time = datetime.now()
            end_time_string=end_time.strftime(TIME_FORMAT)
            logger.print_on_console('Step Execution end time is : '+end_time_string)
            logger.print_on_console( "----Keyword :",tsp.name,' execution Completed----\n')
            ellapsed_time=end_time-start_time
            logger.print_on_console('Step Elapsed time is : ',str(ellapsed_time)+'\n')
            #Changing the overallstatus of the scenario if it's Fail or Terminate
            if self.status==TEST_RESULT_FAIL or self.status==TERMINATE:
                self.reporting_obj.overallstatus=self.status

        self.reporting_obj.generate_report_step(tsp,self.status,tsp.name+' EXECUTED and the result is  '+self.status,ellapsed_time,keyword_flag,result[3])

        return index

    def split_input(self,input,keyword):
        inpval = []
        input_list=[]

        input_list = input[0].split(SEMICOLON)

        if keyword in WS_KEYWORDS:
            input_list=[input[0]]

        elif keyword in DYNAMIC_KEYWORDS:
            input_list=[]
            string=input[0]
            index=string.find(';')
            if index >-1:
                input_list.append(string[0:index])
                input_list.append(string[index+1:len(string)])
            elif string != '':
                input_list.append(string)

        for x in input_list:
            x=self.dynamic_var_handler_obj.replace_dynamic_variable(x,keyword)
            inpval.append(x)

        return inpval

    def store_result(self,result,tsp):
        output=tsp.outputval.split(SEMICOLON)
        keyword_response=result[-2]
        if result[-2] == OUTPUT_CONSTANT:
            keyword_response=result[-3]

        logger.print_on_console('Result obtained is ',keyword_response)
        log.info('Result obtained is: ')
        log.info(keyword_response)

        if len(output)>0 and output[0] != '':
            self.dynamic_var_handler_obj.store_dynamic_value(output[0],keyword_response)

        if len(output)>1:
            self.dynamic_var_handler_obj.store_dynamic_value(output[1],result[1])

    def keywordinvocation(self,index,inpval,*args):
        import time
        time.sleep(1)
        result=(TEST_RESULT_FAIL,TEST_RESULT_FALSE,OUTPUT_CONSTANT,None)
        #Check for 'terminate_flag' before execution
        if not(terminate_flag):
            #Check for 'pause_flag' before execution
            if pause_flag:
                pause_execution.execute(PAUSE)

            teststepproperty = handler.tspList[index]

            #Custom object implementation for Web
            if teststepproperty.objectname==CUSTOM:
                if self.verify_exists==False:
                    previous_step=handler.tspList[index-1]
                    apptype=previous_step.apptype.lower()

                    if  apptype in self.verify_dict and previous_step.name==self.verify_dict[apptype]:
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
            elif teststepproperty.name==VERIFY_EXISTS and self.verify_exists:
                self.verify_exists=False



            #get the output varible from the teststep property
            outputstring = teststepproperty.outputval

            #Check the apptype and pass to perticular module
            if teststepproperty.apptype.lower() == APPTYPE_GENERIC:
                #Generic apptype module call
                result = self.invokegenerickeyword(teststepproperty,self.generic_dispatcher_obj,inpval)

            elif teststepproperty.apptype.lower() == APPTYPE_WEB:
                #Web apptype module call
                result = self.invokewebkeyword(teststepproperty,self.web_dispatcher_obj,inpval,args[0])

            elif teststepproperty.apptype.lower() == APPTYPE_WEBSERVICE:
                #Webservice apptype module call
                result = self.invokewebservicekeyword(teststepproperty,self.webservice_dispatcher_obj,inpval)

            elif teststepproperty.apptype.lower() == APPTYPE_DESKTOP:
                #Desktop apptype module call
                result = self.invokeDesktopkeyword(teststepproperty,self.desktop_dispatcher_obj,inpval)

            elif teststepproperty.apptype.lower() == APPTYPE_DESKTOP_JAVA:
                #OEBS apptype module call
                result = self.invokeoebskeyword(teststepproperty,self.oebs_dispatcher_obj,inpval)

            temp_result=list(result)
            if temp_result[2]==OUTPUT_CONSTANT:
                temp_result[2]=None
            logger.print_on_console( 'Result in methodinvocation : ', teststepproperty.name,' : ',temp_result,'\n')
            log.info('Result in methodinvocation : '+ str(teststepproperty.name)+' : ')
            log.info(result)
            log.info(KEYWORD_EXECUTION_COMPLETED+ '\n' )

            if result!=TERMINATE:
                self.store_result(result,teststepproperty)
                self.status=result[0]
                index+=1
            else:
                index=result
                self.status=result

            print '\n'

            #Checking for stop keyword
            if teststepproperty.name==STOP:
                index=len(handler.tspList)
            return index,result
        else:
            return TERMINATE


    def executor(self,tsplist,action):

        i = 0

        status=True

        self.scenario_start_time=datetime.now()
        start_time_string=self.scenario_start_time.strftime(TIME_FORMAT)
        logger.print_on_console('Scenario Execution start time is : '+start_time_string)


        while (i < len(tsplist)):
            tsp = tsplist[i]
            #Check for 'terminate_flag' before execution
            if not(terminate_flag):
                #Check for 'pause_flag' before execution
                if pause_flag:
                    pause_execution.execute(PAUSE)
                try:
                    i = self.methodinvocation(i)
                    if i== TERMINATE:
                        logger.print_on_console('Terminating the execution')
                        status=i
                        break
                    elif i==BREAK_POINT:
                        logger.print_on_console('Debug Stopped')
                        status=i
                        break

                except Exception as e:
                    log.error(e)
                    logger.print_on_console(e)
                    status=False
                    i=i+1
            else:
                logger.print_on_console('Terminating the execution')
                status=TERMINATE
                break

        self.scenario_end_time=datetime.now()
        end_time_string=self.scenario_end_time.strftime(TIME_FORMAT)
        logger.print_on_console('Scenario Execution end time is : '+end_time_string)

        self.scenario_ellapsed_time=self.scenario_end_time-self.scenario_start_time
        self.reporting_obj.build_overallstatus(self.scenario_start_time,self.scenario_end_time,self.scenario_ellapsed_time)
        logger.print_on_console('Step Elapsed time is : ',str(self.scenario_ellapsed_time))




        return status

    def invokegenerickeyword(self,teststepproperty,dispatcher_obj,inputval):
        keyword = teststepproperty.name
        res = dispatcher_obj.dispatcher(teststepproperty,*inputval)
        return res

    def invokeoebskeyword(self,teststepproperty,dispatcher_obj,inputval):
        keyword = teststepproperty.name
        res = dispatcher_obj.dispatcher(teststepproperty,inputval)
        return res

    def invokewebservicekeyword(self,teststepproperty,dispatcher_obj,inputval):
        keyword = teststepproperty.name
        res = dispatcher_obj.dispatcher(teststepproperty,*inputval)
        return res

    def invokewebkeyword(self,teststepproperty,dispatcher_obj,inputval,reporting_obj):

        keyword = teststepproperty.name
        res = dispatcher_obj.dispatcher(teststepproperty,inputval,self.reporting_obj)
        return res

    def invokeDesktopkeyword(self,teststepproperty,dispatcher_obj,inputval):
        keyword = teststepproperty.name
        res = dispatcher_obj.dispatcher(teststepproperty,inputval)
        return res

    def get_all_the_imports(self):
        maindir = os.getcwd()
        os.chdir('..')
        curdir = os.getcwd()
        path= curdir + '//Nineteen68//plugins'
        for root, dirs, files in os.walk(path):
            for d in dirs:
                p = path + '\\' + d
                sys.path.append(p)
        os.chdir(maindir)


    def invoke_controller(self,action,input_breakpoint,*args):
        status = False
        global terminate_flag,break_point,pause_flag
        if execution_mode.lower() == PARALLEL:

            handler.tspList=[]
            terminate_flag=False
            pause_flag=False
            obj = handler.Handler()
            t = test.Test()
            suites_list,flag = t.gettsplist()
            if flag:
                try:
                    input_breakpoint=int(input_breakpoint)
                    if input_breakpoint >0:
                        break_point=input_breakpoint-1
                except ValueError,NameError:
                    logger.print_on_console('Invalid breakpoint number')


            #in future this value will come from the UI
            scenarios = scenario_num
            print 'No  of Suites : ',len(suites_list)
            j=1
            for suite in suites_list:
                #EXECUTION GOES HERE
                status = False
                flag=True
                #Iterate through the suite
                log.info('---------------------------------------------------------------------')
                logger.print_on_console('---------------------------------------------------------------------')
                log.info('***SUITE ', j ,' EXECUTION STARTED***')
                logger.print_on_console('***SUITE ', j ,' EXECUTION STARTED***')
                logger.print_on_console('---------------------------------------------------------------------')
                for i in range( len(suite)):
                    do_not_execute = False
                    #create a object of controller for each scenario
                    con =Controller()
                    #Check for the disabled scenario

                    for k in scenarios:
                        if k == (i + 1):
                            do_not_execute = True
                            break



                    if (not do_not_execute) :
                        logger.print_on_console( '***Scenario ' ,(i  + 1 ) ,' execution started***')
                        log.info('***Scenario '  + str((i  + 1 ) ) + ' execution started***')
                        for d in suite[i]:
                            flag=obj.parse_json(d)
                            if flag == False:
                                break
                            print '\n'
                            tsplist = obj.read_step()
                            for k in range(len(tsplist)):
                                if tsplist[k].name.lower() == 'openbrowser':
                                    tsplist[k].inputval = unicode(args[0])

                        if flag:
                            status = con.executor(tsplist,'debug')

                        else:
                            print 'Invalid script'
                        logger.print_on_console( '***Scenario' ,(i  + 1 ) ,' execution completed***')
                        log.info('Saving the Report json of Scenario '+str((i  + 1 )))
                        logger.print_on_console( '***Saving the Report json of Scenario ',(i  + 1 ),'***')
                        log.info( '***Scenario' + str((i  + 1 )) +' execution completed***')
                        obj.clearList(con)
                    else:
                        logger.print_on_console ('Scenario ' , (i + 1) ,' has been disabled for execution!!!')
                        log.info('Scenario ' + str((i + 1) ) +' has been disabled for execution!!!')
                    #logic for condition check
                    report_json=con.reporting_obj.report_json[OVERALLSTATUS]
                    overall_status=report_json[0]['overallstatus']
                    if(condition_check==True):
                        if(overall_status=='Pass'):
                            continue
                        else:
                            break
                log.info('---------------------------------------------------------------------')
                logger.print_on_console('---------------------------------------------------------------------')
                log.info('***SUITE ', j ,' EXECUTION COMPLETED***')
                logger.print_on_console('***SUITE ', j ,' EXECUTION COMPLETED***')
                logger.print_on_console('---------------------------------------------------------------------')
                j=j+1

        elif execution_mode.lower() == SERIAL:
            handler.tspList=[]
            terminate_flag=False
            pause_flag=False
            obj = handler.Handler()
            t = test.Test()
            suites_list,flag = t.gettsplist()
            if flag:
                try:
                    input_breakpoint=int(input_breakpoint)
                    if input_breakpoint >0:
                        break_point=input_breakpoint-1
                except ValueError,NameError:
                    logger.print_on_console('Invalid breakpoint number')


            #in future this value will come from the UI
            scenarios = scenario_num
            logger.print_on_console( 'Length of Suite : ',len(suites_list))

            #EXECUTION GOES HERE
            status = False
            flag=True
            #Iterate through the suite

            for browser in range( len(browsers)):
                j=1
                for suite in suites_list:
                    log.info('-----------------------------------------------')
                    logger.print_on_console('-----------------------------------------------')
                    log.info('***SUITE '+str( j) +' EXECUTION STARTED***')
                    logger.print_on_console('***SUITE ', j ,' EXECUTION STARTED***')
                    log.info('-----------------------------------------------')
                    logger.print_on_console('-----------------------------------------------')
                    for i in range( len(suite)):
                        do_not_execute = False
                        #create a object of controller for each scenario
                        con =Controller()
                        #Check for the disabled scenario

                        for k in scenarios:
                            if k == (i + 1):
                                do_not_execute = True
                                break



                        if (not do_not_execute) :
                            logger.print_on_console( '***Scenario ' ,(i  + 1 ) ,' execution started***')
                            log.info('***Scenario '  + str((i  + 1 ) ) + ' execution started***')
                            for d in suite[i]:
                                flag=obj.parse_json(d)
                                if flag == False:
                                    break
                                print '\n'
                                tsplist = obj.read_step()
                                for k in range(len(tsplist)):
                                    if tsplist[k].name.lower() == 'openbrowser':
                                        tsplist[k].inputval = unicode(browsers[browser])

                            if flag:

                                status = con.executor(tsplist,'debug')


                            else:
                                log.error('Invalid script')
                            logger.print_on_console( '***Scenario' ,(i  + 1 ) ,' execution completed***')
                            log.info( '***Scenario ' + str((i  + 1 )) +' execution completed***')
                            log.info('Saving the Report json of Scenario '+str((i  + 1 )))
                            logger.print_on_console( '***Saving the Report json of Scenario ',(i  + 1 ),'***')
                            filename='Scenario'+str(i  + 1)+'.json'
                            con.reporting_obj.save_report_json(filename)
                            obj.clearList(con)
                        else:
                            logger.print_on_console( 'Scenario ' , (i + 1) ,' has been disabled for execution!!!')
                            log.info('Scenario ' + str((i + 1) ) +' has been disabled for execution!!!')
                         #logic for condition check
                        report_json=con.reporting_obj.report_json[OVERALLSTATUS]
                        overall_status=report_json[0]['overallstatus']
                        if(condition_check==True):
                            if(overall_status=='Pass'):
                                continue
                            else:
                                break

                    log.info('-----------------------------------------------')
                    logger.print_on_console('-----------------------------------------------')
                    log.info('***SUITE '+ str(j) +' EXECUTION COMPLETED***')
                    logger.print_on_console('***SUITE ', j ,' EXECUTION COMPLETED***')
                    log.info('-----------------------------------------------')
                    logger.print_on_console('-----------------------------------------------')
                    j=j+1
        return status



    def invoke_parralel_exe(self,action,input_breakpoint):
        #create a ThreadPoolExecutor to perform parallel execution
        executor = ThreadPoolExecutor(max_workers=len(browsers))

        #create Future object of  size number of browsers selected
        for browser in range(len(browsers)):
            #create a future object and start execution
            future = executor.submit(TestThread(browsers[browser]))
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
                        print 'Update the result json as terminate'
                    else:
                        print 'Update the result json as complete'
                executor.shutdown()
                break

        print 'Parralel execution completed'

    def execute(self):
        kill_process()
        obj = Controller()
        t = test.Test()
        list,flag = t.gettsplist()
        if flag:
            logger.print_on_console('*** SUITE EXECUTION STARTED***')
            obj.executor(list,'debug')
            logger.print_on_console('***SUITE EXECUTION COMPLETED***')

def kill_process():
    try:
        os.system("TASKKILL /F /IM chromedriver.exe")
        os.system("TASKKILL /F /IM IEDriverServer.exe")
        os.system("TASKKILL /F /IM IEDriverServer64.exe")
        os.system("TASKKILL /F /IM CobraWinLDTP.exe")
        logger.print_on_console( 'Stale processes killed')
    except Exception as e:
        log.error(e)
        logger.print_on_console(e)

#main method
if __name__ == '__main__':
    kill_process()
    obj = Controller()
    print 'Controller object created'
    t = test.Test()
    list,flag = t.gettsplist()
    if flag:
        logger.print_on_console('***SUITE EXECUTION STARTED***')
        obj.executor(list,'debug')
        logger.print_on_console('***SUITE EXECUTION COMPLETED***')
        obj.reporting_obj.print_report_json()

    else:
        print 'Invalid script'
    kill_process()




