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
import logger
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
        def createFile():
            print inputval
            return 'Create a file: '+ inputval[1] + ' in the path: ' + inputval[0]
        def verifyFileExists():
            return 'Verify '+ inputval[1] + ' file exists in the path: ' + inputval[0]
        def deleteFile():
            return 'delete: ' + inputval[1] + ' file from the path: ' + inputval[0]
        def renameFile():
            return 'rename filename ' + inputval[1] +' to '+ inputval[2]+ ' in the path '+ inputval[0]
        def savefile():
            return 'Save File: '+ inputval[1] + 'and stored in: '+ inputval[0]


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

        #Folder operations
        def createFolder():
            print inputval
            return 'Create a folder: '+ inputval[1] + ' in the path: ' + inputval[0]
        def verifyFolderExists():
            return 'Verify '+ inputval[1] + ' folder exists in the path: ' + inputval[0]
        def deleteFolder():
            return 'delete: ' + inputval[1] + ' folder from the path: ' + inputval[0]
        def renameFolder():
            return 'rename folder ' + inputval[1] +' to '+ inputval[2]+ ' in the path '+ inputval[0]

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
##            String path = testStepProperty.getInputVal().get(0).trim();
##            if (UtilKeyword.checkforDynamicVariables(path)) {
##                path = UtilKeyword.dynamicVarGeneration(path, null);
##            }
##            String fileName = testStepProperty.getInputVal().get(1).trim();
##            if (UtilKeyword.checkforDynamicVariables(fileName)) {
##                fileName = UtilKeyword.dynamicVarGeneration(fileName, null);
##            }
##            String extension = FilenameUtils.getExtension(path + fileName);
##
##            if (extension.equalsIgnoreCase(TestAutomationConstants.FILE_TYPE_TEXT) || extension.equals(TestAutomationConstants.FILE_TYPE_XML)) {
##                testDesicriptionDirectory.put("clearFileContent", "Clear all the content of the file '"
##                        + fileName + "' present in the path  '" + path + "'");
##            }  else if (extension.equals(TestAutomationConstants.FILE_TYPE_XLS) || extension.equals(TestAutomationConstants.FILE_TYPE_XLSX)) {
##                if(testStepProperty.getInputVal().size() == 3){
##                 String sheetName = testStepProperty.getInputVal().get(2).trim();
##                    if (UtilKeyword.checkforDynamicVariables(sheetName)) {
##                        sheetName = UtilKeyword.dynamicVarGeneration(
##                                sheetName, null);
##                    }
##                testDesicriptionDirectory.put("clearFileContent", "Clear all the content of the file '"
##                        + fileName + "','" + sheetName + "' present in the path  '" + path + "'");
##                }else{
##                    testDesicriptionDirectory.put("clearFileContent", "ClearFileContent failed - SheetName is missing");
##                }
##            }else{
##                testDesicriptionDirectory.put("clearFileContent", "ClearFileContent failed - File type is Invalid ");
##            }
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
            return "Compare '" + inputval[1]+ "' and '" + inputval[0] + "'."
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
            if '@' in output:
                row,col=output.split('@')
                return "The index count for the dynamic variable "+ inputval[0] + " is " + "Row: "+str(row) + " and Column: "+str(col)
            else:
                return "The index count for the dynamic variable "+ inputval[0] + " is " + output
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
            return "Press "+ input +" Key"
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

    def oebs(self,keyword,tsp,inputval,input,output,con,reporting_obj):
        def LaunchApplication():
            return 'The application present in the path'+ inputval[0] + 'is launched'
        def FindWindowAndAttach():
            return 'Find window and attach is executed'
        def CloseApplication():
            return 'The application is closed'
        def SwitchToFrame():
            return 'Control switched to Frame():'+ input
        def setFocus():
            return 'Set focus on'+ "'" + tsp.custname + "'"
        def waitForElementVisible():
            return 'Wait until the element'  + "'" + tsp.custname + "'"+  'is visible'
        def verifyHidden():
            return 'Verify' + tsp.custname +  'is hidden'
        def verifyDisabled():
            return 'Verify' + "'" + tsp.custname + "'" +  'is disabled'
        def verifyEnabled():
            return 'Verify' + "'" + tsp.custname + "'" +  'is enabled'
        def verifyVisible():
            return 'Verify' + "'" + tsp.custname + "'" +  'is visible'
        def verifyReadOnly():
            return 'Verify' + "'" + tsp.custname + "'" +  'is read-only'
        def verifyToolTipText():
            return 'Verify' + input + ' is the tooltip of '+ "'" + tsp.custname + "'"
        def getToolTipText():
            return 'Get the tool tip from the ' + "'" + tsp.custname + "'" + ' and save the tool tip text \'' + output + '\' in ' + tsp.output
        def verifyExists():
            return 'Verify ' + "'" + tsp.custname + "'" + ' exists'
        def verifyDoesNotExists():
            return 'Verify ' + "'" + tsp.custname + "'" + ' does not exists'
        def rightClick():
            return 'Perform right click on element' + "'" + tsp.custname + "'"
        def drag():
            return 'Perform drag on element' + "'" + tsp.custname + "'"
        def drop():
            return'Perform drop on element' + "'" + tsp.custname + "'"
        def setText():
            return 'Enter text ' + input + ' in the '+ "'" + tsp.custname + "'"
        def getText():
            return 'Get text from the ' + "'" + tsp.custname + "'" + ' and save the text \'' + output + '\' in ' + tsp.outputval
        def getTextboxLength():
            return 'Get length from the ' + "'" + tsp.custname + "'" + ' and save the length \'' + output + '\' in ' + tsp.outputval
        def verifyTextboxLength():
            return 'Verify ' + input + ' is the length of textbox ' + "'" + tsp.custname + "'"
        def verifyText():
            return 'Verify ' + input + ' is the text in the ' + "'" + tsp.custname + "'"
        def clearText():
            return 'Clear text from the ' + "'" + tsp.custname + "'"
        def click():
            return 'Click on the ' + "'" + tsp.custname + "'"
        def doubleClick():
            return 'DoubleClick on the ' + "'" + tsp.custname + "'"
        def verifyButtonName():
            return 'Verify ' + input +  'is the name of ' + "'" + tsp.custname + "'"
        def getButtonName():
            return 'Get the name of the ' + "'" + tsp.custname + "'" + 'and save the +output+ in ' + tsp.outputval
        def getLinkText():
            return 'Get Text From ' + "'" + tsp.custname + "'" + ' and save the text \'' + output + '\' in ' + tsp.outputval
        def verifyLinkText():
            return 'Verify text ' + input + ' is the name of the ' + "'" + tsp.custname + "'"
        def selectRadioButton():
            return 'Select ' + "'" + tsp.custname + "'"
        def getStatus():
            return 'Get the status of the ' + "'" + tsp.custname + "'" + ' and save the status \'' + output + '\' in ' + tsp.outputval
        def selectCheckbox():
            return 'Select ' + "'" + tsp.custname + "'"
        def unselectCheckbox():
            return 'Unselect '+ "'" + tsp.custname + "'"
        def selectValueByIndex():
            return 'Select value with index value ' + input + ' in the ' + "'" + tsp.custname + "'"
        def getCount():
            return'Get the count of values in the ' + "'" + tsp.custname + "'" + ' and save the count \'' + output + '\' in ' + tsp.outputval
        def selectValueByText():
            return 'Select value ' + input + ' in the ' + "'" + tsp.custname + "'"
        def verifySelectedValue():
            return 'Verify value ' + input + ' is selected in the ' + "'" + tsp.custname + "'"
        def verifyCount():
            return 'Verify ' + input + ' is the count of the ' + "'" + tsp.custname + "'"
        def verifyAllValues():
            return 'Verify values ' + input + ' are present in the ' + "'" + tsp.custname + "'"
        def verifySelectedValues():
            return 'Verify values ' + input + ' are selected in the ' + "'" + tsp.custname + "'"
        def getSelected():
            return 'Get Selected value of '+  "'" + tsp.custname + "'" + ' and save value \'' + output + '\' in '+ tsp.outputval
        def verifyValuesExists():
            return 'Verify values ' + input + ' exists in the '+  "'" + tsp.custname + "'"
        def getValueByIndex():
            return 'Get value with index ' + input + ' in the '     + "'" + tsp.custname + "'" + ' and save the value \'' + output + '\' in ' + tsp.outputval
        def selectMultipleValuesByIndexes():
            return 'Select values with index values ' + input + ' in the '+ "'" + "'" + tsp.custname + "'" + "'"
        def selectMultipleValuesByText():
            return 'Select values ' + input + ' in the '+ "'" + "'" + tsp.custname + "'" + "'"
        def getMultipleValuesByIndexes():
            return 'Get values with indexes ' + input + ' in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output + ' in  '+ tsp.outputval
        def selectAllValues():
            return 'Select all values in the ' + "'" + tsp.custname + "'"
        def deselectAll():
            return'Deselect all values in the ' + "'" + tsp.custname + "'"
        def getRowCount():
            return 'Get row count of the ' + "'" + tsp.custname  + "'" + ' and save the count \'' + output + '\' in ' + tsp.outputval
        def getColumnCount():
            return'Get column count of the ' + "'" + tsp.custname + "'" + ' and save the count \'' + output + '\' in ' + tsp.outputval
        def getCellValue():
            f_input = input.split(',')
            return 'Get cell value of '+ "'" + tsp.custname + '['+f_input[0] +']['+ f_input[1] + "]'" + ' in the table and save the value ' + output + ' in ' + tsp.outputval
        def verifyCellValue():
            f_input = input.split(',')
            return 'Verify cell value ' + f_input[2] + ' is present in the ' + "'" + tsp.custname + '['+f_input[0] +']['+ f_input[1] + "]'" +  '  table'
        def cellClick():
            f_input = input.split(',')
            return 'Click ' + "'" + tsp.custname + '['+f_input[0] +']['+ f_input[1] + "]'"
        def clickElement():
            return 'Click ' + "'" + tsp.custname + "'"
        def getElementText():
            return'Get the text of the element ' + "'" + tsp.custname + "'" + ' and save the value  \'' + output + '\' in ' + tsp.outputval
        def verifyElementText():
            return 'Verify ' + input + ' is the the text of the ' + "'" + tsp.custname + "'"
        def sendFunctionKeys():
            return 'Press ' + tsp.inputval[0] + ' key'
        def right():
            return 'Right button clicked ' + input + ' times'
        def left():
            return 'Left button clicked ' + input + ' times'
        def up():
            return 'Up button clicked ' + input + ' times'
        def down():
            return 'Down button clicked ' + input + ' times'
        def closeFrame():
            return 'Close frame ' + "'" + tsp.custname + "'"
        def toggleMaximize():
            return 'Perform toggle maximize operation on ' + "'" + tsp.custname + "'"
        def toggleMinimize():
            return 'Perform toggle minimize operation on ' + "'" + tsp.custname + "'"
        return locals()[keyword]()

    def sap(self,keyword,tsp,inputval,input,output,con,reporting_obj):
        #-----------------------------------Added this step as input was returned as a string
        if type(input) is str:                  #----checking if input is a string
            if "," in input:                    #----checking if the string has a ","
                input = input.split(",")        #--------spliting the input by checking for "," then store the result in list input
        #-----------------------------------------if  more than one dynamic variable is given as output , considers only the first one
        try:
            if len(tsp.outputval)>0:
                if(";" in tsp.outputval):
                    i = tsp.outputval.index(";")
                    tsp.outputval=tsp.outputval[:i]
                if("," in output):
                    ni = output.index(',')
                    output =output[:ni]
        except:
            pass
        #-----------------------------------------
        #Launch keywords
        def LaunchApplication():
            return ' The application present in the path '+"'"+ inputval[0]+"'"+ ' is launched'+ '.'
        def GetPageTitle():
            return ' The page title is '+"'"+output +"'"+' and  is saved  in the variable ' +"'"+tsp.outputval+"'"+ '.'
        def CloseApplication():
            return ' The application is closed'+ '.'
        def GetErrorMessage():
            return ' Get the error message '+"'"+output+"'"+'.'
        def StartTransaction():
            return ' Start the transaction with ID'+"'"+inputval+"'"+'.'
        def ToolBarAction():
            return ' Perform '+"'"+inputval+"'"+' action from tool bar. '
        def GetPopUpText():
            return ' Get pop-up text and save the text '+"'"+output+"'"+' in '+"'"+ tsp.outputval+"'"+'.'
        def ServerConnect():
            return ' Connect to SAP server '+"'"+inputval+"'"+'.'


        #Textbox keywords
        def GetText():
            return ' Get Text From '+ "'" +tsp.custname + "'" + ' and save the text '+"'"+ output + "'"+' in ' +"'"+ tsp.outputval+"'"+ '.'
        def SetSecureText():
            return ' Enter secure text ' +"'"+inputval[0]+"'"+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def ClearText():
            return ' Clear text from the '+ "'" + tsp.custname + "'"+ '.'
        def SetText():
            return ' Enter text '+"'"+ inputval[0]+"'"+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def VerifyText():
            return ' Verify ' + "'"+input + "'"+' is the text in the '+ "'" + tsp.custname + "'"+ '.'
        def GetTextBoxLength():
            return ' Get length from the '+ "'" + tsp.custname + "'"+ ' and save the length '+ "'"+output+ "'"+' in '+"'"+tsp.outputval+"'"+ '.'
        def VerifyTextBoxLength():
            return ' Verify ' +"'"+ input +"'"+' is the length of textbox '+ "'" + tsp.custname + "'"+ '.'

        #Button link keywords
        def GetButtonName():
            return ' Get ButtonName From '+ "'" + tsp.custname + "'" + ' and save the text '+"'"+ output + "'"+' in ' +"'"+ tsp.outputval+"'"+'.'
        def VerifyButtonName():
            return ' Verify text ' +"'"+input+"'"+ ' is the name of the '+ "'"+tsp.custname+"'"+'.'
        def UploadFile():
            return ' Upload the file present in the path ' + "'"+input +"'"+ '.'

        #Dropdown keywords
        def GetSelected():
            return ' Get Selected value of '+ "'" + tsp.custname + "'"+ ' and save value ' +"'"+ output +"'"+ ' in '+"'"+ tsp.outputval+"'"+ '.'
##        def GetValueByIndex():
##            return 'Get value with index ' + input + ' in the '+ "'" + tsp.custname + "'" + ' and save the value ' + output + ' in '+ tsp.outputval+'.'
        def VerifyValuesExists():
            return ' Verify values ' +"'"+ input +"'"+ ' exists in the '+ "'" + tsp.custname + "'"+'.'
        def SelectValueByText():
            return ' Select value by text '+"'"+input+"'"+' in '+ "'" + tsp.custname + "'"+'.'
        def VerifySelectedValue():
            return ' Verify value ' +"'"+ input +"'"+ ' are selected in the '+ "'" + tsp.custname + "'"+'.'
        def VerifyAllValues():
            return ' Verify values ' +"'"+ input +"'"+ ' are present in the '+ "'" + tsp.custname + "'"+'.'
        def VerifyCount():
            return ' Verify ' +"'"+ input +"'"+ ' is the list count of the ' +"'" + tsp.custname + "'"
##        def SelectValueByIndex():
##            return ' Select value with index value '+ input+' in the '+"'" + tsp.custname + "'"
        def GetCount():
            return ' Get the count of values in the '+ "'" + tsp.custname + "'"+ ' and save the count ' +"'"+output+"'"+ ' in ' +"'"+tsp.outputval+"'"+'.'
        #Element Keywords
##        def ClickElement():
##            return 'Click on ' +"'" + tsp.custname + "'"+'.'
        def GetElementText():
            return ' Get the text of the element '+ "'" + tsp.custname + "'"+ ' and save the value  '+"'"+output +"'"+ ' in '+"'"+ tsp.outputval+"'"+'.'
        def VerifyElementText():
            return ' Verify '+ "'" + input + "'"+ ' is the text of '+"'" + tsp.custname + "'"+'.'

        #Radio checkbox keywords
        def SelectRadioButton():
            return ' Select '+ "'" + tsp.custname + "'"+'.'
        def GetStatus():
            return ' Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' + "'"+output +"'"+ ' in '+"'"+ tsp.outputval+"'"+'.'
        def SelectCheckbox():
            return ' Select '+ "'" + tsp.custname + "'"+'.'
        def UnSelectCheckbox():
            return ' Unselect '+ "'" + tsp.custname + "'"+'.'
        #Table Keywords
        def GetRowCount():
            return ' Get row count of '+ "'" + tsp.custname + "'"+ ' and save the count '+"'"+output+"'"+ ' in '+"'"+ tsp.outputval+"'"+ '.'
        def GetColumnCount():
            return ' Get column Count of ' + "'" + tsp.custname + "'" + ' and save the count ' + "'"+output+"'" + ' in '+"'"+ tsp.outputval+"'"+'.'
        def GetColNumByText():
            return ' Get column number of ' + "'" + tsp.custname + "'" + ' by text '+"'" +input +"'" +' and save the column number ' +"'"+ output +"'"+ ' in '+"'"+ tsp.outputval+"'"+'.'
        def GetRowNumByText():
            return ' Get row number of ' + "'" + tsp.custname + "'" + ' by text '+"'" +input +"'" +' and save the row number ' + "'"+ output +"'" + ' in '+ tsp.outputval+"'"+'.'
        def GetCellValue():
            return ' Get cell value of  '+ "'" + tsp.custname +input + "'" +'in the table and save the value '+"'"+ output +"'"+ " in " +"'"+ tsp.custname +"'"+'.'
        def VerifyCellValue():
            return ' Verify cell value of element in row number ' +"'"+ input[0] +"'"+' and column number '+"'"+input[1] +"'"+' against the input value '+"'"+input[2]+"'"+' present in ' +"'" + tsp.custname + "'"+'.'
        def VerifyTextExists():
            return ' Verify text '+ "'"+input+"'"+' exists in table '+"'"+ tsp.custname +"'"+"and  save the result as "+"'"+ output +"'"+ ' in '+"'"+ tsp.outputval+"'"+'.'
##        def CellClick():
##            return 'Click on '+ "'" + tsp.custname + "'"+'.'
##        def SelectValueByIndex():
##            return ' Select the value with index '+ input+' in the '+"'" + tsp.custname + "'"
##        def SelectValueByText():
##            return 'Select the value '+"'"+input+"'"+' of the '+"'" + tsp.custname + "'"+' with the text '+"'"+input+"'"+' present in the table cell  '+"'" + tsp.custname + "'"+'-['+input+']['+input+']'
        def GetSelected():
            return ' Get Selected value of '+ "'" + tsp.custname + "'"+ ' and save value ' +"'"+ output +"'"+ ' in '+"'"+ tsp.outputval + "'"+'.'
##        def GetTableStatus():
##            return 'Select value by text '+input+' of the '+ 'type '+ "'" + tsp.custname + "'" +' with the element '+input+' present in the table cell '+"'" + tsp.custname + "'"+'-['+ input + ']['+ input +']'+'.'
##        def GetCellToolTip():
##            return 'Get CellToolTip of  ' + input + ' and save the result as  '+output+' in ' + "'" + tsp.custname + "'"+'.'
##        def TableCellClick():
##            return 'Click on table cell ' + input + ' in '+ "'" + tsp.custname + "'"+'.'
##        def TableCellDoubleClick():
##            return 'Double click on cell ' + input + ' in ' +"'" + tsp.custname + "'"+'.'
        def SelectRow():
            return ' Select the row '+"'" + input+"'" +' in '+"'" + tsp.custname + "'"+'.'
        def UnSelectRow():
            return ' Unselect the row  '+"'" +input+"'" +' of '+ "'" + tsp.custname + "'"+ '.'
##        def GetStatus():
##            return 'Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' + "'" +output +"'" + ' in '+ tsp.outputval

        #SAP gerenal keywords
        def Click():
            return ' Click on the '+ "'" +tsp.custname+ "'" +'.'
        def DoubleClick():
            return ' Double click on the '+ "'" +tsp.custname+ "'" +'.'
        def MouseHover():
            return ' Move mouse pointer to ' + "'" + tsp.custname + "'"+'.'
##        def GetToolTipText():
##            return 'Get the tool tip  of '+ "'" +tsp.custname+ "'" +'.'
##        def VerifyToolTipText():
##            return 'Verify ' + input + ' is the tooltip of  '+ "'" + tsp.custname + "'"
        def SetFocus():
            return ' Set the focus on '+ "'" + tsp.custname + "'"+'.'

        #Saputil keywords
        def VerifyEnabled():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is enabled '+'.'
        def VerifyDisabled():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is disabled '+'.'
        def verifyExists():
            return ' Verify '+ "'" + tsp.custname + "'" + '  exists '+'.'

        #Scroll Keywords
        def scrollDown():
            return ' Scroll down by '+ "'"+inputval+"'"+' units and store the output as '+"'"+output+"'"+'.'
        def scrollLeft():
            return ' Scroll left by '+"'"+inputval+"'"+' units and store the output as '+"'"+output+"'"+'.'
        def scrollRight():
            return ' Scroll right by '+"'"+inputval+"'"+' units and store the output as '+"'"+output+"'"+'.'
        def scrollUp():
            return ' Scroll up by '+"'"+inputval+"'"+' units and store the output as '+"'"+output+"'"+'.'
        #Tab Keywords
        def moveTabs():
            return ' Move tab '+ "'" + tsp.custname + "'"+'to left and store the output as '+"'"+output+"'"+'.'
        #Shell(Grid) Keywords
        def PressToolbarButton():
            return ' Pressing Toolbar Button '+"'"+input[0]+"' of '"+tsp.custname+"'"+' and store the output as '+"'"+output+"'"+'.'
        def SelectRows():
            return ' Selecting Row/Rows'+"'"+input[0]+"'"+'and store the output as '+"'"+output+"'"+'.'
        def GetCountOfRows():
            return ' Get row count of ' + "'" + tsp.custname + "'" + ' and save the count ' + "'"+output+"'" + ' in '+"'"+ tsp.outputval+"'"+'.'
        def GetCountOfColumns():
            return ' Get column count of ' + "'" + tsp.custname + "'" + ' and save the count ' + "'"+output+"'" + ' in '+"'"+ tsp.outputval+"'"+'.'
        def GetCellText():
            return ' Get cell text of row '+"'"+input[0]+"'"+'and column '+"'"+input[1]+"'"+' and store the output as '+"'"+output+"'" + ' in '+"'"+ tsp.outputval+"'"+'.'
        return locals()[keyword]()


    def desktop(self,keyword,tsp,inputval,input,output,con,reporting_obj):
        #-----------------------------------Added this step as input was returned as a string
        if type(input) is str:                  #----checking if input is a string
            if "," in input:                    #----checking if the string has a ","
                listInput = input.split(",")        #--------spliting the input by checking for "," then store the result in list input
        #-----------------------------------------if  more than one dynamic variable is given as output , considers only the first one
        try:
            if len(tsp.outputval)>0:
                if(";" in tsp.outputval):
                    i = tsp.outputval.index(";")
                    tsp.outputval=tsp.outputval[:i]
                if("," in output):
                    ni = output.index(',')
                    output =output[:ni]
        except:
            pass
        #-----------------------------------------

        #dropdown keywords(14 keywords)
        def DeselectAll():
            return ' Deselect all values in the '+ "'" + tsp.custname + "'."
        def GetValueByIndex():
            return ' Get value with index ' + "'" +input +"'" + ' in the '+ "'" + tsp.custname + "'" + ' and save the value ' +"'" + output +"'" + ' in '+ "'" +tsp.outputval+"'.",
        def VerifyValuesExists():
            return ' Verify values ' + "'" +input +"'" + ' exists in the '+ "'" + tsp.custname + "'."
        def SelectMultipleValuesByText():
            return ' Select values ' +"'" + input + "'" +'in the '+ "'" + tsp.custname + "'."
        def SelectValueByText():
            return ' Select value by text '+"'" +input+"'" +' of the '+ 'type '+ "'" + tsp.custname + "'" +' with the element '+input+' present in the table cell '+"'" + tsp.custname + "'"+'-['+ input + ']['+ input +']',
        def SelectValueByIndex():
            return ' Select value with index '+ "'" +input+"'" +' in the '+"'" + tsp.custname + "'."
        def GetCount():
            return ' Get the count of the values present in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + "'" +output+"'"  + ' in '+ "'" +tsp.outputval+"'.",
        def SelectMultipleValuesByIndexes():
            return ' Select values by index/indexes' + "'" +input +"'" + 'in the '+ "'" + tsp.custname + "'."
        def VerifyCount():
            return ' Verify ' +"'" + input +"'" + ' is the list count of the ' +"'" + tsp.custname + "'."
        def SelectAllValues():
            return ' Select all values in the '+ "'" + tsp.custname + "'."
        def VerifySelectedValue():
            return ' Verify the selected value from the ' + "'" + tsp.custname + "'"+ ' with the '+ "'" +input+"'."
        def GetSelected():
            return ' Get selected value from the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output+ ' in '+ "'" +tsp.outputval+"'."
        def GetMultipleValuesByIndexes():
            return ' Get values with indexes ' + "'" +input + "'" +' in the '+ "'" + tsp.custname + "'" +' and save the value ' +"'" + output+ "'" +' in ' +"'" +tsp.outputval+"'."
        def VerifyAllValues():
            return ' Verify the values from the '+ "'" + tsp.custname + "'" +' with '+ "'" +input+"'."

        #Tab control keywords( 4 keywords)
        def VerifySelectedTab():
            return ' Verify the selected value from the ' + "'" + tsp.custname + "'"+ ' with the '+"'" + input+"'."
        def GetSelectedTab():
            return ' Get selected value from the '+ "'" + tsp.custname + "'"+ ' and save the value ' + "'" +output+"'" + ' in '+ "'" +tsp.outputval+"'."
        def SelectTabByText():
            return ' Select tab by text '+"'" +input+"'" +' in '+ "'" + tsp.custname+"'."
        def SelectTabByIndex():
            return ' Select tab by index '+"'" +input+"'" +' in '+ "'" + tsp.custname+"'."

        #Date control keywords ( 2 keywords)
        def GetDate():
            return ' Get the date from ' + "'" + tsp.custname + "'" + ' and save the date  in ' +"'" + tsp.outputval+"'."
        def SetDate():
            return ' Set the date, with the format  '+"'" + input +"'" + ' in '+"'" + tsp.custname+"'."

        #Radio checkbox keywords ( 5 keywords)
        #common
        def GetStatus():
            return ' Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' + output + ' in '+"'"+ tsp.outputval+"'."
        #radio
        def SelectRadioButton():
            return ' Select '+ "'" + tsp.custname + "'."
        #checkbox
        def SelectCheckbox():
            return ' Select '+ "'" + tsp.custname + "'"+'.'
        def UnSelectCheckbox():
            return ' Unselect '+ "'" + tsp.custname + "'"+'.'

        #Application keywords(@Window keywords- 7 keywords)
        def LaunchApplication():
            return ' The application present in the path  '+ inputval[0]+ 'is launched.'
        def GetPageTitle():
            return ' Get the title of Application and  save the title in ' +tsp.outputval+"."
        def CloseApplication():
            return ' The application is closed.'
        def FindWindowAndAttach():
            return ' Find window and attach is executed.'
        def SelectMenu():
            return " '"+input+"'"+' menu selected.'
        def MaximizeWindow():
            return ' Perform maximize window operation on the window.'
        def MinimizeWindow():
            return ' Perform minimize window operation on the window.'

        #Mail Related keywords(@Email keywords- 8 keywords)
        def GetAttachmentStatus():
            return ' Attachment is '+"'"+output+"'"+' in the email.'
        def GetBody():
            return ' Fetch '+"'"+'Body'+"'"+' from email and save the value in variable '+tsp.outputval+ '.'
        def GetEmail():
            return ' Fetch the email  which is having '+"'"+'From'+"'"+' as '+"'"+listInput[0]+"'"+', '+"'"+'To'+"'" +' as '+"'"+listInput[1]+"'"+' and '+"'"+'Subject'+"'"+ ' as '+"'"+listInput[2]+"'"
        def GetFromMailID():
            return ' Fetch '+"'"+'From Mail ID'+"'"+' from email and save the value in variable '+tsp.outputval+ '.'
        def GetSubject():
            return ' Fetch '+"'"+'Subject'+"'"+' from email and save the value in variable '+tsp.outputval+'.'
        def GetToMailID():
            return ' Fetch '+"'"+'To Mail ID'+"'"+' from email and save the value in variable '+tsp.outputval+'.'
        def SwitchToFolder():
            return ' Switched to folder'+"'"+input+"'."
        def VerifyEmail():
            return ' Verify email from the path '+"'"+input+"'."

        #TextBox keywords( 5 keywords)
        def ClearText():
            return ' Clear text from the '+ "'" + tsp.custname + "'"+ '.'
        def GetText():
            return ' Get Text From '+ "'" +tsp.custname + "'" + ' and save the text '+"'"+ output + "'"+' in ' + tsp.outputval+ '.'
        def SetText():
            return ' Enter text '+"'"+ input+"'"+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def VerifyText():
            return ' Verify ' + "'"+input + "'"+' is the text in the '+ "'" + tsp.custname + "'"+ '.'
        def SetSecureText():
            return ' Enter secure text ' +"'"+input + "'"+ ' in the  ' + "'" + tsp.custname + "'"+ '.'

        #Element keywords(7 keywords)
        def GetElementText():
            return ' Get the value present in ' + "'" + tsp.custname + "'" +' and save the value ' + output + ' in '+ tsp.outputval+"."
        def VerifyElementDoesNotExists():
            return ' Verify '+ "'" + tsp.custname + "'" + ' does not exists. '
        def ClickElement():
            return ' Click on '+"'" + tsp.custname + "'."
        def MouseHover():
            return ' Move mouse pointer to ' + "'" + tsp.custname + "'"+'.'
        def VerifyElementText():
            return ' Verify if the value '+"'"+input+"'"+ ' is the element text of ' + "'" + tsp.custname + "'."
        def VerifyElementExists():
            return ' Verify if the element '+ "'" + tsp.custname + "' exists."
        def Press():
            return ' Press the ' +"'" + tsp.custname + "'"

        #Button Keywords(7 keywords)
        def Click():
            return ' Click on the ' +"'" + tsp.custname + "'."
        def DoubleClick():
            return ' Double click on the '+"'"+tsp.custname + "'."
        def VerifyButtonName():
            return ' Verify button name '+"'"+tsp.custname + "'" +'and save the value ' + output + ' in '+"'" + tsp.outputval+ "'."
        def GetButtonName():
            return ' Get button name '+"'"+tsp.custname + "'" +'and save the value ' + output + ' in '+"'" + tsp.outputval+ "'."
        def RightClick():
            return ' Right click on the '+"'" + tsp.custname + "'."
        #link Keywords(2 keywords but not in use)
        def GetLinkText():
            return ' Get the value present in ' + "'" + tsp.custname + "'" +' and save the value ' + output + ' in '+ tsp.outputval+"."
        def VerifyLinkText():
            return ' Verify if the value is present in ' + "'" + tsp.custname + "'."

        #Util Keywords( 7 keywords)
        def SetFocus():
            return ' Set focus on '+"'"+tsp.custname+"'."
        def VerifyDisabled():
            return ' Verify if '+"'"+tsp.custname+"'."+' is disabled.'
        def VerifyEnabled():
            return ' Verify if '+"'"+tsp.custname+"'."+' is enabled.'
        def VerifyHidden():
            return ' Verify if '+"'"+tsp.custname+"'."+' is hidden.'
        def VerifyVisible():
            return ' Verify if '+"'"+tsp.custname+"'."+' is visible.'
        def VerifyReadOnly():
            return ' Verify if '+"'"+tsp.custname+"'."+' is read only.'
        def verifyExists():
            return ' Verify if '+"'"+tsp.custname+"'."+' is exists.'

        #Tree Keywords(2):
        def GetNodeTextByIndex():
            try:
                input1="->".join(listInput)
            except:
                input1=input
            return 'Get node text from index path '+"'"+input1+"'"+' and save the value '+"'"+output+"'"+" in '"+ tsp.outputval+"'."
        def ClickTreeNode():
            try:
                input1="->".join(listInput)
            except:
                input1=input
            return 'Click on tree node  '+"'"+input1+"'."

        return locals()[keyword]()

    def mobileapp(self,keyword,tsp,inputval,input,output,con,reporting_obj):
        output_list=tsp.outputval
        if len(output_list) > 1 :
            output_list = output_list.split(';')
            output_list=output_list[0]
        else:
            output_list=output_list
        def InstallApplication():
            return 'The application present in the path '+ inputval[0] +  ' is installed'
        def UnInstallApplication():
            return 'The application present in the path '+ inputval[0] +  ' is uninstalled'
        def LaunchApplication():
            return 'The application present in the path '+ inputval[0] +  ' is launched'
        def CloseApplication():
            return 'The application is closed'
        def SwipeUp():
            return 'Performed swipe up operation'
        def VerifyDoesNotExists():
            return ' Verify '+ "'" + tsp.custname + "'" + '  does not exists '
        def SwipeDown():
            return 'Performed swipe down operation'
        def SwipeLeft():
            return 'Performed swipe left operation'
        def HideSoftKeyBoard():
            return 'Performed HideSoftKeyBoard operation'
        def BackPress():
            return 'Performed Back Press operation'
        def SwipeRight():
            return 'Performed swipe right operation'
        def ToggleOn():
            return 'Performed toggle on operation on  ' + "'" + tsp.custname + "'"
        def ToggleOff():
            return 'Performed toggle off operation on  ' + "'" + tsp.custname + "'"
        def InvokeDevice():
            return 'Invoking  ' + "'" + input + "'"
        def GetDevices():
            return 'Get all the connected devices ' + ' and save the result  '+ output + ' in ' + output_list+ '.'
        def PressElement():
            return 'Press ' + "'" + tsp.custname + "'"
        def LongPressElement():
            return 'Long Press ' + "'" + tsp.custname + "'"
        def GetElementText():
            return'Get the text of the element ' + "'" + tsp.custname + "'" + ' and save the value  ' + output + ' in ' + output_list
        def VerifyElementText():
            return 'Verify ' + input + ' is the the text of the ' + "'" + tsp.custname + "'"
        def WaitForElementExists():
            return 'Wait until the element'  + "'" + tsp.custname + "'"+  'is exists'
        def VerifyEnabled():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is enabled '
        def SetDate():
            return 'Set date '+ inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def SetNumber():
            return 'Set number '+ inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def GetTime():
            return 'Get Time From '+ "'" +tsp.custname + "'" + ' and save the time '+ output + ' in ' + output_list+ '.'
        def GetDate():
            return 'Get Date From '+ "'" +tsp.custname + "'" + ' and save the date '+ output + ' in ' + output_list+ '.'
        def SetTime():
            return 'Enter time '+ inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def VerifyElementEnabled():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is enabled '
        def VerifyElementDisabled():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is Disabled '
        def VerifyDisabled():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is disabled '
        def VerifyExists():
            return ' Verify '+ "'" + tsp.custname + "'" + '  exists '
        def VerifyElementExists():
            return ' Verify '+ "'" + tsp.custname + "'" + '  exists '
        def VerifyHidden():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is Hidden '
        def VerifyVisible():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is Visible '
        def GetButtonName():
            return ' Get ButtonName From '+ "'" + tsp.custname + "'" + ' and save the text '+ output + ' in ' + output_list
        def VerifyButtonName():
            return 'Verify text ' + input + ' is the name of the '+ "'" + tsp.custname + "'"
        def Press():
            return 'Press on the '+ "'" + tsp.custname + "'"
        def LongPress():
            return 'Long press on the '+ "'" + tsp.custname + "'"
        #Radio checkbox keywords
        def SelectRadioButton():
            return 'Select '+ "'" + tsp.custname + "'"
        def GetStatus():
            return 'Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' + output + ' in '+ output_list
        def SelectCheckbox():
            return 'Select '+ "'" + tsp.custname + "'"
        def UnSelectCheckbox():
            return 'Unselect '+ "'" + tsp.custname + "'"

        #textbox keywords
        def SendValue():
            return ' Enter value ' + input+ ' in the '+ "'" + tsp.custname + "'"
        def GetText():
            return 'Get Text From '+ "'" +tsp.custname + "'" + ' and save the text '+ output + ' in ' + output_list+ '.'
        def SetSecureText():
             return 'Enter secure text ' +inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def ClearText():
             return 'Clear text from the '+ "'" + tsp.custname + "'"+ '.'
        def SetText():
            return 'Enter text '+ inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def SetMaxValue():
            return 'Set maximum value in seekbar  ' + "'" + tsp.custname + "'"+ '.'
        def SetMidValue():
            return 'Set mid value in seekbar  ' + "'" + tsp.custname + "'"+ '.'
        def SetMinValue():
            return 'Set minimum value in seekbar  ' + "'" + tsp.custname + "'"+ '.'
        def VerifyText():
            return 'Verify ' + input + ' is the the text in the '+ "'" + tsp.custname + "'"+ '.'
        def GetTextboxLength():
            return 'Get length from the '+ "'" + tsp.custname + "'"+ ' and save the length '+output+'in'+output_list+ '.'
        def VerifyTextboxLength():
            return 'Verify ' + input + ' is the length of textbox '+ "'" + tsp.custname + "'"+ '.'

        #dropdown keywords
        def GetValueByIndex():
            return 'Get value with index ' + input + ' in the '+ "'" + tsp.custname + "'" + ' and save the value ' + output + ' in '+ output_list
        def GetSelectedValue():
            return 'Get Selected value of '+ "'" + tsp.custname + "'"+ ' and save value ' + output + ' in '+ output_list+ '.'
        def VerifySelectedValue():
            return 'Verify value ' + input + ' are selected in the '+ "'" + tsp.custname + "'"+'.'
        def SelectValueByText():
            return 'Select value by text '+input+' of the '+ 'type '+ "'" + tsp.custname + "'" +' with the element '+input+' present in the table cell '+"'" + tsp.custname + "'"+'-['+ input + ']['+ input +']'
        def GetMultipleValuesByIndexes():
            return 'Get values with indexes ' + input + ' in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output + ' in  '+ tsp.oututval

        def GetAllValues():
            return 'getAllValues ' + output + ' are present in the' + "'" + tsp.custname + "'"
        def VerifyAllValues():
            return 'Verify values ' + input + ' are present in the '+ "'" + tsp.custname + "'"


        def VerifyCount():
            return 'Verify ' + input + ' is the list count of the ' +"'" + tsp.custname + "'"

        def SelectValueByIndex():
            return ' Select value with index value '+ input+' in the '+"'" + tsp.custname + "'"
        def GetCount():
            return 'Get the count of values in the '+ "'" + tsp.custname + "'"+ ' and save the count ' + output + ' in ' +output_list
        def GetViewByIndex():
            return 'Get View with index ' + input + ' in the '+ "'" + tsp.custname + "'" + ' and save the value ' + output + ' in '+ output_list
        def GetSelectedViews():
            return 'Get Selected value of '+ "'" + tsp.custname + "'"+ ' and save value ' + output + ' in '+output_list+ '.'
        def VerifySelectedViews():
            return 'Verify value ' + input + ' are selected in the '+ "'" + tsp.custname + "'"+'.'
        def SelectViewByText():
            return 'Select value by text '+input+' of the '+ 'type '+ "'" + tsp.custname + "'" +' with the element '+input+' present in the table cell '+"'" + tsp.custname + "'"+'-['+ input + ']['+ input +']'
        def GetMultipleViewsByIndexes():
            return 'Get values with indexes ' + input + ' in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output + ' in  '+ tsp.ouputval

        def GetAllViews():
            return 'getAllValues ' + output + ' are present in the' + "'" + tsp.custname + "'"
        def VerifyAllViews():
            return 'Verify values ' + input + ' are present in the '+ "'" + tsp.custname + "'"
        def SelectMultipleViewsByIndexes():
            return 'Select values ' + input + ' in the '+ "'" + "'" + tsp.custname + "'" + "'"

        def VerifyListCount():
            return 'Verify ' + input + ' is the list count of the ' +"'" + tsp.custname + "'"

        def SelectViewByIndex():
            return 'Select the value '+ input+' of the '+"'" + tsp.custname + "'"+' with the index '+input+' present in the table cell  '+"'" + tsp.custname + "'"+'-['+input+']['+input+']'
        def GetListCount():
            return 'Get the count of values in the '+ "'" + tsp.custname + "'"+ ' and save the count ' + output + ' in ' +output_list
        def SelectMultipleViewsByText():
            return 'Select values ' + input + 'in the '+ "'" + tsp.custname + "'"


        # dropdown keywords
        def GetRowCount():
            return 'Get the count of cells in the table ' + "'" + tsp.custname + "'" + ' and save the count ' + output + ' in ' + output_list

        def VerifyRowCount():
            return 'Verify ' + input + ' is the list count of the ' +"'" + tsp.custname + "'"

        def CellClick():
            return 'Click on the cell number ' + input + ' in the table ' +"'" + tsp.custname + "'"

        def GetCellValue():
            return "Get data from the cell number '" + input+ " in the table '" + tsp.custname + "'" +' and save the value ' + output + ' in ' + output_list

        def VerifyCellValue():
            return "Verify data from the cell number '" + input+ " in the table '" + tsp.custname + "'"


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
        def sendFunctionKeys():
            return 'Press ' + tsp.inputval[0] + ' key'
        #Textbox keywords
        def setText():
            return 'Enter text '+ input+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def clearText():
            return 'Clear text from the ' + "'" + tsp.custname + "'"
        def getText():
            return 'Get text from the ' + "'" + tsp.custname + "'" + ' and save the text \'' + output + '\' in ' + tsp.outputval
        def getTextboxLength():
            return 'Get length from the ' + "'" + tsp.custname + "'" + ' and save the length \'' + output + '\' in ' + tsp.outputval
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
            return 'Select values ' + input + ' in the '+ "'" + tsp.custname + "'"
        def deselectAll():
            return 'Deselect all values in the '+ "'" + tsp.custname + "'"
        def getValueByIndex():
            return 'Get value with index ' + input + ' in the '+ "'" + tsp.custname + "'" + ' and save the value ' + output + ' in '+ tsp.outputval
        def verifyValuesExists():
            return 'Verify values ' + input + ' exists in the '+ "'" + tsp.custname + "'"
        def selectValueByText():
            return 'Select value '+input+' in ' + tsp.custname
        def getMultipleValuesByIndexes():
            return 'Get values with indexes ' + input + ' in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output + ' in  '+ tsp.outputval
        def verifySelectedValue():
            return 'Verify value ' + input + ' are selected in the '+ "'" + tsp.custname + "'"
        def verifySelectedValues():
            return 'Verify values ' + input + ' are selected in the '+ "'" + tsp.custname + "'"
        def getAllValues():
            return 'getAllValues ' + output + ' are present in the' + "'" + tsp.custname + "'"
        def verifyAllValues():
            return 'Verify values ' + input + ' are present in the '+ "'" + tsp.custname + "'"
        def selectMultipleValuesByIndexes():
            return 'Select values with index values ' + input + ' in the '+ "'" + tsp.custname + "'"
        def selectAllValues():
            return 'Select all values in the ' +"'" + tsp.custname + "'"
        def verifyCount():
            return 'Verify ' + input + ' is the list count of the ' +"'" + tsp.custname + "'"
        def verifySelectedValue():
            return 'Verify value ' + input + ' is selected in the ' +"'" + tsp.custname + "'"
        def selectValueByIndex():
            return ' Select value with index value '+ input+' in the '+"'" + tsp.custname + "'"
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
            return ' Open url ' + input  + ' in the browser'
        def navigateBack():
            return 'Navigate back in the browser'
        def verifyTextExists():
            return 'Verify ' + input + ' exist and Number of occurance of the text ' + input + ' is '+ output +' time(s).'
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
            return 'Perform tab on '+ "'" + tsp.custname + "'"

        def rightClick():
            return 'Perform right click on element '+ "'" + tsp.custname + "'"
        def doubleClick():
            return 'Double click on the '+ "'" + tsp.custname + "'"
        def waitForElementVisible():
            return 'Wait until the element '+ "'" + tsp.custname + "'" +'is visible'
        def dropFile():
            return 'Drop file executed'

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
        def selectByAbsoluteValue():
            return 'Select value with exact text'+ "  "+"'" +input + "'"+"  " + ' present in the '+ "'" + tsp.custname + "'"

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

        def getColNumByText():
            return 'Get column number of ' + "'" + tsp.custname + "'" + ' by text '+input +' and save the column number ' + output + ' in '+ tsp.outputval
        def getRowNumByText():
            return 'Get row number of ' + "'" + tsp.custname + "'" + ' by text '+input +' and save the row number ' + output + ' in '+ tsp.outputval
        def getCellValue():
            return 'Get row number of ' + "'" + tsp.custname + "'" + ' by text '+input +' and save the row number ' + output + ' in '+ tsp.outputval

        return locals()[keyword]()
