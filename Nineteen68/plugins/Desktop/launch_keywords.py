#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     17-11-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import win32gui
import win32process
import win32con
import win32api
import logger
import Exceptions
import os
import desktop_constants
import ctypes
import re
import time
from PIL import ImageGrab
from PIL.ImageOps import flip
import struct
from ctypes import wintypes
import ldtp
from ldtp.client_exception import LdtpExecutionError

window_name=None
window_handle=None
class Launch_Keywords():



    def __init__(self):
        self.windowname=''
        self.aut_handle=None
        self.ldtpObj=None
        self.windowHandle=None

    def launch_application(self,input_val,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        try:
        # check file exists
            filePath,windowName,timeout=input_val[0],input_val[1],input_val[2]
            if(os.path.isfile(filePath)):
                directory = os.path.dirname(filePath)
                #check for any existing instance of app by window name
                title_matched_windows=self.getProcessWindows(windowName)
                if len(title_matched_windows)>=1:
                    self.multiInstance=title_matched_windows[0]
                    logger.log('please close the existing application instnace with the given window name and try again')
                    logger.log('Terminate the execution')
                elif len(title_matched_windows)==0:
                    value=win32api.ShellExecute(0,'open',filePath,None,directory,1)
                    if int(value)>32:
                        logger.log('The specified application is launched')
                        result=	self.find_window_and_attach(windowName,timeout)
                        if result!=None:
                            status=desktop_constants.TEST_RESULT_PASS
                            return status,self.windowname
                    else :
                        error_code=int(win32api.GetLastError())
                        if error_code in desktop_constants.DESKTOP_ERROR_CODES.keys():
                            logger.log(desktop_constants.DESKTOP_ERROR_CODES.get(error_code))
                        else:
                            logger.log('unable to launch the application')
            else:
                logger.log('The file does not exists')

        except Exception as e:
            Exceptions.error(e)
        return status,self.windowname

    def getPageTitle(self,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        try:
            if self.windowname!='':
                status=desktop_constants.TEST_RESULT_PASS
                return status,self.windowname
        except Exception as e:
            Exceptions.error(e)
        return status,self.windowname

    def closeApplication(self,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        try:
            if window_handle!=None:
                win32gui.PostMessage(window_handle,win32con.WM_CLOSE,0,0)
                status=desktop_constants.TEST_RESULT_PASS
                return status
        except Exception as e:
            Exceptions.error(e)
        return status

    def captureScreenshot(self,hwnd):
        time.sleep(0.120)
        image=None

        if(hwnd!=None):
            mainhandle=hwnd
            hdc=win32gui.GetDC(win32gui.GetDesktopWindow())
            hdcMemDc=win32gui.CreateCompatibleDC(hdc)

            parent=win32gui.GetWindow(hwnd,4)
            ancestor=win32gui.GetWindow(mainhandle,3)
            foreground=win32gui.GetForegroundWindow()
            if foreground!=mainhandle:
                fg_thread, fg_process_id = win32process.GetWindowThreadProcessId(foreground)
                aut_thread, aut_process_id = win32process.GetWindowThreadProcessId(mainhandle)
                if fg_process_id==aut_process_id:
                    image=self.capture_window( win32gui.GetDesktopWindow())
            else:
                if  self.getWindowText(ancestor)!=None and len(self.getWindowText(ancestor))>0:
                    image=self.capture_window( ancestor)
                elif self.getWindowText(parent)!=None and len(self.getWindowText(parent))>0:
                    image=self.capture_window( parent)
                else:
                    image=self.capture_window( hwnd)
        return image



    def capture_window(self,hwnd):
        toplist, winlist = [], []
        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, toplist)
        hwnd=win32gui.GetForegroundWindow()
        win32gui.SetForegroundWindow(hwnd)
        bbox = win32gui.GetWindowRect(hwnd)
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
        EnumWindows(EnumWindowsProc(foreach_window), 0)
        return handles

    def patternMatching(self,toMatch,matchIn):
        regex=None
        pattern=None

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
            windowname=window_name
            aut_handle = win32gui.FindWindow(None,windowname)
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
                        self.bring_to_top(aut_handle,5)
                        return True
                else:
                    self.bring_to_top(aut_handle,1)
                    return True
        except Exception as e:
            Exceptions.error(e)

        return False

    def bring_to_top(self,aut_handle,value):
       try:
            win32gui.BringWindowToTop(aut_handle)
            win32gui.ShowWindow(aut_handle,value)
            #win32gui.SetForegroundWindow(aut_handle)
       except Exception as e:
            Exceptions.error(e)

    def higlight(self,objectname,parent,*args):
        status=False
        try:
            method_input=objectname.split(';')
            actual_obj=method_input[0]
            index=method_input[1]

            self.set_to_foreground()
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
            states=ldtp.getAllStates(self.windowname,actual_obj)

            if desktop_constants.VISIBLE_CHECK in states:
                size=ldtp.getobjectsize(self.windowname,object)
                logger.log( 'object size '+str(size))
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
                status=desktop_constants.TEST_RESULT_PASS
        except Exception as e:
            status=False
            Exceptions.error(e)
        return status

    def find_window_and_attach(self,windowname,launch_time_out):
        logger.log('windowname is '+windowname)
        status=False
        if not(windowname is None and windowname is ''):
            start_time = time.time()
            while True:
                    if int(time.time() - start_time) == launch_time_out:
                            break
                    title_matched_windows=self.getProcessWindows(windowname)
                    if len(title_matched_windows)>1:
                        break
                    elif len(title_matched_windows)==1:
                        self.windowHandle=title_matched_windows[0]
                        self.windowname=self.getWindowText(self.windowHandle)

                        self.set_to_foreground()
                        time.sleep(0.5)
                        logger.log('Application handle found')
##                        tempTitle = windowTitle.replaceAll("[^a-zA-Z0-9]", "*")
                        # need  to create a ldtp object here
                        global window_name
                        window_name=self.windowname
                        global window_handle
                        window_handle=title_matched_windows[0]
                        break
                    if(self.windowname!=''):
                        break
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

    def verifyWindowTitle(self):
        try:
            newWindowName=self.getWindowText(window_handle)
            if newWindowName!=self.windowname:
                self.windowname=newWindowName
                window_name=newWindowName
        except Exception as e:
            Exceptions.error(e)


    def find_window(self,windowname):
        aut_handle = win32gui.FindWindow(None,windowname)
        if int(aut_handle) > 0:
            return aut_handle
        return None


