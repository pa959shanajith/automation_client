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
import oebsServer
import oebs_api
from oebs_msg import *
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

class Utilities:
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


    #Method to swoop till the element at the given Object location
    def swooptoelement(self,acc,objecttofind,currentxpathtemp,index,xpath):
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

    #    print path
        if path == currentxpathtemp:
            global accessContextParent

            #accessContext = acc
            accessContextParent = acc
            #print accessContextParent

        for index in range(elementObj.childrenCount):
            elementObj = acc.getAccessibleChildFromContext(index)

            elementcontext=elementObj.getAccessibleContextInfo()
            if elementcontext.role == 'internal frame':
                if 'active' in elementcontext.states:
                    self.swooptoelement(elementObj,objecttofind,currentxpathtemp,index,path)
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
                        self.swooptoelement(elementObj,objecttofind,currentxpathtemp,index,path)
                    else:
                        index = index + 1
            else:
                self.swooptoelement(elementObj,objecttofind,currentxpathtemp,index,path)




    def methodtofillmap(self,acc,xpath,i):
        global  accessContext
        curaccinfo = acc.getAccessibleContextInfo()
       # path = getXpath(acc)
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
                        if(objectDictWithNameDesc.has_key(namewithdesc)):
                            objectDictWithNameDesc.pop(namewithdesc)
                            deletedobjectlist.append(namewithdesc)
                        else:
                            objectDictWithNameDesc[namewithdesc]=path
                elif(objectDictWithNameDesc):
                    if(objectDictWithNameDesc.has_key(namewithdesc)):
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
        #OBJECTLOCATION for the object is sent from the user
        del oebs_key_objects.keyword_input[:]
        oebs_key_objects.xpath = locator
        #Application name is sent from the user
        oebs_key_objects.applicationname = applicationname
        oebsServer_obj=oebsServer.OebsKeywords()
        isjavares, hwnd = oebsServer_obj.isjavawindow(oebs_key_objects.applicationname)
        #method enables to move to perticular object and fetches its Context
        uniquepath=oebs_key_objects.xpath
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

        self.swooptoelement(oebs_api.JABContext(hwnd),oebs_key_objects.xpath,parentxpathtemp,0,'')
        self.methodtofillmap(oebs_api.JABContext(hwnd),'',0)
        flag = 'false'
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
        if(objectDictWithNameDesc.has_key(keytocompare)):
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
            self.swooptoelement(oebs_api.JABContext(hwnd),oebs_key_objects.xpath,xpathneeded,0,'')
            accessContext=accessContextParent
            flag='true'

        elif (accessContextParent):
            tema = retacc.getAccessibleContextInfo()
            if retacc is not None:
                parentInfo = retacc.getAccessibleContextInfo()
                accarrname = []
                accarrdesc = []
                global accessContext
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
        global accessContext
        if flag == 'true' :
             return accessContext
        else :
            return 'fail'

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

    def clientresponse(self):
        clientresp=[]
        if(oebs_key_objects.keyword_output[0] != ''):
            clientresp.append({
                "keywordStatus" : oebs_key_objects.keyword_output[0],
                "keywordResponse" : oebs_key_objects.keyword_output[1],
                "keywordMessage" : oebs_key_objects.custom_msg
            })
        else:
            oebs_key_objects.custom_msg.append[:]
            oebs_key_objects.custom_msg.append(MSG_ELEMENT_NOT_FOUND)
            clientresp.append({
                "keywordMessage" : oebs_key_objects.custom_msg
            })
        global accessContext
        accessContext.releaseJavaObject()
        return str(clientresp)

    def cleardata(self):
        del oebs_key_objects.keyword_input[:]
        del oebs_key_objects.keyword_output[:]
##        global accessContext
##        accessContext=''


    def menugenerator(self,acc):
        menubarelement(acc,0,'')
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
            menubarelement(elementObj,index,path)



    def createMap(self,acc, tempne,xpath,j,window):
        path=''
        size = ''
        global index
        if index is 0:
            global access
            access=acc
            index=1

        curaccinfo = acc.getAccessibleContextInfo()
        tagrole = curaccinfo.role
        tagname = curaccinfo.name
        text = curaccinfo.name

        if xpath == '':
            if len(curaccinfo.name.strip()) == 0:
                path = curaccinfo.role + '[' + str(j) + ']'
            else:
                if 'panel' in curaccinfo.role:
                    path = curaccinfo.role  + '[' + str(j) + ']'
                else:
                   path  = curaccinfo.role + '[' + str(curaccinfo.name.strip()) + ']'
        else:
            if len(curaccinfo.name.strip()) == 0:
                 path = xpath + '/' + curaccinfo.role  + '[' + str(j) + ']'
            else:
                if 'panel' in curaccinfo.role:
                    path = xpath + '/' + curaccinfo.role  + '[' + str(j) + ']'
                else:
                    path = xpath + '/' + curaccinfo.role  + '[' + str(curaccinfo.name.strip()) + ']'

        if 'showing' in  curaccinfo.states:
            x = curaccinfo.x
            y = curaccinfo.y
            w = curaccinfo.width
            h = curaccinfo.height
            size=str(x)+','+str(y)+','+str(w)+','+str(h)
            global activeframename
            states=curaccinfo.states
            if('internal frame' in path):
                if(not(activeframename)):
                    if(curaccinfo.role == 'internal frame'):
                        if('active' in states):
                            regularexp = re.compile('(internal frame(.*?|\s)*[\]]+)')
                            newxpath = regularexp.findall(path)
                            newlist2=[]
                            for i in range(len(newxpath)):
                                newlist2.append(newxpath[i][0])
                            framename=newlist2[(len(newlist2)-1)]
                            activeframename=framename
                            objectDict[size] = path

                else:
                    if(activeframename in path):
                        objectDict[size] = path
            else:
                objectDict[size] = path

            size = ''

        for i in range(curaccinfo.childrenCount):
            childacc = acc.getAccessibleChildFromContext(i)
            acc.releaseJavaObject()
            self.createMap(childacc, tempne,path,i,window)

        return objectDict


    def getobjectforcustom(self,acc,window,parentxpath,type,eleIndex):
        tempne=[]
        eleproperties=''
        xpath=''
        counter=0
        xpathsplitarr=parentxpath.split(';')
        parentxpath=xpathsplitarr[0]
        if(int(eleIndex) < 0):
            return eleproperties
        descriptiongiven=xpathsplitarr[10]
        self.acccontext(acc,tempne,xpath,0,window)
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


