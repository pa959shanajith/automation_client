#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:
# Copyright:   (c) rakesh.v
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from jira.client import JIRA
import os
import logger
import logging
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import json
log = logging.getLogger("saucelabcontroller.py")
import base64
import time
import subprocess
import re

class SaucelabWindow():
    # jira = None
    # def __init__(self,x=0):
    #     self.x = x
    #     self.jira_details=None

    # def connectJIRA(self,jira_serverlocation , jira_uname , jira_pwd ):
    #     try:
    #         jira_options = {'server': jira_serverlocation}
    #         jira = JIRA(options=jira_options,basic_auth=(jira_uname,jira_pwd))
    #         return jira
    #     except Exception as e:
    #         logger.print_on_console("Failed to connect to JIRA")

    def get_webconf_details(self,saucelab_input_dict,socket):
        """
            Method to fetch saucelab configurations
            returns list of os names and respective browser configurations
        """
        res = "invalidcredentials"
        try:
           response = requests.get("https://app.saucelabs.com/rest/v1/info/platforms/webdriver/")
           data = json.loads(response.text)
           # Create empty lists and dictionary to hold the options for each dropdown
           os_names = []
           browser_names = {}
           chrome_versions = []
           firefox_versions = []
           edge_versions = []
           ie_versions = []
           safari_versions = []
           # Extract the OS name, browser name, and version for each platform and add them to the corresponding list
           for platform in data:
                os_name = platform['os']
                browser_name = platform['long_name']
                browser_version = platform['short_version']

                # Add OS name to the list
                if os_name not in os_names:
                    os_names.append(os_name)

                # Add browser versions to the corresponding browser dictionary
                if browser_name == 'Google Chrome':
                    if browser_name not in browser_names:
                        browser_names[browser_name] = {}
                    if browser_version.isdigit() and int(browser_version) >= 75:
                        if browser_version not in chrome_versions:
                            chrome_versions.append(browser_version)
                        if os_name not in browser_names[browser_name]:
                            browser_names[browser_name][os_name] = []
                        browser_names[browser_name][os_name].append(browser_version)
                elif browser_name == 'Firefox':
                    if browser_name not in browser_names:
                        browser_names[browser_name] = {}
                    if browser_version.isdigit() and int(browser_version) >= 75:
                        if browser_version not in firefox_versions:
                            firefox_versions.append(browser_version)
                        if os_name not in browser_names[browser_name]:
                            browser_names[browser_name][os_name] = []
                        browser_names[browser_name][os_name].append(browser_version)
                elif browser_name == 'Microsoft Edge':
                    if browser_name not in browser_names:
                        browser_names[browser_name] = {}
                    if browser_version.isdigit() and int(browser_version) >= 75:
                        if browser_version not in edge_versions:
                            edge_versions.append(browser_version)
                        if os_name not in browser_names[browser_name]:
                            browser_names[browser_name][os_name] = []
                        browser_names[browser_name][os_name].append(browser_version)
                elif browser_name == 'Safari':
                    if browser_name not in browser_names:
                        browser_names[browser_name] = {}
                    if browser_version.isdigit():
                        if browser_version not in safari_versions:
                            safari_versions.append(browser_version)
                        if os_name not in browser_names[browser_name]:
                                browser_names[browser_name][os_name] = []
                        browser_names[browser_name][os_name].append(browser_version)
                elif browser_name == 'Internet Explorer':
                    if browser_name not in browser_names:
                        browser_names[browser_name] = {}
                    if browser_version.isdigit():
                        if browser_version not in ie_versions:
                            ie_versions.append(browser_version)
                        if os_name not in browser_names[browser_name]:
                            browser_names[browser_name][os_name] = []
                        browser_names[browser_name][os_name].append(browser_version)

            # Create the API response dictionary
           res = {'os_names': sorted([os_name for os_name in os_names]),
                            'browser': browser_names}
           socket.emit('sauceconfresponse',res)

        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('sauceconfresponse','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('sauceconfresponse','Invalid Credentials')
            else:
                socket.emit('sauceconfresponse','Fail')
            logger.print_on_console('Exception in fetching the sauce details')


    def get_mobileconf_details(self,saucleb_input_dict,socket):
        """
                Method to fetch saucelab configurations
                returns list of os names and respective browser configurations
        """
        res = "invalidcredentials"
        try:
            authorization = str(base64.b64encode(bytes(saucleb_input_dict['SauceLabusername']+':'+saucleb_input_dict['SauceLabAccessKey'], 'ascii')), 'ascii')
            headers = {
                'Authorization': 'Basic '+authorization
            }
            http = urllib3.PoolManager()
            # response = requests.get('https://app.saucelabs.com/rest/v1/info/platforms/webdriver',headers=headers)
            # response = http.request('GET', 'https://app.saucelabs.com/rest/v1/info/platforms/webdriver', headers=headers)
            retry_limit = 10
            retry_counter = 0
            while retry_counter < retry_limit:
                try:
                    # Send request to API endpoint
                    # respon = requests.post(endpoint_url, headers=headers, json=body)
                    response = http.request('GET', 'https://app.saucelabs.com/rest/v1/info/platforms/webdriver', headers=headers)
                    if response.status != 200:
                        log.info("Unable to connect to server retrying Status code is: %s",
                            response.status)
                        logger.print_on_console("Connection error occurred in Fetching Emulator Device Details")
                        time.sleep(2)
                    else:
                        break
                except Exception as e:
                    log.error(e)
                    logger.print_on_console("Unable to connect to server retrying.")
                    time.sleep(2)
                retry_counter += 1
            if retry_counter == retry_limit:
                logger.print_on_console("Maximum retry limit reached. Unable to connect to the server.")
            data = response.data.decode('utf-8')

            # if response.status_code == 200:
            # if True:

            data = json.loads(data)
            androidVersions = {}
            iphoneVersions = {}
            for detail in data:
                if detail['api_name'] == 'android':
                    if detail['short_version'] not in androidVersions.keys():
                        androidVersions[detail['short_version']] = []
                    androidVersions[detail['short_version']].append(detail['long_name'])
                if detail['api_name'] == 'iphone':
                    if detail['short_version'] not in iphoneVersions.keys():
                        iphoneVersions[detail['short_version']] = []
                    iphoneVersions[detail['short_version']].append(detail['long_name'])

            res = {}
            res['emulator'] = {
                    'android' : androidVersions,
                    'iphone': iphoneVersions
                }

            # response_real_devices = requests.get('https://api.us-west-1.saucelabs.com/v1/rdc/devices',headers=headers,timeout = 120)
            retry_limit1 = 10
            retry_counter1 = 0
            while retry_counter1 < retry_limit1:
                try:
                    # Send request to API endpoint
                    # respon = requests.post(endpoint_url, headers=headers, json=body)
                    response_real_devices = requests.get('https://api.us-west-1.saucelabs.com/v1/rdc/devices',headers=headers)
                    if response_real_devices.status_code != 200:
                        log.info("Unable to connect to server retrying Status code is: %s",
                            response_real_devices.status_code)
                        logger.print_on_console("Connection error occurred in Fetching Real Device Details")
                        time.sleep(2)
                    else:
                        break
                except Exception as e:
                    log.error(e)
                    logger.print_on_console("Unable to connect to server retrying.")
                    time.sleep(2)
                retry_counter1 += 1
            if retry_counter1 == retry_limit1:
                logger.print_on_console("Maximum retry limit reached. Unable to connect to the server.")
                
            if response_real_devices.status_code== 200:
                data = json.loads(response_real_devices.text)
                androidVersions = {}
                iphoneVersions = {}
                for detail in data:
                    if detail['os'] == 'ANDROID':
                        if detail['osVersion'] not in androidVersions.keys():
                            androidVersions[detail['osVersion']] = []
                        androidVersions[detail['osVersion']].append(detail['name'])
                    if detail['os'] == 'IOS':
                        if detail['osVersion'] not in iphoneVersions.keys():
                            iphoneVersions[detail['osVersion']] = []
                        iphoneVersions[detail['osVersion']].append(detail['name'])

                res['real_devices'] = {
                        'android' : androidVersions,
                        'iphone': iphoneVersions
                    }

                if saucleb_input_dict['action'] == 'sauceMobileWebDetails' :
                    authorization = str(base64.b64encode(bytes(saucleb_input_dict['SauceLabusername'] +':'+saucleb_input_dict['SauceLabAccessKey'], 'ascii')), 'ascii')
                    headers = {
                        'Authorization': 'Basic '+authorization
                    }
                    # storage_url = 'https://api.us-west-1.saucelabs.com/v1/storage/files'
                    # response = requests.get(storage_url, headers=headers)
                    
                    retry_limit2 = 10
                    retry_counter2 = 0
                    while retry_counter2 < retry_limit2:
                        try:
                            # Send request to API endpoint
                            # respon = requests.post(endpoint_url, headers=headers, json=body)
                            storage_url = 'https://api.us-west-1.saucelabs.com/v1/storage/files'
                            response = requests.get(storage_url, headers=headers)
                            if response.status_code != 200:
                                log.info("Unable to connect to server retrying Status code is: %s",
                                    response.status_code)
                                logger.print_on_console("Error Ocuured while Fetch Mobile APK")
                                time.sleep(2)
                            else:
                                break
                        except Exception as e:
                            log.error(e)
                            logger.print_on_console("Unable to connect to server retrying.")
                            time.sleep(2)
                        retry_counter2 += 1
                    if retry_counter2 == retry_limit2:
                        logger.print_on_console("Maximum retry limit reached. Unable to connect to the server.")


                    stored_files = []
                    if response.status_code == 200:
                        storage_data = response.json()
                        for items in storage_data['items']:
                            if items['kind'] == 'android':
                                stored_files.append({
                                    'id':items['id'],
                                    'name':items['name'],
                                    'group_id': items['group_id'],
                                    'kind': items['kind'],
                                    'appPackageName': items['metadata']['identifier']
                                })
                    
                    res['stored_files'] = stored_files
                
            socket.emit('sauceconfresponse',res)
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('sauceconfresponse','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('sauceconfresponse','Invalid Credentials')
            else:
                socket.emit('sauceconfresponse','Fail')
            logger.print_on_console('Exception in fetching the sauce details')

    def update_mobile_details(self,saucleb_input_dict,socket):
        """
                Method to upload saucelab mobile configurations
                returns list of os names and respective browser configurations
        """
        res = "invalidcredentials"
        try:
            username = saucleb_input_dict['SauceLabusername']
            access_key = saucleb_input_dict['SauceLabAccessKey']
            upload_url = "https://api.us-west-1.saucelabs.com/v1/storage/upload"
            apk_path = saucleb_input_dict['SauceLabUploadApk']['apkPath']
            with open(apk_path, "rb") as file:
                apk_data = file.read()

            files = {
                'payload': apk_data,
                'name': saucleb_input_dict['SauceLabUploadApk']['apkName']
            }

            auth = (username, access_key)

            response = requests.post(upload_url, files=files, auth=auth)
            aapt_path=os.environ['ANDROID_HOME']+"\\build-tools\\33.0.1\\aapt.exe"
            try:
                result = subprocess.run([aapt_path, 'dump', 'badging', apk_path], capture_output=True, text=True, check=True)
                output = result.stdout
            except subprocess.CalledProcessError as e:
                print(f"Error executing aapt.exe: {e}")
                exit(1)
            # Use regular expressions to extract the app activity from the output
            match = re.search(r"launchable-activity: name='([^']*)'", output)
            if match:
                res = match.group(1)
                print(f"App Activity: {res}")
            else:
                print("Unable to find app activity in the APK file.")

            data_to_server = {
                "name": saucleb_input_dict['SauceLabUploadApk']['apkName'],
                "activity": res
            }


            socket.emit('sauceconfresponse', data_to_server)
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('sauceconfresponse','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('sauceconfresponse','Invalid Credentials')
            else:
                socket.emit('sauceconfresponse','Fail')
            logger.print_on_console('Exception in fetching the sauce details')
        