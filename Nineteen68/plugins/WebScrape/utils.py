#-------------------------------------------------------------------------------
# Name:        utils.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     28-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import win32gui
import win32process
import win32con

class Utils:
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
        hwnd =Utils.get_hwnds_for_pid(self,pid)
        winSize = len(hwnd)
        win32gui.ShowWindow(hwnd[winSize - 1], win32con.SW_MAXIMIZE)
        win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd[winSize - 1], win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        return hwnd[winSize - 1]


