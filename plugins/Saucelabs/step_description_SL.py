class StepDescription:

    def generic(self,keyword,tsp,inputval,input,output):
        if str(keyword) in ["typecast","split","displayvariablevalue"]:
            if type(output) is list:
                    output=','.join(output)
        #Date operations
        inputval=inputval[0].split(";")
        def getCurrentTime():
            return 'Get current time of the system and save the time '+ "'"+ output + "'"+ ' in '+ "'"+ tsp.outputval+ "'"
        def getCurrentDate():
            return 'Get current date of the system and save the date '+ "'" + str(output)+ "'" + ' in '+ "'"+ tsp.outputval+ "'"
        def getCurrentDateAndTime():
            return 'Get current date time of the system and save the date time '+"'"+ inputval[0] +"' and '"+ inputval[1] + "'"+ ' in '+"'"+ tsp.outputval+"'"
        def getCurrentDay():
            return 'Get current day of the system and save the day '+ "'" + str(output)+ "'" + ' in '+ "'"+ tsp.outputval+ "'"
        def getCurrentDayDateAndTime():
            return 'Get current day date time of the system and save the day date time '+"'"+ str(output) + "'"+ ' in '+"'"+ tsp.outputval+"'"
        def dateAddition():
            return "Add the date '"+ inputval[0] + "' to '"+ inputval[1]+ "' number of days and save the date '" + output + "' in '"+ tsp.outputval+"'"
        def dateCompare():
            return "Compare '" + inputval[1]+ "' and '" + inputval[0] + "'."
        def datedifference():
            return "Get the difference between the dates '"+ inputval[0]+ "' and '"+ inputval[1]+ "' and save the date '" + output+ "' in '"+ tsp.outputval + "'"
        def yearAddition():
            return "Add "+inputval[0] +" years to date '"+inputval[1]+ "' and save the date '"+output+"' in '"+tsp.outputval+ "'"
        def monthAddition():
            return "Add "+inputval[0] +" months to date '"+inputval[1]+ "' and save the date '"+output+"' in '"+tsp.outputval+ "'"
        def changeDateFormat():
            return "Change the format of the date '"+ inputval[0] + "' to format '"+ inputval[1]+ "' and save the date  '" + output + "' in "+"'"+tsp.outputval+"'"

        #File operations
        def createFile():
            return "Create a file: '"+ inputval[1] +"' in the path: '"+ inputval[0]+"'"
        def verifyFileExists():
            return "Verify '"+ inputval[1] +"' file exists in the path: '" + inputval[0]+"'"
        def deleteFile():
            return "delete: '"+ inputval[1] +"' file from the path: '"+ inputval[0]+"'"
        def renameFile():
            return "rename filename '"+ inputval[1] +"' to '"+ inputval[2]+"' in the path '"+ inputval[0]+"'"
        def savefile():
            return "File saved: '"+ inputval[1] +"'and stored in: '"+ inputval[0]+"'"
        def executeFile():
            return "Perform execution of the file'"+ input+"'"
        def verifycontent():
            return "Verify '"+ inputval[1]+"' is present in the file '"+ inputval[0]+"'"
        def getcontent():
            return "Get content from the file '"+ input+"' and save it in '"+ tsp.outputval+"'"
        def comparefiles():
            return "Compared the contents of files '"+ inputval[0] + "' and '"+ inputval[1]+"'"
        def compareinputs():
            return "Compared the inputs '"+ inputval[0] + "' and '"+ inputval[1]+"'"
        def beautify():
            return "Beautified the "+inputval[1]+" input '"+ inputval[0]+"'"
        def getxmlblockdata():
            return "Get the xml block data of file '" + inputval[0] + "'and save the result in '"+ tsp.outputval+"'"
        def selectivexmlfilecompare():
            return "Selectively compare xml block data between file '" + inputval[2] + "' and file '"+ inputval[0]+"'and save the result in '"+ tsp.outputval+"'"
        def compxmlfilewithxmlblock():
            return "Compare xml file '" + inputval[0] + "' with the xml block amd save the result in '"+ tsp.outputval+"'"
        def cellbycellcompare():
            return "Compared cell by cell data between file "+inputval[2]+" and file '"+ inputval[0]+"'"
        def executescript():
            return "Perform execution of the script '"+ input+"'"
        def writetofile():
            return "Write '"+ inputval[1] + "' to file  '" + inputval[0] + "'"
        def verifyfileimages():
            return "Compare images '" + inputval[0]+ "' and '" + inputval[1]+ "'"
        def imagesimilaritypercentage():
            return "Compare images '" + inputval[0]+ "' and '" + inputval[1]+ "'"
        def clearfilecontent():
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

        #Folder operations
        def createFolder():
            return "Create a folder: '"+ inputval[1] + "' in the path: '" + inputval[0]+"'"
        def verifyFolderExists():
            return "Verify '"+ inputval[1] + "' folder exists in the path: '" + inputval[0]+"'"
        def deleteFolder():
            return "Delete: '" + inputval[1] + "' folder from the path: '" + inputval[0]+"'"
        def renameFolder():
            return "Rename folder '" + str(inputval[1]) +"' to '"+ str(inputval[2])+ "' in the path '"+ inputval[0]+"'"

        #Math opeartions
        def add():
            return "Add the numbers '"+ input+"' and save the value '"+output +"' in '"+ tsp.outputval+"'"
        def evaluate():
            return "Evaluate Mathematical expression '"+ input+"' and save the result '"+ output +"' in '"+ tsp.outputval+"'"

        #Compare keywords
        def verifyobjects():
            return "Verify objects '"+ inputval[0] +"' and '"+ inputval[1]+"' and save the result in '"+ tsp.outputval +"'."

        #String operations
        def toLowerCase():
            return 'Change ' +"'"+ input+"'"+ ' to Lower case and save the value ' +"'"+ output+"'"+' in '+"'"+ tsp.outputval+"'"
        ##def evaluate():
            ##return 'Evaluate Mathematical expression ' +"'"+ input+ "'"+' and save the result ' +"'"+ output +"'"+ ' in '+"'"+ tsp.outputval+"'"
        def toUpperCase():
            return 'Change ' +"'"+ input+"'"+ ' to Upper case and save the value ' +"'"+ output+"'"+ ' in ' +"'"+ tsp.outputval+"'"
        def trim():
            return 'Trim ' +"'"+ input+"'"+ ' and save the value ' +"'"+ output +"'"+ ' in '+"'"+ tsp.outputval+"'"
        def typeCast():
            return 'Type cast '+"'"+ str(inputval[0])+"'"+' to '+"'"+ str(inputval[1])+"'"+' and save the value '+"'"+ output+"'"+' in '+"'"+tsp.outputval+"'"
        def split():
            return 'Split the string ' +"'"+ str(inputval[0])+"'"+' with split character '+"'"+str(inputval[1])+"'"+' and save the value: '+"'"+ output+"'"+' in '+"'"+tsp.outputval+"'"
        def right():
            return "Perform String operation RIGHT on string '"+ input+ "' with index '"+ inputval[1]+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def left():
            return "Perform String operation LEFT on string '"+ input+ "' with index '"+ inputval[1]+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def mid():
            return "Perform String operation MID on string '" + input+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def concatenate():
            return "Concatenate string '"+ input + "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def numberformatter():
            return "Format value '"+ input + "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def find():
            return "Verify input string '"+ input + "' contains '"+ inputval[1] + "'"
        def replace():
            return "In string '"+ inputval[0] + "' replace '"+ inputval[1] + "' with '"+ inputval[2]+ "' and save the updated input string '" + output+ "' in '" + tsp.outputval + "'"
        def getStringLength():
            return "Get the length of the string '" + input+ "' and save the length '" + output + "' in '"+ tsp.outputval + "'"
        def getSubString():
            return "Get Substring of the string '"+ inputval[0]+ "' with index/range '"+ inputval[1]+ "'  and save the Substring '" + output+ "' in '"+ tsp.outputval + "'"
        def stringGeneration():
            if input.find("num") != -1:
                return "Generate a number having a length '"+ input + "'."
            else:
                return "Generate a character string having a length '"+ input + "'."

        #Clipboard keywords
        def savetoclipboard():
            return "Save the value '"+input +"' to ClipBoard and store the output '"+ output+ "' in '"+ tsp.outputval + "'."
        def getfromclipboard():
            return "Get data from ClipBoard and save the value '"+ output+ "' in '"+ tsp.outputval + "'."

        #delay keywords
        def wait():
            return "Wait for '" +input+"'  second(s)"
        def pause():
            return 'Pause the application until the user interrupts'

        #Dynamic variable keywords
        def createDynVariable():
            return "Create a variable '"+str(inputval[0])+"' with value '"+ str(inputval[1]) + "'"
        def deleteDynVariable():
            return ("Delete variable "+str(inputval)).replace('[','').replace(']','')
        def displayvariablevalue():
            return output.replace('\n',' ')
        def verifyValues():
            return "Verify values '" + str(inputval[0]) + "' and '" + inputval[1]+ "' and save the result in '"+ tsp.outputval + "'."
        def capturescreenshot():
            return 'Captured Screenshot'
        def comparecontent():
            return "Compare the contents of file '"+ str(inputval[0])+ "' and '"+ str(inputval[1])+ "'"
        def copyValue():
            return "Copy value to variable '"+str(inputval[0])+ "' from variable '"+str(inputval[1])+ "'"
        def getIndexCount():
            if '@' in output:
                row,col=output.split('@')
                return "The index count for the dynamic variable "+ inputval[0] + " is " + "Row: "+str(row) + " and Column: "+str(col)
            else:
                return "The index count for the dynamic variable "+ inputval[0] + " is " + output
        def getlinenumber():
            return "Get the line number of content '"+str(inputval[0])+ "' from file '"+str(inputval[1])+"' and save the value '" + output + "' in "+tsp.outputval
        def getparam():
            return "Get data from file '"+str(inputval[0])+ "' and  sheet '"+str(inputval[1])+ "'"
        def modifyValue():
            return "Modify variable '"+ str(inputval[0]) + "' value to '"+str(inputval[1])+ "'"
        def mousepress():
            return 'Mouse left button pressed'
        def replacecontent():
            return "Replace '"+str(inputval[0]) + "' in the '"+ str(inputval[1])+"' with the '"+str(inputval[2])+"'"
        def sendFunctionKeys():
            return "Press '"+ input +"' Key"
        def stop():
            return "Stop the Execution"

        #Generic-XML
        def getblockcount():
            return "Get the Block Count of XML and save the value '" + output+ "' in '" + tsp.outputval + "'"
        def getblockvalue():
            return 'Get Block Value of XML and save the value '+"'"+ output+"'"+' in '+"'" + tsp.outputval + "'"
        def gettagvalue():
            return "Get Tag Value of XML and save the value '" + output+ "' in '" + tsp.outputval + "'"

        #DB-operations
        def getdata():
            return "Execute SQL Query '"+ inputval[5]+"' and save resultset in '" + tsp.outputval + "'"
        def verifydata():
            return "Verify SQL Query '"+ inputval[5]+ "' and result is same as '"+ inputval[7] + ","+ inputval[8] + "'"
        def exportdata():
            return "Execute SQL Query '"+ inputval[5]+"' and save resultset in '" + tsp.outputval + "'"
        def runquery():
            return "Execute SQL Query '"+ inputval[5]+"' and save resultset in '" + tsp.outputval + "'"
        def secureexportdata():
            return "Execute SQL Query '"+ inputval[5]+"' and save resultset in '" + tsp.outputval + "'"
        def securegetdata():
            return "Execute SQL Query '"+ inputval[5]+"' and save resultset in '" + tsp.outputval + "'"
        def securerunquery():
            return "Execute SQL Query '"+ inputval[5]+"' and save resultset in '" + tsp.outputval + "'"
        def secureverifydata():
            return "Verify SQL Query '"+ inputval[5]+ "' and result is same as '"+ inputval[7] + ","+ inputval[8] + "'"

        #Excel Keywords
        def clearcell():
            return 'clear cell '+"'"+ input+"'"
        def clearexcelpath():
            return 'Clear the saved excel file path'
        def deleterow():
            return 'Delete row '+"'"+ input+"'"
        def getcolumncount():
            return 'Get column count of the '+"'"+tsp.custname+"'"+' and save the count '+"'"+output+"'"+' in '+"'"+tsp.outputval+"'"
        def getrowcount():
            return 'Get row count of the '+"'"+tsp.custname+"'"+' and save the count '+"'"+output+"'"+' in '+"'"+tsp.outputval+"'"
        def readcell():
            return 'Read the content from the cell '+"'"+ input+"'"+' and save the value '+"'"+output+"'"+' in '+"'"+tsp.outputval+"'"
        def setexcelpath():
            return 'Sets the excel file path: '+"'"+ input+"'"+' internally for the excel operations'
        def writetocell():
            return 'Write '+"'"+ str(''.join(inputval[2:]))+"'"+' to cell '+"'"+ inputval[0]+','+ inputval[1]+"'"

        return locals()[keyword]()

    def web(self,keyword,tsp,inputval,input,output):
         #-----------------------------------Added this step as input was returned as a string
        if type(input) is str:                  #----checking if input is a string
            if "," in input:                    #----checking if the string has a ","
                inputL = input.split(",")        #--------spliting the input by checking for "," then store the result in list input
        ##        #-----------------------------------Added this step as input was returned as a string
        ##        if type(input) is str:                  #----checking if input is a string
        ##            if "," in input:                    #----checking if the string has a ","
        ##                input = input.split(",")        #--------spliting the input by checking for "," then store the result in list input
        ##        #-----------------------------------------if  more than one dynamic variable is given as output , considers only the first one
        ##        try:
        ##            if len(tsp.outputval)>0:
        ##                if(";" in tsp.outputval):
        ##                    i = tsp.outputval.index(";")
        ##                    tsp.outputval=tsp.outputval[:i]
        ##                if("," in output):
        ##                    ni = output.index(',')
        ##                    output =output[:ni]
        ##        except:
        ##            pass

        browser={"1":"Chrome","2":"Firefox","3":"Internet Explorer","7":"Edge Legacy","8":"Edge Chromium"}
        if tsp.custname == '@Custom':       # checking if  cust name is @Custom
            if type(input) is str:                  #----checking if input is a string
                if "," in input:                    #----checking if the string has a ","
                    input = input.split(",")
            if type(input) is list:
                if len(input)==4:   #check is it is custom object(as input for custom object consists of 4 parameters)
                    ele_type=input[0]
                    visible_text=input[1]
                    cust_index= input[2]
                    input =input[3]                 #since the last parameter is the input for custom elements
        #-----------------------------------------
        output=str(output)
        if type(input) is list:
            for i in input:
                i=str(i)
        else:
            input=str(input)
        #Popup keywords
        def verifyPopUpText():
            return 'Verify ' +"'"+ input+"'"+ '  is the Popup text '
        def verifydialogtext():
            return 'Verify '+ "'"+input +"'"+ ' is the text of Window Dialog '
        def dismissPopUp():
            return 'Close the Popup'
        def acceptPopUp():
            return 'Accept the Popup'
        def getPopUpText():
            return 'Get the text of the Popup and save the text '+"'" + output+"'"+ ' in ' +"'"+tsp.outputval+"'"
        def sendFunctionKeys():
            return 'Press ' + "'"+input+"'"+ ' key'
        #Textbox keywords
        def setText():
            return 'Enter text '+ "'"+input+"'"+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def clearText():
            return 'Clear text from the ' + "'" + tsp.custname + "'"
        def getText():
            return 'Get text from the ' + "'" + tsp.custname + "'" + ' and save the text ' +"'" + output +"'" +' in ' +"'"+tsp.outputval+"'"
        def getTextboxLength():
            return 'Get length from the ' + "'" + tsp.custname + "'" + ' and save the length '+"'" +output+"'" +' in ' +"'"+tsp.outputval+"'"
        def verifyText():
            return 'Verify ' + "'"+input +"'"+ ' is the the text in the '+ "'" + tsp.custname + "'"
        def sendValue():
            return 'Enter value ' + "'"+input+"'"+' in the '+ "'" + tsp.custname + "'"
        def verifyTextboxLength():
            return 'Verify ' +"'"+ input + "'"+' is the length of textbox '+ "'" + tsp.custname + "'"
        def setSecureText():
            return 'Enter secure text ' +"'"+input+"'"+ ' in the  ' + "'" + tsp.custname + "'"
        def sendSecureValue():
            return 'Enter secure value ' +"'"+input+"'"+ ' in the  ' + "'" + tsp.custname + "'"
        def iossendkey():
            return 'Press '+"'"+input+"'"+" Key"

        #Image keywords
        def verifywebimages():
            return 'Compare images '+ "'" + tsp.custname + "'" + ' and ' +"'"+input+"'"
        def imagesimilaritypercentage():
            return 'Compare images '+ "'" + tsp.custname + "'" + ' and ' +"'"+input+"'"

        #dropdown keywords
        def getSelected():
            return 'Get Selected value of '+ "'" + tsp.custname + "'"+ ' and save the value ' +"'"+output +"'"+' in '+"'"+tsp.outputval+"'"
        def selectMultipleValuesByText():
            return 'Select values ' +"'"+ str(input) +"'"+ ' in the '+ "'" + tsp.custname + "'"
        def deselectAll():
            return 'Deselect all values in the '+ "'" + tsp.custname + "'"
        def getValueByIndex():
            return 'Get value with index ' +"'"+ input +"'"+' in the '+ "'" + tsp.custname + "'" + ' and save the value ' +"'"+output +"'"+' in '+"'"+tsp.outputval+"'"
        def verifyValuesExists():
            return 'Verify values ' +"'"+ input +"'"+ ' exists in the '+ "'" + tsp.custname + "'"
        def selectValueByText():
            if tsp.custname=="@Custom":
                return 'Select text '+"'" +input+"'" +' with visible text '+"'" +visible_text+"'" +' of the type '+"'" +ele_type+"'" +' with the index '+"'" +cust_index+"'" +' present in '+ "'" + tsp.custname + "'"
            else:
                return 'Select value '+"'"+input+"'"+' in ' + tsp.custname
        def getMultipleValuesByIndexes():
            return 'Get values with indexes ' +"'"+ str(input) +"'"+ ' in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output + ' in  '+ tsp.outputval
        def verifySelectedValue():
            return 'Verify value ' +"'"+ input +"'"+ ' is selected in the '+ "'" + tsp.custname + "'"
        def verifySelectedValues():
            return 'Verify values ' +"'"+ input +"'"+ ' are selected in the '+ "'" + tsp.custname + "'"
        def getAllValues():
            return 'Get all the values present in the '+"'"+tsp.custname+"' and save the values '"+ output + ' in ' + "'" + tsp.outputval + "' ."
        def verifyAllValues():
            return 'Verify values ' +"'"+ str(input) +"'"+ ' are present in the '+ "'" + tsp.custname + "'"
        def selectMultipleValuesByIndexes():
            return 'Select values with index values ' +"'"+ str(input) +"'"+ ' in the '+ "'" + tsp.custname + "'"
        def selectAllValues():
            return 'Select all values in the ' +"'" + tsp.custname + "'"
        def verifyCount():
            return 'Verify ' +"'"+ input +"'"+ ' is the list count of the ' +"'" + tsp.custname + "'"
        def selectValueByIndex():
            if tsp.custname=="@Custom":
                return 'Select value '+"'" +input+"'" +' with visible text '+"'" +visible_text+"'" +' of the type '+"'" +ele_type+"'" +' with the index '+"'" +cust_index+"'" +' present in '+ "'" + tsp.custname + "'"
            else:
                return 'Select the value with the index '+input+' in ' + tsp.custname
        def getCount():
            return 'Get the count of values in the '+ "'" + tsp.custname + "'"+ ' and save the count ' +"'"+output+"'"+' in '+"'"+tsp.outputval+"'"
        #Radio checkbox keywords
        def selectRadioButton():
            return 'Select '+ "'" + tsp.custname + "'"
        def getStatus():
            return 'Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' +"'"+output+"'"+' in '+"'"+tsp.outputval+"'"
        def selectCheckbox():
            return 'Select '+ "'" + tsp.custname + "'"
        def unselectCheckbox():
            return 'Unselect '+ "'" + tsp.custname + "'"

        #Browser keywords
        def openBrowser():
            return "Open '"+ browser[inputval[0]]+"' browser"
        def opennewbrowser():
            return 'Open new instance of the browser'
        def maximizeBrowser():
            return 'Maximize the browser ' +"'"+input+"'"
        def closeBrowser():
            return 'Close the browser '
        def navigateToURL():
            return 'Navigate to url ' +"'"+ input+"'"+ ' in the browser'
        def navigateforward():
            return 'Navigate forward in the browser'
        def navigateWithAuthenticate():
            return 'Navigate to url ' +"'"+input[0]+"'"+' with authentication of '+"'"+input[1]+"' in the browser."
        def navigateBack():
            return 'Navigate back in the browser'
        def verifyTextExists():
            return 'Verify ' +"'"+ input + "'"+' exist in the browser and number of occurance of the text ' +"'"+ input + "'"+' is '+"'"+output+"'"+' time(s).'
        def getCurrentURL():
            return 'Get current url of the web page and save the URL '+"'"+output+"'"+' in '+"'"+tsp.outputval+"'"
        def verifyCurrentURL():
            return 'Verify url '+"'"+ input +"'"+ ' is the current url of the web page'
        def verifyPageTitle():
            return 'Verify ' + "'"+input+"'"+ ' is the page title of the web page'
        def getPageTitle():
            return 'Get the title of the web page and save the title '+"'"+output+"'"+' in '+"'"+tsp.outputval+"'"
        def closeSubWindows():
            if input =="All":
                return "Closed All sub windows"
            else:
                return 'Closed the current sub window.'
        def openNewTab():
            return 'Open new tab in the current browser'
        def clearCache():
            return 'Clear the cache of browser'
        def refresh():
            return 'Refresh the web page'
        def getbrowsername():
            return "Get the name of the browser and save the browser name '"+output+"' in '"+tsp.outputval+"'"

        #Element keywords
        def getToolTipText():
            return 'Get the tool tip from the '+ "'" + tsp.custname + "'"+ ' and save the tool tip text ' +"'"+output+"'"+ ' in ' +"'"+tsp.outputval+"'"
        def verifyToolTipText():
            return 'Verify ' +"'"+ input +"'"+ ' is the tooltip of  '+ "'" + tsp.custname + "'"
        def clickElement():
            return 'Click on '+ "'" + tsp.custname + "'"
        def mouseClick():
            if len(inputval)>0:
                return 'Mouse Click on  '+ "'" + tsp.custname +'['+inputval[0]+']['+inputval[1]+']'+"'"
            else:
                return 'Mouse Click on  '+ "'" + tsp.custname + "'"
        def verifyElementText():
            return 'Verify ' +"'"+ input +"'"+ ' is the text of the '+ "'" + tsp.custname + "'"
        def verifyelementexists():
            return 'Verify '+ "'" + tsp.custname + "'" + ' exists '
        def getElementText():
            return 'Get the text of the element '+ "'" + tsp.custname + "'"+ ' and save the text  '+"'"+ output +"'"+ ' in '+"'"+tsp.outputval+"'"
        def verifyDoesNotExists():
            return 'Verify '+ "'" + tsp.custname + "'" + '  does not exists '
        def tab():
            return 'Perform tab on '+ "'" + tsp.custname + "'"

        def rightClick():
            return 'Perform right click on '+ "'" + tsp.custname + "'"
        def doubleClick():
            return 'Double click on '+ "'" + tsp.custname + "'"
        def waitForElementVisible():
            return 'Wait until the element '+ "'" + tsp.custname + "'" +'is visible'
        def dropFile():
            return 'Drop file executed'

        #Button link keywords
        def click():
            return 'Click on '+ "'" + tsp.custname + "'"
        def cellClick():
            return 'Click on ' + "'" + tsp.custname + "'"
        def verifyButtonName():
            return 'Verify text ' +"'"+ input +"'"+ ' is the name of the '+ "'" + tsp.custname + "'"
        def uploadFile():
            return 'Upload the file  present in the path ' +"'" + input + "'" +'.'
        def getLinkText():
            return 'Get text From '+ "'" + tsp.custname + "'" + ' and save the text '+"'"+output+"'"+' in ' +"'"+tsp.outputval+"'"
        def getButtonName():
            return 'Get ButtonName From '+ "'" + tsp.custname + "'" + ' and save the text '+"'"+output+"'"+' in ' +"'"+tsp.outputval+"'"
        def verifyLinkText():
            return 'Verify text ' + "'"+input +"'"+ ' is the name of the ' +"'" + tsp.custname + "'"

        #utilweb operations
        def verifyReadOnly():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is read-only'
        def verifyEnabled():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is Enabled '
        def verifyDisabled():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is Disabled '
        def verifyExists():
            return 'Verify '+ "'" + tsp.custname + "'" + '  exists '
        def verifyHidden():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is Hidden '
        def verifyVisible():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is Visible '
        def mouseHover():
            return 'Move mouse pointer to '+ "'" + tsp.custname + "'"
        def setFocus():
            return 'Set the focus on '+ "'" + tsp.custname + "'"
        def press():
            return 'Press on the '+ "'" + tsp.custname + "'"
        def drag():
            return 'Perform drag on element '+ "'" + tsp.custname + "'"
        def drop():
            return 'Perform drop on element '+ "'" + tsp.custname + "'"
        def selectByAbsoluteValue():
            return 'Select value with exact text'+"'" +input + "'"+ ' present in the '+ "'" + tsp.custname + "'"
        def switchToWindow():
            return 'Control switched to window '+"'"+input+"'"
        def getElementTagValue():
            return 'Get the html tag value of ' + "'" + tsp.custname + "'" + ' and save the value ' +"'"+output+"'"+' in ' +"'"+tsp.outputval+"'"
        def getAttributeValue():
            return 'Get the attribute ' + "'" + tsp.inputval[0] + "'" + ' of ' + "'" + tsp.custname + "'" + ' and save the value ' +"'"+output+"'"+' in ' +"'"+tsp.outputval+"'"
        def verifyAttribute():
            input=inputval[0].split(';')
            return 'verify the attribute ' + "'"+ input[0] +"'"+ ' has value stored in ' +"'" + input[1] + "'"+' present in the ' +"'"+tsp.custname+"'"

        #Table keywords
        def getCellToolTip():
            inputval=tsp.inputval[0].split(';')
            return 'Get the cell tooltip from the '+ "'" + tsp.custname +'['+str(inputval[0])+']['+str(inputval[1])+']'+ "'"+ ' and save the tool tip text ' +"'"+output+"'"+' in ' +"'"+tsp.outputval+"'"
        def verifyCellToolTip():
            inputval=tsp.inputval[0].split(';')
            return 'Verify cell tooltip value '+"'"+input+"'"+' is present in the '+ "'"+ tsp.custname +'['+str(inputval[0])+']['+str(inputval[1])+']'+ "' table."
        # def cellclick():
        #     return 'Click on ' + "'" + tsp.custname + "'"
        def getRowCount():
            return 'Get row count of the ' + "'" + tsp.custname + "'" + ' and save the count ' +"'"+output+"'"+' in '+"'"+tsp.outputval+"'"
        def getColumnCount():
            return 'Get column count of the '+ "'" + tsp.custname + "'"+ ' and save the count '+"'"+output+"'"+' in '+"'"+tsp.outputval+"'"
        def verifyCellValue():
            inputval=tsp.inputval[0].split(';')
            # input = input[2:]# getting list elements from pos 3 till end
            # input = ','.join(input)# if list is make it into a string
            return 'Verify cell value'+"'"+str(input)+"'" +'  is present in the '+ "'" + tsp.custname +'['+inputval[0]+']['+inputval[1]+']'+"' table."

        def getColNumByText():
            return 'Get column number of ' + "'" + tsp.custname + "'" + ' by text '+"'"+input +"'"+' and save the column number ' +"'"+ output + "'"+' in '+"'"+tsp.outputval+"'"
        def getRowNumByText():
            return 'Get row number of ' + "'" + tsp.custname + "'" + ' by text '+"'"+input +"'"+' and save the row number ' +"'"+output +"'"+ ' in '+"'"+tsp.outputval+"'"
        def getCellValue():
            inputval=tsp.inputval[0].split(';')
            return 'Get cell value of ' + "'" + tsp.custname +'['+str(inputval[0])+']['+str(inputval[0])+']'+"'" + ' in the table and save the value ' +"'"+output +"'"+ ' in '+"'"+tsp.outputval+"'"
        #custom keyword
        def getobjectcount():
            return 'Get Object count of the type '+"'" +ele_type+"'" +' and save the count '+"'" +output+"'" +' in '+"'"+tsp.outputval+"'"

        #iris keywords
        def clickiris():
            return 'Click on '+ "'" +tsp.custname+ "'" +'.'
        def doubleclickiris():
            return 'Double click on '+ "'" +tsp.custname+ "'" +'.'
        def rightclickiris():
            return 'Right click on '+ "'" +tsp.custname+ "'" +'.'
        def setsecuretextiris():
            return 'Enter secure text '+"'"+ input+"'"+ ' in ' + "'" + tsp.custname + "'"+ '.'
        def settextiris():
            return 'Enter text '+"'"+ input+"'"+ ' in ' + "'" + tsp.custname + "'"+ '.'
        def cleartextiris():
            return 'Clear the text for '+ "'" + tsp.custname + "'"+ '.'
        def gettextiris():
            return 'Get text From '+ "'" +tsp.custname + "'" + ' and save the text '+"'"+ output + "'"+' in ' +"'"+ tsp.outputval+"'"+ '.'
        def getrowcountiris():
            return 'Get row count of '+ "'" + tsp.custname + "'"+ ' and save the count '+"'"+output+"'"+ ' in '+"'"+ tsp.outputval+"'"+ '.'
        def getcolcountiris():
            return 'Get column Count of ' + "'" + tsp.custname + "'" + ' and save the count ' + "'"+output+"'" + ' in '+"'"+ tsp.outputval+"'"+'.'
        def getcellvalueiris():
            return 'Get cell value of ' + "'" + tsp.custname +'['+inputL[0]+']['+inputL[1]+']'+"'" + ' in the table and save the value ' +"'"+output +"'"+ ' in '+"'"+tsp.outputval+"'"
        def verifyexistsiris():
            return 'Verify '+ "'" + tsp.custname + "'" + '  exists '+'.'
        def verifytextiris():
            return 'Verify ' + "'"+input + "'"+' is the text in the '+ "'" + tsp.custname + "'"+ '.'
        return locals()[keyword]()