#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sakshi.goyal
#
# Created:     15-09-2017
# Copyright:   (c) sakshi.goyal 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pywinauto

def click(args):
    result = False
    id = "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLMGMMTC_VIEW"
    import win32com.client
    SapGui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    ses = SapGui.FindById("ses[0]")
    elem=ses.FindById(id)
    print args[0]
    try:
        #------------------------------Condition to check if its a table element
            if(elem.type=='GuiTableControl'):
                arg=args
                if(len(arg)==1 and arg[0]==''):
                    pass
                elif (len(arg)==2):
                    if(isinstance(arg[0],int) and isinstance(arg[1],int)):
                        row=int(arg[0])-1
                        col=int(arg[1])-1
                        elem = elem.GetCell(row, col)
                    else:
                        pass
                elif(len(arg)>2):
                    row=int(arg[2])-1
                    col=int(arg[3])-1
                    elem = elem.GetCell(row, col)
                else:
                    elem=None
        #--------------------------------mouse will move over to the middle of the element and click
            left =  elem.__getattr__("ScreenLeft")
            width = elem.__getattr__("Width")
            x = left + width/2
            top =  elem.__getattr__("ScreenTop")
            height = elem.__getattr__("Height")
            y= top + height/2
            if(elem.type=='GuiTab'):
                x=left + width*0.75
                y=top+height*0.25
            pywinauto.mouse.click(button='left', coords=(int(x), int(y)))
            result=True
    except Exception as e:
        import traceback
        traceback.print_exc()
    return result

class TestClass(object):
    #Test for table click without arguments
    def test1(self):
        args = ['']
        assert click(args) == True

    #Test for table click with arguments
    def test2(self):
        args = ['3','1']
        assert click(args) == True

    #Test for custom table click without arguments
    def test3(self):
        args = ['table','1']
        assert click(args) == True

    #Test for custom table click with arguments
    def test4(self):
        args = ['table','1','2','1']
        assert click(args) == True

    #Test for table click with wrong arguments
    def test5(self):
        args = ['2']
        assert click(args) == False


