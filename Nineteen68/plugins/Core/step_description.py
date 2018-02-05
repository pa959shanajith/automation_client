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

        if str(keyword) in ["typecast","split","displayvariablevalue"]:
            if type(output) is list:
                    output=','.join(output)
                    print output

        #Date operations
        def getcurrenttime():
            return 'Get current time of the system and save the time '+ output + ' in '+ tsp.outputval
        def getcurrentdate():
            return 'Get current date of the system and save the date ' + tsp.outputval + ' in '+ tsp.outputval
        def getcurrentdateandtime():
            return 'Get current date and time of the system and save the date and time '+ inputval[0] + ' and '+ inputval[1] + ' in '+ tsp.outputval


        #File operations
        def createfile():
            return 'Create a file: '+ inputval[1] + ' in the path: ' + inputval[0]
        def verifyfileexists():
            return 'Verify '+ inputval[1] + ' file exists in the path: ' + inputval[0]
        def deletefile():
            return 'delete: ' + inputval[1] + ' file from the path: ' + inputval[0]
        def renamefile():
            return 'rename filename ' + inputval[1] +' to '+ inputval[2]+ ' in the path '+ inputval[0]
        def savefile():
            return 'Save File: '+ inputval[1] + 'and stored in: '+ inputval[0]


        def executefile():
            return 'Perform execution of the file'  + input
        def verifycontent():
            return ' Verify '+ inputval[1]+ ' is present in the file ' + input
        def getcontent():
                return 'Get content from the file ' + input+ ' and save it in '+ tsp.outputval
        def comparefiles():
            return 'Compare the contents of file ' + input + ' and '+ input
        def executescript():
            return 'Perform execution of the file ' + input

        #Folder operations
        def createfolder():
            print inputval
            return 'Create a folder: '+ inputval[1] + ' in the path: ' + inputval[0]
        def verifyfolderexists():
            return 'Verify '+ inputval[1] + ' folder exists in the path: ' + inputval[0]
        def deletefolder():
            return 'delete: ' + inputval[1] + ' folder from the path: ' + inputval[0]
        def renamefolder():
            return 'rename folder ' + inputval[1] +' to '+ inputval[2]+ ' in the path '+ inputval[0]

        #Math opeartions
        def add():
            return 'Add the numbers ' + input+ ' and save the value ' + output + ' in '+ tsp.outputval
        def evaluate():
            return 'Evaluate Mathematical expression ' + input+ ' and save the result ' + output + '  in '+ tsp.outputval

        #Compare keywords
        def verifyobjects():
            return 'Verify objects ' + input + ' and ' + input+ ' and save the result in '+ tsp.outputval + '.'

        #String operations
        def tolowercase():
            return 'Change ' +"'"+ input+"'"+ ' to Lower case and save the value ' +"'"+ output+"'"+ ' in ' + tsp.outputval
        def evaluate():
            return 'Evaluate Mathematical expression ' +"'"+ input+ "'"+' and save the result ' +"'"+ output +"'"+ '  in '+ tsp.outputval
        def touppercase():
            return 'Change ' +"'"+ input+"'"+ ' to Upper case and save the value ' +"'"+ output+"'"+ ' in ' + tsp.outputval
        def trim():
            return 'Trim ' +"'"+ input+"'"+ ' and save the value ' +"'"+ output +"'"+ ' in '+ tsp.outputval
        def typecast():
            return 'Type cast '+"'"+ str(inputval[0])+"'"+' to '+"'"+ str(inputval[1])+"'"+' and save the value '+"'"+ output+"'"+' in '+"'"+tsp.outputval+"'"
        def split():
            return 'Split the string ' +"'"+ str(inputval[0])+"'"+' with split character '+"'"+str(inputval[1])+"'"+' and save the value: '+"'"+ output+"'"+' in '+"'"+tsp.outputval+"'"

        #delay keywords
        def wait():
            return 'Wait for ' + input+ ' Second(s)'
        def pause():
            return 'Pause the application until the user interrupts'
        def displayvariablevalue():
            return output.replace('\n',' ')

        #Dynamic variable keywords
        def deletedynvariable():
            return 'Delete variable ' + inputval[0]



        def getblockvalue():
            return 'Get Block Value of XML and save the value '+"'"+ output+"'"+' in '+"'" + tsp.outputval + "'"

        def verifyvalues():
            return "Verify values \"" + input + "\" and \"" + inputval[1]+ "\" and save the result in \""+ tsp.outputval + "\"."

        def capturescreenshot():
            return 'Captured Screenshot'

        def changedateformat():
            return "Change the format of the date '"+ input + "' to format '"+ inputval[1]+ "' and save the date  '" + output + "' in "+tsp.outputval

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


        def comparecontent():
            return "Compare the contents of file '"+ input+ "' and '"+ inputval[1]+ "'"

        def concatenate():
            return "Concatenate string '"+ input + "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def copyvalue():
            return "Copy value to variable '"+ input+ "' from variable '"+ inputval[1] + "'"
        def createdynvariable():
            return "Create a variable '"+ input+ "' with value '"+ inputval[1] + "'"
        def dateaddition():
            return "Add the date '"+ input + "' to'"+ inputval[1]+ "' number of days and save the date'" + output + "' in '"+ tsp.outputval
        def datecompare():
            return "Compare '" + inputval[1]+ "' and '" + inputval[0] + "'."
        def datedifference():
            return "Get the difference between the dates '"+ input+ "' and '"+ inputval[1]+ "' and save the date '" + output+ "' in '"+ tsp.outputval + "'"
        def exportdata():
            return "Execute SQL Query '"+ inputval[5]+" and save resultset in " + output
        def find():
            return "Verify input string '"+ input + "' contains '"+ inputval[1] + "'"
        def getblockcount():
            return "Get the Block Count of XML and save the value '" + output+ "' in '" + tsp.outputval + "'"
        def getcontent():
            return "Get content from the pdf '" + input+ "' and save it in '"+ tsp.outputval + "'"
        def getcurrentdate():
            return 'Get current date of the system and save the date ' + tsp.outputval + ' in '+ tsp.outputval
        def getcurrentdateandtime():
            return 'Get current date and time of the system and save the date and time '+ inputval[0] + ' and '+ inputval[1] + ' in '+ tsp.outputval
        def getcurrenttime():
            return 'Get current time of the system and save the time '+ output + ' in '+ tsp.outputval
        def getdata():
            return "Execute SQL Query '"+ inputval[5]+" and save resultset in " + output
        def getindexcount():
            if '@' in output:
                row,col=output.split('@')
                return "The index count for the dynamic variable "+ inputval[0] + " is " + "Row: "+str(row) + " and Column: "+str(col)
            else:
                return "The index count for the dynamic variable "+ inputval[0] + " is " + output
        def getlinenumber():
            return "Get the line number of content '"+ input+ "' from file '"+ inputval[1]+ "' and save the value '" + output + "' in "+tsp.outputval
        def getparam():
            return "Get data from file '"+ input + "' and  sheet '"+ inputval[1] + "'"
        def getstringlength():
            return "Get the length of the string '" + input+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def getsubstring():
            return "Get Substring of the string '"+ input+ "' with index/range '"+ inputval[1]+ "'  and save the value '" + output+ "' in variable '"+ tsp.outputval + "'"
        def gettagvalue():
            return "Get Tag Value of XML and save the value '" + output+ "' in '" + tsp.outputval + "'"
        def left():
            return "Perform String operation Left on string '"+ input+ "' with index '"+ inputval[1]+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def mid():
            return "Perform String operation Mid on string '" + input+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def modifyvalue():
            return "Modify variable '"+ input + "' value to '"+ inputval[1] + "'"
        def monthaddition():
            return "Add Months '"+ input + "' value to '"+ inputval[1] + "'"
        def mousepress():
            return 'Mouse Pressed'
        def replace():
            return "In string '"+ input + "' replace '"+ inputval[1] + "' with '"+ inputval[2]+ "' and save the updated input string '" + output+ "' in '" + tsp.outputval + "'"
        def replacecontent():
            return "Replace '"+ input + "' in the '"+ inputval[1] + " with the "+ inputval[2]
        def right():
            return "Perform String operation right on string '"+ input+ "' with index '"+ inputval[1]+ "' and save the value '" + output + "' in '"+ tsp.outputval + "'"
        def runquery():
            return "Execute SQL Query '"+ inputval[5]+" and save resultset in " + output
        def secureexportdata():
            return "Execute SQL Query '"+ inputval[5]+" and save resultset in " + output
        def securegetdata():
            return "Execute SQL Query '"+ inputval[5]+" and save resultset in " + output
        def securerunquery():
            return "Execute SQL Query '"+ inputval[5]+" and save resultset in " + output
        def secureverifydata():
            return "Verify SQL Query '"+ inputval[5]+ "' and result is same as '"+ inputval[7] + ","+ inputval[8] + "'"
        def sendfunctionkeys():
            return "Press '"+ input +"' Key"
##        def split():
##            return "Split the string '"+ input+ "' with split character '"+ inputval[1]+ "' and save the value:"+ inputval[2] + " in '"+ tsp.outputval + "'"
        def stop():
            return "Stop the Execution"
        def stringgeneration():
            return "Generate a charecter string having a length '"+ input + "'."
        def tolowercase():
            return ' Change ' + input+ ' to Lower case and save the value ' + output+ ' in ' + tsp.outputval
        def touppercase():
            return ' Change ' + input+ ' to Upper case and save the value ' + output+ ' in ' + tsp.outputval
        def trim():
            return ' Trim ' + input+ ' and save the value ' + output + ' in '+ tsp.outputval
        def verifycontent():
            return "Verify '"+ inputval[1]+ "' is present in the file '" + input + "'"
        def verifydata():
            return "Verify SQL Query '"+ inputval[5]+ "' and result is same as '"+ inputval[7] + ","+ inputval[8] + "'"
        def verifyfileimages():
            return "Compare images '" + input+ "' and '" + inputval[1]+ "'"
        def wait():
            return 'Wait for ' + input+ ' Second(s)'
        def writetofile():
            return "Write '"+ inputval[1] + "' to file  '" + input + "'"
        def yearaddition():
            return "Add Years '"+ input + "' value to '"+ inputval[1] + "'"

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
            return 'Read the content from the cell '+"'"+ input+"'"+' and save the value '+"'"+output+"'"+' in variable '+"'"+tsp.outputval+"'"
        def setexcelpath():
            return 'Sets the excel file path: '+"'"+ input+"'"+' internally for the excel operations'
        def writetocell():
            return 'Write '+"'"+ str(''.join(inputval[2:]))+"'"+' to cell '+"'"+ inputval[0]+','+ inputval[1]+"'"

        return locals()[keyword]()


    def webservices(self,keyword,tsp,inputval,input,output,con,reporting_obj):
        def setwholebody():
            return 'Set the entire body ' +"'"+ input+"'"+ ' that needs to be sent in the request'
        def setoperations():
            return 'Set the Operation ' +"'"+ input+"'"+ 'that needs to be performed on the request'
        def setmethods():
            return 'Set the method type ' +"'"+ input +"'"+ ' for the operation.'
        def setheadertemplate():
            return 'Set the header ' +"'"+ input+"'"+ ' from the header Template.'
        def setendpointurl():
            return 'Set the end point URL ' +"'"+ input +"'"+ '.'
        def settagvalue():
            return 'Set the Tag Value ' +"'"+ input +"'"+ ' for the tag '+ "'" + tsp.custname + "'" + '.'
        def setheader():
            return 'Set the header '+"'"+ input +"'"+ ' that needs to be sent in the request.'
        def settagattribute():
            return 'Set the Tag attribute ' +"'"+ input +"'"+ ' for the tag '+ "'" + tsp.custname + "'" + '.'
        def getheader():
            return 'Fetch the header ' +"'"+ output+"'"+ ' that was received as a response.'
        def getbody():
            return 'Fetch the entire body ' +"'"+ output+"'"+ ' that was received as a response.'
        def addclientcertificate():
            return 'Add the certificate present in the '+"'"+ inputval[0]+"'"+ ' to the '+ "'"+inputval[1] +"'"+ '.'
        def getservercertificate():
            return 'Fetch the Server certificate and save it in '+ "'"+inputval[1] +"'"+ '.'
        def executerequest():
            return 'Execute the request.'
        #return locals()[key](keyword)
        return locals()[keyword]()

    def oebs(self,keyword,tsp,inputval,input,output,con,reporting_obj):
        def launchapplication():
            return 'The application present in the path'+ inputval[0] + 'is launched'
        def findwindowandattach():
            return 'Find window and attach is executed'
        def closeapplication():
            return 'The application is closed'
        def switchtoframe():
            return 'Control switched to Frame():'+ input
        def setfocus():
            return 'Set focus on'+ "'" + tsp.custname + "'"
        def waitforelementvisible():
            return 'Wait until the element'  + "'" + tsp.custname + "'"+  'is visible'
        def verifyhidden():
            return 'Verify' + tsp.custname +  'is hidden'
        def verifydisabled():
            return 'Verify' + "'" + tsp.custname + "'" +  'is disabled'
        def verifyenabled():
            return 'Verify' + "'" + tsp.custname + "'" +  'is enabled'
        def verifyvisible():
            return 'Verify' + "'" + tsp.custname + "'" +  'is visible'
        def verifyreadonly():
            return 'Verify' + "'" + tsp.custname + "'" +  'is read-only'
        def verifytooltiptext():
            return 'Verify' +"'"+ input + "'"+' is the tooltip of '+ "'" + tsp.custname + "'"
        def gettooltiptext():
            return 'Get the tool tip from the ' + "'" + tsp.custname + "'" + ' and save the tool tip text \'' + output + '\' in ' + tsp.output
        def verifyexists():
            return 'Verify ' + "'" + tsp.custname + "'" + ' exists'
        def verifydoesnotexists():
            return 'Verify ' + "'" + tsp.custname + "'" + ' does not exists'
        def rightclick():
            return 'Perform right click on element' + "'" + tsp.custname + "'"
        def drag():
            return 'Perform drag on element' + "'" + tsp.custname + "'"
        def drop():
            return'Perform drop on element' + "'" + tsp.custname + "'"
        def settext():
            return 'Enter text ' +"'"+ input +"'"+ ' in the '+ "'" + tsp.custname + "'"
        def gettext():
            return 'Get text from the ' + "'" + tsp.custname + "'" + ' and save the text \'' + output + '\' in ' + tsp.outputval
        def gettextboxlength():
            return 'Get length from the ' + "'" + tsp.custname + "'" + ' and save the length \'' + output + '\' in ' + tsp.outputval
        def verifytextboxlength():
            return 'Verify ' +"'"+ input +"'"+ ' is the length of textbox ' + "'" + tsp.custname + "'"
        def verifytext():
            return 'Verify ' +"'"+ input +"'"+ ' is the text in the ' + "'" + tsp.custname + "'"
        def cleartext():
            return 'Clear text from the ' + "'" + tsp.custname + "'"
        def click():
            return 'Click on the ' + "'" + tsp.custname + "'"
        def doubleclick():
            return 'DoubleClick on the ' + "'" + tsp.custname + "'"
        def verifybuttonname():
            return 'Verify ' +"'"+ input +"'"+  'is the name of ' + "'" + tsp.custname + "'"
        def getbuttonname():
            return 'Get the name of the ' + "'" + tsp.custname + "'" + 'and save the +output+ in ' + tsp.outputval
        def getlinktext():
            return 'Get Text From ' + "'" + tsp.custname + "'" + ' and save the text \'' + output + '\' in ' + tsp.outputval
        def verifylinktext():
            return 'Verify text ' + "'"+input +"'"+ ' is the name of the ' + "'" + tsp.custname + "'"
        def selectradiobutton():
            return 'Select ' + "'" + tsp.custname + "'"
        def getstatus():
            return 'Get the status of the ' + "'" + tsp.custname + "'" + ' and save the status \'' + output + '\' in ' + tsp.outputval
        def selectcheckbox():
            return 'Select ' + "'" + tsp.custname + "'"
        def unselectcheckbox():
            return 'Unselect '+ "'" + tsp.custname + "'"
        def selectvaluebyindex():
            return 'Select value with index value ' +"'"+ input +"'"+ ' in the ' + "'" + tsp.custname + "'"
        def getcount():
            return'Get the count of values in the ' + "'" + tsp.custname + "'" + ' and save the count \'' + output + '\' in ' + tsp.outputval
        def selectvaluebytext():
            return 'Select value ' + "'"+input +"'"+ ' in the ' + "'" + tsp.custname + "'"
        def verifyselectedvalue():
            return 'Verify value ' + "'"+input +"'"+ ' is selected in the ' + "'" + tsp.custname + "'"
        def verifycount():
            return 'Verify ' + "'"+input +"'"+ ' is the count of the ' + "'" + tsp.custname + "'"
        def verifyallvalues():
            return 'Verify values ' + "'"+input +"'"+ ' are present in the ' + "'" + tsp.custname + "'"
        def verifyselectedvalues():
            return 'Verify values ' +"'"+ input + "'"+' are selected in the ' + "'" + tsp.custname + "'"
        def getselected():
            return 'Get Selected value of '+  "'" + tsp.custname + "'" + ' and save value \'' + output + '\' in '+ tsp.outputval
        def verifyvaluesexists():
            return 'Verify values ' +"'"+ input +"'"+ ' exists in the '+  "'" + tsp.custname + "'"
        def getvaluebyindex():
            return 'Get value with index ' +"'"+ input +"'"+ ' in the '     + "'" + tsp.custname + "'" + ' and save the value \'' + output + '\' in ' + tsp.outputval
        def selectmultiplevaluesbyindexes():
            return 'Select values with index values ' +"'"+ input +"'"+ ' in the '+ "'" + "'" + tsp.custname + "'" + "'"
        def selectmultiplevaluesbytext():
            return 'Select values ' + "'"+input +"'"+ ' in the '+ "'" + "'" + tsp.custname + "'" + "'"
        def getmultiplevaluesbyindexes():
            return 'Get values with indexes ' +"'"+ input +"'"+ ' in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output + ' in  '+ tsp.outputval
        def selectallvalues():
            return 'Select all values in the ' + "'" + tsp.custname + "'"
        def deselectall():
            return'Deselect all values in the ' + "'" + tsp.custname + "'"
        def getrowcount():
            return 'Get row count of the ' + "'" + tsp.custname  + "'" + ' and save the count \'' + output + '\' in ' + tsp.outputval
        def getcolumncount():
            return'Get column count of the ' + "'" + tsp.custname + "'" + ' and save the count \'' + output + '\' in ' + tsp.outputval
        def getcellvalue():
            f_input = input.split(',')
            return 'Get cell value of '+ "'" + tsp.custname + '['+f_input[0] +']['+ f_input[1] + "]'" + ' in the table and save the value ' + output + ' in ' + tsp.outputval
        def verifycellvalue():
            f_input = input.split(',')
            return 'Verify cell value ' + f_input[2] + ' is present in the ' + "'" + tsp.custname + '['+f_input[0] +']['+ f_input[1] + "]'" +  '  table'
        def cellclick():
            f_input = input.split(',')
            return 'Click ' + "'" + tsp.custname + '['+f_input[0] +']['+ f_input[1] + "]'"
        def clickelement():
            return 'Click ' + "'" + tsp.custname + "'"
        def getelementtext():
            return'Get the text of the element ' + "'" + tsp.custname + "'" + ' and save the value  \'' + output + '\' in ' + tsp.outputval
        def verifyelementtext():
            return 'Verify ' +"'"+ input +"'"+ ' is the the text of the ' + "'" + tsp.custname + "'"
        def sendfunctionkeys():
            return 'Press ' + tsp.inputval[0] + ' key'
        def right():
            return 'Right button clicked ' + input + ' times'
        def left():
            return 'Left button clicked ' + input + ' times'
        def up():
            return 'Up button clicked ' + input + ' times'
        def down():
            return 'Down button clicked ' + input + ' times'
        def closeframe():
            return 'Close frame ' + "'" + tsp.custname + "'"
        def togglemaximize():
            return 'Perform toggle maximize operation on ' + "'" + tsp.custname + "'"
        def toggleminimize():
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
        def launchapplication():
            return ' The application present in the path '+"'"+ inputval[0]+"'"+ ' is launched'+ '.'
        def getpagetitle():
            return ' The page title is '+"'"+output +"'"+' and  is saved  in the variable ' +"'"+tsp.outputval+"'"+ '.'
        def closeapplication():
            return ' The application is closed'+ '.'
        def geterrormessage():
            return ' Get the error message '+"'"+output+"'"+'.'
        def starttransaction():
            return ' Start the transaction with ID'+"'"+inputval+"'"+'.'
        def toolbaraction():
            return ' Perform '+"'"+inputval+"'"+' action from tool bar. '
        def getpopuptext():
            return ' Get pop-up text and save the text '+"'"+output+"'"+' in '+"'"+ tsp.outputval+"'"+'.'
        def serverconnect():
            return ' Connect to SAP server '+"'"+inputval+"'"+'.'


        #Textbox keywords
        def gettext():
            return ' Get Text From '+ "'" +tsp.custname + "'" + ' and save the text '+"'"+ output + "'"+' in ' +"'"+ tsp.outputval+"'"+ '.'
        def setsecuretext():
            return ' Enter secure text ' +"'"+inputval[0]+"'"+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def cleartext():
            return ' Clear text from the '+ "'" + tsp.custname + "'"+ '.'
        def settext():
            return ' Enter text '+"'"+ inputval[0]+"'"+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def verifytext():
            return ' Verify ' + "'"+input + "'"+' is the text in the '+ "'" + tsp.custname + "'"+ '.'
        def gettextboxlength():
            return ' Get length from the '+ "'" + tsp.custname + "'"+ ' and save the length '+ "'"+output+ "'"+' in '+"'"+tsp.outputval+"'"+ '.'
        def verifytextboxlength():
            return ' Verify ' +"'"+ input +"'"+' is the length of textbox '+ "'" + tsp.custname + "'"+ '.'

        #Button link keywords
        def getbuttonname():
            return ' Get ButtonName From '+ "'" + tsp.custname + "'" + ' and save the text '+"'"+ output + "'"+' in ' +"'"+ tsp.outputval+"'"+'.'
        def verifybuttonname():
            return ' Verify text ' +"'"+input+"'"+ ' is the name of the '+ "'"+tsp.custname+"'"+'.'
        def uploadfile():
            return ' Upload the file present in the path ' + "'"+input +"'"+ '.'

        #Dropdown keywords
        def getselected():
            return ' Get Selected value of '+ "'" + tsp.custname + "'"+ ' and save value ' +"'"+ output +"'"+ ' in '+"'"+ tsp.outputval+"'"+ '.'
        ##        def GetValueByIndex():
        ##            return 'Get value with index ' + input + ' in the '+ "'" + tsp.custname + "'" + ' and save the value ' + output + ' in '+ tsp.outputval+'.'
        def verifyvaluesexists():
            return ' Verify values ' +"'"+ input +"'"+ ' exists in the '+ "'" + tsp.custname + "'"+'.'
        def selectvaluebytext():
            return ' Select value by text '+"'"+input+"'"+' in '+ "'" + tsp.custname + "'"+'.'
        def verifyselectedvalue():
            return ' Verify value ' +"'"+ input +"'"+ ' are selected in the '+ "'" + tsp.custname + "'"+'.'
        def verifyallvalues():
            return ' Verify values ' +"'"+ input +"'"+ ' are present in the '+ "'" + tsp.custname + "'"+'.'
        def verifycount():
            return ' Verify ' +"'"+ input +"'"+ ' is the list count of the ' +"'" + tsp.custname + "'"
        ##        def SelectValueByIndex():
        ##            return ' Select value with index value '+ input+' in the '+"'" + tsp.custname + "'"
        def getcount():
            return ' Get the count of values in the '+ "'" + tsp.custname + "'"+ ' and save the count ' +"'"+output+"'"+ ' in ' +"'"+tsp.outputval+"'"+'.'
        #Element Keywords
        ##        def ClickElement():
        ##            return 'Click on ' +"'" + tsp.custname + "'"+'.'
        def getelementtext():
            return ' Get the text of the element '+ "'" + tsp.custname + "'"+ ' and save the value  '+"'"+output +"'"+ ' in '+"'"+ tsp.outputval+"'"+'.'
        def verifyelementtext():
            return ' Verify '+ "'" + input + "'"+ ' is the text of '+"'" + tsp.custname + "'"+'.'

        #Radio checkbox keywords
        def selectradiobutton():
            return ' Select '+ "'" + tsp.custname + "'"+'.'
        def getstatus():
            return ' Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' + "'"+output +"'"+ ' in '+"'"+ tsp.outputval+"'"+'.'
        def selectcheckbox():
            return ' Select '+ "'" + tsp.custname + "'"+'.'
        def unselectcheckbox():
            return ' Unselect '+ "'" + tsp.custname + "'"+'.'
        #Table Keywords
        def getrowcount():
            return ' Get row count of '+ "'" + tsp.custname + "'"+ ' and save the count '+"'"+output+"'"+ ' in '+"'"+ tsp.outputval+"'"+ '.'
        def getcolumncount():
            return ' Get column Count of ' + "'" + tsp.custname + "'" + ' and save the count ' + "'"+output+"'" + ' in '+"'"+ tsp.outputval+"'"+'.'
        def getcolnumbytext():
            return ' Get column number of ' + "'" + tsp.custname + "'" + ' by text '+"'" +input +"'" +' and save the column number ' +"'"+ output +"'"+ ' in '+"'"+ tsp.outputval+"'"+'.'
        def getrownumbytext():
            return ' Get row number of ' + "'" + tsp.custname + "'" + ' by text '+"'" +input +"'" +' and save the row number ' + "'"+ output +"'" + ' in '+ tsp.outputval+"'"+'.'
        def getcellvalue():
            return ' Get cell value of  '+ "'" + tsp.custname +input + "'" +'in the table and save the value '+"'"+ output +"'"+ " in " +"'"+ tsp.custname +"'"+'.'
        def verifycellvalue():
            return ' Verify cell value of element in row number ' +"'"+ input[0] +"'"+' and column number '+"'"+input[1] +"'"+' against the input value '+"'"+input[2]+"'"+' present in ' +"'" + tsp.custname + "'"+'.'
        def verifytextexists():
            return ' Verify text '+ "'"+input+"'"+' exists in table '+"'"+ tsp.custname +"'"+"and  save the result as "+"'"+ output +"'"+ ' in '+"'"+ tsp.outputval+"'"+'.'
        ##        def CellClick():
        ##            return 'Click on '+ "'" + tsp.custname + "'"+'.'
        ##        def SelectValueByIndex():
        ##            return ' Select the value with index '+ input+' in the '+"'" + tsp.custname + "'"
        ##        def SelectValueByText():
        ##            return 'Select the value '+"'"+input+"'"+' of the '+"'" + tsp.custname + "'"+' with the text '+"'"+input+"'"+' present in the table cell  '+"'" + tsp.custname + "'"+'-['+input+']['+input+']'
        def getselected():
            return ' Get Selected value of '+ "'" + tsp.custname + "'"+ ' and save value ' +"'"+ output +"'"+ ' in '+"'"+ tsp.outputval + "'"+'.'
        ##        def GetTableStatus():
        ##            return 'Select value by text '+input+' of the '+ 'type '+ "'" + tsp.custname + "'" +' with the element '+input+' present in the table cell '+"'" + tsp.custname + "'"+'-['+ input + ']['+ input +']'+'.'
        ##        def GetCellToolTip():
        ##            return 'Get CellToolTip of  ' + input + ' and save the result as  '+output+' in ' + "'" + tsp.custname + "'"+'.'
        ##        def TableCellClick():
        ##            return 'Click on table cell ' + input + ' in '+ "'" + tsp.custname + "'"+'.'
        ##        def TableCellDoubleClick():
        ##            return 'Double click on cell ' + input + ' in ' +"'" + tsp.custname + "'"+'.'
        def selectrow():
            return ' Select the row '+"'" + input+"'" +' in '+"'" + tsp.custname + "'"+'.'
        def unselectrow():
            return ' Unselect the row  '+"'" +input+"'" +' of '+ "'" + tsp.custname + "'"+ '.'
        ##        def GetStatus():
        ##            return 'Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' + "'" +output +"'" + ' in '+ tsp.outputval

        #SAP gerenal keywords
        def click():
            return ' Click on the '+ "'" +tsp.custname+ "'" +'.'
        def doubleclick():
            return ' Double click on the '+ "'" +tsp.custname+ "'" +'.'
        def mousehover():
            return ' Move mouse pointer to ' + "'" + tsp.custname + "'"+'.'
        ##        def GetToolTipText():
        ##            return 'Get the tool tip  of '+ "'" +tsp.custname+ "'" +'.'
        ##        def VerifyToolTipText():
        ##            return 'Verify ' + input + ' is the tooltip of  '+ "'" + tsp.custname + "'"
        def setfocus():
            return ' Set the focus on '+ "'" + tsp.custname + "'"+'.'

        #Saputil keywords
        def verifyenabled():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is enabled '+'.'
        def verifydisabled():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is disabled '+'.'
        def verifyexists():
            return ' Verify '+ "'" + tsp.custname + "'" + '  exists '+'.'

        #Scroll Keywords
        def scrolldown():
            return ' Scroll down by '+ "'"+inputval+"'"+' units and store the output as '+"'"+output+"'"+'.'
        def scrollleft():
            return ' Scroll left by '+"'"+inputval+"'"+' units and store the output as '+"'"+output+"'"+'.'
        def scrollright():
            return ' Scroll right by '+"'"+inputval+"'"+' units and store the output as '+"'"+output+"'"+'.'
        def scrollup():
            return ' Scroll up by '+"'"+inputval+"'"+' units and store the output as '+"'"+output+"'"+'.'
        #Tab Keywords
        def movetabs():
            return ' Move tab '+ "'" + tsp.custname + "'"+'to left and store the output as '+"'"+output+"'"+'.'
        #Shell(Grid) Keywords
        def presstoolbarbutton():
            return ' Pressing Toolbar Button '+"'"+input[0]+"' of '"+tsp.custname+"'"+' and store the output as '+"'"+output+"'"+'.'
        def selectrows():
            return ' Selecting Row/Rows'+"'"+input[0]+"'"+'and store the output as '+"'"+output+"'"+'.'
        def getcountofrows():
            return ' Get row count of ' + "'" + tsp.custname + "'" + ' and save the count ' + "'"+output+"'" + ' in '+"'"+ tsp.outputval+"'"+'.'
        def getcountofcolumns():
            return ' Get column count of ' + "'" + tsp.custname + "'" + ' and save the count ' + "'"+output+"'" + ' in '+"'"+ tsp.outputval+"'"+'.'
        def getcelltext():
            return ' Get cell text of row '+"'"+input[0]+"'"+'and column '+"'"+input[1]+"'"+' and store the output as '+"'"+output+"'" + ' in '+"'"+ tsp.outputval+"'"+'.'
        def selecttreenode():
            inp = input
            if(len(inputval)>1):
                inp = '->'.join(inputval)
            return ' Select node '+"'"+inp+"'"+' in '+"'"+tsp.custname+"'"+'.'
        def getnodenamebyindex():
            inp = input
            if(len(inputval)>1):
                inp = '->'.join(inputval)
            return ' Get name of node at index'+"'"+inp+"'"+' and store the output as '+"'"+output+"'" + ' in '+"'"+ tsp.outputval+"'"+'.'
        return locals()[keyword]()


    def desktop(self,keyword,tsp,inputval,input,output,con,reporting_obj):
        #-----------------------------------Added this step as input was returned as a string
        if type(input) is str:                 #----checking if input is a string
            listInput=[]
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
        def deselectall():
            return ' Deselect all values in the '+ "'" + tsp.custname + "'."
        def getvaluebyindex():
            return ' Get value with index ' + "'" +input +"'" + ' in the '+ "'" + tsp.custname + "'" + ' and save the value ' +"'" + output +"'" + ' in '+ "'" +tsp.outputval+"'.",
        def verifyvaluesexists():
            return ' Verify values ' + "'" +input +"'" + ' exists in the '+ "'" + tsp.custname + "'."
        def selectmultiplevaluesbytext():
            return ' Select values ' +"'" + input + "'" +'in the '+ "'" + tsp.custname + "'."
        def selectvaluebytext():
            return ' Select value by text '+"'" +input+"'" +' of the '+ 'type '+ "'" + tsp.custname + "'" +' with the element '+input+' present in the table cell '+"'" + tsp.custname + "'"+'-['+ input + ']['+ input +']',
        def selectvaluebyindex():
            return ' Select value with index '+ "'" +input+"'" +' in the '+"'" + tsp.custname + "'."
        def getcount():
            return ' Get the count of the values present in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + "'" +output+"'"  + ' in '+ "'" +tsp.outputval+"'.",
        def selectmultiplevaluesbyindexes():
            return ' Select values by index/indexes' + "'" +input +"'" + 'in the '+ "'" + tsp.custname + "'."
        def verifycount():
            return ' Verify ' +"'" + input +"'" + ' is the list count of the ' +"'" + tsp.custname + "'."
        def selectallvalues():
            return ' Select all values in the '+ "'" + tsp.custname + "'."
        def verifyselectedvalue():
            return ' Verify the selected value from the ' + "'" + tsp.custname + "'"+ ' with the '+ "'" +input+"'."
        def getselected():
            return ' Get selected value from the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output+ ' in '+ "'" +tsp.outputval+"'."
        def getmultiplevaluesbyindexes():
            return ' Get values with indexes ' + "'" +input + "'" +' in the '+ "'" + tsp.custname + "'" +' and save the value ' +"'" + output+ "'" +' in ' +"'" +tsp.outputval+"'."
        def verifyallvalues():
            return ' Verify the values from the '+ "'" + tsp.custname + "'" +' with '+ "'" +input+"'."

        #Tab control keywords( 4 keywords)
        def verifyselectedtab():
            return ' Verify the selected value from the ' + "'" + tsp.custname + "'"+ ' with the '+"'" + input+"'."
        def getselectedtab():
            return ' Get selected value from the '+ "'" + tsp.custname + "'"+ ' and save the value ' + "'" +output+"'" + ' in '+ "'" +tsp.outputval+"'."
        def selecttabbytext():
            return ' Select tab by text '+"'" +input+"'" +' in '+ "'" + tsp.custname+"'."
        def selecttabbyindex():
            return ' Select tab by index '+"'" +input+"'" +' in '+ "'" + tsp.custname+"'."

        #Date control keywords ( 2 keywords)
        def getdate():
            return ' Get the date from ' + "'" + tsp.custname + "'" + ' and save the date  in ' +"'" + tsp.outputval+"'."
        def setdate():
            return ' Set the date, with the format  '+"'" + input +"'" + ' in '+"'" + tsp.custname+"'."

        #Radio checkbox keywords ( 5 keywords)
        #common
        def getstatus():
            return ' Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' + output + ' in '+"'"+ tsp.outputval+"'."
        #radio
        def selectradiobutton():
            return ' Select '+ "'" + tsp.custname + "'."
        #checkbox
        def selectcheckbox():
            return ' Select '+ "'" + tsp.custname + "'"+'.'
        def unselectcheckbox():
            return ' Unselect '+ "'" + tsp.custname + "'"+'.'

        #Application keywords(@Window keywords- 7 keywords)
        def launchapplication():
            return ' The application present in the path  '+ inputval[0]+ ' is launched.'
        def getpagetitle():
            return ' Get the title of Application and  save the title in ' +tsp.outputval+"."
        def closeapplication():
            return ' The application is closed.'
        def findwindowandattach():
            return ' Find window and attach is executed.'
        def selectmenu():
            return " '"+input+"'"+' menu selected.'
        def maximizewindow():
            return ' Perform maximize window operation on the window.'
        def minimizewindow():
            return ' Perform minimize window operation on the window.'

        #Mail Related keywords(@Email keywords- 8 keywords)
        def getattachmentstatus():
            return ' Attachment is '+"'"+output+"'"+' in the email.'
        def getbody():
            return ' Fetch '+"'"+'Body'+"'"+' from email and save the value in variable '+tsp.outputval+ '.'
        def getemail():
            return ' Fetch the email  which is having '+"'"+'From'+"'"+' as '+"'"+listInput[0]+"'"+', '+"'"+' To '+"'" +' as '+"'"+listInput[1]+"'"+' and '+"'"+'Subject'+"'"+ ' as '+"'"+listInput[2]+"'"
        def getfrommailid():
            return ' Fetch '+"'"+'From Mail ID'+"'"+' from email and save the value in variable '+tsp.outputval+ '.'
        def getsubject():
            return ' Fetch '+"'"+'Subject'+"'"+' from email and save the value in variable '+tsp.outputval+'.'
        def gettomailid():
            return ' Fetch '+"'"+'To Mail ID'+"'"+' from email and save the value in variable '+tsp.outputval+'.'
        def switchtofolder():
            return ' Switched to folder'+"'"+input+"'."
        def verifyemail():
            return ' Verify email from the path '+"'"+input+"'."
        def settomailid():
            if len(listInput)>0:
                input = ", ".join(listInput)
            else:
                input =str(inputval[0])
            return ' Set '+"'"+'To Mail ID'+"'"+' as '+"'"+input+"'"+' for the email and save the value in variable '+tsp.outputval+'.'
        def setcc():
            if len(listInput)>0:
                input = ", ".join(listInput)
            else:
                input =str(inputval[0])
            return ' Set '+"'"+'CC'+"'"+' as '+"'"+input+"'"+' for the email and save the value in variable '+tsp.outputval+'.'
        def setbcc():
            if len(listInput)>0:
                input = ", ".join(listInput)
            else:
                input =str(inputval[0])
            return ' Set '+"'"+'BCC'+"'"+' as '+"'"+input+"'"+' for the email and save the value in variable '+tsp.outputval+'.'
        def setsubject():
            return ' Set '+"'"+'Subject'+"'"+' as '+"'"+input+"'"+' for the email and save the value in variable '+tsp.outputval+'.'
        def setbody():
            return ' Set '+"'"+'Body'+"'"+' as '+"'"+input+"'"+' for the email and save the value in variable '+tsp.outputval+ '.'
        def setattachments():
            if len(listInput)>0:
                input = ", ".join(listInput)
            else:
                input =str(inputval[0])
            return ' Set attachment/attachments from the path '+"'"+input+"'"+' for the email and save the value in variable '+tsp.outputval+ '.'
        def sendemail():
            return ' Send the email and save the value in variable '+tsp.outputval+ '.'

        #TextBox keywords( 5 keywords)
        def cleartext():
            return ' Clear text from the '+ "'" + tsp.custname + "'"+ '.'
        def gettext():
            return ' Get Text From '+ "'" +tsp.custname + "'" + ' and save the text '+"'"+ output + "'"+' in ' + tsp.outputval+ '.'
        def settext():
            return ' Enter text '+"'"+ input+"'"+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def verifytext():
            return ' Verify ' + "'"+input + "'"+' is the text in the '+ "'" + tsp.custname + "'"+ '.'
        def setsecuretext():
            return ' Enter secure text ' +"'"+input + "'"+ ' in the  ' + "'" + tsp.custname + "'"+ '.'

        #Element keywords(7 keywords)
        def getelementtext():
            return ' Get the value present in ' + "'" + tsp.custname + "'" +' and save the value ' + output + ' in '+ tsp.outputval+"."
        def verifyelementdoesnotexists():
            return ' Verify '+ "'" + tsp.custname + "'" + ' does not exists. '
        def clickelement():
            return ' Click on '+"'" + tsp.custname + "'."
        def mousehover():
            return ' Move mouse pointer to ' + "'" + tsp.custname + "'"+'.'
        def verifyelementtext():
            return ' Verify if the value '+"'"+input+"'"+ ' is the element text of ' + "'" + tsp.custname + "'."
        def verifyelementexists():
            return ' Verify if the element '+ "'" + tsp.custname + "' exists."
        def press():
            return ' Press the ' +"'" + tsp.custname + "'"

        #Button Keywords(7 keywords)
        def click():
            return ' Click on the ' +"'" + tsp.custname + "'."
        def doubleclick():
            return ' Double click on the '+"'"+tsp.custname + "'."
        def verifybuttonname():
            return ' Verify button name '+"'"+tsp.custname + "'" +' and save the value ' + output + ' in '+"'" + tsp.outputval+ "'."
        def getbuttonname():
            return ' Get button name '+"'"+tsp.custname + "'" +' and save the value ' + output + ' in '+"'" + tsp.outputval+ "'."
        def rightclick():
            return ' Right click on the '+"'" + tsp.custname + "'."
        #link Keywords(2 keywords but not in use)
        def getlinktext():
            return ' Get the value present in ' + "'" + tsp.custname + "'" +' and save the value ' + output + ' in '+ tsp.outputval+"."
        def verifylinktext():
            return ' Verify if the value is present in ' + "'" + tsp.custname + "'."

        #Util Keywords( 7 keywords)
        def setfocus():
            return ' Set focus on '+"'"+tsp.custname+"'."
        def verifydisabled():
            return ' Verify if '+"'"+tsp.custname+"'."+' is disabled.'
        def verifyenabled():
            return ' Verify if '+"'"+tsp.custname+"'."+' is enabled.'
        def verifyhidden():
            return ' Verify if '+"'"+tsp.custname+"'."+' is hidden.'
        def verifyvisible():
            return ' Verify if '+"'"+tsp.custname+"'."+' is visible.'
        def verifyreadonly():
            return ' Verify if '+"'"+tsp.custname+"'."+' is read only.'
        def verifyexists():
            return ' Verify if '+"'"+tsp.custname+"'."+' is exists.'
        #Tree Keywords(2):
        def getnodenamebyindex():
            try:
                input1="->".join(listInput)
            except:
                input1=input
            return 'Get node text from index path '+"'"+input1+"'"+' and save the value '+"'"+output+"'"+" in '"+ tsp.outputval+"'."
        def selecttreenode():
            try:
                input1="->".join(listInput)
            except:
                input1=input
            return 'Select the tree node  '+"'"+input1+"'."

        return locals()[keyword]()

    def mobileapp(self,keyword,tsp,inputval,input,output,con,reporting_obj):
        output_list=tsp.outputval
        if len(output_list) > 1 :
            output_list = output_list.split(';')
            output_list=output_list[0]
        else:
            output_list=output_list
        def installapplication():
            return 'The application present in the path '+ inputval[0] +  ' is installed'
        def unInstallapplication():
            return 'The application present in the path '+ inputval[0] +  ' is uninstalled'
        def launchapplication():
            return 'The application present in the path '+ inputval[0] +  ' is launched'
        def closeapplication():
            return 'The application is closed'
        def swipeup():
            return 'Performed swipe up operation'
        def verifydoesnotexists():
            return ' Verify '+ "'" + tsp.custname + "'" + '  does not exists '
        def swipedown():
            return 'Performed swipe down operation'
        def swipeleft():
            return 'Performed swipe left operation'
        def hidesoftkeyboard():
            return 'Performed HideSoftKeyBoard operation'
        def backpress():
            return 'Performed Back Press operation'
        def swiperight():
            return 'Performed swipe right operation'
        def toggleon():
            return 'Performed toggle on operation on  ' + "'" + tsp.custname + "'"
        def toggleoff():
            return 'Performed toggle off operation on  ' + "'" + tsp.custname + "'"
        def invokedevice():
            return 'Invoking  ' + "'" + input + "'"
        def getdevices():
            return 'Get all the connected devices ' + ' and save the result  '+ output + ' in ' + output_list+ '.'
        def presselement():
            return 'Press ' + "'" + tsp.custname + "'"
        def longpresselement():
            return 'Long Press ' + "'" + tsp.custname + "'"
        def getelementtext():
            return'Get the text of the element ' + "'" + tsp.custname + "'" + ' and save the value  ' + output + ' in ' + output_list
        def verifyelementtext():
            return 'Verify ' + input + ' is the the text of the ' + "'" + tsp.custname + "'"
        def waitforelementexists():
            return 'Wait until the element'  + "'" + tsp.custname + "'"+  'is exists'
        def verifyenabled():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is enabled '
        def setdate():
            return 'Set date '+ inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def setnumber():
            return 'Set number '+ inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def gettime():
            return 'Get Time From '+ "'" +tsp.custname + "'" + ' and save the time '+ output + ' in ' + output_list+ '.'
        def getdate():
            return 'Get Date From '+ "'" +tsp.custname + "'" + ' and save the date '+ output + ' in ' + output_list+ '.'
        def settime():
            return 'Enter time '+ inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def verifyelementenabled():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is enabled '
        def verifyelementdisabled():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is Disabled '
        def verifydisabled():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is disabled '
        def verifyexists():
            return ' Verify '+ "'" + tsp.custname + "'" + '  exists '
        def verifyelementexists():
            return ' Verify '+ "'" + tsp.custname + "'" + '  exists '
        def verifyhidden():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is Hidden '
        def verifyvisible():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is Visible '
        def getbuttonname():
            return ' Get ButtonName From '+ "'" + tsp.custname + "'" + ' and save the text '+ output + ' in ' + output_list
        def verifybuttonname():
            return 'Verify text ' + input + ' is the name of the '+ "'" + tsp.custname + "'"
        def press():
            return 'Press on the '+ "'" + tsp.custname + "'"
        def longpress():
            return 'Long press on the '+ "'" + tsp.custname + "'"
        #Radio checkbox keywords
        def selectradiobutton():
            return 'Select '+ "'" + tsp.custname + "'"
        def getstatus():
            return 'Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' + output + ' in '+ output_list
        def selectcheckbox():
            return 'Select '+ "'" + tsp.custname + "'"
        def unselectcheckbox():
            return 'Unselect '+ "'" + tsp.custname + "'"

        #textbox keywords
        def sendvalue():
            return ' Enter value ' + input+ ' in the '+ "'" + tsp.custname + "'"
        def gettext():
            return 'Get Text From '+ "'" +tsp.custname + "'" + ' and save the text '+ output + ' in ' + output_list+ '.'
        def setsecuretext():
             return 'Enter secure text ' +inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def cleartext():
             return 'Clear text from the '+ "'" + tsp.custname + "'"+ '.'
        def settext():
            return 'Enter text '+ inputval[0]+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def setmaxvalue():
            return 'Set maximum value in seekbar  ' + "'" + tsp.custname + "'"+ '.'
        def setmidvalue():
            return 'Set mid value in seekbar  ' + "'" + tsp.custname + "'"+ '.'
        def setminvalue():
            return 'Set minimum value in seekbar  ' + "'" + tsp.custname + "'"+ '.'
        def verifytext():
            return 'Verify ' + input + ' is the the text in the '+ "'" + tsp.custname + "'"+ '.'
        def gettextboxlength():
            return 'Get length from the '+ "'" + tsp.custname + "'"+ ' and save the length '+output+'in'+output_list+ '.'
        def verifytextboxlength():
            return 'Verify ' + input + ' is the length of textbox '+ "'" + tsp.custname + "'"+ '.'

        #dropdown keywords
        def getvaluebyindex():
            return 'Get value with index ' + input + ' in the '+ "'" + tsp.custname + "'" + ' and save the value ' + output + ' in '+ output_list
        def getselectedvalue():
            return 'Get Selected value of '+ "'" + tsp.custname + "'"+ ' and save value ' + output + ' in '+ output_list+ '.'
        def verifyselectedvalue():
            return 'Verify value ' + input + ' are selected in the '+ "'" + tsp.custname + "'"+'.'
        def selectvaluebytext():
            return 'Select value by text '+input+' of the '+ 'type '+ "'" + tsp.custname + "'" +' with the element '+input+' present in the table cell '+"'" + tsp.custname + "'"+'-['+ input + ']['+ input +']'
        def getmultiplevaluesbyindexes():
            return 'Get values with indexes ' + input + ' in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output + ' in  '+ tsp.outputval

        def getallvalues():
            return 'Get all the values present in the '+"'"+tsp.custname+"' and save the values '"+ output + ' in ' + "'" + tsp.outputval + "' ."
        def verifyallvalues():
            return 'Verify values ' + input + ' are present in the '+ "'" + tsp.custname + "'"


        def verifycount():
            return 'Verify ' + input + ' is the list count of the ' +"'" + tsp.custname + "'"

        def selectvaluebyindex():
            return ' Select value with index value '+ input+' in the '+"'" + tsp.custname + "'"
        def getcount():
            return 'Get the count of values in the '+ "'" + tsp.custname + "'"+ ' and save the count ' + output + ' in ' +output_list
        def getviewbyindex():
            return 'Get View with index ' + input + ' in the '+ "'" + tsp.custname + "'" + ' and save the value ' + output + ' in '+ output_list
        def getselectedviews():
            return 'Get Selected value of '+ "'" + tsp.custname + "'"+ ' and save value ' + output + ' in '+output_list+ '.'
        def verifyselectedviews():
            return 'Verify value ' + input + ' are selected in the '+ "'" + tsp.custname + "'"+'.'
        def selectviewbytext():
            return 'Select value by text '+input+' of the '+ 'type '+ "'" + tsp.custname + "'" +' with the element '+input+' present in the table cell '+"'" + tsp.custname + "'"+'-['+ input + ']['+ input +']'
        def getmultipleviewsbyindexes():
            return 'Get values with indexes ' + input + ' in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output + ' in  '+ tsp.ouputval

        def getallviews():
            return 'Get all the views present in the '+"'"+tsp.custname+"' and save the values '"+ output + ' in ' + "'" + tsp.outputval + "' ."
        def verifyallviews():
            return 'Verify values ' + input + ' are present in the '+ "'" + tsp.custname + "'"
        def selectmultipleviewsbyindexes():
            return 'Select values ' + input + ' in the '+ "'" + "'" + tsp.custname + "'" + "'"

        def verifylistcount():
            return 'Verify ' + input + ' is the list count of the ' +"'" + tsp.custname + "'"

        def selectviewbyindex():
            return 'Select the value '+ input+' of the '+"'" + tsp.custname + "'"+' with the index '+input+' present in the table cell  '+"'" + tsp.custname + "'"+'-['+input+']['+input+']'
        def getlistcount():
            return 'Get the count of values in the '+ "'" + tsp.custname + "'"+ ' and save the count ' + output + ' in ' +output_list
        def selectmultipleviewsbytext():
            return 'Select values ' + input + 'in the '+ "'" + tsp.custname + "'"


        # dropdown keywords
        def getrowcount():
            return 'Get the count of cells in the table ' + "'" + tsp.custname + "'" + ' and save the count ' + output + ' in ' + output_list

        def verifyrowcount():
            return 'Verify ' + input + ' is the list count of the ' +"'" + tsp.custname + "'"

        def cellclick():
            return 'Click on the cell number ' + input + ' in the table ' +"'" + tsp.custname + "'"

        def getcellvalue():
            return "Get data from the cell number '" + input+ " in the table '" + tsp.custname + "'" +' and save the value ' + output + ' in ' + output_list

        def verifycellvalue():
            return "Verify data from the cell number '" + input+ " in the table '" + tsp.custname + "'"


        return locals()[keyword]()

    def web(self,keyword,tsp,inputval,input,output,con,reporting_obj):
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

        #Popup keywords
        def verifypopuptext():
            return ' Verify ' +"'"+ input+"'"+ '  is the Popup text '
        def verifydialogtext():
            return ' Verify '+ "'"+input +"'"+ ' is the text of Window Dialog '
        def dismisspopup():
            return 'Close the Popup'
        def acceptpopup():
            return 'Accept the Popup'
        def getpopuptext():
            return 'Get the text of the Popup and save the text '+"'" + output+"'"+ ' in ' + tsp.outputval
        def sendfunctionkeys():
            return 'Press ' + "'"+input+"'"+ ' key'
        #Textbox keywords
        def settext():
            return 'Enter text '+ "'"+input+"'"+ ' in the  ' + "'" + tsp.custname + "'"+ '.'
        def cleartext():
            return 'Clear text from the ' + "'" + tsp.custname + "'"
        def gettext():
            return 'Get text from the ' + "'" + tsp.custname + "'" + ' and save the text \'' +"'" + output +"'" + '\' in ' + tsp.outputval
        def gettextboxtength():
            return 'Get length from the ' + "'" + tsp.custname + "'" + ' and save the length \'' + output + '\' in ' + tsp.outputval
        def verifytext():
            return 'Verify ' + "'"+input +"'"+ ' is the the text in the '+ "'" + tsp.custname + "'"
        def sendvalue():
            return ' Enter value ' + "'"+input+"'"+' in the '+ "'" + tsp.custname + "'"
        def verifytextboxlength():
            return 'Verify ' +"'"+ input + "'"+' is the length of textbox '+ "'" + tsp.custname + "'"
        def setsecuretext():
            return 'Enter secure text ' +"'"+input+"'"+ ' in the  ' + "'" + tsp.custname + "'"
        def sendsecurevalue():
            return 'Enter secure value ' +"'"+input+"'"+ ' in the  ' + "'" + tsp.custname + "'"

        def iossendkey():
            return 'Press '+"'"+input+"'"+" Key"




        #Image keywords
        def verifywebimages():
            return ' Compare images '+ "'" + tsp.custname + "'" + ' and ' + input

        #dropdown keywords
        def getselected():
            return 'Get Selected value of '+ "'" + tsp.custname + "'"+ ' and save value ' + output + ' in '+ tsp.outputval
        def selectmultiplevaluesbytext():
            return 'Select values ' +"'"+ input +"'"+ ' in the '+ "'" + tsp.custname + "'"
        def deselectall():
            return 'Deselect all values in the '+ "'" + tsp.custname + "'"
        def getvaluebyindex():
            return 'Get value with index ' +"'"+ input +"'"+' in the '+ "'" + tsp.custname + "'" + ' and save the value ' + output + ' in '+ tsp.outputval
        def verifyvaluesexists():
            return 'Verify values ' +"'"+ input +"'"+ ' exists in the '+ "'" + tsp.custname + "'"
        def selectvaluebytext():
            if tsp.custname=="@Custom":
                return 'Select text '+"'" +input+"'" +' with visible text '+"'" +visible_text+"'" +' of the type '+"'" +ele_type+"'" +' with the index '+"'" +cust_index+"'" +' present in '+ "'" + tsp.custname + "'"
            else:
                return 'Select value '+"'"+input+"'"+' in ' + tsp.custname
        def getmultiplevaluesbyindexes():
            return 'Get values with indexes ' +"'"+ input +"'"+ ' in the '+ "'" + tsp.custname + "'"+ ' and save the value ' + output + ' in  '+ tsp.outputval
        def verifyselectedvalue():
            return 'Verify value ' +"'"+ input +"'"+ ' are selected in the '+ "'" + tsp.custname + "'"
        def verifyselectedvalues():
            return 'Verify values ' +"'"+ input +"'"+ ' are selected in the '+ "'" + tsp.custname + "'"
        def getallvalues():
            return 'Get all the values present in the '+"'"+tsp.custname+"' and save the values '"+ output + ' in ' + "'" + tsp.outputval + "' ."
        def verifyallvalues():
            return 'Verify values ' +"'"+ input +"'"+ ' are present in the '+ "'" + tsp.custname + "'"
        def selectmultiplevaluesbyindexes():
            return 'Select values with index values ' +"'"+ input +"'"+ ' in the '+ "'" + tsp.custname + "'"
        def selectallvalues():
            return 'Select all values in the ' +"'" + tsp.custname + "'"
        def verifycount():
            return 'Verify ' +"'"+ input +"'"+ ' is the list count of the ' +"'" + tsp.custname + "'"
        def verifyselectedvalue():
            return 'Verify value ' +"'"+ input +"'"+ ' is selected in the ' +"'" + tsp.custname + "'"
        def selectvaluebyindex():
            if tsp.custname=="@Custom":
                return 'Select value '+"'" +input+"'" +' with visible text '+"'" +visible_text+"'" +' of the type '+"'" +ele_type+"'" +' with the index '+"'" +cust_index+"'" +' present in '+ "'" + tsp.custname + "'"
            else:
                return ' Select value with index value '+"'"+ input+"'"+' in the '+"'" + tsp.custname + "'"
        def getcount():
            return 'Get the count of values in the '+ "'" + tsp.custname + "'"+ ' and save the count ' + output + ' in ' +tsp.outputval
        #Radio checkbox keywords
        def selectradiobutton():
            return 'Select '+ "'" + tsp.custname + "'"
        def getstatus():
            return 'Get the status of the ' + "'" + tsp.custname + "'"+ ' and save the status ' + output + ' in '+ tsp.outputval
        def selectcheckbox():
            return 'Select '+ "'" + tsp.custname + "'"
        def unselectcheckbox():
            return 'Unselect '+ "'" + tsp.custname + "'"

        #Browser keywords
        def openbrowser():
            return ' Open ' + reporting_obj.browser_type+ ' browser'
        def opennewbrowser():
            return 'Open new instance of the browser'
        def maximizebrowser():
            return 'Maximize the browser ' +input
        def closebrowser():
            return 'Close the browser '
        def navigatetourl():
            return 'Open url ' +"'"+ input+"'"+ ' in the browser'
        def navigateforward():
            return 'Navigate forward in the browser'
        def navigatewithauthenticate():
            return ' Open url ' +"'"+input[0]+"'"+' with '+"'"+input[1]+"' and '"+input[2] +"' in the browser."
        def navigateback():
            return 'Navigate back in the browser'
        def verifytextexists():
            return 'Verify ' +"'"+ input + "'"+' exist and Number of occurance of the text ' +"'"+ input + "'"+' is '+ output +' time(s).'
        def getcurrenturl():
            return 'Get current url of the web page and save the URL '+ output + ' in '+ tsp.outputval
        def verifycurrenturl():
            return ' Verify url '+"'"+ input +"'"+ ' is the current url of the web page'
        def verifypagetitle():
            return 'Verify ' + "'"+input+"'"+ ' is the page title of the web page'
        def getpagetitle():
            return 'Get the title of the web page and save the title '+ output + ' in '+ tsp.outputval
        def closesubwindows():
            if input =="All":
                return "Closed All sub windows"
            else:
                return 'Closed the current sub window.'
        def opennewtab():
            return 'Open new tab in the current browser'
        def clearcache():
            return 'Clear the cache of browser'
        def refresh():
            return 'Refresh the web page'

        #Element keywords
        def gettooltiptext():
            return 'Get the tool tip from the '+ "'" + tsp.custname + "'"+ ' and save the tool tip text ' +"'"+output+"'"+ ' in ' + tsp.outputval
        def verifytooltiptext():
            return 'Verify ' +"'"+ input +"'"+ ' is the tooltip of  '+ "'" + tsp.custname + "'"
        def clickelement():
            return ' Click '+ "'" + tsp.custname + "'"
        def mouseclick():
            return ' Mouse Click on  '+ "'" + tsp.custname + "'"
        def verifyelementtext():
            return 'Verify ' +"'"+ input +"'"+ ' is the text of the '+ "'" + tsp.custname + "'"
        def verifyelementexists():
            return ' Verify '+ "'" + tsp.custname + "'" + ' exists '
        def getelementtext():
            return 'Get the text of the element '+ "'" + tsp.custname + "'"+ ' and save the value  '+"'"+ output +"'"+ ' in '+ tsp.outputval
        def verifydoesnotexists():
            return ' Verify '+ "'" + tsp.custname + "'" + '  does not exists '
        def tab():
            return 'Perform tab on '+ "'" + tsp.custname + "'"

        def rightclick():
            return 'Perform right click on element '+ "'" + tsp.custname + "'"
        def doubleclick():
            return 'Double click on the '+ "'" + tsp.custname + "'"
        def waitforelementvisible():
            return 'Wait until the element '+ "'" + tsp.custname + "'" +'is visible'
        def dropfile():
            return 'Drop file executed'

        #Button link keywords
        def click():
            return ' Click on the '+ "'" + tsp.custname + "'"
        def cellclick():
            return 'Click ' + "'" + tsp.custname + "'"
        def verifybuttonname():
            return 'Verify text ' +"'"+ input +"'"+ ' is the name of the '+ "'" + tsp.custname + "'"
        def uploadfile():
            return ' Upload the file  present in the path ' +"'" + input + "'" +'.'
        def getlinktext():
            return ' Get Text From '+ "'" + tsp.custname + "'" + ' and save the text '+ output + ' in ' + tsp.outputval
        def getbuttonname():
            return ' Get ButtonName From '+ "'" + tsp.custname + "'" + ' and save the text '+ output + ' in ' + tsp.outputval
        def verifylinktext():
            return 'Verify text ' + "'"+input +"'"+ ' is the name of the ' +"'" + tsp.custname + "'"

        #utilweb operations
        def verifyreadonly():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is read-only'
        def verifyenabled():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is enabled '
        def verifydisabled():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is disabled '
        def verifyexists():
            return ' Verify '+ "'" + tsp.custname + "'" + '  exists '
        def verifyhidden():
            return ' Verify '+ "'" + tsp.custname + "'" + ' is Hidden '
        def verifyvisible():
            return 'Verify '+ "'" + tsp.custname + "'" + ' is Visible '
        def mousehover():
            return ' Move mouse pointer to '+ "'" + tsp.custname + "'"
        def setfocus():
            return ' Set the focus on '+ "'" + tsp.custname + "'"
        def press():
            return 'Press on the '+ "'" + tsp.custname + "'"
        def drag():
            return 'Perform drag on element '+ "'" + tsp.custname + "'"
        def drop():
            return 'Perform drop on element '+ "'" + tsp.custname + "'"
        def selectbyabsolutevalue():
            return 'Select value with exact text'+"'" +input + "'"+ ' present in the '+ "'" + tsp.custname + "'"
        def switchtowindow():
            return 'Control switched to window '+"'"+input+"'"

        #Table keywords
        def getcelltooltip():
            return 'Get the cell tooltip from the '+ "'" + tsp.custname + "'"+ ' and save the tool tip text ' + output+ ' in ' + tsp.outputval
        def cellclick():
            return 'Click ' + "'" + tsp.custname + "'"
        def getrowcount():
            return 'Get row count of the ' + "'" + tsp.custname + "'" + ' and save the count ' + output + ' in '+ tsp.outputval
        def getcolumncount():
            return 'Get column count of the '+ "'" + tsp.custname + "'"+ ' and save the count '+ output + ' in '+ tsp.outputval
        def verifycellvalue():
            return 'Verify cell value [Null] is present in the '+ "'" + tsp.custname + "'" + ' Invalid input'

        def getcolnumbytext():
            return 'Get column number of ' + "'" + tsp.custname + "'" + ' by text '+"'"+input +"'"+' and save the column number ' +"'"+ output + "'"+' in '+ tsp.outputval
        def getrownumbytext():
            return 'Get row number of ' + "'" + tsp.custname + "'" + ' by text '+"'"+input +"'"+' and save the row number ' +"'"+output +"'"+ ' in '+ tsp.outputval
        def getcellvalue():
            return 'Get row number of ' + "'" + tsp.custname + "'" + ' by text '+"'"+input +"'"+' and save the row number ' +"'"+output +"'"+ ' in '+ tsp.outputval

        #custom keyword
        def getobjectcount():
            return 'Get Object count of the type '+"'" +ele_type+"'" +' and save the count '+"'" +output+"'" +' in '+"'"+tsp.outputval+"'"


        return locals()[keyword]()


# Start of Mainframe Keyword Reporting
#==========================================================================================================#

    def mainframe(self,keyword,tsp,inputval,input,output,con,reporting_obj):
        #-----------------------------------Added this step as input was returned as a string
        listInput = input
        if type(input) is str:                  #----checking if input is a string
            if "," in input:                    #----checking if the string has a ","
                listInput = input.split(",")        #--------spliting the input by checking for "," then store the result in list input
        def launchmainframe():
            print input
            if len(listInput) == 2:
                return "Launch Mainframe through emulator '" + listInput[1] + "' present in the path '" + listInput[0] +"'"
            else:
                return "Launch mainframe failed due to insufficient parameter(s)"

        def login():
            if len(listInput) == 3:
                return "Login to the Mainframe using Region : '"+listInput[0] + "' UserID : '"+listInput[1] + "' and Password : '"+listInput[2] + "'"
            else:
                return "Login failed due to insufficient parameter(s)"

        def securelogin():
            if len(listInput) == 3:
                return "Login to the Mainframe using Region : '"+listInput[0] + "' UserID : '"+listInput[1] + "' and Password : '"+listInput[2] + "'"
            else:
                return "SecureLogin failed due to insufficient parameter(s)"

        def logoff():
            if input is not None:
                return "Logoff from Mainframe using option'"+input +"'"
            else:
                return "Logoff failed due to insufficient parameter(s)"

        def sendvalue():
            if input is not None:
                return "Enter value : '" + input + "'"
            else:
                return "SendValue failed due to insufficient parameter(s)"

        def submitjob():
            if len(listInput) == 2:
                return "Submit the job present in file : '" + listInput[0] + "' with member name '" + listInput[1] + "'"
            else:
                return "SubmitJob failed due to insufficient parameter(s)"
        def jobstatus():
            if input is not None:
                return "Status of the Job with the Job ID : '" + input + "'" + "is '" + output + "'"
            else:
                return "JobStatus failed due to insufficient parameter(s)"

        def sendfunctionkeys():
            if input is not None:
                return "Execute Function key  : '" + listInput[0] + "'"
            else:
                return "SendFunctionKeys failed due to insufficient parameter(s)"

        def gettext():
            if len(listInput) == 3:
                return "Get the text from row  : '" + listInput[0] + "'" + " column :'"+listInput[1] + "' of length : '" + listInput[2] +"' and store the text '" + output + "' in " + tsp.outputval
            else:
                return "GetText failed due to insufficient parameter(s)"

        def settext():
            if len(listInput) == 3:
                return "Enter the text '"+ listInput[2] + "' at row  : '" + listInput[0] + "'" + " column :'"+listInput[1] + "'"
            else:
                return "SetText failed due to insufficient parameter(s)"

        def setcursor():
            if len(listInput) == 2:
                return "Set the cursor at at row  : '" + listInput[0] + "'" + " column :'"+listInput[1] + "'"
            else:
                return "SetCursor failed due to insufficient parameter(s)"

        def verifytextexists():
            if input is not None:
                return "Verify text : '" + input + "' present in Emulator screen "
            else:
                return "VerifyTextExists failed due to insufficient parameter(s)"
        return locals()[keyword]()

#==========================================================================================================#
#End of Mainframe Keyword Reporting starts
