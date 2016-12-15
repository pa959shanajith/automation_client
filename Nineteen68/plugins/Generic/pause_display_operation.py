#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     29-08-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx
import threading
t=''


class AppFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title,
                          size=(300, 130),style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(1, 2)

        self.text1 = wx.StaticText(self.panel, label="Application Paused!! Click OK to continue")
        self.sizer.Add(self.text1, pos=(0, 1), flag=wx.TOP | wx.LEFT | wx.BOTTOM,border=10)
        self.line = wx.StaticLine(self.panel)
        self.sizer.Add(self.line, pos=(1, 0),flag= wx.Center, border=50)
        self.okbutton = wx.Button(self.panel, label="OK")
        self.okbutton.Bind(wx.EVT_BUTTON, self.OnOk)   # need to implement OnExit(). Leave notrace
        self.sizer.Add(self.okbutton, pos=(2, 1), flag=wx.TOP | wx.ALIGN_CENTER, border=5)
        self.sizer.AddGrowableCol(1)
        self.panel.SetSizer(self.sizer)
        self.CenterOnScreen()
        self.Centre()
        self.Show()



    def OnOk(self, event):
        print 'Before pause called'
        self.Close()
        print 'After pause called'


def execute():
    app = wx.App()
    AppFrame(None, title="SLK Nineteen68 - Pause")
    app.MainLoop()

    return True




class AppFrame2(wx.Frame):

    def __init__(self, parent, title):
        global t
        str=title
        title="SLK Nineteen68 - Display Value"
        wx.Frame.__init__(self, parent, title=title,style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)

        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(1, 2)
        self.text1 = wx.StaticText(self.panel, label=str)
        self.sizer.Add(self.text1, pos=(0, 1), flag=wx.TOP | wx.LEFT | wx.BOTTOM,border=10)
        self.line = wx.StaticLine(self.panel)
        self.text1.Wrap(330)
        self.sizer.Add(self.line, pos=(1, 0),flag= wx.Center, border=50)
        self.okbutton = wx.Button(self.panel, label="OK")
        self.okbutton.Bind(wx.EVT_BUTTON, self.OnOk)   # need to implement OnExit(). Leave notrace
        self.sizer.Add(self.okbutton, pos=(5, 1), flag=wx.TOP | wx.ALIGN_CENTER, border=5)
        self.sizer.AddGrowableCol(1)

        self.panel.SetSizer(self.sizer)


        self.Centre()
        self.Show()
        t = threading.Timer(3,self.hello)
        t.start()




    def OnOk(self, event):
        self.Close()



    def hello(self):
        if(self):
            self.Close()



def display_value(input):
    app = wx.App()
    AppFrame2(None, title=input)
    app.MainLoop()
    global t
    t.cancel()
    return True








