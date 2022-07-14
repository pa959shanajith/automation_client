#-------------------------------------------------------------------------------
# Name:        utils_web.py
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
import pyautogui
if SYSTEM_OS=='Windows' :
    from pyrobot import Robot
    import win32gui
    import win32gui
    import win32process
    import win32con
import threading
local_uw = threading.local()

class Utils:

    def __init__(self):
        if SYSTEM_OS =='Windows':
            self.robot=Robot()
            self.rect=''
        local_uw.log = logging.getLogger('utils_web.py')

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

    def slide_linux(self,a,b,speed=0):
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
            position=self.getpos_linux()
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
            import pyautogui as pag
            pag.moveTo(x,y)

    def mouse_move_posix(self,x,y):
        local_uw.log.debug('Moving the mouse to')
        local_uw.log.debug(x)
        local_uw.log.debug(y)
        pyautogui.moveTo(x,y)
    def mouse_move(self,x,y):
        local_uw.log.debug('Moving the mouse to')
        local_uw.log.debug(x)
        local_uw.log.debug(y)
        self.robot.set_mouse_pos(x,y)

    def loop_childwindows(self,actwindow,param):
        local_uw.log.debug('Inside loop_childwindows')
        class_name = win32gui.GetClassName(actwindow)
        if class_name == 'Internet Explorer_Server' or class_name == 'Chrome_RenderWidgetHostHWND' or class_name == 'WebKit2WebViewWindowClass':
            local_uw.log.debug(class_name)
            rect=win32gui.GetWindowRect(actwindow)
            local_uw.log.info('Rect is ')
            local_uw.log.info(rect)
            self.rect=rect
        return True

    def getpos(self):
        local_uw.log.debug('Getting the mouse position')
        point=self.robot.get_mouse_pos()
        local_uw.log.debug(point)
        return point[0],point[1]

    def getpos_linux(self):
        local_uw.log.debug('Getting the mouse position')
        import pyautogui as pag
        point=pag.position()
        local_uw.log.debug(point)
        return point[0],point[1]

    def mouse_press(self,button):
        local_uw.log.debug('Mouse press ')
        local_uw.log.debug(button)
        self.robot.mouse_down(button)

    def mouse_release(self,button):
        local_uw.log.debug('Release mouse ')
        local_uw.log.debug(button)
        self.robot.mouse_up(button)

    def enumwindows(self):
        local_uw.log.info('Finding the active window')
        actwindow = win32gui.GetForegroundWindow()
        local_uw.log.debug('ACtive window is ')
        local_uw.log.debug(actwindow)
        win32gui.EnumChildWindows(actwindow, self.loop_childwindows,None)

    def get_element_location(self,webelement):
        local_uw.log.info('Getting the element location')
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
        try:
            hwnds = []
            win32gui.EnumWindows(callback, hwnds)
        except Exception as e:
            local_uw.log.error(e)
        return hwnds

    def bring_Window_Front(self,pid):
        hwnd =self.get_hwnds_for_pid(pid)
        win_handle=None
        try:
            winSize = len(hwnd)
            if winSize>0:
                win32gui.ShowWindow(hwnd[winSize - 1], win32con.SW_MAXIMIZE)
                win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                win_handle=hwnd[winSize - 1]
                local_uw.log.debug(win_handle)
        except Exception as e:
            local_uw.log.error(e)
        return win_handle
