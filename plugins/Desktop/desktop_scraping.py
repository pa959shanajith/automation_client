#-------------------------------------------------------------------------------
# Name:        desktop_scraping.py
# Purpose:     full scrape and (click and add) methods of scraping are defined in this script
#
# Author:      wasimakram.sutar,anas.ahmed
#
# Created:     09-05-2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from pywinauto.application import Application
import desktop_dispatcher
import pywinauto
import pyHook
import pythoncom
import ctypes
import win32gui
import win32api
import time
import json
import win32com.client
import win32process
from threading import Thread
from constants import *
import desktop_launch_keywords
import base64
import logger
import wx
ctrldownflag = False
stopumpingmsgs = False

import logging
log = logging.getLogger( 'desktop_scraping.py' )
actualobjects = []
allobjects = []
click_count = 0
class Scrape:
    def clickandadd(self, operation, wxobject):
        window_name = desktop_launch_keywords.window_name
        obj = desktop_launch_keywords.Launch_Keywords()
        obj.bring_Window_Front()
        if ( operation == 'STARTCLICKANDADD' ):
            obj.set_to_foreground()
            global view
            view = []
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
                        #method returns 1 if the coordinates passed of any xpath, is near to the curson postion coordinates
                        #returns 0 if if coordinates doesnot fit into the condition
                        def match(x, y, width, height, coord_x, coord_y):
                            expectedx = int(x) + int(width)
                            expectedy = int(y) + int(height)
                            if ( (coord_x >= x and coord_x <= expectedx) and (coord_y >= y and coord_y <= expectedy) ):
                                return 1
                            else:
                                return 0
                        try:
                            global allobjects
                            if str(wxobject.backend_process).strip() == 'B':
                                wxobject.startbutton.SetBackgroundColour(wx.Colour(211,211,211))
                                wxobject.startbutton.Disable()
                            allobjects = self.get_all_children_caller()
                            objects = allobjects['view']
                            tempobjects = []
                            for i in allobjects['view']:
                                res = match(i['x_screen'], i['y_screen'], i['width'], i['height'], self.coordX, self.coordY)
                                if ( res == 1 ):
                                    tempobjects.append(i)
                            actualelement = ''
                            for i in range (len(tempobjects)):
                                try:
                                    first_ele = tempobjects[i]
                                    actualelement = first_ele
                                    next_ele = tempobjects[i+1]
                                    if( (first_ele['x_screen'] > next_ele['x_screen']) and (first_ele['y_screen'] > next_ele['y_screen']) ):
                                        tempobjects[i+1] = first_ele
                                        actualelement = first_ele
                                    else:
                                        actualelement = next_ele
                                except Exception as e:
                                    break
                            """calling dispatcher methods to check if the scrapped elements actually exist or not, if not present fails and returns an exception"""
                            disp_obj = desktop_dispatcher.DesktopDispatcher()
                            ele = disp_obj.get_desktop_element(actualelement['xpath'], actualelement['url'])
                            global actualobjects
                            global click_count
                            if ( actualelement not in actualobjects ):#------check to remove duplicate elements
                                actualobjects.append(actualelement)
                            else:
                                click_count -= 1

                            if str(wxobject.backend_process).strip() == 'B':  
                                if click_count == len(actualobjects):
                                    wxobject.startbutton.Enable()
                                    wxobject.startbutton.SetBackgroundColour('')
                        except Exception as e:
                            logger.print_on_console( 'Clicked option is not a part of DesktopGUI' )
                            log.error( 'Clicked option is not a part of DesktopGUI. Error msg : ', e )
                        return True

                    def get_all_children_caller(self):
                        allobjs = {}
                        try:
                            #=====================================check for uia
                            if ( str(wxobject.backend_process).strip() == 'A' ):
                                win = desktop_launch_keywords.app_win32.top_window()
                                ch = win.children()
                            elif ( str(wxobject.backend_process).strip() == 'B' ):
                                win = desktop_launch_keywords.app_uia.top_window()
                                ch=[]
                                def rec_ch(child):
                                    ch.append(child)
                                    for c in child.children():
                                        rec_ch(c)
                                rec_ch(win)
                            #===================================================
                            objects = None
                            ne = []
                            obj = desktop_launch_keywords.Launch_Keywords()
                            obj.bring_Window_Front()
                            winrect = desktop_launch_keywords.win_rect
                            scrape_obj = Scrape()
                            objects =  scrape_obj.get_all_children(ch, ne, 0, '', win, winrect, str(wxobject.backend_process).strip())
                            allobjs["view"] = objects
                        except Exception as e:
                            logger.print_on_console( e )
                            log.error( e )
                        return allobjs

                    def abort(self):
                        self._want_continue = 0

                class StartPump(Thread):
                    #print "starting pump"
                    def __init__(self):
                        Thread.__init__(self)
                        self._want_continue = 1
                        self.stopumpingmsgs = False
                        self.ctrldownflag = False
                        self.start()

                    def StopPump(self):
                        self.stopumpingmsgs = True
                        wsh = win32com.client.Dispatch("WScript.Shell")
                        wsh.SendKeys("^")

                    def run(self):
                        def OnMouseLeftDown(evnt):
                            try:
                                wndNames = evnt.WindowName
                                if ( wndNames is not 'Running applications' ):
                                        clicked_handle = evnt.Window
                                        while True:
                                            if ( clicked_handle == 0 ):   #comparing wether parent window is same as clicked window
                                                break
                                            else:
                                                if ( not(clicked_handle == self.handle ) ):    #recursivelt getting the parent handle
                                                    clicked_handle=win32gui.GetParent(clicked_handle)
                                                else:
                                                    if ( self.ctrldownflag is True ):
                                                        self.ctrldownflag = False       #if control flag is clicked
                                                        return True
                                                    else:
                                                        pos = evnt.Position
                                                        coordX = pos[0]
                                                        coordY = pos[1]
                                                        obj = OutlookThread(coordX, coordY, window_id)
                                                        global click_count
                                                        click_count += 1
                                                        return False
                            except Exception as e:
                                log.error( 'Error occoured while performing OnMouseLeftDown function, Error Msg : ', e )
                                logger.print_on_console( 'Error occoured while performing OnMouseLeftDown function.' )

                            if ( self.stopumpingmsgs is True ):
                                self.hm.UnhookKeyboard()
                                self.hm.UnhookMouse()
                                ctypes.windll.user32.PostQuitMessage(0)
                                return True

                        def OnKeyDown( event ):
                            if ( self.stopumpingmsgs is True ):
                                self.hm.UnhookKeyboard()
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

                        def OnKeyUp( evnt ):
                            self.ctrldownflag = False
                            return True

                        global window_id
                        get_obj = GetObject()
                        window_id, self.handle = get_obj.GetWindow()
                        self.hm = pyHook.HookManager()
                        self.hm.KeyDown = OnKeyDown
                        self.hm.KeyUp = OnKeyUp
                        self.hm.MouseLeftDown = OnMouseLeftDown
                        self.hm.HookKeyboard()
                        self.hm.HookMouse()
                        pythoncom.PumpMessages()

                class GetObject():
                    def GetWindow( self ):
                        """ Returns the id of window to scrape and brings the window to foreground """
                        wndId = 0
                        wndName = window_name
                        handle = win32gui.FindWindow(None, wndName)
                        foreThread = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                        appThread = win32api.GetCurrentThreadId()
                        if ( foreThread != appThread ):
                            try:
                                win32process.AttachThreadInput(foreThread[0], appThread, True)
                                win32gui.BringWindowToTop(handle)
                                win32gui.ShowWindow(handle, 5)
                                win32process.AttachThreadInput(foreThread[0], appThread, False)
                            except Exception as e:
                                pass
                        else:
                            win32gui.BringWindowToTop(handle)
                            win32gui.ShowWindow(handle,5)
                        return wndId, handle

                global obj_ref
                obj_ref = StartPump()
            except Exception as exception:
                logger.print_on_console ( 'Exception occoured when trying to perform START_CLICK_AND_ADD' )
                log.error('Exception occoured when trying to perform START_CLICK_AND_ADD, Error Msg : ', exception)
        elif ( operation == 'STOPCLICKANDADD' ):
            global actualobjects
            global click_count
            try:
                allobjects = actualobjects
                obj_ref.StopPump()
                actualobjects = []
                click_count = 0
            except Exception as exception:
                logger.print_on_console ( 'Exception occoured when trying to perform STOP_CLICK_AND_ADD' )
                log.error('Exception occoured when trying to perform STOP_CLICK_AND_ADD, Error Msg : ', exception)
            return allobjects

    def get_all_children(self, ch, ne, i, path, win, winrect, backend_process):
        try:
            for i in range(len(ch)):
                 hiddentag = 'Yes'
                 text = ''
                 new_text = ''
                 text_initial = ''
                 text_old = ''
                 parent = ''
                 coordinates = ''
                 canselectmultiple = 'false'
                 tag = ch[i].friendly_class_name()
                 log.info(tag)
                 try:
                    coordinates = ch[i].client_rect()
                 except:
                    """ Logic to find height and width for non hwndwrapper elements """
                    coordinates_obj = Rectangle()
                    coordinates_obj.set_coordinates(ch[i])
                    pass
                 cor = ch[i].rectangle()
                 properties = ''
                 try:
                     try:
                        properties = json.loads(json.dumps(ch[i].get_properties(    ), default=lambda x: str(x)))
                     except Exception as e:
                        #----hardcoding only done for 32bit python as its not performing via ch[i].get_properties
                        #----' id {0}'.format(button.idCommand)) or
                        #----RuntimeError: GetButtonInfo failed for "element" with command id XXXX occours when one of the properties not correct
                        #----Please Refer SWAPY application and check the element ,if all the properties are not populating , chances are this
                        #--- error will occour.I have noticed most of the time ch[i].texts() is the problem hence setting it to u''
                        try:
                            getProperties = {'is_enabled' : ch[i].is_enabled(),
                                           'is_visible' : ch[i].is_visible(),
                                           'style' : ch[i].style(),
                                           'fonts' : ch[i].fonts(),
                                           'client_rects' : ch[i].client_rects(),
                                           'texts' : '',
                                           'class_name' : ch[i].class_name(),
                                           'is_unicode' : ch[i].is_unicode(),
                                           'control_id' : ch[i].control_id(),
                                           'menu_items' : ch[i].menu_items(),
                                           'user_data' : ch[i].user_data(),
                                           'friendly_class_name' : ch[i].friendly_class_name(),
                                           'control_count' : ch[i].control_count(),
                                           'exstyle' : ch[i].exstyle(),
                                           'context_help_id' : ch[i].context_help_id(),
                                           'rectangle' : ch[i].rectangle()
                                          }
                            properties = json.loads(json.dumps(getProperties, default=lambda x: str(x)))
                        except Exception as e:
                            """Some properties dont exists in ele<uia> when comapred to ele<win32>"""
                            try:
                                getProperties = {'is_enabled' : ch[i].is_enabled(),
                                           'is_visible' : ch[i].is_visible(),
                                           'style' : '',
                                           'fonts' : '',
                                           'client_rects' : '',
                                           'texts' : '',
                                           'class_name' : ch[i].class_name(),
                                           'is_unicode' : '',
                                           'control_id' : '',
                                           'menu_items' :'',
                                           'user_data' : '',
                                           'friendly_class_name' : ch[i].friendly_class_name(),
                                           'control_count' : '',
                                           'exstyle' : '',
                                           'context_help_id' :'',
                                           'rectangle' : ch[i].rectangle()
                                          }
                                properties = json.loads(json.dumps(getProperties, default=lambda x:str(x)))
                            except Exception as e:
                                log.error( 'Error occoured while getting properties of the element, Error Msg : ', e )
                                logger.print_on_console ( 'Error occoured while getting properties of the element' )
                                pass
                     properties["url"] =  win.texts()[0] if len(win.texts()) > 0 else ""
                     properties['control_id'] = ch[i].element_info.control_id
                     properties['parent'] = ch[i].element_info.parent.class_name
                     if ( backend_process == 'A' ):
                         handle = ch[i].handle
                         text_initial = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem = handle, cache_enable = False).name
                         text = text_initial
                         if ( text == '' ):
                            t = ch[i].texts()
                            if ( len(t) >= 2 ):
                                text = t[1]
                         if ( text == '' ):
                            text = ch[i].friendly_class_name()
                         text_old = text
                         text = text_old
                     elif ( backend_process == 'B' ):
                        text_initial = ch[i].texts()
                        text = text_initial
                        if ( type(text) == list ):
                            if ( text[0] == '' ):
                                handle = ch[i].handle
                                text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem = handle, cache_enable = False).name
                                if ( text == '' or text == None ):
                                    text = ch[i].friendly_class_name()
                            else:
                                try:
                                    if ( type(text[0]) == list ):
                                        try:
                                            text = str(text[0][0])
                                        except:
                                            text = text[0][0].encode('ascii', 'replace')
                                    else:
                                        text = str(text[0])
                                except:
                                    text = text[0].encode('ascii', 'replace')
                        else:
                            if ( text == '' or text[0] == '' ):
                                handle = ch[i].handle
                                text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem = handle, cache_enable = False).name
                                if ( text == '' or None ):
                                    text = ch[i].friendly_class_name()
                            else:
                                text = text_initial[0]
                        text_old = text
                        text = text_old
                     url = properties['url']
                     parent = properties['parent']
                     rectangle = properties['rectangle']
                     path = str (parent) + '[' + str(i) + ']'
                     if ( tag == 'Button' ):
                        tag = 'button'
                        text =  str(text) + '_btn'
                     elif ( tag == 'Edit' ):
                        tag = 'input'
                        text =  str(text) + '_txtbox'
                     elif ( tag == 'RadioButton' ):
                        tag = 'radiobutton'
                        text = str(text) + '_radiobtn'
                     elif ( tag == 'ComboBox' ):
                        tag = 'select'
                        text= str(text) + '_select'
                     elif ( tag == 'CheckBox' ):
                        tag ='checkbox'
                        text = str(text) + '_chkbox'
                     elif ( tag == 'ListView' ):
                        tag = 'list'
                        canselectmultiple="true"
                        text = str(text) + '_lst'
                     elif ( tag == 'ListBox' ):
                        tag = 'list'
                        canselectmultiple="true"
                        text = str(text) + '_lst'
                     elif ( tag == 'TabControl' ):
                        tag = 'tab'
                        text = str(text) + '_tab'
                     elif ( tag == 'TreeView' ):
                        tag = 'tree'
                        text = str(text) + '_tree'
                     elif ( tag == 'DateTimePicker' ):
                        tag = 'datepicker'
                        text = str(text) + '_dtp'
                     elif ( tag == 'Table' ):
                        tag = 'table'
                        text = str(text) + '_table'
                     else:
                        tag = 'label'
                        if ( not isinstance(text, str) ):
                            text = str(text) + '_elmnt'
                        else:
                            text = text + '_elmnt'
                     left = 0
                     top = 0
                     try:
                        width = coordinates.width()
                        height = coordinates.height()
                     except:
                        width = coordinates_obj.width
                        height = coordinates_obj.height
                        pass
                     x_screen = cor.left
                     y_screen = cor.top
                     left = cor.left - winrect[0]
                     top = cor.top - winrect[1]
                     if ( top < 0 ):
                        top = -top
                     if ( left < 0 ):
                        left = -left
                     control_id = properties['control_id']
                     if ( control_id == None ):
                        control_id ='null'
                     #--------------------------------------------hidden_flag
                     if ( properties['is_visible'] == True ):
                        hiddentag = False
                     elif ( properties['is_visible'] == False ):
                        hiddentag = True
                     #------------------------------------------------------
                     flag = False
                     for k in range(len(ne)):
                        if ( ne[k]['xpath'] == path ):
                            flag = True
                     #----------------------------------------------------
                     new_path = ''
                     className = ch[i].friendly_class_name()
                     #handling for UIA listbox
                     if ( ch[i].backend.name == 'uia' and ch[i].friendly_class_name() == 'ListBox' ):
                        new_text=text_old
                     elif ( text_initial != '' ):
                        if ( type(text_initial) == list ):
                            try:
                                new_text = ', '.join([x.encode('utf-8') for x in text_initial])
                            except:
                                new_text = ', '.join(str(v) for v in text_initial)
                        else:
                            try:
                                new_text = str(text_initial)
                            except:
                                new_text = text_initial.encode('ascii', 'replace')
                     else :
                        new_text = text_old
                     new_path = path + ';' + className + ';' + str(control_id) + ";" + new_text + ';' + backend_process
                     #----------------------------------------------------
                     if ( not flag ):
                        ne.append({"custname" : text,
                                "tag" : tag,
                                "url" : url,
                                'control_id' : control_id,
                                'parent' : parent,
                                'xpath' : new_path,
                                'hiddentag' : hiddentag,
                                'top' : top,
                                'left' : left,
                                'height' : height,
                                'width' : width,
                                'x_screen' : x_screen,
                                'y_screen' : y_screen,
                                'canselectmultiple' : canselectmultiple
                                })
                     else:
                        logger.print_on_console( 'This element is duplicate' )
                        log.info( 'This element is duplicate' )
                 except Exception as e:
                    logger.print_on_console( e )
                    log.error( e )
        except Exception as e:
            logger.print_on_console( e )
            log.error( e )
        return ne

    def full_scrape(self, wxobject):
        allobjects = {}
        try:
            #=====================================check for uia
            if ( str(wxobject.backend_process).strip() == 'A' ):
                win = desktop_launch_keywords.app_win32.top_window()
                ch = win.children()
            elif ( str(wxobject.backend_process).strip() == 'B' ):
                win = desktop_launch_keywords.app_uia.top_window()
                ch = []
                def rec_ch(child):
                    ch.append(child)
                    for c in child.children():
                        rec_ch(c)
                rec_ch(win)
            #===================================================
            ne = []
            obj = desktop_launch_keywords.Launch_Keywords()
            obj.set_to_foreground()
            obj.bring_Window_Front()
            winrect = desktop_launch_keywords.win_rect;
            allobjects =  self.get_all_children(ch, ne, 0, '', win, winrect, str(wxobject.backend_process).strip())
        except Exception as e:
            log.error( 'Error occoured while performing full_scrape, Error Msg : ', e )
            logger.print_on_console( 'Error occoured while performing full_scrape' )
        return allobjects

class Rectangle:
    def __init__(self):
        self.height = None
        self.width = None
    def set_coordinates(self,child):
        try:
            self.height = int(child.rectangle().bottom) - int(child.rectangle().top)
            self.width = int(child.rectangle().right) - int(child.rectangle().left)
        except Exception as e:
            logger.print_on_console( 'Error fetching object coordinates' )
            log.error( 'Error fetching object coordinates, Error Msg : ', e )