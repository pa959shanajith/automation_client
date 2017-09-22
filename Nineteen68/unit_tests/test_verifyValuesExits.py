from selenium import webdriver
import os
from selenium.webdriver.support.ui import Select
import ast

def verifyValuesExists(input):
        visibilityFlag=True
        flag = True
        err_msg=None
        drivers_path = "D:\Nineteen68_Git_Core\Nineteen68\Drivers"
        CHROME_DRIVER_PATH = drivers_path + "\\chromedriver.exe"
        driver = webdriver.Chrome(CHROME_DRIVER_PATH)
        try:
            input = ast.literal_eval(input)
            print input
            driver.get('https://nucleus.slkgroup.com:4450/OA_HTML/RF.jsp?function_id=28716&resp_id=-1&resp_appl_id=-1&security_group_id=0&lang_code=US&oas=AKSR9O-Nnp2e3mzhwTyruw..&params=KQ0ueFd3h5ncJDQ0.532EQ')
            webelement = driver.find_element_by_id('Accessibility')
            if input[0] != '':
                cell = webelement
                inp_val = input[0]
            if input is not None:
                if len(inp_val.strip()) != 0:
                    select = Select(cell)
                    iList = select.options

                else:
                    status='false'
                opt_len = len(iList)
                temp = []
                inp_val_len = len(input)
                for x in range(0,len(iList)):
                    internal_val = iList[x].text.strip()
                    temp.append(internal_val)
                count = 0
                for y in range(0,inp_val_len):
                    input_temp = input[y].strip()
                    if (input_temp in temp):
                        count+=1
                        flag = True
                    else:
                        flag = False
                if(not(flag == False)):
                    status='true'
                else:
                    status='false'
            else:
                status='false'
        except Exception as e:
            err_msg=e
            status='false'
        return status

var_name=[]
with open("verify_values_exits.txt") as f:
    for line in f:
        if(line.strip()!=''):
            if(line.find('#')==-1):
                eq_index = line.find(';')
                var_name.append((line[:eq_index].strip(),line[eq_index+1:].strip()))

import pytest
@pytest.mark.parametrize("input,expected", var_name)
def test_func(input,expected):
    assert verifyValuesExists(input) == expected
