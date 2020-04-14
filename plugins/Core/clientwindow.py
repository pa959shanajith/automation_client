import wx
import sys
import os
import time
import http.client
import logging
import logging.config
import base64
import platform
import uuid
from datetime import datetime
import core_utils
import logger
import threading
from constants import *
import controller
import readconfig
import json
import socket
import requests
import io
import handler
import update_module
try:
    from socketlib_override import SocketIO,BaseNamespace
except ImportError:
    from socketIO_client import SocketIO,BaseNamespace
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
global update_obj
log = logging.getLogger('clientwindow.py')
wxObject = None
browsername = None
qcdata = None
qcObject = None
soc=None
pdfgentool = None
qcConFlag=False
browsercheckFlag=False
updatecheckFlag=False
chromeFlag=False
firefoxFlag=False
desktopScrapeFlag=False
sapScrapeFlag=False
mobileScrapeFlag=False
mobileWebScrapeFlag=False
pdfScrapeFlag = False
debugFlag = False
oebsScrapeFlag = False
irisFlag = False
executionOnly=False
socketIO = None
allow_connect = False
icesession = None
plugins_list = []
configvalues = None
execution_flag = False
closeActiveConnection = False
connection_Timer = None
NINETEEN68_HOME = os.environ["NINETEEN68_HOME"]
IMAGES_PATH = NINETEEN68_HOME + "/assets/images/"
os.environ["IMAGES_PATH"] = IMAGES_PATH
ICE_CONST= NINETEEN68_HOME + "/assets/ice_const.json"
CONFIG_PATH= NINETEEN68_HOME + "/assets/config.json"
CERTIFICATE_PATH = NINETEEN68_HOME + "/assets/CA_BUNDLE"
LOGCONFIG_PATH = NINETEEN68_HOME + "/assets/logging.conf"
DRIVERS_PATH = NINETEEN68_HOME + "/lib/Drivers"
CHROME_DRIVER_PATH = DRIVERS_PATH + "/chromedriver"
GECKODRIVER_PATH = DRIVERS_PATH + "/geckodriver"
if SYSTEM_OS == "Windows":
    CHROME_DRIVER_PATH += ".exe"
    GECKODRIVER_PATH += ".exe"
MANIFEST_LOC= NINETEEN68_HOME + '/assets/about_manifest.json'
LOC_7Z = NINETEEN68_HOME + '/Lib/7zip/7z.exe'
UPDATER_LOC = NINETEEN68_HOME + '/assets/Update.exe'
if (os.path.exists(UPDATER_LOC[:-3] + "py")): UPDATER_LOC = UPDATER_LOC[:-3] + "py"
SERVER_LOC = None

class MainNamespace(BaseNamespace):
    core_utils_obj = core_utils.CoreUtils()

    def on_message(self, *args):
        global action,wxObject,browsername,desktopScrapeFlag,allow_connect,browsercheckFlag,connection_Timer,updatecheckFlag
        try:
            if(str(args[0]) == 'connected'):
                if(allow_connect):
                    wxObject.schedule.Enable()
                    wxObject.cancelbutton.Enable()
                    wxObject.terminatebutton.Enable()
                    wxObject.clearbutton.Enable()
                    wxObject.rbox.Enable()
                    if browsercheckFlag == False:
                        browsercheckFlag = check_browser()
                    if updatecheckFlag == False:
                        msg='Checking for client package updates'
                        logger.print_on_console(msg)
                        log.info(msg)
                        updatecheckFlag = check_update(True)
                    if executionOnly:
                        msg='Execution only Mode enabled'
                        logger.print_on_console(msg)
                        log.info(msg)
                    sch_mode = wxObject.schedule.GetValue()
                    if sch_mode: socketIO.emit('toggle_schedule',sch_mode)
                    msg = ("Schedule" if sch_mode else "Normal") + " Mode: Connection to the Nineteen68 Server established"
                    logger.print_on_console(msg)
                    log.info(msg)
                    conn_time = float(configvalues['connection_timeout'])
                    if (not (connection_Timer != None and connection_Timer.isAlive())
                     and (conn_time >= 8)):
                        log.info("Connection Timeout timer Started")
                        connection_Timer = threading.Timer(conn_time*60*60, wxObject.closeConnection)
                        connection_Timer.start()
                else:
                    threading.Timer(1,wxObject.killSocket).start()

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
                    response = json.loads(self.core_utils_obj.unwrap(str(args[1]), ice_ndac_key))
                    plugins_list = response['plugins']
                    err_res = None
                    if(response['id'] != icesession['ice_id'] and response['connect_time'] != icesession['connect_time']):
                        err_res="Invalid response received"
                    if(response['res'] != 'success'):
                        if('err_msg' in response):
                            err_res=response['err_msg']
                    if(err_res is not None):
                        logger.print_on_console(err_res)
                        log.info(err_res)
                        threading.Timer(0.5,wxObject.killSocket).start()
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

            elif(str(args[0]) == 'fail'):
                fail_msg = "Fail"
                if len(args) > 1 and args[1]=="conn":
                    fail_msg+="ed to connect to Nineteen68 Server"
                if len(args) > 1 and args[1]=="disconn":
                    fail_msg+="ed to disconnect from Nineteen68 Server"
                logger.print_on_console(fail_msg)
                log.info(fail_msg)
                threading.Timer(0.1,wxObject.killSocket).start()

        except Exception as e:
            err_msg='Error while Connecting to Server'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_focus(self, *args):
        try:
            appType=args[2]
            appType=appType.lower()
            if appType==APPTYPE_WEB:
                core_utils.get_all_the_imports('WebScrape')
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
                    #con =controller.Controller()
                    core_utils.get_all_the_imports('Oebs')
                    import utils
                    light =utils.Utils()
                    res = light.highlight(args[0],args[1])
                    logger.print_on_console('Highlight result: '+str(res))
            elif appType==APPTYPE_DESKTOP.lower():
                #con =controller.Controller()
                core_utils.get_all_the_imports('Desktop')
                import desktop_highlight
                highlightObj=desktop_highlight.highLight()
                highlightObj.highLiht_element(args[0],args[1])
            elif appType==APPTYPE_SAP.lower():
                #con =controller.Controller()
                core_utils.get_all_the_imports('SAP')
                import sap_highlight
                highlightObj=sap_highlight.highLight()
                highlightObj.highlight_element(args[0])
        except Exception as e:
            err_msg='Error while Highlighting'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_executeTestSuite(self, *args):
        global wxObject, execution_flag
        try:
            exec_data = args[0]
            batch_id = exec_data["batchId"]
            if(not execution_flag):
                socketIO.emit('return_status_executeTestSuite', {'status': 'success', 'batchId': batch_id})
                wxObject.mythread = TestThread(wxObject, EXECUTE, exec_data)
            else:
                #obj = handler.Handler()
                #_,_,_,scenarioIds,_,_,_,_,_,_,_ = obj.parse_json_execute(exec_data)
                #data = {'scenario_ids': scenarioIds, 'batchId': batch_id, 'time': str(datetime.now())}
                data = {'execution_id': exec_data['executionIds'], 'time': str(datetime.now())}
                emsg = 'Execution already in progress. Skipping current request.'
                log.warn(emsg)
                logger.print_on_console(emsg)
                """ Sending scenario details for skipped execution to update the same in reports. """
                socketIO.emit('return_status_executeTestSuite',{'status':'skipped', 'data':data, 'batchId': batch_id})
        except Exception as e:
            err_msg='Error while Executing'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_debugTestCase(self, *args):
        global wxObject
        try:
            if check_execution_lic("result_debugTestCase"): return None
            exec_data = args[0]
            wxObject.mythread = TestThread(wxObject, DEBUG, exec_data)
            wxObject.choice=wxObject.rbox.GetStringSelection()
            logger.print_on_console(str(wxObject.choice)+' is Selected')
            if wxObject.choice == 'Normal':
                wxObject.killChildWindow(debug=True)
            wxObject.debug_mode=False
            wxObject.breakpoint.Disable()
            if wxObject.choice in ['Stepwise','RunfromStep']:
                global debugFlag
                debugFlag = True
                wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
        except Exception as e:
            err_msg='Error while Debugging'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_webscrape(self,*args):
        try:
            global action,wxObject,browsername,desktopScrapeFlag,data,socketIO
            if check_execution_lic("scrape"): return None
            elif bool(wxObject.scrapewindow): return None
            args = list(args)
            d = args[0]
            action = d['action']
            data = {}
            if action == 'userobject':
                core_utils.get_all_the_imports('WebScrape')
                import UserObjectScrape
                webscrape=UserObjectScrape.UserObject()
                webscrape.get_user_object(d,socketIO)
            else:
                if action == 'scrape':
                    task = d['task']
                    if str(task) == 'OPEN BROWSER CH':
                        browsername = '1'
                    elif str(task) == 'OPEN BROWSER IE':
                        browsername = '3'
                    elif str(task) == 'OPEN BROWSER FX':
                        browsername = '2'
                    elif str(task) == 'OPEN BROWSER SF':
                        browsername = '6'
                elif action == 'compare':
                    task = d['task']
                    data['view'] = d['viewString']
                    data['scrapedurl'] = d['scrapedurl']
                    if str(task) == 'OPEN BROWSER CH':
                        browsername = '1'
                    elif str(task) == 'OPEN BROWSER IE':
                        browsername = '3'
                    elif str(task) == 'OPEN BROWSER FX':
                        browsername = '2'
                wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
        except Exception as e:
            err_msg='Error while Scraping Web application'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_LAUNCH_DESKTOP(self, *args):
        try:
            if check_execution_lic("scrape"): return None
            elif bool(wxObject.scrapewindow): return None
            #con = controller.Controller()
            global browsername
            browsername = args
            core_utils.get_all_the_imports('Desktop')
            import desktop_scrape
            global desktopScrapeObj
            desktopScrapeObj=desktop_scrape
            global desktopScrapeFlag
            desktopScrapeFlag=True
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
        except Exception as e:
            err_msg='Error while Scraping Desktop application'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_LAUNCH_SAP(self, *args):
        try:
            if check_execution_lic("scrape"): return None
            elif bool(wxObject.scrapewindow): return None

            #con = controller.Controller()
            global browsername
            browsername = args[0]
            core_utils.get_all_the_imports('SAP')
            import sap_scrape
            global sapScrapeObj
            sapScrapeObj=sap_scrape
            global sapScrapeFlag
            sapScrapeFlag=True
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
        except Exception as e:
            err_msg='Error while Scraping SAP application'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_LAUNCH_MOBILE(self, *args):
        try:
            if check_execution_lic("scrape"): return None
            elif bool(wxObject.scrapewindow): return None
            global browsername
            #con = controller.Controller()
            if str(args[0]).endswith('apk'):
                browsername = args[0]+";"+args[1]
            elif str(args[4])=='ios':
                browsername = args[0] + ";" + args[1] + ";" + args[2]+";" + args[3]+";" + args[4]
            """
            elif str(args[0]).endswith('app'):
                browsername = args[0] + ";" + args[2]+";" + args[3]
            elif str(args[0]).endswith('ipa'):
                browsername = args[0] + ";" + args[2] + ";" + args[3]+";" + args[4]
            """
            #con =controller.Controller()
            if SYSTEM_OS=='Darwin':
                core_utils.get_all_the_imports('Mobility/MobileApp')
            else:
                core_utils.get_all_the_imports('Mobility')
            import mobile_app_scrape
            global mobileScrapeObj
            mobileScrapeObj=mobile_app_scrape
            global mobileScrapeFlag
            mobileScrapeFlag=True
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
        except Exception as e:
            err_msg='Error while Scraping Mobile application'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_LAUNCH_MOBILE_WEB(self, *args):
        try:
            if check_execution_lic("scrape"): return None
            elif bool(wxObject.scrapewindow): return None
            global mobileWebScrapeObj,mobileWebScrapeFlag
            #con = controller.Controller()
            global browsername
            browsername = args[0]+";"+args[1]
            if SYSTEM_OS=='Darwin':
                core_utils.get_all_the_imports('Mobility/MobileWeb')
            else:
                core_utils.get_all_the_imports('Mobility')
            import mobile_web_scrape
            mobileWebScrapeObj=mobile_web_scrape
            mobileWebScrapeFlag=True
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
        except Exception as e:
            err_msg='Error while Scraping Mobile application'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_PDF_SCRAPE(self, *args):
        try:
            if check_execution_lic("scrape"): return None
            elif bool(wxObject.scrapewindow): return None
            logger.print_on_console(" Entering inside PDF scrape")
            global pdfScrapeObj,pdfScrapeFlag
            global browsername
            browsername = args[0]
            #con =controller.Controller()
            core_utils.get_all_the_imports('PDF')
            import pdf_scrape_dispatcher
            pdfScrapeObj=pdf_scrape_dispatcher
            pdfScrapeFlag=True
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
        except Exception as e:
            err_msg='Error while Scraping in PDF Window'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_LAUNCH_OEBS(self, *args):
        try:
            if check_execution_lic("scrape"): return None
            elif bool(wxObject.scrapewindow): return None
            global oebsScrapeObj,oebsScrapeFlag
            #con = controller.Controller()
            global browsername
            browsername = args[0]
            core_utils.get_all_the_imports('Oebs')
            import scrape_dispatcher
            oebsScrapeObj=scrape_dispatcher
            oebsScrapeFlag=True
            wx.PostEvent(wxObject.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, wxObject.GetId()))
        except Exception as e:
            err_msg='Error while Scraping Oracle application'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_wsdl_listOfOperation(self, *args):
        try:
            if check_execution_lic("result_wsdl_listOfOperation"): return None
            global socketIO
            #contrlr = controller.Controller()
            core_utils.get_all_the_imports('WebServices')
            import wsdlgenerator
            wsdlurl = str(args[0])
            wsdl_object = wsdlgenerator.WebservicesWSDL()
            response = wsdl_object.listOfOperation(wsdlurl)
            response=str(response)
            log.debug(response)
            socketIO.emit('result_wsdl_listOfOperation',response)
        except Exception as e:
            err_msg='Error while Fetching WSDL Operations'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_wsdl_ServiceGenerator(self, *args):
        try:
            global socketIO
            serverCertificate=None
            serverCerificate_pass=None
            auth_uname=None
            auth_pass=None
            #contrlr = controller.Controller()
            core_utils.get_all_the_imports('WebServices')
            import wsdlgenerator
            wsgen_inputs=eval(str(args[0]))
            wsdlurl = wsgen_inputs['wsdlurl']
            # Trimming URL for the following defect fix (1263 : Regression_WebService_WSDL : Request header and body are not loaded on click of "Add" button for WSDL)
            wsdlurl = wsdlurl.strip()
            operations = wsgen_inputs['operations']
            soapVersion = wsgen_inputs['soapVersion']
            if len(wsgen_inputs['serverCertificate'])!=0:
                Server_data= wsgen_inputs['serverCertificate']['certsDetails']
                Server_data =Server_data.split(';')
                serverCertificate = Server_data[0]
                serverCerificate_pass = Server_data[2]
                auth_Details= wsgen_inputs['serverCertificate']['authDetails']
                auth_Details= auth_Details.split(';')
                auth_uname= auth_Details[0]
                auth_pass= auth_Details[1]
            wsdl_object = wsdlgenerator.BodyGenarator(wsdlurl,operations,soapVersion,serverCertificate,serverCerificate_pass,auth_uname,auth_pass)
            responseHeader = wsdl_object.requestHeader()
            responseBody = wsdl_object.requestBody()
            from bs4 import BeautifulSoup
            responseBody = BeautifulSoup(responseBody, "xml").prettify()
            stringHeader=''
            if(responseHeader != None):
                for key in responseHeader:
                    logger.print_on_console(key,'==========',responseHeader[key])
                    log.info(key,'==========',responseHeader[key])
                    stringHeader = stringHeader + str(key) + ": " + str (responseHeader[key]) + "##"
            responseHeader = stringHeader
            logger.print_on_console('responseHeader after:::',responseHeader)
            logger.print_on_console('responseBody:::::',responseBody)
            log.info('responseHeader after:::',responseHeader)
            log.info('responseBody:::::',responseBody)
            response=responseHeader+"rEsPONseBOdY:"+responseBody
            response=str(response)
            logger.print_on_console(response)
            socketIO.emit('result_wsdl_ServiceGenerator',response)
        except Exception as e:
            err_msg='Error while Fetching WSDL Response'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_qclogin(self, *args):
        global qcObject
        err_msg = None
        try:
            if(qcObject == None):
                core_utils.get_all_the_imports('Qc')
                import QcController
                qcObject = QcController.QcWindow()

            qcdata = args[0]
            response = qcObject.qc_dict[qcdata.pop('qcaction')](qcdata)
            socketIO.emit('qcresponse', response)
        except KeyError:
            err_msg = 'Invalid ALM operation'
        except Exception as e:
            err_msg = 'Error in ALM operations'
            log.error(e, exc_info=True)
        if err_msg is not None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
            try: socketIO.emit('qcresponse','Error:Qc Operations')
            except: pass

    def on_render_screenshot(self,*args):
        try:
            global socketIO
            filepath = args[0]
            data_URIs=[]
            msg = "Request recieved for processing screenshots for report"
            logger.print_on_console(msg)
            log.info(msg)
            num_path = len(filepath)
            for i in range(num_path):
                path = filepath[i]
                if not (os.path.exists(path)):
                    data_URIs.append(None)
                    logger.print_on_console("Error while rendering Screenshot: File \""+path+"\" not found!")
                    log.error("File \""+path+"\" not found!")
                else:
                    with open(path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                        base64_data=encoded_string.decode('UTF-8').strip()
                        data_URIs.append(base64_data)
            socketIO.emit('render_screenshot',data_URIs)
            msg = "Request for processing screenshots completed successfully"
            logger.print_on_console(msg)
            log.info(msg)
        except Exception as e:
            err_msg='Error while sending screenshot data'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)
            socketIO.emit('render_screenshot','fail')

    def on_webCrawlerGo(self,*args):
        try:
            #con = controller.Controller()
            core_utils.get_all_the_imports('WebOcular')
            import webocular
            wobj = webocular.Webocular()
            # logger.print_on_console("length is ",len(args))
            args=list(args)
            global socketIO
            # Currently there are 5 arguments.
            #args[0] is URL, args[1] is level, args[2] is agent, args[3] is proxy,args[4] is searchData
            # wobj.runCrawler(args[0],args[1],args[2],args[3],socketIO,wxObject)
            wobj.runCrawler(socketIO,wxObject,*args)

        except Exception as e:
            socketIO.emit('result_web_crawler_finished','{"progress" : "fail"}')
            err_msg='Error while Crawling'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_jiralogin(self,*args):
        try:
            #con = controller.Controller()
            core_utils.get_all_the_imports('Jira')
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
            err_msg='Error in JIRA operations'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_update_screenshot_path(self,*args):
        spath=args[0]
        import constants
        if(SYSTEM_OS=='Darwin'):
            spath=spath["mac"]
        else:
            spath=spath["default"]
        if len(spath) != 0 and os.path.exists(spath):
            constants.SCREENSHOT_PATH=os.path.normpath(spath)+os.sep
        else:
            constants.SCREENSHOT_PATH="Disabled"
            logger.print_on_console("Screenshot capturing disabled since user does not have sufficient privileges for screenshot folder\n")
            log.info("Screenshot capturing disabled since user does not have sufficient privileges for screenshot folder\n")

    def on_generateFlowGraph(self,*args):
        try:
            global socketIO
            #con = controller.Controller()
            core_utils.get_all_the_imports('AutomatedPathGenerator')
            import apg
            fg = apg.AutomatedPathGenerator(socketIO)
            args=list(args)
            #args[0] is version, args[1] is filepath
            fg.generate_flowgraph(str(args[0]),str(args[1]))
        except Exception as e:
            err_msg='Error while generating flowgraph'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_apgOpenFileInEditor(self, *args):
        try:
            global socketIO
            #con = controller.Controller()
            core_utils.get_all_the_imports('AutomatedPathGenerator')
            import apg
            fg = apg.AutomatedPathGenerator(socketIO)
            args = list(args)
            # args[0] is Editor name, args[1] is filepath, args[2] is line number
            fg.open_file_in_editor(str(args[0]), str(args[1]), int(args[2]))
        except Exception as e:
            err_msg='Error while Opening File In Editor (APG)'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_runDeadcodeIdentifier(self, *args):
        try:
            global socketIO
            #con = controller.Controller()
            core_utils.get_all_the_imports('AutomatedPathGenerator')
            from generateAST import DeadcodeIdentifier
            dci = DeadcodeIdentifier()
            result = dci.start(str(args[0]),str(args[1]))
            socketIO.emit('deadcode_identifier',result)
        except Exception as e:
            err_msg='Error occured while running deadcode identifier'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)
            socketIO.emit('deadcode_identifier',False)

    def on_killSession(self,*args):
        global wxObject
        try:
            msg = 'Connection termination request triggered remotely by ' + args[0]
            logger.print_on_console(msg)
            log.info(msg)
            threading.Timer(1,wxObject.OnNodeConnect,[wx.EVT_BUTTON]).start()
        except Exception as e:
            err_msg='Exception while Remote Disconnect'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_disconnect(self, *args):
        log.info('Disconnect triggered')
        if (socketIO is not None) and (not socketIO.waiting_for_close):
            ice_ndac_key = "".join(['a','j','k','d','f','i','H','F','E','o','w','#','D','j',
                'g','L','I','q','o','c','n','^','8','s','j','p','2','h','f','Y','&','d'])
            icesession=json.loads(self.core_utils_obj.unwrap(socketIO._http_session.params['icesession'], ice_ndac_key))
            icesession['connect_time'] = str(datetime.now())
            icesession = self.core_utils_obj.wrap(json.dumps(icesession), ice_ndac_key)
            socketIO._http_session.params['icesession'] = icesession
            msg = 'Connectivity issue with Nineteen68 Server. Attempting to restore connectivity...'
            logger.print_on_console(msg)
            log.error(msg)
            if not bool(wxObject): return
            wxObject.schedule.Disable()
            wxObject.connectbutton.Disable()
        if not bool(wxObject): return
        wxObject.connectbutton.SetBitmapLabel(wxObject.connect_img)
        wxObject.connectbutton.SetName('connect')

    def on_irisOperations(self, *args):
        try:
            global socketIO
            #con = controller.Controller()
            core_utils.get_all_the_imports('IRIS')
            import iris_operations
            if(args[1]=='updateDataset'):
                check = iris_operations.update_dataset(args[0])
                socketIO.emit('iris_operations_result',check)
            elif(args[1]=='checkDuplicate'):
                check = iris_operations.check_duplicates(args[0],socketIO)
        except Exception as e:
            err_msg='Error occured in iris operations'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)


class SocketThread(threading.Thread):
    """Test Worker Thread Class."""
    daemon = True

    def __init__(self):
        """Init Worker Thread Class."""
        super(SocketThread, self).__init__()
        self.start()

    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        global socketIO, icesession, allow_connect
        allow_connect = False
        server_port = int(configvalues['server_port'])
        server_IP = configvalues['server_ip']
        server_cert = configvalues['server_cert']
        if "disable_server_cert" in configvalues and configvalues["disable_server_cert"]=="Yes":
            server_cert = False
        else:
            if os.path.exists(server_cert) == False:
                server_cert = CERTIFICATE_PATH +'/server.crt'
        client_cert = (CERTIFICATE_PATH + '/client.crt', CERTIFICATE_PATH + '/client.key')
        temp_server_IP = 'https://' + server_IP
        key='USERNAME'
        if(not(key in os.environ)):
            key='USER'
        username=str(os.environ[key]).lower()
        core_utils_obj = core_utils.CoreUtils()
        icesession = {
            'ice_id': str(uuid.uuid4()),
            'connect_time': str(datetime.now()),
            'username': username
        }
        ice_ndac_key = "".join(['a','j','k','d','f','i','H','F','E','o','w','#','D','j',
            'g','L','I','q','o','c','n','^','8','s','j','p','2','h','f','Y','&','d'])
        icesession_enc = core_utils_obj.wrap(json.dumps(icesession), ice_ndac_key)
        params={'username':username,'icesession': icesession_enc}
        try:
            socketIO = SocketIO(temp_server_IP,server_port,MainNamespace,verify=server_cert,cert=client_cert,params=params)
            socketIO.wait()
        except ValueError as e:
            msg = str(e).replace("[engine.io waiting for connection] ",'').replace("[SSL: CERTIFICATE_VERIFY_FAILED] ",'')
            if "_ssl.c" in msg:
                msg = msg[:msg.index("(_ssl")]
            logger.print_on_console(msg)
            log.error(msg)
            wxObject.connectbutton.Enable()
        except Exception as e:
            msg = "Error in server connection"
            logger.print_on_console(msg)
            log.error(msg)
            log.error(e,exc_info=True)
            wxObject.connectbutton.Enable()


class TestThread(threading.Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self, wxObject, action, json_data):
        """Init Worker Thread Class."""
        super(TestThread, self).__init__()
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
        self.con = ''
        self.action = action.lower()
        self.json_data = json_data
        self.debug_mode = wxObject.debug_mode
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
        global socketIO, execution_flag, closeActiveConnection,connection_Timer
        batch_id = self.json_data["batchId"]
        try:
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
            self.wxObject.schedule.Disable()
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
                execution_flag = True
                apptype =(self.json_data)['apptype']
            if(apptype == "DesktopJava"):
                apptype = "oebs"
            if(apptype.lower() not in plugins_list):
                logger.print_on_console('This app type is not part of the license.')
                status=TERMINATE
            else:
                status = self.con.invoke_controller(self.action,self,self.debug_mode,runfrom_step,self.json_data,self.wxObject,socketIO,qcObject)

            logger.print_on_console('Execution status '+status)

            if status==TERMINATE:
                logger.print_on_console('---------Termination Completed-------')

            #Removed execute,debug button
            self.wxObject.breakpoint.Clear()
            self.wxObject.rbox.Enable()
            self.wxObject.breakpoint.Disable()
            self.wxObject.cancelbutton.Enable()
            if self.action==DEBUG:
                testcasename = handler.local_handler.testcasename
                self.wxObject.killChildWindow(debug=True)
                if (len(testcasename) > 0 or apptype.lower() not in plugins_list):
                    if('UserObjectScrape' in sys.modules):
                        import UserObjectScrape
                        if(UserObjectScrape.update_data!={}):
                            data=UserObjectScrape.update_data
                            UserObjectScrape.update_data={}
                            data['status']=status
                            socketIO.emit('result_debugTestCase',data)
                        else:
                            socketIO.emit('result_debugTestCase',status)
                    else:
                        socketIO.emit('result_debugTestCase',status)
                else:
                    socketIO.emit('result_debugTestCaseWS',status)
            elif self.action==EXECUTE:
                socketIO.emit('result_executeTestSuite', {"status":status, "batchId": batch_id})
        except Exception as e:
            log.error(e, exc_info=True)
            status=TERMINATE
            if socketIO is not None:
                if self.action==DEBUG:
                    self.wxObject.killChildWindow(debug=True)
                    socketIO.emit('result_debugTestCase',status)
                elif self.action==EXECUTE:
                    socketIO.emit('result_executeTestSuite', {"status":status, "batchId": batch_id})
        if closeActiveConnection:
            closeActiveConnection = False
            connection_Timer = threading.Timer(300, wxObject.closeConnection)
            connection_Timer.start()

        self.wxObject.mythread = None
        execution_flag = False
        self.wxObject.schedule.Enable()


class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        wx.CallAfter(self.out.AppendText, string)

    def flush(self):
        pass


class ClientWindow(wx.Frame):
    def __init__(self, appName):
        wx.Frame.__init__(self, parent=None,id=-1, title=appName,
                   pos=(300, 150),  size=(800, 730),style=wx.DEFAULT_FRAME_STYLE & ~ (wx.MAXIMIZE_BOX))
        self.SetBackgroundColour('#e6e7e8')
        ##self.ShowFullScreen(True,wx.ALL)
        ##self.SetBackgroundColour('#D0D0D0')
        self.logfilename_error_flag = False
        # Check if config file is present and valid
        self.is_config_missing = 'configmissing' in configvalues
        self.is_config_invalid = 'errorflag' in configvalues
        self.debugwindow = None
        self.scrapewindow = None
        self.pausewindow = None
        self.pluginPDF = None
        self.id = id
        self.appName = appName
        self.mainclass = self
        self.mythread = None
        self.action=''
        self.debug_mode=False
        self.choice='Normal'
        global wxObject,browsercheckFlag,updatecheckFlag
        wxObject = self
        self.iconpath = IMAGES_PATH +"slk.ico"
        self.connect_img=wx.Image(IMAGES_PATH +"connect.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.disconnect_img=wx.Image(IMAGES_PATH +"disconnect.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.enabledStatus = [False,False,False,False,False,False,False,False]

        """
        Creating Root Logger using logger file config and setting logfile path,which is in config.json
        """
        try:
            logfilename = os.path.normpath(configvalues["logFile_Path"]).replace("\\","\\\\")
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
        self.editMenu.Append(self.configItem)
        self.menubar.Append(self.editMenu, '&Edit')

        self.pdfReportItem = wx.MenuItem(self.toolMenu, 151,text = "Generate PDF &Report",kind = wx.ITEM_NORMAL)
        self.toolMenu.Append(self.pdfReportItem)
        self.pdfReportBatchItem = wx.MenuItem(self.toolMenu, 152,text = "Generate PDF Report (B&atch)",kind = wx.ITEM_NORMAL)
        self.toolMenu.Append(self.pdfReportBatchItem)
        self.menubar.Append(self.toolMenu, 'T&ools')
        self.SetMenuBar(self.menubar)

        self.aboutItem = wx.MenuItem(self.helpMenu, 160, text="About", kind=wx.ITEM_NORMAL)
        self.helpMenu.Append(self.aboutItem)
        self.updateItem = wx.MenuItem(self.helpMenu, 161, text="Check for Updates", kind=wx.ITEM_NORMAL)
        self.helpMenu.Append(self.updateItem)
        self.updateItem.Enable(False)
        self.rollbackItem = wx.MenuItem(self.helpMenu, 162, text="Rollback", kind=wx.ITEM_NORMAL)
        self.helpMenu.Append(self.rollbackItem)
        self.rollbackItem.Enable(False)
        self.menubar.Append(self.helpMenu, '&Help')

        self.Bind(wx.EVT_MENU, self.menuhandler)
        self.connectbutton = wx.BitmapButton(self.panel, bitmap=self.connect_img,pos=(10, 10), size=(100, 25), name='connect')
        self.connectbutton.Bind(wx.EVT_BUTTON, self.OnNodeConnect)
        self.connectbutton.SetToolTip(wx.ToolTip("Connect to Nineteen68 Server"))
        self.log = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(12, 38), size=(760,500), style = wx.TE_MULTILINE|wx.TE_READONLY)
        font1 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL,  False, 'Consolas')
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
        if self.logfilename_error_flag or self.is_config_invalid or self.is_config_missing:
            self.cancelbutton.Disable()
            self.terminatebutton.Disable()
            self.clearbutton.Disable()
            self.connectbutton.Disable()
            self.rbox.Disable()
        self.DisableAll()
        updatecheckFlag = configvalues['update_check'].lower() == 'no'
        browsercheckFlag = configvalues['browser_check'].lower() == 'no'
        self.OnClear(wx.EVT_LEFT_DOWN)
        self.verifyMACAddress()
        self.connectbutton.SetFocus()

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
        elif id==151:      # When user selects Tools > Generate PDF Report
            try:
                if (self.pluginPDF!= None) and (bool(self.pluginPDF) != False):
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
                About_window(parent = None,id = -1, title="About")
            except Exception as e:
                msg = "Error while selecting about file"
                logger.print_on_console(msg)
                log.info(msg)
                log.error(e)
        elif id==161:      # When user selects Edit > Check for updates
            try:
                log.info('--Check for updates selected--')
                Check_Update_window(parent = None,id = -1, title="Check for Updates")
            except Exception as e:
                msg = "Error while updating file"
                logger.print_on_console(msg)
                log.info(msg)
                log.error(e)

        elif id==162:      # When user selects Edit > Rollback
            try:
                log.info('--Rollback selected--')
                rollback_window(parent = None,id = -1, title="Rollback")
            except Exception as e:
                msg = "Error while rolling back file"
                logger.print_on_console(msg)
                log.info(msg)
                log.error(e)

    def onChecked_Schedule(self, e):
        global connection_Timer,socketIO
        conn_time = float(configvalues['connection_timeout'])
        if conn_time >= 8:
            if (connection_Timer != None and connection_Timer.isAlive()):
                connection_Timer.cancel()
                log.info("Timer Restarted due to change in connection mode")
            else:
                log.info("Connection Timeout timer Started")
            connection_Timer = threading.Timer(conn_time*60*60, wxObject.closeConnection)
            connection_Timer.start()
        mode=self.schedule.GetValue()
        msg = ("En" if mode else "Dis") + "abling Schedule mode"
        logger.print_on_console(msg)
        log.info(msg)
        socketIO.emit('toggle_schedule',mode)

    def onRadioBox(self,e):
        self.choice=self.rbox.GetStringSelection()
        logger.print_on_console(str(self.choice)+' is Selected')
        if self.choice == 'Normal':
            self.breakpoint.Clear()
            self.breakpoint.Disable()
            self.killChildWindow(debug=True)
        self.debug_mode=False
        # self.breakpoint.Disable()
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
        global connection_Timer
        controller.terminate_flag=True
        controller.disconnect_flag=True
        logger.print_on_console('Disconnected from Nineteen68 server')
        if (connection_Timer != None and connection_Timer.isAlive()):
            log.info("Connection Timeout timer Stopped")
            connection_Timer.cancel()
            connection_Timer=None
        stat = self.killChildWindow(True,True,True,True)
        if stat[1]: socketIO.emit('scrape','Terminate')
        self.killSocket(True)
        self.Destroy()
        controller.kill_process()
        if SYSTEM_OS == "Windows":
            os.system("TASKKILL /F /IM nineteen68MFapi.exe")
        sys.exit(0)

    def OnKillProcess(self, event):
        controller.kill_process()

    def OnTerminate(self, event, state=''):
        global execution_flag
        stat = self.killChildWindow(True,True,True,True)
        if stat[1]: socketIO.emit('scrape','Terminate')
        if(state=="term_exec"):
            controller.disconnect_flag=True
            print("")
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
        self.schedule.Enable()
        execution_flag = False

    def OnClear(self,event):
        self.log.Clear()
        print('********************************************************************************************************')
        print('============================================ '+self.appName+' ============================================')
        print('********************************************************************************************************')

    def OnNodeConnect(self,event):
        try:
            global socketIO, connection_Timer
            name = self.connectbutton.GetName()
            self.connectbutton.Disable()
            if(name == 'connect'):
                port = int(configvalues['server_port'])
                conn = http.client.HTTPConnection(configvalues['server_ip'],port)
                conn.connect()
                conn.close()
                self.socketthread = SocketThread()
                self.rollbackItem.Enable(True)
                self.updateItem.Enable(True)
            else:
                self.OnTerminate(event,"term_exec")
                self.killSocket(True)
                log.info('Disconnected from Nineteen68 server')
                logger.print_on_console('Disconnected from Nineteen68 server')
                self.connectbutton.SetBitmapLabel(self.connect_img)
                self.connectbutton.SetName('connect')
                self.connectbutton.SetToolTip(wx.ToolTip("Connect to Nineteen68 Server"))
                self.schedule.SetValue(False)
                self.schedule.Disable()
                self.connectbutton.Enable()
                self.rollbackItem.Enable(False)
                self.updateItem.Enable(False)
                if (connection_Timer != None and connection_Timer.isAlive()):
                    log.info("Connection Timeout Timer Stopped")
                    connection_Timer.cancel()
                    connection_Timer=None
        except Exception as e:
            emsg="Forbidden request, Connection refused, please configure server ip and server port in Edit -> Configuration, and re-connect."
            logger.print_on_console(emsg)
            log.error(emsg)
            self.cancelbutton.Disable()
            self.terminatebutton.Disable()
            self.clearbutton.Disable()
            self.connectbutton.Enable()
            self.rbox.Disable()
            log.error(e,exc_info=True)

    def killSocket(self, disconn=False):
        #Disconnects socket client
        global socketIO
        try:
            if socketIO is not None:
                if disconn:
                    log.info('Sending socket disconnect request')
                    socketIO.send('unavailableLocalServer', dnack = True)
                socketIO.disconnect()
                del socketIO
                socketIO = None
                wxObject.socketthread.join()
                log.info('Connection Closed')
        except Exception as e:
            log.error("Error while closing connection")
            log.error(e,exc_info=True)

    def closeConnection(self):
        global closeActiveConnection
        try:
            if execution_flag:
                err_msg="Delaying closing Connection due to active execution."
                closeActiveConnection = True
            else:
                self.killSocket()
                err_msg="Closing active connection due to timeout."
            logger.print_on_console(err_msg)
            log.info(err_msg)
        except Exception as e:
            err_msg="Error while closing connection"
            logger.print_on_console(err_msg)
            log.error(err_msg)
            log.error(e)

    def killChildWindow(self, debug=False, scrape=False, display=False, pdf=False):
        #Close the debug window
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
        try:
            global mobileScrapeFlag,qcConFlag,mobileWebScrapeFlag,desktopScrapeFlag, pdfScrapeFlag
            global sapScrapeFlag,debugFlag,browsername,action,oebsScrapeFlag
            global socketIO,data
            #con = controller.Controller()
            self.schedule.Disable()
            if(irisFlag == True):
                core_utils.get_all_the_imports('IRIS')
            if mobileScrapeFlag==True:
                self.scrapewindow = mobileScrapeObj.ScrapeWindow(parent = self,id = -1, title="SLK Nineteen68 - Mobile Scrapper",filePath = browsername,socketIO = socketIO)
                mobileScrapeFlag=False
            elif qcConFlag==True:
                self.scrapewindow = qcConObj.QcWindow(parent = None,id = -1, title="SLK Nineteen68 - Mobile Scrapper",filePath = qcdata,socketIO = socketIO)
                qcConFlag=False
            elif mobileWebScrapeFlag==True:
                self.scrapewindow = mobileWebScrapeObj.ScrapeWindow(parent = self,id = -1, title="SLK Nineteen68 - Mobile Scrapper",browser = browsername,socketIO = socketIO)
                mobileWebScrapeFlag=False
            elif desktopScrapeFlag==True:
                self.scrapewindow = desktopScrapeObj.ScrapeWindow(parent = self,id = -1, title="SLK Nineteen68 - Desktop Scrapper",filePath = browsername,socketIO = socketIO,irisFlag = irisFlag)
                desktopScrapeFlag=False
                browsername = ''
            elif sapScrapeFlag==True:
                self.scrapewindow = sapScrapeObj.ScrapeWindow(parent = self,id = -1, title="SLK Nineteen68 - SAP Scrapper",filePath = browsername,socketIO = socketIO,irisFlag = irisFlag)
                sapScrapeFlag=False
            elif oebsScrapeFlag==True:
                self.scrapewindow = oebsScrapeObj.ScrapeDispatcher(parent = self,id = -1, title="SLK Nineteen68 - Oebs Scrapper",filePath = browsername,socketIO = socketIO,irisFlag = irisFlag)
                oebsScrapeFlag=False
            elif pdfScrapeFlag==True:
                self.scrapewindow = pdfScrapeObj.ScrapeDispatcher(parent = self,id = -1, title="SLK Nineteen68 - PDF Scrapper",filePath = browsername,socketIO = socketIO,irisFlag = irisFlag)
                pdfScrapeFlag=False
            elif debugFlag == True:
                self.debugwindow = DebugWindow(parent = None,id = -1, title="Debugger")
                debugFlag = False
            else:
                browsernumbers = ['1','2','3','6']
                if browsername in browsernumbers:
                    logger.print_on_console('Browser name : '+str(browsername))
                    #con = controller.Controller()
                    core_utils.get_all_the_imports('Web')
                    core_utils.get_all_the_imports('WebScrape')
                    import Nineteen68_WebScrape
                    self.scrapewindow = Nineteen68_WebScrape.ScrapeWindow(parent = self,id = -1, title="SLK Nineteen68 - Web Scrapper",browser = browsername,socketIO = socketIO,action=action,data=data,irisFlag = irisFlag)
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
                    elif flag == 'debug':
                        #call debug logic
                        self.pausewindow = pause_display_operation.Debug(parent = self,id = -1, title="SLK Nineteen68 - Debug Mode",input = inputvalue)
                    elif flag == 'error':
                        #call debug error logic
                        self.pausewindow = pause_display_operation.Error(parent = self,id = -1, title="SLK Nineteen68 - Debug Mode",input = inputvalue)
        except Exception as e:
            log.error(e,exc_info=True)

    def verifyMACAddress(self):
        flag = False
        core_utils_obj = core_utils.CoreUtils()
        system_mac = core_utils_obj.getMacAddress()
        mac_verification_key = "".join(['N','1','i','1','N','2','e','3','T','5','e','8','E','1','3','n','2','1','S','i','X','t','Y','3','4','e','I','g','H','t','5','5'])
        irisMAC = []
        execMAC=[]
        global irisFlag
        global executionOnly
        try:
            with open(CERTIFICATE_PATH+'/license.key', mode='r') as f:
                key = "".join(f.readlines()[1:-1]).replace("\n","").replace("\r","")
                key = core_utils_obj.unwrap(key, mac_verification_key)
                mac_addr = key[36:-36]
                mac_addr = (mac_addr.replace('-',':').replace(' ','')).lower().split(",")
                index = 0
                for mac in mac_addr:
                    iris_index=-1
                    if "iris" in mac:
                        iris_index=mac.index("iris")+4
                        mac_addr[index] = mac[iris_index:]
                        irisMAC.append(mac[iris_index:])
                    if "exec_only" in mac:
                        exec_index=mac.index("exec_only")+9
                        if iris_index > -1:
                            exec_index=iris_index
                        mac_addr[index] = mac[exec_index:]
                        execMAC.append(mac[exec_index:])
                    index = index + 1
                if(system_mac in mac_addr):
                    flag = True
                    if system_mac in execMAC:
                        executionOnly=True
                    if ((system_mac in irisMAC) and os.path.isdir(NINETEEN68_HOME+'/plugins/IRIS')):
                        irisFlag = True
                        controller.iris_flag = True
        except Exception as e:
            log.error(e,exc_info=True)
        if not flag:
            msg = "Unauthorized: Access denied, system is not registered with Nineteen68"
            logger.print_on_console(msg)
            log.error(msg)
        else: self.EnableAll()
        return flag

    def DisableAll(self):
        self.enabledStatus = [self.menubar.IsEnabledTop(0),self.menubar.IsEnabledTop(1),
            self.connectbutton.IsEnabled(),self.schedule.IsEnabled(),self.rbox.IsEnabled(),
            self.cancelbutton.IsEnabled(),self.terminatebutton.IsEnabled(),self.clearbutton.IsEnabled()]
        self.menubar.EnableTop(0,False)
        self.menubar.EnableTop(1,False)
        self.connectbutton.Disable()
        self.schedule.Disable()
        self.rbox.Disable()
        self.cancelbutton.Disable()
        self.terminatebutton.Disable()
        self.clearbutton.Disable()

    def EnableAll(self):
        if self.enabledStatus[0]: self.menubar.EnableTop(0,True)
        if self.enabledStatus[1]: self.menubar.EnableTop(1,True)
        if self.enabledStatus[2]: self.connectbutton.Enable()
        if self.enabledStatus[3]: self.schedule.Enable()
        if self.enabledStatus[4]: self.rbox.Enable()
        if self.enabledStatus[5]: self.cancelbutton.Enable()
        if self.enabledStatus[6]: self.terminatebutton.Enable()
        if self.enabledStatus[7]: self.clearbutton.Enable()


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
            "Frame":[(300, 150),(470,700)],
            "S_address":[(12,8 ),(90, 28),(100,8 ),(140,-1)],
            "S_port": [(270,8 ),(70, 28),(340,8 ), (105,-1)],
            "Chrm_path":[(12,38),(80, 28),(100,38), (310,-1),(415,38),(30, -1)],
            "Ffox_path":[(12,68),(80, 28),(100,68), (310,-1),(415,68),(30, -1)],
            "Log_path":[(12,98),(80, 28),(100,98), (310,-1),(415,98),(30, -1)],
            "Q_timeout":[(12,128),(85, 28),(100,128), (80,-1)],
            "Timeout":[(185,128),(50, 28),(240,128), (80,-1)],
            "Delay":[(325,128),(40, 28),(360,128), (85,-1)],
            "Step_exec":[(12,158),(120, 28),(130,158),(80,-1)],
            "Disp_var":[(225,158),(140, 28),(360,158), (85,-1)],
            "S_cert":[(12,188),(85, 28),(100,188),(310,-1),(415,188),(30, -1)],
            "C_Timeout" :[(12,218),(120, 28),(130,218), (80,-1)],
            "Delay_Stringinput":[(225,218),(140, 28),(360,218), (85,-1)],
            "Ignore_cert":[(12,248)],
            "IE_arch":[(150,248)],
            "Dis_s_cert":[(290,248)],
            "Ex_flag":[(12,308)],
            "Ignore_v_check":[(150,308)],
            "S_flag":[(340,368)],
            "Ret_url":[(12,368)],
            "En_secu_check":[(308,308)],
            "Brow_ch":[(115,368)],
            "High_ch":[ (225,368)],
            "Iris_prediction":[(12,428)],
            "hide_soft_key":[(180,428)],
            "extn_enabled":[(320,428)],
            "update_check":[(12,488)],
            "Save":[(100,608), (100, 28)],
            "Close":[(250,608), (100, 28)]
        }
        else:
            config_fields={
            "Frame":[(300, 150),(600,700)],
            "S_address":[(12,8),(90,28),(116,8 ),(140,-1)],
            "S_port": [(352,8),(70,28),(430,8 ),(105,-1)],
            "Chrm_path":[(12,38),(80,28),(116,38),(382,-1),(504,38),(30, -1)],
            "Ffox_path":[(12,68),(80,28),(116,68),(382,-1),(504,68),(30, -1)],
            "Log_path":[(12,98),(80, 28),(116,98),(382,-1),(504,98),(30, -1)],
            "Q_timeout":[(12,128),(85, 28),(116,128), (80,-1)],
            "Timeout":[(225,130),(50, 28),(290,130),(80,-1)],
            "Delay":[(404,128),(40, 28),(448,128), (85,-1)],
            "Step_exec":[(12,158),(120, 28),(142,158),(80,-1)],
            "Disp_var":[(288,158),(140, 28),(448,158),(85,-1)],
            "S_cert":[(12,188),(85, 28),(116,188),(382,-1),(504,188),(30, -1)],
            "Ignore_cert":[(20,318)],
            "IE_arch":[(158,258)],
            "Dis_s_cert":[(335,258)],
            "Ex_flag":[(12,258)],
            "Ignore_v_check":[(170,318)],
            "S_flag":[(396,378)],
            "Ret_url":[(12,378)],
            "En_secu_check":[(358,318)],
            "Brow_ch":[(130,378)],
            "High_ch":[(260,378)],
            "Save":[(130,550),(100, 28)],
            "C_Timeout" :[(12,218),(120, 28),(180,218), (80,-1)],
            "Delay_Stringinput":[(288,218),(140, 28),(448,218), (85,-1)],
            "Iris_prediction":[(12,428)],
            "hide_soft_key":[(230,428)],
            "extn_enabled":[(400,428)],
            "update_check":[(12,480)],
            "Close":[(370,550),(120, 28)]
        }
        wx.Frame.__init__(self, parent, title=title,
                   pos=config_fields["Frame"][0], size=config_fields["Frame"][1], style = wx.CAPTION|wx.CLIP_CHILDREN)
        self.SetBackgroundColour('#e6e7e8')
        self.iconpath = IMAGES_PATH +"slk.ico"
        self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.wicon)
        self.updated = False
        self.panel = wx.Panel(self)

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
            self.log_file_path.SetValue(os.path.normpath(NINETEEN68_HOME + '/logs/TestautoV2.log'))
        else:
            self.log_file_path.SetValue(isConfigJson['logFile_Path'])

        self.qu_timeout=wx.StaticText(self.panel, label="Query Timeout", pos=config_fields["Q_timeout"][0],size=config_fields["Q_timeout"][1], style=0, name="")
        self.query_timeout=wx.TextCtrl(self.panel, pos=config_fields["Q_timeout"][2], size=config_fields["Q_timeout"][3])
        if isConfigJson['queryTimeOut']=="":
            self.query_timeout.SetValue("sec")
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.query_timeout.SetFont(font)
            self.query_timeout.SetForegroundColour('#848484')
        elif isConfigJson!=False:
            self.query_timeout.SetValue(isConfigJson['queryTimeOut'])
        else:
            self.query_timeout.SetValue("3")

        self.timeOut=wx.StaticText(self.panel, label="Time Out", pos=config_fields["Timeout"][0],size=config_fields["Timeout"][1], style=0, name="")
        self.time_out=wx.TextCtrl(self.panel, pos=config_fields["Timeout"][2], size=config_fields["Timeout"][3])
        if isConfigJson['timeOut']=="":
            self.time_out.SetValue("sec")
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.time_out.SetFont(font)
            self.time_out.SetForegroundColour('#848484')
        elif isConfigJson!=False:
            self.time_out.SetValue(isConfigJson['timeOut'])
        else:
            self.time_out.SetValue("1")

        self.delayText=wx.StaticText(self.panel, label="Delay", pos=config_fields["Delay"][0],size=config_fields["Delay"][1], style=0, name="")
        self.delay=wx.TextCtrl(self.panel, pos=config_fields["Delay"][2], size=config_fields["Delay"][3])
        if isConfigJson['delay']=="":
            self.delay.SetValue("sec")
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.delay.SetFont(font)
            self.delay.SetForegroundColour('#848484')
        elif isConfigJson!=False:
            self.delay.SetValue(isConfigJson['delay'])
        else:
            self.delay.SetValue("0.3")

        #Delay input box kept for provide the delay in typestring.
        self.delay_stringinput=wx.StaticText(self.panel, label="Delay for StringInput", pos=config_fields["Delay_Stringinput"][0],size=config_fields["Delay_Stringinput"][1], style=0, name="")
        self.Delay_input=wx.TextCtrl(self.panel, pos=config_fields["Delay_Stringinput"][2], size=config_fields["Delay_Stringinput"][3])
        if isConfigJson['delay_stringinput']=="":
            self.Delay_input.SetValue("sec")
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.Delay_input.SetFont(font)
            self.Delay_input.SetForegroundColour('#848484')
        elif isConfigJson!=False:
            self.Delay_input.SetValue(isConfigJson['delay_stringinput'])
        else:
            self.Delay_input.SetValue("0.005")

        self.stepExecWait=wx.StaticText(self.panel, label="Step Execution Wait", pos=config_fields["Step_exec"][0],size=config_fields["Step_exec"][1], style=0, name="")
        self.step_exe_wait=wx.TextCtrl(self.panel, pos=config_fields["Step_exec"][2], size=config_fields["Step_exec"][3])
        if isConfigJson['stepExecutionWait']=="":
            self.step_exe_wait.SetValue("sec")
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.step_exe_wait.SetFont(font)
            self.step_exe_wait.SetForegroundColour('#848484')
        elif isConfigJson!=False:
            self.step_exe_wait.SetValue(isConfigJson['stepExecutionWait'])
        else:
            self.step_exe_wait.SetValue("1")

        self.dispVarTimeOut=wx.StaticText(self.panel, label="Display Variable Timeout", pos=config_fields["Disp_var"][0],size=config_fields["Disp_var"][1], style=0, name="")
        self.disp_var_timeout=wx.TextCtrl(self.panel, pos=config_fields["Disp_var"][2], size=config_fields["Disp_var"][3])
        if isConfigJson['displayVariableTimeOut']=="":
            self.disp_var_timeout.SetValue("sec")
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.disp_var_timeout.SetFont(font)
            self.disp_var_timeout.SetForegroundColour('#848484')
        else:
            self.disp_var_timeout.SetValue(isConfigJson['displayVariableTimeOut'])
        
        

        self.sev_cert=wx.StaticText(self.panel, label="Server Cert", pos=config_fields["S_cert"][0],size=config_fields["S_cert"][1], style=0, name="")
        self.server_cert=wx.TextCtrl(self.panel, pos=config_fields["S_cert"][2], size=config_fields["S_cert"][3])
        self.server_cert_btn=wx.Button(self.panel, label="...",pos=config_fields["S_cert"][4], size=config_fields["S_cert"][5])
        self.server_cert_btn.Bind(wx.EVT_BUTTON, self.fileBrowser_servcert)
        if (not isConfigJson) or (isConfigJson and isConfigJson['server_cert']=='./assets/CA_BUNDLE/server.crt'):
            self.server_cert.SetValue(os.path.normpath(CERTIFICATE_PATH + '/server.crt'))
        else:
            self.server_cert.SetValue(isConfigJson['server_cert'])

        self.connection_timeout=wx.StaticText(self.panel, label="Connection Timeout", pos=config_fields["C_Timeout"][0],size=config_fields["C_Timeout"][1], style=0, name="")
        self.conn_timeout=wx.TextCtrl(self.panel,id=9,pos=config_fields["C_Timeout"][2], size=config_fields["C_Timeout"][3])
        
        if isConfigJson!=False and int(isConfigJson['connection_timeout'])>=8:
            self.conn_timeout.SetValue(isConfigJson['connection_timeout'])
        else:
            self.conn_timeout.SetValue("0")
        
        ## Binding placeholders and restricting textareas to just numeric characters
        self.disp_var_timeout.Bind(wx.EVT_SET_FOCUS,self.toggle1_generic)
        self.disp_var_timeout.Bind(wx.EVT_KILL_FOCUS,self.toggle2_generic)
        self.disp_var_timeout.Bind(wx.EVT_CHAR, self.handle_keypress)
        
        self.query_timeout.Bind(wx.EVT_SET_FOCUS,self.toggle1_generic)
        self.query_timeout.Bind(wx.EVT_KILL_FOCUS,self.toggle2_generic)
        self.query_timeout.Bind(wx.EVT_CHAR, self.handle_keypress)

        self.time_out.Bind(wx.EVT_SET_FOCUS,self.toggle1_generic)
        self.time_out.Bind(wx.EVT_KILL_FOCUS,self.toggle2_generic)
        self.time_out.Bind(wx.EVT_CHAR, self.handle_keypress)
        
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
        self.rbox1 = wx.RadioBox(self.panel, label = 'Ignore Certificate', pos = config_fields["Ignore_cert"][0], choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['ignore_certificate'].title()==lblList[0]:
            self.rbox1.SetSelection(0)
        else:
            self.rbox1.SetSelection(1)

        self.rbox2 = wx.RadioBox(self.panel, label = 'IE Architecture Type', pos = config_fields["IE_arch"][0], choices = lblList2,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['bit_64'].title() != 'Yes':
            self.rbox2.SetSelection(1)
        else:
            self.rbox2.SetSelection(0)

        self.rbox9 = wx.RadioBox(self.panel, label = 'Disable Server Cert Check', pos = config_fields["Dis_s_cert"][0], choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['disable_server_cert'].title() == lblList[0]:
            self.rbox9.SetSelection(0)
        else:
            self.rbox9.SetSelection(1)

        self.rbox5 = wx.RadioBox(self.panel, label = 'Exception Flag', pos = config_fields["Ex_flag"][0], choices = lblList4,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['exception_flag'].title()!=lblList4[0]:
            self.rbox5.SetSelection(1)
        else:
            self.rbox5.SetSelection(0)

        self.rbox6 = wx.RadioBox(self.panel, label = 'Ignore Visibility Check', pos = config_fields["Ignore_v_check"][0], choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['ignoreVisibilityCheck'].title()==lblList[0]:
            self.rbox6.SetSelection(0)
        else:
            self.rbox6.SetSelection(1)

        self.rbox3 = wx.RadioBox(self.panel, label = 'ScreenShot Flag', pos = config_fields["S_flag"][0], choices = lblList3,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['screenShot_Flag'].title()!=lblList3[0]:
            self.rbox3.SetSelection(1)
        else:
            self.rbox3.SetSelection(0)

        self.rbox4 = wx.RadioBox(self.panel, label = 'Retrieve URL', pos = config_fields["Ret_url"][0], choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['retrieveURL'].title()!=lblList[0]:
            self.rbox4.SetSelection(1)
        else:
            self.rbox4.SetSelection(0)

        self.rbox7 = wx.RadioBox(self.panel, label = 'Enable Security Check', pos = config_fields["En_secu_check"][0], choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['enableSecurityCheck'].title()==lblList[0]:
            self.rbox7.SetSelection(0)
        else:
            self.rbox7.SetSelection(1)

        self.rbox8 = wx.RadioBox(self.panel, label = 'Browser Check', pos = config_fields["Brow_ch"][0], choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['browser_check'].title()!=lblList[0]:
            self.rbox8.SetSelection(1)
        else:
            self.rbox8.SetSelection(0)

        self.rbox10 = wx.RadioBox(self.panel, label = 'Highlight Check', pos = config_fields["High_ch"][0], choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['highlight_check'].title()==lblList[0]:
            self.rbox10.SetSelection(0)
        else:
            self.rbox10.SetSelection(1)

        self.rbox11 = wx.RadioBox(self.panel, label = 'Prediction for IRIS Objects', pos = config_fields["Iris_prediction"][0], choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson!=False and isConfigJson['prediction_for_iris_objects'].title()==lblList[0]:
            self.rbox11.SetSelection(0)
        else:
            self.rbox11.SetSelection(1)

        self.rbox12 = wx.RadioBox(self.panel, label = "Hide Soft. Keyboard", pos = config_fields["hide_soft_key"][0], choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['hide_soft_key'].title() == lblList[0]:
            self.rbox12.SetSelection(0)
        else:
            self.rbox12.SetSelection(1)

        self.rbox13 = wx.RadioBox(self.panel, label = "Extension Enable", pos = config_fields["extn_enabled"][0], choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['extn_enabled'].title() == lblList[0]:
            self.rbox13.SetSelection(0)
        else:
            self.rbox13.SetSelection(1)

        self.rbox14 = wx.RadioBox(self.panel, label = "Update Check", pos = config_fields["update_check"][0], choices = lblList,
         majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        if isConfigJson != False and isConfigJson['update_check'].title() == lblList[0]:
            self.rbox14.SetSelection(0)
        else:
            self.rbox14.SetSelection(1)

        self.error_msg=wx.StaticText(self.panel, label="", pos=(85,568),size=(350, 28), style=0, name="")
        self.save_btn=wx.Button(self.panel, label="Save",pos=config_fields["Save"][0], size=config_fields["Save"][1])
        self.save_btn.Bind(wx.EVT_BUTTON, self.config_check)
        self.close_btn=wx.Button(self.panel, label="Close",pos=config_fields["Close"][0], size=config_fields["Close"][1])
        self.close_btn.Bind(wx.EVT_BUTTON, self.close)
        self.Bind(wx.EVT_CLOSE, self.close)

        if wxObject.connectbutton.GetName().lower() != "connect":
            self.sev_add.Enable(False)
            self.server_add.Enable(False)
            self.sev_port.Enable(False)
            self.server_port.Enable(False)
            self.sev_cert.Enable(False)
            self.server_cert.Enable(False)
            self.server_cert_btn.Enable(False)

        self.Centre()
        wx.Frame(self.panel)
        self.Show()

    #allows only integer and float values 
    def handle_keypress(self, event):
        keycode = event.GetKeyCode()
        if chr(keycode) in ['0','1','2','3','4','5','6','7','8','9','.','\x08','ĺ','ļ','Ĺ','ĸ','\x7f']:
            event.Skip()

    def toggle1_generic(self,evt):
        self.demo=evt.EventObject
        if self.demo.Id == 9:
            if self.demo.GetValue()=="0 or >=8 hrs":
                self.demo.SetValue("")
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
                self.demo.SetFont(font)
                self.demo.SetForegroundColour('#000000')
            evt.Skip()
        else:
            if self.demo.GetValue()=="sec":
                self.demo.SetValue("")
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
                self.demo.SetFont(font)
                self.demo.SetForegroundColour('#000000')
            evt.Skip()
    
    

    def toggle2_generic(self,evt):
        self.demo=evt.EventObject
        if self.demo.Id == 9:
            if self.demo.GetValue() == "":
                self.demo.SetValue("0 or >=8 hrs")
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
                self.demo.SetFont(font)
                self.demo.SetForegroundColour('#848484')
            evt.Skip()
        else:
            if self.demo.GetValue() == "":
                self.demo.SetValue("sec")
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
                self.demo.SetFont(font)
                self.demo.SetForegroundColour('#848484')
            evt.Skip()



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
        firefox_path=self.firefox_path.GetValue()
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
        iris_prediction = self.rbox11.GetStringSelection()
        hide_soft_key = self.rbox12.GetStringSelection()
        conn_timeout = self.conn_timeout.GetValue()
        extn_enabled = self.rbox13.GetStringSelection()
        update_check = self.rbox14.GetStringSelection()
        delay_string_in = self.Delay_input.GetValue()
        #----------------creating data dictionary
        data['server_ip'] = server_add.strip()
        data['server_port'] = server_port.strip()
        data['ignore_certificate'] = ignore_certificate.strip()
        data['chrome_path'] = chrome_path.strip() if chrome_path.strip().lower()!='default' else 'default'
        data['firefox_path'] = firefox_path.strip() if firefox_path.strip().lower()!='default' else 'default'
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
        data['prediction_for_iris_objects'] = iris_prediction.strip()
        data['hide_soft_key'] = hide_soft_key.strip()
        data['connection_timeout']= conn_timeout.strip()
        data['extn_enabled']= extn_enabled.strip()
        data['update_check']= update_check.strip()
        data['delay_stringinput']=delay_string_in.strip()
        config_data=data
        if (data['server_ip']!='' and data['server_port']!='' and data['server_cert']!='' and
            data['chrome_path']!='' and data['queryTimeOut'] not in ['','sec'] and data['logFile_Path']!='' and
            data['delay'] not in ['','sec'] and data['timeOut'] not in ['','sec'] and data['stepExecutionWait'] not in ['','sec'] and
            data['displayVariableTimeOut'] not in ['','sec'] and data['delay_stringinput'] not in ['','sec'] and data['firefox_path']!='' and  data['connection_timeout'] not in ['','0 or >=8 hrs']):
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
            self.ff_path.SetLabel('Firefox Path')
            self.ff_path.SetForegroundColour((0,0,0))
            self.delayText.SetLabel('Delay')
            self.delayText.SetForegroundColour((0,0,0))
            self.timeOut.SetLabel('Time Out')
            self.timeOut.SetForegroundColour((0,0,0))
            self.stepExecWait.SetLabel('Step Execution Wait')
            self.stepExecWait.SetForegroundColour((0,0,0))
            self.dispVarTimeOut.SetLabel('Display Variable Timeout')
            self.dispVarTimeOut.SetForegroundColour((0,0,0))
            self.connection_timeout.SetLabel('Connection Timeout')
            self.connection_timeout.SetForegroundColour((0,0,0))
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
            if (os.path.isfile(data['chrome_path'])==True or str(data['chrome_path']).strip()=='default') and os.path.isfile(data['server_cert'])==True and os.path.isfile(data['logFile_Path'])==True and (os.path.isfile(data['firefox_path'])==True or str(data['firefox_path']).strip()=='default'):
                if int(data['connection_timeout'])in range(1, 8):
                    self.error_msg.SetLabel("Connection Timeout must be greater than or equal to 8")
                    self.error_msg.SetForegroundColour((255,0,0))
                    self.connection_timeout.SetForegroundColour((255,0,0))
                else:
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

                if os.path.isfile(data['firefox_path'])==True or str(data['firefox_path']).strip()=='default':
                    self.ff_path.SetLabel('Firefox Path')
                    self.ff_path.SetForegroundColour((0,0,0))
                elif  os.path.isfile(data['firefox_path'])!=True:
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
                self.delay_stringinput.SetLabel('Delay for stringinput*')
                self.delay_stringinput.SetForegroundColour((255,0,0))
            else:
                self.delay_stringinput.SetLabel('Delay for stringinput')
                self.delay_stringinput.SetForegroundColour((0,0,0))
            if data['queryTimeOut']=="sec":
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
            if data['firefox_path']=='':
                self.ff_path.SetLabel('Firefox Path*')
                self.ff_path.SetForegroundColour((255,0,0))
            else:
                self.ff_path.SetLabel('Firefox Path')
                self.ff_path.SetForegroundColour((0,0,0))
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
        dlg = wx.FileDialog(self, message="Choose a file ...",defaultDir=NINETEEN68_HOME,defaultFile="", wildcard="Chrome executable (*chrome.exe)|*chrome.exe|" \
            "All files (*.*)|*.*", style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.chrome_path.SetValue(path)
        dlg.Destroy()
    """This method open a file selector dialog , from where file path can be set """
    def fileBrowser_ffpath(self,event):
        dlg = wx.FileDialog(self, message="Choose a file ...",defaultDir=NINETEEN68_HOME,defaultFile="", wildcard="Firefox executable (*firefox.exe)|*firefox.exe|" \
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
        dlg = wx.FileDialog(self, message="Choose a file ...",defaultDir=NINETEEN68_HOME,defaultFile="", wildcard="Certificate file (*.crt)|*.crt|" \
            "All files (*.*)|*.*", style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.server_cert.SetValue(path)
        dlg.Destroy()

    """This method closes the wxPython config window instance"""
    def close(self, event):
        self.Destroy()
        global configvalues, browsercheckFlag, chromeFlag, firefoxFlag,updatecheckFlag
        configvalues = readconfig.readConfig().readJson() # Re-reading config values
        browsercheckFlag=False
        if configvalues['browser_check'].lower() == 'no':
            browsercheckFlag=True
            chromeFlag=firefoxFlag=False
        updatecheckFlag = configvalues['update_check'].lower() == 'no'
        try:
            logfilename = os.path.normpath(configvalues["logFile_Path"]).replace("\\","\\\\")
            logging.config.fileConfig(LOGCONFIG_PATH,defaults={'logfilename': logfilename},disable_existing_loggers=False)
        except Exception as e:
            log.error(e)
        wxObject.EnableAll()
        if self.updated:
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
            msg = 'A product of Dimension Labs \n'
            msg = msg +str(self.get_Info_1(data))+str(self.get_Info_2(data))+str(self.get_Info_3(data))+str(self.get_Info_4())+str(self.get_Info_5(data))+str(self.get_Info_6())
            #------------------------------------Different co-ordinates for Windows and Mac
            if SYSTEM_OS=='Windows':
                upload_fields= {
                "Frame":[(300, 150),(465,220)],
                "disp_msg":[(12,18),(80, 28),(100,18), (310,-1),(415,18),(30, -1)],
                "Close":[(340,148), (100, 28)]
            }
            else:
                upload_fields={
                "Frame":[(300, 150),(550,220)],#(diff +85,+10 from windows)
                "disp_msg":[(12,38),(80,28),(116,38),(382,-1),(504,38),(30, -1)],
                "Close":[(285,88),(100, 28)]
            }
            wx.Frame.__init__(self, parent, title=title,pos=upload_fields["Frame"][0], size=upload_fields["Frame"][1], style = wx.CAPTION|wx.CLIP_CHILDREN)
            self.SetBackgroundColour('#e6e7e8')
            self.iconpath = IMAGES_PATH +"slk.ico"
            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.wicon)
            self.panel = wx.Panel(self)
            self.disp_msg = wx.TextCtrl(self.panel, pos = upload_fields["disp_msg"][0], size = (425, 120), style = wx.TE_MULTILINE|wx.TE_READONLY)
            self.close_btn = wx.Button(self.panel, label="Close",pos=upload_fields["Close"][0], size=upload_fields["Close"][1])
            self.close_btn.Bind(wx.EVT_BUTTON, self.close)
            self.disp_msg.AppendText( msg )
            self.Centre()
            wx.Frame(self.panel)
            self.Show()
        except Exception as e:
            logger.print_on_console("Error occured in About")
            log.error("Error occured in About ,Err msg : " + str(e))


    def get_client_manifest(self):
        data=None
        try:
            with open(MANIFEST_LOC) as f:
                data = json.load(f)
        except Exception as e:
            msg = 'Unable to fetch package manifest.'
            logger.print_on_console(msg)
            log.error(msg)
        return data

    def get_Info_1(self,data):
        str1=''
        try:
            str1='Version : '+list(data['version'])[0]+'.'+list(data['version'][list(data['version'])[0]]['subversion'])[0]+' \n'
        except Exception as e:
            log.error(e)
        return str1

    def get_Info_2(self,data):
        str1=''
        try:
            str1='Updated on : '+(data['version'][list(data['version'])[0]]['subversion'][list(data['version'][list(data['version'])[0]]['subversion'])[0]]['updated_on'])+' \n'
        except Exception as e:
            log.error(e)
        return str1

    def get_Info_3(self,data):
        str1=''
        try:
            str1='Baseline : '+(data['version'][list(data['version'])[0]]['subversion'][list(data['version'][list(data['version'])[0]]['subversion'])[0]]['baseline'])+' \n'
        except Exception as e:
            log.error(e)
        return str1

    def get_Info_4(self):
        return 'Copyright ?? -SLK Software Solutions \n'

    def get_Info_5(self,data):
        str1=''
        try:
            str1='Fixes :'+' \n'
            b=(data['version'][list(data['version'])[0]]['subversion'][list(data['version'][list(data['version'])[0]]['subversion'])[0]]['fixes'])
            for i in b:
                str1=str1+i+' : '+b[i]+' \n'
        except Exception as e:
            log.error(e)
        return str1

    def get_Info_6(self):
        return 'For any queries write to us @ : support.nineteen68@slkgroup.com'

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
            self.iconpath = IMAGES_PATH +"slk.ico"
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
            update_obj.run_updater()
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
            self.iconpath = IMAGES_PATH +"slk.ico"
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
            res = os.path.exists(os.path.normpath(NINETEEN68_HOME+'/assets/Nineteen68_backup.7z'))
            self.rollback_obj = update_module.Update_Rollback()
            if ( res == False ):
                self.disp_msg.AppendText( "Nineteen68 ICE backup not found, cannot rollback changes.")
            else:
                self.rollback_obj.update(None, None, None, NINETEEN68_HOME, LOC_7Z, UPDATER_LOC, 'ROLLBACK')
                self.disp_msg.AppendText( "Click 'Rollback' to run previous version of Nineteen68.")
                self.rollback_btn.Enable()
            self.Centre()
            wx.Frame(self.panel)
            self.Show()
        except Exception as e:
            log.error('Error occured in rollback_window class : ' + str(e))
            logger.print_on_console('Error occured while trying to rollback.')

    def rollback(self,event):
        """Rolls back Nineteen68"""
        try:
            self.close(event)
            logger.print_on_console("--Rolling back to previous version of Nineteen68--")
            log.info("--Rolling back to previous version of Nineteen68--")
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
        self.iconpath = IMAGES_PATH +"slk.ico"
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
        wxObject.mythread.resume(False)
        wxObject.debugwindow = None
        self.Destroy()

    def OnContinue(self, event):
        msg = "Event Triggered to proceed to next step"
        logger.print_on_console(msg)
        controller.pause_flag=False
        wxObject.mythread.resume(True)


def check_browser():
    try:
        try:
            try:
                if os.path.isfile(ICE_CONST)==True:
                    params = json.load(open(ICE_CONST))
                    if params['CHROME_VERSION'] != "":
                        for k,v in list(params['CHROME_VERSION'].items()):
                            CHROME_DRIVER_VERSION[str(k)]=[int(str(v)[:2]),int(str(v)[3:])]
                    if params['FIREFOX_VERSION'] != "":
                        for k,v in list(params['FIREFOX_VERSION'].items()):
                            FIREFOX_BROWSER_VERSION[str(k)]=[int(str(v)[:2]),int(str(v)[3:])]
                else:
                    logger.print_on_console("Unable to locate ICE parameters")
            except Exception as e:
                logger.print_on_console("Unable to locate ICE parameters")
                log.error(e)
            global chromeFlag,firefoxFlag
            logger.print_on_console('Checking for browser versions...')
            import subprocess
            from selenium import webdriver
            from selenium.webdriver import ChromeOptions
            p = subprocess.Popen(CHROME_DRIVER_PATH + ' --version', stdout=subprocess.PIPE, bufsize=1, shell=True)
            a = p.stdout.readline()
            a = a.decode('utf-8')[13:17]
            choptions1 = webdriver.ChromeOptions()
            if str(configvalues['chrome_path']).lower()!="default":
                choptions1.binary_location=str(configvalues['chrome_path'])
            choptions1.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=choptions1, executable_path=CHROME_DRIVER_PATH)
            # Check for the chrome 75 version.
            # As the key value of 'version' is changed from 'version' to 'browserVersion'
            browser_ver=''
            if 'version' in  driver.capabilities.keys():
                browser_ver = driver.capabilities['version']
            elif 'browserVersion' in  driver.capabilities.keys():
                browser_ver = driver.capabilities['browserVersion']
            browser_ver = int(browser_ver.encode('utf-8')[:2])
            try:
                driver.close()
                driver.quit()
            except:
                pass
            driver=None
            for k,v in list(CHROME_DRIVER_VERSION.items()):
                if a == k:
                    if browser_ver >= v[0] and browser_ver <= v[1]:
                        chromeFlag=True
            if chromeFlag == False :
                logger.print_on_console('WARNING!! : Chrome version ',str(browser_ver),' is not supported.')
        except Exception as e:
            logger.print_on_console("Error in checking chrome version")
            log.error("Error in checking chrome version")
            log.error(e,exc_info=True)
        try:
            p = subprocess.Popen(GECKODRIVER_PATH + ' --version', stdout=subprocess.PIPE, bufsize=1, shell=True)
            a = p.stdout.readline()
            a = a.decode('utf-8')[12:16]
            caps=webdriver.DesiredCapabilities.FIREFOX
            caps['marionette'] = True
            from selenium.webdriver.firefox.options import Options
            options = Options()
            options.add_argument('--headless')
            if str(configvalues['firefox_path']).lower()!="default":
                from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
                binary = FirefoxBinary(str(configvalues['firefox_path']))
                driver = webdriver.Firefox(capabilities=caps,firefox_options=options,firefox_binary=binary, executable_path=GECKODRIVER_PATH)
            else:
                driver = webdriver.Firefox(capabilities=caps,firefox_options=options, executable_path=GECKODRIVER_PATH)
            browser_ver = float(driver.capabilities['browserVersion'].encode('utf-8')[:4])
            try:
                driver.close()
                driver.quit()
            except:
                pass
            driver=None
            for k,v in list(FIREFOX_BROWSER_VERSION.items()):
                if a == k:
                    if browser_ver >= v[0] or browser_ver <= v[1]:
                        firefoxFlag=True
            if firefoxFlag == False:
                logger.print_on_console('WARNING!! : Firefox version ',str(browser_ver),' is not supported.')
        except Exception as e:
            logger.print_on_console("Error in checking Firefox version")
            log.error("Error in checking Firefox version")
            log.error(e,exc_info=True)
        if chromeFlag == True and firefoxFlag == True:
            logger.print_on_console('Current version of browsers are supported')
        return True
    except Exception as e:
        logger.print_on_console("Error while checking browser compatibility")
        log.debug("Error while checking browser compatibility")
        log.debug(e)
    return False

def check_execution_lic(event):
    if executionOnly:
        msg='Execution only allowed'
        log.info(msg)
        logger.print_on_console(msg)
        socketIO.emit(event,'ExecutionOnlyAllowed')
    return executionOnly

def check_update(flag):
    global update_obj
    SERVER_LOC = "https://" + str(configvalues['server_ip']) + ':' + str(configvalues['server_port']) + '/fileserver/'
    #------------------------------------------------------------getting server manifest
    def get_server_manifest_data():
        data = None
        request = None
        emsg = "Error in fetching update manifest from server"
        try:
            request = requests.get(SERVER_LOC + "/manifest.json", verify=False)
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
        update_obj.update(data, MANIFEST_LOC, SERVER_LOC, NINETEEN68_HOME, LOC_7Z, UPDATER_LOC, 'UPDATE')
    #---------------------------------------updater
    data = get_server_manifest_data()
    update_updater_module(data)
    UPDATE_MSG=update_obj.send_update_message()
    l_ver = update_obj.fetch_current_value()
    #check if update avaliable
    if ( UPDATE_MSG == 'Update Available!!! Click on update' and flag == True ):
        logger.print_on_console("An update is available. Click on 'Help' menu option -> 'Check for Updates' sub-menu option -> 'Update' button")
        logger.print_on_console('The latest ICE version : ',l_ver)
        log.info(UPDATE_MSG)
    elif ( UPDATE_MSG == 'You are running the latest version of Nineteen68' and flag == True ):
        logger.print_on_console( "No updates available" )
        log.info( "No updates available" )
    elif ( UPDATE_MSG == 'An Error has occoured while checking for new versions of Nineteen68, kindly contact Support Team'):
        if not (os.path.exists(MANIFEST_LOC)):
            logger.print_on_console( "Client manifest unavaliable." )
            log.info( "Client manifest unavaliable." )
        else:
            logger.print_on_console( UPDATE_MSG )
            log.info( UPDATE_MSG )
    return False,l_ver

