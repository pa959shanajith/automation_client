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
import json
log = logging.getLogger("saucelabcontroller.py")
import base64


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
            response = requests.get('https://app.saucelabs.com/rest/v1/info/platforms/webdriver',headers=headers)
            
            if response.status_code == 200:
                data = json.loads(response.text)
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

            response_real_devices = requests.get('https://api.us-west-1.saucelabs.com/v1/rdc/devices',headers=headers)
            if response_real_devices.status_code == 200:
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
        