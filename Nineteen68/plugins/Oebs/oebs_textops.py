#-------------------------------------------------------------------------------
# Name:        oebs_textops.py
# Purpose:     keywords in this script enables to perform action on text Objects.
#
# Author:      sushma.p
#
# Created:     24-10-2016
# Copyright:   (c) yesubabu.d,vishvas.a2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from oebs_msg import *
import logging
import oebs_key_objects
import winuser
import win32api
import win32com.client
import oebs_mouseops
import oebs_keyboardops
import oebs_serverUtilities
from oebs_utilops import UtilOperations
import time

shell = win32com.client.Dispatch("WScript.Shell")

class TextOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()
        self.utilops_obj=UtilOperations()
        self.keywordops_obj=oebs_keyboardops.KeywordOperations()

    #Method to get Text of the given Object location
    def gettext(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        #this is the response obtained from the keyword
        keywordresponse=''
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_TEXTOPS,DEF_GETTEXT)
            #checks element is accessible
            if charinfo.accessibleText == 1:
                if 'enabled' in charinfo.states:
                    logging.debug('FILE: %s , DEF: %s MSG: Text Box is accessible',OEBS_TEXTOPS,DEF_GETTEXT)
                    #gets the text information
                    charinfo = acc.getAccessibleTextInfo(0,1)
                    #fetches text from 0th to nth location
                    text = acc.getAccessibleTextRange(0,charinfo.charCount - 1)
                    logging.debug('FILE: %s , DEF: %s MSG: Text Box text is %s',OEBS_TEXTOPS,DEF_GETTEXT,text)
                    #sets the result to pass
                    keywordresult=MSG_PASS
                    logging.debug('FILE: %s , DEF: %s MSG: Result:%s',OEBS_TEXTOPS,DEF_GETTEXT,text)
                    keywordresponse = text
                    oebs_key_objects.custom_msg.append("MSG_RESULT_IS")
                else:
                    logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_GETTEXT,MSG_DISABLED_OBJECT)
                    oebs_key_objects.custom_msg.append("ERR_OBJECT_DISABLED")
            else:
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_TEXTOPS,DEF_GETTEXT,MSG_INVALID_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_OBJECT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_TEXTOPS,DEF_GETTEXT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_TEXTOPS,DEF_GETTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_TEXTOPS,DEF_GETTEXT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(keywordresponse))

    #Method to settext at the given Object location
    def settext(self,acc):

        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        #this is the response obtained from the keyword
        keywordresponse=MSG_FALSE
        try:
            #gets the entire context information
            time.sleep(3)
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_TEXTOPS,DEF_SETTEXT)
            if 'enabled' in curaccinfo.states:
                #checks whether action can be performed on the object
                if curaccinfo.accessibleAction == 1:
                    #checks whether text object editable
                    if 'editable' in curaccinfo.states:
                        logging.debug('FILE: %s , DEF: %s MSG: Text Box is accessible',OEBS_TEXTOPS,DEF_SETTEXT)
                        #checks element is accessible
                        if curaccinfo.accessibleText == 1:
                            if len(oebs_key_objects.keyword_input) == 1:
                                #checks if the text is empty
                                if (oebs_key_objects.keyword_input[0] != ''):
                                    text=oebs_key_objects.keyword_input[0]
                                    logging.debug('FILE: %s , DEF: %s MSG: Text to be set is %s',OEBS_TEXTOPS,DEF_SETTEXT,text)
                                    #if text != None:
                                    #gets the full length of the text
                                    character=acc.getAccessibleTextInfo(0,1)
                                    #sets the text value to the object
                                    result = acc.setTextContents(text)
                                    if result:
                                        #sets the result to pass
                                        keywordresult=MSG_PASS
                                        keywordresponse=MSG_TRUE
                                else:
                                    logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_SETTEXT,MSG_INVALID_INPUT)
                                    oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
                            else:
                                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_SETTEXT,MSG_INVALID_NOOF_INPUT)
                                oebs_key_objects.custom_msg.append("ERR_INVALID_NO_INPUT")
                        else:
                            logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_SETTEXT,MSG_INVALID_OBJECT)
                            oebs_key_objects.custom_msg.append("ERR_INVALID_OBJECT")
                    else:
                        logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_SETTEXT,MSG_OBJECT_READONLY)
                        oebs_key_objects.custom_msg.append(MSG_OBJECT_READONLY)
                else:
                    #gets the entire context information
                    curaccinfo = acc.getAccessibleContextInfo()
                    logging.debug('FILE: %s , DEF: %s MSG: Text Box is accessible',OEBS_TEXTOPS,DEF_SETTEXT)
                    x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
                    y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
                    logging.debug('FILE: %s , DEF: %s MSG: Text Box is accessible',OEBS_TEXTOPS,DEF_SETTEXT)
                    if len(oebs_key_objects.keyword_input) == 1:
                        #if text != None:
                        if (oebs_key_objects.keyword_input[0] != ''):
                            text=oebs_key_objects.keyword_input[0]
                            index = len(text)
                            logging.debug('FILE: %s , DEF: %s MSG: Text to be set is %s',OEBS_TEXTOPS,DEF_SETTEXT,text)
                            #Visibility check for scrollbar
                            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
                                oebs_mouseops.MouseOperation('click',x_coor,y_coor)

                                #code added to gain the FOCUSED state for the textbox
                                for mouseindex in range(3):
                                    curaccinfo = acc.getAccessibleContextInfo()
                                    if 'focused' in curaccinfo.states:
                                        break
                                    else:
                                        time.sleep(3)

                                #checks whether text object editable
                                if 'editable' in curaccinfo.states:
                                    #code enables to check the status of the mouse
                                    #periodically for 10 sec(max)
                                    #mkes the count value 1 once mouse is active

                                    #Commenting a code waiting for 10 sec in setText operation

                                    mousestate=oebs_mouseops.GetCursorInfo('state')
                                    while(mousestate == 65543):
                                         mousestate=oebs_mouseops.GetCursorInfo('state')


                                    if 'focused' in curaccinfo.states:
                                        #gets the full length of the text
                                        character=acc.getAccessibleTextInfo(0,1)

                                        self.keywordops_obj.KeyboardOperation('keypress','HOME')
                                        #clears the text untill all characters are deleted
                                        for num in range(character.charCount):
                                            shell.SendKeys("{DELETE}")


                                        #sets the text value to the object
                                        for length in range(index):
                                            shell.SendKeys('{'+text[length]+'}')
                                            #sets the result to pass;
                                            keywordresult=MSG_PASS
                                            keywordresponse=MSG_TRUE
                                    else:
                                        logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_SETTEXT,MSG_ELEMENT_NON_EDITABLE)
                                        oebs_key_objects.custom_msg.append(MSG_ELEMENT_NON_EDITABLE)

                                else:
                                    logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_SETTEXT,MSG_OBJECT_READONLY)
                                    oebs_key_objects.custom_msg.append(MSG_OBJECT_READONLY)
                            else:
                                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_SETTEXT,MSG_ELEMENT_NOT_VISIBLE)
                                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
                        else:
                            logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_SETTEXT,MSG_INVALID_INPUT)
                            oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
                    else:
                        logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_SETTEXT,MSG_INVALID_NOOF_INPUT)
                        oebs_key_objects.custom_msg.append("ERR_INVALID_NO_INPUT")
            else:
                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_SETTEXT,MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_DISABLED_OBJECT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_TEXTOPS,DEF_SETTEXT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_TEXTOPS,DEF_SETTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_TEXTOPS,DEF_SETTEXT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(keywordresponse))

   #Method to verifytext of the given Object location matches with the User Provided Text
    def verifytext(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        try:
            #sets the verifyresponse to FALSE
            verifyresponse = MSG_FALSE
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_TEXTOPS,DEF_VERIFYTEXT)
            #checks element is accessible
            if curaccinfo.accessibleText == 1:
                if len(oebs_key_objects.keyword_input) == 1:
                    textVerify=oebs_key_objects.keyword_input[0]
                    if (textVerify != None and textVerify != 0 ):
                        #gets the text information
                        character=acc.getAccessibleTextInfo(0,1)
                        #fetches text from 0th to nth location
                        fetchedText = acc.getAccessibleTextRange(0,character.charCount - 1)
                        #checks the user provided text with the text in the object
                        if fetchedText == textVerify:
                            logging.debug('FILE: %s , DEF: %s MSG: Text verified',OEBS_TEXTOPS,DEF_VERIFYTEXT)
                            #sets the verifyresponse to TRUE
                            verifyresponse = MSG_TRUE
                             #sets the keywordresult to pass
                            keywordresult=MSG_PASS
                        else:
                            logging.debug('FILE: %s , DEF: %s MSG: Text verification failed',OEBS_TEXTOPS,DEF_VERIFYTEXT)
                            oebs_key_objects.custom_msg.append(str('Text verification failed \'' + fetchedText + '\' not equal to \''+textVerify+"\'."))
                    else:
                        logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_VERIFYTEXT,MSG_INVALID_INPUT)
                        oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
                else:
                    logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_VERIFYTEXT,MSG_INVALID_NOOF_INPUT)
                    oebs_key_objects.custom_msg.append("ERR_INVALID_NO_INPUT")
            else:
                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_VERIFYTEXT,MSG_INVALID_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_INVALID_OBJECT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_TEXTOPS,DEF_VERIFYTEXT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_TEXTOPS,DEF_VERIFYTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_TEXTOPS,DEF_VERIFYTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Verify Response %s',OEBS_TEXTOPS,DEF_VERIFYTEXT,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))



    #Method to cleartext of the given Object location matches with the User Provided Text
    def cleartext(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        #this is the response obtained from the keyword
        verifyresponse=MSG_FALSE
        try:
            time.sleep(3)
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_TEXTOPS,DEF_CLEARTEXT)
            if 'enabled' in curaccinfo.states:
                #checks whether an action can be performed on the object
                if curaccinfo.accessibleAction == 1:
                    if 'editable' in curaccinfo.states:
                        # formula for changing co-ordinates to center of the element
                        x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
                        y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
                        logging.debug('FILE: %s , DEF: %s MSG: Formula Created',OEBS_TEXTOPS,DEF_CLEARTEXT)
                        #checks element is accessible
                        if curaccinfo.accessibleText == 1:
                            #sets the text to empty
                            text=''
                            #sets the text value to the object
                            result = acc.setTextContents(text)
                            if result:
                                #sets the result to pass
                                keywordresult=MSG_PASS
                                verifyresponse=MSG_TRUE
                                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_CLEARTEXT,MSG_TEXTBOX_CLEARED)
                        else:
                            logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_CLEARTEXT,MSG_INVALID_OBJECT)
                            oebs_key_objects.custom_msg.append(MSG_INVALID_OBJECT)
                    else:
                        logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_CLEARTEXT,MSG_OBJECT_READONLY)
                        oebs_key_objects.custom_msg.append(MSG_OBJECT_READONLY)
                else:
                    if 'editable' in curaccinfo.states:
                        x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
                        y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
                        logging.debug('FILE: %s , DEF: %s MSG: Formula Created',OEBS_TEXTOPS,DEF_CLEARTEXT)
                        text=''
                        if text != None:
                            #Visibility check for scrollbar
                            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
                                oebs_mouseops.MouseOperation('click',x_coor,y_coor)

                                #code added to gain the FOCUSED state for the textbox
                                for mouseindex in range(3):
                                    curaccinfo = acc.getAccessibleContextInfo()
                                    if 'focused' in curaccinfo.states:
                                        break
                                    else:
                                        time.sleep(3)

                                #checks whether text object editable
                                if 'editable' in curaccinfo.states:
                                    #code enables to check the status of the mouse
                                    #periodically for 10 sec(max)
                                    #mkes the count value 1 once mouse is active
                                    count=0
                                    for mouseindex in range(20):
                                        mousestate=oebs_mouseops.GetCursorInfo('state')
                                        #65543 stands for STATE of mouse to be WAIT
                                        if mousestate == 65543:
                                            time.sleep(0.5)
                                        else:
                                            count=1
                                            break

                                    if count == 1:
                                        if 'focused' in curaccinfo.states:
                                            #gets the full length of the text
                                            character=acc.getAccessibleTextInfo(0,1)
                                            self.keywordops_obj.KeyboardOperation('keypress','HOME')
                                            #clears the text until all characters are deleted
                                            for num in range(character.charCount):
                                                shell.SendKeys("{DELETE}")
                                            logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_CLEARTEXT,MSG_TEXTBOX_CLEARED)
                                            #sets the result to pass
                                            keywordresult=MSG_PASS
                                            verifyresponse=MSG_TRUE
                                        else:
                                            logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_CLEARTEXT,MSG_ELEMENT_NOT_VISIBLE)
                                            oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_FOCUSABLE)
                                else:
                                    logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_CLEARTEXT,MSG_ELEMENT_NON_EDITABLE)
                                    oebs_key_objects.custom_msg.append(MSG_ELEMENT_NON_EDITABLE)
                            else:
                                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_CLEARTEXT,MSG_ELEMENT_NOT_VISIBLE)
                                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
                    else:
                        logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_CLEARTEXT,MSG_OBJECT_READONLY)
                        oebs_key_objects.custom_msg.append(MSG_OBJECT_READONLY)
            else:
                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_TEXTOPS,DEF_CLEARTEXT,MSG_DISABLED_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_OBJECT_DISABLED")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_TEXTOPS,DEF_CLEARTEXT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_TEXTOPS,DEF_CLEARTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_TEXTOPS,DEF_CLEARTEXT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))
