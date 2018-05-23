#-------------------------------------------------------------------------------
# Name:        radio_checkbox_keywords
# Purpose:     Module for radio and checkbox keywords
#
# Author:      anas.ahmed1,kavyashree,sakshi.goyal,saloni.goyal
#
# Created:     7-04-2017
# Copyright:   (c) anas.ahmed1 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sap_constants
import logger
from constants import *
from saputil_operations import SapUtilKeywords
from sap_launch_keywords import Launch_Keywords
import logging
import logging.config
log = logging.getLogger('radio_checkbox_keywords_sap.py')

class Radio_Checkbox_keywords():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()

    def select_radiobutton(self, sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    ses.FindById(id).Select()
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                else:
                        logger.print_on_console('Element state does not allow to perform the operation')
                        err_msg = sap_constants.ERROR_MSG
                        log.info(err_msg)
            else:
                    logger.print_on_console('element not present on the page where operation is trying to be performed')
                    err_msg = sap_constants.ERROR_MSG
                    log.info(err_msg)
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            log.error(e)
            logger.print_on_console("Error occured in selectRadioButton")
        return status,result,value,err_msg

    def select_checkbox(self, sap_id , *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    b=ses.FindById(id)
                    b.selected =1
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Element state does not allow to perform the operation')
                    err_msg = sap_constants.ERROR_MSG
                    log.info(err_msg)
            else:
                logger.print_on_console('element not present on the page where operation is trying to be performed')
                err_msg = sap_constants.ERROR_MSG
                log.info(err_msg)
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            log.error(err_msg,e)
            logger.print_on_console("Error occured in selectCheckbox")

        return status,result,value,err_msg

    def unselect_checkbox(self, sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    b=ses.FindById(id)
                    b.selected =0
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Element state does not allow to perform the operation')
                    err_msg = sap_constants.ERROR_MSG
                    log.info(err_msg)
            else:
                logger.print_on_console('element not present on the page where operation is trying to be performed')
                err_msg = sap_constants.ERROR_MSG
                log.info(err_msg)
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console("Error occured in unselectCheckbox")
            log.error(e)
        return status,result,value,err_msg

    def get_status(self, sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):
                #----------------------------------------------------------Check for radio
                if(ses.FindById(id).type == "GuiRadioButton"):
                    value = ses.FindById(id).selected
                    if(value==True):
                        value=sap_constants.SELECTED_CHECK
                    else:
                        value=sap_constants.UNSELECTED_CHECK
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE

                #----------------------------------------------------------Check for Checkbox
                elif(ses.FindById(id).type == "GuiCheckBox"):
                    value = ses.FindById(id).selected
                    if(value ==True):
                        value=sap_constants.CHECKED_CHECK
                    else:
                        value=sap_constants.UNCHECKED_CHECK
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                #----------------------------------------------------------Check for Button
                elif(ses.FindById(id).type == "GuiButton"):
                    try:
                        value = ses.FindById(id).selected
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
                    except:
                        logger.print_on_console('Button element does not have status')
            else:
                logger.print_on_console('element not present on the page where operation is trying to be performed')
                err_msg = sap_constants.ERROR_MSG
                log.info(err_msg)
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console("Error occured in getStatus")
            log.error(e)
        return status,result,value,err_msg




