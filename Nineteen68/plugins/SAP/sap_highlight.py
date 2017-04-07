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

import logger

launchobj=ninteen_68_sap_scrape.obj

import logging
import logging.config
log = logging.getLogger('sap_highlight.py')

class highLight():

    def highlight_element(self, elem):
        logger.print_on_console('Highlight Object: ' +objname)
        with open('domelements.json', 'r') as f:
            data = json.load(f)
        view = data['view']
        screen_name = ""
        for obj in view:
            if(obj['id'] == elem):
                i = str(obj['path']).index('/')
                screen_name = obj['path'][:i]
                top_left_x = obj['screenleft']
                top_left_y = obj['screentop']
                bottom_right_x = obj['screenleft'] + obj['width']
                bottom_right_y = obj['screentop'] + obj['height']
                break
        toplist, winlist = [], []
        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, toplist)
        app = [(hwnd, title) for hwnd, title in winlist if screen_name in title]
        app = app[0]
        hwnd = app[0]
        try:
            win32gui.SetForegroundWindow(hwnd)
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






