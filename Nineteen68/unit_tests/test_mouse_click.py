from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pyautogui

def mouse_click(input,ids):
        print input[1],input[3]
        err_msg=None
        try:
            if not(input is None):
                row_num=int(input[1])-1
                col_num=int(input[3])-1
                drivers_path = "D:\Nineteen68_Git_Core\Nineteen68\Drivers"
                CHROME_DRIVER_PATH = drivers_path + "\\chromedriver.exe"
                driver = webdriver.Chrome(CHROME_DRIVER_PATH)
                driver.get("https://www.ahridirectory.org/ahridirectory/pages/rfr/defaultSearch.aspx")
                cell=driver.find_element_by_id(ids)
                if(cell!=None):
                    webelement=cell
                    print webelement
                    if cell.is_enabled():
                        ele_coordinates=cell.location
                        pyautogui.mouseDown(ele_coordinates.get('x')+9,ele_coordinates.get('y')+6)
                        status='true'
        except Exception as e:
            status="false"
            err_msg=e
        return status



var_name=[]
with open("mouse-click.txt") as f:
    for line in f:
        if(line.strip()!=''):
            if(line.find('#')==-1):
                eq_index = line.find(';')
                eq_index1 = line.find(' ')
                var_name.append((line[:eq_index].strip(),line[eq_index+1:eq_index1].strip(),line[eq_index1:].strip()))
                print var_name


import pytest
@pytest.mark.parametrize("input,ids,expected", var_name)
def test_myfunc(input,ids,expected):
    assert mouse_click(input,ids) == expected








