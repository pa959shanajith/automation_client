import os
filename=""
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from timeit import default_timer as timer
from datetime import timedelta
import time
from constants import *
import sauceclient
import threading
local_wk=threading.local()
log=logging.getLogger('web_keywords.py')
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

class Browser_Keywords:

    def __init__(self):
        self.obj=Textbox_Keywords()
        pass
    
    def openBrowser(self,url,browser,scenario,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        # browser={'browserName': "chrome",'sauce:options':{'name':scenario}}
        local_wk.driver = webdriver.Remote(command_executor=url, desired_capabilities=browser)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def navigateToURL(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        url=input[0]
        if url[0:7].lower()!='http://' and url[0:8].lower()!='https://' and url[0:5].lower()!='file:':
            url='http://'+url
        input=url
        local_wk.driver.get(input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def maximizeBrowser(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        local_wk.driver.maximize_window()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg
    
    def verifyPageTitle(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        inp_title=input[0]
        input=inp_title
        title=local_wk.driver.title
        output_val= 'True' if title==input else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg 

    def getPageTitle(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val=local_wk.driver.title
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getCurrentURL(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val=local_wk.driver.current_url
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getBrowserName(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val=local_wk.driver.name
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg
    
    def verifyCurrentURL(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        inp_url=input[0]
        input=inp_url
        url=local_wk.driver.current_url
        output_val = 'True' if url==input else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg 
    
    def openNewTab(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        local_wk.driver.execute_script('window.open('');')
        local_wk.driver.switch_to.window(local_wk.driver.window_handles[int(local_wk.driver.window_handles.index(local_wk.driver.current_window_handle))+1])
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def refresh(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        local_wk.driver.refresh()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def navigateBack(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        local_wk.driver.execute_script('window.history.go(-1)')
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg
    
    def closeSubWindows(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        # if(input[0].lower()=='all'):
        # else:
        local_wk.driver.close()
        local_wk.driver.switch_to.window(local_wk.driver.window_handles[-1])
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg
    
    def switchToWindow(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        local_wk.driver.switch_to.window(local_wk.driver.window_handles[int(input[0])-1])
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg
    
    def navigateWithAuthenticate(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input_val=input
        url=input_val[0]
        user=input_val[1]
        password=self.obj.decrypt(input_val[2])
        if url[0:7].lower() == 'http://': url=url[0:7]+user+':'+password+'@'+url[7:]
        elif url[0:8].lower() == 'https://': url=url[0:8]+user+':'+password+'@'+url[8:]
        # url=url)
        input=[url,user,password]
        local_wk.driver.get(url)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def execute_js(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        local_wk.driver.execute_script(inputval)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def clearCache(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        if local_wk.driver != None:
            if local_wk.driver.name == 'internet explorer' or local_wk.driver.name == 'MicrosoftEdge':
                local_wk.driver.delete_all_cookies()
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            elif local_wk.driver.name == 'chrome':
                local_wk.driver.get('chrome://settings/clearBrowserData')
                time.sleep(5)
                local_wk.driver.execute_script('return document.querySelector("body > settings-ui").shadowRoot.querySelector("#container").querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("settings-privacy-page").shadowRoot.querySelector("settings-clear-browsing-data-dialog").shadowRoot.querySelector("#clearBrowsingDataDialog").querySelector("#clearBrowsingDataConfirm").click();')
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            elif local_wk.driver.name=='msedge':
                local_wk.driver.get('edge://settings/clearBrowserData')
                time.sleep(5)
                local_wk.driver.execute_script('return document.getElementById("clear-now").click();')
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            elif local_wk.driver.name=='firefox':
                local_wk.driver.get('about:preferences#privacy')
                time.sleep(5)
                local_wk.driver.find_element_by_css_selector('#clearSiteDataButton').click()
                time.sleep(5)
                local_wk.driver.execute_script("document.getElementsByTagName('browser')[0].contentWindow.document.getElementsByTagName('dialog')[0].shadowRoot.children[3].children[2].click()")
                time.sleep(5)
                local_wk.driver.switch_to.alert.accept()
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyTextExists(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        occurrences_javascript = "function occurrences(string, subString, allowOverlapping) {      string += '';     subString += '';     if (subString.length <= 0) return (string.length + 1);      var n = 0,pos = 0,step = allowOverlapping ? 1 : subString.length;      while (true) {         pos = string.indexOf(subString, pos);         if (pos >= 0) {             ++n;             pos += step;         } else break;     }     return n; }; function saddNodesOuter(sarray, scollection) { 	for (var i = 0; scollection && scollection.length && i < scollection.length; i++) { 		sarray.push(scollection[i]); 	} }; function stext_content(f) { 	var sfirstText = ''; 	var stextdisplay = ''; 	for (var z = 0; z < f.childNodes.length; z++) { 		var scurNode = f.childNodes[z]; 		swhitespace = /^\\s*$/; 		if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) { 			sfirstText = scurNode.nodeValue; 			stextdisplay = stextdisplay + sfirstText; 		} 	} 	return (stextdisplay); }; var sae = []; var substr = arguments[0]; var sele = arguments.length > 1 ? arguments[1].getElementsByTagName('*') :  document.getElementsByTagName('*'); var text_occurrences = 0; saddNodesOuter(sae, sele);  for(var j=0;j<sae.length;j++){ 	stagname = sae[j].tagName.toLowerCase(); 	 	if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') { 		text_occurrences += occurrences(stext_content(sae[j]),substr); 	} 	 }; return text_occurrences;bstr = arguments[0]; var sele = arguments.length > 1 ? arguments[1].getElementsByTagName('*') :  document.getElementsByTagName('*'); var text_occurrences = 0; saddNodesOuter(sae, sele);  for(var j=0;j<sae.length;j++){ 	stagname = sae[j].tagName.toLowerCase(); 	 	if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') { 		text_occurrences += occurrences(stext_content(sae[j]),substr); 	} 	 }; return text_occurrences;"
        output_val=int(local_wk.driver.execute_script(occurrences_javascript,input))
        status=TEST_RESULT_PASS if output_val != 0 else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg 

    def closeBrowser(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        local_wk.driver.quit()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

class Browser_Popup_Keywords():

    def __init__(self):
        pass

    def acceptPopUp(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        local_wk.driver.switch_to.alert.accept()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg 
    
    def dismissPopUp(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        local_wk.driver.switch_to.alert.dismiss()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg 

    def getPopUpText(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val=local_wk.driver.switch_to.alert.text
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg 
    
    def verifyPopUpText(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        text=input[0]
        input=text
        popup_text = local_wk.driver.switch_to.alert.text
        output_val='True' if popup_text==input else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg 

class Button_link_Keywords():

    def __init__(self):
        pass

    def getButtonName(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        buttontext=webelement.text
        buttontext=webelement.get_attribute('value') if buttontext == None or buttontext == '' else buttontext
        output_val=buttontext
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg 

    def verifyButtonName(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        verify_button=input[0]
        input=verify_button
        buttontext=webelement.text
        buttontext=webelement.get_attribute('value') if buttontext == None or buttontext == '' else buttontext
        output_val='True' if buttontext == input else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getLinkText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        linktext=webelement.get_attribute('href')
        linktext=webelement.text if linktext == None or linktext == '' else linktext
        output_val=linktext
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg 

    def verifyLinkText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        verify_link=input[0]
        input=verify_link
        linktext=webelement.get_attribute('href')
        linktext=webelement.text if linktext == None or linktext == '' else linktext
        output_val='True' if linktext == input else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg
            
class Dropdown_Keywords():

    def __init__(self):
        pass

    def selectAllValues(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        select = Select(webelement)
        for i in range(0,len(select.options)):
            input=select.options[i].text
            None if select.options[i].is_selected() else select.select_by_visible_text(input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg
        
    def selectValueByIndex(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        local_wk.driver.execute_script('arguments[0].selectedIndex=arguments[1]',webelement,input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def selectMultipleValuesByIndexes(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        for i in input:
            input1=i
            local_wk.driver.execute_script('arguments[0].options[arguments[1]].selected=true',webelement,int(input1)-1)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getMultipleValuesByIndexes(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        total=local_wk.driver.execute_script('return arguments[0].childElementCount', webelement)
        output_val=[]
        for inputindex in input:
            output_val.append(str(local_wk.driver.execute_script('return arguments[0].options[arguments[1]].text', webelement,int(inputindex)-1)))
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyValuesExists(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        select = Select(webelement)
        option_len = select.options
        opt_len = len(option_len)
        inp_val_len = len(input)
        temp=[]
        count=0
        [temp.append(select.options[x].text.strip()) for x in range(0,opt_len)]
        for y in range(0,inp_val_len):
            input_temp = input[y].strip()
            if (input_temp in temp):
                count+=1
            else:
                break
        if count == inp_val_len:
            output_val = 'True'
        else:
            output_val = 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def selectByAbsoluteValue(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        select = Select(webelement)
        select.select_by_visible_text(input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def selectValueByText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        select = Select(webelement)
        select.select_by_visible_text(input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def selectMultipleValuesByText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        select = Select(webelement)
        for i in input:
            input1=i
            select.select_by_visible_text(input1)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getCount(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        select = Select(webelement)
        iList = select.options
        iListSize = len(iList)
        output_val=iListSize
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyCount(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        select = Select(webelement)
        iList = select.options
        iListSize = len(iList)
        output_val='True' if iListSize == int(input) else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifySelectedValue(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        select = Select(webelement)
        if '[' in input[0]:
            input=input[0][2:-2]
        else: input=input[0]
        first_value = select.first_selected_option.text
        output_val='True' if first_value == input else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifySelectedValues(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        import json
        temp=input[0]
        temp=temp.replace("\'",'\"')
        temp=json.loads(temp)
        all_value=[]
        select = Select(webelement)
        opt_len = len(select.all_selected_options)
        for x in range(0,opt_len): all_value.append(select.all_selected_options[x].text)
        import copy
        temp1=copy.deepcopy(all_value)
        for i in range(0,len(temp)):
            if temp[i] in all_value:
                temp1.remove(temp[i])
        output_val='True' if len(temp1)==0 else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getAllValues(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        select = Select(webelement)
        opt_len = len(select.options)
        temp=[]
        for x in range(0,opt_len): temp.append(select.options[x].text)
        output_val=temp
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg
    
    def getSelected(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        select = Select(webelement)
        opt_len = len(select.all_selected_options)
        temp=[]
        for x in range(0,opt_len): temp.append(select.all_selected_options[x].text)
        output_val=temp
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg
    
    def verifyAllValues(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        select = Select(webelement)
        opt_len = len(select.options)
        temp=[]
        flag=True
        for x in range(0,opt_len): 
            temp.append(select.options[x].text)
        for i in input:
            if i not in temp:
                flag=False
                break
        output_val='True' if flag else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getValueByIndex(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        select = Select(webelement)
        output_val=select.options[int(input)].text
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def deselectAll(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        select = Select(webelement)
        select.deselect_all()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

class Element_Keywords:

    def __init__(self):
        pass

    def click(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        local_wk.driver.execute_script("var evType; element=arguments[0]; if (document.createEvent) {     evType = 'Click executed through part-1';     var evt = document.createEvent('MouseEvents');     evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = 'Click executed through part-2';   	setTimeout(function() {     element.click();   	}, 100); } return (evType);",webelement)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def press(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        webelement.click()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg
    
    def doubleClick(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        webdriver.ActionChains(local_wk.driver).move_to_element(webelement).double_click(webelement).perform()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def rightClick(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        webdriver.ActionChains(local_wk.driver).move_to_element(webelement).context_click(webelement).perform()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getAttributeValue(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        attr_name=input[0]
        input=attr_name
        output_val=webelement.get_attribute(input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyAttribute(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input_val=input
        input=input_val[0]
        input1=input_val[1]
        attr_val=webelement.get_attribute(input)
        output_val='True' if attr_val == input1 else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def mouseHover(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        webdriver.ActionChains(local_wk.driver).move_to_element(webelement).perform()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def setFocus(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        local_wk.driver.execute_script('arguments[0].focus();',webelement)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getElementTagValue(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val=webelement.tag_name
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg
    
    def uploadFile(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0].replace("\\","/")
        input=input
        webelement.send_keys(input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def dropFile(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0].replace("\\","/")
        input=input
        webelement.send_keys(input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getElementText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        text=webelement.get_attribute('value')
        if(text is None or text is ''): text=webelement.get_attribute('name')
        if(text is None or text is ''): text=webelement.get_attribute('title')
        if(text is None or text is ''): text=webelement.get_attribute('placeholder')
        output_val=text
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg
    
    def verifyElementText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        text=webelement.get_attribute('value')
        if(text is None or text is ''): text=webelement.get_attribute('name')
        if(text is None or text is ''): text=webelement.get_attribute('title')
        if(text is None or text is ''): text=webelement.get_attribute('placeholder')
        output_val='True' if text == input else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getToolTipText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val=webelement.get_attribute('title')
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyToolTipText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        tooltip=webelement.get_attribute('title')
        output_val='True' if tooltip == input else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

class Radio_checkbox_Keywords():

    def __init__(self):
        pass

    def selectRadioButton(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        webelement.click()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getStatus(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val='selected' if webelement.is_selected() else 'unselected'
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def selectCheckbox(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        if webelement.is_selected():
            err_msg=ERROR_CODE_DICT['ERR_OBJECTSELECTED']
        else:
            webelement.click()
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def unselectCheckbox(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        webelement.click()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

class Table_Keywords():

    def __init__(self):
        pass

    def getRowCount(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val=local_wk.driver.execute_script('var targetTable = arguments[0]; var rowCount = targetTable.rows; return rowCount.length;',webelement)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getColumnCount(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val=local_wk.driver.execute_script('var targetTable = arguments[0]; var columnCount = 0; var rows = targetTable.rows; if(rows.length > 0) { 	for (var i = 0; i < rows.length; i++) { 		var cells = rows[i].cells; 		var tempColumnCount = 0; 		for (var j = 0; j < cells.length; j++) { 			tempColumnCount += cells[j].colSpan; 		} 		if (tempColumnCount > columnCount) { 			columnCount = tempColumnCount; 		} 	} } return columnCount;',webelement)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getRowNumByText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val=local_wk.driver.execute_script('var temp = fun(arguments[0], arguments[1]); return temp; function fun(table, str) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy, child;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (cell.innerText.indexOf(str)>= 0) return yyy + cell.rowSpan;             else if (cell.children.length > 0) {                 for (var i = 0; i < cell.children.length; i++) {                     child = cell.children[i];                     if (child.value == str) return yyy + cell.rowSpan; 					else{ 					var a=child.value; 					if(a){ 					var b=a; 					if(b.indexOf(str)>=0)return yyy + cell.rowSpan; 					}	 				}			 					                 }             }         }     }     return null; };',webelement,input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getColNumByText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val=local_wk.driver.execute_script('var temp = fun(arguments[0], arguments[1]); return temp; function fun(table, str) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy, child;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (cell.innerText.indexOf(str)>= 0) return xx + cell.colSpan;             else if (cell.children.length > 0) {                 for (var i = 0; i < cell.children.length; i++) {                     child = cell.children[i];                     if (child.value == str) return xx + cell.colSpan; 					else{ 					var a=child.value; 					if(a){ 					var b=a; 					if(b.indexOf(str)>=0)return xx + cell.colSpan; 					}	 				}			 					                 }             }         }     }     return null; };',webelement,input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg
    
    def getCellValue(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        row=input[0]
        col=input[1]
        remoteele=local_wk.driver.execute_script('var temp = fun(arguments[0], arguments[2], arguments[1]); return temp;  function fun(table, x, y) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (xx <= x && x < xx + cell.colSpan && yyy <= y && y < yyy + cell.rowSpan) return cell;         }     }     return null; };',webelement,int(row)-1,int(col)-1)
        output_val=local_wk.driver.execute_script("var mytarget = arguments[0]; var mynodes = mytarget.childNodes; var result = []; if (typeof  String.prototype.trim  !== 'function')  {       String.prototype.trim  =   function()  {             return  this.replace(/^\\s+|\\s+$/g,'');        } } recursfunc(mynodes); return result.toString();  function recursfunc(mynodes) {     for (var i = 0; i < mynodes.length; i++) {         if (mynodes[i].nodeName.toUpperCase() == \'#TEXT\') {             if ((mynodes[i].parentNode.nodeName.toUpperCase() != \'OPTION\') & (mynodes[i].parentNode.nodeName.toUpperCase() != \'SCRIPT\')) {                 var myvalue = mynodes[i].nodeValue;                 if (myvalue.trim().length > 0) {                     result.push(myvalue);                 }             }         } else if (mynodes[i].nodeName.toUpperCase() == \'INPUT\') {             if (mynodes[i].type.toUpperCase() == \'RADIO\') {                 if (mynodes[i].checked == true) {                     var myvalue = \'Selected\';                 } else {                     var myvalue = \'Unselected\';                 }             } else if (mynodes[i].type.toUpperCase() == \'CHECKBOX\') {                 if (mynodes[i].checked == true) {                     var myvalue = \'Checked\';                 } else {                     var myvalue = \'Unchecked\';                 }             } else if ((mynodes[i].type.toUpperCase() == \'BUTTON\') | (mynodes[i].type.toUpperCase() == \'SUBMIT\') | (mynodes[i].type.toUpperCase() == \'TEXT\')) {                 var myvalue = mynodes[i].value;             } else if (mynodes[i].type.toUpperCase() == \'IMAGE\') {                 var myvalue = mynodes[i].title;                 if (myvalue.trim().length < 1) {                     myvalue = mynodes[i].value;                     if (myvalue != undefined) {                         if (myvalue.trim().length < 1) {                             myvalue = \'Image\';                         }                     } else {                         myvalue = \'Image\';                     }                 }             }else{ var myvalue=mynodes[i].value; }             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \'IMG\') {             var myvalue = mynodes[i].title;             if (myvalue.trim().length < 1) {                 myvalue = mynodes[i].value;                 if (myvalue != undefined) {                     if (myvalue.trim().length < 1) {                         myvalue = \'Image\';                     }                 } else {                     myvalue = \'Image\';                 }             }             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \'TEXTAREA\') {             var myvalue = mynodes[i].value;             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \'SELECT\') {             var myselect = mynodes[i].selectedOptions;             if (myselect != undefined | myselect != null) {                 for (var j = 0; j < myselect.length; j++) {                     var myvalue = mynodes[i].selectedOptions[j].textContent;                     result.push(myvalue);                 }             } else {                 var myvalue = dropdowncallie(mynodes[i]);                 result.push(myvalue);             }         } else if ((mynodes[i].nodeName.toUpperCase() == \'I\')) {             var myvalue = mynodes[i].textContent;             result.push(myvalue);         }         if (mynodes[i].hasChildNodes()) {             recursfunc(mynodes[i].childNodes);         }     } }  function dropdowncallie(op) {     var x = op.options[op.selectedIndex].text;     return x; };",remoteele)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyCellValue(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        row=input[0]
        col=input[1]
        input=input[2]
        remoteele=local_wk.driver.execute_script('var temp = fun(arguments[0], arguments[2], arguments[1]); return temp;  function fun(table, x, y) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (xx <= x && x < xx + cell.colSpan && yyy <= y && y < yyy + cell.rowSpan) return cell;         }     }     return null; };',webelement,int(row)-1,int(col)-1)
        content=local_wk.driver.execute_script("var mytarget = arguments[0]; var mynodes = mytarget.childNodes; var result = []; if (typeof  String.prototype.trim  !== 'function')  {       String.prototype.trim  =   function()  {             return  this.replace(/^\\s+|\\s+$/g,'');        } } recursfunc(mynodes); return result.toString();  function recursfunc(mynodes) {     for (var i = 0; i < mynodes.length; i++) {         if (mynodes[i].nodeName.toUpperCase() == \'#TEXT\') {             if ((mynodes[i].parentNode.nodeName.toUpperCase() != \'OPTION\') & (mynodes[i].parentNode.nodeName.toUpperCase() != \'SCRIPT\')) {                 var myvalue = mynodes[i].nodeValue;                 if (myvalue.trim().length > 0) {                     result.push(myvalue);                 }             }         } else if (mynodes[i].nodeName.toUpperCase() == \'INPUT\') {             if (mynodes[i].type.toUpperCase() == \'RADIO\') {                 if (mynodes[i].checked == true) {                     var myvalue = \'Selected\';                 } else {                     var myvalue = \'Unselected\';                 }             } else if (mynodes[i].type.toUpperCase() == \'CHECKBOX\') {                 if (mynodes[i].checked == true) {                     var myvalue = \'Checked\';                 } else {                     var myvalue = \'Unchecked\';                 }             } else if ((mynodes[i].type.toUpperCase() == \'BUTTON\') | (mynodes[i].type.toUpperCase() == \'SUBMIT\') | (mynodes[i].type.toUpperCase() == \'TEXT\')) {                 var myvalue = mynodes[i].value;             } else if (mynodes[i].type.toUpperCase() == \'IMAGE\') {                 var myvalue = mynodes[i].title;                 if (myvalue.trim().length < 1) {                     myvalue = mynodes[i].value;                     if (myvalue != undefined) {                         if (myvalue.trim().length < 1) {                             myvalue = \'Image\';                         }                     } else {                         myvalue = \'Image\';                     }                 }             }else{ var myvalue=mynodes[i].value; }             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \'IMG\') {             var myvalue = mynodes[i].title;             if (myvalue.trim().length < 1) {                 myvalue = mynodes[i].value;                 if (myvalue != undefined) {                     if (myvalue.trim().length < 1) {                         myvalue = \'Image\';                     }                 } else {                     myvalue = \'Image\';                 }             }             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \'TEXTAREA\') {             var myvalue = mynodes[i].value;             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \'SELECT\') {             var myselect = mynodes[i].selectedOptions;             if (myselect != undefined | myselect != null) {                 for (var j = 0; j < myselect.length; j++) {                     var myvalue = mynodes[i].selectedOptions[j].textContent;                     result.push(myvalue);                 }             } else {                 var myvalue = dropdowncallie(mynodes[i]);                 result.push(myvalue);             }         } else if ((mynodes[i].nodeName.toUpperCase() == \'I\')) {             var myvalue = mynodes[i].textContent;             result.push(myvalue);         }         if (mynodes[i].hasChildNodes()) {             recursfunc(mynodes[i].childNodes);         }     } }  function dropdowncallie(op) {     var x = op.options[op.selectedIndex].text;     return x; };",remoteele)
        output_val='True' if content == input else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getCellToolTip(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        row=input[0]
        col=input[1]
        output_val=local_wk.driver.execute_script("var temp = tooltip(arguments[0], arguments[1], arguments[2]); return temp; function tooltip(table, row, col) {     var no_of_rows = table.rows.length;     var no_of_col = table.rows[row - 1].cells.length;     var ele = table.rows[row - 1];     var i, j, k, tp;     for (i = 0; i < no_of_rows; i++) {         for (j = 0; j < no_of_col; j++) {             if (i == row - 1 && j == col - 1) {                 if (ele.cells[col - 1].hasAttribute('title')) {                           tp = ele.cells[col - 1].title;                     }                     else if (ele.cells[col - 1].children.length > 0) {                         for (k = 0; k < ele.cells[col - 1].children.length; k++) {                             finalele = recurseDomChildren(ele.cells[col - 1].children[k]);                             if (finalele != undefined && finalele != '') {                                                            if (finalele.hasAttribute('title') && finalele != undefined) {                                             tp = finalele.title;                                         break;                                     }                                 }                             }                         } else {                             if (ele.hasAttribute('title') && ele != undefined) {                                          tp = ele.title;                                 }                             }                         }                     }                 }                 return tp;             };              function recurseDomChildren(start) {                 var nodes, ele1;                 if (start.hasAttribute('title') && start != undefined) {                           ele1 = start;                         return ele1;                     }                     else if (start.childNodes.length > 0) {                         nodes = start.childNodes;                         ele1 = loopNodeChildren(nodes);                         if (ele1 != '') {                                      return ele1;                         }                     }                 }                  function loopNodeChildren(nodes) {                     var node, ele2;                     for (var i = 0; i < nodes.length; i++) {                         node = nodes[i];                         if (node.childNodes.length > 0) {                             ele2 = recurseDomChildren(node);                             if (ele2 != ''  && ele2 != undefined) {                                      if (ele2.hasAttribute('title')){                                                     break;                                     }                                 }                             }                             else if (node.nodeType === 1) {                                 if (node.hasAttribute('title') && node != undefined) {                                              ele2 = node;                                         break;                                     }                                 }                                 else {                                     ele2 = '';                                       }                             }                             return ele2;                         }; ",webelement,row,col)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyCellToolTip(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        row=input[0]
        col=input[1]
        input=input[2]
        tooltip=local_wk.driver.execute_script("var temp = tooltip(arguments[0], arguments[1], arguments[2]); return temp; function tooltip(table, row, col) {     var no_of_rows = table.rows.length;     var no_of_col = table.rows[row - 1].cells.length;     var ele = table.rows[row - 1];     var i, j, k, tp;     for (i = 0; i < no_of_rows; i++) {         for (j = 0; j < no_of_col; j++) {             if (i == row - 1 && j == col - 1) {                 if (ele.cells[col - 1].hasAttribute('title')) {                           tp = ele.cells[col - 1].title;                     }                     else if (ele.cells[col - 1].children.length > 0) {                         for (k = 0; k < ele.cells[col - 1].children.length; k++) {                             finalele = recurseDomChildren(ele.cells[col - 1].children[k]);                             if (finalele != undefined && finalele != '') {                                                            if (finalele.hasAttribute('title') && finalele != undefined) {                                             tp = finalele.title;                                         break;                                     }                                 }                             }                         } else {                             if (ele.hasAttribute('title') && ele != undefined) {                                          tp = ele.title;                                 }                             }                         }                     }                 }                 return tp;             };              function recurseDomChildren(start) {                 var nodes, ele1;                 if (start.hasAttribute('title') && start != undefined) {                           ele1 = start;                         return ele1;                     }                     else if (start.childNodes.length > 0) {                         nodes = start.childNodes;                         ele1 = loopNodeChildren(nodes);                         if (ele1 != '') {                                      return ele1;                         }                     }                 }                  function loopNodeChildren(nodes) {                     var node, ele2;                     for (var i = 0; i < nodes.length; i++) {                         node = nodes[i];                         if (node.childNodes.length > 0) {                             ele2 = recurseDomChildren(node);                             if (ele2 != ''  && ele2 != undefined) {                                      if (ele2.hasAttribute('title')){                                                     break;                                     }                                 }                             }                             else if (node.nodeType === 1) {                                 if (node.hasAttribute('title') && node != undefined) {                                              ele2 = node;                                         break;                                     }                                 }                                 else {                                     ele2 = '';                                       }                             }                             return ele2;                         }; ",webelement,row,col)
        output_val='True' if tooltip == input else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getInnerTable(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        row=input[0]
        col=input[1]
        output_val=local_wk.driver.execute_script("var temp = fun(arguments[0], arguments[1], arguments[2]); return temp;  function fun(table, x, y) {     row = table.rows[x];     cell = row.cells[y];     tableCheck = cell.getElementsByTagName('table'); if(tableCheck.length > 0){        console.log(tableCheck[0]);       return tableCheck[0];    }else{      return null; } }",webelement,row,col)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def cellClick(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        row=input[0]
        col=input[1]
        if len(input)==2:
            remoteele=local_wk.driver.execute_script('var temp = fun(arguments[0], arguments[2], arguments[1]); return temp;  function fun(table, x, y) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (xx <= x && x < xx + cell.colSpan && yyy <= y && y < yyy + cell.rowSpan) return cell;         }     }     return null; };',webelement,int(row)-1,int(col)-1)
            if len(remoteele.find_elements_by_xpath('.//*')) > 0:
                remoteele.find_elements_by_xpath('.//*')[0].click()
            else:
                remoteele.click()
        elif len(input)>2:
            input=input[3]
            remoteele=local_wk.driver.execute_script('var temp = fun(arguments[0], arguments[2], arguments[1]); return temp;  function fun(table, x, y) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (xx <= x && x < xx + cell.colSpan && yyy <= y && y < yyy + cell.rowSpan) return cell;         }     }     return null; };',webelement,int(row)-1,int(col)-1)
            if input[2].lower=='button':
                obj="//input[@type='button' or @type='button' or @type='submit' or @type='reset' or @type='file']"
            elif input[2].lower=='img':
                obj="//img"
            elif input[2].lower=='image':
                obj="//input[@type='image' or @type='img']"
            elif input[2].lower=='checkbox':
                obj="//input[@type='checkbox']"
            elif input[2].lower=='radiobutton':
                obj="//input[@type='radio']"
            elif input[2].lower=='link':
                obj="//a"
            elif input[2].lower=='textbox':
                obj="//input[@type='text' or @type='email' or @type='password' or @type='range' or @type='search' or @type='url']"
            else:
                obj=input[2].lower()
            remoteele.find_elements_by_xpath('obj')[int(input)].click()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

class Textbox_Keywords():

    def __init__(self):
        self.key = b'\x74\x68\x69\x73\x49\x73\x41\x53\x65\x63\x72\x65\x74\x4b\x65\x79'
        pass

    def clearText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        webelement.clear()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def setText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        local_wk.driver.execute_script('arguments[0].value=arguments[1]',webelement,input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def sendValue(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        webelement.send_keys(input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val=local_wk.driver.execute_script('return arguments[0].value',webelement)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        text_val=local_wk.driver.execute_script('return arguments[0].value',webelement)
        output_val='True' if text_val == input else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def getTextboxLength(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val=webelement.get_attribute('maxlength')
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyTextboxLength(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        text_len=webelement.get_attribute('maxlength')
        output_val='True' if text_len == input else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def setSecureText(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        # input=self.decrypt(input_val[0])
        local_wk.driver.execute_script('arguments[0].value=arguments[1]',webelement,self.decrypt(input))
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def sendSecureValue(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input[0]
        # input=self.decrypt(input_val[0])
        webelement.send_keys(self.decrypt(input))
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    
    def decrypt(self,enc):
        import base64
        from Crypto.Cipher import AES
        unpad = lambda s : s[0:-ord(s[-1])]
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc).decode('utf-8'))

class Util_Keywords():

    def __init__(self):
        self.action=None
        self.keys_info={}
        pass

    def _createKeysInfoDict(self):
        self.keys_info['null']=Keys.NULL
        self.keys_info['cancel']=Keys.CANCEL
        self.keys_info['help']=Keys.HELP
        self.keys_info['backspace']=Keys.BACKSPACE
        self.keys_info['tab']=Keys.TAB
        self.keys_info['clear']=Keys.CLEAR
        self.keys_info['return']=Keys.RETURN
        self.keys_info['enter']=Keys.ENTER
        self.keys_info['control']=Keys.CONTROL
        self.keys_info['ctrl']=Keys.CONTROL
        self.keys_info['alt']=Keys.ALT
        self.keys_info['pause']=Keys.PAUSE
        self.keys_info['escape']=Keys.ESCAPE
        self.keys_info['space']=Keys.SPACE
        self.keys_info['pageup']=Keys.PAGE_UP
        self.keys_info['pagedown']=Keys.PAGE_DOWN
        self.keys_info['end']=Keys.END
        self.keys_info['home']=Keys.HOME
        self.keys_info['leftarrow']=Keys.LEFT
        self.keys_info['rightarrow']=Keys.RIGHT
        self.keys_info['uparrow']=Keys.UP
        self.keys_info['downarrow']=Keys.DOWN
        self.keys_info['insert']=Keys.INSERT
        self.keys_info['delete']=Keys.DELETE
        self.keys_info['semicolon']=Keys.SEMICOLON
        self.keys_info['equals']=Keys.EQUALS
        self.keys_info['numpad0']=Keys.NUMPAD0
        self.keys_info['numpad1']=Keys.NUMPAD1
        self.keys_info['numpad2']=Keys.NUMPAD2
        self.keys_info['numpad3']=Keys.NUMPAD3
        self.keys_info['numpad4']=Keys.NUMPAD4
        self.keys_info['numpad5']=Keys.NUMPAD5
        self.keys_info['numpad6']=Keys.NUMPAD6
        self.keys_info['numpad7']=Keys.NUMPAD7
        self.keys_info['numpad8']=Keys.NUMPAD8
        self.keys_info['numpad9']=Keys.NUMPAD9
        self.keys_info['f1']=Keys.F1
        self.keys_info['f2']=Keys.F2
        self.keys_info['f3']=Keys.F3
        self.keys_info['f4']=Keys.F4
        self.keys_info['f5']=Keys.F5
        self.keys_info['f6']=Keys.F6
        self.keys_info['f7']=Keys.F7
        self.keys_info['f8']=Keys.F8
        self.keys_info['f9']=Keys.F9
        self.keys_info['f10']=Keys.F10
        self.keys_info['f11']=Keys.F11
        self.keys_info['f12']=Keys.F12
        self.keys_info['multiply']=Keys.MULTIPLY
        self.keys_info['add']=Keys.ADD
        self.keys_info['subtract']=Keys.SUBTRACT
        self.keys_info['divide']=Keys.DIVIDE
        self.keys_info['separator']=Keys.SEPARATOR
        self.keys_info['decimal']=Keys.DECIMAL
        pass

    def tab(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        webelement.send_keys(Keys.TAB)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def sendFunctionKeys(self,webelement,input,*args):
        self._createKeysInfoDict()
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input1=input[0]
        if input1.lower() in self.keys_info:
            digits = [int(i)for i in input if i.isdigit()]
            try:
                webelement.send_keys(self.keys_info[input1.lower()]*digits[0])
            except Exception as e:
                webelement.send_keys(self.keys_info[input1.lower()])
        else:
            webelement.send_keys(input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyVisible(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        visibility=local_wk.driver.execute_script("var isVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })(); var s = arguments[0]; return isVisible(s);",webelement)
        output_val='True' if visibility else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyHidden(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        hidden=local_wk.driver.execute_script("var isVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })(); var s = arguments[0]; return isVisible(s);",webelement)
        output_val='True' if not(hidden) else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyEnabled(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        enabled = webelement.is_enabled()
        output_val='True' if enabled else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyDisabled(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        disabled = webelement.is_enabled()
        output_val='True' if not(disabled) else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyExists(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val='True' if webelement != None or webelement != '' else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyDoesNotExists(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        output_val='True' if webelement == None or webelement == '' else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def verifyReadOnly(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        readonly_value = webelement.get_attribute('readonly')
        output_val='True' if readonly_value is not None and readonly_value.lower() =='true' or readonly_value is '' else 'False'
        status=TEST_RESULT_PASS if output_val == 'True' else 'Fail'
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def drag(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        self.action=webdriver.ActionChains(local_wk.driver).click_and_hold(webelement).move_to_element(webelement)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def drop(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        self.action.release(webelement).perform()
        self.action=''
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def waitForElementVisible(self,webelement,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        input=input
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.common.by import By
        element_present = EC.presence_of_element_located((By.XPATH, input))
        WebDriverWait(local_wk.driver, 10).until(element_present)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

class Sauce_Config():

    def get_sauceconf(self):
        Saucelabs_config_path=os.environ['AVO_ASSURE_HOME']+os.sep+'assets'+os.sep+'sauce_config.json'
        import json
        conf_obj = open(Saucelabs_config_path, 'r')
        conf = json.load(conf_obj)
        conf_obj.close()
        # self.proxies=self.conf["proxy"]
        self.username = conf["sauce_username"]
        self.access_key = conf["sauce_access_key"]
        self.platform = conf["platform"]
        self.url = conf["remote_url"]
        return conf

    def get_sauceclient(self):
        return sauceclient.SauceClient(self.username,self.access_key)

    def get_saucejobs(self, sc):
        return sauceclient.Jobs(sc)