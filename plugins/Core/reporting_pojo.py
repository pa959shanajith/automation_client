#-------------------------------------------------------------------------------
# Name:        reporting_pojo
# Purpose:
#
# Author:      sushma.p
#
# Created:
# Copyright:   (c) sushma.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class ReportingStep:
    """
        def : __init__
        purpose : Constructor to create a pojo of each step in the report
        param : _id,name,parent_id,status,step,comments,step_description,ellapsedtime,testscript_name

    """

    def __init__(self,_id,name,parent_id,status,step,comments,step_description,ellapsedtime,testscript_name,screenshot_path,remark,testcase_details,execute_result_data):
        self._id=_id
        self.name=name
        self.parent_id=parent_id
        self.status=status
        self.step=step
        self.comments=comments
        self.step_description=step_description
        self.ellapsedtime=ellapsedtime
        self.testscript_name=testscript_name
        self.screenshot_path= screenshot_path
        self.remarks=remark
        self.testcase_details=testcase_details
        self.execute_result_data = execute_result_data
        # self.configureKey = configureKey
        # self.profilename = profilename
        # self.executionListId = executionListId



