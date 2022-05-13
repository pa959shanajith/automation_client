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
import time
import readconfig
global count
count=''
accessContext=''
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
    def swooptoelement(self , a, objecttofind, currentxpathtemp, i, p, windowname, object_type, errors = False, allow_showing = False):
        queue = []
        active_parent = False
        page_tab_list = False
        queue.append((p,a,i,0))
        identifiers = objecttofind.split(';')
        uniquepath = identifiers[0]
        #getting the internal frame name :
        
        internal_frame_list = []
        for each_internal_frame in uniquepath.split('/'):
            if each_internal_frame.find('internal frame')!=-1:
                internal_frame_list.append(each_internal_frame.lstrip('internal frame[')[:-1])
        
        while len(queue) > 0:
            xpath, acc, index, paneindex = queue.pop(0)
            elementObj = acc.getAccessibleContextInfo()

            if xpath == '':
                if len(elementObj.description.strip()) == 0:
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
                        if object_type == "@Custom":
                            path = elementObj.role + '[' + str(index) + ']' + '[' + str(elementObj.description.strip()) + ']'
                        else:
                            path = elementObj.role + '[' + str(elementObj.description.strip()) + ']'

            else:
                if len(elementObj.description.strip()) == 0:
                    if 'internal frame' in elementObj.role or 'frame' in elementObj.role:
                        path = xpath + '/' + elementObj.role
                    elif 'panel' in elementObj.role:
                        path = xpath + '/' + elementObj.role + '[' + str(index) + ']'
                    else:
                        path = xpath + '/' + elementObj.role  + '[' + str(index) + ']'

                else:
                    if 'internal frame' in elementObj.role:
                        if elementObj.description.strip() not in internal_frame_list:
                            continue
                        path = xpath + '/' + elementObj.role
                    elif 'panel' in elementObj.role:
                        path = xpath + '/' + elementObj.role + '[' + str(index) + ']'
                    else:
                        if object_type == "@Custom":
                            path = xpath + '/' + elementObj.role  + '[' + str(index) + ']'  + '[' + str(elementObj.description.strip()) + ']'
                        else:
                            path = xpath + '/' + elementObj.role  + '[' + str(elementObj.description.strip()) + ']'
            if path == currentxpathtemp:
                if currentxpathtemp.split("/").pop() == 'internal frame' and elementObj.name != identifiers[1]:
                    continue
                if page_tab_list:
                    return active_parent, acc, paneindex == 0
                return active_parent, acc, True

            curr = currentxpathtemp.split('/')
            p = path.split('/')
            index = len(p) - 1
            if len(curr) > index and curr[index] == p[index]:
                if 'active' in elementObj.states and windowname != elementObj.name:
                    active_parent = True
                for index in range(elementObj.childrenCount):
                    element = acc.getAccessibleChildFromContext(index)
                    elementcontext=element.getAccessibleContextInfo()
                    if elementcontext.role == "page tab list" and "page tab list" not in currentxpathtemp:
                        page_tab_list = True
                    if elementcontext.role == 'internal frame':
                        if 'active' in elementcontext.states or (allow_showing and 'showing' in elementcontext.states):
                            queue.append((path, element, index, paneindex))
                        else:
                            hasinternal=0
                            children=elementcontext.childrenCount
                            for childrencount in range(int(children)):
                                childobj=element.getAccessibleChildFromContext(childrencount)
                                childrencontext=childobj.getAccessibleContextInfo()
                                if 'internal frame' in childrencontext.role:
                                    hasinternal=1
                                    break
                            if hasinternal ==1:
                                queue.append((path, element, index, paneindex))
                            else:
                                index = index + 1
                    else:
                        if elementcontext.role == 'scroll pane':
                            queue.append((path, element, index, index))
                        else:
                            queue.append((path, element, index, paneindex))   
            if len(queue) == 0:
                if errors: logger.print_on_console("Object not found in provided path, searching in alternate scroll panes for the object")
                pane_occurances = [m.start() for m in re.finditer('scroll pane', currentxpathtemp)]
                variable_path = currentxpathtemp
                for i in range(len(pane_occurances) - 1, -1, -1):
                    fixed_path = variable_path[0:pane_occurances[i]]
                    skip_over = variable_path[pane_occurances[i]:len(variable_path)].find('/') + pane_occurances[i]
                    variable_path = fixed_path + 'scroll pane' + variable_path[skip_over:len(variable_path)]
                    if errors: log.info('Searching for object in alternate xpath: ' + variable_path)
                    active_parent, acc, visible = self.iterate_over_other_panes(a,objecttofind,variable_path,0,'',windowname, pane_occurances[i], object_type)
                    if acc and str(acc) != '':
                        return active_parent, acc, visible
                log.info(ERROR_CODE_DICT['err_alternate_path'])
                if errors: logger.print_on_console(ERROR_CODE_DICT['err_alternate_path'])
                return False, '', False
        return False, '', False


    def iterate_over_other_panes(self, a, objecttofind, currentxpathtemp, i, p, windowname, location, object_type):
        queue = []
        active_parent = False
        queue.append((p,a,i,0))
        identifiers = objecttofind.split(';')
        uniquepath = identifiers[0]
        alt_paths = {}
        alt_paths_list = []
        internal_frame_list = []
        visited = {}
        for each_internal_frame in uniquepath.split('/'):
            if each_internal_frame.find('internal frame')!=-1:
                internal_frame_list.append(each_internal_frame.lstrip('internal frame[')[:-1])
        
        while len(queue) > 0:
            xpath, acc, index, paneindex = queue.pop(0)
            elementObj = acc.getAccessibleContextInfo()

            if xpath == '':
                if len(elementObj.description.strip()) == 0:
                    if 'internal frame' in elementObj.role or 'frame' in elementObj.role or ('scroll pane' in elementObj.role and len(path) + 1 >= location):
                        path = elementObj.role
                    elif 'panel' in elementObj.role:
                        path = elementObj.role + '[' + str(index) + ']'
                    else:
                        path = elementObj.role + '[' + str(index) + ']'

                else:
                    if 'internal frame' in elementObj.role or 'frame' in elementObj.role or ('scroll pane' in elementObj.role and len(path) + 1 >= location):
                        path = elementObj.role
                    elif 'panel' in elementObj.role:
                        path = elementObj.role + '[' + str(index) + ']'
                    else:
                        if object_type == "@Custom":
                            path = elementObj.role  + '[' + str(index) + ']' + '[' + str(elementObj.description.strip()) + ']'
                        else:
                            path = elementObj.role + '[' + str(elementObj.description.strip()) + ']'
            else:
                if len(elementObj.description.strip()) == 0:
                    if 'internal frame' in elementObj.role or 'frame' in elementObj.role or ('scroll pane' in elementObj.role and len(path) + 1>= location):
                        path = xpath + '/' + elementObj.role
                    elif 'panel' in elementObj.role:
                        path = xpath + '/' + elementObj.role + '[' + str(index) + ']'
                    else:
                        path = xpath + '/' + elementObj.role  + '[' + str(index) + ']'
                else:
                    if 'internal frame' in elementObj.role:
                        if elementObj.description.strip() not in internal_frame_list:
                            continue
                        path = xpath + '/' + elementObj.role
                    elif 'scroll pane' in elementObj.role and len(path) + 1 >= location :
                        path = xpath + '/' + elementObj.role
                    elif 'panel' in elementObj.role:
                        path = xpath + '/' + elementObj.role + '[' + str(index) + ']'
                    else:
                        if object_type == "@Custom":
                            path = xpath + '/' + elementObj.role  + '[' + str(index) + ']' + '[' + str(elementObj.description.strip()) + ']'
                        else:
                            path = xpath + '/' + elementObj.role  + '[' + str(elementObj.description.strip()) + ']'
            if path in visited:
                continue
            else:
                visited[path + str(index)] = True
            if path.split('/').pop() == 'text[0]':
                new_path = self.get_alt_paths(path, currentxpathtemp)
                log.info("Hidden Push button detected, creating new xpath: " + new_path)
                if new_path != '':
                    logger.print_on_console("Hidden Push button detected, creating new xpaths")
                    alt_paths_list.append(new_path)
                    alt_paths[new_path] = len(alt_paths_list) - 1

            if path == currentxpathtemp or path in alt_paths:
                return active_parent, acc, paneindex == 0

            curr = currentxpathtemp.split('/')
            p = path.split('/')
            index = len(p) - 1
            if (len(curr) > index and curr[index] == p[index]) or (len(alt_paths_list) > 0 and self.in_alt_paths(alt_paths_list, p[index], index)):
                if 'active' in elementObj.states and windowname != elementObj.name:
                    active_parent = True
                for index in range(elementObj.childrenCount):
                    element = acc.getAccessibleChildFromContext(index)

                    elementcontext=element.getAccessibleContextInfo()
                    if elementcontext.role == 'internal frame':
                        if 'active' in elementcontext.states:
                            queue.append((path, element, index, paneindex))
                        else:
                            hasinternal=0
                            children=elementcontext.childrenCount
                            for childrencount in range(int(children)):
                                childobj=element.getAccessibleChildFromContext(childrencount)
                                childrencontext=childobj.getAccessibleContextInfo()
                                if 'internal frame' in childrencontext.role:
                                    hasinternal=1
                                    break
                            if hasinternal ==1:
                                queue.append((path, element, index , paneindex))
                            else:
                                index = index + 1
                    else:
                        if elementcontext.role == 'scroll pane':
                            queue.append((path, element, index, index))
                        else:
                            queue.append((path, element, index, paneindex))
            elif len(queue) == 0:
                return active_parent, '', False 
        return active_parent, '', False 
    
    def get_alt_paths(self, path, xpath):
        index_text = path.index('text[0]')
        if index_text == -1: return ''
        semi_path = xpath[index_text : len(xpath)]
        pat = r'(?<=\[).+?(?=\])'
        m = re.findall(pat, semi_path)
        if not m or len(m) <= 0: return ''
        if not m[0].isdigit(): return ''
        new_index = m[0]
        semi_path = semi_path.replace(m[0],str(int(new_index) + 1))
        li_path = list(semi_path)
        semi_path = ''.join(li_path)
        return xpath[0:index_text] + semi_path

    def in_alt_paths(self, alt_paths_list, path, index):
        for alt_path in alt_paths_list:
            path_list = alt_path.split("/")
            if index < len(path_list) and path_list[index] == path:
                return True
        return False

    def object_generator(self,applicationname,locator,keyword,inputs,outputs,object_type, errors = False, allow_showing = False):
        global accessContext
        accessContext = ''
        active_parent = None
        #OBJECTLOCATION for the object is sent from the user
        del oebs_key_objects.keyword_input[:]
        oebs_key_objects.xpath = locator
        #Application name is sent from the user
        oebs_key_objects.applicationname = applicationname
        oebs_key_objects.object_type = object_type
        utils_obj=oebs_utils.Utils()
        isjavares, hwnd = utils_obj.isjavawindow(oebs_key_objects.applicationname)
        #method enables to move to perticular object and fetches its Contexts
        uniquepath=oebs_key_objects.xpath
        flag = 'false'
        if ';' in uniquepath:
            requiredxpath = uniquepath.split(';')
            parentxpathtemp = ''
            absolute_path = requiredxpath[0]

            regularexp = re.compile('(frame(.*?|\s)*[\]]+)')
            newxpath = regularexp.findall(absolute_path)

            newlist2=[]
            for i in range(len(newxpath)):
                newlist2.append(newxpath[i][0])

            for i in range(len(newlist2)):
                absolute_path = absolute_path.replace(newlist2[i],'frame')

            active_parent, accessContextParent, visible = self.swooptoelement(oebs_api.JABContext(hwnd), oebs_key_objects.xpath, absolute_path ,0 ,'', applicationname, object_type, errors, allow_showing)
            accessContextParent = accessContextParent or ''
            if active_parent is None:
                active_parent = False

            identifiers = oebs_key_objects.xpath.split(';')
            uniquepath = identifiers[0]
            name = identifiers[1]
            description=''
            try:
                description=identifiers[10]
            except Exception:
                description=''
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
                active_parent, accessContextParent, visible = self.swooptoelement(oebs_api.JABContext(hwnd),oebs_key_objects.xpath,xpathneeded,0,'', applicationname, object_type)
                flag='true'

        accessContext=accessContextParent
        #keyword is sent from the user
        oebs_key_objects.keyword = keyword
        #input sent from the user
        inputs = ast.literal_eval(str(inputs))
        inputs = [n for n in inputs]

        for index in range(len(inputs)):
            oebs_key_objects.keyword_input.append(inputs[index])
        #output thats to be sent from the server to client
        oebs_key_objects.keyword_output = outputs.split(';')
        configvalues = readconfig.configvalues
        ignore_hidden = configvalues['ignoreVisibilityCheck']
        if str(accessContextParent) != '' and ((ignore_hidden == 'No' and visible) or ignore_hidden == 'Yes'):
            if ignore_hidden == 'Yes' and not visible:
                logger.print_on_console(ERROR_CODE_DICT['wrn_found_not_visible'])  
            return accessContextParent, True, active_parent
        elif str(accessContextParent) != '' and ignore_hidden == 'No' and not visible:
            logger.print_on_console(ERROR_CODE_DICT['err_found_not_visible'])
            return 'fail', False, False
        else:
            return 'fail', False, False


    def getsize(self,xpath,windowname):
        #object is identified using normal object identification
        accessContext, visible = self.object_generator(windowname,xpath,'',[],'','')
        #context is taken from global value
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
            k = 1
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
                if 'internal frame' in elementObj.role or 'frame' in elementObj.role:
                    path = elementObj.role
                else:
                    path = elementObj.role + '[' + str(index) + ']'
             else:
                if 'internal frame' in elementObj.role or 'frame' in elementObj.role:
                    path = elementObj.role
                else:
                    path = elementObj.role + '[' + str(elementObj.name.strip()) + ']'
        else:
            if len(elementObj.name.strip()) == 0:
                if 'internal frame' in elementObj.role or 'frame' in elementObj.role:
                    path = xpath + '/' + elementObj.role
                else:
                    path = xpath + '/' + elementObj.role  + '[' + str(index) + ']'
            else:
                if 'internal frame' in elementObj.role or 'frame' in elementObj.role:
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


    def getobjectforcustom(self,windowname,parentxpath,element_type,eleIndex):
        utils_obj=oebs_utils.Utils()
        isjavares, hwnd = utils_obj.isjavawindow(windowname)
        acc = oebs_api.JABContext(hwnd)
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
        fullscrape_obj.custom_winrect(windowname)
        fullscrape_obj.acccontext_custom(acc,tempne,xpath,0,windowname)
        verifyflag=False
        parent_index = 0
        for index in range(len(tempne)):
            xpatharr=(str(tempne[index].get('xpath'))).split(';')
            tag=str(tempne[index].get('tag'))
            path=xpatharr[0]
            runTimedescription=''
            if(xpatharr[10]):
                runTimedescription=xpatharr[10]
            if(parentxpath== path and verifyflag == False):
                verifyflag = True
                parent_index = index
            elif(verifyflag == False and descriptiongiven == runTimedescription and runTimedescription != ''):
                verifyflag = True
                parent_index = index
            if(verifyflag):
                if( not((tag == 'panel') or (tag == 'scroll pane') or (tag =='viewport'))):
                    if(tag == element_type):
                        if index >= parent_index:
                            if(int(counter) == int(eleIndex)):
                                eleproperties=str(tempne[index].get('xpath'))
                                return eleproperties
                            counter+=1

        return eleproperties


