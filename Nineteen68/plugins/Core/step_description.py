#-------------------------------------------------------------------------------
# Name:        step_description.py
# Purpose:
#
# Author:      sushma.p
#
# Created:
# Copyright:   (c) sushma.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class StepDescription:


    def generic(self,keyword,tsp,input,output,con,reporting_obj):

        #Date operations
        def getCurrentTime():
            return 'Get current time of the system and save the time '+ output + ' in '+ tsp.outputval
        def getCurrentDate():
            return 'Get current date of the system and save the date ' + tsp.outputval + ' in '+ tsp.outputval
        def getCurrentDateAndTime():
            return 'Get current date and time of the system and save the date and time '+ tsp.inputval[0] + ' and '+ tsp.inputval[1] + ' in '+ tsp.outputval


        #File operations
        def executeFile():
            return 'Perform execution of the file'  + input
        def verifyContent():
            return ' Verify '+ tsp.inputval[1]+ ' is present in the file ' + input
        def getContent():
                return 'Get content from the file ' + input+ ' and save it in '+ tsp.outputval
        def compareFiles():
            return 'Compare the contents of file ' + input + ' and '+ input
        def executeScript():
            return 'Perform execution of the file ' + input

        #Math opeartions
        def add():
            return 'Add the numbers ' + input+ ' and save the value ' + output + ' in '+ tsp.outputval
        def evaluate():
            return 'Evaluate Mathematical expression ' + input+ ' and save the result ' + output + '  in '+ tsp.outputval

        #Compare keywords
        def VerifyObjects():
            return 'Verify objects ' + input + ' and ' + input+ ' and save the result in '+ tsp.outputval + '.'

        #String operations
        def toLowerCase():
            return ' Change ' + input+ ' to Lower case and save the value ' + output+ ' in ' + tsp.outputval
        def evaluate():
            return 'Evaluate Mathematical expression ' + input+ ' and save the result ' + output + '  in '+ tsp.outputval
        def concatenate():
            return ' Concatenate string '+ input + ',' + sb.toString()+ ' and save the value ' + output + ' in '+ tsp.outputval
        def toUpperCase():
            return ' Change ' + input+ ' to Upper case and save the value ' + output+ ' in ' + tsp.outputval
        def trim():
            return ' Trim ' + input+ ' and save the value ' + output + ' in '+ tsp.outputval


        #delay keywords
        def wait():
            return 'Wait for ' + input+ ' Second(s)'
        def pause():
            return 'Pause the application until the user interrupts'
        def displayVariableValue():
            return output.replace('\n',' ')

        #Dynamic variable keywords
        def deleteDynVariable():
            return 'Delete variable ' + tsp.inputval[0]
        return locals()[keyword]()


        def GetBlockValue():
            return 'Get Block Value of XML and save the value '" + output+ "' in '" + tsp.outputval + "''

        def VerifyValues():
            return "Verify values \"" + input + "\" and \"" + tsp.inputval[1]+ "\" and save the result in \""+ tsp.outputval + "\"."

        def captureScreenshot():

            return 'Captured Screenshot'

        def changeDateFormat():

            return "Change the format of the date '"+ input + "' to format '"+ tsp.inputval[1]+ "' and save the date  '" + output + "' in "+tsp.outputval

        def clearFileContent():
#            this needs to be implemeted
##            if(testStepProperty.getInputVal().size() == 2){
##			String path = testStepProperty.getInputVal().get(0).trim();
##			if (UtilKeyword.checkforDynamicVariables(path)) {
##				path = UtilKeyword.dynamicVarGeneration(path, null);
##			}
##			String fileName = testStepProperty.getInputVal().get(1).trim();
##			if (UtilKeyword.checkforDynamicVariables(fileName)) {
##				fileName = UtilKeyword.dynamicVarGeneration(fileName, null);
##			}
##			String extension = FilenameUtils.getExtension(path + fileName);
##
##			if (extension.equalsIgnoreCase(TestAutomationConstants.FILE_TYPE_TEXT) || extension.equals(TestAutomationConstants.FILE_TYPE_XML)) {
##				testDesicriptionDirectory.put("clearFileContent", "Clear all the content of the file '"
##						+ fileName + "' present in the path  '" + path + "'");
##			}  else if (extension.equals(TestAutomationConstants.FILE_TYPE_XLS) || extension.equals(TestAutomationConstants.FILE_TYPE_XLSX)) {
##				if(testStepProperty.getInputVal().size() == 3){
##				 String sheetName = testStepProperty.getInputVal().get(2).trim();
##		            if (UtilKeyword.checkforDynamicVariables(sheetName)) {
##						sheetName = UtilKeyword.dynamicVarGeneration(
##								sheetName, null);
##					}
##				testDesicriptionDirectory.put("clearFileContent", "Clear all the content of the file '"
##						+ fileName + "','" + sheetName + "' present in the path  '" + path + "'");
##				}else{
##					testDesicriptionDirectory.put("clearFileContent", "ClearFileContent failed - SheetName is missing");
##				}
##			}else{
##				testDesicriptionDirectory.put("clearFileContent", "ClearFileContent failed - File type is Invalid ");
##			}
            return  "Cleard all the content of the file '"


        def compareContent():
            return "Compare the contents of file '"+ input+ "' and '"+ tsp.inputval[1]+ "'"

        def concatenate():
            return "Concatenate string '"+ input + "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def copyValue():
            return "Copy value to variable '"+ input+ "' from variable '"+ tsp.inputval[1] + "'"
        def createDynVariable():
            return "Create a variable '"+ input+ "' with value '"+ tsp.inputval[1] + "'"
        def dateAddition():
            return "Add the date '"+ input + "' to'"+ tsp.inputval[1]+ "' number of days and save the date'" + output + "' in '"+ tsp.outputval
        def dateCompare():
            return "Compare '" + input+ "' and '" + tsp.inputval[1] + "'."
        def dateDifference():
            return "Get the difference between the dates '"+ input+ "' and '"+ tsp.inputval[1]+ "' and save the date '" + output+ "' in '"+ tsp.outputval + "'"
        def exportData():
            return "Execute SQL Query '"+ tsp.inputval[5]+" and save resultset in " + output
        def find():
            return "Verify input string '"+ input + "' contains '"+ tsp.inputval[1] + "'"
        def getBlockCount():
            return "Get the Block Count of XML and save the value '" + output+ "' in '" + tsp.outputval + "'"
        def getContent():
            return "Get content from the pdf '" + input+ "' and save it in '"+ tsp.outputval + "'"
        def getCurrentDate():
            return 'Get current date of the system and save the date ' + tsp.outputval + ' in '+ tsp.outputval
        def getCurrentDateAndTime():
            return 'Get current date and time of the system and save the date and time '+ tsp.inputval[0] + ' and '+ tsp.inputval[1] + ' in '+ tsp.outputval
        def getCurrentTime():
            return 'Get current time of the system and save the time '+ output + ' in '+ tsp.outputval
        def getData():
            return "Execute SQL Query '"+ tsp.inputval[5]+" and save resultset in " + output
        def getIndexCount():
            return "The index count for the dynamic variable '"+ input+ "' is '"+ tsp.inputval[1] + "'"
        def getLineNumber():
            return "Get the line number of content '"+ input+ "' from file '"+ tsp.inputval[1]+ "' and save the value '" + output + "' in "+tsp.outputval
        def getParam():
            return "Get data from file '"+ input + "' and  sheet '"+ tsp.inputval[1] + "'"
        def getStringLength():
            return "Get the length of the string '" + input+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def getSubString():
            return "Get Substring of the string '"+ input+ "' with index/range '"+ tsp.inputval[1]+ "'  and save the value '" + output+ "' in variable '"+ tsp.outputval + "'"
        def getTagValue():
            return "Get Tag Value of XML and save the value '" + output+ "' in '" + tsp.outputval + "'"
        def left():
            return "Perform String operation Left on string '"+ input+ "' with index '"+ tsp.inputval[1]+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def mid():
            return "Perform String operation Mid on string '" + input+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def modifyValue():
            return "Modify variable '"+ input + "' value to '"+ tsp.inputval[1] + "'"
        def monthAddition():
            return "Add Months '"+ input + "' value to '"+ tsp.inputval[1] + "'"
        def mousePress():
            return 'Mouse Pressed'
        def replace():
            return "In string '"+ input + "' replace '"+ tsp.inputval[1] + "' with '"+ tsp.inputval[2]+ "' and save the updated input string '" + output+ "' in '" + tsp.outputval + "'"
        def replaceContent():
            return "Replace '"+ input + "' in the '"+ tsp.inputval[1] + " with the "+ tsp.inputval[2]
        def right():
            return "Perform String operation right on string '"+ input+ "' with index '"+ tsp.inputval[1]+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def runQuery():
            return "Execute SQL Query '"+ tsp.inputval[5]+" and save resultset in " + output
        def secureExportData():
            return "Execute SQL Query '"+ tsp.inputval[5]+" and save resultset in " + output
        def secureGetData():
            return "Execute SQL Query '"+ tsp.inputval[5]+" and save resultset in " + output
        def secureRunQuery():
            return "Execute SQL Query '"+ tsp.inputval[5]+" and save resultset in " + output
        def secureVerifyData():
            return "Verify SQL Query '"+ tsp.inputval[5]+ "' and result is same as '"+ tsp.inputval[7] + ","+ tsp.inputval[8] + "'"
        def sendFunctionKeys():
            return "Execute Function key  "+ input
        def split():
            return "Split the string '"+ input+ "' with split character '"+ tsp.inputval[1]+ "' and save the value:"+ tsp.inputval[2] + " in '"+ tsp.outputval + "'"
        def stop():
            return "Stop the Exceution"
        def stringGeneration():
            return "Generate a charecter string having a length '"+ input + "'."
        def toLowerCase():
            return ' Change ' + input+ ' to Lower case and save the value ' + output+ ' in ' + tsp.outputval
        def toUpperCase():
            return ' Change ' + input+ ' to Upper case and save the value ' + output+ ' in ' + tsp.outputval
        def trim():
            return ' Trim ' + input+ ' and save the value ' + output + ' in '+ tsp.outputval
        def verifyContent():
            return "Verify '"+ tsp.inputval[1]+ "' is present in the file '" + input + "'"
        def verifyData():
            return "Verify SQL Query '"+ tsp.inputval[5]+ "' and result is same as '"+ tsp.inputval[7] + ","+ tsp.inputval[8] + "'"
        def verifyFileImages():
            return "Compare images '" + input+ "' and '" + tsp.inputval[1]+ "'"
        def wait():
            return 'Wait for ' + input+ ' Second(s)'
        def writeToFile():
            return "Write '"+ tsp.inputval[1] + "' to file  '" + input + "'"
        def yearAddition():
            return "Add Years '"+ input + "' value to '"+ tsp.inputval[1] + "'"


    def webservices(self,keyword,tsp,input,output,con,reporting_obj):

        def setWholeBody():
            return 'Set the entire body ' + input+ ' that needs to be sent in the request'
        def setOperations():
            return 'Set the Operation ' + input+ 'that needs to be performed on the request'
        def setMethods():
            return 'Set the method type ' + input + ' for the operation.'
        def setHeaderTemplate():
            return 'Set the header ' + input+ ' from the header Template.'
        def setEndPointURL():
            return 'Set the end point URL ' + input + '.'
        def setTagValue():
            return 'Set the Tag Value ' + input + ' for the tag '+ "'" + tsp.custname + "'" + '.'
        def setHeader():
            return 'Set the header '+ input + ' that needs to be sent in the request.'
        def setTagAttribute():
            return 'Set the Tag attribute ' + input + ' for the tag '+ "'" + tsp.custname + "'" + '.'


        def getHeader():
            return 'Fetch the header ' + output+ ' that was received as a response.'
        def getBody():
            return 'Fetch the entire body ' + output+ ' that was received as a response.'
        def addClientCertificate():
            return 'Add the certificate present in the '+ tsp.inputval[0]+ ' to the '+ tsp.inputval[1] + '.'
        def getServerCertificate():
            return 'Fetch the Server certificate and save it in '+ tsp.inputval[1] + '.'
        def executeRequest():
            return 'Execute the request.'
        locals()[key](keyword)


    def desktop(self,keyword,tsp,input,output,con,reporting_obj):
        #dropdown keywords
        def DeselectAll():
            return 'Deselect all values in the '+ "'" + tsp.custname + "'"
        def GetValueByIndex():
            return 'Get value with index ' + input + ' in the '+ "'" + tsp.custname + "'" + ' and save the value ' + output + ' in '+ tsp.outputval,
        def VerifyValuesExists():
            return 'Verify values ' + input + ' exists in the '+ "'" + tsp.custname + "'"
        def SelectMultipleValuesByText():
            return 'Select values ' + input + 'in the '+ "'" + tsp.custname + "'"
        def SelectValueByText():
            return 'Select value by text '+input+' of the '+ 'type '+ "'" + tsp.custname + "'" +' with the element '+input+' present in the table cell '+"'" + tsp.custname + "'"+'-['+ input + ']['+ input +']',
        def GetCount():
            return 'Get the count of the values present in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output + ' in '+ tsp.outputval,
        def SelectMultipleValuesByText():
            return 'Select values ' + input + 'in the '+ "'" + tsp.custname + "'"
        def SelectMultipleValuesByText():
            return 'Select values ' + input + 'in the '+ "'" + tsp.custname + "'"
        def VerifyCount():
            return 'Verify the count of the values present in the ' + "'" + tsp.custname + "'" + ' with the '+ input
        def SelectAllValues():
            return 'Select all values in the '+ "'" + tsp.custname + "'"
        def VerifySelectedValue():
            return 'Verify the selected value from the ' + "'" + tsp.custname + "'"+ ' with the '+ input
        def GetSelected():
            return 'Get selected value from the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output+ ' in '+ tsp.outputval
        def GetMultipleValuesByIndexes():
            return 'Get values with indexes ' + input + ' in the '+ "'" + tsp.custname + "'" +'and save the value ' + input+ ' in  ' +tsp.outputval
        def VerifyAllValues():
            return 'Verify the values from the '+ "'" + tsp.custname + "'" +' with '+ input

        #Radio checkbox keywords
        def SelectRadioButton():
            return 'Select '+ "'" + tsp.custname + "'"
        def GetStatus():
            return 'Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' + output + ' in '+ tsp.outputval + ')'

        #Application keywords
        def LaunchApplication():
            return ' The application present in the path  '+ tsp.inputval[0]+ 'is launched'
        def GetPageTitle():
            return ' The page title is '+ output +' and  is saved  in the variable ' +tsp.outputval
        def CloseApplication():
            return ' The application is closed'

        #Element keywords
        def GetElementText():
            return ' Get the value present in ' + "'" + tsp.custname + "'" +' and save the value ' + output + ' in '+ tsp.outputval
        def VerifyElementDoesNotExists():
            return 'Verify '+ "'" + tsp.custname + "'" + ' does not exists '
        def ClickElement():
            return 'Click on ' +"'" + tsp.custname + "'"

        #text box
        return locals()[keyword]()

    def web(self,keyword,tsp,input,output,con,reporting_obj):

        #Popup keywords
        def verifyPopUpText():
            return ' Verify ' + input+ '  is the Popup text '
        def verifyDialogText():
            return ' Verify '+ input + ' is the text of Window Dialog '
        def dismissPopUp():
            return 'Close the Popup'
        def acceptPopUp():
            return 'Accept the Popup'
        def getPopUpText():
            return 'Get the text of the Popup and save the text ' + output+ ' in ' + tsp.outputval


        #Textbox keywords
        def verifyText():
            return 'Verify ' + input + ' is the the text in the '+ "'" + tsp.custname + "'"
        def sendValue():
            return ' Enter value ' + input+ ' in the '+ "'" + tsp.custname + "'"
        def verifyTextboxLength():
            return 'Verify ' + input + ' is the length of textbox '+ "'" + tsp.custname + "'"
        def setSecureText():
            return 'Enter secure text ' +tsp.inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"



        #Image keywords
        def verifyWebImages():
            return ' Compare images '+ "'" + tsp.custname + "'" + ' and ' + input

        #dropdown keywords
        def getSelected():
            return 'Get Selected value of '+ "'" + tsp.custname + "'"+ ' and save value ' + output + ' in '+ tsp.outputval
        def selectMultipleValuesByText():
            return 'Select values ' + mulInputVal.toString() + ' in the '+ "'" + tsp.custname + "'"
        def deselectAll():
            return 'Deselect all values in the '+ "'" + tsp.custname + "'"
        def getValueByIndex():
            return 'Get value with index ' + input + ' in the '+ "'" + tsp.custname + "'" + ' and save the value ' + output + ' in '+ tsp.outputval,
        def verifyValuesExists():
            return 'Verify values ' + input + ' exists in the '+ "'" + tsp.custname + "'"
        def selectValueByText():
            return 'Select value by text '+input+' of the '+ 'type '+ "'" + tsp.custname + "'" +' with the element '+input+' present in the table cell '+"'" + tsp.custname + "'"+'-['+ input + ']['+ input +']',
        def getMultipleValuesByIndexes():
            return 'Get values with indexes ' + inputValsb.toString() + ' in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + TestAutomationController.multipleOutputResult + ' in  '+ tsp.outputval
        def verifySelectedValues():
            return 'Verify values ' + input + ' are selected in the '+ "'" + tsp.custname + "'"
        def getAllValues():
            return 'getAllValues ' + output + ' are present in the' + "'" + tsp.custname + "'"
        def verifyAllValues():
            return 'Verify values ' + input + ' are present in the '+ "'" + tsp.custname + "'"
        def selectMultipleValuesByIndexes():
            return 'Select values ' + mulInputValin.toString() + ' in the '+ "'" + tsp.custname + "'"
        def selectAllValues():
            return 'Select all values in the ' +"'" + tsp.custname + "'"
        def verifyCount():
            return 'Verify ' + input + ' is the list count of the ' +"'" + tsp.custname + "'"
        def verifySelectedValue():
            return 'Verify value ' + input + ' is selected in the ' +"'" + tsp.custname + "'"
        def selectValueByIndex():
            return 'Select the value '+ input+' of the '+"'" + tsp.custname + "'"+' with the index '+input+' present in the table cell  '+"'" + tsp.custname + "'"+'-['+input+']['+input+']'
        def getCount():
            return 'Get the count of values in the '+ "'" + tsp.custname + "'"+ ' and save the count ' + output + ' in ' +tsp.outputval

        #Radio checkbox keywords
        def selectRadioButton():
            return 'Select '+ "'" + tsp.custname + "'"
        def getStatus():
            return 'Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' + output + ' in '+ tsp.outputval
        def selectCheckbox():
            return 'Select '+ "'" + tsp.custname + "'"
        def unselectCheckbox():
            return 'Unselect '+ "'" + tsp.custname + "'"

        #Browser keywords
        def openBrowser():
            return ' Open ' + reporting_obj.browser_type+ ' browser'
        def openNewBrowser():
            return 'Open new instance of the browser'
        def maximizeBrowser():
            return 'Maximize the browser ' + input
        def closeBrowser():
            return 'Close the browser '
        def navigateToURL():
            return 'Open url ' + input+ ' in the browser'
        def navigateForward():
            return 'Navigate forward in the browser'
        def navigateWithAuthenticate():
            return ' Open url ' + input	+ ' in the browser'
        def navigateBack():
            return 'Navigate back in the browser'
        def verifyTextExists():
            return 'Verify static text ' + input + ' exists'
        def getCurrentURL():
            return 'Get current url of the web page and save the URL '+ output + ' in '+ tsp.outputval
        def verifyCurrentURL():
            return ' Verify url '+ input + ' is the current url of the web page'
        def verifyPageTitle():
            return 'Verify ' + input+ ' is the page title of the web page'
        def getPageTitle():
            return 'Get the title of the web page and save the title '+ output + ' in '+ tsp.outputval
        def closeSubWindows():
            return 'Closed the current sub window.'
        def openNewTab():
            return 'Open new tab in the current browser'

        #Element keywords
        def getToolTipText():
            return 'Get the tool tip from the '+ "'" + tsp.custname + "'"+ ' and save the tool tip text ' + output+ ' in ' + tsp.outputval
        def verifyToolTipText():
            return 'Verify ' + input + ' is the tooltip of  '+ "'" + tsp.custname + "'"
        def clickElement():
            return ' Click '+ "'" + tsp.custname + "'"
        def mouseClick():
            return ' Mouse Click on  '+ "'" + tsp.custname + "'"
        def verifyElementText():
            return 'Verify ' + input + ' is the the text of the '+ "'" + tsp.custname + "'"
        def verifyElementExists():
            return ' Verify '+ "'" + tsp.custname + "'" + ' exists '
        def getElementText():
            return 'Get the text of the element '+ "'" + tsp.custname + "'"+ ' and save the value  '+ output + ' in '+ tsp.outputval
        def verifyDoesNotExists():
            return ' Verify '+ "'" + tsp.custname + "'" + '  does not exists '
        def tab():
            return 'Perform tab on '+ "'" + tsp.custname + "'" + ')'

        def rightClick():
            return 'Perform right click on element '+ "'" + tsp.custname + "'"
        def doubleClick():
            return 'Double click on the '+ "'" + tsp.custname + "'"
        def waitForElementVisible():
            return 'Wait until the element '+ "'" + tsp.custname + "'" +'is visible'

        #Button link keywords
        def click():
            return ' Click on the '+ "'" + tsp.custname + "'"
        def cellClick():
            return 'Click ' + "'" + tsp.custname + "'"
        def verifyButtonName():
            return 'Verify text ' + input + ' is the name of the '+ "'" + tsp.custname + "'"
        def uploadFile():
            return ' Upload the file '+ filename + ' present in the path ' + input + '.'
        def getLinkText():
            return ' Get Text From '+ "'" + tsp.custname + "'" + ' and save the text '+ output + ' in ' + tsp.outputval
        def getButtonName():
            return ' Get ButtonName From '+ "'" + tsp.custname + "'" + ' and save the text '+ output + ' in ' + tsp.outputval
        def verifyLinkText():
            return 'Verify text ' + input + ' is the name of the ' +"'" + tsp.custname + "'"

        #utilweb operations
        def verifyReadOnly():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is read-only'
        def verifyEnabled():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is enabled '
        def verifyDisabled():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is disabled '
        def verifyExists():
            return ' Verify '+ "'" + tsp.custname + "'" + '  exists '
        def verifyHidden():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is Hidden '
        def verifyVisible():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is Visible '
        def mouseHover():
            return ' Move mouse pointer to '+ "'" + tsp.custname + "'"
        def setFocus():
            return ' Set the focus on '+ "'" + tsp.custname + "'"
        def press():
            return 'Press on the '+ "'" + tsp.custname + "'"
        def drag():
            return 'Perform drag on element '+ "'" + tsp.custname + "'"
        def drop():
            return 'Perform drop on element '+ "'" + tsp.custname + "'"

        #Table keywords
        def getCellToolTip():
            return 'Get the cell tooltip from the '+ "'" + tsp.custname + "'"+ ' and save the tool tip text ' + output+ ' in ' + tsp.outputval
        def cellClick():
            return 'Click ' + "'" + tsp.custname + "'"
        def getRowCount():
            return 'Get row count of the ' + "'" + tsp.custname + "'" + ' and save the count ' + output + ' in '+ tsp.outputval
        def getColumnCount():
            return 'Get column count of the '+ "'" + tsp.custname + "'"+ ' and save the count '+ output + ' in '+ tsp.outputval
        def verifyCellValue():
            return 'Verify cell value [Null] is present in the '+ "'" + tsp.custname + "'" + ' Invalid input'
        def cellClick():
            return 'Click ' + "'" + tsp.custname + "'"
        def getColNumByText():
            return 'Get column number of ' + "'" + tsp.custname + "'" + ' by text '+input +' and save the column number ' + output + ' in '+ tsp.outputval
        def getRowNumByText():
            return 'Get row number of ' + "'" + tsp.custname + "'" + ' by text '+input +' and save the row number ' + output + ' in '+ tsp.outputval
        def getCellValue():
            return 'Get row number of ' + "'" + tsp.custname + "'" + ' by text '+input +' and save the row number ' + output + ' in '+ tsp.outputval
        return locals()[keyword]()

