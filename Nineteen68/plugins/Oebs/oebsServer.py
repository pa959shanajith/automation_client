#-------------------------------------------------------------------------------
# Name:        oebsServer.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     09/09/2015
# Copyright:   (c) rakesh.v 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

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
import utils

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

log = logging.getLogger('oebsServer.py')

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
        self.utils_obj=utils.Utils()


    def getobjectsize(self,windowname,path):
        self.utils_obj.windowsrun()
        log.debug('MSG:\nWindows Run Executed.',DEF_GETENTIREOBJECTLIST)
        isjavares, hwnd = self.utils_obj.isjavawindow(windowname)
        log.debug('FILE: %s, DEF: %s , MSG:\njava window status obtained is :%s',str(isjavares))
        if (isjavares):
##            log.debug('MSG:\nThe Scraped Data is:\n %s',DEF_GETENTIREOBJECTLIST)
##            del self.utilities_obj.cordinates[:]
            del oebs_serverUtilities.cordinates[:]
            result=self.utilities_obj.getsize(path,windowname)
            return result
        else:
            log.debug('MSG: %s',MSG_NOT_JAVA_WINDOW_INFO)
            return MSG_NOT_JAVA_WINDOW_INFO

    def getbuttonname(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.buttonops_obj.getbuttonname(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifybuttonname(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if ( accessContext):
            if str(accessContext) != 'fail':
                self.buttonops_obj.verifybuttonname(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def click(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.buttonops_obj.click(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def doubleclick(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.buttonops_obj.doubleclick(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def gettext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
       # self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.txtops_obj.gettext(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def settext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.txtops_obj.settext(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)

        return self.utilities_obj.clientresponse()

    def gettextboxlength(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.txtops_obj.gettextboxlength(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return oebs_key_objects.keyword_output

    def verifytextboxlength(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.txtops_obj.verifytextboxlength(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return oebs_key_objects.keyword_output

    def verifytext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
       # self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.txtops_obj.verifytext(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def cleartext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.txtops_obj.cleartext(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def setfocus(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.utilops_obj.setfocus(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyenabled(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        #log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
##        self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.utilops_obj.verifyenabled(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifydisabled(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.utilops_obj.verifydisabled(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyvisible(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.utilops_obj.verifyvisible(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyhidden(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.utilops_obj.verifyhidden(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyreadonly(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.utilops_obj.verifyreadonly(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def gettooltiptext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.utilops_obj.gettooltiptext(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifytooltiptext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.utilops_obj.verifytooltiptext(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyexists(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.utilops_obj.verifyexists(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifydoesnotexists(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.utilops_obj.verifydoesnotexists(accessContext)
        elif (str(accessContext) == 'fail'):
            self.utilops_obj.verifydoesnotexists(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse('verifydoesnotexists')

    def sendfunctionkeys(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.utilops_obj.sendfunctionkeys(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getlinktext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.buttonops_obj.getlinktext(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifylinktext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
       # self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.buttonops_obj.verifylinktext(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def selectradiobutton(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
       # self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.radiocheckboxops_obj.selectradiobutton(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def selectcheckbox(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.radiocheckboxops_obj.selectcheckbox(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def unselectcheckbox(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
               self.radiocheckboxops_obj.unselectcheckbox(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getstatus(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.radiocheckboxops_obj.getstatus(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getselected(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.getselected(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyselectedvalue(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
       # self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.verifyselectedvalue(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()
    ##-------------------------------------------------------------------------------------------

    def getcount(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                contextinfo = accessContext.getAccessibleContextInfo()
                if(contextinfo.role == 'combo box'):
                    accessContext = self.utilities_obj.looptolist(accessContext)

                self.dropdownlistboxops_obj.getcount(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()


    def verifycount(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            contextinfo = accessContext.getAccessibleContextInfo()
            if(len(oebs_key_objects.keyword_input) != 0 and oebs_key_objects.keyword_input[0] !='' ):
                if(contextinfo.role == 'combo box'):
                    accessContext=self.utilities_obj.looptolist(accessContext)
                self.dropdownlistboxops_obj.verifycount(accessContext)
            else:
                log.debug('MSG:%s',MSG_INVALID_INPUT)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyallvalues(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.verifyallvalues(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyvaluesexists(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.verifyvaluesexists(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def selectvaluebyindex(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.selectvaluebyindex(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getvaluebyindex(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           self.dropdownlistboxops_obj.getvaluebyindex(accessContext)
           if str(accessContext) != 'fail':
            log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
            return self.utilities_obj.clientresponse()

    def selectvaluebytext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.selectvaluebytext(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def selectmultiplevaluesbyindexes(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.selectmultiplevaluesbyindexes(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def deselectall(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.deselectall(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def selectallvalues(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.selectallvalues(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getmultiplevaluesbyindexes(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.getmultiplevaluesbyindexes(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyselectedvalues(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.verifyselectedvalues(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def selectmultiplevaluesbytext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.dropdownlistboxops_obj.selectmultiplevaluesbytext(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()


    def getallstates(self,windowname,path):
    ##    windowsrun()
        isjavares, hwnd = self.utils_obj.isjavawindow(windowname)
        state =  self.utilities_obj.getstate(oebs_api.JABContext(hwnd),path,windowname,0,'')
        state = str(state)
        return state

    def rightclick(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.utilops_obj.rightclick(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def clickelement(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.elementsops_obj.clickelement(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getelementtext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.elementsops_obj.getelementtext(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifyelementtext(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if ( accessContext):
            if str(accessContext) != 'fail':
                self.elementsops_obj.verifyelementtext(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getrowcount(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):

            #contextinfo = accessContext.getAccessibleTableInfo()
            #if(contextinfo.role == 'table'):
            #accessContext = oebs_serverUtilities.looptolist(accessContext)
            if str(accessContext) != 'fail':
                self.tableops_obj.getrowcount(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getcolumncount(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):

            #contextinfo = accessContext.getAccessibleTableInfo()
            #if(contextinfo.role == 'table'):
            #accessContext = oebs_serverUtilities.looptolist(accessContext)
            if str(accessContext) != 'fail':
                self.tableops_obj.getcolumncount(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getcellvalue(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.tableops_obj.getcellvalue(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def verifycellvalue(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.tableops_obj.verifycellvalue(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def cellclick(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.tableops_obj.cellclick(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def switchtoframe(self,applicationname,objectname,keyword,inputs,outputs):
    # this method has sends the root object to the keyword implementation
    # unlike other keywords where the actual elements object is sent
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        inputs = ast.literal_eval(str(inputs))
        #input sent from the user
        inputs = ast.literal_eval(str(inputs))
        inputs = [n for n in inputs]
        for index in range(len(inputs)):
            oebs_key_objects.keyword_input.append(inputs[index])
    #output thats to be sent from the server to client
        oebs_key_objects.keyword_output = outputs.split(';')
        isjavares, hwnd = self.utils_obj.isjavawindow(applicationname)
    #root object is taken
        accessContext=oebs_api.JABContext(hwnd)
    #root object is sent to the keyword ie., frame's object is taken to definition
        self.utilops_obj.switchtoframe(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def right(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.scrollbarops_obj.right(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def left(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.scrollbarops_obj.left(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def up(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.scrollbarops_obj.up(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def down(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.scrollbarops_obj.down(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def closeframe(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
           if str(accessContext) != 'fail':
                self.internalframeops_obj.closeframe(accessContext)
        log.debug('MSG:Keyword response : %s',OEBS_INTERNALFRAMEOPS,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def togglemaximize(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.internalframeops_obj.togglemaximize(accessContext)
        log.debug('MSG:Keyword response : %s',OEBS_INTERNALFRAMEOPS,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def toggleminimize(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swoopToElement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            if str(accessContext) != 'fail':
                self.internalframeops_obj.toggleminimize(accessContext)
        log.debug('MSG:Keyword response : %s',OEBS_INTERNALFRAMEOPS,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def waitforelementvisible(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        accessContext =  self.utilities_obj.object_generator(applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        log.debug('MSG:Keyword response : %s',DEF_WAITFORELEMENTVISIBLE,oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def drag(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            self.utilops_obj.drag(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def drop(self,applicationname,objectname,keyword,inputs,outputs):
        # accessContext object gets value on call of swooptoelement definition
        global accessContext
        log.debug('MSG: applicationname:%s , objectname:%s , keyword: %s , inputs:%s , outputs: %s',applicationname,objectname,keyword,inputs,outputs)
        #self.elementsops_obj.waitforelementvisible(applicationname,objectname,keyword,inputs,outputs)
        accessContext = self.utilities_obj.object_generator(applicationname, objectname, keyword, inputs, outputs)
        if (accessContext):
            self.utilops_obj.drop(accessContext)
        log.debug('MSG:Keyword response : %s',oebs_key_objects.keyword_output)
        return self.utilities_obj.clientresponse()

    def getobjectforcustom(self,windowname,parentXpath,type,eleIndex):
        tempne = []
        self.utils_obj.windowsrun()
        log.debug('MSG:Windows Run Executed.')
        isjavares, hwnd = self.utils_obj.isjavawindow(windowname)
        log.debug('MSG:java window status obtained is :%s',str(isjavares))
        if (isjavares):
            eleproperty=self.utilities_obj.getobjectforcustom(oebs_api.JABContext(hwnd),windowname,parentXpath,type,eleIndex)
##            log.debug('MSG:The Scraped Data is:\n %s',tempne)
            return eleproperty
        else:
            log.debug('MSG: %s',MSG_NOT_JAVA_WINDOW_INFO)
            return 'fail'
