# content of test_class.py
from selenium import webdriver
import os
from selenium.webdriver.support.ui import Select
import ast
def selectByAbsoluteValue(input):
    err_msg=None
    drivers_path = "D:/Nineteen68_Git_Core/Nineteen68/Drivers"
    CHROME_DRIVER_PATH = drivers_path + "/chromedriver.exe"
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    input = ast.literal_eval(input)
    if len(input)==5:
        driver.get('https://www.ahridirectory.org/ahridirectory/pages/rfr/defaultSearch.aspx')
        webelement = driver.find_element_by_id('cp1_search1_dl1_modelStatus')
        if webelement is not None:
            print "here"
            if (input is not None):
                    dropVal=input[2]
                    row_num=int(input[0])-1
                    col_num=int(input[1])-1
                    inp_val = input[4]
                    try:
                        if dropVal.lower()=='dropdown':
                            cell = webelement
                            if(cell!=None):
                                if cell.is_enabled():
                                    if len(inp_val.strip()) != 0:
                                        print Select(cell)
                                        select = Select(cell)
                                        iList = select.options
                                    else:
                                        status='false'
                                else:
                                        status='false'
                            else:
                                status='false'
                    except Exception as e:
                        err_msg=e
                        status='false'
    elif (len(input) == 1):
        driver.get('https://nucleus.slkgroup.com:4450/OA_HTML/RF.jsp?function_id=28716&resp_id=-1&resp_appl_id=-1&security_group_id=0&lang_code=US&oas=AKSR9O-Nnp2e3mzhwTyruw..&params=KQ0ueFd3h5ncJDQ0.532EQ')
        webelement = driver.find_element_by_id('Accessibility')
        if input[0] != '':
            try:
                cell = webelement
                inp_val = input[0]
                if len(inp_val.strip()) != 0:
                    select = Select(cell)
                    iList = select.options
                else:
                    status='false'
            except Exception as e:
                status='false'
                err_msg=e
        else:
            status='false'
    else:
        status='false'
    try:
        if inp_val !='':
            temp=[]
            for i in range (0,len(iList)):
                internal_val = iList[i].text
                temp.append(internal_val)
            if (inp_val in temp):
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
with open("select_by_abs.txt") as f:
    for line in f:
        if(line.strip()!=''):
            if(line.find('#')==-1):
                eq_index = line.find(';')
                var_name.append((line[:eq_index].strip(),line[eq_index+1:].strip()))

import pytest
@pytest.mark.parametrize("input,expected", var_name)
def test_myfunc(input,expected):
    assert selectByAbsoluteValue(input) == expected
