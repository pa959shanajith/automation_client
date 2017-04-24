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

    def clickandadd(self,operation):
        print 'inside methodddd start click and add'
        if operation == 'STARTCLICKANDADD':
            try:
                class OutlookThread(Thread):
                    def __init__(self, coordX, coordY, window_id):
                        Thread.__init__(self)
                        self.coordX = coordX
                        self.coordY = coordY
                        self.window_id = window_id
                        self._want_continue = 1
                        self.start()

                    def run(self):
                        pythoncom.CoInitialize()
                        get_object = GetObject()
                        ses = get_object.GetSession(self.window_id)
                        print "Coordinates" , self.coordX, self.coordY
                        try:
                            obj = ses.FindByPosition(self.coordX, self.coordY, False)
                            print "Id of object", obj(0)
                            elem = ses.FindById(obj(0))

                            wnd_title = ses.FindById(self.window_id).Text
                            path = wnd_title + elem.__getattr__("Id")[25:]
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
                        except Exception as e:
                            print e
                        return True

                    def abort(self):
                        self._want_continue = 0

                class StartPump(Thread):
                    def __init__(self):
                        Thread.__init__(self)
                        self._want_continue = 1
                        self.stopumpingmsgs = False
                        self.ctrldownflag = False
                        self.start()

                    def StopPump(self):
                        print "Inside stop pump"
                        #ctypes.windll.user32.PostQuitMessage(0)
                        self.stopumpingmsgs = True
                        wsh = win32com.client.Dispatch("WScript.Shell")
                        wsh.SendKeys("^")

                    def run(self):
                        def OnMouseLeftDown(evnt):
                            global ctrldownflag
                            if (self.stopumpingmsgs == True):
                                self.hm.UnhookKeyboard()
                                self.hm.UnhookMouse()
                                ctypes.windll.user32.PostQuitMessage(0)
                                return True
                            if (ctrldownflag is True):
                                return True
                            else:
                                pos = evnt.Position
                                coordX = pos[0]
                                coordY = pos[1]
                                obj = OutlookThread(coordX, coordY, window_id)
                                return False

                        def OnKeyDown(event):
                            global ctrldownflag
                            if (self.stopumpingmsgs == True):
                                self.hm.UnhookKeyboard()
                                self.hm.UnhookMouse()
                                ctypes.windll.user32.PostQuitMessage(0)
                                return True
                            else:
                                if (event.Key == 'Lcontrol'):
                                    print "Inside OnKeyDown LControl"
                                    ctrldownflag = True
                                    #ctypes.windll.user32.PostQuitMessage(0)
                                    return True
                                else:
                                    ctrldownflag = False
                                    return True

                        def OnKeyUp(evnt):
                            print "Inside OnKeyUp event"
                            global ctrldownflag
                            ctrldownflag = False
                            self.stopumpingmsgs = True
                            obj_ref.StopPump()
                            return True

                        def dumpToJson():
                            """ Storing scraped elements in json """
                            try:
                                print "Dumping to json"
                                data['scrapetype'] = 'cna'
                                data['scrapedin'] = ''
                                data['view'] = view
                                with open('domelements.json', 'w') as outfile:
                                    json.dump(data, outfile, indent=4, sort_keys=False)
                                    outfile.close()
                                print "Data dumped to json"
                            except Exception as e:
                                print e

                        global window_id
                        get_obj = GetObject()
                        window_id = get_obj.GetWindow()
                        self.hm = pyHook.HookManager()
                        self.hm.KeyDown = OnKeyDown
                        self.hm.KeyUp = OnKeyUp
                        self.hm.MouseLeftDown = OnMouseLeftDown
                        self.hm.HookKeyboard()
                        self.hm.HookMouse()
                        pythoncom.PumpMessages()
                        dumpToJson()

                class GetObject():
                    def GetSession(self, window_id):
                        """ Returns the session of window to scrape """
                        pythoncom.CoInitialize()
                        SapGui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
                        i = window_id.index("ses")
                        sesId = window_id[0:i+6]
                        ses = SapGui.FindById(str(sesId))
                        return ses

                    def GetWindow(self):
                        """ Returns the id of window to scrape and brings the window to foreground """
                        pythoncom.CoInitialize()
                        SapGui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
                        scrape = Scrape()
                        wnd = scrape.getWindow(SapGui)
                        wndId = wnd.Id
                        wndName = wnd.Text
                        print wndName

                        handle = win32gui.FindWindow(None, wndName)
                        foreThread = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                        appThread = win32api.GetCurrentThreadId()
                        if( foreThread != appThread ):
                            win32process.AttachThreadInput(foreThread[0], appThread, True)
                            win32gui.BringWindowToTop(handle)
                            win32gui.ShowWindow(handle,3)
                            win32process.AttachThreadInput(foreThread[0], appThread, False)
                        else:
                            win32gui.BringWindowToTop(handle)
                            win32gui.ShowWindow(handle,3)
                        return wndId

                global obj_ref
                obj_ref = StartPump()
            except Exception as exception:
                pass

        elif operation == 'STOPCLICKANDADD':
            try:
                obj_ref.StopPump()
                return data
            except Exception as exception:
                pass
