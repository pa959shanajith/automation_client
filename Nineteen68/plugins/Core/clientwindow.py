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
import requests
import io
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

log = logging.getLogger('clientwindow.py')
wxObject = None
browsername = None
qcdata = None
soc=None
qcConFlag=False
browsercheckFlag=False
chromeFlag=False
firefoxFlag=False
desktopScrapeFlag=False
sapScrapeFlag=False
mobileScrapeFlag=False
mobileWebScrapeFlag=False
debugFlag = False
oebsScrapeFlag = False
irisFlag = False
socketIO = None
allow_connect = False
icesession = None
plugins_list = []
configvalues = None
CONFIG_PATH= os.environ["NINETEEN68_HOME"] + '/Lib/config.json'
IMAGES_PATH = os.environ["NINETEEN68_HOME"] + "/Nineteen68/plugins/Core/Images/"
os.environ["IMAGES_PATH"] = IMAGES_PATH
CERTIFICATE_PATH = os.environ["NINETEEN68_HOME"] + "/Scripts/CA_BUNDLE"
LOGCONFIG_PATH = os.environ["NINETEEN68_HOME"] + "/logging.conf"
DRIVERS_PATH = os.environ["NINETEEN68_HOME"] + "/Drivers"
CHROME_DRIVER_PATH = DRIVERS_PATH + "/chromedriver.exe"
GECKODRIVER_PATH = DRIVERS_PATH + '/geckodriver.exe'

""" Override SocketIO library's warn method used for logging.
    This is needed because this library doesn't gives anything to stdout or stderr
    on exception/warning. Hence Adding custom check and raising exception. Ref #1847.
"""
def socketIO_warn_override(self, msg, *attrs):
    self._log(logging.WARNING, msg, *attrs)
    if ("[SSL: CERTIFICATE_VERIFY_FAILED]" in msg) or ("hostname" in msg and "doesn't match " in msg):
        raise ValueError("[Certifiate Mismatch] "+ msg)
SocketIO._warn = socketIO_warn_override


class MainNamespace(BaseNamespace):
    def on_message(self, *args):
        global action,wxObject,browsername,desktopScrapeFlag,allow_connect,browsercheckFlag

        if(str(args[0]) == 'connected'):
            if(allow_connect):
                logger.print_on_console('Normal Mode: Connection to the Nineteen68 Server established')
                wxObject.schedule.Enable()
                wxObject.cancelbutton.Enable()
                wxObject.terminatebutton.Enable()
                wxObject.clearbutton.Enable()
                wxObject.rbox.Enable()
                if browsercheckFlag == False:
                    browsercheckFlag = check_browser()
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
        data = {}
        if action == 'scrape':
            if str(task) == 'OPEN BROWSER CH':
                browsername = '1'
            elif str(task) == 'OPEN BROWSER IE':
                browsername = '3'
            elif str(task) == 'OPEN BROWSER FX':
                browsername = '2'
            elif str(task) == 'OPEN BROWSER SF':
                browsername = '6'
        elif action == 'compare':
            data['view'] = d['viewString']
            data['scrapedurl'] = d['scrapedurl']
            if str(task) == 'OPEN BROWSER CH':
                browsername = '1'
            elif str(task) == 'OPEN BROWSER IE':
                browsername = '3'
            elif str(task) == 'OPEN BROWSER FX':
                browsername = '2'
        wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

    def on_focus(self, *args):
        appType=args[2]
        appType=appType.lower()
        if appType==APPTYPE_WEB:
            import highlight
            light =highlight.Highlight()
            res = light.perform_highlight(args[0],args[1])
            logger.print_on_console('Highlight result: '+str(res))
        if appType==APPTYPE_MOBILE.lower():
            import highlight_MW
            light =highlight_MW.Highlight()
            res = light.highlight(args,None,None)
            logger.print_on_console('Highlight result: '+str(res))
        if appType==APPTYPE_DESKTOP_JAVA.lower():
            if(not args[0].startswith('iris')):
                con =controller.Controller()
                con.get_all_the_imports('Oebs')
                import utils
                light =utils.Utils()
                res = light.highlight(args[0],args[1])
                logger.print_on_console('Highlight result: '+str(res))
        elif appType==APPTYPE_DESKTOP.lower():
            con =controller.Controller()
            con.get_all_the_imports('Desktop')
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
        browsername = args
        con.get_all_the_imports('Desktop')
        import desktop_scrape
        global desktopScrapeObj
        desktopScrapeObj=desktop_scrape
        global desktopScrapeFlag
        desktopScrapeFlag=True
        wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))

    def on_LAUNCH_SAP(self, *args):
        try:
            con = controller.Controller()
            global browsername
            browsername = args[0]
            con.get_all_the_imports('SAP')
            import sap_scrape
            global sapScrapeObj
            sapScrapeObj=sap_scrape
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
                    if('Fail@f@!l' in client_data):
                        client_data=client_data[:client_data.find('@f@!l')]
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
        import mobile_app_scrape
        global mobileScrapeObj
        mobileScrapeObj=mobile_app_scrape
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
        import mobile_web_scrape
        mobileWebScrapeObj=mobile_web_scrape
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

    def on_generateFlowGraph(self,*args):
        try:
            global socketIO
            con = controller.Controller()
            con.get_all_the_imports('AutomatedPathGenerator')
            import apg
            fg = apg.AutomatedPathGenerator(socketIO)
            args=list(args)
            #args[0] is version, args[1] is filepath
            fg.generate_flowgraph(str(args[0]),str(args[1]))
        except Exception as e:
            log.error(e)
            logger.print_on_console('Exception in generate flowgraph')

    def on_apgOpenFileInEditor(self, *args):
        try:
            global socketIO
            con = controller.Controller()
            con.get_all_the_imports('AutomatedPathGenerator')
            import apg
            fg = apg.AutomatedPathGenerator(socketIO)
            args = list(args)
            # args[0] is Editor name, args[1] is filepath, args[2] is line number
            fg.open_file_in_editor(str(args[0]), str(args[1]), int(args[2]))
        except Exception as e:
            log.error(e)
            logger.print_on_console('Exception in APG Open File In Editor')

    def on_killSession(self,*args):
        global wxObject
        try:
            user = args[0]
            wxObject.OnNodeConnect(wx.EVT_BUTTON)
            msg = 'Connection terminated remotely by ' + user
            logger.print_on_console(msg)
            log.info(msg)
        except Exception as e:
            log.error(e)
            logger.print_on_console('Exception while Remote Disconnect')

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
        if configvalues.has_key("disable_server_cert") and configvalues["disable_server_cert"]=="Yes":
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
        try:
            socketIO = SocketIO(temp_server_IP,server_port,MainNamespace,verify=server_cert,cert=client_cert,params=params)
            socketIO.wait()
        except ValueError as e:
            msg = str(e).replace("[engine.io waiting for connection] ",'').replace("[SSL: CERTIFICATE_VERIFY_FAILED] ",'')
            if "_ssl.c" in msg:
                msg = msg[:msg.index("(_ssl")]
            #msg = msg.replace("[Certifiate Mismatch] ",'')
            logger.print_on_console(msg)
            self.wxobject.connectbutton.Enable()

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
    def __init__(self, appName):
        wx.Frame.__init__(self, parent=None,id=-1, title=appName,
                   pos=(300, 150),  size=(800, 730),style=wx.DEFAULT_FRAME_STYLE & ~ (wx.MAXIMIZE_BOX))
        self.SetBackgroundColour('#e6e7e8')
        ##self.ShowFullScreen(True,wx.ALL)
        ##self.SetBackgroundColour('#D0D0D0')
        self.logfilename_error_flag = False
        # Check if config file is present
        self.is_config_present_flag = os.path.isfile(CONFIG_PATH)
        self.debugwindow = None
        self.scrapewindow = None
        self.pausewindow = None
        self.id =id
        self.mainclass = self
        self.mythread = None
        self.action=''
        self.debug_mode=False
        self.choice='Normal'
        global wxObject,browsercheckFlag
        wxObject = self
        self.iconpath = IMAGES_PATH +"slk.ico"
        self.connect_img=wx.Image(IMAGES_PATH +"connect.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.disconnect_img=wx.Image(IMAGES_PATH +"disconnect.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()

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

        ## Following two lines set 'CRITICAL' leg level for selenium, uncomment these to not log entries from
        ## selenium if current log level is < CRITICAL
        # selenium_log = logging.getLogger("selenium")
        # selenium_log.setLevel(logging.CRITICAL)

        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(6, 5)
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        box = wx.BoxSizer(wx.VERTICAL)
        self.menubar = wx.MenuBar()
        self.fileMenu = wx.Menu()
        self.editMenu = wx.Menu()
        #own event
        self.Bind( wx.EVT_CHOICE, self.test)
        ##self.Bind(wx.EVT_CHOICE, self.debug)
        ##self.Bind(wx.EVT_CLOSE, self.closeScrapeWindow)
        #own event
        self.loggerMenu = wx.Menu()
        self.infoItem = wx.MenuItem(self.loggerMenu, 100,text = "Info",kind = wx.ITEM_NORMAL)
        self.loggerMenu.AppendItem(self.infoItem)

        self.debugItem = wx.MenuItem(self.loggerMenu, 101,text = "Debug",kind = wx.ITEM_NORMAL)
        self.loggerMenu.AppendItem(self.debugItem)

        self.errorItem = wx.MenuItem(self.loggerMenu, 102,text = "Error",kind = wx.ITEM_NORMAL)
        self.loggerMenu.AppendItem(self.errorItem)

        self.fileMenu.AppendMenu(wx.ID_ANY, "Logger Level", self.loggerMenu)
        self.menubar.Append(self.fileMenu, '&File')
        #-----------------------------------------------------Config Menu Begins
        self.configItem = wx.MenuItem(self.editMenu, 103,text = "Configuration",kind = wx.ITEM_NORMAL)
        self.editMenu.AppendItem(self.configItem)
        self.menubar.Append(self.editMenu, '&Edit')
        #-------------------------------------------------------Config Menu Ends
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
        self.breakpoint = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(225, 595), size=(60,20), style = wx.TE_RICH)
        box.Add(self.breakpoint, 1, wx.ALL|wx.EXPAND, 5)
        self.breakpoint.Disable()

        self.cancelbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"killStaleProcess.png", wx.BITMAP_TYPE_ANY), wx.Point(360, 555), wx.Size(50, 42))
        self.cancelbutton.Bind(wx.EVT_LEFT_DOWN, self.OnKillProcess)
        self.cancelbutton.SetToolTip(wx.ToolTip("To kill Stale process"))
        self.cancel_label=wx.StaticText(self.panel, -1, 'Kill Stale Process', wx.Point(340, 600), wx.Size(100, 70))

        self.terminatebutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"terminate.png", wx.BITMAP_TYPE_ANY), wx.Point(475, 555), wx.Size(50, 42))
        self.terminatebutton.Bind(wx.EVT_LEFT_DOWN, self.OnTerminate)
        self.terminatebutton.SetToolTip(wx.ToolTip("To Terminate the execution"))
        self.terminate_label=wx.StaticText(self.panel, -1, 'Terminate', wx.Point(475, 600), wx.Size(100, 70))

        self.clearbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"clear.png", wx.BITMAP_TYPE_ANY), wx.Point(590, 555), wx.Size(50, 42))
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
        if (self.logfilename_error_flag)==True or self.is_config_present_flag==False:
            self.cancelbutton.Disable()
            self.terminatebutton.Disable()
            self.clearbutton.Disable()
            self.connectbutton.Disable()
            self.rbox.Disable()
        threading.Timer(0.2,self.verifyMACAddress).start()
        if configvalues['browser_check'].lower()=='no':
            browsercheckFlag=True
        else:
            browsercheckFlag=False

    """
    Menu Items:
      1. Modifying Logger and Handlers Level dynamically without creating a new logger object
         When logging level is changed from Client window using "File" button.
      2. Edit client configuration
    """
    def menuhandler(self, event):
        id = event.GetId()
        if id == 100:     # When user selects INFO level
            logger.print_on_console( '--Logger level : INFO selected--')
            log.info('--Logger level : INFO selected--')
            logging.getLogger().setLevel(logging.INFO)
            for handler in logging.root.handlers[:]:
                    handler.setLevel(logging.INFO)
        elif id == 101:    # When user selects DEBUG level
            logger.print_on_console( '--Logger level : DEBUG selected--')
            log.info('--Logger level : DEBUG selected--')
            logging.getLogger().setLevel(logging.DEBUG)
            for handler in logging.root.handlers[:]:
                handler.setLevel(logging.DEBUG)
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
                Config_window(parent = None,id = -1, title="Nineteen68 Configuration")
            except Exception as e:
                msg = "Error while updating configuration"
                logger.print_on_console(msg)
                log.info(msg)
                log.error(e)

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
            os.system("TASKKILL /F /IM nineteen68MFapi.exe")
        exit()

    def OnKillProcess(self, event):
        controller.kill_process()

    def OnTerminate(self, event, *args):
        self.killDebugWindow()
        if self.killScrapeWindow():
            socketIO.emit('scrape','Terminate')
        self.killPauseWindow()
        if(len(args) > 0 and args[0]=="term_exec"):
            controller.disconnect_flag=True
            print ""
            msg = "---------Terminating all active operations-------"
        else:
            msg ="---------Termination Started-------"
        logger.print_on_console(msg)
        log.info(msg)
        controller.terminate_flag=True
        #Handling the case where user clicks terminate when the execution is paused
        #Resume the execution
        if controller.pause_flag:
            controller.pause_flag=False
            wxObject.mythread.resume(False)

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
            emsg="Forbidden request, Connection refused, please configure server ip and server port in Edit -> Configuration, and re-connect."
            logger.print_on_console(emsg)
            log.error(emsg)
            self.cancelbutton.Disable()
            self.terminatebutton.Disable()
            self.clearbutton.Disable()
            self.connectbutton.Enable()
            self.rbox.Disable()
            log.error(e)

    def killDebugWindow(self):
        #Close the debug window
        flag=False
        try:
            if (self.debugwindow != None) and (bool(self.debugwindow) != False):
                self.debugwindow.Destroy()
                flag = True
            self.debugwindow = None
        except Exception as e:
            log.error("Error while killing debug window")
            log.error(e)
        return flag

    def killScrapeWindow(self):
        #Close the scrape window
        flag=False
        try:
            if (self.scrapewindow != None) and (bool(self.scrapewindow) != False):
                self.scrapewindow.Destroy()
                flag = True
            self.scrapewindow = None
        except Exception as e:
            log.error("Error while killing scrape window")
            log.error(e)
        return flag

    def killPauseWindow(self):
        #Close the pause/display window
        flag=False
        try:
            if (self.pausewindow != None) and (bool(self.pausewindow) != False):
                self.pausewindow.OnOk()
                flag = True
            self.pausewindow = None
        except Exception as e:
            log.error("Error while killing pause window")
            log.error(e)
        return flag

    def test(self,event):
        global mobileScrapeFlag,qcConFlag,mobileWebScrapeFlag,desktopScrapeFlag
        global sapScrapeFlag,debugFlag,browsername,action,oebsScrapeFlag
        global socketIO,data
        con = controller.Controller()
        if(irisFlag == True):
            if(os.path.isdir(os.environ["NINETEEN68_HOME"] + '/Nineteen68/plugins/IRIS')):
                con.get_all_the_imports('IRIS')
        if mobileScrapeFlag==True:
            self.scrapewindow = mobileScrapeObj.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Mobile Scrapper",filePath = browsername,socketIO = socketIO)
            mobileScrapeFlag=False
        elif qcConFlag==True:
            self.scrapewindow = qcConObj.QcWindow(parent = None,id = -1, title="SLK Nineteen68 - Mobile Scrapper",filePath = qcdata,socketIO = socketIO)
            qcConFlag=False
        elif mobileWebScrapeFlag==True:
            self.scrapewindow = mobileWebScrapeObj.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Mobile Scrapper",browser = browsername,socketIO = socketIO)
            mobileWebScrapeFlag=False
        elif desktopScrapeFlag==True:
            self.scrapewindow = desktopScrapeObj.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Desktop Scrapper",filePath = browsername,socketIO = socketIO,irisFlag = irisFlag)
            desktopScrapeFlag=False
            browsername = ''
        elif sapScrapeFlag==True:
            self.scrapewindow = sapScrapeObj.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - SAP Scrapper",filePath = browsername,socketIO = socketIO,irisFlag = irisFlag)
            sapScrapeFlag=False
        elif oebsScrapeFlag==True:
            self.scrapewindow = oebsScrapeObj.ScrapeDispatcher(parent = None,id = -1, title="SLK Nineteen68 - Oebs Scrapper",filePath = browsername,socketIO = socketIO,irisFlag = irisFlag)
            oebsScrapeFlag=False
        elif debugFlag == True:
            self.debugwindow = DebugWindow(parent = None,id = -1, title="Debugger")
            debugFlag = False
        else:
            browsernumbers = ['1','2','3','6']
            if browsername in browsernumbers:
                logger.print_on_console('Browser name : '+str(browsername))
                #con = controller.Controller()
                con.get_all_the_imports('Web')
                con.get_all_the_imports('WebScrape')
                import Nineteen68_WebScrape
                self.scrapewindow = Nineteen68_WebScrape.ScrapeWindow(parent = None,id = -1, title="SLK Nineteen68 - Web Scrapper",browser = browsername,socketIO = socketIO,action=action,data=data,irisFlag = irisFlag)
                browsername = ''
            else:
                import pause_display_operation
                o = pause_display_operation.PauseAndDisplay()
                flag,inputvalue = o.getflagandinput()
                if flag == 'pause':
                    #call pause logic
                    self.pausewindow = pause_display_operation.Pause(parent = None,id = -1, title="SLK Nineteen68 - Pause")
                elif flag == 'display':
                    #call display logic
                    self.pausewindow = pause_display_operation.Display(parent = self,id = -1, title="SLK Nineteen68 - Display Variable",input = inputvalue)

    def verifyMACAddress(self):
        flag = False
        core_utils_obj = core_utils.CoreUtils()
        system_mac = core_utils_obj.getMacAddress()
        mac_verification_key = "".join(['N','1','i','1','N','2','e','3','T','5','e','8','E','1','3','n','2','1','S','i','X','t','Y','3','4','e','I','g','H','t','5','5'])
        irisMAC = []
        global irisFlag
        try:
            with open(CERTIFICATE_PATH+'/license.key', mode='r') as f:
                key = "".join(f.readlines()[1:-1]).replace("\n","").replace("\r","")
                key = core_utils_obj.unwrap(key, mac_verification_key)
                mac_addr = key[36:-36]
                if ("," in mac_addr):
                    mac_addr = (mac_addr.replace('-',':').replace(' ','')).lower().split(",")
                else:
                    mac_addr = [mac_addr.replace('-',':').replace(' ','').lower()]
                index = 0
                for mac in mac_addr:
                    if(str(mac).startswith("iris")):
                        mac_addr[index] = mac[4:]
                        irisMAC.append(mac[4:])
                    index = index + 1
                if(system_mac in mac_addr):
                    flag = True
                    if ((system_mac in irisMAC) and os.path.isdir(os.environ["NINETEEN68_HOME"]+'/Nineteen68/plugins/IRIS')):
                        irisFlag = True
                        controller.iris_flag = True
        except:
            pass
        if not flag:
            logger.print_on_console("Unauthorized: Access denied, system is not registered with Nineteen68")
            self.connectbutton.Disable()
        return flag

"""Checks if config file is present, if not prompts the user to enter config file details"""
class Config_window(wx.Frame):

    """The design of the config window is defined in the _init_() method"""
    def __init__(self, parent,id, title):
        #----------------------------------
        isConfigJson=self.readconfigJson()
        #----------------------------------
        global socketIO
        wx.Frame.__init__(self, parent, title=title,
                   pos=(300, 150), size=(470, 450), style = wx.CAPTION|wx.CLIP_CHILDREN)
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = IMAGES_PATH +"slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        self.updated = False
        self.connectEnabled = wxObject.connectbutton.IsEnabled()
        self.socketIO = socketIO
        self.panel = wx.Panel(self)
        wxObject.connectbutton.Disable()

        self.currentDirectory = os.environ["NINETEEN68_HOME"]
        self.defaultServerCrt = './Scripts/CA_BUNDLE/server.crt'

        self.sev_add=wx.StaticText(self.panel, label="Server Address", pos=(12,8 ),size=(90, 28), style=0, name="")
        self.server_add=wx.TextCtrl(self.panel, pos=(100,8 ), size=(140,-1))
        if isConfigJson!=False:
            self.server_add.SetValue(isConfigJson['server_ip'])

        self.sev_port=wx.StaticText(self.panel, label="Server Port", pos=(270,8 ),size=(70, 28), style=0, name="")
        self.server_port=wx.TextCtrl(self.panel, pos=(340,8 ), size=(105,-1))
        if isConfigJson!=False:
            self.server_port.SetValue(isConfigJson['server_port'])
        else:
            self.server_port.SetValue("8443")

        self.ch_path=wx.StaticText(self.panel, label="Chrome Path", pos=(12,38),size=(80, 28), style=0, name="")
        self.chrome_path=wx.TextCtrl(self.panel, pos=(100,38), size=(310,-1))
        wx.Button(self.panel, label="...",pos=(415,38), size=(30, -1)).Bind(wx.EVT_BUTTON, self.fileBrowser_chpath)
        if isConfigJson!=False:
            self.chrome_path.SetValue(isConfigJson['chrome_path'])
        else:
            self.chrome_path.SetValue('default')

        self.log_fpath=wx.StaticText(self.panel, label="Log File Path", pos=(12,68),size=(80, 28), style=0, name="")
        self.log_file_path=wx.TextCtrl(self.panel, pos=(100,68), size=(310,-1))
        wx.Button(self.panel, label="...",pos=(415,68), size=(30, -1)).Bind(wx.EVT_BUTTON, self.fileBrowser_logfilepath)
        if isConfigJson!=False:
            self.log_file_path.SetValue(isConfigJson['logFile_Path'])

        self.qu_timeout=wx.StaticText(self.panel, label="Query Timeout", pos=(12,98),size=(85, 28), style=0, name="")
        self.query_timeout=wx.TextCtrl(self.panel, pos=(100,98), size=(80,-1))
        if isConfigJson!=False:
            self.query_timeout.SetValue(isConfigJson['queryTimeOut'])
        else:
            self.query_timeout.SetValue("3")

        wx.StaticText(self.panel, label="Time Out", pos=(185,98),size=(50, 28), style=0, name="")
        self.time_out=wx.TextCtrl(self.panel, pos=(240,98), size=(80,-1))
        if isConfigJson!=False:
            self.time_out.SetValue(isConfigJson['timeOut'])
        else:
            self.time_out.SetValue("1")

        wx.StaticText(self.panel, label="Delay", pos=(325,98),size=(40, 28), style=0, name="")
        self.delay=wx.TextCtrl(self.panel, pos=(360,98), size=(85,-1))
        if isConfigJson!=False:
            self.delay.SetValue(isConfigJson['delay'])
        else:
            self.delay.SetValue("0.3")

        wx.StaticText(self.panel, label="Step Execution Wait", pos=(12,128),size=(120, 28), style=0, name="")
        self.step_exe_wait=wx.TextCtrl(self.panel, pos=(130,128), size=(80,-1))
        if isConfigJson!=False:
            self.step_exe_wait.SetValue(isConfigJson['stepExecutionWait'])
        else:
            self.step_exe_wait.SetValue("1")

        wx.StaticText(self.panel, label="Display Variable Timeout", pos=(225,128),size=(140, 28), style=0, name="")
        self.disp_var_timeout=wx.TextCtrl(self.panel, pos=(360,128), size=(85,-1))
        if isConfigJson!=False:
            self.disp_var_timeout.SetValue(isConfigJson['displayVariableTimeOut'])

        self.sev_cert=wx.StaticText(self.panel, label="Server Cert", pos=(12,158),size=(85, 28), style=0, name="")
        self.server_cert=wx.TextCtrl(self.panel, pos=(100,158), size=(310,-1))
        wx.Button(self.panel, label="...",pos=(415,158), size=(30, -1)).Bind(wx.EVT_BUTTON, self.fileBrowser_servcert)
        if (not isConfigJson) or (isConfigJson and isConfigJson['server_cert']==self.defaultServerCrt):
            self.defaultServerCrt = os.path.normpath(self.currentDirectory+'/Scripts/CA_BUNDLE/server.crt')
            self.server_cert.SetValue(self.defaultServerCrt)
        else:
            self.server_cert.SetValue(isConfigJson['server_cert'])

        lblList = ['Yes', 'No']
        lblList2 = ['64-bit', '32-bit']
        lblList3 = ['All', 'Fail']
        lblList4 = ['False', 'True']
        self.rbox1 = wx.RadioBox(self.panel, label = 'Ignore Certificate', pos = (12,188), choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['ignore_certificate'].title()==lblList[0]:
            self.rbox1.SetSelection(0)
        else:
            self.rbox1.SetSelection(1)

        self.rbox2 = wx.RadioBox(self.panel, label = 'IE Architecture Type', pos = (130,188), choices = lblList2,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['bit_64'].title() != 'Yes':
            self.rbox2.SetSelection(1)
        else:
            self.rbox2.SetSelection(0)

        self.rbox9 = wx.RadioBox(self.panel, label = 'Disable Server Certificate Check', pos = (260,188), choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['disable_server_cert'].title() == lblList[0]:
            self.rbox9.SetSelection(0)
        else:
            self.rbox9.SetSelection(1)

        self.rbox5 = wx.RadioBox(self.panel, label = 'Exception Flag', pos = (12,248), choices = lblList4,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['exception_flag'].title()!=lblList4[0]:
            self.rbox5.SetSelection(1)
        else:
            self.rbox5.SetSelection(0)

        self.rbox6 = wx.RadioBox(self.panel, label = 'Ignore Visibility Check', pos = (150,248), choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['ignoreVisibilityCheck'].title()==lblList[0]:
            self.rbox6.SetSelection(0)
        else:
            self.rbox6.SetSelection(1)

        self.rbox3 = wx.RadioBox(self.panel, label = 'ScreenShot Flag', pos = (340,308), choices = lblList3,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['screenShot_Flag'].title()!=lblList3[0]:
            self.rbox3.SetSelection(1)
        else:
            self.rbox3.SetSelection(0)

        self.rbox4 = wx.RadioBox(self.panel, label = 'Retrieve URL', pos = (12,308), choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['retrieveURL'].title()!=lblList[0]:
            self.rbox4.SetSelection(1)
        else:
            self.rbox4.SetSelection(0)

        self.rbox7 = wx.RadioBox(self.panel, label = 'Enable Security Check', pos = (310,248), choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['enableSecurityCheck'].title()==lblList[0]:
            self.rbox7.SetSelection(0)
        else:
            self.rbox7.SetSelection(1)

        self.rbox8 = wx.RadioBox(self.panel, label = 'Browser Check', pos = (115,308), choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['browser_check'].title()!=lblList[0]:
            self.rbox8.SetSelection(1)
        else:
            self.rbox8.SetSelection(0)

        self.rbox10 = wx.RadioBox(self.panel, label = 'Highlight Check', pos = (225,308), choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['highlight_check'].title()==lblList[0]:
            self.rbox10.SetSelection(0)
        else:
            self.rbox10.SetSelection(1)

        self.error_msg=wx.StaticText(self.panel, label="", pos=(85,360),size=(350, 28), style=0, name="")
        wx.Button(self.panel, label="Save",pos=(100,388), size=(100, 28)).Bind(wx.EVT_BUTTON, self.config_check)
        wx.Button(self.panel, label="Close",pos=(250,388), size=(100, 28)).Bind(wx.EVT_BUTTON, self.close)

        self.Centre()
        wx.Frame(self.panel)
        self.Show()

    """This method verifies and checks if correct data is present,then creates a dictionary and sends this dictionary to jsonCreater()"""
    def config_check(self,event):
        data = {}
        config_data={}
        bit_64='Yes'
        ignore_certificate=self.rbox1.GetStringSelection()
        if self.rbox2.GetStringSelection()!='64-bit':
            bit_64='No'
        screenShot_Flag=self.rbox3.GetStringSelection()
        retrieveURL=self.rbox4.GetStringSelection()
        exception_flag=self.rbox5.GetStringSelection()
        ignoreVisibilityCheck=self.rbox6.GetStringSelection()
        enableSecurityCheck=self.rbox7.GetStringSelection()
        server_add=self.server_add.GetValue()
        server_port=self.server_port.GetValue()
        chrome_path=self.chrome_path.GetValue()
        logFile_Path=self.log_file_path.GetValue()
        queryTimeOut=self.query_timeout.GetValue()
        time_out=self.time_out.GetValue()
        delay=self.delay.GetValue()
        stepExecutionWait=self.step_exe_wait.GetValue()
        displayVariableTimeOut=self.disp_var_timeout.GetValue()
        server_cert=self.server_cert.GetValue()
        browser_check=self.rbox8.GetStringSelection()
        disable_server_cert=self.rbox9.GetStringSelection()
        highlight_check=self.rbox10.GetStringSelection()
        #----------------creating data dictionary
        data['server_ip'] = server_add.strip()
        data['server_port'] = server_port.strip()
        data['ignore_certificate'] = ignore_certificate.strip()
        data['chrome_path'] = chrome_path.strip()
        data['bit_64'] = bit_64.strip()
        data['logFile_Path'] = logFile_Path.strip()
        data['screenShot_Flag'] = screenShot_Flag.strip()
        data['queryTimeOut'] = queryTimeOut.strip()
        data['timeOut'] = time_out.strip()
        data['stepExecutionWait'] = stepExecutionWait.strip()
        data['displayVariableTimeOut'] = displayVariableTimeOut.strip()
        data['retrieveURL'] = retrieveURL.strip()
        data['delay'] = delay.strip()
        data['ignoreVisibilityCheck'] = ignoreVisibilityCheck.strip()
        data['enableSecurityCheck'] = enableSecurityCheck.strip()
        data['exception_flag'] = exception_flag.strip().lower()
        data['server_cert'] =server_cert.strip()
        data['browser_check']=browser_check.strip()
        data['disable_server_cert'] = disable_server_cert.strip()
        data['highlight_check'] = highlight_check.strip()
        config_data=data
        if data['server_ip']!='' and data['server_port']!='' and data['server_cert']!='' and data['chrome_path']!='' and data['queryTimeOut']!='' and data['logFile_Path']!='':
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
            self.sev_cert.SetLabel('Server Cert')
            self.sev_cert.SetForegroundColour((0,0,0))
            self.ch_path.SetLabel('Chrome Path')
            self.ch_path.SetForegroundColour((0,0,0))
            #---------------------------------------resetting the static texts
            if (os.path.isfile(data['chrome_path'])==True or str(data['chrome_path']).strip()=='default') and os.path.isfile(data['server_cert'])==True and os.path.isfile(data['logFile_Path'])==True:
                self.jsonCreater(config_data)
            else:
                self.error_msg.SetLabel("Marked fields '^' contain invalid path, Data not saved")
                self.error_msg.SetForegroundColour((0,0,255))
                if os.path.isfile(data['server_cert'])!=True:
                    self.sev_cert.SetLabel('Server Cert^')
                    self.sev_cert.SetForegroundColour((0,0,255))
                else:
                    self.sev_cert.SetLabel('Server Cert')
                    self.sev_cert.SetForegroundColour((0,0,0))

                if os.path.isfile(data['chrome_path'])==True or str(data['chrome_path']).strip()=='default':
                    self.ch_path.SetLabel('Chrome Path')
                    self.ch_path.SetForegroundColour((0,0,0))
                elif  os.path.isfile(data['chrome_path'])!=True:
                    self.ch_path.SetLabel('Chrome Path^')
                    self.ch_path.SetForegroundColour((0,0,255))

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
            if data['queryTimeOut']=='':
                self.qu_timeout.SetLabel('Query Timeout*')
                self.qu_timeout.SetForegroundColour((255,0,0))
            else:
                self.qu_timeout.SetLabel('Query Timeout')
                self.qu_timeout.SetForegroundColour((0,0,0))
            if data['server_cert']=='':
                self.sev_cert.SetLabel('Server Cert*')
                self.sev_cert.SetForegroundColour((255,0,0))
            else:
                self.sev_cert.SetLabel('Server Cert')
                self.sev_cert.SetForegroundColour((0,0,0))
            if data['chrome_path']=='':
                self.ch_path.SetLabel('Chrome Path*')
                self.ch_path.SetForegroundColour((255,0,0))
            else:
                self.ch_path.SetLabel('Chrome Path')
                self.ch_path.SetForegroundColour((0,0,0))
            if data['browser_check']=='':
                self.ch_path.SetLabel('Browser Check*')
                self.ch_path.SetForegroundColour((255,0,0))
            else:
                self.ch_path.SetLabel('Browser Check')
                self.ch_path.SetForegroundColour((0,0,0))


    """jsonCreater saves the data in json form, location of file to be saved must be defined. This method will overwrite the existing .json file"""
    def jsonCreater(self,data):
        try:
            if wx.MessageBox("Config file has been edited, Would you like to save?","Confirm Save",wx.ICON_QUESTION | wx.YES_NO) == wx.YES:
                # Write JSON file
                with io.open('./Lib/config.json', 'w', encoding='utf8') as outfile:
                    str_ = json.dumps(data,indent=4, sort_keys=True,separators=(',', ': '), ensure_ascii=False)
                    outfile.write(unicode(str_))
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
        dlg = wx.FileDialog(self, message="Choose a file ...",defaultDir=self.currentDirectory,defaultFile="", wildcard="Chrome executable (*chrome.exe)|*chrome.exe|" \
            "All files (*.*)|*.*", style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.chrome_path.SetValue(path)
        dlg.Destroy()
    """This method open a file selector dialog , from where file path can be set """
    def fileBrowser_logfilepath(self,event):
        dlg = wx.DirDialog(None, "Choose a folder", "", wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            log_path = dlg.GetPath()
            log_path= os.path.normpath(log_path+"/TestautoV2.log")
            f = open(log_path, "a+")
            f.close()
            self.log_file_path.SetValue(log_path)
        dlg.Destroy()
    """This method open a file selector dialog , from where file path can be set """
    def fileBrowser_servcert(self,event):
        dlg = wx.FileDialog(self, message="Choose a file ...",defaultDir=self.currentDirectory,defaultFile="", wildcard="Certificate file (*.crt)|*.crt|" \
            "All files (*.*)|*.*", style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.server_cert.SetValue(path)
        dlg.Destroy()

    """This method closes the wxPython instance"""
    def close(self,event):
        self.Close()
        self.Destroy()
        global configvalues, browsercheckFlag
        configvalues = readconfig.readConfig().readJson() # Re-reading config values
        if configvalues['browser_check'].lower()=='no':
            browsercheckFlag=True
        else:
            browsercheckFlag=False
        try:
            logfilename = configvalues["logFile_Path"].replace("\\","\\\\")
            logging.config.fileConfig(LOGCONFIG_PATH,defaults={'logfilename': logfilename},disable_existing_loggers=False)
        except Exception as e:
            log.error(e)
        if self.updated or self.connectEnabled:
            wxObject.connectbutton.Enable()
        msg = '--Edit Config closed--'
        logger.print_on_console(msg)
        log.info(msg)

class DebugWindow(wx.Frame):
    def __init__(self, parent,id, title):
        wx.Frame.__init__(self, parent, title=title, pos=(300, 150),  size=(200, 75),
            style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX) )
        self.SetBackgroundColour('#e6e7e8')
        ##style = wx.CAPTION|wx.CLIP_CHILDREN
        self.iconpath = IMAGES_PATH +"slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        self.panel = wx.Panel(self)
        self.continue_debugbutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"play.png", wx.BITMAP_TYPE_ANY), (65, 15), (35, 28))
        self.continue_debugbutton.Bind(wx.EVT_LEFT_DOWN, self.Resume)
        self.continue_debugbutton.SetToolTip(wx.ToolTip("To continue the execution"))
        self.continuebutton = wx.StaticBitmap(self.panel, -1, wx.Bitmap(IMAGES_PATH +"step.png", wx.BITMAP_TYPE_ANY), (105, 15), (35, 28))
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
        wxObject.debugwindow = None
        self.Destroy()

    def OnContinue(self, event):
        logger.print_on_console('Event Triggered to Resume')
        log.info('Event Triggered to Resume')
        controller.pause_flag=False
        wxObject.mythread.resume(debug_mode)


def check_browser():
    try:
        try:
            global chromeFlag,firefoxFlag
            logger.print_on_console('Checking for browser versions...')
            import subprocess
            from selenium import webdriver
            from selenium.webdriver import ChromeOptions
            a=[]
            p = subprocess.Popen('chromedriver.exe --version', stdout=subprocess.PIPE, bufsize=1,cwd=DRIVERS_PATH,shell=True)
            for line in iter(p.stdout.readline, b''):
                a.append(str(line))
            a=float(a[0][13:17])
            choptions1 = webdriver.ChromeOptions()
            if str(configvalues['chrome_path']).lower()!="default":
                choptions1.binary_location=str(configvalues['chrome_path'])
            choptions1.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=choptions1, executable_path=CHROME_DRIVER_PATH)
            browser_ver = driver.capabilities['version']
            browser_ver1 = browser_ver.encode('utf-8')
            browser_ver = int(browser_ver1[:2])
            try:
                driver.close()
                driver.quit()
            except:
                pass
            driver=None
            for i in CHROME_DRIVER_VERSION:
                if a == i[0]:
                    if browser_ver >= i[1] and browser_ver <= i[2]:
                        chromeFlag=True
            if chromeFlag == False :
                logger.print_on_console('WARNING!! : Chrome version',browser_ver,' is not supported.')
        except Exception as e:
            logger.print_on_console("Error in checking chrome version")
            log.error("Error in checking chrome version")
            log.error(e)
        try:
            p = subprocess.Popen('geckodriver.exe --version', stdout=subprocess.PIPE, bufsize=1,cwd=DRIVERS_PATH,shell=True)
            a=[]
            for line in iter(p.stdout.readline, b''):
                a.append(str(line))
            a=float(a[0][12:16])
            caps=webdriver.DesiredCapabilities.FIREFOX
            caps['marionette'] = True
            from selenium.webdriver.firefox.options import Options
            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Firefox(capabilities=caps,firefox_options=options, executable_path=GECKODRIVER_PATH)
            browser_ver=driver.capabilities['browserVersion']
            browser_ver1 = browser_ver.encode('utf-8')
            browser_ver = float(browser_ver1[:4])
            try:
                driver.close()
                driver.quit()
            except:
                pass
            driver=None
            for i in FIREFOX_BROWSER_VERSION:
                if a == i[0]:
                    if browser_ver >= i[1] or browser_ver <= i[2]:
                        firefoxFlag=True
            if firefoxFlag == False:
                logger.print_on_console('WARNING!! : Firefox version',browser_ver,' is not supported.')
        except Exception as e:
            logger.print_on_console("Error in checking Firefox version")
            log.error("Error in checking Firefox version")
            log.error(e)
        if chromeFlag == True and firefoxFlag == True:
            logger.print_on_console('Current version of browsers are supported')
        return True
    except Exception as e:
        logger.print_on_console("Error while checking browser compatibility")
        log.debug("Error while checking browser compatibility")
        log.debug(e)
    return False