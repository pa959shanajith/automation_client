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
import time
import os
import controller
import readconfig
import logger
import logging
log = logging.getLogger('delay_operations.py')
dispflag = ''
dispinput = None
cont = None

class Pause(wx.Frame):
    def __init__(self, parent,id, title):
        wx.Frame.__init__(self, parent, title=title,
                          size=(300, 130),style=wx.STAY_ON_TOP| wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX))
        self.SetBackgroundColour('#e6e7e8')
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(1, 2)
        self.iconpath = os.environ["IMAGES_PATH"] + "/slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)

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


    def OnOk(self, *event):
        self.resume_execution()
        self.Destroy()

    def resume_execution(self):
        global cont
        cont.paused  = False
        # Notify so thread will wake after lock released
        try:
            cont.pause_cond.notify()
            # Now release the lock
            cont.pause_cond.release()
        except Exception as e:
            log.error('Debug is not paused to Resume')
            log.error(e)

    def pause_execution(self):
        global cont
        cont.paused=True
        cont.pause_cond.acquire()
        with cont.pause_cond:
            while cont.paused:
                cont.pause_cond.wait()


class Display(wx.Frame):
    def __init__(self, parent, id,title,input):
        str=input
        wx.Frame.__init__(self, parent, title="Nineteen68 - DisplayValue",   size=(400, 300),style=wx.STAY_ON_TOP|wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX))
        self.SetBackgroundColour('#e6e7e8')
        self.panel = wx.Panel(self)
        self.iconpath = os.environ["IMAGES_PATH"] + "/slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        self.t = wx.TextCtrl(self.panel, wx.ID_ANY,  size=(380, 200),  style = wx.TE_MULTILINE|wx.TE_READONLY)
        self.t.Clear()
        self.t.AppendText(str)

        self.okbutton = wx.Button(self.panel, label="OK", pos=(150, 230))
        self.okbutton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.okbutton.SetFocus()
        self.Centre()
        self.Show()
        configobj = readconfig.readConfig()
        configvalues = configobj.readJson()
        interval = configvalues['displayVariableTimeOut']
        if interval == '':
            interval = 3
        else:
            try:
                interval = int(interval)
            except:
                interval = 3
        t = threading.Timer(interval,self.OnOk)
        t.start()

    def OnOk(self, *event):
        if(self):
            self.resume_execution()
            self.Destroy()

    def resume_execution(self):
        global cont
        cont.paused = False
        # Notify so thread will wake after lock released
        try:
            cont.pause_cond.notify()
            # Now release the lock
            cont.pause_cond.release()
        except Exception as e:
            log.error('Debug is not paused to Resume')
            log.error(e)


class PauseAndDisplay:
    def __init__(self):
        pass

    def display_value(self,input,wx_object,mythread):
        global dispinput, dispflag, cont
        dispinput = input
        dispflag = 'display'
        cont = mythread
        wx.PostEvent(wx_object.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wx_object.GetId()))
        self.pause_execution()

    def execute(self,wx_object,mythread):
        global dispflag, cont
        dispflag = 'pause'
        cont = mythread
        wx.PostEvent(wx_object.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wx_object.GetId()))
        self.pause_execution()

    def getflagandinput(self):
        global dispflag,dispinput
        return dispflag,dispinput

    def pause_execution(self):
        global cont
        cont.paused=True
        cont.pause_cond.acquire()
        with cont.pause_cond:
            while cont.paused:
                cont.pause_cond.wait()
