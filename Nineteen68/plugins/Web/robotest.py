#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     09-11-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from pyrobot import Robot
robot = Robot()

robot.set_mouse_pos(300,400)

robot.click_mouse(button='right')

