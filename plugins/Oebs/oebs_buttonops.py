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
from oebs_constants import *
import oebs_mouseops
import oebs_key_objects
import oebsServer
import logging
import logger
import time
import oebs_serverUtilities
from oebs_utilops import UtilOperations

log = logging.getLogger('oebs_buttonops.py')


class ButtonOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()
        self.utilops_obj=UtilOperations()

    #Method to get button name of the given Object/XPATH
    def getbuttonname(self,acc):
        del oebs_key_objects.custom_msg[:]
        #sets the keywordresult to FAIL
        keywordresult=MSG_FAIL
        keywordresponse=''
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_GETBUTTONNAME)
            if charinfo.accessibleAction == 1:
                if (charinfo.name != None and charinfo.name != ''):
                    buttonName = charinfo.name
                    if 'alt' in buttonName:
                        buttonName=buttonName.split("alt",1)[0].strip()
                    elif 'ALT' in buttonName:
                        buttonName=buttonName.split("ALT",1)[0].strip()
                    else:
                        buttonName=buttonName.strip()
                    log.debug('%s %s',MSG_RESULT_IS,buttonName)
                    keywordresult=MSG_PASS
                    keywordresponse = buttonName
                    oebs_key_objects.custom_msg.append(str(MSG_RESULT_IS + keywordresponse))
                else:
                    log.debug('%s',MSG_NAME_NOT_DEFINED)
                    logger.print_on_console(MSG_NAME_NOT_DEFINED)
                    oebs_key_objects.custom_msg.append(MSG_NAME_NOT_DEFINED)
            else:
                log.debug('%s',MSG_INVALID_OBJECT)
                logger.print_on_console(MSG_INVALID_OBJECT)
                oebs_key_objects.custom_msg.append(MSG_INVALID_OBJECT)
        except Exception as e:
            err_msg = ERROR_CODE_DICT['err_get_button_name']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            self.utilities_obj.cleardata()
            log.debug('%s',e)
        log.debug('Result %s',keywordresponse)
        log.debug('Status %s',keywordresult)
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
            log.debug('Received Object Context',DEF_VERIFYBUTTONNAME)
            if charinfo.accessibleAction == 1:
                nameVerify=oebs_key_objects.keyword_input[0]
                log.debug('Name Received %s',nameVerify)
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
                            log.debug('Button names matched',DEF_VERIFYBUTTONNAME)
                            verifyresponse = MSG_TRUE
                            keywordresult=MSG_PASS
                        else:
                            log.debug('Button names mismatched',DEF_VERIFYBUTTONNAME)
                            logger.print_on_console(DEF_VERIFYBUTTONNAME)
                            oebs_key_objects.custom_msg.append(str('Button names mismatched. Expected:' + nameVerify + ' ; Actual:'+buttonname))
                    else:
                        log.debug('%s',MSG_NAME_NOT_DEFINED)
                        logger.print_on_console(MSG_NAME_NOT_DEFINED)
                        oebs_key_objects.custom_msg.append(MSG_NAME_NOT_DEFINED)
                else:
                    log.debug('MSG:%s',MSG_INVALID_INPUT)
                    logger.print_on_console(MSG_INVALID_INPUT)
                    oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)
            else:
                log.debug('MSG:%s',MSG_INVALID_OBJECT)
                logger.print_on_console(MSG_INVALID_OBJECT)
                oebs_key_objects.custom_msg.append(MSG_INVALID_OBJECT)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_button']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Result %s',keywordresult)
        log.debug('Status %s',str(verifyresponse))
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
            time.sleep(1)
            acc.requestFocus()
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_CLICK)
            objstates = charinfo.states
            x_coor = int(charinfo.x + (0.5 * charinfo.width))
            y_coor = int(charinfo.y + (0.5 * charinfo.height))
            #Visibility check for scrollbar
            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
                #check for object enabled
                if 'enabled' in objstates and 'showing' in objstates:
                    log.debug('Click Happens on :%s , %s',x_coor,y_coor)
                    oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                    log.debug('Click Successful',DEF_CLICK)
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                elif 'enabled' in objstates and 'showing' not in objstates:
                    log.debug('Object Disabled', ERROR_CODE_DICT['err_visibility_click'])
                    logger.print_on_console(ERROR_CODE_DICT['err_visibility_click'])
                    oebs_key_objects.custom_msg.append(ERROR_CODE_DICT['err_visibility_click'])     
                else:
                    log.debug('Object Disabled',MSG_DISABLED_OBJECT)
                    logger.print_on_console(MSG_DISABLED_OBJECT)
                    oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                logger.print_on_console(MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_click']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',keywordresult)
        log.debug('Status: %s',keywordresult)
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
            log.debug('Received Object Context',DEF_DOUBLECLICK)
            objstates = charinfo.states
            x_coor = int(charinfo.x + (0.5 * charinfo.width))
            y_coor = int(charinfo.y + (0.5 * charinfo.height))
            #Visibility check for scrollbar
            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
                #check for object enabled
                if 'enabled' in objstates and 'showing' in objstates:
                    log.debug('Double Click Happens on :%s , %s',x_coor,y_coor)
                    oebs_mouseops.MouseOperation('doubleClick',x_coor,y_coor)
                    log.debug('Double Click Successful',DEF_DOUBLECLICK)
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                elif 'enabled' in objstates and 'showing' not in objstates:
                    log.debug('Object Disabled', ERROR_CODE_DICT['err_visibility_click'])
                    logger.print_on_console(ERROR_CODE_DICT['err_visibility_click'])
                    oebs_key_objects.custom_msg.append(ERROR_CODE_DICT['err_visibility_click'])  
                else:
                    log.debug('Object Disabled',MSG_DISABLED_OBJECT)
                    logger.print_on_console(MSG_DISABLED_OBJECT)
                    oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                logger.print_on_console(MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_double_click']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Status %s',keywordresult)
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
            log.debug('Received Object Context',DEF_GETLINKTEXT)
            if(curaccinfo.role == 'text'):
                #gets the text information
                curaccinfo = acc.getAccessibleTextInfo(0,1)
                #fetches text from 0th to nth location
                linktext = acc.getAccessibleTextRange(0,curaccinfo.charCount - 1)
                log.debug('Text received is: %s',linktext)
                #sets the result to pass
                keywordresult=MSG_PASS
                log.debug('Result:%s',linktext)
                keywordresponse = linktext
                oebs_key_objects.custom_msg.append(str(MSG_RESULT_IS + keywordresponse))
            elif(curaccinfo.role == 'push button'):
                linktext = curaccinfo.name
                keywordresult=MSG_PASS
                log.debug('Result:%s',linktext)
                keywordresponse = linktext
                oebs_key_objects.custom_msg.append(str(MSG_RESULT_IS + keywordresponse))
            else:
                logger.print_on_console(ERROR_CODE_DICT['err_object']) 
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_link_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Status %s',keywordresult)
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
            log.debug('Received Object Context',DEF_VERIFYLINKTEXT)
            if(curaccinfo.role == 'text'):
                #gets the text information
                curaccinfo = acc.getAccessibleTextInfo(0,1)
                #fetches text from 0th to nth location
                linktext = acc.getAccessibleTextRange(0,curaccinfo.charCount - 1)
                if len(oebs_key_objects.keyword_input) == 1:
                    verificationtext=oebs_key_objects.keyword_input[0]
                    log.debug('User provided text: %s',verificationtext)
                    if (verificationtext != None and verificationtext != 0 ):
                        if verificationtext == linktext:
                            #sets the result to pass
                            keywordresult=MSG_PASS
                            verifyresponse=MSG_TRUE
                            log.debug('Verification result: %s',verifyresponse)
                        else:
                            log.debug('Verification result: %s',verifyresponse)
                            oebs_key_objects.custom_msg.append(str('Link names mismatched. Expected:' + linktext + " Obtained:"+verificationtext))
                else:
                    log.debug('%s',MSG_INVALID_INPUT)
                    logger.print_on_console(MSG_INVALID_INPUT)
                    oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)
            elif(curaccinfo.role == 'push button'):
                linktext = curaccinfo.name
                if len(oebs_key_objects.keyword_input) == 1:
                    verificationtext=oebs_key_objects.keyword_input[0]
                    log.debug('User provided text: %s',verificationtext)
                    if (verificationtext != None and verificationtext != 0 ):
                        if verificationtext == linktext:
                            #sets the result to pass
                            keywordresult=MSG_PASS
                            verifyresponse=MSG_TRUE
                            log.debug('Verification result: %s',verifyresponse)
                        else:
                            log.debug('Verification result: %s',verifyresponse)
                            oebs_key_objects.custom_msg.append(str('Link names mismatched. Expected:' + linktext + " Obtained:"+verificationtext))
                else:
                    log.debug('%s',MSG_INVALID_INPUT)
                    logger.print_on_console(MSG_INVALID_INPUT)
                    oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)
            else:
                logger.print_on_console(ERROR_CODE_DICT['err_object'])
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_link_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Status %s',keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))