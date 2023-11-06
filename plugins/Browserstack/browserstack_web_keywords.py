import os
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from timeit import default_timer as timer
from datetime import timedelta
import time
from constants import *
import threading
import browserstack_constants

local_bwk=threading.local()
log=logging.getLogger('browserstack_web_keywords.py')

class Browser_Keywords:

    def __init__(self):
        # self.obj=Textbox_Keywords()
        pass
    
    def openBrowser(self,url,browser,scenario,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        local_bwk.driver = webdriver.Remote(command_executor=url, desired_capabilities=browser)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def navigateToURL(self,input,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        url=input[0]
        if url[0:7].lower()!='http://' and url[0:8].lower()!='https://' and url[0:5].lower()!='file:':
            url='http://'+url
        input=url
        local_bwk.driver.get(input)
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg

    def closeBrowser(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_val=OUTPUT_CONSTANT
        local_bwk.driver.quit()
        status=TEST_RESULT_PASS
        methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output_val,err_msg


class Browserstack_config():

    def save_browserstackconf(self,*args):
        # self.username = args[0]["sauce_username"]
        # self.access_key = args[0]["sauce_access_key"]
        # self.platform = args["platform"]
        # self.url = args[0]["remote_url"]
        if args[0]['apptype'] == 'Web':
            if args[0]['browserName'] == 'Google Chrome':
                args[0]['browserName'] = 'Chrome'
            if args[0]['browserName'] == 'Microsoft Edge':
                args[0]['browserName'] = 'edge'
            if args[0]['browserName'] == 'Firefox':
                args[0]['browserName'] = 'firefox'
            if args[0]['browserName'] == 'Internet Explorer':
                args[0]['browserName'] = 'ie'
            
            browserstack_constants.Browserstack_Username = args[0]["browserstack_username"]
            browserstack_constants.Browserstack_key = args[0]["browserstack_access_key"]
            browserstack_constants.os = args[0]['os']
            browserstack_constants.osVersion = args[0]['osVersion']
            browserstack_constants.browserVersion = args[0]['browserVersion']
            browserstack_constants.browserName = args[0]['browserName']

        elif args[0]['apptype'] == 'MobileWeb':
            browserstack_constants.Browserstack_Username = args[0]["browserstack_username"]
            browserstack_constants.Browserstack_key = args[0]["browserstack_access_key"]
            browserstack_constants.Mobile =  args[0]['Mobile']
        elif args[0]['apptype'] == 'MobileApp':
            browserstack_constants.Browserstack_Username = args[0]["browserstack_username"]
            browserstack_constants.Browserstack_key = args[0]["browserstack_access_key"]
            browserstack_constants.Mobile =  args[0]['Mobile']
        else:
            logger.print_on_console("App type Not available")
        url = "https://{}:{}@hub.browserstack.com/wd/hub".format(browserstack_constants.Browserstack_Username,browserstack_constants.Browserstack_key)
        browserstack_constants.remote_url = url

        return

    def get_browserstackconf(self):
        conf = {
           'os': browserstack_constants.os,
           'os_version': browserstack_constants.osVersion,
           'browser_version': browserstack_constants.browserVersion,
           'browser':browserstack_constants.browserName,
           'browserstack_username': browserstack_constants.Browserstack_Username,
           'browserstack_access_key': browserstack_constants.Browserstack_key,
           'remote_url': browserstack_constants.remote_url,
           'Mobile': browserstack_constants.Mobile,
        }
        self.username = conf["browserstack_username"]
        self.access_key = conf["browserstack_access_key"]
        self.remote_url = conf["remote_url"]
        self.os = conf["os"]
        self.os = conf["Mobile"]
        return conf