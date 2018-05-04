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
#import wx

import socket
#from socketIO_client import SocketIO,BaseNamespace
##import launch_keywords
##desktop_scraping_obj = desktop_scraping.Scrape()
import os
import time
#import logger
obj=None
TD=None
loginflag=False
urlflag=False
dictFolderJson=None
con = None
sent=0
#import core_utils
class QcWindow():

    def __init__(self,filePath):
        status=None
        try:
            global obj,sent
            flag=0
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
                    print("Connection Build - ",TD)
                    global urlflag
                    urlflag=False
                    TD.InitConnectionEx(str(Qc_Url))
                    urlflag=True
                    un=str(user_name)
                    pw=str(pass_word)
                    TD.Login(un,pw)
                    loginflag=True
                    status = self.getDomain(filePath)
                except Exception as eqc:
                    print('Connection Failed..')
                    self.quit_qc()
                    flag=1
                    #self.quit_qc()
                    #logger.print_on_console('Please provide valid credentials - Connection not established / Login unsuccessful')
            elif(filePath["qcaction"]=='project'):
                status = self.getProjects(filePath)
            elif(filePath["qcaction"]=='folder'):
                status = self.ListTestSetFolder(filePath)
            elif(filePath["qcaction"]=='testcase'):
                status = self.test_case_generator(filePath)
            elif(filePath["qcaction"]=='qcupdate'):
                status = self.update_qc_details(filePath)
            elif(filePath["qcaction"]=='qcquit'):
                status = self.quit_qc()
                flag=1
            if not flag:
                if status!=None:
                    self.emit_data()
                else:
                    con.send("Fail#E&D@Q!C#")
            else:
                pass
        except Exception as e:
            print 'Error in Qc actions...'
            con.send('Fail#E&D@Q!C#')
            sent=1
           # logger.print_on_console('Something went wrong - Lost Connection with QC')

    def getDomain(self,filePath):
        try:
            print('Fetching the list of Domains')
            domain_dict={}
            key="domain"
            domain_dict.setdefault(key, [])
            if(TD.connected==True):
                print('Connection Successful')
                domain_dict['login_status']=True
                listDomains=TD.VisibleDomains
                if(len(listDomains)>0):
                    for dom in listDomains:
##                        print dom,'',key
                        domain_dict[key].append(str(dom))
            dictFolder = json.dumps(domain_dict)
            global dictFolderJson
            dictFolderJson=json.loads(dictFolder)
            print('Fetched Domains Successfully')
        except Exception as e:
            print('Something went wrong - Lost Connection with QC')
            dictFolderJson=None

        return dictFolderJson


    def getProjects(self,filePath):
        print('Fetching the list of Projects')
        try:
            domain_name=filePath["domain"]
##            print domain_name,' domain name'
            projects_dict={}
            key="project"
            projects_dict.setdefault(key, [])
##            print TD.connected,'wats the status'
            if(TD.connected==True):
                print('Connection Successful')
                list_projects=TD.VisibleProjects(domain_name)
                if(len(list_projects)>0):
                    for pro in list_projects:
##                        print pro
                        projects_dict[key].append(str(pro))
                    dictFolder = json.dumps(projects_dict)
                    global dictFolderJson
                    dictFolderJson=json.loads(dictFolder)
                    print('Fetched Projects Successfully')
                else:
                    print('Please select valid domain')
        except Exception as eproject:
            print('Error in fetching projects')
            #print eproject
##            logger.print_on_console('Something went wrong - Lost Connection with QC')
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
                    print('NO FOLDERS EXIST')
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
                print('invalid connection')
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
            print e
            #logger.print_on_console('Something went wrong - Unable to fetch the TestSet(s)')
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
                       ts_complete_name = tsname.name + '/'+ tsname.testid
                       test_case_dict[key].append(str(ts_complete_name))
                i=i+1
##            print test_case_dict,'no'
            OverallList=[]
            OverallList.append(test_case_dict)
            global dictFolderJson
            dictFolderJson = json.dumps(OverallList)
            dictFolderJson=json.loads(dictFolderJson)
        except Exception as e:
            #logger.print_on_console('Something went wrong - Unable to fetch the TestCase(s)')
            print e
            dictFolderJson=None
        return dictFolderJson

    def update_qc_details(self,data):
        print('****Updating QCDetails****')
        status = False
        try:

            #Get the details (comma separated )- QC url, username and password
##            data="http://srv03wap121:8080/qcbin,Chethan,Chethan1,ENTERPRISE,DimensionLab,root\TestFolder1,TestSet1,[1]QC-2,Failed"
            #logger.log('Getting the details with comma separated')
            #print 'Getting the details with comma separated'
            qcDomain =  data['qc_domain']
            qcProject = data['qc_project']
            tsFolder = data['qc_folder']
            tsList = data['qc_tsList']
            testrunname = data['qc_testrunname']
            result =  data['qc_update_status']
            #print TD.connected
            if(TD.connected==True):
                TD.Connect(qcDomain,qcProject)
                #Connection Established
                #logger.log('Connection Established')
                TSetFact = TD.TestSetFactory
                #Getting the test set factory
                #logger.log('Getting the test set factory')
                tsTreeMgr = TD.testsettreemanager
                tsFolder = tsTreeMgr.NodeByPath(tsFolder)
                tsList = tsFolder.FindTestSets(tsList)
                #Getting the test lists
                #logger.log('Getting the test lists')
                theTestSet = tsList.Item(1)
                #Getting the test set
                #logger.log('Getting the test set')
                tsFolder = theTestSet.TestSetFolder
                tsTestFactory = theTestSet.tsTestFactory
                tsTestList = tsTestFactory.NewList("")
                print tsFolder,tsTestFactory,tsTestList
                for tsTest in tsTestList:
                    #Iterate the Test list
                    #logger.log('Iterate the Test list')
                    if tsTest.Name == testrunname:
                        #logger.log('Test runname matched')
                        RunFactory = tsTest.RunFactory
                        #RunFactory object created
                        #logger.log('RunFactory object created')
                        obj_theRun = RunFactory.AddItem(testrunname)
                        #Updating the details in QC
                        #print result
                        #logger.log('Updating the details in QC')
                        obj_theRun.Status = result
                        #Scenario execution status updated
                        #logger.log('Scenario execution status updated')
                        obj_theRun.Post()
                        obj_theRun.Refresh()
                        status = True
                        #QC Details updated successfully
                        #logger.log('QC Details updated successfully')
                        print('****Updated QCDetails Successfully****')
            else:
                print('Qc is disconnected..')
        except Exception as e:
            print('Something went wrong - Connection not established/ Login unsuccessful/Domain/Project/Folder/Testset/Testrun name wrong')
            status = False
##            print status
        global dictFolderJson
        if(status):
            dictFolderJson = {'QC_UpdateStatus':True}
            """
            TD.Logout()
            TD.releaseconnection()
            print 'closing_connection'
            """
        else:
            dictFolderJson = {'QC_UpdateStatus':False}
        return status

    def quit_qc(self):
##        print 'quiting qc'
##        print urlflag
        global sent
        try:
            sent=1
            if TD.connected==True and loginflag==True:
                con.send('closedqc#E&D@Q!C#')
                print('Closing QC Connection')
                TD.Logout()
                TD.releaseconnection()
                print 'Logout S'
            elif urlflag==False:
                con.send('invalidurl#E&D@Q!C#')
            else:
                con.send('invalidcredentials#E&D@Q!C#')
                print('Releasing QC Connection')
                TD.releaseconnection()
            global dictFolderJson
            dictFolderJson=None
            return True
        except Exception as e:
            print 'Error in Quit_qc'
            con.send("Fail#E&D@Q!C#")

    def emit_data(self):
##        print d,' in emit data'
        global dictFolderJson,sent
        data_to_send = json.dumps(dictFolderJson).encode('utf-8')
        data_to_send+='#E&D@Q!C#'
        sent=1
        con.send(data_to_send)
        # 10 is the limit of MB set as per Nineteen68 standards
        """
        if self.core_utilsobject.getdatasize(str(d),'mb') < 10:
            self.socketIO.emit('qcresponse',d)
        else:
            print 'Scraped data exceeds max. Limit.'
            self.socketIO.emit('qcresponse','Response Body exceeds max. Limit.')
        logger.print_on_console('Fetched data successfully')
        """

if __name__ == '__main__':
##    logging.basicConfig(filename='python-deskscrappy.log', level=logging.WARNING, format='%(asctime)s %(message)s')
    host = 'localhost'
    port = 10000
    print('Qc Started...')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(30)
        con, addr = s.accept()
        client_data =''
        while(True):
            try:
                data_stream = con.recv(1024)
                client_data+=data_stream
                if('#E&D@Q!C#' in data_stream):
                    #print data_stream
                    parsed_data = client_data[:client_data.find('#E&D@Q!C#')]
                    data_to_use = json.loads(parsed_data.decode('utf-8'))
                    #print data_to_use
                    qc_ref = QcWindow(data_to_use)
                    client_data=''
                    if(sent!=1):
                        con.send("Fail#E&D@Q!C#")
                    else:
                        sent=0
            except Exception as e:
                print 'Error in data receiving'
                con.send("Fail#E&D@Q!C#")
                break
    except Exception as e:
        print 'Error in running Qc'

