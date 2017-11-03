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

log = logging.getLogger('Dispatcher.py')

class MainframeDispatcher:
    mainframe_obj=mainframe_keywords.MainframeKeywords()

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
        except Exception as e:
            log.error(e)
            import traceback
            traceback.print_exc()
        return result