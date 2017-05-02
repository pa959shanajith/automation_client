#-------------------------------------------------------------------------------
# Name:        sap_highlight
# Purpose:     Module for highlighting objects
#
#Author:      anas.ahmed1,kavyashree,sakshi.goyal,saloni.goyal
#
# Created:     07-04-2017
# Copyright:   (c) anas.ahmed1 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import json
import win32gui
import win32process
import win32con
import win32api
import time
import ninteen_68_sap_scrape
import launch_keywords
import logger

launchobj=ninteen_68_sap_scrape.obj

import logging
import logging.config
log = logging.getLogger('sap_highlight.py')

class highLight():

    def highlight_element(self, elem):
        launch = launch_keywords.Launch_Keywords()
        ses, window = launch.getSessWindow()
        i = elem.index("/")
        elemId = window.Id + elem[i:]
        elem_to_highlight = ses.FindById(elemId)
        screen_name = elem[:i]
        top_left_x = elem_to_highlight.ScreenLeft
        top_left_y = elem_to_highlight.ScreenTop
        bottom_right_x = elem_to_highlight.ScreenLeft + elem_to_highlight.Width
        bottom_right_y = elem_to_highlight.ScreenTop + elem_to_highlight.Height
        toplist, winlist = [], []
        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, toplist)
        app = [(hwnd, title) for hwnd, title in winlist if screen_name == title]
        app = app[0]
        hwnd = app[0]
        try:
            foreThread = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
            appThread = win32api.GetCurrentThreadId()
            if( foreThread != appThread ):
                win32process.AttachThreadInput(foreThread[0], appThread, True)
                win32gui.BringWindowToTop(hwnd)
                win32gui.ShowWindow(hwnd,5)
                win32process.AttachThreadInput(foreThread[0], appThread, False)
            else:
                win32gui.BringWindowToTop(hwnd)
                win32gui.ShowWindow(hwnd,3)
            time.sleep(2)
            #win32gui.BringWindowToTop(hwnd)
            #win32gui.ShowWindow(hwnd,1)

            rgn1=win32gui.CreateRectRgnIndirect((top_left_x,top_left_y,bottom_right_x,bottom_right_y))
            rgn2=win32gui.CreateRectRgnIndirect((top_left_x+4,top_left_y+4,bottom_right_x-4,bottom_right_y-4))
            hdc=win32gui.CreateDC("DISPLAY", None, None)
            brush=win32gui.GetSysColorBrush(13)
            win32gui.CombineRgn(rgn1,rgn1,rgn2,3)
            win32gui.FillRgn(hdc,rgn1,brush)
            win32gui.SystemParametersInfo(win32con.SPI_SETFOREGROUNDLOCKTIMEOUT,5,win32con.SPIF_SENDWININICHANGE or win32con.SPIF_UPDATEINIFILE)
            win32gui.DeleteObject(rgn1)
            win32gui.DeleteObject(rgn2)
            win32gui.DeleteDC(hdc)
        except Exception as e:
            logger.print_on_console(e)













