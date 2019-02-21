#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     13-02-2017
# Copyright:   (c) prudhvi.gujjuboyina 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger
import logging
import constants
import json
import os
configvalues = None
##log = logging.getLogger('readconfig.py')

class readConfig():

    def __init__(self):
        self.config_path = os.environ["NINETEEN68_HOME"] + '/Lib/config.json'

    def readJson(self):
        global configvalues
        configvalues={"server_ip":"", "server_port":"", "ignore_certificate":"",
        "chrome_path":"", "bit_64":"", "logFile_Path":"", "screenShot_Flag":"",
        "queryTimeOut":"", "timeOut":"", "stepExecutionWait":"", "displayVariableTimeOut":"",
        "retrieveURL":"", "delay":"", "ignoreVisibilityCheck":"", "exception_flag":"",
        "server_cert":"", "enableSecurityCheck":"","browser_check":"","disable_server_cert":"","highlight_check":"","firefox_path":"",
        "prediction_for_iris_objects":""}
        if os.path.isfile(self.config_path)==True:
            try:
                params = json.load(open(self.config_path))
                configvalues['server_ip']=params['server_ip']
                configvalues['server_port']=params['server_port']
                configvalues['ignore_certificate']=params['ignore_certificate']
                configvalues['chrome_path']=params['chrome_path']
                configvalues['firefox_path']=params['firefox_path']
                configvalues['bit_64']=params['bit_64']
                configvalues['logFile_Path']=params['logFile_Path']
                configvalues['screenShot_Flag']=params['screenShot_Flag']
                configvalues['queryTimeOut']=params['queryTimeOut']
                configvalues['timeOut']=params['timeOut']
                configvalues['stepExecutionWait']=params['stepExecutionWait']
                configvalues['displayVariableTimeOut'] = params['displayVariableTimeOut']
                configvalues['retrieveURL']=params['retrieveURL']
                configvalues['delay']=params['delay']
                configvalues['ignoreVisibilityCheck']=params['ignoreVisibilityCheck']
                configvalues['exception_flag']=params['exception_flag']
                configvalues['server_cert']=params['server_cert']
                configvalues['enableSecurityCheck'] = params['enableSecurityCheck']
                configvalues['browser_check'] = params['browser_check']
                configvalues['disable_server_cert'] = params['disable_server_cert']
                configvalues['highlight_check'] = params['highlight_check']
                configvalues['prediction_for_iris_objects'] = params['prediction_for_iris_objects']
            except Exception as e:
                configvalues['errorflag']=e
        else:
            configvalues['configmissing']=os.path.isfile(self.config_path)
        return configvalues