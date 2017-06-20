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
import launch_keywords
import ninteen_68_desktop_scrape
import base64
import logger
ctrldownflag = False
stopumpingmsgs = False


actualobjects = []
allobjects = []
class Scrape:
    def clickandadd(self,operation,app_uia,window_name):
        obj = launch_keywords.Launch_Keywords()
        obj.set_to_foreground()
        data={}
        if operation == 'STARTCLICKANDADD':
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
                            obj = Scrape()
                            global allobjects
                            allobjects = obj.full_scrape(app_uia)
                            objects = allobjects['view']
                            tempobjects = []
                            for i in objects:
                                res = match(i['x_screen'],i['y_screen'],i['width'],i['height'],self.coordX,self.coordY)
                                if res == 1:
                                    tempobjects.append(i)
                            actualelement = ''
                            for i in range (len(tempobjects)):
                                try:
                                    first_ele = tempobjects[i]
                                    actualelement = first_ele
                                    next_ele = tempobjects[i+1]
                                    if ((first_ele['x_screen'] < next_ele['x_screen']) and (first_ele['y_screen'] < next_ele['y_screen'])):
                                        actualelement = first_ele
                                except Exception as e:
                                    break

                            disp_obj = desktop_dispatcher.DesktopDispatcher()
                            ele = disp_obj.get_desktop_element(actualelement['xpath'],actualelement['url'],app_uia)
                            global actualobjects
                            actualobjects.append(actualelement)
                        except Exception as e:
                            logger.print_on_console('Clicked option is not a part of DesktopGUI')
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
                                print e

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
                        get_obj = GetObject()
                        window_id, self.handle = get_obj.GetWindow()
                        self.hm = pyHook.HookManager()
                        self.hm.KeyDown = OnKeyDown
                        self.hm.KeyUp = OnKeyUp
                        self.hm.MouseLeftDown = OnMouseLeftDown
                        self.hm.HookKeyboard()
                        self.hm.HookMouse()
                        pythoncom.PumpMessages()
    ##                        dumpToJson()

                class GetObject():
    ##
                    def GetWindow(self):
                        """ Returns the id of window to scrape and brings the window to foreground """
                        wndId = 0
                        wndName = window_name
                        handle = win32gui.FindWindow(None, wndName)
                        foreThread = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                        appThread = win32api.GetCurrentThreadId()
                        if( foreThread != appThread ):
                            win32process.AttachThreadInput(foreThread[0], appThread, True)
                            win32gui.BringWindowToTop(handle)
                            win32gui.ShowWindow(handle,5)
                            win32process.AttachThreadInput(foreThread[0], appThread, False)
                        else:
                            win32gui.BringWindowToTop(handle)
                            win32gui.ShowWindow(handle,5)
                        return wndId, handle

                global obj_ref
                obj_ref = StartPump()
            except Exception as exception:
                pass

        elif operation == 'STOPCLICKANDADD':
            try:
                obj_ref.StopPump()
                with open('domelements.json', 'w') as outfile:
                    allobjects["view"] = actualobjects
                    json.dump(allobjects, outfile, indent=4, sort_keys=False)
                    outfile.close()
##                return view
                global actualobjects
                actualobjects = []
            except Exception as exception:
                pass
            return allobjects


    def get_all_children(self,ch,ne,i,path,win,winrect):
        try:
            for i in range (len(ch)):
                 hiddentag = 'Yes'
                 text = ''
                 parent = ''
                 coordinates = ''
                 children = ch[i]
                 tag = children.friendly_class_name()
                 print 'tag ::::: ',tag
##                 if tag == 'Button' or tag =='RadioButton' or tag == 'Edit' or tag == 'ComboBox' or tag == 'Static' or tag == 'GroupBox' or tag == 'CheckBox' or tag== 'ListView' or tag == 'ListBox'or tag == 'TreeView'or tag == 'TabControl' or tag == 'DateTimePicker'  or tag == 'Toolbar':
                 coordinates = children.client_rect()
                 cor = children.rectangle()
                 properties = ''
                 try:
                    properties = json.loads(json.dumps(children.get_properties(    ), default=lambda x: str(x)))
                 except Exception as e:
                    print e
                 if properties['is_visible'] == True :
                     properties["url"] =  win.texts()[0] if len(win.texts())>0 else ""
                     properties['control_id'] = children.element_info.control_id
                     properties['parent'] = children.element_info.parent.class_name
                     handle = children.handle
                     text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem=handle,cache_enable=False).name
                     if text =='':
                        t = children.texts()
                        if len(t) >= 2:
                            text = t[1]
                     if text == '':
                        text = children.friendly_class_name()
                     text = text.strip()
                     url = properties['url']
                     parent = properties['parent']
                     rectangle = properties['rectangle']
                     path = str (parent) + '[' + str(i) + ']'
##                         if path == '':
##                            path = str (parent) + '[' + str(i) + ']'
##                         else:
##                            path = path + '/' + children.friendly_class_name() + '[' + str(i) + ']'
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
                        text= str(text) + '_dropdown'
                     elif tag == 'CheckBox':
                        tag ='checkbox'
                        text= str(text) + '_chkbox'
                     elif tag == 'ListView':
                        tag = 'list'
                        text= str(text) + '_list'
                     elif tag == 'ListBox':
                        tag = 'list'
                        text= str(text) + '_list'
                     elif tag == 'TabControl':
                        tag = 'tab'
                        text= str(text) + '_tab'
                     elif tag == 'DateTimePicker':
                        tag = 'datepicker'
                        text= str(text) + '_dtp'
                     else:
                        tag = 'label'
                        text= str(text) + '_lbl'


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
                        if not flag:
                            ne.append({"custname":text,
                                    "tag":tag,
                                    "url":url,
                                    'control_id':control_id,
                                    'parent':parent,
                                    'xpath' : path,
                                    'hiddentag':hiddentag,
                                    'top': top,
                                    'left': left,
                                    'height': height,
                                    'width': width,
                                    'x_screen':x_screen,
                                    'y_screen':y_screen
                                    })
                        else:
                            print 'This element is duplicate'
                 else:
                    text = ''
                    handle = children.handle
                    text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem=handle,cache_enable=False).name

##             ch = children.children()
##             for i in range(len(ch)):
##                self.get_all_children(ch[i],ne,i,path,win,winrect)
        except Exception as e:
            print e
        return ne

    def full_scrape(self,app_uia):
        allobjects = {}
        try:
            win = app_uia.top_window()
            ch = win.children()
            a = ''
            ne = []
            obj = launch_keywords.Launch_Keywords()
            obj.set_to_foreground()
            winrect = launch_keywords.win_rect;
            a =  self.get_all_children(ch,ne,0,'',win,winrect)
            import json
##            scraped_object=ldtp.getentireobjectlist(launch_keywords.window_name)
            try:
                img=ninteen_68_desktop_scrape.obj.captureScreenshot()
                img.save('out.png')
                with open("out.png", "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                allobjects['mirror'] =encoded_string.encode('UTF-8').strip()
            except Exception as e:
                print 'Unable to capture the screenshot'
            with open('domelements.json', 'w') as outfile:
                allobjects["view"] = a
                json.dump(allobjects, outfile, indent=4, sort_keys=False)
                outfile.close()

        except Exception as e:
            print e
        return allobjects

##        scraped_object=''
##        try:

##            scraped_object=ldtp.getentireobjectlist(launch_keywords.window_name)
##            img=ninteen_68_desktop_scrape.obj.captureScreenshot()
##            img.save('out.png')
##            with open("out.png", "rb") as image_file:
##                encoded_string = base64.b64encode(image_file.read())
##            import json
##            scraped_object=json.loads(scraped_object)
##            scraped_object1['']=scraped_object
##            scraped_object['mirror'] =encoded_string.encode('UTF-8').strip()

##            with open('domelements.json', 'w') as outfile:
##                json.dump(scraped_object, outfile, indent=4, sort_keys=False)
##                outfile.close()
##            return scraped_object
##        except LdtpExecutionError as exception:
##            pass
##        return scraped_object


##obj = Scrape()
##obj.clickandadd('9584','Calculator','STARTCLICKANDADD')
##import time
##time.sleep(10)
##abc=obj.clickandadd('5584','Calculator','STOPCLICKANDADD')
##print 'ABCCCCCCCCCCCC',abc
##obj.full_scrape('Software Center')