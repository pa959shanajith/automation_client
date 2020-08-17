#-------------------------------------------------------------------------------
# Name:        utils_web_MW.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     10-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sys



import logging
from constants import SYSTEM_OS
if SYSTEM_OS!='Darwin':
    from pyrobot_MW import Robot
    import win32gui
    import win32process
    import win32con


log = logging.getLogger('utils_web_MW.py')

class Utils:

    def __init__(self):
        self.robot=Robot()
        self.rect=''

    def slide(self,a,b,speed=0):
        from time import sleep
        while True:
            if speed == 'slow':
                sleep(0.005)
                Tspeed = 2
            if speed == 'fast':
                sleep(0.001)
                Tspeed = 5
            if speed == 0:
                sleep(0.001)
                Tspeed = 3
            position=self.getpos()
            x = position[0]
            y = position[1]
            if abs(x-a) < 5:
                if abs(y-b) < 5:
                    break

            if a < x:
                x -= Tspeed
            if a > x:
                x += Tspeed
            if b < y:
                y -= Tspeed
            if b > y:
                y += Tspeed
            self.mouse_move(x,y)

    def mouse_move(self,x,y):
        log.debug('Moving the mouse to')
        log.debug(x)
        log.debug(y)
        self.robot.set_mouse_pos(x,y)

    def loop_childwindows(self,actwindow,param):
        log.debug('Inside loop_childwindows')
        class_name = win32gui.GetClassName(actwindow)
        if class_name == 'Internet Explorer_Server' or class_name == 'Chrome_RenderWidgetHostHWND' or class_name == 'WebKit2WebViewWindowClass':
            log.debug(class_name)
            rect=win32gui.GetWindowRect(actwindow)
            log.info('Rect is ')
            log.info(rect)
            self.rect=rect
        return True

    def getpos(self):
        log.debug('Getting the mouse position')
        point=self.robot.get_mouse_pos()
        log.debug(point)
        return point[0],point[1]

    def mouse_press(self,button):
        log.debug('Mouse press ')
        log.debug(button)
        self.robot.mouse_down(button)

    def mouse_release(self,button):
        log.debug('Release mouse ')
        log.debug(button)
        self.robot.mouse_up(button)

    def enumwindows(self):
        log.info('Finding the active window')
        actwindow = win32gui.GetForegroundWindow()
        log.debug('ACtive window is ')
        log.debug(actwindow)
        win32gui.EnumChildWindows(actwindow, self.loop_childwindows,None)

    def get_element_location(self,webelement):
        log.info('Getting the element location')
        return webelement.location_once_scrolled_into_view


    """win32 utilities
    def : bring_Window_Front
    param : pid of the browser opened by driver
    Brings the browser window to front
    """

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

    def bring_Window_Front(self,pid):
        hwnd =self.get_hwnds_for_pid(pid)
        winSize = len(hwnd)
        win32gui.ShowWindow(hwnd[winSize - 1], win32con.SW_MAXIMIZE)
        win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        return hwnd[winSize - 1]
