#-------------------------------------------------------------------------------
# Name:        Launch Keywords
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
import win32con
import win32api
import logger


import os
import sap_constants
import ctypes
import re
import time
from PIL import ImageGrab
from PIL.ImageOps import flip
import struct
from ctypes import wintypes
from constants import *

window_name=None
window_handle=None
window_pid=None

from pywinauto.application import Application
from pywinauto import keyboard
import win32com.client
import json
import pywinauto
import win32ui
from ctypes import windll
from PIL import Image
import base64

import logging
import logging.config
log = logging.getLogger('launch_keywords.py')

class Launch_Keywords():



    def __init__(self):
        self.windowname=''
        self.aut_handle=None
        self.ldtpObj=None
        self.windowHandle=None

    def enter_keyword(self,*args):
        status=sap_constants.TEST_RESULT_FALSE
        result=sap_constants.TEST_RESULT_FAIL
        err_msg=None
        value=''
        try:
            handle = win32gui.FindWindow(None, 'SAP')
            win32gui.SetForegroundWindow(handle)
            keyboard.SendKeys('{ENTER}')
            status=sap_constants.TEST_RESULT_TRUE
            result=sap_constants.TEST_RESULT_PASS
        except Exception as e:
            err_msg='Failed to press ENTER'
            log.error(err_msg,e)
            #logger.print_on_console('Failed to press ENTER',e)
        return status,result,value,err_msg

    def launch_application(self,input_val,*args):
        server = "SL2 [52.165.148.179]"
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        app_just=False
        err_msg=None
        term = None

        try:
        # check file exists
            if len(input_val)==2:
                filePath,windowName=input_val[0],input_val[1]
                timeout=5
            elif len(input_val)==3:
                filePath,windowName,timeout=input_val[0],input_val[1],input_val[2]
            start_window=0
            try:
             start_window = pywinauto.findwindows.find_window(title=windowName)
            except Exception as e:
                  log.error(e)
                  logger.print_on_console("Could not find specified window name")

            if start_window>=1:
                #self.multiInstance=title_matched_windows[0]
                logger.print_on_console('SAP window already exists please close the first instance')

            if start_window==0:
                logger.print_on_console('Starting new SAP window')
                #app = Application(backend="win32").start(r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe").window(title="SAP Logon 740")
                app = Application(backend="win32").start(filePath).window(title=windowName)
                logger.print_on_console('connecting to  new SAP window')
                #app = Application(backend="win32").connect(path = r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe").window(title="SAP Logon 740")
                app = Application(backend="win32").connect(path = filePath).window(title=windowName)
                app.Edit.set_edit_text(u'')
                app.Edit.type_keys(server, with_spaces = True)
                #app.Edit.type_keys("{ENTER}") #keyboard.SendKeys('{KEY}')- is win32 equivalent in pywinauto.application
                keyboard.SendKeys('{ENTER}')
                #logger.print_on_console('Pressed enter key')
                #incase onening second window fails , connect via giving a sleep command
                time.sleep(4)
                logger.print_on_console('The specified application is launched Successfully')

                if app!=None and app!='':
                    status=sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
##                            return status,self.windowname
                else:
                    logger.print_on_console('The given window name is not found')
                    term = TERMINATE
            else :
                error_code=int(win32api.GetLastError())
                #logger.print_on_console("inside else part ")
                if error_code in sap_constants.SAP_ERROR_CODES.keys():
                    logger.print_on_console("checking for error codes ")
                    logger.print_on_console(sap_constants.SAP_ERROR_CODES.get(error_code))
                    term =TERMINATE
                else:
                    logger.print_on_console('unable to launch the application')
                    term =TERMINATE

        except Exception as e:
            logger.print_on_console("Exception found",e)
            err_msg = sap_constants.ERROR_MSG
            term =TERMINATE
        if term!=None:
            return term
        return status,result,self.windowname,err_msg

    def getPageTitle(self,*args):
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        err_msg=None
        try:
            if self.windowname!='':
                status=sap_constants.TEST_RESULT_PASS
                result = sap_constants.TEST_RESULT_TRUE
                return status,self.windowname
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG
        return status,result,self.windowname,err_msg

    def closeApplication(self, *args):
        status=sap_constants.TEST_RESULT_FAIL
        result=sap_constants.TEST_RESULT_FALSE
        verb = ''
        err_msg=None
        try:
            SapGui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
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
            app = Application(backend="win32").connect(path = r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe").window(title="SAP Logon 740")
            app.Close()
            status=sap_constants.TEST_RESULT_PASS
            result=sap_constants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg='Error has occured :',e
        return status,result,verb,err_msg

##    def captureScreenshot(self, SapGui, data):
##
##        """
##        name: captureScreenshot
##        purpose: To capture screenshot of the scraped window
##        parameters: List of scraped elements
##        returns: Nothing
##        """
##        screen_name = ""
##        for obj in data:
##            if(obj['custname'] == 'titl'):
##                screen_name = obj['text']
##                break
##
##        if(screen_name == ""):
##            name = ""
##            name = data[0]['xpath']
##            i = name.index('/')
##            screen_name = name[:i]
##            print screen_name
##
##        handle = win32gui.FindWindow(None, screen_name)
##        left, top, right, bottom = win32gui.GetWindowRect(handle)
##        width = right - left
##        height = bottom - top
##        handleDC = win32gui.GetWindowDC(handle)
##        DC  = win32ui.CreateDCFromHandle(handleDC)
##        saveDC = DC.CreateCompatibleDC()
##        saveBitMap = win32ui.CreateBitmap()
##        saveBitMap.CreateCompatibleBitmap(DC, width, height)
##        saveDC.SelectObject(saveBitMap)
##        result = windll.user32.PrintWindow(handle, saveDC.GetSafeHdc(), 0)
####        logger.print_on_console(' result from print on window:',result)
##        bmpinfo = saveBitMap.GetInfo()
##        bmpbuff = saveBitMap.GetBitmapBits(True)
##        im = Image.frombuffer(
##            'RGB',
##            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
##            bmpbuff, 'raw', 'BGRX', 0, 1)
##        win32gui.DeleteObject(saveBitMap.GetHandle())
##        saveDC.DeleteDC()
##        DC.DeleteDC()
##        win32gui.ReleaseDC(handle, handleDC)
##        if result == 1:
####            logger.print_on_console('saving screenshot as screenshot.png')
##            im.save(r'.\screenshot.png')
####        logger.print_on_console('image obtained and going to 1968_sap_scrape ',im)
##        return im
    def captureScreenshot(self, SapGui, data):

        """
        name: captureScreenshot
        purpose: To capture screenshot of the scraped window
        parameters: List of scraped elements
        returns: Nothing
        """
        screen_name = ""
        for obj in data:
            if(obj['custname'] == 'titl'):
                screen_name = obj['text']
                break

        if(screen_name == ""):
            name = ""
            name = data[0]['xpath']
            i = name.index('/')
            screen_name = name[:i]
            print screen_name

        handle = win32gui.FindWindow(None, screen_name)
        try:
            #win32gui.SetForegroundWindow(handle)
            foreThread = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
            appThread = win32api.GetCurrentThreadId()
            if( foreThread != appThread ):
                win32process.AttachThreadInput(foreThread[0], appThread, True)
                win32gui.BringWindowToTop(handle)
                win32gui.ShowWindow(handle,3)
                win32process.AttachThreadInput(foreThread[0], appThread, False)
            else:
                win32gui.BringWindowToTop(handle)
                win32gui.ShowWindow(handle,3)
            time.sleep(2)
        except Exception as e:
            print e
        bbox = win32gui.GetWindowRect(handle)
        img = ImageGrab.grab(bbox)
        try:
            img.save(r'.\screenshot.png')
            return img
        except Exception as e:
            print e

    def capture_window(self,handle):
        toplist, winlist = [], []
        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, toplist)
        hwnd=win32gui.GetForegroundWindow()
        win32gui.SetForegroundWindow(handle)
        bbox = win32gui.GetWindowRect(handle)
        img = ImageGrab.grab(bbox)
        return img



    def getProcessWindows(self,windowName):
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible

        handles = []
        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
    ##                titles.append(buff.value)
                if self.patternMatching(windowName,buff.value):
                    handles.append(hwnd)
            return True
        win32gui.EnumWindows(foreach_window, None)
        return handles

    def patternMatching(self,toMatch,matchIn):
        regex=None
        pattern=None
        status=None
        toMatch=toMatch.strip().replace('*','.*')
        matchIn=matchIn.strip()
        if toMatch.endswith('*'):
            regex=toMatch+"([^a-zA-Z0-9-#.()%@!:;\"'?><,$+=()|{}&\\s]|$).*"
        elif toMatch.startswith('.'):
            regex=".*([^a-zA-Z0-9-#.()%@!:;\"'?><,$+=()|{}&\\s]|^)" + toMatch
        elif '*' in toMatch and toMatch.index('*')>0 and toMatch.index('*')<len(toMatch):
            toMatch = toMatch.replaceAll("[^a-zA-Z0-9*.]", ".*")
            regex=toMatch.replace(".*",".*([a-zA-Z0-9-#.()%@!:;\"'?><,$+=()|{}&\\s]|^)")
        else :
            return toMatch==matchIn
        status= re.match(regex,matchIn)

        try:
            if status.group()!=None:
                return True
        except Exception as e:
                return False
        return False


    def set_to_foreground(self):
        try:
##            windowname=window_name
##            aut_handle = win32gui.FindWindow(None,windowname)
            aut_handle=window_handle
            if aut_handle> 0:
                foreground=win32gui.GetForegroundWindow()
                application_pid=win32process.GetWindowThreadProcessId(aut_handle)
                foreground_pid=win32process.GetWindowThreadProcessId(foreground)
                if application_pid!=foreground_pid:
                    process_id=    win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                    i= win32gui.GetWindowRect(aut_handle)

                    if i[0] <= -32000:
                        fg_thread, fg_process = win32process.GetWindowThreadProcessId(foreground)
                        aut_thread, aut_process = win32process.GetWindowThreadProcessId(aut_handle)
                        win32process.AttachThreadInput(aut_thread, fg_thread, True)
                        self.bring_to_top(aut_handle,4)
                        return True
                    else:
##                        self.bring_to_top(aut_handle,4)
##                        self.bring_to_top(aut_handle,5)
                        self.hide_always_on_top_windows()
                        win32gui.SetForegroundWindow(aut_handle)
                        return True
                else:
                    self.bring_to_top(aut_handle,1)
                    return True
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG

        return False

    def hide_always_on_top_windows(self):
        win32gui.EnumWindows(self._window_enum_callback_hide, None)

    def _window_enum_callback_hide(self, hwnd, unused):
        if hwnd != window_handle: # ignore self
            # Is the window visible and marked as an always-on-top (topmost) window?
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & win32con.WS_EX_TOPMOST:
                # Ignore windows of class 'Button' (the Start button overlay) and
                # 'Shell_TrayWnd' (the Task Bar).
                className = win32gui.GetClassName(hwnd)
                if not (className == 'Button' or className == 'Shell_TrayWnd'):
                    # Force-minimize the window.
                    # Fortunately, this seems to work even with windows that
                    # have no Minimize button.
                    # Note that if we tried to hide the window with SW_HIDE,
                    # it would disappear from the Task Bar as well.
                    win32gui.ShowWindow(hwnd, win32con.SW_FORCEMINIMIZE)

    def bring_to_top(self,aut_handle,value):
       try:
            win32gui.BringWindowToTop(aut_handle)
            win32gui.ShowWindow(aut_handle,value)
            #win32gui.SetForegroundWindow(aut_handle)
       except Exception as e:
##            Exceptions.error(e)
            err_msg = sap_constants.ERROR_MSG

    def higlight(self,objectname,parent,*args):
        status=sap_constants.TEST_RESULT_FAIL
        try:
            method_input=objectname.split(';')
            actual_obj=method_input[0]
            index=method_input[1]

            self.set_to_foreground()
##            self.bring_to_top(window_handle,4)
            time.sleep(1)
#           for menu buttons click and highlight
            if actual_obj[:3]=='mnu':
                    if parent=='mnuApplication':
                        size=ldtp.getobjectsize(self.windowname,parent)
                        ldtp.generatemouseevent(size[0] + (size[2]) / 2, size[1]+ (size[3] / 2), "b1c")
                        time.sleep(1)
                        if actual_obj.endswith('1'):
                            obj_index=ldtp.getobjectproperty(self.windowname,actual_obj,'obj_index')
                            if obj_index==None:
                                actual_obj=actual_obj[0:-1]
                                index=ldtp.getObjectProperty(self,windowname,actual_obj, "obj_index")
            states=ldtp.getallstates(self.windowname,actual_obj)

            if sap_constants.VISIBLE_CHECK in states:
                size=ldtp.getobjectsize(self.windowname,actual_obj)
                logger.print_on_console( 'object size '+str(size))
                rgn1=win32gui.CreateRectRgnIndirect((size[0] + 1, size[1] + 1,
        							size[0] + size[2] - 1, size[1] + size[3] - 1))
                rgn2=win32gui.CreateRectRgnIndirect((size[0] + 4, size[1] + 4,
        							size[0] + size[2] - 4, size[1] + size[3] - 4))
                hdc=win32gui.CreateDC("DISPLAY", None, None)
                brush=win32gui.GetSysColorBrush(13)
                win32gui.CombineRgn(rgn1,rgn1,rgn2,3)
                win32gui.FillRgn(hdc,rgn1,brush)
                win32gui.SystemParametersInfo(win32con.SPI_SETFOREGROUNDLOCKTIMEOUT,5,win32con.SPIF_SENDWININICHANGE or win32con.SPIF_UPDATEINIFILE)
                win32gui.DeleteObject(rgn1)
                win32gui.DeleteObject(rgn2)
                win32gui.DeleteDC(hdc)
                status=sap_constants.TEST_RESULT_PASS
        except Exception as e:
            status=False
##            Exceptions.error(e)
##            import traceback
##            traceback.print_exc()
            err_msg = sap_constants.ERROR_MSG
        return status

    def find_window_and_attach(self,windowname,launch_time_out):
        logger.print_on_console('Given windowname is '+windowname)
        try:

            if not(windowname is None and windowname is ''):
                start_time = time.time()
                var = 1
                while var==1:

                    if int(time.time()-start_time) >= launch_time_out:
                        break
                    title_matched_windows=self.getProcessWindows(windowname)

                    if len(title_matched_windows)>1:
                        break
                    elif len(title_matched_windows)==1:

                        self.windowHandle=title_matched_windows[0]
                        self.windowname=self.getWindowText(self.windowHandle)

    ##                    self.set_to_foreground()
    ##                    time.sleep(0.5)
                        logger.print_on_console('Application handle found')
    ##                        tempTitle = windowTitle.replaceAll("[^a-zA-Z0-9]", "*")
                        # need  to create a ldtp object here
                        global window_name
                        window_name=self.windowname
                        global window_handle
                        window_handle=title_matched_windows[0]
                        global window_pid
                        window_pid=self.get_window_pid(self.windowname)
                        self.windowHandle=title_matched_windows[0]
                        break

                    if(self.windowname!=''):
                        break
        except Exception as e:
            import traceback
            traceback.print_exc()

        return self.windowname


    def getWindowText(self,hwnd):
        text=None
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible
        if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                text=buff.value
        return text
    def get_window_pid(self,title):
        hwnd = win32gui.FindWindow(None, title)
        threadid,pid = win32process.GetWindowThreadProcessId(hwnd)
        return pid

    def verifyWindowTitle(self):
        try:
            newWindowName=self.getWindowText(window_handle)
            if newWindowName!=self.windowname:
                self.windowname=newWindowName
                window_name=newWindowName
        except Exception as e:
##            Exceptions.error(e)
            err_msg = sap_constants.ERROR_MSG

    def find_window(self,windowname):
        aut_handle = win32gui.FindWindow(None,windowname)
        if int(aut_handle) > 0:
            return aut_handle
        return None

##
##Launch_Keywords=Launch_Keywords()
##Launch_Keywords.launch_application(['C:\Windows\system32\calc.exe','Calculator'])
##print Launch_Keywords.captureScreenshot()