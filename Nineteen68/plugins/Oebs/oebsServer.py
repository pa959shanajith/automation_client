import os
import sys
import shutil
import glob
import oebs_api
import win32gui
import json
from oebs_msg import *

import logging
import oebs_mouseops
import oebs_msg
import oebs_key_objects

import oebs_textops
import oebs_serverUtilities

from oebs_utilops import UtilOperations
from oebs_buttonops import ButtonOperations
from oebs_radiocheckboxops import RadioCheckboxOperations
from oebs_dropdownlistboxops import DropdownListboxOperations
from oebs_elementsops import ElementOperations
from oebsclickandadd import ClickAndAdd
from oebs_tableops import TableOperations
from oebs_scrollbarops import ScrollbarOperations
from oebs_internalframeops import InternalFrameOperations
import ast
import time
import xml.etree.ElementTree as ET
k = 0
cordinates = []
state = []
objectDict = {}
#config file location
#global values
accessContext = ''
debugmode=''


class OebsKeywords:

    def __init__(self):
        self.txtops_obj=oebs_textops.TextOperations()
        self.utilities_obj=oebs_serverUtilities.Utilities()
        self.utilops_obj=UtilOperations()
        self.buttonops_obj=ButtonOperations()
        self.radiocheckboxops_obj=RadioCheckboxOperations()
        self.dropdownlistboxops_obj=DropdownListboxOperations()

        self.elementsops_obj=ElementOperations()
        self.oebsclickandadd_obj=ClickAndAdd()
        self.tableops_obj=TableOperations()
        self.scrollbarops_obj=ScrollbarOperations()
        self.internalframeops_obj=InternalFrameOperations()


    def windowsrun(self):
        logging.debug('FILE: %s , DEF: %s',FILE_OEBSSERVER,DEF_WINDOWSRUN)
        return (oebs_api.bridgeDll.Windows_run())

    #Function to get HWND using window name
    def GetHwndFromWindowName(self,windowname):
        try:
            hwnd = win32gui.FindWindow(None, windowname)
            logging.debug('FILE: %s , DEF: %s MSG: Window Handle Fetched',FILE_OEBSSERVER,DEF_GETHWNDFROMWINDOWNAME)
        except:
            logging.debug('FILE: %s , DEF: %s , MSG: Window Handle Fetch Fail',FILE_OEBSSERVER,DEF_GETHWNDFROMWINDOWNAME)
            hwnd = None
        return hwnd

    #Confirm open window is a java window
    def isjavawindow(self,windowname):
        logging.debug('FILE: %s , DEF: %s , MSG: Window Name Received: %s',FILE_OEBSSERVER,DEF_ISJAVAWINDOW, windowname)
        isjavares = False
        logging.debug('FILE: %s , DEF: %s , MSG: Window BRIDGE DLL Status: %s',FILE_OEBSSERVER,DEF_ISJAVAWINDOW,oebs_api.bridgeDll )
        if (oebs_api.bridgeDll != None):
            self.windowsrun()
            hwnd = self.GetHwndFromWindowName(windowname)
            logging.debug('FILE: %s , DEF: %s , MSG: API Call for Java window check',FILE_OEBSSERVER,DEF_ISJAVAWINDOW)
            isjavares = oebs_api.isJavaWindow(hwnd)
            return (isjavares, hwnd)
        else:
            logging.debug('FILE: %s , DEF: %s ,MSG: %s.',FILE_OEBSSERVER,DEF_ISJAVAWINDOW,MSG_ACCESS_BRIDGE_INIT_ERROR)
            return (isjavares, MSG_ACCESS_BRIDGE_INIT_ERROR)

    #Full scrape method
    def getentireobjectlist(self,windowname):
        tempne = []
        self.windowsrun()
        logging.debug('FILE: %s , DEF: %s , MSG:\nWindows Run Executed.',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST)
        isjavares, hwnd = self.isjavawindow(windowname)
        logging.debug('FILE: %s, DEF: %s , MSG:\njava window status obtained is :%s',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST,str(isjavares))
        if (isjavares):
            self.utilities_obj.acccontext(oebs_api.JABContext(hwnd), tempne,'',0,windowname)
            logging.debug('FILE: %s , DEF: %s , MSG:\nThe Scraped Data is:\n %s',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST,tempne)
            vie = {'view': tempne}
            return json.dumps(vie)
        else:
            logging.debug('FILE: %s , DEF: %s , MSG: %s',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST,MSG_NOT_JAVA_WINDOW_INFO)
            return 'fail'

    def getobjectsize(self,windowname,path):
        self.windowsrun()
        logging.debug('FILE: %s , DEF: %s , MSG:\nWindows Run Executed.',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST)
        isjavares, hwnd = self.isjavawindow(windowname)
        logging.debug('FILE: %s, DEF: %s , MSG:\njava window status obtained is :%s',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST,str(isjavares))
        if (isjavares):
            logging.debug('FILE: %s , DEF: %s , MSG:\nThe Scraped Data is:\n %s',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST)
##            del self.utilities_obj.cordinates[:]
            del oebs_serverUtilities.cordinates[:]
            result=self.utilities_obj.getsize(path,windowname)
            return result
        else:
            logging.debug('FILE: %s , DEF: %s , MSG: %s',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST,MSG_NOT_JAVA_WINDOW_INFO)
            return MSG_NOT_JAVA_WINDOW_INFO

    def getbuttonname(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETBUTTONNAME,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.buttonops_obj.getbuttonname(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETBUTTONNAME,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifybuttonname(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYBUTTONNAME,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.buttonops_obj.verifybuttonname(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYBUTTONNAME,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def click(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_CLICK,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.buttonops_obj.click(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_CLICK,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def doubleclick(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_DOUBLECLICK,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.buttonops_obj.doubleclick(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_DOUBLECLICK,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def gettext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETTEXT,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.txtops_obj.gettext(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETTEXT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def settext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_SETTEXT,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.txtops_obj.settext(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_SETTEXT,oebs_key_objects.keyword_output)

        return self.utilities_obj.clientresponse()

    def gettextboxlength(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETTEXTBOXLENGTH,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.txtops_obj.gettextboxlength(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETTEXTBOXLENGTH,oebs_key_objects.keyword_output)
        return oebs_key_objects.keyword_output

    def verifytextboxlength(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYTEXTBOXLENGTH,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.txtops_obj.verifytextboxlength(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYTEXTBOXLENGTH,oebs_key_objects.keyword_output)
        return oebs_key_objects.keyword_output

    def verifytext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYTEXT,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.txtops_obj.verifytext(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYTEXT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def cleartext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_CLEARTEXT,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.txtops_obj.cleartext(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_CLEARTEXT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def setfocus(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_SETFOCUS,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilops_obj.setfocus(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_SETFOCUS,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyenabled(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYENABLED,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilops_obj.verifyenabled(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYENABLED,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifydisabled(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYDISABLED,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilops_obj.verifydisabled(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYDISABLED,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyvisible(applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYVISIBLE,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilops_obj.verifyvisible(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYVISIBLE,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyhidden(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYHIDDEN,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilops_obj.verifyhidden(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYHIDDEN,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyreadonly(applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYREADONLY,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilops_obj.verifyreadonly(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYREADONLY,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def gettooltiptext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETTOOLTIPTEXT,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilops_obj.gettooltiptext(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETTOOLTIPTEXT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifytooltiptext(applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYTOOLTIPTEXT,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilops_obj.verifytooltiptext(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYTOOLTIPTEXT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyexists(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYEXISTS,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilops_obj.verifyexists(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYEXISTS,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifydoesnotexists(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYDOESNOTEXISTS,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilops_obj.verifydoesnotexists(accessContext)
        elif (str(accessContext) == 'fail'):
            self.utilops_obj.verifydoesnotexists(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYDOESNOTEXISTS,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def sendfunctionkeys(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_SENDFUNCTIONKEYS,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilops_obj.sendfunctionkeys(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_SENDFUNCTIONKEYS,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getlinktext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETLINKTEXT,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.buttonops_obj.getlinktext(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETLINKTEXT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifylinktext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYLINKTEXT,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.buttonops_obj.verifylinktext(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYLINKTEXT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def selectradiobutton(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_SELECTRADIOBUTTON,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.radiocheckboxops_obj.selectradiobutton(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_SELECTRADIOBUTTON,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def selectcheckbox(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_SELECTCHECKBOX,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.radiocheckboxops_obj.selectcheckbox(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_SELECTCHECKBOX,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def unselectcheckbox(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_UNSELECTCHECKBOX,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
               self.radiocheckboxops_obj.unselectcheckbox(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_UNSELECTCHECKBOX,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getstatus(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETSTATUS,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.radiocheckboxops_obj.getstatus(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETSTATUS,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getselected(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETSELECTED,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.getselected(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETSELECTED,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyselectedvalue(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYSELECTEDVALUE,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.verifyselectedvalue(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYSELECTEDVALUE,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()
    ##-------------------------------------------------------------------------------------------

    def getcount(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETCOUNT,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                contextinfo = accessContext.getAccessibleContextInfo()
                if(contextinfo.role == 'combo box'):
                    accessContext = self.utilities_obj.looptolist(accessContext)

                self.dropdownlistboxops_obj.getcount(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETCOUNT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()


    def verifycount(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYCOUNT,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            contextinfo = accessContext.getAccessibleContextInfo()
            if(len(oebs_key_objects.keyword_input) != 0 and oebs_key_objects.keyword_input[0] !='' ):
                if(contextinfo.role == 'combo box'):
                    accessContext=self.utilities_obj.looptolist(accessContext)
                self.dropdownlistboxops_obj.verifycount(accessContext)
            else:
                logging.debug('FILE: %s , DEF: %s MSG:%s',FILE_OEBSSERVER,DEF_VERIFYCOUNT,MSG_INVALID_INPUT)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYCOUNT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyallvalues(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYALLVALUES,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.verifyallvalues(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYALLVALUES,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyvaluesexists(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYVALUESEXISTS,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.verifyvaluesexists(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYVALUESEXISTS,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def selectvaluebyindex(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_SELECTVALUEBYINDEX,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.selectvaluebyindex(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_SELECTVALUEBYINDEX,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getvaluebyindex(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETVALUEBYINDEX,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            self.dropdownlistboxops_obj.getvaluebyindex(accessContext)
            if str(accessContext) != 'fail':
                logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETVALUEBYINDEX,oebs_key_objects.keyword_output)
                return self.utilities_obj.clientresponse()

    def selectvaluebytext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_SELECTVALUEBYTEXT,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.selectvaluebytext(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_SELECTVALUEBYTEXT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def selectmultiplevaluesbyindexes(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_SELECTMULTIPLEVALUESBYINDEXES,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.selectmultiplevaluesbyindexes(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_SELECTMULTIPLEVALUESBYINDEXES,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def deselectall(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_DESELECTALL,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.deselectall(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_DESELECTALL,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def selectallvalues(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_SELECTALLVALUES,applicationname,objectname,keyword,inputs,outputs)
        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.selectallvalues(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_SELECTALLVALUES,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getmultiplevaluesbyindexes(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETMULTIPLEVALUESBYINDEXES,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.getmultiplevaluesbyindexes(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETMULTIPLEVALUESBYINDEXES,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyselectedvalues(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYSELECTEDVALUES,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.verifyselectedvalues(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_VERIFYSELECTEDVALUES,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def selectmultiplevaluesbytext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_SELECTMULTIPLEVALUEBYTEXT,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.selectmultiplevaluesbytext(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_SELECTMULTIPLEVALUEBYTEXT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()


    def getallstates(self,windowname,path):
    ##    windowsrun()
        isjavares, hwnd = self.isjavawindow(windowname)
        state =  self.utilities_obj.getstate(oebs_api.JABContext(hwnd),path,windowname,0,'')
        state = str(state)
        return state

    def rightclick(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_RIGHTCLICK,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilops_obj.rightclick(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_RIGHTCLICK,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def clickelement(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_CLICKELEMENT,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilities_obj.clickelement(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_CLICKELEMENT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getelementtext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETELEMENTTEXT,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilities_obj.getelementtext(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_CLICKELEMENT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyelementtext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYELEMENTTEXT,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.utilities_obj.verifyelementtext(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_CLICKELEMENT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def createObjetctMap(self,windowname):
        tempne = []
        self.windowsrun()
        logging.debug('FILE: %s , DEF: %s , MSG:\nWindows Run Executed.',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST)
        isjavares, hwnd = self.isjavawindow(windowname)
        logging.debug('FILE: %s, DEF: %s , MSG:\njava window status obtained is :%s',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST,str(isjavares))
        if (isjavares):
            map = self.utilities_obj.createMap(oebs_api.JABContext(hwnd), tempne,'',0,windowname)
            logging.debug('FILE: %s , DEF: %s , MSG:\n',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST)
    ##        print 'Map : ',map
            return map
        else:
            logging.debug('FILE: %s , DEF: %s , MSG: %s',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST,MSG_NOT_JAVA_WINDOW_INFO)
            return 'fail'

    def clickandadd(self,windowname,operation):
        operation=operation.upper()
        self.windowsrun()
        logging.debug('FILE: %s , DEF: %s , MSG:\nWindows Run Executed.',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST)
        isjavares, hwnd = self.isjavawindow(windowname)
        logging.debug('FILE: %s, DEF: %s , MSG:\njava window status obtained is :%s',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST,str(isjavares))
        if (isjavares):
            map = {}
            if(operation == 'STARTCLICKANDADD'):
                map = self.createObjetctMap(windowname)
    ##            print 'MAP:::::::::::::',map
            result = self.oebsclickandadd_obj.clickandadd(oebs_api.JABContext(hwnd),map,windowname,operation)
            logging.debug('FILE: %s , DEF: %s , MSG:\n',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST)
    ##        print 'Map : ',map
            return result
        else:
            logging.debug('FILE: %s , DEF: %s , MSG: %s',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST,MSG_NOT_JAVA_WINDOW_INFO)
            return 'fail'


    def getrowcount(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETROWCOUNT,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            #contextinfo = accessContext.getAccessibleTableInfo()
            #if(contextinfo.role == 'table'):
            #accessContext = oebs_serverUtilities.looptolist(accessContext)
            if str(accessContext) != 'fail':
                self.tableops_obj.getrowcount(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETROWCOUNT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getcolumncount(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETCOLUMNCOUNT,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            #contextinfo = accessContext.getAccessibleTableInfo()
            #if(contextinfo.role == 'table'):
            #accessContext = oebs_serverUtilities.looptolist(accessContext)
            if str(accessContext) != 'fail':
                self.tableops_obj.getcolumncount(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETCOLUMNCOUNT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getcellvalue(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETCELLVALUE,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.tableops_obj.getcellvalue(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETCELLVALUE,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifycellvalue(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_GETCELLVALUE,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.tableops_obj.verifycellvalue(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_GETCELLVALUE,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def cellclick(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_CELLCLICK,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.tableops_obj.cellclick(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_CELLCLICK,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def switchtoframe(self,applicationname,objectname,keyword,inputs,outputs):
    # this method has sends the root object to the keyword implementation
    # unlike other keywords where the actual elements object is sent
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_CELLCLICK,applicationname,objectname,keyword,inputs,outputs)
        inputs = ast.literal_eval(str(inputs))
        #input sent from the user
        inputs = ast.literal_eval(str(inputs))
        inputs = [n for n in inputs]
        for index in range(len(inputs)):
            oebs_key_objects.keyword_input.append(inputs[index])
    #output thats to be sent from the server to client
        oebs_key_objects.keyword_output = outputs.split(';')
        isjavares, hwnd = self.isjavawindow(applicationname)
    #root object is taken
        accessContext=oebs_api.JABContext(hwnd)
    #root object is sent to the keyword ie., frame's object is taken to definition
        self.utilops_obj.switchtoframe(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_SWITCHTOFRAME,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def right(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',OEBS_SCROLLBAR,DEF_RIGHT,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.scrollbarops_obj.right(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',OEBS_SCROLLBAR,DEF_RIGHT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def left(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',OEBS_SCROLLBAR,DEF_LEFT,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.scrollbarops_obj.left(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',OEBS_SCROLLBAR,DEF_LEFT,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def up(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',OEBS_SCROLLBAR,DEF_UP,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.scrollbarops_obj.up(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',OEBS_SCROLLBAR,DEF_UP,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def down(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_DOWN,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.scrollbarops_obj.down(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',OEBS_SCROLLBAR,DEF_DOWN,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def closeframe(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_CLOSEFRAME,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.internalframeops_obj.closeframe(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',OEBS_INTERNALFRAMEOPS,DEF_CLOSEFRAME,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def togglemaximize(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_TOGGLEMAXIMIZE,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.internalframeops_obj.togglemaximize(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMAXIMIZE,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def toggleminimize(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_TOGGLEMINIMIZE,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.internalframeops_obj.toggleminimize(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',OEBS_INTERNALFRAMEOPS,DEF_TOGGLEMINIMIZE,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def waitforelementvisible(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_VERIFYVISIBLE,applicationname,objectname,keyword,inputs,outputs)
        accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_WAITFORELEMENTVISIBLE,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def drag(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_DRAG,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            self.utilops_obj.drag(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_DRAG,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def drop(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        logging.debug('FILE: %s , DEF: %s , MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',FILE_OEBSSERVER,DEF_DROP,applicationname,objectname,keyword,inputs,outputs)
        self.utilities_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        if (oebs_key_objects.keyword_output[1]):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            self.utilops_obj.drop(accessContext)
        logging.debug('FILE: %s , DEF: %s , MSG:Keyword response : %s',FILE_OEBSSERVER,DEF_DROP,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getobjectforcustom(self,windowname,parentXpath,type,eleIndex):
        tempne = []
        self.windowsrun()
        logging.debug('FILE: %s , DEF: %s , MSG:\nWindows Run Executed.',FILE_OEBSSERVER,DEF_GETOBJECTFORCUSTOM)
        isjavares, hwnd = self.isjavawindow(windowname)
        logging.debug('FILE: %s, DEF: %s , MSG:\njava window status obtained is :%s',FILE_OEBSSERVER,DEF_GETOBJECTFORCUSTOM,str(isjavares))
        if (isjavares):
            eleproperty=self.utilities_obj.getobjectforcustom(oebs_api.JABContext(hwnd),windowname,parentXpath,type,eleIndex)
            logging.debug('FILE: %s , DEF: %s , MSG:\nThe Scraped Data is:\n %s',FILE_OEBSSERVER,DEF_GETOBJECTFORCUSTOM,tempne)

            return eleproperty
        else:
            logging.debug('FILE: %s , DEF: %s , MSG: %s',FILE_OEBSSERVER,DEF_GETENTIREOBJECTLIST,MSG_NOT_JAVA_WINDOW_INFO)
            return 'fail'
