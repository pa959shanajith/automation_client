#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sakshi.goyal
#
# Created:     28-09-2017
# Copyright:   (c) sakshi.goyal 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def selectTreeNode(sap_id,input_val,*args):
    result = 'False'
    import win32com.client
    SapGui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    ses = SapGui.FindById("ses[0]")
    node = ''
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
    print input_val
    try:
        if(id != None):
            if(elem.type == 'GuiShell' and elem.SubType == 'Tree'):
                for i in range(0,len(input_val)):
                    if(i==0):
                        node = elem.TopNode
                        try:
                            while (elem.GetNodeTextByKey(node)).lower() != input_val[i].lower():
                                node = elem.GetNextNodeKey(node)
                        except:
                            pass
                    else:
                        child_nodes = elem.GetSubNodesCol(node)
                        j = 0
                        try:
                            node = child_nodes[j]
                            while (elem.GetNodeTextByKey(child_nodes[j])).lower() != input_val[i].lower():
                                node = elem.GetNextNodeKey(child_nodes[j])
                                j = j + 1
                        except:
                            pass
                if(elem.GetNodeTextByKey(node) == input_val[len(input_val)-1]):
                    elem.DoubleClickNode(node)
                    result = 'True'
                else:
                    print 'Invalid input'
            else:
                print "Element is not a tree object"
        else:
            print "Element not present on the page where operation is trying to be performed"
    except Exception as e:
        print "Error occured in SelectTreeNode :",e
    return result

var_name=[]
with open("unittest_selectTreeNode_input.txt") as f:
    for line in f:
        if(line.strip()!=''):
            eq_index = line.find(',')
            eq_index1 = line.find('#')
            var_name.append((line[:eq_index].strip(),line[eq_index+1:eq_index1].strip(),line[eq_index1+1:].strip()))

import pytest
@pytest.mark.parametrize("input1,input2,expected", var_name)
def test_myfunc(input1,input2, expected):
    assert selectTreeNode(input1,input2) == expected
