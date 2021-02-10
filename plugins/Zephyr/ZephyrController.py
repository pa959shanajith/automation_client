#-------------------------------------------------------------------------------
# Name:        ZephyrController.py
# Purpose:
#
# Author:      keerthana.pai
#
# Created:     10/11/2020
# Copyright:   (c) keerthana.pai 2020
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
import readconfig
log = logging.getLogger("ZephyrController.py")

class ZephyrWindow():
    base_url = "https://prod-play.zephyr4jiracloud.com/connect"
    _headers = None
    account_id = None
    access_key = None
    secret_key = None
    payload = None
    jira_url = None
    jira_username = None
    jira_access_token = None
    relative_path = None
    canonical_path = None

    def __init__(self):
        self.zephyr_dict = {
            'domain': self.login,
            'project': self.get_projects
        }

    def login(self,filePath):
        res = "invalidcredentials"
        try:
            exp = time.time() + 3600
            self.account_id = filePath["zephyrAccNo"]
            self.access_key = filePath["zephyrAcKey"]
            self.secret_key = filePath["zephyrSecKey"]
            execFlag = filePath["execFlag"]
            self.payload = {
                'sub': self.account_id,
                'iss': self.access_key,
                'exp': time.time()+exp,
                'iat': time.time()
            } 

            self.relative_path = "/public/rest/api/1.0/serverinfo"
            self.canonical_path = 'GET&'+self.relative_path+'&'
            self.payload['qsh'] = hashlib.sha256(self.canonical_path.encode('utf-8')).hexdigest()
            token = jwt.encode(self.payload, self.secret_key, algorithm='HS256').strip().decode('utf-8')
            self._headers = {
                'Authorization': 'JWT ' + token,
                'Content-Type': 'text/plain',
                'zapiAccessKey': self.access_key
            }
            respon = requests.get(self.base_url+self.relative_path, headers=self._headers,verify=False,proxies=readconfig.proxies)

            if execFlag == "0":
                self.jira_url = filePath["zephyrJiraUrl"]
                self.jira_username = filePath["zephyrJiraUserName"]
                self.jira_access_token = filePath["zephyrJiraAccToken"]
                login_url = "/rest/api/3/project/search"
                tokengen = self.jira_username + ":" + self.jira_access_token
                # from requests.auth import HTTPBasicAuth
                # auth=HTTPBasicAuth('c5017', 'Welcome#20')
                encSt = base64.b64encode(bytes(tokengen, 'utf-8'))
                headersVal = {'Authorization':'Basic %s'% encSt.decode('ascii')}
                #checking account id
                acc_id_url = self.jira_url+"/rest/api/3/myself"
                acc_id_resp = requests.get(acc_id_url, headers=headersVal,verify=False,proxies=readconfig.proxies)
                if acc_id_resp.status_code == 200:
                    res_str = acc_id_resp.json()
                    if not (res_str["accountId"] == self.account_id):
                        return res            
                resp = requests.get(self.jira_url+login_url, headers=headersVal, verify=False,proxies=readconfig.proxies)
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
            elif execFlag == "1" and respon.status_code == 200:
                res = []
                return res
        except Exception as e:
            err_msg='Error while Login in Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return res
        
    def get_projects(self,filePath):
        res = []
        try:
            project_name = filePath["domain"]
            #fetch versions for version id to fetch cycles
            versions = self.jira_url+"/rest/api/3/project/"+self.project_dict[project_name]+"/version"
            tokengen = self.jira_username + ":" + self.jira_access_token
            encSt = base64.b64encode(bytes(tokengen, 'utf-8'))
            headersVal = {'Authorization':'Basic %s'% encSt.decode('ascii')}
            resp = requests.get(versions, headers=headersVal, verify=False,proxies=readconfig.proxies)
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

                resp = requests.get(self.base_url+self.relative_path, headers=self._headers,verify=False,proxies=readconfig.proxies)
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

                            #fetch tests for each cycle
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

                            resp = requests.get(self.base_url+self.relative_path, headers=self._headers,verify=False,proxies=readconfig.proxies)
                            JsonObject = resp.json()
                            if resp.status_code == 200:
                                if 'searchObjectList' in JsonObject and len(JsonObject['searchObjectList']) != 0:
                                    issue = [{'id':JsonObject['searchObjectList'][i]['execution']['id'],'name':JsonObject['searchObjectList'][i]['issueSummary'],'issueId':JsonObject['searchObjectList'][i]['execution']['issueId']} for i in range(len(JsonObject['searchObjectList'])) ]
                                    newObj['tests'] = issue
                            res.append(newObj)
        except Exception as eproject:
            err_msg = 'Error while fetching releases from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res

    def update_zephyr_test_details(self,data):
        status = False
        try:
            if(self.account_id == None) :
                qcLoginLoad = {}
                qcLoginLoad["zephyrAccNo"] = data['zephyr_accNo']
                qcLoginLoad["zephyrSecKey"] = data['zephyr_secKey']
                qcLoginLoad["zephyrAcKey"] = data['zephyr_acKey']
                qcLoginLoad["execFlag"] = "1"
                self.login(qcLoginLoad)
            # update status demo
            self.relative_path = "/public/rest/api/1.0/execution/"+str(data['testId'])
            rel_path = "/public/rest/api/1.0/execution/"+str(data['testId'])
            self.canonical_path = 'PUT&'+rel_path+'&'
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

            resp = requests.put(self.base_url+self.relative_path, headers=self._headers,json=exec_data,verify=False,proxies=readconfig.proxies)
            status = (resp.status_code == 200)
        except Exception as e:
            err_msg = 'Error while updating data in Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return status