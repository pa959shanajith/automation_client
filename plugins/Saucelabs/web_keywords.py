import os
filename=""
import logging
log=logging.getLogger('web_keywords.py')
class Browser_Keywords:

    def __init__(self,f):
        self.f=f
    
    def openBrowser(self,space,url,browser,*args):
        self.f.write(space+"driver = webdriver.Remote(command_executor='"+url+"', desired_capabilities="+str(browser)+")")
        self.f.write(space+"status='Pass'")

    def navigateToURL(self,space,input,*args):
        if "'" in input[0]:
            input[0]=input[0][1:-1]
        url=input[0]
        if url[0:7].lower()!='http://' and url[0:8].lower()!='https://' and url[0:5].lower()!='file:':
            url='http://'+url
        self.f.write(space+"input='"+url+"'")
        self.f.write(space+"driver.get(input)")
        self.f.write(space+"status='Pass'")

    def maximizeBrowser(self,space,*args):
        self.f.write(space+"driver.maximize_window()")   
        self.f.write(space+"status='Pass'") 
    
    def verifyPageTitle(self,space,input,*args):
        inp_title=input[0]
        self.f.write(space+"input="+inp_title)
        self.f.write(space+"title=driver.title")
        self.f.write(space+"output= 'True' if title==input else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def getPageTitle(self,space,*args):
        self.f.write(space+"output=driver.title")
        self.f.write(space+"status='Pass'")

    def getCurrentURL(self,space,*args):
        self.f.write(space+"output=driver.current_url")
        self.f.write(space+"status='Pass'")
    
    def verifyCurrentURL(self,space,input,*args):
        inp_url=input[0]
        self.f.write(space+"input="+inp_url)
        self.f.write(space+"url=driver.current_url")
        self.f.write(space+"output = 'True' if url==input else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")
    
    def openNewTab(self,space,*args):
        self.f.write(space+"driver.execute_script('window.open('');')")
        self.f.write(space+"driver.switch_to.window(driver.window_handles[int(driver.window_handles.index(driver.current_window_handle))+1])")
        self.f.write(space+"status='Pass'")

    def refresh(self,space,*args):
        self.f.write(space+"driver.refresh()")
        self.f.write(space+"status='Pass'")

    def navigateBack(self,space,*args):
        self.f.write(space+"driver.execute_script('window.history.go(-1)')")
        self.f.write(space+"status='Pass'")
    
    def closeSubWindows(self,space,input,*args):
        # if(input[0].lower()=='all'):
        # else:
        self.f.write(space+"driver.close()")
        self.f.write(space+"driver.switch_to.window(driver.window_handles[-1])")
        self.f.write(space+"status='Pass'")
    
    def switchToWindow(self,space,input,*args):
        inp=int(input[0][1:-1])
        self.f.write(space+"driver.switch_to.window(driver.window_handles["+str(int(inp)-1)+"])")
        self.f.write(space+"status='Pass'")
    
    def navigateWithAuthenticate(self,space,input,*args):
        input_val=input
        self.f.write(space+"url="+input_val[0])
        self.f.write(space+"user="+input_val[1])
        self.f.write(space+"password=decrypt("+input_val[2]+")")
        self.f.write(space+"if url[0:7].lower() == 'http://': url=url[0:7]+user+':'+password+'@'+url[7:]")
        self.f.write(space+"elif url[0:8].lower() == 'https://': url=url[0:8]+user+':'+password+'@'+url[8:]")
        # self.f.write(space+"url="+url)
        self.f.write(space+"input=[url,user,password]")
        self.f.write(space+"driver.get(url)")
        self.f.write(space+"status='Pass'")

    def execute_js(self,space,input,*args):
        self.f.write(space+"driver.execute_script(inputval)")
        self.f.write(space+"status='Pass'")

    def clearCache(self,space,*args):
        self.f.write(space+"driver.get('chrome://settings/clearBrowserData')")
        self.f.write(space+"time.sleep(5)")
        self.f.write(space+"""driver.execute_script('return document.querySelector("body > settings-ui").shadowRoot.querySelector("#container").querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("settings-privacy-page").shadowRoot.querySelector("settings-clear-browsing-data-dialog").shadowRoot.querySelector("#clearBrowsingDataDialog").querySelector("#clearBrowsingDataConfirm").click();')""")
        self.f.write(space+"status='Pass'")

    def verifyTextExists(self,space,input,*args):
        self.f.write(space+"input="+input[0])
        occurrences_javascript = "function occurrences(string, subString, allowOverlapping) {      string += '';     subString += '';     if (subString.length <= 0) return (string.length + 1);      var n = 0,pos = 0,step = allowOverlapping ? 1 : subString.length;      while (true) {         pos = string.indexOf(subString, pos);         if (pos >= 0) {             ++n;             pos += step;         } else break;     }     return n; }; function saddNodesOuter(sarray, scollection) { 	for (var i = 0; scollection && scollection.length && i < scollection.length; i++) { 		sarray.push(scollection[i]); 	} }; function stext_content(f) { 	var sfirstText = ''; 	var stextdisplay = ''; 	for (var z = 0; z < f.childNodes.length; z++) { 		var scurNode = f.childNodes[z]; 		swhitespace = /^\\s*$/; 		if (scurNode.nodeName === '#text' && !(swhitespace.test(scurNode.nodeValue))) { 			sfirstText = scurNode.nodeValue; 			stextdisplay = stextdisplay + sfirstText; 		} 	} 	return (stextdisplay); }; var sae = []; var substr = arguments[0]; var sele = arguments.length > 1 ? arguments[1].getElementsByTagName('*') :  document.getElementsByTagName('*'); var text_occurrences = 0; saddNodesOuter(sae, sele);  for(var j=0;j<sae.length;j++){ 	stagname = sae[j].tagName.toLowerCase(); 	 	if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') { 		text_occurrences += occurrences(stext_content(sae[j]),substr); 	} 	 }; return text_occurrences;bstr = arguments[0]; var sele = arguments.length > 1 ? arguments[1].getElementsByTagName('*') :  document.getElementsByTagName('*'); var text_occurrences = 0; saddNodesOuter(sae, sele);  for(var j=0;j<sae.length;j++){ 	stagname = sae[j].tagName.toLowerCase(); 	 	if (stagname != 'script' && stagname != 'meta' && stagname != 'html' && stagname != 'head' && stagname != 'style' && stagname != 'body' && stagname != 'form' && stagname != 'link' && stagname != 'noscript' && stagname != 'option' && stagname != '!' && stagname != 'code' && stagname != 'pre' && stagname != 'br' && stagname != 'animatetransform' && stagname != 'noembed') { 		text_occurrences += occurrences(stext_content(sae[j]),substr); 	} 	 }; return text_occurrences;"
        self.f.write(space+"output=int(driver.execute_script(\""+occurrences_javascript+"\",input))")
        self.f.write(space+"status='Pass' if output != 0 else 'Fail'")

    def closeBrowser(self,space,*args):
        self.f.write(space+"driver.quit()")
        self.f.write(space+"status='Pass'")

class Browser_Popup_Keywords():

    def __init__(self,f):
        self.f=f

    def acceptPopUp(self,space,input,*args):
        self.f.write(space+"driver.switch_to.alert.accept()")
        self.f.write(space+"status='Pass'") 
    
    def dismissPopUp(self,space,input,*args):
        self.f.write(space+"driver.switch_to.alert.dismiss()")
        self.f.write(space+"status='Pass'") 

    def getPopUpText(self,space,input,*args):
        self.f.write(space+"output=driver.switch_to.alert.text")
        self.f.write(space+"status='Pass'") 
    
    def verifyPopUpText(self,space,input,*args):
        text=input[0]
        self.f.write(space+"input="+text)
        self.f.write(space+"popup_text = driver.switch_to.alert.accept()")
        self.f.write(space+"outpuiut='True' if popup_text==input else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

class Button_link_Keywords():

    def __init__(self,f):
        self.f=f

    def getButtonName(self,space,webelement,input,*args):
        self.f.write(space+"buttontext="+webelement+".text")
        self.f.write(space+"buttontext="+webelement+".get_attribute('value') if buttontext == None or buttontext == '' else buttontext")
        self.f.write(space+"output=buttontext")
        self.f.write(space+"status='Pass'") 

    def verifyButtonName(self,space,webelement,input,*args):
        verify_button=input[0]
        self.f.write(space+"input="+verify_button)
        self.f.write(space+"buttontext="+webelement+".text")
        self.f.write(space+"buttontext="+webelement+".get_attribute('value') if buttontext == None or buttontext == '' else buttontext")
        self.f.write(space+"output='True' if buttontext == input else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def getLinkText(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"linktext="+webelement+".get_attribute('href')")
        self.f.write(space+"linktext="+webelement+".text if linktext == None or linktext == '' else linktext")
        self.f.write(space+"output=linktext")
        self.f.write(space+"status='Pass'") 

    def verifyLinkText(self,space,webelement,input,*args):
        verify_link=input[0]
        self.f.write(space+"input="+verify_link)
        self.f.write(space+"linktext="+webelement+".get_attribute('href')")
        self.f.write(space+"linktext="+webelement+".text if linktext == None or linktext == '' else linktext")
        self.f.write(space+"output='True' if linktext == input else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")
            
class Dropdown_Keywords():

    def __init__(self,f):
        self.f=f

    def selectAllValues(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"select = Select("+webelement+")")
        self.f.write(space+"for i in range(0.len(select.options)):")
        self.f.write(space+"\tNone if select.options[i].is_selected() else select.select_by_visible_text(input)")
        self.f.write(space+"status='Pass'")
        
    def selectValueByIndex(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"driver.execute_script('arguments[0].selectedIndex=arguments[1]',"+webelement+",input)")
        self.f.write(space+"status='Pass'")

    def selectMultipleValuesByIndexes(self,space,webelement,input,*args):
        input=input[0].split(',')
        for i in input:
            self.f.write(space+"input="+i)
            self.f.write(space+"driver.execute_script('arguments[0].selectedIndex=arguments[1]',"+webelement+",input)")
        self.f.write(space+"status='Pass'")

    def selectByAbsoluteValue(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"select = Select("+webelement+")")
        self.f.write(space+"select.select_by_value(input)")
        self.f.write(space+"status='Pass'")

    def selectValueByText(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"select = Select("+webelement+")")
        self.f.write(space+"select.select_by_visible_text(input)")
        self.f.write(space+"status='Pass'")

    def selectMultipleValuesByText(self,space,webelement,input,*args):
        self.f.write(space+"select = Select("+webelement+")")
        input=input[0].split(',')
        for i in input:
            self.f.write(space+"input="+i)
            self.f.write(space+"select.select_by_visible_text(input)")
        self.f.write(space+"status='Pass'")

    def getCount(self,space,webelement,input,*args):
        self.f.write(space+"select = Select("+webelement+")")
        self.f.write(space+"iList = select.options")
        self.f.write(space+"iListSize = len(iList)")
        self.f.write(space+"output=iListSize")
        self.f.write(space+"status='Pass'")
    
    def verifyCount(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"select = Select("+webelement+")")
        self.f.write(space+"iList = select.options")
        self.f.write(space+"iListSize = len(iList)")
        self.f.write(space+"output='True' if iListSize == input else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def verifySelectedValue(self,space,webelement,input,*args):
        input_val=input[0].split(",")
        self.f.write(space+"input="+input_val[0])
        self.f.write(space+"select = Select("+webelement+")")
        self.f.write(space+"first_value = select.first_selected_option.text")
        self.f.write(space+"output='True' if first_value == input else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def verifySelectedValues(self,space,webelement,input,*args):
        input_val=input[0].split(",")
        self.f.write(space+"input="+input_val)
        self.f.write(space+"select = Select("+webelement+")")
        self.f.write(space+"all_value = select.all_selected_options")
        self.f.write(space+"temp="+input_val)
        self.f.write(space+"import copy\ntemp1=copy.deepcopy(temp)")
        self.f.write(space+"for i in range(0,len(temp)):\n\tif temp[i] in all_value:\n\t\ttemp1.remove(temp[i])")
        self.f.write(space+"output='True' if len(temp1)==0 else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def getAllValues(self,space,webelement,input,*args):
        self.f.write(space+"select = Select("+webelement+")")
        self.f.write(space+"opt_len = len(select.options)")
        self.f.write(space+"temp=[]")
        self.f.write(space+"for x in range(0,opt_len): temp.append(select.options[x].text)")
        self.f.write(space+"output=temp")
        self.f.write(space+"status='Pass'")
    
    def getSelected(self,space,webelement,input,*args):
        self.f.write(space+"select = Select("+webelement+")")
        self.f.write(space+"opt_len = len(select.options)")
        self.f.write(space+"temp=[]")
        self.f.write(space+"for x in range(0,opt_len): temp.append(select.all_selected_options[x].text)")
        self.f.write(space+"output=temp")
        self.f.write(space+"status='Pass'")
    
    def verifyAllValues(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"select = Select("+webelement+")")
        self.f.write(space+"opt_len = len(select.options)")
        self.f.write(space+"temp=[]")
        self.f.write(space+"flag==True")
        self.f.write(space+"for x in range(0,opt_len): temp.append(select.options[x].text)")
        self.f.write(space+"for i in input:\n\tif i not in temp:\n\t\tflag=False\n\t\tbreak")
        self.f.write(space+"output='True' if flag else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def getValueByIndex(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"select = Select("+webelement+")")
        self.f.write(space+"output=select.options[input].text")
        self.f.write(space+"status='Pass'")

    def deselectAll(self,space,webelement,input,*args):
        self.f.write(space+"select = Select("+webelement+")")
        self.f.write(space+"select.deselect_all()")
        self.f.write(space+"status='Pass'")

class Element_Keywords:

    def __init__(self,f):
        self.f=f

    def click(self,space,webelement,input,*args):
        self.f.write(space+"driver.execute_script(\"var evType; element=arguments[0]; if (document.createEvent) {     evType = 'Click executed through part-1';     var evt = document.createEvent('MouseEvents');     evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = 'Click executed through part-2';   	setTimeout(function() {     element.click();   	}, 100); } return (evType);\","+webelement+")")
        self.f.write(space+"status='Pass'")

    def press(self,space,webelement,input,*args):
        self.f.write(space+""+webelement+".click()")
        self.f.write(space+"status='Pass'")
    
    def doubleClick(self,space,webelement,input,*args):
        self.f.write(space+"webdriver.ActionChains(driver).move_to_element("+webelement+").double_click("+webelement+").perform()")
        self.f.write(space+"status='Pass'")

    def rightClick(self,space,webelement,input,*args):
        self.f.write(space+"webdriver.ActionChains(driver).move_to_element("+webelement+").context_click("+webelement+").perform()")
        self.f.write(space+"status='Pass'")

    def getAttributeValue(self,space,webelement,input,*args):
        attr_name=input[0]
        self.f.write(space+"input="+attr_name)
        self.f.write(space+"output="+webelement+".get_attribute(input)")
        self.f.write(space+"status='Pass'")

    def verifyAttribute(self,space,webelement,input,*args):
        input_val=input
        self.f.write(space+"input="+input_val[0])
        self.f.write(space+"input1="+input_val[1])
        self.f.write(space+"attr_val="+webelement+".get_attribute(input)")
        self.f.write(space+"output='True' if attr_val == input1 else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def mouseHover(self,space,webelement,input,*args):
        self.f.write(space+"webdriver.ActionChains(driver).move_to_element("+webelement+").perform()")
        self.f.write(space+"status='Pass'")

    def setFocus(self,space,webelement,input,*args):
        self.f.write(space+"driver.execute_script('arguments[0].focus();',"+webelement+")")
        self.f.write(space+"status='Pass'")

    def getElementTagValue(self,space,webelement,input,*args):
        self.f.write(space+"output="+webelement+".tag_name")
        self.f.write(space+"status='Pass'")
    
    def uploadFile(self,space,webelement,input,*args):
        input=input[0].replace("\\","/")
        self.f.write(space+"input="+input)
        self.f.write(space+""+webelement+".sendKeys(input)")
        self.f.write(space+"status='Pass'")

    def dropFile(self,space,webelement,input,*args):
        input=input[0].replace("\\","/")
        self.f.write(space+"input="+input)
        self.f.write(space+""+webelement+".sendKeys(input)")
        self.f.write(space+"status='Pass'")

    def getElementText(self,space,webelement,input,*args):
        self.f.write(space+"text="+webelement+".get_attribute('value')")
        self.f.write(space+"if(text is None or text is ''): text="+webelement+".get_attribute('name')")
        self.f.write(space+"if(text is None or text is ''): text="+webelement+".get_attribute('title')")
        self.f.write(space+"if(text is None or text is ''): text="+webelement+".get_attribute('placeholder')")
        self.f.write(space+"output=text")
        self.f.write(space+"status='Pass'")
    
    def verifyElementText(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"text="+webelement+".get_attribute('value')")
        self.f.write(space+"if(text is None or text is ''): text="+webelement+".get_attribute('name')")
        self.f.write(space+"if(text is None or text is ''): text="+webelement+".get_attribute('title')")
        self.f.write(space+"if(text is None or text is ''): text="+webelement+".get_attribute('placeholder')")
        self.f.write(space+"output='True' if text == input else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def getToolTipText(self,space,webelement,input,*args):
        self.f.write(space+"output="+webelement+".get_attribute('title')")
        self.f.write(space+"status='Pass'")

    def verifyToolTipText(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"tooltip="+webelement+".get_attribute('title')")
        self.f.write(space+"output='True' if tooltip == input[0] else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

class Radio_checkbox_Keywords():

    def __init__(self,f):
        self.f=f

    def selectRadioButton(self,space,webelement,input,*args):
        self.f.write(space+""+webelement+".click()")
        self.f.write(space+"status='Pass'")

    def getStatus(self,space,webelement,input,*args):
        self.f.write(space+"output='selected' if "+webelement+".is_selected() else 'unselected'")
        self.f.write(space+"status='Pass'")

    def selectCheckbox(self,space,webelement,input,*args):
        self.f.write(space+""+webelement+".click()")
        self.f.write(space+"status='Pass'")

    def unselectCheckbox(self,space,webelement,input,*args):
        self.f.write(space+""+webelement+".click()")
        self.f.write(space+"status='Pass'")

class Table_Keywords():

    def __init__(self,f):
        self.f=f

    def getRowCount(self,space,webelement,input,*args):
        self.f.write(space+"output=driver.execute_script('var targetTable = arguments[0]; var rowCount = targetTable.rows; return rowCount.length;',"+webelement+")")
        self.f.write(space+"status='Pass'")

    def getColoumnCount(self,space,webelement,input,*args):
        self.f.write(space+"output=driver.execute_script('var targetTable = arguments[0]; var columnCount = 0; var rows = targetTable.rows; if(rows.length > 0) { 	for (var i = 0; i < rows.length; i++) { 		var cells = rows[i].cells; 		var tempColumnCount = 0; 		for (var j = 0; j < cells.length; j++) { 			tempColumnCount += cells[j].colSpan; 		} 		if (tempColumnCount > columnCount) { 			columnCount = tempColumnCount; 		} 	} } return columnCount;',"+webelement+")")
        self.f.write(space+"status='Pass'")

    def getRowNumByText(self,space,webelement,input,*args):
        self.f.write(space+"output=driver.execute_script('var temp = fun(arguments[0], arguments[1]); return temp; function fun(table, str) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy, child;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (cell.innerText.indexOf(str)>= 0) return yyy + cell.rowSpan;             else if (cell.children.length > 0) {                 for (var i = 0; i < cell.children.length; i++) {                     child = cell.children[i];                     if (child.value == str) return yyy + cell.rowSpan; 					else{ 					var a=child.value; 					if(a){ 					var b=a; 					if(b.indexOf(str)>=0)return yyy + cell.rowSpan; 					}	 				}			 					                 }             }         }     }     return null; };',"+webelement+")")
        self.f.write(space+"status='Pass'")

    def getColNumByText(self,space,webelement,input,*args):
        self.f.write(space+"output=driver.execute_script('var temp = fun(arguments[0], arguments[1]); return temp; function fun(table, str) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy, child;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (cell.innerText.indexOf(str)>= 0) return xx + cell.colSpan;             else if (cell.children.length > 0) {                 for (var i = 0; i < cell.children.length; i++) {                     child = cell.children[i];                     if (child.value == str) return xx + cell.colSpan; 					else{ 					var a=child.value; 					if(a){ 					var b=a; 					if(b.indexOf(str)>=0)return xx + cell.colSpan; 					}	 				}			 					                 }             }         }     }     return null; };',"+webelement+")")
        self.f.write(space+"status='Pass'")
    
    def getCellValue(self,space,webelement,input,*args):
        self.f.write(space+"row="+input[0])
        self.f.write(space+"col="+input[1])
        self.f.write(space+"remoteele=driver.execute_script('var temp = fun(arguments[0], arguments[2], arguments[1]); return temp;  function fun(table, x, y) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (xx <= x && x < xx + cell.colSpan && yyy <= y && y < yyy + cell.rowSpan) return cell;         }     }     return null; };',"+webelement+",row,col)")
        self.f.write(space+"output=driver.execute_script(\"var mytarget = arguments[0]; var mynodes = mytarget.childNodes; var result = []; if (typeof  String.prototype.trim  !== 'function')  {       String.prototype.trim  =   function()  {             return  this.replace(/^\\s+|\\s+$/g,'');        } } recursfunc(mynodes); return result.toString();  function recursfunc(mynodes) {     for (var i = 0; i < mynodes.length; i++) {         if (mynodes[i].nodeName.toUpperCase() == \'#TEXT\') {             if ((mynodes[i].parentNode.nodeName.toUpperCase() != \'OPTION\') & (mynodes[i].parentNode.nodeName.toUpperCase() != \'SCRIPT\')) {                 var myvalue = mynodes[i].nodeValue;                 if (myvalue.trim().length > 0) {                     result.push(myvalue);                 }             }         } else if (mynodes[i].nodeName.toUpperCase() == \'INPUT\') {             if (mynodes[i].type.toUpperCase() == \'RADIO\') {                 if (mynodes[i].checked == true) {                     var myvalue = \'Selected\';                 } else {                     var myvalue = \'Unselected\';                 }             } else if (mynodes[i].type.toUpperCase() == \'CHECKBOX\') {                 if (mynodes[i].checked == true) {                     var myvalue = \'Checked\';                 } else {                     var myvalue = \'Unchecked\';                 }             } else if ((mynodes[i].type.toUpperCase() == \'BUTTON\') | (mynodes[i].type.toUpperCase() == \'SUBMIT\') | (mynodes[i].type.toUpperCase() == \'TEXT\')) {                 var myvalue = mynodes[i].value;             } else if (mynodes[i].type.toUpperCase() == \'IMAGE\') {                 var myvalue = mynodes[i].title;                 if (myvalue.trim().length < 1) {                     myvalue = mynodes[i].value;                     if (myvalue != undefined) {                         if (myvalue.trim().length < 1) {                             myvalue = \'Image\';                         }                     } else {                         myvalue = \'Image\';                     }                 }             }else{ var myvalue=mynodes[i].value; }             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \'IMG\') {             var myvalue = mynodes[i].title;             if (myvalue.trim().length < 1) {                 myvalue = mynodes[i].value;                 if (myvalue != undefined) {                     if (myvalue.trim().length < 1) {                         myvalue = \'Image\';                     }                 } else {                     myvalue = \'Image\';                 }             }             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \'TEXTAREA\') {             var myvalue = mynodes[i].value;             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \'SELECT\') {             var myselect = mynodes[i].selectedOptions;             if (myselect != undefined | myselect != null) {                 for (var j = 0; j < myselect.length; j++) {                     var myvalue = mynodes[i].selectedOptions[j].textContent;                     result.push(myvalue);                 }             } else {                 var myvalue = dropdowncallie(mynodes[i]);                 result.push(myvalue);             }         } else if ((mynodes[i].nodeName.toUpperCase() == \'I\')) {             var myvalue = mynodes[i].textContent;             result.push(myvalue);         }         if (mynodes[i].hasChildNodes()) {             recursfunc(mynodes[i].childNodes);         }     } }  function dropdowncallie(op) {     var x = op.options[op.selectedIndex].text;     return x; };\","+webelement+")")
        self.f.write(space+"status='Pass'")

    def verifyCellValue(self,space,webelement,input,*args):
        self.f.write(space+"row="+input[0])
        self.f.write(space+"col="+input[1])
        self.f.write(space+"input="+input[2])
        self.f.write(space+"remoteele=driver.execute_script('var temp = fun(arguments[0], arguments[2], arguments[1]); return temp;  function fun(table, x, y) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (xx <= x && x < xx + cell.colSpan && yyy <= y && y < yyy + cell.rowSpan) return cell;         }     }     return null; };',"+webelement+",row,col)")
        self.f.write(space+"content=driver.execute_script(\"var mytarget = arguments[0]; var mynodes = mytarget.childNodes; var result = []; if (typeof  String.prototype.trim  !== 'function')  {       String.prototype.trim  =   function()  {             return  this.replace(/^\\s+|\\s+$/g,'');        } } recursfunc(mynodes); return result.toString();  function recursfunc(mynodes) {     for (var i = 0; i < mynodes.length; i++) {         if (mynodes[i].nodeName.toUpperCase() == \'#TEXT\') {             if ((mynodes[i].parentNode.nodeName.toUpperCase() != \'OPTION\') & (mynodes[i].parentNode.nodeName.toUpperCase() != \'SCRIPT\')) {                 var myvalue = mynodes[i].nodeValue;                 if (myvalue.trim().length > 0) {                     result.push(myvalue);                 }             }         } else if (mynodes[i].nodeName.toUpperCase() == \'INPUT\') {             if (mynodes[i].type.toUpperCase() == \'RADIO\') {                 if (mynodes[i].checked == true) {                     var myvalue = \'Selected\';                 } else {                     var myvalue = \'Unselected\';                 }             } else if (mynodes[i].type.toUpperCase() == \'CHECKBOX\') {                 if (mynodes[i].checked == true) {                     var myvalue = \'Checked\';                 } else {                     var myvalue = \'Unchecked\';                 }             } else if ((mynodes[i].type.toUpperCase() == \'BUTTON\') | (mynodes[i].type.toUpperCase() == \'SUBMIT\') | (mynodes[i].type.toUpperCase() == \'TEXT\')) {                 var myvalue = mynodes[i].value;             } else if (mynodes[i].type.toUpperCase() == \'IMAGE\') {                 var myvalue = mynodes[i].title;                 if (myvalue.trim().length < 1) {                     myvalue = mynodes[i].value;                     if (myvalue != undefined) {                         if (myvalue.trim().length < 1) {                             myvalue = \'Image\';                         }                     } else {                         myvalue = \'Image\';                     }                 }             }else{ var myvalue=mynodes[i].value; }             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \'IMG\') {             var myvalue = mynodes[i].title;             if (myvalue.trim().length < 1) {                 myvalue = mynodes[i].value;                 if (myvalue != undefined) {                     if (myvalue.trim().length < 1) {                         myvalue = \'Image\';                     }                 } else {                     myvalue = \'Image\';                 }             }             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \'TEXTAREA\') {             var myvalue = mynodes[i].value;             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \'SELECT\') {             var myselect = mynodes[i].selectedOptions;             if (myselect != undefined | myselect != null) {                 for (var j = 0; j < myselect.length; j++) {                     var myvalue = mynodes[i].selectedOptions[j].textContent;                     result.push(myvalue);                 }             } else {                 var myvalue = dropdowncallie(mynodes[i]);                 result.push(myvalue);             }         } else if ((mynodes[i].nodeName.toUpperCase() == \'I\')) {             var myvalue = mynodes[i].textContent;             result.push(myvalue);         }         if (mynodes[i].hasChildNodes()) {             recursfunc(mynodes[i].childNodes);         }     } }  function dropdowncallie(op) {     var x = op.options[op.selectedIndex].text;     return x; };\","+webelement+")")
        self.f.write(space+"output='True' if content == input else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def getCellToolTip(self,space,webelement,input,*args):
        self.f.write(space+"row="+input[0])
        self.f.write(space+"col="+input[1])
        self.f.write(space+"output=driver.execute_script(\"var temp = tooltip(arguments[0], arguments[1], arguments[2]); return temp; function tooltip(table, row, col) {     var no_of_rows = table.rows.length;     var no_of_col = table.rows[row - 1].cells.length;     var ele = table.rows[row - 1];     var i, j, k, tp;     for (i = 0; i < no_of_rows; i++) {         for (j = 0; j < no_of_col; j++) {             if (i == row - 1 && j == col - 1) {                 if (ele.cells[col - 1].hasAttribute('title')) {                           tp = ele.cells[col - 1].title;                     }                     else if (ele.cells[col - 1].children.length > 0) {                         for (k = 0; k < ele.cells[col - 1].children.length; k++) {                             finalele = recurseDomChildren(ele.cells[col - 1].children[k]);                             if (finalele != undefined && finalele != '') {                                                            if (finalele.hasAttribute('title') && finalele != undefined) {                                             tp = finalele.title;                                         break;                                     }                                 }                             }                         } else {                             if (ele.hasAttribute('title') && ele != undefined) {                                          tp = ele.title;                                 }                             }                         }                     }                 }                 return tp;             };              function recurseDomChildren(start) {                 var nodes, ele1;                 if (start.hasAttribute('title') && start != undefined) {                           ele1 = start;                         return ele1;                     }                     else if (start.childNodes.length > 0) {                         nodes = start.childNodes;                         ele1 = loopNodeChildren(nodes);                         if (ele1 != '') {                                      return ele1;                         }                     }                 }                  function loopNodeChildren(nodes) {                     var node, ele2;                     for (var i = 0; i < nodes.length; i++) {                         node = nodes[i];                         if (node.childNodes.length > 0) {                             ele2 = recurseDomChildren(node);                             if (ele2 != ''  && ele2 != undefined) {                                      if (ele2.hasAttribute('title')){                                                     break;                                     }                                 }                             }                             else if (node.nodeType === 1) {                                 if (node.hasAttribute('title') && node != undefined) {                                              ele2 = node;                                         break;                                     }                                 }                                 else {                                     ele2 = '';                                       }                             }                             return ele2;                         }; \","+webelement+",row,col)")
        self.f.write(space+"status='Pass'")

    def verifyCellToolTip(self,space,webelement,input,*args):
        self.f.write(space+"row="+input[0])
        self.f.write(space+"col="+input[1])
        self.f.write(space+"input="+input[2])
        self.f.write(space+"tooltip=driver.execute_script(\"var temp = tooltip(arguments[0], arguments[1], arguments[2]); return temp; function tooltip(table, row, col) {     var no_of_rows = table.rows.length;     var no_of_col = table.rows[row - 1].cells.length;     var ele = table.rows[row - 1];     var i, j, k, tp;     for (i = 0; i < no_of_rows; i++) {         for (j = 0; j < no_of_col; j++) {             if (i == row - 1 && j == col - 1) {                 if (ele.cells[col - 1].hasAttribute('title')) {                           tp = ele.cells[col - 1].title;                     }                     else if (ele.cells[col - 1].children.length > 0) {                         for (k = 0; k < ele.cells[col - 1].children.length; k++) {                             finalele = recurseDomChildren(ele.cells[col - 1].children[k]);                             if (finalele != undefined && finalele != '') {                                                            if (finalele.hasAttribute('title') && finalele != undefined) {                                             tp = finalele.title;                                         break;                                     }                                 }                             }                         } else {                             if (ele.hasAttribute('title') && ele != undefined) {                                          tp = ele.title;                                 }                             }                         }                     }                 }                 return tp;             };              function recurseDomChildren(start) {                 var nodes, ele1;                 if (start.hasAttribute('title') && start != undefined) {                           ele1 = start;                         return ele1;                     }                     else if (start.childNodes.length > 0) {                         nodes = start.childNodes;                         ele1 = loopNodeChildren(nodes);                         if (ele1 != '') {                                      return ele1;                         }                     }                 }                  function loopNodeChildren(nodes) {                     var node, ele2;                     for (var i = 0; i < nodes.length; i++) {                         node = nodes[i];                         if (node.childNodes.length > 0) {                             ele2 = recurseDomChildren(node);                             if (ele2 != ''  && ele2 != undefined) {                                      if (ele2.hasAttribute('title')){                                                     break;                                     }                                 }                             }                             else if (node.nodeType === 1) {                                 if (node.hasAttribute('title') && node != undefined) {                                              ele2 = node;                                         break;                                     }                                 }                                 else {                                     ele2 = '';                                       }                             }                             return ele2;                         }; \","+webelement+",row,col)")
        self.f.write(space+"output='True' if tooltip == input else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def getInnerTable(self,space,webelement,input,*args):
        self.f.write(space+"row="+input[0])
        self.f.write(space+"col="+input[1])
        self.f.write(space+"output=driver.execute_script(\"var temp = fun(arguments[0], arguments[1], arguments[2]); return temp;  function fun(table, x, y) {     row = table.rows[x];     cell = row.cells[y];     tableCheck = cell.getElementsByTagName('table'); if(tableCheck.length > 0){        console.log(tableCheck[0]);       return tableCheck[0];    }else{      return null; } }\","+webelement+",row,col)")
        self.f.write(space+"status='Pass'")

    def cellClick(self,space,webelement,input,*args):
        self.f.write(space+"row="+input[0])
        self.f.write(space+"col="+input[1])
        self.f.write(space+"input="+input[3])
        if len(input)==2:
            self.f.write(space+"remoteele=driver.execute_script('var temp = fun(arguments[0], arguments[2], arguments[1]); return temp;  function fun(table, x, y) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (xx <= x && x < xx + cell.colSpan && yyy <= y && y < yyy + cell.rowSpan) return cell;         }     }     return null; };',"+webelement+",row,col)")
            self.f.write(space+"remoteele.find_elements_by_xpath('.//*')[0].click()")
        elif len(input)>2:
            self.f.write(space+"remoteele=driver.execute_script('var temp = fun(arguments[0], arguments[2], arguments[1]); return temp;  function fun(table, x, y) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (xx <= x && x < xx + cell.colSpan && yyy <= y && y < yyy + cell.rowSpan) return cell;         }     }     return null; };',"+webelement+",row,col)")
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
                obj="//"+input[2].lower()
            self.f.write(space+"remoteele.find_elements_by_xpath('"+obj+"')[input].click()")
        self.f.write(space+"status='Pass'")

class Textbox_Keywords():

    def __init__(self,f):
        self.f=f
        # self.key = b'\x74\x68\x69\x73\x49\x73\x41\x53\x65\x63\x72\x65\x74\x4b\x65\x79'

    def clearText(self,space,webelement,input,*args):
        self.f.write(space+""+webelement+".clear()")
        self.f.write(space+"status='Pass'")

    def setText(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"driver.execute_script('arguments[0].value=arguments[1]',"+webelement+",input)")
        self.f.write(space+"status='Pass'")

    def sendValue(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+""+webelement+".send_keys(input)")
        self.f.write(space+"status='Pass'")

    def getText(self,space,webelement,input,*args):
        self.f.write(space+"output=driver.execute_script('return arguments[0].value',"+webelement+")")
        self.f.write(space+"status='Pass'")

    def verifyText(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"text_val=driver.execute_script('return arguments[0].value',"+webelement+")")
        self.f.write(space+"output='True' if text_val == input else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def getTextboxLength(self,space,webelement,input,*args):
        self.f.write(space+"output="+webelement+".get_attribute('maxlength')")
        self.f.write(space+"status='Pass'")

    def verifyTextboxLength(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"text_len="+webelement+".get_attribute('maxlength')")
        self.f.write(space+"output='True' if text_len == input else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def setSecureText(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        # input=self.decrypt(input_val[0])
        self.f.write(space+"driver.execute_script('arguments[0].value=arguments[1]',"+webelement+",decrypt(input))")
        self.f.write(space+"status='Pass'")

    def sendSecureValue(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        # input=self.decrypt(input_val[0])
        self.f.write(space+""+webelement+".send_keys(decrypt(input))")
        self.f.write(space+"status='Pass'")

    
    # def decrypt(self,enc):
    #     import base64
    #     from Crypto.Cipher import AES
    #     unpad = lambda s : s[0:-ord(s[-1])]
    #     enc = base64.b64decode(enc)
    #     cipher = AES.new(self.key, AES.MODE_ECB)
    #     return unpad(cipher.decrypt(enc).decode('utf-8'))

class Util_Keywords():

    def __init__(self,f):
        self.f=f

    def tab(self,space,webelement,input,*args):
        self.f.write(space+""+webelement+".send_keys(Keys.TAB)")
        self.f.write(space+"status='Pass'")

    def sendFunctionKeys(self,space,webelement,input,*args):
        self.f.write(space+"input="+input[0])
        self.f.write(space+""+webelement+".send_keys(input)")
        self.f.write(space+"status='Pass'")

    def verifyVisible(self,space,webelement,input,*args):
        self.f.write(space+"visibility=driver.execute_script(\"var isVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })(); var s = arguments[0]; return isVisible(s);\","+webelement+")")
        self.f.write(space+"output='True' if visibility else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def verifyHidden(self,space,webelement,input,*args):
        self.f.write(space+"hidden=driver.execute_script(\"var isVisible = (function() {     function inside(schild, sparent) {         while (schild) {             if (schild === sparent) return true;             schild = schild.parentNode;         }         return false;     };     return function(selem) {         if (document.hidden || selem.offsetWidth == 0 || selem.offsetHeight == 0 || selem.style.visibility == 'hidden' || selem.style.display == 'none' || selem.style.opacity === 0) return false;         var srect = selem.getBoundingClientRect();         if (window.getComputedStyle || selem.currentStyle) {             var sel = selem,                 scomp = null;             while (sel) {                 if (sel === document) {                     break;                 } else if (!sel.parentNode) return false;                 scomp = window.getComputedStyle ? window.getComputedStyle(sel, null) : sel.currentStyle;                 if (scomp && (scomp.visibility == 'hidden' || scomp.display == 'none' || (typeof scomp.opacity !== 'undefined' && !(scomp.opacity > 0)))) return false;                 sel = sel.parentNode;             }         }         return true;     } })(); var s = arguments[0]; return isVisible(s);\","+webelement+")")
        self.f.write(space+"output='True' if not(hidden) else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def verifyEnabled(self,space,webelement,input,*args):
        self.f.write(space+"enabled = "+webelement+".is_enabled()")
        self.f.write(space+"output='True' if enabled else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def verifyDisabled(self,space,webelement,input,*args):
        self.f.write(space+"disabled = "+webelement+".is_enabled()")
        self.f.write(space+"output='True' if not(disabled) else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def verifyExists(self,space,webelement,input,*args):
        self.f.write(space+"output='True' if "+webelement+" != None or "+webelement+" != '' else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def verifyDoesNotExists(self,space,webelement,input,*args):
        self.f.write(space+"output='True' if "+webelement+" == None or "+webelement+" == '' else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def verifyReadOnly(self,space,webelement,input,*args):
        self.f.write(space+"readonly_value = "+webelement+".get_attribute('readonly')")
        self.f.write(space+"output='True' if readonly_value is not None and readonly_value.lower() =='true' or readonly_value is '' else 'False'")
        self.f.write(space+"status='Pass' if output == 'True' else 'Fail'")

    def drag(self,space,webelement,input,*args):
        self.f.write(space+"action=webdriver.ActionChains(driver).clickAndHold("+webelement+").move_to_element("+webelement+").double_click("+webelement+").perform()")
        self.f.write(space+"status='Pass'")

    def drop(self,space,webelement,input,*args):
        self.f.write(space+"action.release("+webelement+").perform()")
        self.f.write(space+"status='Pass'")

    def waitForElementVisible(self,space,webelement,input,*args):
        self.f.write(space+"input="+input)
        self.f.write(space+"from selenium.webdriver.support.ui import WebDriverWait")
        self.f.write(space+"from selenium.webdriver.support import expected_conditions as EC")
        self.f.write(space+"from selenium.common.exceptions import TimeoutException")
        self.f.write(space+"from selenium.webdriver.common.by import By")
        self.f.write(space+"element_present = EC.presence_of_element_located((By.XPATH, input))")
        self.f.write(space+"WebDriverWait(driver, 10).until(element_present)")
        self.f.write(space+"status='Pass'")