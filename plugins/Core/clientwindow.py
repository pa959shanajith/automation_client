import wx
import sys
import os
import time
import logging
import core
import core_utils
import logger
import threading
import wx.lib.scrolledpanel
import wx.richtext
from constants import *
import controller
import readconfig
import json
import requests
import io
import handler
import update_module
import benchmark
isTrial = readconfig.configvalues.get("isTrial")
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
log = logging.getLogger('clientwindow.py')
root = None
wxObject = None
icesession = None
configvalues = None
proxies = None
update_obj = None
SERVER_LOC = None
pdfgentool = None


class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        wx.CallAfter(self.out.AppendText, string)
        # wx.CallAfter(self.out.MoveEnd)
        # wx.CallAfter(self.out.WriteText, string)
        # wx.CallAfter(self.out.MoveEnd)
        # wx.CallAfter(self.out.ShowPosition,self.out.GetLastPosition())

    # def write_color(self, string, color):
    #     if(color=='RED'): rgb_color=(220,53,69)
    #     elif(color=='GREEN'): rgb_color=(40,167,69)
    #     elif(color=='YELLOW'): rgb_color=(255, 193, 7)
    #     else: rgb_color=(0, 50, 250)
    #     wx.CallAfter(self.out.BeginTextColour, rgb_color)
    #     self.write(string)
    #     wx.CallAfter(self.out.EndTextColour)
    #     wx.CallAfter(self.out.BeginTextColour, (0, 50, 250))

    def flush(self):
        pass


class ClientWindow(wx.Frame):
    def __init__(self):
        self.appName = root.name
        wx.Frame.__init__(self, parent=None,id=-1, title=self.appName,
                   pos=(300, 150),  size=(800, 730),style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER  | wx.MAXIMIZE_BOX))
        self.SetBackgroundColour('#e6e7e8')
        ##self.ShowFullScreen(True,wx.ALL)
        ##self.SetBackgroundColour('#D0D0D0')
        self.debugwindow = None
        self.scrapewindow = None
        self.pausewindow = None
        self.pluginPDF = None
        self.aboutWindow = None
        self.ProxyConfig_window = None
        self.Config_window = None
        self.Check_Update_window = None
        self.rollback_window = None
        self.action=''
        self.debug_mode=False
        self.choice='Normal'
        global wxObject
        self.iconpath = IMAGES_PATH +"avo.ico"
        self.connect_img=wx.Image(IMAGES_PATH +"connect.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.disconnect_img=wx.Image(IMAGES_PATH +"disconnect.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.register_img=wx.Image(IMAGES_PATH +"register.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.enabledStatus = [False,False,False,False,False,False,False,False]
        wxObject = self

        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(6, 5)
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        box = wx.BoxSizer(wx.VERTICAL)
        self.menubar = wx.MenuBar()
        self.fileMenu = wx.Menu()
        self.editMenu = wx.Menu()
        self.toolMenu = wx.Menu()
        self.helpMenu = wx.Menu()
        #own event
        self.Bind(wx.EVT_CHOICE, self.test)
        #own event
        self.loggerMenu = wx.Menu()
        self.infoItem = wx.MenuItem(self.loggerMenu, 100,text = "&Info",kind = wx.ITEM_NORMAL)
        self.loggerMenu.Append(self.infoItem)
        self.debugItem = wx.MenuItem(self.loggerMenu, 101,text = "&Debug",kind = wx.ITEM_NORMAL)
        self.loggerMenu.Append(self.debugItem)
        self.errorItem = wx.MenuItem(self.loggerMenu, 102,text = "&Error",kind = wx.ITEM_NORMAL)
        self.loggerMenu.Append(self.errorItem)
        self.fileMenu.AppendSubMenu(self.loggerMenu, "&Logger Level")
        self.menubar.Append(self.fileMenu, '&File')

        self.configItem = wx.MenuItem(self.editMenu, 103,text = "&Configuration",kind = wx.ITEM_NORMAL)
        # Name : A Sreenivasulu Date : 02/08/2022
        # configuration editmenu is disabled with low TLS Security Level
        configmenu = self.editMenu.Append(self.configItem)
        if isTrial:
            configmenu.Enable(False)
        # end
        self.proxyconfigItem = wx.MenuItem(self.editMenu, 104,text = "&Proxy Configuration",kind = wx.ITEM_NORMAL)
        self.editMenu.Append(self.proxyconfigItem)
        self.menubar.Append(self.editMenu, '&Edit')
        self.pdfReportItem = wx.MenuItem(self.toolMenu, 151,text = "Generate PDF &Report",kind = wx.ITEM_NORMAL)
        self.toolMenu.Append(self.pdfReportItem)
        self.pdfReportBatchItem = wx.MenuItem(self.toolMenu, 152,text = "Generate PDF Report (B&atch)",kind = wx.ITEM_NORMAL)
        self.toolMenu.Append(self.pdfReportBatchItem)
        self.menubar.Append(self.toolMenu, 'T&ools')
        self.SetMenuBar(self.menubar)

        self.aboutItem = wx.MenuItem(self.helpMenu, 160, text="About", kind=wx.ITEM_NORMAL)
        self.helpMenu.Append(self.aboutItem)
        if SYSTEM_OS!='Linux':
            self.updateItem = wx.MenuItem(self.helpMenu, 161, text="Check for Updates", kind=wx.ITEM_NORMAL)
            self.helpMenu.Append(self.updateItem)
            self.updateItem.Enable(True)
            self.rollbackItem = wx.MenuItem(self.helpMenu, 162, text="Rollback", kind=wx.ITEM_NORMAL)
            self.helpMenu.Append(self.rollbackItem)
            self.rollbackItem.Enable(True)
        self.menubar.Append(self.helpMenu, '&Help')

        self.Bind(wx.EVT_MENU, self.menuhandler)
        self.connectbutton = wx.BitmapButton(self.panel, bitmap=self.connect_img,pos=(10, 10), size=(100, 25), name='connect')
        self.connectbutton.Bind(wx.EVT_BUTTON, self.OnNodeConnect)
        self.connectbutton.SetToolTip(wx.ToolTip("Connect to Avo Assure Server"))
        self.log = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(12, 38), size=(760,500), style = wx.TE_MULTILINE|wx.TE_READONLY)
        # self.log = wx.richtext.RichTextCtrl(self.panel, wx.ID_ANY, pos=(12, 38), size=(760,500), style = wx.richtext.RE_MULTILINE|wx.richtext.RE_READONLY|wx.TE_RICH2)
        font1 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL,  False, 'Consolas')
        self.log.SetForegroundColour((0,50,250))
        # self.log.BeginTextColour((0, 50, 250))
        self.log.SetFont(font1)

        if SYSTEM_OS == 'Windows':
            self.schedule = wx.CheckBox(self.panel, label='Do Not Disturb', pos=(120, 10), size=(120, 25))
        else:
            self.schedule = wx.CheckBox(self.panel, label = 'Do Not Disturb',pos=(120, 10))
        # self.schedule = wx.CheckBox(self.panel, label = 'Do Not Disturb',pos=(120, 10), size=(100, 25))
        self.schedule.SetToolTip(wx.ToolTip("Enable Do Not Disturb Mode"))
        self.schedule.Bind(wx.EVT_CHECKBOX,self.onChecked_Schedule)
        self.schedule.Disable()

        box.Add(self.log, 1, wx.ALL|wx.EXPAND, 5)

        #Radio buttons
        lblList = ['Normal', 'Stepwise', 'RunfromStep']
        self.rbox = wx.RadioBox(self.panel,label = 'Debug options', pos = (10, 548), choices = lblList ,size=(380, 100),
        majorDimension = 1, style = wx.RA_SPECIFY_ROWS)

        self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)
        self.breakpoint = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(267, 605), size=(88,25), style = wx.TE_RICH)
        box.Add(self.breakpoint, 1, wx.ALL|wx.EXPAND, 5)
        self.breakpoint.Bind(wx.EVT_CHAR, self.handle_keypress)
        self.breakpoint.Disable()

        self.cancelbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"killStaleProcess.png", wx.BITMAP_TYPE_ANY), wx.Point(440, 555), wx.Size(50, 42))
        self.cancelbutton.Bind(wx.EVT_LEFT_DOWN, self.OnKillProcess)
        self.cancelbutton.SetToolTip(wx.ToolTip("To kill Stale process"))
        self.cancel_label=wx.StaticText(self.panel, -1, 'Kill Stale Process', wx.Point(435, 600), wx.Size(100, 70))

        self.terminatebutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"terminate.png", wx.BITMAP_TYPE_ANY), wx.Point(555, 555), wx.Size(50, 42))
        self.terminatebutton.Bind(wx.EVT_LEFT_DOWN, self.OnTerminate)
        self.terminatebutton.SetToolTip(wx.ToolTip("To Terminate the execution"))
        self.terminate_label=wx.StaticText(self.panel, -1, 'Terminate', wx.Point(547, 600), wx.Size(100, 70))

        self.clearbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"clear.png", wx.BITMAP_TYPE_ANY), wx.Point(670, 555), wx.Size(50, 42))
        self.clearbutton.Bind(wx.EVT_LEFT_DOWN, self.OnClear)
        self.clearbutton.SetToolTip(wx.ToolTip("To clear the console area"))
        self.clear_label=wx.StaticText(self.panel, -1, 'Clear', wx.Point(677, 600), wx.Size(100, 70))
        self.Bind(wx.EVT_CLOSE, root.close)

        box.AddStretchSpacer()

        # redirect text here
        redir=RedirectText(self.log)
        sys.stdout=redir
        self.panel.SetSizer(self.sizer)
        self.Centre()
        self.Show()

    """ Allows only integer values, directional keys and a single hyphen to provide a range """
    def handle_keypress(self, event):
        cur_input=chr(event.GetKeyCode())
        if cur_input in '0123456789\x08\x09ĺĽĻļĹĸŷŸŹźŻž\x7f': event.Skip()
        elif cur_input == '-':
            prev_input=event.EventObject.Value
            if prev_input != '' and prev_input.count('-') == 0: event.Skip()

    """
    Menu Items:
      1. Modifying Logger and Handlers Level dynamically without creating a new logger object
         When logging level is changed from Client window using "File" button.
      2. Edit client configuration
    """
    def menuhandler(self, event):
        global pdfgentool
        id = event.GetId()
        if id == 100:     # When user selects INFO level
            logging.getLogger().setLevel(logging.INFO)
            for handler in logging.root.handlers[:]:
                    handler.setLevel(logging.INFO)
            logging.getLogger('socketio.client').setLevel(logging.WARN)
            logging.getLogger('engineio.client').setLevel(logging.WARN)
            logger.print_on_console( '--Logger level : INFO selected--')
            log.info('--Logger level : INFO selected--')
        elif id == 101:    # When user selects DEBUG level
            logging.getLogger().setLevel(logging.DEBUG)
            for handler in logging.root.handlers[:]:
                handler.setLevel(logging.DEBUG)
            logging.getLogger('socketio.client').setLevel(logging.DEBUG)
            logging.getLogger('engineio.client').setLevel(logging.DEBUG)
            logger.print_on_console( '--Logger level : DEBUG selected--')
            log.info('--Logger level : DEBUG selected--')
        elif id ==102:     # When user selects ERROR level
            logger.print_on_console( '--Logger level : ERROR selected--')
            log.info( '--Logger level : ERROR selected--')
            logging.getLogger().setLevel(logging.ERROR)
            for handler in logging.root.handlers[:]:
                handler.setLevel(logging.ERROR)
        elif id==103:      # When user selects Edit > Configuraion
            try:
                msg = '--Edit Config selected--'
                logger.print_on_console(msg)
                log.info(msg)
                if(self.Config_window):
                    self.Config_window.Raise()
                else:
                    self.Config_window = Config_window(parent = None,id = -1, title="Avo Assure Configuration")
            except Exception as e:
                msg = "Error while updating configuration"
                logger.print_on_console(msg)
                log.info(msg)
                log.error(e)
        elif id==104:     # When user selects Edit > Proxy Configuraion
            try:
                msg = '--Edit Proxy Config selected--'
                logger.print_on_console(msg)
                log.info(msg)
                if (self.ProxyConfig_window):
                    self.ProxyConfig_window.Raise()
                else:
                    self.ProxyConfig_window = ProxyConfig_window(parent = None,id = -1, title="Avo Assure Proxy Configuration")
            except Exception as e:
                msg = "Error while updating proxy configuration"
                logger.print_on_console(msg)
                log.info(msg)
                log.error(e)
        elif id==151:      # When user selects Tools > Generate PDF Report
            try:
                if (self.pluginPDF!= None) and (bool(self.pluginPDF) != False):
                    self.pluginPDF.Raise()
                    msg = 'Report PDF generation plugin is already active'
                else:
                    if pdfgentool is None:
                        #con = controller.Controller()
                        core_utils.get_all_the_imports('PdfReport')
                        import pdfReportGenerator as pdfgentool
                    msg = 'Initializing Report PDF generation plugin'
                    self.pluginPDF = pdfgentool.GeneratePDFReport("PDF Report Generator", pdfgentool.pdfkit_conf)
                logger.print_on_console(msg)
                log.info(msg)
            except Exception as e:
                msg = "Error while loading PDF generation plugin"
                logger.print_on_console(msg)
                log.info(msg)
                log.error(e)
        elif id==152:      # When user selects Tools > Generate PDF Report (Batch)
            try:
                if (self.pluginPDF!= None) and (bool(self.pluginPDF) != False):
                    msg = 'Report PDF generation plugin is already active'
                    self.pluginPDF.Raise()
                else:
                    if pdfgentool is None:
                        #con = controller.Controller()
                        core_utils.get_all_the_imports('PdfReport')
                        import pdfReportGenerator as pdfgentool
                    msg = 'Initializing Report PDF generation plugin (Batch mode)'
                    self.pluginPDF = pdfgentool.GeneratePDFReportBatch("PDF Report Generator - Batch Mode", pdfgentool.pdfkit_conf)
                logger.print_on_console(msg)
                log.info(msg)
            except Exception as e:
                msg = "Error while loading PDF generation plugin (Batch mode)"
                logger.print_on_console(msg)
                log.info(msg)
                log.error(e)

        elif id == 160:      # When user selects Edit > About
            try:
                log.info('--About selected--')
                if (self.aboutWindow):
                    self.aboutWindow.Raise()
                else:
                    self.aboutWindow = About_window(parent = None,id = -1, title="About")
            except Exception as e:
                msg = "Error while selecting about file"
                logger.print_on_console(msg)
                log.info(msg)
                log.error(e)
        elif id==161:      # When user selects Edit > Check for updates
            try:
                log.info('--Check for updates selected--')
                if (self.Check_Update_window):
                    self.Check_Update_window.Raise()
                else:
                    self.Check_Update_window = Check_Update_window(parent = None,id = -1, title="Check for Updates")
            except Exception as e:
                msg = "Error while updating file"
                logger.print_on_console(msg)
                log.info(msg)
                log.error(e)

        elif id==162:      # When user selects Edit > Rollback
            try:
                log.info('--Rollback selected--')
                if (self.rollback_window):
                    self.rollback_window.Raise()
                else:
                    self.rollback_window = rollback_window(parent = None,id = -1, title="Rollback")
            except Exception as e:
                msg = "Error while rolling back file"
                logger.print_on_console(msg)
                log.info(msg)
                log.error(e)

    def onChecked_Schedule(self, e):
        conn_time = float(configvalues['connection_timeout'])
        if conn_time >= 8:
            if (core.connection_Timer != None and core.connection_Timer.isAlive()):
                core.connection_Timer.cancel()
                log.info("Timer Restarted due to change in connection mode")
            else:
                log.info("Connection Timeout timer Started")
            core.connection_Timer = threading.Timer(conn_time*60*60, root.closeConnection)
            core.connection_Timer.start()
        mode=self.schedule.GetValue()
        msg = ("En" if mode else "Dis") + "abling Do Not Disturb mode"
        logger.print_on_console(msg)
        log.info(msg)
        core.set_ICE_status(one_time_ping = True)

    def onRadioBox(self,e):
        self.choice=self.rbox.GetStringSelection()
        logger.print_on_console(str(self.choice)+' is Selected')
        self.debug_mode=False
        if self.choice == 'Normal':
            self.breakpoint.Clear()
            self.breakpoint.Disable()
            self.killChildWindow(debug=True)
        elif self.choice in ['Stepwise','RunfromStep']:
            self.debug_mode=True
            ##if self.debugwindow == None:
            ##    self.debugwindow = DebugWindow(parent = None,id = -1, title="Debugger")
            if self.choice=='RunfromStep':
                self.breakpoint.Enable()
            else:
                self.breakpoint.Clear()
                self.breakpoint.Disable()

    def OnKillProcess(self, event):
        controller.kill_process()

    def OnTerminate(self, event, state=''):
        term_only = state != "term_exec"
        stat = self.killChildWindow(True,True,True,True)
        if stat[1]: core.socketIO.emit('scrape','Terminate')
        if term_only:
            msg = "---------Termination Started-------"
            if root.gui: benchmark.stop(True)
        else:
            controller.disconnect_flag=True
            print("")
            msg = "---------Terminating all active operations-------"
            if root.gui: benchmark.stop(False)
        logger.print_on_console(msg,color="YELLOW")
        log.info(msg)
        controller.terminate_flag=True
        controller.manual_terminate_flag=True
        #Calling AWS stop job on terminate (if present)
        try:
            root.testthread.con.aws_obj.stop_job()
        except:
            pass
        # Stop all SauceLabs jobs on click of terminate
        try:
            import script_generator
            scl_ops = script_generator.Sauce_Config()
            _ = scl_ops.get_sauceconf()
            sc = scl_ops.get_sauceclient()
            j = scl_ops.get_saucejobs(sc)
            all_jobs = j.get_jobs(full=None,limit=2)
            for i in range(0,len(all_jobs)):
                if all_jobs[i]['status'] == 'in progress': j.stop_job(all_jobs[i]['id'])
        except:
            pass
        #Handling the case where user clicks terminate when the execution is paused
        #Resume the execution
        if controller.pause_flag:
            controller.pause_flag=False
            root.testthread.resume(False)
        self.schedule.Enable()
        core.execution_flag = False
        core.set_ICE_status(one_time_ping = True, connect=term_only)

    def OnClear(self,event):
        self.log.Clear()
        root.print_banner()

    def OnNodeConnect(self,event):
        try:
            name = self.connectbutton.GetName()
            self.connectbutton.Disable()
            if(name == 'connect' or name == 'register'):
                root.connection(name)
            else:
                self.OnTerminate(event,"term_exec")
                root.connection(name)
                if self.connectbutton.GetName() != "register":
                    wx.CallAfter(self.enable_connect)
                wx.CallAfter(self.schedule.SetValue,False)
                wx.CallAfter(self.schedule.Disable)
                if SYSTEM_OS!='Linux':
                    wx.CallAfter(self.rollbackItem.Enable,False)
                    wx.CallAfter(self.updateItem.Enable,False)
        except:
            wx.CallAfter(self.cancelbutton.Disable)
            wx.CallAfter(self.terminatebutton.Disable)
            wx.CallAfter(self.clearbutton.Disable)
            wx.CallAfter(self.connectbutton.Enable)
            wx.CallAfter(self.rbox.Disable)

    def enable_connect(self, enable_button = True, repaint_title = True):
        self.connectbutton.SetBitmapLabel(self.connect_img)
        self.connectbutton.SetName('connect')
        self.connectbutton.SetToolTip(wx.ToolTip("Connect to Avo Assure Server"))
        if repaint_title: self.SetTitle(self.appName)
        if enable_button: self.connectbutton.Enable()

    def enable_disconnect(self, enable_button = True):
        self.connectbutton.SetBitmapLabel(self.disconnect_img)
        self.connectbutton.SetName('disconnect')
        self.connectbutton.SetToolTip(wx.ToolTip("Disconnect from Avo Assure Server"))
        if enable_button: self.connectbutton.Enable()

    def enable_register(self, enable_button = True, repaint_title = True):
        self.connectbutton.SetBitmapLabel(self.register_img)
        self.connectbutton.SetName("register")
        self.connectbutton.SetToolTip(wx.ToolTip("Register ICE with Avo Assure Server"))
        if repaint_title: self.SetTitle(self.appName)
        if enable_button: self.connectbutton.Enable()

    def killChildWindow(self, debug=False, scrape=False, display=False, pdf=False,register=False):
        #Close the debug window
        if register:
            root.token_obj.kill_window()
        stat = []
        flag=False
        if debug:
            try:
                if (self.debugwindow != None) and (bool(self.debugwindow) != False):
                    self.debugwindow.Destroy()
                    flag = True
                self.debugwindow = None
            except Exception as e:
                log.error("Error while closing debug window")
                log.error(e)
        stat.append(flag)

        #Close the scrape window
        flag=False
        if scrape:
            try:
                if (self.scrapewindow != None) and (bool(self.scrapewindow) != False):
                    if hasattr(self.scrapewindow, 'cropandaddobj') and self.scrapewindow.cropandaddobj != None:
                        self.scrapewindow.cropandaddobj.terminate_flag = True
                    self.scrapewindow.Destroy()
                    flag = True
                self.scrapewindow = None
            except Exception as e:
                log.error("Error while closing scrape window")
                log.error(e)
        stat.append(flag)

        #Close the pause/display window
        flag=False
        if display:
            try:
                if (self.pausewindow != None) and (bool(self.pausewindow) != False):
                    self.pausewindow.OnOk()
                    flag = True
                self.pausewindow = None
            except Exception as e:
                log.error("Error while closing pause window")
                log.error(e)
        stat.append(flag)

        #Close the PDF plugin window
        flag=False
        if pdf:
            try:
                if (self.pluginPDF != None) and (bool(self.pluginPDF) != False):
                    self.pluginPDF.OnClose()
                    flag = True
                self.pluginPDF = None
            except Exception as e:
                log.error("Error while unloading PDF plugin")
                log.error(e)
        stat.append(flag)
        return stat

    def test(self,event):
        root.debug_scrape()

    def DisableAll(self):
        self.enabledStatus = [self.connectbutton.IsEnabled(),self.schedule.IsEnabled(),
            self.rbox.IsEnabled(),self.cancelbutton.IsEnabled(),
            self.terminatebutton.IsEnabled(),self.clearbutton.IsEnabled()]
            # self.menubar.IsEnabledTop(0),self.menubar.IsEnabledTop(1)]
        self.connectbutton.Disable()
        self.schedule.Disable()
        self.rbox.Disable()
        self.cancelbutton.Disable()
        self.terminatebutton.Disable()
        self.clearbutton.Disable()
        # self.menubar.EnableTop(0,False) # Disable File Menu
        # self.menubar.EnableTop(1,False) # Disable Edit Menu

    def EnableAll(self):
        if self.enabledStatus[0]: self.connectbutton.Enable()
        if self.enabledStatus[1]: self.schedule.Enable()
        if self.enabledStatus[2]: self.rbox.Enable()
        if self.enabledStatus[3]: self.cancelbutton.Enable()
        if self.enabledStatus[4]: self.terminatebutton.Enable()
        if self.enabledStatus[5]: self.clearbutton.Enable()
        # if self.enabledStatus[6]: self.menubar.EnableTop(0,True)
        # if self.enabledStatus[7]: self.menubar.EnableTop(1,True)


"""Checks if config file is present, if not prompts the user to enter config file details"""
class Config_window(wx.Frame):

    """The design of the config window is defined in the _init_() method"""
    def __init__(self, parent,id, title):
        wxObject.DisableAll()
        #----------------------------------
        isConfigJson=self.readconfigJson()
        #----------------------------------

        #------------------------------------Different co-ordinates for Windows and Mac
        if SYSTEM_OS=='Windows':
            config_fields= {
            "Frame":[(300, 150),(470,670)],
            "S_address":[(12,12),(85, 25),(110,8),(140,-1)],
            "S_port": [(270,12),(70, 25),(340,8), (105,-1)],
            "Chrm_path":[(12,42),(80, 25),(110,38), (300,-1),(415,38),(30, -1)],
            "Chrm_profile":[(12,72),(80, 25),(110,68), (300,-1),(415,68),(30, -1)],
            "Chrm_extn_path":[(12,102),(80, 25),(110,98), (300,-1),(415,98),(30, -1)],
            "Ffox_path":[(12,132),(80, 25),(110,128), (300,-1),(415,128),(30, -1)],
            "Log_path":[(12,162),(80, 25),(110,158), (300,-1),(415,158),(30, -1)],
            "S_cert":[(12,192),(95, 25),(110,188),(300,-1),(415,188),(30, -1)],
            "Q_timeout":[(12,222),(85, 25),(110,218), (70,-1)],
            "Timeout":[(190,222),(50, 25),(250,218), (70,-1)],
            "Delay":[(333,222),(40, 25),(375,218), (70,-1)],
            "Step_exec":[(12,252),(110, 25),(135,248),(70,-1)],
            "global_waittimeout":[(12,312),(120, 25),(135,308),(70,-1)],
            "max_tries":[(222,312),(150, 25),(375,308), (70,-1)],
            "Disp_var": [(222, 252), (135, 25), (375, 248), (70, -1)],
            "C_Timeout" :[(12,282),(120, 25),(135,278), (70,-1)],
            "Delay_Stringinput":[(222,282),(130, 25),(375,278), (70,-1)],
            "panel1":[(12,345),(100,20),(440,185),(8, 365)],
            "err_text":[(50,555),(350, 25)],
            "Save":[(100,580), (100, 28)],
            "Close":[(250,580), (100, 28)]
            }
        elif SYSTEM_OS=='Darwin':
            config_fields={
            "Frame":[(300, 150),(600,670)],
            "S_address":[(12,12),(90,25),(116,8),(140,-1)],
            "S_port": [(352,12),(70,25),(430,8), (105,-1)],
            "Chrm_path":[(12,42),(80,25),(116,38),(382,-1),(504,38),(30, -1)],
            "Chrm_profile":[(12,72),(80,25),(116,68),(382,-1),(504,68),(30, -1)],
            "Chrm_extn_path":[(12,102),(80, 25),(110,98), (300,-1),(415,98),(30, -1)],
            "Ffox_path":[(12,132),(80,25),(116,128),(382,-1),(504,98),(30, -1)],
            "Log_path":[(12,162),(80, 25),(116,158),(382,-1),(504,128),(30, -1)],
            "S_cert":[(12,192),(85, 25),(116,188),(382,-1),(504,158),(30, -1)],
            "Q_timeout":[(12,222),(85, 25),(116,218), (80,-1)],
            "Timeout":[(225,222),(50, 25),(290,218),(80,-1)],
            "Delay":[(404,222),(40, 25),(448,218), (85,-1)],
            "Step_exec":[(12,252),(120, 25),(142,248),(80,-1)],
            "global_waittimeout":[(12,312),(120, 25),(180,308),(80,-1)],
            "max_tries":[(273,312),(150, 25),(450,308), (85,-1)],
            "Disp_var": [(273, 252), (135, 25), (450, 248), (85, -1)],
            "C_Timeout" :[(12,282),(120, 25),(180,278), (80,-1)],
            "Delay_Stringinput":[(273,282),(130, 25),(450,278), (85,-1)],
            "panel1":[(10,345),(100,20),(440,185),(8, 365)],
            "err_text":[(85,555),(350, 25)],
            "Save":[(130,580),(100, 28)],
            "Close":[(370,580),(120, 28)]
            }
        elif SYSTEM_OS=='Linux':
            # position size
            config_fields={
            "Frame":[(300, 150),(600,670)], 
            "S_address":[(12,12),(120,25),(150,8),(140,25)], 
            "S_port": [(320,11),(120,25),(434,8), (140,25)], 
            "Chrm_path":[(12,42),(120,25),(150,38),(370,25),(534,38),(40, 25)], 
            "Chrm_profile":[(12,72),(120,25),(150,68),(370,25),(534,68),(40, 25)], 
            "Chrm_extn_path":[(12,102),(120,25),(150,98), (370,25),(534,98),(40,25)],
            "Ffox_path":[(12,132),(120,25),(150,128),(370,25),(534,128),(40,25)],
            "Log_path":[(12,162),(120, 25),(150,158),(370,25),(534,158),(40,25)],
            "S_cert":[(12,192),(130, 25),(150,188),(370,25),(534,188),(40,25)],
            "Q_timeout":[(12,222),(115, 25),(150,218), (80,25)],
            "Timeout":[(235,222),(80, 25),(315,218),(80,25)],
            "Delay":[(404,222),(41, 25),(490,218), (85,25)],
            "Step_exec":[(12,252),(150, 25),(180,248),(80,25)],
            "Disp_var": [(273, 252), (-1, 25), (490, 248), (85, 25)],
            "C_Timeout" :[(12,282),(-1, 25),(180,278), (80,25)],
            "Delay_Stringinput":[(273,282),(-1, 25),(490,278), (85,25)],
            "global_waittimeout":[(12,312),(-1, 25),(180,308),(80,25)],
            "max_tries":[(273,312),(-1, 25),(490,308), (85,25)],
            "panel1":[(10,345),(100,20),(565,185),(12,365)],
            "err_text":[(85,555),(350, 25)],
            "Save":[(130,580),(100, 28)],
            "Close":[(370,580),(120, 28)]
            }
        

        wx.Frame.__init__(self, parent, title=title,
            pos=config_fields["Frame"][0], size=config_fields["Frame"][1],style = wx.CAPTION|wx.CLIP_CHILDREN)

        self.iconpath = IMAGES_PATH +"avo.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        self.updated = False
        self.panel = wx.Panel(self)

        #This is the panel which will have scrolling panel and which will contain the radiobuttons
        self.panel1 = wx.lib.scrolledpanel.ScrolledPanel(self.panel,-1,size=config_fields["panel1"][2], pos=config_fields["panel1"][3])
        self.panel1.SetupScrolling()

        self.sev_add=wx.StaticText(self.panel, label="Server Address", pos=config_fields["S_address"][0],size=config_fields["S_address"][1], style=0, name="")
        self.server_add=wx.TextCtrl(self.panel, pos=config_fields["S_address"][2], size=config_fields["S_address"][3])
        if isConfigJson!=False:
            self.server_add.SetValue(isConfigJson['server_ip'])

        self.sev_port=wx.StaticText(self.panel, label="Server Port", pos=config_fields["S_port"][0],size=config_fields["S_port"][1], style=0, name="")
        self.server_port=wx.TextCtrl(self.panel, pos=config_fields["S_port"][2], size=config_fields["S_port"][3])
        if isConfigJson!=False:
            self.server_port.SetValue(isConfigJson['server_port'])
        else:
            self.server_port.SetValue("8443")

        self.ch_path=wx.StaticText(self.panel, label="Chrome Path", pos=config_fields["Chrm_path"][0],size=config_fields["Chrm_path"][1], style=0, name="")
        self.chrome_path=wx.TextCtrl(self.panel, pos=config_fields["Chrm_path"][2], size=config_fields["Chrm_path"][3])
        self.chrome_path_btn=wx.Button(self.panel, label="...", pos=config_fields["Chrm_path"][4], size=config_fields["Chrm_path"][5])
        self.chrome_path_btn.Bind(wx.EVT_BUTTON, self.fileBrowser_chpath)
        if isConfigJson!=False:
            self.chrome_path.SetValue(isConfigJson['chrome_path'])
        else:
            self.chrome_path.SetValue('default')

        self.ch_profile=wx.StaticText(self.panel, label="Chrome Profile", pos=config_fields["Chrm_profile"][0],size=config_fields["Chrm_path"][1], style=0, name="")
        self.chrome_profile=wx.TextCtrl(self.panel, pos=config_fields["Chrm_profile"][2], size=config_fields["Chrm_profile"][3])
        self.chrome_profile_btn=wx.Button(self.panel, label="...", pos=config_fields["Chrm_profile"][4], size=config_fields["Chrm_profile"][5])
        self.chrome_profile_btn.Bind(wx.EVT_BUTTON, self.fileBrowser_chprofile)
        if isConfigJson!=False:
            self.chrome_profile.SetValue(isConfigJson['chrome_profile'])
        else:
            self.chrome_profile.SetValue('default')

        self.ch_extn_path=wx.StaticText(self.panel, label="Extension Path", pos=config_fields["Chrm_extn_path"][0],size=config_fields["Chrm_extn_path"][1], style=0, name="")
        self.chrome_extnpath=wx.TextCtrl(self.panel, pos=config_fields["Chrm_extn_path"][2], size=config_fields["Chrm_extn_path"][3])
        self.chrome_extnpath_btn=wx.Button(self.panel, label="+", pos=config_fields["Chrm_extn_path"][4], size=config_fields["Chrm_extn_path"][5])
        self.chrome_extnpath_btn.Bind(wx.EVT_BUTTON, self.fileBrowser_chextnpath)
        if isConfigJson!=False:
            self.chrome_extnpath.SetValue(isConfigJson['chrome_extnpath'])
        else:
            self.chrome_extnpath.SetValue('default')  

        if isConfigJson['clear_cache'] == 'Yes':
            self.chrome_profile.SetValue('default')
            self.chrome_profile.SetEditable(False)
            self.chrome_profile.SetBackgroundColour((211,211,211))

        self.ff_path=wx.StaticText(self.panel, label="Firefox Path", pos=config_fields["Ffox_path"][0],size=config_fields["Ffox_path"][1], style=0, name="")
        self.firefox_path=wx.TextCtrl(self.panel, pos=config_fields["Ffox_path"][2], size=config_fields["Ffox_path"][3])
        self.firefox_path_btn=wx.Button(self.panel, label="...", pos=config_fields["Ffox_path"][4], size=config_fields["Ffox_path"][5])
        self.firefox_path_btn.Bind(wx.EVT_BUTTON, self.fileBrowser_ffpath)
        if isConfigJson!=False:
            self.firefox_path.SetValue(isConfigJson['firefox_path'])
        else:
            self.firefox_path.SetValue('default')

        self.log_fpath=wx.StaticText(self.panel, label="Log File Path", pos=config_fields["Log_path"][0],size=config_fields["Log_path"][1], style=0, name="")
        self.log_file_path=wx.TextCtrl(self.panel, pos=config_fields["Log_path"][2], size=config_fields["Log_path"][3])
        self.log_file_path_btn=wx.Button(self.panel, label="...",pos=config_fields["Log_path"][4], size=config_fields["Log_path"][5])
        self.log_file_path_btn.Bind(wx.EVT_BUTTON, self.fileBrowser_logfilepath)
        if (not isConfigJson) or (isConfigJson and isConfigJson['logFile_Path']=='./logs/TestautoV2.log'):
            self.log_file_path.SetValue(os.path.normpath(AVO_ASSURE_HOME + '/logs/TestautoV2.log'))
        else:
            self.log_file_path.SetValue(isConfigJson['logFile_Path'])

        self.sev_cert=wx.StaticText(self.panel, label="Server Certificate", pos=config_fields["S_cert"][0],size=config_fields["S_cert"][1], style=0, name="")
        self.server_cert=wx.TextCtrl(self.panel, pos=config_fields["S_cert"][2], size=config_fields["S_cert"][3])
        self.server_cert_btn=wx.Button(self.panel, label="...",pos=config_fields["S_cert"][4], size=config_fields["S_cert"][5])
        self.server_cert_btn.Bind(wx.EVT_BUTTON, self.fileBrowser_servcert)
        if (not isConfigJson) or (isConfigJson and isConfigJson['server_cert']=='./assets/CA_BUNDLE/server.crt'):
            self.server_cert.SetValue(os.path.normpath(CERTIFICATE_PATH + '/server.crt'))
        else:
            self.server_cert.SetValue(isConfigJson['server_cert'])

        font_italic = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
        self.qu_timeout=wx.StaticText(self.panel, label="Query Timeout", pos=config_fields["Q_timeout"][0],size=config_fields["Q_timeout"][1], style=0, name="")
        self.query_timeout=wx.TextCtrl(self.panel, pos=config_fields["Q_timeout"][2], size=config_fields["Q_timeout"][3])
        if isConfigJson['queryTimeOut']=="":
            self.query_timeout.SetValue("sec")
            self.query_timeout.SetFont(font_italic)
            self.query_timeout.SetForegroundColour('#848484')
        elif isConfigJson!=False:
            self.query_timeout.SetValue(isConfigJson['queryTimeOut'])
        else:
            self.query_timeout.SetValue("3")

        self.timeOut=wx.StaticText(self.panel, label="Time Out", pos=config_fields["Timeout"][0],size=config_fields["Timeout"][1], style=0, name="")
        self.time_out=wx.TextCtrl(self.panel, pos=config_fields["Timeout"][2], size=config_fields["Timeout"][3])
        if isConfigJson['timeOut']=="":
            self.time_out.SetValue("sec")
            self.time_out.SetFont(font_italic)
            self.time_out.SetForegroundColour('#848484')
        elif isConfigJson!=False:
            self.time_out.SetValue(isConfigJson['timeOut'])
        else:
            self.time_out.SetValue("1")

        self.globalWait_TimeOut=wx.StaticText(self.panel, label="Global Wait Time Out", pos=config_fields["global_waittimeout"][0],size=config_fields["global_waittimeout"][1], style=0, name="")
        self.globalWait_TO=wx.TextCtrl(self.panel, pos=config_fields["global_waittimeout"][2], size=config_fields["global_waittimeout"][3])
        if isConfigJson['globalWaitTimeOut']=="":
            self.globalWait_TO.SetValue("sec")
            self.globalWait_TO.SetFont(font_italic)
            self.globalWait_TO.SetForegroundColour('#848484')
        elif isConfigJson!=False:
            self.globalWait_TO.SetValue(isConfigJson['globalWaitTimeOut'])
        else:
            self.globalWait_TO.SetValue("0")

        self.delayText=wx.StaticText(self.panel, label="Delay", pos=config_fields["Delay"][0],size=config_fields["Delay"][1], style=0, name="")
        self.delay=wx.TextCtrl(self.panel, pos=config_fields["Delay"][2], size=config_fields["Delay"][3])
        if isConfigJson['delay']=="":
            self.delay.SetValue("sec")
            self.delay.SetFont(font_italic)
            self.delay.SetForegroundColour('#848484')
        elif isConfigJson!=False:
            self.delay.SetValue(isConfigJson['delay'])
        else:
            self.delay.SetValue("0.3")

        self.stepExecWait=wx.StaticText(self.panel, label="Step Execution Wait", pos=config_fields["Step_exec"][0],size=config_fields["Step_exec"][1], style=0, name="")
        self.step_exe_wait=wx.TextCtrl(self.panel, pos=config_fields["Step_exec"][2], size=config_fields["Step_exec"][3])
        if isConfigJson['stepExecutionWait']=="":
            self.step_exe_wait.SetValue("sec")
            self.step_exe_wait.SetFont(font_italic)
            self.step_exe_wait.SetForegroundColour('#848484')
        elif isConfigJson!=False:
            self.step_exe_wait.SetValue(isConfigJson['stepExecutionWait'])
        else:
            self.step_exe_wait.SetValue("1")

        self.dispVarTimeOut=wx.StaticText(self.panel, label="Display Variable Timeout", pos=config_fields["Disp_var"][0],size=config_fields["Disp_var"][1], style=0, name="")
        self.disp_var_timeout=wx.TextCtrl(self.panel, pos=config_fields["Disp_var"][2], size=config_fields["Disp_var"][3])
        if isConfigJson['displayVariableTimeOut']=="":
            self.disp_var_timeout.SetValue("sec")
            self.disp_var_timeout.SetFont(font_italic)
            self.disp_var_timeout.SetForegroundColour('#848484')
        else:
            self.disp_var_timeout.SetValue(isConfigJson['displayVariableTimeOut'])

        self.connection_timeout=wx.StaticText(self.panel, label="Connection Timeout", pos=config_fields["C_Timeout"][0],size=config_fields["C_Timeout"][1], style=0, name="")
        self.conn_timeout=wx.TextCtrl(self.panel, id=9, pos=config_fields["C_Timeout"][2], size=config_fields["C_Timeout"][3])
        if isConfigJson!=False and int(isConfigJson['connection_timeout'])>=8:
            self.conn_timeout.SetValue(isConfigJson['connection_timeout'])
        else:
            self.conn_timeout.SetValue("0")
        # Max Retries for App Launch config value
        self.max_retries=wx.StaticText(self.panel, label="Max Retries for App Launch", pos=config_fields["max_tries"][0],size=config_fields["max_tries"][1], style=0, name="")
        self.max_launch_retries = wx.TextCtrl(self.panel, pos=config_fields["max_tries"][2], size=config_fields["max_tries"][3])
        if isConfigJson['displayVariableTimeOut']=="":
            self.max_launch_retries.SetValue("sec")
            self.max_launch_retries.SetFont(font_italic)
            self.max_launch_retries.SetForegroundColour('#848484')
        else:
            self.max_launch_retries.SetValue(isConfigJson['max_retries_app_launch'])
            

        #Delay input box kept for provide the delay in typestring.
        self.delay_stringinput=wx.StaticText(self.panel, label="Delay for String Input", pos=config_fields["Delay_Stringinput"][0],size=config_fields["Delay_Stringinput"][1], style=0, name="")
        self.Delay_input=wx.TextCtrl(self.panel, pos=config_fields["Delay_Stringinput"][2], size=config_fields["Delay_Stringinput"][3])
        if isConfigJson['delay_stringinput']=="":
            self.Delay_input.SetValue("sec")
            self.Delay_input.SetFont(font_italic)
            self.Delay_input.SetForegroundColour('#848484')
        elif isConfigJson!=False:
            self.Delay_input.SetValue(isConfigJson['delay_stringinput'])
        else:
            self.Delay_input.SetValue("0.005")

        self.config_param=wx.StaticText(self.panel,label="Config Parameters",pos=config_fields["panel1"][0],size=config_fields["panel1"][1], style=0, name="")
        font = wx.Font(9, wx.DEFAULT, wx.ITALIC, wx.BOLD)
        self.config_param.SetFont(font)

        #ToolTips for static texts boxes
        self.sev_add.SetToolTip(wx.ToolTip("Server Address"))
        self.sev_port.SetToolTip(wx.ToolTip("Server Port"))
        self.ch_path.SetToolTip(wx.ToolTip("Chrome installation path or default"))
        self.ch_profile.SetToolTip(wx.ToolTip("Chrome profile path or default"))
        self.ff_path.SetToolTip(wx.ToolTip("Firefox installation path or default"))
        self.log_fpath.SetToolTip(wx.ToolTip(" ICE Log file path"))
        self.sev_cert.SetToolTip(wx.ToolTip("Server certificate file path or default"))
        self.qu_timeout.SetToolTip(wx.ToolTip("Timeout for database queries"))
        self.timeOut.SetToolTip(wx.ToolTip("Timeout for waitForElementVisible[in seconds]"))
        self.delayText.SetToolTip(wx.ToolTip("Delay to switch between browser tabs[seconds]"))
        self.stepExecWait.SetToolTip(wx.ToolTip("Delay between each step[in seconds]"))
        self.dispVarTimeOut.SetToolTip(wx.ToolTip("displayVariable popup duration[in seconds]"))
        self.connection_timeout.SetToolTip(wx.ToolTip("Timeout from server [in hours 0 or >8]"))
        self.delay_stringinput.SetToolTip(wx.ToolTip("Character input delay for sendFunctionKeys"))
        self.globalWait_TimeOut.SetToolTip(wx.ToolTip("Timeout to wait for all objects to visible in AUT [in seconds]"))
        self.ch_extn_path.SetToolTip(wx.ToolTip("Chrome/Chromium extension path or default"))
        self.max_retries.SetToolTip(wx.ToolTip("Maximum retries to launch PDF Reader for normalizePDF keyword"))

        ## Binding placeholders and restricting textareas to just numeric characters
        self.server_port.Bind(wx.EVT_CHAR, self.handle_keypress)
        self.disp_var_timeout.Bind(wx.EVT_SET_FOCUS,self.toggle1_generic)
        self.disp_var_timeout.Bind(wx.EVT_KILL_FOCUS,self.toggle2_generic)
        self.disp_var_timeout.Bind(wx.EVT_CHAR, self.handle_keypress)

        self.max_launch_retries.Bind(wx.EVT_SET_FOCUS,self.toggle1_generic)
        self.max_launch_retries.Bind(wx.EVT_KILL_FOCUS,self.toggle2_generic)
        self.max_launch_retries.Bind(wx.EVT_CHAR, self.handle_keypress)

        self.query_timeout.Bind(wx.EVT_SET_FOCUS,self.toggle1_generic)
        self.query_timeout.Bind(wx.EVT_KILL_FOCUS,self.toggle2_generic)
        self.query_timeout.Bind(wx.EVT_CHAR, self.handle_keypress)

        self.time_out.Bind(wx.EVT_SET_FOCUS,self.toggle1_generic)
        self.time_out.Bind(wx.EVT_KILL_FOCUS,self.toggle2_generic)
        self.time_out.Bind(wx.EVT_CHAR, self.handle_keypress)

        self.globalWait_TO.Bind(wx.EVT_SET_FOCUS,self.toggle1_generic)
        self.globalWait_TO.Bind(wx.EVT_KILL_FOCUS,self.toggle2_generic)
        self.globalWait_TO.Bind(wx.EVT_CHAR, self.handle_keypress)

        self.delay.Bind(wx.EVT_SET_FOCUS,self.toggle1_generic)
        self.delay.Bind(wx.EVT_KILL_FOCUS,self.toggle2_generic)
        self.delay.Bind(wx.EVT_CHAR, self.handle_keypress)

        self.Delay_input.Bind(wx.EVT_SET_FOCUS,self.toggle1_generic)
        self.Delay_input.Bind(wx.EVT_KILL_FOCUS,self.toggle2_generic)
        self.Delay_input.Bind(wx.EVT_CHAR, self.handle_keypress)

        self.step_exe_wait.Bind(wx.EVT_SET_FOCUS,self.toggle1_generic)
        self.step_exe_wait.Bind(wx.EVT_KILL_FOCUS,self.toggle2_generic)
        self.step_exe_wait.Bind(wx.EVT_CHAR, self.handle_keypress)

        self.conn_timeout.Bind(wx.EVT_SET_FOCUS,self.toggle1_generic)
        self.conn_timeout.Bind(wx.EVT_KILL_FOCUS,self.toggle2_generic)
        self.conn_timeout.Bind(wx.EVT_CHAR, self.handle_keypress)

        lblList = ['Yes', 'No']
        lblList2 = ['64-bit', '32-bit']
        lblList3 = ['All', 'Fail']
        lblList4 = ['False', 'True']
        lblList5 = ['High', 'Med', 'Low']
        self.bSizer = wx.BoxSizer( wx.VERTICAL )

        self.rbox9 = wx.RadioBox(self.panel1, label = 'TLS Security Level', choices = lblList5,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False:
            tls_level_val = isConfigJson['tls_security'].title()
            if tls_level_val == lblList5[1]:
                self.rbox9.SetSelection(1)
            elif tls_level_val == lblList5[2]:
                self.rbox9.SetSelection(2)
            else:
                self.rbox9.SetSelection(0)
        else:
            self.rbox9.SetSelection(0)
        self.rbox9.SetToolTip(wx.ToolTip("Gives the user an option to bypass TLS certificate verification and/or" +
            " hostname verification of Avo Assure in case of unavailability of a valid certificate." +
            "\nHigh: Enforce TLS Certificate and Hostname Verification\nMed: Enforce TLS Certificate and" +
            " Disable Hostname Verification\nLow: Disable TLS Certificate and Hostname Verification"))

        self.rbox1 = wx.RadioBox(self.panel1, label = 'Ignore AUT Certificate', choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        self.rbox1.SetToolTip(wx.ToolTip("Indicates if the errors of the AUT website's security certificates are to be ignored or not. It is applicable only for IE"))
        if isConfigJson!=False and isConfigJson['ignore_certificate'].title()==lblList[0]:
            self.rbox1.SetSelection(0)
        else:
            self.rbox1.SetSelection(1)

        self.rbox2 = wx.RadioBox(self.panel1, label = 'IE Architecture Type', choices = lblList2,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['bit_64'].title() != 'Yes':
            self.rbox2.SetSelection(1)
        else:
            self.rbox2.SetSelection(0)
        self.rbox2.SetToolTip(wx.ToolTip("Checks if the Client machine is a 64-bit machine or 32-bit"))

        self.rbox5 = wx.RadioBox(self.panel1, label = 'Exception Flag',choices = lblList4,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['exception_flag'].title()!=lblList4[0]:
            self.rbox5.SetSelection(1)
        else:
            self.rbox5.SetSelection(0)
        self.rbox5.SetToolTip(wx.ToolTip("Determines whether to terminate the scenario and continue execution from the next scenario in the Test Suite or to continue executing the next step in case of the error (Object is not found)"))

        self.rbox6 = wx.RadioBox(self.panel1, label = 'Ignore Visibility Check',  choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['ignoreVisibilityCheck'].title()==lblList[0]:
            self.rbox6.SetSelection(0)
        else:
            self.rbox6.SetSelection(1)
        self.rbox6.SetToolTip(wx.ToolTip("Checks the visibility of the element during execution and is applicable only for Web Applications"))

        self.rbox3 = wx.RadioBox(self.panel1, label = 'ScreenShot Flag', choices = lblList3,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['screenShot_Flag'].title()!=lblList3[0]:
            self.rbox3.SetSelection(1)
        else:
            self.rbox3.SetSelection(0)
        self.rbox3.SetToolTip(wx.ToolTip("Facilitates capturing the screenshots of the test steps based on its value"))

        self.rbox4 = wx.RadioBox(self.panel1, label = 'HTTP Status Code Check', choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['httpStatusCode'].title()!=lblList[0]:
            self.rbox4.SetSelection(1)
        else:
            self.rbox4.SetSelection(0)
        self.rbox4.SetToolTip(wx.ToolTip("Determines whether to continue to debug/execute or stop in case of AUT website status code errors like 400, 401, 404, 500 et al. It is applicable only for Web Applications. "))

        self.rbox8 = wx.RadioBox(self.panel1, label ='Browser Check', choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['browser_check'].title()!=lblList[0]:
            self.rbox8.SetSelection(1)
        else:
            self.rbox8.SetSelection(0)
        self.rbox8.SetToolTip(wx.ToolTip("Enables or disables Browser Compatibility check based on the selection."))

        self.rbox7 = wx.RadioBox(self.panel1, label = 'Enable Security Check', choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['enableSecurityCheck'].title()==lblList[0]:
            self.rbox7.SetSelection(0)
        else:
            self.rbox7.SetSelection(1)
        self.rbox7.SetToolTip(wx.ToolTip("Provides an option for the IE browser to set all the security zones to the same level while executing the openBrowser keywords. It is applicable only when automating Web Applications in IE browser"))

        self.rbox10 = wx.RadioBox(self.panel1, label = 'Highlight Check', choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['highlight_check'].title()==lblList[0]:
            self.rbox10.SetSelection(0)
        else:
            self.rbox10.SetSelection(1)
        self.rbox10.SetToolTip(wx.ToolTip("When the user verifies the existence of an element using the verifyExists keyword, the radio button for Highlight Check highlights the element (or not) based on the selection. It is applicable only for the verifyExists keyword"))

        self.rbox11 = wx.RadioBox(self.panel1, label = 'Prediction for IRIS Objects', choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['prediction_for_iris_objects'].title()==lblList[0]:
            self.rbox11.SetSelection(0)
        else:
            self.rbox11.SetSelection(1)
        self.rbox11.SetToolTip(wx.ToolTip("Enables or disables IRIS prediction based on its value"))

        self.rbox12 = wx.RadioBox(self.panel1, label = "Hide Soft. Keyboard", choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['hide_soft_key'].title() == lblList[0]:
            self.rbox12.SetSelection(0)
        else:
            self.rbox12.SetSelection(1)
        self.rbox12.SetToolTip(wx.ToolTip('Indicates if the keypad, in Android devices, shows or not. It is applicable only for Android-based applications'))

        self.rbox13 = wx.RadioBox(self.panel1, label = "Extension Enable", choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['extn_enabled'].title() == lblList[0]:
            self.rbox13.SetSelection(0)
        else:
            self.rbox13.SetSelection(1)
        self.rbox13.SetToolTip(wx.ToolTip("Enables browser extension for Advanced debug mode."))

        self.rbox14 = wx.RadioBox(self.panel1, label = "Update Check", choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['update_check'].title() == lblList[0]:
            self.rbox14.SetSelection(0)
        else:
            self.rbox14.SetSelection(1)
        self.rbox14.SetToolTip(wx.ToolTip("Checks for the availability of ICE updates"))

        self.rbox15 = wx.RadioBox(self.panel1, label = "Headless Mode", choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['headless_mode'].title() == lblList[0]:
            self.rbox15.SetSelection(0)
            self.headlessOldVal = "Yes"
        else:
            self.rbox15.SetSelection(1)
            self.headlessOldVal = "No"
        self.rbox15.SetToolTip(wx.ToolTip("Enables or disables Headless execution mode for Browser"))

        #adding the radio button for clear cache:
        self.rbox16 = wx.RadioBox(self.panel1, label = "Clear Cache", choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['clear_cache'].title() == lblList[0]:
            self.rbox16.SetSelection(0)
        else:
            self.rbox16.SetSelection(1)
        self.rbox16.SetToolTip(wx.ToolTip("Enables or disables Clear Cache"))
        self.rbox16.Bind(wx.EVT_RADIOBOX, self.OnClearCache)

        #adding the radio button for Screen Recording:
        self.rbox17 = wx.RadioBox(self.panel1, label = "Screen Recording", choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['screen_rec'].title() == lblList[0]:
            self.rbox17.SetSelection(0)
        else:
            self.rbox17.SetSelection(1)
        self.rbox17.SetToolTip(wx.ToolTip("Enables or disables Screen Recording"))

        #adding the radio button for fullscreenshot for scrapping:
        self.rbox18 = wx.RadioBox(self.panel1, label = "Full Screenshot", choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['full_screenshot'].title() == lblList[0]:
            self.rbox18.SetSelection(0)
        else:
            self.rbox18.SetSelection(1)
        self.rbox18.SetToolTip(wx.ToolTip("Enables or disables Full Screenshot"))


        #adding the radio button for disabling popup in browser:
        self.rbox19 = wx.RadioBox(self.panel1, label = "Close Browser Popup", choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['close_browser_popup'].title() == lblList[0]:
            self.rbox19.SetSelection(0)
        else:
            self.rbox19.SetSelection(1)
        self.rbox19.SetToolTip(wx.ToolTip("Enables or disables popup for Browser"))

        # Adding the radio button for enabling use of remote debugging port for browsers.
        # This is needed for DevToolsActivePort file doesn't exist error
        self.rbox20 = wx.RadioBox(self.panel1, label = "Use Custom Debug Port", choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['use_custom_debugport'].title() == lblList[0]:
            self.rbox20.SetSelection(0)
        else:
            self.rbox20.SetSelection(1)
        self.rbox20.SetToolTip(wx.ToolTip("Enables or disables use of remote debugging port for browsers"))

        self.rbox21 = wx.RadioBox(self.panel1, label = "Disable Screen Timeout", choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        is_admin = core_utils.check_isadmin()
        if isConfigJson!=False:
            if is_admin:
                log.info("ICE is run as admin")
                dis_sys_screenoff = isConfigJson['disable_screen_timeout'].title()
                if dis_sys_screenoff == lblList[0]:
                    self.rbox21.SetSelection(0)
                elif dis_sys_screenoff == lblList[1]:
                    self.rbox21.SetSelection(1)
            else:
                log.info("ICE is run as normal")
                self.rbox21.SetSelection(1)
        else:
            self.rbox21.SetSelection(1)           
        self.rbox21.SetToolTip(wx.ToolTip("Enables or Disables automatic screen lock during execution when ICE is run as admin."))

        #adding the radio button for opening browser in incognito/private mode:
        self.rbox22 = wx.RadioBox(self.panel1, label = "Incognito/Private Mode", choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['incognito_private_mode'].title() == lblList[0]:
            self.rbox22.SetSelection(0)
        else:
            self.rbox22.SetSelection(1)
        self.rbox22.SetToolTip(wx.ToolTip("Enables or disables incognito/private mode for Browser"))

        self.rbox23 = wx.RadioBox(self.panel1, label = "Kill Stale Process", choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['kill_stale'].title() == lblList[0]:
            self.rbox23.SetSelection(0)
        else:
            self.rbox23.SetSelection(1)
        self.rbox23.SetToolTip(wx.ToolTip("Kills stale processes before start of every execution"))

        self.rbox24 = wx.RadioBox(self.panel1, label = "Browser Screenshots", choices = lblList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['browser_screenshots'].title() == lblList[0]:
            self.rbox24.SetSelection(0)
        else:
            self.rbox24.SetSelection(1)
        self.rbox24.SetToolTip(wx.ToolTip("Captures screenshots using Browser's driver instance"))

        #Adding GridSizer which will show the radio buttons into grid of 12 rows and 2 colums it can be changed based on the requirements
        self.gs=wx.GridSizer(12,2,5,5)
        self.gs.AddMany([(self.rbox9,0,wx.EXPAND), (self.rbox1,0,wx.EXPAND), (self.rbox2,0,wx.EXPAND),
            (self.rbox5,0,wx.EXPAND), (self.rbox6,0,wx.EXPAND), (self.rbox3,0,wx.EXPAND),
            (self.rbox4,0,wx.EXPAND), (self.rbox8,0,wx.EXPAND), (self.rbox7,0,wx.EXPAND),
            (self.rbox10,0,wx.EXPAND), (self.rbox11,0,wx.EXPAND), (self.rbox12,0,wx.EXPAND),
            (self.rbox13,0,wx.EXPAND), (self.rbox14,0,wx.EXPAND), (self.rbox15,0,wx.EXPAND),
            (self.rbox16,0,wx.EXPAND), (self.rbox17,0,wx.EXPAND), (self.rbox18,0,wx.EXPAND),
            (self.rbox19,0,wx.EXPAND), (self.rbox20,0,wx.EXPAND), (self.rbox21,0,wx.EXPAND),
            (self.rbox22,0,wx.EXPAND), (self.rbox23,0,wx.EXPAND), (self.rbox24,0,wx.EXPAND)])

        #adding  GridSizer to bSizer which is a box sizer
        self.bSizer.Add(self.gs, 1, wx.EXPAND | wx.TOP, 5)
        #now setting that boxsizer to our panel1
        self.panel1.SetSizer(self.bSizer)

        self.error_msg=wx.StaticText(self.panel, label="", pos=config_fields["err_text"][0],size=config_fields["err_text"][1], style=wx.ALIGN_CENTRE, name="")
        self.save_btn=wx.Button(self.panel, label="Save",pos=config_fields["Save"][0], size=config_fields["Save"][1])
        self.save_btn.Bind(wx.EVT_BUTTON, self.config_check)
        self.close_btn=wx.Button(self.panel, label="Close",pos=config_fields["Close"][0], size=config_fields["Close"][1])
        self.close_btn.Bind(wx.EVT_BUTTON, self.close)
        self.Bind(wx.EVT_CLOSE, self.close)

        if wxObject.connectbutton.GetName().lower() == "disconnect":
            self.sev_add.Enable(False)
            self.server_add.Enable(False)
            self.sev_port.Enable(False)
            self.server_port.Enable(False)
            self.sev_cert.Enable(False)
            self.server_cert.Enable(False)
            self.server_cert_btn.Enable(False)
            self.rbox9.Enable(False)
        
        if not(is_admin):
            self.rbox21.Enable(False)

        self.Centre()
        wx.Frame(self.panel)
        self.Show()

    """ Allows only integer and float values + directional keys"""
    def handle_keypress(self, event):
        if chr(event.GetKeyCode()) in '0123456789.\x08\x09ĺĽĻļĹĸŷŸŹźŻž\x7f': event.Skip()

    def toggle1_generic(self,evt):
        self.demo=evt.EventObject
        if (self.demo.Id == 9 and self.demo.GetValue()=="0 or >=8 hrs") or self.demo.GetValue()=="sec":
            self.demo.SetValue("")
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
            self.demo.SetFont(font)
            self.demo.SetForegroundColour('#000000')
        evt.Skip()

    def toggle2_generic(self,evt):
        self.demo=evt.EventObject
        if self.demo.GetValue() == "":
            if self.demo.Id == 9: self.demo.SetValue("0 or >=8 hrs")
            else: self.demo.SetValue("sec")
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.demo.SetFont(font)
            self.demo.SetForegroundColour('#848484')
        evt.Skip()

    def OnClearCache(self,event):
        if self.rbox16.GetStringSelection()=='Yes':
            self.chrome_profile.SetValue('default')
            self.chrome_profile.SetEditable(False)
            self.chrome_profile_btn.Disable()
            self.chrome_profile.SetBackgroundColour((211,211,211))
        else:
            self.chrome_profile.SetEditable(False)
            self.chrome_profile.SetBackgroundColour((255,255,255))
            self.chrome_profile_btn.Enable()

    """This method verifies and checks if correct data is present,then creates a dictionary and sends this dictionary to jsonCreater()"""
    def config_check(self,event):
        data = {}
        config_data={}
        ignore_certificate=self.rbox1.GetStringSelection()
        bit_64=self.rbox2.GetStringSelection()
        screenShot_Flag=self.rbox3.GetStringSelection()
        httpStatusCode=self.rbox4.GetStringSelection()
        exception_flag=self.rbox5.GetStringSelection()
        ignoreVisibilityCheck=self.rbox6.GetStringSelection()
        enableSecurityCheck=self.rbox7.GetStringSelection()
        server_add=self.server_add.GetValue()
        server_port=self.server_port.GetValue()
        chrome_path=self.chrome_path.GetValue()
        chrome_profile=self.chrome_profile.GetValue()
        chrome_extnpath=self.chrome_extnpath.GetValue()
        firefox_path=self.firefox_path.GetValue()
        logFile_Path=self.log_file_path.GetValue()
        queryTimeOut=self.query_timeout.GetValue()
        time_out=self.time_out.GetValue()
        globalWait_TO=self.globalWait_TO.GetValue()
        delay=self.delay.GetValue()
        stepExecutionWait=self.step_exe_wait.GetValue()
        displayVariableTimeOut=self.disp_var_timeout.GetValue()
        max_retries_app_launch=self.max_launch_retries.GetValue()
        server_cert=self.server_cert.GetValue()
        browser_check=self.rbox8.GetStringSelection()
        tls_security=self.rbox9.GetStringSelection()
        highlight_check=self.rbox10.GetStringSelection()
        iris_prediction = self.rbox11.GetStringSelection()
        hide_soft_key = self.rbox12.GetStringSelection()
        conn_timeout = self.conn_timeout.GetValue()
        extn_enabled = self.rbox13.GetStringSelection()
        update_check = self.rbox14.GetStringSelection()
        headless_mode = self.rbox15.GetStringSelection()
        delay_string_in = self.Delay_input.GetValue()
        clear_cache = self.rbox16.GetStringSelection()
        screen_rec = self.rbox17.GetStringSelection()
        full_screenshot = self.rbox18.GetStringSelection()
        close_browser_popup = self.rbox19.GetStringSelection()
        use_custom_debugport = self.rbox20.GetStringSelection()
        disable_screen_timeout = self.rbox21.GetStringSelection()
        incognito_private_mode = self.rbox22.GetStringSelection()
        kill_stale = self.rbox23.GetStringSelection()
        browser_screenshots = self.rbox24.GetStringSelection()
        if extn_enabled == 'Yes' and headless_mode == 'Yes':
            self.error_msg.SetLabel("Extension Enable must be disabled when Headless Mode is enabled")
            self.error_msg.SetForegroundColour((255,0,0))
            return
        #----------------creating data dictionary
        data['server_ip'] = server_add.strip()
        data['server_port'] = server_port.strip()
        data['ignore_certificate'] = ignore_certificate.strip()
        data['chrome_path'] = chrome_path.strip() if chrome_path.strip().lower()!='default' else 'default'
        data['chrome_profile'] = chrome_profile.strip() if chrome_profile.strip().lower()!='default' else 'default'
        data['chrome_extnpath'] = chrome_extnpath.strip() if chrome_extnpath.strip().lower()!='default' else 'default'
        data['firefox_path'] = firefox_path.strip() if firefox_path.strip().lower()!='default' else 'default'
        data['bit_64'] = 'Yes' if bit_64.strip()=='64-bit' else 'No'
        data['logFile_Path'] = logFile_Path.strip()
        data['screenShot_Flag'] = screenShot_Flag.strip()
        data['queryTimeOut'] = queryTimeOut.strip()
        data['timeOut'] = time_out.strip()
        data['globalWaitTimeOut'] = globalWait_TO.strip()
        data['stepExecutionWait'] = stepExecutionWait.strip()
        data['displayVariableTimeOut'] = displayVariableTimeOut.strip()
        data['max_retries_app_launch'] = max_retries_app_launch.strip()
        data['httpStatusCode'] = httpStatusCode.strip()
        data['delay'] = delay.strip()
        data['ignoreVisibilityCheck'] = ignoreVisibilityCheck.strip()
        data['enableSecurityCheck'] = enableSecurityCheck.strip()
        data['exception_flag'] = exception_flag.strip().lower()
        data['server_cert'] =server_cert.strip()
        data['browser_check']=browser_check.strip()
        data['tls_security'] = tls_security.strip()
        data['highlight_check'] = highlight_check.strip()
        data['prediction_for_iris_objects'] = iris_prediction.strip()
        data['hide_soft_key'] = hide_soft_key.strip()
        data['connection_timeout']= conn_timeout.strip()
        data['extn_enabled']= extn_enabled.strip()
        data['update_check']= update_check.strip()
        data['headless_mode']=headless_mode.strip()
        data['delay_stringinput']=delay_string_in.strip()
        data['clear_cache']=clear_cache.strip()
        data['screen_rec']=screen_rec.strip()
        data['full_screenshot']=full_screenshot.strip()
        data['close_browser_popup']=close_browser_popup.strip()
        data['use_custom_debugport']=use_custom_debugport.strip()
        data['disable_screen_timeout']=disable_screen_timeout.strip()
        data['incognito_private_mode']=incognito_private_mode.strip()
        data['kill_stale']=kill_stale.strip()
        data['browser_screenshots']=browser_screenshots.strip()
        data['file_server_ip']=readconfig.configvalues["file_server_ip"]
        data['ice_Token']=readconfig.configvalues['ice_Token']
        data['sample_application_urls']=readconfig.configvalues['sample_application_urls']
        data['isTrial']=readconfig.configvalues['isTrial']
        data['element_load_timeout']=readconfig.configvalues['element_load_timeout']
        config_data=data
        if (data['server_ip']!='' and data['server_port']!='' and data['server_cert']!='' and
            data['chrome_path']!='' and data['queryTimeOut'] not in ['','sec'] and data['logFile_Path']!='' and
            data['delay'] not in ['','sec'] and data['timeOut'] not in ['','sec'] and data['stepExecutionWait'] not in ['','sec'] and
            data['displayVariableTimeOut'] not in ['','sec'] and data['delay_stringinput'] not in ['','sec'] and
            data['firefox_path']!='' and data['connection_timeout'] not in ['','0 or >=8 hrs'] and data['chrome_profile']!='' and
            data['chrome_extnpath']!='' and data['max_retries_app_launch'] not in ['','sec']):
            #---------------------------------------resetting the static texts
            self.error_msg.SetLabel("")
            self.sev_add.SetLabel('Server Address')
            self.sev_add.SetForegroundColour((0,0,0))
            self.sev_port.SetLabel('Server Port')
            self.sev_port.SetForegroundColour((0,0,0))
            self.log_fpath.SetLabel('Log File Path')
            self.log_fpath.SetForegroundColour((0,0,0))
            self.qu_timeout.SetLabel('Query Timeout')
            self.qu_timeout.SetForegroundColour((0,0,0))
            self.sev_cert.SetLabel('Server Certificate')
            self.sev_cert.SetForegroundColour((0,0,0))
            self.ch_path.SetLabel('Chrome Path')
            self.ch_path.SetForegroundColour((0,0,0))
            self.ff_path.SetLabel('Firefox Path')
            self.ff_path.SetForegroundColour((0,0,0))
            self.ch_profile.SetLabel('Chrome Profile')
            self.ch_profile.SetForegroundColour((0,0,0))
            self.ch_extn_path.SetLabel('Chrome Extn')
            self.ch_extn_path.SetForegroundColour((0,0,0))
            self.delayText.SetLabel('Delay')
            self.delayText.SetForegroundColour((0,0,0))
            self.timeOut.SetLabel('Time Out')
            self.globalWait_TimeOut.SetLabel('Global wait Time Out')
            self.globalWait_TimeOut.SetForegroundColour((0,0,0))
            self.timeOut.SetForegroundColour((0,0,0))
            self.stepExecWait.SetLabel('Step Execution Wait')
            self.stepExecWait.SetForegroundColour((0,0,0))
            self.dispVarTimeOut.SetLabel('Display Variable Timeout')
            self.dispVarTimeOut.SetForegroundColour((0,0,0))
            self.connection_timeout.SetLabel('Connection Timeout')
            self.connection_timeout.SetForegroundColour((0,0,0))
            self.max_retries.SetLabel('Max Retries for App Launch')
            self.max_retries.SetForegroundColour((0,0,0))
            #---------------------------------------creating the file in specified path
            try:
                f = open(data['logFile_Path'], "a+")
                f.close()
            except Exception as e:
                msg = "Either logfile path doesn't exists or user doesn't have sufficient privileges."
                logger.print_on_console(msg)
                log.error(msg)
                log.error(e)
                data['logFile_Path'] = ''

            #---------------------------------------resetting the static texts
            if ((os.path.isfile(data['chrome_path'])==True or str(data['chrome_path']).strip()=='default') and
                (os.path.isfile(data['server_cert'])==True or str(data['server_cert']).strip()=='default') and
                (os.path.isfile(data['firefox_path'])==True or str(data['firefox_path']).strip()=='default') and
                os.path.isfile(data['logFile_Path'])==True):
                if int(data['connection_timeout']) in range(1, 8):
                    self.error_msg.SetLabel("Connection Timeout must be greater than or equal to 8")
                    self.error_msg.SetForegroundColour((255,0,0))
                    self.connection_timeout.SetForegroundColour((255,0,0))
                else:
                    self.jsonCreater(config_data)
            else:
                self.error_msg.SetLabel("Marked fields '^' contain invalid path, Data not saved")
                self.error_msg.SetForegroundColour((0,0,255))
                if os.path.isfile(data['server_cert'])!=True or str(data['server_cert']).strip()=='default':
                    self.sev_cert.SetLabel('Server Certificate^')
                    self.sev_cert.SetForegroundColour((0,0,255))
                else:
                    self.sev_cert.SetLabel('Server Certificate')
                    self.sev_cert.SetForegroundColour((0,0,0))

                if os.path.isfile(data['chrome_path'])==True or str(data['chrome_path']).strip()=='default':
                    self.ch_path.SetLabel('Chrome Path')
                    self.ch_path.SetForegroundColour((0,0,0))
                elif os.path.isfile(data['chrome_path'])!=True:
                    self.ch_path.SetLabel('Chrome Path^')
                    self.ch_path.SetForegroundColour((0,0,255))

                if os.path.isfile(data['firefox_path'])==True or str(data['firefox_path']).strip()=='default':
                    self.ff_path.SetLabel('Firefox Path')
                    self.ff_path.SetForegroundColour((0,0,0))
                elif os.path.isfile(data['firefox_path'])!=True:
                    self.ff_path.SetLabel('Firefox Path^')
                    self.ff_path.SetForegroundColour((0,0,255))

                if os.path.isfile(data['logFile_Path'])!=True:
                    self.log_fpath.SetLabel('Log File Path^')
                    self.log_fpath.SetForegroundColour((0,0,255))
                else:
                    self.log_fpath.SetLabel('Log File Path')
                    self.log_fpath.SetForegroundColour((0,0,0))
        else:
            self.error_msg.SetLabel("Do not leave marked '*' fields empty, Data not saved")
            self.error_msg.SetForegroundColour((255,0,0))
            if data['server_ip']=='':
                self.sev_add.SetLabel('Server Address*')
                self.sev_add.SetForegroundColour((255,0,0))
            else:
                self.sev_add.SetLabel('Server Address')
                self.sev_add.SetForegroundColour((0,0,0))
            if data['server_port']=='':
                self.sev_port.SetLabel('Server Port*')
                self.sev_port.SetForegroundColour((255,0,0))
            else:
                self.sev_port.SetLabel('Server Port')
                self.sev_port.SetForegroundColour((0,0,0))
            if data['logFile_Path']=='':
                self.log_fpath.SetLabel('Log File Path*')
                self.log_fpath.SetForegroundColour((255,0,0))
            else:
                self.log_fpath.SetLabel('Log File Path')
                self.log_fpath.SetForegroundColour((0,0,0))
            if data['delay_stringinput']=="sec":
                self.delay_stringinput.SetLabel('Delay for String Input*')
                self.delay_stringinput.SetForegroundColour((255,0,0))
            else:
                self.delay_stringinput.SetLabel('Delay for String Input')
                self.delay_stringinput.SetForegroundColour((0,0,0))
            if data['queryTimeOut']=="sec":
                self.qu_timeout.SetLabel('Query Timeout*')
                self.qu_timeout.SetForegroundColour((255,0,0))
            else:
                self.qu_timeout.SetLabel('Query Timeout')
                self.qu_timeout.SetForegroundColour((0,0,0))
            if data['server_cert']=='':
                self.sev_cert.SetLabel('Server Certificate*')
                self.sev_cert.SetForegroundColour((255,0,0))
            else:
                self.sev_cert.SetLabel('Server Certificate')
                self.sev_cert.SetForegroundColour((0,0,0))
            if data['chrome_path']=='':
                self.ch_path.SetLabel('Chrome Path*')
                self.ch_path.SetForegroundColour((255,0,0))
            else:
                self.ch_path.SetLabel('Chrome Path')
                self.ch_path.SetForegroundColour((0,0,0))
            if data['firefox_path']=='':
                self.ff_path.SetLabel('Firefox Path*')
                self.ff_path.SetForegroundColour((255,0,0))
            else:
                self.ff_path.SetLabel('Firefox Path')
                self.ff_path.SetForegroundColour((0,0,0))
            if data['chrome_profile']=='':
                self.ch_profile.SetLabel('Chrome Profile*')
                self.ch_profile.SetForegroundColour((255,0,0))
            else:
                self.ch_profile.SetLabel('Chrome Profile')
                self.ch_profile.SetForegroundColour((0,0,0))
            if data['chrome_extnpath']=='':
                self.ch_extn_path.SetLabel('Chrome Extn*')
                self.ch_extn_path.SetForegroundColour((255,0,0))
            else:
                self.ch_extn_path.SetLabel('Chrome Extn')
                self.ch_extn_path.SetForegroundColour((0,0,0))
            if data['delay']=="sec":
                self.delayText.SetLabel('Delay*')
                self.delayText.SetForegroundColour((255,0,0))
            else:
                self.delayText.SetLabel('Delay')
                self.delayText.SetForegroundColour((0,0,0))
            if data['timeOut']=="sec":
                self.timeOut.SetLabel('Time Out*')
                self.timeOut.SetForegroundColour((255,0,0))
            else:
                self.timeOut.SetLabel('Time Out')
                self.timeOut.SetForegroundColour((0,0,0))
            if data['globalWaitTimeOut']=="sec":
                self.globalWait_TimeOut.SetLabel('Time Out*')
                self.globalWait_TimeOut.SetForegroundColour((255,0,0))
            else:
                self.globalWait_TimeOut.SetLabel('Time Out')
                self.globalWait_TimeOut.SetForegroundColour((0,0,0))
            if data['stepExecutionWait']=="sec":
                self.stepExecWait.SetLabel('Step Execution Wait*')
                self.stepExecWait.SetForegroundColour((255,0,0))
            else:
                self.stepExecWait.SetLabel('Step Execution Wait')
                self.stepExecWait.SetForegroundColour((0,0,0))
            if data['displayVariableTimeOut']=="sec":
                self.dispVarTimeOut.SetLabel('Display Variable Timeout*')
                self.dispVarTimeOut.SetForegroundColour((255,0,0))
            else:
                self.dispVarTimeOut.SetLabel('Display Variable Timeout')
                self.dispVarTimeOut.SetForegroundColour((0,0,0))
            if data['connection_timeout']=="0 or >=8 hrs":
                self.connection_timeout.SetLabel('Connection Timeout*')
                self.connection_timeout.SetForegroundColour((255,0,0))
            else:
                self.connection_timeout.SetLabel('Connection Timeout')
                self.connection_timeout.SetForegroundColour((0,0,0))
            
            if data['max_retries_app_launch'] == "sec":
                self.max_retries.SetLabel('Max Retries for App Launch*')
                self.max_retries.SetForegroundColour((255,0,0))
            else:
                self.max_retries.SetLabel('Max Retries for App Launch')
                self.max_retries.SetForegroundColour((0, 0, 0))

    """jsonCreater saves the data in json form, location of file to be saved must be defined. This method will overwrite the existing .json file"""
    def jsonCreater(self,data):
        try:
            if wx.MessageBox("Config file has been edited, Would you like to save?","Confirm Save",wx.ICON_QUESTION | wx.YES_NO) == wx.YES:
                # Write JSON file
                with io.open(CONFIG_PATH, 'w', encoding='utf8') as outfile:
                    str_ = json.dumps(data,indent=4, sort_keys=True,separators=(',', ': '), ensure_ascii=False)
                    outfile.write(str(str_))
                logger.print_on_console('--Configuration saved--')
                log.info('--Configuration saved--')
                self.updated = True
        except Exception as e:
            msg = "Error while updating configuration"
            logger.print_on_console(msg)
            log.info(msg)
            log.error(e)

    """readconfigJson reads the config present in the set location, if file not present return 'Config file absent' """
    def readconfigJson(self):
        try:
            with open(CONFIG_PATH) as json_data:
                return json.load(json_data)
        except Exception as e:
            log.error(e)
            return False
            #return "Config file absent"

    """This method open a file selector dialog , from where file path can be set """
    def fileBrowser_chpath(self,event):
        dlg = wx.FileDialog(self, message="Choose a file ...",defaultDir=AVO_ASSURE_HOME,defaultFile="", wildcard="Chrome executable (*chrome.exe)|*chrome.exe|" \
            "All files (*.*)|*.*", style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.chrome_path.SetValue(path)
        dlg.Destroy()

    def fileBrowser_chprofile(self,event):
        dlg = wx.DirDialog(self, message="Choose a folder ...",defaultPath=AVO_ASSURE_HOME, style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.chrome_profile.SetValue(path)
        dlg.Destroy()

    def fileBrowser_chextnpath(self,event):
        dlg = wx.DirDialog(self, message="Choose a folder ...",defaultPath=AVO_ASSURE_HOME, style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            new_path = dlg.GetPath()
            old_path=self.chrome_extnpath.GetValue()
            if old_path == 'default':
                path=new_path
            else:
                path=old_path+';'+new_path
            self.chrome_extnpath.SetValue(path)
        dlg.Destroy()

    """This method open a file selector dialog , from where file path can be set """
    def fileBrowser_ffpath(self,event):
        dlg = wx.FileDialog(self, message="Choose a file ...",defaultDir=AVO_ASSURE_HOME,defaultFile="", wildcard="Firefox executable (*firefox.exe)|*firefox.exe|" \
            "All files (*.*)|*.*", style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.firefox_path.SetValue(path)
        dlg.Destroy()
    """This method open a file selector dialog , from where file path can be set """
    def fileBrowser_logfilepath(self,event):
        dlg = wx.DirDialog(None, "Choose a folder", "", wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            log_path = dlg.GetPath()
            log_path= os.path.normpath(log_path+"/TestautoV2.log")
            self.log_file_path.SetValue(log_path)
        dlg.Destroy()
    """This method open a file selector dialog , from where file path can be set """
    def fileBrowser_servcert(self,event):
        dlg = wx.FileDialog(self, message="Choose a file ...",defaultDir=AVO_ASSURE_HOME,defaultFile="", wildcard="Certificate file (*.crt)|*.crt|" \
            "All files (*.*)|*.*", style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.server_cert.SetValue(path)
        dlg.Destroy()

    """This method closes the wxPython config window instance"""
    def close(self, event):
        self.Destroy()
        global configvalues
        configvalues = readconfig.readConfig().readJson() # Re-reading config values
        core.configvalues = configvalues
        core.browsercheckFlag=False
        if configvalues['browser_check'].lower() == 'no':
            core.browsercheckFlag=True
            core.chromeFlag=core.firefoxFlag=False
        core.updatecheckFlag = configvalues['update_check'].lower() == 'no'
        if self.headlessOldVal != configvalues['headless_mode']:
            controller.kill_process()
        try:
            logfilename = os.path.normpath(configvalues["logFile_Path"]).replace("\\","\\\\")
            logging.config.fileConfig(LOGCONFIG_PATH,defaults={'logfilename': logfilename},disable_existing_loggers=False)
        except Exception as e:
            log.error(e)
        wxObject.EnableAll()
        if self.updated and root.token_obj.tokenwindow is None:
            wxObject.connectbutton.Enable()
        msg = '--Edit Config closed--'
        logger.print_on_console(msg)
        log.info(msg)

#-------------------
"""Displays the details of ICE, versions, etc.(can be customised/it is read only)"""
class About_window(wx.Frame):
    """Initialization and defining the wx-components of the pop-up"""
    def __init__(self, parent, id, title):
        try:
            data = self.get_client_manifest()
            msg1='Avo Assure ICE '+ str(data['version']) + ' (64-bit)' +' \n'
            msg2='Updated on : '+ str(data['updated_on']) +' \n'
            msg3='For any queries write to us at support@avoautomation.com'+' \n'
            msg4='© Avo Automation\n'
            #------------------------------------Different co-ordinates for Windows and Mac
            if SYSTEM_OS=='Windows':
                upload_fields= {
                "Frame":[(300, 150),(400,220)],
                "disp_msg":[(12,18),(80, 28),(100,18), (310,-1),(415,18),(30, -1)],
                "Close":[(280,148), (100, 28)]
            }
            elif SYSTEM_OS=='Darwin':
                upload_fields={
                "Frame":[(300, 150),(400,220)],#(diff +85,+10 from windows)
                "disp_msg":[(12,38),(80,28),(116,38),(382,-1),(504,38),(30, -1)],
                "Close":[(285,148),(100, 28)]
            }
            else:
                upload_fields={
                "Frame":[(300, 150),(460,220)],
                "disp_msg":[(12,38),(80,28),(116,38),(382,-1),(504,38),(30, -1)],
                "Close":[(285,148),(100, 28)]
            }
            wx.Frame.__init__(self, parent, title=title,pos=upload_fields["Frame"][0], size=upload_fields["Frame"][1], style = wx.CAPTION|wx.CLIP_CHILDREN)
            self.SetBackgroundColour('#e6e7e8')
            self.iconpath = IMAGES_PATH +"avo.ico"
            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.wicon)
            self.panel = wx.Panel(self)
            self.image = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH + 'AVO_Assure.png', wx.BITMAP_TYPE_ANY), wx.Point(10, 10))
            self.msg1=wx.StaticText(self.panel, -1, str(msg1), wx.Point(170, 20), wx.Size(200, 50)).SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            if SYSTEM_OS=='Windows':
                self.msg2=wx.StaticText(self.panel, -1, str(msg2), wx.Point(170, 55), wx.Size(200, 50))
                self.msg3=wx.StaticText(self.panel, -1, str(msg3), wx.Point(10, 90), wx.Size(350, 50))
            else:
                self.msg2 = wx.StaticText(self.panel, -1, str(msg2), wx.Point(170, 55), wx.Size(300, 50))
                self.msg3 = wx.StaticText(self.panel, -1, str(msg3), wx.Point(10, 90), wx.Size(400, 50))
            self.msg4=wx.StaticText(self.panel, -1, str(msg4), wx.Point(10, 120), wx.Size(200, 50))
            self.close_btn = wx.Button(self.panel, label="Close",pos=upload_fields["Close"][0], size=upload_fields["Close"][1])
            self.close_btn.Bind(wx.EVT_BUTTON, self.close)
            self.Centre()
            wx.Frame(self.panel)
            self.Show()
        except Exception as e:
            logger.print_on_console("Error occured in About")
            log.error("Error occured in About, Err msg : " + str(e))


    def get_client_manifest(self):
        data=None
        try:
            with open(MANIFEST_LOC) as f:
                data = json.load(f)
        except:
            msg = 'Unable to fetch package manifest.'
            logger.print_on_console(msg)
            log.error(msg)
        return data

    def close(self, event):
        self.Close()
        self.Destroy()
        wxObject.EnableAll()
        log.info('--About pop-up closed--')

#-------------
"""Checks if config file is present, if not prompts the user to enter config file details"""
class Check_Update_window(wx.Frame):
    """Initialization and defining the wx-components of the pop-up"""
    global update_obj
    def __init__(self, parent, id, title):
        """Check if updates are avaliable"""
        try:
            boolval,l_ver=check_update(False)
            if boolval is False and l_ver == "N/A":
                msg = "Update Failed!"
                logger.print_on_console(msg)
                log.error(msg)
                return None
            #------------------------------------Different co-ordinates for Windows and Mac
            if SYSTEM_OS=='Windows':
                upload_fields= {
                "Frame":[(300, 150),(465,160)],
                "disp_msg":[(12,18),(80, 28),(100,18), (310,-1),(415,18),(30, -1)],
                "Update":[(100,88), (100, 28)],
                "Close":[(250,88), (100, 28)]
            }
            else:
                upload_fields={
                "Frame":[(300, 150),(550,160)],#(diff +85,+10 from windows)
                "disp_msg":[(12,38),(80,28),(116,38),(382,-1),(504,38),(30, -1)],
                "Update":[(135,88),(100, 28)],
                "Close":[(285,88),(100, 28)]
            }
            wx.Frame.__init__(self, parent, title=title,pos=upload_fields["Frame"][0], size=upload_fields["Frame"][1], style = wx.CAPTION|wx.CLIP_CHILDREN)
            self.SetBackgroundColour('#e6e7e8')
            self.iconpath = IMAGES_PATH +"avo.ico"
            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.wicon)
            self.updated = False
            self.panel = wx.Panel(self)
            self.disp_msg = wx.TextCtrl(self.panel, pos = upload_fields["disp_msg"][0], size = (425, 60), style = wx.TE_MULTILINE|wx.TE_READONLY)
            self.update_btn = wx.Button(self.panel, label="Update",pos=upload_fields["Update"][0], size=upload_fields["Update"][1])
            self.update_btn.Bind(wx.EVT_BUTTON, self.update_ice)
            self.close_btn = wx.Button(self.panel, label="Close",pos=upload_fields["Close"][0], size=upload_fields["Close"][1])
            self.close_btn.Bind(wx.EVT_BUTTON, self.close)
            self.update_btn.Disable()
            UPDATE_MSG = update_obj.send_update_message()
            if ( UPDATE_MSG == 'Update Available!!! Click on update' ):
                self.disp_msg.AppendText( "An update is available, click on 'Update' button to install the latest patch : " + str(l_ver) + "\n")
                self.disp_msg.AppendText( "Warning! ICE will close when update starts...")
                self.update_btn.Enable()
            else:
                self.disp_msg.SetValue(UPDATE_MSG)
            self.Centre()
            wx.Frame(self.panel)
            self.Show()
        except Exception as e:
            msg = "Error occured while checking for updates"
            logger.print_on_console(msg)
            log.error(msg)
            log.error(e, exc_info=True)

    """updates ICE"""
    def update_ice(self,event):
        try:
            self.close(event)
            logger.print_on_console("--Updating Files and Packages--")
            log.info("--Updating Files and Packages--")
            l_ver=check_update(False)
            l_ver=l_ver[1]
            update_obj.run_updater(l_ver)
        except Exception as e:
            log.error('Error occured in update_ice : ' + str(e))
            logger.print_on_console('Error occured in update_ice : ' + str(e))

    def close(self, event):
        self.Close()
        self.Destroy()
        wxObject.EnableAll()
        log.info('--Updater pop-up closed--')

class rollback_window(wx.Frame):
    """Initialization and defining the wx-components of the pop-up"""
    def __init__(self, parent, id, title):
        """Check if updates are avaliable"""
        try:
            #------------------------------------Different co-ordinates for Windows and Mac
            if SYSTEM_OS=='Windows':
                upload_fields= {
                "Frame":[(300, 150),(465,160)],
                "disp_msg":[(12,18),(80, 28),(100,18), (310,-1),(415,18),(30, -1)],
                "Rollback":[(100,88), (100, 28)],
                "Close":[(250,88), (100, 28)]
            }
            else:
                upload_fields={
                "Frame":[(300, 150),(550,160)],#(diff +85,+10 from windows)
                "disp_msg":[(12,38),(80,28),(116,38),(382,-1),(504,38),(30, -1)],
                "Rollback":[(135,88),(100, 28)],
                "Close":[(285,88),(100, 28)]
            }
            wx.Frame.__init__(self, parent, title=title,pos=upload_fields["Frame"][0], size=upload_fields["Frame"][1], style = wx.CAPTION|wx.CLIP_CHILDREN)
            self.SetBackgroundColour('#e6e7e8')
            self.iconpath = IMAGES_PATH +"avo.ico"
            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.wicon)
            self.panel = wx.Panel(self)
            self.rollback_obj = None
            self.disp_msg = wx.TextCtrl(self.panel, pos = upload_fields["disp_msg"][0], size = (425, 60), style = wx.TE_MULTILINE|wx.TE_READONLY)
            self.rollback_btn = wx.Button(self.panel, label="Rollback",pos=upload_fields["Rollback"][0], size=upload_fields["Rollback"][1])
            self.rollback_btn.Bind(wx.EVT_BUTTON, self.rollback)
            self.close_btn = wx.Button(self.panel, label="Close",pos=upload_fields["Close"][0], size=upload_fields["Close"][1])
            self.close_btn.Bind(wx.EVT_BUTTON, self.close)
            self.rollback_btn.Disable()
            res = os.path.exists(os.path.normpath(AVO_ASSURE_HOME+'/assets/AvoAssureICE_backup.7z'))
            self.rollback_obj = update_module.Update_Rollback()
            if ( res == False ):
                self.disp_msg.AppendText( "Avo Assure ICE backup not found, cannot rollback changes.")
            else:
                self.rollback_obj.update(None, None, None, AVO_ASSURE_HOME, LOC_7Z, UPDATER_LOC, 'ROLLBACK')
                self.disp_msg.AppendText( "Click 'Rollback' to run previous version of Avo Assure ICE.")
                self.rollback_btn.Enable()
            self.Centre()
            wx.Frame(self.panel)
            self.Show()
        except Exception as e:
            log.error('Error occured in rollback_window class : ' + str(e))
            logger.print_on_console('Error occured while trying to rollback.')

    def rollback(self,event):
        """Rolls back Avo Assure ICE"""
        try:
            self.close(event)
            logger.print_on_console("--Rolling back to previous version of Avo Assure ICE--")
            log.info("--Rolling back to previous version of Avo Assure ICE--")
            self.rollback_obj.run_rollback()
        except Exception as e:
            log.error('Error occured in rollback : ' + str(e))
            logger.print_on_console('Error occured in rollback : ' + str(e))

    def close(self, event):
        self.Close()
        self.Destroy()
        wxObject.EnableAll()
        log.info('--Rollback pop-up closed--')
#------------------


class DebugWindow(wx.Frame):
    def __init__(self, parent,id, title):
        wx.Frame.__init__(self, parent, title=title, pos=(300, 150),  size=(200, 75),
            style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX) )
        self.SetBackgroundColour('#e6e7e8')
        ##style = wx.CAPTION|wx.CLIP_CHILDREN
        self.iconpath = IMAGES_PATH +"avo.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        self.panel = wx.Panel(self)
        self.continue_debugbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"play.png", wx.BITMAP_TYPE_ANY), (65, 15), (35, 28))
        self.continue_debugbutton.Bind(wx.EVT_LEFT_DOWN, self.Resume)
        self.continue_debugbutton.SetToolTip(wx.ToolTip("Resume"))
        self.continuebutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"step.png", wx.BITMAP_TYPE_ANY), (105, 15), (35, 28))
        self.continuebutton.Bind(wx.EVT_LEFT_DOWN, self.OnContinue)
        self.continuebutton.SetToolTip(wx.ToolTip("Proceed to next step"))
        self.Centre()
        style = self.GetWindowStyle()
        self.SetWindowStyle( style|wx.STAY_ON_TOP )
        self.Bind(wx.EVT_CLOSE, self.Resume)
        wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Show()

    def Resume(self, event):
        msg = "Event Triggered to Resume Debug"
        logger.print_on_console(msg)
        log.info(msg)
        controller.pause_flag=False
        root.testthread.resume(False)
        wxObject.debugwindow = None
        self.Destroy()

    def OnContinue(self, event):
        msg = "Event Triggered to proceed to next step"
        logger.print_on_console(msg)
        controller.pause_flag=False
        root.testthread.resume(True)


class ProxyConfig_window(wx.Frame):
    """Initialization and defining the wx-components of the pop-up"""
    def __init__(self, parent, id, title):
        try:
            data = self.readproxyconfig()
            #------------------------------------Different co-ordinates for Windows and Mac
            if SYSTEM_OS=='Windows':
                upload_fields= {
                "Frame":[(300, 170),(400, 230)],
                "disp_msg":[(12,18),(80, 28),(100,18), (310,-1),(415,18),(30, -1)],
                "proxy_enable":[(17,7), (180,40)],
                "proxy_url":[(17,67),(95, 50),(120,61), (245,-1)],
                "username":[(17,97),(95, 20),(120,91), (245,-1)],
                "passwd":[(17,128),(95, 20),(120,122), (245,-1)],
                "Save":[(157, 153), (100, 28)],
                "Close":[(264,153), (100, 28)]
            }
            elif SYSTEM_OS=='Darwin':
                upload_fields={
                "Frame":[(300, 150),(550,220)],#(diff +85,+10 from windows)
                "disp_msg":[(12,38),(80,28),(116,38),(382,-1),(504,38),(30, -1)],
                "Close":[(285,88),(100, 28)]
            }
            elif SYSTEM_OS=='Linux':
                upload_fields= {
                "Frame": [(300, 170), (420, 230)],
                "disp_msg": [(12, 18), (80, 28), (100, 18), (310, -1), (415, 18), (30, -1)],
                "proxy_enable": [(17, 7), (180, 40)],
                "proxy_url": [(17, 67), (95, 50), (150, 61), (245, 25)],
                "username": [(17, 97), (130, 40), (150, 91), (245, 25)],
                "passwd": [(17, 128), (130, 50), (150, 122), (245, 25)],
                "Save": [(157, 153), (100, 28)],
                "Close": [(264, 153), (100, 28)]
            }
            lblList = ['Enabled', 'Disabled']
            wx.Frame.__init__(self, parent, title=title,pos=upload_fields["Frame"][0], size=upload_fields["Frame"][1], style = wx.CAPTION|wx.CLIP_CHILDREN)
            self.SetBackgroundColour('#e6e7e8')
            self.iconpath = IMAGES_PATH + "avo.ico"
            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.wicon)
            self.panel = wx.Panel(self)
            self.rbox1 = wx.RadioBox(self.panel, label = 'Enable Proxy', choices = lblList, majorDimension = 1,
                style = wx.RA_SPECIFY_ROWS, pos=upload_fields["proxy_enable"][0], size=upload_fields["proxy_enable"][1])
            self.rbox1.SetToolTip(wx.ToolTip("Enable or Disable Proxy in Avo Assure ICE"))
            self.rbox1.Bind(wx.EVT_RADIOBOX, self.radio_check)
            self.proxy_url_path=wx.StaticText(self.panel, label="Proxy URL", pos=upload_fields["proxy_url"][0],size=upload_fields["proxy_url"][1], style=0, name="")
            self.proxy_url_path.SetToolTip(wx.ToolTip("Proxy URL (must start with http:// or https://)"))
            self.proxy_url=wx.TextCtrl(self.panel, pos=upload_fields["proxy_url"][2], size=upload_fields["proxy_url"][3])
            if data != False:
                self.proxy_url.SetValue(data['url'])
            else:
                self.proxy_url.SetValue('')

            self.proxy_user_path=wx.StaticText(self.panel, label="Proxy Username", pos=upload_fields["username"][0],size=upload_fields["username"][1], style=0, name="")
            self.proxy_user_path.SetToolTip(wx.ToolTip("Username for proxy authentication"))
            self.proxy_user = wx.TextCtrl(self.panel, pos=upload_fields["username"][2], size=upload_fields["username"][3])
            if data != False:
                self.proxy_user.SetValue(data['username'])
            else:
                self.proxy_user.SetValue('')

            self.proxy_pass_path=wx.StaticText(self.panel, label="Proxy Password", pos=upload_fields["passwd"][0],size=upload_fields["passwd"][1], style=0, name="")
            self.proxy_pass_path.SetToolTip(wx.ToolTip("Password for proxy authentication"))
            self.proxy_pass=wx.TextCtrl(self.panel, pos=upload_fields["passwd"][2], size=upload_fields["passwd"][3])
            if data != False:
                self.proxy_pass.SetValue(data['password'])
            else:
                self.proxy_pass.SetValue('')

            if data != False and data['enabled'].title()==lblList[0]:
                self.rbox1.SetSelection(0)
                self.toggle_all(True)
            else:
                self.rbox1.SetSelection(1)
                self.toggle_all(False)

            # self.image = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH + 'AVO_Assure.png', wx.BITMAP_TYPE_ANY), wx.Point(10, 10))
            self.close_btn = wx.Button(self.panel, label="Close",pos=upload_fields["Close"][0], size=upload_fields["Close"][1])
            self.close_btn.Bind(wx.EVT_BUTTON, self.close)
            self.save_btn=wx.Button(self.panel, label="Save",pos=upload_fields["Save"][0], size=upload_fields["Save"][1])
            self.save_btn.Bind(wx.EVT_BUTTON, self.save)
            self.Centre()
            wx.Frame(self.panel)
            self.Show()
        except Exception as e:
            logger.print_on_console("Error occured in Proxy Config")
            log.error("Error occured in Proxy Config. Err msg : " + str(e))

    def readproxyconfig(self):
        try:
            with open(PROXY_PATH) as json_data:
                return json.load(json_data)
        except Exception as e:
            log.error(e)
            return False

    def jsonCreater(self, data):
        try:
            if wx.MessageBox("Would you like to save updated proxy config?","Confirm Save",wx.ICON_QUESTION | wx.YES_NO) == wx.YES:
                # Write JSON file
                with io.open(PROXY_PATH, 'w', encoding='utf8') as outfile:
                    str_ = json.dumps(data,indent=4, sort_keys=True,separators=(',', ': '), ensure_ascii=False)
                    outfile.write(str(str_))
                logger.print_on_console('--Proxy Configuration saved--')
                log.info('--Proxy Configuration saved--')
                self.updated = True
        except Exception as e:
            msg = "Error while updating configuration"
            logger.print_on_console(msg)
            log.info(msg)
            log.error(e)

    def close(self, event):
        self.Destroy()
        global proxies
        proxies = readconfig.readProxyConfig().readJson()
        core.proxies = proxies

    def save(self,event):
        data = {
            'enabled': self.rbox1.GetStringSelection(),
            'url': self.proxy_url.GetValue(),
            'username': self.proxy_user.GetValue(),
            'password': self.proxy_pass.GetValue()
        }
        nosave = False
        if data['enabled'] == "Enabled":
            if not (data['url'].startswith("http://") or data['url'].startswith("https://")):
                self.proxy_url_path.SetLabel('Proxy URL*')
                self.proxy_url_path.SetForegroundColour((255,0,0))
                nosave = True
            else:
                self.proxy_url_path.SetLabel('Proxy URL')
                self.proxy_url_path.SetForegroundColour((0,0,0))
            if len(data['username']) == 0 and len(data['password']) != 0:
                self.proxy_user_path.SetLabel('Proxy Username*')
                self.proxy_user_path.SetForegroundColour((255,0,0))
                nosave = True
            else:
                self.proxy_user_path.SetLabel('Proxy Username')
                self.proxy_user_path.SetForegroundColour((0,0,0))
            if len(data['username']) != 0 and len(data['password']) == 0:
                self.proxy_pass_path.SetLabel('Proxy Password*')
                self.proxy_pass_path.SetForegroundColour((255,0,0))
                nosave = True
            else:
                self.proxy_pass_path.SetLabel('Proxy Password')
                self.proxy_pass_path.SetForegroundColour((0,0,0))
        if not nosave:
            self.jsonCreater(data)

    def toggle_all(self, value):
        self.proxy_url.Enable(value)
        self.proxy_user.Enable(value)
        self.proxy_pass.Enable(value)

    def radio_check(self,event):
        self.toggle_all(self.rbox1.GetStringSelection() == 'Enabled')


def check_update(flag):
    global update_obj
    SERVER_LOC = "https://" + str(configvalues['server_ip']) + ':' + str(configvalues['server_port']) + '/patchupdate/'
    req_kw_args = core.ConnectionThread(None).get_ice_session(no_params=True)
    req_kw_args.pop('assert_hostname', None)

    #------------------------------------------------------------getting server manifest
    def get_server_manifest_data():
        data = None
        request = None
        emsg = "Error in fetching update manifest from server"
        try:
            request = requests.get(SERVER_LOC + "/manifest.json", verify=False)
            if(request.status_code ==200):
                data = json.loads(request.text) #will return json of the manifest
        except Exception as e:
            log.error(emsg)
            log.error(e,exc_info=True)
            logger.print_on_console(emsg)
        return data
    #-----------------------------------------------------------Updater Module
    def update_updater_module(data):
        global update_obj
        update_obj = update_module.Update_Rollback()
        update_obj.update(data, MANIFEST_LOC, SERVER_LOC, AVO_ASSURE_HOME, LOC_7Z, UPDATER_LOC, 'UPDATE')
    #---------------------------------------updater
    data = get_server_manifest_data()
    update_updater_module(data)
    UPDATE_MSG=update_obj.send_update_message()
    l_ver = update_obj.fetch_current_value()
    SERVER_CHECK_MSG = update_obj.server_check_message()
    if (SERVER_CHECK_MSG): log.info(SERVER_CHECK_MSG)
    #check if update avaliable
    if ( UPDATE_MSG == 'Update Available!!! Click on update' and flag == True ):
        logger.print_on_console("An update is available. Click on 'Help' menu option -> 'Check for Updates' sub-menu option -> 'Update' button")
        logger.print_on_console('The latest ICE version : ',l_ver)
        log.info(UPDATE_MSG)
    elif ( UPDATE_MSG == 'You are running the latest version of Avo Assure ICE' and flag == True ):
        logger.print_on_console( "No updates available" )
        log.info( "No updates available" )
    elif ( UPDATE_MSG == 'An Error has occured while checking for new versions of Avo Assure ICE, kindly contact Support Team'):
        if not (os.path.exists(MANIFEST_LOC)):
            logger.print_on_console( "Client manifest unavaliable." )
            log.info( "Client manifest unavaliable." )
        else:
            statcode=requests.get(SERVER_LOC + "/manifest.json", **req_kw_args).status_code
            if( requests.get(SERVER_LOC, **req_kw_args).status_code == 404) : UPDATE_MSG = UPDATE_MSG[:UPDATE_MSG.index(',')+1] + ' Patch updater server not hosted.'
            elif(statcode == 404) : UPDATE_MSG = UPDATE_MSG[:UPDATE_MSG.index(',')+1] + ' "manifest.json" not found, Please ensure "manifest.json" is present in patch updater folder'
            elif(statcode !=404 or statcode !=200): UPDATE_MSG = UPDATE_MSG[:UPDATE_MSG.index(',')+1] + ' "manifest.json error". ERROR_CODE: ' + str(statcode)
            logger.print_on_console( UPDATE_MSG )
            log.info( UPDATE_MSG )
    return False,l_ver

