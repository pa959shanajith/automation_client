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
log = logging.getLogger('sap_launch_keywords.py')
from sap_scraping import Scrape

class Launch_Keywords():

    def __init__(self):
        self.uk = SapUtilKeywords()
        self.windowname = ''
        self.filePath = ''

    def getSession(self, *args):
        ses = None
        try:
            #time.sleep(2)
            try:
                SapGui = self.uk.getSapObject()
            except Exception as e:
                log.error( sap_constants.NO_INSTANCE_OPEN_ERROR+ ' : ' + str(e) )
                logger.print_on_console( sap_constants.NO_INSTANCE_OPEN_ERROR  )
            scrapingObj = Scrape()
            wnd = scrapingObj.getWindow(SapGui)
            wndId =  wnd.__getattr__('id')
            i = wndId.index('wnd')
            wndNumber = wndId[i+4]
            j = wndId.index('ses')
            sesId = wndId[j:j+6]
            ses = SapGui.FindByid(str(sesId))
        except Exception as e:
            log.error( sap_constants.NO_INSTANCE_OPEN_ERROR + ' : ' + str(e) )
            logger.print_on_console( sap_constants.NO_INSTANCE_OPEN_ERROR )
        return ses

    def getSessWindow(self, *args):
        ses, wnd = None, None
        try:
            SapGui = self.uk.getSapObject()
            scrapingObj = Scrape()
            wnd = scrapingObj.getWindow(SapGui)
            latest_conn = list(SapGui.children)[-1] #getting latest connection
            ses = list(latest_conn.children)[-1] #getting lastest session
        except Exception as e:
            log.error( sap_constants.NO_INSTANCE_OPEN_ERROR, e )
            logger.print_on_console( sap_constants.NO_INSTANCE_OPEN_ERROR )
        return ses, wnd

    def close_window(self, *args):
        """Closes the Main/Dialog Window"""
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg  = None
        value = OUTPUT_CONSTANT
        try:
            ses, wnd = self.getSessWindow()
            if ( ses and wnd ):
                wndId =  wnd.__getattr__('id')
                if( ses.FindById(wndId).type == "GuiModalWindow" or "GuiMainWindow" ):
                    ses.FindById(wndId).Close()
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Element is not GuiModalWindow or GuiMainWindow type'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in Close Window" )
        return status, result, value, err_msg


    def maximize_window(self, *args):
        """Maximizes the Main/Dialog Window"""
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg  = None
        value = OUTPUT_CONSTANT
        try:
            ses, wnd = self.getSessWindow()
            if ( ses and wnd ):
                wndId =  wnd.__getattr__('id')
                if( ses.FindById(wndId).type == "GuiModalWindow" or "GuiMainWindow"):
                    ses.FindById(wndId).Maximize()
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Element is not GuiModalWindow or GuiMainWindow type'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in Maximize Window" )
        return status, result, value, err_msg

    def minimize_window(self, *args):
        """Minimizes the SAP Main/Dialog Window"""
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg  = None
        value = OUTPUT_CONSTANT
        try:
            ses, wnd = self.getSessWindow()
            if ( ses and wnd ):
                wndId =  wnd.__getattr__('id')
                if( ses.FindById(wndId).type == "GuiModalWindow" or "GuiMainWindow" ):
                    ses.FindById(wndId).Iconify()
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Element is not GuiModalWindow or GuiMainWindow type'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in Minimize Window" )
        return status, result, value, err_msg

    def restore_window(self, *args):
        """Restores the Main/Dialog Window"""
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg  = None
        value = OUTPUT_CONSTANT
        try:
            ses, wnd = self.getSessWindow()
            if ( ses and wnd ):
                wndId =  wnd.__getattr__('id')
                if( ses.FindById(wndId).type == "GuiModalWindow" or "GuiMainWindow"):
                    ses.FindById(wndId).Restore()
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Element is not GuiModalWindow or GuiMainWindow type'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in Restore Window" )
        return status, result, value, err_msg

    def getWindowName(self, *args):
        """Retrives popup-dialog/window text"""
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg  = None
        value = OUTPUT_CONSTANT
        try:
            ses, wnd = self.getSessWindow()
            if ( ses and wnd ):
                wndId =  wnd.__getattr__('id')
                if( ses.FindById(wndId).type == "GuiModalWindow" ):
                    value = ses.FindById(wndId).PopupDialogText
                    if not(value):
                        value = ses.FindById(wndId).Text
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Element is not GuiModalWindow type'
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in Get Window Name" )
        return status, result, value, err_msg
    def getStatusBarMessage(self, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            ses, wnd = self.getSessWindow()
            if ( ses and wnd ):
                wndId =  wnd.__getattr__('id')
                sbarId = wndId + '/sbar'
                sbar = ses.FindById(sbarId)
                value = sbar.FindByName("pane[0]", "GuiStatusPane").text
                if ( value == '' or value == None ):
                    err_msg = "No message displayed in status bar"
                else:
                    msgdict = {'S':'Success','W':'Warning','E':'Error','A':'Abort','I':'Information'}#msgdict is a dictionary containing sbar message types, map appropriate value to given key
                    if ( str(sbar.MessageType) in msgdict ):
                        value = msgdict[str(sbar.MessageType)] +' : '+ value
                    else:
                        log.info( 'Unable to map message type' )
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.SESSION_AND_WINDOW_ERROR
            #-----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in getStatusBarMessage" )
        return status, result, value, err_msg

    def doubleClickStatusBar(self, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            ses, wnd = self.getSessWindow()
            if ( ses and wnd ):
                wndId =  wnd.__getattr__('id')
                sbarId = wndId + '/sbar'
                if ( ses.FindById(sbarId).FindByName("pane[0]", "GuiStatusPane").text != '' or None ):
                    ses.FindById(sbarId).DoubleClick()
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = "No message, unable to perform DoubleClick on status bar"
            else:
                err_msg = sap_constants.SESSION_AND_WINDOW_ERROR
            #-----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console ( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in doubleClickStatusBar" )
        return status, result, value, err_msg

    def startTransaction(self, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            ses = self.getSession()
            if ( ses ):
                tcode = input_val[0]
                ses.StartTransaction(tcode)
                status = sap_constants.TEST_RESULT_PASS
                result = sap_constants.TEST_RESULT_TRUE
            else:
                err_msg = sap_constants.SESSION_ERROR
            #-----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console ( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in Start Transaction" )
        return status, result, value, err_msg

    def toolbar_actions(self, input_val, *args):
        """ Enter, Save, Back, Exit, Cancel, Log off, Print, Find, Find next, First Page, Previous Page, Next Page, Last Page, Creates new session,Generates shortcut, Help, Customize Local Layout """
        """ All of the above commands are case insensitive. """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            ses, wnd = self.getSessWindow()
            if ( ses and wnd ):
                wndId =  wnd.__getattr__('id')
                tbar_action = wndId +'/tbar[0]'
                tbar = ses.FindById(tbar_action) #get the window id from getSessWindow and append /tbar[0]
                i = 0
                while True:
                    try:
                        tooltip = tbar.Children(i).tooltip.split("(")[0]
                        if ( tooltip.strip().lower() == input_val[0].strip().lower() ):
                            id = tbar.Children(i).Id
                            btn = ses.FindById(id)
                            if ( btn.Changeable == True):
                                if( input_val[0].strip().lower() == "creates new session" ):
                                    shell = win32com.client.Dispatch("WScript.Shell")
                                    shell.AppActivate(wnd.Text)
                                    shell.SendKeys("^{+}")
                                elif ( input_val[0].strip().lower() == "generates shortcut" ):
                                    shell = win32com.client.Dispatch("WScript.Shell")
                                    shell.AppActivate(wnd.Text)
                                    shell.SendKeys("^{;}")
                                elif ( input_val[0].strip().lower() == "customize local layout" ):
                                    shell = win32com.client.Dispatch("WScript.Shell")
                                    shell.AppActivate(wnd.Text)
                                    shell.SendKeys("%{F12}")
                                else:
                                    btn.Press()
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            else:
                                err_msg = 'Button is disabled'
                            break
                    except Exception as e:
                        log.error( e )
                        err_msg = 'Could not find the specified button'
                        break
                    i = i + 1
            else:
                err_msg = sap_constants.SESSION_AND_WINDOW_ERROR
            #-----------------------------------logging
            if ( err_msg ):
                log.info( err_msg)
                logger.print_on_console ( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in ToolbarActions" )
        return status,result,value,err_msg

    def selectMenu(self, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        flag=False
        try:
            ses, wnd = self.getSessWindow()
            if ( ses and wnd ):
                wndId =  wnd.__getattr__('id')
                mbar_action = wndId +'/mbar'
                mbar = ses.FindById(mbar_action) #get the window id from getSessWindow and append /mbar
                global index,flag1,flag2
                index = 0
                flag1 = flag2 =  False
                def menuSelector(fobj):
                    global index,flag1,flag2
                    try:
                        for i in list(fobj.Children):
                            if( i.Name != input_val[index] ):
                                flag1 = False
                            elif( i.Name == input_val[index] ):
                                log.debug("Selecting menu item : ",i.Name)
                                i.Select()
                                flag1 = True
                                index = index + 1
                                if ( index < len(input_val) ):
                                    menuSelector(i)
                                else:
                                    flag2 = True
                                    break
                            if( flag2 ):
                                break
                    except Exception as e:
                        err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
                menuSelector(mbar)
                if ( flag1 == True and flag2 == True ):
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                elif( flag1 != False or flag2 == False ):
                    err_msg = "Unable to find the menu item"
            else:
                err_msg = sap_constants.SESSION_AND_WINDOW_ERROR
            #-----------------------------------logging
            if ( err_msg ):
                log.info( err_msg)
                logger.print_on_console ( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in SelectMenu" )
        return status,result,value,err_msg

    def launch_application(self, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        term = None
        try:
        # check file exists
            if ( len(input_val) == 2 ):
                self.filePath,self.windowName=input_val[0],input_val[1]
            start_window = 0
            try:
             start_window = pywinauto.findwindows.find_window(title=self.windowName)
            except Exception as e:
                log.debug( "Could not find specified window name" )
                log.info( e )
            if ( start_window == 0 ):
                log.debug( 'Starting new SAP window' )
                try:
                    app = Application(backend="win32").start(self.filePath).window(title=self.windowName)
                    log.debug( 'Launching new SAP window' )
                    time.sleep(4)
                    log.debug( 'The specified application is launched Successfully' )
                except:
                    err_msg = 'Incorrect file path or window name'
                    term = TERMINATE
                try:#To check if input Window name is correct
                    app = None
                    log.debug( 'Connecting to specified SAP window' )
                    win = pywinauto.findwindows.find_window(title=self.windowName)
                    app = Application(backend = "win32").connect(path = self.filePath).window(title = self.windowName)
                    log.debug( 'Connected to specified SAP window' )
                except:
                    log.debug( 'Specified SAP Logon window name is incorrect' )
                if ( app ):
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'The given window name is not found'
                    term = TERMINATE
            elif ( start_window > 1 ):
                SetForegroundWindow(find_window(title=self.windowName))
                logger.print_on_console( 'SAP Logon window already exists will proceed further' )
                log.debug( 'SAP Logon window already exists' )
                status = sap_constants.TEST_RESULT_PASS
                result = sap_constants.TEST_RESULT_TRUE
                # made changes : launch will not terminate if window already exists
            else:
                error_code = int(win32api.GetLastError())
                if ( error_code in list(sap_constants.SAP_ERROR_CODES.keys()) ):
                    err_msg = sap_constants.ERROR_MSG + ' : ' + sap_constants.SAP_ERROR_CODES.get(error_code)
                else:
                    err_msg = 'Unable to launch SAP application'
                term = TERMINATE
            #----------------------------------logging
            if ( err_msg ):
                log.error( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occurred in Launch Application" )
            term = TERMINATE
        if ( term  ):
            return term
        return status, result, value, err_msg

    def serverConnect(self, input_val, *args):
        server = input_val[0]
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        term = None
        app = None
        start_window = 0
        flag = True
        try:
            start_window = pywinauto.findwindows.find_window(title=self.windowName)
            if ( start_window > 1 ):
                try:
                    app = Application(backend = "win32").connect(path = self.filePath).window(title = self.windowName)
                    SetForegroundWindow(find_window(title = self.windowName))
                    try:
                        editEle = app.Edit
                        edit2Ele = app.Edit2
                        editExists = editEle.exists()
                        edit2Exists = edit2Ele.exists()
                        if ( editExists and edit2Exists ):
                            ele = (edit2Ele if (editEle.Rectangle().top > edit2Ele.Rectangle().top) else editEle)
                        elif ( editExists ):
                            ele = editEle
                        elif ( edit2Exists ):
                            ele = edit2Ele
                        ele.set_edit_text('')
                        ele.type_keys(server, with_spaces = True)
                        time.sleep(0.4)#this delay is introduced as ServerConnect in SAP 7.70 upwards is very fast(would always select the first server connection)
                        if ( app['Log &OnButton'].exists() and app['Log &OnButton'].is_enabled() ):
                            app['Log &OnButton'].click()
                        elif ( app['Log &On'].exists() and app['Log &On'].is_enabled() ):
                            app['Log &OnButton'].click()
                        elif ( app.Button.exists() and app.Button.is_enabled() ):
                            app.Button.click()
                    except Exception as e:
                        err_msg = err_msg = sap_constants.ERROR_MSG + ' : ' + "Unable to Find LogOn Button or Filter Text Box, " + str(e)
                        flag = False

                    if ( flag ):
                        time.sleep(5)
                        if ( app != None and app != '' ):
                            try:
                                SapGui = self.uk.getSapObject()
                                SapGui.Children(0).Children(0)
                                log.debug( 'Connected to SAP' )
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            except Exception as e:
                                err_msg = sap_constants.ERROR_MSG + ' : ' + 'Given Server discription is incorrect, ' + str(e)
                                term = TERMINATE
                        else:
                            err_msg = 'The given window name is not found'
                            term = TERMINATE
                except Exception as e:
                    err = str(e)
                    if ('not found!' in err): err = err[:err.index('not found!')]
                    err_msg = sap_constants.ERROR_MSG + ' : ' + "SAP Logon window '" + self.windowName + "' does not exist for " + err
                    term = TERMINATE
            elif ( start_window == 0 ):
                err_msg = 'SAP Logon window does not exist'
                term = TERMINATE
            #---------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Could not find specified window name" )
            term = TERMINATE
        if ( term ):
            return term
        return status, result, verb, err_msg


    def getPageTitle(self, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            ses = self.getSession()
            if ( ses ):
                value = ses.ActiveWindow.Text
                status = sap_constants.TEST_RESULT_PASS
                result = sap_constants.TEST_RESULT_TRUE
            else :
                err_msg = sap_constants.SESSION_ERROR
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occurred in Get Page Title' )
        return status, result, value, err_msg

    def getPopUpText(self, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            ses, wnd = self.getSessWindow()
            if ( ses and wnd ):
                wnd_title = wnd.Text
                from sap_scraping import Scrape
                scrapingObj = Scrape()
                data = scrapingObj.full_scrape(wnd, wnd_title)
                for elem in data:
                    if ( elem['tag'] == "input" ):
                        if ( elem['text'] != "" ):
                            value = elem['text']
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                            err_msg = None
                            break
                        else:
                            err_msg = sap_constants.INVALID_INPUT
                    else:
                        err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.SESSION_AND_WINDOW_ERROR
            #--------------------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occurred in Get Popup Text' )
        return status, result, value, err_msg

    def closeApplication(self, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        try:
            try:
                SapGui = self.uk.getSapObject()
            except Exception as e:
                logger.print_on_console( sap_constants.ERROR_MSG + " : " +str(e) )
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
                        logger.print_on_console( "The specified application is closed Successfully" )
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
            status = sap_constants.TEST_RESULT_PASS
            result = sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occurred in closeApplication' )
        return status, result, verb, err_msg

    def captureScreenshot(self, screen_name, screen_id):

        """
        name: captureScreenshot
        purpose: To capture screenshot of the scraped window
        parameters: List of scraped elements
        returns: Nothing
        """
        img = None
        if ( "wnd[0]" not in screen_id ):
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
            error = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( error )
            logger.print_on_console( "Error has occurred while capturing screenshot" )
        #img.save(r'.\screenshot.png')
        return img

    def capture_window(self, handle):
        img = None
        bbox = None
        toplist, winlist = [], []
        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, toplist)
        hwnd = win32gui.GetForegroundWindow()
        win32gui.SetForegroundWindow(handle)
        bbox = win32gui.GetWindowRect(handle)
        img = ImageGrab.grab(bbox)
        return img

    def setWindowToForeground(self, sap_id):
        try:
            i = sap_id.index("/")
            wndNAME = sap_id[:i]
            app = Application()
            app.connect(title_re=wndNAME+"*")
            app.window(title_re=wndNAME+"*").set_focus()
            # handle = win32gui.FindWindow(None, wndNAME)
            # print(handle)
            # foreground_handle = win32gui.GetForegroundWindow()
            # print(foreground_handle)
            # if ( handle != foreground_handle ):
            #     foreThread = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
            #     appThread = win32api.GetCurrentThreadId()
            #     if ( foreThread != appThread ):
            #         win32process.AttachThreadInput(foreThread[0], appThread, True)
            #         win32gui.BringWindowToTop(handle)
            #         win32gui.ShowWindow(handle,5)
            #         win32process.AttachThreadInput(foreThread[0], appThread, False)
            #     else:
            #         win32gui.BringWindowToTop(handle)
            #         win32gui.ShowWindow(handle,5)
        except Exception as e:
            error = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error(error)
