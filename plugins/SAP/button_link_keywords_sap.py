#-------------------------------------------------------------------------------
# Name:        ButtonLinkKeyword
# Purpose:     Module for Button link keywords
#
# Author:      anas.ahmed1,kavyasree.l.Sakshi,Saloni
#
# Created:     07-04-2017
# Copyright:   (c) anas.ahmed1 (2017)
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sap_constants
from sap_launch_keywords import Launch_Keywords
from saputil_operations import SapUtilKeywords
from constants import *
import logger
import logging
log = logging.getLogger('button_link_keywords_sap.py')

class ButtonLinkKeyword():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()

##    def click(self, sap_id, *args):
##        self.lk.setWindowToForeground(sap_id)
##        id,ses=self.uk.getSapElement(sap_id)
##        status=sap_constants.TEST_RESULT_FAIL
##        result=sap_constants.TEST_RESULT_FALSE
##        #log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
##        #verb = OUTPUT_CONSTANT
##        value=OUTPUT_CONSTANT
##        err_msg=None
##        try:
##                if(id != None):
##                 if(ses.FindById(id).Changeable == True):
##                    ses.FindById(id).Press()
##                    status =sap_constants.TEST_RESULT_PASS
##                    result = sap_constants.TEST_RESULT_TRUE
##                 else:
##                        log.info('Element state does not allow to perform the operation')
##                        err_msg = 'Element state does not allow to perform the operation'
##                else:
##                    log.info('element not present on the page where operation is trying to be performed')
##                    err_msg = 'element not present on the page where operation is trying to be performed'
##        except Exception as e:
##            import traceback
##            traceback.getexc()
####            logger.print_on_console('Error has occured',e)
##            log.error(e)
##        return status,result,value,err_msg

    def get_button_name(self,  sap_id , *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( ses.FindById(id).Text ):
                    value = ses.FindById(id).Text
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Button name is not defined'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg)
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error(err_msg)
            logger.print_on_console("Error occured in getButtonName")
        return status,result,value,err_msg

    def verify_button_name(self,  sap_id , input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( ses.FindById(id).Text and (ses.FindById(id).Text.lstrip() == input_val[0].lstrip()) ):
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Button name does not match'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in verifyButtonName" )
        return status,result,value,err_msg

    def button_uploadFile(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            result = None
            if ( id and ses ):
                filepath = input_val[0]
                if ( ses.FindById(id).Changeable == True ):
                    j = 1
                    index = 0
                    li = []
                    """finding the occurence of \ (backslash) in filepath and appending the index in list"""
                    for letter in filepath:
                        if( letter == '\\' ):
                            li.append(index)
                        index = index + 1
                    """for every occurence of backslash which is not succeeded with another backslash, appending it with another backslash
                     so that it is not considered as an escape character"""
                    for i in li:
                        if ( filepath[i + 1] != '\\' ):
                            filepath = filepath[:i] + '\\' + filepath[i:]
                            """incresing the indexes stored in the list by one...since one more backslash has been added in the string"""
                            for k in range(j, len(li)):
                                li[k] = li[k] + 1
                            j = j + 1
                    ses.FindById(id).text = filepath
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.ELEMENT_NOT_CHANGEABLE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in uploadFile" )
        return status,result,value,err_msg