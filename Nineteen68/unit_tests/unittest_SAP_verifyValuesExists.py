#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sakshi.goyal
#
# Created:     06-10-2017
# Copyright:   (c) sakshi.goyal 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def verifyValuesExists(sap_id,input_val,*args):
    result = 'False'
    import win32com.client
    SapGui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    ses = SapGui.FindById("ses[0]")
    input_val = input_val.split(';')
    wnd = ses.ActiveWindow
    wndId =  wnd.__getattr__('id')
    title = ses.ActiveWindow.Text
    if("/" in title):
        i = sap_id.index("/",len(title))
    else:
        i = sap_id.index("/")
    id = wndId + sap_id[i:]
    elem = ses.FindById(id)
    dd_entries = []
    i = 0
    flag=True
    try:
        if(id != None):
            entries = ses.FindById(id).Entries
            while True:
                try:
                    dd_entries.append(str(entries(i).value).lower())
                    i = i + 1
                except Exception as e:
                    break
            for inp in input_val:
                if(inp.lower().strip() not in dd_entries):
                    flag = False
                    break
            if flag==True:
                result = 'True'
    except Exception as e:
          print "Error occured",e
    return result


var_name=[]
with open("unittest_SAP_verifyValuesExists_input.txt") as f:
    for line in f:
        if(line.strip()!=''):
            eq_index = line.find(',')
            eq_index1 = line.find('#')
            var_name.append((line[:eq_index].strip(),line[eq_index+1:eq_index1].strip(),line[eq_index1+1:].strip()))

import pytest
@pytest.mark.parametrize("input1,input2,expected", var_name)
def test_myfunc(input1,input2, expected):
    assert verifyValuesExists(input1,input2) == expected
