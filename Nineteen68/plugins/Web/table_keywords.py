#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     08-11-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


from selenium import webdriver
import Exceptions
import webconstants
import logger
import json
from  selenium.webdriver.common import action_chains
import time
import browser_Keywords
driver=''
class TableOperationKeywords():

#   returns the row count of table if the table found with the given xpath
        def getRowCount(self,element,*args):
            driver=browser_Keywords.driver_obj
            status=webconstants.STATUS_FAIL
            row_count=None
            visibleFlag==True
            if visibleFlag==True:
                try:
                    webElement=driver.find_elements_by_xpath(xpath)
                    if webElement!=None:
                        js='var targetTable = arguments[0]; var rowCount = targetTable.rows; return rowCount.length;'
                        row_count = driver.execute_script(js,element)
                        if(row_count>=0):
                            status=webconstants.STATUS_SUCCESS
                            return status,row_count
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.log('hidden object')
            return status,row_count

#   returns the no of coloumns of the table if the table found with the given xpath
        def getColoumnCount(self,element,*args):
            status=webconstants.STATUS_FAIL
            coloumn_count=None
            driver=browser_Keywords.driver_obj
            visibleFlag==True
            if visibleFlag==True:
                try:
                    webElement=element
                    if webElement!=None:
                        js='var targetTable = arguments[0]; var columnCount = 0; var rows = targetTable.rows; if(rows.length > 0) { 	for (var i = 0; i < rows.length; i++) { 		var cells = rows[i].cells; 		var tempColumnCount = 0; 		for (var j = 0; j < cells.length; j++) { 			tempColumnCount += cells[j].colSpan; 		} 		if (tempColumnCount > columnCount) { 			columnCount = tempColumnCount; 		} 	} } return columnCount;'
                        coloumn_count = driver.execute_script(js,element)
                        if(coloumn_count>=0):
                            status=webconstants.STATUS_SUCCESS
                            print coloumn_count
                            return status,coloumn_count
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.log('hidden object')
            return status,coloumn_count

#   returns the cell value of cell with ',' seperated values, if the table found with the given xpath
        def getCellValue(self,element,row_num,col_num,*args):
            status=webconstants.STATUS_FAIL
            cellVal=None
            driver=browser_Keywords.driver_obj
            visibleFlag==True
            try:
                if visibleFlag==True:
                    row_num=int(row_num)
                    col_num=int(col_num)
                    row_count=self.getRowCountJs(element)
                    col_count=self.getColoumnCountJs(element)
                    if row_num>row_count or col_num>col_count:
                        logger.log('Invalid Input')
                    else:
                        remoteWebElement=self.javascriptExecutor(element,row_num-1,col_num-1)
                        cellVal=self.getChildNodes(remoteWebElement)
                        cellVal=cellVal.strip()
                        status=webconstants.STATUS_SUCCESS
                else:
                    print 'hidden object'
            except Exception as e:
                Exceptions.error(e)
            return status,cellVal

#   verifies the cell value with the given text input, if the table found with the given xpath
        def verifyCellValue(self,element,row_num,col_num,expected_value,*args):
            status=webconstants.STATUS_FAIL
            cellVal=None
            driver=browser_Keywords.driver_obj
            visibleFlag==True
            try:
                if visibleFlag==True:
                    row_num=int(row_num)
                    col_num=int(col_num)
                    row_count=self.getRowCountJs(element)
                    col_count=self.getColoumnCountJs(element)
                    if row_num>row_count or col_num>col_count:
                        logger.log('Invalid Input')
                    else:
                        actual_rowNum=row_num-1
                        actual_colNum=col_num-1
                        remoteWebElement=self.javascriptExecutor(element,actual_rowNum,actual_colNum)
                        cellVal=self.getChildNodes(remoteWebElement)
                        cellVal=cellVal.strip()
                        expected_value=expected_value.strip()
                        if(cellVal == expected_value):
                            status=webconstants.STATUS_SUCCESS
                else:
                    print 'hidden object'
            except Exception as e:
                Exceptions.error(e)
            return status

#   returns the  tooltip text  of given cell, if the table found with the given xpath
        def getCellToolTip(self,element,row_number,col_number,*args):
            status=webconstants.STATUS_FAIL
            tooltip=None
            driver=browser_Keywords.driver_obj
            visibleFlag==True
            if visibleFlag==True:
                try:
                    row_number=int(row_number)
                    col_number=int(col_number)
                    row_count=self.getRowCountJs(element)
                    col_count=self.getColoumnCountJs(element)
                    if row_number>row_count or col_number>col_count:
                        logger.log('Invalid Input')
                    else:
                        contents = self.getTooltip(element, row_number,
    							col_number);
                        if contents !=None:
                            tooltip=contents
                            status=webconstants.STATUS_SUCCESS
                            return status,contents
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.log('hidden object')
            return status,tooltip

#   lclicks on the given cell, if the table found with the given xpath
        def cellClick(self,element,row_number,col_number,*args):
            status=webconstants.STATUS_FAIL
            row_number=int(row_number)-1
            col_number=int(col_number)-1
            driver=browser_Keywords.driver_obj
            visibleFlag==True
            if visibleFlag==True:
                try:
                    if len(args)==0:
                        cell=self.javascriptExecutor(element,row_number,col_number)
                        element_list=cell.find_elements_by_xpath('.//*')
                        print element_list
                        if len(list(element_list))>0:
                            xpath=self.getElemntXpath(element_list[0])
                            cell=driver.find_element_by_xpath(xpath)
                        try:
                            if(cell!=None):
                                if cell.is_enabled():
                                    if isinstance(driver,webdriver.Ie):
                                        try:
                                            js = 'var evType; element=arguments[0]; if (document.createEvent) {     evType = "Click executed through part-1";     var evt = document.createEvent("MouseEvents");     evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = "Click executed through part-2";   	setTimeout(function() {     element.click();   	}, 100); } return (evType);'
                                            click=driver.execute_script(js,element)
                                            status=webconstants.STATUS_SUCCESS
                                        except Exceptions as e:
                                            action=action_chains.ActionChains(driver)
                                            action.move_to_element(cell).click(cell).perform()
                                            status=webconstants.STATUS_SUCCESS
                                    else:
                                        try:
                                            cell.click()
                                        except Exception as e:
                                            js = 'var evType; element=arguments[0]; if (document.createEvent) {     evType = "Click executed through part-1";     var evt = document.createEvent("MouseEvents");     evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = "Click executed through part-2";   	setTimeout(function() {     element.click();   	}, 100); } return (evType);'
                                            click=driver.execute_script(js,element)
                                            status=webconstants.STATUS_SUCCESS
                        except Exception as e:
                            Exceptions.error(e)
                    elif len(args)>0:
                        tag=args[0]
                        index=args[1]
                        eleStatus=False
                        counter = 1
                        cell=self.javascriptExecutor(element,row_number,col_number)
                        element_list=cell.find_elements_by_xpath('.//*')
                        for member in element_list:
                              js1='function getElementXPath(elt) {var path = "";for (; elt && elt.nodeType == 1; elt = elt.parentNode){idx = getElementIdx(elt);xname = elt.tagName;if (idx >= 1){xname += "[" + idx + "]";}path = "/" + xname + path;}return path;}function getElementIdx(elt){var count = 1;for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling){if(sib.nodeType == 1 && sib.tagName == elt.tagName){count++;}}return count;}return getElementXPath(arguments[0]).toLowerCase();'
                              xpath=driver.execute_script(js1,member)
                              cellChild = driver.find_element_by_xpath(xpath)
                              tagName = cellChild.tag_name
                              tagType = cellChild.get_attribute('type')
                              xpath_elements=xpath.split('/')
                              lastElement=xpath_elements[len(xpath_elements)-1]
                              childindex=lastElement[lastElement.find("[")+1:lastElement.find("]")]
                              if tag=='button':
                                   if( (tagName==('input') and tagType==('button')) or tagType==('submit') or tagType==('reset') or tagType==('file')):
                                      if index==childindex:
                                        eleStatus =True
                                      else:
                                        if counter==index:
                                           index =childindex
                                           eleStatus =True
                                        else:
                                            counter+=counter
                              elif tag=='image':
                                  if(tagName==('input') and (tagType==('img') or tagType==('image'))):
                                     if index==childindex:
                                        eleStatus =True
                                     else:
                                        if counter==index:
                                           index =childindex
                                           eleStatus =True
                                        else:
                                            counter+=counter
                              elif tag=='img':
                                 if index==childindex:
                                        eleStatus =True
                                 else:
                                        if counter==index:
                                           index =childindex
                                           eleStatus =True
                                        else:
                                            counter+=counter
                              elif tag=='checkbox':
                                 if(tagName==('input') and (tagType==('checkbox')) ):
                                     if index==childindex:
                                        print index
                                        print childindex
                                        eleStatus =True
                                     else:
                                        if counter==index:
                                           index =childindex
                                           eleStatus =True
                                        else:
                                            counter+=counter
                              elif tag=='radiobutton':
                                 if (tagName==('input') and tagType==('radio')):
                                    if index==childindex:
                                        eleStatus =True
                                    else:
                                        if counter==index:
                                           index =childindex
                                           eleStatus =True
                                        else:
                                            counter+=counter
                              elif tag=='textbox':
                                 if (tagName==('input') and (tagType==('text') or tagType==('email') or tagType==('password') or tagType==('range') or tagType==('search') or tagType==('url')) ):
                                    if index==childindex:
                                        eleStatus =True
                                    else:
                                        if counter==index:
                                           index =childindex
                                           eleStatus =True
                                        else:
                                            counter+=counter
                              elif tag=='link':
                                if(tagName==('a')):
                                    if index==childindex:
                                        eleStatus =True
                                    else:
                                        if counter==index:
                                           index =childindex
                                           eleStatus =True
                                        else:
                                            counter+=counter
                              else:
                                    eleStatus=True


                              if eleStatus==True:
                                if cellChild.is_enabled():
                                    try:
                                      print 'before click'
                                      if not (cellChild is None):
                                        driver.execute_script("arguments[0].scrollIntoView(true);",cellChild);
                                        if isinstance(driver,webdriver.Ie):
                                            try:
                                                js = 'var evType; element=arguments[0]; if (document.createEvent) {     evType = "Click executed through part-1";     var evt = document.createEvent("MouseEvents");     evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = "Click executed through part-2";   	setTimeout(function() {     element.click();   	}, 100); } return (evType);'
                                                click=driver.execute_script(js,cellChild)
                                                status=webconstants.STATUS_SUCCESS
                                                break;
                                            except Exceptions as e:
                                                action=action_chains.ActionChains(driver)
                                                action.move_to_element(cellChild).click(cellChild).perform()
                                                status=webconstants.STATUS_SUCCESS
                                                break;
                                        else:
                                            try:
                                                cellChild.click()
                                                print 'click performed'
                                                status=webconstants.STATUS_SUCCESS
                                                break
                                            except Exception as e:
                                                js = 'var evType; element=arguments[0]; if (document.createEvent) {     evType = "Click executed through part-1";     var evt = document.createEvent("MouseEvents");     evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);   	setTimeout(function() {     	element.dispatchEvent(evt);     }, 100); } else {     evType = "Click executed through part-2";   	setTimeout(function() {     element.click();   	}, 100); } return (evType);'
                                                click=driver.execute_script(js,cellChild)
                                                status=webconstants.STATUS_SUCCESS
                                                break


                                    except Exception as e:
                                     Exceptions.error(e)

                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.log('hidden object')
            return status




        def getRowNumByText(self,element,text,*args):
            status=webconstants.STATUS_FAIL
            row_number=None
            text=text.strip()
            driver=browser_Keywords.driver_obj
            visibleFlag==True
            if visibleFlag==True:
                try:
                    js='var temp = fun(arguments[0], arguments[1]); return temp; function fun(table, str) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy, child;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (cell.innerText.indexOf(str)>= 0) return yyy + cell.rowSpan;             else if (cell.children.length > 0) {                 for (var i = 0; i < cell.children.length; i++) {                     child = cell.children[i];                     if (child.value == str) return yyy + cell.rowSpan; 					else{ 					var a=child.value; 					if(a){ 					var b=a; 					if(b.indexOf(str)>=0)return yyy + cell.rowSpan; 					}	 				}			 					                 }             }         }     }     return null; };'
                    row_number=driver.execute_script(js,element,text)
                    status=webconstants.STATUS_SUCCESS
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.log('hidden object')
            return status,row_number

        def getColNumByText(self,element,text,*args):
            status=webconstants.STATUS_FAIL
            col_number=None
            driver=browser_Keywords.driver_obj
            visibleFlag==True
            text=text.strip()
            if visibleFlag==True:
                try:
                    js='var temp = fun(arguments[0], arguments[1]); return temp; function fun(table, str) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy, child;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (cell.innerText.indexOf(str)>= 0) return xx + cell.colSpan;             else if (cell.children.length > 0) {                 for (var i = 0; i < cell.children.length; i++) {                     child = cell.children[i];                     if (child.value == str) return xx + cell.colSpan; 					else{ 					var a=child.value; 					if(a){ 					var b=a; 					if(b.indexOf(str)>=0)return xx + cell.colSpan; 					}	 				}			 					                 }             }         }     }     return null; };'
                    col_number=driver.execute_script(js,element,text)
                    status=webconstants.STATUS_SUCCESS
                except Exception as e:
                    Exceptions.error(e)
            else:
                logger.log('hidden object')
            return status,col_number


        def getChildNodes(self,element):
            contents=None
            try:
                js='var mytarget = arguments[0]; var mynodes = mytarget.childNodes; var result = []; if (typeof  String.prototype.trim  !== "function")  {       String.prototype.trim  =   function()  {             return  this.replace(/^\\s+|\\s+$/g,"");        } } recursfunc(mynodes); return result.toString();  function recursfunc(mynodes) {     for (var i = 0; i < mynodes.length; i++) {         if (mynodes[i].nodeName.toUpperCase() == \"#TEXT\") {             if ((mynodes[i].parentNode.nodeName.toUpperCase() != \"OPTION\") & (mynodes[i].parentNode.nodeName.toUpperCase() != \"SCRIPT\")) {                 var myvalue = mynodes[i].nodeValue;                 if (myvalue.trim().length > 0) {                     result.push(myvalue);                 }             }         } else if (mynodes[i].nodeName.toUpperCase() == \"INPUT\") {             if (mynodes[i].type.toUpperCase() == \"RADIO\") {                 if (mynodes[i].checked == true) {                     var myvalue = \"Selected\";                 } else {                     var myvalue = \"Unselected\";                 }             } else if (mynodes[i].type.toUpperCase() == \"CHECKBOX\") {                 if (mynodes[i].checked == true) {                     var myvalue = \"Checked\";                 } else {                     var myvalue = \"Unchecked\";                 }             } else if ((mynodes[i].type.toUpperCase() == \"BUTTON\") | (mynodes[i].type.toUpperCase() == \"SUBMIT\") | (mynodes[i].type.toUpperCase() == \"TEXT\")) {                 var myvalue = mynodes[i].value;             } else if (mynodes[i].type.toUpperCase() == \"IMAGE\") {                 var myvalue = mynodes[i].title;                 if (myvalue.trim().length < 1) {                     myvalue = mynodes[i].value;                     if (myvalue != undefined) {                         if (myvalue.trim().length < 1) {                             myvalue = \"Image\";                         }                     } else {                         myvalue = \"Image\";                     }                 }             }             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \"IMG\") {             var myvalue = mynodes[i].title;             if (myvalue.trim().length < 1) {                 myvalue = mynodes[i].value;                 if (myvalue != undefined) {                     if (myvalue.trim().length < 1) {                         myvalue = \"Image\";                     }                 } else {                     myvalue = \"Image\";                 }             }             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \"TEXTAREA\") {             var myvalue = mynodes[i].value;             result.push(myvalue);         } else if (mynodes[i].nodeName.toUpperCase() == \"SELECT\") {             var myselect = mynodes[i].selectedOptions;             if (myselect != undefined | myselect != null) {                 for (var j = 0; j < myselect.length; j++) {                     var myvalue = mynodes[i].selectedOptions[j].textContent;                     result.push(myvalue);                 }             } else {                 var myvalue = dropdowncallie(mynodes[i]);                 result.push(myvalue);             }         } else if ((mynodes[i].nodeName.toUpperCase() == \"I\")) {             var myvalue = mynodes[i].textContent;             result.push(myvalue);         }         if (mynodes[i].hasChildNodes()) {             recursfunc(mynodes[i].childNodes);         }     } }  function dropdowncallie(op) {     var x = op.options[op.selectedIndex].text;     return x; };'
                contents = driver.execute_script(js,element)
            except Exception as e:
                Exceptions.error(e)
            print contents
            print type(contents)
            return contents

        def getRowCountJs(self,element):
            js = 'var targetTable = arguments[0]; var rowCount = targetTable.rows; return rowCount.length;'
            row_count = driver.execute_script(js,element)
            return row_count

        def javascriptExecutor(self,element,row_num,col_num):
            remoteWebElement=None
            try:
                js='var temp = fun(arguments[0], arguments[2], arguments[1]); return temp;  function fun(table, x, y) {     var m = [],         row, cell, xx, tx, ty, xxx, yyy;     for (yyy = 0; yyy < table.rows.length; yyy++) {         row = table.rows[yyy];         for (xxx = 0; xxx < row.cells.length; xxx++) {             cell = row.cells[xxx];             xx = xxx;             for (; m[yyy] && m[yyy][xx]; ++xx) {}             for (tx = xx; tx < xx + cell.colSpan; ++tx) {                 for (ty = yyy; ty < yyy + cell.rowSpan; ++ty) {                     if (!m[ty]) m[ty] = [];                     m[ty][tx] = true;                 }             }             if (xx <= x && x < xx + cell.colSpan && yyy <= y && y < yyy + cell.rowSpan) return cell;         }     }     return null; };'
                remoteWebElement=driver.execute_script(js,element,row_num,col_num)
            except Exception as e:
                Exceptions.error(e)
            return remoteWebElement

        def getColoumnCountJs(self,element):
            js = 'var targetTable = arguments[0]; var rowCount = targetTable.rows; return rowCount.length;'
            row_count = driver.execute_script(js,element)
            return row_count

        def getTooltip(self,element,row_num,col_num):
            contents=None
            try:
                js = 'var temp = tooltip(arguments[0], arguments[1], arguments[2]); return temp;  function tooltip(table, row, col) {     var no_of_rows = table.rows.length;     var no_of_col = table.rows[row - 1].cells.length;     var ele = table.rows[row - 1];     var i, j, k, tp;     for (i = 0; i < no_of_rows; i++) {         for (j = 0; j < no_of_col; j++) {             if (i == row - 1 && j == col - 1) {                 if (ele.cells[col - 1].hasAttribute(\"title\")) {                     tp = ele.cells[col - 1].title;                 } else if (ele.cells[col - 1].children.length > 0) {                     for (k = 0; k < ele.cells[col - 1].children.length; k++) {                         finalele = recurseDomChildren(ele.cells[col - 1].children[k]);                         if (finalele != undefined && finalele != \"\") {                             if (finalele.hasAttribute(\"title\") && finalele != undefined) {                                 tp = finalele.title;                                 break;                             }                         }                     }                 } else {                     if (ele.hasAttribute(\"title\") && ele != undefined) {                         tp = ele.title;                     }                 }             }         }     }     return tp; };  function recurseDomChildren(start) {     var nodes, ele1;     if (start.hasAttribute(\"title\") && start != undefined) {         ele1 = start;         return ele1;     } else if (start.childNodes.length > 0) {         nodes = start.childNodes;         ele1 = loopNodeChildren(nodes);         if (ele1 != \"\") {             return ele1;         }     } }  function loopNodeChildren(nodes) {     var node, ele2;     for (var i = 0; i < nodes.length; i++) {         node = nodes[i];         if (node.childNodes.length > 0) {             ele2 = recurseDomChildren(node);             if (ele2 != \"\"  && ele2 != undefined) {               if(ele2.hasAttribute(\"title\")){                 break;               }             }         } else if (node.nodeType === 1) {             if (node.hasAttribute(\"title\") && node != undefined) {                 ele2 = node;                 break;             }         } else {             ele2 = \"\";         }     }     return ele2; };'
                contents = driver.execute_script(js,element,row_num,col_num)
            except Exception as e:
                Exceptions.error(e)
            return contents

        def getElemntXpath(self,element):
            xpath=None
            try:
                js = 'function getElementXPath(elt) {var path = "";for (; elt && elt.nodeType == 1; elt = elt.parentNode){idx = getElementIdx(elt);xname = elt.tagName;if (idx >= 1){xname += "[" + idx + "]";}path = "/" + xname + path;}return path;}function getElementIdx(elt){var count = 1;for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling){if(sib.nodeType == 1 && sib.tagName == elt.tagName){count++;}}return count;}return getElementXPath(arguments[0]).toLowerCase();'
                xpath = driver.execute_script(js,element)
            except Exception as e:
                Exceptions.error(e)
            return xpath

##if __name__ == '__main__':

##        driver = webdriver.Chrome( executable_path='chromedriver.exe')
##        res=raw_input('click ok after navigating')
##        time.sleep(5)
##        a=TableOperationKeywords()
##        element = driver.find_element_by_xpath('/html/body/form/div[3]/table/tbody/tr[3]/td[2]/div[1]/div[4]/div[1]/div[2]/table')
##        print type(element)
##        print element
##        nested_table=element.find_elements_by_tag_name('table')
##        for table in nested_table:
##            print a.getCellValue(nested_table[0],1,1,driver,True)
##
##
####        res,rownum=a.getCellValue(True,element[0],1,3,driver)
####        res=a.verifyCellValue(True,element[0],1,3,rownum,driver)
##
##        print 'End of main's