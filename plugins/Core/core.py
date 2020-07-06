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
import signal
from datetime import datetime
from random import random
import core_utils
import logger
import threading
from constants import *
import controller
import readconfig
import clientwindow
import json
import socket
import requests
import io
import handler
import update_module
from icetoken import ICEToken
try:
    from socketlib_override import SocketIO,BaseNamespace
except ImportError:
    from socketIO_client import SocketIO,BaseNamespace
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
log = logging.getLogger('core.py')
root = None
cw = None
browsername = None
qcdata = None
qcObject = None
soc=None
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
irisFlag = True
executionOnly=False
socketIO = None
allow_connect = False
plugins_list = []
configvalues = {}
execution_flag = False
closeActiveConnection = False
connection_Timer = None
core_utils_obj = core_utils.CoreUtils()
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


class MainNamespace(BaseNamespace):
    def on_message(self, *args):
        global action,cw,browsername,desktopScrapeFlag,allow_connect,connection_Timer,updatecheckFlag,executionOnly
        kill_conn = False
        try:
            if(str(args[0]) == 'connected'):
                if allow_connect:
                    sch_mode = cw.schedule.GetValue() if root.gui else False
                    if sch_mode: socketIO.emit('toggle_schedule',sch_mode)
                    msg = ("Schedule" if sch_mode else "Normal") + " Mode: Connection to the Nineteen68 Server established"
                    logger.print_on_console(msg)
                    log.info(msg)
                    msg = "ICE Name: " + root.ice_token["icename"]
                    logger.print_on_console(msg)
                    log.info(msg)
                    if root.gui:
                        cw.schedule.Enable()
                        cw.cancelbutton.Enable()
                        cw.terminatebutton.Enable()
                        cw.clearbutton.Enable()
                        cw.rollbackItem.Enable(True)
                        cw.updateItem.Enable(True)
                        cw.rbox.Enable()
                    if browsercheckFlag == False:
                        check_browser()
                    if updatecheckFlag == False and root.gui:
                        msg='Checking for client package updates'
                        logger.print_on_console(msg)
                        log.info(msg)
                        updatecheckFlag = clientwindow.check_update(True)
                    if executionOnly:
                        msg='Execution only Mode enabled'
                        logger.print_on_console(msg)
                        log.info(msg)
                    conn_time = float(configvalues['connection_timeout'])
                    if (not (connection_Timer != None and connection_Timer.isAlive())
                     and (conn_time >= 8)):
                        log.info("Connection Timeout timer Started")
                        connection_Timer = threading.Timer(conn_time*60*60, root.closeConnection)
                        connection_Timer.start()
                else: kill_conn = True

            elif(str(args[0]) == 'schedulingEnabled'):
                logger.print_on_console('Schedule Mode Enabled')
                log.info('Schedule Mode Enabled')
                
            elif(str(args[0]) == 'schedulingDisabled'):
                logger.print_on_console('Schedule Mode Disabled')
                log.info('Schedule Mode Disabled')

            elif(str(args[0]) == 'checkConnection'):
                err_res = None
                enable_reregister = False
                try:
                    global plugins_list
                    ice_ndac_key = "".join(['a','j','k','d','f','i','H','F','E','o','w','#','D','j',
                        'g','L','I','q','o','c','n','^','8','s','j','p','2','h','f','Y','&','d'])
                    response = json.loads(core_utils_obj.unwrap(str(args[1]), ice_ndac_key))
                    if(response['id'] != root.icesession['ice_id'] or response['connect_time'] != root.icesession['connect_time']):
                        err_res="Invalid response received"
                        logger.print_on_console(err_res)
                        log.info(err_res)
                        kill_conn = True
                    else:
                        if response['status'] != "allow": enable_reregister = True
                        if response['res'] == 'success':
                            executionOnly = root.ice_token["icetype"] != "normal"
                            allow_connect = True
                            plugins_list = response['plugins']
                            if root.gui:
                                cw.connectbutton.SetBitmapLabel(cw.disconnect_img)
                                cw.connectbutton.SetName("disconnect")
                                cw.connectbutton.SetToolTip(wx.ToolTip("Disconnect from Nineteen68 Server"))
                            controller.disconnect_flag=False
                        else:
                            if 'err_msg' in response: err_res = response['err_msg']
                            else: err_res = "Unable to Connect to Server"
                            logger.print_on_console(err_res)
                            log.info(err_res)
                            kill_conn = True
                except Exception as e:
                    err_res = 'Error while checking connection request'
                    logger.print_on_console(err_res)
                    log.info(err_res)
                    log.error(e)
                    kill_conn = True

                if enable_reregister:
                    root.ice_action = "register"
                    root.ice_token = None
                    root.token_obj.delete_token()
                    if root.gui:
                        logger.print_on_console("ICE is not registered with Nineteen68. Click to Register")
                        cw.enable_register()
                    else:
                        logger.print_on_console("ICE is not registered with Nineteen68. Try Again")
                if root.gui: cw.connectbutton.Enable()

            elif(str(args[0]) == 'fail'):
                fail_msg = "Fail"
                if len(args) > 1 and args[1]=="conn":
                    fail_msg+="ed to connect to Nineteen68 Server"
                if len(args) > 1 and args[1]=="disconn":
                    fail_msg+="ed to disconnect from Nineteen68 Server"
                logger.print_on_console(fail_msg)
                log.info(fail_msg)
                kill_conn = True

        except Exception as e:
            err_msg='Error while Connecting to Server'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)
            kill_conn = True

        if kill_conn:
            if root.gui: threading.Timer(0.5,root.killSocket).start()
            else: root._wants_to_close = True

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
        global cw, execution_flag
        try:
            exec_data = args[0]
            batch_id = exec_data["batchId"]
            aws_mode=False
            if len(args)>0 and args[0]['apptype']=='MobileApp':
                if args[0]['suitedetails'][0]['browserType'][0]=='2':
                    aws_mode = True
            if(not execution_flag):
                socketIO.emit('return_status_executeTestSuite', {'status': 'success', 'batchId': batch_id})
                root.testthread = TestThread(root, EXECUTE, exec_data, aws_mode)
            else:
                socketIO.emit('return_status_executeTestSuite', {'status': 'skipped', 'batchId': batch_id})
                emsg = 'Execution already in progress. Skipping current request.'
                log.warn(emsg)
                logger.print_on_console(emsg)
        except Exception as e:
            err_msg='Error while Executing'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_debugTestCase(self, *args):
        global cw
        try:
            if check_execution_lic("result_debugTestCase"): return None
            exec_data = args[0]
            root.testthread = TestThread(root, DEBUG, exec_data, False)
            cw.choice=cw.rbox.GetStringSelection()
            logger.print_on_console(str(cw.choice)+' is Selected')
            if cw.choice == 'Normal':
                cw.killChildWindow(debug=True)
            cw.debug_mode=False
            cw.breakpoint.Disable()
            if cw.choice in ['Stepwise','RunfromStep']:
                global debugFlag
                debugFlag = True
                wx.PostEvent(cw.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, cw.GetId()))
        except Exception as e:
            err_msg='Error while Debugging'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_webscrape(self,*args):
        try:
            global action,cw,browsername,desktopScrapeFlag,data,socketIO
            if check_execution_lic("scrape"): return None
            elif bool(cw.scrapewindow): return None
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
                wx.PostEvent(cw.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, cw.GetId()))
        except Exception as e:
            err_msg='Error while Scraping Web application'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_LAUNCH_DESKTOP(self, *args):
        try:
            if check_execution_lic("scrape"): return None
            elif bool(cw.scrapewindow): return None
            #con = controller.Controller()
            global browsername
            browsername = args
            core_utils.get_all_the_imports('Desktop')
            import desktop_scrape
            global desktopScrapeObj
            desktopScrapeObj=desktop_scrape
            global desktopScrapeFlag
            desktopScrapeFlag=True
            wx.PostEvent(cw.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, cw.GetId()))
        except Exception as e:
            err_msg='Error while Scraping Desktop application'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_LAUNCH_SAP(self, *args):
        try:
            if check_execution_lic("scrape"): return None
            elif bool(cw.scrapewindow): return None

            #con = controller.Controller()
            global browsername
            browsername = args[0]
            core_utils.get_all_the_imports('SAP')
            import sap_scrape
            global sapScrapeObj
            sapScrapeObj=sap_scrape
            global sapScrapeFlag
            sapScrapeFlag=True
            wx.PostEvent(cw.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, cw.GetId()))
        except Exception as e:
            err_msg='Error while Scraping SAP application'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_LAUNCH_MOBILE(self, *args):
        try:
            if check_execution_lic("scrape"): return None
            elif bool(cw.scrapewindow): return None
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
            wx.PostEvent(cw.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, cw.GetId()))
        except Exception as e:
            err_msg='Error while Scraping Mobile application'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_LAUNCH_MOBILE_WEB(self, *args):
        try:
            if check_execution_lic("scrape"): return None
            elif bool(cw.scrapewindow): return None
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
            wx.PostEvent(cw.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, cw.GetId()))
        except Exception as e:
            err_msg='Error while Scraping Mobile application'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_PDF_SCRAPE(self, *args):
        try:
            if check_execution_lic("scrape"): return None
            elif bool(cw.scrapewindow): return None
            logger.print_on_console(" Entering inside PDF scrape")
            global pdfScrapeObj,pdfScrapeFlag
            global browsername
            browsername = args[0]
            #con =controller.Controller()
            core_utils.get_all_the_imports('PDF')
            import pdf_scrape_dispatcher
            pdfScrapeObj=pdf_scrape_dispatcher
            pdfScrapeFlag=True
            wx.PostEvent(cw.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, cw.GetId()))
        except Exception as e:
            err_msg='Error while Scraping in PDF Window'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_LAUNCH_OEBS(self, *args):
        try:
            if check_execution_lic("scrape"): return None
            elif bool(cw.scrapewindow): return None
            global oebsScrapeObj,oebsScrapeFlag
            #con = controller.Controller()
            global browsername
            browsername = args[0]
            core_utils.get_all_the_imports('Oebs')
            import scrape_dispatcher
            oebsScrapeObj=scrape_dispatcher
            oebsScrapeFlag=True
            wx.PostEvent(cw.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, cw.GetId()))
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
            log.info('responseHeader after:::' + str(responseHeader))
            log.info('responseBody:::::' + str(responseBody))
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
            # wobj.runCrawler(args[0],args[1],args[2],args[3],socketIO,root)
            wobj.runCrawler(socketIO,root,*args)

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
        try:
            msg = 'Connection termination request triggered remotely by ' + args[0]
            logger.print_on_console(msg)
            log.info(msg)
            if (len(args) > 1 and args[1 == "dereg"]):
                msg = 'ICE "'+root.ice_token["icename"]+'" is Deregistered.'
                logger.print_on_console(msg)
                log.info(msg)
                root.token_obj.delete_token()
            if root.gui: threading.Timer(1,cw.OnNodeConnect,[wx.EVT_BUTTON]).start()
            else: threading.Timer(1,root.connection,["disconnect"]).start()
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
            root.icesession['connect_time'] = str(datetime.now())
            socketIO._http_session.params['icesession'] = core_utils_obj.wrap(json.dumps(root.icesession), ice_ndac_key)
            if root.gui:
                if not bool(cw): return
                cw.schedule.Disable()
                cw.connectbutton.Disable()
            """Enables the Register button , if disconnection happened due to Invalid Token"""
            if root.ice_token is None:
                if root.gui: cw.enable_register()
                return
            else:
                msg = 'Connectivity issue with Nineteen68 Server. Attempting to restore connectivity...'
                logger.print_on_console(msg)
                log.error(msg)
        if not bool(cw): return
        if root.ice_token:
            cw.connectbutton.SetBitmapLabel(cw.connect_img)
            cw.connectbutton.SetName('connect')

    def on_irisOperations(self, *args):
        try:
            global socketIO
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


class ConnectionThread(threading.Thread):
    """Test Worker Thread Class."""
    daemon = True

    def __init__(self, ice_action):
        """Init Worker Thread Class."""
        super(ConnectionThread, self).__init__()
        self.ice_action = ice_action

    def get_ice_session(self):
        server_cert = configvalues['server_cert']
        if configvalues["disable_server_cert"] == "Yes":
            server_cert = False
        elif server_cert != "default":
            if os.path.exists(server_cert) == False:
                server_cert = CERTIFICATE_PATH +'/server.crt'
        client_cert = (CERTIFICATE_PATH + '/client.crt', CERTIFICATE_PATH + '/client.key')
        key='USERNAME'
        if key not in os.environ:
            key='USER'
        username = str(os.environ[key]).lower()
        root.ice_token["hostname"] = socket.gethostname()
        root.icesession = {
            'ice_id': str(uuid.uuid4()),
            'connect_time': str(datetime.now()),
            'username': username,
            'iceaction': self.ice_action,
            'icetoken': root.ice_token,
            'data': random()*100000000000000
        }
        ice_ndac_key = "".join(['a','j','k','d','f','i','H','F','E','o','w','#','D','j',
            'g','L','I','q','o','c','n','^','8','s','j','p','2','h','f','Y','&','d'])
        icesession_enc = core_utils_obj.wrap(json.dumps(root.icesession), ice_ndac_key)
        params={'username': username, 'icename': root.ice_token["icename"],
            'ice_action': self.ice_action, 'icesession': icesession_enc}
        args = {"cert": client_cert, "params": params}
        if server_cert != "default": args["verify"] = server_cert
        return args

    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        reg_hostname = hostname = socket.gethostname()
        if "hostname" in root.ice_token: reg_hostname=root.ice_token["hostname"]
        """Check if registered hostname in the Token matches with the current hostname"""
        if reg_hostname != hostname:
            msg="Access denied: Hostname doesn't match. ICE is registered with a  different hostname "+reg_hostname
            logger.print_on_console(msg)
            log.error(msg)
            root.ice_token = None
            if root.gui: cw.enable_register()
            return False
        global socketIO, allow_connect
        allow_connect = False
        err_msg=None
        server_port = int(configvalues['server_port'])
        server_IP = 'https://' + configvalues['server_ip']
        try:
            kw_args = self.get_ice_session()
            socketIO = SocketIO(server_IP, server_port, MainNamespace, **kw_args)
            root.socketIO = socketIO
            socketIO.wait()
        except ValueError as e:
            err_msg = str(e).replace("[engine.io waiting for connection] ",'').replace("[SSL: CERTIFICATE_VERIFY_FAILED] ",'')
            if "_ssl.c" in err_msg:
                err_msg = err_msg[:err_msg.index("(_ssl")]
        except Exception as e:
            err_msg = "Error in server connection"
            log.error(e,exc_info=True)
        if (err_msg):
            logger.print_on_console(err_msg)
            log.error(err_msg)
            if root.gui: cw.connectbutton.Enable()


class TestThread(threading.Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self, main, action, json_data, aws_mode):
        """Init Worker Thread Class."""
        super(TestThread, self).__init__()
        self.main = main
        self.cw = main.cw
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
        self.debug_mode = False if not(self.cw) else self.cw.debug_mode
        self.aws_mode = aws_mode
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
        global execution_flag, closeActiveConnection, connection_Timer
        batch_id = None
        try:
            runfrom_step=1
            if self.action==EXECUTE: batch_id = self.json_data["batchId"]
            elif self.action==DEBUG:
                self.debug_mode=False
                self.cw.breakpoint.Disable()
                if self.cw.choice in ['Stepwise','RunfromStep']:
                    self.debug_mode=True
                    if self.cw.choice=='RunfromStep':
                        self.cw.breakpoint.Enable()
                        try:
                            runfrom_step=self.cw.breakpoint.GetValue()
                            runfrom_step=int(runfrom_step)
                        except Exception as e:
                            runfrom_step=0
            if self.main.gui:
                self.cw.schedule.Disable()
                self.cw.rbox.Disable()
                self.cw.breakpoint.Disable()
                self.cw.terminatebutton.Enable()
            self.con = controller.Controller()
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
                status = self.con.invoke_controller(self.action,self,self.debug_mode,runfrom_step,self.json_data,self.main,socketIO,qcObject,self.aws_mode)

            logger.print_on_console('Execution status '+status)

            if status==TERMINATE:
                logger.print_on_console('---------Termination Completed-------')
            if self.main.gui:
                if self.cw.choice=='RunfromStep':
                    self.cw.breakpoint.Enable()
                else:
                    self.cw.breakpoint.Disable()
                #Removed execute,debug button
                self.cw.breakpoint.Clear()
                self.cw.rbox.Enable()
                # self.cw.breakpoint.Disable()
                self.cw.cancelbutton.Enable()
            if self.action==DEBUG:
                testcasename = handler.local_handler.testcasename
                self.cw.killChildWindow(debug=True)
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
                    self.cw.killChildWindow(debug=True)
                    socketIO.emit('result_debugTestCase',status)
                elif self.action==EXECUTE:
                    socketIO.emit('result_executeTestSuite', {"status":status, "batchId": batch_id})
        if closeActiveConnection:
            closeActiveConnection = False
            connection_Timer = threading.Timer(300, root.closeConnection)
            connection_Timer.start()

        self.main.testthread = None
        execution_flag = False
        if self.main.gui: self.cw.schedule.Enable()


class Main():
    def __init__(self, appName, args):
        self.name = appName
        self.gui = not (args.register or args.connect)
        self.cw = None
        self.testthread = None
        self.socketthread = None
        self.ice_token = None
        self.icesession = None
        self.server_url = None
        self._wants_to_close = False
        self.opts = args
        global root, cw, browsercheckFlag, updatecheckFlag
        os.environ["ice_mode"] = "gui" if self.gui else "cli"
        root = self
        updatecheckFlag = configvalues['update_check'].lower() == 'no'
        browsercheckFlag = configvalues['browser_check'].lower() == 'no'
        is_config_missing = 'configmissing' in configvalues
        is_config_invalid = 'errorflag' in configvalues
        logfilename_error_flag = False
        wx_app = None

        if self.gui:
            wx_app = wx.App()
            clientwindow.configvalues = configvalues
            clientwindow.root = root
            cw = clientwindow.ClientWindow()
            self.cw = cw

        """ Creating Root Logger using logger file config and setting logfile path, which is in config.json """
        try:
            logfilename = os.path.normpath(configvalues["logFile_Path"]).replace("\\","\\\\")
            logging.config.fileConfig(LOGCONFIG_PATH,defaults={'logfilename': logfilename},disable_existing_loggers=False)
        except Exception as e:
            logfilename_error_flag = True
            log.error(e)

        log.info('Started')
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.CRITICAL)

        '''Following two lines set 'CRITICAL' log level for selenium, uncomment these to not log entries from selenium if current log level is < CRITICAL'''
        # selenium_log = logging.getLogger("selenium")
        # selenium_log.setLevel(logging.CRITICAL)

        print('********************************************************************************************************')
        print('============================================ '+appName+' ============================================')
        print('********************************************************************************************************')

        if self.gui:
            if logfilename_error_flag or is_config_invalid or is_config_missing:
                cw.cancelbutton.Disable()
                cw.terminatebutton.Disable()
                cw.clearbutton.Disable()
                cw.connectbutton.Disable()
                cw.rbox.Disable()
            cw.DisableAll()
        self.verifyRegistration()
        if is_config_missing:
            err = "Configure "+appName+" by navigating to Edit -> Configuration"
            logger.print_on_console(err)
            log.info(err)
        elif is_config_invalid:
            err = "[Error]: Syntax error in config file.\n"+str(configvalues['errorflag'])+ " config field is missing. Please check and restart "+appName+"."
            logger.print_on_console(err)
            log.info(err)
            log.error(configvalues['errorflag'])
        elif logfilename_error_flag:
            err = "[Error]: Please provide a valid logfile path in config file and restart "+appName+"."
            logger.print_on_console(err)
            log.info(err)
            logfilename_error_flag = False
        if self.gui:
            cw.connectbutton.SetFocus()
            wx_app.MainLoop()
        else:
            if self.opts.connect:
                connectmode = "connect"
                if self.opts.token:
                    msg = "Connecting ICE in guest mode"
                    logger.print_on_console(msg)
                    log.info(msg)
                    connectmode = "guestconnect"
                self.connection(connectmode)
            try:
                signal.signal(signal.SIGINT, self.close)
                while True:
                    time.sleep(3)
                    if self._wants_to_close: break
            except KeyboardInterrupt: pass
            finally: self.close()

    def close(self, *args):
        global connection_Timer
        controller.terminate_flag = True
        controller.disconnect_flag = True
        if self.socketthread: logger.print_on_console('Disconnected from Nineteen68 server')
        if (connection_Timer != None and connection_Timer.isAlive()):
            log.info("Connection Timeout timer Stopped")
            connection_Timer.cancel()
            connection_Timer = None
        if self.gui:
            stat = cw.killChildWindow(True,True,True,True,True)
            if stat[1]: socketIO.emit('scrape','Terminate')
            cw.Destroy()
        self.killSocket(True)
        controller.kill_process()
        if SYSTEM_OS == "Windows":
            os.system("TASKKILL /F /IM nineteen68MFapi.exe")
        sys.exit(0)

    def register(self, token, hold = False):
        ice_ndac_key = "".join(['a','j','k','d','f','i','H','F','E','o','w','#','D','j',
            'g','L','I','q','o','c','n','^','8','s','j','p','2','h','f','Y','&','d'])
        emsg = "Error: Invalid Server address or Token . Please try again"
        try:
            token_dec = core_utils_obj.unwrap(token,ice_ndac_key).split("@")
            token_info = {'token':token_dec[0],'icetype':token_dec[1] ,'icename':token_dec[2]}
            if self.gui and token_info["icetype"] != "normal":
                emsg = "Token is provisioned for CI-CD ICE. Either use a token provisioned for Normal mode or register ICE in command line mode."
                raise ValueError("Invalid Token/ICE mode")
            if not self.gui and token_info["icetype"] == "normal":
                emsg = "Token is provisioned for Normal ICE. Either use a token provisioned for CI-CD mode or register ICE in GUI mode."
                raise ValueError("Invalid Token/ICE mode")
            self.ice_token = token_info
            url = self.server_url.split(":")
            configvalues['server_ip']=url[0]
            if len(url) == 1: url.append("443")
            configvalues['server_port']=url[1]
            if not hold: self.connection("register")
        except Exception as e:
            logger.print_on_console(emsg)
            log.error(emsg)
            log.error(e)
            if self.gui: self.cw.enable_register()
            else: self._wants_to_close = True

    def connection(self, mode):
        try:
            if mode == 'register':
                if self.ice_token is None:
                    self.verifyRegistration()
                    return None
                kw_args = ConnectionThread(mode).get_ice_session()
                data = kw_args.pop('params')
                del data['username']
                del data['ice_action']
                server_url = "https://"+self.server_url+"/ICE_provisioning_register"
                res = requests.post(server_url, data=data, **kw_args)
                response = res.content
                try:
                    err_res = None
                    enable_reregister = False
                    if response == "fail":
                        err_res = "ICE registration failed."
                    else:
                        ice_ndac_key = "".join(['a','j','k','d','f','i','H','F','E','o','w','#','D','j',
                            'g','L','I','q','o','c','n','^','8','s','j','p','2','h','f','Y','&','d'])
                        response = json.loads(core_utils_obj.unwrap(response, ice_ndac_key))
                    if err_res or response['id'] != self.icesession['ice_id'] or response['connect_time'] != self.icesession['connect_time']:
                        if not err_res: err_res = "Invalid response received"
                        logger.print_on_console(err_res)
                        log.info(err_res)
                        enable_reregister = True
                    else:
                        if response['res'] != 'success' and 'err_msg' in response: err_res = response['err_msg']
                        if response['status'] != "validICE":
                            enable_reregister = True
                        if err_res is not None:
                            logger.print_on_console(err_res)
                            log.info(err_res)
                        else:
                            self.ice_action="connect"
                            """To save the token after successful registration"""
                            self.token_obj.save_token(self.ice_token)
                            with io.open(clientwindow.CONFIG_PATH, 'w', encoding='utf8') as outfile:
                                str_ = json.dumps(configvalues,indent=4, sort_keys=True,separators=(',', ': '), ensure_ascii=False)
                                outfile.write(str(str_))
                            clientwindow.configvalues = configvalues
                            if self.gui:
                                cw.EnableAll()
                                cw.connectbutton.SetBitmapLabel(cw.connect_img)
                                cw.connectbutton.SetName('connect')
                                cw.connectbutton.SetToolTip(wx.ToolTip("Connect to Nineteen68 Server"))
                            msg='ICE "'+data["icename"]+'" registered successfully with Nineteen68'
                            logger.print_on_console(msg)
                            log.info(msg)
                except Exception as e:
                    err_res = 'Error in ICE Registration'
                    logger.print_on_console(err_res)
                    log.info(err_res)
                    log.error(e, exc_info=True)
                    enable_reregister = True
                if enable_reregister:
                    self.ice_action = "register"
                    self.ice_token = None
                    self.token_obj.delete_token()
                    if self.gui:
                        logger.print_on_console("ICE is not registered with Nineteen68. Click to Register")
                        cw.enable_register()
                    else:
                        logger.print_on_console("ICE is not registered with Nineteen68. Try Again")
                if self.gui: cw.connectbutton.Enable()
                else: self._wants_to_close = True
            elif mode == 'connect' or mode == "guestconnect":
                # Re-Check token file on connection
                status = self.verifyRegistration(verifyonly = True)
                if status == False:
                    self.ice_action = "register"
                    self.ice_token = None
                    msg = "ICE is not registered with Nineteen68."
                    if self.gui:
                        msg += " Click to Register"
                        logger.print_on_console(msg)
                        log.error(msg)
                        cw.enable_register()
                    else:
                        logger.print_on_console(msg)
                        log.error(msg)
                        self._wants_to_close = True
                    return None
                # ICE is registered
                ip = configvalues['server_ip']
                port = int(configvalues['server_port'])
                conn = http.client.HTTPConnection(ip,port)
                conn.connect()
                conn.close()
                self.socketthread = ConnectionThread(mode)
                self.socketthread.start()
            else:
                self.killSocket(True)
                log.info('Disconnected from Nineteen68 server')
                logger.print_on_console('Disconnected from Nineteen68 server')
                global connection_Timer
                if (connection_Timer != None and connection_Timer.isAlive()):
                    log.info("Connection Timeout Timer Stopped")
                    connection_Timer.cancel()
                    connection_Timer = None
                if not self.gui: self._wants_to_close = True
                else:
                    if not self.token_obj.token: cw.enable_register()
        except Exception as e:
            emsg="Forbidden request, Connection refused, please configure server ip and server port in "
            if self.gui: emsg += "Edit -> Configuration"
            else: emsg += "configuration file located at NINETEEN68_HOME/assets/config.json"
            emsg += ", and retry."
            if mode == "register":
                self.ice_token=None
                emsg = "Connection refused: Invalid Server URL."
                if self.gui:
                    emsg += " Click on Connect to retry Registration" 
                    cw.enable_register()
            logger.print_on_console(emsg)
            log.error(emsg)
            log.error(e,exc_info=True)
            raise

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
                self.socketthread.join()
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

    def verifyRegistration(self, verifyonly = False):
        global executionOnly
        emsg = "Nineteen68 ICE is not registered."
        executionOnly = True
        try:
            self.token_obj = ICEToken()
            self.server_url = configvalues['server_ip']+':'+configvalues['server_port']
            if self.token_obj.token:
                self.ice_token = self.token_obj.token
                emsg = None
                icetype = self.ice_token["icetype"]
                name = self.ice_token["icename"]
                if self.gui:
                    if icetype != "normal":
                        emsg = "Access denied: "+name+" is registered for CI-CD mode. ICE has to run in command line mode"
                    else:
                        executionOnly = False
                        cw.EnableAll()
                        if verifyonly: cw.connectbutton.Disable()
                else:
                    if icetype != "ci-cd":
                        emsg = "Access denied: "+name+" is registered for Normal mode. ICE has to run in GUI mode"
                    elif self.opts.register:
                        emsg = "Registration denied: ICE already Registered."
                if emsg:
                    log.error(emsg)
                    logger.print_on_console(emsg)
                    if not self.gui: self._wants_to_close=True
                    return False
                return True
            else:
                if self.gui:
                    if not verifyonly: self.token_obj.token_window(self, IMAGES_PATH)
                else:
                    if self.opts.host is not None: self.server_url = self.opts.host
                    if self.opts.register:
                        self.register(self.opts.token)
                    elif self.opts.connect and self.opts.token:
                        self.register(self.opts.token, hold=True)
                    else:
                        logger.print_on_console(emsg)
                        log.error(emsg)
                        self.close()
                return False
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console(emsg)
            log.error(emsg)

    def debug_scrape(self):
        try:
            global mobileScrapeFlag,mobileWebScrapeFlag,desktopScrapeFlag, pdfScrapeFlag
            global sapScrapeFlag,debugFlag,browsername,action,oebsScrapeFlag
            global socketIO,data
            cw.schedule.Disable()
            if(irisFlag == True):
                core_utils.get_all_the_imports('IRIS')
            if mobileScrapeFlag==True:
                cw.scrapewindow = mobileScrapeObj.ScrapeWindow(parent = cw,id = -1, title="SLK Nineteen68 - Mobile Scrapper",filePath = browsername,socketIO = socketIO)
                mobileScrapeFlag=False
            elif mobileWebScrapeFlag==True:
                cw.scrapewindow = mobileWebScrapeObj.ScrapeWindow(parent = cw,id = -1, title="SLK Nineteen68 - Mobile Scrapper",browser = browsername,socketIO = socketIO)
                mobileWebScrapeFlag=False
            elif desktopScrapeFlag==True:
                cw.scrapewindow = desktopScrapeObj.ScrapeWindow(parent = cw,id = -1, title="SLK Nineteen68 - Desktop Scrapper",filePath = browsername,socketIO = socketIO,irisFlag = irisFlag)
                desktopScrapeFlag=False
                browsername = ''
            elif sapScrapeFlag==True:
                cw.scrapewindow = sapScrapeObj.ScrapeWindow(parent = cw,id = -1, title="SLK Nineteen68 - SAP Scrapper",filePath = browsername,socketIO = socketIO,irisFlag = irisFlag)
                sapScrapeFlag=False
            elif oebsScrapeFlag==True:
                cw.scrapewindow = oebsScrapeObj.ScrapeDispatcher(parent = cw,id = -1, title="SLK Nineteen68 - Oebs Scrapper",filePath = browsername,socketIO = socketIO,irisFlag = irisFlag)
                oebsScrapeFlag=False
            elif pdfScrapeFlag==True:
                cw.scrapewindow = pdfScrapeObj.ScrapeDispatcher(parent = cw,id = -1, title="SLK Nineteen68 - PDF Scrapper",filePath = browsername,socketIO = socketIO,irisFlag = irisFlag)
                pdfScrapeFlag=False
            elif debugFlag == True:
                cw.debugwindow = clientwindow.DebugWindow(parent = cw,id = -1, title="Debugger")
                debugFlag = False
            else:
                browsernumbers = ['1','2','3','6']
                if browsername in browsernumbers:
                    logger.print_on_console('Browser name : '+str(browsername))
                    #con = controller.Controller()
                    core_utils.get_all_the_imports('Web')
                    core_utils.get_all_the_imports('WebScrape')
                    import Nineteen68_WebScrape
                    cw.scrapewindow = Nineteen68_WebScrape.ScrapeWindow(parent = cw,id = -1, title="SLK Nineteen68 - Web Scrapper",browser = browsername,socketIO = socketIO,action=action,data=data,irisFlag = irisFlag)
                    browsername = ''
                else:
                    import pause_display_operation
                    o = pause_display_operation.PauseAndDisplay()
                    flag,inputvalue = o.getflagandinput()
                    if flag == 'pause':
                        #call pause logic
                        cw.pausewindow = pause_display_operation.Pause(parent = None,id = -1, title="SLK Nineteen68 - Pause")
                    elif flag == 'display':
                        #call display logic
                        cw.pausewindow = pause_display_operation.Display(parent = cw,id = -1, title="SLK Nineteen68 - Display Variable",input = inputvalue)
                    elif flag == 'debug':
                        #call debug logic
                        cw.pausewindow = pause_display_operation.Debug(parent = cw,id = -1, title="SLK Nineteen68 - Debug Mode",input = inputvalue)
                    elif flag == 'error':
                        #call debug error logic
                        cw.pausewindow = pause_display_operation.Error(parent = cw,id = -1, title="SLK Nineteen68 - Debug Mode",input = inputvalue)
        except Exception as e:
            log.error(e,exc_info=True)


def check_browser():
    global browsercheckFlag
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
            logger.print_on_console('Browser compatibility check started')
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
                    if browser_ver >= v[0] and browser_ver <= v[1]:
                        firefoxFlag=True
            if firefoxFlag == False:
                logger.print_on_console('WARNING!! : Firefox version ',str(browser_ver),' is not supported.')
        except Exception as e:
            logger.print_on_console("Error in checking Firefox version")
            log.error("Error in checking Firefox version")
            log.error(e,exc_info=True)
        if chromeFlag == True and firefoxFlag == True:
            logger.print_on_console('Current version of browsers are supported')
        browsercheckFlag = True
    except Exception as e:
        err = "Error while checking for browser compatibility"
        logger.print_on_console(err)
        log.debug(err)
        log.debug(e)
        browsercheckFlag = False
    finally:
        logger.print_on_console('Browser compatibility check completed')
    return browsercheckFlag


def check_execution_lic(event):
    if executionOnly:
        msg='Execution only allowed'
        log.info(msg)
        logger.print_on_console(msg)
        socketIO.emit(event,'ExecutionOnlyAllowed')
    return executionOnly
