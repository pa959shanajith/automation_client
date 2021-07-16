# -*- coding: UTF-8 -*-
#javaAccessBridgeHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2007-2017 NV Access Limited, Peter Vágner, Renaud Paquay, Babbage B.V.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.


import queue # Python 3 import
from ctypes import *
from ctypes.wintypes import *
from ctypes import wintypes
import time
import win32gui
from constants import *
import logging
log=logging.getLogger('oebs_api.py')
import winuser
import oebs_api2
import oebs_event_handler
import oebs_control_types
import oebs_jab_object
import oebs_click_and_add


from oebs_xpath_generator import PathGenerator
previousMouseEvent , previousCaretEvent  = None , None
path_obj = None
isRunning=False
isRecording = False

#Some utility functions to help with function defines

def _errcheck(res, func, args):
    if not res:
        raise RuntimeError("Result %s" % res)
    return res

def _fixBridgeFunc(restype,name,*argtypes,**kwargs):
    try:
        func=getattr(windowsbridgeDll,name)
    except Exception as e:
        log.error(e)
        log.error("%s not found in Java Access Bridge dll"%name)
        return
    func.restype=restype
    func.argtypes=argtypes
    if kwargs.get('errcheck'):
        func.errcheck=_errcheck

#Load the first available access bridge dll
legacyAccessBridge=True
dllbit = '64'
try:
    windowsbridgeDll=getattr(cdll,'windowsAccessBridge-64')
    log.info("windowsbridgeDll-64 loaded successfully")
    legacyAccessBridge=False
    isRunning = True
except Exception as e:
    log.debug(e)
    try:
        windowsbridgeDll=getattr(cdll,'windowsAccessBridge-32')
        log.info("windowsbridgeDll-32 loaded successfully")
        legacyAccessBridge=False
        dllbit = '32'
        isRunning = True
    except Exception as e:
        log.debug(e)
        try:
            windowsbridgeDll=cdll.windowsAccessBridge
            log.info("windowsbridgeDll loaded successfully")
            isRunning = True
        except WindowsError:
            windowsbridgeDll=None

#Definitions of access bridge types, structs and prototypes

jchar=c_wchar
jint=c_int
jString=c_wchar
jfloat=c_float
jboolean=c_bool
class JOBJECT64(c_int if legacyAccessBridge else c_int64):
    pass
AccessibleTable=JOBJECT64

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

class AccessibleTableInfo(Structure):
    _fields_=[
        ('caption',JOBJECT64),
        ('summary',JOBJECT64),
        ('rowCount',jint),
        ('columnCount',jint),
        ('accessibleContext',JOBJECT64),
        ('accessibleTable',JOBJECT64),
    ]

class AccessibleTableCellInfo(Structure):
    _fields_=[
        ('accessibleContext',JOBJECT64),
        ('index',jint),
        ('row',jint),
        ('column',jint),
        ('rowExtent',jint),
        ('columnExtent',jint),
        ('isSelected',jboolean),
    ]

MAX_KEY_BINDINGS=50
ACCESSIBLE_SHIFT_KEYSTROKE=1
ACCESSIBLE_CONTROL_KEYSTROKE=2
ACCESSIBLE_META_KEYSTROKE=4
ACCESSIBLE_ALT_KEYSTROKE=8
ACCESSIBLE_ALT_GRAPH_KEYSTROKE=16
ACCESSIBLE_BUTTON1_KEYSTROKE=32
ACCESSIBLE_BUTTON2_KEYSTROKE=64
ACCESSIBLE_BUTTON3_KEYSTROKE=128

class AccessibleKeyBindingInfo(Structure):
    _fields_=[
        ('character',jchar),
        ('modifiers',jint),
    ]

class AccessibleKeyBindings(Structure):
    _fields_=[
        ('keyBindingsCount',c_int),
        ('keyBindingInfo',AccessibleKeyBindingInfo*MAX_KEY_BINDINGS),
    ]

AccessBridge_FocusGainedFP=CFUNCTYPE(None,c_long,JOBJECT64,JOBJECT64)
AccessBridge_MousePressedFP=CFUNCTYPE(None,c_long,JOBJECT64,JOBJECT64)
#AccessBridge_PropertyNameChangeFP=CFUNCTYPE(None,c_long,JOBJECT64,JOBJECT64,c_wchar_p,c_wchar_p)
#AccessBridge_PropertyDescriptionChangeFP=CFUNCTYPE(None,c_long,JOBJECT64,JOBJECT64,c_wchar_p,c_wchar_p)
#AccessBridge_PropertyValueChangeFP=CFUNCTYPE(None,c_long,JOBJECT64,JOBJECT64,c_wchar_p,c_wchar_p)
AccessBridge_PropertyStateChangeFP=CFUNCTYPE(None,c_long,JOBJECT64,JOBJECT64,c_wchar_p,c_wchar_p)
#AccessBridge_PropertyCaretChangeFP=CFUNCTYPE(None,c_long,JOBJECT64,JOBJECT64,c_int,c_int)
#AccessBridge_PropertyActiveDescendentChangeFP=CFUNCTYPE(None,c_long,JOBJECT64,JOBJECT64,JOBJECT64,JOBJECT64)

#Appropriately set the return and argument types of all the access bridge dll functions
if windowsbridgeDll:
    _fixBridgeFunc(None,'Windows_run')
    _fixBridgeFunc(None,'setFocusGainedFP',c_void_p)
    _fixBridgeFunc(None,'setMousePressedFP',c_void_p)
    #_fixBridgeFunc(None,'setPropertyNameChangeFP',c_void_p)
    #_fixBridgeFunc(None,'setPropertyDescriptionChangeFP',c_void_p)
    #_fixBridgeFunc(None,'setPropertyValueChangeFP',c_void_p)
    _fixBridgeFunc(None,'setPropertyStateChangeFP',c_void_p)
    #_fixBridgeFunc(None,'setPropertyCaretChangeFP',c_void_p)
    #_fixBridgeFunc(None,'setPropertyActiveDescendentChangeFP',c_void_p)
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
    _fixBridgeFunc(JOBJECT64,'getParentWithRole',c_long,JOBJECT64,POINTER(c_wchar))
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
    _fixBridgeFunc(BOOL,'doAccessibleActions',c_long,JOBJECT64,POINTER(AccessibleActionsToDo),POINTER(jint),errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleTableInfo',c_long,JOBJECT64,POINTER(AccessibleTableInfo))
    _fixBridgeFunc(BOOL,'getAccessibleTableCellInfo',c_long,AccessibleTable,jint,jint,POINTER(AccessibleTableCellInfo),errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleTableRowHeader',c_long,JOBJECT64,POINTER(AccessibleTableInfo))
    _fixBridgeFunc(BOOL,'getAccessibleTableColumnHeader',c_long,JOBJECT64,POINTER(AccessibleTableInfo))
    _fixBridgeFunc(BOOL,'setTextContents',c_long,JOBJECT64,POINTER(jString),errcheck=True)
    _fixBridgeFunc(BOOL,'getAccessibleActions',c_long,JOBJECT64,POINTER(AccessibleActions),errcheck=True)
    _fixBridgeFunc(BOOL,'doAccessibleActions',c_long,JOBJECT64,POINTER(AccessibleActionsToDo),POINTER(jint))
    _fixBridgeFunc(BOOL,'selectAllAccessibleSelectionFromContext',c_long,JOBJECT64,errcheck=True)
    _fixBridgeFunc(BOOL,'addAccessibleSelectionFromContext',c_long,JOBJECT64,jint,errcheck=True)
    _fixBridgeFunc(BOOL,'removeAccessibleSelectionFromContext',c_long,JOBJECT64,jint,errcheck=True)
    _fixBridgeFunc(JOBJECT64,'getAccessibleTableRowDescription',c_long,JOBJECT64,jint)
    _fixBridgeFunc(JOBJECT64,'getAccessibleTableColumnDescription',c_long,JOBJECT64,jint)
    _fixBridgeFunc(jint,'getAccessibleTableRow',c_long,AccessibleTable,jint)
    _fixBridgeFunc(jint,'getAccessibleTableColumn',c_long,AccessibleTable,jint)
    _fixBridgeFunc(jint,'getAccessibleTableIndex',c_long,AccessibleTable,jint,jint)
    _fixBridgeFunc(BOOL,'getAccessibleKeyBindings',c_long,JOBJECT64,POINTER(AccessibleKeyBindings),errcheck=True)

#NVDA specific code

#isRunning=False
# Cache of the last active window handle for a given JVM ID. In theory, this
# cache should not be needed, as it should always be possible to retrieve the
# window handle of a given accessible context by calling getTopLevelObject then
# getHWNDFromAccessibleContext. However, getTopLevelObject sometimes returns 
# accessible contexts that make getHWNDFromAccessibleContext fail. To workaround
# the issue, we use this cache as a fallback when either getTopLevelObject or
# getHWNDFromAccessibleContext fails.
vmIDsToWindowHandles={}
internalFunctionQueue=queue.Queue(1000)
internalFunctionQueue.__name__="JABHandler.internalFunctionQueue"

def internalQueueFunction(func,*args,**kwargs):
    try:
        internalFunctionQueue.put_nowait((func,args,kwargs))
        oebs_click_and_add.get_core().requestPump()
    except Exception as e:
        log.info("error at internal queue {}".format(e))

def internal_getWindowHandleFromAccContext(vmID,accContext):
    try:
        topAC=windowsbridgeDll.getTopLevelObject(vmID,accContext)
        try:
            return windowsbridgeDll.getHWNDFromAccessibleContext(vmID,topAC)
        finally:
            windowsbridgeDll.releaseJavaObject(vmID,topAC)
    except:
        return None

def getWindowHandleFromAccContext(vmID,accContext):
    hwnd=internal_getWindowHandleFromAccContext(vmID,accContext)
    if hwnd:
        vmIDsToWindowHandles[vmID]=hwnd
        return hwnd
    else:
        return vmIDsToWindowHandles.get(vmID)


class JABContext(object):

    def __init__(self,hwnd=None,vmID=None,accContext=None):
        if hwnd and not vmID:
            vmID=c_long()
            accContext=JOBJECT64()
            try:
                windowsbridgeDll.getAccessibleContextFromHWND(hwnd,byref(vmID),byref(accContext))
            except Exception as e:
                log.debug(e)
            #Record  this vm ID and window handle for later use with other objects
            vmID=vmID.value
            vmIDsToWindowHandles[vmID]=hwnd
        elif vmID and not hwnd:
            topAC=windowsbridgeDll.getTopLevelObject(vmID,accContext)   #added by me
            hwnd = getWindowHandleFromAccContext(vmID,accContext)
            #added by me
            windowsbridgeDll.releaseJavaObject(vmID,topAC)
            vmIDsToWindowHandles[vmID]=hwnd
        self.hwnd=hwnd
        self.vmID=vmID
        self.accContext=accContext

    def __del__(self):
        if isRunning:
            try:
                windowsbridgeDll.releaseJavaObject(self.vmID,self.accContext)
            except:
                log.error("Error releasing java object")


    def __eq__(self,jabContext):
        if self.vmID==jabContext.vmID and windowsbridgeDll.isSameObject(self.vmID,self.accContext,jabContext.accContext):
            return True
        else:
            return False

    def __ne__(self,jabContext):
        if self.vmID!=jabContext.vmID or not windowsbridgeDll.isSameObject(self.vmID,self.accContext,jabContext.accContext):
            return True
        else:
            return False

    def getVersionInfo(self):
        info=AccessBridgeVersionInfo()
        windowsbridgeDll.getVersionInfo(self.vmID,byref(info))
        return info

    def getObjectDepth(self):
        return windowsbridgeDll.getObjectDepth(self.vmID,self.accContext)

    def getAccessibleContextInfo(self):
        info=AccessibleContextInfo()
        windowsbridgeDll.getAccessibleContextInfo(self.vmID,self.accContext,byref(info))
        return info

    def getAccessibleTextInfo(self,x,y):
        textInfo=AccessibleTextInfo()
        windowsbridgeDll.getAccessibleTextInfo(self.vmID,self.accContext,byref(textInfo),x,y)
        return textInfo

    def getAccessibleTextItems(self,index):
        textItemsInfo=AccessibleTextItemsInfo()
        windowsbridgeDll.getAccessibleTextItems(self.vmID,self.accContext,byref(textItemsInfo),index)
        return textItemsInfo

    def getAccessibleTextSelectionInfo(self):
        textSelectionInfo=AccessibleTextSelectionInfo()
        windowsbridgeDll.getAccessibleTextSelectionInfo(self.vmID,self.accContext,byref(textSelectionInfo))
        return textSelectionInfo

    def getAccessibleTextRange(self,start,end):
        length=((end+1)-start)
        if length<=0:
            return u""
        text=create_unicode_buffer(length+1)
        windowsbridgeDll.getAccessibleTextRange(self.vmID,self.accContext,start,end,text,length)
        return text.value

    def getAccessibleTextLineBounds(self,index):
        index=max(index,0)
        log.debug("lineBounds: index %s"%index)
        #Java returns end as the last character, not end as past the last character
        startIndex=c_int()
        endIndex=c_int()
        windowsbridgeDll.getAccessibleTextLineBounds(self.vmID,self.accContext,index,byref(startIndex),byref(endIndex))
        start=startIndex.value
        end=endIndex.value
        log.debug("line bounds: start %s, end %s"%(start,end))
        if end<start or start<0:
            # Invalid or empty line.
            return (0,-1)
        ok=False
        # OpenOffice sometimes returns offsets encompassing more than one line, so try to narrow them down.
        # Try to retract the end offset.
        while not ok:
            windowsbridgeDll.getAccessibleTextLineBounds(self.vmID,self.accContext,end,byref(startIndex),byref(endIndex))
            tempStart=max(startIndex.value,0)
            tempEnd=max(endIndex.value,0)
            log.debug("line bounds: tempStart %s, tempEnd %s"%(tempStart,tempEnd))
            if tempStart>(index+1):
                # This line starts after the requested index, so set end to point at the line before.
                end=tempStart-1
            else:
                ok=True
        ok=False
        # Try to retract the start.
        while not ok:
            windowsbridgeDll.getAccessibleTextLineBounds(self.vmID,self.accContext,start,byref(startIndex),byref(endIndex))
            tempStart=max(startIndex.value,0)
            tempEnd=max(endIndex.value,0)
            log.debug("line bounds: tempStart %s, tempEnd %s"%(tempStart,tempEnd))
            if tempEnd<(index-1):
                # This line ends before the requested index, so set start to point at the line after.
                start=tempEnd+1
            else:
                ok=True
        log.debug("line bounds: returning %s, %s"%(start,end))
        return (start,end)


    def getAccessibleParentFromContext(self):
        accContext=windowsbridgeDll.getAccessibleParentFromContext(self.vmID,self.accContext)
        if accContext:
            return self.__class__(self.hwnd,self.vmID,accContext)
        else:
            return None

    def getAccessibleParentWithRole(self, role):
        accContext=windowsbridgeDll.getParentWithRole(self.vmID,self.accContext, role)
        if accContext:
            return self.__class__(self.hwnd,self.vmID,accContext)
        else:
            return None

    def getAccessibleChildFromContext(self,index):
        accContext=windowsbridgeDll.getAccessibleChildFromContext(self.vmID,self.accContext,index)
        if accContext:
            return self.__class__(self.hwnd,self.vmID,accContext)
        else:
            return None

    def getActiveDescendent(self):
        accContext=windowsbridgeDll.getActiveDescendent(self.vmID,self.accContext)
        if accContext:
            return self.__class__(self.hwnd,self.vmID,accContext)
        else:
            return None

    def getAccessibleContextAt(self,x,y):
        newAccContext=JOBJECT64()
        res=windowsbridgeDll.getAccessibleContextAt(self.vmID,self.accContext,x,y,byref(newAccContext))
        if not res or not newAccContext:
            return None
        if not windowsbridgeDll.isSameObject(self.vmID,newAccContext,self.accContext):
            return self.__class__(self.hwnd,self.vmID,newAccContext)
        elif newAccContext!=self.accContext:
            windowsbridgeDll.releaseJavaObject(self.vmID,newAccContext)
        return None

    def getCurrentAccessibleValueFromContext(self):
        buf=create_unicode_buffer(SHORT_STRING_SIZE+1)
        windowsbridgeDll.getCurrentAccessibleValueFromContext(self.vmID,self.accContext,buf,SHORT_STRING_SIZE)
        return buf.value

    def selectTextRange(self,start,end):
        windowsbridgeDll.selectTextRange(start,end)

    def setCaretPosition(self,offset):
        windowsbridgeDll.setCaretPosition(self.vmID,self.accContext,offset)

    def getTextAttributesInRange(self, startIndex, endIndex):
        attributes = AccessibleTextAttributesInfo()
        length = c_short()
        windowsbridgeDll.getTextAttributesInRange(self.vmID, self.accContext, startIndex, endIndex, byref(attributes), byref(length))
        return attributes, length.value

    def getAccessibleRelationSet(self):
        relations = AccessibleRelationSetInfo()
        windowsbridgeDll.getAccessibleRelationSet(self.vmID, self.accContext, byref(relations))
        return relations

    def setTextContents(self,string):
        return windowsbridgeDll.setTextContents(self.vmID,self.accContext,string)

    def getAccessibleActions(self):
        actions=AccessibleActions()
        windowsbridgeDll.getAccessibleActions(self.vmID,self.accContext,byref(actions))
        return actions

    def doAccessibleActions(self,actionCount,action):
        actionstodo = AccessibleActionsToDo()
        actionstodo.actionsCount = actionCount
        actionstodo.actions[0].name = action
        res = jint()
        result = windowsbridgeDll.doAccessibleActions(self.vmID,self.accContext,byref(actionstodo),byref(res))
        return result

    def selectAllAccessibleSelectionFromContext(self):
        windowsbridgeDll.selectAllAccessibleSelectionFromContext(self.vmID,self.accContext)

    def addAccessibleSelectionFromContext(self,index):
        windowsbridgeDll.addAccessibleSelectionFromContext(self.vmID,self.accContext,index)

    def removeAccessibleSelectionFromContext(self,index):
        windowsbridgeDll.removeAccessibleSelectionFromContext(self.vmID,self.accContext,index)

    def getAccessibleTableInfo(self):
        info=AccessibleTableInfo()
        if windowsbridgeDll.getAccessibleTableInfo(self.vmID,self.accContext,byref(info)):
            # #6992: Querying the hwnd for table related objects can cause the app to crash.
            # A table is almost certainly contained within a single hwnd,
            # so just pass the hwnd for the querying object.
            info.jabCaption=JABContext(hwnd=self.hwnd,vmID=self.vmID,accContext=info.caption) if info.caption else None
            info.jabSummary=JABContext(hwnd=self.hwnd,vmID=self.vmID,accContext=info.summary) if info.summary else None
            info.jabContext=JABContext(hwnd=self.hwnd,vmID=self.vmID,accContext=info.accessibleContext) if info.accessibleContext else None
            info.jabTable=JABContext(hwnd=self.hwnd,vmID=self.vmID,accContext=info.accessibleTable) if info.accessibleTable else None
            return info

    def getAccessibleTableCellInfo(self,row,col):
        info=AccessibleTableCellInfo()
        if windowsbridgeDll.getAccessibleTableCellInfo(self.vmID,self.accContext,row,col,byref(info)):
            # #6992: Querying the hwnd for table related objects can cause the app to crash.
            # A table is almost certainly contained within a single hwnd,
            # so just pass the hwnd for the querying object.
            info.jabContext=JABContext(hwnd=self.hwnd,vmID=self.vmID,accContext=info.accessibleContext) if info.accessibleContext else None
            return info

    def getAccessibleTableRow(self,index):
        return windowsbridgeDll.getAccessibleTableRow(self.vmID,self.accContext,index)

    def getAccessibleTableColumn(self,index):
        return windowsbridgeDll.getAccessibleTableColumn(self.vmID,self.accContext,index)

    def getAccessibleTableRowHeader(self):
        info=AccessibleTableInfo()
        if windowsbridgeDll.getAccessibleTableRowHeader(self.vmID,self.accContext,byref(info)):
            # #6992: Querying the hwnd for table related objects can cause the app to crash.
            # A table is almost certainly contained within a single hwnd,
            # so just pass the hwnd for the querying object.
            info.jabCaption=JABContext(hwnd=self.hwnd,vmID=self.vmID,accContext=info.caption) if info.caption else None
            info.jabSummary=JABContext(hwnd=self.hwnd,vmID=self.vmID,accContext=info.summary) if info.summary else None
            info.jabContext=JABContext(hwnd=self.hwnd,vmID=self.vmID,accContext=info.accessibleContext) if info.accessibleContext else None
            info.jabTable=JABContext(hwnd=self.hwnd,vmID=self.vmID,accContext=info.accessibleTable) if info.accessibleTable else None
            return info

    def getAccessibleTableRowDescription(self,row):
        accContext=windowsbridgeDll.getAccessibleTableRowDescription(self.vmID,self.accContext,row)
        if accContext:
            # #6992: Querying the hwnd for table related objects can cause the app to crash.
            # A table is almost certainly contained within a single hwnd,
            # so just pass the hwnd for the querying object.
            return JabContext(hwnd=self.hwnd,vmID=self.vmID,accContext=accContext)

    def getAccessibleTableColumnHeader(self):
        info=AccessibleTableInfo()
        if windowsbridgeDll.getAccessibleTableColumnHeader(self.vmID,self.accContext,byref(info)):
            # #6992: Querying the hwnd for table related objects can cause the app to crash.
            # A table is almost certainly contained within a single hwnd,
            # so just pass the hwnd for the querying object.
            info.jabCaption=JABContext(hwnd=self.hwnd,vmID=self.vmID,accContext=info.caption) if info.caption else None
            info.jabSummary=JABContext(hwnd=self.hwnd,vmID=self.vmID,accContext=info.summary) if info.summary else None
            info.jabContext=JABContext(hwnd=self.hwnd,vmID=self.vmID,accContext=info.accessibleContext) if info.accessibleContext else None
            info.jabTable=JABContext(hwnd=self.hwnd,vmID=self.vmID,accContext=info.accessibleTable) if info.accessibleTable else None
            return info

    def getAccessibleTableColumnDescription(self,column):
        accContext=windowsbridgeDll.getAccessibleTableColumnDescription(self.vmID,self.accContext,column)
        if accContext:
            # #6992: Querying the hwnd for table related objects can cause the app to crash.
            # A table is almost certainly contained within a single hwnd,
            # so just pass the hwnd for the querying object.
            return JabContext(hwnd=self.hwnd,vmID=self.vmID,accContext=accContext)

    def getAccessibleKeyBindings(self):
        bindings=AccessibleKeyBindings()
        if windowsbridgeDll.getAccessibleKeyBindings(self.vmID,self.accContext,byref(bindings)):
            return bindings

    def releaseJavaObject(self):
        #windowsbridgeDll.releaseJavaObject(self.vmID,self.accContext)
        windowsbridgeDll.releaseJavaObject(self.hwnd,self.accContext)

@AccessBridge_FocusGainedFP
def internal_event_focusGained(vmID, event,source):
    global isRecording
    if isRecording:
        hwnd=getWindowHandleFromAccContext(vmID,source)
        internalQueueFunction(event_gainFocus,vmID,source,hwnd)
    try:
        windowsbridgeDll.releaseJavaObject(vmID,event)
    except Exception as e:
        log.debug(e)

def event_gainFocus(vmID,accContext,hwnd):
    jabContext=JABContext(hwnd=hwnd,vmID=vmID,accContext=accContext)
    if not winuser.isDescendantWindow(winuser.getForegroundWindow(),jabContext.hwnd):
        return
    focus=oebs_event_handler.lastQueuedFocusObject
    if (isinstance(focus,oebs_jab_object.JAB) and focus.jabContext==jabContext):
        return 
    obj=oebs_jab_object.JAB(jabContext=jabContext)
    if oebs_api2.getFocusObject() == None:
        oebs_api2.setFocusObject(obj)
    if obj._get_role()==oebs_control_types.ROLE_UNKNOWN:
        return
    oebs_event_handler.queueEvent("gainFocus",obj)

@AccessBridge_MousePressedFP
def internal_event_mousePressed(vmID,event,source):
    try:
        global isRecording
        if isRecording:
            hwnd=getWindowHandleFromAccContext(vmID,source)
            internalQueueFunction(event_mousePressed,vmID,source,hwnd)
        windowsbridgeDll.releaseJavaObject(vmID,event)
    except Exception as e:
        log.debug(e)

def event_mousePressed(vmID,accContext,hwnd):
    global previousMouseEvent
    jabContext=JABContext(hwnd=hwnd,vmID=vmID,accContext=accContext)
    if previousMouseEvent is not None and jabContext == previousMouseEvent:
        return
    obj=oebs_jab_object.JAB(jabContext=jabContext)
    path_obj.get_path(obj,"mousePressed")
    previousMouseEvent = jabContext

#@AccessBridge_PropertyActiveDescendentChangeFP
def internal_event_activeDescendantChange(vmID, event,source,oldDescendant,newDescendant):
    global isRecording
    if isRecording:
        hwnd=getWindowHandleFromAccContext(vmID,source)
        internalQueueFunction(event_gainFocus,vmID,newDescendant,hwnd)
    for accContext in [event,oldDescendant]:
        windowsbridgeDll.releaseJavaObject(vmID,accContext)

#@AccessBridge_PropertyNameChangeFP
def event_nameChange(vmID,event,source,oldVal,newVal):
    global isRecording
    if isRecording:
        jabContext=JABContext(vmID=vmID,accContext=source)
        focus=oebs_api2.getFocusObject()
        if isinstance(focus, oebs_jab_object.JAB) and focus.jabContext == jabContext:
            obj = focus
        else:
            obj = oebs_jab_object.JAB(jabContext=jabContext)
        if obj:
            oebs_event_handler.queueEvent("nameChange", obj)
    windowsbridgeDll.releaseJavaObject(vmID,event)

#@AccessBridge_PropertyDescriptionChangeFP
def event_descriptionChange(vmID,event,source,oldVal,newVal):
    global isRecording
    if isRecording:
        jabContext=JABContext(vmID=vmID,accContext=source)
        focus=oebs_api2.getFocusObject()
        if isinstance(focus, oebs_jab_object.JAB) and focus.jabContext == jabContext:
            obj = focus
        else:
            obj = oebs_jab_object.JAB(jabContext=jabContext)
        if obj:
            oebs_event_handler.queueEvent("descriptionChange", obj)
    windowsbridgeDll.releaseJavaObject(vmID,event)

#@AccessBridge_PropertyValueChangeFP
def event_valueChange(vmID,event,source,oldVal,newVal):
    global isRecording
    if isRecording:
        jabContext=JABContext(vmID=vmID,accContext=source)
        focus=oebs_api2.getFocusObject()
        if isinstance(focus, oebs_jab_object.JAB) and focus.jabContext == jabContext:
            obj = focus
        else:
            obj = oebs_jab_object.JAB(jabContext=jabContext)
        if obj:
            oebs_event_handler.queueEvent("valueChange", obj)
    windowsbridgeDll.releaseJavaObject(vmID,event)

@AccessBridge_PropertyStateChangeFP
def internal_event_stateChange(vmID,event,source,oldState,newState):
    global isRecording
    if isRecording:
        internalQueueFunction(event_stateChange,vmID,source,oldState,newState)
    windowsbridgeDll.releaseJavaObject(vmID,event)

def event_stateChange(vmID,accContext,oldState,newState):
    jabContext=JABContext(vmID=vmID,accContext=accContext)
    focus=oebs_api2.getFocusObject()
    #For broken tabs and menus, we need to watch for things being selected and pretend its a focus change
    stateList=newState.split(',')
    if "focused" in stateList or "selected" in stateList:
        obj=oebs_jab_object.JAB(jabContext=jabContext)
        path_obj.get_path(obj,"stateChange")
        if not obj:
            return
        if focus!=obj and oebs_event_handler.lastQueuedFocusObject!=obj and obj._get_role() in (oebs_control_types.ROLE_MENUITEM,oebs_control_types.ROLE_TAB,oebs_control_types.ROLE_MENU):
            oebs_event_handler.queueEvent("gainFocus",obj)
            return
    if isinstance(focus,oebs_jab_object.JAB) and focus.jabContext==jabContext:
        obj=focus
    else:
        obj=oebs_jab_object.JAB(jabContext=jabContext)
        if not obj:
            return
    oebs_event_handler.queueEvent("stateChange",obj)

#@AccessBridge_PropertyCaretChangeFP
def internal_event_caretChange(vmID, event,source,oldPos,newPos):
    global isRecording
    if isRecording:
        hwnd=getWindowHandleFromAccContext(vmID,source)
        if oldPos<0 and newPos>=0:
            internalQueueFunction(event_gainFocus,vmID,source,hwnd)
        else:
            internalQueueFunction(event_caret,vmID,source,hwnd)
    windowsbridgeDll.releaseJavaObject(vmID,event)

def event_caret(vmID, accContext, hwnd):
    global previousCaretEvent
    jabContext = JABContext(hwnd=hwnd, vmID=vmID, accContext=accContext)
    if previousCaretEvent is not None and jabContext == previousCaretEvent:
        return
    focus = oebs_api2.getFocusObject()
    if isinstance(focus, oebs_jab_object.JAB) and focus.jabContext == jabContext:
        obj = focus
    else:
        obj = oebs_jab_object.JAB(jabContext=jabContext)
        if not obj:
            return
    path_obj.get_path(obj,"caret")


def event_enterJavaWindow(hwnd):
    internalQueueFunction(enterJavaWindow_helper,hwnd)

def enterJavaWindow_helper(hwnd):
    vmID=c_long()
    accContext=JOBJECT64()
    gotFocus=False
    timeout=time.time()+0.2
    while time.time()<timeout and not oebs_event_handler.isPendingEvents("gainFocus"):
        try:
            windowsbridgeDll.getAccessibleContextWithFocus(hwnd,byref(vmID),byref(accContext))
        except:
            pass
        if vmID and accContext:
            break
        time.sleep(0.01)
    if not vmID or not accContext: 
        try:
            windowsbridgeDll.getAccessibleContextFromHWND(hwnd,byref(vmID),byref(accContext))
        except:
            return
    vmID=vmID.value
    vmIDsToWindowHandles[vmID]=hwnd
    lastFocus=oebs_event_handler.lastQueuedFocusObject
    if isinstance(lastFocus,oebs_jab_object.JAB) and lastFocus.windowHandle==hwnd:
        return
    event_gainFocus(vmID,accContext,hwnd)
def isJavaWindow(hwnd):
    if not windowsbridgeDll:
        return False
    try:
        windowsbridgeDll.Windows_run()
        time.sleep(0.01)
        win32gui.PumpWaitingMessages()
        time.sleep(0.01)
        return windowsbridgeDll.isJavaWindow(hwnd)
    except Exception as e:
        return bool(0)

def initialize():
    global isRunning , isRecording , internalFunctionQueue , path_obj
    path_obj = PathGenerator(window_name = oebs_click_and_add.core.window_name)
    log.info("WindowName Recived from core in JABhadler " + oebs_click_and_add.get_core().window_name)
    if not windowsbridgeDll:
        raise NotImplementedError("dll not available")
    windowsbridgeDll.Windows_run()
    #Accept wm_copydata and any wm_user messages from other processes even if running with higher privilages
    try:
        ChangeWindowMessageFilter=getattr(windll.user32,'ChangeWindowMessageFilter',None)
        if ChangeWindowMessageFilter:
            if not ChangeWindowMessageFilter(winuser.WM_COPYDATA,1):
                raise WinError()
            for msg in range(winuser.WM_USER+1,65535):
                if not ChangeWindowMessageFilter(msg,1):
                    raise WinError()
    except Exception as e:
        log.debug(e)
    #Register java events
    windowsbridgeDll.setFocusGainedFP(internal_event_focusGained)
    windowsbridgeDll.setMousePressedFP(internal_event_mousePressed)
    windowsbridgeDll.setPropertyStateChangeFP(internal_event_stateChange)
    isRunning=True
    isRecording = True

def pumpAll():
    if isRunning:
        oebs_event_handler.flushQueue(internalFunctionQueue)

def terminate():
    global isRunning, windowsbridgeDll
    if not windowsbridgeDll or not isRunning:
        return
    if legacyAccessBridge:
        del cdll.windowsAccessBridge 
    else:
        delattr(cdll,'windowsAccessBridge-'+dllbit)
    isRunning=False

def terminateEvents():
    global isRecording, windowsbridgeDll, isRunning
    if not windowsbridgeDll or not isRunning or not isRecording:
        return
    windowsbridgeDll.setFocusGainedFP(None)
    windowsbridgeDll.setMousePressedFP(None)
    windowsbridgeDll.setPropertyStateChangeFP(None)
    end_recording()

def start_recording():
    global isRecording
    isRecording = True

def end_recording():
    global isRecording,previousCaretEvent,previousMouseEvent
    isRecording = False
    previousCaretEvent , previousMouseEvent = None , None
