#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     21-11-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from launch_keywords import ldtp
import launch_keywords
import logger
import Exceptions
import desktop_constants
import editable_text
from launch_keywords import Launch_Keywords

editable_text=editable_text.Text_Box()
class Util_Keywords():

        def verifyEnabled(self,element,parent,*args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')
            object_xpath=object_xpath[0].strip()
            try:
                if launch_keywords.window_name!=None:
                    if object_xpath!=None and editable_text.verify_parent(object_xpath,parent):
                        states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                        if desktop_constants.ENABLED_CHECK in states:
                            status=desktop_constants.TEST_RESULT_PASS
                            result=desktop_constants.TEST_RESULT_TRUE
                            return status,result
                    else:
                        logger.print_on_console('element not found')
            except Exception as e:
                Exceptions.error(e)
            return status,result

        def verifyDisabled(self,element,parent,*args):
            status=desktop_constants.TEST_RESULT_FAIL
            result=desktop_constants.TEST_RESULT_FALSE
            object_xpath=element.split(';')
            object_xpath=object_xpath[0].strip()
            try:
                if launch_keywords.window_name!=None:
                    if object_xpath!=None and  editable_text.verify_parent(object_xpath,parent):
                        states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                        if not desktop_constants.ENABLED_CHECK in states:
                            status=desktop_constants.TEST_RESULT_PASS
                            result=desktop_constants.TEST_RESULT_TRUE
                            return status,result
                    else:
                        logger.print_on_console('element not found')
            except Exception as e:
                Exceptions.error(e)
            return status,result

        def verifyVisible(self,element,parent,*args):
                status=desktop_constants.TEST_RESULT_FAIL
                result=desktop_constants.TEST_RESULT_FALSE
                object_xpath=element.split(';')
                object_xpath=object_xpath[0].strip()
                try:
                    if launch_keywords.window_name!=None:
                        if object_xpath!=None and  editable_text.verify_parent(object_xpath,parent):
                            states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                            if  desktop_constants.VISIBLE_CHECK in states:
                                status=desktop_constants.TEST_RESULT_PASS
                                result=desktop_constants.TEST_RESULT_TRUE
                                return status,result
                        else:
                            logger.print_on_console('element not found')
                except Exception as e:
                    Exceptions.error(e)
                return status,result

        def verifyExists(self,element,parent,*args):
                status=desktop_constants.TEST_RESULT_FAIL
                result=desktop_constants.TEST_RESULT_FALSE
                object_xpath=element.split(';')
                object_xpath=object_xpath[0].strip()
                try:
                    if launch_keywords.window_name!=None:
                        if object_xpath!=None and  editable_text.verify_parent(object_xpath,parent):
                            states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                            if  desktop_constants.VISIBLE_CHECK in states:
                                status=desktop_constants.TEST_RESULT_PASS
                                result=desktop_constants.TEST_RESULT_TRUE
                                return status,result
                        else:
                            logger.print_on_console('element not found')
                except Exception as e:
                    Exceptions.error(e)
                return status,result

        def verifyHidden(self,element,parent,*args):
                status=desktop_constants.TEST_RESULT_FAIL
                result=desktop_constants.TEST_RESULT_FALSE
                object_xpath=element.split(';')
                object_xpath=object_xpath[0].strip()
                try:
                    if launch_keywords.window_name!=None:
                        if object_xpath!=None and  editable_text.verify_parent(object_xpath,parent):
                            states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                            if  not desktop_constants.VISIBLE_CHECK in states:
                                status=desktop_constants.TEST_RESULT_PASS
                                result=desktop_constants.TEST_RESULT_TRUE
                                return status,result
                        else:
                            logger.print_on_console('element not found')
                except Exception as e:
                    Exceptions.error(e)
                return status,result

        def verifyReadOnly(self,element,parent,*args):
                status=desktop_constants.TEST_RESULT_FAIL
                result=desktop_constants.TEST_RESULT_FALSE
                object_xpath=element.split(';')
                object_xpath=object_xpath[0].strip()
                try:
                    if launch_keywords.window_name!=None:
                        if object_xpath!=None and  editable_text.verify_parent(object_xpath,parent):
                            states=ldtp.getallstates(launch_keywords.window_name,object_xpath)
                            if   desktop_constants.VISIBLE_CHECK in states and desktop_constants.ENABLED_CHECK in states:
                                classID=ldtp.istextstateenabled(launch_keywords.window_name,object_xpath)
                                if int(classID)!=1:
                                    status=desktop_constants.TEST_RESULT_PASS
                                    result=desktop_constants.TEST_RESULT_TRUE
                                    return status,result
                        else:
                            logger.print_on_console('element not found')
                except Exception as e:
                    Exceptions.error(e)
                return status,result

        def setFocus(self,element,parent,*args):
                status=desktop_constants.TEST_RESULT_FAIL
                result=desktop_constants.TEST_RESULT_FALSE
                object_xpath=element.split(';')
                object_xpath=object_xpath[0].strip()

                try:
                    if launch_keywords.window_name!=None:
                        if object_xpath!=None and  editable_text.verify_parent(object_xpath,parent):
                            temp_obj = Launch_Keywords()
                            temp_obj.set_to_foreground()
                            ldtp.wait()
                            objCoordinates=ldtp.getobjectsize(launch_keywords.window_name,object_xpath)
                            xCoordinate = objCoordinates[0] + (50);
                            yCoordinate = objCoordinates[1] + (objCoordinates[3]/2);
                            flagEnable=ldtp.simulatemousemove(0, 0, xCoordinate, yCoordinate);
                            if flagEnable==1:
                                status=desktop_constants.TEST_RESULT_PASS
                                result=desktop_constants.TEST_RESULT_TRUE
                                return status,result
                        else:
                            logger.print_on_console('element not found')
                except Exception as e:
                    Exceptions.error(e)
                return status,result

