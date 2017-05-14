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
from saputil_operations import SapUtilKeywords

import logging
import logging.config
log = logging.getLogger('element_keywords.py')

class ElementKeywords():
    def __init__(self):
        self.uk = SapUtilKeywords()

    def click_element(self, sap_id, *args):
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        from pyrobot import Robot
        lk=Launch_Keywords()
        w1,w2,wndname,w3=lk.getPageTitle()
        button='Left'
        value=OUTPUT_CONSTANT
        err_msg=None
        result = None
        try:
            if(id != None):
                    elem=ses.FindById(id)
                    if(elem.Type == "GuiTab"):
                        elem.Select()
                    left =  elem.__getattr__("ScreenLeft")
                    width = elem.__getattr__("Width")
                    x = left + width/2
                    top =  elem.__getattr__("ScreenTop")
                    height = elem.__getattr__("Height")
                    y= top + height/2
                    rob =Robot(str(wndname))
                    rob.move_and_click(x, y, button)
                    status=sap_constants.TEST_RESULT_PASS
                    result=sap_constants.TEST_RESULT_TRUE
            else:
                log.info('element not present on the page where operation is trying to be performed')
                err_msg='element not present on the page where operation is trying to be performed'
        except Exception as e:
            log.error(e)
            logger.print_on_console("Exception has occured :",e)
        return status,result,value,err_msg

    def get_element_text(self, sap_id, *args):
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):

                        value = ses.FindById(id).text
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
            else:
                log.info('element not present on the page where operation is trying to be performed')
                err_msg='element not present on the page where operation is trying to be performed'
        except Exception as e:
            log.error(e)
            logger.print_on_console("Exception has occured :",e)
        #log.info(RETURN_RESULT)
        return status,result,value,err_msg

    def getTooltipText(self, sap_id,*args):
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            #id = elem.__getattr__("Id")
            if(id != None):
                if(ses.FindById(id).Changeable == True):
                    value = ses.FindById(id).tooltip
                    if(value != None):
                        status=sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        value=OUTPUT_CONSTANT
                        logger.print_on_console('ToolTipText not avaliable for the element ')

                else:
                    err_msg = sap_constants.ERROR_MSG
                    logger.print_on_console('Cannot get ToolTipText for the element ')
            else:
                err_msg = sap_constants.ERROR_MSG
                logger.print_on_console('Element does not exist')

        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
            logger.print_on_console('Error cooured in getTooltipText and is :',e)
        return status,result,value,err_msg

    def getInputHelp(self, sap_id, url, input_val, *args):
            sendfnt=SendFunctionKeys()
            lk=Launch_Keywords()
            id,ses=self.uk.getSapElement(sap_id)
            elem = ses.FindById(id)
            status=sap_constants.TEST_RESULT_FAIL
            result=sap_constants.TEST_RESULT_FALSE
            value=OUTPUT_CONSTANT
            err_msg=None
            try:
                if(id != None):
                            if(elem.type == "GuiTableControl"):
                                row=int(input_val[0])-1
                                col=int(input_val[1])-1
                                elem = elem.GetCell(row, col)

                            if(elem.type == "GuiTextField" or elem.type == "GuiCTextField" or elem.type == "GuiRadioButton" or elem.type == "GuiCheckBox"):
                                elem.SetFocus()
                                sendfnt.sendfunction_keys("F4")
                                d1,d2,error,d3=lk.getErrorMessage()
                                if(error=="No input help is available"):
                                    logger.print_on_console('No input help is available')
                                    err_msg='No input help is available'
                                else:
                                    status=sap_constants.TEST_RESULT_PASS
                                    result=sap_constants.TEST_RESULT_TRUE
                            else:
                                logger.print_on_console('No input help is available')
                                err_msg='No input help is available'

                else:
                    log.info('element not present on the page where operation is trying to be performed')
                    err_msg='element not present on the page where operation is trying to be performed'
            except Exception as e:
                log.error(e)
                logger.print_on_console("Exception has occured :",e)
            #log.info(RETURN_RESULT)
            return status,result,value,err_msg
