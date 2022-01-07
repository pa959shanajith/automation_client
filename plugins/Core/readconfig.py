#-------------------------------------------------------------------------------
# Name:        readconfig.py
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
from urllib.parse import quote_plus as encodeURL
configvalues = None
proxies = None
log = logging.getLogger('readconfig.py')


class readConfig():

    def __init__(self):
        self.config_path = constants.CONFIG_PATH

    def readJson(self):
        global configvalues
        configvalues={"server_ip":"", "server_port":"", "ignore_certificate":"",
        "chrome_path":"", "chrome_profile":"","bit_64":"", "logFile_Path":"", "screenShot_Flag":"",
        "queryTimeOut":"", "timeOut":"", "stepExecutionWait":"", "displayVariableTimeOut":"",
        "httpStatusCode":"", "delay":"", "ignoreVisibilityCheck":"", "exception_flag":"",
        "server_cert":"", "enableSecurityCheck":"","browser_check":"","tls_security":"","highlight_check":"",
        "firefox_path":"", "prediction_for_iris_objects":"","hide_soft_key":"","connection_timeout":"","extn_enabled":"",
        "headless_mode":"","update_check":"", "delay_stringinput":"","clear_cache":"","screen_rec":"","full_screenshot":"",
        "close_browser_popup":"","incognito_private_mode":"", "use_custom_debugport":"","disable_screen_timeout":"",
        "globalWaitTimeOut":"", "kill_stale":"","chrome_extnpath":"","browser_screenshots":""}
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
                configvalues['globalWaitTimeOut']=params['globalWaitTimeOut']
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
                configvalues['full_screenshot']=params['full_screenshot']
                configvalues['close_browser_popup']=params['close_browser_popup']
                configvalues['incognito_private_mode']=params['incognito_private_mode']
                configvalues['use_custom_debugport']=params['use_custom_debugport']
                configvalues['disable_screen_timeout']=params['disable_screen_timeout']
                configvalues['chrome_extnpath']=params['chrome_extnpath']
                configvalues['kill_stale']=params['kill_stale']
                configvalues['browser_screenshots']=params['browser_screenshots']
            except Exception as e:
                configvalues['errorflag']=e
        else:
            configvalues['configmissing']=os.path.isfile(self.config_path)
        return configvalues


class readProxyConfig():

    def __init__(self):
        self.proxy_path = constants.PROXY_PATH

    def readRawJson(self):
        proxyobj = None
        def unwrap(enc):
            import base64
            from Crypto.Cipher import AES
            unpad = lambda s : s[0:-ord(s[-1])]
            enc = base64.b64decode(enc)
            cipher = AES.new(b'\x74\x68\x69\x73\x49\x73\x41\x53\x65\x63\x72\x65\x74\x4b\x65\x79', AES.MODE_ECB)
            return unpad(cipher.decrypt(enc).decode('utf-8'))
        if os.path.isfile(self.proxy_path)==True:
            try:
                conf = open(self.proxy_path, 'r')
                proxy = json.load(conf)
                conf.close()
                if 'enabled' in proxy and proxy['enabled'] == 'Enabled':
                    scheme = 'http'
                    if proxy['url'][0:7] == "http://":
                        proxy['url'] = proxy['url'][7:]
                    elif proxy['url'][0:8] == "https://":
                        scheme = 'https'
                        proxy['url'] = proxy['url'][8:]
                    proxy['scheme'] = scheme
                    proxy['password'] = encodeURL(unwrap(proxy['password']))
                    proxyobj = proxy
                elif 'enabled' in proxy and proxy['enabled'] == 'Disabled':
                    proxyobj = {}
            except Exception as e:
                log.error(e,exc_info=True)
        return proxyobj

    def readJson(self):
        global proxies
        proxy = self.readRawJson()
        if proxy:
            proxy_url = proxy['scheme'] + "://" + encodeURL(proxy['username'])+":"+proxy['password']+"@"+proxy['url']
            proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
        else:
            proxies = proxy
        return proxies
