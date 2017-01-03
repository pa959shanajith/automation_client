#-------------------------------------------------------------------------------
# Name:        reporting
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


class Reporting:

    """
        def : __init__
        purpose : Constructor to create report_json string

    """
    def __init__(self):
        self.report_string=[]
        self.overallstatus=[]
        self.report_json={ROWS:self.report_string,OVERALLSTATUS:self.overallstatus}
        self.nested_flag=False
        self.pid_list=[]
        self.parent_id=0
        self.id_counter=1
        self.testscript_name=None

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
        obj[COMMENTS]=report_obj.comments
        obj[STEP_DESCRIPTION]=TEST_SCRIPT_NAME+': '+report_obj.testscript_name
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

        obj={}
        obj[ID]=report_obj._id
        obj[KEYWORD]=report_obj.name
        obj[PARENT_ID]=report_obj.parent_id
        obj[STATUS]=report_obj.status
        obj[STEP]=report_obj.step
        obj[COMMENTS]=report_obj.comments
        obj[STEP_DESCRIPTION]=report_obj.step_description
        obj[ELLAPSED_TIME]=report_obj.ellapsedtime
        self.report_string.append(obj)

    def generate_report_step(self,tsp,status,step_description,ellapsedtime,keyword_flag):
        """
        def : generate_report_step
        purpose : calls the method 'generate_keyword_step' to add each step to the report
        param : tsp,status,step_description,ellapsedtime,keyword_flag


        """
        parent_id=0
        name=tsp.name
        if keyword_flag and self.nested_flag:
            parent_id=self.get_pid()
        elif not(keyword_flag):
            parent_id=tsp.parent_id
            step_description=tsp.step_description
            name=self.name

        reporting_pojo_obj=reporting_pojo.ReportingStep(self.id_counter,name,parent_id,status,STEP+str(tsp.stepnum),'',step_description,ellapsedtime,tsp.testscript_name)

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


