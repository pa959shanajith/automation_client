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

import json
import os
from requests.auth import HTTPBasicAuth
import requests
import logger
import logging
log = logging.getLogger("Qccontroller.py")


class QcWindow():
    dictFolderJson=None
    cookies = None
    headers = None
    _headers = None
    Qc_Url = None

    def __init__(self):
        pass

    def Login1(self,filePath):
        status=None
        try:
            if(filePath["qcaction"]=='domain'):
                try:
                    user_name=filePath["qcUsername"]
                    pass_word=filePath["qcPassword"]
                    self.Qc_Url=filePath["qcURL"]
                    loginflag=False
                    self.headers = {'cache-control': "no-cache"}
                    login_url = self.Qc_Url + '/authentication-point/authenticate'
                    resp = requests.post(login_url, auth=HTTPBasicAuth(user_name, pass_word),  headers=self.headers)
                    if resp.status_code == 200:
                        cookieName = resp.headers.get('Set-Cookie')
                        LWSSO_COOKIE_KEY = cookieName[cookieName.index("=") + 1: cookieName.index(";")]
                        self.cookies = {'LWSSO_COOKIE_KEY': LWSSO_COOKIE_KEY}
                    qcSessionEndPoint = self.Qc_Url + "/rest/site-session"    
                    response = requests.post(qcSessionEndPoint, headers=self.headers, cookies=self.cookies)
                    if response.status_code == 200 | response.status_code == 201:
                        cookieName = response.headers.get('Set-Cookie').split(",")[1]
                        QCSession = cookieName[cookieName.index("=") + 1: cookieName.index(";")]
                        self.cookies['QCSession'] = QCSession
                
                    #fetching domains
                    dictFolderJson=None
                    domain_dict={}
                    key="domain"
                    domain_dict.setdefault(key, [])
                    domain_dict['login_status']=True
                    self._headers = {
                        'accept': 'application/json'
                    }
                    
                    DomainURL = self.Qc_Url + '/rest/domains/'
                    _resp = requests.get(DomainURL, headers=self._headers, cookies=self.cookies)   
                    JsonObject = _resp.json()
                    DomainList = [item['Name'] for item in JsonObject['Domains']['Domain']]
                    if(len(DomainList)>0):
                        for dom in DomainList:
                            domain_dict[key].append(str(dom))
                    dictFolder = json.dumps(domain_dict)
                    dictFolderJson=json.loads(dictFolder)
                    return dictFolderJson
                except Exception as eqc:
                    self.quit_qc()
                    flag=1
            else:
                pass
        except Exception as e:
            print('Error in Qc action')
        

    def getProjects(self,filePath):
        try:
            global dictFolderJson
            domain_name=filePath["domain"]
            projects_dict={}
            key="project"
            projects_dict.setdefault(key, [])
            ProjectURL = self.Qc_Url + '/rest/domains/' + domain_name + '/projects'
            resp = requests.get(ProjectURL, headers=self._headers, cookies=self.cookies)
            JsonObject = resp.json()
            if type(JsonObject['Projects']['Project']) is list:
                list_projects = [item['Name'] for item in JsonObject['Projects']['Project']]
            if type(JsonObject['Projects']['Project']) is dict:
                list_projects = [JsonObject['Projects']['Project']['Name']]

            if(len(list_projects)>0):
                for pro in list_projects:
                    projects_dict[key].append(str(pro))
                dictFolder = json.dumps(projects_dict)
                dictFolderJson=json.loads(dictFolder)
                return dictFolderJson
            else:
                print('Invalid domain selected')
        except Exception as eproject:
            print('Error in fetching projects')
            dictFolderJson=None

    def ListTestSetFolder(self,filePath):
        ##The final list which contains the testsets and testset under the specified path
        try:
            global dictFolderJson
            testsetpath=filePath["foldername"]
            domain_name=filePath["domain"]
            project_name=filePath["project"]       
            test_plan_path=filePath["foldername"]

            json_str =json.loads(self.find_folder_id(test_plan_path.split("\\"), "test-set-folders", 0, "id", domain_name, project_name ))
            if 'entities' in json_str:
                return create_key_value(json_str['entities'][0]['Fields'])
            else:
                return create_key_value(json_str['Fields'])

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
                
                """
                This procedure will return list of test-instances in a given test set
                :param hp: HP object
                :param tid: integer test set identifier
                :returns: list test instances list
                """
                '''
                params = '{cycle-id[' + tid + ']}'
                url = self.base_url + '/qcbin/rest/domains/' + domain_name + '/projects/' + project_name + '/test-instances'
                response = requests.get(url, params=params, headers=self.getheaders())
                test_inst = text_to_xml(response.content, "Entity/Fields/Field\[@Name='test-instance'\]/Value/text()")
                '''

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



    
    def find_folder_id(self, arrFolder, strAPI, parentID, fields, almDomain, almProject):
        try:
            response = ""

            midPoint = "/rest/domains/" + almDomain + "/projects/" + almProject 


            URL = self.Qc_Url + midPoint + "/" + strAPI
            
            for folderName in arrFolder:
                #payload = {"query": "{name['" + "Subject" + "'];parent-id[" + str(parentID) + "]}", "fields": fields}
                payload = {"query": "{name['" + folderName + "']}"}
                response = requests.get(URL, params=payload, headers=self.headers, cookies=self.cookies)
                
                
                obj = json.loads(response.text)
                if obj["TotalResults"] >= 1:
                    parentID = get_field_value(obj['entities'][0]['Fields'], "id")
                    # print("folder id of " + folderName + " is " + str(parentID))
                else:
                    # print("Folder " + folderName + " does not exists")
                    data = "<Entity Type=" + chr(34) + strAPI[0:len(strAPI) - 1] + chr(34) + "><Fields><Field Name=" + chr(
                        34) + "name" + chr(
                        34) + "><Value>" + folderName + "</Value></Field><Field Name=" + chr(34) + "parent-id" + chr(
                        34) + "><Value>" + str(parentID) + "</Value></Field></Fields> </Entity>"
                    response = requests.post(almURL + midPoint + "/" + strAPI, data=data, headers=self.headers, cookies=self.cookies)
                    obj = json.loads(response.text)
                    if response.status_code == 200 | response.status_code == 201:
                        parentID = get_field_value(obj['Fields'], "id")
                        # print("folder id of " + folderName + " is " + str(parentID))
            return response.text
            #return parentID  it should be returning this


        except Exception as e:
            print('Error while fetching testsets')
            dictFolderJson=None    

    def get_field_value(self, obj, field_name):
        try:
            for field in obj:
                if field['Name'] == field_name:
                    return field['values'][0]['value']
        except Exception as e:
            print('Error ')

    def create_key_value(self, obj_json):
        try:
            final_dic = {}
            for elem in obj_json:
                if len(elem['values']) >= 1:
                    if 'value' in elem['values'][0]:
                        final_dic[elem["Name"]] = elem["values"][0]['value']
            return final_dic        
        except Exception as e:
            print('Error')

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

