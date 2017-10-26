#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      anas.ahmed
#
# Created:     26-10-2017
# Copyright:   (c) anas.ahmed 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def get_status(webelement,input,*args):
    print webelement
    print input
    result = 'False'
    visibilityFlag=True
    status=None
    if webelement is not None:
        try:
            if webelement.tag_name=='table':
                if len(input)==4:
                    webelement=getActualElement(webelement,input)
                elif len(input)==3:
                    temp_status=__fetch_status_array(webelement,input)
                    status=temp_status[0]
            if status==None and webelement!=None:
                output=__fetch_status(webelement)
                result='True'
        except Exception as e:
            #err_msg=self.__web_driver_exception(e)
            print e
    return result

def __fetch_status(webelement,*args):
    try:
        input_type=webelement.get_attribute('type').lower();
        if webelement.is_selected():
            if input_type in ['submit','button','reset']:
                status=webelement.is_selected()
            else:
                status='Selected'
        else:
            if input_type in ['submit','button','reset']:
                status=webelement.is_selected()
            else:
                status='UnSelected'
    except Exception as e:
        #err_msg=self.__web_driver_exception(e)
        print e
    return status

def __fetch_status_array(webelement,input):
    status_list=[]
    try:
        driver=browser_Keywords.driver_obj
        row_num=input[0]
        col_num=input[1]
        row_num=int(row_num)
        col_num=int(col_num)
        tag_name=input[2]
        cell=driver.execute_script(webconstants.GET_CELL_JS,webelement,row_num-1,col_num-1)
        element_list=cell.find_elements_by_xpath('.//*')
        if tag_name=='radio' or tag_name=='checkbox' or tag_name in ['submit','button','reset'] :
            log.debug('Tagname is',tag_name)
            for element in element_list:
                element_xpath=driver.execute_script(webconstants.GET_XPATH_JS,element)
                child=driver.find_element_by_xpath(element_xpath)
                if child!=None:
                    tag_name=child.tag_name
                    tag_type=child.get_attribute('type')
                    if tag_name=='input' and tag_type=='radio':
                        status_list.append(__fetch_status(child))
                    elif tag_name=='input' and tag_type=='checkbox':
                        status_list.append(__fetch_status(child))
                    elif tag_name=='input' and tag_type in ['submit','button','reset']:
                        status_list.append(__fetch_status(child))


    except Exception as e:
        err_msg=self.__web_driver_exception(e)
    log.debug(status_list)
    return status_list

var_name=[]
with open("unittest_WEB_GetStatus_input.txt") as f:
    for line in f:
        if(line.strip()!=''):
            eq_index = line.find('~')
            eq_index1 = line.find('#')
            var_name.append((line[:eq_index].strip(),line[eq_index+1:eq_index1].strip(),line[eq_index1+1:].strip()))
            print var_name

import pytest
@pytest.mark.parametrize("input1,input2,expected", var_name)
def test_myfunc(input1,input2,expected):
    print input1
    print input2
    print expected
    assert get_status(input1,input2) == expected