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
import xmltodict
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
            json_str =(self.find_folder_and_testsets(test_plan_path.split("\\"), "test-set-folders", 0, "parent-id", domain_name, project_name ))
            folder_dict={}
            TestSet_dict={}
            key="testfolder"
            keyTS="TestSet"
            folder_dict.setdefault(key, [])
            TestSet_dict.setdefault(keyTS,[])
            treeList = json_str['folderl']
            if (len(treeList)>0):
                for folder in treeList:
                    temp_dict={}
                    temp_dict['foldername']=str(folder)
                    temp_dict['folderpath']=str(testsetpath+"\\"+str(folder))
                    folder_dict[key].append(temp_dict)
            tsList = json_str['testn']
            if(len(tsList)>0):
                for testset in tsList:
                    try:
                        TestSet_dict[keyTS].append(str(testset[0])+";"+str(testset[1]))
                    except:
                        TestSet_dict[keyTS].append(((testset[0]).encode('utf-8'))+";"+str(testset[1]))
            else:
                tsList = json_str['testn']
                if(len(tsList)>0):
                    for testset in tsList:
                        try:
                            TestSet_dict[keyTS].append(str(testset[0])+";"+str(testset[1]))
                        except:
                            TestSet_dict[keyTS].append(((testset[0]).encode('utf-8'))+";"+str(testset[1]))
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

    def find_folder_and_testsets(self, arrFolder, strAPI, parentID, fields, almDomain, almProject):
        try:
            response = ""
            midPoint = "/rest/domains/" + almDomain + "/projects/" + almProject 
            URL = self.Qc_Url + midPoint + "/" + strAPI
            URL_for_testsets = self.Qc_Url + midPoint + "/" + "test-sets"
            #URL_for_testsets = self.Qc_Url + midPoint + "/" + "tests"
            #for folderName in arrFolder:
            if(arrFolder[arrFolder.__len__()-1] != None) :
                folderName = arrFolder[arrFolder.__len__()-1]
                payload = {"query": "{name['" + folderName + "']}", "fields": fields}
                response = requests.get(URL, params=payload, headers=self.headers, cookies=self.cookies)
                o = xmltodict.parse(response.content)
                x = json.dumps(o)
                y = json.loads(x)
                k=y["Entities"]["Entity"]["Fields"]["Field"]

                #fetching folder parent id for given folder name
                for i in k:
                    if i["@Name"] == "id":
                        parentID=i['Value']

                fields = "id,name"
                payload1 = {"query": "{parent-id[" + str(parentID) + "]}", "fields": fields}
                res = requests.get(URL, params=payload1, headers=self.headers, cookies=self.cookies)
                o1 = xmltodict.parse(res.content)
                x1 = json.dumps(o1)
                y1 = json.loads(x1)
                fol_list = []
                if(int(y1["Entities"]["@TotalResults"]) >1 ):
                    k1 = y1["Entities"]["Entity"]
                #contains all the folder names
                    for f in k1:
                        l = f["Fields"]["Field"]
                        for n in l:
                            if n["@Name"] == "name" :
                                fol_name = n["Value"]
                                fol_list.append(fol_name)
                elif (int(y1["Entities"]["@TotalResults"]) == 1 ):
                    k1 = y1["Entities"]["Entity"]
                    l = k1["Fields"]["Field"]
                    for n in l:
                        if n["@Name"] == "name" :
                            fol_name = n["Value"]
                            fol_list.append(fol_name)
                #fetching testsets
                payload = {"query": "{parent-id[" + str(parentID) + "]}", "fields": fields}
                fields = "id,name"
                res1 = requests.get(URL_for_testsets, params=payload, headers=self.headers, cookies=self.cookies)
                o2 = xmltodict.parse(res1.content)
                x2 = json.dumps(o2)
                y2 = json.loads(x2)
                tests_list = []    #contains name
                tests_list_1 = []  #contains id
                if(int(y2["Entities"]["@TotalResults"]) >1 ):
                    k2 = y2["Entities"]["Entity"]
                    for c in k2:
                        l = c["Fields"]["Field"]
                        test_name_id = []
                        for t in l:
                            if t["@Name"] == "name" :
                                test_name = t["Value"]
                                test_name_id.append(test_name)
                            elif t["@Name"] == "id" :
                                test_id = t["Value"]
                                test_name_id.append(test_id)
                        tests_list_1.append(test_name_id) 
                        test_name_id = []       
                elif (int(y2["Entities"]["@TotalResults"]) == 1 ):
                    k2 = y2["Entities"]["Entity"]
                    l = k2["Fields"]["Field"]
                    test_name_id = []
                    for n in l:
                        if n["@Name"] == "name" :
                            test_name = n["Value"]
                            test_name_id.append(test_name)
                        elif n["@Name"] == "id" :
                            test_id = n["Value"]
                            test_name_id.append(test_id)    
                    tests_list_1.append(test_name_id)
                    test_name_id = []
                ans = {}
                key = "folderl"
                key1 = "testn"
                ans[key] = fol_list
                ans[key1] = tests_list_1
            return ans    
        except Exception as e:
            print('Error while fetching testsets')
            ans = {} 
            fol_list = []
            tests_list_1 = []
            key = "folderl"
            key1 = "testn"
            ans[key] = fol_list   
            ans[key1] = tests_list_1

    def test_case_generator(self,filePath):
        try:
            global dictFolderJson
            test_case_dict={}
            key="testcase"
            testsetpath=filePath["foldername"]
            test_set_name=filePath["testset"]
            almDomain=filePath["domain"]
            almProject=filePath["project"]
            test_case_dict.setdefault(key, [])
            response = ""
            midPoint = "/rest/domains/" + almDomain + "/projects/" + almProject 
            URL = self.Qc_Url + midPoint + "/" + "test-set-folders"
            URL_for_testsets = self.Qc_Url + midPoint + "/" + "test-sets"
            URL_for_testcases = self.Qc_Url + midPoint + "/" + "test-instances"
            arrFolder = testsetpath.split("\\")
            if(arrFolder[arrFolder.__len__()-1] != None) :
                folderName = arrFolder[arrFolder.__len__()-1]
                fields = "parent-id"
                payload = {"query": "{name['" + folderName + "']}", "fields": fields}
                response = requests.get(URL, params=payload, headers=self.headers, cookies=self.cookies)
                o = xmltodict.parse(response.content)
                x = json.dumps(o)
                y = json.loads(x)
                k=y["Entities"]["Entity"]["Fields"]["Field"]
                #fetching folder parent id for given folder name
                for i in k:
                    if i["@Name"] == "id":
                        parentID=i['Value']
            #fetching testsets
            fields = "id,name"
            payload = {"query": "{parent-id[" + str(parentID) + "]}", "fields": fields}
            res1 = requests.get(URL_for_testsets, params=payload, headers=self.headers, cookies=self.cookies)
            o2 = xmltodict.parse(res1.content)
            x2 = json.dumps(o2)
            y2 = json.loads(x2)
            test_id = None
            if(int(y2["Entities"]["@TotalResults"]) >1 ):
                k2 = y2["Entities"]["Entity"]
                for c in k2:
                    l = c["Fields"]["Field"]
                    flag = 0
                    for t in l:
                        if t["@Name"] == "name" :
                            if( t["Value"] == test_set_name ):
                                flag =1
                        elif( t["@Name"] == "id" and  flag == 1):
                            test_id = t["Value"]
            elif (int(y2["Entities"]["@TotalResults"]) == 1 ):
                k2 = y2["Entities"]["Entity"]
                l = k2["Fields"]["Field"]
                flag = 0
                for t in l:
                    if t["@Name"] == "name" :
                        if( t["Value"] == test_set_name ):
                            flag =1
                    elif( t["@Name"] == "id" and  flag == 1):
                        test_id = t["Value"]
            fields = "test-id,name,status"
            payload = {"query": "{cycle-id[" + str(test_id) + "]}", "fields": fields}
            #fetching test cases 
            response = requests.get(URL_for_testcases , params=payload, headers=self.headers, cookies=self.cookies)
            o = xmltodict.parse(response.content)
            x = json.dumps(o)
            y = json.loads(x)
            testc_list = []
            if(int(y["Entities"]["@TotalResults"]) >1 ):
                k2 = y["Entities"]["Entity"]
                for c in k2:
                    l = c["Fields"]["Field"]
                    testc_name_id = []
                    for n in l:                    
                        if n["@Name"] == "test-id" :
                            test_id = n["Value"]
                            testc_name_id.append(test_id)
                        elif n["@Name"] == "name" :
                            test_name = n["Value"]
                            testc_name_id.append(test_name)    
                    testc_list.append(testc_name_id) 
                    testc_name_id = []       
            elif (int(y2["Entities"]["@TotalResults"]) == 1 ):
                k2 = y2["Entities"]["Entity"]
                l = k2["Fields"]["Field"]
                testc_name_id = []
                for n in l:
                    if n["@Name"] == "test-id" :
                        test_id = n["Value"]
                        testc_name_id.append(test_id)
                    elif n["@Name"] == "name" :
                        test_name = n["Value"]
                        testc_name_id.append(test_name)      
                testc_list.append(testc_name_id)
                testc_name_id = []
            for tsname in testc_list:
                try:
                    ts_complete_name = tsname[0] + '/'+ tsname[1]
                    test_case_dict[key].append(str(ts_complete_name))
                except:
                    ts_complete_name = (tsname[0]).encode('utf-8') + '/'+ tsname[1]
                    test_case_dict[key].append((ts_complete_name).encode('utf-8'))
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
            almDomain =  data['qc_domain']
            almProject = data['qc_project']
            tsFolder = data['qc_folder']
            tsList = data['qc_tsList']
            testrunname = data['qc_testrunname']
            response = ""
            midPoint = "/rest/domains/" + almDomain + "/projects/" + almProject 
            URL = self.Qc_Url + midPoint + "/" + "test-set-folders"
            URL_for_testsets = self.Qc_Url + midPoint + "/" + "test-sets"
            URL_for_testcases = self.Qc_Url + midPoint + "/" + "test-instances"
            arrFolder = tsFolder.split("\\")
            if(arrFolder[arrFolder.__len__()-1] != None) :
                folderName = arrFolder[arrFolder.__len__()-1]
                fields = "parent-id"
                payload = {"query": "{name['" + folderName + "']}", "fields": fields}
                response = requests.get(URL, params=payload, headers=self.headers, cookies=self.cookies)
                o = xmltodict.parse(response.content)
                x = json.dumps(o)
                y = json.loads(x)
                k=y["Entities"]["Entity"]["Fields"]["Field"]
                #fetching folder parent id for given folder name
                for i in k:
                    if i["@Name"] == "id":
                        parentID=i['Value']
            #fetching testset id
            fields = "id,name"
            payload = {"query": "{parent-id[" + str(parentID) + "]}", "fields": fields}
            res1 = requests.get(URL_for_testsets, params=payload, headers=self.headers, cookies=self.cookies)
            o2 = xmltodict.parse(res1.content)
            x2 = json.dumps(o2)
            y2 = json.loads(x2)
            test_id = None
            if(int(y2["Entities"]["@TotalResults"]) >1 ):
                k2 = y2["Entities"]["Entity"]
                for c in k2:
                    l = c["Fields"]["Field"]
                    flag = 0
                    for t in l:
                        if t["@Name"] == "name" :
                            if( t["Value"] == tsList ):
                                flag =1
                        elif( t["@Name"] == "id" and  flag == 1):
                            test_id = t["Value"]
            elif (int(y2["Entities"]["@TotalResults"]) == 1 ):
                k2 = y2["Entities"]["Entity"]
                l = k2["Fields"]["Field"]
                flag = 0
                for t in l:
                    if t["@Name"] == "name" :
                        if( t["Value"] == tsList ):
                            flag =1
                    elif( t["@Name"] == "id" and  flag == 1):
                        test_id = t["Value"]
            fields = "name"
            payload = {"query": "{cycle-id[" + str(test_id) + "]}", "fields": fields}
            #fetching test case id 
            response = requests.get(URL_for_testcases , params=payload, headers=self.headers, cookies=self.cookies)
            o = xmltodict.parse(response.content)
            x = json.dumps(o)
            y = json.loads(x)
            testc_list = []
            tsn = testrunname    
            tsn1 = tsn.split("]")
            tsn = tsn1[1] + " " + tsn1[0] + "]"
            if(int(y["Entities"]["@TotalResults"]) >1 ):
                k2 = y["Entities"]["Entity"]
                for c in k2:
                    l = c["Fields"]["Field"]
                    flag = 0
                    for n in l:      
                        if n["@Name"] == "name" :
                            if( n["Value"] == tsn ):
                                flag = 1                
                        elif n["@Name"] == "id" and flag == 1:
                            testc_id = n["Value"]                  
            elif (int(y2["Entities"]["@TotalResults"]) == 1 ):
                k2 = y2["Entities"]["Entity"]
                l = k2["Fields"]["Field"]
                flag = 0
                for n in l:
                    if n["@Name"] == "name" :
                        if( n["Value"] == tsn ):
                            flag = 1                
                    elif n["@Name"] == "id" and flag == 1:
                        testc_id = n["Value"] 
            #updating status             
            result =  data['qc_update_status'] 
            URL_for_testcase_update = self.Qc_Url + midPoint + "/" + "test-instances"  + "/" + testc_id
            data1 ='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Entity Type="test-instance"><Fields><Field Name="status"><Value>'+ result +'</Value></Field></Fields></Entity>'
            payload = { "body": data1, "data": data1}
            self.headers = {'Content-Type': "application/xml",
                            'Accept': "application/xml"}
            respons = requests.put(URL_for_testcase_update , data= data1, headers=self.headers, cookies=self.cookies)
            status = True
        except Exception as e:
            print('Error while updating QC')
            status = False
        return status

    def quit_qc(self,filepath):
        try:
            ProjectURL = self.Qc_Url + '/authentication-point/logout'
            resp = requests.get(ProjectURL)
            return "closedqc"
        except Exception as e:
            print('Error while quitting qc')