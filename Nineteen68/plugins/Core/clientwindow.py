import wx
import sys
import os
import time
import httplib
import logging
import logging.config
import base64
import platform
import uuid
from datetime import datetime
import core_utils
import logger
import threading
from socketIO_client import SocketIO,BaseNamespace
from constants import *
import controller
import readconfig
import httplib
import json
import socket


log = logging.getLogger('clientwindow.py')
wxObject = None
browsername = None
qcdata = None
soc=None
qcConFlag=False
desktopScrapeFlag=False
sapScrapeFlag=False
mobileScrapeFlag=False
mobileWebScrapeFlag=False
debugFlag = False
oebsScrapeFlag = False
socketIO = None
allow_connect = False
icesession = None
plugins_list = []
configvalues = None
IMAGES_PATH = os.environ["NINETEEN68_HOME"] + "/Nineteen68/plugins/Core/Images"
CERTIFICATE_PATH = os.environ["NINETEEN68_HOME"] + "/Scripts/CA_BUNDLE"
LOGCONFIG_PATH = os.environ["NINETEEN68_HOME"] + "/logging.conf"


class MainNamespace(BaseNamespace):
    def on_message(self, *args):
        global action,wxObject,browsername,desktopScrapeFlag,allow_connect

        if(str(args[0]) == 'connected'):
            if(allow_connect):
                logger.print_on_console('Normal Mode: Connection to the Nineteen68 Server established')
                wxObject.schedule.Enable()
                log.info('Normal Mode: Connection to the Nineteen68 Server established')
            else:
                if socketIO != None:
                    log.info('Closing the socket')
                    socketIO.disconnect()
                    log.info(socketIO)

        elif(str(args[0]) == 'schedulingEnabled'):
            logger.print_on_console('Schedule Mode Enabled')
            log.info('Schedule Mode Enabled')

        elif(str(args[0]) == 'schedulingDisabled'):
            logger.print_on_console('Schedule Mode Disabled')
            log.info('Schedule Mode Disabled')

        elif(str(args[0]) == 'checkConnection'):
            try:
                global icesession,plugins_list
                ice_ndac_key = "".join(['a','j','k','d','f','i','H','F','E','o','w','#','D','j',
                    'g','L','I','q','o','c','n','^','8','s','j','p','2','h','f','Y','&','d'])
                core_utils_obj = core_utils.CoreUtils()
                response = json.loads(core_utils_obj.unwrap(str(args[1]), ice_ndac_key))
                plugins_list = response['plugins']
                err_res = None
                if(response['id'] != icesession['ice_id'] and response['connect_time'] != icesession['connect_time']):
                    err_res="Invalid response received"
                if(response['res'] != 'success'):
                    if(response.has_key('err_msg')):
                        err_res=response['err_msg']
                if(err_res is not None):
                    wxObject.schedule.Disable()
                    ##if socketIO != None:
                    ##    log.info('Closing the socket')
                    ##    socketIO.disconnect()
                    ##    log.info(socketIO)
                    logger.print_on_console(err_res)
                    log.info(err_res)
                else:
                    allow_connect = True
                    wxObject.connectbutton.SetBitmapLabel(wxObject.disconnect_img)
                    wxObject.connectbutton.SetName("disconnect")
                    wxObject.connectbutton.SetToolTip(wx.ToolTip("Disconnect from Nineteen68 Server"))
                    controller.disconnect_flag=False
                wxObject.connectbutton.Enable()
            except Exception as e:
                logger.print_on_console('Error while checking connection request')
                log.info('Error while checking connection request')
                log.error(e)

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

    def on_focus(self, *args):
        appType=args[2]
        appType=appType.lower()
        if appType==APPTYPE_WEB:
            import highlight
            light =highlight.Highlight()
            res = light.highlight(args,None,None)
            logger.print_on_console('Highlight result: '+str(res))
        if appType==APPTYPE_MOBILE.lower():
            import highlight_MW
            light =highlight_MW.Highlight()
            res = light.highlight(args,None,None)
            logger.print_on_console('Highlight result: '+str(res))
        if appType==APPTYPE_DESKTOP_JAVA.lower():
            con =controller.Controller()
            con.get_all_the_imports('Oebs')
            import utils
            light =utils.Utils()
            res = light.highlight(args[0],args[1])
            logger.print_on_console('Highlight result: '+str(res))
        elif appType==APPTYPE_DESKTOP.lower():
            con =controller.Controller()
            con.get_all_the_imports('Desktop2')
            import desktop_highlight
            highlightObj=desktop_highlight.highLight()
            highlightObj.highLiht_element(args[0],args[1])
        elif appType==APPTYPE_SAP.lower():
            con =controller.Controller()
            con.get_all_the_imports('SAP')
            import sap_highlight
            highlightObj=sap_highlight.highLight()
##            i = args[0].rfind(",")
##            var = args[0][:i]
            highlightObj.highlight_element(args[0])


    def on_executeTestSuite(self, *args):
        global wxObject,socketIO
        args=list(args)
        socketIO.emit('return_status_executeTestSuite','success')
        wxObject.mythread = TestThread(wxObject,EXECUTE,args[0],wxObject.debug_mode)

    def on_debugTestCase(self, *args):
        global wxObject
        args=list(args)
        wxObject.mythread = TestThread(wxObject,DEBUG,args[0],wxObject.debug_mode)
        wxObject.choice=wxObject.rbox.GetStringSelection()
        logger.print_on_console(str(wxObject.choice)+' is Selected')
        if wxObject.choice == 'Normal':
            wxObject.killDebugWindow()
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
            logger.print_on_console('Error in SAP')
            log.error(e)

    def on_qclogin(self, *args):
        global qcdata
        global soc
        global socketIO
        server_data=''
        data_stream=None
        client_data=None
        try:
            if platform.system() == "Windows":
                if len(args) > 0:
                    qcdata = args[0]
                    if soc is None:
                        import subprocess
                        path = os.environ["NINETEEN68_HOME"] + "/Nineteen68/plugins/Qc/QcController.exe"
                        pid = subprocess.Popen(path, shell=True)
                        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        soc.connect(("localhost",10000))

                    data_to_send = json.dumps(qcdata).encode('utf-8')
                    data_to_send+='#E&D@Q!C#'
                    soc.send(data_to_send)
                    while True:
                        data_stream= soc.recv(1024)
                        server_data+=data_stream
                        if '#E&D@Q!C#' in server_data:
                            break
                    client_data= server_data[:server_data.find('#E&D@Q!C#')]
                    if('Fail' in client_data):
                        logger.print_on_console('Error occurred in QC')
                    socketIO.emit('qcresponse',client_data)
                else:
                    socketIO.emit('qcresponse','Error:data recevied empty')
            else:
                 socketIO.emit('qcresponse','Error:Failed in running Qc')
        except Exception as e:
            log.error(e)
            socketIO.emit('qcresponse','Error:Qc Operations')

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
        if platform.system()=='Darwin':
            con.get_all_the_imports('Mobility/MobileWeb')
        else:
            con.get_all_the_imports('Mobility')
        import ninteen_68_mobile_web_scrape
        mobileWebScrapeObj=ninteen_68_mobile_web_scrape
        mobileWebScrapeFlag=True
        wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

    def on_LAUNCH_OEBS(self, *args):
        global oebsScrapeObj,oebsScrapeFlag
        con = controller.Controller()
        global browsername
        browsername = args[0]
        con =controller.Controller()
        con.get_all_the_imports('Oebs')
        import scrape_dispatcher
        oebsScrapeObj=scrape_dispatcher
        oebsScrapeFlag=True
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
        log.debug(response)
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
                if not (os.path.exists(path)):
                    data_URIs.append(None)
                    logger.print_on_console("Error while rendering Screenshot: File \""+path+"\" not found!")
                    log.error("File \""+path+"\" not found!")
                else:
                    encoded_string = ''
                    with open(path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                    base64_data=encoded_string.encode('UTF-8').strip()
                    data_URIs.append(base64_data)
            socketIO.emit('render_screenshot',data_URIs)
        except Exception as e:
            logger.print_on_console('Error while sending screenshot data')
            socketIO.emit('render_screenshot','fail')
            log.error(e)

    def on_webCrawlerGo(self,*args):
        try:
            con = controller.Controller()
            con.get_all_the_imports('WebOcular')
            import webocular
            wobj = webocular.Webocular()
            args=list(args)
            global socketIO
            #args[0] is URL, args[1] is level, args[2] is agent
            wobj.runCrawler(args[0],args[1],args[2],socketIO,wxObject)
        except Exception as e:
            logger.print_on_console('Error in Webocular')
            log.error(e)

    def on_jiralogin(self,*args):
        try:
            con = controller.Controller()
            con.get_all_the_imports('Jira')
            import jiracontroller
            obj = jiracontroller.JiraWindow()
            global socketIO
            if args[0] == JIRA_ACTION_1:
                data = args[1]
                obj.getAllAutoDetails(data,socketIO)
            elif args[0] == JIRA_ACTION_2:
                data = args[1]
                obj.createIssue(data,socketIO)
        except Exception as e:
            logger.print_on_console('Exception in jira emit')
            log.error(e)

    def on_update_screenshot_path(self,*args):
        spath=args[0]
        import constants
        if(platform.system()=='Darwin'):
            spath=spath["mac"]
        else:
            spath=spath["default"]
        if len(spath) != 0 and os.path.exists(spath):
            constants.SCREENSHOT_PATH=spath
        else:
            constants.SCREENSHOT_PATH="Disabled"
            logger.print_on_console("Screenshot capturing disabled since user does not have sufficient privileges for screenshot folder\n")
            log.info("Screenshot capturing disabled since user does not have sufficient privileges for screenshot folder\n")


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
        global socketIO, icesession
        server_port = int(configvalues['server_port'])
        server_IP = configvalues['server_ip']
        server_cert = configvalues['server_cert']
        if configvalues.has_key("ignore_server_certificate"):
            server_cert = False
        else:
            if os.path.exists(server_cert) == False:
                server_cert = CERTIFICATE_PATH +'/server.crt'
        client_cert = (CERTIFICATE_PATH + '/client.crt', CERTIFICATE_PATH + '/client.key')
        temp_server_IP = 'https://' + server_IP
        key='USERNAME'
        if(not(os.environ.has_key(key))):
            key='USER'
        username=str(os.environ[key]).lower()
        core_utils_obj = core_utils.CoreUtils()
        icesession = {
            'ice_id':str(uuid.uuid4()),
            'connect_time':str(datetime.now()),
            'username':username
        }
        ice_ndac_key = "".join(['a','j','k','d','f','i','H','F','E','o','w','#','D','j',
            'g','L','I','q','o','c','n','^','8','s','j','p','2','h','f','Y','&','d'])
        icesession_enc = core_utils_obj.wrap(json.dumps(icesession), ice_ndac_key)
        params={'username':username,'icesession':icesession_enc}
        socketIO = SocketIO(temp_server_IP,server_port,MainNamespace,verify=server_cert,cert=client_cert,params=params)
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
            time.sleep(2)
##            controller.kill_process()
            self.con = controller.Controller()
            self.con.conthread=self
            #Removed breakpoint
##            value= self.wxObject.breakpoint.GetValue()
            value=''
            status = self.con.invoke_parralel_exe(EXECUTE,value,self)
            if status==TERMINATE:
                logger.print_on_console('---------Termination Completed-------')
            else:
                logger.print_on_console('***SUITE EXECUTION COMPLETED***')
##            self.wxObject.debugbutton.Enable()
##            self.wxObject.executebutton.Enable()
            self.wxObject.cancelbutton.Enable()
            socketIO.emit('result_executeTestSuite',status)
        except Exception as m:
            log.error(m)


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
            self.wxObject.cancelbutton.Disable()
            self.wxObject.terminatebutton.Enable()
            runfrom_step=1
            if self.action==DEBUG:
                self.debug_mode=False
                self.wxObject.breakpoint.Disable()
                if self.wxObject.choice in ['Stepwise','RunfromStep']:
                    self.debug_mode=True
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
            self.wxObject.breakpoint.Disable()
            self.con = controller.Controller()
            self.wxObject.terminatebutton.Enable()
            self.con.configvalues=configvalues
            self.con.exception_flag=(str(configvalues["exception_flag"]).strip().lower()=="true")
            status = ''
            apptype = ''
            if(self.action == DEBUG):
                apptype = (self.json_data)[0]['apptype']
            else:
                apptype =(self.json_data)['apptype']
            if(apptype == "DesktopJava"):
                apptype = "oebs"
            if(apptype.lower() not in plugins_list):
                logger.print_on_console('This app type is not part of the license.')
                status=TERMINATE
            else:
                status = self.con.invoke_controller(self.action,self,self.debug_mode,runfrom_step,self.json_data,self.wxObject,socketIO,soc)

            logger.print_on_console('Execution status',status)

            if status==TERMINATE:
                logger.print_on_console('---------Termination Completed-------')

            #Removed execute,debug button
            self.wxObject.breakpoint.Clear()
            self.wxObject.rbox.Enable()
            self.wxObject.breakpoint.Enable()
            self.wxObject.cancelbutton.Enable()
            self.wxObject.terminatebutton.Disable()
            self.wxObject.mythread=None
            import handler
            testcasename = handler.testcasename
            if self.action==DEBUG:
                self.wxObject.killDebugWindow()
                if (len(testcasename) > 0 or apptype.lower() not in plugins_list):
                    socketIO.emit('result_debugTestCase',status)
                else:
                    socketIO.emit('result_debugTestCaseWS',status)
            elif self.action==EXECUTE:
                socketIO.emit('result_executeTestSuite',status)
        except Exception as e:
            log.error(e)
            status=TERMINATE
            if socketIO is not None:
                if self.action==DEBUG:
                    self.wxObject.killDebugWindow()
                    socketIO.emit('result_debugTestCase',status)
                elif self.action==EXECUTE:
                    socketIO.emit('result_executeTestSuite',status)



class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        wx.CallAfter(self.out.AppendText, string)



class ClientWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None,id=-1, title="ICE Engine",
                   pos=(300, 150),  size=(800, 730),style=wx.DEFAULT_FRAME_STYLE & ~ (wx.MAXIMIZE_BOX)  )
        self.SetBackgroundColour('#e6e7e8')
        ##self.ShowFullScreen(True,wx.ALL)
        ##self.SetBackgroundColour('#D0D0D0')
        self.logfilename_error_flag = False
        self.debugwindow = None
        self.new = None
        self.id =id
        self.mainclass = self
        self.mythread = None
        self.action=''
        self.debug_mode=False
        self.choice='Normal'
        global wxObject
        wxObject = self
        self.iconpath = IMAGES_PATH +"/slk.ico"
        self.connect_img=wx.Image(IMAGES_PATH +"/connect.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.disconnect_img=wx.Image(IMAGES_PATH +"/disconnect.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        """
        Creating Root Logger using logger file config and setting logfile path,which is in config.json
        """
        try:
            logfilename = configvalues["logFile_Path"].replace("\\","\\\\")
            logging.config.fileConfig(LOGCONFIG_PATH,defaults={'logfilename': logfilename},disable_existing_loggers=False)
        except Exception as e:
            self.logfilename_error_flag = True
            log.error(e)

        self.logger = logging.getLogger("Nineteen68")
        log.info('Started')
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.CRITICAL)

        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(6, 5)
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        box = wx.BoxSizer(wx.VERTICAL)
        self.menubar = wx.MenuBar()
        self.fileMenu = wx.Menu()
        #own event
        self.Bind( wx.EVT_CHOICE, self.test)
        ##self.Bind(wx.EVT_CHOICE, self.debug)
        ##self.Bind(wx.EVT_CLOSE, self.closeScrapeWindow)
        #own event
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
        self.connectbutton = wx.BitmapButton(self.panel, bitmap=self.connect_img,pos=(10, 10), size=(100, 25), name='connect')
        self.connectbutton.Bind(wx.EVT_BUTTON, self.OnNodeConnect)
        self.connectbutton.SetToolTip(wx.ToolTip("Connect to Nineteen68 Server"))
        self.log = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(12, 38), size=(760,500), style = wx.TE_MULTILINE|wx.TE_READONLY)
        font1 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL,  False, u'Consolas')
        self.log.SetForegroundColour((0,50,250))
        self.log.SetFont(font1)

        self.schedule = wx.CheckBox(self.panel, label = 'Schedule',pos=(120, 10), size=(100, 25))
        self.schedule.SetToolTip(wx.ToolTip("Enable Scheduling Mode"))
        self.schedule.Bind(wx.EVT_CHECKBOX,self.onChecked_Schedule)
        self.schedule.Disable()

        box.Add(self.log, 1, wx.ALL|wx.EXPAND, 5)

        #Radio buttons
        lblList = ['Normal', 'Stepwise', 'RunfromStep']
        self.rbox = wx.RadioBox(self.panel,label = 'Debug options', pos = (10, 548), choices = lblList ,size=(300, 100),
        majorDimension = 1, style = wx.RA_SPECIFY_ROWS)

        self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)
        ##self.rbox.SetBackgroundColour('#9f64e2')
        self.breakpoint = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(230, 598), size=(60,20), style = wx.TE_RICH)
        box.Add(self.breakpoint, 1, wx.ALL|wx.EXPAND, 5)
        self.breakpoint.Disable()

        self.cancelbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"/killStaleProcess.png", wx.BITMAP_TYPE_ANY), wx.Point(360, 555), wx.Size(50, 42))
        self.cancelbutton.Bind(wx.EVT_LEFT_DOWN, self.OnKillProcess)
        self.cancelbutton.SetToolTip(wx.ToolTip("To kill Stale process"))
        self.cancel_label=wx.StaticText(self.panel, -1, 'Kill Stale Process', wx.Point(340, 600), wx.Size(100, 70))

        self.terminatebutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"/terminate.png", wx.BITMAP_TYPE_ANY), wx.Point(475, 555), wx.Size(50, 42))
        self.terminatebutton.Bind(wx.EVT_LEFT_DOWN, self.OnTerminate)
        self.terminatebutton.SetToolTip(wx.ToolTip("To Terminate the execution"))
        self.terminate_label=wx.StaticText(self.panel, -1, 'Terminate', wx.Point(475, 600), wx.Size(100, 70))

        self.clearbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"/clear.png", wx.BITMAP_TYPE_ANY), wx.Point(590, 555), wx.Size(50, 42))
        self.clearbutton.Bind(wx.EVT_LEFT_DOWN, self.OnClear)
        self.clearbutton.SetToolTip(wx.ToolTip("To clear the console area"))
        self.clear_label=wx.StaticText(self.panel, -1, 'Clear', wx.Point(600, 600), wx.Size(100, 70))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        box.AddStretchSpacer()

        # redirect text here
        redir=RedirectText(self.log)
        sys.stdout=redir
        self.panel.SetSizer(self.sizer)
        self.Centre()
        self.Show()
		#747 disable buttons if any flag raised (Himanshu)
        if (self.logfilename_error_flag):
            self.cancelbutton.Disable()
            self.terminatebutton.Disable()
            self.clearbutton.Disable()
            self.connectbutton.Disable()
            self.rbox.Disable()
        threading.Timer(0.2,self.verifyMACAddress).start()

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

    def onChecked_Schedule(self, e):
        mode=self.schedule.GetValue()
        global socketIO
        socketIO.emit('toggle_schedule',mode)

    def onRadioBox(self,e):
        self.choice=self.rbox.GetStringSelection()
        logger.print_on_console(str(self.choice)+' is Selected')
        if self.choice == 'Normal':
            self.breakpoint.Clear()
            self.breakpoint.Disable()
            self.killDebugWindow()
        self.debug_mode=False
        self.breakpoint.Disable()
        if self.choice in ['Stepwise','RunfromStep']:
            self.debug_mode=True
            ##if self.debugwindow == None:
            ##    self.debugwindow = DebugWindow(parent = None,id = -1, title="Debugger")
            if self.choice=='RunfromStep':
                self.breakpoint.Enable()
            else:
                self.breakpoint.Clear()
                self.breakpoint.Disable()

    def OnClose(self, event):
        controller.terminate_flag=True
        controller.disconnect_flag=True
        global socketIO
        logger.print_on_console('Disconnected from Nineteen68 server')
        if socketIO != None:
            log.info('Sending Socket disconnect request')
            socketIO.emit('unavailableLocalServer')
            socketIO.disconnect()
            del socketIO
            socketIO = None
        self.killDebugWindow()
        self.killScrapeWindow()
        self.Destroy()
        controller.kill_process()
        if platform.system() == "Windows":
            os.system("TASKKILL /F /IM QcController.exe")
        exit()
         # you may also do:  event.Skip()
         # since the default event handler does call Destroy(), too

    def OnKillProcess(self, event):
        controller.kill_process()

    def OnTerminate(self, event, *args):
        self.killDebugWindow()
        scrape_window_open=self.killScrapeWindow()
        if(len(args) > 0 and args[0]=="term_exec"):
            controller.disconnect_flag=True
            print ""
            logger.print_on_console('---------Terminating all active operations-------')
        else:
            logger.print_on_console('---------Termination Started-------')
            if scrape_window_open == True:
                socketIO.emit('scrape','Terminate')
        controller.terminate_flag=True
        #Handling the case where user clicks terminate when the execution is paused
        #Resume the execution
        if controller.pause_flag:
            self.resume(False)

    def OnClear(self,event):
        self.log.Clear()

    def OnNodeConnect(self,event):
        try:
            global socketIO
            name = self.connectbutton.GetName()
            self.connectbutton.Disable()
            if(name == 'connect'):
                port = int(configvalues['server_port'])
                conn = httplib.HTTPConnection(configvalues['server_ip'],port)
                conn.connect()
                conn.close()
                self.mythread = SocketThread(self)
            else:
                self.OnTerminate(event,"term_exec")
                logger.print_on_console('Disconnected from Nineteen68 server')
                if socketIO is not None:
                    log.info('Sending Socket disconnect request')
                    socketIO.emit('unavailableLocalServer')
                    socketIO.disconnect()
                    del socketIO
                    socketIO = None
                self.connectbutton.SetBitmapLabel(self.connect_img)
                self.connectbutton.SetName('connect')
                self.connectbutton.SetToolTip(wx.ToolTip("Connect to Nineteen68 Server"))
                self.schedule.SetValue(False)
                self.schedule.Disable()
                self.connectbutton.Enable()
        except Exception as e:
            emsg="Forbidden request, Connection refused, please check the server ip and server port in Config.json, and restart the client window."
            logger.print_on_console(emsg)
            log.error(emsg)
            self.cancelbutton.Disable()
            self.terminatebutton.Disable()
            self.clearbutton.Disable()
            self.connectbutton.Disable()
            self.rbox.Disable()
            log.error(e)

    def killDebugWindow(self):
        #Close the debug window
        flag=False
        try:
            if (self.debugwindow != None) and (bool(self.debugwindow) != False):
                self.debugwindow.Close()
                flag=True
            self.debugwindow = None
        except Exception as e:
            log.error("Error while killing debug window")
            log.error(e)
        return flag

    def killScrapeWindow(self):
        #Close the scrape window
        flag=False
        try:
            if (self.new != None) and (bool(self.new) != False):
                self.new.Close()
                flag=True
            self.new = None
        except Exception as e:
            log.error("Error while killing scrape window")
            log.error(e)
        return flag

    def test(self,event):
        global mobileScrapeFlag,qcConFlag,mobileWebScrapeFlag,desktopScrapeFlag
        global sapScrapeFlag,debugFlag,browsername,action,oebsScrapeFlag
        global socketIO,data
        if mobileScrapeFlag==True:
            self.new = mobileScrapeObj.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Mobile Scrapper",filePath = browsername,socketIO = socketIO)
            mobileScrapeFlag=False
        elif qcConFlag==True:
            self.new = qcConObj.QcWindow(parent = None,id = -1, title="SLK Nineteen68 - Mobile Scrapper",filePath = qcdata,socketIO = socketIO)
            qcConFlag=False
        elif mobileWebScrapeFlag==True:
            self.new = mobileWebScrapeObj.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Mobile Scrapper",browser = browsername,socketIO = socketIO)
            mobileWebScrapeFlag=False
        elif desktopScrapeFlag==True:
            self.new = desktopScrapeObj.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Desktop Scrapper",filePath = browsername,socketIO = socketIO)
            desktopScrapeFlag=False
            browsername = ''
        elif sapScrapeFlag==True:
            self.new = sapScrapeObj.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - SAP Scrapper",filePath = browsername,socketIO = socketIO)
            sapScrapeFlag=False
        elif oebsScrapeFlag==True:
            self.new = oebsScrapeObj.ScrapeDispatcher(parent = None,id = -1, title="SLK Nineteen68 - Oebs Scrapper",filePath = browsername,socketIO = socketIO)
            oebsScrapeFlag=False
        elif debugFlag == True:
            self.debugwindow = DebugWindow(parent = None,id = -1, title="Debugger")
            debugFlag = False
        else:
            browsernumbers = ['1','2','3','6']
            if browsername in browsernumbers:
                logger.print_on_console('Browser name : '+str(browsername))
                con = controller.Controller()
                con.get_all_the_imports('Web')
                con.get_all_the_imports('WebScrape')
                import Nineteen68_WebScrape
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

    def verifyMACAddress(self):
        flag = False
        core_utils_obj = core_utils.CoreUtils()
        system_mac = core_utils_obj.getMacAddress()
        mac_verification_key = "".join(['N','1','i','1','N','2','e','3','T','5','e','8','E','1','3','n','2','1','S','i','X','t','Y','3','4','e','I','g','H','t','5','5'])
        try:
            with open(CERTIFICATE_PATH+'\license.key', mode='r') as f:
                key = "".join(f.readlines()[1:-1]).replace("\n","").replace("\r","")
                key = core_utils_obj.unwrap(key, mac_verification_key)
                mac_addr = key[36:-36]
                if ("," in mac_addr):
                    mac_addr = mac_addr.split(",")
                else:
                    mac_addr = [mac_addr]
                if(system_mac in mac_addr):
                    flag = True
        except:
            pass
        if not flag:
            logger.print_on_console("Unauthorized: Access denied, system is not registered with Nineteen68")
            self.connectbutton.Disable()
        return flag

class DebugWindow(wx.Frame):
    def __init__(self, parent,id, title):
        wx.Frame.__init__(self, parent, title=title, pos=(300, 150),  size=(200, 75),
            style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX) )
        self.SetBackgroundColour('#e6e7e8')
        ##style = wx.CAPTION|wx.CLIP_CHILDREN
        self.iconpath = IMAGES_PATH +"/slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        self.panel = wx.Panel(self)
        self.continue_debugbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"/play.png", wx.BITMAP_TYPE_ANY), (65, 15), (35, 28))
        self.continue_debugbutton.Bind(wx.EVT_LEFT_DOWN, self.Resume)
        self.continue_debugbutton.SetToolTip(wx.ToolTip("To continue the execution"))
        self.continuebutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"/step.png", wx.BITMAP_TYPE_ANY), (105, 15), (35, 28))
        self.continuebutton.Bind(wx.EVT_LEFT_DOWN, self.OnContinue)
        self.continuebutton.SetToolTip(wx.ToolTip("To Resume the execution "))
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

    def OnContinue(self, event):
        logger.print_on_console('Event Triggered to Resume')
        log.info('Event Triggered to Resume')
        self.resume(True)

    def resume(self,debug_mode):
        controller.pause_flag=False
        wxObject.mythread.resume(debug_mode)

    def OnExit(self, event):
        self.Close()
        wxObject.debugwindow = None
