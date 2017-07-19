#-------------------------------------------------------------------------------
# Name:        reporting.py
# Purpose:
#
# Author:      sushma.p
#
# Created:
# Copyright:   (c) sushma.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from constants import *
import json
import reporting_pojo
import logger
import logging
import step_description
from datetime import datetime
import core_utils
log = logging.getLogger("reporting.py")


class Reporting:

    """
        def : __init__
        purpose : Constructor to create report_json string

    """
    def __init__(self):
        self.report_string=[]
        self.overallstatus_array=[]
        self.overallstatus_array_incomplete = []
        self.report_json={ROWS:self.report_string,OVERALLSTATUS:self.overallstatus_array}
        self.report_json_condition_check={ROWS:self.report_string,OVERALLSTATUS:self.overallstatus_array_incomplete}
        self.nested_flag=False
        self.pid_list=[]
        self.parent_id=0
        self.id_counter=1
        self.testscript_name=None
        self.overallstatus=TEST_RESULT_PASS
        self.browser_version='NA'
        self.browser_type='NA'
        self.start_time=''
        self.end_time=''
        self.ellapsed_time=''
        self.name=''
        self.user_termination=False
        self.step_description_obj=step_description.StepDescription()
        self.core_utilsobject = core_utils.CoreUtils()

    def get_description(self,tsp,con):
        """
        def : get_description
        purpose : To Fetch the step description of given keyword
        param : tsp,con - Instance of <controller>


        """
        description=None
        try:

            inputVal=[]
            outputval=[]
            input=[]
            inputVal=tsp.inputval[0].split(';')
            for x in inputVal:
                x=con.dynamic_var_handler_obj.replace_dynamic_variable(x,tsp.name,con)
                input.append(x)
            input=','.join(input)
            output=tsp.outputval
            output=con.dynamic_var_handler_obj.replace_dynamic_variable(x,tsp.name,con)
            if (tsp.name in MULTIPLE_OUTPUT_KEYWORDS and output != '' and output != None) or tsp.name==GENERIC_KEYWORD  :
                output=tsp.additionalinfo
            apptype=tsp.apptype
##            inputVal=tsp.inputval[0].split(';')
            outputval=tsp.outputval.split(';')[0]
            params=tsp.name,tsp,inputVal,input,output,con,self
            apptype_description={'generic':self.step_description_obj.generic,
            'web':self.step_description_obj.web,
            'mobileapp':self.step_description_obj.mobileapp,
            'mobileweb':self.step_description_obj.web,
            'webservices':self.step_description_obj.webservices,
            'desktop':self.step_description_obj.desktop,
            'sap':self.step_description_obj.sap,
            'desktopjava':self.step_description_obj.oebs}
            description=apptype_description[apptype.lower()](*params)
            description=self.core_utilsobject.get_UTF_8(description)
##            description=description.encode('utf-8')

        except Exception as e:
            log.error(e)
            description=tsp.name+' Executed'
        return description


    def build_overallstatus(self,start_time,end_time,ellapsed_time):
        """
        def : build_overallstatus
        purpose : builds the overallstatus field of report_json
        param : start_time,end_time,ellapsed_time

        """
        if self.overallstatus==TERMINATE:
            self.add_termination_step()
        self.start_time=str(start_time)
        self.end_time=str(end_time)
        self.ellapsed_time=str(ellapsed_time)
        obj={}
        obj[ELLAPSED_TIME]=self.ellapsed_time
        obj[END_TIME]=self.end_time
        obj[BROWSER_VERSION]=self.browser_version
        obj[START_TIME]=self.start_time
        obj[OVERALLSTATUS]=self.overallstatus
        obj[BROWSER_TYPE]=self.browser_type
        self.overallstatus_array.append(obj)

    def build_overallstatus_conditionCheck(self):
            """
            def : build_overallstatus_conditionCheck
            purpose : builds the overallstatus field of condition check report_json

            """
            self.start_time = datetime.now()
            self.end_time = datetime.now()
            self.ellapsed_time = self.end_time - self.start_time
            obj={}
            obj[ELLAPSED_TIME]=str(self.ellapsed_time)
            obj[END_TIME]=str(self.end_time)
            obj[BROWSER_VERSION]=""
            obj[START_TIME]=str(self.start_time)
            obj[OVERALLSTATUS]=INCOMPLETE
            obj[BROWSER_TYPE]=""
            self.overallstatus_array_incomplete.append(obj)

    def get_pid(self):
        """
        def : get_pid
        purpose : gets the top most id present in the pid_list

        """
        if len(self.pid_list)>0:
            self.parent_id=self.pid_list[-1].split(',')[1]
        return self.parent_id

    def pop_pid(self):
        """
        def : pop_pid
        purpose : adds and returns the top most id present in the pid_list

        """
        if len(self.pid_list)>0:
            self.parent_id=self.pid_list.pop()
        return self.parent_id


    def add_pid(self,pid_name):
        """
        def : add_pid
        purpose : adds the name and id of the step to pid_list in the format <<name,id>>
        param: pid_name

        """
        self.nested_flag=True
        self.pid_list.append(pid_name+','+str(self.id_counter))

    def remove_nested_flag(self):
        """
        def : remove_nested_flag
        purpose : makes the nested_flag variable False

        """
        self.nested_flag=False

    def add_testscriptname(self,report_obj):
        """
        def : add_testscriptname
        purpose : adds the Testscriptname to the report
        param : report_obj - Instance of <reporting_pojo>

        """
        obj={}
        obj[ID]=report_obj._id
        obj[KEYWORD]=TEST_SCRIPT_NAME
        obj[PARENT_ID]=report_obj.parent_id
        obj[COMMENTS]=''
        obj[STEP_DESCRIPTION]=TEST_SCRIPT_NAME+': '+report_obj.testscript_name
        self.report_string.append(obj)
        self.id_counter+=1

    def add_termination_step(self):
        """
        def : add_termination_step
        purpose : adds the Termination_step to the report

        """
        obj={}
        obj[ID]=self.id_counter
        obj[KEYWORD]=''
        obj[PARENT_ID]=''
        obj[COMMENTS]=''
        description=PROGRAM_TERMINATION
        obj[STEP]=description
        if self.user_termination:
            description=USER_TERMINATION
        else:
            description="Terminated by program"
        obj[STEP_DESCRIPTION]=description
        self.report_string.append(obj)
        self.id_counter+=1



    def generate_keyword_step(self,report_obj):
        """
        def : generate_keyword_step
        purpose : create each step in the report
        param : report_obj - Instance of <reporting_pojo>


        """
        if report_obj.testscript_name != self.testscript_name:
            self.testscript_name=report_obj.testscript_name
            self.add_testscriptname(report_obj)
            try:
                report_obj._id+=1
            except Exception as e:
                log.error(e)
        obj={}
        report_obj._id=self.core_utilsobject.get_UTF_8(report_obj._id)
        obj[ID]=report_obj._id
        report_obj.name=self.core_utilsobject.get_UTF_8(report_obj.name)
        obj[KEYWORD]=report_obj.name
        report_obj.parent_id=self.core_utilsobject.get_UTF_8(report_obj.parent_id)
        obj[PARENT_ID]=report_obj.parent_id
        report_obj.status=self.core_utilsobject.get_UTF_8(report_obj.status)
        obj[STATUS]=report_obj.status
        report_obj.step=self.core_utilsobject.get_UTF_8(report_obj.step)
        obj[STEP]=report_obj.step
        report_obj.comments=self.core_utilsobject.get_UTF_8(report_obj.comments)
        obj[COMMENTS]=report_obj.comments
        report_obj.step_description=self.core_utilsobject.get_UTF_8(report_obj.step_description)
        obj[STEP_DESCRIPTION]=report_obj.step_description
        report_obj.screenshot_path=self.core_utilsobject.get_UTF_8(report_obj.screenshot_path)
        obj[SCREENSHOT_PATH]= report_obj.screenshot_path
        report_obj.ellapsedtime=self.core_utilsobject.get_UTF_8(report_obj.ellapsedtime)
        obj[ELLAPSED_TIME]=report_obj.ellapsedtime
        self.report_string.append(obj)

    def generate_report_step(self,tsp,status,con,ellapsedtime,keyword_flag,*args):
        """
        def : generate_report_step
        purpose : calls the method 'generate_keyword_step' to add each step to the report
        param : tsp,status,controller_instance,ellapsedtime,keyword_flag


        """
        comments=''
        screenshot_path = None
        parent_id=0
        name=tsp.name
        step_description=''
        if keyword_flag:
            step_description=self.get_description(tsp,con)
            if self.nested_flag:
                parent_id=self.get_pid()
##        if keyword_flag and self.nested_flag:
##            parent_id=self.get_pid()
        elif not(keyword_flag):
            parent_id=tsp.parent_id
            step_description=tsp.step_description
            name=self.name
            ##            Added this line to remove status for conditional keyword in reports
            status = ''
        if len(args)>0:
            if args[0] != None:
                result_tuple=args[0]
                if "Terminate" not in result_tuple:
                    comments= result_tuple[3]
                if(len(result_tuple) == 5):
                    screenshot_path = result_tuple[4]
                else:
                    screenshot_path = None

        reporting_pojo_obj=reporting_pojo.ReportingStep(self.id_counter,name,parent_id,status,STEP+str(tsp.stepnum),comments,step_description,str(ellapsedtime),tsp.testscript_name,screenshot_path)

        self.generate_keyword_step(reporting_pojo_obj)
        self.id_counter+=1



    def print_report_json(self):

        """
        def : print_report_json
        purpose : printing the report json


        """

        print '--------------------------------------------------------------------'
        print json.dumps(self.report_json)
        print '--------------------------------------------------------------------'



    def save_report_json(self,filename):
        log.debug('Saving report json to a file')
        with open(filename, 'w') as outfile:
                log.info('Writing report data to the file '+filename)
                json.dump(self.report_json, outfile, indent=4, sort_keys=False)
        outfile.close()

    def save_report_json_conditioncheck(self,filename):
        log.debug('Saving report json to a file')
        self.build_overallstatus_conditionCheck()
        with open(filename, 'w') as outfile:
                log.info('Writing report data to the file '+filename)
                json.dump(self.report_json_condition_check, outfile, indent=4, sort_keys=False)
        outfile.close()




