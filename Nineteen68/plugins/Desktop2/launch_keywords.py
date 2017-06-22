#-------------------------------------------------------------------------------
# Name:        launch_keywords.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     29/05/2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from pywinauto.application import Application
import win32gui
import win32process
import win32con
import win32api
import subprocess
import logger
import  datetime
import os
import desktop_constants
import ctypes
import re
import time
from PIL import ImageGrab
from PIL.ImageOps import flip
import struct
from ctypes import wintypes
from constants import *
win_rect = 0
large = (0,0,0,0)
window_name=None
window_handle=None
window_pid=None
app_uia = None
import logging
log = logging.getLogger('launch_keywords.py')
class Launch_Keywords():



    def __init__(self):
        self.windowname=''
        self.aut_handle=None
        self.ldtpObj=None
        self.windowHandle=None

    def launch_application(self,input_val,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        term = None
        try:
        # check file exists
            if len(input_val)==1:
                filePath=input_val[0]
                timeout=5
            if(os.path.isfile(filePath)):
                directory = os.path.dirname(filePath)
                #check for any existing instance of app by window name
                filename,file_ext=os.path.splitext(filePath)
                if file_ext == '.bat':
                    log.debug('executing .bat file')
                    logger.print_on_console('executing .bat  file')
                    p = subprocess.Popen(filePath,cwd=os.path.dirname(filePath))
                    status=desktop_constants.TEST_RESULT_PASS
                    result = desktop_constants.TEST_RESULT_TRUE
                elif file_ext == '.exe':
                    value=win32api.ShellExecute(0,'open',filePath,None,directory,1)
                    time.sleep(3)
                    if int(value)>32:
                        status=desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
            else:
                term =TERMINATE
                logger.print_on_console('The file does not exists')

        except Exception as e:
            err_msg = desktop_constants.ERROR_MSG
            term =TERMINATE
        if term!=None:
            return term
        return status,result,self.windowname,err_msg

    def getPageTitle(self,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        err_msg=None
        try:
            if self.windowname!='':
                status=desktop_constants.TEST_RESULT_PASS
                result = desktop_constants.TEST_RESULT_TRUE
                return status,result,self.windowname,err_msg
        except Exception as e:
##            Exceptions.error(e)
            err_msg = desktop_constants.ERROR_MSG
        return status,result,self.windowname,err_msg

    def closeApplication(self,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if self.windowHandle!=None:
                win32gui.PostMessage(self.windowHandle,win32con.WM_CLOSE,0,0)
                status=desktop_constants.TEST_RESULT_PASS
                result = desktop_constants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg = desktop_constants.ERROR_MSG
        return status,result,verb,err_msg


    def captureScreenshot(self):
        image=None
        hwnd=window_handle
        try:
            if(hwnd!=None):
                mainhandle=hwnd
                hdc=win32gui.GetDC(win32gui.GetDesktopWindow())
                hdcMemDc=win32gui.CreateCompatibleDC(hdc)

                parent=win32gui.GetWindow(window_handle,4)
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
                if image==None:
                    win32gui.SetForegroundWindow(window_handle)
                    image=self.capture_window( window_handle)
        except Exception as e:
            import traceback
            traceback.print_exc()
            if image==None:
                win32gui.SetForegroundWindow(window_handle)
                image=self.capture_window( window_handle)

        return image




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
            aut_handle=window_handle
            if aut_handle> 0:
                foreground=win32gui.GetForegroundWindow()
                application_pid=win32process.GetWindowThreadProcessId(aut_handle)
                foreground_pid=win32process.GetWindowThreadProcessId(foreground)
                if application_pid!=foreground_pid:
                    process_id=    win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                    i= win32gui.GetWindowRect(aut_handle)
                    pid = self.get_window_pid(window_name)
                    rect = self.getParentRectangle(pid)
                    if i[0] <= -32000:
                        fg_thread, fg_process = win32process.GetWindowThreadProcessId(foreground)
                        aut_thread, aut_process = win32process.GetWindowThreadProcessId(aut_handle)
                        win32process.AttachThreadInput(aut_thread, fg_thread, True)
                        self.bring_to_top(aut_handle,4)
                        return True
                    else:
                        self.bring_to_top(aut_handle,4)
                        self.hide_always_on_top_windows()
                        win32gui.SetForegroundWindow(aut_handle)
                        return True
                else:
                    self.bring_to_top(aut_handle,1)
                    return True
        except Exception as e:
            err_msg = desktop_constants.ERROR_MSG

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
            err_msg = desktop_constants.ERROR_MSG

    def getParentRectangle(self,pid):
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible
        i = []
        tup_list = []
        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                fg_thread, fg_process_id = win32process.GetWindowThreadProcessId(hwnd)
                if fg_process_id == pid:
                    i = win32gui.GetWindowRect(hwnd)
                    global win_rect
                    tup_list.append(i)
                    min_val = min(x[1] for x in tup_list)
                    max_val = max(b for b in tup_list if b[1] == min_val)
                    global win_rect
                    win_rect = max_val
            return True
        win32gui.EnumWindows(foreach_window, None)

        return i

    def find_window_and_attach(self,input_val,*args):
        global window_name
        global window_handle
        global window_pid
        global app_uia
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        windowname =''
        launch_time_out = 0
        try:
            if len(input_val) == 2:
                windowname=input_val[0]
                launch_time_out = input_val[1]
            elif len(input_val) == 1:
                windowname=input_val[0]
            title_matched_windows=self.getProcessWindows(windowname)
            hwnd = win32gui.FindWindow(None, windowname)
            threadid,temp_pid = win32process.GetWindowThreadProcessId(hwnd)
            flag = False
            if len(title_matched_windows)>1:
                pidset = set()
                for i in title_matched_windows:
                    threadid,pid = win32process.GetWindowThreadProcessId(i)
                    pidset.add(pid)
                if len(pidset) == 1:
                    flag = True
                else:
                    for i in range(0,len(pidset)):
                        if pidset.pop() == temp_pid:
                            flag = True
                        else:
                            flag = False
                if flag:
                    if not(windowname is None and windowname is ''):
                        start_time = time.time()
                        var = 1
                        while var==1:
                            title_matched_windows=self.getProcessWindows(windowname)
                            if len(title_matched_windows)>1:
                                self.windowHandle=title_matched_windows[0]
                                self.windowname=self.getWindowText(self.windowHandle)
                                window_name=self.windowname
                                logger.print_on_console('Given windowname is '+windowname)
                                logger.print_on_console('Select the type of scrape (Full scrape/Click and Add) from scrape window')
                                window_handle=title_matched_windows[0]
                                window_pid=self.get_window_pid(self.windowname)
                                self.windowHandle=title_matched_windows[0]
                                app_uia = Application().connect(process = window_pid)
                                status=desktop_constants.TEST_RESULT_PASS
                                result = desktop_constants.TEST_RESULT_TRUE
                                break
                else:
                    self.multiInstance=title_matched_windows[0]
                    term = TERMINATE
            if len(title_matched_windows)==1:
                if not(windowname is None and windowname is ''):
                    start_time = time.time()
                    var = 1
                    while var==1:
                        title_matched_windows=self.getProcessWindows(windowname)
                        if len(title_matched_windows)==1:
                            self.windowHandle=title_matched_windows[0]
                            self.windowname=self.getWindowText(self.windowHandle)
                            logger.print_on_console('Application handle found')
                            window_name=self.windowname
                            logger.print_on_console('Given windowname is '+windowname)
                            window_handle=title_matched_windows[0]
                            window_pid=self.get_window_pid(self.windowname)
                            self.windowHandle=title_matched_windows[0]
                            app_uia = Application().connect(process = window_pid)
                            status=desktop_constants.TEST_RESULT_PASS
                            result = desktop_constants.TEST_RESULT_TRUE
                            break
                elif len(title_matched_windows)==0:
                    logger.print_on_console('The given window name is not found')
                    term = TERMINATE
        except Exception as e:
            logger.print_on_console(e)

        return status,result,self.windowname,err_msg


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
            err_msg = desktop_constants.ERROR_MSG

    def find_window(self,windowname):
        aut_handle = win32gui.FindWindow(None,windowname)
        if int(aut_handle) > 0:
            return aut_handle
        return None

    def save_screeenshot(self):
        try:
            import readconfig
            configobj = readconfig.readConfig()
            configvalues = configobj.readJson()
            path = configvalues['screenShot_PathName']
            if not os.path.exists(path):
                os.makedirs(path)
            filename=self.generateUniqueFileName()
            filePath = path + filename
            img=self.captureScreenshot()
            img.save(filePath + 'out.png')
            logger.print_on_console ('Screen captured and stored in location :' +filePath)
        except Exception as e:
            logger.print_on_console( e)

    def generateUniqueFileName(self):
        filename=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S_"+str(time.strftime("%Y%m%d%H%M%S")))
        return filename

    def select_menu(self, input,*args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        verb = OUTPUT_CONSTANT
        err_msg = None
        input_val = ''
        try:
            input_val = input[0]
            if len(input_val) > 0:
                win = app_uia.top_window()
                win.menu_select(input_val)
                log.info(STATUS_METHODOUTPUT_UPDATE)
                status = desktop_constants.TEST_RESULT_PASS
                result = desktop_constants.TEST_RESULT_TRUE
        except Exception as exception:
            logger.print_on_console ('Exception : Please give -> for separating the menu item/menu item not present ')
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status, result, verb, err_msg

    def maximize_window(self, input,*args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        verb = OUTPUT_CONSTANT
        err_msg = None
        input_val = ''
        try:
            win = app_uia.top_window()
            win.Maximize()
            log.info(STATUS_METHODOUTPUT_UPDATE)
            status = desktop_constants.TEST_RESULT_PASS
            result = desktop_constants.TEST_RESULT_TRUE
        except Exception as exception:
            logger.print_on_console ('Exception : Maximize window error ')
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status, result, verb, err_msg


    def minimize_window(self, input,*args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        verb = OUTPUT_CONSTANT
        err_msg = None
        input_val = ''
        try:
            win = app_uia.top_window()
            win.Minimize()
            log.info(STATUS_METHODOUTPUT_UPDATE)
            status = desktop_constants.TEST_RESULT_PASS
            result = desktop_constants.TEST_RESULT_TRUE
        except Exception as exception:
            logger.print_on_console (  'Exception : Minimize  window error ')
            log.error(exception)
            logger.print_on_console(exception)
        log.info(RETURN_RESULT)
        return status, result, verb, err_msg

    def get_hwnds_for_pid(self,pid):
        def callback(hwnd, hwnds):

            if win32gui.IsWindowVisible(hwnd):
                # logging.warning('inside 2nd def function')
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                # logging.warning('found id is == %s ', found_pid)
                if found_pid == pid:
                    # logging.warning('found pid %s ', pid)

                    hwnds.append(hwnd)
            return True
        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds

    def bring_Window_Front(self):
        try:
            pid = self.get_window_pid(window_name)
            hwnd =self.get_hwnds_for_pid(pid)
            winSize = len(hwnd)
            win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
            win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
            win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
            return hwnd[winSize - 1]
        except Exception as e:
            logger.print_on_console ('AUT closed')
