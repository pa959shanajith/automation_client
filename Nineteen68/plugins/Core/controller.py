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


#index for iterating the teststepproperty for executor
i = 0

class Controller():

    generic_dispatcher_obj = None
    web_dispatcher_obj = None
    oebs_dispatcher_obj = None
    webservice_dispatcher_obj = None
    outlook_dispatcher_obj = None

    def __init__(self):
        self.get_all_the_imports()
        import generic_dispatcher
        self.generic_dispatcher_obj = generic_dispatcher.GenericKeywordDispatcher()
        import web_dispatcher
        self.web_dispatcher_obj = web_dispatcher.Dispatcher()
        import oebs_dispatcher
        self.oebs_dispatcher_obj = oebs_dispatcher.OebsDispatcher()
        import websevice_dispatcher
        self.webservice_dispatcher_obj = websevice_dispatcher.Dispatcher()
        import outlookdispatcher
        self.outlook_dispatcher_obj = outlookdispatcher.Dispatcher()


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
        generickeywordresult = GenericKeywordResult()
        status = constants.TEST_RESULT_FAIL

    def methodinvocation(self,index,*args):
        tsp = handler.tspList[index]
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

        return index

    def keywordinvocation(self,index,*args):
        inpval = []
        #if termination flag is true then thorough Testautomation exception else do the following
        teststepproperty = handler.tspList[index]
        rawinput = teststepproperty.inputval
        if len(args) > 0:
            rawinput = args[0]

        inputs = rawinput[0].split(constants.SEMICOLON)
        for i in range(0,len(inputs )):
            inpval.append(inputs[i])
            print 'Input: ',i + 1 , '= ',inputs[i]


        #get the output varible from the teststep property
        outputstring = teststepproperty.outputval

        #Check the apptype and pass to perticular module
        if teststepproperty.apptype.lower() == constants.APPTYPE_GENERIC:
            #Generic apptype module call goes here
            result = self.invokegenerickeyword(teststepproperty,self.generic_dispatcher_obj,inpval)
            print 'Result in methodinvocation : ',result
##            os.chdir(currentdir)

        elif teststepproperty.apptype.lower() == constants.APPTYPE_WEB:
            #Web apptype module call goes here

            result = self.invokewebkeyword(teststepproperty,self.web_dispatcher_obj,inpval)
            print 'Result in methodinvocation------ : ',result, '\n\n'

        elif teststepproperty.apptype.lower() == constants.APPTYPE_WEBSERVICE:
            #Webservice apptype module call goes here
             #OEBS apptype module call goes here
            result = self.invokewebservicekeyword(teststepproperty,self.webservice_dispatcher_obj,inpval)
            print 'Result in methodinvocation : ',result
##            os.chdir(currentdir)
        elif teststepproperty.apptype.lower() == constants.APPTYPE_DESKTOP:
            #Desktop apptype module call goes here
            print 'Dont forget to implement me'
        elif teststepproperty.apptype.lower() == constants.APPTYPE_DESKTOP_JAVA:

            #OEBS apptype module call goes here
            result = self.invokeoebskeyword(teststepproperty,self.oebs_dispatcher_obj,inpval)
            print 'Result in methodinvocation : ',result
##            os.chdir(currentdir)
        return index+1


    def executor(self,tsplist,action):
        i = 0
        #populate all the keywords here
        #NonWebKeywords
        #CustomKeyword
        #CustomDesktopKeywords
        #CustomOebsKeywords
        #multipleOutputKeyword
        #SwitchToWindowKeywords
##        next_index=0
        while (i < len(tsplist)):
            tsp = tsplist[i]
            try:
                methodstatus = ''
                #and isinstance(tsplist,TestStepProperty)
                if tsp != None and isinstance(tsp,TestStepProperty) :
                    keyword = tsp.name
                    input = tsp.inputval[0]
                    addtionalinfo = tsp.additionalinfo
                    apptype = tsp.apptype
                    print 'Keyword : ',keyword
                    print 'Input :',input
                    print 'Apptype : ',apptype
                    #skip the step if  <<Ignore.This.Step>> Constants passed in input
                    if input.find(constants.IGNORE_THIS_STEP) != -1 :
                        #Skip the current step execution
                        #update in the report
                        #increment the tsp index to point to next step and continue
                        i = i + 1
                        continue
                    else:
                        if addtionalinfo != None:
                            if addtionalinfo == constants.IGNORE_THIS_STEP:
                                #Skip the current step execution
                                #update in the report
                                #increment the tsp index to point to next step and continue
                                i = i + 1
                                continue

                    i = self.keywordinvocation(i)
                else:
                    i = self.methodinvocation(i)

            except Exception as e:
                Exceptions.error(e)
                i=i+1
                print i


    def invokegenerickeyword(self,teststepproperty,dispatcher_obj,inputval):

        keyword = teststepproperty.name
        print "----Keyword :",keyword,' execution Started----\n'
        res = dispatcher_obj.dispatcher(keyword,*inputval)

        print "----Keyword :",keyword,' execution completed----\n\n'
        return res

    def invokeoebskeyword(self,teststepproperty,dispatcher_obj,inputval):

        keyword = teststepproperty.name
        print "----Keyword :",keyword,' execution Started----\n'

        res = dispatcher_obj.dispatcher(teststepproperty,inputval)
        print "----Keyword :",keyword,' execution completed----\n\n'
        return res

    def invokewebservicekeyword(self,teststepproperty,dispatcher_obj,inputval):

        keyword = teststepproperty.name
        print "----Keyword :",keyword,' execution Started----\n'
        res = dispatcher_obj.dispatcher(keyword,*inputval)
        print "----Keyword :",keyword,' execution completed----\n\n'
        return res
    def invokewebkeyword(self,teststepproperty,dispatcher_obj,inputval):

        keyword = teststepproperty.name
        print "----Keyword :",keyword,' execution Started----\n'
        res = dispatcher_obj.dispatcher(teststepproperty,inputval)
        print "----Keyword :",keyword,' execution completed----\n\n'
        return res
    def get_all_the_imports(self):
        maindir = os.getcwd()
        os.chdir('..')
        curdir = os.getcwd()
        path= curdir + '\Nineteen68\plugins'
        for root, dirs, files in os.walk(path):
            for d in dirs:
                p = path + '\\' + d
                sys.path.append(p)
        os.chdir(maindir)

if __name__ == '__main__':
    obj = Controller()
    print 'Controller object created'



    t = test.Test()
    list,flag = t.gettsplist()
    if flag:
        obj.executor(list,'debug')
    else:
        print 'Invalid script'





