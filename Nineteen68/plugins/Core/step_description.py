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


    def generic(self,keyword,tsp,inputval,input,output,con,reporting_obj):

        #Date operations
        def getCurrentTime():
            return 'Get current time of the system and save the time '+ output + ' in '+ tsp.outputval
        def getCurrentDate():
            return 'Get current date of the system and save the date ' + tsp.outputval + ' in '+ tsp.outputval
        def getCurrentDateAndTime():
            return 'Get current date and time of the system and save the date and time '+ inputval[0] + ' and '+ inputval[1] + ' in '+ tsp.outputval


        #File operations
        def executeFile():
            return 'Perform execution of the file'  + input
        def verifyContent():
            return ' Verify '+ inputval[1]+ ' is present in the file ' + input
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
            return 'Delete variable ' + inputval[0]



        def GetBlockValue():
            return 'Get Block Value of XML and save the value '" + output+ "' in '" + tsp.outputval + "''

        def VerifyValues():
            return "Verify values \"" + input + "\" and \"" + inputval[1]+ "\" and save the result in \""+ tsp.outputval + "\"."

        def captureScreenshot():

            return 'Captured Screenshot'

        def changeDateFormat():

            return "Change the format of the date '"+ input + "' to format '"+ inputval[1]+ "' and save the date  '" + output + "' in "+tsp.outputval

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
            return "Compare the contents of file '"+ input+ "' and '"+ inputval[1]+ "'"

        def concatenate():
            return "Concatenate string '"+ input + "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def copyValue():
            return "Copy value to variable '"+ input+ "' from variable '"+ inputval[1] + "'"
        def createDynVariable():
            return "Create a variable '"+ input+ "' with value '"+ inputval[1] + "'"
        def dateAddition():
            return "Add the date '"+ input + "' to'"+ inputval[1]+ "' number of days and save the date'" + output + "' in '"+ tsp.outputval
        def dateCompare():
            return "Compare '" + input+ "' and '" + inputval[1] + "'."
        def dateDifference():
            return "Get the difference between the dates '"+ input+ "' and '"+ inputval[1]+ "' and save the date '" + output+ "' in '"+ tsp.outputval + "'"
        def exportData():
            return "Execute SQL Query '"+ inputval[5]+" and save resultset in " + output
        def find():
            return "Verify input string '"+ input + "' contains '"+ inputval[1] + "'"
        def getBlockCount():
            return "Get the Block Count of XML and save the value '" + output+ "' in '" + tsp.outputval + "'"
        def getContent():
            return "Get content from the pdf '" + input+ "' and save it in '"+ tsp.outputval + "'"
        def getCurrentDate():
            return 'Get current date of the system and save the date ' + tsp.outputval + ' in '+ tsp.outputval
        def getCurrentDateAndTime():
            return 'Get current date and time of the system and save the date and time '+ inputval[0] + ' and '+ inputval[1] + ' in '+ tsp.outputval
        def getCurrentTime():
            return 'Get current time of the system and save the time '+ output + ' in '+ tsp.outputval
        def getData():
            return "Execute SQL Query '"+ inputval[5]+" and save resultset in " + output
        def getIndexCount():
            return "The index count for the dynamic variable '"+ input+ "' is '"+ inputval[1] + "'"
        def getLineNumber():
            return "Get the line number of content '"+ input+ "' from file '"+ inputval[1]+ "' and save the value '" + output + "' in "+tsp.outputval
        def getParam():
            return "Get data from file '"+ input + "' and  sheet '"+ inputval[1] + "'"
        def getStringLength():
            return "Get the length of the string '" + input+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def getSubString():
            return "Get Substring of the string '"+ input+ "' with index/range '"+ inputval[1]+ "'  and save the value '" + output+ "' in variable '"+ tsp.outputval + "'"
        def getTagValue():
            return "Get Tag Value of XML and save the value '" + output+ "' in '" + tsp.outputval + "'"
        def left():
            return "Perform String operation Left on string '"+ input+ "' with index '"+ inputval[1]+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def mid():
            return "Perform String operation Mid on string '" + input+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def modifyValue():
            return "Modify variable '"+ input + "' value to '"+ inputval[1] + "'"
        def monthAddition():
            return "Add Months '"+ input + "' value to '"+ inputval[1] + "'"
        def mousePress():
            return 'Mouse Pressed'
        def replace():
            return "In string '"+ input + "' replace '"+ inputval[1] + "' with '"+ inputval[2]+ "' and save the updated input string '" + output+ "' in '" + tsp.outputval + "'"
        def replaceContent():
            return "Replace '"+ input + "' in the '"+ inputval[1] + " with the "+ inputval[2]
        def right():
            return "Perform String operation right on string '"+ input+ "' with index '"+ inputval[1]+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def runQuery():
            return "Execute SQL Query '"+ inputval[5]+" and save resultset in " + output
        def secureExportData():
            return "Execute SQL Query '"+ inputval[5]+" and save resultset in " + output
        def secureGetData():
            return "Execute SQL Query '"+ inputval[5]+" and save resultset in " + output
        def secureRunQuery():
            return "Execute SQL Query '"+ inputval[5]+" and save resultset in " + output
        def secureVerifyData():
            return "Verify SQL Query '"+ inputval[5]+ "' and result is same as '"+ inputval[7] + ","+ inputval[8] + "'"
        def sendFunctionKeys():
            return "Execute Function key  "+ input
        def split():
            return "Split the string '"+ input+ "' with split character '"+ inputval[1]+ "' and save the value:"+ inputval[2] + " in '"+ tsp.outputval + "'"
        def stop():
            return "Stop the Execution"
        def stringGeneration():
            return "Generate a charecter string having a length '"+ input + "'."
        def toLowerCase():
            return ' Change ' + input+ ' to Lower case and save the value ' + output+ ' in ' + tsp.outputval
        def toUpperCase():
            return ' Change ' + input+ ' to Upper case and save the value ' + output+ ' in ' + tsp.outputval
        def trim():
            return ' Trim ' + input+ ' and save the value ' + output + ' in '+ tsp.outputval
        def verifyContent():
            return "Verify '"+ inputval[1]+ "' is present in the file '" + input + "'"
        def verifyData():
            return "Verify SQL Query '"+ inputval[5]+ "' and result is same as '"+ inputval[7] + ","+ inputval[8] + "'"
        def verifyFileImages():
            return "Compare images '" + input+ "' and '" + inputval[1]+ "'"
        def wait():
            return 'Wait for ' + input+ ' Second(s)'
        def writeToFile():
            return "Write '"+ inputval[1] + "' to file  '" + input + "'"
        def yearAddition():
            return "Add Years '"+ input + "' value to '"+ inputval[1] + "'"
        return locals()[keyword]()


    def webservices(self,keyword,tsp,inputval,input,output,con,reporting_obj):

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
            return 'Add the certificate present in the '+ inputval[0]+ ' to the '+ inputval[1] + '.'
        def getServerCertificate():
            return 'Fetch the Server certificate and save it in '+ inputval[1] + '.'
        def executeRequest():
            return 'Execute the request.'
        return locals()[key](keyword)

    def sap(self,keyword,tsp,inputval,input,output,con,reporting_obj):
        print 'keyword',keyword
        #Launch keywords
        def LaunchApplication():
            return ' The application present in the path '+ inputval[0]+ ' is launched'+ '.'
        def GetPageTitle():
            return ' The page title is '+ output +' and  is saved  in the variable ' +tsp.outputval+ '.'
        def CloseApplication():
            return ' The application is closed'+ '.'
        def GetErrorMessage():
            return ' Get the error message '+output+'.'
        def GetPageTitle():
            return ' Get page title '+output+'.'
        def StartTransaction():
            return ' Start the transaction with ID'+inputval+'.'
        def ToolBarAction():
            return ' Perform '+inputval+' action from tool bar. '
        def GetPopUpText():
            return ' get Pop-up text and save the text  '+output+'in'+ tsp.outputval+'.'


        #Textbox keywords
        def GetText():
            return 'Get Text From '+ "'" +tsp.custname + "'" + ' and save the text '+ output + ' in ' + tsp.outputval+ '.'
        def SetSecureText():
             return 'Enter secure text ' +inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def ClearText():
             return 'Clear text from the '+ "'" + tsp.custname + "'"+ '.'
        def SetText():
            return 'Enter text '+ inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def VerifyText():
            return 'Verify ' + input + ' is the the text in the '+ "'" + tsp.custname + "'"+ '.'
        def GetTextBoxLength():
            return 'Get length from the '+ "'" + tsp.custname + "'"+ ' and save the length '+output+'in'+tsp.outputval+ '.'
        def VerifyTextBoxLength():
            return 'Verify ' + input + ' is the length of textbox '+ "'" + tsp.custname + "'"+ '.'

        #Button link keywords
        def GetButtonName():
            return ' Get ButtonName From '+ "'" + tsp.custname + "'" + ' and save the text '+ output + ' in ' + tsp.outputval+'.'
        def VerifyButtonName():
            return 'Verify text ' + input + ' is the name of the '+ "'" + tsp.custname + "'"+ '.'
        def UploadFile():
            return 'Upload the file '+ filename + ' present in the path ' + input + '.'

        #Dropdown keywords
        def GetSelected():
            return 'Get Selected value of '+ "'" + tsp.custname + "'"+ ' and save value ' + output + ' in '+ tsp.outputval+ '.'
##        def GetValueByIndex():
##            return 'Get value with index ' + input + ' in the '+ "'" + tsp.custname + "'" + ' and save the value ' + output + ' in '+ tsp.outputval+'.'
        def VerifyValuesExists():
            return 'Verify values ' + input + ' exists in the '+ "'" + tsp.custname + "'"+'.'
        def SelectValueByText():
            return 'Select value by text '+input+' of the '+ 'type '+ "'" + tsp.custname + "'" +' with the element '+input+' present in the table cell '+"'" + tsp.custname + "'"+'-['+ input + ']['+ input +']'+'.'
        def VerifySelectedValue():
            return 'Verify value ' + input + ' are selected in the '+ "'" + tsp.custname + "'"+'.'
        def VerifyAllValues():
            return 'Verify values ' + input + ' are present in the '+ "'" + tsp.custname + "'"+'.'
        def VerifyCount():
            return 'Verify ' + input + ' is the list count of the ' +"'" + tsp.custname + "'"+'.'
##        def SelectValueByIndex():
##            return 'Select the value '+ input+' of the '+"'" + tsp.custname + "'"+' with the index '+input+' present in the table cell  '+"'" + tsp.custname + "'"+'-['+input+']['+input+']'+'.'
        def GetCount():
            return 'Get the count of values in the '+ "'" + tsp.custname + "'"+ ' and save the count ' + output + ' in ' +tsp.outputval+'.'
        #Element Keywords
##        def ClickElement():
##            return 'Click on ' +"'" + tsp.custname + "'"+'.'
        def GetElementText():
            return 'Get the text of the element '+ "'" + tsp.custname + "'"+ ' and save the value  '+ output + ' in '+ tsp.outputval+'.'
        def VerifyElementText():
            return 'Verify the text of the element '+ "'" + tsp.custname + "'"+ ' is the same as input text'+input+' and save the result as  '+ output + ' in '+ tsp.outputval+'.'


        #Radio checkbox keywords
        def SelectRadioButton():
            return 'Select '+ "'" + tsp.custname + "'"+'.'
        def GetStatus():
            return 'Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' + output + ' in '+ tsp.outputval+'.'
        def SelectCheckbox():
            return 'Select '+ "'" + tsp.custname + "'"+'.'
        def UnSelectCheckbox():
            return 'Unselect '+ "'" + tsp.custname + "'"+'.'
        #Table Keywords
        def GetRowCount():
            return 'Get Row count of '+ "'" + tsp.custname + "'"+ ' and save value ' + output + ' in '+ tsp.outputval+ '.'
        def GetColumnCount():
            return 'Get Column Count of ' + "'" + tsp.custname + "'" + ' and save the value ' + output + ' in '+ tsp.outputval+'.'
        def GetColNumByText():
            return 'Get column number of ' + "'" + tsp.custname + "'" + ' by text '+input +' and save the column number ' + output + ' in '+ tsp.outputval
        def GetRowNumByText():
            return 'Get row number of ' + "'" + tsp.custname + "'" + ' by text '+input +' and save the row number ' + output + ' in '+ tsp.outputval
        def GetCellValue():
            return 'Get Cell value of  '+ "'" + tsp.custname + "'" ' by row, column '+input +  ' and save it in outputs as  '+ output + " in " + tsp.custname +'.'
        def VerifyCellValue():
            return 'Verify cell value of element in row number ' + input[0] +' and column number '+input[1] +' against the input value '+input[2]+' present in ' +"'" + tsp.custname + "'"+'.'
        def VerifyTextExists():
            return 'Verify Text '+ input[2]+' exists in row number '+input[0]+' and column number '+input[1]+' of '+"'" + tsp.custname + "'"+'.'
##        def CellClick():
##            return 'Click on '+ "'" + tsp.custname + "'"+'.'
        def SelectValueByIndex():
            return 'Select the value '+ input+' of the '+"'" + tsp.custname + "'"+' with the index '+input+' present in the table cell  '+"'" + tsp.custname + "'"+'-['+input+']['+input+']'
        def SelectValueByText():
            return 'Select the value '+ input+' of the '+"'" + tsp.custname + "'"+' with the Text '+input+' present in the table cell  '+"'" + tsp.custname + "'"+'-['+input+']['+input+']'
        def GetSelected():
            return 'Get Selected value of '+ "'" + tsp.custname + "'"+ ' and save value ' + output + ' in '+"'"+ tsp.custname + "'"+'.'
##        def GetTableStatus():
##            return 'Select value by text '+input+' of the '+ 'type '+ "'" + tsp.custname + "'" +' with the element '+input+' present in the table cell '+"'" + tsp.custname + "'"+'-['+ input + ']['+ input +']'+'.'
##        def GetCellToolTip():
##            return 'Get CellToolTip of  ' + input + ' and save the result as  '+output+' in ' + "'" + tsp.custname + "'"+'.'
##        def TableCellClick():
##            return 'Click on table cell ' + input + ' in '+ "'" + tsp.custname + "'"+'.'
##        def TableCellDoubleClick():
##            return 'Double click on cell ' + input + ' in ' +"'" + tsp.custname + "'"+'.'
        def SelectRow():
            return 'Select the row '+ input+' in '+"'" + tsp.custname + "'"+'.'
        def UnSelectRow():
            return 'Unselect the row  '+input+' of '+ "'" + tsp.custname + "'"+ '.'
        def GetStatus():
            return 'Get Status of '

        return locals()[keyword]()

        #SAP gerenal keywords
        def Click():
            return 'Click on '+ "'" +tsp.custname+ "'" +'.'
        def DoubleClick():
            return 'Double click on '+ "'" +tsp.custname+ "'" +'.'
        def MouseHover():
            return 'Mouse hovered over  ' + "'" + tsp.custname + "'"+'.'
        def GetToolTipText():
            return 'Get the tool tip  of '+ "'" +tsp.custname+ "'" +'.'
        def VerifyToolTipText():
            return 'Verify ' + input + ' is the tooltip of  '+ "'" + tsp.custname + "'"
        def SetFocus():
            return ' Set focus on '+ "'" + tsp.custname + "'"+'.'

        #Saputil keywords
        def VerifyEnabled():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is enabled '+'.'
        def VerifyDisabled():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is disabled '+'.'
        def verifyExists():
            return ' Verify '+ "'" + tsp.custname + "'" + '  exists '+'.'

        #Scroll Keywords
        def scrollDown():
            return ' Scroll down by'+inputval+' units and store the output as '+output+'.'
        def scrollLeft():
            return ' Scroll left by'+inputval+' units and store the output as '+output+'.'
        def scrollRight():
            return ' Scroll right by'+inputval+' units and store the output as '+output+'.'
        def scrollUp():
            return ' Scroll up by'+inputval+' units and store the output as '+output+'.'
        #Tab Keywords
        def moveTabs():
            return ' Move tab '+ "'" + tsp.custname + "'"+'to left and store the output as '+output+'.'


    def desktop(self,keyword,tsp,inputval,input,output,con,reporting_obj):
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

        #Tab control keywords
        def VerifySelectedTab():
            return 'Verify the selected value from the ' + "'" + tsp.custname + "'"+ ' with the '+ input
        def GetSelectedTab():
            return 'Get selected value from the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output+ ' in '+ tsp.outputval
        def SelectTabByText():
            return 'Select value by text '+input+' of the '+ 'type '+ "'" + tsp.custname
        def SelectTabByIndex():
            return 'Select value by index '+input+' of the '+ 'type '+ "'" + tsp.custname

        #Radio checkbox keywords
        def SelectRadioButton():
            return 'Select '+ "'" + tsp.custname + "'"
        def GetStatus():
            return 'Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' + output + ' in '+ tsp.outputval + ')'

        #Application keywords
        def LaunchApplication():
            return ' The application present in the path  '+ inputval[0]+ 'is launched'
        def GetPageTitle():
            return ' Get the title of Application and  save the title in ' +tsp.outputval
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

    def mobileapp(self,keyword,tsp,inputval,input,output,con,reporting_obj):
        #dropdown keywords



        def getValueByIndex():
            return 'Get value with index ' + input + ' in the '+ "'" + tsp.custname + "'" + ' and save the value ' + output + ' in '+ tsp.outputval,

        def selectValueByText():
            return 'Select value by text '+input+' of the '+ 'type '+ "'" + tsp.custname + "'" +' with the element '+input+' present in the table cell '+"'" + tsp.custname + "'"+'-['+ input + ']['+ input +']',
        def getMultipleValuesByIndexes():
            return 'Get values with indexes ' + inputValsb.toString() + ' in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + TestAutomationController.multipleOutputResult + ' in  '+ tsp.outputval

        def getAllValues():
            return 'getAllValues ' + output + ' are present in the' + "'" + tsp.custname + "'"
        def verifyAllValues():
            return 'Verify values ' + input + ' are present in the '+ "'" + tsp.custname + "'"


        def verifyCount():
            return 'Verify ' + input + ' is the list count of the ' +"'" + tsp.custname + "'"

        def selectValueByIndex():
            return 'Select the value '+ input+' of the '+"'" + tsp.custname + "'"+' with the index '+input+' present in the table cell  '+"'" + tsp.custname + "'"+'-['+input+']['+input+']'
        def getCount():
            return 'Get the count of values in the '+ "'" + tsp.custname + "'"+ ' and save the count ' + output + ' in ' +tsp.outputval

        #text box
        return locals()[keyword]()

    def web(self,keyword,tsp,inputval,input,output,con,reporting_obj):

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
            return 'Enter secure text ' +inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"
        def sendSecureValue():
            return 'Enter secure value ' +inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"



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
        def verifySelectedValue():
            return 'Verify value ' + input + ' are selected in the '+ "'" + tsp.custname + "'"
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
            return 'Verify ' + input + ' exist and Number of occurance of the text ' + input + ' is'+ tsp.outputval +' time(s).'
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

