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
log = logging.getLogger('Dispatcher.py')

class MainframeDispatcher:

    mainframe_obj=mainframe_keywords.MainframeKeywords()

    def __init__(self):
        self.exception_flag=''
        self.action = None

    def dispatcher(self,teststepproperty,input):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name
        err_msg=None
        result=[TEST_RESULT_FAIL,TEST_RESULT_FALSE,OUTPUT_CONSTANT,err_msg]

        try:
            dict={'LaunchMainframe' : self.mainframe_obj.launch_mainframe,
                  'Login' : self.mainframe_obj.login,
                  'SecureLogin' : self.mainframe_obj.secure_login,
                  'LogOff' : self.mainframe_obj.logoff,
                  'SendValue' : self.mainframe_obj.send_value,
                  'SubmitJob' : self.mainframe_obj.submit_job,
                  'JobStatus' : self.mainframe_obj.job_status,
                  'SendFunctionKeys' : self.mainframe_obj.send_function_keys,
                  'GetText' : self.mainframe_obj.get_text,
                  'SetText' : self.mainframe_obj.set_text,
                  'SetCursor' : self.mainframe_obj.set_cursor,
                  'VerifyTextExists' : self.mainframe_obj.verify_text_exists
                  }

            if keyword in dict.keys():
                result=dict[keyword](input)
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
            import traceback
            traceback.print_exc()
        return result