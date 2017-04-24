#-------------------------------------------------------------------------------
# Name:        Sap_scrapping
# Purpose:     Module for full scrape and ClickAndAdd . ClickAndAdd is not supported as of now
#
# Author:      anas.ahmed1,kavyashree,sakshi.goyal,saloni.goyal
#
# Created:     07-04-2017
# Copyright:   (c) anas.ahmed1 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from pywinauto.application import Application
import win32com.client
import json
import base64
import logger
import logging
import logging.config
log = logging.getLogger('sap_scraping.py')

""" Class to fully scrape a SAP Gui."""

class Scrape:

    """" Method to recursively obtain all the elements/objects in the screen."""
    def full_scrape(self, object,wnd_title):

        """
        name: full_scrape
        purpose: To recursively obtain all the elements/objects in the window
        parameters: window to be scrapped
        returns: list of scraped elements
        """

        if(wnd_title[-3] == "(" and wnd_title[-1] == ")"):
            wnd_title = wnd_title[:-4]
        view = []
        i = 0;
        while True:
            try:
                elem = object.Children(i)
                # Not scraping GuiMenuBar and GuiToolBar with id tbar[0]
                if("mbar" in str(elem.__getattr__("Id")) or "tbar[0]" in str(elem.__getattr__("Id"))):

                    i = i + 1
                else:

                    path = wnd_title + elem.__getattr__("Id")[25:]

                    """ Python dictionary to store the properties associated with the objects."""
                    dict = {
                            'xpath': path,
                            'id': elem.__getattr__("Id"),
                            'text': elem.__getattr__("Text"),
                            'tag': elem.__getattr__("Type"),
                            'custname': elem.__getattr__("Name"),
                            'screenleft': elem.__getattr__("ScreenLeft"),
                            'screentop': elem.__getattr__("ScreenTop"),
                            'left': elem.__getattr__("Left"),
                            'top': elem.__getattr__("Top"),
                            'height': elem.__getattr__("Height"),
                            'width': elem.__getattr__("Width"),
                            'tooltip': elem.__getattr__("ToolTip"),
                            'defaulttooltip': elem.__getattr__("DefaultToolTip")
                           }

                    view.append(dict)
                    i = i + 1
                    # recursive call to self
                    view.extend(self.full_scrape(elem, wnd_title))
            except:
                break
        return view


   ## @staticmethod
    def getWindow(self, object):
        """
        name: getWindow
        purpose : if multiple windows are open, prompt the user to choose the one to scrape
        parameters: SapGui Application Object
        returns: GuiWindow object
        """

        window_to_scrape = object
        number_of_active_screens = 0
        c = 0
        while True:
            try:
                con = object.Children(c)
                s = 0
                while True:
                    try:
                        ses = con.Children(s)
                        w = 0
                        while True:
                            try:
                                wnd = ses.Children(w)
                                number_of_active_screens = number_of_active_screens + 1
                                window_to_scrape = wnd
                                w = w + 1
                            except:
                                #logger.print_on_console('error in w:',e)
                                break
                        s = s + 1
                    except:
                        #logger.print_on_console('error in s:',e)
                        break
                c = c + 1
            except:
                #logger.print_on_console('error in c:',e)
                break
##        logger.print_on_console('Number of screens are :',number_of_active_screens)
        if(number_of_active_screens > 10):
            logger.print_on_console('Number of Active Screens Greater than 10 not supported at the moment')
            title=None
            try:
                if(window_to_scrape.__getattr__("Text").lower() != title.strip().lower()):
                    self.getWindow(object)
            except Exception as e:
                print e
                return None
##        logger.print_on_console('Window that is being scraped is :',wnd.text)
        return window_to_scrape

