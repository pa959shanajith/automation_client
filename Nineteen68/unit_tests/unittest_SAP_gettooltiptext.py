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

def getTooltipText(sap_id,*args):
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
            arg=args[0]
##            if ";" in input_val:
##                arg=input_val.split(';')
            if(len(arg)==1 and arg[0]==''):
                pass
            elif len(arg)==2 :
                row=int(arg[0])-1
                col=int(arg[1])-1
                elem = elem.GetCell(row, col)
            else:
                elem=None
                print 'Invalid Arguments Passed'
        #------------------------------Condition to check if its a table element
        if(id != None):
                value = elem.tooltip
                if value== '':
                    value = elem.DefaultTooltip
                    if value =='':
                        value ="Null"
                if(value != None or value =="Null"):
                    result='True'
                    print "value is :",value
                else:
                    print 'ToolTipText not avaliable for the element '
        else:
            print 'Element does not exist'

    except Exception as e:
        print 'Error occoured in getTooltipText and is :',e
    return result

var_name=[]
with open("gettooltiptext_input.txt") as f:
    for line in f:
        if(line.strip()!=''):
            eq_index = line.find(';')
            var_name.append((line[:eq_index].strip(),line[eq_index+1:].strip()))
    print var_name

import pytest
@pytest.mark.parametrize("input,expected", var_name)
def test_myfunc(input,expected):
    assert getTooltipText(input) == expected