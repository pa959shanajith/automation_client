#-------------------------------------------------------------------------------
# Name:        script_generator.py
# Purpose:
#
# Author:      rakshak.kamath
#
# Created:
# Copyright:   (c) rakshak.kamath
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import requests
import time
import json
import logging
from datetime import datetime
import web_keywords
import generic_keywords
import step_description_SL
import subprocess
import logger
import sauceclient

log = logging.getLogger('saucelabs_script_generator.py')

def request_content(self, url, filename, dirpath=None, body=None, content_type=''):
    """Send http request for asset content"""
    headers = self.make_auth_headers(content_type)
    connection = sauceclient.http_client.HTTPSConnection('saucelabs.com')
    full_url = url + 'screenshots.zip'
    filename1 = 'SaucelabsScreenshots_'+filename + '.zip'
    connection.request('GET', full_url, body, headers=headers)
    response1 = connection.getresponse()
    data = response1.read()
    if dirpath:
        if os.path.exists(dirpath):
            full_path = os.path.join(dirpath, filename1)
            log.info('Screenshot Asset Path: '+full_path)
            with open(full_path, 'wb') as file_handle:
                file_handle.write(data)
        else:
            raise NotADirectoryError("Path does not exist")
    else:
        with open(filename1, 'wb') as file_handle:
            file_handle.write(data)
    full_url = url + 'video.mp4'
    filename2 = 'ScreenRecording_' +filename + '.mp4'
    connection.request('GET', full_url, body, headers=headers)
    response2 = connection.getresponse()
    data = response2.read()
    if dirpath:
        if os.path.exists(dirpath):
            full_path = os.path.join(dirpath, filename2)
            log.info("Video Asset Path: "+full_path)
            with open(full_path, 'wb') as file_handle:
                file_handle.write(data)
        else:
            raise NotADirectoryError("Path does not exist")
    else:
        with open(filename2, 'wb') as file_handle:
            file_handle.write(data)
    connection.close()
    if response1.status not in [200, 201]:
        raise sauceclient.SauceException('{}: {}.\nSauce Status NOT OK'.format(
            response1.status, response1.reason), response1=response1)
    if response2.status not in [200, 201]:
        raise sauceclient.SauceException('{}: {}.\nSauce Status NOT OK'.format(
            response2.status, response2.reason), response2=response2)
    return True

def get_job_asset_content(self, job_id, filename, dirpath=None):
    """Get content collected for a specific asset on a specific job."""
    endpoint = 'https://saucelabs.com/rest/v1/{}/jobs/{}/assets/'.format(
        self.client.sauce_username, job_id)
    return self.client.request_content(endpoint,filename,dirpath)

sauceclient.SauceClient.request_content = request_content
sauceclient.Jobs.get_job_asset_content = get_job_asset_content

Saucelabs_path=os.environ['AVO_ASSURE_HOME']+os.sep+'plugins'+os.sep+'Saucelabs'
python_cwd=os.environ['AVO_ASSURE_HOME']
Saucelabs_tests=Saucelabs_path+os.sep+'tests'
Saucelabs_config_path=os.environ['AVO_ASSURE_HOME']+os.sep+'assets'+os.sep+'sauce_config.json'
scenario_name=""

class SauceLabs_Operations():

    def __init__(self,scenario_name,index):
        self.filename=Saucelabs_tests+os.sep+scenario_name+index+".py"
        self.filename1=Saucelabs_tests+os.sep+scenario_name+index+".txt"
        self.f=open(self.filename,"w")
        open(self.filename1,"w").close()
        browser_obj = web_keywords.Browser_Keywords(self.f)
        browser_popup_obj = web_keywords.Browser_Popup_Keywords(self.f)
        button_link_obj = web_keywords.Button_link_Keywords(self.f)
        dropdown_obj = web_keywords.Dropdown_Keywords(self.f)
        element_obj = web_keywords.Element_Keywords(self.f)
        radio_check_obj = web_keywords.Radio_checkbox_Keywords(self.f)
        table_obj = web_keywords.Table_Keywords(self.f)
        textbox_obj = web_keywords.Textbox_Keywords(self.f)
        util_obj = web_keywords.Util_Keywords(self.f)
        self.step_description_obj = step_description_SL.StepDescription()
        generic_string = generic_keywords.StringOperation(self.f)
        generic_date = generic_keywords.DateOperation(self.f)
        generic_file = generic_keywords.FileOperation(self.f)
        genric_folder = generic_keywords.FolderOperation(self.f)
        dyn_var_obj = generic_keywords.DynamicVariables(self.f)
        generic_util = generic_keywords.Util(self.f)
        self.obj=Sauce_Config()
        self.conf = self.obj.get_sauceconf()
        self.browsers={'1':{'browserName': "chrome", 'sauce:options':{}},'2':{'browserName': "firefox", 'sauce:options':{}},'3':{'browserName': "internet explorer", 'sauce:options':{}},'7':{'browserName': "MicrosoftEdge", 'sauce:options':{}},'8':{'browserName': "MicrosoftEdge", 'sauce:options':{}}}
        self.code="""import pytest
from selenium import webdriver
import logging
import time
import os
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from timeit import default_timer as timer
from datetime import timedelta
count=0
report=[]
testscriptname=''
input=''
output=''
err_msg=''
action=''
status='Fail'
parentId=0
loopId=0
dyn_var_map={}
f=''
def decrypt(enc):
    import base64
    from Crypto.Cipher import AES
    unpad = lambda s : s[0:-ord(s[-1])]
    enc = base64.b64decode(enc)
    cipher = AES.new(b'\x74\x68\x69\x73\x49\x73\x41\x53\x65\x63\x72\x65\x74\x4b\x65\x79', AES.MODE_ECB)
    return unpad(cipher.decrypt(enc).decode('utf-8'))

def addTestscriptName(testscript_name):
    global testscriptname,count,report
    obj={}
    obj["id"]=count
    obj["parentId"]=0
    obj["Comments"]=""
    obj['Keyword']=testscript_name
    obj['StepDescription']='TestCase Name: '+testscript_name
    count+=1
    testscriptname=testscript_name
    report.append(obj)

def addforloop(step):
    global count,parentId,input,output,dyn_var_map,start
    obj={}
    obj["id"]=count
    obj["parentId"]=parentId
    obj["status"]=status
    if step['name'] == 'for':
        obj["Keyword"]=''
        obj["StepDescription"]='Execute the steps in the loop for the given count '+str(output)
    elif step['name'] == 'endFor':
        obj["StepDescription"]='EndFor: completed'
    obj["Comments"]=step['stepnum']
    obj["Step"]=""
    obj["screenshot_path"]=""
    obj["EllapsedTime"]=str(timedelta(seconds=end-start))
    obj["Remark"]=""
    obj["testcase_details"]=""
    obj['input']=input
    obj['output']=output
    obj['dyn_var_map']=dyn_var_map
    loopId=count
    parentId=count
    count+=1
    start = timer()
    report.append(obj)
    
def addTeststep(step):
    global testscriptname,count,report,input,output,status,dyn_var_map,f,parentId,loopId,start,err_msg
    count+=1
    obj={}
    end = timer()
    if step['testscript_name']!=testscriptname:
        addTestscriptName(step['testscript_name'])
    if step['name']=='for':
        if loopId==0:
            addforloop(step)
        else:
            parentId=loopId
        obj["status"]=''
        obj["Keyword"]=''
        obj["id"]=count
        obj["parentId"]=parentId
        obj["Step"]=''
        obj["Comments"]=err_msg
        obj["StepDescription"]='Iteration '+str(output)+' started'
        obj["screenshot_path"]=""
        obj["EllapsedTime"]=str(timedelta(seconds=end-start))
        obj["Remark"]=""
        obj["testcase_details"]=""
        obj['input']=input
        obj['output']=output
        obj['dyn_var_map']=dyn_var_map
        parentId=count
    elif step['name']=='endfor':
        obj["status"]=''
        obj["Keyword"]=step['name']
        obj["id"]=count
        obj["parentId"]=parentId
        obj["Step"]=''
        obj["Comments"]=err_msg
        obj["StepDescription"]='Iteration: '+str(output)+' executed'
        obj["screenshot_path"]=""
        obj["EllapsedTime"]=str(timedelta(seconds=end-start))
        obj["Remark"]=""
        obj["testcase_details"]=""
        obj['input']=input
        obj['output']=output
        obj['dyn_var_map']=dyn_var_map
        addforloop(count)
        if(input==output):
            loopId=0
    elif step['name'] in ['if','endIf','elseIf','else']:
        text="Encountered :"+step['name']
        if step['name'] in ['if','elseIf']:
            text=text+" Condition is "+output
        obj["id"]=count
        obj["Keyword"]=step['name']
        obj["parentId"]=parentId
        obj["status"]=""
        obj["Step"]=step['stepnum']
        obj["Comments"]=err_msg
        obj["StepDescription"]=text
        obj["screenshot_path"]=""
        obj["EllapsedTime"]=str(timedelta(seconds=end-start))
        obj["Remark"]=""
        obj["testcase_details"]=""
        obj['input']=input
        obj['output']=output
        obj['dyn_var_map']=dyn_var_map
    else:
        obj["id"]=count
        obj["Keyword"]=step['name']
        obj["parentId"]=parentId
        obj["status"]=status
        obj["Step"]=step['stepnum']
        obj["Comments"]=err_msg
        obj["StepDescription"]=""
        obj["screenshot_path"]=""
        obj["EllapsedTime"]=str(timedelta(seconds=end-start))
        obj["Remark"]=""
        obj["testcase_details"]=""
        obj['input']=input
        obj['output']=output
        obj['dyn_var_map']=dyn_var_map
    obj['index']=step['index']
    obj['apptype']=step['apptype']
    obj['inputval']=step['inputval']
    output=""
    input=""
    err_msg=""
    start = timer()
    status="Fail"
    report.append(obj)
    f.truncate(0)
    f.seek(0)
    f.write(json.dumps(report))

def check_dyn_var(inp):
    global input,dyn_var_map
    if inp in dyn_var_map:
        return dyn_var_map[inp]
    else:
        return inp

def store_dyn_var(out):
    global output,dyn_var_map
    if '{' in out and '}'in out:
        dyn_var_map[out[1:-1]]=output

def check_url(url):
    import re
    res=re.match(('-?\\d+(\\.\\d+)?'),url)
    if res is None:
        driver.switch_to.default_content()
    else:
        driver.switch_to.default_content()
        url_list=url.split('/')[:-1]
        for i in url_list:
            if 'i' in i:
                tag='iframe'
                index=i.split('i')[0]
            elif 'f' in i:
                tag='frame'
                index=i.split('f')[0]
            driver.switch_to.frame(driver.find_elements_by_tag_name(tag)[int(index)])

def getWebElement(identifier):
    identifiers=identifier.split(';')
    webelement=None
    print(identifiers[0])
    tempwebElement = driver.find_elements_by_xpath(identifiers[0])
    print(tempwebElement,len(tempwebElement))
    if (len(tempwebElement) == 1):
        temp=tempwebElement[0]
        print('Webelement found by OI1')
    if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
        tempwebElement = driver.find_elements_by_id(identifiers[1])
        if (len(tempwebElement) == 1):
            temp=tempwebElement[0]
            print('Webelement found by OI2')
        if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
            tempwebElement = driver.find_elements_by_xpath(identifiers[2])
            if (len(tempwebElement) == 1):
                temp=tempwebElement[0]
                print('Webelement found by OI3')
            if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                tempwebElement = driver.find_elements_by_name(identifiers[3])
                if (len(tempwebElement) == 1):
                    temp=tempwebElement[0]
                    print('Webelement found by OI4')
                if ((len(tempwebElement) > 1) or (len(tempwebElement) == 0)):
                    tempwebElement = driver.find_elements_by_css_selector(identifiers[11])
                    if (len(tempwebElement) == 1):
                        temp=tempwebElement[0]
                        print('Webelement found by OI6')
                    else:
                        temp = None
    webelement = temp
    return webelement
start = timer()
"""
        self.web_keys = {
            # 'getobjectcount':local_Wd.custom_object.get_object_count,
            # 'getobject':local_Wd.custom_object.get_object,
            'click': element_obj.click,
            'press'  : element_obj.press,
            'doubleClick' : element_obj.doubleClick,
            'rightClick' : element_obj.rightClick,
            # 'uploadFile'  : element_obj.uploadFile,

            
            'verifyButtonName' : button_link_obj.verifyButtonName,
            'getButtonName': button_link_obj.getButtonName,
            'getLinkText'    : button_link_obj.getLinkText,
            'verifyLinkText' : button_link_obj.verifyLinkText,

            'acceptPopUp' : browser_popup_obj.acceptPopUp,
            'dismissPopUp':browser_popup_obj.dismissPopUp,
            'getPopUpText':browser_popup_obj.getPopUpText,
            'verifyPopUpText':browser_popup_obj.verifyPopUpText,


            'getStatus': radio_check_obj.getStatus,
            'selectRadioButton': radio_check_obj.selectRadioButton,
            'selectCheckbox': radio_check_obj.selectCheckbox,
            'unselectCheckbox': radio_check_obj.unselectCheckbox,

            'getRowCount' : table_obj.getRowCount,
            'getColumnCount' : table_obj.getColumnCount,
            'getCellValue' : table_obj.getCellValue,
            'verifyCellValue' : table_obj.verifyCellValue,
            'cellClick' : table_obj.cellClick,
            'getRowNumByText' : table_obj.getRowNumByText,
            'getColNumByText' : table_obj.getColNumByText,
            'getInnerTable' : table_obj.getInnerTable,
            'getCellToolTip' : table_obj.getCellToolTip,
            'verifyCellToolTip' : table_obj.verifyCellToolTip,

            'getElementText' : element_obj.getElementText,
            'verifyElementText' : element_obj.verifyElementText,
            'clickElement' : element_obj.click,
            'getToolTipText' : element_obj.getToolTipText,
            'verifyToolTipText' : element_obj.verifyToolTipText,
            'drag':util_obj.drag,
            'drop':util_obj.drop,
            # 'dropFile': element_obj.dropFile,

            'setText':textbox_obj.setText,
            'sendValue':textbox_obj.sendValue,
            'getText':textbox_obj.getText,
            'verifyText':textbox_obj.verifyText,
            'clearText':textbox_obj.clearText,
            'getTextboxLength':textbox_obj.getTextboxLength,
            'verifyTextboxLength':textbox_obj.verifyTextboxLength,
            'setSecureText':textbox_obj.setSecureText,
            'sendSecureValue':textbox_obj.sendSecureValue,

            'selectValueByIndex':dropdown_obj.selectValueByIndex,
            'getCount':dropdown_obj.getCount,
            'selectValueByText':dropdown_obj.selectValueByText,
            'verifySelectedValues':dropdown_obj.verifySelectedValues,
            'verifySelectedValue':dropdown_obj.verifySelectedValue,
            'verifyCount':dropdown_obj.verifyCount,
            'selectAllValues':dropdown_obj.selectAllValues,
            'selectMultipleValuesByIndexes':dropdown_obj.selectMultipleValuesByIndexes,
            'getSelected':dropdown_obj.getSelected,
            'selectMultipleValuesByText':dropdown_obj.selectMultipleValuesByText,
            'getMultipleValuesByIndexes':dropdown_obj.getMultipleValuesByIndexes,
            'verifyAllValues':dropdown_obj.verifyAllValues,
            'selectByAbsoluteValue':dropdown_obj.selectByAbsoluteValue,

            'getAllValues':dropdown_obj.getAllValues,
            'getValueByIndex':dropdown_obj.getValueByIndex,
            'verifyValuesExists':dropdown_obj.verifyValuesExists,
            'deselectAll':dropdown_obj.deselectAll,


            'verifyVisible':util_obj.verifyVisible,
            'verifyExists':util_obj.verifyExists,
            'verifyDoesNotExists':util_obj.verifyDoesNotExists,
            'verifyEnabled':util_obj.verifyEnabled,
            'verifyDisabled':util_obj.verifyDisabled,
            'verifyHidden':util_obj.verifyHidden,
            'verifyReadOnly':util_obj.verifyReadOnly,
            'tab':util_obj.tab,
            'sendFunctionKeys':util_obj.sendFunctionKeys,
            'setFocus':element_obj.setFocus,
            'mouseHover':element_obj.mouseHover,
            # 'rightclick':obj.rightclick,
            # 'mouseclick':util_obj.mouseClick,
            # 'verifywebimages':util_obj.verify_web_images,
            # 'imagesimilaritypercentage':util_obj.image_similarity_percentage,
            'waitForElementVisible':util_obj.waitForElementVisible,
            'getElementTagValue': element_obj.getElementTagValue,
            'getAttributeValue': element_obj.getAttributeValue,
            'verifyAttribute': element_obj.verifyAttribute,


            'openBrowser':browser_obj.openBrowser,
            'navigateToURL':browser_obj.navigateToURL,
            'getPageTitle':browser_obj.getPageTitle,
            'getCurrentURL':browser_obj.getCurrentURL,
            'maximizeBrowser':browser_obj.maximizeBrowser,
            'refresh':browser_obj.refresh,
            'verifyCurrentURL':browser_obj.verifyCurrentURL,
            'closeBrowser':browser_obj.closeBrowser,
            'closeSubWindows':browser_obj.closeSubWindows,
            'switchToWindow':browser_obj.switchToWindow,
            'verifyTextExists':browser_obj.verifyTextExists,
            'verifyPageTitle':browser_obj.verifyPageTitle,
            'clearCache':browser_obj.clearCache,
            'navigateWithAuthenticate':browser_obj.navigateWithAuthenticate,
            'navigateBack':browser_obj.navigateBack,
            'openNewTab':browser_obj.openNewTab,
            'execute_js':browser_obj.execute_js,
            'getBrowserName':browser_obj.getBrowserName
        }
        self.generic_keys={
            'toLowerCase': generic_string.toLowerCase,
            'toUpperCase' : generic_string.toUpperCase,
            'trim'    : generic_string.trim,
            'left'     : generic_string.left,
            'right'  : generic_string.right,
            'mid' : generic_string.mid,
            'getStringLength'      : generic_string.getStringLength,
            'find'      : generic_string.find,
            'replace':generic_string.replace,
            'split' : generic_string.split,
            'concatenate' : generic_string.concatenate,
            'getSubString':generic_string.getSubString,
            'stringGeneration':generic_string.stringGeneration,
            # 'savetoclipboard':generic_string.save_to_clip_board,
            # 'getfromclipboard':generic_string.get_from_clip_board,
            'getCurrentDate' : generic_date.getCurrentDate,
            'getCurrentTime' : generic_date.getCurrentTime,
            'getCurrentDateAndTime': generic_date.getCurrentDateAndTime,
            'getCurrentDay' : generic_date.getCurrentDay,
            'getCurrentDayDateAndTime' : generic_date.getCurrentDayDateAndTime,
            # 'dateDifference' : generic_date.dateDifference,
            # 'dateAddition'    : generic_date.dateAddition,
            # 'monthAddition'  :generic_date.monthAddition,
            # 'yearAddition' : generic_date.yearAddition,
            # 'changeDateFormat'     : generic_date.changeDateFormat,
            # 'dateCompare'  : generic_date.dateCompare,
            # 'saveFile':generic_file.saveFile,
            'createFile':generic_file.createFile,
            'renameFile':generic_file.renameFile,
            'deleteFile':generic_file.deleteFile,
            'verifyFileExists':generic_file.verifyFileExists,
            'createFolder':genric_folder.createFolder,
            'renameFolder':genric_folder.renameFolder,
            'deleteFolder':genric_folder.deleteFolder,
            'verifyFolderExists':genric_folder.verifyFolderExists,
            # 'comparecontent':generic_file.compare_content,
            # 'comparejsoncontent':generic_file.json_compare_content,
            # 'replacecontent':generic_file.replace_content,
            # 'verifycontent':generic_file.verify_content,
            # 'clearfilecontent':generic_file.clear_content,
            # 'getlinenumber':generic_file.get_line_number,
            # 'getcontent':generic_file.get_content,
            # 'writetofile':generic_file.write_to_file,
            # # 'writetocell':generic_excel.write_cell,
            # 'readcell':generic_excel.read_cell,
            # 'clearcell':generic_excel.clear_cell,
            # 'setexcelpath':generic_excel.set_excel_path,
            # 'storeexcelpath':generic_excel.set_excel_path,
            # 'clearexcelpath':generic_excel.clear_excel_path,
            # 'deleterow':generic_excel.delete_row,
            # 'getrowcount':generic_excel.get_rowcount,
            # 'getcolumncount':generic_excel.get_colcount,
            # 'runquery':generic_database.runQuery,
            # 'securerunquery': generic_database.secureRunQuery,
            # 'getdata':generic_database.getData,
            # 'securegetdata': generic_database.secureGetData,
            # 'exportdata':generic_database.exportData,
            # 'secureverifydata': generic_database.secureVerifyData,
            # 'verifydata':generic_database.verifyData,
            # 'secureexportdata': generic_database.secureExportData,
            # 'evallogicalexpression':generic_logical.eval_expression,
            # 'capturescreenshot':generic_screenshot.captureScreenshot,
            'executeFile':generic_util.executeFile,
            # 'evaluate':generic_util.eval,
            'wait':generic_util.wait,
            # 'pause':generic_delay.pause,
            # 'sendfunctionkeys':generic_sendkeys.sendfunction_keys,
            # 'getblockcount' : xml_oper.get_block_count,
            # 'gettagvalue' : xml_oper.get_tag_value,
            # 'getblockvalue' : xml_oper.get_block_value,
            # 'verifyobjects': xml_oper.verifyObjects,
            'typeCast':generic_string.typeCast,
            # 'verifyfileimages':util_operation_obj.verify_file_images,
            # 'imagesimilaritypercentage':util_operation_obj.image_similarity_percentage,
            'stop':generic_string.stop,
            'createDynVariable':dyn_var_obj.createDynVariable,
            'copyValue':dyn_var_obj.copyValue,
            'modifyValue':dyn_var_obj.modifyValue,
            'deleteDynVariable':dyn_var_obj.deleteDynVariable,
            # 'displayvariablevalue':generic_delay.display_variable_value,
            'verifyValues':generic_string.verifyValues,
            'getindexcount':generic_string.getIndexCount,
            # 'writewordfile': generic_word.writeWordFile,
            # 'readworddoc': generic_word.readWorddoc,
            # 'readallcheckbox': generic_word.readallcheckbox,
            # 'getalltablesfromdoc': generic_word.getAllTablesFromDoc,
            # 'readjson': generic_word.readjson,
            # 'readxml': generic_word.readxml,
            # 'readpdf': generic_word.readPdf,
            # 'getkeyvalue': json_oper.get_key_value,
            # 'comparefiles': generic_file_xml.compare_files,
            # 'beautify': generic_file_xml.beautify_file,
            # 'compareinputs': generic_file_xml.compare_inputs,
            # 'getxmlblockdata' :generic_file_xml.getXmlBlockData,
            # 'selectivexmlfilecompare' : generic_file_xml.selectiveXmlFileCompare,
            # 'compxmlfilewithxmlblock' : generic_file_xml.compXmlFileWithXmlBlock,
            # 'cellbycellcompare': generic_file.cell_by_cell_compare
            }



    def complie_TC(self,tsp,scenario_name,browser,index,execute_result_data,socketIO):
        try:
            self.f.write(self.code)
            from collections import deque
            stack = deque()
            flag=True
            space="\n"
            overall_status="Pass"
            stack1 = deque()
            for i in tsp:
                if i.name in ['if','elseIf','for']:
                    stack1.append(i.name)
                elif i.name=='endIf' and stack1[-1] in ['if','elseIf']:
                    stack1.pop()
                elif i.name=='endFor' and stack1[-1] == 'for':
                    stack1.pop()
            if (len(stack1)!=0):
                logger.print_on_console("Dangling if/for statement")
                return False
            path=Saucelabs_tests+os.sep+scenario_name+index+'.txt'
            path=path.replace('\\','\\\\')
            self.f.write("\nf=open('"+path+"','w+')")
            step_index=0        
            for i in tsp:
                step={
                    "name":i.name,
                    "stepnum": "Step"+str(i.stepnum),
                    "testscript_name": i.testscript_name,
                    "inputval":i.inputval,
                    "apptype":i.apptype,
                    "index":step_index
                }
                step_index += 1
                all_input=i.inputval[0].split(';')
                input_value=[]
                for inp in all_input:
                    if ('{' in inp and '}' in inp):
                        inputs="check_dyn_var("+repr(inp.split("{")[1].split("}")[0])+")"
                    else:
                        inputs="'"+inp+"'"
                    input_value.append(inputs)
                if i.apptype == 'Generic':
                    if i.name =='for':
                        self.f.write(space+"input=int("+input_value[0][1:-1]+")+1")
                        self.f.write(space+"for i in range(1,input):")
                        self.f.write(space+"\toutput=i")
                        self.f.write(space+"\tstatus='Pass'")
                        self.f.write(space+"\taddTeststep("+repr(step)+")")
                        space=space+"\t"
                        stack.append("for")
                    elif i.name == 'if':
                        if "check_dyn_var(" not in input_value[0]:
                            input_value[0]=input_value[0].replace("(","")
                        if "check_dyn_var(" not in input_value[2]:
                            input_value[2]=input_value[2].replace(")","")
                        # input=""+check_dyn_var('MsgCancel')+"=="+check_dyn_var('MsgCancel')
                        self.f.write(space+"expr='\"'+str("+input_value[0]+")+'\"'+"+input_value[1]+"+'\"'+str("+input_value[2]+")+'\"'")
                        self.f.write(space+"output=str(eval(expr))")
                        self.f.write(space+"addTeststep("+repr(step)+")")
                        self.f.write(space+"if eval(expr):")
                        self.f.write(space+"\tstatus='Pass'")
                        space+='\t'
                        stack.append("if")
                    elif i.name == 'elseIf':
                        if stack[-1]=='if' or stack[-1]=='elseIf':
                            space=space[:-1]
                            self.f.write(space+"expr=''+"+input_value[0]+"+"+input_value[1]+"+"+input_value[2])
                            self.f.write(space+"output=str(eval(expr))")
                            self.f.write(space+"addTeststep("+repr(step)+")")
                            self.f.write(space+"elif eval(expr):")
                            self.f.write(space+"\tstatus='Pass'")
                            space+='\t'
                            stack.append("elif")
                        else:
                            logger.print_on_console("Dangling: elseIf in " +str(i.testscript_name))
                            return False
                    elif i.name == 'endIf':
                        if stack[-1]=='if' or stack[-1]=='elseIf' or stack[-1]=='else':
                            self.f.write(space+"output=''")
                            self.f.write(space+"status='Pass'")
                            stack.pop()
                            if ('{' in i.outputval and '}' in i.outputval):
                                self.f.write(space+"store_dyn_var("+repr(i.outputval)+")")
                            space=space[:-1]
                            self.f.write(space+"addTeststep("+repr(step)+")")
                        else:
                            logger.print_on_console("Dangling: endIf in " +str(i.testscript_name))
                            return False
                    elif i.name == 'endFor':
                        if stack[-1]=='for':
                            self.f.write(space+"output=''")
                            self.f.write(space+"status='Pass'")
                            stack.pop()
                            if ('{' in i.outputval and '}' in i.outputval):
                                self.f.write(space+"store_dyn_var("+repr(i.outputval)+")")
                            self.f.write(space+"addTeststep("+repr(step)+")")
                            space=space[:-1]
                        else:
                            logger.print_on_console("Dangling: elseFor in " +str(i.testscript_name))
                            return False
                    elif i.name == 'else':
                        if stack[-1]=='if' or stack[-1]=='elseIf':
                            space=space[:-1]
                            self.f.write(space+"\taddTeststep("+repr(step)+")")
                            self.f.write(space+"else:")
                            self.f.write(space+"\tstatus='Pass'")
                            space+='\t'
                            stack.append("else")
                        else:
                            logger.print_on_console("Dangling: else in " +str(i.testscript_name))
                            return False
                    elif i.name in self.generic_keys:
                        self.f.write(space+"try:")
                        space+='\t'
                        self.generic_keys[i.name](space,input_value)
                        space=space[:-1]
                        self.f.write(space+"except Exception as e:")
                        self.f.write(space+"\toutput='False'")
                        self.f.write(space+"\terr_msg='Input error: please provide the valid input.'")
                        self.f.write(space+"\tprint(e)")
                        if ('{' in i.outputval and '}' in i.outputval):
                            self.f.write(space+"store_dyn_var("+repr(i.outputval)+")")
                        self.f.write(space+"addTeststep("+repr(step)+")")
                    else:
                        logger.print_on_console(i.name+" keyword is not supported in saucelabs execution.")
                        return False
                    
                    
                elif i.apptype == 'Web':
                    self.f.write(space+"try:")
                    space+='\t'
                    if i.custname=='@Generic':
                        if flag != False:
                            if i.name in self.generic_keys:
                                self.generic_keys[i.name](space,input_value)
                            else:
                                logger.print_on_console(i.name+" keyword is not supported in saucelabs execution.")
                                return False
                    elif i.custname=='@Browser' or i.custname=='@BrowserPopUp':
                        if(i.name=="openBrowser"):
                            self.browsers[browser]["platform"]=self.conf["platform"]
                            self.browsers[browser]["sauce:options"].update({"name":scenario_name})
                            self.browsers[browser]["sauce:options"].update({"idleTimeout":10})
                            self.web_keys[i.name](space,self.conf['remote_url'],self.browsers[browser])
                        else:
                            self.web_keys[i.name](space,input_value)
                    elif i.custname=='@Custom':
                        logger.print_on_console("@Custom is not supported in saucelabs execution.")
                        return False
                    else:
                        if i.name in self.web_keys:
                            xpath=i.objectname.split(';')[0]
                            if(i.name=="waitForElementVisible"):
                                input_value="'"+xpath+"'"
                            self.f.write(space+"check_url("+repr(i.url)+")")
                            a=i.objectname.split(';')
                            a[10]=''
                            i.objectname=';'.join(a)
                            self.f.write(space+"webelement=getWebElement("+repr(i.objectname)+")")
                            self.f.write(space+"if webelement!=None:")
                            space=space+"\t"
                            webelement="webelement"
                            self.web_keys[i.name](space,webelement,input_value)
                            space=space[:-1]
                        else:
                            logger.print_on_console(i.name+" keyword is not supported in saucelabs execution.")
                            return False
                    space=space[:-1]
                    self.f.write(space+"except Exception as e:")
                    self.f.write(space+"\tif hasattr(e,'msg') and e.msg.find(\"can't receive further commands\")!=-1:")
                    self.f.write(space+"\t\texit()")
                    self.f.write(space+"\toutput='False'")
                    self.f.write(space+"\terr_msg='Input error: please provide the valid input.'")
                    self.f.write(space+"\tprint(e)")
                    if ('{' in i.outputval and '}' in i.outputval):
                        self.f.write(space+"store_dyn_var("+repr(i.outputval)+")")
                    self.f.write(space+"addTeststep("+repr(step)+")")
            self.f.write("\nf.close()")
            # self.f.write("\nprint(driver.session_id)")
            self.f.close()
            from datetime import datetime
            now=datetime.now()
            file_py=Saucelabs_tests+os.sep+scenario_name+index
            p = subprocess.Popen('python -m pytest "'+file_py+'.py"', stdout=subprocess.PIPE, bufsize=1, shell=True, cwd=python_cwd)
            output=p.stdout.readlines()
            p.wait()
            flag=True
            f1=open(self.filename1,"r")
            steps=f1.readlines()
            report=json.loads(steps[0].replace("'",'"'))
            apptype_description={'generic':self.step_description_obj.generic,
            'web':self.step_description_obj.web}
            tsp_index=0
            for i in range(0,len(report)):
                if report[i]['Keyword'] in ['if','elseIf']:
                    report[i]['StepDescription'] = 'Encountered :'+report[i]['Keyword']+' Condition is '+report[i]['output']
                    del report[i]['input'],report[i]['output'],report[i]['dyn_var_map'],report[i]['apptype'],report[i]['index'],report[i]['inputval']
                elif report[i]['Keyword'] == 'endIf':
                    report[i]['StepDescription'] = 'Encountered :endIf'
                    del report[i]['input'],report[i]['output'],report[i]['dyn_var_map'],report[i]['apptype'],report[i]['index'],report[i]['inputval']
                if report[i]['StepDescription'] == '':
                    report[i]['StepDescription'] = apptype_description[report[i]['apptype'].lower()](report[i]['Keyword'],tsp[report[i]['index']],report[i]['inputval'],report[i]['input'],report[i]['output'])
                    if report[i]['status']=='Fail':
                        overall_status='Fail'
                    del report[i]['input'],report[i]['output'],report[i]['dyn_var_map'],report[i]['apptype'],report[i]['index'],report[i]['inputval']
            sc = self.obj.get_sauceclient()
            j = self.obj.get_saucejobs(sc)
            all_jobs=j.get_jobs(start=int(now.timestamp()),full=True)
            time.sleep(5)
            import constants
            filename = datetime.now().strftime("%Y%m%d%H%M%S")
            dirpath = constants.SCREENSHOT_PATH if (constants.SCREENSHOT_PATH not in ['screenshot_path', 'Disabled']) else Saucelabs_tests+os.sep
            video_path = dirpath+'ScreenRecording_' +filename + '.mp4'
            for i in range(0,len(all_jobs)):
                file_creations_status=j.get_job_asset_content(all_jobs[i]['id'],filename,dirpath)
                status=all_jobs[i]['error']
                import controller
                if controller.terminate_flag:
                    overall_status="Terminate"
                    step={
                        "id": len(report)+1,
                        "Keyword": "",
                        "parentId": "",
                        "Comments": "",
                        "Step": "Terminated",
                        "StepDescription": "Terminated by the user"
                    }
                    report.append(step)
                    flag='Terminate'
            overallstatus=self.build_overallstatus(self.browsers[browser]['browserName'],overall_status,all_jobs[i],j,video_path)
            execute_result_data['reportData'] = { 'rows' : report, "overallstatus" : overallstatus}
            socketIO.emit('result_executeTestSuite', execute_result_data)
            f1.close()
            return flag
        except Exception as e:
            logger.print_on_console("Error in Sauce Labs Execution")
            log.error(e)
            self.f.close()
            f1.close()
            return False

    def build_overallstatus(self,browser,overall_status,jobs,j,video_path):
        """
        def : build_overallstatus
        purpose : builds the overallstatus field of report_json
        param : start_time,end_time,ellapsed_time

        """
        # if self.overallstatus==TERMINATE:
            # self.add_termination_step()
        # self.start_time=str(start_time)
        # self.end_time=str(end_time)
        # self.ellapsed_time=str(ellapsed_time)
        import time
        while(jobs['consolidated_status'].lower() == 'in progress'):
            time.sleep(5)
            jobs=j.get_job(jobs['id'])
        start=datetime.fromtimestamp(jobs['start_time'])
        end=datetime.fromtimestamp(jobs['end_time'])
        getTym = end.strftime('%Y-%m-%d %H:%M:%S')
        getDat = getTym.split(" ")[0].split("-")
        date1 = getDat[1] + "/" + getDat[2] + "/" + getDat[0]
        time1 = getTym.split(" ")[1]
        elap = end - start
        obj={}
        obj['EllapsedTime']=str(elap)
        obj['EndTime']=end.strftime('%Y-%m-%d %H:%M:%S.%f')
        obj['browserVersion']=jobs['browser_version']
        obj['StartTime']=start.strftime('%Y-%m-%d %H:%M:%S.%f')
        obj['overallstatus']=overall_status
        obj['browserType']=browser
        obj['date']=date1
        obj['time']=time1
        obj['video']=video_path
        return [obj]

class Sauce_Config():

    def get_sauceconf(self):
        # conf_obj = open(Saucelabs_config_path, 'r')
        # conf = json.load(conf_obj)
        # conf_obj.close()
        # # self.proxies=self.conf["proxy"]
        # self.username = conf["sauce_username"]
        # self.access_key = conf["sauce_access_key"]
        # self.platform = conf["platform"]
        # self.url = conf["remote_url"]
        # Saucelabs_config_path=os.environ['AVO_ASSURE_HOME']+os.sep+'assets'+os.sep+'sauce_config.json'
        import saucelab_constants
        conf = {
            'platform': saucelab_constants.Platform,
            'version': saucelab_constants.Version,
            'sauce_username': saucelab_constants.Saucelabs_Username,
            'sauce_access_key': saucelab_constants.Saucelabs_key,
            'remote_url': saucelab_constants.SaucelabsURL
        }
        # conf_obj = open(Saucelabs_config_path, 'r')
        # conf_obj.close()
        # self.proxies=self.conf["proxy"]
        self.username = conf["sauce_username"]
        self.access_key = conf["sauce_access_key"]
        self.platform = conf["platform"]
        self.url = conf["remote_url"]
        return conf
        return conf

    def get_sauceclient(self):
        return sauceclient.SauceClient(self.username,self.access_key)

    def get_saucejobs(self, sc):
        return sauceclient.Jobs(sc)