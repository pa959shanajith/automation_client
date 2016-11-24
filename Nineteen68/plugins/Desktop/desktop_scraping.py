#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     17-11-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pyHook
import pythoncom
import ctypes
import win32gui
import win32api
import ldtp
import time
import json
import win32com.client
import win32process
from threading import Thread
from ldtp import *
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

    def clickandadd(self,process_id,page_title,operation):
        if operation == 'STARTCLICKANDADD':
            try:
                class OutlookThread(Thread):
                    def __init__(self):
                        """Init Worker Thread Class."""
                        Thread.__init__(self)
                        self._want_continue = 1
                        self.start()    # start the thread

                    def run(self):
                        """Run Worker Thread."""
                        self.DataToInt = int(process_id)
                        self.currForeWin = win32gui.GetForegroundWindow()
                        self.PidToCheck = win32process.GetWindowThreadProcessId(self.currForeWin)
                        if self.PidToCheck[1] == self.DataToInt:
                            self.objNameArr =  ldtp.getobjectnameatcoords()
                            print 'object name',self.objNameArr
                            try:
                                if self.objNameArr[0] != 'None' and self.objNameArr[1] != 'None':
                                    self.infoArray =  ldtp.getobjectinfo(self.objNameArr[0], self.objNameArr[1])
                                    for k in self.infoArray:
                                        self.objProp = ldtp.getobjectproperty(self.objNameArr[0], self.objNameArr[1],k)
                                        if 'key' in k:
                                            custname.append(self.objNameArr[1])
                                        elif 'class' in k:
                                            tag.append(self.objProp)
                                        elif 'obj_index' in k:
                                            xpath.append(self.objNameArr[1] + ';' + self.objProp )
                                        elif 'parent' in k:
                                            url.append(self.objProp)
                                        elif 'children' in k:
                                            ids.append(self.objProp)
                                        elif 'label' in k:
                                            text.append(self.objProp)
                                        elif 'window_id' in k:
                                            rakesh = 1
                            except LdtpExecutionError as msg:
                                pass
                        else:
                            return True

                    def abort(self):
                        self._want_continue = 0
                class StartPump(Thread):
                    def __init__(self):
                        """Init Worker Thread Class."""
                        Thread.__init__(self)
                        self._want_continue = 1
                        self.stopumpingmsgs = False
                        self.ctrldownflag = False
                        self.start()

                    def run(self):

                        def OnMouseLeftDown(event):
                            global ctrldownflag
                            if (self.stopumpingmsgs == True):
                                self.hm.UnhookKeyboard()
                                self.hm.UnhookMouse()
                                ctypes.windll.user32.PostQuitMessage(0)
                                return True
                            if (ctrldownflag is True):
                                return True
                            else:
                                obj = OutlookThread()
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
                                    ctrldownflag = True
                                    return True
                                else:
                                    ctrldownflag = False
                                    return True

                        def OnKeyUp(event):
                            global ctrldownflag
                            ctrldownflag = False
                            return True
                        def FinalJson():
                            global objNameArr
                            global ne
                            global jsonArray
                            global custname
                            global tag
                            global xpath
                            global url
                            global ids
                            global text
                            try:
                                for i in range(0,len(custname)):
                                    ne.append({'xpath': xpath[i], 'tag': tag[i],
                                                'url': url[i], 'text': text[i],
                                                'id': ids[i], 'custname': custname[i],
                                                'hiddentag': 'No'})
                                jsonArray = {"view": ne}
                                print 'json array',jsonArray
                                with open('domelements.json', 'w') as outfile:
                                    json.dump(jsonArray, outfile, indent=4, sort_keys=False)
                                outfile.close()
                                ne = []
                                jsonArray = []
                                custname =[]
                                tag = []
                                xpath = []
                                url = []
                                ids = []
                                text = []
                            except IndexError as esxception:
                                ctypes.windll.user32.PostQuitMessage(0)

                        self.hm = pyHook.HookManager()
                        self.hm.KeyDown = OnKeyDown
                        self.hm.KeyUp = OnKeyUp
                        self.hm.MouseLeftDown = OnMouseLeftDown
                        self.hm.HookKeyboard()
                        self.hm.HookMouse()
                        pythoncom.PumpMessages()
                        FinalJson()

                    def StopPump(self):
                        self.stopumpingmsgs = True
                        wsh = win32com.client.Dispatch("WScript.Shell")
                        wsh.SendKeys("^")
                global obj_ref
                obj_ref = StartPump()

            except Exception as exception:
                pass
        elif operation == 'STOPCLICKANDADD':
            try:
                global obj_ref
                obj_ref.StopPump()
            except Exception as exception:
                pass
##        except Exception as esxception:
##            c.send("FAIL" + "\n")
##            pass


    def full_scrape(self, window_title):
        try:
            print ' full scrape'
            scraped_object=ldtp.getentireobjectlist(window_title)
            with open('domelements.json', 'w') as outfile:
                json.dump(scraped_object, outfile, indent=4, sort_keys=False)
            outfile.close()
        except LdtpExecutionError as exception:
            pass


##obj = Scrape()
##obj.clickandadd('5584','Calculator','STARTCLICKANDADD')
##import time
##time.sleep(10)
##obj.clickandadd('5584','Calculator','STOPCLICKANDADD')
##obj.full_scrape('Software Center')