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
from socketIO_client import SocketIO,BaseNamespace
i = 0
wxObject = None
browsername = None
class MainNamespace(BaseNamespace):
    def on_message(self, *args):
##        print 'Inside debugTestCase method'
##        print '------------------',args
        global action,wxObject,browsername
##        self.action=DEBUG
##        global wxObject
##        mythread = TestThread(wxObject,self.action)
##        print args
##        print(args)
        if str(args[0]) == 'OPEN BROWSER CH':
##            print args[0]

##            global wxObject
##            print wxObject
##            global browsername
            browsername = 'CH'
##            print 'Browser name : ',browsername
##            wxObject.test()
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

            time.sleep(5)
##            print 'Importing done'
        elif str(args[0]) == 'OPEN BROWSER IE':
##            print args[0]

##            global wxObject
##            print wxObject
##            global browsername
            browsername = 'IE'
##            print 'Browser name : ',browsername
##            wxObject.test()
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

            time.sleep(5)
##            print 'Importing done'
        elif str(args[0]) == 'OPEN BROWSER FX':
##            print args[0]

##            global wxObject
##            print wxObject

            browsername = 'FX'
##            print 'Browser name : ',browsername
##            wxObject.test()
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

            time.sleep(5)
            print 'Importing done'
        elif str(args[0]) == 'debugTestCase':
            print 'on_debugTestCase',args
            self.mythread = TestThread(wxObject,DEBUG,args[1])



        if(str(args[0]) == 'connected'):
            print('Connection to the Node Server established')


##        elif (str(args[0]) == 'killbrowser'):
##            global wxObject
##            print wxObject
##            global browsername
##            browsername = 'CH'
##            print 'Browser name : ',browsername
####            wxObject.test()
##            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
##            time.sleep(5)
##            con = controller.Controller()
##            con.get_all_the_imports('WebScrape')
##            import browserops
##            driver = browserops.driver
##            driver.close()
##            wxObject.new.Close()
##            print 'Kill the drivers'



    def on_emit(self, *args):
        print 'aaa', args[0]
        if str(args[0]) == 'connected':
            print 'Connected'

    def on_focus(self, *args):
        print 'in focus------------aaa', args[0]
        print '++++++++++++++++++',args
        import highlight
        light =highlight.Highlight()
        res = light.highlight(args[0],None,None)
        print 'Highlight result: ',res

    def on_debugTestCase(self, *args):
        print '------------------on_emit'
        global wxObject
        self.mythread = TestThread(wxObject,DEBUG,args[0])
##        self.socketIO.send(d)





    #----------------------------------------------------------------------
    def __init__(self,wxObject):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self.wxobject = wxObject
        self.start()




    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        global socketIO
        socketIO = SocketIO('10.41.31.41',3000,MainNamespace)

        ##socketIO = SocketIO('localhost',8124)
##        socketIO.send('I am ready to process the request')
        socketIO.emit('news')
        socketIO.emit('focus')
        socketIO.wait()



socketIO = None

class SocketThread(threading.Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self,wxObject):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self.wxobject = wxObject
        self.start()




    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        global socketIO
        socketIO = SocketIO('10.41.31.5',3000,MainNamespace)

        ##socketIO = SocketIO('localhost',8124)
##        socketIO.send('I am ready to process the request')
        socketIO.emit('news')
        socketIO.emit('focus')
        socketIO.emit('debugTestCase')
        socketIO.wait()



class Parallel(threading.Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self,wxObject):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self.wxObject = wxObject
        self.paused = False
        # Explicitly using Lock over RLock since the use of self.paused
        # break reentrancy anyway, and I believe using Lock could allow
        # one thread to pause the worker, while another resumes; haven't
        # checked if Condition imposes additional limitations that would
        # prevent that. In Python 2, use of Lock instead of RLock also
        # boosts performance.
        self.pause_cond = threading.Condition(threading.Lock())
        self.con=''
        self.start()    # start the thread

     #should just resume the thread
    def resume(self):
        self.con.resume_execution()


    #----------------------------------------------------------------------
    def run(self):
        global socketIO
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        try:

            self.wxObject.executebutton.Disable()
            self.wxObject.debugbutton.Disable()
            self.wxObject.cancelbutton.Disable()
            self.wxObject.terminatebutton.Enable()
            self.wxObject.pausebutton.Show()

            import time
            time.sleep(2)
##            controller.kill_process()
            self.con = controller.Controller()
            self.con.conthread=self
            value= self.wxObject.breakpoint.GetValue()

            status = self.con.invoke_parralel_exe(EXECUTE,value,self)

            if status==TERMINATE:
                print '---------Termination Completed-------'

            else:
                logger.print_on_console('***SUITE EXECUTION COMPLETED***')

            self.wxObject.debugbutton.Enable()
            self.wxObject.executebutton.Enable()
            self.wxObject.cancelbutton.Enable()
            socketIO.emit('debugTestCase',status)
##
        except Exception as m:
            print m





class TestThread(threading.Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self,wxObject,action,json_data):
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
        self.con=''
        self.action=action
        self.json_data=json_data
        self.start()    # start the thread


    #should just resume the thread
    def resume(self):
        self.con.resume_execution()



    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        global socketIO
        try:
            self.wxObject.executebutton.Disable()
            self.wxObject.debugbutton.Disable()
            self.wxObject.cancelbutton.Disable()
            self.wxObject.terminatebutton.Enable()
            if self.action==EXECUTE:
                self.wxObject.pausebutton.Show()
            else:
                self.wxObject.continue_debugbutton.Show()


            time.sleep(2)
            controller.kill_process()
            self.con = controller.Controller()
            value= self.wxObject.breakpoint.GetValue()
            debug_mode=False
            runfrom_step=0
            status = self.con.invoke_controller(self.action,self,debug_mode,runfrom_step,self.json_data)
            logger.print_on_console('Execution status',status)

            if status==TERMINATE:
                logger.print_on_console('---------Termination Completed-------')


            controller.kill_process()
            self.wxObject.debugbutton.Enable()
            self.wxObject.executebutton.Enable()
            self.wxObject.cancelbutton.Enable()
            self.wxObject.terminatebutton.Disable()

            socketIO.emit('result_debugTestCase',status)
        except Exception as m:
            print m



class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        wx.CallAfter(self.out.AppendText, string)

class ClientWindow(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, parent=None,id=-1, title="SLK Nineteen68 - Client Window",
                   pos=(300, 150),  size=(800, 730)  )
        self.SetBackgroundColour(   (245,222,179))
        self.id =id
        self.mainclass = self
        self.mythread = ''
        self.action=''
        global wxObject
        wxObject = self
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
        #own event
        self.Bind( wx.EVT_CHOICE, self.test)
        #own event

        #own event
##        self.Bind(wx.EVT_CHOICE, self.debug)
        #own event
##        self.Bind(wx.EVT_CLOSE, self.closeScrapeWindow)
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
        self.connectbutton = wx.Button(self.panel, label="Connect To Node" ,pos=(10, 10), size=(100, 28))
        self.connectbutton.Bind(wx.EVT_BUTTON, self.OnNodeConnect)
        self.connectbutton.SetToolTip(wx.ToolTip("Connect to node Server"))
        self.log = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(12, 38), size=(760,500), style = wx.TE_MULTILINE|wx.TE_READONLY)
        font1 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL,  False, u'Consolas')
        self.log.SetForegroundColour((0,50,250))
        self.log.SetFont(font1)
        box.Add(self.log, 1, wx.ALL|wx.EXPAND, 5)
##        self.debugbutton = wx.Button(self.panel, label="Debug" ,pos=(10, 548), size=(100, 28))
##        self.debugbutton.Bind(wx.EVT_BUTTON, self.OnDebug)
##        self.debugbutton.SetToolTip(wx.ToolTip("To Debug the script"))

##        self.continue_debugbutton = wx.Button(self.panel, label="Resume Debug" ,pos=(120, 548), size=(100, 28))
##        self.continue_debugbutton.Bind(wx.EVT_BUTTON, self.OnContinueDebug)   # need to implement OnExit(). Leave notrace
##        self.continue_debugbutton.SetToolTip(wx.ToolTip("To continue the execution "))
##        self.continue_debugbutton.Hide()

        self.terminatebutton = wx.Button(self.panel, label="Terminate" ,pos=(470, 548), size=(100, 28))
        self.terminatebutton.Bind(wx.EVT_BUTTON, self.OnTerminate)
        self.terminatebutton.SetToolTip(wx.ToolTip("Terminate button logic imp in progress"))
        self.terminatebutton.Disable()

        self.pausebutton = wx.Button(self.panel, label="Pause" ,pos=(230, 548), size=(100, 28))
        self.pausebutton.Bind(wx.EVT_BUTTON, self.OnPause)   # need to implement OnExit(). Leave notrace
        self.pausebutton.SetToolTip(wx.ToolTip("To pause the execution "))
        self.pausebutton.Hide()

        self.continuebutton = wx.Button(self.panel, label="Continue" ,pos=(230, 548), size=(100, 28))
        self.continuebutton.Bind(wx.EVT_BUTTON, self.OnContinue)   # need to implement OnExit(). Leave notrace
        self.continuebutton.SetToolTip(wx.ToolTip("To continue the execution "))
        self.continuebutton.Hide()



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


        self.Bind(wx.EVT_CLOSE, self.OnClose)

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
        logger.print_on_console( '--Logger level : INFO selected--')





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
        logger.print_on_console( '--Logger level : DEBUG selected--')

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
        logger.print_on_console( '--Logger level : ERROR selected--')

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


    def OnClose(self, event):

        print 'KILLING THE THREAD'
        controller.terminate_flag=True
        print self.debug
        import debug_window
        if isinstance(self.debug , debug_window.DebugWindow) and self.debug.IsShown():
            self.debug.Destroy()

        self.Destroy()
         # you may also do:  event.Skip()
                        # since the default event handler does call Destroy(), too

##    def closeScrapeWindow(self):
##        global socketIO
##        print 'SocketIO : ',socketIO
##        if socketIO != None:
##            log.info('Closing the socket')
##            socketIO.disconnect()
##            log.info(socketIO)
##            self.new.Close()

    def OnExit(self, event):
        global socketIO
        print 'SocketIO : ',socketIO
        if socketIO != None:
            log.info('Closing the socket')
            socketIO.disconnect()
            log.info(socketIO)
##            self.new.Close()
        self.debug.Close()
        self.Close()


        #----------------------------------------------------------------------
    def OnPause(self, event):
        logger.print_on_console('Event Triggered to Pause')
        log.info('Event Triggered to Pause')
        controller.pause_flag=True
        self.pausebutton.Hide()
        self.continuebutton.Show()


    def OnContinueDebug(self, event):
        logger.print_on_console('Event Triggered to Resume Debug')
        log.info('Event Triggered to Resume Debug')
        controller.pause_flag=False
        self.mythread.resume()
        self.continuebutton.Hide()



    #----------------------------------------------------------------------
    def OnContinue(self, event):
        logger.print_on_console('Event Triggered to Resume')
        log.info('Event Triggered to Resume')
        self.resume()

    def resume(self):
        controller.pause_flag=False
        self.mythread.resume()
        self.continuebutton.Hide()
        self.pausebutton.Show()
    #----------------------------------------------------------------------
    def OnTerminate(self, event):
        logger.print_on_console('---------Termination Started-------')
        controller.terminate_flag=True
        #Handling the case where user clicks terminate when the execution is paused
        #Resume the execution
        if controller.pause_flag:
            self.resume()


    #----------------------------------------------------------------------
    def OnClear(self,event):
##        self.test()
        self.log.Clear()


    #-----------------------------------------------------------------------
    def OnExecute(self,event):
        global action
        self.action=EXECUTE
        if execution_mode.lower() == 'serial':
            print( '=======================================================================================================')
            logger.print_on_console('Execution mode : SERIAL')
            print( '=======================================================================================================')
            self.mythread=TestThread(self,self.action)
        elif execution_mode.lower() == 'parallel':
            logger.print_on_console('Execution mode : PARALLEL')
            print( '=======================================================================================================')
            self.mythread=Parallel(self)
        else:
            logger.print_on_console('Please provide valid execution mode')

    def OnDebug(self,event):
        self.debug()
##        global action
##        self.action=STEP_BY_SETP_DEBUG
##        self.mythread = TestThread(self,self.action)

    def OnNodeConnect(self,event):
        self.mythread = SocketThread(self)
        self.connectbutton.Disable()

    def test(self,event):
##        print 'Self',self
        global browsername
        print 'Browser name : ',browsername
        con = controller.Controller()
        con.get_all_the_imports('WebScrape')
        import Nineteen68_WebScrape
        global socketIO
        self.new = Nineteen68_WebScrape.ScrapeWindow(parent = None,id =None, title="SLK Nineteen68 - Web Scrapper",browser = browsername,socketIO = socketIO)

    def debug(self):

        import debug_window
        global socketIO,action
        self.action=STEP_BY_SETP_DEBUG
        self.mythread = TestThread(self,self.action)
        thread_obj=self.mythread
        self.debug = debug_window.DebugWindow(parent = None,id = -1, title="SLK Nineteen68 - Debug Window",browser = browsername,socketIO = socketIO,thread=self.mythread)
##        self.new.Show()

    def OnNodeConnect(self,event):
        self.mythread = SocketThread(self)
        self.connectbutton.Disable()

    def test(self,event):
##        print 'Self',self
        global browsername
        print 'Browser name : ',browsername
        con = controller.Controller()
        con.get_all_the_imports('WebScrape')
        import Nineteen68_WebScrape
        global socketIO
        self.new = Nineteen68_WebScrape.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Web Scrapper",browser = browsername,socketIO = socketIO)
##        self.new.Show()




#----------------------------------------------------------------------
def main():
    app = wx.App()
    ClientWindow()
    print( '*******************************************************************************************************')
    print( '=========================================Nineteen68 Client Window======================================')
    print( '*******************************************************************************************************')
    app.MainLoop()

if __name__ == "__main__":
    main()


