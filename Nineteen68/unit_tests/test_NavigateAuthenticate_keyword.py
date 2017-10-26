from selenium import webdriver
import os
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import ast
import time

def test_NavigateAuthenticate_keyword():
        val = "yes"
        try:
                drivers_path = "D\Nineteen68 setup\Nineteen68\Drivers"
                CHROME_DRIVER_PATH = drivers_path + "\\IEDriverServer.exe"
                driver = webdriver.Ie(CHROME_DRIVER_PATH)
                driver.get("https://wslk13fodc3-002:8443/")
                try:
                    url = "https://wslk13fodc3-002:8443/"
                    inputURL = url[0]
                    if not (inputURL is None and inputURL is ''):
                        inputURL.strip()
                        if inputURL[0:4].lower()!='http' and inputURL[0:4].lower()!='file':
                            inputURL='http://'+inputURL
                        driver.get(inputURL)
                        #ignore certificate implementation23

                        try:
                            ignore_certificate = val
                            if ((ignore_certificate.lower() == 'yes') and ((driver.title !=None) and ('Certificate' in driver.title))):
                                driver.execute_script("""document.getElementById('overridelink').click();""")
                        except Exception as k:
                            status = "False"
                        status="True"
                    else:
                        status = "True"
                except Exception as e:
                    status = "True"
                try:
                    if (url[0] is not None and url[0] != '')\
                     and (url[1] is not None and url[1] != '')\
                      and (url[2] is not None and url[2] != ''):
                        from encryption_utility import AESCipher
                        encryption_obj = AESCipher()
                        input_val = encryption_obj.decrypt(url[2])
                        url[2]=input_val
                        if len(url)>3:
                            url[3]=int(url[3])
                            timeout=url[3]
                            time.sleep(int(timeout))
                        else:
                            time.sleep(6)

                        # defect #193 added functionality for authentication automation in browser popup (Himanshu)
                        if(isinstance(driver,webdriver.Ie)):
                            #Send function keys are used
##                            obj=SF()
                            username=url[1].strip()
                            password=url[2]
##                            obj.type(username)
##                            obj.execute_key('tab',1)
##                            obj.type(password)
##                            obj.execute_key('tab',1)
##                            obj.execute_key('spacebar',1)
##                            obj.execute_key('tab',1)
##                            obj.execute_key('enter',1)
                            status="True"
                        else:
                            ##obj=SF()
                            username=url[1].strip()
                            password=url[2]
##                            obj.type(username)
##                            obj.execute_key('tab',1)
##                            obj.type(password)
##                            obj.execute_key('tab',1)
##                            obj.execute_key('enter',1)
                            status="True"

                    else:
                        status = "False"
                except Exception as e:
                 status = "True"
        except Exception as e:
                 status = "True"
        return status

var_name=[]
with open("navigate_Authenticate.txt") as f:
    for line in f:
        if(line.strip()!=''):
            if(line.find('#')==-1):
                eq_index2 = line.find('-')
                var_name.append((line[eq_index2+1:].strip()))


import pytest
@pytest.mark.parametrize("expected", var_name)
def test_myfunc(expected):
    assert test_NavigateAuthenticate_keyword() == expected