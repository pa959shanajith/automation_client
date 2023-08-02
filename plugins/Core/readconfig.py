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
        configvalues = {}
        if os.path.isfile(self.config_path) == True:
            try:
                with open(self.config_path, 'r') as conf:
                    configvalues = json.load(conf)
            except Exception as e:
                configvalues['errorflag'] = e
        else:
            configvalues['configmissing'] = os.path.isfile(self.config_path)
        return configvalues

    def updateconfig(self, config_data):
        #Here, we recieve hole data of configvalues and re-writing the config.json file
        global configvalues
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_data, f, indent = 4)
                configvalues = config_data
        except Exception as e:
            log.error(e)
            log.info("Error occurred while altering config.json")

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
