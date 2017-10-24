#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      anas.ahmed
#
# Created:     24-10-2017
# Copyright:   (c) anas.ahmed 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def verifyTooltipText(sap_id,input_val,*args):
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
        #------------------------------Condition to check if its a table element
        if(elem.type=='GuiTableControl'):
            #arg=args[0]
            if ";" in input_val:
                arg=input_val.split(';')
                print arg
            if(len(arg)==1 and arg[0]==''):
                pass
            elif len(arg)==3 :
                row=int(arg[0])-1
                col=int(arg[1])-1
                input_val=arg[2]
                elem = elem.GetCell(row, col)
            else:
                elem=None
                print "Invalid Arguments Passed"
        #--------------------changing Null to ''
        if input_val.strip()=="Null":
            input_val=''
        #------------------------------Condition to check if its a table element
        if(id != None):
            if input_val.strip()==elem.tooltip.strip() or input_val.strip()==elem.DefaultTooltip.strip() :
                result='True'
            else:
                print input_val
                print elem.tooltip
                print elem.DefaultTooltip
                print 'ToolTipText does not match input text.'
        else:
            print 'Element does not exist'
    except Exception as e:
        print 'Error occoured in verifyTooltipText and is :',e
    return result

var_name=[]
with open("verifytooltiptext_input.txt") as f:
    for line in f:
        if(line.strip()!=''):
            eq_index = line.find(',')
            eq_index1 = line.find('#')
            var_name.append((line[:eq_index].strip(),line[eq_index+1:eq_index1].strip(),line[eq_index1+1:].strip()))
    print var_name

import pytest
@pytest.mark.parametrize("input1,input2,expected", var_name)
def test_myfunc(input1,input2,expected):
    assert verifyTooltipText(input1,input2) == expected