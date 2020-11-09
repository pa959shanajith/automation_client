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
import base64
import datetime
import jwt
import time
import hashlib
log = logging.getLogger("Qccontroller.py")

class QcWindow():
    _headers = None
    account_id = None
    access_key = None
    secret_key = None
    payload = None
    jira_url = None
    jira_username = None
    jira_access_token = None

    def __init__(self):
        self.qc_dict = {
            'domain': self.login,
            'project': self.get_projects
        }

    def login(self,filePath):
        res = "invalidcredentials"
        try:
            exp = time.time() + 3600
            self.account_id = filePath["qcURL"]
            self.access_key = filePath["qcUsername"]
            self.secret_key = filePath["qcPassword"]
            self.jira_url = filePath["qcJiraUrl"]
            self.jira_username = filePath["qcJiraUserName"]
            self.jira_access_token = filePath["qcJiraAccToken"]
            self.payload = {
                'sub': self.account_id,
                'iss': self.access_key,
                'exp': time.time()+exp,
                'iat': time.time()
            }

            self.base_url = "https://prod-play.zephyr4jiracloud.com/connect"
            self.relative_path = "/public/rest/api/1.0/serverinfo"
            self.canonical_path = 'GET&'+self.relative_path+'&'
            self.payload['qsh'] = hashlib.sha256(self.canonical_path.encode('utf-8')).hexdigest()
            token = jwt.encode(self.payload, self.secret_key, algorithm='HS256').strip().decode('utf-8')
            self._headers = {
                'Authorization': 'JWT ' + token,
                'Content-Type': 'text/plain',
                'zapiAccessKey': self.access_key
            }
            respon = requests.get(self.base_url+self.relative_path, headers=self._headers,verify=False)
            # if resp.status_code == 200:

            login_url = "/rest/api/3/project/search"
            # user_name = "keerthana.pai@slkgroup.com"
            # pass_word = "SZgs90BOXp7Cjn8lYc8J9C59"
            tokengen = self.jira_username + ":" + self.jira_access_token
            #  DOOOOOOOOO THISSSSS
            # from requests.auth import HTTPBasicAuth
            # auth=HTTPBasicAuth('c5017', 'Welcome#20')
            encSt = base64.b64encode(bytes(tokengen, 'utf-8'))
            headersVal = {'Authorization':'Basic %s'% encSt.decode('ascii')}
            #checking account id
            acc_id_url = self.jira_url+"/rest/api/3/myself"
            acc_id_resp = requests.get(acc_id_url, headers=headersVal,verify=False)
            if acc_id_resp.status_code == 200:
                res_str = acc_id_resp.json()
                if not (res_str["accountId"] == self.account_id):
                    return res            
            resp = requests.get(self.jira_url+login_url, headers=headersVal, verify=False)
            JsonObject = None
            if resp.status_code == 200 and respon.status_code == 200:
                # response = json.loads(resp.text)
                JsonObject = resp.json()
                if len(JsonObject["values"]) == 0:
                    return res
                res = [{'id':i['id'],'name':i['name']} for i in JsonObject["values"]]
            self.project_dict = {}
            if JsonObject != None:
                for item in JsonObject["values"]:
                    self.project_dict[item['name']] = item['id']
        except Exception as e:
            err_msg='Error while Login in qTest'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return res
        
    def get_projects(self,filePath):
        res = []
        try:
            project_name = filePath["domain"]

            #fetch versions for version id to fetch cycles
            versions = "https://nineteen68.atlassian.net/rest/api/3/project/"+self.project_dict[project_name]+"/version"
            user_name = "keerthana.pai@slkgroup.com"
            pass_word = "SZgs90BOXp7Cjn8lYc8J9C59"
            # myobj = {'username': user_name, 'password':pass_word}
            tokengen = user_name + ":" + pass_word
            encSt = base64.b64encode(bytes(tokengen, 'utf-8'))
            headersVal = {'Authorization':'Basic %s'% encSt.decode('ascii')}
            resp = requests.get(versions, headers=headersVal, verify=False)
            response = resp.json()
            self.versions = []
            if resp.status_code == 200:
                if 'values' in response and len(response['values']) != 0:
                    self.versions = [ {'id': i['id'], 'name': i['name']} for i in response['values']]
                version = {'id': -1}
                self.versions.append(version)

            self.cycles = []
            for i in self.versions:
                # fetch cycles
                self.base_url = "https://prod-play.zephyr4jiracloud.com/connect"
                self.relative_path = "/public/rest/api/1.0/cycles/search?projectId="+self.project_dict[project_name]+"&versionId="+str(i['id'])
                rel_path = "/public/rest/api/1.0/cycles/search"
                parameters = "projectId="+self.project_dict[project_name]+"&versionId="+str(i['id'])
                self.canonical_path = 'GET&'+rel_path+'&'+parameters
                self.payload['qsh'] = hashlib.sha256(self.canonical_path.encode('utf-8')).hexdigest()
                token = jwt.encode(self.payload, self.secret_key, algorithm='HS256').strip().decode('utf-8')
                self._headers = {
                    'Authorization': 'JWT ' + token,
                    'Content-Type': 'text/plain',
                    'zapiAccessKey': self.access_key
                }

                resp = requests.get(self.base_url+self.relative_path, headers=self._headers,verify=False)
                JsonObject = resp.json()
                if resp.status_code == 200:
                    for i in JsonObject:
                        if i['id'] != '-1':
                            newObj = {}
                            newObj["cycle"]=i['name']
                            newObj["cycleId"]=i["id"]
                            newObj['projectId']=i['projectId']
                            newObj['versionId']=i['versionId']
                            newObj['tests'] = []
                            # cycle = {'id': i['id'],'name': i['name'],'projectId': i['projectId'],'versionId': i['versionId']}

                            #fetch tests for each cycle
                            self.base_url = "https://prod-play.zephyr4jiracloud.com/connect"
                            self.relative_path = "/public/rest/api/1.0/executions/search/cycle/"+str(i['id'])+"?versionId="+str(i['versionId'])+"&projectId="+str(i['projectId'])
                            rel_path = "/public/rest/api/1.0/executions/search/cycle/"+str(i['id'])
                            parameters = "projectId="+str(i['projectId'])+"&versionId="+str(i['versionId'])
                            self.canonical_path = 'GET&'+rel_path+'&'+parameters
                            self.payload['qsh'] = hashlib.sha256(self.canonical_path.encode('utf-8')).hexdigest()
                            token = jwt.encode(self.payload, self.secret_key, algorithm='HS256').strip().decode('utf-8')
                            self._headers = {
                                'Authorization': 'JWT ' + token,
                                'Content-Type': 'application/json',
                                'zapiAccessKey': self.access_key
                            }

                            resp = requests.get(self.base_url+self.relative_path, headers=self._headers,verify=False)
                            JsonObject = resp.json()
                            if resp.status_code == 200:
                                if 'searchObjectList' in JsonObject and len(JsonObject['searchObjectList']) != 0:
                                    issue = [{'id':JsonObject['searchObjectList'][i]['execution']['id'],'name':JsonObject['searchObjectList'][i]['issueSummary'],'issueId':JsonObject['searchObjectList'][i]['execution']['issueId']} for i in range(len(JsonObject['searchObjectList'])) ]
                                    newObj['tests'] = issue
                            res.append(newObj)
        except Exception as eproject:
            err_msg = 'Error while fetching releases from qTest'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res

    def update_zephyr_test_details(self,data):
        status = False
        try:
            # update status demo
            self.base_url = "https://prod-play.zephyr4jiracloud.com/connect"
            self.relative_path = "/public/rest/api/1.0/execution/"+str(data['testId'])
            rel_path = "/public/rest/api/1.0/execution/"+str(data['testId'])
            # parameters = "projectId=10000&versionId=10054"
            self.canonical_path = 'PUT&'+rel_path+'&'
            # exec_data = {
            #     "status": {"id": "2"},
            #     "id": "b2c2a59a-d342-4f15-a266-d3e5c9d9d601",
            #     "projectId": 10000,
            #     "issueId": 11199,
            #     "cycleId": "d628b4e6-60aa-4f5c-965b-14f5de4b2080",
            #     "versionId": 10054
            # }

            exec_data = {
                "cycleId": data['cycleId'],
                "id": data['testId'],
                "issueId": data['issueId'],
                "projectId": data['projectId'],
                "status": data['status'],
                "versionId": data['versionId']
            }
            self.payload['qsh'] = hashlib.sha256(self.canonical_path.encode('utf-8')).hexdigest()
            token = jwt.encode(self.payload, self.secret_key, algorithm='HS256').strip().decode('utf-8')
            self._headers = {
                'Authorization': 'JWT ' + token,
                'Content-Type': 'application/json',
                'zapiAccessKey': self.access_key
            }

            # releases = []
            # releaseURL = self.Qc_Url + '/api/v3/projects/'+str(self.project_dict[project_name])+'/releases?includeClosed=true'
            resp = requests.put(self.base_url+self.relative_path, headers=self._headers,json=exec_data,verify=False)
            JsonObject = resp.json()
            # if resp.status_code == 200:
            status = (resp.status_code == 200)
                # response = resp.text          
           
            # self.base_url = "https://prod-play.zephyr4jiracloud.com/connect"
            # self.relative_path = "/public/rest/api/1.0/executions/search/cycle/d628b4e6-60aa-4f5c-965b-14f5de4b2080?versionId=10054&projectId=10000"
            # rel_path = "/public/rest/api/1.0/execution/b2c2a59a-d342-4f15-a266-d3e5c9d9d601"
            # # parameters = "projectId=10000&versionId=10054"
            # self.canonical_path = 'PUT&'+rel_path+'&'
            # exec_data = {
            #     "status":{"id":2},
            #     "id":"b2c2a59a-d342-4f15-a266-d3e5c9d9d601",
            #     "projectId":10000,
            #     "issueId":11199,
            #     "cycleId":"d628b4e6-60aa-4f5c-965b-14f5de4b2080",
            #     "versionId":10054
            # }
            # self.payload['qsh'] = hashlib.sha256(self.canonical_path.encode('utf-8')).hexdigest()
            # token = jwt.encode(self.payload, self.secret_key, algorithm='HS256').strip().decode('utf-8')
            # self._headers = {
            #     'Authorization': 'JWT ' + token,
            #     'Content-Type': 'application/json',
            #     'zapiAccessKey': self.access_key
            # }

            # # releases = []
            # # releaseURL = self.Qc_Url + '/api/v3/projects/'+str(self.project_dict[project_name])+'/releases?includeClosed=true'
            # resp = requests.post(self.base_url+self.relative_path, headers=self._headers,json=exec_data,verify=False)
            # JsonObject = resp.json()
            # if resp.status_code == 200:
            #     response = resp.text                 
            
            
            
            # updateRequest = {}
            # updateRequest['submittedBy'] = data['user']
            # if data['qc_status_over']['overallstatus'].lower() == "pass":
            #     updateRequest['status']={"id":601}
            # elif data['qc_status_over']['overallstatus'].lower() == "fail":
            #     updateRequest['status']={"id":602}
            # elif data['qc_status_over']['overallstatus'].lower() == "terminate":
            #     updateRequest['status']={"id":603}
            # # Converting time format
            # # From: YYYY-MM-DD hh:mm:ss.ffffff
            # # To: YYYY-MM-DDThh:mm:ss.fffZ
            # updateRequest['exe_start_date']=data['qc_status_over']['StartTime'][:10]+"T"+data['qc_status_over']['StartTime'][11:23]+"Z"
            # updateRequest['exe_end_date']=data['qc_status_over']['EndTime'][:10]+"T"+data['qc_status_over']['EndTime'][11:23]+"Z"
            # getstepsAPI = self.Qc_Url + "/api/v3/projects/"+str(data['qc_projectid'])+"/test-runs/"+str(data['qc_suiteid'])+"?expand=testcase.teststep"
            # res2 = requests.get(getstepsAPI,  headers=self._headers,verify=False)
            # resp2 = res2.json()
            
            # if data['qc_stepsup']:
            #     updateRequest['test_step_logs'] = []
            #     # if(len(resp2['test_case']['test_steps'])>len(data['steps'])):
            #     stepLength = len(data['steps'])
            #     # else:
            #         # stepLength = len(resp2['test_case']['test_steps'])
            #     for j in range(tsplistLen):
            #         try:
            #             stepStatus = data['steps'][j]
            #             if stepStatus != 603:
            #                 stepId = resp2['test_case']['test_steps'][j]['id']
            #                 updateRequest['test_step_logs'].append({"test_step_id":stepId,"status":{"id":stepStatus}})
            #             else:
            #                 stepId = [resp2['test_case']['test_steps'][k]['id'] for k in range(j,len(resp2['test_case']['test_steps']))]
            #                 updateRequest['test_step_logs'].extend([{"test_step_id":step,"status":{"id":stepStatus}} for step in stepId])
            #                 break
            #         except Exception:
            #             stepStatus = 603
            #             stepId = [resp2['test_case']['test_steps'][k]['id'] for k in range(j,tsplistLen)]
            #             updateRequest['test_step_logs'].extend([{"test_step_id":step,"status":{"id":stepStatus}} for step in stepId])
            #             break

            # updatetestlog = self.Qc_Url + "/api/v3/projects/"+str(data['qc_projectid'])+"/test-runs/"+str(data['qc_suiteid'])+"/test-logs"
            # res3 = requests.post(updatetestlog, headers = self._headers, json=updateRequest,verify=False) 
            # status = (res3.status_code == 201)
        except Exception as e:
            err_msg = 'Error while updating data in qTest'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return status