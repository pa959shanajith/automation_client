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
from oebs_constants import *
import oebs_key_objects
import oebs_serverUtilities
import oebs_mouseops
import time
import logging
import logger
import winuser
import win32api
import readconfig
from oebs_utilops import UtilOperations

log = logging.getLogger('oebs_elementsops.py')

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
            time.sleep(1)
            acc.requestFocus()
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_CLICKELEMENT)
            objstates = charinfo.states
            #x_coor = int(charinfo.x + (0.5 * charinfo.width))
            #y_coor = int(charinfo.y + (0.5 * charinfo.height))
            x_coor = int(charinfo.x + 25 )
            y_coor = int(charinfo.y + 10)
            #Visibility check for scrollbar
            if(self.utilops_obj.getObjectVisibility(acc,x_coor,y_coor)):
            #check for object enabled
                if 'enabled' in objstates:
                    log.debug('Click Happens on :%s , %s',x_coor,y_coor)
                    oebs_mouseops.MouseOperation('click',x_coor,y_coor)
                    charinfo = acc.getAccessibleContextInfo()
                    if 'selectable' in charinfo.states and 'selected' not in charinfo.states:
                        logger.print_on_console('Element clicked but operation not detected, Please use alternative keyword double click')
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                    log.debug('%s',MSG_CLICK_SUCCESSFUL)
                    oebs_key_objects.custom_msg.append(str(MSG_CLICK_SUCCESSFUL))
                else:
                    log.debug('MSG:%s',MSG_DISABLED_OBJECT)
                    logger.print_on_console(MSG_DISABLED_OBJECT)
                    oebs_key_objects.custom_msg.append(MSG_DISABLED_OBJECT)
            else:
                log.debug('MSG:%s',MSG_ELEMENT_NOT_VISIBLE)
                logger.print_on_console(MSG_ELEMENT_NOT_VISIBLE)
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_VISIBLE)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_click_element']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',keywordresult)
        log.debug('Status: %s',keywordresult)
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
            log.debug('Received Object Context',DEF_GETELEMENTTEXT)
            objstates = charinfo.states
            #check for element hidden
            if 'hidden' in objstates:
                verifyresponse = MSG_FALSE
                keywordresult=MSG_FAIL
                log.debug('%s',MSG_HIDDEN_OBJECT)
                oebs_key_objects.custom_msg.append(MSG_HIDDEN_OBJECT)
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
                    log.debug('element text is %s',elementtext)
                    #sets the result to pass
                    keywordresult=MSG_PASS
                    log.debug('Result:%s',elementtext)
                    #keywordresponse = elementtext.encode('utf-8')
                    keywordresponse = elementtext
                    oebs_key_objects.custom_msg.append("MSG_RESULT_IS")
                else:
                    log.debug('%s',MSG_TEXT_NOT_DEFINED)
                    logger.print_on_console(MSG_TEXT_NOT_DEFINED)
                    oebs_key_objects.custom_msg.append(MSG_TEXT_NOT_DEFINED)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_element_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Status %s',keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(keywordresponse))

    def verifyelementexists(self,acc):
        del oebs_key_objects.custom_msg[:]
         #sets the keywordresult to FAIL
        keywordresult = MSG_FAIL
        verifyresponse = MSG_FALSE
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_VERIFYEXISTS)
            if('showing' in curaccinfo.states and 'visible' in curaccinfo.states):
                verifyresponse = MSG_TRUE
                keywordresult = MSG_PASS
            else:
                log.debug('%s',DEF_VERIFYEXISTS,MSG_INVALID_INPUT)
                logger.print_on_console(MSG_INVALID_INPUT)
                oebs_key_objects.custom_msg.append(MSG_HIDDEN_OBJECT)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_element_exists']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',DEF_VERIFYEXISTS,e)
            log.debug('Status %s',DEF_VERIFYEXISTS,keywordresult)
        log.debug('Status %s',DEF_VERIFYEXISTS,keywordresult)
        log.debug('Verify Element Exists Response %s',DEF_VERIFYEXISTS,str(verifyresponse))
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))


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
            log.debug('Received Object Context',DEF_VERIFYELEMENTTEXT)
            objstates = curaccinfo.states
            #check for element hidden
            if 'hidden' in objstates:
                verifyresponse = MSG_FALSE
                keywordresult=MSG_FAIL
                log.debug('%s',MSG_HIDDEN_OBJECT)
                oebs_key_objects.custom_msg.append(MSG_HIDDEN_OBJECT)
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
                                log.debug('element text is %s',elementtext)
                                #checks the user provided text with the text in the object
                                if elementtext == textVerify:
                                    log.debug('Text verified',DEF_VERIFYELEMENTTEXT)
                                    #sets the verifyresponse to TRUE
                                    verifyresponse = MSG_TRUE
                                    #sets the keywordresult to pass
                                    keywordresult=MSG_PASS
                                else:
                                    log.debug('Text verification failed',DEF_VERIFYELEMENTTEXT)
                                    oebs_key_objects.custom_msg.append(str('Text verification failed \'' + elementtext + '\' not equal to \''+textVerify+"\'."))
                            else:
                                log.debug('%s',MSG_TEXT_NOT_DEFINED)
                                logger.print_on_console(MSG_TEXT_NOT_DEFINED)
                                oebs_key_objects.custom_msg.append(MSG_TEXT_NOT_DEFINED)
                        else:
                            log.debug('MSG:%s',MSG_INVALID_INPUT)
                            oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)
                else:
                    log.debug('MSG:%s',MSG_INVALID_NOOF_INPUT)
                    logger.print_on_console(MSG_INVALID_INPUT)
                    oebs_key_objects.custom_msg.append(MSG_INVALID_INPUT)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_element_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',keywordresult)
        log.debug('Status %s',keywordresult)
        log.debug('Verify Response %s',str(verifyresponse))
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
        configvalues = readconfig.configvalues
        try:
            #gets the entire context information
            log.debug('Received Object Context',DEF_WAITFORELEMENTVISIBLE)
            #geting mouse state
            mousestate=oebs_mouseops.GetCursorInfo('state')
            delay=int(configvalues['timeOut'])
            while(mousestate == 65543):
                mousestate=oebs_mouseops.GetCursorInfo('state')
            start_time = time.time()
            logger.print_on_console("Waiting for element to be visible")
            while True:
                acc, visible =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs, errors = False)
                if acc and str(acc) != "fail":
                    break
                if time.time() - start_time >= delay:
                    break
                time.sleep(0.25)
            if(acc and str(acc) != 'fail'):
                charinfo = acc.getAccessibleContextInfo()
                objstates = charinfo.states
                #check for object visible
                if(('showing' in objstates) and ('visible' in objstates)):
                    verifyresponse = MSG_TRUE
                    keywordresult=MSG_PASS
                    log.debug('%s',keywordresult)
                else:
                    verifyresponse = MSG_FALSE
                    keywordresult=MSG_FAIL
                    oebs_key_objects.custom_msg.append(MSG_TIME_OUT_EXCEPTION)
                    logger.print_on_console(MSG_TIME_OUT_EXCEPTION)
                    log.debug('%s',keywordresult)
            else:
                oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_EXISTS)
                logger.print_on_console(MSG_ELEMENT_NOT_EXISTS)
                log.debug('%s',MSG_ELEMENT_NOT_EXISTS)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_wait_element_visible']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',keywordresult)
        log.debug('Status: %s',keywordresult)
        # response is sent to the client
        self.utilities_obj.cleardata()
        oebs_key_objects.keyword_output.append(str(keywordresult))
        oebs_key_objects.keyword_output.append(str(verifyresponse))

