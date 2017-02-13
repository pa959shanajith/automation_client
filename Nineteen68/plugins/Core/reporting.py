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

log = logging.getLogger("reporting.py")


class Reporting:

    """
        def : __init__
        purpose : Constructor to create report_json string

    """
    def get_description(self,tsp,con):
        d=tsp.name+' Executed'
        try:
            input=[]
            for x in tsp.inputval:
                x=con.dynamic_var_handler_obj.replace_dynamic_variable(x,tsp.name,con)
                input.append(x)
            input=''.join(tsp.inputval)
            output=tsp.outputval
            step_desc={'verifyPopUpText':' Verify ' + input+ '  is the Popup text ',
                'DeselectAll':'Deselect all values in the '+ tsp.custname,
                'navigateForward':'Navigate forward in the browser',
                'getCurrentDate':'Get current date of the system and save the date ' + tsp.outputval + ' in '+ tsp.outputval ,
                'getValueByIndex':'Get value with index ' + input + ' in the '+ tsp.custname + ' and save the value ' + output + ' in '+ tsp.outputval,
                'setWholeBody':'Set the entire body ' + input+ ' that needs to be sent in the request',
                'getToolTipText':'Get the tool tip from the '+ tsp.custname+ ' and save the tool tip text ' + output+ ' in ' + tsp.outputval,
                'executeFile':'Perform execution of the file'  + input,
                'verifyValuesExists':'Verify values ' + input + ' exists in the '+ tsp.custname ,
                'navigateWithAuthenticate':' Open url ' + input	+ ' in the browser',
                'navigateBack':'Navigate back in the browser',
                'verifyTextExists':'Verify static text ' + input + ' exists',
                'ClickElement': 'Click on ' +tsp.custname,
                'SelectMultipleValuesByText':'Select values ' + input + 'in the '+ tsp.custname,
                'selectRadioButton':'Select '+ tsp.custname ,
                'add':'Add the numbers ' + input+ ' and save the value ' + output + ' in '+ tsp.outputval,
                'setOperations':'Set the Operation ' + input+ 'that needs to be performed on the request',
                'setFocus':' Set the focus on '+ tsp.custname ,
                'cellClick':'Click ' + tsp.custname ,
                'verifyDialogText':' Verify '+ input + ' is the text of Window Dialog ',
                'evaluate':'Evaluate Mathematical expression ' + input+ ' and save the result ' + output + '  in '+ tsp.outputval,
                'SelectMultipleValuesByIndexes':'Select values with index ' + input + ' in the '+ tsp.custname,
                'getRowCount':'Get row count of the ' + tsp.custname + ' and save the count ' + output + ' in '+ tsp.outputval ,
                'verifyPageTitle':'Verify ' + input+ ' is the page title of the web page',
                'press':'Press on the '+ tsp.custname,
                'rightClick':'Perform right click on element '+ tsp.custname,
                'selectValueByText':'Select value by text '+input+' of the '+ 'type '+ objectName +' with the element '+objectIndex+' present in the table cell '+tsp.custname+'-['+ input + ']['+ colNum +']',
                'toLowerCase':' Change ' + input+ ' to Lower case and save the value ' + output+ ' in ' + tsp.outputval ,
                'closeSubWindows':'Closed the current sub window.',
                'setMethods':'Set the method type ' + input + ' for the operation.',
                'drop':'Perform drop on element '+ tsp.custname,
                'VerifyObjects':'Verify objects ' + input + ' and ' + secondInput+ ' and save the result in '+ tsp.outputval + '.',
                'addClientCertificate':'Add the certificate present in the '+ tsp.inputval[0]+ ' to the '+ tsp.inputval[1] + '.',
                'winDialog':'Invalid input for Window dialog',
                'winDialogClick':'Check Checkbox of Window dialog ',
                'dismissPopUp':'Close the Popup',
                'setHeaderTemplate':'Set the header ' + input+ ' from the header Template.',
                'GetCount':'Get the count of the values present in the '+ tsp.custname+ ' and save the value ' + output + ' in '+ tsp.outputval,
                'getBody':'Fetch the entire body ' + output+ ' that was received as a response.',
                'openNewBrowser':'Open new instance of the browser',
                'square':'Get Square of ' + input+ ' and save the value ' + output + ' in '+ tsp.outputval,
                'maximizeBrowser':'Maximize the browser ' + input,
                'VerifyElementText':'Verify ' + input + ' is the the text of the '+ tsp.custname,
                'verifyEnabled':' Verify '+ tsp.custname + ' is enabled ',
                'SelectRadioButton':'Select '+ tsp.custname ,
                'getColumnCount':'Get column count of the '+ tsp.custname+ ' and save the count '+ output + ' in '+ tsp.outputval,
                'doubleClick':'Double click on the '+ tsp.custname,
                'closeBrowser':'Close the browser ',
                'click':' Click on the '+ tsp.custname,
                'getCurrentDateAndTime':'Get current date and time of the system and save the date and time '+ tsp.inputval[0] + ' and '+ tsp.inputval[1] + ' in '+ tsp.outputval ,
                'verifyExists':' Verify '+ tsp.custname + '  exists ',
                'verifyButtonName':'Verify text ' + input + ' is the name of the '+ tsp.custname,
                'VerifyElementExists':' Verify '+ tsp.custname + ' exists ',
                'uploadFile':' Upload the file '+ filename + ' present in the path ' + input + '.',
                'verifyCellValue':'Verify cell value [Null] is present in the '+ tsp.custname + ' Invalid input',
                'getStatus':'Get the status of the ' + tsp.custname+ ' and save the status ' + output + ' in '+ tsp.outputval ,
                'SelectCheckbox':' Select '+ tsp.custname ,
                'getElementText':'Get the text of the element '+ tsp.custname+ ' and save the value  '+ output + ' in '+ tsp.outputval,
                'getLinkText':' Get Text From '+ tsp.custname + ' and save the text '+ output + ' in ' + tsp.outputval,
                'getMultipleValuesByIndexes':'Get values with indexes ' + inputValsb.toString() + ' in the '+ tsp.custname+ ' and save the value ' + TestAutomationController.multipleOutputResult + ' in  '+ tsp.outputval,
                'VerifyCount':'Verify the count of the values present in the ' + tsp.custname + ' with the '+ input,
                'concatenate':' Concatenate string '+ input + ',' + sb.toString()+ ' and save the value ' + output + ' in '+ tsp.outputval ,
                'verifyCurrentURL':' Verify url '+ input + ' is the current url of the web page',
                'selectMultipleValuesByText':'Select values ' + mulInputVal.toString() + ' in the '+ tsp.custname,
                'closeSubWindow':'Close the Subwindow',
                'verifySelectedValues':'Verify values ' + input + ' are selected in the '+ tsp.custname,
                'getAllValues':'getAllValues ' + output + ' are present in the' + tsp.custname,
                'getCellToolTip':'Get the cell tooltip from the '+ tsp.custname+ ' and save the tool tip text ' + output+ ' in ' + tsp.outputval,
                'subtract':' Subtract the numbers '+ input + ' and save the value ' + output + ' in'+ tsp.outputval,
                'wait':'Wait for ' + input+ ' Second(s)',
                'SelectValueByIndex':'Select value with index ' + input + ' in the '+ tsp.custname,
                'getDialogText':'Get the text of the Window Dialog and save the value '+ output + ' in '+ tsp.outputval ,
                'getColNumByText':'Get column number of ' + tsp.custname + ' by text '+input +' and save the column number ' + output + ' in '+ tsp.outputval ,
                'verifyText':'Verify ' + input + ' is the the text in the '+ tsp.custname,
                'sendValue':' Enter value ' + input+ ' in the '+ tsp.custname,
                'verifyWebImages':' Compare images '+ tsp.custname + ' and ' + input ,
                'toUpperCase':' Change ' + input+ ' to Upper case and save the value ' + output+ ' in ' + tsp.outputval,
                'pause':'Pause the application until the user interrupts',
                'VerifyValuesExists':'Verify values ' + val.toString().substring(1,val.toString().length()-1) + ' exists in the '+ tsp.custname ,
                'SelectValueByText':' Select value with text'+ input + ' in the ' + tsp.custname,
                'divide':'Divide the numbers '+ input + ' and save the value ' + output + ' in '+ tsp.outputval,
                'setEndPointURL':'Set the end point URL ' + input + '.',
                'selectCheckbox':' Select '+ tsp.custname,
                'verifyContent':' Verify '+ tsp.inputval[1]+ ' is present in the file ' + input ,
                'VerifySelectedValue':'Verify the selected value from the ' + tsp.custname+ ' with the '+ verifyInput.toString(),
                'deleteDynVariable':'Delete variable ' + tsp.inputval[0],
                'acceptPopUp':'Accept the Popup',
                'getCurrentTime':'Get current time of the system and save the time '+ output + ' in '+ tsp.outputval ,
                'mouseHover':' Move mouse pointer to '+ tsp.custname ,
                'SelectAllValues':'Select all values in the '+ tsp.custname,
                'verifyDoesNotExists':' Verify '+ tsp.custname + '  does not exists ',
                'GetPageTitle':' The page title is '+ output +' and  is saved  in the variable ' +tsp.outputval,
                'getPopUpText':'Get the text of the Popup and save the text ' + output+ ' in ' + tsp.outputval ,
                'setTagValue':'Set the Tag Value ' + input + ' for the tag '+ tsp.custname + '.',
                'getRowNumByText':'Get row number of ' + tsp.custname + ' by text '+input +' and save the row number ' + output + ' in '+ tsp.outputval ,
                'verifyAllValues':'Verify values ' + input + ' are present in the '+ tsp.custname,
                'GetElementText':' Get the value present in ' + tsp.custname +' and save the value ' + output + ' in '+ tsp.outputval,
                'getSelected':'Get Selected value of '+ tsp.custname+ ' and save value ' + output + ' in '+ tsp.outputval ,
                'getTextboxLength':'Get length from the ' + tsp.custname+' and save the length ' + output + ' in '+ tsp.outputval,
                'deselectAll':'Deselect all values in the '+ tsp.custname ,
                'verifyHidden':' Verify '+ tsp.custname + ' is Hidden ',
                'getContent':'Get content from the pdf ' + input+ ' and save it in '+ tsp.outputval ,
                'VerifyElementDoesNotExists':'Verify '+ tsp.custname + ' does not exists ',
                'getServerCertificate':'Fetch the Server certificate and save it in '+ tsp.inputval[1] + '.',
                'selectMultipleValuesByIndexes':'Select values ' + mulInputValin.toString() + ' in the '+ tsp.custname,
                'LaunchApplication':' The application present in the path  '+ tsp.inputval[0]+ 'is launched',
                'openBrowser':' Open ' + self.browser_type+ ' browser',
                'GetSelected':'Get selected value from the '+ tsp.custname+ ' and save the value ' + output+ ' in '+ tsp.outputval,
                'randomNumber':'Get Random number of length ' + input+ ' and save the result in '+ tsp.outputval,
                'trim':' Trim ' + input+ ' and save the value ' + output + ' in '+ tsp.outputval,
                'verifyToolTipText':'Verify ' + input + ' is the tooltip of  '+ tsp.custname ,
                'executeScript':'Perform execution of the file ' + input,
                'clickElement':' Click '+ tsp.custname,
                'executeRequest':'Execute the request.',
                'getCurrentURL':'Get current url of the web page and save the URL '+ output + ' in '+ tsp.outputval,
                'mouseClick':' Mouse Click on  '+ tsp.custname ,
                'tab':'Perform tab on '+ tsp.custname + ')',
                'GetMultipleValuesByIndexes':'Get values with indexes ' + inputValsbDesk.toString() + ' in the '+ tsp.custname +'and save the value ' + TestAutomationController.multipleOutputResult + ' in  ' +tsp.outputval,
                'verifyElementText':'Verify ' + input + ' is the the text of the '+ tsp.custname ,
                'compareFiles':'Compare the contents of file ' + input + ' and '+ input ,
                'verifyLength':'Verify ' + input + ' is the length of text in the ' +tsp.custname,
                'unselectCheckbox':'Unselect '+ tsp.custname ,
                'getLength':'Get text length from the '+ tsp.custname+ ' and save the value ' + output + ' in ' +tsp.outputval,
                'squareRoot':'Get Square root of ' + input+ ' and save the result in  '+ tsp.outputval,
                'verifySelectedValue':'Verify value ' + input + ' is selected in the ' +tsp.custname,
                'VerifyAllValues':'Verify the values from the '+ tsp.custname +' with '+ mulInputAll.toString(),
                'modulus':'Get Modulus of ' + input+ ' and save the value ' + output + ' in ' +tsp.outputval,
                'openNewTab':'Open new tab in the current browser',
                'verifyVisible':'Verify '+ tsp.custname + ' is Visible ',
                'verifyDisabled':'Verify '+ tsp.custname + ' is disabled ',
                'verifyElementExists':'Verify '+ tsp.custname + '  exists ',
                'GetStatus':'Get the status of the ' + tsp.custname+ ' and save the status ' + output + ' in '+ tsp.outputval + ')',
                'selectValueByIndex':'Select the value '+ keywordInput+' of the '+objectName+' with the index '+objectIndex+' present in the table cell  '+tsp.custname+'-['+input+']['+colNum+']',
                'GetValueByIndex':'Get value from the '+ tsp.custname+ 'with index ' + input + ' and save the value '+ output + ' in '+ tsp.outputval,
                'drag':'Perform drag on element ' +tsp.custname,
                'multiply':'Multiply the numbers '+ input + ' and save the value  ' + output + ' in ' +tsp.outputval,
                'getCount':'Get the count of values in the '+ tsp.custname+ ' and save the count ' + output + ' in ' +tsp.outputval,
                'verifyTextboxLength':'Verify ' + input + ' is the length of textbox '+ tsp.custname,
                'setTagAttribute':'Set the Tag attribute ' + input + ' for the tag '+ tsp.custname + '.',
                'verifyReadOnly':'Verify '+ tsp.custname + ' is read-only',
                'selectAllValues':'Select all values in the ' +tsp.custname,
                'UnSelectCheckbox':'Unselect '+ tsp.custname ,
                'verifyLinkText':'Verify text ' + input + ' is the name of the ' +tsp.custname,
                'getPageTitle':'Get the title of the web page and save the title '+ output + ' in '+ tsp.outputval,
                'getHeader':'Fetch the header ' + output+ ' that was received as a response.',
                'CloseApplication':' The application is closed',
                'navigateToURL':'Open url ' + input+ ' in the browser',
                'waitForElementVisible':'Wait until the element '+ tsp.custname +'is visible',
                'setHeader':'Set the header '+ input + ' that needs to be sent in the request.',
                'verifyCount':'Verify ' + input + ' is the list count of the ' +tsp.custname
            }
            d=step_desc[tsp.name]
        except Exception as e:
            d=tsp.name+' Executed'
        return d


    def __init__(self):
        self.report_string=[]
        self.overallstatus_array=[]
        self.report_json={ROWS:self.report_string,OVERALLSTATUS:self.overallstatus_array}
        self.nested_flag=False
        self.pid_list=[]
        self.parent_id=0
        self.id_counter=1
        self.testscript_name=None
        self.overallstatus=TEST_RESULT_PASS
        self.browser_version='-'
        self.browser_type='-'
        self.start_time=''
        self.end_time=''
        self.ellapsed_time=''
        self.name=''
        self.user_termination=False



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
        def : add_testscriptname
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

    def generate_report_step(self,tsp,status,con,ellapsedtime,keyword_flag,*args):
        """
        def : generate_report_step
        purpose : calls the method 'generate_keyword_step' to add each step to the report
        param : tsp,status,step_description,ellapsedtime,keyword_flag


        """
        comments=''
        parent_id=0
        name=tsp.name

        step_description=self.get_description(tsp,con)
        if keyword_flag and self.nested_flag:
            parent_id=self.get_pid()
        elif not(keyword_flag):
            parent_id=tsp.parent_id
            step_description=tsp.step_description
            name=self.name
        if len(args)>0:
            if args[0] != None:
                comments=args[0]

        reporting_pojo_obj=reporting_pojo.ReportingStep(self.id_counter,name,parent_id,status,STEP+str(tsp.stepnum),comments,step_description,str(ellapsedtime),tsp.testscript_name)

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




