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
def get_status(sap_id, *args):
    result = 'False'
    import win32com.client
    SapGui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    ses = SapGui.FindById("ses[0]")
    wnd = ses.ActiveWindow
    wndId =  wnd.__getattr__('id')
    title = ses.ActiveWindow.Text
    if("/" in title):
        i = sap_id.index("/",len(title))
    else:
        i = sap_id.index("/")
    id = wndId + sap_id[i:]
    elem = ses.FindById(id)
    print elem.type
    try:
        if(id != None):
##                if(ses.FindById(id).Changeable == True):
                #----------------------------------------------------------Check for radio
                if(elem.type == "GuiRadioButton"):
                    value = ses.FindById(id).selected
                    if(value==True):
                        value=sap_constants.SELECTED_CHECK
                    else:
                        value=sap_constants.UNSELECTED_CHECK
                    result='True'
                #----------------------------------------------------------Check for Checkbox
                elif(elem.type == "GuiCheckBox"):
                    value = ses.FindById(id).selected
                    if(value ==True):
                        value=sap_constants.CHECKED_CHECK
                    else:
                        value=sap_constants.UNCHECKED_CHECK
                    result='True'
                #----------------------------------------------------------Check for Button
                elif(elem.type == "GuiButton"):
                    try:
                        value = ses.FindById(id).selected
                        result='True'
                    except:
                        print 'Button element does not have status'
        else:
            print 'element not present on the page where operation is trying to be performed'
    except Exception as e:
        print e
    return result

var_name=[]
with open("unittest_SAP_GetStatus_radio_checkbox_button_input.txt") as f:
    for line in f:
        if(line.strip()!=''):
            eq_index = line.find(',')
            var_name.append((line[:eq_index].strip(),line[eq_index+1:].strip()))
        print var_name

import pytest
@pytest.mark.parametrize("input1,expected", var_name)
def test_myfunc(input1,expected):
    print input1
    print expected
    assert get_status(input1) == expected