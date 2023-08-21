import os
filename=""
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
# from selenium import webdriver
from appium import webdriver
import time
from constants import *
import logger
import sauceclient
import threading
import saucelab_constants
from constants import *

import threading

# local_wk=threading.local()

local_mak=threading.local()
log=logging.getLogger('web_keywords_MA.py')
def request_content(self, url, filename, dirpath=None, body=None, content_type=''):
    """Send http request for asset content"""
    headers = self.make_auth_headers(content_type)
    connection = sauceclient.http_client.HTTPSConnection('saucelabs.com')
    full_url = url + 'screenshots.zip'
    filename1 = 'SaucelabsScreenshots_'+filename + '.zip'
    connection.request('GET', full_url, body, headers=headers)
    response1 = connection.getresponse()
    data = response1.read()
    if dirpath:
        if os.path.exists(dirpath):
            full_path = os.path.join(dirpath, filename1)
            log.info('Screenshot Asset Path: '+full_path)
            with open(full_path, 'wb') as file_handle:
                file_handle.write(data)
        else:
            raise NotADirectoryError("Path does not exist")
    else:
        with open(filename1, 'wb') as file_handle:
            file_handle.write(data)
    full_url = url + 'video.mp4'
    filename2 = 'ScreenRecording_' +filename + '.mp4'
    connection.request('GET', full_url, body, headers=headers)
    response2 = connection.getresponse()
    data = response2.read()
    if dirpath:
        if os.path.exists(dirpath):
            full_path = os.path.join(dirpath, filename2)
            log.info("Video Asset Path: "+full_path)
            with open(full_path, 'wb') as file_handle:
                file_handle.write(data)
        else:
            raise NotADirectoryError("Path does not exist")
    else:
        with open(filename2, 'wb') as file_handle:
            file_handle.write(data)
    connection.close()
    if response1.status not in [200, 201]:
        raise sauceclient.SauceException('{}: {}.\nSauce Status NOT OK'.format(
            response1.status, response1.reason), response1=response1)
    if response2.status not in [200, 201]:
        raise sauceclient.SauceException('{}: {}.\nSauce Status NOT OK'.format(
            response2.status, response2.reason), response2=response2)
    return True

def get_job_asset_content(self, job_id, filename, dirpath=None):
    """Get content collected for a specific asset on a specific job."""
    endpoint = 'https://saucelabs.com/rest/v1/{}/jobs/{}/assets/'.format(
        self.client.sauce_username, job_id)
    return self.client.request_content(endpoint,filename,dirpath)

sauceclient.SauceClient.request_content = request_content
sauceclient.Jobs.get_job_asset_content = get_job_asset_content

class LaunchAndInstallSL():

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e

    def installApplication(self, inputs_value, *args):
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        driver = ''
        try:
            url = 'https://ondemand.us-west-1.saucelabs.com:443/wd/hub'
            local_mak.driver = webdriver.Remote(command_executor=url, desired_capabilities=args[0])
            log.info(local_mak.driver)
            log.info("APP INSTALLED")
            status = TEST_RESULT_PASS
            result = TEST_RESULT_TRUE
        except Exception as e:
            err_msg = self.print_error("Not able to install or launch application")
            log.error(e,exc_info=True)    
        return status, result, output, err_msg

class Sauce_Config():

    def save_sauceconf(self,*args):
        saucelab_constants.Saucelabs_Username = args[0]["sauce_username"]
        saucelab_constants.Saucelabs_key = args[0]["sauce_access_key"]
        saucelab_constants.Saucelabs_Url = args[0]["remote_url"]
        saucelab_constants.Mobile = args[0]['mobile']
        return

    def get_sauceconf(self):
        Saucelabs_config_path=os.environ['AVO_ASSURE_HOME']+os.sep+'assets'+os.sep+'sauce_config.json'
        import json
        # self.proxies=self.conf["proxy"]
        conf = {
            'platform': saucelab_constants.Platform,
            'sauce_username': saucelab_constants.Saucelabs_Username,
            'sauce_access_key': saucelab_constants.Saucelabs_key,
            'remote_url': saucelab_constants.Saucelabs_Url,
            'mobile': saucelab_constants.Mobile
        }
        self.username = conf["sauce_username"]
        self.access_key = conf["sauce_access_key"]
        self.platform = conf["platform"]
        self.url = conf["remote_url"]
        return conf

    def get_sauceclient(self):
        return sauceclient.SauceClient(self.username,self.access_key)

    def get_saucejobs(self, sc):
        return sauceclient.Jobs(sc)