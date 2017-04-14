#-------------------------------------------------------------------------------
# Name:        Element_Keywords
# Purpose:      contains click and get element text
#
# Author:      anas.ahmed1,kavyashree,sakshi.goyal,saloni.goyal
#
# Created:     7-04-2017
# Copyright:   (c) anas.ahmed1 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sap_constants
import launch_keywords
from launch_keywords import Launch_Keywords
from constants import *
import logger
from text_keywords_sap import Text_Keywords

import logging
import logging.config
log = logging.getLogger('element_keywords.py')

class ElementKeywords():


    def click_element(self, sap_id, *args):
        tk=Text_Keywords()
        id,ses=tk.attach(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        #verb = OUTPUT_CONSTANT
        value=OUTPUT_CONSTANT
        err_msg=None
        result = None
        try:
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    ses.FindById(id).SetFocus()
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
                else:
                        log.info('Element state does not allow to perform the operation')
                        err_msg='element not present on the page where operation is trying to be performed'
            else:
                log.info('element not present on the page where operation is trying to be performed')
                err_msg='element not present on the page where operation is trying to be performed'
        except Exception as e:
            log.error(e)
            logger.print_on_console("Exception has occured :",e)
        #log.info(RETURN_RESULT)
        return status,result,value,err_msg

    def get_element_text(self, sap_id, *args):
        tk=Text_Keywords()
        id,ses=tk.attach(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=''
        err_msg=None
        try:
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    if(ses.FindById(id).type == 'GuiLabel'):
                        value =  ses.FindById(id).text
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg='element not present on the page where operation is trying to be performed'
            else:
                log.info('element not present on the page where operation is trying to be performed')
                err_msg='element not present on the page where operation is trying to be performed'
        except Exception as e:
            log.error(e)
            logger.print_on_console("Exception has occured :",e)
        #log.info(RETURN_RESULT)
        return status,result,value,err_msg
