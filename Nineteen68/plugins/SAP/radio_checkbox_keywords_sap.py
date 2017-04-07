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
import launch_keywords
import logger
from constants import *
from text_keywords_sap import Text_Keywords

import logging
import logging.config
log = logging.getLogger('radio_checkbox_keywords_sap.py')

class Radio_Checkbox_keywords():
    def select_radiobutton(self, sap_id, *args):
        tk=Text_Keywords()
        id,ses=tk.attach(sap_id)
        status=sap_constants.TEST_RESULT_FALSE
        result=sap_constants.TEST_RESULT_FAIL
        #verb = OUTPUT_CONSTANT
        value=''
        err_msg=None
        try:
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    ses.FindById(id).Select()
                    status=sap_constants.TEST_RESULT_TRUE
                    result=sap_constants.TEST_RESULT_PASS
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
            logger.print_on_console(err_msg,e)

        return status,result,value,err_msg

    def select_checkbox(self, sap_id , *args):
        tk=Text_Keywords()
        id,ses=tk.attach(sap_id)
        status=sap_constants.TEST_RESULT_FALSE
        result=sap_constants.TEST_RESULT_FAIL
        #verb = OUTPUT_CONSTANT
        value=''
        err_msg=None
        try:

            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    ses.FindById(id).Selected = 1
                    status=sap_constants.TEST_RESULT_TRUE
                    result=sap_constants.TEST_RESULT_PASS
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
            logger.print_on_console(err_msg,e)

        return status,result,value,err_msg

    def unselect_checkbox(self, sap_id, *args):
        tk=Text_Keywords()
        id,ses=tk.attach(sap_id)
        status=sap_constants.TEST_RESULT_FALSE
        result=sap_constants.TEST_RESULT_FAIL
        #verb = OUTPUT_CONSTANT
        value=''
        err_msg=None
        try:

            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    ses.FindById(id).Selected = 0
                    status=sap_constants.TEST_RESULT_TRUE
                    result=sap_constants.TEST_RESULT_PASS
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
            logger.print_on_console(err_msg,e)

            log.error(err_msg,e)
        return status,result,value,err_msg

    def get_status_checkbox(self, sap_id, *args):
        tk=Text_Keywords()
        id,ses=tk.attach(sap_id)
        status=sap_constants.TEST_RESULT_FALSE
        result=sap_constants.TEST_RESULT_FAIL
        #verb = OUTPUT_CONSTANT
        value=''
        err_msg=None
        try:

            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    if(ses.FindById(id).type == "GuiCheckBox"):
                        value = ses.FindById(id).selected
                        status=sap_constants.TEST_RESULT_TRUE
                        result=sap_constants.TEST_RESULT_PASS
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
            logger.print_on_console(err_msg,e)
            log.error(err_msg,e)
        return status,result,value,err_msg

    def get_status_radiobtn(self, sap_id, *args):
        tk=Text_Keywords()
        id,ses=tk.attach(sap_id)
        status=sap_constants.TEST_RESULT_FALSE
        result=sap_constants.TEST_RESULT_FAIL
        #verb = OUTPUT_CONSTANT
        value=''
        err_msg=None
        try:

            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    if(ses.FindById(id).type == "GuiCheckBox"):
                        value = ses.FindById(id).selected
                        status=sap_constants.TEST_RESULT_TRUE
                        result=sap_constants.TEST_RESULT_PASS
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
            logger.print_on_console(err_msg,e)
            log.error(err_msg,e)
        return status,result,value,err_msg




