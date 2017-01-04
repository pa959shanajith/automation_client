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
from launch_keywords import Launch_Keywords
from ldtp.client_exception import LdtpExecutionError

class ElementKeywords():
    def verify_element_exists(self, element , parent , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        try:
            if launch_keywords.window_name!=None:
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                if (check == True):
                    ldtp.wait()
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    if(desktop_constants.ENABLED_CHECK in states):
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('element not present on the page where operation is trying to be performed')
        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result

    def verify_element_doesNot_exists(self, element , parent , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        try:
            if launch_keywords.window_name!=None:
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                if (check == True):
                    ldtp.wait()
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    if(not(desktop_constants.VISIBLE_CHECK in states)):
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('element not present on the page where operation is trying to be performed')
        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result

    def click_element(self, element , parent  , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        try:
            if launch_keywords.window_name!=None:
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                if (check == True):
                    temp_obj = Launch_Keywords()
                    temp_obj.set_to_foreground()
                    ldtp.wait()
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    if(desktop_constants.VISIBLE_CHECK  in states):
                        objCoordinates = ldtp.getobjectsize(launch_keywords.window_name,dektop_element[0])
                        xCoordinate = 0;
                        yCoordinate = 0;
                        if((objCoordinates[2]/2)<20):
                            xCoordinate = objCoordinates[0]+(objCoordinates[2]/2)
                        else:
                            xCoordinate = objCoordinates[0]+20
                        yCoordinate = objCoordinates[1] + (objCoordinates[3]/2)
                        ldtp.generatemouseevent(xCoordinate, yCoordinate, 'b1c')
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console('Element state does not allow to perform the operation')
                else:
                    logger.print_on_console('element not present on the page where operation is trying to be performed')
        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result

    def get_element_text(self, element , parent , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        label=None
        try:
            if launch_keywords.window_name!=None:
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                if (check == True):
                    label = ldtp.getobjectproperty(launch_keywords.window_name, dektop_element[0],'label')
                    if(label is not None):
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('element not present on the page where operation is trying to be performed')
        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result,label

    def verify_element_text(self, element , parent ,input, *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        try:
            if launch_keywords.window_name!=None:
                input_val = input[0]
                dektop_element = element.split(';')
                verify_obj = Text_Box()
                check = verify_obj.verify_parent(dektop_element[0],parent)
                if (check == True):
                    label = ldtp.getobjectproperty(launch_keywords.window_name, dektop_element[0],'label')
                    if(link_text == input_val):
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('element not present on the page where operation is trying to be performed')
        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result