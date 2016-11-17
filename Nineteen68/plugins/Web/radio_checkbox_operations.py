#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     08-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import selenium
import Exceptions
from webconstants import *
import logger
import browser_Keywords
from utilweb_operations import UtilWebKeywords
class RadioCheckboxKeywords:

    def __init__(self):
        self.utilobj=UtilWebKeywords()
        self.status={'radio':'Checked',
                    'checkbox':'Selected'}


    def select_radiobutton(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        if webelement is not None:
            try:
                if ele.is_enabled():
                    is_visible=self.utilobj.is_visible(webelement)
                    if len(args)>0:
                        visibilityFlag=args[0]
                        if not(visibilityFlag and is_visible):
                            browser_Keywords.driver_obj.execute_script(CLICK_RADIO_CHECKBOX,webelement)
                        else:
                            webelement.click()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                else:
                    logger.log('Element is disabled')
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput


    def select_checkbox(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    if not(webelement.is_selected()):
                        is_visble=self.utilobj.is_visible(webelement)
                        if len(args)>0:
                            visibilityFlag=args[0]
                        if not(visibilityFlag and is_visble ):
                            browser_Keywords.driver_obj.execute_script(CLICK_RADIO_CHECKBOX,webelement)
                        else:
                            webelement.click()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        logger.log('Checkbox is already selected')
                else:
                    logger.log('Element is disabled')
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput


    def unselect_checkbox(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        if webelement is not None:
            try:
                if webelement.is_enabled():
                    if webelement.is_selected():
                        is_visible=self.utilobj.is_visible(webelement)
                        if len(args)>0:
                            visibilityFlag=args[0]
                        if not(visibilityFlag and is_visible ):
                            browser_Keywords.driver_obj.execute_script(CLICK_RADIO_CHECKBOX,webelement)
                        else:
                            webelement.click()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        logger.log('Checkbox is already Unselected')
                else:
                    logger.log('Element is disabled')
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput

    def get_status(self,webelement,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        visibilityFlag=True
        status=None
        if webelement is not None:
            try:
                status,methodoutput=self.__fetch_status(webelement)
                logger.log('Status is:'+status)
            except Exception as e:
                    Exceptions.error(e)
        return status,methodoutput

    def __fetch_status(self,webelement,*args):
        type=webelement.get_attribute("type").lower();
        if webelement.is_selected():
            status=self.status[type]
            methodoutput=TEST_RESULT_TRUE
        else:
            status='Un'+self.status[type].lower()
            methodoutput=TEST_RESULT_TRUE
        return status,methodoutput

