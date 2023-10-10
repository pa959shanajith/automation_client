import base64
from jira.client import JIRA
import os
import logger
import logging
import requests
from requests.auth import HTTPBasicAuth
import json
log = logging.getLogger("browserstackcontroller.py")


class BrowserstackWindow():
    def get_webconf_details(self,browserstack_data, socket):
        res = "invalidcredentials"
        try:
            browserstack_data['Browserstack_uname']
            browserstack_data['BrowserstackAccessKey']
            authorization = str(base64.b64encode(
            bytes(browserstack_data['Browserstack_uname']+':'+browserstack_data['BrowserstackAccessKey'], 'ascii')), 'ascii')
            headers = {
                'Authorization': 'Basic '+authorization
            }
            url = "https://api.browserstack.com/automate/browsers.json"
            response = requests.get(url,headers=headers)
            data = response.json()
            sorted_os = {
                "os": {}
            }

            # Sort by OS
            for item in data:
                os = item["os"]
                if os == "Windows":
                    sorted_os["os"][os] = os
                elif os == "OS X":
                    sorted_os["os"][os] = "OS X"

            final_sorted_os = sorted_os["os"]  # Extract the nested dictionary

            # Sort by OS Version
            os_versions = {}

            for version_os in data:
                if version_os['os']!='ios' and version_os['os']!='android':
                    os_name = version_os["os"]
                    os_version = version_os["os_version"]
                    
                    if os_name not in os_versions:
                        os_versions[os_name] = []
                    if os_name == 'Windows' and os_version == 'XP':
                        continue
                    if os_name =='OS X'and os_version =='Snow Leopard':
                        continue
                    if os_name =='OS X'and os_version =='Lion':
                        continue
                    if os_name =='OS X'and os_version =='Mountain Lion':
                        continue
                    if os_version not in os_versions[os_name]:
                        os_versions[os_name].append(os_version)

            browser = {}

            for browser_version in data:
                if browser_version['browser'] not in ["android", "iphone", "ipad", "samsung"]:
                    browser_name = browser_version["browser"]
                    if browser_name == 'ie':
                        browser_name = 'Internet Explorer'
                    if browser_name == 'chrome':
                        browser_name = 'Google Chrome'  
                    if browser_name == 'edge':
                        browser_name = 'Microsoft Edge'
                    if browser_name == 'firefox':
                        browser_name = 'Firefox' 
                    if browser_name == 'safari':
                        continue       
                    os_name = browser_version["os"]
                    os_version = browser_version["os_version"]
                    browser_version_str = browser_version["browser_version"]
                    
                    
                        browser_version_num = float(browser_version_str)
                        if (browser_name == 'Internet Explorer' or browser_name == 'safari') or (browser_name != 'ie' and browser_name != 'safari' and browser_version_num >= 75):
                            if browser_name not in browser:
                                browser[browser_name] = {}
                            
                            os_osversion_key = os_name + ' ' + os_version
                            if os_osversion_key not in browser[browser_name]:
                                browser[browser_name][os_osversion_key] = []
                            
                            browser[browser_name][os_osversion_key].append(browser_version_str)
                   
                        

            res = {'os': final_sorted_os,'os_names': os_versions, 'browser': browser}
            socket.emit('browserstack_confresponse', res)

        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('browserstack_confresponse', 'Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('browserstack_confresponse', 'Invalid Credentials')
            else:
                socket.emit('browserstack_confresponse', 'Fail')
            logger.print_on_console('Exception in fetching the browserstcak details')
