import wx
import sys
import os
import controller
import time
from constants import *
import logging
import logging.config
import logger
import threading
from values_from_ui import *


log = logging.getLogger('clientwindow.py')

class Parallel(threading.Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self,wxObject):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self.wxObject = wxObject

        self.start()    # start the thread

    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        try:

            self.wxObject.executebutton.Disable()
            self.wxObject.debugbutton.Disable()
            self.wxObject.cancelbutton.Disable()
            self.wxObject.terminatebutton.Enable()

            time.sleep(2)
##            controller.kill_process()
            con = controller.Controller()
            logging.debug( 'Controller object created')
            value= self.wxObject.breakpoint.GetValue()


##                t = test.Test()
##                t.gettsplist()


            print 'Breakpoint value : ',value
            status = con.invoke_parralel_exe('debug',value)
            if status==TERMINATE:
                print '---------Termination Completed-------'
##                    self.terminatebutton.Enable()
            else:
                logger.print_on_console('***SUITE EXECUTION COMPLETED***')
##                con.execute()
##            controller.kill_process()
            self.wxObject.debugbutton.Enable()
            self.wxObject.executebutton.Enable()
            self.wxObject.cancelbutton.Enable()
##                self.wxObject.pausebutton.Disable()
##                self.wxObject.continuebutton.Disable()
            self.wxObject.terminatebutton.Disable()
        except Exception as m:
            print m





class TestThread(threading.Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self,wxObject):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self.wxObject = wxObject
         #flag to pause thread
        self.paused = False
        # Explicitly using Lock over RLock since the use of self.paused
        # break reentrancy anyway, and I believe using Lock could allow
        # one thread to pause the worker, while another resumes; haven't
        # checked if Condition imposes additional limitations that would
        # prevent that. In Python 2, use of Lock instead of RLock also
        # boosts performance.
        self.pause_cond = threading.Condition(threading.Lock())
        self.start()    # start the thread

    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        try:
            with self.pause_cond as a:
                while self.paused:
                    a.wait()
##                self.wxObject.pausebutton.Enable()
                self.wxObject.executebutton.Disable()
                self.wxObject.debugbutton.Disable()
                self.wxObject.cancelbutton.Disable()
                self.wxObject.terminatebutton.Enable()

                time.sleep(2)
                controller.kill_process()
                con = controller.Controller()
                print 'Controller object created'
                value= self.wxObject.breakpoint.GetValue()


##                t = test.Test()
##                t.gettsplist()


                print 'Breakpoint value : ',value
                status = con.invoke_controller('debug',value)
                if status==TERMINATE:
                    print '---------Termination Completed-------'
##                    self.terminatebutton.Enable()
                else:
                    logger.print_on_console('-----------------------------------------------')
                    log.info('-----------------------------------------------')
                    logger.print_on_console('***SUITE EXECUTION COMPLETED***')
                    log.info('***SUITE EXECUTION COMPLETED***')
                    logger.print_on_console('-----------------------------------------------')
                    log.info('-----------------------------------------------')
##                con.execute()
                controller.kill_process()
                self.wxObject.debugbutton.Enable()
                self.wxObject.executebutton.Enable()
                self.wxObject.cancelbutton.Enable()
##                self.wxObject.pausebutton.Disable()
##                self.wxObject.continuebutton.Disable()
                self.wxObject.terminatebutton.Disable()
        except Exception as m:
            print m
class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        wx.CallAfter(self.out.WriteText, string)

class ClientWindow(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, parent=None,id=-1, title="SLK Nineteen68 - Client Window",
                   pos=(300, 150),  size=(800, 730)  )
        self.SetBackgroundColour(   (245,222,179))
        self.mainclass = self
        self.mythread = None
        curdir = os.getcwd()
        ID_FILE_NEW = 1
        self.iconpath = curdir + "\\slk.ico"

        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d %(message)s',
                            datefmt='%y-%m-%d %H:%M:%S',
                            filename='TestautoV2.log',
                            filemode='a')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logging.addLevelName('INFO','i')
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)


        self.logger = logging.getLogger("Nineteen68")
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(6, 5)
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        box = wx.BoxSizer(wx.VERTICAL)
        self.menubar = wx.MenuBar()
        self.fileMenu = wx.Menu()

        self.configMenu = wx.Menu()
        self.infoItem = wx.MenuItem(self.configMenu, 100,text = "Info",kind = wx.ITEM_NORMAL)
        self.configMenu.AppendItem(self.infoItem)

        self.debugItem = wx.MenuItem(self.configMenu, 101,text = "Debug",kind = wx.ITEM_NORMAL)
        self.configMenu.AppendItem(self.debugItem)

        self.errorItem = wx.MenuItem(self.configMenu, 102,text = "Error",kind = wx.ITEM_NORMAL)
        self.configMenu.AppendItem(self.errorItem)

        self.fileMenu.AppendMenu(wx.ID_ANY, "Logger Level", self.configMenu)
        self.fileMenu.AppendSeparator()
        self.menubar.Append(self.fileMenu, '&File')
        self.SetMenuBar(self.menubar)

        self.Bind(wx.EVT_MENU, self.menuhandler)
        self.log = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(12, 38), size=(760,500), style = wx.TE_MULTILINE|wx.TE_READONLY)
        font1 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL,  False, u'Consolas')
        self.log.SetForegroundColour((0,50,250))
        self.log.SetFont(font1)
        box.Add(self.log, 1, wx.ALL|wx.EXPAND, 5)
        self.debugbutton = wx.Button(self.panel, label="Debug" ,pos=(10, 548), size=(100, 28))
        self.debugbutton.Bind(wx.EVT_BUTTON, self.OnDebug)
        self.debugbutton.SetToolTip(wx.ToolTip("To Debug the script"))
        self.terminatebutton = wx.Button(self.panel, label="Terminate" ,pos=(470, 548), size=(100, 28))
        self.terminatebutton.Bind(wx.EVT_BUTTON, self.OnTerminate)
        self.terminatebutton.SetToolTip(wx.ToolTip("Terminate button logic imp in progress"))
        self.terminatebutton.Disable()



        self.breakpointbutton = wx.Button(self.panel, label="Breakpoint",pos=(590, 548), size=(100, 28))
        self.breakpointbutton.Bind(wx.EVT_BUTTON,None)   # need to implement OnExtract()
        self.breakpointbutton.SetToolTip(wx.ToolTip("Breakpoint"))

        self.breakpoint = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(700, 548), size=(50,28), style = wx.TE_RICH)
        box.Add(self.breakpoint, 1, wx.ALL|wx.EXPAND, 5)

        self.executebutton = wx.Button(self.panel, label="Execute" ,pos=(12, 588), size=(100, 28))
        self.executebutton.Bind(wx.EVT_BUTTON, self.OnExecute)
        self.executebutton.SetToolTip(wx.ToolTip("To execute the script"))

        self.cancelbutton = wx.Button(self.panel, label="Exit" ,pos=(350, 548), size=(100, 28))
        self.cancelbutton.Bind(wx.EVT_BUTTON, self.OnExit)   # need to implement OnExit(). Leave notrace
        self.cancelbutton.SetToolTip(wx.ToolTip("To exit and close the browser"))

        self.clearbutton = wx.Button(self.panel, label="Clear" ,pos=(120, 588), size=(100, 28))
        self.clearbutton.Bind(wx.EVT_BUTTON, self.OnClear)   # need to implement OnExit(). Leave notrace
        self.clearbutton.SetToolTip(wx.ToolTip("To clear the console area"))

        box.AddStretchSpacer()

        self.label1 = wx.StaticText(self.panel,label = "@ 2016 SLK Software Services Pvt. Ltd. All Rights Reserved. Patent Pending.",pos=(12, 628), size=(400, 28))

        # redirect text here
        redir=RedirectText(self.log)
        sys.stdout=redir
        self.panel.SetSizer(self.sizer)
        self.Centre()
        style = self.GetWindowStyle()
        self.Show()

    def menuhandler(self, event):
      id = event.GetId()

      if id == 100:
        print '--Logger level : INFO selected--'





        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.INFO,
                            format='[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
                            datefmt='%y-%m-%d %H:%M:%S',
                            filename='TestautoV2.log',
                            filemode='a')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logging.addLevelName('INFO','i')
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
      elif id == 101:
        print '--Logger level : DEBUG selected--'

        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d %(message)s',
                            datefmt='%y-%m-%d %H:%M:%S',
                            filename='TestautoV2.log',
                            filemode='a')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        logging.addLevelName('DEBUG','d')
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
      elif id ==102:
        print '--Logger level : ERROR selected--'

        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.ERROR,
                            format='%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d %(message)s',
                            datefmt='%y-%m-%d %H:%M:%S',
                            filename='TestautoV2.log',
                            filemode='a')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        logging.addLevelName('ERROR','e')
        console.setLevel(logging.ERROR)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)





    def OnExit(self, event):
        self.Close()

        #----------------------------------------------------------------------
    def OnPause(self, event):

        print '--------- Paused-------'

        self.mythread.pause()

        print '---------controller.pause-------'

    #----------------------------------------------------------------------
    def OnContinue(self, event):
        print '--------- Continue-------'
        self.mythread.resume()
        print '---------controller.Continue-------'
    #----------------------------------------------------------------------
    def OnTerminate(self, event):
        print '---------Termination Started-------'
        self.cancelbutton.Enable()
        controller.terminate_flag=True

    #----------------------------------------------------------------------
    def OnClear(self,event):
        self.log.Clear()
    #-----------------------------------------------------------------------
    def OnExecute(self,event):
        if execution_mode.lower() == 'serial':
            print 'Serial execution'
            TestThread(self)
        elif execution_mode.lower() == 'parallel':
            print 'Parallel execution'
            Parallel(self)
        else:
            print 'Please provide valid execution mode'

    def OnDebug(self,event):
        self.mythread = TestThread(self)




#----------------------------------------------------------------------
def main():
    app = wx.App()
    ClientWindow()
    app.MainLoop()

if __name__ == "__main__":
    main()



