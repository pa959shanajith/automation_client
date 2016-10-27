#-------------------------------------------------------------------------------
# Name:        oebs_elementsops.py
# Purpose:     keywords in this script are used to perform dropdown and listbox operation.
#
# Author:      sushma.p
#
# Created:     24-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import oebs_api
from oebs_msg import *
import oebs_key_objects
import oebs_serverUtilities
import oebs_mouseops
import time
import logging
import winuser
import win32api
from oebs_utilops import UtilOperations

class ElementOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()
        self.utilops_obj=UtilOperations()

    #Method to perform click operation
    def clickelement(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordResult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_ELEMENTS,DEF_CLICKELEMENT)
            objstates = charinfo.states
            #x_coor = int(charinfo.x + (0.5 * charinfo.width))
            #y_coor = int(charinfo.y + (0.5 * charinfo.height))
            x_coor = int(charinfo.x + 25 )
            y_coor = int(charinfo.y + 10)
            #Visibility check for scrollbar
            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
            #check for object enabled
                if 'enabled' in objstates:
                    logging.debug('FILE: %s , DEF: %s MSG: Click Happens on :%s , %s',OEBS_ELEMENTS,DEF_CLICKELEMENT,x_coor,y_coor)
                    oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_ELEMENTS,DEF_CLICKELEMENT,MSG_CLICK_SUCCESSFUL)
                    oebs_key_objects.custom_msg.append(str(MSG_CLICK_SUCCESSFUL))
                else:
                    logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_ELEMENTS,DEF_CLICKELEMENT,MSG_DISABLED_OBJECT)
                    oebs_key_objects.custom_msg.append("ERR_OBJECT_DISABLED")
            else:
                logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_ELEMENTS,DEF_CLICKELEMENT,MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_ELEMENTS,DEF_CLICKELEMENT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_ELEMENTS,DEF_CLICKELEMENT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_ELEMENTS,DEF_CLICKELEMENT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to get element Text of the given Object location
    def getelementtext(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        #this is the response obtained from the keyword
        keywordresponse=''
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_ELEMENTS,DEF_GETELEMENTTEXT)
            objstates = charinfo.states
            #check for element hidden
            if 'hidden' in objstates:
                verifyresponse = MSG_FALSE
                keywordresult=MSG_FAIL
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_ELEMENTS,DEF_GETELEMENTTEXT,MSG_HIDDEN_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_HIDDEN_OBJECT")
            else:
                if (charinfo.name != None and charinfo.name !=''):
                    fetchedText = charinfo.name
                    if 'alt' in fetchedText:
                        splitval=fetchedText.split("alt",1)[0]
                    elif 'ALT' in fetchedText:
                        splitval=fetchedText.split("ALT",1)[0]
                    else:
                        splitval=fetchedText
                    elementtext = splitval.strip()
                    logging.debug('FILE: %s , DEF: %s MSG: element text is %s',OEBS_ELEMENTS,DEF_GETELEMENTTEXT,elementtext)
                    #sets the result to pass
                    keywordresult=MSG_PASS
                    logging.debug('FILE: %s , DEF: %s MSG: Result:%s',OEBS_ELEMENTS,DEF_GETELEMENTTEXT,elementtext)
                    keywordresponse = elementtext.encode('utf-8')
                    oebs_key_objects.custom_msg.append("MSG_RESULT_IS")
                else:
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_ELEMENTS,DEF_GETELEMENTTEXT,MSG_TEXT_NOT_DEFINED)
                    oebs_key_objects.custom_msg.append(MSG_TEXT_NOT_DEFINED)
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_ELEMENTS,DEF_GETELEMENTTEXT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_ELEMENTS,DEF_GETELEMENTTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_ELEMENTS,DEF_GETELEMENTTEXT,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(keywordresponse))


    #Method to verify element text of the given Object location matches with the User Provided Text
    def verifyelementtext(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        try:
            #sets the verifyresponse to FALSE
            verifyresponse = MSG_FALSE
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_ELEMENTS,DEF_VERIFYELEMENTTEXT)
            objstates = curaccinfo.states
            #check for element hidden
            if 'hidden' in objstates:
                verifyresponse = MSG_FALSE
                keywordresult=MSG_FAIL
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_ELEMENTS,DEF_GETELEMENTTEXT,MSG_HIDDEN_OBJECT)
                oebs_key_objects.custom_msg.append("ERR_HIDDEN_OBJECT")
            else:
                if len(oebs_key_objects.keyword_input) == 1:
                        textVerify=oebs_key_objects.keyword_input[0]
                        if (textVerify != None and textVerify != ''):
                            #gets the text information
                            if (curaccinfo.name != None and curaccinfo.name !=''):
                                fetchedText = curaccinfo.name
                                if 'alt' in fetchedText:
                                    splitval=fetchedText.split("alt",1)[0]
                                elif 'ALT' in fetchedText:
                                    splitval=fetchedText.split("ALT",1)[0]
                                else:
                                    splitval=fetchedText
                                elementtext = splitval.strip()
                                logging.debug('FILE: %s , DEF: %s MSG: element text is %s',OEBS_ELEMENTS,DEF_VERIFYELEMENTTEXT,elementtext)
                                #checks the user provided text with the text in the object
                                if elementtext == textVerify:
                                    logging.debug('FILE: %s , DEF: %s MSG: Text verified',OEBS_ELEMENTS,DEF_VERIFYELEMENTTEXT)
                                    #sets the verifyresponse to TRUE
                                    verifyresponse = MSG_TRUE
                                    #sets the keywordresult to pass
                                    keywordresult=MSG_PASS
                                else:
                                    logging.debug('FILE: %s , DEF: %s MSG: Text verification failed',OEBS_ELEMENTS,DEF_VERIFYELEMENTTEXT)
                                    oebs_key_objects.custom_msg.append(str('Text verification failed \'' + elementtext + '\' not equal to \''+textVerify+"\'."))
                            else:
                                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_ELEMENTS,DEF_VERIFYELEMENTTEXT,MSG_TEXT_NOT_DEFINED)
                                oebs_key_objects.custom_msg.append(MSG_TEXT_NOT_DEFINED)
                        else:
                            logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_ELEMENTS,DEF_VERIFYELEMENTTEXT,MSG_INVALID_INPUT)
                            oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
                else:
                    logging.debug('FILE: %s , DEF: %s MSG:%s',OEBS_ELEMENTS,DEF_VERIFYELEMENTTEXT,MSG_INVALID_NOOF_INPUT)
                    oebs_key_objects.custom_msg.append("ERR_INVALID_INPUT")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_ELEMENTS,DEF_VERIFYELEMENTTEXT,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_ELEMENTS,DEF_VERIFYELEMENTTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status %s',OEBS_ELEMENTS,DEF_VERIFYELEMENTTEXT,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Verify Response %s',OEBS_ELEMENTS,DEF_VERIFYELEMENTTEXT,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


    #Method to waitforelementvisible
    def waitforelementvisible(self,applicationname,objectname,keyword,inputs,outputs):
        acc = ''
        del oebs_key_objects.custom_msg[:]
        #sets the keywordResult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            logging.debug('FILE: %s , DEF: %s MSG: Received Object Context',OEBS_ELEMENTS,DEF_WAITFORELEMENTVISIBLE)
            #geting mouse state
            mousestate=oebs_mouseops.GetCursorInfo('state')
            while(mousestate == 65543):
                mousestate=oebs_mouseops.GetCursorInfo('state')
            acc =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if(acc):
                charinfo = acc.getAccessibleContextInfo()
                objstates = charinfo.states
                #check for object visible
                if(('showing' in objstates) and ('visible' in objstates)):
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_ELEMENTS,DEF_WAITFORELEMENTVISIBLE,keywordresult)
                else:
                    verifyresponse = MSG_FALSE
                    keywordresult=MSG_FAIL
                    oebs_key_objects.custom_msg.append("ERR_TIME_OUT_EXCEPTION")
                    logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_ELEMENTS,DEF_WAITFORELEMENTVISIBLE,keywordresult)
            else:
                oebs_key_objects.custom_msg.append("ERR_ELEMENT_NOT_EXISTS")
                logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_ELEMENTS,DEF_WAITFORELEMENTVISIBLE,"ERR_ELEMENT_NOT_EXISTS")
        except Exception as e:
            self.utilities_obj.cleardata()
            logging.debug('FILE: %s , DEF: %s MSG: %s',OEBS_ELEMENTS,DEF_WAITFORELEMENTVISIBLE,e)
            logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_ELEMENTS,DEF_WAITFORELEMENTVISIBLE,keywordresult)
        logging.debug('FILE: %s , DEF: %s MSG: Status: %s',OEBS_ELEMENTS,DEF_WAITFORELEMENTVISIBLE,keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

