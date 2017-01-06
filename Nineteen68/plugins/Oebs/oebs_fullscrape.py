#-------------------------------------------------------------------------------
# Name:        oebs_fullscrape.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     15-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

##import oebs_key_objects
##import oebsServer
import utils
import logging
import oebs_api
from oebs_msg import *
import ast
import json
import re
access=''
index=0
k = 0
cordinates = []
states = []

log = logging.getLogger('oebs_fullscrape.py')

class FullScrape:

    def getentireobjectlist(self,windowname):
        utils_obj=utils.Utils()
        tempne = []
        utils_obj.windowsrun()
        log.debug('MSG:\nWindows Run Executed.',DEF_GETENTIREOBJECTLIST)
        isjavares, hwnd = utils_obj.isjavawindow(windowname)
        log.debug('FILE: %s, DEF: %s , MSG:\njava window status obtained is :%s',str(isjavares))
        if (isjavares):
            self.acccontext(oebs_api.JABContext(hwnd), tempne,'',0,windowname)
            log.debug('MSG:\nThe Scraped Data is:\n %s',tempne)
            vie = {'view': tempne}
            utils_obj.save_json(vie)
            return json.dumps(vie)
        else:
            log.debug('MSG: %s',MSG_NOT_JAVA_WINDOW_INFO)
            return 'fail'

    #Method accontext called by getentireobjectlist
    #contains full scrape logic
    def acccontext(self,acc, tempne,xpath,i,window):
        curaccinfo = acc.getAccessibleContextInfo()
       # path = getXpath(acc)
        tagrole = curaccinfo.role
        tagname = curaccinfo.name
        text = curaccinfo.name
        if xpath == '':
            if len(curaccinfo.name.strip()) == 0:
                path = curaccinfo.role + '[' + str(i) + ']'
            else:
                if 'panel' in curaccinfo.role:
                    path = curaccinfo.role  + '[' + str(i) + ']'
                else:
                   path  = curaccinfo.role + '[' + str(curaccinfo.name.strip()) + ']'
        else:
            if len(curaccinfo.name.strip()) == 0:
                path = xpath + '/' + curaccinfo.role  + '[' + str(i) + ']'
            else:
                if 'panel' in curaccinfo.role:
                    path = xpath + '/' + curaccinfo.role + '[' + str(i) + ']'
                else:
                    path = xpath + '/' + curaccinfo.role  + '[' + str(curaccinfo.name.strip()) + ']'

        if len( curaccinfo.name) == 0 :
            tagname = curaccinfo.role
        if curaccinfo.accessibleText == 1:
            charinfo = acc.getAccessibleTextInfo(0,1)
            text = acc.getAccessibleTextRange(0,charinfo.charCount - 1)
        text = text.encode('utf-8').strip()
        text = str(text)
        text = text.strip()
        if len(text) == 0:
            text = tagrole
        text = text.replace('<','')
        text = text.replace('>','')
        childrencount = curaccinfo.childrenCount
        name = ''
        description = 'null'
        indexInParent = 'null'
        parentname = ''
        parenttag = 'null'
        parentchildcount = 'null'
        parentindex = 'null'
        parentxpathtemp = 'null'
        parentxpath = 'null'
        if (curaccinfo.name):
            name = curaccinfo.name
        else:
            name = ''
        if (curaccinfo.description):
            description = curaccinfo.description
        else:
            description = ''
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
            if len(name.strip() ) == 0:
                name = ''
            if len(parentname.strip()) == 0:
                parentname = ''
            if len(curaccinfo.name) == 0 :
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
            tempne.append({"custname":text.strip(),
                    "tag":curaccinfo.role,
                    "xpath":path + ';' + name.strip() + ';' + str(indexInParent)  + ';' + str(childrencount) + ';'+ str(parentname).strip() + ';' + str(parentxpath) + ';' + str(parentchildcount) + ';' + str(parentindex)+ ';' + str(parenttag)+ ';' + str(curaccinfo.role) + ';' + description,
                    'hiddentag':'No',
                    'id':'null',
                    "text":text.strip(),
                    "url":window})
        for i in range(curaccinfo.childrenCount):
            childacc = acc.getAccessibleChildFromContext(i)
            self.acccontext(childacc, tempne,path,i,window)


