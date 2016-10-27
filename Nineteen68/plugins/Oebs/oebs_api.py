#javaAccessBridgeHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import Queue
from ctypes import *
from ctypes.wintypes import *
import win32gui
import os
import winuser
import logging

#Some utility functions to help with function defines

def _errcheck(res, func, args):
    if not res:
        raise RuntimeError("Result %s" % res)
    return res

def _fixBridgeFunc(restype,name,*argtypes,**kwargs):
    try:
        func=getattr(bridgeDll,name)
    except AttributeError:
        logging.warning("%s not found in Java Access Bridge dll"%name)
        return
    func.restype=restype
    func.argtypes=argtypes
    if kwargs.get('errcheck'):
        func.errcheck=_errcheck

#Load the first available access bridge dll
legacyAccessBridge=True
try:
    bridgeDll=getattr(cdll,'windowsAccessBridge-64')
    legacyAccessBridge=False
except WindowsError:
    try:
##      os.chdir("C:\Program Files\Java Access Bridge\installerFiles")
##      bridgeDll=cdll.LoadLibrary("WindowsAccessBridge.dll")
        bridgeDll=cdll.windowsaccessbridge
        print "LOADED"
    except WindowsError:
        bridgeDll=None

#Definitions of access bridge types, structs and prototypes

jint=c_int
jString=c_wchar
jfloat=c_float
class JOBJECT64(c_int if legacyAccessBridge else c_int64):
    pass

MAX_STRING_SIZE=1024
SHORT_STRING_SIZE=256

class AccessBridgeVersionInfo(Structure):
    _fields_=[
        ('VMVersion',WCHAR*SHORT_STRING_SIZE),
        ('bridgeJavaClassVersion',WCHAR*SHORT_STRING_SIZE),
        ('bridgeJavaDLLVersion',WCHAR*SHORT_STRING_SIZE),
        ('bridgeWinDLLVersion',WCHAR*SHORT_STRING_SIZE),
    ]

class AccessibleContextInfo(Structure):
    _fields_=[
        ('name',WCHAR*MAX_STRING_SIZE),
        ('description',WCHAR*MAX_STRING_SIZE),
        ('role',WCHAR*SHORT_STRING_SIZE),
        ('role_en_US',WCHAR*SHORT_STRING_SIZE),
        ('states',WCHAR*SHORT_STRING_SIZE),
        ('states_en_US',WCHAR*SHORT_STRING_SIZE),
        ('indexInParent',jint),
        ('childrenCount',jint),
        ('x',jint),
        ('y',jint),
        ('width',jint),
        ('height',jint),
        ('accessibleComponent',BOOL),
        ('accessibleAction',BOOL),
        ('accessibleSelection',BOOL),
        ('accessibleText',BOOL),
        ('accessibleValue',BOOL),
        ('accessibleInterfaces',BOOL),
    ]

class AccessibleTextInfo(Structure):
    _fields_=[
        ('charCount',jint),
        ('caretIndex',jint),
        ('indexAtPoint',jint),
    ]

class AccessibleTextItemsInfo(Structure):
    _fields_=[
        ('letter',WCHAR),
        ('word',WCHAR*SHORT_STRING_SIZE),
        ('sentence',WCHAR*MAX_STRING_SIZE),
    ]

class AccessibleTextSelectionInfo(Structure):
    _fields_=[
        ('selectionStartIndex',jint),
        ('selectionEndIndex',jint),
        ('selectedText',WCHAR*MAX_STRING_SIZE),
    ]

class AccessibleTextRectInfo(Structure):
    _fields_=[
        ('x',jint),
        ('y',jint),
        ('width',jint),
        ('height',jint),
    ]

class AccessibleTextAttributesInfo(Structure):
    _fields_=[
        ('bold',BOOL),
        ('italic',BOOL),
        ('underline',BOOL),
        ('strikethrough',BOOL),
        ('superscript',BOOL),
        ('subscript',BOOL),
        ('backgroundColor',WCHAR*SHORT_STRING_SIZE),
        ('foregroundColor',WCHAR*SHORT_STRING_SIZE),
        ('fontFamily',WCHAR*SHORT_STRING_SIZE),
        ('fontSize',jint),
        ('alignment',jint),
        ('bidiLevel',jint),
        ('firstLineIndent',jfloat),
        ('LeftIndent',jfloat),
        ('rightIndent',jfloat),
        ('lineSpacing',jfloat),
        ('spaceAbove',jfloat),
        ('spaceBelow',jfloat),
        ('fullAttributesString',WCHAR*MAX_STRING_SIZE),
    ]

class AccessibleTableInfo(Structure):
    _fields_=[
        ("caption", JOBJECT64 ),
        ("summary", JOBJECT64 ),
        ("rowCount", jint),
        ("columnCount", jint),
        ("accessibleContext", JOBJECT64 ),
        ("accessibleTable", JOBJECT64),

    ]
class AccessibleTableCellInfo(Structure):
    _fields_=[
        ("accessibleContext", JOBJECT64),
        ("index", jint),
        ("row", jint),
        ("column", jint),
        ("rowExtent", jint),
        ("columnExtent", jint),
        ("isSelected", BOOL),

    ]
class VisibleChildrenInfo(Structure):
    _fields_ = [
         ("returnedChildrenCount", jint),
        ("children", JOBJECT64 *SHORT_STRING_SIZE),
    ]
MAX_RELATION_TARGETS = 25
MAX_RELATIONS = 5

class AccessibleRelationInfo(Structure):
    _fields_ = [
        ("key", WCHAR * SHORT_STRING_SIZE),
        ("targetCount", jint),
        ("targets", JOBJECT64 * MAX_RELATION_TARGETS),
    ]

class AccessibleRelationSetInfo(Structure):
    _fields_ = [
        ("relationCount", jint),
        ("relations", AccessibleRelationInfo * MAX_RELATIONS),
    ]

MAX_ACTION_INFO = 256
MAX_ACTIONS_TO_DO = 32

class AccessibleActionInfo(Structure):
    _fields_ = (
        ("name", c_wchar * SHORT_STRING_SIZE),
    )

class AccessibleActions(Structure):
    _fields_ = (
        ("actionsCount", jint),
        ("actionInfo", AccessibleActionInfo * MAX_ACTION_INFO),
    )

class AccessibleActionsToDo(Structure):
    _fields_ = (
        ("actionsCount", jint),
        ("actions", AccessibleActionInfo * MAX_ACTIONS_TO_DO),
    )

AccessBridge_SetMouseClickedFP=CFUNCTYPE(None,c_long,JOBJECT64,JOBJECT64)
##AccessBridge_FocusGainedFP=CFUNCTYPE(None,c_long,JOBJECT64,JOBJECT64)
AccessBridge_PropertyStateChangeFP=CFUNCTYPE(None,c_long,JOBJECT64,JOBJECT64,c_wchar_p,c_wchar_p)
##AccessBridge_PropertyCaretChangeFP=CFUNCTYPE(None,c_long,JOBJECT64,JOBJECT64,c_int,c_int)
##AccessBridge_PropertyActiveDescendentChangeFP=CFUNCTYPE(None,c_long,JOBJECT64,JOBJECT64,JOBJECT64,JOBJECT64)

#Appropriately set the return and argument types of all the access bridge dll functions
if bridgeDll:
    _fixBridgeFunc(None,'Windows_run')
    _fixBridgeFunc(None,'setMouseClickedFP',c_void_p)
    _fixBridgeFunc(None,'setMousePressedFP',c_void_p)
    _fixBridgeFunc(None,'setFocusGainedFP',c_void_p)
    _fixBridgeFunc(None,'setPropertyStateChangeFP',c_void_p)
    _fixBridgeFunc(None,'setPropertyCaretChangeFP',c_void_p)
    _fixBridgeFunc(None,'setPropertyActiveDescendentChangeFP',c_void_p)
    _fixBridgeFunc(None,'releaseJavaObject',c_long,JOBJECT64)
    _fixBridgeFunc(BOOL,'getVersionInfo',POINTER(AccessBridgeVersionInfo),errcheck=True)
    _fixBridgeFunc(BOOL,'isJavaWindow',HWND)
    _fixBridgeFunc(BOOL,'isSameObject',c_long,JOBJECT64,JOBJECT64)
    _fixBridgeFunc(BOOL,'getAccessibleContextFromHWND',HWND,POINTER(c_long),POINTER(JOBJECT64),errcheck=True)
    _fixBridgeFunc(HWND,'getHWNDFromAccessibleContext',c_long,JOBJECT64,errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleContextAt',c_long,JOBJECT64,jint,jint,POINTER(JOBJECT64),errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleContextWithFocus',HWND,POINTER(c_long),POINTER(JOBJECT64),errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleContextInfo',c_long,JOBJECT64,POINTER(AccessibleContextInfo),errcheck=True)
    _fixBridgeFunc(JOBJECT64,'getAccessibleChildFromContext',c_long,JOBJECT64,jint,errcheck=True)
    _fixBridgeFunc(JOBJECT64,'getAccessibleParentFromContext',c_long,JOBJECT64)
    _fixBridgeFunc(BOOL,'getAccessibleRelationSet',c_long,JOBJECT64,POINTER(AccessibleRelationSetInfo),errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleTextInfo',c_long,JOBJECT64,POINTER(AccessibleTextInfo),jint,jint,errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleTextItems',c_long,JOBJECT64,POINTER(AccessibleTextItemsInfo),jint,errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleTextSelectionInfo',c_long,JOBJECT64,POINTER(AccessibleTextSelectionInfo),errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleTextAttributes',c_long,JOBJECT64,jint,POINTER(AccessibleTextAttributesInfo),errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleTextLineBounds',c_long,JOBJECT64,jint,POINTER(jint),POINTER(jint),errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleTextRange',c_long,JOBJECT64,jint,jint,POINTER(c_wchar),c_short,errcheck=True)
    _fixBridgeFunc(BOOL,'getCurrentAccessibleValueFromContext',c_long,JOBJECT64,POINTER(c_wchar),c_short,errcheck=True)
    _fixBridgeFunc(BOOL,'selectTextRange',c_long,JOBJECT64,c_int,c_int,errcheck=True)
    _fixBridgeFunc(BOOL,'getTextAttributesInRange',c_long,JOBJECT64,c_int,c_int,POINTER(AccessibleTextAttributesInfo),POINTER(c_short),errcheck=True)
    _fixBridgeFunc(JOBJECT64,'getTopLevelObject',c_long,JOBJECT64,errcheck=True)
    _fixBridgeFunc(c_int,'getObjectDepth',c_long,JOBJECT64)
    _fixBridgeFunc(JOBJECT64,'getActiveDescendent',c_long,JOBJECT64)
    _fixBridgeFunc(BOOL,'requestFocus',c_long,JOBJECT64,errcheck=True)
    _fixBridgeFunc(BOOL,'setCaretPosition',c_long,JOBJECT64,c_int,errcheck=True)
    _fixBridgeFunc(BOOL,'getCaretLocation',c_long,JOBJECT64,POINTER(AccessibleTextRectInfo),jint,errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleActions',c_long,JOBJECT64,POINTER(AccessibleActions),errcheck=True)
    _fixBridgeFunc(BOOL,'doAccessibleActions',c_long,JOBJECT64,POINTER(AccessibleActionsToDo),POINTER(jint))
    _fixBridgeFunc(BOOL,'setTextContents',c_long,JOBJECT64,POINTER(jString),errcheck=True)
    _fixBridgeFunc(JOBJECT64,'getAccessibleSelectionFromContext',c_long,JOBJECT64,errcheck=True)
    _fixBridgeFunc(JOBJECT64,'getVisibleChildren',c_long,JOBJECT64,jint,POINTER(VisibleChildrenInfo),errcheck=True)
    _fixBridgeFunc(BOOL,'selectAllAccessibleSelectionFromContext',c_long,JOBJECT64,errcheck=True)
    _fixBridgeFunc(BOOL,'addAccessibleSelectionFromContext',c_long,JOBJECT64,jint,errcheck=True)
    _fixBridgeFunc(BOOL,'removeAccessibleSelectionFromContext',c_long,JOBJECT64,jint,errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleTableInfo',c_long,JOBJECT64,POINTER(AccessibleTableInfo),errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleTableCellInfo',c_long,JOBJECT64,jint,jint,POINTER(AccessibleTableCellInfo),errcheck=True)

#NVDA specific code

isRunning=False
vmIDsToWindowHandles={}
internalFunctionQueue=Queue.Queue(1000)
internalFunctionQueue.__name__="JABHandler.internalFunctionQueue"

def internalQueueFunction(func,*args,**kwargs):
    internalFunctionQueue.put_nowait((func,args,kwargs))

class JABContext(object):

    def __init__(self,hwnd=None,vmID=None,accContext=None):
        if hwnd and not vmID:
            vmID=c_int()
            accContext=JOBJECT64()
            bridgeDll.getAccessibleContextFromHWND(hwnd,byref(vmID),byref(accContext))
            vmID=vmID.value
            #Record  this vm ID and window handle for later use with other objects
            vmIDsToWindowHandles[vmID]=hwnd
        elif vmID and not hwnd:
            hwnd=vmIDsToWindowHandles.get(vmID)
            if not hwnd:
                topAC=bridgeDll.getTopLevelObject(vmID,accContext)
                hwnd=bridgeDll.getHWNDFromAccessibleContext(vmID,topAC)
                bridgeDll.releaseJavaObject(vmID,topAC)
                #Record  this vm ID and window handle for later use with other objects
                vmIDsToWindowHandles[vmID]=hwnd
        self.hwnd=hwnd
        self.vmID=vmID
        self.accContext=accContext

    def __del__(self):
        if isRunning:
            try:
                bridgeDll.releaseJavaObject(self.vmID,self.accContext)
            except:
                logging.debugWarning("Error releasing java object",exc_info=True)


    def __eq__(self,jabContext):
        if self.vmID==jabContext.vmID and bridgeDll.isSameObject(self.vmID,self.accContext,jabContext.accContext):
            return True
        else:
            return False

    def __ne__(self,jabContext):
        if self.vmID!=jabContext.vmID or not bridgeDll.isSameObject(self.vmID,self.accContext,jabContext.accContext):
            return True
        else:
            return False

    def getVersionInfo(self):
        info=AccessBridgeVersionInfo()
        bridgeDll.getVersionInfo(self.vmID,byref(info))
        return info

    def getAccessibleContextInfo(self):
        info=AccessibleContextInfo()
        bridgeDll.getAccessibleContextInfo(self.vmID,self.accContext,byref(info))
        return info

    def getAccessibleTextInfo(self,x,y):
        textInfo=AccessibleTextInfo()
        bridgeDll.getAccessibleTextInfo(self.vmID,self.accContext,byref(textInfo),x,y)
        return textInfo

    def getAccessibleTextItems(self,index):
        textItemsInfo=AccessibleTextItemsInfo()
        bridgeDll.getAccessibleTextItems(self.vmID,self.accContext,byref(textItemsInfo),index)
        return textItemsInfo

    def getAccessibleTextSelectionInfo(self):
        textSelectionInfo=AccessibleTextSelectionInfo()
        bridgeDll.getAccessibleTextSelectionInfo(self.vmID,self.accContext,byref(textSelectionInfo))
        return textSelectionInfo

    def getAccessibleTextRange(self,start,end):
        length=((end+1)-start)
        if length<=0:
            return u""
        text=create_unicode_buffer(length+1)
        bridgeDll.getAccessibleTextRange(self.vmID,self.accContext,start,end,text,length)
        return text.value

    def getAccessibleTextLineBounds(self,index):
        index=max(index,0)
        logging.debug("lineBounds: index %s"%index)
        #Java returns end as the last character, not end as past the last character
        startIndex=c_int()
        endIndex=c_int()
        bridgeDll.getAccessibleTextLineBounds(self.vmID,self.accContext,index,byref(startIndex),byref(endIndex))
        start=startIndex.value
        end=endIndex.value
        logging.debug("line bounds: start %s, end %s"%(start,end))
        if end<start or start<0:
            # Invalid or empty line.
            return (0,-1)
        ok=False
        # OpenOffice sometimes returns offsets encompassing more than one line, so try to narrow them down.
        # Try to retract the end offset.
        while not ok:
            bridgeDll.getAccessibleTextLineBounds(self.vmID,self.accContext,end,byref(startIndex),byref(endIndex))
            tempStart=max(startIndex.value,0)
            tempEnd=max(endIndex.value,0)
            logging.debug("line bounds: tempStart %s, tempEnd %s"%(tempStart,tempEnd))
            if tempStart>(index+1):
                # This line starts after the requested index, so set end to point at the line before.
                end=tempStart-1
            else:
                ok=True
        ok=False
        # Try to retract the start.
        while not ok:
            bridgeDll.getAccessibleTextLineBounds(self.vmID,self.accContext,start,byref(startIndex),byref(endIndex))
            tempStart=max(startIndex.value,0)
            tempEnd=max(endIndex.value,0)
            logging.debug("line bounds: tempStart %s, tempEnd %s"%(tempStart,tempEnd))
            if tempEnd<(index-1):
                # This line ends before the requested index, so set start to point at the line after.
                start=tempEnd+1
            else:
                ok=True
        logging.debug("line bounds: returning %s, %s"%(start,end))
        return (start,end)


    def getAccessibleParentFromContext(self):
        accContext=bridgeDll.getAccessibleParentFromContext(self.vmID,self.accContext)
        if accContext:
            return self.__class__(self.hwnd,self.vmID,accContext)
        else:
            return None

    def getAccessibleChildFromContext(self,index):
        accContext=bridgeDll.getAccessibleChildFromContext(self.vmID,self.accContext,index)
        if accContext:
            return self.__class__(self.hwnd,self.vmID,accContext)
        else:
            return None

    def getAccessibleSelectionFromContext(self,index):
        accContext=bridgeDll.getAccessibleSelectionFromContext(self.vmID,self.accContext,index)
        if accContext:
            return self.__class__(self.hwnd,self.vmID,accContext)
        else:
            return None

    def getActiveDescendent(self):
        accContext=bridgeDll.getActiveDescendent(self.vmID,self.accContext)
        if accContext:
            return self.__class__(self.hwnd,self.vmID,accContext)
        else:
            return None

    def getAccessibleContextAt(self,x,y):
        newAccContext=JOBJECT64()
        res=bridgeDll.getAccessibleContextAt(self.vmID,self.accContext,x,y,byref(newAccContext))
        if not res or not newAccContext:
            return None
        if not bridgeDll.isSameObject(self.vmID,newAccContext,self.accContext):
            return self.__class__(self.hwnd,self.vmID,newAccContext)
        elif newAccContext!=self.accContext:
            bridgeDll.releaseJavaObject(self.vmID,newAccContext)
        return None

    def getCurrentAccessibleValueFromContext(self):
        buf=create_unicode_buffer(SHORT_STRING_SIZE+1)
        bridgeDll.getCurrentAccessibleValueFromContext(self.vmID,self.accContext,buf,SHORT_STRING_SIZE)
        return buf.value

    def selectTextRange(self,start,end):
        bridgeDll.selectTextRange(start,end)

    def setCaretPosition(self,offset):
        bridgeDll.setCaretPosition(self.vmID,self.accContext,offset)

    def getTextAttributesInRange(self, startIndex, endIndex):
        attributes = AccessibleTextAttributesInfo()
        length = c_short()
        bridgeDll.getTextAttributesInRange(self.vmID, self.accContext, startIndex, endIndex, byref(attributes), byref(length))
        return attributes, length.value

    def getAccessibleRelationSet(self):
        relations = AccessibleRelationSetInfo()
        bridgeDll.getAccessibleRelationSet(self.vmID, self.accContext, byref(relations))
        return relations

    def setTextContents(self,string):
       return bridgeDll.setTextContents(self.vmID,self.accContext,string)

    def getAccessibleActions(self):
        actions=AccessibleActions()
        bridgeDll.getAccessibleActions(self.vmID,self.accContext,byref(actions))
        return actions

    def doAccessibleActions(self,actionCount,action):
        actionstodo = AccessibleActionsToDo()
        actionstodo.actionsCount = actionCount
        actionstodo.actions[0].name = action
        res = jint()
        result = bridgeDll.doAccessibleActions(self.vmID,self.accContext,byref(actionstodo),byref(res))
        return result

    def selectAllAccessibleSelectionFromContext(self):
        bridgeDll.selectAllAccessibleSelectionFromContext(self.vmID,self.accContext)

    def addAccessibleSelectionFromContext(self,index):
        bridgeDll.addAccessibleSelectionFromContext(self.vmID,self.accContext,index)

    def removeAccessibleSelectionFromContext(self,index):
        bridgeDll.removeAccessibleSelectionFromContext(self.vmID,self.accContext,index)

    def getAccessibleTableInfo(self):
        info=AccessibleTableInfo()
        bridgeDll.getAccessibleTableInfo(self.vmID,self.accContext,byref(info))
        return info

    def getAccessibleTableCellInfo(self,x,y):
        info=AccessibleTableCellInfo()
        bridgeDll.getAccessibleTableCellInfo(self.vmID,self.accContext,x,y,byref(info))
        return info

    def getTopLevelObject(self):
        accContext=bridgeDll.getTopLevelObject(self.vmID,self.accContext)
        if accContext:
            return self.__class__(self.hwnd,self.vmID,accContext)
        else:
            return None

    def releaseJavaObject(self):
        bridgeDll.releaseJavaObject(self.hwnd,self.accContext)

##@AccessBridge_FocusGainedFP
def internal_event_focusGained(vmID, event,source):
    internalQueueFunction(event_gainFocus,vmID,source)
    bridgeDll.releaseJavaObject(vmID,event)

@AccessBridge_SetMouseClickedFP
def mouseclickeddelegatefp(vmID, event, source):
    internalQueueFunction(abc,vmID, source)
    bridgeDll.releaseJavaObject(vmID, source)
    bridgeDll.releaseJavaObject(vmID, event)

def abc(vmID,accContext):
    bridgeDll.releaseJavaObject(vmID, accContext)

def event_gainFocus(vmID,accContext):
    tempContext=accContext
    while tempContext:
        try:
            tempContext=bridgeDll.getActiveDescendent(vmID,tempContext)
            print "eventgain"
        except:
            tempContext=None
        try:
            depth=bridgeDll.getObjectDepth(vmID,tempContext)
        except:
            depth=-1
        if tempContext and (depth<=0 or bridgeDll.isSameObject(vmID,accContext,tempContext)):
            tempContext=None
        if tempContext:
            bridgeDll.releaseJavaObject(vmID,accContext)
            accContext=tempContext
    jabContext=JABContext(vmID=vmID,accContext=accContext)
    if not winUser.isDescendantWindow(winUser.getForegroundWindow(),jabContext.hwnd):
        return
    # focus=eventHandler.lastQueuedFocusObject
    # if (isinstance(focus,NVDAObjects.JAB.JAB) and focus.jabContext==jabContext):
        # return
    # obj=NVDAObjects.JAB.JAB(jabContext=jabContext)
    # if obj.role==controlTypes.ROLE_UNKNOWN:
        # return
    # eventHandler.queueEvent("gainFocus",obj)

##@AccessBridge_PropertyActiveDescendentChangeFP
def internal_event_activeDescendantChange(vmID, event,source,oldDescendant,newDescendant):
    internalQueueFunction(event_gainFocus,vmID,newDescendant)
    for accContext in [event,oldDescendant]:
        bridgeDll.releaseJavaObject(vmID,accContext)

@AccessBridge_PropertyStateChangeFP
def internal_event_stateChange(vmID,event,source,oldState,newState):
##  internalQueueFunction(event_stateChange,vmID,source,oldState,newState)
    bridgeDll.releaseJavaObject(vmID, source)
    bridgeDll.releaseJavaObject(vmID,event)

def event_stateChange(vmID,accContext,oldState,newState):
    jabContext=JABContext(vmID=vmID,accContext=accContext)
    # focus=api.getFocusObject()
    #For broken tabs and menus, we need to watch for things being selected and pretend its a focus change
    # stateList=newState.split(',')
    # if "focused" in stateList or "selected" in stateList:
    #     obj=NVDAObjects.JAB.JAB(jabContext=jabContext)
    #     if not obj:
    #         return
    #     if focus!=obj and eventHandler.lastQueuedFocusObject!=obj and obj.role in (controlTypes.ROLE_MENUITEM,controlTypes.ROLE_TAB,controlTypes.ROLE_MENU):
    #         eventHandler.queueEvent("gainFocus",obj)
    #         return
    # if isinstance(focus,NVDAObjects.JAB.JAB) and focus.jabContext==jabContext:
    #     obj=focus
    # else:
    #     obj=NVDAObjects.JAB.JAB(jabContext=jabContext)
    #     if not obj:
    #         return
    # eventHandler.queueEvent("stateChange",obj)

##@AccessBridge_PropertyCaretChangeFP
def internal_event_caretChange(vmID, event,source,oldPos,newPos):
    if oldPos<0 and newPos>=0:
        internalQueueFunction(event_gainFocus,vmID,source)
    internalQueueFunction(event_caret,vmID,source)
    bridgeDll.releaseJavaObject(vmID,event)

def event_caret(vmID, accContext):
    jabContext = JABContext(vmID=vmID, accContext=accContext)
    # focus = api.getFocusObject()
    # if isinstance(focus, NVDAObjects.JAB.JAB) and focus.jabContext == jabContext:
    #     obj = focus
    # else:
    #     obj = NVDAObjects.JAB.JAB(jabContext=jabContext)
    #     if not obj:
    #         return
    # eventHandler.queueEvent("caret", obj)

def event_enterJavaWindow(hwnd):
    vmID=c_int()
    accContext=JOBJECT64()
    try:
        bridgeDll.getAccessibleContextFromHWND(hwnd,byref(vmID),byref(accContext))
    except:
        return
    vmID=vmID.value
    vmIDsToWindowHandles[vmID]=hwnd
    # lastFocus=eventHandler.lastQueuedFocusObject
    # if isinstance(lastFocus,NVDAObjects.JAB.JAB) and lastFocus.windowHandle==hwnd:
    #     return
    internalQueueFunction(event_gainFocus,vmID,accContext)

def isJavaWindow(hwnd):
    if not bridgeDll:
        return False
    bridgeDll.Windows_run()
    win32gui.PumpWaitingMessages()
    return bridgeDll.isJavaWindow(hwnd)

def setpropertychange():
    bridgeDll.setPropertyStateChangeFP(internal_event_stateChange)

def initialize():
    global isRunning
    if not bridgeDll:
        raise NotImplementedError("dll not available")
    bridgeDll.Windows_run()
    #Accept wm_copydata and any wm_user messages from other processes even if running with higher privilages
    ChangeWindowMessageFilter=getattr(windll.user32,'ChangeWindowMessageFilter',None)
    if ChangeWindowMessageFilter:
        if not ChangeWindowMessageFilter(winUser.WM_COPYDATA,1):
            raise WinError()
        for msg in xrange(winUser.WM_USER+1,65535):
            if not ChangeWindowMessageFilter(msg,1):
                raise WinError()
    #Register java events
##  bridgeDll.setFocusGainedFP(internal_event_focusGained)
##  bridgeDll.setPropertyActiveDescendentChangeFP(internal_event_activeDescendantChange)
##  win32gui.PumpWaitingMessages()
    win32gui.PumpWaitingMessages()
    bridgeDll.setPropertyStateChangeFP(internal_event_stateChange)
    bridgeDll.setMouseClickedFP(mouseclickeddelegatefp)
##  win32gui.PumpWaitingMessages()
##  bridgeDll.setPropertyCaretChangeFP(internal_event_caretChange)
##  win32gui.PumpWaitingMessages()
##  bridgeDll.setMouseClickedFP(mouseclickeddelegatefp)
##  bridgeDll.setMousePressedFP(mouseclickeddelegatefp)
##  win32gui.PumpWaitingMessages()
##  bridgeDll.setFocusGainedFP(None)
##  bridgeDll.setPropertyActiveDescendentChangeFP(None)
##  bridgeDll.setPropertyStateChangeFP(None)
##  bridgeDll.setPropertyCaretChangeFP(None)
    isRunning=True

# def pumpAll():
#     if isRunning:
#         queueHandler.flushQueue(internalFunctionQueue)

def terminate():
    global isRunning, bridgeDll
    if not bridgeDll or not isRunning:
        return
    bridgeDll.setFocusGainedFP(None)
    bridgeDll.setPropertyActiveDescendentChangeFP(None)
##  bridgeDll.setPropertyStateChangeFP(None)
    bridgeDll.setPropertyCaretChangeFP(None)
    h=bridgeDll._handle
    bridgeDll=None
    if legacyAccessBridge:
        del cdll.windowsAccessBridge
    else:
        delattr(cdll,'windowsAccessBridge-32')
    windll.kernel32.FreeLibrary(h)
    isRunning=False