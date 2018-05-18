#-------------------------------------------------------------------------------
# Name:        desktop_highlight.py
# Purpose:     Highlight the selected element from the elements tree in Scrape screen, this feature is basically used to identify the right object
#
# Author:      wasimakram.sutar
#
# Created:     22/06/2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import desktop_launch_keywords
from pywinauto.application import Application
import logger
import time
from desktop_editable_text import Text_Box


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
            logger.print_on_console( e)
        return ele

    def highlight_desktop_element(self,ele):
        try:
            ele.draw_outline(thickness=5)
            time.sleep(2)
            logger.print_on_console('Element highlight completed successfully...')
        except Exception as e:
            logger.print_on_console( e)

    def highLiht_element(self,objname,parent,*args):
        try:
            app_uia = desktop_launch_keywords.app_uia
            obj = desktop_launch_keywords.Launch_Keywords()
            obj.set_to_foreground()
            obj.bring_Window_Front()
            time.sleep(1)
            element = self.get_desktop_element(objname,parent,app_uia)
            verify_obj = Text_Box()
            check = verify_obj.verify_parent(element,parent)
            if check:
                self.highlight_desktop_element(element)
            else:
                logger.print_on_console('Element highlight failed...')
        except Exception as e:
            logger.print_on_console('Element highlight failed...')




