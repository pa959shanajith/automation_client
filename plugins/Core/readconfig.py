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

import logging
import constants
import json
import os
configvalues = None
proxies_config = {}
log = logging.getLogger('readconfig.py')

class readConfig():

    def __init__(self):
        self.config_path = os.environ["AVO_ASSURE_HOME"] + '/assets/config.json'

    def readJson(self):
        global configvalues
        configvalues={"server_ip":"", "server_port":"", "ignore_certificate":"",
        "chrome_path":"", "chrome_profile":"","bit_64":"", "logFile_Path":"", "screenShot_Flag":"",
        "queryTimeOut":"", "timeOut":"", "stepExecutionWait":"", "displayVariableTimeOut":"",
        "httpStatusCode":"", "delay":"", "ignoreVisibilityCheck":"", "exception_flag":"",
        "server_cert":"", "enableSecurityCheck":"","browser_check":"","tls_security":"","highlight_check":"","firefox_path":"",
        "prediction_for_iris_objects":"","hide_soft_key":"","connection_timeout":"","extn_enabled":"","headless_mode":"","update_check":"","delay_stringinput":"","clear_cache":"","screen_rec":""}
        if os.path.isfile(self.config_path)==True:
            try:
                conf = open(self.config_path, 'r')
                params = json.load(conf)
                conf.close()
                configvalues['server_ip']=params['server_ip']
                configvalues['server_port']=params['server_port']
                configvalues['ignore_certificate']=params['ignore_certificate']
                configvalues['chrome_path']=params['chrome_path']
                configvalues['chrome_profile']=params['chrome_profile']
                configvalues['firefox_path']=params['firefox_path']
                configvalues['bit_64']=params['bit_64']
                configvalues['logFile_Path']=params['logFile_Path']
                configvalues['screenShot_Flag']=params['screenShot_Flag']
                configvalues['queryTimeOut']=params['queryTimeOut']
                configvalues['timeOut']=params['timeOut']
                configvalues['stepExecutionWait']=params['stepExecutionWait']
                configvalues['displayVariableTimeOut'] = params['displayVariableTimeOut']
                configvalues['httpStatusCode']=params['httpStatusCode']
                configvalues['delay']=params['delay']
                configvalues['ignoreVisibilityCheck']=params['ignoreVisibilityCheck']
                configvalues['exception_flag']=params['exception_flag']
                configvalues['server_cert']=params['server_cert']
                configvalues['enableSecurityCheck'] = params['enableSecurityCheck']
                configvalues['browser_check'] = params['browser_check']
                configvalues['tls_security'] = params['tls_security']
                configvalues['highlight_check'] = params['highlight_check']
                configvalues['prediction_for_iris_objects'] = params['prediction_for_iris_objects']
                configvalues['hide_soft_key'] = params['hide_soft_key']
                configvalues['connection_timeout'] = params['connection_timeout']
                configvalues['extn_enabled'] = params['extn_enabled']
                configvalues['update_check'] = params['update_check']
                configvalues['headless_mode'] = params['headless_mode']
                configvalues['delay_stringinput']=params['delay_stringinput']
                configvalues['clear_cache']=params['clear_cache']
                configvalues['screen_rec']=params['screen_rec']
            except Exception as e:
                configvalues['errorflag']=e
        else:
            configvalues['configmissing']=os.path.isfile(self.config_path)
        return configvalues

class readProxyConfig():

    def __init__(self):
        self.proxy_path= AVO_ASSURE_HOME + "/assets/proxy.json"

    def readJson(self):
        if os.path.isfile(self.proxy_path)==True:
            try:
                conf = open(self.proxy_path, 'r')
                proxy = json.load(conf)
                if 'enabled' in proxy and proxy['enabled']== 'Enabled':
                    proxy['password']=self.decrypt(proxy['password'])
                    proxy_url=proxy['username']+":"+proxy['password']+"@"+proxy['url']
                    proxies_config = {"http":"http://"+proxy_url,
                                "https":":https://"+proxy_url}
                elif 'enabled' in proxy and proxy['enabled']== 'Disabled':
                    proxies_config={}
            except Exception as e:
                log.error(e,exc_info=True)
        return proxies_config

    def decrypt(enc):
        import base64
        from Crypto.Cipher import AES
        unpad = lambda s : s[0:-ord(s[-1])]
        enc = base64.b64decode(enc)
        cipher = AES.new(b'\x74\x68\x69\x73\x49\x73\x41\x53\x65\x63\x72\x65\x74\x4b\x65\x79', AES.MODE_ECB)
        return unpad(cipher.decrypt(enc).decode('utf-8'))