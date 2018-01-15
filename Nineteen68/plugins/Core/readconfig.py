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

##log = logging.getLogger('readconfig.py')

class readConfig():

    def __init__(self):
        self.config_path = os.environ["NINETEEN68_HOME"] + '/config.json'

    def readJson(self):
        configvalues={"server_ip":"", "server_port":"", "ignore_certificate":"",
        "chrome_path":"", "bit_64":"", "logFile_Path":"", "screenShot_Flag":"",
        "queryTimeOut":"", "timeOut":"", "stepExecutionWait":"", "displayVariableTimeOut":"",
        "retrieveURL":"", "delay":"", "ignoreVisibilityCheck":"", "server_cert":""}
        try:
            config = json.loads(open(self.config_path).read())
            params = config['configuration']
            configvalues['server_ip']=params['server_ip']
            configvalues['server_port']=params['server_port']
            configvalues['ignore_certificate']=params['ignore_certificate']
            configvalues['chrome_path']=params['chrome_path']
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
            configvalues['server_cert']=params['server_cert']
        except Exception as e:
            configvalues['errorflag']=e
        return configvalues

