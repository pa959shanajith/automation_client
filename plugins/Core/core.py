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
import subprocess
from datetime import datetime
from selenium import webdriver, common
from random import random
import core_utils
import logger
import threading
from os.path import normpath
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
import shutil
from icetoken import ICEToken
import benchmark
import stat
if SYSTEM_OS=='Windows':
    from win32com.client import Dispatch
from urllib import request
from bs4 import BeautifulSoup                                                               
from socketiolib import SocketIO, BaseNamespace, prepare_http_session
import ssl
from urllib import request


try:
   _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

log = logging.getLogger('core.py')
root = None
cw = None
browsername = None
qcdata = None
zephyrdata = None
qcObject = None
qtestObject = None
zephyrObject = None
testrailObject = None
azureObject = None
soc=None
browsercheckFlag=False
updatecheckFlag=False
chromeFlag=False
edgeFlag=False
edgeFlagComp=False
chromiumFlag=False
firefoxFlag=False
edgeFlag=False
chromiumFlag=False
desktopScrapeFlag=False
sapScrapeFlag=False
mobileScrapeFlag=False
mobileWebScrapeFlag=False
pdfScrapeFlag = False
debugFlag = False
oebsScrapeFlag = False
executionOnly=False
socketIO = None
allow_connect = False
plugins_list = []
configvalues = {}
proxies = None
execution_flag = False
closeActiveConnection = False
connection_Timer = None
status_ping_thread = None
update_obj = None
termination_inprogress = False
browsercheck_inprogress = False
application_path = None
execReq = None
core_utils_obj = core_utils.CoreUtils() 


def _process_ssl_errors(e):
    err = "[TLS Certificate Error] TLS certificate is invalid"
    err_msg = "Error occured while connecting to server due to TLS certificate error."
    desc_err_msg = ("Try changing Server Certificate Path to 'default'." +
        " If that doesn't work, then try lowering TLS security Level in Avo Assure Client configuration." +
        "\nNote: Setting TLS security level to 'Low' will result in an insecure HTTPS connection\n")
    error = str(e).replace("[engine.io waiting for connection] ",'').replace("[SSL: CERTIFICATE_VERIFY_FAILED] ",'')
    if "_ssl.c" in error:
        err = error[:error.index("(_ssl")]
    elif 'SSLCertVerificationError' in error and "doesn't match" in error:
        err = "[TLS Hostname Mismatch] " + error.split('SSLCertVerificationError')[1][2:-3]
        desc_err_msg = ("Provide a valid hostname for which TLS certificate is issued for." +
            " If that doesn't work, then try setting TLS security Level to 'Med' in Avo Assure Client configuration\n")
    elif 'bad handshake' in error and 'certificate verify failed' in error:
        err = "[TLS Certificate Mismatch] TLS certificate does not match with Server"
    elif 'certificate' in error and 'key values mismatch' in error:
        desc_err_msg = "Client Certificate CA bundle is invalid."
    logger.print_on_console(err_msg)
    logger.print_on_console(err)
    logger.print_on_console(desc_err_msg)
    return err, err_msg, desc_err_msg


class MainNamespace(BaseNamespace):
    def on_message(self, *args):
        global action,cw,browsername,desktopScrapeFlag,allow_connect,connection_Timer,updatecheckFlag,executionOnly
        kill_conn = False
        try:
            if(str(args[0]) == 'connected'):
                err_res = None
                enable_reregister = False
                try:
                    global plugins_list
                    response = json.loads(args[1])
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
                            try:
                                isTrial_val = configvalues["isTrial"]
                                LicenseType = response["license_data"]["LicenseTypes"].lower()
                                isTrial_update = ''
                                if LicenseType == "trial" and isTrial_val != 1:
                                    isTrial_update = 1
                                if LicenseType != "trial" and isTrial_val != 0:
                                    isTrial_update = 0
                                    wx.CallAfter(cw.configItem.Enable)
                                if isTrial_update != '':
                                    configvalues["isTrial"] = isTrial_update
                                    obj_readConfig_class = readconfig.readConfig()
                                    obj_readConfig_class.updateconfig(configvalues)
                                    # By default configItem is disabled for trial users.
                                    # while connect, Here we enabling(LicenseType != "trial") or disabling(LicenseType == "trial") it by user license without restarting the application ice
                                    log.info("The licence you have has changed.")
                                    logger.print_on_console("Your license is modified")
                            except Exception as e:
                                log.error(e)
                                log.info("Error occurred while changing isTrail value in config.json")
                            if root.gui:
                                wx.CallAfter(cw.enable_disconnect)
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
                        logger.print_on_console("Avo Assure Client is not registered with Avo Assure. Click to Register")
                        wx.CallAfter(cw.enable_register)
                    else:
                        logger.print_on_console("Avo Assure Client is not registered with Avo Assure. Try Again")
                if root.gui: wx.CallAfter(cw.connectbutton.Enable)

                if allow_connect:
                    dnd_mode = wx.CallAfter(cw.schedule.GetValue) if root.gui else False
                    msg = ("Do Not Disturb" if dnd_mode else "Normal") + " Mode: Connection to the Avo Assure Server established"
                    logger.print_on_console(msg)
                    log.info(msg)
                    set_ICE_status(False, True, 60000)
                    msg = "Avo Assure Client Name: " + root.ice_token["icename"]
                    logger.print_on_console(msg)
                    log.info(msg)
                    if root.gui:
                        # cw.SetTitle(root.name + " (" + root.ice_token["icename"] + ")")
                        wx.CallAfter(cw.SetTitle,root.name + " (" + root.ice_token["icename"] + ")")
                        wx.CallAfter(cw.schedule.Enable)
                        wx.CallAfter(cw.cancelbutton.Enable)
                        wx.CallAfter(cw.terminatebutton.Enable)
                        wx.CallAfter(cw.clearbutton.Enable)
                        if SYSTEM_OS!='Linux':
                            wx.CallAfter(cw.rollbackItem.Enable,True)
                            wx.CallAfter(cw.updateItem.Enable,True)
                        wx.CallAfter(cw.rbox.Enable)
                    if browsercheckFlag == False:
                        check_browser()
                    #if updatecheckFlag == False and root.gui:
                    if updatecheckFlag == False:
                        msg='Checking for client package updates'
                        logger.print_on_console(msg)
                        log.info(msg)
                        check_PatchUpdate()
                        #updatecheckFlag = clientwindow.check_update(True)
                    if executionOnly:
                        msg='Execution only Mode enabled'
                        logger.print_on_console(msg)
                        log.info(msg)
                    socketIO.timer.resume()
                    socketIO.emit('getconstants', '', dnack=True)
                    conn_time = float(configvalues['connection_timeout'])
                    if (not (connection_Timer != None and connection_Timer.isAlive())
                     and (conn_time >= 8)):
                        log.info("Connection Timeout timer Started")
                        connection_Timer = threading.Timer(conn_time*60*60, root.closeConnection)
                        connection_Timer.start()

            elif(str(args[0]) == 'schedulingEnabled'):
                logger.print_on_console('Do Not Disturb Mode Enabled')
                log.info('Do Not Disturb Mode Enabled')

            elif(str(args[0]) == 'schedulingDisabled'):
                logger.print_on_console('Do Not Disturb Mode Disabled')
                log.info('Do Not Disturb Mode Disabled')

            elif(str(args[0]) == 'fail'):
                fail_msg = "Fail"
                if len(args) > 1 and args[1]=="conn":
                    fail_msg+="ed to connect to Avo Assure Server"
                if len(args) > 1 and args[1]=="disconn":
                    fail_msg+="ed to disconnect from Avo Assure Server"
                logger.print_on_console(fail_msg)
                log.info(fail_msg)
                kill_conn = True

            elif(str(args[0]) == 'decline'):
                fail_msg="Please accept Avo Assure terms and conditions before connecting to Avo Assure Server"
                logger.print_on_console(fail_msg)
                log.info(fail_msg)
                kill_conn = True
                if root.gui: wx.CallAfter(cw.connectbutton.Enable)

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
            wait_until_browsercheck()
            headless_mode = str(configvalues['headless_mode'])=='Yes'
            if headless_mode:
                logger.print_on_console('Object cannot be highlighted in headless mode')
                log.error('Object cannot be highlighted in headless mode')
            else:
                if appType==APPTYPE_WEB:
                    core_utils.get_all_the_imports('WebScrape')
                    import highlight
                    light =highlight.Highlight()
                    #last arg will be scenario flag
                    res = light.perform_highlight(args[0],args[1],args[-1])
                    logger.print_on_console('Highlight result: '+str(res))
                if appType==APPTYPE_MOBILE.lower():
                    core_utils.get_all_the_imports('Mobility/MobileWeb')
                    import highlight_MW
                    light =highlight_MW.Highlight()
                    res = light.perform_highlight(args[0],args[1])
                    logger.print_on_console('Highlight result: '+str(res))
                if appType==APPTYPE_DESKTOP_JAVA.lower():
                    if(not args[0].startswith('iris')):
                        core_utils.get_all_the_imports('Oebs')
                        import oebs_utils
                        light = oebs_utils.Utils()
                        if args[1] == '' or args[1] == ' ':
                            err_msg = 'Invalid Window Name, Highlighting Failed'
                            log.error(err_msg)
                            logger.print_on_console(err_msg)
                        else:
                            res = light.highlight(args[0],args[1],args[3],args[4],args[5],args[6])
                            logger.print_on_console('Highlight result: '+str(res))
                elif appType==APPTYPE_DESKTOP.lower():
                    core_utils.get_all_the_imports('Desktop')
                    import desktop_highlight
                    highlightObj=desktop_highlight.highLight()
                    highlightObj.highlight_element(args[0],args[1])
                elif appType==APPTYPE_SAP.lower():
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
        global cw, execution_flag, qcObject, qtestObject, zephyrObject, azureObject, execReq,testrailObject
        wait_until_browsercheck()
        try:
            exec_data = args[0]
            batch_id = exec_data["batchId"]
            execReq = exec_data
            if("integration" in exec_data):
                if("alm" in exec_data["integration"] and exec_data["integration"]["alm"]["url"] != ""):
                    if(qcObject == None):
                        core_utils.get_all_the_imports('Qc')
                        import QcController
                        qcObject = QcController.QcWindow()
                if("qtest" in exec_data["integration"] and exec_data["integration"]["qtest"]["url"] != ""):
                    if(qtestObject == None):
                        core_utils.get_all_the_imports('QTest')
                        import QTestController
                        qtestObject = QTestController.QTestWindow()
                if("zephyr" in exec_data["integration"] and exec_data["integration"]["zephyr"]["url"] != ""):
                    if(zephyrObject == None):
                        core_utils.get_all_the_imports('Zephyr')
                        import ZephyrController
                        zephyrObject = ZephyrController.ZephyrWindow()
                if("azure" in exec_data["integration"] and exec_data["integration"]["azure"]["url"] != ""):
                    if(azureObject == None):
                        core_utils.get_all_the_imports('Azure')
                        import azurecontroller
                        azureObject = azurecontroller.AzureWindow()
                if("testrail" in exec_data["integration"] and exec_data["integration"]["testrail"]["url"] != ""):
                    if(testrailObject == None):
                        core_utils.get_all_the_imports('Testrail')
                        import testrailController
                        testrailObject = testrailController.testrailWindow()
            aws_mode=False
            if len(args)>0 and args[0]['apptype']=='MobileApp':
                if args[0]['suitedetails'][0]['browserType'][0]=='2':
                    aws_mode = True
            if not execution_flag:
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
        global cw, debugFlag
        try:
            if check_execution_lic("result_debugTestCase"): return None
            wait_until_browsercheck()
            exec_data = args[0]
            root.testthread = TestThread(root, DEBUG, exec_data, False)
            cw.choice=cw.rbox.GetStringSelection()
            logger.print_on_console(str(cw.choice)+' is Selected')
            if cw.choice == 'Normal':
                cw.killChildWindow(debug=True)
            cw.debug_mode=False
            cw.breakpoint.Disable()
            if cw.choice in ['Stepwise','RunfromStep']:
                debugFlag = True
                wx.PostEvent(cw.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CHOICE.typeId, cw.GetId()))
        except Exception as e:
            err_msg='Error while Debugging'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_webscrape(self,*args):#initScraping_ICE socket connection
        try:
            global action,cw,browsername,desktopScrapeFlag,data
            if check_execution_lic("scrape"): return None
            elif bool(cw.scrapewindow): return None
            wait_until_browsercheck()
            args = list(args)
            d = args[0]
            action = d['action']
            headless_mode = str(configvalues['headless_mode'])=='Yes'
            if headless_mode and action in ['scrape','replace']:
                log.info("Scraping cannot be performed in headless mode")
                logger.print_on_console("Scraping cannot be performed in headless mode")
                socketIO.emit('scrape','Terminate')
                return None
            data = {}
            if action == 'userobject':
                core_utils.get_all_the_imports('WebScrape')
                import UserObjectScrape
                webscrape=UserObjectScrape.UserObject()
                webscrape.get_user_object(d,socketIO)
            elif action == 'update_dataset':
                core_utils.get_all_the_imports('IRIS')
                import iris_operations
                iris_operations.update_dataset(d,socketIO)
            else:
                if action in ['scrape','replace']:
                    task = d['task']
                    if str(task) == 'OPEN BROWSER CH':
                        browsername = '1'
                    elif str(task) == 'OPEN BROWSER IE':
                        browsername = '3'
                    elif str(task) == 'OPEN BROWSER FX':
                        browsername = '2'
                    elif str(task) == 'OPEN BROWSER SF':
                        browsername = '6'
                    elif str(task) == 'OPEN BROWSER EDGE':
                        browsername = '7'
                    elif str(task) == 'OPEN BROWSER CHROMIUM':
                        browsername = '8'
                elif action == 'compare':
                    task = d['task']
                    if (d.get('scenarioLevel')==True):
                        data['view'] = d['view']
                        data['scenarioLevel'] = True
                    else:
                        data['view'] = d['viewString']          #view and scraped url extracted here
                        data['scrapedurl'] = d['scrapedurl']
                        data['scenarioLevel'] = False
                    if str(task) == 'OPEN BROWSER CH':
                        browsername = '1'
                    elif str(task) == 'OPEN BROWSER IE':
                        browsername = '3'
                    elif str(task) == 'OPEN BROWSER FX':
                        browsername = '2'
                    elif str(task) == 'OPEN BROWSER EDGE':
                        browsername = '7'
                    elif str(task) == 'OPEN BROWSER CHROMIUM':
                        browsername = '8'
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
            wait_until_browsercheck()
            global action
            core_utils.get_all_the_imports('IRIS')
            d = list(args)[0]
            if (type(d)==dict): action = d['action']
            else: action = None
            if action == 'update_dataset':
                import iris_operations_ai
                iris_operations_ai.update_dataset(d,socketIO)
            else:
                global browsername, desktopScrapeObj, desktopScrapeFlag
                browsername = args
                core_utils.get_all_the_imports('Desktop')
                import desktop_scrape
                desktopScrapeObj=desktop_scrape
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
            wait_until_browsercheck()
            global action
            core_utils.get_all_the_imports('IRIS')
            d = list(args)[0]
            if (type(d)==dict): action = d['action']
            else: action = None
            if action == 'update_dataset':
                import iris_operations
                iris_operations.update_dataset(d,socketIO)
            else:
                global browsername, sapScrapeObj, sapScrapeFlag
                browsername = args[0]
                core_utils.get_all_the_imports('SAP')
                import sap_scrape
                sapScrapeObj=sap_scrape
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
            wait_until_browsercheck()
            global browsername
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
            core_utils.get_all_the_imports('Mobility')
            core_utils.get_all_the_imports('Saucelabs')
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
            wait_until_browsercheck()
            global mobileWebScrapeObj,mobileWebScrapeFlag,action,data
            global browsername
            browsername = args[0]+";"+args[1]
            args = list(args)
            d = args[2]
            data = {}
            action = d['action']
            core_utils.get_all_the_imports('Mobility')
            if action == 'userobject':
                core_utils.get_all_the_imports('Mobility/MobileWeb')
                import UserObjectScrape_MW
                webscrape=UserObjectScrape_MW.UserObject()
                webscrape.get_user_object(d,socketIO)
            elif action == 'compare':
                mobileWebScrapeFlag=True
                # task = d['task']
                data['view'] = d['viewString']
                data['scrapedurl'] = d['scrapedurl']
            else:
                if action == 'scrape':
                    # task = d['task']
                    core_utils.get_all_the_imports('Mobility/MobileWeb')
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
            wait_until_browsercheck()
            logger.print_on_console("Entering inside PDF scrape")
            global pdfScrapeObj,pdfScrapeFlag
            global browsername
            browsername = args[0]
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
            wait_until_browsercheck()
            global action
            core_utils.get_all_the_imports('IRIS')
            d = list(args)[0]
            if (type(d)==dict): action = d['action']
            else: action = None
            if action == 'update_dataset':
                import iris_operations
                iris_operations.update_dataset(d,socketIO)
            else:
                global browsername, oebsScrapeObj, oebsScrapeFlag
                browsername = args[0]
                core_utils.get_all_the_imports('Oebs')
                import oebs_scrape_dispatcher
                oebsScrapeObj=oebs_scrape_dispatcher
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
            wait_until_browsercheck()
            core_utils.get_all_the_imports('WebServices')
            import wsdlgenerator
            wsdlurl = str(args[0])
            wsdl_object = wsdlgenerator.WebservicesWSDL()
            import_def=False
            response = wsdl_object.listOfOperation(wsdlurl,import_def)
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
            wait_until_browsercheck()
            serverCertificate=None
            serverCerificate_pass=None
            auth_uname=None
            auth_pass=None
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
                    log.info(key)
                    log.info(responseHeader[key])
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

    def on_WS_ImportDefinition(self, *args):
        try:
            if check_execution_lic("result_WS_ImportDefinition"): return None
            wait_until_browsercheck()
            core_utils.get_all_the_imports('WebServices')
            import wsdlgenerator
            wsdlurl = str(args[0])
            wsdl_object = wsdlgenerator.WebservicesWSDL()
            import_def=True
            response = wsdl_object.listOfOperation(wsdlurl,import_def)
            log.debug(response)
            socketIO.emit('result_WS_ImportDefinition',response)
        except Exception as e:
            err_msg='Error while Fetching WSDL Operations'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_ExecuteRequestTemplate(self, *args):
        try:
            wait_until_browsercheck()
            core_utils.get_all_the_imports('WebServices')
            import  webservices
            wsdlurl = str(args[0])
            ws_object = webservices.WSkeywords()
            response = ws_object.executeRequestTemplate(wsdlurl)
            response=str(response)
            log.debug(response)
            socketIO.emit('result_ExecuteRequestTemplate',response)
        except Exception as e:
            err_msg='Error while executing'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_qclogin(self, *args):
        global qcObject
        err_msg = None
        try:
            wait_until_browsercheck()
            if qcObject is None:
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

    def on_qtestlogin(self, *args):
        global qtestObject
        err_msg = None
        try:
            wait_until_browsercheck()
            if qtestObject is None:
                core_utils.get_all_the_imports('QTest')
                import QTestController
                qtestObject = QTestController.QTestWindow()
            qcdata = args[0]
            response = qtestObject.qc_dict[qcdata.pop('qcaction')](qcdata)
            socketIO.emit('qcresponse', response)
        except KeyError:
            err_msg = 'Invalid qTest operation'
        except Exception as e:
            err_msg = 'Error in qTest operations'
            log.error(e, exc_info=True)
        if err_msg is not None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
            try: socketIO.emit('qcresponse','Error:Qtest Operations')
            except: pass

    def on_zephyrlogin(self, *args):
        global zephyrObject
        err_msg = None
        try:
            wait_until_browsercheck()
            if zephyrObject is None:
                core_utils.get_all_the_imports('Zephyr')
                import ZephyrController
                zephyrObject = ZephyrController.ZephyrWindow()
            zephyrdata = args[0]
            response = zephyrObject.zephyr_dict[zephyrdata.pop('zephyraction')](zephyrdata)
            socketIO.emit('qcresponse', response)
        except KeyError:
            err_msg = 'Invalid Zephyr operation'
        except Exception as e:
            err_msg = 'Error in Zephyr operations'
            log.error(e, exc_info=True)
        if err_msg is not None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
            try: socketIO.emit('qcresponse','Error:Zephyr Operations')
            except: pass

    def on_render_screenshot(self,*args):
        try:
            wait_until_browsercheck()
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
            wait_until_browsercheck()
            core_utils.get_all_the_imports('WebOcular')
            import webocular
            wobj = webocular.Webocular()
            args=list(args)
            # Currently there are 5 arguments.
            # args[0] is URL, args[1] is level, args[2] is agent, args[3] is proxy,args[4] is searchData
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
            wait_until_browsercheck()
            core_utils.get_all_the_imports('Jira')
            import jiracontroller
            obj = jiracontroller.JiraWindow()
            if args[0] == JIRA_ACTION_1:
                data = args[1]
                obj.getAllAutoDetails(data,socketIO)
            elif args[0] == JIRA_ACTION_2:
                data = args[1]
                obj.createIssue(data,socketIO)
            elif args[0] == JIRA_ACTION_3:
                data = args[1]
                obj.getConfigureFields(data,socketIO)
            elif args[0] == JIRA_ACTION_4:
                data = args[1]
                obj.get_projects(data,socketIO)
            elif args[0] == JIRA_ACTION_5:
                data = args[1]
                data['project_selected']=args[2]
                data['item_type']=args[3]
                obj.get_testcases(data,socketIO)
            elif args[0] == JIRA_ACTION_6:
                data = args[1]
                data['project_selected']=args[2]
                data['item_type']=args[3]
                obj.get_testcases_json(data,socketIO)    
        except Exception as e:
            err_msg='Error in JIRA operations'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_azurelogin(self,*args):
        try:
            wait_until_browsercheck()
            core_utils.get_all_the_imports('Azure')
            import azurecontroller
            obj = azurecontroller.AzureWindow()
            if args[0] == Azure_ACTION_1:
                data = args[1]
                obj.get_all_auto_details(data,socketIO)
            elif args[0] == Azure_ACTION_2:
                data = args[1]
                obj.get_createWorkItem(data,socketIO)
            elif args[0] == Azure_ACTION_3:
                data = args[1]
                obj.get_configure_fields(data,socketIO)
            elif args[0] == Azure_ACTION_4:
                data = args[1]
                obj.get_projects(data,socketIO)
            elif args[0] == Azure_ACTION_5:
                data = args[1]
                data['project_selected']=args[2]
                data['item_type']=args[3]
                obj.get_testcases(data,socketIO)
            elif args[0] == Azure_ACTION_6:
                data = args[1]
                obj.get_userstories(data,socketIO)
            elif args[0] == Azure_ACTION_7:
                data = args[1]
                obj.get_testplans(data,socketIO)
            elif args[0] == Azure_ACTION_8:
                data = args[1]
                obj.get_testsuites(data,socketIO)
            elif args[0] == Azure_ACTION_9:
                data = args[1]
                obj.get_testcases(data,socketIO)
        except Exception as e:
            err_msg='Error in Azure operations'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)
    
    def on_saucelablogin(self,*args):
        try:
            wait_until_browsercheck()
            core_utils.get_all_the_imports('Saucelabs')
            import saucelabcontroller
            obj = saucelabcontroller.SaucelabWindow()
            if args[0]['action'] == Saucelab_ACTION_1:
                data = args[0]
                obj.get_webconf_details(data,socketIO)
            elif args[0]['action'] == Saucelab_ACTION_2:
                data = args[0]
                obj.get_mobileconf_details(data,socketIO)
            elif args[0]['action'] == Saucelab_ACTION_3:
                data = args[0]
                obj.update_mobile_details(data,socketIO)
        except Exception as e:
            err_msg='Error in Saucelab operations'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_logintobrowserstack(self, *args):
        try:
            wait_until_browsercheck()
            core_utils.get_all_the_imports('Browserstack')
            import browserstackcontroller
            obj = browserstackcontroller.BrowserstackWindow()
            if args[0]['action'] == Browserstack_ACTION_1:
                data = args[0]
                obj.get_webconf_details(data, socketIO)
            elif args[0]['action'] == Browserstack_ACTION_2:
                data = args[0]
                obj.get_mobileconf_details(data, socketIO)
            elif args[0]['action'] == Browserstack_ACTION_3:
                data = args[0]
                obj.uploadApk_bs(data, socketIO)
            else:
                logger.print_on_console("Not able to login to BrowserStack")  

        except Exception as e:        
                err_msg='Error in Browserstack operations'
                log.error(err_msg)
                logger.print_on_console(err_msg)
                log.error(e,exc_info=True)

    def on_update_screenshot_path(self,*args):
        if root.gui: benchmark.init(args[1], socketIO)
        intv = 120000
        if args and len(args) >= 2:
            try: intv = int(args[2])
            except: pass
        set_ICE_status(False, True, intv)
        spath=args[0]
        import constants
        if(SYSTEM_OS=='Darwin'):
            spath=spath["mac"]
        elif SYSTEM_OS == 'Linux':
            spath=spath['linux']
        else:
            spath=spath["default"]
        if  len(spath) == 0 :
            constants.SCREENSHOT_PATH = os.getcwd()+OS_SEP+'screenshots'
        elif len(spath) != 0 and os.path.exists(spath):
            constants.SCREENSHOT_PATH=os.path.normpath(spath)+OS_SEP
        else:
            constants.SCREENSHOT_PATH="Disabled"
            logger.print_on_console("Screenshot capturing disabled since user does not have sufficient privileges for screenshot folder\n")
            log.info("Screenshot capturing disabled since user does not have sufficient privileges for screenshot folder\n")
        #----------------------------------------------------------------------Object Prediction Path
        if args and len(args) >= 3:
            predictionPath = args[3]
            if(SYSTEM_OS=='Darwin'):
                predictionPath = predictionPath["mac"]
            else:
                predictionPath = predictionPath["default"]
            if len(predictionPath) != 0 and os.path.exists(predictionPath):
                constants.PREDICTION_IMG_DIR = os.path.normpath(predictionPath) + OS_SEP
                #check if folders exist, if they dont create:
                check_list = ['button','checkbox','dropdown','textbox','scroll','image','label','listbox','radiobutton','table','tree']
                for c in check_list:
                    if (os.path.exists(constants.PREDICTION_IMG_DIR + str(c))):
                        log.debug( str(c) + ' folder found in object prediction dataset path')
                    else:
                        try:
                            log.debug( 'Creating folder ' + str(c) + ' in object prediction dataset path....')
                            os.makedirs(constants.PREDICTION_IMG_DIR + str(c))
                            log.debug( 'Created folder ' + str(c) + ' in object prediction dataset path')
                        except Exception as e:
                            log.error( 'Error occured during the creation of ' + str(c) + ' folder in dataset path, ERR_MSG : ' + str(e) )
                #below code is redundant once all CBU's move to AvoAssure_3.2 & upwards
                #check if'hscroll','vscroll' folders exist, if so move contents to scroll and delete hscroll and vscroll
                for s in ['hscroll','vscroll']:
                    if (os.path.exists(constants.PREDICTION_IMG_DIR + s)):
                        try:
                            file_names = os.listdir(constants.PREDICTION_IMG_DIR + s)
                            for file_name in file_names:
                                try: shutil.move(os.path.join(constants.PREDICTION_IMG_DIR + s, file_name), constants.PREDICTION_IMG_DIR + 'scroll')
                                except: log.debug( file_name + '" already exists, in destination path.')
                            shutil.rmtree(constants.PREDICTION_IMG_DIR + s)
                        except :
                            log.error( 'Unable to delete '+ s +' dir' )
            else:
                constants.PREDICTION_IMG_DIR="Disabled"
                # logger.print_on_console("Object Prediction Manual Training disabled since user does not have sufficient privileges for object prediction dataset folder\n")
                # log.info("Object Prediction Manual Training disabled since user does not have sufficient privileges for object prediction dataset folder\n")

    def on_generateFlowGraph(self,*args):
        try:
            wait_until_browsercheck()
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
            wait_until_browsercheck()
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
            wait_until_browsercheck()
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
            if (len(args) > 1 and args[1] == "dereg"):
                msg = 'Avo Assure Client "'+root.ice_token["icename"]+'" is Deregistered.'
                logger.print_on_console(msg)
                log.info(msg)
                root.token_obj.delete_token()
                root.ice_token = None
            if root.gui: threading.Timer(1,cw.OnNodeConnect,[wx.EVT_BUTTON]).start()
            else: threading.Timer(1,root.connection,["disconnect"]).start()
        except Exception as e:
            err_msg='Exception while Remote Disconnect'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_connect_error(self, *args):
        """ Connection related errors are passed here
        """
        # print(args)
        # print(socketIO.eio.hidden_error)
        pass

    def on_disconnect(self, *args):
        if not allow_connect: return
        log.info('Disconnect triggered')
        stop_ping_thread()
        if socketIO is not None:
            root.icesession['connect_time'] = str(datetime.now())
            socketIO.eio.http.params['icesession'] = json.dumps(root.icesession)
            if root.gui:
                if not bool(cw): return
                cw.schedule.Disable()
                cw.connectbutton.Disable()
            """Enables the Register button , if disconnection happened due to Invalid Token"""
            if root.ice_token is None:
                if root.gui: wx.CallAfter(cw.enable_register)
                return
            else:
                msg = 'Connectivity issue with Avo Assure Server. Attempting to restore connectivity...'
                logger.print_on_console(msg)
                log.error(msg)
        if root.ice_token:
            if not bool(cw): return
            cw.enable_connect(enable_button = False, repaint_title = False)

    def on_irisOperations(self, *args):
        try:
            wait_until_browsercheck()
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

    def on_getSerialNumber(self, *args):
        try:
            wait_until_browsercheck()
            core_utils.get_all_the_imports('Mobility')
            core_utils.get_all_the_imports('Saucelabs')
            import mobile_app_scrape
            obj = mobile_app_scrape.MobileWindow()
            obj.run_adb_devices(socketIO)
        except Exception as e:
            err_msg='Error occured in getting the device serial number'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)       

    def on_checkingMobileClient(self, *args):
        try:
            wait_until_browsercheck()
            core_utils.get_all_the_imports('Mobility')
            import mobile_app_scrape
            obj = mobile_app_scrape.MobileWindow()
            obj.checking_mobile_client(socketIO)
        except Exception as e:
            err_msg='Error occured in Checking Mobile Client'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e,exc_info=True)

    def on_LAUNCH_SAP_GENIUS(self, *args):
        try:
            if check_execution_lic("scrape"):
                return None
            elif bool(cw.scrapewindow):
                return None

            global application_path, sapScrapeFlag
            application_path = args[0]
            app_details = []
            file_location = application_path.split(';')[0]
            window_name = application_path.split(';')[1]
            server_name = [application_path.split(';')[2]]
            app_details.append(file_location)
            app_details.append(window_name)
            core_utils.get_all_the_imports('SAP')
            import sap_launch_keywords
            obj = sap_launch_keywords.Launch_Keywords()
            launch_status = obj.launch_application(app_details)
            server_connect_status = obj.serverConnect(server_name)
            sapScrapeFlag=True
        except Exception as error:
            err_msg='Error while launching SAP application through Genius'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(error,exc_info=True)

    def on_START_SCRAPE_SAP_GENIUS(self, *args):
        try:
            if check_execution_lic("scrape"):
                return None
            elif bool(cw.scrapewindow):
                return None

            global sapScrapeFlag
            core_utils.get_all_the_imports('SAP')
            import sap_scraping_genius
            sap_scraping_obj = sap_scraping_genius.Scrape()
            sap_scraping_obj.clickandadd('STARTCLICKANDADD', socketIO, args[1])
            sapScrapeFlag=True
        except Exception as error:
            err_msg='Error while Scraping SAP application through Genius'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(error,exc_info=True)

    def on_STOP_SCRAPE_SAP_GENIUS(self, *args):
        try:
            if check_execution_lic("scrape"):
                return None
            elif bool(cw.scrapewindow):
                return None

            global sapScrapeFlag
            core_utils.get_all_the_imports('SAP')
            import sap_scraping_genius
            import sap_launch_keywords
            sap_scraping_obj = sap_scraping_genius.Scrape()
            sap_scraping_obj.clickandadd('STOPCLICKANDADD', socketIO, args[1])
            sap_launch_keywords_obj = sap_launch_keywords.Launch_Keywords()
            sap_launch_keywords_obj.close_window()
            sapScrapeFlag=True
        except Exception as error:
            err_msg='Error while Scraping SAP application through Genius'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(error,exc_info=True)

    def on_testraillogin(self, *args):
        global testrailObject
        err_msg = None
        try:
            wait_until_browsercheck()
            if testrailObject is None:
                core_utils.get_all_the_imports('Testrail')
                import testrailController
                testrailObject = testrailController.testrailWindow()
            data = args[0]
            response = testrailObject.testrail_dict[data['testrailAction']](data)
            
            if data['testrailAction'] == 'getTestCases':
                socketIO.emit(f'qcresponse{response[0]["section_id"]}', response)
            elif data['testrailAction'] == 'getSections':
                socketIO.emit(f'qcresponse{response[0]["suite_id"]}', response)
            else:
                socketIO.emit('qcresponse', response)
        except KeyError:
            err_msg = 'Invalid testrail operation'
        except Exception as e:
            err_msg = e
            log.error(e, exc_info=True)
        if err_msg is not None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
            error = 'testrail Operations'
            try: socketIO.emit('qcresponse',f'Error:{error}')
            except: pass


class ConnectionThread(threading.Thread):
    """Socket Connection Thread Class."""
    daemon = True
    name = "socketIO_connection"

    def __init__(self, ice_action):
        """Init Worker Thread Class."""
        super(ConnectionThread, self).__init__()
        self.ice_action = ice_action

    def get_ice_session(self, no_params = False):
        server_cert = configvalues['server_cert']
        tls_security = configvalues['tls_security']
        if tls_security == "Low":
            server_cert = False
        elif server_cert != "default":
            if os.path.exists(server_cert) == False:
                server_cert = CERTIFICATE_PATH + OS_SEP +'server.crt'
        client_cert = (CERTIFICATE_PATH + OS_SEP + 'client.crt', CERTIFICATE_PATH + OS_SEP + 'client.key')
        args = {
            "cert": client_cert,
            "proxies": proxies,
            "headers": {'User-Agent': 'AvoAssure/' + os.getenv('AVO_ASSURE_VERSION', '3.0.0')}
        }
        if server_cert != "default": args["verify"] = server_cert
        if tls_security != "High": args['assert_hostname'] = False
        if no_params:
            return args
        username = str(os.getenv('USERNAME', os.getenv('USER', 'N/A'))).lower()
        root.ice_token["hostname"] = socket.gethostname()
        root.icesession = {
            'ice_id': str(uuid.uuid4()),
            'connect_time': str(datetime.now()),
            'username': username,
            'iceaction': self.ice_action,
            'icetoken': root.ice_token,
            'data': random()*100000000000000,
            'host': configvalues['server_ip']
        }
        params={'username': username, 'icename': root.ice_token["icename"],
            'ice_action': self.ice_action, 'icesession': json.dumps(root.icesession)}
        args["params"] = params
        return args

    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        reg_hostname = hostname = socket.gethostname()
        if "hostname" in root.ice_token: reg_hostname=root.ice_token["hostname"]
        """Check if registered hostname in the Token matches with the current hostname"""
        if reg_hostname != hostname:
            msg="Access denied: Hostname doesn't match. Avo Assure Client is registered with a different hostname "+reg_hostname
            logger.print_on_console(msg)
            log.error(msg)
            root.ice_token = None
            if root.gui: wx.CallAfter(cw.enable_register)
            return False
        global socketIO, allow_connect
        allow_connect = False
        err = None
        err_msg = "Error in Server Connection"
        server_url = 'https://' + configvalues['server_ip'] + ':' + configvalues['server_port']
        try:
            kw_args = self.get_ice_session()
            kw = {
                'request_timeout': 10,
                'http_session': prepare_http_session(kw_args),
                'ssl_verify': kw_args.get('verify', True)
            }
            socketIO = SocketIO(**kw)
            socketIO.register_namespace(MainNamespace())
            socketIO.connect(server_url)
            root.socketIO = socketIO
            # socketIO.wait()
        except Exception as e:
            err = e
            if socketIO is not None and socketIO.eio.hidden_error:
                err = e = socketIO.eio.hidden_error
                socketIO.eio.hidden_error = None
            if 'certificate' in str(e) or 'SSLError' in str(e):
                err, err_msg, _ = _process_ssl_errors(e)
            else:
                logger.print_on_console(err_msg)
        if err:
            log.error(err_msg)
            log.error(err)
            if root.gui: wx.CallAfter(cw.connectbutton.Enable)

    
class TestThread(threading.Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self, main, action, json_data, aws_mode, cicd_mode=False):
        """Init Worker Thread Class."""
        super(TestThread, self).__init__()
        self.name = "test_thread"
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
        self.cicd_mode = cicd_mode
        self.test_status = 'pass'
        self.start()    # start the thread

    #should just resume the thread
    def resume(self,debug_mode):
        if self.con == '': return
        if not(debug_mode):
            self.con.debug_mode=False
        self.con.resume_execution()

    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        if self.cicd_mode:
            check_browser()
            cicd_integration_obj(self.json_data)
        global execution_flag, closeActiveConnection, connection_Timer, termination_inprogress, execReq
        batch_id = None
        termination_inprogress = True
        try:
            self.con = controller.Controller()
            self.con.configvalues=configvalues
            self.con.exception_flag=(str(configvalues["exception_flag"]).strip().lower()=="true")
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
                            if "-" not in runfrom_step:
                                runfrom_step=int(runfrom_step)
                        except Exception as e:
                            runfrom_step=0
            if self.main.gui:
                self.cw.schedule.Disable()
                self.cw.rbox.Disable()
                self.cw.breakpoint.Disable()
                self.cw.terminatebutton.Enable()
            status = ''
            apptype = ''
            if(self.action == DEBUG):
                apptype = (self.json_data)[0]['apptype']
            else:
                execution_flag = True
                #set Avo Assure Client status as busy
                set_ICE_status(True)
                if root.gui: benchmark.stop(True)
                apptype = self.json_data['apptype']
            if apptype == "DesktopJava": apptype = "oebs"
            if self.cicd_mode:
            # if apptype.lower() not in plugins_list:
            #     logger.print_on_console('This app type is not part of the license.')
            #     status=TERMINATE
            # else:
                status = self.con.invoke_controller(self.action,self,self.debug_mode,runfrom_step,self.json_data,self.main,socketIO,qcObject,qtestObject,zephyrObject,azureObject,testrailObject,self.aws_mode,self.cicd_mode)
            else:
                if apptype.lower() not in plugins_list:
                    logger.print_on_console('This app type is not part of the license.')
                    status=TERMINATE
                else:
                    status = self.con.invoke_controller(self.action,self,self.debug_mode,runfrom_step,self.json_data,self.main,socketIO,qcObject,qtestObject,zephyrObject,azureObject,testrailObject,self.aws_mode,self.cicd_mode)

            logger.print_on_console('Execution status '+status)
            if status==TERMINATE:
                logger.print_on_console('---------Termination Completed-------',color="YELLOW")
            if self.cicd_mode:
                opts = self.main.opts
                if self.test_status == 'pass' and status != COMPLETED: self.test_status = 'fail'
                result = {"status":status, "batchId": batch_id, "testStatus": self.test_status}
                result['exec_req'] = {'execReq':self.json_data}
                result["event"] = "result_executeTestSuite"
                result["configkey"] = opts.configkey
                result["executionListId"] = opts.executionListId
                result["agentname"] = opts.agentname
                server_url = 'https://' + opts.serverurl + ':' + opts.serverport + '/setExecStatus'
                # res = requests.post(server_url,json=result, verify=False)
                from retryapis_cicd import Retryrequests
                res = Retryrequests.retry_cicd_apis(self, server_url, result)
                controller.kill_process()
            else:
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
                    if self.test_status == 'pass' and status != COMPLETED: self.test_status = 'fail'
                    result = {"status":status, "batchId": batch_id, "testStatus": self.test_status}
                    if controller.manual_terminate_flag: result["userTerminated"] = True
                    result['execReq'] = execReq
                    socketIO.emit('result_executeTestSuite', result)
        except Exception as e:
            log.error(e, exc_info=True)
            if self.cicd_mode is False:
                status=TERMINATE
                if socketIO is not None:
                    if self.action==DEBUG:
                        self.cw.killChildWindow(debug=True)
                        socketIO.emit('result_debugTestCase',status)
                    elif self.action==EXECUTE:
                        result = {"status":status, "batchId": batch_id, "testStatus": 'fail'}
                        if controller.manual_terminate_flag: result["userTerminated"] = True
                        result['execReq'] = execReq
                        socketIO.emit('result_executeTestSuite', result)
        if closeActiveConnection:
            closeActiveConnection = False
            connection_Timer = threading.Timer(300, self.main.closeConnection)
            connection_Timer.start()

        self.main.testthread = None
        execution_flag = False
        #set Avo Assure Client status as available
        termination_inprogress = False
        set_ICE_status(True)
        if self.main.gui:
            if self.cw.choice=='RunfromStep': self.cw.breakpoint.Enable()
            else: self.cw.breakpoint.Disable()
            # self.cw.breakpoint.Clear()
            self.cw.rbox.Enable()
            self.cw.cancelbutton.Enable()
            self.cw.schedule.Enable()


class Main():
    def __init__(self, appName, args, loadingobj):
        self.name = appName
        self.gui = not (args.register or args.connect)
        self.cw = None
        self.testthread = None
        self.socketthread = None
        self.ice_token = None
        self.icesession = None
        self.server_url = None
        self._wants_to_close = False
        self.ice_register_token = None
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
        # else:
        #logger.init_colorama(autoreset=True)
        if not self.opts.execute:
            loadingobj.Close()
        
        """ Creating Root Logger using logger file config and setting logfile path, which is in config.json """
        try:
            logfilename = os.path.normpath(configvalues["logFile_Path"]).replace("\\","\\\\")
            logging.config.fileConfig(LOGCONFIG_PATH,defaults={'logfilename': logfilename},disable_existing_loggers=False)
        except Exception as e:
            logfilename_error_flag = True
            log.error(e)

        log.info('Started')
        self.print_banner()
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.CRITICAL)

        '''Following two lines set 'CRITICAL' log level for selenium, uncomment these to not log entries from selenium if current log level is < CRITICAL'''
        # selenium_log = logging.getLogger("selenium")
        # selenium_log.setLevel(logging.CRITICAL)

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
                    msg = "Connecting Avo Assure Client in guest mode"
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

    def close(self, *args):
        global connection_Timer
        controller.terminate_flag = True
        controller.manual_terminate_flag = True
        controller.disconnect_flag = True
        if self.socketthread: logger.print_on_console('Disconnected from Avo Assure server')
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
            nul = subprocess.DEVNULL
            subprocess.Popen("TASKKILL /F /IM AvoAssureMFapi.exe", stdout=nul, stderr=nul)
        sys.exit(0)


    def register(self, token, hold = False):
        ice_das_key = "".join(['a','j','k','d','f','i','H','F','E','o','w','#','D','j',
            'g','L','I','q','o','c','n','^','8','s','j','p','2','h','f','Y','&','d'])
        err = False
        err_msg = "Error: Invalid Server address or Token . Please try again"
        try:
            token_dec = core_utils_obj.unwrap(token,ice_das_key).split("@")
            token_info = {'token':token_dec[0],'icetype':token_dec[1] ,'icename':token_dec[2]}
            if self.gui and token_info["icetype"] != "normal":
                err_msg = "Token is provisioned for CI-CD Avo Assure Client. Either use a token provisioned for Normal mode or register Avo Assure Client in command line mode."
                raise ValueError("Invalid Token/Avo Assure Client mode")
            if not self.gui and token_info["icetype"] == "normal":
                err_msg = "Token is provisioned for Normal Avo Assure Client. Either use a token provisioned for CI-CD mode or register Avo Assure Client in GUI mode."
                raise ValueError("Invalid Token/Avo Assure Client mode")
            self.ice_token = token_info
            url = self.server_url.split(":")
            configvalues['server_ip']=url[0]
            if len(url) == 1: url.append("443")
            configvalues['server_port']=url[1]
            if not hold: self.connection("register")
            # Name : sreenivasulu A
            if self.ice_register_token == "validICE":
                return True
        except requests.exceptions.SSLError as e:
            err, err_msg, _ = _process_ssl_errors(str(e))
        except Exception as e:
            err = e
            if 'certificate' in str(e):
                err, err_msg, _ = _process_ssl_errors(e)
                return False
            else:
                logger.print_on_console(err_msg)
                return False
        if err:
            log.error(err_msg)
            log.error(err)
            if self.gui: wx.CallAfter(self.cw.enable_register)
            else: self._wants_to_close = True
            # Name : sreenivasulu A
            return False 

    def connection(self, mode):
        try:
            if mode == 'register':
                if self.ice_token is None:
                    self.verifyRegistration()
                    return None
                kw_args = ConnectionThread(mode).get_ice_session()
                data = kw_args.pop('params')
                prep_req = prepare_http_session(kw_args)
                del data['username']
                del data['ice_action']
                kw_args.pop('assert_hostname', None)
                server_url = "https://"+self.server_url+"/ICE_provisioning_register"
                res = prep_req.post(server_url, data=data, **kw_args)
                response = res.content
                try:
                    err_res = None
                    enable_reregister = False
                    if response == "fail":
                        err_res = "Avo Assure Client registration failed."
                    else:
                        response = json.loads(response)
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
                                wx.CallAfter(cw.enable_connect)
                                # cw.enable_connect()
                            msg='Avo Assure Client "'+data["icename"]+'" registered successfully with Avo Assure'
                            self.ice_register_token = response["status"]
                            logger.print_on_console(msg)
                            log.info(msg)
                except Exception as e:
                    err_res = 'Error in Avo Assure Client Registration'
                    logger.print_on_console(err_res)
                    log.info(err_res)
                    log.error(e, exc_info=True)
                    enable_reregister = True
                if enable_reregister:
                    self.ice_action = "register"
                    self.ice_token = None
                    self.token_obj.delete_token()
                    if self.gui:
                        logger.print_on_console("Avo Assure Client is not registered with Avo Assure. Click to Register")
                        wx.CallAfter(cw.enable_register)
                    else:
                        logger.print_on_console("Avo Assure Client is not registered with Avo Assure. Try Again")
                if self.gui: wx.CallAfter(cw.connectbutton.Enable)
                else: self._wants_to_close = True
            elif mode == 'connect' or mode == "guestconnect":
                if mode == "guestconnect": status = True
                else:
                    # Re-Check token file on connection
                    status = self.verifyRegistration(verifyonly = True)
                if status == False:
                    self.ice_action = "register"
                    self.ice_token = None
                    msg = "Avo Assure Client is not registered with Avo Assure."
                    if self.gui:
                        msg += " Click to Register"
                        logger.print_on_console(msg)
                        log.error(msg)
                        wx.CallAfter(cw.enable_register)
                    else:
                        logger.print_on_console(msg)
                        log.error(msg)
                        self._wants_to_close = True
                    return None
                # Avo Assure Client is registered
                ip = configvalues['server_ip']
                port = configvalues['server_port']
                conn = http.client.HTTPConnection(ip,int(port))
                if proxies:
                    proxy = readconfig.readProxyConfig().readRawJson()
                    proxy_url = proxy['url'].split(':')
                    proxy_port = 80 if proxy['scheme'] == 'http' else 443
                    if len(proxy_url) > 1:
                        proxy_url, proxy_port = proxy_url
                    auth_hash = base64.b64encode((proxy['username']+":"+proxy['password']).encode('utf-8')).decode("utf-8")
                    conn = http.client.HTTPSConnection(proxy_url, port=proxy_port)
                    conn.set_tunnel((ip+':'+port), headers={"Proxy-Authorization": f"Basic {auth_hash}"})
                conn.connect()
                conn.close()
                self.socketthread = ConnectionThread(mode)
                self.socketthread.start()
                self.socketthread.join()
            else:
                self.killSocket(True)
                log.info('Disconnected from Avo Assure server')
                logger.print_on_console('Disconnected from Avo Assure server')
                global connection_Timer
                if (connection_Timer != None and connection_Timer.isAlive()):
                    log.info("Connection Timeout Timer Stopped")
                    connection_Timer.cancel()
                    connection_Timer = None
                if not self.gui: self._wants_to_close = True
                else:
                    if not self.token_obj.token: wx.CallAfter(cw.enable_register)
        except Exception as e:
            emsg="Forbidden request, Connection refused, please configure server ip and server port in "
            if self.gui: emsg += "Edit -> Configuration"
            else: emsg += "configuration file located at AVO_ASSURE_HOME/assets/config.json"
            emsg += ", and retry."
            if mode == "register":
                self.ice_token = None
                emsg = "Connection refused: Invalid Server URL."
                if self.gui:
                    emsg += " Click on Connect to retry Registration"
                    wx.CallAfter(cw.enable_register)
            logger.print_on_console(emsg)
            log.error(emsg)
            log.error(e,exc_info=True)
            raise

    def killSocket(self, disconn=False):
        #Disconnects socket client
        global socketIO
        try:
            stop_ping_thread()
            log.info('Cancelling Ping Thread')
            if socketIO is not None:
                if disconn:
                    log.info('Sending socket disconnect request')
                    socketIO.send('unavailableLocalServer', dnack=True)
                socketIO.safe_disconnect()
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
                cw.OnNodeConnect(wx.EVT_BUTTON)
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
        emsg = "Avo Assure Client is not registered."
        executionOnly = True
        try:
            self.token_obj = ICEToken()
            self.server_url = configvalues['server_ip']+':'+configvalues['server_port']
            self.Ice_Token = configvalues['ice_Token']
            if self.token_obj.token:
                self.ice_token = self.token_obj.token
                emsg = None
                icetype = self.ice_token["icetype"]
                name = self.ice_token["icename"]
                if self.gui:
                    if icetype != "normal":
                        emsg = "Access denied: "+name+" is registered for CI-CD mode. Avo Assure Client has to run in command line mode"
                    else:
                        executionOnly = False
                        cw.EnableAll()
                        if verifyonly: cw.connectbutton.Disable()
                else:
                    if icetype != "ci-cd":
                        emsg = "Access denied: "+name+" is registered for Normal mode. Avo Assure Client has to run in GUI mode"
                    elif self.opts.register:
                        emsg = "Registration denied: Avo Assure Client already Registered."
                if emsg:
                    log.error(emsg)
                    logger.print_on_console(emsg)
                    if not self.gui: self._wants_to_close=True
                    return False
                return True
            else:
                if self.gui:
                    if not verifyonly:
                        wx.CallAfter(cw.enable_register,enable_button=False)
                        self.token_obj.token_window(self, IMAGES_PATH)
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
            wait_until_browsercheck()
            cw.schedule.Disable()
            core_utils.get_all_the_imports('IRIS')
            if mobileScrapeFlag==True:
                cw.scrapewindow = mobileScrapeObj.ScrapeWindow(parent = cw,id = -1, title="Avo Assure - Mobile Scrapper",filePath = browsername,socketIO = socketIO)
                mobileScrapeFlag=False
            elif mobileWebScrapeFlag==True:
                cw.scrapewindow = mobileWebScrapeObj.ScrapeWindow(parent = cw,id = -1, title="Avo Assure - Mobile Scrapper",browser = browsername,socketIO = socketIO,action=action,data=data)
                mobileWebScrapeFlag=False
            elif desktopScrapeFlag==True:
                cw.scrapewindow = desktopScrapeObj.ScrapeWindow(parent = cw,id = -1, title="Desktop-Element Identification",filePath = browsername,socketIO = socketIO)
                desktopScrapeFlag=False
                browsername = ''
            elif sapScrapeFlag==True:
                cw.scrapewindow = sapScrapeObj.ScrapeWindow(parent = cw,id = -1, title="SAP-Element Identification",filePath = browsername,socketIO = socketIO)
                sapScrapeFlag=False
            elif oebsScrapeFlag==True:
                oebsScrapeFlag=False
                cw.scrapewindow = oebsScrapeObj.ScrapeDispatcher(parent = cw,id = -1, title="Oebs-Element Identification",filePath = browsername,socketIO = socketIO)
            elif pdfScrapeFlag==True:
                cw.scrapewindow = pdfScrapeObj.ScrapeDispatcher(parent = cw,id = -1, title="Avo Assure - PDF Scrapper",filePath = browsername,socketIO = socketIO)
                pdfScrapeFlag=False
            elif debugFlag == True:
                cw.debugwindow = clientwindow.DebugWindow(parent = cw,id = -1, title="Debugger")
                debugFlag = False
            else:
                if browsername in BROWSER_NAME:
                    logger.print_on_console('Browser Name : '+ BROWSER_NAME[browsername])
                    core_utils.get_all_the_imports('Web')
                    core_utils.get_all_the_imports('WebScrape')
                    sys.coinit_flags = 2
                    import web_scrape
                    # scrapewindow title is changed < Avo Assure - Web Scrapper > to < AvoAssure Object Identification > To <Web-Element Identification>
                    # changed  on Date:08/07/2022
                    # Author : sreenivasulu
                    cw.scrapewindow = web_scrape.ScrapeWindow(parent = cw,id = -1, title="Web-Element Identification",browser = browsername,socketIO = socketIO,action=action,data=data)
                    browsername = ''
                else:
                    import pause_display_operation
                    o = pause_display_operation.PauseAndDisplay()
                    flag,inputvalue = o.getflagandinput()
                    if flag == 'pause':
                        #call pause logic
                        cw.pausewindow = pause_display_operation.Pause(parent = None,id = -1, title="Avo Assure - Pause")
                    elif flag == 'display':
                        #call display logic
                        cw.pausewindow = pause_display_operation.Display(parent = cw,id = -1, title="Avo Assure - Display Variable",input = inputvalue)
                    elif flag == 'debug':
                        #call debug logic
                        cw.pausewindow = pause_display_operation.Debug(parent = cw,id = -1, title="Avo Assure - Debug Mode",input = inputvalue)
                    elif flag == 'error':
                        #call debug error logic
                        cw.pausewindow = pause_display_operation.Error(parent = cw,id = -1, title="Avo Assure - Debug Mode",input = inputvalue)
        except Exception as e:
            log.error(e,exc_info=True)

    def print_banner(self):
        print('********************************************************************************')
        print('================================ '+self.name+' ================================')
        print('********************************************************************************')

def get_version_via_com(filename):
    import pythoncom
    pythoncom.CoInitialize()
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version


def get_Browser_Version(browser_Name):
    try:
        path_flag=False
        paths=''
        if browser_Name == 'CHROME':
            path_flag=False
            if readconfig.configvalues['chrome_path'] == 'default':
                paths = [os.path.expandvars(r'%ProgramFiles%\\Google\\Chrome\\Application\\chrome.exe'),
                os.path.expandvars(r'%ProgramFiles(x86)%\\Google\\Chrome\\Application\\chrome.exe')]
                for p in paths:
                    if os.path.exists(p):
                        path_flag=True
                        break
            else:
                paths=[readconfig.configvalues['chrome_path']] 
                for p in paths:
                    if os.path.exists(p):
                        path_flag=True

            if path_flag == True:    
                chrome_version = list(filter(None, [get_version_via_com(p) for p in paths]))[0]
                return chrome_version
            else:
                logger.print_on_console("Chrome not found in default paths")
                log.error("Chrome not found in default paths")
                return -1
                               

        elif browser_Name == 'FIREFOX':
            path_flag=False 
            if readconfig.configvalues['firefox_path'] == 'default':
                paths = [os.path.expandvars(r'%ProgramFiles%\\Mozilla Firefox\\firefox.exe'),
                os.path.expandvars(r'%ProgramFiles(x86)%\\Mozilla Firefox\\firefox.exe')]


                for p in paths:
                    if os.path.exists(p):
                        path_flag=True
                        break
            else:
                paths=[readconfig.configvalues['firefox_path']]
                for p in paths:
                    if os.path.exists(p):
                        path_flag=True
        
            if path_flag == True:     
                firefox_version = list(filter(None, [get_version_via_com(p) for p in paths]))[0]
                return firefox_version 
            else:
                logger.print_on_console("Firefox not found in default paths") 
                log.error("Firefox not found in default paths") 
                return -1

        elif browser_Name == 'EDGE':
            path_flag=False
            paths = [os.path.expandvars(r'%ProgramFiles%\\Microsoft\\Edge\\Application\\msedge.exe'),
                os.path.expandvars(r'%ProgramFiles(x86)%\\Microsoft\\Edge\\Application\\msedge.exe')]

            for p in paths:
                if os.path.exists(p):
                    path_flag=True
                    break

            if path_flag == True:
                edge_version=list(filter(None, [get_version_via_com(p) for p in paths]))[0]
                return edge_version
            else:
                logger.print_on_console("Edge Chromium not found in default paths") 
                log.error("Edge Chromium not found in default paths") 
                return -1 

        elif browser_Name == 'IE':
            path_flag=False
            paths = [os.path.expandvars(r'%ProgramFiles%\\Internet Explorer\\iexplore.exe'),
                os.path.expandvars(r'%ProgramFiles(x86)%\Internet Explorer\\iexplore.exe')]

            for p in paths:
                if os.path.exists(p):
                    path_flag=True
                    break

            if path_flag == True:
                ie_version=list(filter(None, [get_version_via_com(p) for p in paths]))[0]
                return ie_version
            else:
                logger.print_on_console("IE not found in default paths") 
                log.error("IE not found in default paths") 
                return -1         
             
    except:
        return -1

def check_browser():
    global browsercheckFlag, browsercheck_inprogress
    browsercheck_inprogress = True
    try:
        logger.print_on_console('Browser compatibility check started')
        global chromeFlag,firefoxFlag,edgeFlag,chromiumFlag, edgeFlagComp
        try:
            if SYSTEM_OS == 'Windows':
                CHROME_VERSION=get_Browser_Version('CHROME')
                CHROMIUM_VERSION=get_Browser_Version('EDGE') 
                FIREFOX_VERSION=  get_Browser_Version('FIREFOX')
                IE_VERSION=  get_Browser_Version('IE')

            elif SYSTEM_OS == 'Darwin':
                if os.path.exists("/Applications/Google Chrome.app"):
                    CHROME_VERSION=os.popen('mdls -raw -name kMDItemVersion "/Applications/Google Chrome.app"').read()
                    if 'could not find' in CHROME_VERSION:
                        CHROME_VERSION=-1
                    else:
                        CHROME_VERSION=CHROME_VERSION.split(".")[0] 
                else:
                    CHROME_VERSION=-1  

                if os.path.exists("/Applications/Microsoft Edge.app"):
                    CHROMIUM_VERSION=os.popen('mdls -raw -name kMDItemVersion "/Applications/Microsoft Edge.app"').read()
                    if 'could not find' in CHROMIUM_VERSION:
                        CHROMIUM_VERSION=-1   
                    else:
                        CHROMIUM_VERSION=CHROMIUM_VERSION.split(".")[0] 
                else:
                    CHROMIUM_VERSION=-1    

                if os.path.exists("/Applications/Firefox.app"):
                    FIREFOX_VERSION=os.popen('mdls -raw -name kMDItemVersion "/Applications/Firefox.app"').read()
                    if 'could not find' in FIREFOX_VERSION:
                        FIREFOX_VERSION=-1
                    else:
                        FIREFOX_VERSION=FIREFOX_VERSION.split(".")[0] 
                else:
                    FIREFOX_VERSION=-1
            elif SYSTEM_OS=='Linux':
                if os.path.exists('/usr/bin/google-chrome'):
                    with os.popen('/usr/bin/google-chrome --version') as p:
                        CHROME_VERSION = p.read()
                        p.close()
                    if 'not found' in CHROME_VERSION:
                        CHROME_VERSION=-1
                    else:
                        CHROME_VERSION=CHROME_VERSION.split(".")[0].split(" ")[2]
                else:
                    CHROME_VERSION=-1
                if os.path.exists('/usr/bin/microsoft-edge'):
                    with os.popen('/usr/bin/microsoft-edge --version') as p:
                        CHROMIUM_VERSION = p.read()
                        p.close()
                    if 'not found' in CHROMIUM_VERSION:
                        CHROMIUM_VERSION=-1
                    else:
                        CHROMIUM_VERSION=CHROMIUM_VERSION.split(".")[0].split(" ")[2]
                else:
                    CHROMIUM_VERSION=-1
                if os.path.exists('/usr/bin/firefox'):
                    with os.popen('firefox --version') as p:
                        FIREFOX_VERSION=p.read()
                        p.close()
                    if 'not found' in FIREFOX_VERSION:
                        FIREFOX_VERSION=-1
                    else:
                        FIREFOX_VERSION=FIREFOX_VERSION.split(".")[0].split(" ")[2]
                else:
                    FIREFOX_VERSION=-1       
        except Exception as e:
            logger.print_on_console("Unable to locate Avo Assure Client parameters")
            log.error(e)
        #checking browser for IE
        if SYSTEM_OS == 'Windows':
            try:
                if IE_VERSION != -1:
                    try:
                        URL=readconfig.configvalues["file_server_ip"]+ "/IEDriverServer.exe"
                        if proxies:
                            fileObj = requests.get(URL,verify=False,proxies=proxies)
                            if(fileObj.status_code == 200):
                                open(normpath(DRIVERS_PATH + "/IEDriverServer.exe"), 'wb').write(fileObj.content)
                        else:
                            request.urlretrieve(URL,normpath(DRIVERS_PATH + "/IEDriverServer.exe"))
                        ieFlag = True  
                    except:
                        ieFlag = False

                    if ieFlag == False:
                        logger.print_on_console('Unable to download Internet Explorer driver from AvoAssure server')
            except Exception as e:
                logger.print_on_console("Unable to download Internet Explorer driver from AvoAssure server")
                log.error("Unable to download compatible Internet Explorer driver from AvoAssure server")
                log.error(e,exc_info=True)

        #checking browser for chrome
        if SYSTEM_OS == 'Windows':
            if CHROME_VERSION != -1:
                chromeFlag = False
                counter = 0
                if os.path.exists(CHROME_DRIVER_PATH):
                    p = subprocess.Popen('"' + CHROME_DRIVER_PATH + '" --version', stdout=subprocess.PIPE, bufsize=1, shell=True)
                    a = p.stdout.readline()
                    a = a.decode('utf-8')[13:17]
                    a=a.split('.')[0]
                    CHROME_VERSION = CHROME_VERSION.split('.')[0]
                    if str(a) == CHROME_VERSION:
                        chromeFlag = True
                while not chromeFlag and counter < 2:
                    if not os.path.exists(CHROME_DRIVER_PATH) or chromeFlag == False:
                        DRIVER_VERSION = str(int(CHROME_VERSION) - counter)
                        try:
                            URL=readconfig.configvalues["file_server_ip"]+"/chromedriver"+DRIVER_VERSION+".exe"
                            if proxies:
                                fileObj = requests.get(URL,verify=False,proxies=proxies)
                                if(fileObj.status_code == 200):
                                    open(CHROME_DRIVER_PATH, 'wb').write(fileObj.content)
                            else:
                                request.urlretrieve(URL,CHROME_DRIVER_PATH)
                            chromeFlag = True
                        except:
                            logger.print_on_console(f"Unable to download compatible chrome driver version {DRIVER_VERSION} from AvoAssure server")
                            chromeFlag = False
                        counter += 1
                    if chromeFlag == True and counter > 1:
                        logger.print_on_console(f"Using lower version {DRIVER_VERSION} of Driver for latest Chrome version {CHROME_VERSION}")   

        elif SYSTEM_OS == 'Darwin':
            if CHROME_VERSION != -1:
                chromeFlag = False
                counter = 0
                if os.path.exists(CHROME_DRIVER_PATH):
                    p = os.popen('"' + CHROME_DRIVER_PATH + '" --version')
                    a = p.read()
                    a=a.split(' ')[1].split('.')[0]
                    if str(a) == CHROME_VERSION:
                        chromeFlag = True
                while not chromeFlag and counter < 2:
                    if not os.path.exists(CHROME_DRIVER_PATH) or chromeFlag == False:
                        DRIVER_VERSION = str(int(CHROME_VERSION) - counter)
                        try:
                            URL=readconfig.configvalues["file_server_ip"]+"/Mac"+"/chromedriver"+DRIVER_VERSION
                            request.urlretrieve(URL,CHROME_DRIVER_PATH)
                            chromeFlag = True
                        except:
                            logger.print_on_console(f"Unable to download compatible chrome driver version {DRIVER_VERSION} from AvoAssure server")
                            chromeFlag = False
                        counter += 1 
                    if chromeFlag == True and counter > 1:
                        logger.print_on_console(f"Using lower version {DRIVER_VERSION} of Driver for latest Chrome version {CHROME_VERSION}")
        elif SYSTEM_OS == 'Linux':
            if CHROME_VERSION != -1:
                chromeFlag = False
                counter = 0
                if os.path.exists(CHROME_DRIVER_PATH):
                    p = os.popen('"' + CHROME_DRIVER_PATH + '" --version')
                    a = p.read()
                    a=a.split(' ')[1].split('.')[0]
                    if str(a) == CHROME_VERSION:
                        chromeFlag = True
                while not chromeFlag and counter < 2:
                    if not os.path.exists(CHROME_DRIVER_PATH) or chromeFlag == False:
                        DRIVER_VERSION = str(int(CHROME_VERSION) - counter)
                        try:
                            URL=readconfig.configvalues["file_server_ip"]+"/"+SYSTEM_OS.lower()+"/"+platform.machine().lower()+"/chromedriver"+DRIVER_VERSION
                            request.urlretrieve(URL,CHROME_DRIVER_PATH)
                            chromeFlag = True
                            os.chmod(CHROME_DRIVER_PATH,stat.S_IEXEC | os.stat(CHROME_DRIVER_PATH).st_mode)
                        except Exception as e:
                            logger.print_on_console(f"Unable to download compatible chrome driver version {DRIVER_VERSION} from AvoAssure server")
                            log.debug("Error in chrome driver download")
                            log.error(e)
                            chromeFlag = False 
                        counter += 1 
                    if chromeFlag == True and counter > 1:
                        logger.print_on_console(f"Using lower version {DRIVER_VERSION} of Driver for latest Chrome version {CHROME_VERSION}")       
        
        #checking browser for firefox
        if SYSTEM_OS == 'Windows':
            try:
                if FIREFOX_VERSION != -1:
                    try:
                        URL=readconfig.configvalues["file_server_ip"]+"/geckodriver.exe"
                        if proxies:
                            fileObj = requests.get(URL,verify=False,proxies=proxies)
                            if(fileObj.status_code == 200):
                                open(GECKODRIVER_PATH, 'wb').write(fileObj.content)
                        else:
                            request.urlretrieve(URL,GECKODRIVER_PATH)
                        firefoxFlag = True  
                    except:
                        logger.print_on_console("Unable to download compatible firefox driver from AvoAssure server")
                        firefoxFlag = False

                    if firefoxFlag == False:
                        logger.print_on_console('Unable to download compatible firefox driver from AvoAssure server')
            except Exception as e:
                logger.print_on_console("Unable to download compatible firefox driver from AvoAssure server")
                log.error("Unable to download compatible firefox driver from AvoAssure server")
                log.error(e,exc_info=True)
        elif SYSTEM_OS == 'Darwin':
            try:
                if FIREFOX_VERSION != -1:
                    try:
                        URL=readconfig.configvalues["file_server_ip"]+"/Mac"+"/geckodriver"
                        request.urlretrieve(URL,GECKODRIVER_PATH)
                        firefoxFlag = True  
                    except:
                        firefoxFlag = False

                    if firefoxFlag == False:
                        logger.print_on_console('Unable to download compatible firefox driver from AvoAssure server')
            except Exception as e:
                logger.print_on_console("Unable to download compatible firefox driver from AvoAssure server")
                log.error("Unable to download compatible firefox driver from AvoAssure server")
                log.error(e,exc_info=True)
        elif SYSTEM_OS == 'Linux':
            try:
                if FIREFOX_VERSION != -1:
                    try:
                        URL=readconfig.configvalues["file_server_ip"]+"/"+SYSTEM_OS.lower()+"/"+platform.machine().lower()+"/geckodriver"
                        request.urlretrieve(URL,GECKODRIVER_PATH)
                        os.chmod(GECKODRIVER_PATH,stat.S_IEXEC | os.stat(GECKODRIVER_PATH).st_mode)
                        firefoxFlag = True  
                    except Exception as e:
                        log.debug("Error in firefox driver check and download ")
                        log.error(e)
                        firefoxFlag = False

                    if firefoxFlag == False:
                        logger.print_on_console('Unable to download compatible firefox driver from AvoAssure server')
            except Exception as e:
                logger.print_on_console("Unable to download compatible firefox driver from AvoAssure server")
                log.error("Unable to download compatible firefox driver from AvoAssure server")
                log.error(e,exc_info=True)

        #Checking browser for microsoft edge
        try:
            enable_edge_check = str(os.getenv('__ICE_ALLOW_EDGE_LEGACY', False)).lower() != 'false'
            if not enable_edge_check:
                logger.print_on_console("WARNING!! : MS Edge Legacy is not supported")
            elif('Windows-10' in platform.platform()):
                import psutil
                edgeFlagComp = "MicrosoftEdge.exe" not in [p.name() for p in psutil.process_iter()]
                if edgeFlagComp:
                    #from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
                    p = subprocess.Popen('"' + EDGE_DRIVER_PATH + '" --version', stdout=subprocess.PIPE, bufsize=1,cwd=DRIVERS_PATH,shell=True)
                    a = p.stdout.readline()
                    a = a.decode('utf-8')[28:40]
                    driver = webdriver.Edge(executable_path=EDGE_DRIVER_PATH)
                    browser_ver = driver.capabilities['browserVersion']
                    browser_ver1 = browser_ver.encode('utf-8')
                    browser_ver = float(browser_ver1[:8])
                    try:
                        driver.close()
                        driver.quit()
                    except:
                        pass
                    for k,v in list(EDGE_VERSION.items()):
                        if a == k:
                            if str(browser_ver) >= v[0] or str(browser_ver) <= v[1]:
                                edgeFlag = True
                    if edgeFlag == False:
                        logger.print_on_console('WARNING!! : MS Edge Legacy version ',str(browser_ver),' is not supported.')
                else:
                    logger.print_on_console("WARNING!! : To perform MS Edge Legacy check, all instances of MS Edge legacy should be closed. Close the instances and restart Avo Assure Client again")
            else:
                logger.print_on_console("WARNING!! : MS Edge Legacy is supported only in Windows10 platform")
        except Exception as e:
            logger.print_on_console("Error in checking Edge Legacy version")
            log.error("Error in checking Edge Legacy version")
            log.error(e,exc_info=True)

        #checking browser for microsoft edge(chromium based)
        # try:
        if SYSTEM_OS == 'Windows':
            if CHROMIUM_VERSION != -1:
                chromiumFlag = False
                counter = 0
                if os.path.exists(EDGE_CHROMIUM_DRIVER_PATH):
                    p = subprocess.Popen('"' + EDGE_CHROMIUM_DRIVER_PATH + '" --version', stdout=subprocess.PIPE, bufsize=1,cwd=DRIVERS_PATH,shell=True)
                    a = p.stdout.readline()
                    a = a.decode('utf-8').split(' ')
                    if len(a) == 5:
                        a = a[3]
                    else:
                        a = a[1]    
                    a=a.split('.')[0]
                    CHROMIUM_VERSION = CHROMIUM_VERSION.split('.')[0]
                    if str(a) == CHROMIUM_VERSION:
                        chromiumFlag = True
                while not chromiumFlag and counter < 2:
                    if not os.path.exists(EDGE_CHROMIUM_DRIVER_PATH) or chromiumFlag == False:
                        DRIVER_VERSION = str(int(CHROMIUM_VERSION) - counter)
                        try:
                            URL=readconfig.configvalues["file_server_ip"]+"/msedgedriver"+DRIVER_VERSION+".exe"
                            if proxies:
                                fileObj = requests.get(URL,verify=False,proxies=proxies)
                                if(fileObj.status_code == 200):
                                    open(EDGE_CHROMIUM_DRIVER_PATH, 'wb').write(fileObj.content)
                            else:
                                request.urlretrieve(URL,EDGE_CHROMIUM_DRIVER_PATH)
                            chromiumFlag = True
                        except:
                            logger.print_on_console(f"Unable to download compatible Edge Chromium driver {DRIVER_VERSION} from AvoAssure server")
                            chromiumFlag = False
                        counter += 1
                    if chromiumFlag == True and counter > 1:
                        logger.print_on_console(f"Using lower version {DRIVER_VERSION} of Driver for latest Edge version {CHROMIUM_VERSION.split('.')[0]}")      
        elif SYSTEM_OS == 'Darwin':
            if CHROMIUM_VERSION != -1:
                chromiumFlag = False
                counter = 0
                # if os.path.exists(EDGE_CHROMIUM_DRIVER_PATH):
                #     p = os.popen('"' + EDGE_CHROMIUM_DRIVER_PATH + '" --version')
                #     a = p.read()
                #     a=a.split(' ')[1].split('.')[0]
                #     if str(a) == CHROMIUM_VERSION:
                #         chromiumFlag = True
                while not chromiumFlag and counter < 2:
                    if not os.path.exists(EDGE_CHROMIUM_DRIVER_PATH) or chromiumFlag == False:
                        DRIVER_VERSION = str(int(CHROMIUM_VERSION) - counter)
                        try:
                            URL=readconfig.configvalues["file_server_ip"]+"/Mac"+"/msedgedriver"+DRIVER_VERSION
                            request.urlretrieve(URL,EDGE_CHROMIUM_DRIVER_PATH)
                            chromiumFlag = True
                        except:
                            logger.print_on_console(f"Unable to download compatible Edge Chromium driver {DRIVER_VERSION} from AvoAssure server")
                            chromiumFlag = False
                        counter += 1
                    if chromiumFlag == True and counter > 1:
                        logger.print_on_console(f"Using lower version {DRIVER_VERSION} of Driver for latest Edge version {CHROMIUM_VERSION}")
        elif SYSTEM_OS == 'Linux':
            if CHROMIUM_VERSION != -1:
                chromiumFlag = False
                counter = 0
                if os.path.exists(EDGE_CHROMIUM_DRIVER_PATH):
                    p = os.popen('"' + EDGE_CHROMIUM_DRIVER_PATH + '" --version')
                    a = p.read()
                    a=a.split(' ')[3].split('.')[0]
                    if str(a) == CHROMIUM_VERSION:
                        chromiumFlag = True
                while not chromiumFlag and counter < 2:
                    if not os.path.exists(EDGE_CHROMIUM_DRIVER_PATH) or chromiumFlag == False:
                        DRIVER_VERSION = str(int(CHROMIUM_VERSION) - counter)
                        try:
                            URL=readconfig.configvalues["file_server_ip"]+"/"+SYSTEM_OS.lower()+"/"+platform.machine().lower()+"/msedgedriver"+DRIVER_VERSION
                            request.urlretrieve(URL,EDGE_CHROMIUM_DRIVER_PATH)
                            chromiumFlag = True
                            os.chmod(EDGE_CHROMIUM_DRIVER_PATH,stat.S_IEXEC | os.stat(EDGE_CHROMIUM_DRIVER_PATH).st_mode)
                        except Exception as e:
                            logger.print_on_console(f"Unable to download compatible Edge Chromium driver {DRIVER_VERSION} from AvoAssure server")
                            log.debug("Error in edge-chromium driver download")
                            log.error(e)
                            chromiumFlag = False
                        counter += 1
                    if chromiumFlag == True and counter > 1:
                        logger.print_on_console(f"Using lower version {DRIVER_VERSION} of Driver for latest Edge version {CHROMIUM_VERSION}")

        if chromeFlag == True and firefoxFlag == True and edgeFlag == True and chromiumFlag == True:
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
        browsercheck_inprogress = False
    return browsercheckFlag  

def wait_until_browsercheck():
    if browsercheck_inprogress:
        info_msg = "Waiting until Browser Compatibility check is completed"
        logger.print_on_console(info_msg)
        log.info(info_msg)
    while True:
        if browsercheck_inprogress: time.sleep(1)
        else: break

def check_PatchUpdate():
    try:
        global patchcheckFlag
        import update_module
        flag = True
        data = None
        SERVER_LOC = "https://" + str(configvalues['server_ip']) + ':' + str(configvalues['server_port']) + '/patchupdate/'
        req_kw_args = ConnectionThread(None).get_ice_session(no_params=True)
        req_kw_args.pop('assert_hostname', None)

        manifest_req = requests.get(SERVER_LOC+'/manifest.json', **req_kw_args)
        if(manifest_req.status_code == 200):
            data = json.loads(manifest_req.text)

        def update_updater_module(data):
            global update_obj
            update_obj = update_module.Update_Rollback()
            update_obj.update(data, MANIFEST_LOC, SERVER_LOC, AVO_ASSURE_HOME, LOC_7Z, UPDATER_LOC, 'UPDATE')

        if data:
            update_updater_module(data)
            UPDATE_MSG=update_obj.send_update_message()
            l_ver = update_obj.fetch_current_value()
            SERVER_CHECK_MSG = update_obj.server_check_message()
            if (SERVER_CHECK_MSG):log.info(SERVER_CHECK_MSG)
            #check if update avaliable
            if ( UPDATE_MSG == 'Update Available!!! Click on update' and flag == True ):
                logger.print_on_console("An update is available. Click on 'Help' menu option -> 'Check for Updates' sub-menu option -> 'Update' button")
                logger.print_on_console('The latest Avo Assure Client version : ',l_ver)
                log.info(UPDATE_MSG)
            elif ( UPDATE_MSG == 'You are running the latest version of Avo Assure Client' and flag == True ):
                logger.print_on_console( "No updates available" )
                log.info( "No updates available" )
            elif ( UPDATE_MSG == 'An Error has occured while checking for new versions of Avo Assure Client, kindly contact Support Team'):
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
            patchcheckFlag = True
        else:
            err = "Error while checking for manifest.json"
            logger.print_on_console(err)
            log.debug(err)
            patchcheckFlag = False
    except Exception as e:
        err = "Error while checking for patch update"
        logger.print_on_console(err)
        log.debug(err)
        log.debug(e)
        patchcheckFlag = False
    finally:
        logger.print_on_console('Check for client patch update completed')
    return patchcheckFlag

def check_execution_lic(event):
    if executionOnly:
        msg='Execution only allowed'
        log.info(msg)
        logger.print_on_console(msg)
        socketIO.emit(event,'ExecutionOnlyAllowed')
    return executionOnly

def set_ICE_status(one_time_ping = False,connect=True,interval = 60000):
    """
    def : set_ICE_status
    purpose : communicates Avo Assure Client status (availble/busy)
    param : status (bool)
    return : Timer

    """
    global socketIO,root,execution_flag,cw,status_ping_thread, termination_inprogress
    if not one_time_ping and socketIO is not None:
        if status_ping_thread and status_ping_thread.is_alive():
            status_ping_thread.cancel()
            status_ping_thread = None
        status_ping_thread = threading.Timer(int(interval)/2000, set_ICE_status,[])
        status_ping_thread.setName("Status Ping")
        status_ping_thread.start()
    log.debug('Ping Server')
    # Add Avo Assure Client identification and status, which is busy by default
    if SYSTEM_OS=='Darwin':
        result = {"hostip":socket.gethostname(),"time":str(datetime.utcnow()),"connected":connect}
    else:
        result = {"hostip":socket.gethostbyname(socket.gethostname()),"time":str(datetime.utcnow()),"connected":connect}
    result['status'] = execution_flag or termination_inprogress
    if cw is not None:
        result['mode'] = cw.schedule.GetValue()
    else:
        result['mode'] = False
    result["host"] = readconfig.configvalues['server_ip']
    token_obj = ICEToken()
    ice_token = None
    if token_obj.token:
        ice_token = token_obj.token
        result["icename"] = ice_token["icename"]
    else:
        result["icename"] = socket.gethostname()
    if socketIO is not None:
        socketIO.emit('ICE_status_change',result)

def stop_ping_thread():
    global status_ping_thread
    if status_ping_thread is not None and status_ping_thread.is_alive():
        status_ping_thread.cancel()
        time.sleep(0.5)
        status_ping_thread = None

def cicd_integration_obj(*args):
    global cw, execution_flag, qcObject, qtestObject, zephyrObject, azureObject, execReq
    try:
        log.debug("Inside cicd_integration_obj")
        exec_data = args[0]
        batch_id = exec_data["batchId"]
        execReq = exec_data
        if("integration" in exec_data):
            if("alm" in exec_data["integration"] and exec_data["integration"]["alm"]["url"] != ""):
                if(qcObject == None):
                    core_utils.get_all_the_imports('Qc')
                    import QcController
                    qcObject = QcController.QcWindow()
            if("qtest" in exec_data["integration"] and exec_data["integration"]["qtest"]["url"] != ""):
                if(qtestObject == None):
                    core_utils.get_all_the_imports('QTest')
                    import QTestController
                    qtestObject = QTestController.QTestWindow()
            if("zephyr" in exec_data["integration"] and exec_data["integration"]["zephyr"]["url"] != ""):
                if(zephyrObject == None):
                    core_utils.get_all_the_imports('Zephyr')
                    import ZephyrController
                    zephyrObject = ZephyrController.ZephyrWindow()
            if("azure" in exec_data["integration"] and exec_data["integration"]["azure"]["url"] != ""):
                if(azureObject == None):
                    core_utils.get_all_the_imports('Azure')
                    import azurecontroller
                    azureObject = azurecontroller.AzureWindow()
    except Exception as e:
        log.error(e, exc_info=True)