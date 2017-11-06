#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      anas.ahmed
#
# Created:     24-10-2017
# Copyright:   (c) anas.ahmed 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def verifyVisible(sap_id, *args):
    print sap_id
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
    try:
        if(id != None):
            try:
                ses.FindById(id)
                print "Element is visible"
                result='True'
            except Exception as e:
                if e[2][2]=='The control could not be found by id.':
                    print "Element is hidden"
    except Exception as e:
        print "Element is hidden/Does not exist on the page"
    return result

var_name=[]
with open("verify_visible_hidden_input.txt") as f:
    for line in f:
        if(line.strip()!=''):
            eq_index = line.find(',')
            var_name.append((line[:eq_index].strip(),line[eq_index+1:].strip()))
    print var_name

import pytest
@pytest.mark.parametrize("input,expected", var_name)
def test_myfunc(input,expected):
    assert verifyVisible(input) == expected