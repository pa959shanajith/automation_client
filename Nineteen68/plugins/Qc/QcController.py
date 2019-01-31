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

import win32com.client
import json
import socket
import os
TD=None
loginflag=False
urlflag=False
dictFolderJson=None
con = None
sent=0

class QcWindow():

    def __init__(self,filePath):
        status=None
        try:
            global sent,loginflag,TD,urlflag
            flag=0
            if(filePath["qcaction"]=='domain'):
                try:
                    user_name=filePath["qcUsername"]
                    pass_word=filePath["qcPassword"]
                    Qc_Url=filePath["qcURL"]
                    domain_dict={}
                    key="view"
                    domain_dict.setdefault(key, [])
                    loginflag=False
                    TD = win32com.client.Dispatch("TDApiOle80.TDConnection")
                    urlflag=False
                    TD.InitConnectionEx(str(Qc_Url))
                    urlflag=True
                    un=str(user_name)
                    pw=str(pass_word)
                    TD.Login(un,pw)
                    loginflag=True
                    status = self.getDomain(filePath)
                except Exception as eqc:
                    self.quit_qc()
                    flag=1
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
                    con.send("Fail@f@!l#E&D@Q!C#")
            else:
                pass
        except Exception as e:
            print('Error in Qc action')
            con.send('Fail@f@!l#E&D@Q!C#')
            sent=1

    def getDomain(self,filePath):
        try:
            global dictFolderJson
            domain_dict={}
            key="domain"
            domain_dict.setdefault(key, [])
            if(TD.connected==True):
                domain_dict['login_status']=True
                listDomains=TD.VisibleDomains
                if(len(listDomains)>0):
                    for dom in listDomains:
                        domain_dict[key].append(str(dom))
            dictFolder = json.dumps(domain_dict)
            dictFolderJson=json.loads(dictFolder)
        except Exception as e:
            print('Error in getting domains')
            dictFolderJson=None

        return dictFolderJson


    def getProjects(self,filePath):
        try:
            global dictFolderJson
            domain_name=filePath["domain"]
            projects_dict={}
            key="project"
            projects_dict.setdefault(key, [])
            if(TD.connected==True):
                list_projects=TD.VisibleProjects(domain_name)
                if(len(list_projects)>0):
                    for pro in list_projects:
                        projects_dict[key].append(str(pro))
                    dictFolder = json.dumps(projects_dict)
                    dictFolderJson=json.loads(dictFolder)
                else:
                    print('Invalid domain selected')
        except Exception as eproject:
            print('Error in fetching projects')
            dictFolderJson=None
        return dictFolderJson

    def ListTestSetFolder(self,filePath):
        ##The final list which contains the testsets and testset under the specified path
        try:
            global dictFolderJson
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
                        try:
                            TestSet_dict[keyTS].append(str(testset.name)+";"+str(testset.id))
                        except:
                            TestSet_dict[keyTS].append(((testset.name).encode('utf-8'))+";"+str(testset.id))
                else:
                    tsList = testset_folder.FindTestSets("")
                    if(len(tsList)>0):
                        for testset in tsList:
                            try:
                                TestSet_dict[keyTS].append(str(testset.name)+";"+str(testset.id))
                            except:
                                TestSet_dict[keyTS].append(((testset.name).encode('utf-8'))+";"+str(testset.id))
                ice_list_folder=folder_dict['testfolder']
                if(type(ice_list_folder)==list):
                    for fol in ice_list_folder:
                        delfolder = TD.TestSetTreeManager.NodeByPath(fol['folderpath'])
                        delTestSetList = delfolder.FindTestSets("")
                        if(delTestSetList != None):
                            for ts in delTestSetList:
                                try:
                                    remID=str(ts.name)+";"+str(ts.id)
                                except:
                                    remID=((ts.name).encode('utf-8'))+";"+str(ts.id)
                                ice_list=TestSet_dict['TestSet']
                                ice_list.remove(remID)
            else:
                print('Invalid connection')
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
            dictFolderJson = json.dumps(OverallList)
            dictFolderJson=json.loads(dictFolderJson)
        except Exception as e:
            print('Error while fetching testsets')
            dictFolderJson=None
        finally:
            return dictFolderJson



    def test_case_generator(self,filePath):
        try:
            global dictFolderJson
            test_case_dict={}
            key="testcase"
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
                if (test_case_ind.name).encode('utf-8')==(test_set_name).encode('utf-8'):
                   abc=listTC[i].tsTestFactory
                   qc_ts=abc.NewList("")
                   for tsname in qc_ts:
                       try:
                           ts_complete_name = tsname.name + '/'+ tsname.testid
                           test_case_dict[key].append(str(ts_complete_name))
                       except:
                           ts_complete_name = (tsname.name).encode('utf-8') + '/'+ tsname.testid
                           test_case_dict[key].append((ts_complete_name).encode('utf-8'))
                i=i+1
            OverallList=[]
            OverallList.append(test_case_dict)
            dictFolderJson = json.dumps(OverallList)
            dictFolderJson=json.loads(dictFolderJson)
        except Exception as e:
            print('Error while fetching testcases')
        return dictFolderJson

    def update_qc_details(self,data):
        status = False
        try:
            global dictFolderJson
            qcDomain =  data['qc_domain']
            qcProject = data['qc_project']
            tsFolder = data['qc_folder']
            tsList = data['qc_tsList']
            testrunname = data['qc_testrunname']
            result =  data['qc_update_status']
            if(TD.connected==True):
                TD.Connect(qcDomain,qcProject)
                TSetFact = TD.TestSetFactory
                #Getting the test set factory
                tsTreeMgr = TD.testsettreemanager
                tsFolder = tsTreeMgr.NodeByPath(tsFolder)
                tsList = tsFolder.FindTestSets(tsList)
                #Getting the test lists
                theTestSet = tsList.Item(1)
                #Getting the test set
                tsFolder = theTestSet.TestSetFolder
                tsTestFactory = theTestSet.tsTestFactory
                tsTestList = tsTestFactory.NewList("")
                for tsTest in tsTestList:
                    #Iterate the Test list
                    if tsTest.Name == testrunname:
                        RunFactory = tsTest.RunFactory
                        #RunFactory object created
                        obj_theRun = RunFactory.AddItem(testrunname)
                        #Updating the details in QC
                        obj_theRun.Status = result
                        #Scenario execution status updated
                        obj_theRun.Post()
                        obj_theRun.Refresh()
                        status = True
            else:
                print('Qc is disconnected')
        except Exception as e:
            print('Error while updating QC')
            status = False
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
        try:
            global sent,dictFolderJson
            sent=1
            if TD.connected==True and loginflag==True:
                con.send('closedqc#E&D@Q!C#')
                TD.Logout()
                TD.releaseconnection()
            elif urlflag==False:
                con.send('invalidurl#E&D@Q!C#')
            else:
                con.send('invalidcredentials#E&D@Q!C#')
                TD.releaseconnection()
            dictFolderJson=None
            return True
        except Exception as e:
            print('Error while quitting qc')
            con.send("Fail@f@!l#E&D@Q!C#")

    def emit_data(self):
        try:
            global dictFolderJson,sent
            data_to_send = json.dumps(dictFolderJson).encode('utf-8')
            data_to_send+='#E&D@Q!C#'
            sent=1
            con.send(data_to_send)
        except Exception as e:
            print('Error while emitting data')

if __name__ == '__main__':
    host = 'localhost'
    port = 10000
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
                    parsed_data = client_data[:client_data.find('#E&D@Q!C#')]
                    data_to_use = json.loads(parsed_data.decode('utf-8'))
                    qc_ref = QcWindow(data_to_use)
                    client_data=''
                    if(sent!=1):
                        con.send("Fail@f@!l#E&D@Q!C#")
                    else:
                        sent=0
            except Exception as e:
                con.send("Fail@f@!l#E&D@Q!C#")
                break
    except Exception as e:
        print("Exception occured in QC")
