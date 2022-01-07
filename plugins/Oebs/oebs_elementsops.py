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
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
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
                        err_msg = ERROR_CODE_DICT['err_operation_detect']
                        logger.print_on_console(err_msg)
                    else:    
                        methodoutput = TEST_RESULT_TRUE
                        status=TEST_RESULT_PASS
                        log.debug('%s',MSG_CLICK_SUCCESSFUL)
                else:
                    err_msg = MSG_DISABLED_OBJECT
                    log.debug('MSG:%s',err_msg)
                    logger.print_on_console(err_msg)
            else:
                err_msg = MSG_ELEMENT_NOT_VISIBLE
                log.debug('MSG:%s',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_click_element']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',status)
        log.debug('Status: %s',status)
        return status,methodoutput,output_res,err_msg
        
    #Method to get element Text of the given Object location
    def getelementtext(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_GETELEMENTTEXT)
            objstates = charinfo.states
            #check for element hidden
            if 'hidden' in objstates:
                methodoutput = TEST_RESULT_FALSE
                status=TEST_RESULT_FAIL
                err_msg = MSG_HIDDEN_OBJECT
                log.debug('%s',err_msg)
                logger.print_on_console(err_msg)
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
                    status=TEST_RESULT_PASS
                    log.debug('Result:%s',elementtext)
                    #methodoutput = elementtext.encode('utf-8')
                    methodoutput = elementtext
                else:
                    err_msg = MSG_TEXT_NOT_DEFINED
                    log.debug('%s',err_msg)
                    logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_element_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        # response is sent to the client
        self.utilities_obj.cleardata()
        return status,methodoutput,output_res,err_msg

    #Method to verify element text of the given Object location matches with the User Provided Text
    def verifyelementtext(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #sets the methodoutput to FALSE
            methodoutput = TEST_RESULT_FALSE
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_VERIFYELEMENTTEXT)
            objstates = curaccinfo.states
            #check for element hidden
            if 'hidden' in objstates:
                methodoutput = TEST_RESULT_FALSE
                status=TEST_RESULT_FAIL
                log.debug('%s',MSG_HIDDEN_OBJECT)
                err_msg = MSG_HIDDEN_OBJECT
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
                                    #sets the methodoutput to TRUE
                                    methodoutput = TEST_RESULT_TRUE
                                    #sets the status to pass
                                    status=TEST_RESULT_PASS
                                else:
                                    log.debug('Text verification failed',DEF_VERIFYELEMENTTEXT)
                                    err_msg = str('Text verification failed \'' + elementtext + '\' not equal to \''+textVerify+"\'.")
                                    logger.print_on_console(err_msg)
                            else:
                                err_msg = MSG_TEXT_NOT_DEFINED
                                log.debug('%s',err_msg)
                                logger.print_on_console(err_msg)
                        else:
                            err_msg = MSG_INVALID_INPUT
                            log.debug('MSG:%s',err_msg)
                            logger.print_on_console(err_msg)
                else:
                    err_msg = MSG_INVALID_INPUT
                    log.debug('MSG:%s',err_msg)
                    logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_element_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        log.debug('Verify Response %s',str(methodoutput))
        return status,methodoutput,output_res,err_msg

    #Method to waitforelementvisible
    def waitforelementvisible(self,applicationname,objectname,keyword,inputs,outputs):
        acc = ''
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
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
                acc, visible, active_parent =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs, errors = False)
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
                    methodoutput = TEST_RESULT_TRUE
                    status=TEST_RESULT_PASS
                    log.debug('%s',status)
                else:
                    methodoutput = TEST_RESULT_FALSE
                    status=TEST_RESULT_FAIL
                    err_msg = MSG_TIME_OUT_EXCEPTION
                    logger.print_on_console(err_msg)
                    log.debug('%s',err_msg)
            else:
                err_msg = MSG_ELEMENT_NOT_EXISTS
                logger.print_on_console(err_msg)
                log.debug('%s',err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_wait_element_visible']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status: %s',status)
        log.debug('Status: %s',status)
        # response is sent to the client
        return status,methodoutput,output_res,err_msg

