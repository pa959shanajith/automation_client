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

##log = logging.getLogger('readconfig.py')

class readConfig():

##    def __init__(self,node_ip,node_port,screenShot_PathName,ignore_certificate,chrome_path,bit_64,logFile_Path,screenShot_Flag,queryTimeOut,timeOut,stepExecutionWait):
##        self.node_ip=node_ip
##        self.node_port=node_port
##        self.screenShot_PathName=screenShot_PathName
##        self.ignore_certificate=ignore_certificate
##        self.chrome_path=chrome_path
##        self.bit_64=bit_64
##        self.logFile_Path=logFile_Path
##        self.screenShot_Flag=screenShot_Flag
##        self.queryTimeOut=queryTimeOut
##        self.timeOut=timeOut
##        self.stepExecutionWait = stepExecutionWait


    def readJson(self):
##        global configvalues
        configvalues={}
        config = json.loads(open('config.json').read())
        params=config['configuration']
        configvalues['node_ip']=params['node_ip']
        configvalues['node_port']=params['node_port']
        configvalues['screenShot_PathName']=params['screenShot_PathName']
        configvalues['ignore_certificate']=params['ignore_certificate']
        configvalues['chrome_path']=params['chrome_path']
        configvalues['bit_64']=params['bit_64']
        configvalues['logFile_Path']=params['logFile_Path']
        configvalues['screenShot_Flag']=params['screenShot_Flag']
        configvalues['queryTimeOut']=params['queryTimeOut']
        configvalues['timeOut']=params['timeOut']
        configvalues['stepExecutionWait']=params['stepExecutionWait']
        configvalues['displayVariableTimeOut'] = params['displayVariableTimeOut']
        return configvalues
##        Config=readConfig(node_ip,node_port,screenShot_PathName,ignore_certificate,chrome_path,bit_64,logFile_Path,screenShot_Flag,queryTimeOut,timeOut,stepExecutionWait)





