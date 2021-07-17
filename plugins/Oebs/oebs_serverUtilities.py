#-------------------------------------------------------------------------------
# Name:        oebs_serverUtilities.py
# Purpose:     This file contains the primary objects for each keyword
#
# Author:      sushma.p
#
# Created:     24-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import oebs_key_objects
import oebs_utils
import oebs_fullscrape
import oebs_api
from oebs_constants import *
import oebs_click_and_add
import ast
import json
import re
global count
count=''
accessContext=''
accessContextParent = ''
access=''
index=0
k = 0
cordinates = []
states = []
objectDict = {}
objectDictWithNameDesc={}
activeframename=''
deletedobjectlist=[]
import logger
import logging

log = logging.getLogger('oebs_serverUtilities.py')

class Utilities:

    #Method to swoop till the element at the given Object location
    def swooptoelement(self,a,objecttofind,currentxpathtemp,i,p,windowname):
        queue = []
        active_parent = False
        queue.append((p,a,i))
        identifiers = objecttofind.split(';')
        uniquepath = identifiers[0]
        name = identifiers[1]
        indexinParent = identifiers[2]
        childrencount = identifiers[3]
        parentname = identifiers[4]
        parxpath = identifiers[5]
        parentchildcount = identifiers[6]
        parentindex = identifiers[7]
        parenttag = identifiers[8]
        childtag = identifiers[9]
        #getting the internal frame name :
        
        internal_frame_list = []
        for each_internal_frame in uniquepath.split('/'):
            if each_internal_frame.find('internal frame')!=-1:
                internal_frame_list.append(each_internal_frame.lstrip('internal frame[')[:-1])
        
        while len(queue) > 0:
            xpath, acc, index = queue.pop(0)
            elementObj = acc.getAccessibleContextInfo()

            if xpath == '':
                if len(elementObj.name.strip()) == 0:
                    if 'internal frame' in elementObj.role or 'frame' in elementObj.role:
                        path = elementObj.role
                    elif 'panel' in elementObj.role:
                        path = elementObj.role + '[' + str(index) + ']'
                    else:
                        path = elementObj.role + '[' + str(index) + ']'

                else:
                    if 'internal frame' in elementObj.role or 'frame' in elementObj.role:
                        path = elementObj.role
                    elif 'panel' in elementObj.role:
                        path = elementObj.role + '[' + str(index) + ']'
                    else:
                        path = elementObj.role + '[' + str(elementObj.name.strip()) + ']'

            else:
                if len(elementObj.name.strip()) == 0:
                    if 'internal frame' in elementObj.role:
                        path = xpath + '/' + elementObj.role
                    elif 'panel' in elementObj.role:
                        path = xpath + '/' + elementObj.role + '[' + str(index) + ']'
                    else:
                        path = xpath + '/' + elementObj.role  + '[' + str(index) + ']'

                else:
                    if 'internal frame' in elementObj.role:
                        path = xpath + '/' + elementObj.role
                    elif 'panel' in elementObj.role:
                        path = xpath + '/' + elementObj.role + '[' + str(index) + ']'
                    else:
                        path = xpath + '/' + elementObj.role  + '[' + str(elementObj.name.strip()) + ']'

            if path == currentxpathtemp:
                global accessContextParent
                accessContextParent = acc
                return active_parent

            curr = currentxpathtemp.split('/')
            p = path.split('/')
            index = len(p) - 1
            if curr[index] == p[index]:
                if 'active' in elementObj.states and windowname != elementObj.name:
                    active_parent = True
                for index in range(elementObj.childrenCount):
                    elementObj = acc.getAccessibleChildFromContext(index)

                    elementcontext=elementObj.getAccessibleContextInfo()
                    if elementcontext.role == 'internal frame':
                        if 'active' in elementcontext.states:
                            queue.append((path, elementObj, index))
                        else:
                            hasinternal=0
                            children=elementcontext.childrenCount
                            for childrencount in range(int(children)):
                                childobj=elementObj.getAccessibleChildFromContext(childrencount)
                                childrencontext=childobj.getAccessibleContextInfo()
                                if 'internal frame' in childrencontext.role:
                                    hasinternal=1
                                    break
                            if hasinternal ==1:
                                queue.append((path, elementObj, index))
                            else:
                                index = index + 1
                    else:
                        queue.append((path, elementObj, index))     

    def methodtofillmap(self,acc,xpath,i):
        global  accessContext
        curaccinfo = acc.getAccessibleContextInfo()
        tagrole = curaccinfo.role
        tagname = ''
        text = curaccinfo.name
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

        global activeframename
        if('internal frame' in curaccinfo.role):
            if('active' in curaccinfo.states):
                activeframename=curaccinfo.name.strip()

        if(activeframename):
            if(activeframename in path):
                global objectDictWithNameDesc
                name=''
                desc=''
                if(curaccinfo.name):
                    name=str(curaccinfo.name)
                else:
                    name=str(curaccinfo.name)
                if(curaccinfo.description):
                    desc=str(curaccinfo.description)
                else:
                    desc=str(curaccinfo.description)
                namewithdesc=name+';'+desc
                if(deletedobjectlist):
                    if(not(namewithdesc in deletedobjectlist)):
                        if(namewithdesc in objectDictWithNameDesc):
                            objectDictWithNameDesc.pop(namewithdesc)
                            deletedobjectlist.append(namewithdesc)
                        else:
                            objectDictWithNameDesc[namewithdesc]=path
                elif(objectDictWithNameDesc):
                    if(namewithdesc in objectDictWithNameDesc):
                        objectDictWithNameDesc.pop(namewithdesc)
                        deletedobjectlist.append(namewithdesc)
                    else:
                        objectDictWithNameDesc[namewithdesc]=path

                else:
                    objectDictWithNameDesc[namewithdesc]=path

        for i in range(curaccinfo.childrenCount):
            childacc = acc.getAccessibleChildFromContext(i)
            acc.releaseJavaObject()
            self.methodtofillmap(childacc,path,i)
        return accessContext


    def object_generator(self,applicationname,locator,keyword,inputs,outputs):
        global accessContext
        global ELEMENT_FOUND
        ELEMENT_FOUND=False
        active_parent = None
        #OBJECTLOCATION for the object is sent from the user
        del oebs_key_objects.keyword_input[:]
        oebs_key_objects.xpath = locator
        #Application name is sent from the user
        oebs_key_objects.applicationname = applicationname
        utils_obj=oebs_utils.Utils()
        isjavares, hwnd = utils_obj.isjavawindow(oebs_key_objects.applicationname)
        #method enables to move to perticular object and fetches its Contexts
        uniquepath=oebs_key_objects.xpath
        flag = 'false'
        if ';' in uniquepath:
            requiredxpath = uniquepath.split(';')
            parentxpathtemp = ''
            parentxpathtemp = requiredxpath[5]

            regularexp = re.compile('(frame(.*?|\s)*[\]]+)')
            newxpath = regularexp.findall(parentxpathtemp)

            newlist2=[]
            for i in range(len(newxpath)):
                newlist2.append(newxpath[i][0])

            for i in range(len(newlist2)):
                parentxpathtemp=parentxpathtemp.replace(newlist2[i],'frame')

            active_parent = self.swooptoelement(oebs_api.JABContext(hwnd),oebs_key_objects.xpath,parentxpathtemp,0,'', applicationname)
            if active_parent is None:
                active_parent = False
            self.methodtofillmap(oebs_api.JABContext(hwnd),'',0)

            identifiers = oebs_key_objects.xpath.split(';')
            uniquepath = identifiers[0]
            name = identifiers[1]
            indexinParent = identifiers[2]
            childrencount = identifiers[3]
            parentname = identifiers[4]
            parxpath = identifiers[5]
            parentchildcount = identifiers[6]
            parentindex = identifiers[7]
            parenttag = identifiers[8]
            childtag = identifiers[9]
            description=''
            try:
                description=identifiers[10]
            except Exception:
                description=''
            global accessContextParent
            retacc = accessContextParent
            keytocompare=name+';'+description
            if(keytocompare in objectDictWithNameDesc):
                xpathneeded=objectDictWithNameDesc.get(keytocompare)
                regularexp = re.compile('(frame(.*?|\s)*[\]]+)')
                newxpath = regularexp.findall(xpathneeded)

                newlist2=[]
                for i in range(len(newxpath)):
                    newlist2.append(newxpath[i][0])

                for i in range(len(newlist2)):
                    xpathneeded=xpathneeded.replace(newlist2[i],'frame')
                if(accessContextParent):
                    accessContextParent.releaseJavaObject()
                self.swooptoelement(oebs_api.JABContext(hwnd),oebs_key_objects.xpath,xpathneeded,0,'', applicationname)
                accessContext=accessContextParent
                flag='true'

            elif (accessContextParent):
                tema = retacc.getAccessibleContextInfo()
                if retacc is not None:
                    parentInfo = retacc.getAccessibleContextInfo()
                    accarrname = []
                    accarrdesc = []

                    for index in range(parentInfo.childrenCount):
                        elementObj = retacc.getAccessibleChildFromContext(index)
                        childInfo = elementObj.getAccessibleContextInfo()
                        if len(childInfo.name) > 0 :
                            if ((name == str(childInfo.name).strip()) and (childtag == str(childInfo.role))):
                                accessContext = elementObj
                                accarrname.append(elementObj)

                    if(len(accarrname) > 1 or len(accarrname) == 0):
                        for index in range(parentInfo.childrenCount):
                            elementObj = retacc.getAccessibleChildFromContext(index)
                            childInfo = elementObj.getAccessibleContextInfo()
                            if len(description) != 0 and len(childInfo.description) > 0:
                                if (description == str(childInfo.description).strip() and childtag == str(childInfo.role)):
                                    accessContext=elementObj
                                    accarrdesc.append(elementObj)

                        if(len(accarrdesc) > 1 or len(accarrdesc) == 0):
                            if( int(parentchildcount) < int(parentInfo.childrenCount)):
                                for index in range(parentInfo.childrenCount):
                                    elementObj = retacc.getAccessibleChildFromContext(index)
                                    childInfo = elementObj.getAccessibleContextInfo()
                                    if('focused' in childInfo.states):
                                        firstelecontext=retacc.getAccessibleChildFromContext(0)
                                        firsteleinfo=firstelecontext.getAccessibleContextInfo()
                                        if((firsteleinfo.role == 'text') and (firsteleinfo.childrenCount == 1)):
                                            firstelechildcontext=firstelecontext.getAccessibleChildFromContext(0)
                                            firstelechildinfo=firstelechildcontext.getAccessibleContextInfo()
                                            if(firstelechildinfo.role == 'push button'):
                                                indexinParent=int(indexinParent)+1
                                                for index in range(parentInfo.childrenCount):
                                                    elementObj = retacc.getAccessibleChildFromContext(index)
                                                    childInfo = elementObj.getAccessibleContextInfo()
                                                    if(str(indexinParent) == str(childInfo.indexInParent).strip() and childtag == str(childInfo.role)):
                                                        accessContext=elementObj
                                                        flag = 'true'
                                                        break
                                    elif(not('internal frame' in parentxpathtemp)):
                                         for index in range(parentInfo.childrenCount):
                                            elementObj = retacc.getAccessibleChildFromContext(index)
                                            childInfo = elementObj.getAccessibleContextInfo()
                                            if(str(indexinParent) == str(childInfo.indexInParent).strip() and childtag == str(childInfo.role)):
                                                accessContext=elementObj
                                                flag = 'true'
                                                break
                            else:
                                for index in range(parentInfo.childrenCount):
                                    elementObj = retacc.getAccessibleChildFromContext(index)
                                    childInfo = elementObj.getAccessibleContextInfo()
                                    if(str(indexinParent) == str(childInfo.indexInParent).strip() and childtag == str(childInfo.role)):
                                        accessContext=elementObj
                                        flag = 'true'
                                        break
                        else:
                            accessContext = accarrdesc[0]
                            flag = 'true'
                    else:
                        accessContext = accarrname[0]
                        flag = 'true'


        #keyword is sent from the user
        oebs_key_objects.keyword = keyword
        #input sent from the user
        inputs = ast.literal_eval(str(inputs))
        inputs = [n for n in inputs]

        for index in range(len(inputs)):
            oebs_key_objects.keyword_input.append(inputs[index])
        #output thats to be sent from the server to client
        oebs_key_objects.keyword_output = outputs.split(';')

        if flag == 'true' :
             ELEMENT_FOUND=True
             return accessContext
        else :
            ELEMENT_FOUND=False
            return 'fail'

    def object_generator_test(self,applicationname,locator,keyword,inputs,outputs):
            global accessContext
            global ELEMENT_FOUND
            ELEMENT_FOUND=False
            active_parent = None
            #OBJECTLOCATION for the object is sent from the user
            del oebs_key_objects.keyword_input[:]
            oebs_key_objects.xpath = locator
            #Application name is sent from the user
            oebs_key_objects.applicationname = applicationname
            utils_obj=oebs_utils.Utils()
            isjavares, hwnd = utils_obj.isjavawindow(oebs_key_objects.applicationname)
            #method enables to move to perticular object and fetches its Contexts
            uniquepath=oebs_key_objects.xpath
            flag = 'false'
            if ';' in uniquepath:
                requiredxpath = uniquepath.split(';')
                parentxpathtemp = ''
                parentxpathtemp = requiredxpath[5]

                regularexp = re.compile('(frame(.*?|\s)*[\]]+)')
                newxpath = regularexp.findall(parentxpathtemp)

                newlist2=[]
                for i in range(len(newxpath)):
                    newlist2.append(newxpath[i][0])

                for i in range(len(newlist2)):
                    parentxpathtemp=parentxpathtemp.replace(newlist2[i],'frame')

                active_parent = self.swooptoelement(oebs_api.JABContext(hwnd),oebs_key_objects.xpath,parentxpathtemp,0,'', applicationname)
                if active_parent is None:
                    active_parent = False
                self.methodtofillmap(oebs_api.JABContext(hwnd),'',0)

                identifiers = oebs_key_objects.xpath.split(';')
                uniquepath = identifiers[0]
                name = identifiers[1]
                indexinParent = identifiers[2]
                childrencount = identifiers[3]
                parentname = identifiers[4]
                parxpath = identifiers[5]
                parentchildcount = identifiers[6]
                parentindex = identifiers[7]
                parenttag = identifiers[8]
                childtag = identifiers[9]
                description=''
                try:
                    description=identifiers[10]
                except Exception:
                    description=''
                global accessContextParent
                retacc = accessContextParent
                keytocompare=name+';'+description
                if(keytocompare in objectDictWithNameDesc):
                    xpathneeded=objectDictWithNameDesc.get(keytocompare)
                    regularexp = re.compile('(frame(.*?|\s)*[\]]+)')
                    newxpath = regularexp.findall(xpathneeded)

                    newlist2=[]
                    for i in range(len(newxpath)):
                        newlist2.append(newxpath[i][0])

                    for i in range(len(newlist2)):
                        xpathneeded=xpathneeded.replace(newlist2[i],'frame')
                    if(accessContextParent):
                        accessContextParent.releaseJavaObject()
                    self.swooptoelement(oebs_api.JABContext(hwnd),oebs_key_objects.xpath,xpathneeded,0,'', applicationname)
                    accessContext=accessContextParent
                    flag='true'

                elif (accessContextParent):
                    tema = retacc.getAccessibleContextInfo()
                    if retacc is not None:
                        parentInfo = retacc.getAccessibleContextInfo()
                        accarrname = []
                        accarrdesc = []

                        for index in range(parentInfo.childrenCount):
                            elementObj = retacc.getAccessibleChildFromContext(index)
                            childInfo = elementObj.getAccessibleContextInfo()
                            if len(childInfo.name) > 0 :
                                if ((name == str(childInfo.name).strip()) and (childtag == str(childInfo.role))):
                                    accessContext = elementObj
                                    accarrname.append(elementObj)

                        if(len(accarrname) > 1 or len(accarrname) == 0):
                            for index in range(parentInfo.childrenCount):
                                elementObj = retacc.getAccessibleChildFromContext(index)
                                childInfo = elementObj.getAccessibleContextInfo()
                                if len(description) != 0 and len(childInfo.description) > 0:
                                    if (description == str(childInfo.description).strip() and childtag == str(childInfo.role)):
                                        accessContext=elementObj
                                        accarrdesc.append(elementObj)

                            if(len(accarrdesc) > 1 or len(accarrdesc) == 0):
                                if( int(parentchildcount) < int(parentInfo.childrenCount)):
                                    for index in range(parentInfo.childrenCount):
                                        elementObj = retacc.getAccessibleChildFromContext(index)
                                        childInfo = elementObj.getAccessibleContextInfo()
                                        if('focused' in childInfo.states):
                                            firstelecontext=retacc.getAccessibleChildFromContext(0)
                                            firsteleinfo=firstelecontext.getAccessibleContextInfo()
                                            if((firsteleinfo.role == 'text') and (firsteleinfo.childrenCount == 1)):
                                                firstelechildcontext=firstelecontext.getAccessibleChildFromContext(0)
                                                firstelechildinfo=firstelechildcontext.getAccessibleContextInfo()
                                                if(firstelechildinfo.role == 'push button'):
                                                    indexinParent=int(indexinParent)+1
                                                    for index in range(parentInfo.childrenCount):
                                                        elementObj = retacc.getAccessibleChildFromContext(index)
                                                        childInfo = elementObj.getAccessibleContextInfo()
                                                        if(str(indexinParent) == str(childInfo.indexInParent).strip() and childtag == str(childInfo.role)):
                                                            accessContext=elementObj
                                                            flag = 'true'
                                                            break
                                        elif(not('internal frame' in parentxpathtemp)):
                                            for index in range(parentInfo.childrenCount):
                                                elementObj = retacc.getAccessibleChildFromContext(index)
                                                childInfo = elementObj.getAccessibleContextInfo()
                                                if(str(indexinParent) == str(childInfo.indexInParent).strip() and childtag == str(childInfo.role)):
                                                    accessContext=elementObj
                                                    flag = 'true'
                                                    break
                                else:
                                    for index in range(parentInfo.childrenCount):
                                        elementObj = retacc.getAccessibleChildFromContext(index)
                                        childInfo = elementObj.getAccessibleContextInfo()
                                        if(str(indexinParent) == str(childInfo.indexInParent).strip() and childtag == str(childInfo.role)):
                                            accessContext=elementObj
                                            flag = 'true'
                                            break
                            else:
                                accessContext = accarrdesc[0]
                                flag = 'true'
                        else:
                            accessContext = accarrname[0]
                            flag = 'true'


            #keyword is sent from the user
            oebs_key_objects.keyword = keyword
            #input sent from the user
            inputs = ast.literal_eval(str(inputs))
            inputs = [n for n in inputs]

            for index in range(len(inputs)):
                oebs_key_objects.keyword_input.append(inputs[index])
            #output thats to be sent from the server to client
            oebs_key_objects.keyword_output = outputs.split(';')

            if flag == 'true' :
                ELEMENT_FOUND=True
                return accessContext, active_parent
            else :
                ELEMENT_FOUND=False
                return 'fail', active_parent


    def getsize(self,xpath,windowname):
        #object is identified using normal object identification
        self.object_generator(windowname,xpath,'',[],'')
        #context is taken from global value
        global accessContext
        acc=accessContext
        #fetching the context
        curaccinfo=acc.getAccessibleContextInfo()
        global cordinates
        cordinates.append(curaccinfo.x)
        cordinates.append(curaccinfo.y)
        cordinates.append(curaccinfo.width)
        cordinates.append(curaccinfo.height)
        return cordinates

    #Method to get the states

    def getstate(self,acc,loc,url,i,xpath):
        curaccinfo = acc.getAccessibleContextInfo()
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
        if path == loc:
            global k
            k = 1;
        for i in range(curaccinfo.childrenCount):
            if k == 0:
                childacc = acc.getAccessibleChildFromContext(i)
                acc.releaseJavaObject()
                getstate(childacc,loc,url,i,path)
        if k == 1:
            return curaccinfo.states
        else:
            return 'abc'

    #Method to get looptolist for dropdown
    def looptolist(self,acc):
        global accessContext
        charinfo = acc.getAccessibleContextInfo()
        for i in range(charinfo.childrenCount):
            childacc = acc.getAccessibleChildFromContext(i)
            acc.releaseJavaObject()
            contextInfo = childacc.getAccessibleContextInfo()
            if contextInfo.role == 'list':
                accessContext = childacc
                break
            self.looptolist(childacc)
        return accessContext

    def clientresponse(self,*args):
        clientresp=()
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=None
        err_msg=None
        if(oebs_key_objects.keyword_output[0] != ''):
            if oebs_key_objects.keyword_output[0]== MSG_PASS:
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
                output=oebs_key_objects.keyword_output[1]
            elif len(oebs_key_objects.keyword_output) > 1:
                output=oebs_key_objects.keyword_output[1]
            else:
                err_msg = ERROR_CODE_DICT['err_window_find']
                logger.print_on_console(err_msg)
                log.error(err_msg)

        else:
            del oebs_key_objects.custom_msg[:]
            oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_FOUND)
            logger.print_on_console(MSG_ELEMENT_NOT_FOUND)
            if len(args)>0:
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE

        if oebs_key_objects.custom_msg != [] and status==TEST_RESULT_FAIL:
            err_msg=oebs_key_objects.custom_msg[0]

        if methodoutput==output:
            output=OUTPUT_CONSTANT

        clientresp=(status,methodoutput,output,err_msg)

        global accessContext
        if type(accessContext) != str:
            accessContext.releaseJavaObject()
        return clientresp

    def cleardata(self):
        del oebs_key_objects.keyword_input[:]
        del oebs_key_objects.keyword_output[:]

    def menugenerator(self,acc):
        self.menubarelement(acc,0,'')
        global accessContext
        return accessContext

    def menubarelement(self,acc,index,xpath):
        global accessContext
        elementObj = acc.getAccessibleContextInfo()
        if xpath == '':
             if len(elementObj.name.strip()) == 0:
                if 'internal frame' in elementObj.role:
                    path = elementObj.role
                else:
                    path = elementObj.role + '[' + str(index) + ']'
             else:
                if 'internal frame' in elementObj.role:
                    path = elementObj.role
                else:
                    path = elementObj.role + '[' + str(elementObj.name.strip()) + ']'
        else:
            if len(elementObj.name.strip()) == 0:
                if 'internal frame' in elementObj.role:
                    path = xpath + '/' + elementObj.role
                else:
                    path = xpath + '/' + elementObj.role  + '[' + str(index) + ']'
            else:
                if 'internal frame' in elementObj.role:
                    path = xpath + '/' + elementObj.role
                else:
                    path = xpath + '/' + elementObj.role  + '[' + str(elementObj.name.strip()) + ']'
        if 'menu bar' in elementObj.role:
            accessContext=acc
        for index in range(int(elementObj.childrenCount)):
            elementObj = acc.getAccessibleChildFromContext(index)
            acc.releaseJavaObject()
            elementcontext=elementObj.getAccessibleContextInfo()
            self.menubarelement(elementObj,index,path)


    def getobjectforcustom(self,acc,window,parentxpath,type,eleIndex):
        fullscrape_obj=oebs_fullscrape.FullScrape()
        tempne=[]
        eleproperties=''
        xpath=''
        counter=0
        xpathsplitarr=parentxpath.split(';')
        parentxpath=xpathsplitarr[0]
        if(int(eleIndex) < 0):
            return eleproperties
        descriptiongiven=xpathsplitarr[10]
        fullscrape_obj.custom_winrect(window)
        fullscrape_obj.acccontext(acc,tempne,xpath,0,window)
        verifyflag=False
        for i in range(len(tempne)):
            xpatharr=(str(tempne[i].get('xpath'))).split(';')
            tag=str(tempne[i].get('tag'))
            path=xpatharr[0]
            runTimedescription=''
            if(xpatharr[10]):
                runTimedescription=xpatharr[10]
            if(parentxpath== path and verifyflag == False):
                verifyflag = True
            elif(verifyflag == False and descriptiongiven == runTimedescription):
                verifyflag = True
            if(verifyflag):
                if( not((tag == 'panel') or (tag == 'scroll pane') or (tag =='viewport'))):
                    if(tag == type):
                        if(int(counter) == int(eleIndex)):
                            eleproperties=str(tempne[i].get('xpath'))
                            return eleproperties
                        counter+=1

        return eleproperties


