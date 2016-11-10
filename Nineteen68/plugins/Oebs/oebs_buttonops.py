#-------------------------------------------------------------------------------
# Name:        oebs_buttonops.py
# Purpose:     This file contains code to perform operations on button object.
#
# Author:      sushma.p
#
# Created:     24-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import oebs_api
from oebs_msg import *
import oebs_msg
import oebs_mouseops
import oebs_key_objects
import oebsServer
import logging
import oebs_serverUtilities
from oebs_utilops import UtilOperations


class ButtonOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()
        self.utilops_obj=UtilOperations()

    #Method to get button name of the given Object/XPATH
    def getbuttonname(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL;
        keywordresponse=''
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_BUTTONOPS,DEF_GETBUTTONNAME)
            if charinfo.accessibleAction == 1:
                if (charinfo.name != None and charinfo.name != ''):
                    buttonName = charinfo.name
                    logging.debug('FILE: %s , DEF: %s MSG: %s %s',OEBS_BUTTONOPS,DEF_GETBUTTONNAME,MSG_RESULT_IS,buttonName)
                    keywordresult=MSG_PASS
                    keywordresponse = buttonName
                    oebs_key_objects.custom_msg.append(str(MSG_RESULT_IS + keywordresponse))
                else:
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_BUTTONOPS,DEF_GETBUTTONNAME,MSG_NAME_NOT_DEFINED)
                    oebs_key_objects.custom_msg.append(MSG_NAME_NOT_DEFINED)
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_BUTTONOPS,DEF_GETBUTTONNAME,MSG_INVALID_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_OBJECT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_BUTTONOPS,DEF_GETBUTTONNAME,e)
        logging.debug('FILE: %s , DEF: %s MSG: Result %s',OEBS_BUTTONOPS,DEF_GETBUTTONNAME,keywordresponse)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_BUTTONOPS,DEF_GETBUTTONNAME,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(keywordresponse))


    #Method to verify button name of the given Object/XPATH matches with the User Provided Text
    def verifybuttonname(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_BUTTONOPS,DEF_VERIFYBUTTONNAME)
            if charinfo.accessibleAction == 1:
                nameVerify=oebs_key_objects.keyword_input[0]
                logging.debug('FILE: %s , DEF: %s MSG: Name Received %s',OEBS_BUTTONOPS,DEF_VERIFYBUTTONNAME,nameVerify)
                fetchedText=''
                if (nameVerify != None and nameVerify != '' ):
                    if (charinfo.name != None and charinfo.name != ''):
                        fetchedText = charinfo.name
                        if 'alt' in fetchedText:
                             splitval=fetchedText.split("alt",1)[0]
                        elif 'ALT' in fetchedText:
                             splitval=fetchedText.split("ALT",1)[0]
                        else:
                            splitval=fetchedText
                        buttonname = splitval.strip()
                        keywordresponse=buttonname
                        if buttonname == nameVerify:
                            logging.debug('FILE: %s , DEF: %s MSG: Button names matched',OEBS_BUTTONOPS,DEF_VERIFYBUTTONNAME)
                            verifyresponse = MSG_TRUE
                            keywordresult=MSG_PASS
                        else:
                            logging.debug('FILE: %s , DEF: %s MSG: Button names mismatched',OEBS_BUTTONOPS,DEF_VERIFYBUTTONNAME)
                            oebs_key_objects.custom_msg.append(str('Button names mismatched. Expected:' + nameVerify + ' ; Actual:'+buttonname))
                    else:
                        logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_BUTTONOPS,DEF_GETBUTTONNAME,MSG_NAME_NOT_DEFINED)
                        oebs_key_objects.custom_msg.append(MSG_NAME_NOT_DEFINED)
                else:
                    logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_BUTTONOPS,DEF_VERIFYBUTTONNAME,MSG_INVALID_INPUT)
                    oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
            else:
                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_BUTTONOPS,DEF_VERIFYBUTTONNAME,MSG_INVALID_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_OBJECT")
        except Exception as e:
            self.utilities_obj.cleardata()
       	    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_BUTTONOPS,DEF_VERIFYBUTTONNAME,e)
            logging.debug('FILE: %s , DEF: %s MSG: Result %s',OEBS_BUTTONOPS,DEF_VERIFYBUTTONNAME,keywordresult)
       	logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_BUTTONOPS,DEF_VERIFYBUTTONNAME,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))



    #Method to perform click operation
    def click(self,acc):
        del oebs_key_objects.custom_msg[:]
     	#sets the keywordResult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_BUTTONOPS,DEF_CLICK)
            objstates = charinfo.states
            x_coor = int(charinfo.x + (0.5 * charinfo.width))
            y_coor = int(charinfo.y + (0.5 * charinfo.height))
            #Visibility check for scrollbar
            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
                #check for object enabled
                if 'enabled' in objstates:
                    logging.debug('FILE: %s , DEF: %s MSG: Click Happens on :%s , %s',OEBS_BUTTONOPS,DEF_CLICK,x_coor,y_coor)
                    oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                    logging.debug('FILE: %s , DEF: %s MSG: Click Successful',OEBS_BUTTONOPS,DEF_CLICK)
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                else:
                    logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_BUTTONOPS,DEF_CLICK,MSG_DISABLED_OBJECT)
                    oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")
            else:
                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_CLICK,MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_BUTTONOPS,DEF_CLICK,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_BUTTONOPS,DEF_CLICK,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_BUTTONOPS,DEF_CLICK,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

    #Method to perform doubleclick operation
    def doubleclick(self,acc):
        del oebs_key_objects.custom_msg[:]
    	#sets the keywordResult to FAIL
        keywordresult=MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            print 'charinfo',charinfo.name
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_BUTTONOPS,DEF_DOUBLECLICK)
            objstates = charinfo.states
            x_coor = int(charinfo.x + (0.5 * charinfo.width))
            y_coor = int(charinfo.y + (0.5 * charinfo.height))
            #Visibility check for scrollbar
            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
                #check for object enabled
                if 'enabled' in objstates:
                    logging.debug('FILE: %s , DEF: %s MSG: Double Click Happens on :%s , %s',OEBS_BUTTONOPS,DEF_DOUBLECLICK,x_coor,y_coor)
                    oebs_mouseops.MouseOperation('doubleClick',x_coor,y_coor)
                    logging.debug('FILE: %s , DEF: %s MSG: Double Click Successful',OEBS_BUTTONOPS,DEF_DOUBLECLICK)
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                else:
                    logging.debug('FILE: %s , DEF: %s MSG: Object Disabled',OEBS_BUTTONOPS,DEF_DOUBLECLICK,MSG_DISABLED_OBJECT)
                    oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")
            else:
                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_DOUBLECLICK,MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_TEXTOPS,DEF_DOUBLECLICK,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_TEXTOPS,DEF_DOUBLECLICK,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_TEXTOPS,DEF_DOUBLECLICK,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to get link text of the given Object location
    def getlinktext(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        #this is the response obtained from the keyword
        keywordresponse=''
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_BUTTONOPS,DEF_GETLINKTEXT)
            if(curaccinfo.role == 'text'):
                #gets the text information
                curaccinfo = acc.getAccessibleTextInfo(0,1)
                #fetches text from 0th to nth location
                linktext = acc.getAccessibleTextRange(0,curaccinfo.charCount - 1)
                logging.debug('FILE: %s , DEF: %s MSG: Text received is: %s',OEBS_BUTTONOPS,DEF_GETLINKTEXT,linktext)
                #sets the result to pass
                keywordresult=MSG_PASS
                logging.debug('FILE: %s , DEF: %s MSG: Result:%s',OEBS_BUTTONOPS,DEF_GETLINKTEXT,linktext)
                keywordresponse = linktext
                oebs_key_objects.custom_msg.append(str(MSG_RESULT_IS + keywordresponse))
            elif(curaccinfo.role == 'push button'):
                linktext = curaccinfo.name
                keywordresult=MSG_PASS
                logging.debug('FILE: %s , DEF: %s MSG: Result:%s',OEBS_BUTTONOPS,DEF_GETLINKTEXT,linktext)
                keywordresponse = linktext
                oebs_key_objects.custom_msg.append(str(MSG_RESULT_IS + keywordresponse))
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_BUTTONOPS,DEF_GETLINKTEXT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_BUTTONOPS,DEF_GETLINKTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_BUTTONOPS,DEF_GETLINKTEXT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(keywordresponse))

    #Method to verify link text of the given Object location
    def verifylinktext(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_BUTTONOPS,DEF_VERIFYLINKTEXT)
            if(curaccinfo.role == 'text'):
                #gets the text information
                curaccinfo = acc.getAccessibleTextInfo(0,1)
                #fetches text from 0th to nth location
                linktext = acc.getAccessibleTextRange(0,curaccinfo.charCount - 1)
                if len(oebs_key_objects.keyword_input) == 1:
                    verificationtext=oebs_key_objects.keyword_input[0]
                    logging.debug('FILE: %s , DEF: %s MSG: User provided text: %s',OEBS_BUTTONOPS,DEF_VERIFYLINKTEXT,verificationtext)
                    if (verificationtext != None and verificationtext != 0 ):
                        if verificationtext == linktext:
                            #sets the result to pass
                            keywordresult=MSG_PASS
                            verifyresponse=MSG_TRUE
                            logging.debug('FILE: %s , DEF: %s MSG: Verification result: %s',OEBS_BUTTONOPS,DEF_VERIFYLINKTEXT,verifyresponse)
                        else:
                            logging.debug('FILE: %s , DEF: %s MSG: Verification result: %s',OEBS_BUTTONOPS,DEF_VERIFYLINKTEXT,verifyresponse)
                            oebs_key_objects.custom_msg.append(str('Link names mismatched. Expected:' + linktext + " Obtained:"+verificationtext))
                else:
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_BUTTONOPS,DEF_VERIFYLINKTEXT,MSG_INVALID_INPUT)
                    oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
            elif(curaccinfo.role == 'push button'):
                linktext = curaccinfo.name
                if len(oebs_key_objects.keyword_input) == 1:
                    verificationtext=oebs_key_objects.keyword_input[0]
                    logging.debug('FILE: %s , DEF: %s MSG: User provided text: %s',OEBS_BUTTONOPS,DEF_VERIFYLINKTEXT,verificationtext)
                    if (verificationtext != None and verificationtext != 0 ):
                        if verificationtext == linktext:
                            #sets the result to pass
                            keywordresult=MSG_PASS
                            verifyresponse=MSG_TRUE
                            logging.debug('FILE: %s , DEF: %s MSG: Verification result: %s',OEBS_BUTTONOPS,DEF_VERIFYLINKTEXT,verifyresponse)
                        else:
                            logging.debug('FILE: %s , DEF: %s MSG: Verification result: %s',OEBS_BUTTONOPS,DEF_VERIFYLINKTEXT,verifyresponse)
                            oebs_key_objects.custom_msg.append(str('Link names mismatched. Expected:' + linktext + " Obtained:"+verificationtext))
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_BUTTONOPS,DEF_VERIFYLINKTEXT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_BUTTONOPS,DEF_VERIFYLINKTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_BUTTONOPS,DEF_VERIFYLINKTEXT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))