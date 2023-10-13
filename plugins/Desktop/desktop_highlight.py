#-------------------------------------------------------------------------------
# Name:        desktop_highlight.py
# Purpose:     Highlight the selected element from the elements tree in Scrape screen, this feature is basically used to identify the right object
#
# Author:      wasimakram.sutar,anas.ahmed
#
# Created:     22/06/2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import desktop_launch_keywords
import logger
import time
from desktop_editable_text import Text_Box
import logging
log = logging.getLogger( 'desktop_highlight.py' )

class highLight():

    def get_desktop_element(self, xPath, url):
        #logic to find the desktop element using the xpath
        if ( ";" in xPath ):
            x_var = xPath.split(';')
            xpath = x_var[0]
            if ( len(x_var) == 5 ):
                backend = x_var[4]
        else:
            xpath = xPath
        ele = ''
        try:
            #=========================================================
            try:
                if ( str(backend).strip() == 'B' ):
                    win = desktop_launch_keywords.app_uia.top_window()
                    ch = []
                    def rec_ch(child):
                        ch.append(child)
                        for c in child.children():
                            rec_ch(c)
                    rec_ch(win)
                elif ( str(backend).strip() == 'A' ):
                    win = desktop_launch_keywords.app_win32.top_window()
                    ch = win.children()
            except:
                win = desktop_launch_keywords.app_win32.top_window()
                ch = win.children()
            #=========================================================
            split_xpath = xpath.split('/')
            parent = split_xpath[0]
            index = parent[parent.index('[') + 1 : parent.index(']')]
            ele = ch[int(index)]
            for i in range(1, len(split_xpath)):
                child = split_xpath[i]
                index = child[child.index('[') + 1 : child.index(']')]
                ch = ele.children()
                ele = ch[int(index)]
        except Exception as e:
            log.error( "Error occoured in get_desktop_element : ", e )
            logger.print_on_console( "Error occoured in get_desktop_element : " + str(e) )
        return ele

    def highlight_desktop_element(self, ele):
        try:
            ele.draw_outline(thickness = 5)
            logger.print_on_console( 'Element highlight completed successfully...' )
        except Exception as e:
            log.error( "Error occoured in highlight_desktop_element : ", e )
            logger.print_on_console( "Error occoured in highlight_desktop_element : " + str(e) )

    def highlight_element(self, objname, parent, *args):
        try:
            obj = desktop_launch_keywords.Launch_Keywords()
            obj.set_to_foreground()
            obj.bring_Window_Front()
            time.sleep(1)
            element = self.get_desktop_element(objname, parent)
            verify_obj = Text_Box()
            check = verify_obj.verify_parent(element, parent)
            if ( check ):
                self.highlight_desktop_element(element)
            else:
                logger.print_on_console( 'Element highlight failed...' )
                log.error( 'Element highlight failed...' )
        except Exception as e:
            log.error( "Error occoured in highlight_element : ", e )
            logger.print_on_console( 'Element highlight failed...' )