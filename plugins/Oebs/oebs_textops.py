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

from oebs_constants import *
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
import pythoncom
import logger
from encryption_utility import AESCipher
pythoncom.CoInitialize()
shell = win32com.client.Dispatch("WScript.Shell")

log = logging.getLogger('oebs_textops.py')

class TextOperations:

    def __init__(self):
        self.utilities_obj=oebs_serverUtilities.Utilities()
        self.utilops_obj=UtilOperations()
        self.keywordops_obj=oebs_keyboardops.KeywordOperations()

    #Method to get Text of the given Object location
    def gettext(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            charinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_GETTEXT)
            #checks element is accessible
            if charinfo.accessibleText == 1:
                if 'enabled' in charinfo.states:
                    log.debug('Text Box is accessible',DEF_GETTEXT)
                    #gets the text information
                    charinfo = acc.getAccessibleTextInfo(0,1)
                    #fetches text from 0th to nth location
                    text = acc.getAccessibleTextRange(0,charinfo.charCount - 1)
                    log.debug('Text Box text is %s',text)
                    #sets the result to pass
                    status=TEST_RESULT_PASS
                    log.debug('Result:%s',text)
                    methodoutput = text
                    logger.print_on_console("MSG_RESULT_IS")
                else:
                    err_msg = MSG_DISABLED_OBJECT
                    log.debug('MSG:%s',err_msg)
                    logger.print_on_console(err_msg)
            else:
                err_msg = MSG_INVALID_OBJECT
                log.debug('%s',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_get_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #Method to settext at the given Object location
    def settext(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            time.sleep(3)
            acc.requestFocus()
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_SETTEXT)
            if 'enabled' in curaccinfo.states:
                #checks whether action can be performed on the object
                if curaccinfo.accessibleAction == 1:
                    #checks whether text object editable
                    if 'editable' in curaccinfo.states:
                        log.debug('Text Box is accessible',DEF_SETTEXT)
                        #checks element is accessible
                        if curaccinfo.accessibleText == 1:
                            if len(oebs_key_objects.keyword_input) == 1:
                                #checks if the text is empty
                                if (oebs_key_objects.keyword_input[0] != ''):
                                    text=oebs_key_objects.keyword_input[0]
                                    log.debug('Text to be set is %s',text)
                                    #if text != None:
                                    #gets the full length of the text
                                    character=acc.getAccessibleTextInfo(0,1)
                                    #sets the text value to the object
                                    result = acc.setTextContents(text)
                                    if result:
                                        #sets the result to pass
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                else:
                                    err_msg = MSG_INVALID_INPUT
                                    log.debug('MSG:%s',err_msg)
                                    logger.print_on_console(err_msg)
                            else:
                                err_msg = MSG_INVALID_INPUT
                                log.debug('MSG:%s',err_msg)
                                logger.print_on_console(err_msg)
                        else:
                            err_msg = MSG_INVALID_OBJECT
                            log.debug('MSG:%s',err_msg)
                            logger.print_on_console(err_msg)
                    else:
                        err_msg = MSG_OBJECT_READONLY
                        log.debug('MSG:%s',err_msg)
                        logger.print_on_console(err_msg)
                else:
                    #gets the entire context information
                    curaccinfo = acc.getAccessibleContextInfo()
                    log.debug('Text Box is accessible',DEF_SETTEXT)
                    x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
                    y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
                    log.debug('Text Box is accessible',DEF_SETTEXT)
                    if len(oebs_key_objects.keyword_input) == 1:
                        #if text != None:
                        if (oebs_key_objects.keyword_input[0] != ''):
                            text=oebs_key_objects.keyword_input[0]
                            index = len(text)
                            log.debug('Text to be set is %s',text)
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

                                        self.keywordops_obj.keyboard_operation('keypress','HOME')
                                        #clears the text untill all characters are deleted
                                        for num in range(character.charCount):
                                            shell.SendKeys("{DELETE}")


                                        #sets the text value to the object
                                        for length in range(index):
                                            shell.SendKeys('{'+text[length]+'}')
                                            #sets the result to pass;
                                            status=TEST_RESULT_PASS
                                            methodoutput=TEST_RESULT_TRUE
                                    else:
                                        err_msg = MSG_ELEMENT_NON_EDITABLE
                                        log.debug('MSG:%s',err_msg)
                                        logger.print_on_console(err_msg)
                                else:
                                    err_msg = MSG_OBJECT_READONLY
                                    log.debug('MSG:%s',err_msg)
                                    logger.print_on_console(err_msg)
                            else:
                                err_msg = MSG_ELEMENT_NOT_VISIBLE
                                log.debug('MSG:%s',err_msg)
                                logger.print_on_console(err_msg)
                        else:
                            err_msg = MSG_INVALID_INPUT
                            log.debug('MSG:%s',err_msg)
                            logger.print_on_console(err_msg)
                    else:
                        err_msg = MSG_INVALID_INPUT
                        log.debug('MSG:%s',err_msg)
                        logger.print_on_console(err_msg)
            else:
                err_msg = MSG_DISABLED_OBJECT
                log.debug('MSG:%s',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_set_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('Status %s',status)
            oebs_key_objects.custom_msg=[]
            logger.print_on_console(str(e))
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg

    #implemented for #8010-Azure
    def setsecuretext(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            time.sleep(3)
            acc.requestFocus()
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_SETTEXT)
            if 'enabled' in curaccinfo.states:
                #checks whether action can be performed on the object
                if curaccinfo.accessibleAction == 1:
                    #checks whether text object editable
                    if 'editable' in curaccinfo.states:
                        log.debug('Text Box is accessible',DEF_SETTEXT)
                        #checks element is accessible
                        if curaccinfo.accessibleText == 1:
                            if len(oebs_key_objects.keyword_input) == 1:
                                #checks if the text is empty
                                if (oebs_key_objects.keyword_input[0] != ''):
                                    text=oebs_key_objects.keyword_input[0]
                                    log.debug('SecureText to be set is %s',text)
                                    #if text != None:
                                    #gets the full length of the text
                                    character=acc.getAccessibleTextInfo(0,1)
                                    #decrypt the text:
                                    encryption_obj = AESCipher()
                                    text = encryption_obj.decrypt(text)
                                    #sets the text value to the object
                                    result = acc.setTextContents(text)
                                    if result:
                                        #sets the result to pass
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                else:
                                    err_msg = MSG_INVALID_INPUT
                                    log.debug('MSG:%s',err_msg)
                                    logger.print_on_console(err_msg)
                            else:
                                err_msg = MSG_INVALID_INPUT
                                log.debug('MSG:%s',err_msg)
                                logger.print_on_console(err_msg)
                        else:
                            err_msg = MSG_INVALID_OBJECT
                            log.debug('MSG:%s',err_msg)
                            logger.print_on_console(err_msg)
                    else:
                        err_msg = MSG_OBJECT_READONLY
                        log.debug('MSG:%s',err_msg)
                        logger.print_on_console(err_msg)
                else:
                    #gets the entire context information
                    curaccinfo = acc.getAccessibleContextInfo()
                    log.debug('Text Box is accessible',DEF_SETTEXT)
                    x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
                    y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
                    log.debug('Text Box is accessible {}'.format(DEF_SETTEXT))
                    if len(oebs_key_objects.keyword_input) == 1:
                        #if text != None:
                        if (oebs_key_objects.keyword_input[0] != ''):
                            text=oebs_key_objects.keyword_input[0]
                            #decrypt the text:
                            encryption_obj = AESCipher()
                            text = encryption_obj.decrypt(text)
                            index = len(text)
                            log.debug('Text to be set is %s',text)
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

                                        self.keywordops_obj.keyboard_operation('keypress','HOME')
                                        #clears the text untill all characters are deleted
                                        for num in range(character.charCount):
                                            shell.SendKeys("{DELETE}")


                                        #sets the text value to the object
                                        for length in range(index):
                                            shell.SendKeys('{'+text[length]+'}')
                                            #sets the result to pass;
                                            status=TEST_RESULT_PASS
                                            methodoutput=TEST_RESULT_TRUE
                                    else:
                                        err_msg = MSG_ELEMENT_NON_EDITABLE
                                        log.debug('MSG:%s',err_msg)
                                        logger.print_on_console(err_msg)
                                else:
                                    err_msg = MSG_OBJECT_READONLY
                                    log.debug('MSG:%s',err_msg)
                                    logger.print_on_console(err_msg)
                            else:
                                err_msg = MSG_ELEMENT_NOT_VISIBLE
                                log.debug('MSG:%s',err_msg)
                                logger.print_on_console(err_msg)
                        else:
                            err_msg = MSG_INVALID_INPUT
                            log.debug('MSG:%s',err_msg)
                            logger.print_on_console(err_msg)
                    else:
                        err_msg = MSG_INVALID_NOOF_INPUT
                        log.debug('MSG:%s',err_msg)
                        logger.print_on_console(err_msg)
            else:
                err_msg = MSG_DISABLED_OBJECT
                log.debug('MSG:%s',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_set_secure_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('Status %s',status)
            oebs_key_objects.custom_msg=[]
            logger.print_on_console(str(e))
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg


    #Method to verifytext of the given Object location matches with the User Provided Text
    def verifytext(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            #gets the entire context information
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_VERIFYTEXT)
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
                            log.debug('Text verified',DEF_VERIFYTEXT)
                            #sets the methodoutput to TRUE
                            methodoutput = TEST_RESULT_TRUE
                                #sets the status to pass
                            status=TEST_RESULT_PASS
                        else:
                            log.debug('Text verification failed',DEF_VERIFYTEXT)
                            logger.print_on_console(str('Text verification failed \'' + fetchedText + '\' not equal to \''+textVerify+"\'."))
                    else:
                        err_msg = MSG_INVALID_INPUT
                        log.debug('MSG:%s',err_msg)
                        logger.print_on_console(err_msg)
                else:
                    err_msg = MSG_INVALID_NOOF_INPUT
                    log.debug('MSG:%s',err_msg)
                    logger.print_on_console(err_msg)
            else:
                err_msg = MSG_INVALID_OBJECT
                log.debug('MSG:%s',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_verify_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        log.debug('Verify Response %s',str(methodoutput))
        return status,methodoutput,output_res,err_msg

    #Method to cleartext of the given Object location matches with the User Provided Text
    def cleartext(self,acc):
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        try:
            time.sleep(3)
            #gets the entire context information
            acc.requestFocus()
            curaccinfo = acc.getAccessibleContextInfo()
            log.debug('Received Object Context',DEF_CLEARTEXT)
            if 'enabled' in curaccinfo.states:
                #checks whether an action can be performed on the object
                if curaccinfo.accessibleAction == 1:
                    if 'editable' in curaccinfo.states:
                        # formula for changing co-ordinates to center of the element
                        x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
                        y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
                        log.debug('Formula Created',DEF_CLEARTEXT)
                        #checks element is accessible
                        if curaccinfo.accessibleText == 1:
                            #sets the text to empty
                            text=''
                            #sets the text value to the object
                            result = acc.setTextContents(text)
                            if result:
                                #sets the result to pass
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                                log.debug('MSG:%s',MSG_TEXTBOX_CLEARED)
                        else:
                            err_msg = MSG_INVALID_OBJECT
                            log.debug('MSG:%s',err_msg)
                            logger.print_on_console(err_msg)
                    else:
                        err_msg = MSG_OBJECT_READONLY
                        log.debug('MSG:%s',err_msg)
                        logger.print_on_console(err_msg)
                else:
                    if 'editable' in curaccinfo.states:
                        x_coor = int(curaccinfo.x + (0.5 * curaccinfo.width))
                        y_coor = int(curaccinfo.y + (0.5 * curaccinfo.height))
                        log.debug('Formula Created',DEF_CLEARTEXT)
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
                                            self.keywordops_obj.keyboard_operation('keypress','HOME')
                                            #clears the text until all characters are deleted
                                            for num in range(character.charCount):
                                                shell.SendKeys("{DELETE}")
                                            log.debug('MSG:%s',MSG_TEXTBOX_CLEARED)
                                            #sets the result to pass
                                            status=TEST_RESULT_PASS
                                            methodoutput=TEST_RESULT_TRUE
                                        else:
                                            err_msg = MSG_ELEMENT_NOT_FOCUSABLE
                                            log.debug('MSG:%s',err_msg)
                                            logger.print_on_console(err_msg)
                                else:
                                    err_msg = MSG_ELEMENT_NON_EDITABLE
                                    log.debug('MSG:%s',err_msg)
                                    logger.print_on_console(err_msg)
                            else:
                                err_msg = MSG_ELEMENT_NOT_VISIBLE
                                log.debug('MSG:%s',err_msg)
                                logger.print_on_console(err_msg)
                    else:
                        err_msg = MSG_OBJECT_READONLY
                        log.debug('MSG:%s',err_msg)
                        logger.print_on_console(err_msg)
            else:
                err_msg = MSG_DISABLED_OBJECT
                log.debug('MSG:%s',err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            self.utilities_obj.cleardata()
            err_msg = ERROR_CODE_DICT['err_clear_text']
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.debug('%s',e)
            log.debug('Status %s',status)
        log.debug('Status %s',status)
        return status,methodoutput,output_res,err_msg