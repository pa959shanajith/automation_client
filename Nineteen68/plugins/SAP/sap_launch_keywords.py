#-------------------------------------------------------------------------------
# Name:        SAP_Launch Keywords
# Purpose:     Contains SAP generic Keywords
#
# Author:      anas.ahmed1,kavyasree
#
# Created:     7-04-2017
# Copyright:   (c) anas.ahmed1 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import win32gui
import win32process
import win32api
import logger
import os
import sap_constants
import time
from PIL import ImageGrab
from constants import *
from saputil_operations import SapUtilKeywords
from pywinauto.application import Application
from pywinauto import keyboard
from pywinauto.findwindows import find_window
from pywinauto.win32functions import SetForegroundWindow
import win32com.client
import pywinauto
import logging
import logging.config
log = logging.getLogger('sap_launch_keywords.py')
from sap_scraping import Scrape

class Launch_Keywords():

    def __init__(self):
        self.uk = SapUtilKeywords()
        self.windowname=''
        self.filePath=''

    def getSession(self,*args):
        try:
            time.sleep(2)
            try:
                SapGui=self.uk.getSapObject()
            except Exception as e:
                logger.print_on_console('No instance open of SAP GUI')
            scrapingObj=Scrape()
            wnd = scrapingObj.getWindow(SapGui)
            wndId =  wnd.__getattr__('id')
            i = wndId.index('wnd')
            wndNumber = wndId[i+4]
            j = wndId.index('ses')
            sesId = wndId[j:j+6]
            ses = SapGui.FindByid(str(sesId))
            return ses
        except Exception as e:
            logger.print_on_console('No instance open of SAP GUI')

    def getSessWindow(self,*args):
        try:
            time.sleep(2)
            SapGui=self.uk.getSapObject()
            scrapingObj=Scrape()
            wnd = scrapingObj.getWindow(SapGui)
            wndId =  wnd.__getattr__('id')
            i = wndId.index('wnd')
            wndNumber = wndId[i+4]
            j = wndId.index('ses')
            sesId = wndId[j:j+6]
            ses = SapGui.FindByid(str(sesId))
            return ses,wnd
        except Exception as e:
            logger.print_on_console('No instance open of SAP GUI')

    def getErrorMessage(self,*args):
        time.sleep(2)
        ses,wnd=self.getSessWindow()
        wndId =  wnd.__getattr__('id')
        sbarId = wndId + '/sbar'
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            sbar = ses.FindById(sbarId)
            value = sbar.FindByName("pane[0]", "GuiStatusPane").text
            if value=='' or value==None:
                err_msg='No error message'
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg='Failed to get error message'
            log.error(e)
            logger.print_on_console("Error occured in getErrorMessage")
        return status,result,value,err_msg


    def startTransaction(self,input_val,*args):
        ses=self.getSession()
        tcode=input_val[0]
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            ses.StartTransaction(tcode)
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg='Failed to start transaction'
            log.error(e)
            logger.print_on_console("Error occured in startTransaction")
        return status,result,value,err_msg

    def toolbar_actions(self,input_val,*args):
        """ Enter, Save, Back, Exit, Cancel, Log off, Print, Find, Find next, First Page, Previous Page, Next Page, Last Page, Creates new session,Generates shortcut, Help, Customize Local Layout """
        """ All of the above commands are case insensitive. """
        button = input_val[0]
        ses,wnd=self.getSessWindow()
        wndId =  wnd.__getattr__('id')
        tbar_action = wndId +'/tbar[0]'
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        tbar = ses.FindById(tbar_action) #get the window id from getSessWindow and append /tbar[0]
        i = 0
        while True:
            try:
                tooltip = tbar.Children(i).tooltip.split("(")[0]
                if(tooltip.strip().lower() == button.strip().lower()):
                    id = tbar.Children(i).Id
                    btn = ses.FindById(id)
                    if(btn.Changeable == True):
                        if(button.strip().lower() == "creates new session"):
                            shell = win32com.client.Dispatch("WScript.Shell")
                            shell.AppActivate(wnd.Text)
                            shell.SendKeys("^{+}")
                        elif(button.strip().lower() == "generates shortcut"):
                            shell = win32com.client.Dispatch("WScript.Shell")
                            shell.AppActivate(wnd.Text)
                            shell.SendKeys("^{;}")
                        elif(button.strip().lower() == "customize local layout"):
                            shell = win32com.client.Dispatch("WScript.Shell")
                            shell.AppActivate(wnd.Text)
                            shell.SendKeys("%{F12}")
                        else:
                            btn.Press()
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
                    else:
                        logger.print_on_console("Button is disabled")
                        err_msg='Button is disabled'
                    break
            except Exception as e:
                log.error(e)
                logger.print_on_console("Could not find the specified button")
                err_msg='Could not find the specified button'
                break
            i = i + 1
        return status,result,value,err_msg

    def launch_application(self,input_val,*args):
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        term = None
        try:
        # check file exists
            if len(input_val)==2:
                self.filePath,self.windowName=input_val[0],input_val[1]
                timeout=5
            start_window=0
            try:
             start_window = pywinauto.findwindows.find_window(title=self.windowName)
            except Exception as e:
                  log.error(e)
                  logger.print_on_console("Could not find specified window name")
            if start_window==0:
                logger.print_on_console('Starting new SAP window')
                try:
                    app = Application(backend="win32").start(self.filePath).window(title=self.windowName)
                    logger.print_on_console('connecting to  new SAP window')
                    time.sleep(4)
                    logger.print_on_console('The specified application is launched Successfully')
                except:
                    logger.print_on_console('Incorrect file path or window name')
                    term = TERMINATE

                if app!=None and app!='':
                    status=sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('The given window name is not found')
                    term = TERMINATE
            elif start_window>1:
                SetForegroundWindow(find_window(title=self.windowName))
                logger.print_on_console('SAP Logon window already exists will proceed further')
                err_msg='SAP Logon window already exists'
                status=sap_constants.TEST_RESULT_PASS
                result = sap_constants.TEST_RESULT_TRUE
                # made changes : launch will not terminate if window already exists
            else:
                error_code=int(win32api.GetLastError())
                if error_code in sap_constants.SAP_ERROR_CODES.keys():
                    logger.print_on_console(sap_constants.SAP_ERROR_CODES.get(error_code))
                else:
                    logger.print_on_console('unable to launch the application')
                term =TERMINATE
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured in launchApplication")
            err_msg = sap_constants.ERROR_MSG
            term =TERMINATE
        if term!=None:
            return term
        return status,result,self.windowname,err_msg

    def serverConnect(self,input_val,*args):
        server=input_val[0]
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        term = None
        app = None
        start_window=0
        try:
            start_window = pywinauto.findwindows.find_window(title=self.windowName)
            if(start_window>1):
                try:
                    app = Application(backend="win32").connect(path =self.filePath).window(title=self.windowName)
                    SetForegroundWindow(find_window(title=self.windowName))
                    try:
                        editEle = app.Edit
                        edit2Ele = app.Edit2
                        editExists = editEle.exists()
                        edit2Exists = edit2Ele.exists()
                        if(editExists and edit2Exists):
                            ele = (edit2Ele if(editEle.Rectangle().top > edit2Ele.Rectangle().top) else editEle)
                        elif(editExists):
                            ele = editEle
                        elif(edit2Exists):
                            ele = edit2Ele
                        ele.set_edit_text(u'')
                        ele.type_keys(server, with_spaces = True)
                        if (app['Log &OnButton'].exists() and app['Log &OnButton'].is_enabled()):
                            app['Log &OnButton'].click()
                        elif (app['Log &On'].exists() and app['Log &On'].is_enabled()):
                            app['Log &OnButton'].click()
                        elif (app.Button.exists() and app.Button.is_enabled()):
                            app.Button.click()
                    except Exception as e:
                        log.error(e)
                        logger.print_on_console("Unable to Find LogOn Button or Filter Text Box")
                        err_msg = "Unable to Find LogOn Button or Filter Text Box"
                        return status, result, verb, err_msg
                    time.sleep(5)
                    if app!=None and app!='':
                        try:
                            SapGui=self.uk.getSapObject()
                            SapGui.Children(0).Children(0)
                            logger.print_on_console('Connected to SAP')
                            status=sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                        except:
                            logger.print_on_console('Given Server description is incorrect')
                            err_msg='Given Server discription is incorrect'
                            term = TERMINATE
                    else:
                        logger.print_on_console('The given window name is not found')
                        err_msg='Not connected to SAP Logon , window not found'
                        term = TERMINATE
                except:
                    logger.print_on_console('SAP Logon window does not exist')
                    err_msg='SAP Logon window does not exist'
                    term = TERMINATE
            elif start_window==0:
                logger.print_on_console('SAP Logon window does not exist')
                term = TERMINATE
        except Exception as e:
            log.error(e)
            logger.print_on_console("Could not find specified window name")
        return status,result,verb,err_msg


    def getPageTitle(self,*args):
        ses=self.getSession()
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        try:
            value = ses.ActiveWindow.Text
            status=sap_constants.TEST_RESULT_PASS
            result = sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console('Error occured in getPageTitle')
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg

    def getPopUpText(self, *args):
        ses, wnd = self.getSessWindow()
        wnd_title = wnd.Text
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        value=OUTPUT_CONSTANT
        from sap_scraping import Scrape
        scrapingObj=Scrape()
        data = scrapingObj.full_scrape(wnd, wnd_title)
        try:
            for elem in data:
                if elem['tag'] == "input":
                    if(elem['text'] != ""):
                        value = elem['text']
                        break
            status=sap_constants.TEST_RESULT_PASS
            result = sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console('Error occured in getPopupText')
            err_msg = sap_constants.ERROR_MSG
        return status,result,value,err_msg

    def closeApplication(self, *args):
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            try:
                SapGui=self.uk.getSapObject()
            except Exception as e:
                logger.print_on_console("error1  ",e)
            i, j = 0, 0
            connections = []
            while True:
                try:
                    connections.append(SapGui.Children(i))
                except Exception as e:
                    break
                i = i + 1
            for con in connections:
                j = 0
                while True:
                    try:
                        ses = con.Children(j)
                        id = ses.__getattr__("Id")
                        con.CloseSession(id)
                    except Exception as e:
                        logger.print_on_console("The specified application is closed Successfully ")
                        break
                    j = j + 1
            try:
                time.sleep(2)
                app = Application(backend="win32").connect(path = self.filePath).window(title=self.windowName)
                time.sleep(2)
                app.Close()
            except:
                try:
                     time.sleep(2)
                     app = Application(backend="win32").connect(path = r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe").window(title="SAP Logon 740")
                     time.sleep(2)
                     app.Close()
                except:
                     os.system("TASKKILL /F /IM saplogon.exe")
                     #logger.print_on_console("SAP Logon 740 has is not able to close,please close manually.")
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console('Error occured in closeApplication')
            err_msg = sap_constants.ERROR_MSG
        return status,result,verb,err_msg

    def captureScreenshot(self,screen_name,screen_id):

        """
        name: captureScreenshot
        purpose: To capture screenshot of the scraped window
        parameters: List of scraped elements
        returns: Nothing
        """
        img = None
        if("wnd[0]" not in screen_id):
            try:
                ses = self.getSession()
                i = screen_id.index("wnd")
                screen_id = screen_id[:i+4] + "0" + screen_id[i+5:]
                screen_name = ses.FindById(screen_id).Text
            except Exception as e:
                log.error(e)
        try:
            handle = win32gui.FindWindow(None, screen_name)
            bbox = win32gui.GetWindowRect(handle)
            img = ImageGrab.grab(bbox)
            #win32gui.SetForegroundWindow(handle)
##            foreThread = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
##            appThread = win32api.GetCurrentThreadId()
##            if( foreThread != appThread ):
##                win32process.AttachThreadInput(foreThread[0], appThread, True)
##                win32gui.BringWindowToTop(handle)
##                win32gui.ShowWindow(handle,3)
##                win32process.AttachThreadInput(foreThread[0], appThread, False)
##            else:
##                win32gui.BringWindowToTop(handle)
##                win32gui.ShowWindow(handle,3)
##            time.sleep(2)

        except Exception as e:
            log.error(e)
            logger.print_on_console("Error has occured while capturing screenshot")
        #img.save(r'.\screenshot.png')
        return img

    def setWindowToForeground(self,sap_id):
        try:
            i=sap_id.index("/")
            wndNAME=sap_id[:i]
            handle = win32gui.FindWindow(None, wndNAME)
            foreground_handle = win32gui.GetForegroundWindow()
            if(handle != foreground_handle):
                foreThread = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                appThread = win32api.GetCurrentThreadId()
                if( foreThread != appThread ):
                    win32process.AttachThreadInput(foreThread[0], appThread, True)
                    win32gui.BringWindowToTop(handle)
                    win32gui.ShowWindow(handle,5)
                    win32process.AttachThreadInput(foreThread[0], appThread, False)
                else:
                    win32gui.BringWindowToTop(handle)
                    win32gui.ShowWindow(handle,5)
        except Exception as e:
            log.error(e)