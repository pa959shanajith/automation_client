import wx
import sys
import os
import controller
import time
from constants import *
import logging
import logging.config
import argparse
import base64

import logger
import threading
from values_from_ui import *
log = logging.getLogger('clientwindow.py')
from socketIO_client import SocketIO,BaseNamespace
import readconfig
import httplib

i = 0
wxObject = None
browsername = None
qcdata = None
qcConFlag=False
desktopScrapeFlag=False
sapScrapeFlag=False
mobileScrapeFlag=False
mobileWebScrapeFlag=False
debugFlag = False
oebsScrapeFlag = False



parser = argparse.ArgumentParser(description="Nineteen68 Platform")
parser.add_argument('--NINETEEN68_HOME', type=str, help='A Required path to Nineteen68 root location')
args = parser.parse_args()

if args.NINETEEN68_HOME < 1:
    parser.error("Required at least 1 argument")

os.environ["NINETEEN68_HOME"] = args.NINETEEN68_HOME
IMAGES_PATH = os.environ["NINETEEN68_HOME"] + "/Nineteen68/plugins/Core/Images"
CERTIFICATE_PATH = os.environ["NINETEEN68_HOME"] + "/Scripts/CA_BUNDLE"

"""
Setting Logging configuration file path

"""

LOGCONFIG_PATH = os.environ["NINETEEN68_HOME"] + "/logging.conf"
configobj = readconfig.readConfig()
#747 check for syntax error in config.json
try:
    configvalues = configobj.readJson()
    jsonSyntaxErrorFlag = False
except:
    jsonSyntaxErrorFlag = True

"""
This code snippet blocks the inheritance of file handlers from
parent process to child process. We are applying the same for only on file
 which is our log file.

"""
if sys.platform == 'win32':
    from ctypes import *
    import msvcrt

    __builtins__open = __builtins__.open

    def __open_inheritance_hack(*args, **kwargs):
        result = __builtins__open(*args, **kwargs)
        handle = msvcrt.get_osfhandle(result.fileno())
        if configvalues["logFile_Path"] in args:
            windll.kernel32.SetHandleInformation(handle, 1, 0)
        return result

    __builtins__.open = __open_inheritance_hack


class MainNamespace(BaseNamespace):
    def on_message(self, *args):
##        print 'Inside debugTestCase method'
        ##print '------------------',args
        global action,wxObject,browsername,desktopScrapeFlag
        if str(args[0]) == 'OPEN BROWSER CH':

            browsername = '1'
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
##            time.sleep(5)
        elif str(args[0]) == 'OPEN BROWSER IE':

            browsername = '3'
##
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

##            time.sleep(5)
##            print 'Importing done'
        elif str(args[0]) == 'OPEN BROWSER FX':
##
            browsername = '2'
##
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

##            time.sleep(5)
            print 'Importing done'
        elif str(args[0]) == 'OPEN BROWSER SF':
##
            browsername = '6'
##
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

##            time.sleep(5)
            print 'Importing done'

        elif str(args[0]) == 'debugTestCase':
            print 'on_debugTestCase_message'
            wxObject.mythread = TestThread(wxObject,DEBUG,args[1])


        if(str(args[0]) == 'connected'):
            logger.print_on_console('Normal Mode: Connection to the Node Server established')
            log.info('Normal Mode: Connection to the Node Server established')
        elif(str(args[0]) == 'reconnected'):
            logger.print_on_console('Schedule Mode:Connection to the Node Server established')
            log.info('Schedule Mode:Connection to the Node Server established')
        elif(str(args[0]) == 'connectionExists'):
            logger.print_on_console('Conenction Already Exists')
            log.info('Conenction Already Exists')

    def on_webscrape(self,*args):
        global action,wxObject,browsername,desktopScrapeFlag,data
        args = list(args)
        d = args[0]
        action = d['action']
        task = d['task']
        data = ''
        if action == 'scrape':
            if str(task) == 'OPEN BROWSER CH':
                browsername = '1'
                wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
            elif str(task) == 'OPEN BROWSER IE':
                browsername = '3'
                wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
            elif str(task) == 'OPEN BROWSER FX':
                browsername = '2'
                wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
            elif str(task) == 'OPEN BROWSER SF':
                browsername = '6'
                wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
        elif action == 'compare':
            data = d['viewString']
            if str(task) == 'OPEN BROWSER CH':
                browsername = '1'
                wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
            elif str(task) == 'OPEN BROWSER IE':
                browsername = '3'
                wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
            elif str(task) == 'OPEN BROWSER FX':
                browsername = '2'
                wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))


    def on_emit(self, *args):
        if str(args[0]) == 'connected':
            print 'Connected'

    def on_focus(self, *args):

        appType=args[2]
        appType=appType.lower()
        if appType==APPTYPE_WEB:
            import highlight
            light =highlight.Highlight()
            res = light.highlight(args,None,None)
            print 'Highlight result: ',res
        if appType==APPTYPE_MOBILE.lower():
            import highlight_MW
            light =highlight_MW.Highlight()
            res = light.highlight(args,None,None)
            print 'Highlight result: ',res
        if appType==APPTYPE_DESKTOP_JAVA.lower():
            con =controller.Controller()
            con.get_all_the_imports('Oebs')
            import utils
            light =utils.Utils()
            res = light.highlight(args[0],args[1])
            print 'Highlight result: ',res
        elif appType==APPTYPE_DESKTOP.lower():
            con =controller.Controller()
            con.get_all_the_imports('Desktop2')
            import desktop_highlight
            highlightObj=desktop_highlight.highLight()
            highlightObj.highLiht_element(args[0],args[1])

  #--------------------------------------------------------------------------------------------------sap change
        elif appType==APPTYPE_SAP.lower():
            con =controller.Controller()
            con.get_all_the_imports('SAP')
            import sap_highlight
            highlightObj=sap_highlight.highLight()
            print 'calling highlight'
##            i = args[0].rfind(",")
##            var = args[0][:i]
            highlightObj.highlight_element(args[0])
            print 'highlight called'
#--------------------------------------------------------------------------------------------------sap change


    def on_executeTestSuite(self, *args):
        global wxObject
        args=list(args)
        wxObject.mythread = TestThread(wxObject,EXECUTE,args[0],wxObject.debug_mode)

    def on_debugTestCase(self, *args):
        global wxObject
        args=list(args)
        wxObject.mythread = TestThread(wxObject,DEBUG,args[0],wxObject.debug_mode)
        wxObject.choice=wxObject.rbox.GetStringSelection()
        print wxObject.choice,' is Selected'
        if wxObject.choice == 'Normal':
            if wxObject.debugwindow != None:
                wxObject.debugwindow.Close()
                wxObject.debugwindow = None

        wxObject.debug_mode=False
        wxObject.breakpoint.Disable()
        if wxObject.choice in ['Stepwise','RunfromStep']:
            global debugFlag
            debugFlag = True
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

    def on_LAUNCH_DESKTOP(self, *args):
        con = controller.Controller()
        global browsername
        browsername = args[0]
        con =controller.Controller()
        con.get_all_the_imports('Desktop2')
        import ninteen_68_desktop_scrape
        global desktopScrapeObj
        desktopScrapeObj=ninteen_68_desktop_scrape
        global desktopScrapeFlag
        desktopScrapeFlag=True
        wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

    def on_LAUNCH_SAP(self, *args):

        try:

            con = controller.Controller()
            global browsername
            browsername = args[0]
            con =controller.Controller()
            con.get_all_the_imports('SAP')
            import ninteen_68_sap_scrape
            global sapScrapeObj
            sapScrapeObj=ninteen_68_sap_scrape
            global sapScrapeFlag
            sapScrapeFlag=True
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

        except Exception as e:
            import traceback
            traceback.print_exc()
            print e


    def on_qclogin(self, *args):
        con = controller.Controller()
        global qcdata
##        con = controller.Controller()
        import json
        qcdata = args[0]
        con.get_all_the_imports('Qc')
        import QcController
        global qcConObj
        qcConObj=QcController
        global qcConFlag
        qcConFlag=True
        wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))


    def on_LAUNCH_MOBILE(self, *args):
        con = controller.Controller()
        global browsername
        con = controller.Controller()
        if str(args[0]).endswith('apk'):
            browsername = args[0]+";"+args[1]
        elif str(args[0]).endswith('app'):
            browsername = args[0] + ";" + args[2]+";" + args[3]
        elif str(args[0]).endswith('ipa'):
            browsername = args[0] + ";" + args[2] + ";" + args[3]+";" + args[4]
        con =controller.Controller()
        import platform
        if platform.system()=='Darwin':
            con.get_all_the_imports('Mobility/MobileApp')
        else:
            con.get_all_the_imports('Mobility')
        import ninteen_68_mobile_scrape
        global mobileScrapeObj
        mobileScrapeObj=ninteen_68_mobile_scrape
        global mobileScrapeFlag
        mobileScrapeFlag=True
        wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

    def on_LAUNCH_MOBILE_WEB(self, *args):
        global mobileWebScrapeObj,mobileWebScrapeFlag
        con = controller.Controller()
        global browsername
        browsername = args[0]+";"+args[1]
        con =controller.Controller()
        import platform
        if platform.system()=='Darwin':
            con.get_all_the_imports('Mobility/MobileWeb')
        else:
            con.get_all_the_imports('Mobility')
        import ninteen_68_mobile_web_scrape

        mobileWebScrapeObj=ninteen_68_mobile_web_scrape

        mobileWebScrapeFlag=True
        ##print mobileWebScrapeFlag
        wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

    def on_LAUNCH_OEBS(self, *args):
        global oebsScrapeObj,oebsScrapeFlag
        print("Entering inside OEBS")
        con = controller.Controller()
        global browsername
        browsername = args[0]
        print("Entering inside OEBS : ",browsername)
        con =controller.Controller()

        con.get_all_the_imports('Oebs')
        import scrape_dispatcher

        oebsScrapeObj=scrape_dispatcher

        oebsScrapeFlag=True
        ##print mobileWebScrapeFlag
        wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

    def on_wsdl_listOfOperation(self, *args):
        global socketIO
        contrlr = controller.Controller()
        contrlr.get_all_the_imports('WebServices')
        import wsdlgenerator
        wsdlurl = str(args[0])
        wsdl_object = wsdlgenerator.WebservicesWSDL()
        response = wsdl_object.listOfOperation(wsdlurl)
        response=str(response)
        print response
        socketIO.emit('result_wsdl_listOfOperation',response)

    def on_wsdl_ServiceGenerator(self, *args):
        global socketIO
        contrlr = controller.Controller()
        contrlr.get_all_the_imports('WebServices')
        import wsdlgenerator
        wsgen_inputs=eval(str(args[0]))
        wsdlurl = wsgen_inputs['wsdlurl']
        operations = wsgen_inputs['operations']
        soapVersion = wsgen_inputs['soapVersion']
        wsdl_object = wsdlgenerator.BodyGenarator(wsdlurl,operations,soapVersion)
        responseHeader = wsdl_object.requestHeader()
        responseBody = wsdl_object.requestBody()
        stringHeader=''
        if(responseHeader != None):
            for key in responseHeader:
                print key,'==========',responseHeader[key]
                stringHeader = stringHeader + str(key) + ": " + str (responseHeader[key]) + "##"
        responseHeader = stringHeader
        print 'responseHeader after:::',responseHeader
        print 'responseBody:::::',responseBody
        response=responseHeader+"rEsPONseBOdY:"+responseBody
        response=str(response)
        print response
        socketIO.emit('result_wsdl_ServiceGenerator',response)

    def on_render_screenshot(self,*args):
        try:
            global socketIO
            filepath = args[0]
            data_URIs=[]
            for path in filepath:
                encoded_string = ''
                with open(path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                base64_data=encoded_string.encode('UTF-8').strip()
                data_URIs.append(base64_data)
            socketIO.emit('render_screenshot',data_URIs)
        except Exception as e:
            print 'Error while sending screenshot data'
            socketIO.emit('render_screenshot','fail')

    def on_webCrawlerGo(self,*args):
        try:
            con = controller.Controller()
            con.get_all_the_imports('WebOccular')
            import weboccular
            wo = weboccular.Weboccular()

            args=list(args)
            global socketIO

            #args[0] is URL, args[1] is level, args[2] is agent
            wo.runCrawler(args[0],args[1],args[2],socketIO,wxObject)

        except Exception as e:
            import traceback
            traceback.print_exc()


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
        server_IP = configvalues['server_ip']
        temp_server_IP = 'https://' + server_IP
        key='USERNAME'
        if(not(os.environ.has_key(key))):
            key='USER'
        username=os.environ[key]
        params={'username':username}
        socketIO = SocketIO(temp_server_IP,int(configvalues['server_port']),MainNamespace,verify= CERTIFICATE_PATH +'/server.crt',cert=(CERTIFICATE_PATH + '/client.crt', CERTIFICATE_PATH + '/client.key'),params=params)
##        socketIO = SocketIO(temp_server_IP,int(configvalues['server_port']),MainNamespace,verify= CERTIFICATE_PATH +'/server.crt',cert=(CERTIFICATE_PATH + '/client.crt', CERTIFICATE_PATH + '/client.key'))
##        socketIO = SocketIO(temp_server_IP,int(configvalues['server_port']),MainNamespace,verify='D:\\CA_BUNDLE\\server.crt',cert=('D:\\CA_BUNDLE\\client.crt', 'D:\\CA_BUNDLE\\client.key'))
        ##socketIO = SocketIO('localhost',8124)
##        socketIO.send('I am ready to process the request')
        socketIO.emit('news')
        socketIO.emit('focus')
        socketIO.emit('debugTestCase')
        socketIO.emit('executeTestSuite')
        socketIO.emit('LAUNCH_DESKTOP')
        socketIO.emit('LAUNCH_SAP')
        socketIO.emit('LAUNCH_MOBILE')
        socketIO.emit('wsdl_listOfOperation')
        socketIO.emit('wsdl_ServiceGenerator')
        socketIO.emit('LAUNCH_MOBILE_WEB')
        socketIO.emit('LAUNCH_OEBS')
        socketIO.emit('webscrape')
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
##                    self.wxObject.continue_debugbutton.Show()
##                    self.wxObject.continuebutton.Show()
##                    self.wxObject.continue_debugbutton.Enable()
##                    self.wxObject.continuebutton.Enable()

                    if self.wxObject.choice=='RunfromStep':
                        self.wxObject.breakpoint.Enable()
                        try:
                            runfrom_step=self.wxObject.breakpoint.GetValue()
                            runfrom_step=int(runfrom_step)
                        except Exception as e:
                            runfrom_step=0
                self.wxObject.rbox.Disable()
            else:
                self.wxObject.rbox.Disable()







##

            self.wxObject.breakpoint.Disable()
##            controller.kill_process()
            self.con = controller.Controller()
            self.wxObject.terminatebutton.Enable()
            self.con.configvalues=configvalues
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
            self.wxObject.breakpoint.Enable()
            self.wxObject.cancelbutton.Enable()
            self.wxObject.terminatebutton.Disable()
##            self.wxObject.continuebutton.Hide()
##            self.wxObject.continue_debugbutton.Hide()
            self.wxObject.mythread=None
            import handler
            testcasename = handler.testcasename
            if self.action==DEBUG:
                if self.wxObject.debugwindow != None:
                    self.wxObject.debugwindow.Close()
                if len(testcasename) > 0:
                    socketIO.emit('result_debugTestCase',status)
                else:
                    socketIO.emit('result_debugTestCaseWS',status)
            elif self.action==EXECUTE:
#                if len(testcasename) > 0:
#                    socketIO.emit('result_executeTestSuite',status)
            #  To check for empty testcase Bug #246 (Himanshu)
                socketIO.emit('result_executeTestSuite',status)
        except Exception as e:
            print e
            status=TERMINATE
            if self.action==DEBUG:
##                if self.wxObject.debugwindow != None:
##                    self.wxObject.debugwindow.Close()
                socketIO.emit('result_debugTestCase',status)
            elif self.action==EXECUTE:
                socketIO.emit('result_executeTestSuite',status)
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
                   pos=(300, 150),  size=(800, 730),style=wx.DEFAULT_FRAME_STYLE & ~ (wx.MAXIMIZE_BOX)  )
##        self.SetBackgroundColour(   (245,222,179))
        self.SetBackgroundColour('#e6e7e8')
##        self.ShowFullScreen(True,wx.ALL)
##        self.SetBackgroundColour('#D0D0D0')
        self.logfilename_error_flag = False

		#747 Screenshot path flag (Himanshu)
        self.screenshotPath_error_flag = False

        self.debugwindow = None
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
        self.iconpath = IMAGES_PATH +"/slk.ico"

        """
        Creating Root Logger using logger file config and setting logfile path,which is in config.json

        """
        try:
            logfilename = configvalues["logFile_Path"].replace("\\","\\\\")
            logging.config.fileConfig(LOGCONFIG_PATH,defaults={'logfilename': logfilename},disable_existing_loggers=False)
        except Exception as e:
            self.logfilename_error_flag = True

        self.logger = logging.getLogger("Nineteen68")

        """
        #747 Screenshot path validity check (Himanshu)

        """
        log.info('Started')
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.CRITICAL)
        if not(jsonSyntaxErrorFlag):
            spath = configvalues['screenShot_PathName']
            self.screenshotPath_error_flag = False
            if not os.path.exists(spath):
                self.screenshotPath_error_flag = True

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
        connect_img=wx.Image(IMAGES_PATH +"/connect.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.connectbutton = wx.BitmapButton(self.panel, bitmap=connect_img,pos=(10, 10), size=(100, 25))
##        self.connectbutton = wx.Button(self.panel, label="Connect" ,pos=(10, 10), size=(100, 28))
        self.connectbutton.Bind(wx.EVT_BUTTON, self.OnNodeConnect)
        self.connectbutton.SetToolTip(wx.ToolTip("Connect to node Server"))
        self.log = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(12, 38), size=(760,500), style = wx.TE_MULTILINE|wx.TE_READONLY)
        font1 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL,  False, u'Consolas')
        self.log.SetForegroundColour((0,50,250))
        self.log.SetFont(font1)

        self.schedule = wx.CheckBox(self.panel, label = 'Schedule',pos=(120, 10), size=(100, 25))
        self.schedule.SetToolTip(wx.ToolTip("Enable Scheduling Mode"))
        self.schedule.Bind(wx.EVT_CHECKBOX,self.onChecked_Schedule)
        self.schedule.Disable()
        self.schedule.Hide()


        box.Add(self.log, 1, wx.ALL|wx.EXPAND, 5)
##        size=(90, 28)

        #Radio buttons
        lblList = ['Normal', 'Stepwise', 'RunfromStep']
        self.rbox = wx.RadioBox(self.panel,label = 'Debug options', pos = (10, 548), choices = lblList ,size=(300, 100),
        majorDimension = 1, style = wx.RA_SPECIFY_ROWS)

##        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)
        self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)
##        self.rbox.SetBackgroundColour('#9f64e2')

##        paly_img = wx.Image("play.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        terminate_img=wx.Image(IMAGES_PATH +"/terminate.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
##        step_img=wx.Image("step.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()


##        self.continue_debugbutton = wx.StaticBitmap(self.rbox, -1, wx.Bitmap("play.png", wx.BITMAP_TYPE_ANY), (75, 50), (35, 28))
##        self.continue_debugbutton.Bind(wx.EVT_LEFT_DOWN, self.Resume)
##        self.continue_debugbutton.SetToolTip(wx.ToolTip("To continue the execution"))
##        self.continue_debugbutton.Hide()
##
##
##
##        self.continuebutton = wx.StaticBitmap(self.rbox, -1, wx.Bitmap("step.png", wx.BITMAP_TYPE_ANY), (105, 50), (35, 28))
##        self.continuebutton.Bind(wx.EVT_LEFT_DOWN, self.OnContinue)
##        self.continuebutton.SetToolTip(wx.ToolTip("To Resume the execution "))
##        self.continuebutton.Hide()




        self.breakpoint = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(230, 598), size=(60,20), style = wx.TE_RICH)
        box.Add(self.breakpoint, 1, wx.ALL|wx.EXPAND, 5)
        self.breakpoint.Disable()


        killprocess_img = wx.Image(IMAGES_PATH +"/killStaleProcess.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.cancelbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"/killStaleProcess.png", wx.BITMAP_TYPE_ANY), (360, 548), (50, 40))
        self.cancelbutton.Bind(wx.EVT_LEFT_DOWN, self.OnExit)
        self.cancelbutton.SetToolTip(wx.ToolTip("To kill Stale process"))
        self.cancel_label=wx.StaticText(self.panel, -1, 'Kill Stale Process', (340, 600), (100, 70))

        self.terminatebutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"/terminate.png", wx.BITMAP_TYPE_ANY), (470, 548), (50, 40))
        self.terminatebutton.Bind(wx.EVT_LEFT_DOWN, self.OnTerminate)
        self.terminatebutton.SetToolTip(wx.ToolTip("To Terminate the execution"))
        self.terminate_label=wx.StaticText(self.panel, -1, 'Terminate', (470, 600), (100, 70))




        self.clearbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"/clear.png", wx.BITMAP_TYPE_ANY), (590, 548), (50, 40))
        self.clearbutton.Bind(wx.EVT_LEFT_DOWN, self.OnClear)
        self.clearbutton.SetToolTip(wx.ToolTip("To clear the console area"))
        self.clear_label=wx.StaticText(self.panel, -1, 'Clear', (600, 600), (100, 70))







        self.Bind(wx.EVT_CLOSE, self.OnClose)

        box.AddStretchSpacer()



        # redirect text here
        redir=RedirectText(self.log)
        sys.stdout=redir
        self.panel.SetSizer(self.sizer)
        self.Centre()
        style = self.GetWindowStyle()
        self.Show()
		#747 disable buttons if any flag raised (Himanshu)
        if (self.logfilename_error_flag or self.screenshotPath_error_flag):
            self.cancelbutton.Disable()
            self.terminatebutton.Disable()
            self.clearbutton.Disable()
            self.connectbutton.Disable()
            self.rbox.Disable()

    """

    Modifying Logger and Handlers Level dynamically without creating a new logger object
    When logging level is changed from Client window using "File" button.

    """

    def menuhandler(self, event):
        id = event.GetId()

        #When user selects INFO level
        if id == 100:
            logger.print_on_console( '--Logger level : INFO selected--')
            log.info('--Logger level : INFO selected--')
            logging.getLogger().setLevel(logging.INFO)
            for handler in logging.root.handlers[:]:
                    handler.setLevel(logging.INFO)
        #When user selects DEBUG level
        elif id == 101:
            logger.print_on_console( '--Logger level : DEBUG selected--')
            log.info('--Logger level : DEBUG selected--')
            logging.getLogger().setLevel(logging.DEBUG)
            for handler in logging.root.handlers[:]:
                handler.setLevel(logging.DEBUG)
        #When user selects ERROR level
        elif id ==102:
            logger.print_on_console( '--Logger level : ERROR selected--')
            log.info( '--Logger level : ERROR selected--')
            logging.getLogger().setLevel(logging.ERROR)
            for handler in logging.root.handlers[:]:
                    handler.setLevel(logging.ERROR)

##    def OnRadiogroup(self, e):
##        rb = e.GetEventObject()
##        print rb.GetLabel(),' is clicked from Radio Group'


    def onChecked_Schedule(self, e):
        mode=self.schedule.GetValue()
        global socketIO
        socketIO.emit('reconnect',mode)


    def onRadioBox(self,e):
        self.choice=self.rbox.GetStringSelection()
        print self.choice,' is Selected'

        if self.choice == 'Normal':
            self.breakpoint.Clear()
            self.breakpoint.Disable()
            if self.debugwindow != None:
                self.debugwindow.Close()
                self.debugwindow = None


        self.debug_mode=False
        self.breakpoint.Disable()
        if self.choice in ['Stepwise','RunfromStep']:
            self.debug_mode=True
##            if self.debugwindow == None:
##                self.debugwindow = DebugWindow(parent = None,id = -1, title="Debugger")
##            self.continue_debugbutton.Show()
##            self.continuebutton.Show()
            if self.choice=='RunfromStep':
                self.breakpoint.Enable()
            else:
                self.breakpoint.Clear()
                self.breakpoint.Disable()

##            if self.mythread==None:
##                self.continue_debugbutton.Disable()
##                self.continuebutton.Disable()
##        else:
##            self.continuebutton.Hide()
##            self.continue_debugbutton.Hide()








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
        controller.kill_process()
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
##        self.continuebutton.Show()


    def Resume(self, event):
        logger.print_on_console('Event Triggered to Resume Debug')
        log.info('Event Triggered to Resume Debug')
        controller.pause_flag=False
        self.mythread.resume(False)
##        self.continuebutton.Hide()
##        self.continue_debugbutton.Hide()



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
        #Close the debug window
        if self.debugwindow != None:
            self.debugwindow.Close()
            self.debugwindow = None
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

##    def OnNodeConnect(self,event):
##        self.mythread = SocketThread(self)
##        self.connectbutton.Disable()

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
        try:
            port = int(configvalues['server_port'])
            conn  = httplib.HTTPConnection(configvalues['server_ip'],port)
            conn.connect()
            conn.close()
            self.mythread = SocketThread(self)
            self.connectbutton.Disable()
##            self.schedule.Enable()
        except Exception as e:
            print 'Forbidden request, Connection refused, please check the server ip and server port in Config.json, and restart the client window.'
            #747 Disable buttons if port or ip is invalid in config.json (Himanshu)
            log.info('Forbidden request, Connection refused, please check the server ip and server port in Config.json, and restart the client window.')
            self.cancelbutton.Disable()
            self.terminatebutton.Disable()
            self.clearbutton.Disable()
            self.connectbutton.Disable()
            self.rbox.Disable()

    def test(self,event):
##        print 'Self',self
        global mobileScrapeFlag
        global qcConFlag
        global mobileWebScrapeFlag
        global desktopScrapeFlag
        global sapScrapeFlag
        global debugFlag
        global socketIO
        global browsername
        global action
        global data
        global oebsScrapeFlag
        if mobileScrapeFlag==True:
##            global socketIO
            self.new = mobileScrapeObj.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Mobile Scrapper",filePath = browsername,socketIO = socketIO)
            mobileScrapeFlag=False
        elif qcConFlag==True:
            #print 'For QC'
##            global socketIO
            self.new = qcConObj.QcWindow(parent = None,id = -1, title="SLK Nineteen68 - Mobile Scrapper",filePath = qcdata,socketIO = socketIO)
            qcConFlag=False
        elif mobileWebScrapeFlag==True:
##            global socketIO
            self.new = mobileWebScrapeObj.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Mobile Scrapper",browser = browsername,socketIO = socketIO)
            mobileWebScrapeFlag=False
        elif desktopScrapeFlag==True:
##            global socketIO
            self.new = desktopScrapeObj.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Desktop Scrapper",filePath = browsername,socketIO = socketIO)
            desktopScrapeFlag=False
            browsername = ''
        elif sapScrapeFlag==True:
##            global socketIO
            self.new = sapScrapeObj.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - SAP Scrapper",filePath = browsername,socketIO = socketIO)
            sapScrapeFlag=False
        elif oebsScrapeFlag==True:
##            global socketIO
            self.new = oebsScrapeObj.ScrapeDispatcher(parent = None,id = -1, title="SLK Nineteen68 - Oebs Scrapper",filePath = browsername,socketIO = socketIO)
            oebsScrapeFlag=False
        elif debugFlag == True:
            self.debugwindow = DebugWindow(parent = None,id = -1, title="Debugger")
            debugFlag = False
        else:
##            global browsername
            browsernumbers = ['1','2','3','6']
            if browsername in browsernumbers:
                print 'Browser name : ',browsername
                con = controller.Controller()
                con.get_all_the_imports('Web')
                con.get_all_the_imports('WebScrape')
                import Nineteen68_WebScrape
##                global socketIO
                self.new = Nineteen68_WebScrape.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Web Scrapper",browser = browsername,socketIO = socketIO,action=action,data=data)
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




class DebugWindow(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self, parent,id, title):
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150),  size=(200, 75) ,style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX) )
        self.SetBackgroundColour('#e6e7e8')
##        style = wx.CAPTION|wx.CLIP_CHILDREN
        curdir = os.getcwd()
        self.iconpath = IMAGES_PATH +"/slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        self.panel = wx.Panel(self)
        #Radio buttons
##        lblList = ['Normal', 'Stepwise', 'RunfromStep']
##        self.rbox = wx.RadioBox(self.panel,label = 'Debug options', pos = (10, 548), choices = lblList ,size=(300, 100),
##        majorDimension = 1, style = wx.RA_SPECIFY_ROWS)

##        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)
##        self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)
##        self.rbox.SetBackgroundColour('#9f64e2')

        paly_img = wx.Image(IMAGES_PATH +"/play.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        terminate_img=wx.Image(IMAGES_PATH +"/terminate.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        step_img=wx.Image(IMAGES_PATH +"/step.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()


        self.continue_debugbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"/play.png", wx.BITMAP_TYPE_ANY), (65, 15), (35, 28))
        self.continue_debugbutton.Bind(wx.EVT_LEFT_DOWN, self.Resume)
        self.continue_debugbutton.SetToolTip(wx.ToolTip("To continue the execution"))
##        self.continue_debugbutton.Hide()



        self.continuebutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"/step.png", wx.BITMAP_TYPE_ANY), (105, 15), (35, 28))
        self.continuebutton.Bind(wx.EVT_LEFT_DOWN, self.OnContinue)
        self.continuebutton.SetToolTip(wx.ToolTip("To Resume the execution "))
##        self.continuebutton.Hide()

        self.Centre()
        style = self.GetWindowStyle()
        self.SetWindowStyle( style|wx.STAY_ON_TOP )
        wx.Frame(self.panel, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Show()


    def Resume(self, event):
        logger.print_on_console('Event Triggered to Resume Debug')
        log.info('Event Triggered to Resume Debug')
        controller.pause_flag=False
        wxObject.mythread.resume(False)
        self.Close()
        wxObject.debugwindow = None
##        self.continuebutton.Hide()
##        self.continue_debugbutton.Hide()



    #----------------------------------------------------------------------
    def OnContinue(self, event):
        logger.print_on_console('Event Triggered to Resume')
        log.info('Event Triggered to Resume')
        self.resume(True)

    #----------------------------------------------------------------------
    def resume(self,debug_mode):
        controller.pause_flag=False
        wxObject.mythread.resume(debug_mode)

    def OnExit(self, event):
        self.Close()
        wxObject.debugwindow = None

#----------------------------------------------------------------------
def main():
	#747 json syntax error flag (Himanshu)
    global jsonSyntaxErrorFlag
    app = wx.App()
    cw = ClientWindow()
    print( '*******************************************************************************************************')
    print( '=========================================Nineteen68 Client Window======================================')
    print( '*******************************************************************************************************')
	#747 user friendly messages if any flag raised (Himanshu)
    if jsonSyntaxErrorFlag:
        logger.print_on_console( "[Error]: Syntax error in config.json file, please check and restart the client window.")
        log.info("[Error]: Syntax error in config.json file, and please check and restart the client window.")
        jsonSyntaxErrorFlag = False
        app.MainLoop()
    elif cw.logfilename_error_flag:
        logger.print_on_console( "[Error]: Please provide a valid logfile path in config.json file and restart the client window.")
        log.info("[Error]: Please provide a valid logfile path in config.json file and restart the client window.")
        cw.logfilename_error_flag = False
        app.MainLoop()
    elif cw.screenshotPath_error_flag:
        logger.print_on_console( "[Error]: Please provide a valid Screenshot path in config.json file and restart the client window.")
        log.info("[Error]: Please provide a valid Screenshot path in config.json file and restart the client window.")
        cw.screenshotPath_error_flag = False
        app.MainLoop()
    else:
        app.MainLoop()

if __name__ == "__main__":
    main()
