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

import oebs_utils
import logging
import oebs_api
from oebs_constants import *
import ast
import json
import re
import win32gui
access=''
index=0
k = 0
cordinates = []
states = []
win_rect = ''

log = logging.getLogger('oebs_fullscrape.py')

class FullScrape:

    def getentireobjectlist(self,windowname):
        utils_obj=oebs_utils.Utils()
        tempne = []
        utils_obj.windowsrun()
        log.debug('MSG:\nWindows Run Executed.',DEF_GETENTIREOBJECTLIST)
        isjavares, hwnd = utils_obj.isjavawindow(windowname)
        log.debug('FILE: %s, DEF: %s , MSG:\njava window status obtained is :%s',str(isjavares))
        if (isjavares):
            global win_rect
            win_rect= win32gui.GetWindowRect(hwnd)
            self.acccontext(oebs_api.JABContext(hwnd), tempne,'',0,windowname)
            log.debug('MSG:\nThe Scraped Data is:\n %s',tempne)
            vie = {'view': tempne}
            utils_obj.save_json(vie)
            return json.dumps(vie)
        else:
            log.debug('MSG: %s',MSG_NOT_JAVA_WINDOW_INFO)
            return 'fail'
    #method to find window rectangle for custom objects
    def custom_winrect(self,windowname):
        utils_obj=oebs_utils.Utils()
        tempne = []
        utils_obj.windowsrun()
        log.debug('MSG:\nWindows Run Executed.',"custom_winrect")
        isjavares, hwnd = utils_obj.isjavawindow(windowname)
        log.debug('FILE: %s, DEF: %s , MSG:\njava window status obtained is :%s',str(isjavares))
        if (isjavares):
            global win_rect
            win_rect= win32gui.GetWindowRect(hwnd)
    #Method accontext called by getentireobjectlist
    #contains full scrape logic
    def acccontext(self,acc, tempne,xpath,i,window):
        curaccinfo = acc.getAccessibleContextInfo()
        tagrole = curaccinfo.role
        tagname = curaccinfo.name
        text = curaccinfo.name
        if xpath == '':
            if len(curaccinfo.description.strip()) == 0:
                path = curaccinfo.role + '[' + str(i) + ']'
            else:
                if 'panel' in curaccinfo.role:
                    path = curaccinfo.role  + '[' + str(i) + ']'
                else:
                   path  = curaccinfo.role + '[' + str(curaccinfo.description.strip()) + ']'
        else:
            if len(curaccinfo.description.strip()) == 0:
                path = xpath + '/' + curaccinfo.role  + '[' + str(i) + ']'
            else:
                if 'panel' in curaccinfo.role:
                    path = xpath + '/' + curaccinfo.role + '[' + str(i) + ']'
                else:
                    path = xpath + '/' + curaccinfo.role  + '[' + str(curaccinfo.description.strip()) + ']'

        if len( curaccinfo.name) == 0 :
            tagname = curaccinfo.role
        if curaccinfo.accessibleText == 1:
            charinfo = acc.getAccessibleTextInfo(0,1)
            text = acc.getAccessibleTextRange(0,charinfo.charCount - 1)
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
        hiddentag = True
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
            hiddentag = False
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
        text = str(text)
        text = text.strip()
        x1_win = win_rect[0]
        y1_win = win_rect[1]
        x2_win = win_rect[2]
        y2_win = win_rect[3]
        width_win = x2_win - x1_win
        height_win = y2_win - y1_win

        x_coor=curaccinfo.x
        y_coor=curaccinfo.y
        width=curaccinfo.width
        height=curaccinfo.height

        left_need = x_coor 
        top_need =  y_coor 

        if len(text) == 0:
            text = tagname
        text = text.replace('<','')
        text = text.replace('>','')
        custname = None
        custname = self.postfixCustname(str(curaccinfo.role),text.strip())
        tempne.append({"custname":custname,
                "tag":curaccinfo.role,
                "xpath":path + ';' + name.strip() + ';' + str(indexInParent)  + ';' + str(childrencount) + ';'+ str(parentname).strip() + ';' + str(parentxpath) + ';' + str(parentchildcount) + ';' + str(parentindex)+ ';' + str(parenttag)+ ';' + str(curaccinfo.role) + ';' + description,
                'hiddentag':str(hiddentag),
                'id':'null',
                "text":text.strip(),
                "url":window,
                "left":left_need,
                "top":top_need,
                "width":width,
                "height":height})
        for i in range(curaccinfo.childrenCount):
            childacc = acc.getAccessibleChildFromContext(i)
            self.acccontext(childacc, tempne,path,i,window)

    def postfixCustname(self,role,custname):
        if(role in ['push button','toggle button']):
            custname = custname + "_btn"
        elif(role in ['edit','Edit Box','text','password text']):
            custname = custname + "_txtbox"
        elif(role == 'combo box'):
            custname = custname +"_select"
        elif(role == 'radio button'):
            custname = custname + "_radiobtn"
        elif(role == 'check box'):
            custname = custname + "_chkbox"
        elif(role == 'table'):
            custname = custname + "_table"
        elif(role in ['list item','list']):
            custname = custname + "_lst"
        elif(role == 'internal frame'):
            custname = custname + "_internalframe"
        elif(role == 'frame'):
            custname = custname + "_frame"
        elif(role == "scroll bar"):
            custname = custname + "_scroll"
        elif(role in ['hyperlink','Static']):
            custname = custname + "_link"
        else:
            custname = custname + "_elmnt"
        return custname

    def acccontext_custom(self,acc, tempne,xpath,i,window):
        curaccinfo = acc.getAccessibleContextInfo()
        tagrole = curaccinfo.role
        tagname = curaccinfo.name
        text = curaccinfo.name
        if xpath == '':
            if len(curaccinfo.description.strip()) == 0:
                path = curaccinfo.role + '[' + str(i) + ']'
            else:
                if 'panel' in curaccinfo.role:
                    path = curaccinfo.role  + '[' + str(i) + ']'
                else:
                    path  = curaccinfo.role + '[' + str(i) + ']' + '[' + str(curaccinfo.description.strip()) + ']'
        else:
            if len(curaccinfo.description.strip()) == 0:
                path = xpath + '/' + curaccinfo.role  + '[' + str(i) + ']'
            else:
                if 'panel' in curaccinfo.role:
                    path = xpath + '/' + curaccinfo.role + '[' + str(i) + ']'
                else:
                    path = xpath + '/' + curaccinfo.role + '[' + str(i) + ']' + '[' + str(curaccinfo.description.strip()) + ']'

        if len( curaccinfo.name) == 0 :
            tagname = curaccinfo.role
        if curaccinfo.accessibleText == 1:
            charinfo = acc.getAccessibleTextInfo(0,1)
            text = acc.getAccessibleTextRange(0,charinfo.charCount - 1)
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
        hiddentag = True
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
            hiddentag = False
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
        text = str(text)
        text = text.strip()
        x1_win = win_rect[0]
        y1_win = win_rect[1]
        x2_win = win_rect[2]
        y2_win = win_rect[3]
        width_win = x2_win - x1_win
        height_win = y2_win - y1_win

        x_coor=curaccinfo.x
        y_coor=curaccinfo.y
        width=curaccinfo.width
        height=curaccinfo.height

        left_need = x_coor 
        top_need =  y_coor 

        if len(text) == 0:
            text = tagname
        text = text.replace('<','')
        text = text.replace('>','')
        custname = None
        custname = self.postfixCustname(str(curaccinfo.role),text.strip())
        # objects which are not on the Screen wont be added to list
        non_interactable = False
        if curaccinfo.role in ["text", "password text", "push button", "radio button", "check box", "combo box", "list"] and (len(description.strip()) == 0 or description == "[ ]" or "enabled" not in curaccinfo.states or 'showing' not in  curaccinfo.states):
            non_interactable = True
        if non_interactable == False:
            tempne.append({"custname":custname,
                "tag":curaccinfo.role,
                "xpath":path + ';' + name.strip() + ';' + str(indexInParent)  + ';' + str(childrencount) + ';'+ str(parentname).strip() + ';' + str(parentxpath) + ';' + str(parentchildcount) + ';' + str(parentindex)+ ';' + str(parenttag)+ ';' + str(curaccinfo.role) + ';' + description,
                'hiddentag':str(hiddentag),
                'id':'null',
                "text":text.strip(),
                "url":window,
                "left":left_need,
                "top":top_need,
                "width":width,
                "height":height})
        for i in range(curaccinfo.childrenCount):
            childacc = acc.getAccessibleChildFromContext(i)
            self.acccontext_custom(childacc, tempne,path,i,window)