#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     21-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import desktop_constants
from editable_text import Text_Box
from launch_keywords import ldtp
import launch_keywords
from ldtp.client_exception import LdtpExecutionError

class Radio_Checkbox_keywords():
    def select_radiobutton(self, element , parent  , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        try:
            if launch_keywords.window_name!=None:
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                if (check == True):
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    if(desktop_constants.ENABLED_CHECK and desktop_constants.VISIBLE_CHECK in states):
                       flag = ldtp.check(launch_keywords.window_name,dektop_element[0])
                       status = desktop_constants.TEST_RESULT_PASS
                       result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        logger.log('Element state does not allow to perform the operation')
                else:
                    logger.log('element not present on the page where operation is trying to be performed')
        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result

    def select_checkbox(self, element , parent  , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        try:
            if launch_keywords.window_name!=None:
                print element
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                if (check == True):
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    if(desktop_constants.ENABLED_CHECK and desktop_constants.VISIBLE_CHECK in states):
                        if(not(desktop_constants.CHECKED_CHECK in states)):

                               flag = ldtp.check(launch_keywords.window_name,dektop_element[0])
                               status = desktop_constants.TEST_RESULT_PASS
                               result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        logger.log('Element state does not allow to perform the operation')
                else:
                    logger.log('element not present on the page where operation is trying to be performed')
        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result

    def unselect_checkbox(self, element , parent  , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        try:
            if launch_keywords.window_name!=None:
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                if (check == True):
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    if(desktop_constants.ENABLED_CHECK and desktop_constants.VISIBLE_CHECK and desktop_constants.CHECKED_CHECK in states):

                           flag = ldtp.uncheck(launch_keywords.window_name,dektop_element[0])
                           status = desktop_constants.TEST_RESULT_PASS
                           result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        logger.log('Element state does not allow to perform the operation')
                else:
                    logger.log('element not present on the page where operation is trying to be performed')
        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result

    def get_status(self, element , parent  , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        flag=None
        try:
            if launch_keywords.window_name!=None:
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                if (check == True):
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    if(desktop_constants.VISIBLE_CHECK in states):
                        if(dektop_element[0].strip()[0:3] == 'chk'):
                            if(desktop_constants.CHECKED_CHECK in states):
                                flag = 'Checked'
                                status=desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                            else:
                                flag = 'UnChecked'
                                status=desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                        if(dektop_element[0].strip()[0:4] == 'rbtn'):
                            if(desktop_constants.SELECTED_CHECK in states):
                                flag = 'Selected'
                                status=desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                            else:
                                flag = 'UnSelected'
                                status=desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        logger.log('Element state does not allow to perform the operation')
                else:
                    logger.log('element not present on the page where operation is trying to be performed')

        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result,flag
