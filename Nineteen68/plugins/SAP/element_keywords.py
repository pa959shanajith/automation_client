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
import pywinauto
import sap_constants
import launch_keywords
from launch_keywords import Launch_Keywords
from constants import *
import logger
from saputil_operations import SapUtilKeywords
from sendfunction_keys import SendFunctionKeys
import logging
import logging.config
log = logging.getLogger('element_keywords.py')

class ElementKeywords():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()

    def click_element(self, sap_id, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        w1,w2,wndname,w3=self.lk.getPageTitle()
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
                    pywinauto.mouse.click(button='left', coords=(int(x), int(y)))
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
        self.lk.setWindowToForeground(sap_id)
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

    def verify_element_text(self, sap_id,url,input_val, *args):
        self.lk.setWindowToForeground(sap_id)
        id,ses=self.uk.getSapElement(sap_id)
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        value=OUTPUT_CONSTANT
        err_msg=None
        try:
            if(id != None):
                    if(len(input_val)==1):
                        if(ses.FindById(id).text== input_val):
                            status=sap_constants.TEST_RESULT_PASS
                            result=sap_constants.TEST_RESULT_TRUE
                    elif(len(input_val)==0):
                        log.info('entered text is empty')
                        err_msg='entered text is empty'
                        logger.print_on_console('entered text is empty')
                    else:
                        log.info('more than one element text entered')
                        err_msg='more than one element text entered'
                        logger.print_on_console('more than one element text entered')
            else:
                log.info('element not present on the page where operation is trying to be performed')
                err_msg='element not present on the page where operation is trying to be performed'
        except Exception as e:
            log.error(e)
            logger.print_on_console("Exception has occured :",e)
        #log.info(RETURN_RESULT)
        return status,result,value,err_msg

    def getTooltipText(self, sap_id,*args):
        self.lk.setWindowToForeground(sap_id)
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
                    if value== '':
                        value = ses.FindById(id).DefaultTooltip
                        if value =='':
                            value =Null
                    if(value != None or value !=Null):
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
        self.lk.setWindowToForeground(sap_id)
        sendfnt=SendFunctionKeys()
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
                            d1,d2,error,d3=self.lk.getErrorMessage()
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
