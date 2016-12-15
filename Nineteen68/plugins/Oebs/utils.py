#-------------------------------------------------------------------------------
# Name:        module2
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
import Exceptions
import json





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
                logger.log('Writing scrape data to domelements.json file')
                json.dump(scrape_data, outfile, indent=4, sort_keys=False)
        outfile.close()

    def set_to_foreground(self,windowname):
        self.windowname=windowname
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
        return False

    def bring_to_top(self,aut_handle,value):
        win32gui.BringWindowToTop(aut_handle)
        win32gui.ShowWindow(aut_handle,value)
        win32gui.SetForegroundWindow(aut_handle)

    def higlight(self,objectname):
        status=True
        try:
            self.set_to_foreground(self.windowname)
            obj=oebsServer.OebsKeywords()
            size=obj.getobjectsize(self.windowname,objectname)
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
        except Exception as e:
            status=False
            Exceptions.error(e)
        return status

    def find_oebswindow_and_attach(self,windowname,*args):
        logger.log('windowname is '+windowname)
        status=False
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
                    logger.log('Application handle found')
                    break;
        if self.aut_handle is not None:
            oebs_dispatcher.windowname=windowname
##            self.set_to_foreground(windowname)
            status=True
        return status

    def find_window_and_attach(self,url,objectname,keyword,windowname,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        windowname=windowname[0]
        res=self.find_oebswindow_and_attach(windowname)
        if status:
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        return status,methodoutput


    def find_window(self,windowname):
        aut_handle = win32gui.FindWindow(None,windowname)
        if int(aut_handle) > 0:
            return aut_handle
        return None

    def windowsrun(self):
        logging.debug('FILE: %s , DEF: %s',FILE_OEBSSERVER,DEF_WINDOWSRUN)
        return (oebs_api.bridgeDll.Windows_run())

    #Confirm open window is a java window
    def isjavawindow(self,windowname):
        logging.debug('FILE: %s , DEF: %s , MSG: Window Name Received: %s',FILE_OEBSSERVER,DEF_ISJAVAWINDOW, windowname)
        isjavares = False
        logging.debug('FILE: %s , DEF: %s , MSG: Window BRIDGE DLL Status: %s',FILE_OEBSSERVER,DEF_ISJAVAWINDOW,oebs_api.bridgeDll )
        if (oebs_api.bridgeDll != None):
            self.windowsrun()
            hwnd = self.GetHwndFromWindowName(windowname)
            logging.debug('FILE: %s , DEF: %s , MSG: API Call for Java window check',FILE_OEBSSERVER,DEF_ISJAVAWINDOW)
            isjavares = oebs_api.isJavaWindow(hwnd)
            return (isjavares, hwnd)
        else:
            logging.debug('FILE: %s , DEF: %s ,MSG: %s.',FILE_OEBSSERVER,DEF_ISJAVAWINDOW,MSG_ACCESS_BRIDGE_INIT_ERROR)
            return (isjavares, MSG_ACCESS_BRIDGE_INIT_ERROR)

    #Function to get HWND using window name
    def GetHwndFromWindowName(self,windowname):
        try:
            hwnd = win32gui.FindWindow(None, windowname)
            logging.debug('FILE: %s , DEF: %s MSG: Window Handle Fetched',FILE_OEBSSERVER,DEF_GETHWNDFROMWINDOWNAME)
        except:
            logging.debug('FILE: %s , DEF: %s , MSG: Window Handle Fetch Fail',FILE_OEBSSERVER,DEF_GETHWNDFROMWINDOWNAME)
            hwnd = None
        return hwnd



