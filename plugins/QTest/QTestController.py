#-------------------------------------------------------------------------------
# Name:        QTestController.py
# Purpose:
#
# Author:      keerthana.pai
#
# Created:     28/12/2020
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
log = logging.getLogger("QTestController.py")

class QTestWindow():
    cookies = None
    headers = None
    _headers = None
    qTest_Url = None
    access_token = None
    token_type = None
    project_dict = None
    release_dict = None

    def __init__(self):
        self.qc_dict = {
            'domain': self.login,
            'project': self.get_projects,
            'folder': self.list_test_set_folder,
            'suitedetails': self.get_suite_details
        }

    def login(self,filePath):
        res = "invalidcredentials"
        try:
            user_name=filePath["qtestusername"]
            pass_word=filePath["qtestpassword"]
            self.qTest_Url=filePath["qtesturl"]
            self.headers = {'cache-control': "no-cache"}
            login_url = self.qTest_Url + '/oauth/token'
            myobj = {'grant_type': 'password', 'username': user_name, 'password':pass_word}
            splitUrl = bytes(self.qTest_Url.split("//")[1].split(".")[0]+':','ascii')
            encSt = base64.b64encode(splitUrl)
            headersVal = {'Authorization':'Basic %s'% encSt.decode('ascii')}
            resp = requests.post(login_url,  headers=headersVal, data = myobj, verify=False)
            if resp.status_code == 200:
                response = json.loads(resp.text)
                self.access_token = response['access_token']
                self.token_type = response['token_type']
               
                domain_dict={}
                key="domain"
                domain_dict.setdefault(key, [])
                domain_dict['login_status']=True
                self._headers = {
                    'accept': 'application/json',
                    'Authorization' : self.token_type+" "+self.access_token
                }
                DomainURL = self.qTest_Url + '/api/v3/projects'
                _resp = requests.get(DomainURL, headers=self._headers,verify=False)   
                JsonObject = _resp.json()
                res = [{'id':i['id'],'name':i['name']} for i in JsonObject]
                self.project_dict = {}
                for item in JsonObject:
                    self.project_dict[item['name']] = item['id']
        except Exception as e:
            err_msg='Error while Login in qTest'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return res
        
    def get_projects(self,filePath):
        res = {"project": []}
        try:
            project_name = filePath["domain"]
            releases = []
            releaseURL = self.qTest_Url + '/api/v3/projects/'+str(self.project_dict[project_name])+'/releases?includeClosed=true'
            resp = requests.get(releaseURL, headers=self._headers,verify=False)
            JsonObject = resp.json()
            # JsonObject.append({'links': [{'rel': 'test-cycles', 'href': 'dummy.dummy'}], 'name': 'rel1'})
            self.release_dict = {}
            for item in JsonObject:
                if 'links' in item:
                    self.release_dict[item['name']] = [i['href'] for i in item['links'] if i['rel']=='test-cycles']
                else:
                    self.release_dict[item['name']] = [self.qTest_Url + "/api/v3/projects/"+str(self.project_dict[project_name])+"/test-cycles?parentType=release&parentId="+str(item['id'])]
            if len(JsonObject) >0:
                releases = list(self.release_dict.keys())
                res["project"] = releases
            else:
                err_msg = 'Selected qTest project has no releases'
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as eproject:
            err_msg = 'Error while fetching releases from qTest'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res

    def get_suite_details(self, filePath):
        res = []
        try:
            suitedata = filePath['suiteData']
            # suiteid = filePath["suiteId"]
            # projectid = filePath["projectId"]
            for i in suitedata:
                suiteid = i['qtestsuiteid']
                projectid = i['qtestprojectid']
                # maptype = i['maptype']
                # if(maptype == 'testsuite'):
                #     URL = self.qTest_Url + '/api/v3/projects/' + str(projectid) + '/test-suites/' + str(suiteid)
                # elif(maptype == 'testrun'):
                URL = self.qTest_Url + '/api/v3/projects/' + str(projectid) + '/test-runs/' + str(suiteid)
                response = requests.get(URL,  headers=self._headers, verify=False)
                resp = response.json()
                if 'name' in resp:
                    i['qtestsuite'] = resp['name']
                    # i['qtestsuite'] = 'dummo'+str(suiteid)
                    res.append(i)
        except:
            pass
        return res

    def list_test_set_folder(self,filePath):
        res = []
        try:
            testsetpath = str(filePath["foldername"])
            almDomain = filePath["domain"]
            almProject = filePath["project"]
            folderUrl = self.release_dict[almProject][0] + '&expand=descendants'
            response = requests.get(folderUrl, headers=self._headers,verify=False)
            JsonObject = response.json()
            # JsonObject = []
            for cycle in JsonObject:
                newObj = {}
                newObj["cycle"]=cycle['name']
                newObj['testsuites'] = []
                # newObj["testsuites"]=[{'name':i['name'],'id':i['id']} for i in cycle['test-suites']]
                for i in cycle['test-suites']:
                    gettestrunAPI = self.qTest_Url + "/api/v3/projects/"+str(almDomain)+"/test-runs?parentId="+str(i['id'])+"&parentType=test-suite"
                    res1 = requests.get(gettestrunAPI,  headers=self._headers,verify=False)
                    resp1 = res1.json()
                    if 'items' in resp1:
                        testruns = [{'id':j['id'],'name':j['name']} for j in resp1['items']]
                    else:
                        testruns = [{'id':j['id'],'name':j['name']} for j in resp1]
                    newObj['testsuites'].append({'id':i['id'],'name':i['name'],'testruns':testruns})
                # newObj[cycle['name']] = [{'name':i['name'],'id':i['id']} for i in cycle['test-suites']]
            res.append(newObj)
        except Exception as e:
            err_msg = 'Error while fetching testsuites from qTest'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return res

    def update_qtest_run_details(self,data, tsplistLen):
        status = False
        stepLength = None
        try:
            if(self.qTest_Url == None) :
                qtestLoginLoad = {}
                qtestLoginLoad["qtestusername"] = data['qtestusername']
                qtestLoginLoad["qtestpassword"] = data['qtestpassword']
                qtestLoginLoad["qtesturl"] = data['qtesturl']
                self.login(qtestLoginLoad)
            updateRequest = {}
            updateRequest['submittedBy'] = data['user']
            if data['qtest_status_over']['overallstatus'].lower() == "pass":
                updateRequest['status']={"id":601}
            elif data['qtest_status_over']['overallstatus'].lower() == "fail":
                updateRequest['status']={"id":602}
            elif data['qtest_status_over']['overallstatus'].lower() == "terminate":
                updateRequest['status']={"id":603}
            # Converting time format
            # From: YYYY-MM-DD hh:mm:ss.ffffff
            # To: YYYY-MM-DDThh:mm:ss.fffZ
            updateRequest['exe_start_date']=data['qtest_status_over']['StartTime'][:10]+"T"+data['qtest_status_over']['StartTime'][11:23]+"Z"
            updateRequest['exe_end_date']=data['qtest_status_over']['EndTime'][:10]+"T"+data['qtest_status_over']['EndTime'][11:23]+"Z"
            getstepsAPI = self.qTest_Url + "/api/v3/projects/"+str(data['qtest_projectid'])+"/test-runs/"+str(data['qtest_suiteid'])+"?expand=testcase.teststep"
            res2 = requests.get(getstepsAPI,  headers=self._headers,verify=False)
            resp2 = res2.json()
            
            if data['qtest_stepsup']:
                updateRequest['test_step_logs'] = []
                # if(len(resp2['test_case']['test_steps'])>len(data['steps'])):
                stepLength = len(data['steps'])
                # else:
                    # stepLength = len(resp2['test_case']['test_steps'])
                for j in range(tsplistLen):
                    try:
                        stepStatus = data['steps'][j]
                        if stepStatus != 603:
                            stepId = resp2['test_case']['test_steps'][j]['id']
                            updateRequest['test_step_logs'].append({"test_step_id":stepId,"status":{"id":stepStatus}})
                        else:
                            stepId = [resp2['test_case']['test_steps'][k]['id'] for k in range(j,len(resp2['test_case']['test_steps']))]
                            updateRequest['test_step_logs'].extend([{"test_step_id":step,"status":{"id":stepStatus}} for step in stepId])
                            break
                    except Exception:
                        stepStatus = 603
                        stepId = [resp2['test_case']['test_steps'][k]['id'] for k in range(j,tsplistLen)]
                        updateRequest['test_step_logs'].extend([{"test_step_id":step,"status":{"id":stepStatus}} for step in stepId])
                        break

            updatetestlog = self.qTest_Url + "/api/v3/projects/"+str(data['qtest_projectid'])+"/test-runs/"+str(data['qtest_suiteid'])+"/test-logs"
            res3 = requests.post(updatetestlog, headers = self._headers, json=updateRequest,verify=False) 
            status = (res3.status_code == 201)
        except Exception as e:
            err_msg = 'Error while updating data in qTest'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return status