#-------------------------------------------------------------------------------
# Name:        sap_scraping_genius
# Purpose:     Module for full scrape and ClickAndAdd SAP genius
#
# Author:      anas.ahmed1,kavyashree,sakshi.goyal,saloni.goyal,ajeya.devadiga
#
# Created:     07-11-2023
# Copyright:   (c) ajeya.devadiga 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import win32com.client
import logger
import logging
import logging.config
log = logging.getLogger('sap_scraping_genius.py')
import pyHook
import pythoncom
import ctypes
import win32gui
import win32api
import win32process
import platform
from threading import Thread
from pywinauto.application import Application
from pywinauto import Desktop
import pywinauto
import os
import json
import ast
import time
import keyboard
import pyautogui
ctrldownflag = False
stopumpingmsgs = False
obj_ref = None
window_id = None
view = []
text_typed = []

""" Class to fully scrape a SAP Gui."""

class Scrape:
    """" Method to recursively obtain all the elements/objects in the screen."""

    def full_scrape(self, object, wnd_title):

        """
        name: full_scrape
        purpose: To recursively obtain all the elements/objects in the window
        parameters: window to be scrapped
        returns: list of scraped elements
        """

        #global view
        view = []
        if ( wnd_title[-3] == "(" and wnd_title[-1] == ")" ):
            wnd_title = wnd_title[:-4]
        i = 0
        while True:
            try:
                custname = None
                elem = object.Children(i)
                # Not scraping GuiMenuBar and GuiToolBar with id tbar[0]
                if ( "mbar" in str(elem.__getattr__("Id")) or "tbar[0]" in str(elem.__getattr__("Id")) ):
                    i = i + 1
                else:
                    path = wnd_title + elem.__getattr__("Id")[25:]
                    custname, tag = self.get_ele_custname_tag(elem)
                    """ Python dictionary to store the properties associated with the objects."""
                    dict = {
                        'xpath': path,
                        'id': elem.__getattr__("Id"),
                        'text': elem.__getattr__("Text"),
                        'tag': tag,
                        'custname': custname,
                        'left': elem.__getattr__("ScreenLeft"),
                        'top': elem.__getattr__("ScreenTop"),
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
                                break
                        s = s + 1
                    except:
                        break
                c = c + 1
            except:
                break
        if ( number_of_active_screens > 10 ):
            logger.print_on_console('Number of Active Screens Greater than 10 not supported at the moment')
            title = None
            try:
                if ( window_to_scrape.__getattr__("Text").lower() != title.strip().lower() ):
                    self.getWindow(object)
            except Exception as e:
                log.error( 'Error occured : ' + str(e) )
                logger.print_on_console( 'Error occured in getWindow' )
                return None
        app=Application()
        try:
            """ The below code will try to connect to window based on window name
            which works fine in case of SAP logon but in case of SAP Business client it might fail to connect 
            as getattr method gives window name as "SAP" but works fine for subsequent screens """
            try:
                app.connect(title=window_to_scrape.__getattr__("Text"))    
                main_window = app.window(title=window_to_scrape.__getattr__("Text")).set_focus()
            except:
                window_name = "SAP GUI"
                app.connect(title=window_name, found_index=1)    
                main_window = app.window(title=window_name).set_focus()

            # Get the screen width and height
            screen_width, screen_height = pywinauto.win32functions.GetSystemMetrics(0), pywinauto.win32functions.GetSystemMetrics(1)

            # Calculate the new width and height for the window (in this case, 50% of the screen)
            new_width = screen_width // 2
            new_height = screen_height
            new_left = 0
            new_top = 0

            # Resize the window
            window_handle = main_window.handle
            pywinauto.win32functions.MoveWindow(window_handle, new_left, new_top, new_width, new_height, True)
        except:
            """
                The below code will run in case of SAP Business client as for the SAP Business client
                the name of the first screen is "SAP GUI" but getattr method returns "SAP", to handle this issue
                we are passing the window name as hardcoded value.
            """

            window_name = "SAP GUI"
            app.connect(title=window_name)    
            app.window(title=window_name).set_focus()

            main_window = app.top_window()

            # Get the screen width and height
            screen_width, screen_height = pywinauto.win32functions.GetSystemMetrics(0), pywinauto.win32functions.GetSystemMetrics(1)

            # Calculate the new width and height for the window (in this case, 50% of the screen)
            new_width = screen_width // 2
            new_height = screen_height
            new_left = 0
            new_top = 0

            # Resize the window
            window_handle = main_window.handle
            pywinauto.win32functions.MoveWindow(window_handle, new_left, new_top, new_width, new_height, True)
        return window_to_scrape

    # def getBaseWindow(self, object):
    #     """
    #         purpose : to get the first window (or base window)
    #         param object: SapGui Application Object
    #         returns: GuiWindow object
    #     """
    #     try:
    #         window_to_scrape = object           # 'app'
    #         con = object.Children(0)            # 'app/con[0]'
    #         ses = con.Children(0)               #'app/con[0]/ses[0]'
    #         w = 0                               # window number
    #         window_to_scrape = ses.Children(w)  #'app/con[0]/ses[0]/wnd[0]'
    #     except Exception as e:
    #         log.error( 'Error occured : ' + str(e) )
    #         logger.print_on_console( 'Error occured in getBaseWindow' )
    #     return window_to_scrape

    def clickandadd(self, operation, socket, user_name):
        """
        name: clickandadd
        purpose : To recursively obtain all the elements/objects in the window and filter out the ones clicked by the user
        parameters: window to be scrapped
        returns: scraped elements
        """
        scrape_obj = Scrape()
        if ( operation == 'STARTCLICKANDADD' ):
            global view, text_typed
            view = []
            text_typed.append("")
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
                        get_details_thread = GetdetailsThread(socket)
                        get_details_thread.join()
                        get_object = GetObject()
                        ses = get_object.GetSession(self.window_id)
                        try:
                            from screeninfo import get_monitors
                            if (str(platform.system()).lower() == 'windows' and str(platform.release()) == str(10) and get_monitors()[0].height >= 1080 and ctypes.windll.shcore.GetScaleFactorForDevice(0)/100 >= 1.25 ):
                                """
                                This custom logic is written for SAP clickandadd scrape specifically for windows 10 when scaling factor is 125%+ and screen resolution is 1080p greater
                                The general FindByPosition logic fails as some versions of SAP GUI are not dependant on scaling factor hence when passing screen x,y it will not the fetch correct elements.
                                Limitation/general info : will collect screeninfo of first monitor in a multi monitor setup
                                """
                                log.debug('Performing ClickAndAdd scrape via custom logic.Condition : Platform: windows 10, Screen: greater that 1080p, Scale&Layout: greater than 125% ')
                                try:
                                    def match(x, y, width, height, coord_x, coord_y):
                                        expectedx = int(x) + int(width)
                                        expectedy = int(y) + int(height)
                                        if ( (coord_x >= x and coord_x <= expectedx) and (coord_y >= y and coord_y <= expectedy) ):
                                            return 1
                                        else:
                                            return 0
                                    SAP_obj = get_object.GetSAPObj()
                                    wndname = scrape_obj.getWindow(SAP_obj)
                                    wnd_title = wndname.__getattr__("Text")
                                    all_items = scrape_obj.full_scrape(wndname,wnd_title)
                                    tempobjects = []
                                    for i in all_items:
                                        res = match(i['left'], i['top'], i['width'], i['height'], self.coordX, self.coordY)
                                        if ( res == 1 ):
                                            tempobjects.append(i)
                                    dict = None
                                    for i in range (len(tempobjects)):
                                        try:
                                            first_ele = tempobjects[i]
                                            dict = first_ele
                                            next_ele = tempobjects[i+1]
                                            if( (first_ele['left'] > next_ele['left']) and (first_ele['top'] > next_ele['top']) ):
                                                tempobjects[i+1] = first_ele
                                                dict = first_ele
                                            else:
                                                dict = next_ele
                                        except Exception as e:
                                            break
                                except Exception as e:
                                    log.error( 'Error occurred in custom clickandadd scraping' + str(e) )
                            else:
                                log.debug('Performing ClickAndAdd scrape via normal logic')
                                obj = ses.FindByPosition(self.coordX, self.coordY, False)
                                elem = ses.FindById(obj(0))
                                # if (elem.type != 'GuiModalWindow'):
                                custname = None
                                wnd_title = ses.FindById(self.window_id).Text
                                path = wnd_title + elem.__getattr__("Id")[25:]
                                custname, tag = scrape_obj.get_ele_custname_tag(elem)
                                keywordOperation = ''
                                if tag == "input":
                                    keywordOperation = "setText"
                                elif tag == "select":
                                    keywordOperation = "selectValueByText"
                                elif tag == "checkbox":
                                    keywordOperation = "click"
                                elif tag == "button":
                                    keywordOperation = "click"
                                elif tag == "radiobutton":
                                    keywordOperation = "selectRadioButton"
                                elif tag == "GuiTab":
                                    keywordOperation = "click"
                                elif tag == "table":
                                    keywordOperation = "getCellValue"
                                elif tag == "gridview":
                                    keywordOperation = "getCellText"
                                elif tag == "GuiOkCodeField":
                                    keywordOperation = "setText"
                                elif tag == "GuiMenubar":
                                    keywordOperation = "click"
                                elif tag == "GuiToolbar":
                                    keywordOperation = "click"
                                elif tag == "GuiTab":
                                    keywordOperation = "click"
                                else:
                                    keywordOperation = "click"
                                
                                dict = {
                                    'xpath': path,
                                    'id': elem.__getattr__("Id"),
                                    'inputVal': elem.__getattr__("Text"),
                                    'tag': tag,
                                    'custname': custname,
                                    'left': elem.__getattr__("ScreenLeft"),
                                    'top': elem.__getattr__("ScreenTop"),
                                    'height': elem.__getattr__("Height"),
                                    'width': elem.__getattr__("Width"),
                                    'keywordVal': keywordOperation,
                                    'window_name': wnd_title,
                                    'tooltip': elem.__getattr__("ToolTip") if hasattr(elem, "ToolTip") else "",
                                    'defaulttooltip': elem.__getattr__("DefaultToolTip") if hasattr(elem, "DefaultToolTip") else "",
                                    'user_name': user_name
                                }

                                if tag == "table" or tag == "gridview":
                                    dict["inputVal"] = "0;0"
                                if tag == "tree":
                                    dict["inputVal"] = ""
                            if ( dict not in view ):#------------to handle duplicate elements from backend
                                view.append(dict)

                            # if len(view) == 0:
                            #     view.append({ object_dict["window_name"] : [object_dict]})
                            # else:
                            #     for element in view:
                            #         if object_dict["window_name"] in element and len(element[object_dict["window_name"]]) > 0:
                            #             element[object_dict["window_name"]].append(object_dict)
                            #     else:
                            #         view.append({ object_dict["window_name"] : [object_dict]})

                            #Highlight objects while scraping
                            import sap_highlight
                            highlight_obj = sap_highlight.highLight()
                            highlight_obj.draw_outline(elem)

                            # get_details_thread = GetdetailsThread()
                            # get_details_thread.join()
                            # else:
                            #     log.error("Gui Modal Window identified - not allowed to scrape")
                        except Exception as e:
                            log.error( 'Error occured : ' + str(e) )
                            logger.print_on_console( 'Clicked option is not a part of SAPGUI' )
                        return True

                    def abort(self):
                        self._want_continue = 0

                class GetdetailsThread(Thread):
                    def __init__(self, socket):
                        """Init Worker Thread Class."""
                        Thread.__init__(self)
                        self._want_continue = 1
                        self.socket = socket
                        self.start()  # start the thread

                    def run(self):
                        if ( len(view) > 0 ):
                            global text_typed
                            id = view[len(view) - 1]['id']
                            get_object = GetObject()
                            ses = get_object.GetSession(window_id)
                            if "data_sent" not in view[len(view) - 1]:
                                view[len(view) - 1]['data_sent'] = "false"
                            try:
                                elem = ses.FindById(id)
                                if ( len(elem.__getattr__("Text")) > 0 ):
                                    text = elem.__getattr__("Text")
                                    view[len(view) - 1]['inputVal'] = str(text).strip()
                                    log.debug("Fetched Text of Element - " + str(text))
                                else:
                                    text = text_typed[0]
                                    view[len(view) - 1]['inputVal'] = str(text).strip()
                                    log.debug("Fetched Text of Element - " + str(text))
                                data = view[len(view) - 1]
                                if "data_sent" in view[len(view) - 1] and view[len(view) - 1]['data_sent'] == "false":
                                    self.socket.emit("sap_scrape_data", data)
                                    view[len(view) - 1]['data_sent'] = "true"
                                    text_typed[0] = ""
                            except Exception as e:
                                log.error('Error occured in GetdetailsThread: ' + str(e))
                                data = view[len(view) - 1]
                                if "data_sent" in view[len(view) - 1] and view[len(view) - 1]['data_sent'] == "false":
                                    view[len(view) - 1]['inputVal'] = text_typed[0]
                                    self.socket.emit("sap_scrape_data", data)
                                    view[len(view) - 1]['data_sent'] = "true"
                                    text_typed[0] = ""
                        return

                    def abort(self):
                        self._want_continue = 0

                class StartPump(Thread):
                    def __init__(self, socket):
                        Thread.__init__(self)
                        self._want_continue = 1
                        self.stopumpingmsgs = False
                        self.ctrldownflag = False
                        self.socket = socket
                        self.start()

                    def StopPump(self):
                        get_details_thread = GetdetailsThread(socket)
                        get_details_thread.join()
                        self.stopumpingmsgs = True
                        keyboard.unhook_all()
                        wsh = win32com.client.Dispatch("WScript.Shell")
                        wsh.SendKeys("^")

                    def run(self):
                        def OnMouseLeftDown(evnt):
                            pythoncom.CoInitialize()
                            try:
                                wndNames = evnt.WindowName
                                if ( wndNames is not 'Running applications' ):
                                    clicked_handle = evnt.Window
                                    while True:
                                        if ( clicked_handle == 0 ):   #comparing whether parent window is same as clicked window
                                            break
                                        else:
                                            if not( clicked_handle == self.handle ):    #recursively getting the parent handle
                                                clicked_handle = win32gui.GetParent(clicked_handle)
                                            else:
                                                if ( self.ctrldownflag is True ):
                                                    self.ctrldownflag = False       #if control flag is clicked
                                                    return True
                                                else:
                                                    pos = evnt.Position
                                                    coordX = pos[0]
                                                    coordY = pos[1]
                                                    obj = OutlookThread(coordX, coordY, window_id)
                                                    pyautogui.click(self.coordX, self.coordY)
                                                    return False

                            except Exception as e:
                                log.error('Error occured while scraping: ' + str(e))

                            if ( self.stopumpingmsgs is True ):
                                # self.hm.UnhookKeyboard()
                                self.hm.UnhookMouse()
                                ctypes.windll.user32.PostQuitMessage(0)
                            return True  # Returning True as we want the click to be performed on the application
##                            if ( self.ctrldownflag is True ):
##                                return True
##                            else:
##                                pos = evnt.Position
##                                coordX = pos[0]
##                                coordY = pos[1]
##                                obj = OutlookThread(coordX, coordY, window_id)
##                                return False

                        def OnKeyDown(event):
                            if ( self.stopumpingmsgs is True ):
                                # self.hm.UnhookKeyboard()
                                self.hm.UnhookMouse()
                                ctypes.windll.user32.PostQuitMessage(0)
                                return True
                            else:
                                if ( event.Key == 'Lcontrol' ):
                                    self.ctrldownflag = True
                                    return True
                                else:
                                    self.ctrldownflag = False
                                    return True

                        def OnKeyUp(evnt):
                            self.ctrldownflag = False
                            return True
                        
                        # Callback function to send the  data when Enter is pressed
                        def on_enter(event):
                            get_details_thread = GetdetailsThread(socket)
                            get_details_thread.join()
                            data = {
                                'xpath': '',
                                'id': '',
                                'inputVal': 'ENTER',
                                'tag': '',
                                'custname': '@Generic',
                                'left': '',
                                'top': '',
                                'height': '',
                                'width': '',
                                'tooltip': '',
                                'defaulttooltip': '',
                                'keywordVal': 'sendFunctionKeys',
                                'window_name': view[len(view) - 1]['window_name'],
                                'data_sent': "true",
                                'user_name': user_name
                            }
                            self.socket.emit("sap_scrape_data", data)

                        def on_key_event(e):
                            global text_typed
                            function_keys = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"]
                            if e.event_type == keyboard.KEY_DOWN:
                                key = e.name
                                if str(key).lower() in function_keys:
                                    data = {
                                        'xpath': '',
                                        'id': '',
                                        'inputVal': str(key),
                                        'tag': '',
                                        'custname': '@Generic',
                                        'left': '',
                                        'top': '',
                                        'height': '',
                                        'width': '',
                                        'tooltip': '',
                                        'defaulttooltip': '',
                                        'keywordVal': 'sendFunctionKeys',
                                        'window_name': view[len(view) - 1]['window_name'],
                                        'data_sent': "true",
                                        'user_name': user_name
                                    }
                                    self.socket.emit("sap_scrape_data", data)
                                elif len(key) == 1:
                                    text_typed[0] += key

                        global window_id
                        get_obj = GetObject()
                        window_id, self.handle = get_obj.GetWindow()
                        self.hm = pyHook.HookManager()
                        # self.hm.KeyDown = OnKeyDown
                        # self.hm.KeyUp = OnKeyUp
                        self.hm.MouseLeftDown = OnMouseLeftDown
                        # self.hm.HookKeyboard()
                        self.hm.HookMouse()
                        keyboard.hook(on_key_event)
                        keyboard.on_press_key("enter", on_enter)
                        pythoncom.PumpMessages()

                class GetObject():
                    def __init__(self):
                        from saputil_operations import SapUtilKeywords
                        self.uk = SapUtilKeywords()

                    def GetSAPObj(self):
                        return self.uk.getSapObject()

                    def GetSession(self, window_id):
                        """ Returns the session of window to scrape """
                        SapGui = self.uk.getSapObject()
                        i = window_id.index("ses")
                        sesId = window_id[0:i+6]
                        ses = SapGui.FindById(str(sesId))
                        return ses

                    def GetWindow(self):
                        """ Returns the id of window to scrape and brings the window to foreground """
                        SapGui = self.uk.getSapObject()
                        scrape = Scrape()
                        wnd = scrape.getWindow(SapGui)
                        wndId = wnd.Id
                        wndName = wnd.Text
                        try:
                            handle = win32gui.FindWindow(None, wndName)

                            """
                                The below condition will run in case of SAP Business client as for the SAP Business client
                                the name of the first screen is "SAP GUI" but getattr method returns "SAP", and the value
                                of the handle will be 0 so we are passing the window name as hardcode in order to get the handle.
                            """

                            if handle == 0 and wndName == "SAP":
                                wndName = "SAP GUI"
                                handle = win32gui.FindWindow(None, wndName)
                        except:
                            pass
                        foreThread = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                        appThread = win32api.GetCurrentThreadId()
                        if ( foreThread != appThread ):
                            win32process.AttachThreadInput(foreThread[0], appThread, True)
                            win32gui.BringWindowToTop(handle)
                            win32gui.ShowWindow(handle,5)
                            win32process.AttachThreadInput(foreThread[0], appThread, False)
                        else:
                            win32gui.BringWindowToTop(handle)
                            win32gui.ShowWindow(handle,5)
                        return wndId, handle

                global obj_ref
                obj_ref = StartPump(socket)
            except Exception as e:
                log.error( 'Error occured : ' + str(e) )
                logger.print_on_console( 'Error occured in Start click and add' )
                pass

        elif ( operation == 'STOPCLICKANDADD' ):
            try:
                obj_ref.StopPump()

                data = {'view': view}
                data = json.dumps(data)
                data_out = ast.literal_eval(data)

                with open(os.environ["AVO_ASSURE_HOME"] + '/output/domelements.json',"w") as f:
                    json.dump(data_out, f, indent=4, sort_keys=False)
                
                return view
            except Exception as e:
                log.error( 'Error occured : ' + str(e) )
                logger.print_on_console( 'Error occured in Stop click and add' )
                pass

    def get_ele_custname_tag(self,elem):
        """
            name: get_ele_custname_tag
            purpose: Method retreves only the custname and tag of the input element
            parameters: <element> object
            returns: tag, custname
        """
        custname=tag=None
        type = elem.__getattr__("Type")
        if ( type == "GuiButton" ):
            custname = elem.__getattr__("Name") + "_btn"
            tag = "button"
        elif ( type == "GuiTextField" or type == "GuiCTextField" or type == "GuiPasswordField" ):
            custname = elem.__getattr__("Name") + "_txtbox"
            tag = "input"
        elif ( type == "GuiComboBox" or type == "GuiBox" ):
            custname = elem.__getattr__("Name") + "_select"
            tag = "select"
        elif ( type == "GuiLabel" ):
            custname = elem.__getattr__("Name") + "_lbl"
            tag = "label"
        elif ( type == "GuiRadioButton" ):
            custname = elem.__getattr__("Name") + "_radiobtn"
            tag = "radiobutton"
        elif ( type == "GuiCheckBox" ):
            custname = elem.__getattr__("Name") + "_chkbox"
            tag = "checkbox"
        elif ( type == "GuiTableControl" ):
            custname = elem.__getattr__("Name") + "_tbl"
            tag = "table"
        elif ( type == "GuiScrollContainer" ):
            custname = elem.__getattr__("Name") + "_scroll"
            tag = type
        elif ( type == "GuiTab" ):
            custname = elem.__getattr__("Name") + "_tab"
            tag = type
        elif ( type == "GuiSimpleContainer" ):
            custname = elem.__getattr__("Name") + "_scontainer"
            tag = 'scontainer'
        elif ( type == "GuiShell" ):
            """Shell has subtypes, filtering via 'custname' and 'tag' type accordingly"""
            Subtype = None
            try : Subtype = elem.SubType
            except : log.debug('Shell does not have a subtype')
            if ( Subtype and Subtype == 'Tree'):
                custname = elem.__getattr__("Name") + "_tree"
                tag = "tree"
            elif ( Subtype and Subtype == 'GridView'):
                custname = elem.__getattr__("Name") + "_gridview"
                tag = "gridview"
            elif ( Subtype and Subtype == 'Calendar'):
                custname = elem.__getattr__("Name") + "_calendar"
                tag = "calendar"
            elif ( Subtype and Subtype == 'Toolbar'):
                custname = elem.__getattr__("Name") + "_toolbar"
                tag = "toolbar"
            elif ( Subtype and Subtype == 'Picture'):
                custname = elem.__getattr__("Name") + "_picture"
                tag = "picture"
            elif ( Subtype and Subtype == 'TextEdit'):
                custname = elem.__getattr__("Name") + "_textbox"
                tag = "text"

            else:
                """
                These elements are of type shell and all have Subtypes
                Tag for these elements will remain shell, these objects will have default shell keywords
                Incase of a CR remove the element from here and assign a tag name to it
                """
                if ( Subtype ) : custname = elem.__getattr__("Name") + '_' + str(Subtype).lower()
                else : custname = elem.__getattr__("Name") + "_shl"
                tag = "shell"
        else:
            custname = elem.__getattr__("Name") + "_elmnt"
            tag = type
        return custname,tag