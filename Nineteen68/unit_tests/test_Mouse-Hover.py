from selenium import webdriver
import os
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import ast

def mouse_hover(ids,vals,path):
        vals = ast.literal_eval(vals)
        err_msg=None
        try:
            len_input=len(vals)
            if(len_input == 2):
                row = int(vals[0])-1
                col = int(vals[1])-1
                drivers_path = "D:\Nineteen68_Git_Core\Nineteen68\Drivers"
                CHROME_DRIVER_PATH = drivers_path + "\\chromedriver.exe"
                driver = webdriver.Chrome(CHROME_DRIVER_PATH)
                driver.get("https://www.ahridirectory.org/ahridirectory/pages/rfr/defaultSearch.aspx")
                cell=driver.find_element_by_id(ids)
                if(cell!=None):
                    webelement=cell
            elif(len_input > 2):
                row = int(vals[0])-1
                col = int(vals[1])-1
                tag=vals[2].lower()
                index=int(vals[3])
                eleStatus = False
                counter = 1
                drivers_path = "D:\Nineteen68_Git_Core\Nineteen68\Drivers"
                CHROME_DRIVER_PATH = drivers_path + "\\chromedriver.exe"
                driver = webdriver.Chrome(CHROME_DRIVER_PATH)
                driver.get("https://www.ahridirectory.org/ahridirectory/pages/rfr/defaultSearch.aspx")
                cell=driver.find_element_by_id(ids)
                xpath=path
                cellChild = driver.find_element_by_xpath(xpath)
                tagName = cellChild.tag_name
                tagType = cellChild.get_attribute('type')
                xpath_elements=xpath.split('/')
                lastElement=xpath_elements[len(xpath_elements)-1]
                childindex=lastElement[lastElement.find("[")+1:lastElement.find("]")]
                childindex = int(childindex)
                if tag=='button':
                   if( (tagName==('input') and tagType==('button')) or tagType==('submit') or tagType==('reset') or tagType==('file')):
                      if index==childindex:
                        eleStatus =True
                      else:
                        if counter==index:
                           index =childindex
                           eleStatus =True
                        else:
                            counter+=1
                elif tag=='image':
                    if(tagName==('input') and (tagType==('img') or tagType==('image'))):
                        if index==childindex:
                            eleStatus =True
                        else:
                            if counter==index:
                                index =childindex
                                eleStatus =True
                            else:
                                counter+=1
                    elif tagName =='img':
                        if index==childindex:
                            eleStatus =True
                        else:
                            if counter==index:
                               index =childindex
                               eleStatus =True
                            else:
                                counter+=1
                elif tag=='img':
                     if index==childindex:
                            eleStatus =True
                     else:
                            if counter==index:
                               index =childindex
                               eleStatus =True
                            else:
                                counter+=1
                elif tag=='checkbox':
                     if(tagName==('input') and (tagType==('checkbox')) ):
                         if index==childindex:
                            eleStatus =True
                         else:
                            if counter==index:
                               index =childindex
                               eleStatus =True
                            else:
                                counter+=1
                elif tag=='radiobutton':
                     if (tagName==('input') and tagType==('radio')):
                        if index==childindex:
                            eleStatus =True
                        else:
                            if counter==index:
                               index =childindex
                               eleStatus =True
                            else:
                                counter+=1
                elif tag=='textbox':
                     if (tagName==('input') and (tagType==('text') or tagType==('email') or tagType==('password') or tagType==('range') or tagType==('search') or tagType==('url')) ):
                        if index==childindex:
                            eleStatus =True
                        else:
                            if counter==index:
                               index =childindex
                               eleStatus =True
                            else:
                                counter+=1
                elif tag=='link':
                    if(tagName==('a')):
                        if index==childindex:
                            eleStatus =True
                        else:
                            if counter==index:
                               index =childindex
                               eleStatus =True
                            else:
                                counter+=1
                else:
                        eleStatus=True

                if eleStatus==True:
                    webelement = cellChild
            else:
                drivers_path = "D:\Nineteen68_Git_Core\Nineteen68\Drivers"
                CHROME_DRIVER_PATH = drivers_path + "\\chromedriver.exe"
                driver = webdriver.Chrome(CHROME_DRIVER_PATH)
                driver.get("https://www.ahridirectory.org/ahridirectory/pages/rfr/defaultSearch.aspx")
                cell=driver.find_element_by_id(ids)
                webelement=cell
            if webelement is not None:
                location=cell.location
                pyautogui.moveTo(int(location.get('x')),int(location.get('y')))
            status='true'
        except Exception as e:
           status="false"
           err_msg="failed"
        return status

var_name=[]
with open("Mouse-Hover.txt") as f:
    for line in f:
        if(line.strip()!=''):
            if(line.find('#')==-1):
                eq_index = line.find(';')
                eq_index1 = line.find(' ')
                eq_index2 = line.find('-')
                var_name.append((line[:eq_index].strip(),line[eq_index+1:eq_index1].strip(),line[eq_index1:eq_index2].strip(),line[eq_index2+1:].strip()))


import pytest
@pytest.mark.parametrize("ids,vals,path,expected", var_name)
def test_myfunc(vals,ids,path,expected):
    assert mouse_hover(ids,vals,path) == expected