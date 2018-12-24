from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pyautogui
import unittest
import json

FIREFOX_BROWSER_VERSION = {"0.13":[52,53],"0.16":[52,53],"0.19":[55,62],"0.21":[55,62]}
CHROME_DRIVER_VERSION = {"2.41":[67,69],"2.40":[66,68],"2.39":[66,68],"2.38":[65,67],"2.37":[64,66],"2.36":[63,65],"2.35":[62,65]}

##class TestBrowser(unittest.TestCase):
def check_browser(input):
    global chromeFlag,firefoxFlag
    chromeFlag=None
    firefoxFlag=None
    status="false"
    configvalues={}
##    chromeFlag=False
##    firefoxFlag=False
    try:
##        import pdb; pdb.set_trace()
        print input
        ICE_CONST=input
        if os.path.isfile(ICE_CONST)==True:
            params = json.load(open(ICE_CONST))
            configvalues['CHROME_VERSION'] = params['CHROME_VERSION']
            configvalues['FIREFOX_VERSION'] = params['FIREFOX_VERSION']
            if configvalues['CHROME_VERSION'] != "":
                for k,v in configvalues['CHROME_VERSION'].items():
                    CHROME_DRIVER_VERSION[str(k)]=[int(str(v)[:2]),int(str(v)[3:])]
            if configvalues['FIREFOX_VERSION'] != "":
                for k,v in configvalues['FIREFOX_VERSION'].items():
                    FIREFOX_BROWSER_VERSION[str(k)]=[int(str(v)[:2]),int(str(v)[3:])]
            try:
                print('Checking for browser versions...')
                import subprocess
                from selenium import webdriver
                from selenium.webdriver import ChromeOptions
                a=[]
                p = subprocess.Popen('chromedriver.exe --version', stdout=subprocess.PIPE, bufsize=1,cwd="D:\PortablePython\PortablePython\Drivers",shell=True)
                for line in iter(p.stdout.readline, b''):
                    a.append(str(line))
                a=a[0][13:17]
                choptions1 = webdriver.ChromeOptions()
    ##            if str(configvalues['chrome_path']).lower()!="default":
    ##                choptions1.binary_location=str(configvalues['chrome_path'])
                choptions1.add_argument('--headless')
                driver = webdriver.Chrome(chrome_options=choptions1, executable_path="D:\PortablePython\PortablePython\Drivers\chromedriver.exe")
                browser_ver = driver.capabilities['version']
                browser_ver1 = browser_ver.encode('utf-8')
                browser_ver = int(browser_ver1[:2])
                try:
                    driver.close()
                    driver.quit()
                except:
                    pass
                driver=None
                for k,v in CHROME_DRIVER_VERSION.items():
                    if a == k:
                        if browser_ver >= v[0] and browser_ver <= v[1]:
                            chromeFlag=True
                if chromeFlag == False :
                    print('WARNING!! : Chrome version',browser_ver,' is not supported.')
            except Exception as e:
    ##            self.assertTrue(False)
                status="false"
                print("Error in checking chrome version")
    ##            log.error("Error in checking chrome version")
    ##            log.error(e)
            try:
                p = subprocess.Popen('geckodriver.exe --version', stdout=subprocess.PIPE, bufsize=1,cwd="D:\PortablePython\PortablePython\Drivers",shell=True)
                a=[]
                for line in iter(p.stdout.readline, b''):
                    a.append(str(line))
                a=a[0][12:16]
                caps=webdriver.DesiredCapabilities.FIREFOX
                caps['marionette'] = True
                from selenium.webdriver.firefox.options import Options
                options = Options()
                options.add_argument('--headless')
                driver = webdriver.Firefox(capabilities=caps,firefox_options=options, executable_path="D:\PortablePython\PortablePython\Drivers\geckodriver.exe")
                browser_ver=driver.capabilities['browserVersion']
                browser_ver1 = browser_ver.encode('utf-8')
                browser_ver = float(browser_ver1[:4])
                try:
                    driver.close()
                    driver.quit()
                except:
                    pass
                driver=None
                for k,v in FIREFOX_BROWSER_VERSION.items():
                    if a == k:
                        if browser_ver >= v[0] or browser_ver <= v[1]:
                            firefoxFlag=True
                if firefoxFlag == False:
                    status="false"
                    print('WARNING!! : Firefox version',browser_ver,' is not supported.')
            except Exception as e:
    ##            self.assertTrue(False)
                    print("Error in checking Firefox version")
    ##                log.error("Error in checking Firefox version")
    ##                log.error(e)
            if chromeFlag == True and firefoxFlag == True:
    ##            self.assertTrue(True)
                print('Current version of browsers are supported')
                status="true"
    ##        self.assertTrue(True)
        else:
            print("Please enter valid ice_const.json path")
            status="false"
    except Exception as e:
##        self.assertTrue(False)
        print("Error while checking browser compatibility")
##        log.debug("Error while checking browser compatibility")
##        log.debug(e)
        status="false"
##    self.assertTrue(status)
    return status

var_name=[]
with open("D:\MasterNew\Nineteen68\Nineteen68\unit_tests\check_version_browser.txt") as f:
    for line in f:
        if(line.strip()!=''):
            if(line.find('#')==-1):
                eq_index = line.find(' ')
                var_name.append((line[:eq_index].strip(),line[eq_index:].strip()))
                print var_name


import pytest
@pytest.mark.parametrize("input,expected",var_name)
def test_myfunc(input,expected):
    assert check_browser(input) == expected








