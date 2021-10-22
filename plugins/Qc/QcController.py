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
from requests.exceptions import ConnectionError
import requests
import logger
import logging
import xmltodict
import readconfig
log = logging.getLogger("Qccontroller.py")

class QcWindow():
    cookies = None
    headers = None
    _headers = None
    Qc_Url = None

    def __init__(self):
        self.qc_dict = {
            'domain': self.login,
            'project': self.get_projects,
            'folder': self.list_test_set_folder,
            'testcase': self.test_case_generator,
            'qcupdate': self.update_qc_details,
            'qcquit': self.quit_qc
        }

    def login(self,filePath):
        res = "invalidcredentials"
        try:
            user_name=filePath["qcUsername"]
            pass_word=filePath["qcPassword"]
            self.Qc_Url=filePath["qcURL"]
            self.headers = {'cache-control': "no-cache"}
            login_url = self.Qc_Url + '/api/authentication/sign-in'
            resp = requests.get(login_url, auth=HTTPBasicAuth(user_name, pass_word),  headers=self.headers,proxies=readconfig.proxies)
            if resp.status_code == 500 or resp.status_code == 503 :
                res = "serverdown"
            if resp.status_code == 200:
                self.cookies=resp.cookies
            else:
                self.headers = {"Content-Type": "application/json"}
                login_url = self.Qc_Url + '/rest/oauth2/login'
                payload={"clientId":user_name,"secret":pass_word}
                resp = requests.post(login_url,  headers=self.headers,data=json.dumps(payload),proxies=readconfig.proxies)
                self.cookies=resp.cookies
        
            #fetching domains
            domain_dict={}
            key="domain"
            domain_dict.setdefault(key, [])
            domain_dict['login_status']=True
            self._headers = {
                'accept': 'application/json'
            }
            DomainURL = self.Qc_Url + '/rest/domains/'
            _resp = requests.get(DomainURL, headers=self._headers, cookies=self.cookies,proxies=readconfig.proxies)   
            JsonObject = _resp.json()
            domain_obj=JsonObject['Domains']['Domain']
            DomainList=[]
            if type(domain_obj)==list:
                DomainList = [item['Name'] for item in domain_obj]
            elif type(domain_obj)==dict:
                DomainList = [v for k,v in domain_obj.items()]
            if(len(DomainList)>0):
                for dom in DomainList:
                    domain_dict[key].append(str(dom))
            res = json.loads(json.dumps(domain_dict))
        except ConnectionError as e:
            res = "notreachable"
            err_msg='Error while Connecting ALM'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        except Exception as e:
            err_msg='Error while Login in ALM'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return res
        
    def get_projects(self,filePath):
        res = {"project": []}
        try:
            domain_name = filePath["domain"]
            projects = []
            ProjectURL = self.Qc_Url + '/rest/domains/' + domain_name + '/projects'
            resp = requests.get(ProjectURL, headers=self._headers, cookies=self.cookies,proxies=readconfig.proxies)
            JsonObject = resp.json()
            list_projects = []
            if type(JsonObject['Projects']['Project']) is list:
                list_projects = [item['Name'] for item in JsonObject['Projects']['Project']]
            if type(JsonObject['Projects']['Project']) is dict:
                list_projects = [JsonObject['Projects']['Project']['Name']]
            if(len(list_projects)>0):
                for pro in list_projects:
                    projects.append(str(pro))
                res["project"] = projects
            else:
                err_msg = 'Selected ALM domain has no projects'
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as eproject:
            err_msg = 'Error while fetching projects from ALM'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res

    def get_folder_parent_id(self, URL, folderName,folderId):
        parentID = 0
        payload = {"query": "{name['" + folderName + "'];id['" + str(folderId) + "']}", "fields": "parent-id"}
        try:
            response = requests.get(URL, params=payload, headers=self.headers, cookies=self.cookies,proxies=readconfig.proxies)
            o = xmltodict.parse(response.content)
            y = json.loads(json.dumps(o))
            k = y["Entities"]["Entity"]["Fields"]["Field"]
            #fetching folder parent id for given folder name
            for i in k:
                if i["@Name"] == "id":
                    parentID = i['Value']
        except:
            pass
        return str(parentID)

    def list_test_set_folder(self,filePath):
        ##The final list which contains the testsets and testset under the specified path
        res = None
        try:
            testsetpath = str(filePath["foldername"])
            almDomain = filePath["domain"]
            almProject = filePath["project"]
            folderName = testsetpath.split("\\")[-1]
            folderId= filePath["folderid"]
            midPoint = "/rest/domains/" + almDomain + "/projects/" + almProject 
            URL = self.Qc_Url + midPoint + "/" + "test-set-folders"
            URL_for_testsets = self.Qc_Url + midPoint + "/" + "test-sets"
            parentID = self.get_folder_parent_id(URL, folderName, folderId)
            payload1 = {"query": "{parent-id[" + parentID + "]}", "fields": "id,name"}
            response1 = requests.get(URL, params=payload1, headers=self.headers, cookies=self.cookies,proxies=readconfig.proxies)
            o1 = xmltodict.parse(response1.content)
            y1 = json.loads(json.dumps(o1))
            folder_list = []
            entity_len = int(y1["Entities"]["@TotalResults"])
            if (entity_len == 1): y1["Entities"]["Entity"] = [y1["Entities"]["Entity"]]
            if (entity_len > 0):
                k1 = y1["Entities"]["Entity"] #contains all the folder names
                for f in k1:
                    l = f["Fields"]["Field"]
                    folder = fid = None
                    for n in l:
                        if n["@Name"] == "name":
                            folder = str(n["Value"])
                        if n["@Name"] == "id":
                            fid = str(n["Value"])
                        if folder != None and fid != None:
                            folder_list.append({"foldername": folder, "folderpath": testsetpath + "\\" + folder,"folderid": fid})

            #fetching testsets
            payload = {"query": "{parent-id[" + parentID + "]}", "fields": "id,name"}
            res1 = requests.get(URL_for_testsets, params=payload, headers=self.headers, cookies=self.cookies,proxies=readconfig.proxies)
            o2 = xmltodict.parse(res1.content)
            y2 = json.loads(json.dumps(o2))
            tests_list = []
            entity_len = int(y2["Entities"]["@TotalResults"])
            if (entity_len == 1): y2["Entities"]["Entity"] = [y2["Entities"]["Entity"]]
            if (entity_len > 0):
                k2 = y2["Entities"]["Entity"]
                for c in k2:
                    l = c["Fields"]["Field"]
                    test_name = ""
                    test_id = ""
                    for t in l:
                        if t["@Name"] == "name":
                            test_name = str(t["Value"])
                        elif t["@Name"] == "id" :
                            test_id = str(t["Value"])
                    tests_list.append({'testset': test_name, 'testsetid': test_id, 'testsetpath': testsetpath, 'folderid': parentID})
            res = [{"testfolder": folder_list, "TestSet": tests_list}]
        except Exception as e:
            err_msg = 'Error while fetching testsets from ALM'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return res

    def test_case_generator(self,filePath):
        res = None
        try:
            testsetpath=filePath["foldername"]
            test_set_name=filePath["testset"]
            almDomain=filePath["domain"]
            almProject=filePath["project"]
            folderId= filePath["folderid"]
            response = ""
            midPoint = "/rest/domains/" + almDomain + "/projects/" + almProject 
            URL = self.Qc_Url + midPoint + "/" + "test-set-folders"
            URL_for_testsets = self.Qc_Url + midPoint + "/" + "test-sets"
            URL_for_testcases = self.Qc_Url + midPoint + "/" + "test-instances"
            folderName = testsetpath.split("\\")[-1]
            parentID = self.get_folder_parent_id(URL, folderName, folderId)
            #fetching testsets
            payload = {"query": "{parent-id[" + parentID + "]}", "fields": "id,name"}
            res1 = requests.get(URL_for_testsets, params=payload, headers=self.headers, cookies=self.cookies,proxies=readconfig.proxies)
            o2 = xmltodict.parse(res1.content)
            y2 = json.loads(json.dumps(o2))
            test_id = None
            entity_len = int(y2["Entities"]["@TotalResults"])
            if (entity_len == 1): y2["Entities"]["Entity"] = [y2["Entities"]["Entity"]]
            if (entity_len > 0):
                k2 = y2["Entities"]["Entity"]
                for c in k2:
                    l = c["Fields"]["Field"]
                    flag = 0
                    for t in l:
                        if t["@Name"] == "name" :
                            if t["Value"] == test_set_name: flag =1
                        elif (t["@Name"] == "id" and flag == 1):
                            test_id = t["Value"]

            payload = {"query": "{cycle-id[" + str(test_id) + "]}", "fields": "test-id,name,status"}
            #fetching test cases 
            response = requests.get(URL_for_testcases , params=payload, headers=self.headers, cookies=self.cookies,proxies=readconfig.proxies)
            o = xmltodict.parse(response.content)
            y = json.loads(json.dumps(o))
            test_case_list = []
            entity_len = int(y["Entities"]["@TotalResults"])
            if (entity_len == 1): y["Entities"]["Entity"] = [y["Entities"]["Entity"]]
            if (entity_len > 0):
                k2 = y["Entities"]["Entity"]
                for c in k2:
                    l = c["Fields"]["Field"]
                    test_id = ""
                    test_name = ""
                    for n in l:
                        if n["@Name"] == "test-id": test_id = str(n["Value"])
                        elif n["@Name"] == "name": test_name = str(n["Value"])
                    test_case_list.append(test_name + '/'+ test_id)
            res = [{"testcase": test_case_list}]
        except Exception as e:
            err_msg = 'Error while fetching testcases from ALM'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return res

    def update_qc_details(self,data):
        status = False
        try:
            if(self.Qc_Url == None) :
                qcLoginLoad = {}
                qcLoginLoad["qcUsername"] = data['qcusername']
                qcLoginLoad["qcPassword"] = data['qcpassword']
                qcLoginLoad["qcURL"] = data['qcurl']
                self.login(qcLoginLoad)
            almDomain =  data['qc_domain']
            almProject = data['qc_project']
            tsFolder = data['qc_folder']
            tsList = data['qc_tsList']
            folderid = data['qc_folderid'] 
            testrunname = data['qc_testrunname']
            for indexTest in range(len(tsFolder)):
                midPoint = "/rest/domains/" + almDomain + "/projects/" + almProject 
                URL = self.Qc_Url + midPoint + "/" + "test-set-folders"
                URL_for_testsets = self.Qc_Url + midPoint + "/" + "test-sets"
                URL_for_testcases = self.Qc_Url + midPoint + "/" + "test-instances"
                folderName = tsFolder[indexTest].split("\\")[-1]
                folderId = folderid[indexTest] 
                parentID = self.get_folder_parent_id(URL, folderName, folderId)
                #fetching testset id
                payload = {"query": "{parent-id[" + str(parentID) + "]}", "fields": "id,name"}
                res1 = requests.get(URL_for_testsets, params=payload, headers=self.headers, cookies=self.cookies,proxies=readconfig.proxies)
                o2 = xmltodict.parse(res1.content)
                y2 = json.loads(json.dumps(o2))
                test_id = None
                entity_len = int(y2["Entities"]["@TotalResults"])
                if (entity_len == 1): y2["Entities"]["Entity"] = [y2["Entities"]["Entity"]]
                if (entity_len > 0):
                    k2 = y2["Entities"]["Entity"]
                    for c in k2:
                        l = c["Fields"]["Field"]
                        flag = 0
                        for t in l:
                            if t["@Name"] == "name" :
                                if(t["Value"] == tsList[indexTest]): flag = 1
                            elif( t["@Name"] == "id" and flag == 1):
                                test_id = t["Value"]
                payload = {"query": "{cycle-id[" + str(test_id) + "]}", "fields": "name"}
                #fetching test case id 
                response = requests.get(URL_for_testcases , params=payload, headers=self.headers, cookies=self.cookies,proxies=readconfig.proxies)
                o = xmltodict.parse(response.content)
                y = json.loads(json.dumps(o))
                tsn1 = []
                tsn = []
                testc_id = []
                # for z in testrunname:
                tsn1.append(testrunname[indexTest].split("]"))
                for x in tsn1:
                    xx=(x[1] + " " + x[0] + "]")[1:]
                    xx=xx.lstrip('0123456789')
                    tsn.append(xx)
                entity_len = int(y["Entities"]["@TotalResults"])
                if (entity_len == 1): y["Entities"]["Entity"] = [y["Entities"]["Entity"]]
                if (entity_len > 0):
                    k2 = y["Entities"]["Entity"]
                    for c in k2:
                        l = c["Fields"]["Field"]
                        flag = 0
                        for n in l:      
                            if n["@Name"] == "name":
                                for nst in tsn:
                                    if n["Value"] == nst: flag = 1                
                            elif n["@Name"] == "id" and flag == 1:
                                testc_id.append(n["Value"])                  
                #updating status             
                result =  data['qc_update_status']
                for t in testc_id:
                    URL_for_testcase_update = self.Qc_Url + midPoint + "/" + "test-instances"  + "/" + t
                    data1 ='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Entity Type="test-instance"><Fields><Field Name="status"><Value>'+ result +'</Value></Field></Fields></Entity>'
                    payload = { "body": data1, "data": data1}
                    self.headers = {'Content-Type': "application/xml", 'Accept': "application/xml"}
                    response = requests.put(URL_for_testcase_update , data= data1, headers=self.headers, cookies=self.cookies,proxies=readconfig.proxies)
                    #status = response.status_code == 200
                if indexTest == 0: status = response.status_code == 200
                else: status = response.status_code == 200 and status
        except Exception as e:
            err_msg = 'Error while updating data in ALM'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return status

    def quit_qc(self,filepath):
        res = None
        try:
            resp = requests.get(self.Qc_Url + '/authentication-point/logout',proxies=readconfig.proxies)
            #status = resp.status_code == 200
            res = "closedqc"
        except Exception as e:
            err_msg = 'Error while logging off from ALM'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return res
