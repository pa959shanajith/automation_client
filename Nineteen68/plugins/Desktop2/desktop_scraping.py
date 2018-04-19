#-------------------------------------------------------------------------------
# Name:        desktop_scraping.py
# Purpose:     Radio check box operations
#
# Author:      wasimakram.sutar
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
import ninteen_68_desktop_scrape
import base64
import logger
ctrldownflag = False
stopumpingmsgs = False

import logging
log = logging.getLogger('desktop_scraping.py')
actualobjects = []
allobjects = []
class Scrape:
    def clickandadd(self,operation,wxobject):
        window_name=desktop_launch_keywords.window_name
        app_uia=desktop_launch_keywords.app_uia
        obj = desktop_launch_keywords.Launch_Keywords()
        obj.bring_Window_Front()
        if operation == 'STARTCLICKANDADD':
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
                        def match(x,y,width,height,coord_x,coord_y):

                            expectedx=int(x)+int(width)
                            expectedy=int(y)+int(height)

                            if((coord_x>= x and coord_x<=expectedx) and (coord_y >= y and coord_y<=expectedy)):
                                return 1
                            else:
                                return 0
                        try:
                            global allobjects
                            allobjects=self.get_all_children_caller(app_uia)
##                            objects = allobjects['view']
                            tempobjects = []
                            for i in allobjects['view']:
                                res = match(i['x_screen'],i['y_screen'],i['width'],i['height'],self.coordX,self.coordY)
                                if res == 1:
                                    tempobjects.append(i)
                            actualelement = ''
                            for i in range (len(tempobjects)):
                                try:
                                    first_ele = tempobjects[i]
                                    actualelement = first_ele
                                    next_ele = tempobjects[i+1]
                                    if ((first_ele['x_screen'] > next_ele['x_screen']) and (first_ele['y_screen'] > next_ele['y_screen'])):
                                        actualelement = first_ele
                                        break
                                except Exception as e:
                                    break
                            disp_obj = desktop_dispatcher.DesktopDispatcher()
                            ele = disp_obj.get_desktop_element(actualelement['xpath'],actualelement['url'],app_uia)
                            global actualobjects
                            if actualelement not in actualobjects:#------check to remove duplicate elements
                                actualobjects.append(actualelement)
                        except Exception as e:
                            logger.print_on_console('Clicked option is not a part of DesktopGUI')
                        return True

                    def get_all_children_caller(self,app_uia):
                        allobjs = {}
                        try:
                            win = app_uia.top_window()
                            ch = win.children()
                            a = ''
                            ne = []
                            obj = desktop_launch_keywords.Launch_Keywords()
                            #obj.set_to_foreground()
                            obj.bring_Window_Front()
                            winrect = desktop_launch_keywords.win_rect
                            scrape_obj=Scrape()
                            a =  scrape_obj.get_all_children(ch,ne,0,'',win,winrect)
                            #import json
                            allobjs["view"] = a
                        except Exception as e:
                            logger.print_on_console(e)
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
                                wndNames=evnt.WindowName
                                if wndNames is not 'Running applications':
                                        clicked_handle=evnt.Window
                                        while True:
                                            if clicked_handle==0L:   #comparing wether parent window is same as clicked window
                                                break
                                            else:
                                                if not(clicked_handle == self.handle ):    #recursivelt getting the parent handle
                                                    clicked_handle=win32gui.GetParent(clicked_handle)
                                                else:
                                                    if (self.ctrldownflag is True):
                                                        self.ctrldownflag = False       #if control flag is clicked
                                                        return True
                                                    else:
                                                        pos = evnt.Position
                                                        coordX = pos[0]
                                                        coordY = pos[1]
                                                        obj = OutlookThread(coordX, coordY, window_id)
                                                        return False
                            except Exception as e:
                                logger.print_on_console( e)

                            if (self.stopumpingmsgs is True):
                                self.hm.UnhookKeyboard()
                                self.hm.UnhookMouse()
                                ctypes.windll.user32.PostQuitMessage(0)
                                return True

                        def OnKeyDown(event):
                            if (self.stopumpingmsgs is True):
                                self.hm.UnhookKeyboard()
                                self.hm.UnhookMouse()
                                ctypes.windll.user32.PostQuitMessage(0)
                                return True
                            else:
                                if (event.Key == 'Lcontrol'):
                                    self.ctrldownflag = True
                                    return True
                                else:
                                    self.ctrldownflag = False
                                    return True

                        def OnKeyUp(evnt):
                            self.ctrldownflag = False
                            return True

                        global window_id
                        #global handle
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
                    def GetWindow(self):
                        """ Returns the id of window to scrape and brings the window to foreground """
                        wndId = 0
                        wndName = window_name
                        handle = win32gui.FindWindow(None, wndName)
                        foreThread = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                        appThread = win32api.GetCurrentThreadId()
                        if( foreThread != appThread ):
                            try:
                                win32process.AttachThreadInput(foreThread[0], appThread, True)
                                win32gui.BringWindowToTop(handle)
                                win32gui.ShowWindow(handle,5)
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
                pass
        elif operation == 'STOPCLICKANDADD':
            global actualobjects
            try:
                obj_ref.StopPump()
                allobjects= actualobjects
                actualobjects = []
            except Exception as exception:
                pass
            return allobjects

    def get_all_children(self,ch,ne,i,path,win,winrect):
        try:
            for i in range (len(ch)):
                 hiddentag = 'Yes'
                 text = ''
                 new_text=''
                 text_initial=''
                 text_old=''
                 parent = ''
                 coordinates = ''
                 children = ch[i]
                 canselectmultiple='false'
                 tag = children.friendly_class_name()
                 log.info(tag)
##                 if tag == 'Button' or tag =='RadioButton' or tag == 'Edit' or tag == 'ComboBox' or tag == 'Static' or tag == 'GroupBox' or tag == 'CheckBox' or tag== 'ListView' or tag == 'ListBox'or tag == 'TreeView'or tag == 'TabControl' or tag == 'DateTimePicker'  or tag == 'Toolbar':
                 coordinates = children.client_rect()
                 cor = children.rectangle()
                 properties = ''
                 try:
                     try:
                        properties = json.loads(json.dumps(children.get_properties(    ), default=lambda x: str(x)))
                     except Exception as e:
                        #----hardcoding only done for 32bit python as its not performing via children.get_properties
                        #----' id {0}'.format(button.idCommand)) or
                        #----RuntimeError: GetButtonInfo failed for "element" with command id XXXX occours when one of the properties not correct
                        #----Please Refer SWAPY application and check the element ,if all the properties are not populating , chances are this
                        #--- error will occour.I have noticed most of the time children.texts() is the problem hence setting it to u''
                        try:
                            getProperties={u'is_enabled': children.is_enabled(),
                                           u'is_visible': children.is_visible(),
                                           u'style': children.style(),
                                           u'fonts': children.fonts(),
                                           u'client_rects': children.client_rects(),
                                           u'texts': u'',
                                           u'class_name': children.class_name(),
                                           u'is_unicode': children.is_unicode(),
                                           u'control_id': children.control_id(),
                                           u'menu_items': children.menu_items(),
                                           u'user_data': children.user_data(),
                                           u'friendly_class_name': children.friendly_class_name(),
                                           u'control_count': children.control_count(),
                                           u'exstyle': children.exstyle(),
                                           u'context_help_id': children.context_help_id(),
                                           u'rectangle': children.rectangle()
                                          }
                            properties = json.loads(json.dumps(getProperties, default=lambda x: str(x)))
                        except Exception as e:
                            logger.print_on_console (e)
                     if properties['is_visible'] == True :
                         properties["url"] =  win.texts()[0] if len(win.texts())>0 else ""
                         properties['control_id'] = children.element_info.control_id
                         properties['parent'] = children.element_info.parent.class_name
                         handle = children.handle
                         text_initial = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem=handle,cache_enable=False).name
                         text=text_initial
                         if text =='':
                            t = children.texts()
                            if len(t) >= 2:
                                text = t[1]
                         if text == '':
                            text = children.friendly_class_name()
                         text_old = text.strip()
                         text=text_old
                         url = properties['url']
                         parent = properties['parent']
                         rectangle = properties['rectangle']
                         path = str (parent) + '[' + str(i) + ']'
                         if tag == 'Button':
                            tag = 'button'
                            text=  str(text) + '_btn'
                         elif tag == 'Edit':
                            tag = 'input'
                            text=  str(text) + '_txtbox'
                         elif tag == 'RadioButton':
                            tag = 'radiobutton'
                            text= str(text) + '_radiobtn'
                         elif tag == 'ComboBox':
                            tag = 'select'
                            text= str(text) + '_select'
                         elif tag == 'CheckBox':
                            tag ='checkbox'
                            text= str(text) + '_chkbox'
                         elif tag == 'ListView':
                            tag = 'list'
                            canselectmultiple="true"
                            text= str(text) + '_lst'
                         elif tag == 'ListBox':
                            tag = 'list'
                            canselectmultiple="true"
                            text= str(text) + '_lst'
                         elif tag == 'TabControl':
                            tag = 'tab'
                            text= str(text) + '_tab'
                         elif tag == 'TreeView':
                            tag = 'tree'
                            text= str(text) + '_tree'
                         elif tag == 'DateTimePicker':
                            tag = 'datepicker'
                            text= str(text) + '_dtp'
                         else:
                            tag = 'label'
                            if not isinstance(text,basestring):
                                text=str(text)+'_elmnt'
                            else:
                                text=text+'_elmnt'


                         left = 0
                         top = 0
                         width = coordinates.width()
                         height = coordinates.height()
                         x_screen = cor.left
                         y_screen = cor.top
                         left = cor.left - winrect[0]
                         top = cor.top - winrect[1]
                         if top < 0:
                            top = -top
                         if left < 0:
                            left = -left
                         control_id = properties['control_id']
                         if control_id == None:
                            control_id ='null'
                         if properties['is_visible'] == True :
                            hiddentag = 'No'
                            flag = False
                            for k in range(len(ne)):
                                if ne[k]['xpath'] == path:
                                    flag = True
                            #----------------------------------------------------
                            new_path=''
                            className=children.friendly_class_name()
                            if text_initial!='':
                                try:
                                    new_text=str(text_initial)
                                except:
                                    new_text=text_initial.encode('ascii', 'replace')
                            else :
                                new_text=text_old
                            new_path=path+';'+className+';'+str(control_id)+";"+new_text
                            #----------------------------------------------------
                            if not flag:
                                ne.append({"custname":text,
                                        "tag":tag,
                                        "url":url,
                                        'control_id':control_id,
                                        'parent':parent,
                                        'xpath' : new_path,
                                        'hiddentag':hiddentag,
                                        'top': top,
                                        'left': left,
                                        'height': height,
                                        'width': width,
                                        'x_screen':x_screen,
                                        'y_screen':y_screen,
                                        'canselectmultiple':canselectmultiple
                                        })
                            else:
                                logger.print_on_console( 'This element is duplicate')
                     else:
                        text = ''
                        handle = children.handle
                        text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem=handle,cache_enable=False).name
                 except Exception as e:
                    logger.print_on_console( e)
        except Exception as e:
            logger.print_on_console( e)
        return ne

    def full_scrape(self,app_uia,wxobject):
        allobjects = {}
        try:
            win = app_uia.top_window()
            ch = win.children()
            a = ''
            ne = []
            obj = desktop_launch_keywords.Launch_Keywords()
            obj.set_to_foreground()
            obj.bring_Window_Front()
            winrect = desktop_launch_keywords.win_rect;
            a =  self.get_all_children(ch,ne,0,'',win,winrect)
            allobjects = a
##            import json
##            try:
##                wxobject.Hide()
##                time.sleep(2)
##                img=ninteen_68_desktop_scrape.obj.captureScreenshot()
##                img.save('out.png')
##                with open("out.png", "rb") as image_file:
##                    encoded_string = base64.b64encode(image_file.read())
##                allobjects['mirror'] =encoded_string.encode('UTF-8').strip()
##            except Exception as e:
##                img=obj.capture_window( win32gui.GetDesktopWindow())
##                img.save('out.png')
##                with open("out.png", "rb") as image_file:
##                    encoded_string = base64.b64encode(image_file.read())
##                allobjects['mirror'] =encoded_string.encode('UTF-8').strip()
##            with open('domelements.json', 'w') as outfile:
##                allobjects["view"] = a
##                json.dump(allobjects, outfile, indent=4, sort_keys=False)
##                outfile.close()

        except Exception as e:
            logger.print_on_console(e)
        return allobjects
