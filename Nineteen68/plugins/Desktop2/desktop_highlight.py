#-------------------------------------------------------------------------------
# Name:        desktop_highlight.py
# Purpose:
#
# Author:
#
# Created:     22-02-2017
# Copyright:   (c) prudhvi.gujjuboyina 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import ninteen_68_desktop_scrape
from pywinauto.application import Application
import logger

launchobj=ninteen_68_desktop_scrape.obj
import time
import launch_keywords

class highLight():

    def get_desktop_element(self,xpath,url,app):
        #logic to find the desktop element using the xpath
        ele = ''
        try:
            win = app.top_window()
            ch = win.children()
            split_xpath = xpath.split('/')
            parent = split_xpath[0]
            index = parent[parent.index('[') + 1 : parent.index(']')]
            ele = ch[int(index)]
            for i in range(1,len(split_xpath)):
                child = split_xpath[i]
                index = child[child.index('[') + 1 : child.index(']')]
                ch = ele.children()
                ele = ch[int(index)]
        except Exception as e:
            print e
        return ele

    def highlight_desktop_element(self,ele):
        try:
            ele.draw_outline(thickness=5)
            time.sleep(2)
            logger.print_on_console('Element highlighted')
        except Exception as e:
            print e

    def highLiht_element(self,objname,parent,*args):
        app_uia = launch_keywords.app_uia
##        obj = launch_keywords.Launch_Keywords()
##        obj.set_to_foreground()
        time.sleep(1)
        ele = self.get_desktop_element(objname,parent,app_uia)
        self.highlight_desktop_element(ele)

##        logger.print_on_console('Highlight Object: ' +objname)
##        print launchobj
##        status=launchobj.higlight(objname,parent,*args)
##        logger.print_on_console(objname+"  Highlight Status "+str(status))





