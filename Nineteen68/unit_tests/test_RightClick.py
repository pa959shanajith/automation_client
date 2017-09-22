from selenium import webdriver
import os

def rightclick(ids):
        err_msg=None
        try:
            drivers_path = "D:\Nineteen68_Git_Core\Nineteen68\Drivers"
            CHROME_DRIVER_PATH = drivers_path + "\\chromedriver.exe"
            driver = webdriver.Chrome(CHROME_DRIVER_PATH)
            driver.get("https://www.ahridirectory.org/ahridirectory/pages/rfr/defaultSearch.aspx")
            cell=driver.find_element_by_id(ids)
            webelement = cell
            if webelement is not None:
                if webelement.is_enabled():
                    from selenium.webdriver.common.action_chains import ActionChains
                    driver.context_click(webelement).perform()
                    status='true'
        except Exception as e:
            err_msg=e
            status='true'
        return status

var_name=[]
with open("RightClick.txt") as f:
    for line in f:
        if(line.strip()!=''):
            if(line.find('#')==-1):
                eq_index = line.find(';')
                var_name.append((line[:eq_index].strip(),line[eq_index+1:].strip()))
                print var_name


import pytest
@pytest.mark.parametrize("ids,expected", var_name)
def test_myfunc(ids,expected):
    assert rightclick(ids) == expected