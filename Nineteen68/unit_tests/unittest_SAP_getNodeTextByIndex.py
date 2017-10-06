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

def getNodeTextByIndex(sap_id,input_val,*args):
    result = 'False'
    import win32com.client
    SapGui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    ses = SapGui.FindById("ses[0]")
    node = ''
    flag = True
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
    try:
        if(id != None):
            if(elem.type == 'GuiShell' and elem.SubType == 'Tree'):
                for i in range(0,len(input_val)):
                    count = int(input_val[i])
                    if(i==0):
                        node = elem.TopNode
                        c = getFirstLevelNodeCount(elem)
                        if(count>c):
                            flag = False
                            break
                        try:
                            while (count-1):
                                node = elem.GetNextNodeKey(node)
                                count = count - 1
                        except:
                            pass
                    else:
                        child_nodes = elem.GetSubNodesCol(node)
                        if(count>len(child_nodes)):
                            flag = False
                            break
                        j = 0
                        try:
                            node = child_nodes[j]
                            while (count-1):
                                node = elem.GetNextNodeKey(child_nodes[j])
                                count = count - 1
                                j = j + 1
                        except Exception as e:
                            pass
                result = elem.GetNodeTextByKey(node)
                if(flag):
                    result = elem.GetNodeTextByKey(node)
                else:
                    print "Invalid input"
            else:
                print "Element is not a tree object"
        else:
            print "Element not present on the page where operation is trying to be performed"
    except Exception as e:
        print "Error occured in SelectTreeNode :",e
    return result

def getFirstLevelNodeCount(tree):
    c = 1
    n = tree.TopNode
    while True:
        try:
            n = tree.GetNextNodeKey(n)
            c = c + 1
        except:
            break
    return c

var_name=[]
with open("unittest_getNodeTextByIndex_input.txt") as f:
    for line in f:
        if(line.strip()!=''):
            eq_index = line.find(',')
            eq_index1 = line.find('#')
            var_name.append((line[:eq_index].strip(),line[eq_index+1:eq_index1].strip(),line[eq_index1+1:].strip()))

import pytest
@pytest.mark.parametrize("input1,input2,expected", var_name)
def test_myfunc(input1,input2, expected):
    assert getNodeTextByIndex(input1,input2) == expected
