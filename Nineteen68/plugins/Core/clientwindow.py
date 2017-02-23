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
        if str(args[0]) == 'OPEN BROWSER CH':

            browsername = '1'
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

            time.sleep(5)
        elif str(args[0]) == 'OPEN BROWSER IE':

            browsername = '3'
##
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

            time.sleep(5)
##            print 'Importing done'
        elif str(args[0]) == 'OPEN BROWSER FX':
##
            browsername = '2'
##
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

            time.sleep(5)
            print 'Importing done'

        elif str(args[0]) == 'debugTestCase':
            print 'on_debugTestCase_message'
            wxObject.mythread = TestThread(wxObject,DEBUG,args[1])


        if(str(args[0]) == 'connected'):
            print('Connection to the Node Server established')


    def on_emit(self, *args):
        if str(args[0]) == 'connected':
            print 'Connected'

    def on_focus(self, *args):

        appType=args[1]
        if appType==APPTYPE_WEB:
            import highlight
            light =highlight.Highlight()
            res = light.highlight(args[0],None,None)
            print 'Highlight result: ',res
        elif appType==APPTYPE_DESKTOP:
            con =controller.Controller()
            con.get_all_the_imports('Desktop')
            import desktop_highlight
            highlightObj=desktop_highlight.highLight()
            highlightObj.highLiht_element(args[0].split(',')[0],args[0].split(',')[1])
            print 'highlight called'

    def on_executeTestSuite(self, *args):
        global wxObject
        args=list(args)
        wxObject.mythread = TestThread(wxObject,EXECUTE,args[0],wxObject.debug_mode)

    def on_debugTestCase(self, *args):
        global wxObject
        args=list(args)
        wxObject.mythread = TestThread(wxObject,DEBUG,args[0],wxObject.debug_mode)

    def on_LAUNCH_DESKTOP(self, *args):
        con = controller.Controller()
        global browsername
        browsername = args[0]
        con =controller.Controller()
        con.get_all_the_imports('Desktop')
        import ninteen_68_desktop_scrape
        global desktopScrapeObj
        desktopScrapeObj=ninteen_68_desktop_scrape
        global desktopScrapeFlag
        desktopScrapeFlag=True

        wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))




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
        socketIO = SocketIO('127.0.0.1',3000,MainNamespace)

        ##socketIO = SocketIO('localhost',8124)
##        socketIO.send('I am ready to process the request')
        socketIO.emit('news')
        socketIO.emit('focus')
        socketIO.emit('debugTestCase')
        socketIO.emit('executeTestSuite')
        socketIO.emit('LAUNCH_DESKTOP')
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
            #Removed execute button
##            self.wxObject.executebutton.Disable()
            #Removed debug button
##            self.wxObject.debugbutton.Disable()
            self.wxObject.cancelbutton.Disable()
            self.wxObject.terminatebutton.Enable()
##            self.wxObject.pausebutton.Show()

            import time
            time.sleep(2)
##            controller.kill_process()
            self.con = controller.Controller()
            self.con.conthread=self
            #Removed breakpoint
##            value= self.wxObject.breakpoint.GetValue()
            value=''

            status = self.con.invoke_parralel_exe(EXECUTE,value,self)

            if status==TERMINATE:
                print '---------Termination Completed-------'

            else:
                logger.print_on_console('***SUITE EXECUTION COMPLETED***')

##            self.wxObject.debugbutton.Enable()
##            self.wxObject.executebutton.Enable()
            self.wxObject.cancelbutton.Enable()
            socketIO.emit('result_executeTestSuite',status)
##
        except Exception as m:
            print m





class TestThread(threading.Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self,wxObject,action,json_data,debug_mode):
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
        self.debug_mode=debug_mode

        self.start()    # start the thread


    #should just resume the thread
    def resume(self,debug_mode):
        if not(debug_mode):
            self.con.debug_mode=False
        self.con.resume_execution()



    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        global socketIO
        try:
            #Removed execute,debug button

            self.wxObject.cancelbutton.Disable()
            self.wxObject.terminatebutton.Enable()
            runfrom_step=1
            if self.action==DEBUG:
                self.debug_mode=False
                self.wxObject.breakpoint.Disable()
                if self.wxObject.choice in ['Stepwise','RunfromStep']:
                    self.debug_mode=True
                    self.wxObject.continue_debugbutton.Show()
                    self.wxObject.continuebutton.Show()
                    self.wxObject.continue_debugbutton.Enable()
                    self.wxObject.continuebutton.Enable()

                    if self.wxObject.choice=='RunfromStep':
                        self.wxObject.breakpoint.Enable()
                        try:
                            runfrom_step=self.wxObject.breakpoint.GetValue()
                            runfrom_step=int(runfrom_step)
                        except Exception as e:
                            runfrom_step=1
                            log.error('Invalid step number, Hence default step num is taken as 1')
                            logger.print_on_console('Invalid step number, Hence default step num is taken as 1')
            else:
                self.wxObject.rbox.Disable()







##

            self.wxObject.breakpoint.Disable()
##            controller.kill_process()
            self.con = controller.Controller()
            self.wxObject.terminatebutton.Enable()
            status = self.con.invoke_controller(self.action,self,self.debug_mode,runfrom_step,self.json_data,self.wxObject,socketIO)
            logger.print_on_console('Execution status',status)


            if status==TERMINATE:
                logger.print_on_console('---------Termination Completed-------')


##            controller.kill_process()
            #Removed execute,debug button
##            self.wxObject.debugbutton.Enable()
##            self.wxObject.executebutton.Enable()
            self.wxObject.breakpoint.Clear()
            self.wxObject.rbox.Enable()
            self.wxObject.cancelbutton.Enable()
            self.wxObject.terminatebutton.Disable()
            self.wxObject.continuebutton.Hide()
            self.wxObject.continue_debugbutton.Hide()
            self.wxObject.mythread=None
            if self.action==DEBUG:
                socketIO.emit('result_debugTestCase',status)
            elif self.action==EXECUTE:
                socketIO.emit('result_executeTestSuite',status)
        except Exception as e:
            print e
            log.error(e)



class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        wx.CallAfter(self.out.AppendText, string)

class ClientWindow(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, parent=None,id=-1, title="ICE Engine",
                   pos=(300, 150),  size=(800, 730),style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.RESIZE_BOX |wx.MAXIMIZE_BOX)  )
##        self.SetBackgroundColour(   (245,222,179))
        self.SetBackgroundColour('#e6e7e8')
##        self.ShowFullScreen(True,wx.ALL)
##        self.SetBackgroundColour('#D0D0D0')

        self.id =id
        self.mainclass = self
        self.mythread = None
        self.action=''
        self.debug_mode=False
        self.choice='Normal'
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
        connect_img=wx.Image("connect.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.connectbutton = wx.BitmapButton(self.panel, bitmap=connect_img,pos=(10, 10), size=(100, 25))
##        self.connectbutton = wx.Button(self.panel, label="Connect" ,pos=(10, 10), size=(100, 28))
        self.connectbutton.Bind(wx.EVT_BUTTON, self.OnNodeConnect)
        self.connectbutton.SetToolTip(wx.ToolTip("Connect to node Server"))
        self.log = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(12, 38), size=(760,500), style = wx.TE_MULTILINE|wx.TE_READONLY)
        font1 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL,  False, u'Consolas')
        self.log.SetForegroundColour((0,50,250))
        self.log.SetFont(font1)

        box.Add(self.log, 1, wx.ALL|wx.EXPAND, 5)
##        size=(90, 28)

        #Radio buttons
        lblList = ['Normal', 'Stepwise', 'RunfromStep']
        self.rbox = wx.RadioBox(self.panel,label = 'Debug options', pos = (10, 548), choices = lblList ,size=(300, 100),
        majorDimension = 1, style = wx.RA_SPECIFY_ROWS)

##        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)
        self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)
##        self.rbox.SetBackgroundColour('#9f64e2')

        paly_img = wx.Image("play.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        terminate_img=wx.Image("terminate.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        step_img=wx.Image("step.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()

##        self.button1 = wx.BitmapButton(self.panel1, id=-1, bitmap=image1,
##        pos=(10, 20), size = (200, image1.GetHeight()+5))

##        self.debugbutton = wx.Button(self.panel, label="Debug" ,pos=(10, 548), size=(100, 28))
##        self.debugbutton.Bind(wx.EVT_BUTTON, self.OnDebug)
##        self.debugbutton.SetToolTip(wx.ToolTip("To Debug the script"))

##

##        self.terminatebutton = wx.BitmapButton(self.panel, bitmap=terminate_img,pos=(470, 548), size=(50, 40))
####        self.terminatebutton = wx.Button(self.panel, label="Terminate" ,pos=(470, 548), size=(100, 28))
##        self.terminatebutton.Bind(wx.EVT_BUTTON, self.OnTerminate)
##        self.terminatebutton.SetToolTip(wx.ToolTip("To Terminate the execution"))
##        self.terminatebutton.Disable()

##        self.pausebutton = wx.Button(self.panel, label="Pause" ,pos=(230, 548), size=(75, 28))
##        self.pausebutton.Bind(wx.EVT_BUTTON, self.OnPause)   # need to implement OnExit(). Leave notrace
##        self.pausebutton.SetToolTip(wx.ToolTip("To pause the execution "))
##        self.pausebutton.Hide()


##        self.continue_debugbutton = wx.Button(self.panel, label="Resume" ,pos=(140, 548), size=(75, 28))
##        self.continue_debugbutton = wx.BitmapButton(self.rbox, bitmap=paly_img,pos=(70, 598), size=(35, 28))

        self.continue_debugbutton = wx.StaticBitmap(self.rbox, -1, wx.Bitmap("play.png", wx.BITMAP_TYPE_ANY), (75, 50), (35, 28))
        self.continue_debugbutton.Bind(wx.EVT_LEFT_DOWN, self.Resume)
        self.continue_debugbutton.SetToolTip(wx.ToolTip("To continue the execution"))
        self.continue_debugbutton.Hide()

##        self.continue_debugbutton = wx.BitmapButton(self.rbox, bitmap=paly_img,pos=(75, 50), size=(35, 28))
##        self.continue_debugbutton.Bind(wx.EVT_BUTTON, self.Resume)
##        self.continue_debugbutton.SetToolTip(wx.ToolTip("To Resume the execution "))
##        self.continue_debugbutton.Hide()

        self.continuebutton = wx.StaticBitmap(self.rbox, -1, wx.Bitmap("step.png", wx.BITMAP_TYPE_ANY), (105, 50), (35, 28))
##        self.continuebutton = wx.BitmapButton(self.panel, bitmap=step_img,pos=(130, 598), size=(35,28))
##        self.continuebutton = wx.Button(self.panel, label="Continue" ,pos=(230, 548), size=(75, 28))
        self.continuebutton.Bind(wx.EVT_LEFT_DOWN, self.OnContinue)
        self.continuebutton.SetToolTip(wx.ToolTip("To Resume the execution "))
        self.continuebutton.Hide()



##        self.breakpointbutton = wx.Button(self.panel, label="Breakpoint",pos=(590, 548), size=(100, 28))
##        self.breakpointbutton.Bind(wx.EVT_BUTTON,None)   # need to implement OnExtract()
##        self.breakpointbutton.SetToolTip(wx.ToolTip("Breakpoint"))

        self.breakpoint = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(230, 598), size=(60,20), style = wx.TE_RICH)
        box.Add(self.breakpoint, 1, wx.ALL|wx.EXPAND, 5)
        self.breakpoint.Disable()

##        self.executebutton = wx.Button(self.panel, label="Execute" ,pos=(12, 588), size=(100, 28))
##        self.executebutton.Bind(wx.EVT_BUTTON, self.OnExecute)
##        self.executebutton.SetToolTip(wx.ToolTip("To execute the script"))

        killprocess_img = wx.Image("killStaleProcess.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.cancelbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap("killStaleProcess.png", wx.BITMAP_TYPE_ANY), (360, 548), (50, 40))
        self.cancelbutton.Bind(wx.EVT_LEFT_DOWN, self.OnExit)
        self.cancelbutton.SetToolTip(wx.ToolTip("To kill Stale process"))
        self.cancel_label=wx.StaticText(self.panel, -1, 'Kill Stale Process', (340, 600), (100, 70))

        self.terminatebutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap("terminate.png", wx.BITMAP_TYPE_ANY), (470, 548), (50, 40))
        self.terminatebutton.Bind(wx.EVT_LEFT_DOWN, self.OnTerminate)
        self.terminatebutton.SetToolTip(wx.ToolTip("To Terminate the execution"))
        self.terminate_label=wx.StaticText(self.panel, -1, 'Terminate', (470, 600), (100, 70))


##        self.cancelbutton = wx.BitmapButton(self.panel, bitmap=killprocess_img,pos=(350, 548), size=(50, 40))
####        self.cancelbutton = wx.Button(self.panel, label="Exit" ,pos=(350, 548), size=(100, 28))
##        self.cancelbutton.Bind(wx.EVT_BUTTON, self.OnExit)
##        self.cancelbutton.SetToolTip(wx.ToolTip("To kill Stale process"))

        self.clearbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap("clear.png", wx.BITMAP_TYPE_ANY), (590, 548), (50, 40))
        self.clearbutton.Bind(wx.EVT_LEFT_DOWN, self.OnClear)
        self.clearbutton.SetToolTip(wx.ToolTip("To clear the console area"))
        self.clear_label=wx.StaticText(self.panel, -1, 'Clear', (600, 600), (100, 70))




##        clear_img = wx.Image("clear.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
##        self.clearbutton = wx.BitmapButton(self.panel, bitmap=clear_img,pos=(590, 548), size=(50,40))
####        self.clearbutton = wx.Button(self.panel, label="Clear" ,pos=(590, 548), size=(100, 28))
##        self.clearbutton.Bind(wx.EVT_BUTTON, self.OnClear)   # need to implement OnExit(). Leave notrace
##        self.clearbutton.SetToolTip(wx.ToolTip("To clear the console area"))


        self.Bind(wx.EVT_CLOSE, self.OnClose)

        box.AddStretchSpacer()

##        self.label1 = wx.StaticText(self.panel,label = "@ 2016 SLK Software Services Pvt. Ltd. All Rights Reserved. Patent Pending.",pos=(12, 628), size=(400, 28))

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

##    def OnRadiogroup(self, e):
##        rb = e.GetEventObject()
##        print rb.GetLabel(),' is clicked from Radio Group'

    def onRadioBox(self,e):
        self.choice=self.rbox.GetStringSelection()
        print self.choice,' is Selected'
        self.debug_mode=False
        self.breakpoint.Disable()
        if self.choice in ['Stepwise','RunfromStep']:
            self.debug_mode=True
            self.continue_debugbutton.Show()
            self.continuebutton.Show()
            if self.choice=='RunfromStep':
                self.breakpoint.Enable()
            if self.mythread==None:
                self.continue_debugbutton.Disable()
                self.continuebutton.Disable()

        else:
            self.continuebutton.Hide()
            self.continue_debugbutton.Hide()








    def OnClose(self, event):

        print 'KILLING THE THREAD'
        controller.terminate_flag=True
        global socketIO
        print 'SocketIO : ',socketIO
        if socketIO != None:
            log.info('Closing the socket')
            socketIO.disconnect()
            log.info(socketIO)
##            self.new.Close()
##        self.Close()
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
        controller.kill_process()
##        global socketIO
##        print 'SocketIO : ',socketIO
##        if socketIO != None:
##            log.info('Closing the socket')
##            socketIO.disconnect()
##            log.info(socketIO)
####            self.new.Close()
##        self.Close()


        #----------------------------------------------------------------------
    def OnPause(self, event):
        logger.print_on_console('Event Triggered to Pause')
        log.info('Event Triggered to Pause')
        controller.pause_flag=True
##        self.pausebutton.Hide()
        self.continuebutton.Show()


    def Resume(self, event):
        logger.print_on_console('Event Triggered to Resume Debug')
        log.info('Event Triggered to Resume Debug')
        controller.pause_flag=False
        self.mythread.resume(False)
        self.continuebutton.Hide()
        self.continue_debugbutton.Hide()



    #----------------------------------------------------------------------
    def OnContinue(self, event):
        logger.print_on_console('Event Triggered to Resume')
        log.info('Event Triggered to Resume')
        self.resume(True)

    def resume(self,debug_mode):
        controller.pause_flag=False
        self.mythread.resume(debug_mode)
##        self.continuebutton.Hide()
##        self.pausebutton.Show()
    #----------------------------------------------------------------------
    def OnTerminate(self, event):
        logger.print_on_console('---------Termination Started-------')
        controller.terminate_flag=True
        #Handling the case where user clicks terminate when the execution is paused
        #Resume the execution
        if controller.pause_flag:
            self.resume(False)


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

##    def debug(self):
##
##        import debug_window
##        global socketIO,action
##        self.action=STEP_BY_SETP_DEBUG
##        self.mythread = TestThread(self,self.action)
##        thread_obj=self.mythread
##        self.debug = debug_window.DebugWindow(parent = None,id = -1, title="SLK Nineteen68 - Debug Window",browser = browsername,socketIO = socketIO,thread=self.mythread)
####        self.new.Show()

    def OnNodeConnect(self,event):
        self.mythread = SocketThread(self)
        self.connectbutton.Disable()

    def test(self,event):
##        print 'Self',self
        if desktopScrapeFlag==True:
            global socketIO

            self.new = desktopScrapeObj.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Desktop Scrapper",filePath = browsername,socketIO = socketIO)
            desktopScrapeFlag=False
        else:
            global browsername
            browsernumbers = ['1','2','3']
            if browsername in browsernumbers:
                print 'Browser name : ',browsername
                con = controller.Controller()
                con.get_all_the_imports('Web')
                con.get_all_the_imports('WebScrape')
                import Nineteen68_WebScrape
                global socketIO
                self.new = Nineteen68_WebScrape.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Web Scrapper",browser = browsername,socketIO = socketIO)
                browsername = ''
            else:
                import pause_display_operation
                o = pause_display_operation.PauseAndDisplay()
                flag,inputvalue = o.getflagandinput()
                if flag == 'pause':
                    #call pause logic
                    self.new = pause_display_operation.Pause(parent = None,id = -1, title="SLK Nineteen68 - Pause")
                elif flag == 'display':
                    #call display logic
                    self.new = pause_display_operation.Display(parent = self,id = -1, title="SLK Nineteen68 - Display Variable",input = inputvalue)





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



