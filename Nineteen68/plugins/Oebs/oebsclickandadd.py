#-------------------------------------------------------------------------------
# Name:        oebsclickandadd.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     09/09/2015
# Copyright:   (c) rakesh.v 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pyHook
import pythoncom
import ctypes
import win32gui
import win32api
import oebsServer
import oebs_api
import oebs_serverUtilities

import re
import time
import json
import win32com.client
import win32process
import socket
import logging
from threading import Thread
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
accessContext = ''
e = []
a = None
##objects = []


class ClickAndAdd:

    def clickandadd(self,acc,objectmap,windowname,operation):
        if operation == 'STARTCLICKANDADD':
            objectmap={}

            try:
                class OutlookThread(Thread):

                    def __init__(self):
                        """Init Worker Thread Class."""
                        Thread.__init__(self)
                        self._want_continue = 1
                        self.start()    # start the thread

                    def run(self):
                        tempne=[]
                        objects = []
                        activewindowobjects=[]
                        server_obj=oebsServer.OebsKeywords()
                        utilities_obj=oebs_serverUtilities.Utilities()
                        isjavares, hwnd =server_obj.isjavawindow(windowname)
                        self.currForeWin = win32gui.GetForegroundWindow()
                        point=win32gui.GetCursorPos()
                        utilities_obj.activeframename=''
                        utilities_obj.objectDict={}

                        #calling createMap on every click
                        objectmap = utilities_obj.createMap(oebs_api.JABContext(hwnd), tempne,'',0,windowname)

                        #method returns 1 if the coordinates passed of any xpath, is near to the curson postion coordinates
                        #returns 0 if if coordinates doesnot fit into the condition
                        def match(objectInfo,point):
                            expectedx=int(objectInfo[0])+int(objectInfo[2])
                            expectedy=int(objectInfo[1])+int(objectInfo[3])
                            if((point[0] >= int(objectInfo[0]) and point[0]<=expectedx) and (point[1] >= int(objectInfo[1]) and point[1]<=expectedy)):
                                return 1
                            else:
                                return 0


                        #method to find the longest xpath from the object's array and remove the xpath if it ends with panel,scroll pane,desktop pane,viewport,page tab list
                        #and start seacrhing for longest xpath again from object's array
                        def findMatch():
                            max=0
                            value=''
                            for i, val in enumerate(objects):
                                strLen=len(val)
                                if(strLen>max):
                                    max=strLen
                                    value=val

                            string=value
                            newlist2=[]
                            regularexp = re.compile('(internal frame(.*?|\s)*[\]]+)')
                            newxpath = regularexp.findall(string)
                            for i in range(len(newxpath)):
                                newlist2.append(newxpath[i][0])

                            for i in range(len(newlist2)):
                                string=string.replace(newlist2[i],'internal frame')
                            array=string.split('/')
                            for string in reversed(array):
                                if(('panel' in string) or ('scroll pane' in string) or ('desktop pane' in string) or ('viewport' in string)  or('page tab list' in string)):
                                    objects.remove(value)
                                    value=findMatch()
                                    break
                                else:
                                    break
                            return value


                        #method which returns the resultant xpath
                        def lastfilter(arrtostorekey):
                            deleteditemarr=[]
                            notdeleteitemarr=[]
                            longestlengthxpath=arrtostorekey[0]
                            flag=False
                            for index in range(1,len(arrtostorekey)):
                                if(arrtostorekey[index]):
                                    #check for menu bar ,if  check is true it means xpath is of menu bar's
                                    if((arrtostorekey[index] in longestlengthxpath) & (flag== False)):
                                        deleteditemarr.append(arrtostorekey[index])
                                    else:
                                        flag=True
                                        arr=[]
                                        newlist2=[]
                                        string=arrtostorekey[index]
                                        regularexp = re.compile('(internal frame(.*?|\s)*[\]]+)')
                                        newxpath = regularexp.findall(string)
                                        for i in range(len(newxpath)):
                                            newlist2.append(newxpath[i][0])

                                        for i in range(len(newlist2)):
                                            string=string.replace(newlist2[i],'internal frame')

                                        chkforlastindex=string.split('internal frame')

                                        if(chkforlastindex[len(chkforlastindex)-1]):
                                            arr.append(longestlengthxpath)
                                            arr.append(arrtostorekey[index])
                                            newarray=method(arr)

                                            if(newarray):
                                                smallest=newarray[0]
                                                for i in range (len(newarray)):
                                                    if(newarray[i] < smallest):
                                                        smallest=newarray[i]
                                                        longestlengthxpath=arr[i]
                                            else:
                                                for i in range (len(arr)):
                                                    if('menu item' in  arr[i]):
                                                        return arr[i]
                                                    elif('menu ' in  arr[i]):
                                                        return arr[i]


                            if(not (deleteditemarr)):
                                for index in range(len(arrtostorekey)):
                                    if(not(longestlengthxpath == arrtostorekey[index])):
                                        deleteditemarr.append(arrtostorekey[index])

                            for i in range (len(deleteditemarr)):
                                arrtostorekey.remove(deleteditemarr[i])

                            return arrtostorekey[0]


                        def method(arr):
                            compiled1=re.compile('(scroll pane\[(\d+)\])')
                            newarray=[]
                            for index in range(len(arr)):
                                if('internal frame' in str(arr[index])):
                                    newlist1=compiled1.findall(str(arr[index]))
                                    length=len(newlist1)
                                    abc= int(newlist1[length-1][1])
                                    newarray.append(abc)
                                else:
                                    return []
                            return newarray



                        def buildJson(acc,key,xpath,i,window):
                            curaccinfo = acc.getAccessibleContextInfo()
                           # path = getXpath(acc)
                            tagrole = curaccinfo.role
                            tagname = curaccinfo.name
                            text = curaccinfo.name
                            x_coor=curaccinfo.x
                            y_coor=curaccinfo.y
                            width=curaccinfo.width
                            height=curaccinfo.height
                            description = 'null'
                            xpathwithindex = ''
                            if xpath == '':
                                if len(curaccinfo.name.strip()) == 0:
                                    path = curaccinfo.role + '[' + str(i) + ']'

                                else:
                                    if 'panel' in curaccinfo.role:
                                        path = curaccinfo.role  + '[' + str(i) + ']'
                                    else:
                                        path = curaccinfo.role + '[' + str(curaccinfo.name.strip()) + ']'
                            else:
                                if len(curaccinfo.name.strip()) == 0:
                                    path = xpath + '/' + curaccinfo.role  + '[' + str(i) + ']'
                                else:
                                    if 'panel' in curaccinfo.role:
                                        path = xpath + '/' + curaccinfo.role  + '[' + str(i) + ']'
                                    else:
                                        path = xpath + '/' + curaccinfo.role  + '[' + str(curaccinfo.name.strip()) + ']'
                            if path == key:
                                if((point[0] >= x_coor and point[0]<=(x_coor+width)) and (point[1] >= y_coor and point[1]<=(y_coor+height))):

                                    childrencount = curaccinfo.childrenCount
                                    name = ''
                                    indexInParent = 'null'
                                    parentname = ''
                                    parenttag = 'null'
                                    parentchildcount = 'null'
                                    parentindex = 'null'
                                    parentxpathtemp = 'null'
                                    parentxpath = 'null'
                                    if curaccinfo.name is not None:
                                        name = curaccinfo.name
                                    else:
                                        name = ''

                                    indexInParent = curaccinfo.indexInParent
                                    if  acc.getAccessibleParentFromContext() is not None:
                                        parentContext = acc.getAccessibleParentFromContext()
                                        parentInfo = parentContext.getAccessibleContextInfo()
                                        parenttag = parentInfo.role
                                        parentname = parentInfo.name
                                        parentchildcount = parentInfo.childrenCount
                                        parentindex = parentInfo.indexInParent
                                        if(parenttag==tagrole):
                                            lastcharindex = path.rfind(parenttag)
                                            parentxpath = path[0:lastcharindex-1]
                                        elif (parenttag in tagrole):
                                            lastcharindex = path.rfind(parenttag)
                                            parentxpath = path[0:lastcharindex-1]
                                        else:
                                            lastcharindex = path.rfind(parenttag)
                                            parentxpathtemp = path[0:lastcharindex]
                                            if(len(parentname) == 0):
                                                parentxpath = str(parentxpathtemp) + str(parenttag) + '[' + str(parentindex) + ']'
                                            elif( (len(parentname) != 0) and (str(parenttag) != 'panel' ) ) :
                                                parentxpath = str(parentxpathtemp) + str(parenttag) + '[' + str(parentname) + ']'
                                            elif( (len(parentname) != 0) and (str(parenttag) == 'panel' ) ) :
                                                parentxpath = str(parentxpathtemp) + str(parenttag) + '[' + str(parentindex) + ']'

                                    if 'showing' in  curaccinfo.states:
                                        if len( curaccinfo.name) == 0 :
                                            tagname = curaccinfo.role
                                        if curaccinfo.description is not None:
                                            description = curaccinfo.description
                                        else:
                                            description = ''
                                        if curaccinfo.accessibleText == 1:
                                            charinfo = acc.getAccessibleTextInfo(0,1)
                                            text = acc.getAccessibleTextRange(0,charinfo.charCount - 1)
                                        text = text.encode('utf-8').strip()
                                        text = str(text)
                                        text = text.strip()
                                        if len(text) == 0:
                                            text = tagname
                                        text = text.replace('<','')
                                        text = text.replace('>','')
                                        global e

                                        e.append({"custname":text,
                                                "tag":curaccinfo.role,
                                                "xpath":key + ';' + name.strip() + ';' + str(indexInParent)  + ';' + str(childrencount) + ';'+ str(parentname).strip() + ';' + str(parentxpath) + ';' + str(parentchildcount) + ';' + str(parentindex)+ ';' + str(parenttag)+ ';' + str(curaccinfo.role) + ';' + description ,
                                                "hiddentag":'No',
                                                "id":'null',
                                                "text":text,
                                                "url":window,
                                                "x_coor":x_coor,
                                                "y_coor":y_coor,
                                                "width":width,
                                                "height":height})
                            for i in range(curaccinfo.childrenCount):
                                childacc = acc.getAccessibleChildFromContext(i)
                                acc.releaseJavaObject()
                                buildJson(childacc, key, path,i,window)

                        #execution after calling createMap starts from here
                        objects = []
                        key=''
                        arrtostorekey=[]

                        #iterating map, spliting the  key(as coordinates x,y,h,w are concatinated with comma )
                        #storing it into an array and passing to match method along with the cursor position(x,y coordinates) where user has clicked
                        for key in objectmap:
                            arr=key.split(',')
                            data = match(arr,point)

                            #if the result is 1 which means the coordinates of xpath is near by the curson position, is stored in an objects array
                            if data == 1:
                                objects.append(objectmap.get(key))

                        #iterating 4 times and each time calling findMatch method and resultant is storing in arrtostorekey array
                        #if objects array is not empty removing the resultant xpath from objects array and calling again findMatch method
                        for i in range (4):
                            key=findMatch()
                            arrtostorekey.append(key)
                            if(objects):
                                objects.remove(key)
                            else:
                                break

                        #calling lastfilter method passing arrtostorekey array having xpath's which has filtered after 1st check, which gives xpath's near by cursor position
                        #2nd check which gives longest 4 xpath's
                        key=lastfilter(arrtostorekey)

                        #calling buildJson method with key(resultant xpath)
                        buildJson(acc,key,'',0,windowname)

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
                        global counter;
                        counter += 1
                        if counter > 1:
                            wsh = win32com.client.Dispatch("WScript.Shell")
                            wsh.SendKeys("^")
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


                        self.hm = pyHook.HookManager()
                        self.hm.KeyDown = OnKeyDown
                        self.hm.KeyUp = OnKeyUp
                        self.hm.MouseLeftDown = OnMouseLeftDown
                        self.hm.HookKeyboard()
                        self.hm.HookMouse()
                        pythoncom.PumpMessages()
    ##                    FinalJson()

                    def StopPump(self):
    ##                    print 'STOP pump'
                        self.stopumpingmsgs = True
                        wsh = win32com.client.Dispatch("WScript.Shell")
                        wsh.SendKeys("^")
                global a
                a = StartPump()
            except Exception as esxception:
                ab = 9

        elif operation == 'STOPCLICKANDADD':
            try:
                global e
                ie = {'view': e}
                scrapeJson =  json.dumps(ie)
                global e
                e = []
                global a
                a.StopPump()
                return scrapeJson
            except Exception as esxception:
                print esxception
                pass
