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



##from Tkinter import *
##import Tkinter
##
##
##import threading

##import logger

import wx
import threading

import time
import os
##pause = False
##display = False
dispflag = ''
dispinput = None
cont = None
import controller
import readconfig
class Pause(wx.Frame):
    def __init__(self, parent,id, title):
        wx.Frame.__init__(self, parent, title=title,
                          size=(300, 130),style=wx.STAY_ON_TOP| wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX))
        self.SetBackgroundColour('#e6e7e8')
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(1, 2)
        self.iconpath = os.environ["NINETEEN68_HOME"] + "\\Nineteen68\\plugins\\Core\\Images" + "\\slk.ico"
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


    def OnOk(self, event):
        self.Close()
        self.resume_execution()

    def resume_execution(self):
        global cont
        cont.paused  = False
        pause_flag=False
        # Notify so thread will wake after lock released
        try:
            cont.pause_cond.notify()
        # Now release the lock
            cont.pause_cond.release()
        except Exception as e:
            print('Debug is not paused to Resume')


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
        self.iconpath = os.environ["NINETEEN68_HOME"] + "\\Nineteen68\\plugins\\Core\\Images" + "\\slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
##        self.sizer = wx.GridBagSizer(1, 2)
##        self.text1 = wx.StaticText(self.panel, label=str)
##        self.sizer.Add(self.text1, pos=(0, 1), flag=wx.TOP | wx.LEFT | wx.BOTTOM,border=10)
##        self.line = wx.StaticLine(self.panel)
##        self.text1.Wrap(330)
##        self.sizer.Add(self.line, pos=(1, 0),flag= wx.Center, border=50)
##        self.okbutton = wx.Button(self.panel, label="OK")
##        self.okbutton.Bind(wx.EVT_BUTTON, self.OnOk)   # need to implement OnExit(). Leave notrace
##        self.sizer.Add(self.okbutton, pos=(2, 1), flag=wx.TOP | wx.ALIGN_CENTER, border=5)
##        self.sizer.AddGrowableCol(1)
##
##        self.panel.SetSizer(self.sizer)
        self.t = wx.TextCtrl(self.panel, wx.ID_ANY,  size=(380, 200),  style = wx.TE_MULTILINE|wx.TE_READONLY)
        self.t.Clear()
        self.t.AppendText(str)

        self.okbutton = wx.Button(self.panel, label="OK", pos=(150, 230))
        self.okbutton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.okbutton.SetFocus()
        self.Centre()
##        s
        self.Show()
##        self.timer(5)
        configobj = readconfig.readConfig()
        configvalues = configobj.readJson()
        interval = configvalues['displayVariableTimeOut']
        if interval == '':
            interval = 3
        else:
            try:
                interval = int( configvalues['displayVariableTimeOut'])
            except Exception as e:
                interval = 3
        t = threading.Timer(interval,self.hello)
        t.start()



    def OnOk(self, event):
        self.Close()
        self.resume_execution()



    def hello(self):
        if(self):
            self.resume_execution()
            self.Close()

    def resume_execution(self):
        global cont
        cont.paused  = False
        pause_flag=False
        # Notify so thread will wake after lock released
        try:
            cont.pause_cond.notify()
        # Now release the lock
            cont.pause_cond.release()
        except Exception as e:
            print('Debug is not paused to Resume')


class PauseAndDisplay:
    def __init__(self):
        self.flag = ''
##        self.pause = False
    def display_value(self,input,wx_object,mythread):
##        global display
##        self.flag = 'display'
        global dispinput
        dispinput = input
        global dispflag
        dispflag = 'display'
        global cont
        cont = mythread
        wx.PostEvent(wx_object.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wx_object.GetId()))
        self.pause_execution()
##        return True

    def execute(self,wx_object,mythread):
##        global pause

        self.flag = 'pause'
        global dispflag
        dispflag = 'pause'
        global cont
        cont = mythread

    ##    app = wx.App()
        wx.PostEvent(wx_object.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wx_object.GetId()))
        self.pause_execution()

    def getflagandinput(self):
        global dispflag
        global dispinput

        return dispflag,dispinput

    def pause_execution(self):
        global cont
        cont.paused=True
        cont.pause_cond.acquire()
        with cont.pause_cond:
            while cont.paused:
                cont.pause_cond.wait()


##class App():
##   def __init__(self):
##       self.root = Tkinter.Tk()
##       self.root.title( 'SLK Nineteen68 - Pause')
####       win = Tkinter.Toplevel(self.root)
##       self.root.geometry("300x150")
##       label = Label(self.root, text='Application Paused Click OK to Continue')
##       label.pack()
####       self.root.iconbitmap(default='C:\Users\wasimakram.sutar\Desktop\ForLoggers\Nineteen68\Nineteen68\plugins\Core\slk.ico')
##       button = Tkinter.Button(self.root, text = 'OK',   command=self.quit,width= 100, height = 50)
####       button.place(relx=6.5, rely=6.5,)
####       button.place(bordermode=OUTSIDE, height=100, width=100)
##
##       button.pack()
##       self.root.lift()
##       self.root.attributes('-topmost', True)
##       self.center(self.root)
##       self.root.mainloop()
####       self.root.lift()
##
##
##   def quit(self):
##       self.root.destroy()
##       self.root = None
##
##   def center(self,toplevel):
##        toplevel.update_idletasks()
##        w = toplevel.winfo_screenwidth()
##        h = toplevel.winfo_screenheight()
##        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
##        x = w/2 - size[0]/2
##        y = h/2 - size[1]/2
##        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
##
##
##def execute():
##    app = App()
##
##
##
##
##class App2():
##   def __init__(self,input):
##        self.w = Tkinter.Tk()
##        self.w.title( 'SLK Nineteen68 - DisplayVariable')
##        self.w.geometry("300x150")
####        self.w.iconbitmap(default='C:\Users\wasimakram.sutar\Desktop\ForLoggers\Nineteen68\Nineteen68\plugins\Core\slk.ico')
##        label = Label(self.w, text=input )
##        label.pack()
##        button = Tkinter.Button(self.w, text = 'OK', command = self.quit,  width= 100, height = 50)
##        button.pack()
##        self.w.lift()
##        self.w.attributes('-topmost', True)
##        self.center(self.w)
##        self.w.after(10000, lambda: self.w.destroy()) # Destroy the widget after 30 seconds
##        self.w.mainloop()
##
##   def quit(self):
##       self.w.destroy()
##
##   def center(self,toplevel):
##        toplevel.update_idletasks()
##        w = toplevel.winfo_screenwidth()
##        h = toplevel.winfo_screenheight()
##        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
##        x = w/2 - size[0]/2
##        y = h/2 - size[1]/2
##        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
##
##
##
##def display_value(input):
##    app = App2(input)






