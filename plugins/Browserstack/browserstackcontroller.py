import base64
from jira.client import JIRA
import os
import logger
import logging
import requests
from requests.auth import HTTPBasicAuth
import json
import readconfig
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
            response = requests.get(url,headers=headers, verify = self.send_tls_security())
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
                    if 'beta' in browser_version_str:
                        continue
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

    def get_mobileconf_details(self, browserstack_data, socket):
        try:
            BROWSERSTACK_USERNAME = browserstack_data['Browserstack_uname']
            BROWSERSTACK_ACCESS_KEY = browserstack_data['BrowserstackAccessKey']
            DEVICES_API_URL = "https://api-cloud.browserstack.com/app-automate/devices.json"
            APPS_API_URL = "https://api-cloud.browserstack.com/app-automate/recent_apps"
            auth_string = f"{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode()
            headers = {
                "Authorization": f"Basic {encoded_auth}",
            }
 
            response_devices = requests.get(DEVICES_API_URL, headers=headers, verify = self.send_tls_security())
            response_data = {'devices': {}, 'stored_files': {}}
 
            if response_devices.status_code == 200:
                recent_apps_data = response_devices.json()
                devices = {}
                if recent_apps_data:
                    for item in recent_apps_data:
                        os = item["os"]
                        os_version = item["os_version"]
                        device = item["device"]
                        if 'beta' in os_version.lower():
                            continue
                        devices.setdefault(os, {}).setdefault(os_version, []).append(device)
                    device_details = {os: {ver: devices[os][ver] for ver in devices[os]} for os in devices}
                    response_data['devices'] = device_details
 
            response_apks = requests.get(APPS_API_URL, headers=headers, verify = self.send_tls_security())
            if response_apks.status_code == 200:
                app_data = response_apks.json()               
                if isinstance(app_data, list):
                    # Handle the case where app_data is a list of dictionaries
                    stored_files = {apps['app_name']: apps['app_url'] for apps in app_data}
                    response_data['stored_files'] = stored_files
                elif isinstance(app_data, dict) and 'message' in app_data and app_data['message'] == 'No results found':
                    # Handle the case where app_data is a dictionary with a 'message' key
                    response_data['stored_files'] = {}
                    logger.print_on_console('Please Upload apk in Avo Assure Settings of BrowserStack')
                else:
                    logger.print_on_console('Please Upload apk in Avo Assure Settings of BrowserStack')
 
            socket.emit('browserstack_confresponse', response_data)
 
        except requests.exceptions.RequestException as e:
            socket.emit('browserstack_confresponse', 'Request to Browserstack API failed')
        except KeyError as e:
            socket.emit('browserstack_confresponse', 'Missing key in browserstack_data')
        except Exception as e:
            logging.error(e)
            socket.emit('browserstack_confresponse', 'An error occurred while processing the request')

    def uploadApk_bs(self, browserstack_data, socket):
        try:
            api_username = browserstack_data['Browserstack_uname']
            api_key = browserstack_data['BrowserstackAccessKey']
            apk_path = browserstack_data['BrowserstackUploadApk']['apkPath']
            base_url = "https://api-cloud.browserstack.com/app-automate/upload"
            auth_string = f"{api_username}:{api_key}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode()
            headers = {
                "Authorization": f"Basic {encoded_auth}",
            }
        
            try:
                with open(apk_path, "rb") as apk_file:
                    files = {"file": apk_file}
                    response = requests.post(base_url, headers=headers, files=files, verify = self.send_tls_security())
        
                    if response.status_code == 200:
                        socket.emit('browserstack_confresponse','Apk Uploaded Successfully')
                        json_response = response.json()
                        app_url = json_response.get("app_url")
                        if app_url:
                            return app_url,None
                        else:
                            return None, "App URL not found in the response."
                    else:
                        return None, f"Failed to upload APK. Status code: {response.status_code}"
        
            except Exception as e:
                return None, f"An error occurred: {str(e)}"
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('browserstack_confresponse','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('browserstack_confresponse','Invalid Credentials')
            else:
                socket.emit('browserstack_confresponse','Fail')
            logger.print_on_console('Exception in fetching the sauce details')
            
    def send_tls_security(self):
        try:
            tls_security = readconfig.configvalues.get("tls_security")
            if tls_security != None and tls_security.lower() == "low":
                # Make a GET request without SSL certificate verification (not recommended)
                return False
            else:
                # Make a GET request with SSL certificate verification
                return True
        except Exception as e:
            log.error(e)
            logger.print_on_console("ERROR:SSLverify flag as False. Disabled TLS Certificate and Hostname Verification.")
            #by default sending false(if this fuction met exception).you can modify this default return and above logger message.
            return False 
