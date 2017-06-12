#-------------------------------------------------------------------------------
# Name:        utils.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     26-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import win32gui
import win32process
import win32con
import win32api
import oebsServer
import oebs_api
from oebs_msg import *
import logger
import logging
import json
from PIL import ImageGrab
import ctypes
from ctypes import wintypes




log = logging.getLogger('utils.py')

class Utils:
    """win32 utilities
    def : bring_Window_Front
    param : pid of the browser opened by driver
    Brings the browser window to front
    """
    def __init__(self):
        self.windowname=''
        self.aut_handle=None

    def save_json(self,scrape_data):
        with open('domelements.json', 'w') as outfile:
                logger.print_on_console('Writing scrape data to domelements.json file')
                log.info('Writing scrape data to domelements.json file')
                json.dump(scrape_data, outfile, indent=4, sort_keys=False)
        outfile.close()

    def set_to_foreground(self,windowname):
        self.windowname=windowname
        flag = True
        aut_handle = win32gui.FindWindow(None,windowname)
        if aut_handle> 0:
            foreground=win32gui.GetForegroundWindow()
            oracle_pid=win32process.GetWindowThreadProcessId(aut_handle)
            foreground_pid=win32process.GetWindowThreadProcessId(foreground)
            if oracle_pid!=foreground_pid:
                process_id=    win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                i= win32gui.GetWindowRect(aut_handle)
                if i[0] <= -32000:

                    fg_thread, fg_process = win32process.GetWindowThreadProcessId(foreground)
                    aut_thread, aut_process = win32process.GetWindowThreadProcessId(aut_handle)
                    win32process.AttachThreadInput(aut_thread, fg_thread, True)
                    self.bring_to_top(aut_handle,4)
                else:
                    self.bring_to_top(aut_handle,5)
            else:
                self.bring_to_top(aut_handle,1)
        else:
            flag = False
        return flag

    def bring_to_top(self,aut_handle,value):
        win32gui.BringWindowToTop(aut_handle)
        win32gui.ShowWindow(aut_handle,value)
        win32gui.SetForegroundWindow(aut_handle)

    def highlight(self,objectname,windowname):
        status=True
        try:
            self.set_to_foreground(windowname)
            obj=oebsServer.OebsKeywords()
            size=obj.getobjectsize(windowname,objectname)
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
        except Exception as e:
            status=False
            log.error(e)
            logger.print_on_console(e)
        return status

    def find_oebswindow_and_attach(self,windowname,*args):
        logger.print_on_console('windowname is '+windowname)
        log.info('windowname is '+windowname)
        status=False
        err_msg=None
        try:
            import oebs_dispatcher
            import time
            load_timeout=1
            if len(args)>0:
                load_timeout=args[0]

            if not(windowname is None and windowname is ''):
                start_time = time.time()
                while (time.time() - start_time) < load_timeout:
                    handle=self.find_window(windowname)
                    if handle is not None:
                        self.aut_handle=handle
                        logger.print_on_console('Application handle found')
                        break;
            if self.aut_handle is not None:
                oebs_dispatcher.windowname=windowname
    ##            self.set_to_foreground(windowname)
                status=True
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=str(e)
        return status,err_msg


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

    def find_javawindow_and_attach(self,windowname,launch_time_out):
        err_msg=None
        try:
            import time
            logger.print_on_console('windowname is '+windowname)
            status=False
            if not(windowname is None and windowname is ''):
                import oebs_dispatcher
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
                            oebs_dispatcher.windowname=self.windowname

                            self.set_to_foreground(self.windowname)
                            time.sleep(0.5)
                            logger.print_on_console('Application handle found')
                            break
                        if(self.windowname!=''):
                            break
        except Exception as e:
            err_msg=str(e)
            log.error(err_msg)
        return self.windowname,err_msg

    def close_application(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg=None
        try:
            if self.aut_handle!=None:
                win32gui.PostMessage(self.aut_handle,win32con.WM_CLOSE,0,0)
                status=TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=str(e)
        return status,result,output,err_msg



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

    def launch_application(self,url,objectname,keyword,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg=None
        try:
        # check file exists
            import os
            if len(input_val)==2:
                filePath,window_name=str(input_val[0]),str(input_val[1])
                timeout=5
            elif len(input_val)==3:
                filePath,windowName,timeout=str(input_val[0]),str(input_val[1]),str(input_val[2])
            if(os.path.isfile(filePath)):
                directory = os.path.dirname(filePath)
                #check for any existing instance of app by window name
                title_matched_windows=self.getProcessWindows(window_name)
                if len(title_matched_windows)>=1:
##                    self.multiInstance=title_matched_windows[0]
                    logger.print_on_console('please close the existing application instnace with the given window name and try again')
                    logger.print_on_console('Terminate the execution')
                elif len(title_matched_windows)==0:
                    value=win32api.ShellExecute(0,'open',filePath,None,directory,1)
                    if int(value)>32:
                        logger.print_on_console('The specified application is launched')
                        result,err_msg=	self.find_javawindow_and_attach(window_name,timeout)
                        if result!=None:
                             status=TEST_RESULT_PASS
                             methodoutput=TEST_RESULT_TRUE
                    else :
                        error_code=int(win32api.GetLastError())
                        if error_code in APPLICATION_ERROR_CODES.keys():
                            err_msg=APPLICATION_ERROR_CODES.get(error_code)
                            logger.print_on_console(err_msg)
                        else:
                            logger.print_on_console('unable to launch the application')
            else:
                logger.print_on_console('The file does not exists')

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=str(e)
        return status,methodoutput,output,err_msg


    def find_window_and_attach(self,url,objectname,keyword,windowname,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        windowname=windowname[0]
        output=OUTPUT_CONSTANT
        res,err_msg=self.find_oebswindow_and_attach(windowname)
        if res:
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        return status,methodoutput,output,err_msg


    def find_window(self,windowname):
        aut_handle = win32gui.FindWindow(None,windowname)
        if int(aut_handle) > 0:
            return aut_handle
        return None

    def windowsrun(self):
        log.debug('FILE: %s , DEF: %s',)
        return (oebs_api.bridgeDll.Windows_run())

    #Confirm open window is a java window
    def isjavawindow(self,windowname):
        log.debug('MSG: Window Name Received: %s', windowname)
        isjavares = False
        log.debug('MSG: Window BRIDGE DLL Status: %s',oebs_api.bridgeDll )
        if (oebs_api.bridgeDll != None):
            self.windowsrun()
            hwnd = self.GetHwndFromWindowName(windowname)
            log.debug('MSG: API Call for Java window check',DEF_ISJAVAWINDOW)
            isjavares = oebs_api.isJavaWindow(hwnd)
            return (isjavares, hwnd)
        else:
            log.debug(',MSG: %s.',MSG_ACCESS_BRIDGE_INIT_ERROR)
            return (isjavares, MSG_ACCESS_BRIDGE_INIT_ERROR)

    #Function to get HWND using window name
    def GetHwndFromWindowName(self,windowname):
        try:
            hwnd = win32gui.FindWindow(None, windowname)
            log.debug('Window Handle Fetched')
        except:
            log.debug('MSG: Window Handle Fetch Fail')
            hwnd = None
        return hwnd


    def captureScreenshot(self,applicationname):
##        time.sleep(0.120)
        image=None
        isjavares, hwnd = self.isjavawindow(applicationname)
        window_handle=hwnd
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
                    image=self.capture_window(win32gui.GetDesktopWindow())
            else:
                if  self.getWindowText(ancestor)!=None and len(self.getWindowText(ancestor))>0:
                    image=self.capture_window( ancestor)
                elif self.getWindowText(parent)!=None and len(self.getWindowText(parent))>0:
                    image=self.capture_window(parent)
            if image==None:
                win32gui.SetForegroundWindow(window_handle)
                image=self.capture_window(window_handle)
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



