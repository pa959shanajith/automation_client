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

import win32gui
import win32process
import win32con
import win32api
import time
import sap_launch_keywords
import logger
import logging
import logging.config
log = logging.getLogger('sap_highlight.py')

class highLight():

    def highlight_element(self, elem):
        try:
            launch = sap_launch_keywords.Launch_Keywords()
            ses, window = launch.getSessWindow()
            try:
                i = elem.index("/")
                elemId = window.Id + elem[i:]
                screen_name = elem[:i]
            except:
                elemId = window.Id
                screen_name = elem
            elem_to_highlight = ses.FindById(elemId)
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
                time.sleep(1)
                if((bottom_right_y+60 <= window.Height) or ('sbar' in str(elemId))):
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
                else:
                    logger.print_on_console("Element not present on the current window. Please scroll down and try again.")
            except:
                pass
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error occured while highlighting")













