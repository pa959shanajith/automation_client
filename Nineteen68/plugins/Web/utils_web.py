#-------------------------------------------------------------------------------
# Name:        utils
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
from pyrobot import Robot
import win32gui

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
        self.robot.set_mouse_pos(x,y)

    def loop_childwindows(self,actwindow,param):
        class_name = win32gui.GetClassName(actwindow)
        if class_name == 'Internet Explorer_Server' or class_name == 'Chrome_RenderWidgetHostHWND' or class_name == 'WebKit2WebViewWindowClass':
            rect=win32gui.GetWindowRect(actwindow)
            self.rect=rect
        return True

    def getpos(self):
        point=self.robot.get_mouse_pos()
        return point[0],point[1]

    def mouse_press(self,button):
        self.robot.mouse_down(button)

    def mouse_release(self,button):
        self.robot.mouse_up(button)

    def enumwindows(self):
        actwindow = win32gui.GetForegroundWindow()
        win32gui.EnumChildWindows(actwindow, self.loop_childwindows,None)

    def get_element_location(self,webelement):
        return webelement.location_once_scrolled_into_view
