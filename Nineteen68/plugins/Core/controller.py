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
import constants
import test
import Exceptions
import handler
import os,sys
import logger
from constants import *
import pause_execution




#index for iterating the teststepproperty for executor
i = 0

#Terminate Flag
terminate_flag=False
pause_flag=False
break_point=-1
verify_exists=False

class Controller():

    generic_dispatcher_obj = None
    web_dispatcher_obj = None
    oebs_dispatcher_obj = None
    webservice_dispatcher_obj = None
    outlook_dispatcher_obj = None
    desktop_dispatcher_obj = None

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
        'oebs':VERIFY_VISIBLE}

    def __load_generic(self):
        try:
            import generic_dispatcher
            self.generic_dispatcher_obj = generic_dispatcher.GenericKeywordDispatcher()
        except Exception as e:
            logger.log('')

    def __load_webservice(self):
        try:
            import websevice_dispatcher
            self.webservice_dispatcher_obj = websevice_dispatcher.Dispatcher()
        except Exception as e:
            logger.log('')

    def __load_oebs(self):
        try:
            import oebs_dispatcher
            self.oebs_dispatcher_obj = oebs_dispatcher.OebsDispatcher()
        except Exception as e:
            logger.log('')

    def __load_outlook(self):
        try:
            import outlookdispatcher
            self.outlook_dispatcher_obj = outlookdispatcher.Dispatcher()
        except Exception as e:
             logger.log('')

    def __load_web(self):
        try:
            import web_dispatcher
            self.web_dispatcher_obj = web_dispatcher.Dispatcher()
        except Exception as e:
             logger.log('')

    def __load_desktop(self):
        try:
            import desktop_dispatcher
            self.desktop_dispatcher_obj = desktop_dispatcher.DesktopDispatcher()
        except Exception as e:
            print '-----------------------------------------------'
            logger.log('')


    def checkfordynamicvariables(self,outputval):
        #checks whether the output value contains dynamic Variables
        status = False;
        if outputval != None and outputval != '':
            if outputval.startswith('{') and outputval.endswith('}'):
                status = True
				 #the following block ignores check for dynamic variable when
				 #the given input is a JSON Token
                 #NEED TO IMPLEMENT
        return status

    def checkyynamicvariableinsidedynamicvariable(self,inputvar):
        input_dict=handler.dynamic_variable_map
        generickeywordresult = GenericKeywordResult()
        status = constants.TEST_RESULT_FAIL
        if inputvar.startswith('{') and inputvar.endswith('}'):
            pattern = '\\[(.*?)\\]'
            regularexp = re.compile(pattern)
            inputafterre = regularexp.findall(inputvar)
            if len(inputafterre) > 0 :
                for i in range(len(inputafterre)):
                    replacestring = ''
                    if input_dict.has_key(inputafterre[i]):
                        replacestring = input_dict.get(inputafterre[i])
                        inputvar = inputvar.replace(inputafterre[i],replacestring)
            return inputvar
        elif (inputvar.count('{') > 0) and (inputvar.count('}') > 0):
            pattern = '\\[(.*?)\\]'
            regularexp = re.compile(pattern)
            inputafterre = regularexp.findall(inputvar)
            if len(inputafterre) > 0 :
                for i in range(len(inputafterre)):
                    replacestring = ''
                    if input_dict.has_key(inputafterre[i]):
                        replacestring = input_dict.get(inputafterre[i])
                        inputvar = inputvar.replace(inputafterre[i],replacestring)
            return inputvar

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
            logger.log('Dangling: '+tsp.name +' in '+tsp.testscript_name+'\n')
        return status



    def methodinvocation(self,index,*args):

        if break_point != -1 and break_point == index:
            index = constants.BREAK_POINT
            return index
        tsp = handler.tspList[index]
        #Check for 'terminate_flag' before execution
        if not(terminate_flag):
            #Check for 'pause_flag' before executionee
            if pause_flag:
                pause_execution.execute(PAUSE)
            if(self.check_dangling(tsp,index)):

                keyword = tsp.name

                print tsp.inputval
                input = tsp.inputval[0]
                addtionalinfo = tsp.additionalinfo
                apptype = tsp.apptype
                print 'Keyword : ',keyword
                print 'Input :',input
                print 'Apptype : ',apptype

                if input.find(constants.IGNORE_THIS_STEP) != -1 :
                    #Skip the current step execution
                    #update in the report
                    #increment the tsp index to point to next step and continue
                    index += 1

                else:
                    if addtionalinfo != None:
                        if addtionalinfo == constants.IGNORE_THIS_STEP:
                            #Skip the current step execution
                            #update in the report
                            #increment the tsp index to point to next step and continue
                            index += 1

                if tsp != None and isinstance(tsp,TestStepProperty) :
                    index = self.keywordinvocation(index,*args)

                elif tsp != None and isinstance(tsp,if_step.If):
                    index = tsp.invoke_condtional_keyword()
                elif tsp != None and isinstance(tsp,for_step.For):
                    index = tsp.invokeFor()
                elif tsp != None and isinstance(tsp,getparam.GetParam):
                    index = tsp.performdataparam()
                elif tsp != None and isinstance(tsp,jumpBy.JumpBy):
                    index = tsp.invoke_jumpby()
                elif tsp != None and isinstance(tsp,jumpTo.JumpTo):
                    index = tsp.invoke_jumpto()


            else:

                index= constants.TERMINATE
        else:
            index= constants.TERMINATE
        return index

    def keywordinvocation(self,index,*args):
        import time
        time.sleep(1)
        global verify_exists
        #Check for 'terminate_flag' before execution
        if not(terminate_flag):
            #Check for 'pause_flag' before execution
            if pause_flag:
                    pause_execution.execute(PAUSE)
            inpval = []

            teststepproperty = handler.tspList[index]
            rawinput = teststepproperty.inputval
            if len(args) > 0:
                rawinput = args[0]

            inputs = rawinput[0].split(constants.SEMICOLON)
            for i in range(0,len(inputs )):
                inpval.append(inputs[i])
                print 'Input: ',i + 1 , '= ',inputs[i]

            #Custom object implementation for Web
            if teststepproperty.objectname==CUSTOM:
                if verify_exists==False:
                    previous_step=handler.tspList[index-1]
                    if previous_step.name==self.verify_dict[previous_step.apptype.lower()]:
                        self.previous_step=previous_step
                        verify_exists=True
                    else:
                        logger.log('ERR_CUSTOM_VERIFYEXISTS: Previous step VerifyExists is missing')
                if verify_exists==True:
                    teststepproperty.parent_xpath=self.previous_step.objectname
                    teststepproperty.url=self.previous_step.url
            elif teststepproperty.name==VERIFY_EXISTS and verify_exists:
                verify_exists=False


            #get the output varible from the teststep property
            outputstring = teststepproperty.outputval

            #Check the apptype and pass to perticular module
            if teststepproperty.apptype.lower() == constants.APPTYPE_GENERIC:
                #Generic apptype module call goes here
                result = self.invokegenerickeyword(teststepproperty,self.generic_dispatcher_obj,inpval)
                print 'Result in methodinvocation : ',result

            elif teststepproperty.apptype.lower() == constants.APPTYPE_WEB:
                #Web apptype module call goes here

                result = self.invokewebkeyword(teststepproperty,self.web_dispatcher_obj,inpval)
                print 'Result in methodinvocation------ : ',result, '\n\n'

            elif teststepproperty.apptype.lower() == constants.APPTYPE_WEBSERVICE:
                #Webservice apptype module call goes here
                 #OEBS apptype module call goes here
                result = self.invokewebservicekeyword(teststepproperty,self.webservice_dispatcher_obj,inpval)
                print 'Result in methodinvocation : ',result

            elif teststepproperty.apptype.lower() == constants.APPTYPE_DESKTOP:
                #Desktop apptype module call goes here
                result = self.invokeDesktopkeyword(teststepproperty,self.desktop_dispatcher_obj,inpval)
                print 'Result in methodinvocation : ',result

            elif teststepproperty.apptype.lower() == constants.APPTYPE_DESKTOP_JAVA:

                #OEBS apptype module call goes here
                result = self.invokeoebskeyword(teststepproperty,self.oebs_dispatcher_obj,inpval)
                print 'Result in methodinvocation : ',result

            index+=1
            if teststepproperty.name=='stop':
                index=len(handler.tspList)
            return index
        else:
            return constants.TERMINATE


    def executor(self,tsplist,action):
        i = 0
        status=True

        while (i < len(tsplist)):
            tsp = tsplist[i]
            #Check for 'terminate_flag' before execution
            if not(terminate_flag):
                #Check for 'pause_flag' before execution
                if pause_flag:
                    pause_execution.execute(PAUSE)
                try:
                    i = self.methodinvocation(i)
                    if i== constants.TERMINATE:
                        logger.log('Terminating the execution')
                        status=i
                        break
                    elif i==constants.BREAK_POINT:
                        logger.log('Debug Stopped')
                        status=i
                        break

                except Exception as e:
                    Exceptions.error(e)
                    status=False
                    i=i+1
            else:
                logger.log('Terminating the execution')
                status=constants.TERMINATE
                break


        return status

    def invokegenerickeyword(self,teststepproperty,dispatcher_obj,inputval):

        keyword = teststepproperty.name
        print "----Keyword :",keyword,' execution Started----'
        res = dispatcher_obj.dispatcher(keyword,*inputval)

        print "----Keyword :",keyword,' execution completed----\n\n'
        return res

    def invokeoebskeyword(self,teststepproperty,dispatcher_obj,inputval):

        keyword = teststepproperty.name
        print "----Keyword :",keyword,' execution Started----'

        res = dispatcher_obj.dispatcher(teststepproperty,inputval)
        print "----Keyword :",keyword,' execution completed----\n\n'
        return res

    def invokewebservicekeyword(self,teststepproperty,dispatcher_obj,inputval):

        keyword = teststepproperty.name
        print "----Keyword :",keyword,' execution Started----'
        res = dispatcher_obj.dispatcher(keyword,*inputval)
        print "----Keyword :",keyword,' execution completed----\n\n'
        return res

    def invokewebkeyword(self,teststepproperty,dispatcher_obj,inputval):

        keyword = teststepproperty.name
        print "----Keyword :",keyword,' execution Started----'
        res = dispatcher_obj.dispatcher(teststepproperty,inputval)
        print "----Keyword :",keyword,' execution completed----\n\n'
        return res

    def invokeDesktopkeyword(self,teststepproperty,dispatcher_obj,inputval):
        keyword = teststepproperty.name
        print "----Keyword :",keyword,' execution Started----'
        res = dispatcher_obj.dispatcher(teststepproperty,inputval)
        print "----Keyword :",keyword,' execution completed----\n\n'
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


    def invoke_controller(self,action,input_breakpoint):
        global terminate_flag,break_point,pause_flag
        terminate_flag=False
        pause_flag=False
        obj = Controller()
        t = test.Test()
        list,flag = t.gettsplist()
        if flag:
            try:
                input_breakpoint=int(input_breakpoint)
                if input_breakpoint >=0:
                    break_point=input_breakpoint+1
            except ValueError,NameError:
                logger.log('Invalid breakpoint number')
            status=obj.executor(list,action)
            return status
        else:
            print 'Invalid script'

    def kill_process(self):
        try:
            os.system("TASKKILL /F /IM chromedriver.exe")
            os.system("TASKKILL /F /IM IEDriverServer.exe")
            os.system("TASKKILL /F /IM IEDriverServer64.exe")
            os.system("TASKKILL /F /IM CobraWinLDTP.exe")
            logger.log( 'Stale processes killed')
        except Exception as e:
            Exceptions.error(e)

#main method
if __name__ == '__main__':
    obj = Controller()
    obj.kill_process()
    print 'Controller object created'
    t = test.Test()
    list,flag = t.gettsplist()
    if flag:
        obj.executor(list,'debug')
    else:
        print 'Invalid script'




