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
ctrldownflag = False
stopumpingmsgs = False
pressedescape = False
counter = 0;
objNameArr = []
xpath = []
url = []
text = []
hiddentag = []
custname = []
tag = []
ids = []
ne = []
jsonArray = []
obj_ref = None


class Scrape:

##    def clickandadd(self,operation):
##        if operation == 'STARTCLICKANDADD':
##            try:
##                class OutlookThread(Thread):
##                    def __init__(self):
##                        """Init Worker Thread Class."""
##                        Thread.__init__(self)
##                        self._want_continue = 1
##                        self.start()    # start the thread
##
##                    def run(self):
##                        """Run Worker Thread."""
##                        self.DataToInt = int(launch_keywords.window_pid)
##                        self.currForeWin = win32gui.GetForegroundWindow()
##                        self.PidToCheck = win32process.GetWindowThreadProcessId(self.currForeWin)
##                        if self.PidToCheck[1] == self.DataToInt:
##                            self.objNameArr =  ldtp.getobjectnameatcoords()
##                            print 'object name',self.objNameArr
##                            try:
##                                if self.objNameArr[0] != 'None' and self.objNameArr[1] != 'None':
##                                    self.infoArray =  ldtp.getobjectinfo(self.objNameArr[0], self.objNameArr[1])
##                                    for k in self.infoArray:
##                                        self.objProp = ldtp.getobjectproperty(self.objNameArr[0], self.objNameArr[1],k)
##                                        if 'key' in k:
##                                            custname.append(self.objNameArr[1])
##                                        elif 'class' in k:
##                                            tag.append(self.objProp)
##                                        elif 'obj_index' in k:
##                                            xpath.append(self.objNameArr[1] + ';' + self.objProp )
##                                        elif 'parent' in k:
##                                            url.append(self.objProp)
##                                        elif 'children' in k:
##                                            ids.append(self.objProp)
##                                        elif 'label' in k:
##                                            text.append(self.objProp)
##                                        elif 'window_id' in k:
##                                            rakesh = 1
##                            except LdtpExecutionError as msg:
##                                pass
##                        else:
##                            return True
##
##                    def abort(self):
##                        self._want_continue = 0
##                class StartPump(Thread):
##                    def __init__(self):
##                        """Init Worker Thread Class."""
##                        Thread.__init__(self)
##                        self._want_continue = 1
##                        self.stopumpingmsgs = False
##                        self.ctrldownflag = False
##                        self.start()
##
##                    def run(self):
##
##                        def OnMouseLeftDown(event):
##                            global ctrldownflag
##                            if (self.stopumpingmsgs == True):
##                                self.hm.UnhookKeyboard()
##                                self.hm.UnhookMouse()
##                                ctypes.windll.user32.PostQuitMessage(0)
##                                return True
##                            if (ctrldownflag is True):
##                                return True
##                            else:
##                                obj = OutlookThread()
##                                return False
##
##
##                        def OnKeyDown(event):
##                            global ctrldownflag
##                            if (self.stopumpingmsgs == True):
##                                self.hm.UnhookKeyboard()
##                                self.hm.UnhookMouse()
##                                ctypes.windll.user32.PostQuitMessage(0)
##                                return True
##                            else:
##                                if (event.Key == 'Lcontrol'):
##                                    ctrldownflag = True
##                                    return True
##                                else:
##                                    ctrldownflag = False
##                                    return True
##
##                        def OnKeyUp(event):
##                            global ctrldownflag
##                            ctrldownflag = False
##                            return True
##                        def FinalJson():
##                            global objNameArr
##                            global ne
##                            global jsonArray
##                            global custname
##                            global tag
##                            global xpath
##                            global url
##                            global ids
##                            global text
##                            try:
##                                for i in range(0,len(custname)):
##                                    ne.append({'xpath': xpath[i], 'tag': tag[i],
##                                                'url': url[i], 'text': text[i],
##                                                'id': ids[i], 'custname': custname[i],
##                                                'hiddentag': 'No'})
##                                jsonArray = {"view": ne}
##                                print 'json array',jsonArray
##                                with open('domelements.json', 'w') as outfile:
##                                    json.dump(jsonArray, outfile, indent=4, sort_keys=False)
##                                outfile.close()
##                                ne = []
##                                jsonArray = []
##                                custname =[]
##                                tag = []
##                                xpath = []
##                                url = []
##                                ids = []
##                                text = []
##                            except IndexError as esxception:
##                                ctypes.windll.user32.PostQuitMessage(0)
##
##                        self.hm = pyHook.HookManager()
##                        self.hm.KeyDown = OnKeyDown
##                        self.hm.KeyUp = OnKeyUp
##                        self.hm.MouseLeftDown = OnMouseLeftDown
##                        self.hm.HookKeyboard()
##                        self.hm.HookMouse()
##                        pythoncom.PumpMessages()
##                        FinalJson()
##
##                    def StopPump(self):
##                        self.stopumpingmsgs = True
##                        wsh = win32com.client.Dispatch("WScript.Shell")
##                        wsh.SendKeys("^")
##                global obj_ref
##                obj_ref = StartPump()
##
##            except Exception as exception:
##                pass
##        elif operation == 'STOPCLICKANDADD':
##            try:
##                global obj_ref
##                obj_ref.StopPump()
####                print jsonArray
##                return jsonArray
##            except Exception as exception:
##                pass
####        except Exception as esxception:
####            c.send("FAIL" + "\n")
####            pass

    def get_all_children(self,ch,ne,i,path,win,winrect):
        try:
            for i in range (len(ch)):
                 hiddentag = 'Yes'
                 text = ''
                 parent = ''
                 coordinates = ''
                 children = ch[i]
                 tag = children.friendly_class_name()
                 if tag == 'Button' or tag =='RadioButton' or tag == 'Edit' or tag == 'ComboBox' or tag == 'Static' or tag == 'GroupBox' or tag == 'CheckBox' or tag== 'ListView' or tag == 'ListBox'or tag == 'TreeView':
                     coordinates = children.client_rect()
                     cor = children.rectangle()
                     properties = json.loads(json.dumps(children.get_properties(    ), default=lambda x: str(x)))
                     if properties['is_visible'] == True :
                         properties["url"] =  win.texts()[0] if len(win.texts())>0 else ""
                         properties['control_id'] = children.element_info.control_id
                         properties['parent'] = children.element_info.parent.class_name
                         handle = children.handle
                         text = pywinauto.uia_element_info.UIAElementInfo(handle_or_elem=handle,cache_enable=False).name
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
                         else:
                            tag = 'label'
                            text= str(text) + '_lbl'

                         left = 0
                         top = 0
                         width = coordinates.width()
                         height = coordinates.height()
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
                                        'width': width
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
##            for i in range (len(ch)):
##                path =ch[i].element_info.parent.class_name
##                path = path + '[' + str(i) + ']'
            a =  self.get_all_children(ch,ne,0,'',win,winrect)
            import json
##            scraped_object=ldtp.getentireobjectlist(launch_keywords.window_name)
            img=ninteen_68_desktop_scrape.obj.captureScreenshot()
            img.save('out.png')
            with open("out.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            allobjects['mirror'] =encoded_string.encode('UTF-8').strip()
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