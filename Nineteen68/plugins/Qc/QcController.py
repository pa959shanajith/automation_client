#-------------------------------------------------------------------------------
# Name:        QcTestLab.py
# Purpose:
#
# Author:      chethan.singh
#
# Created:     10/05/2017
# Copyright:   (c) chethan.singh 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import win32com
from win32com.client import Dispatch
import json
import wx
from socketIO_client import SocketIO,BaseNamespace
##import launch_keywords
##desktop_scraping_obj = desktop_scraping.Scrape()
import os
import logger
obj=None
TD=None
loginflag=False
dictFolderJson=None
import core_utils
class QcWindow(wx.Frame):

    def __init__(self, parent,id, title,filePath,socketIO):
        status=None
        #print ' in the main qc'
        try:
            wx.Frame.__init__(self, parent, title=title,
                       pos=(300, 150),  size=(200, 150) ,style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX|wx.CLOSE_BOX) )
            self.SetBackgroundColour('#e6e7e8')
            self.iconpath = os.environ["NINETEEN68_HOME"] + "/Nineteen68/plugins/Core/Images" + "/slk.ico"
            self.wicon = wx.Icon(self.iconpath, wx.BITMAP_TYPE_ICO)
            self.core_utilsobject = core_utils.CoreUtils()
            global obj
            self.socketIO = socketIO

            if(filePath["qcaction"]=='domain'):
                try:
                    user_name=filePath["qcUsername"]
                    pass_word=filePath["qcPassword"]
                    Qc_Url=filePath["qcURL"]
                    domain_dict={}
                    key="view"
                    domain_dict.setdefault(key, [])
                    global loginflag
                    loginflag=False
                    global TD
                    TD = win32com.client.Dispatch("TDApiOle80.TDConnection")
                    TD.InitConnectionEx(str(Qc_Url))
##                    print TD.connected
                    un=str(user_name)
                    pw=str(pass_word)
##                    print user_name,',',pass_word
                    TD.Login(un,pw)
                    loginflag=True
                    status = self.getDomain(filePath)
                except Exception as eqc:
                    self.quit_qc()
                    logger.print_on_console('Please provide valid credentials - Connection not established / Login unsuccessful')
            elif(filePath["qcaction"]=='project'):
                status = self.getProjects(filePath)
            elif(filePath["qcaction"]=='folder'):
                status = self.ListTestSetFolder(filePath)
            elif(filePath["qcaction"]=='testcase'):
                status = self.test_case_generator(filePath)
            elif(filePath["qcaction"]=='qcquit'):
                status = self.quit_qc()
            if status!=None:
                self.emit_data()
            else:
                self.socketIO.emit('scrape','Fail')
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.print_on_console('Something went wrong - Lost Connection with QC')

    def getDomain(self,filePath):
        try:
            logger.print_on_console('Fetching the list of Domains')
            domain_dict={}
            key="domain"
            domain_dict.setdefault(key, [])
            if(TD.connected==True):
##                logger.print_on_console('Connection Successful')
                listDomains=TD.VisibleDomains
                if(len(listDomains)>0):
                    for dom in listDomains:
##                        print dom,'',key
                        domain_dict[key].append(str(dom))
            dictFolder = json.dumps(domain_dict)
            global dictFolderJson
            dictFolderJson=json.loads(dictFolder)
            logger.print_on_console('Fetched Domains Successfully')
        except Exception as e:
            logger.print_on_console('Something went wrong - Lost Connection with QC')
            dictFolderJson=None

        return dictFolderJson


    def getProjects(self,filePath):
        logger.print_on_console('Fetching the list of Projects')
        try:
            domain_name=filePath["domain"]
##            print domain_name,' domain name'
            projects_dict={}
            key="project"
            projects_dict.setdefault(key, [])
##            print TD.connected,'wats the status'
            if(TD.connected==True):
                logger.print_on_console('Connection Successful')
                list_projects=TD.VisibleProjects(domain_name)
                if(len(list_projects)>0):
                    for pro in list_projects:
##                        print pro
                        projects_dict[key].append(str(pro))
                    dictFolder = json.dumps(projects_dict)
                    global dictFolderJson
                    dictFolderJson=json.loads(dictFolder)
                    logger.print_on_console('Fetched Projects Successfully')
                else:
                    logger.print_on_console('Please select valid domain')
        except Exception as eproject:
            import traceback
            traceback.print_exc()
            logger.print_on_console('Something went wrong - Lost Connection with QC')
            dictFolderJson=None
        return dictFolderJson

    def ListTestSetFolder(self,filePath):
        ##The final list which contains the testsets and testset under the specified path
        try:
            testsetpath=filePath["foldername"]
            domain_name=filePath["domain"]
            project_name=filePath["project"]

            folder_dict={}
            TestSet_dict={}
            key="testfolder"
            keyTS="TestSet"
            folder_dict.setdefault(key, [])
            TestSet_dict.setdefault(keyTS,[])
            ##Contains the list of testsets which is fetched from the given parent folder
            dictTestSet={}
            dictsub={}
            if(TD.connected==True):
##                print 'connection successful'
                TD.connect(domain_name, project_name)
                testset_folder = TD.TestSetTreeManager.NodeByPath(testsetpath)
                treeList=testset_folder.newlist()
                if (len(treeList)>0):
                    for folder in treeList:
                        temp_dict={}
                        temp_dict['foldername']=str(folder.name)
                        temp_dict['folderpath']=str(testsetpath+"\\"+str(folder.name))
                        folder_dict[key].append(temp_dict)
                tsList = testset_folder.FindTestSets("")
                if(len(tsList)>0):
                    for testset in tsList:
##                        print testset.name,' : ',testset.id,':',testset.status,':',testset.modified
                        TestSet_dict[keyTS].append(str(testset.name)+";"+str(testset.id))
                else:
                    logger.print_on_console('NO FOLDERS EXIST')
                    tsList = testset_folder.FindTestSets("")
                    if(len(tsList)>0):
                        for testset in tsList:
##                            print testset.name,' : ',testset.id,':',testset.status,':',testset.modified
                            TestSet_dict[keyTS].append(str(testset.name)+";"+str(testset.id))
##                print 'connection successful'
                ice_list_folder=folder_dict['testfolder']
##                print type(ice_list_folder)
                if(type(ice_list_folder)==list):
##                    print 'ice',ice_list_folder
                    for fol in ice_list_folder:
##                        print fol['folderpath'],' folder name'
##                        print testsetpath+"\\"+fol['folderpath']," in folder"
                        delfolder = TD.TestSetTreeManager.NodeByPath(fol['folderpath'])
                        delTestSetList = delfolder.FindTestSets("")
                        if(delTestSetList != None):
                            for ts in delTestSetList:
                                remID=str(ts.name)+";"+str(ts.id);
##                                print str(ts.name)+";"+str(ts.id),'name is'
                                ice_list=TestSet_dict['TestSet']
                                ice_list.remove(remID)
            else:
                logger.print_on_console(' invalid connection')
##                self.quit_qc()
##                self.socketIO.emit('scrape','Fail')
##            print TestSet_dict,'no',folder_dict
##            print len(TestSet_dict['TestSet'])
            temp_dict_ts={}
            key="TestSet"
            temp_dict_ts.setdefault(key, [])
            for i in TestSet_dict['TestSet']:
                tsp={}
                tsp['testset']=str(i).split(";")[0]
                tsp['testsetid']=str(i).split(";")[1]
                tsp['testsetpath']=testsetpath
                temp_dict_ts[key].append(tsp)
            OverallList=[]
            OverallList.append(folder_dict)
            OverallList.append(temp_dict_ts)
            global dictFolderJson
            dictFolderJson = json.dumps(OverallList)
            dictFolderJson=json.loads(dictFolderJson)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.print_on_console('Something went wrong - Unable to fetch the TestSet(s)')
            dictFolderJson=None
        finally:
            return dictFolderJson



    def test_case_generator(self,filePath):
        try:
            test_case_dict={}
            key="testcase"
##            print filePath
            testsetpath=filePath["foldername"]
            test_set_name=filePath["testset"]
            domain_name=filePath["domain"]
            project_name=filePath["project"]
            test_case_dict.setdefault(key, [])
            TD.connect(domain_name, project_name)
            testCaseList = TD.TestSetTreeManager.NodeByPath(testsetpath)
            listTC=testCaseList.FindTestSets("")
            i=0
            for test_case_ind in listTC:
##                print str(test_case_ind.name)
                if str(test_case_ind.name)==str(test_set_name):
##                   print i
                   abc=listTC[i].tsTestFactory
                   qc_ts=abc.NewList("")
                   for tsname in qc_ts:
##                       print tsname.name
                       test_case_dict[key].append(str(tsname.name))
                i=i+1
##            print test_case_dict,'no'
            OverallList=[]
            OverallList.append(test_case_dict)
            global dictFolderJson
            dictFolderJson = json.dumps(OverallList)
            dictFolderJson=json.loads(dictFolderJson)
        except Exception as e:
            logger.print_on_console('Something went wrong - Unable to fetch the TestCase(s)')
            dictFolderJson=None
        return dictFolderJson


    def quit_qc(self):
        ##print 'quiting qc'
        if TD.connected==True and loginflag==True:
            self.socketIO.emit('qcresponse','closedqc')
            logger.print_on_console('Closing QC Connection')
            TD.Logout()
            TD.releaseconnection()
        else:
            self.socketIO.emit('qcresponse','invalidcredentials')
            logger.print_on_console('Releasing QC Connection')
            TD.releaseconnection()
        global dictFolderJson
        dictFolderJson=None

    def emit_data(self):
        d = dictFolderJson
##        print d,' in emit data'
        # 10 is the limit of MB set as per Nineteen68 standards
        if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
            self.socketIO.emit('qcresponse',d)
        else:
            print 'Scraped data exceeds max. Limit.'
            self.socketIO.emit('qcresponse','Response Body exceeds max. Limit.')
        logger.print_on_console('Fetched data successfully')