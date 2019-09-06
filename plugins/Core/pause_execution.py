#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     25-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx
import threading
app2 = wx.App()

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
        self.okbutton = wx.Button(self.panel, label="Continue")
##        self.okbutton.Bind(wx.EVT_BUTTON, self.OnOk)   # need to implement OnExit(). Leave notrace
        self.sizer.Add(self.okbutton, pos=(2, 1), flag=wx.TOP | wx.ALIGN_CENTER, border=5)
        self.sizer.AddGrowableCol(1)
        self.panel.SetSizer(self.sizer)
        self.CenterOnScreen()
        self.Centre()
##        self.ToggleWindowStyle(wx.STAY_ON_TOP)
##        self.Show()



    def OnOk(self):
        self.Close()
        app2.Exit()


def execute(flag):
    obj=AppFrame(None, title="SLK Nineteen68 - Pause")
    if flag=='pause':
        app2.MainLoop()
    elif flag=='continue':
        obj.OnOk()


    return True