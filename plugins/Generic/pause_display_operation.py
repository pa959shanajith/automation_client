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
        self.iconpath = os.environ["IMAGES_PATH"] + "/avo.ico"
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
        wx.Frame.__init__(self, parent, title="Avo Assure Client - DisplayValue",   size=(400, 300),style=wx.STAY_ON_TOP|wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX))
        self.SetBackgroundColour('#e6e7e8')
        self.panel = wx.Panel(self)
        self.iconpath = os.environ["IMAGES_PATH"] + "/avo.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        self.t = wx.TextCtrl(self.panel, wx.ID_ANY,  size=(380, 200),  style = wx.TE_MULTILINE|wx.TE_READONLY)
        self.t.Clear()
        try:
            self.t.AppendText(input)
        except:
            self.t.AppendText("Text cannot be displayed!")
        self.okbutton = wx.Button(self.panel, label="OK", pos=(150, 230))
        self.okbutton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.okbutton.SetFocus()
        self.Centre()
        self.Show()
        interval = readconfig.configvalues['displayVariableTimeOut']
        try:
            interval = int(interval)
        except:
            interval = 3
        self.done = threading.Timer(interval,self.OnOk)
        self.done.start()

    def OnOk(self, *event):
        if self.done is not None and self.done.is_alive():
            self.done.cancel()
        if (self != None) and (bool(self) != False):
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
            
    def debug_object(self,input,wx_object,mythread,driver):
        global dispinput, dispflag, cont
        dispinput = [input,driver]
        dispflag = 'debug'
        cont = mythread
        wx.PostEvent(wx_object.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wx_object.GetId()))
        self.pause_execution()

    def debug_error(self,input,wx_object,mythread):
        global dispinput, dispflag, cont
        dispinput = input
        dispflag = 'error'
        cont = mythread
        wx.PostEvent(wx_object.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wx_object.GetId()))
        self.pause_execution()

class Debug(wx.Frame):
    def __init__(self, parent,id, title, input):
        wx.Frame.__init__(self, parent, title=title,
                          size=(410, 130),style=wx.STAY_ON_TOP| wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX))
        self.SetBackgroundColour('#e6e7e8')
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.iconpath = os.environ["IMAGES_PATH"] + "/avo.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        label="Debug Paused!! Web Element '"+str(input[0]['custname'])+"' not found in step num"+str(input[0]['stepnum'])
        self.text1 = wx.StaticText(self.panel, label=label,pos=(5,0),style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.text1.Wrap(370)
        self.contbutton = wx.Button(self.panel, label="Continue Debug",pos=(55,65))
        self.contbutton.Bind(wx.EVT_BUTTON, self.OnContinue)   # need to implement OnExit(). Leave notrace
        self.scrapebutton = wx.ToggleButton(self.panel, label="Scrape Object",pos=(245,65))
        self.scrapebutton.Bind(wx.EVT_TOGGLEBUTTON, self.OnScrape)   # need to implement OnExit(). Leave notrace
        self.panel.SetSizer(self.sizer)
        self.CenterOnScreen()
        self.Centre()
        self.Show()

    def OnContinue(self, *event):
        self.resume_execution()
        self.Destroy()

    def OnScrape(self, *event):
        from pywinauto import keyboard
        self.scrapebutton.SetValue(self.scrapebutton.GetValue())
        state = self.scrapebutton.GetValue()
        if state == True:
            self.scrapebutton.SetLabel("Stop Scrape")
            self.Hide()
            time.sleep(5)
            keyboard.SendKeys("^+s")
            self.Show()
        else:
            self.Destroy()
            self.resume_execution()

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

class Error(wx.Frame):
    def __init__(self, parent,id, title, input):
        wx.Frame.__init__(self, parent, title=title,
                          size=(410, 130),style=wx.STAY_ON_TOP| wx.DEFAULT_FRAME_STYLE & ~ (wx.MAXIMIZE_BOX|wx.CLOSE_BOX))
        self.SetBackgroundColour('#e6e7e8')
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.iconpath = os.environ["IMAGES_PATH"] + "/avo.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        label="The newly added object is of "+str(input['newtype'])+" and existing object is of "+str(input['custtype'])
        self.text1 = wx.StaticText(self.panel, label=label,pos=(5,0))
        self.text1.Wrap(370)
        self.contbutton = wx.Button(self.panel, label="Terminate Debug",pos=(55,65))
        self.contbutton.Bind(wx.EVT_BUTTON, self.OnContinue)   # need to implement OnExit(). Leave notrace
        self.scrapebutton = wx.ToggleButton(self.panel, label="Save Object",pos=(245,65))
        self.scrapebutton.Bind(wx.EVT_TOGGLEBUTTON, self.OnScrape)   # need to implement OnExit(). Leave notrace
        self.panel.SetSizer(self.sizer)
        self.CenterOnScreen()
        self.Centre()
        self.Show()

    def OnContinue(self, *event):
        self.resume_execution()
        self.Destroy()
        controller.terminate_flag=True

    def OnScrape(self, *event):
        self.Destroy()
        self.resume_execution()

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