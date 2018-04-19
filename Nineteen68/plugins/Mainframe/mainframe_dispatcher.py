#-------------------------------------------------------------------------------
# Name:        mainframe_dispatcher.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     25/10/2017
# Updated      25/10/2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import mainframe_keywords
import logger
from mainframe_constants import *
import logging
import readconfig
import constants
import screenshot_keywords
log = logging.getLogger('mainframe_dispatcher.py')

class MainframeDispatcher:

    mainframe_obj=mainframe_keywords.MainframeKeywords()

    def __init__(self):
        self.exception_flag=''
        self.action = None

    def dispatcher(self,teststepproperty,input):
        objectname = teststepproperty.objectname
        objectname = objectname.strip()
        keyword = teststepproperty.name.lower()
        err_msg=None
        result=[TEST_RESULT_FAIL,TEST_RESULT_FALSE,OUTPUT_CONSTANT,err_msg]

        try:
            keyword_dict={
                'launchmainframe': self.mainframe_obj.launch_mainframe,
                'connectsession': self.mainframe_obj.connect_session,
                'login': self.mainframe_obj.login,
                'securelogin': self.mainframe_obj.secure_login,
                'logoff': self.mainframe_obj.logoff,
                'sendvalue': self.mainframe_obj.send_value,
                'submitjob': self.mainframe_obj.submit_job,
                'jobstatus': self.mainframe_obj.job_status,
                'sendfunctionkeys': self.mainframe_obj.send_function_keys,
                'gettext': self.mainframe_obj.get_text,
                'settext': self.mainframe_obj.set_text,
                'setcursor': self.mainframe_obj.set_cursor,
                'verifytextexists': self.mainframe_obj.verify_text_exists,
                'disconnectsession': self.mainframe_obj.disconnect_session,
                'closemainframe': self.mainframe_obj.close_mainframe
            }

            if keyword in keyword_dict.keys():
                result=keyword_dict[keyword](input)
            else:
                err_msg=INVALID_KEYWORD
                logger.print_on_console(err_msg)
                result[3]=err_msg
            configobj = readconfig.readConfig()
            configvalues = configobj.readJson()
            screen_shot_obj = screenshot_keywords.Screenshot()
            if self.action == constants.EXECUTE:
                if result !=constants.TERMINATE:
                    result=list(result)
                    if configvalues['screenShot_Flag'].lower() == 'fail':
                        if result[0].lower() == 'fail':
                            file_path = screen_shot_obj.captureScreenshot()
                            result.append(file_path[2])
                    elif configvalues['screenShot_Flag'].lower() == 'all':
                        file_path = screen_shot_obj.captureScreenshot()
                        result.append(file_path[2])
        except Exception as e:
            log.error(e)
        return result