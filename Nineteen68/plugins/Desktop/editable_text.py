#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     17-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import ldtp
import desktop_constants
from encryption_utility import AESCipher
import logger
import Exceptions
import launch_keywords

class Text_Box:
    def set_text(self , element , parent , input_val ,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        try:
            if launch_keywords.window_name!=None:
                dektop_element = element.split(';')
                input_val = input_val[0]
                check = self.verify_parent(dektop_element[0],parent)
                if (check == True):
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    if(desktop_constants.ENABLED_CHECK in states):
                        ldtp.grabfocus(launch_keywords.window_name,dektop_element[0])
                        ldtp.activatetext(launch_keywords.window_name,dektop_element[0])
                        ldtp.settextvalue(launch_keywords.window_name,dektop_element[0], input_val)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        logger.log('Element state does not allow to perform the operation')
                else:
                    logger.log('element not present on the page where operation is trying to be performed')
        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result


    def set_secure_text(self, element , parent , input_val , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        try:
            if launch_keywords.window_name!=None:
                dektop_element = element.split(';')
                input_val = input_val[0]
                check = self.verify_parent(dektop_element[0],parent)
                if (check == True):
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    if(desktop_constants.ENABLED_CHECK in states):
                        ldtp.grabfocus(launch_keywords.window_name,dektop_element[0])
                        ldtp.activatetext(launch_keywords.window_name,dektop_element[0])
                        encryption_obj = AESCipher()
                        input_val_temp = encryption_obj.decrypt(launch_keywords.window_name)
                        ldtp.settextvalue(launch_keywords.window_name,dektop_element[0],input_val_temp)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        logger.log('Element state does not allow to perform the operation')
                else:
                    logger.log('element not present on the page where operation is trying to be performed')
        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result

    def get_text(self, element , parent  , *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        try:
            if launch_keywords.window_name!=None:
                dektop_element = element.split(';')
                check = self.verify_parent(dektop_element[0],parent)
                if (check == True):
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    if(desktop_constants.ENABLED_CHECK in states):
                        ldtp.grabfocus(launch_keywords.window_name,dektop_element[0])
                        ldtp.activatetext(launch_keywords.window_name,dektop_element[0])
                        output = ldtp.gettextvalue(launch_keywords.window_name,dektop_element[0])
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        logger.log('Element state does not allow to perform the operation')
                else:
                    logger.log('element not present on the page where operation is trying to be performed')
        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result,output

    def clear_text(self, element , parent, *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        try:
            if launch_keywords.window_name!=None:
                dektop_element = element.split(';')
                check = self.verify_parent(dektop_element[0],parent)
                if (check == True):
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    if(desktop_constants.ENABLED_CHECK in states):
                        index = 0
                        ldtp.grabfocus(launch_keywords.window_name,dektop_element[0])
                        ldtp.activatetext(launch_keywords.window_name,dektop_element[0])
                        ldtp.deletetext(launch_keywords.window_name,dektop_element[0],index)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        logger.log('Element state does not allow to perform the operation')
                else:
                    logger.log('element not present on the page where operation is trying to be performed')
        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result

    def verify_text(self, element , parent , input_val, *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        try:
            if launch_keywords.window_name!=None:
                dektop_element = element.split(';')
                input_val = input_val[0]
                check = self.verify_parent(dektop_element[0],parent)
                if (check == True):
                    states = ldtp.getallstates(launch_keywords.window_name,dektop_element[0])
                    if(desktop_constants.ENABLED_CHECK in states):
                        ldtp.grabfocus(launch_keywords.window_name,dektop_element[0])
                        ldtp.activatetext(launch_keywords.window_name,dektop_element[0])
                        output = ldtp.gettextvalue(launch_keywords.window_name,dektop_element[0])
                        if (output == input_val):
                            status = desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                    else:
                        logger.log('Element state does not allow to perform the operation')
                else:
                    logger.log('element not present on the page where operation is trying to be performed')
        except LdtpExecutionError as exception:
            Exceptions.error(exception)
        return status,result,output



    def verify_parent(self,element,parent):
        try:
            real_parent=ldtp.getobjectproperty(launch_keywords.window_name,element,'parent')
            parent=parent.strip()
            if(parent == 'pagetitle'):
                parent=launch_keywords.window_name
            if(parent[0:3] == 'dlg'):
                parent = parent.replace('dlg','')
            if(real_parent[0:3] == 'dlg'):
                real_parent = real_parent.replace('dlg','')
            real_parent = real_parent.replace(' ','')
            parent = parent.replace(' ','')
            if(real_parent == parent):
                return True
            else:
                logger.log('verify parent is false')
                return False
        except Exception as e:
            Exceptions.error(e)


