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

    def __init__(self):
        self.zephyr_dict = {
            'login': self.login,
            'project': self.get_projects,
            'release': self.get_release,
            'cyclephase': self.get_cycle_phases,
            'mapcyclephase': self.get_mapped_cycle_phases,
            'testcase': self.get_testcases,
            'maptestcase': self.get_mapped_testcases,
            'projectrepo': self.get_project_repository,
            'repodetails': self.get_all_repos,
            'repotestcase': self.get_repo_testcases
        }
        self.baseURL = None
        self.zephyrURL = None
        self.zephyrUserName = None
        self.zephyrPassword = None
        self.headers = None
        self.release_id = None
        self.project_id = None

    def login(self,filePath):
        res = "invalidcredentials"
        try:
            zephyrPayload = filePath["zephyrPayload"]
            self.baseURL = zephyrPayload["zephyrURL"]
            self.zephyrURL = self.baseURL + "/flex/services/rest/latest"

            relative_path = "/project/lite"
            self.authType = zephyrPayload["authtype"]
            if self.authType == "basic":
                userpass = bytes(zephyrPayload["zephyrUserName"] + ':' + zephyrPayload["zephyrPassword"],'ascii')
                encSt = base64.b64encode(userpass)
                headersVal = {'Authorization':'Basic %s'% encSt.decode('ascii')}
                self.headers =  headersVal
                respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
                if respon.status_code == 200:
                    JsonObject = respon.json()
                    res = [{'id':i['id'],'name':i['name']} for i in JsonObject]
            else:
                self.headers = {'Authorization':'Bearer %s'% zephyrPayload["zephyrApiToken"]}
                respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
                if respon.status_code == 200:
                    JsonObject = respon.json()
                    res = [{'id':i['id'],'name':i['name']} for i in JsonObject]
        except Exception as e:
            err_msg='Error while Login in Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return res

    def get_projects(self,filePath):
        res = []
        try:
            self.zephyrURL = self.baseURL + "/flex/services/rest/latest"

            relative_path = "/project/lite"
            respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
            if respon.status_code == 200:
                JsonObject = respon.json()
                res = [{'id':i['id'],'name':i['name']} for i in JsonObject]
        except Exception as e:
            err_msg='Error while Login in Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return res
        
    def get_release(self,filePath):
        res = []
        try:
            # get all releases
            projectId = filePath["projectId"]
            relative_path = "/release/project/"+str(projectId)
            respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
            if respon.status_code == 200:
                JsonObject = respon.json()
                res = [{'id':i['id'],'name':i['name']} for i in JsonObject]
        except Exception as eproject:
            err_msg = 'Error while fetching releases from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res

    def get_cycle_phases(self,filePath):
        res = {}
        try:
            # get all cycles, phases
            releaseid = filePath["releaseId"]
            self.release_id = releaseid
            relative_path = "/cycle/release/"+str(releaseid)
            respon = requests.get(self.zephyrURL+relative_path, headers = self.headers,proxies = readconfig.proxies, verify = self.send_tls_security())
            if respon.status_code == 200:
                JsonObject = respon.json()
                for cycle in JsonObject:
                    cyclename = cycle["name"]
                    for phase in cycle["cyclePhases"]:
                        phaseObj={}
                        if cyclename in res.keys():
                            phaseObj[phase["tcrCatalogTreeId"]] = phase["name"]
                            res[cyclename].append(phaseObj)
                        else:
                            phaseObj[phase["tcrCatalogTreeId"]] = phase["name"]
                            res[cyclename] = [phaseObj]
        except Exception as eproject:
            err_msg = 'Error while fetching cycles from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res

    def get_mapped_cycle_phases(self,filePath):
        res = {}
        try:
            # get all cycles, phases
            releaseid = filePath["releaseId"]
            self.release_id = releaseid
            mappedPhases = filePath["mappedPhases"]
            relative_path = "/cycle/release/"+str(releaseid)
            respon = requests.get(self.zephyrURL+relative_path, headers = self.headers,proxies = readconfig.proxies, verify = self.send_tls_security())
            if respon.status_code == 200:
                JsonObject = respon.json()
                # Loop through and get cycle, phase and testcases(fetch using API)
                res = {} # {"cyclename":[{"id":"phase1"}]}
                phaseObj = {}
                for cycle in JsonObject:
                    for phase in cycle["cyclePhases"]:
                        if phase["id"] in mappedPhases:
                            phaseObj={}
                            phaseObj[phase["tcrCatalogTreeId"]] = phase["name"]
                            phaseObj["phaseid"] = phase["id"]
                            if cycle["name"] in res.keys(): res[cycle["name"]].append(phaseObj)
                            else: res[cycle["name"]] = [phaseObj]
        except Exception as eproject:
            err_msg = 'Error while fetching cycles, phases from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res

    def get_modules(self,parentFetchList,mods=[]):
        try:
            for parid in parentFetchList:
                relative_path = "/testcasetree/"+str(parid)
                respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
                if respon.status_code == 200:
                    JsonObject = respon.json()
                    if "categories" in JsonObject and len(JsonObject["categories"]) != 0:
                        fp = {}
                        for modul in JsonObject["categories"]:
                            mods.append({
                                "parid":modul["id"],
                                "treeid":parentFetchList[parid]
                            })
                            fp[modul["id"]] = parentFetchList[parid]
                        mods = self.get_modules(fp, mods)
        except Exception as eproject:
            err_msg = 'Error while fetching modules from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return mods

    def get_testcases(self,filePath):
        res = {"modules" : [],"testcases": []}
        updateflag = False
        try:
            # get all testcases
            treeid = filePath["treeId"]
            if "updateflag" in filePath: updateflag = filePath["updateflag"]
            relative_path = "/testcasetree?type=Module&releaseid="+str(self.release_id)+"&revisionid=&parentid="+str(treeid)+"&isShared="
            respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
            if respon.status_code == 200:
                JsonObject = respon.json()
                if len(JsonObject) != 0:
                    for i in range(len(JsonObject)):
                        phaseObj = {JsonObject[i]["id"]:JsonObject[i]["name"]}
                        res["modules"].append(phaseObj)
                        if updateflag: 
                            res["testcases"] = self.get_testcases_treeid(JsonObject[i]["id"], res["testcases"])
                if updateflag: res["parentids"] = self.get_modules(filePath["parentFetchList"],[])
            relative_path = "/testcase/planning/"+str(treeid)+"?pagesize=0&isascorder=true"
            respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())

            if respon.status_code == 500:
                relative_path = "/testcase/planning/"+str(treeid)+"?offset=0&pagesize=1&order=&isascorder=true&tcname="
                respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
                
            if respon.status_code == 200:
                JsonObject = respon.json()
                # Fetch testcases
                if JsonObject["resultSize"] != 0:
                    results = JsonObject["results"]
                    # Fetch requirement details of testcases
                    for i in results:
                        if 'rts' in i:
                            name_err = False
                            if 'tcrTreeTestcase' in i['rts'] and 'testcase' in i['rts']['tcrTreeTestcase'] and 'requirementIds' in i['rts']['tcrTreeTestcase']['testcase']:
                                req_id = i['rts']['tcrTreeTestcase']['testcase']['requirementIds']
                            else:
                                req_id = i['testcase']['requirementIds']
                            requirement_details = self.get_requirement_details(req_id)
                            tc = {
                                'id': i['rts']['tcrTreeTestcase']['testcase']['testcaseId'] if 'tcrTreeTestcase' in i['rts'] and 'testcase' in i['rts']['tcrTreeTestcase'] and 'testcaseId' in i['rts']['tcrTreeTestcase']['testcase'] else i['testcase']['testcaseId'],
                                'cyclePhaseId': i['rts']['cyclePhaseId'],
                                'parentId': treeid,
                                'reqdetails': requirement_details,
                            }
                            try:
                                tc['name'] = i['rts']['tcrTreeTestcase']['testcase']['name'] if 'tcrTreeTestcase' in i['rts'] and 'testcase' in i['rts']['tcrTreeTestcase'] and 'name' in i['rts']['tcrTreeTestcase']['testcase'] else i['testcase']['name']
                            except Exception as excname:
                                name_err = True
                                err_msg = 'Due to no name, Zephyr Testcase with id:'+str(tc['id'])+'  was not displayed.'
                                log.error(err_msg)
                                logger.print_on_console(err_msg)
                                log.error(excname, exc_info=True)
                            if not name_err: res["testcases"].append(tc)
        except Exception as eproject:
            err_msg = 'Error while fetching testcases from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res

    def get_testcases_treeid(self, treeid, tests):
        try:
            relative_path = "/testcasetree?type=Module&releaseid="+str(self.release_id)+"&revisionid=&parentid="+str(treeid)+"&isShared="
            respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
            if respon.status_code == 200:
                JsonObject = respon.json()
                if len(JsonObject) != 0:
                    for i in range(len(JsonObject)):
                        self.get_testcases_treeid(JsonObject[i]["id"], tests)
            relative_path = "/testcase/planning/"+str(treeid)+"?pagesize=0&isascorder=true"
            respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
            if respon.status_code == 200:
                JsonObject = respon.json()
                # Fetch testcases
                if JsonObject["resultSize"] != 0:
                    results = JsonObject["results"]
                    # Fetch requirement details of testcases
                    for i in results:
                        if 'rts' in i:
                            name_err = False
                            req_id = i['testcase']['requirementIds']
                            requirement_details = self.get_requirement_details(req_id)
                            tc = {
                                'id':i['testcase']['testcaseId'],
                                'cyclePhaseId': i['rts']['cyclePhaseId'],
                                'parentId': treeid,
                                'reqdetails': requirement_details,
                            }
                            try:
                                tc['name']=i['testcase']['name']
                            except Exception as excname:
                                name_err = True
                                err_msg = 'Due to no name, Zephyr Testcase with id:'+str(tc['id'])+'  was not displayed.'
                                log.error(err_msg)
                                logger.print_on_console(err_msg)
                                log.error(excname, exc_info=True)
                            if not name_err: tests.append(tc)
        except Exception as eproject:
            err_msg = 'Error while fetching testcases from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return tests

    def get_mapped_testcases(self,filePath):
        res = {"modules" : [],"testcases": []}
        try:
            # get all testcases
            treeid = filePath["treeId"]
            mappedTests = filePath["mappedTests"]
            relative_path = "/testcasetree?type=Module&releaseid="+str(self.release_id)+"&revisionid=&parentid="+str(treeid)+"&isShared="
            respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
            if respon.status_code == 200:
                JsonObject = respon.json()
                if len(JsonObject) != 0:
                    for i in range(len(JsonObject)):
                        phaseObj = {JsonObject[i]["id"]:JsonObject[i]["name"]}
                        res["modules"].append(phaseObj)
            relative_path = "/testcase/planning/"+str(treeid)+"?pagesize=0&isascorder=true"
            respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
            if respon.status_code == 200:
                JsonObject = respon.json()
                # Fetch testcases
                if JsonObject["resultSize"] != 0:
                    results = JsonObject["results"]
                    # Fetch requirement details of testcases
                    for i in results:
                        if 'rts' in i:
                            name_err = False
                            req_id = i['testcase']['requirementIds']
                            requirement_details = self.get_requirement_details(req_id)
                            if int(i['testcase']['testcaseId']) in mappedTests or str(i['testcase']['testcaseId']) in mappedTests:
                                tc = {
                                    'id':i['testcase']['testcaseId'],
                                    'cyclePhaseId': i['rts']['cyclePhaseId'],
                                    'parentId': treeid,
                                    'reqdetails': requirement_details
                                }
                                try:
                                    tc['name']=i['testcase']['name']
                                except Exception as excname:
                                    name_err = True
                                    err_msg = 'Due to no name, Zephyr Testcase with id:'+str(tc['id'])+'  was not displayed.'
                                    log.error(err_msg)
                                    logger.print_on_console(err_msg)
                                    log.error(excname, exc_info=True)
                                if not name_err: res["testcases"].append(tc)
        except Exception as eproject:
            err_msg = 'Error while fetching testcases from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res

    def update_zephyr_test_details(self,data):
        status = False
        try:
            if(self.zephyrURL == None) :
                zephyrLoginLoad = {}
                zephyrLoginLoad["zephyrUserName"] = data['zephyr_username']
                zephyrLoginLoad["zephyrPassword"] = data['zephyr_password']
                zephyrLoginLoad["zephyrURL"] = data['zephyr_url']
                zephyrLoginLoad["zephyrApiToken"] = data['zephyr_apitoken']
                zephyrLoginLoad["authtype"] = data['zephyr_authtype']
                zephyrPayload = {"zephyrPayload":zephyrLoginLoad}
                self.login(zephyrPayload)
            # get schedule
            cyclephaseid = data["treeid"]
            releaseid = data["releaseid"]
            testcaseid = data["testid"]
            status_tc = data["status"]
            parentid = data["parentid"]
            selection_type = data["selectiontype"]
            if selection_type != "Release":
                projectid = data["projectId"][0]
                releaseid_latest = self.get_latest_release(projectid)
                cyclephaseid_latest = self.get_latest_cycle_phases(self.release_id)
                releaseid = [releaseid_latest for i in range(len(releaseid))]
                cyclephaseid = [cyclephaseid_latest for i in range(len(cyclephaseid))]
                parentid = ['-1' for i in range(len(parentid))]
            for index in range(len(cyclephaseid)):
                if parentid[index]=='-1':
                    relative_path = "/execution/user/project?cyclephaseid="+str(cyclephaseid[index])+"&releaseid="+str(releaseid[index])
                else:
                    relative_path = "/execution?parentid="+str(parentid[index])+"&cyclephaseid="+str(cyclephaseid[index])+"&releaseid="+str(releaseid[index])+"&pagesize=0&isascorder=true"
                # relative_path = "/execution/user/project?cyclephaseid="+str(cyclephaseid)+"&releaseid="+str(releaseid)
                respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
                if respon.status_code == 200:
                    JsonObject = respon.json()
                    if JsonObject["resultSize"] != 0:
                        # default userid of Anyone
                        testerid = -10 
                        user_url = self.baseURL + "/flex/services/rest/v3/user"
                        list_user = requests.get(user_url, headers = self.headers, verify = self.send_tls_security())
                        if list_user.status_code == 200:
                            users_json = list_user.json()
                            for obj in users_json:
                                if obj['fullName'] == "Avo Assure":
                                    testerid = obj["id"]
                        results = JsonObject["results"]
                        result = [i for i in results if str(i["tcrTreeTestcase"]["testcase"]["testcaseId"])==str(testcaseid[index])]
                        scheduleid = result[0]["id"]
                        # testerid = result[0]["testerId"]
                        relative_path_update = "/execution/bulk?scheduleids="+str(scheduleid)+"&status="+str(status_tc)+"&testerid="+str(testerid)+"&tcrCatalogTreeId=&allExecutions=&includeanyoneuser="
                        
                        execution_path_update = self.baseURL + "/flex/services/rest/v3/execution/" + str(scheduleid) + "?status="+str(status_tc)+"&testerid="+str(testerid)+"&allExecutions=false&includeanyoneuser=true"
                        ids = []
                        ids.append(scheduleid)
                        data1 = {"ids":ids, "selectedAll":1, "serachView": "false", "teststepUpdate": "false"}
                        # response = requests.put(self.zephyrURL+relative_path_update , headers = self.headers, json = data1 ,proxies = readconfig.proxies, verify = self.send_tls_security())
                        response = requests.put(execution_path_update , headers = self.headers, json = data1 ,proxies = readconfig.proxies, verify = self.send_tls_security())
                        if response.status_code == 200:
                            status = True
        except Exception as e:
            err_msg = 'Error while updating data in Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(e, exc_info=True)
        return status

    def get_requirement_details(self,requirementid):
        res = []
        requirement_list = {}
        try:
            if len(requirementid) >=1:
                for i in requirementid:
                    relative_path = "/requirement/"+str(i)
                    respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
                    if respon.status_code == 200:
                        JsonObject = respon.json()
                        # Fetch requirement details
                        if JsonObject != 0:
                            results = JsonObject
                            requirement_list = {'reqid':results['id'],'reqname':results['name'],'reqdescription': results['details'],'reqcreationdate' : results['reqCreationDate']}
                            req_details_copy = requirement_list.copy()
                            res.append(req_details_copy)
        except Exception as eproject:
            err_msg = 'Error while fetching requirement details from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res

    def send_tls_security(self):
        try:
            tls_security = readconfig.configvalues.get("tls_security")
            if tls_security != None and tls_security.lower() == "low":
                # Make a GET request without SSL certificate verification (not recommended)
                return False
            else:
                # Make a GET request with SSL certificate verification
                return True
        except Exception as e:
            log.error(e)
            logger.print_on_console("ERROR:SSLverify flag as False. Disabled TLS Certificate and Hostname Verification.")
            #by default sending false(if this fuction met exception).you can modify this default return and above logger message.
            return False 
        
    def get_project_repository(self, data):
        res = {}
        try:
            # get all cycles, phases
            project_id = data["projectId"]
            repo_id = data["repoId"]
            self.project_id = project_id
            relative_path = "/testcasetree/projectrepository/"+str(project_id)
            response = requests.get(self.zephyrURL+relative_path, headers = self.headers,proxies = readconfig.proxies, verify = self.send_tls_security())
            if response.status_code == 200:
                json_object = response.json()
                for repo in json_object:
                    if repo["id"] == repo_id:
                        repo_name = repo["name"]
                        for category in repo["categories"]:
                            repo_obj={}
                            if repo_name in res.keys():
                                repo_obj[category["id"]] = category["name"]
                                res[repo_name].append(repo_obj)
                            else:
                                repo_obj[category["id"]] = category["name"]
                                res[repo_name] = [repo_obj]
        except Exception as eproject:
            err_msg = 'Error while fetching cycles from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res
    
    def get_all_repos(self, data):
        res = []
        try:
            # get all repo
            project_id = data["projectId"]
            self.project_id = project_id
            relative_path = "/testcasetree/projectrepository/"+str(project_id)
            response = requests.get(self.zephyrURL+relative_path, headers = self.headers,proxies = readconfig.proxies, verify = self.send_tls_security())
            if response.status_code == 200:
                json_object = response.json()
                res = [{'id':i['id'],'name':i['name']} for i in json_object]
        except Exception as eproject:
            err_msg = 'Error while fetching releases from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res
    
    def get_repo_testcases(self, data):
        res = {"modules" : [],"testcases": [], "release": 0, "cycle": 0}
        try:
            # get all testcases
            tree_id = data["treeId"]
            relative_path = "/testcasetree?type=Module&releaseid=&revisionid=&parentid="+str(tree_id)+"&isShared="
            response = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
            if response.status_code == 200:
                json_object = response.json()
                if len(json_object) != 0:
                    for i in range(len(json_object)):
                        phase_obj = {json_object[i]["id"]:json_object[i]["name"]}
                        res["modules"].append(phase_obj)

            relative_path = "/testcase/tree/"+str(tree_id)+"?pagesize=0&isascorder=true"
            response = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
                
            if response.status_code == 200:
                josn_object = response.json()
                # Fetch testcases
                if josn_object["resultSize"] != 0:
                    results = josn_object["results"]
                    # Fetch requirement details of testcases
                    for i in results:
                        name_err = False
                        if 'testcase' in i and 'requirementIds' in i['testcase']:
                            req_id = i['testcase']['requirementIds']
                        else:
                            req_id = ""
                        requirement_details = self.get_requirement_details(req_id)
                        tc = {
                            'id': i['testcase']['testcaseId'],
                            'cyclePhaseId': i['testcase']['testcaseId'],
                            'parentId': tree_id,
                            'reqdetails': requirement_details,
                        }
                        try:
                            tc['name'] = i['testcase']['name']
                        except Exception as excname:
                            name_err = True
                            err_msg = 'Due to no name, Zephyr Testcase with id:'+str(tc['id'])+'  was not displayed.'
                            log.error(err_msg)
                            logger.print_on_console(err_msg)
                            log.error(excname, exc_info=True)
                        if not name_err: res["testcases"].append(tc)
        except Exception as eproject:
            err_msg = 'Error while fetching testcases from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res
    
    def get_latest_release(self, project_id):
        res = 0
        try:
            relative_path = "/release/project/"+str(project_id)
            respon = requests.get(self.zephyrURL+relative_path, headers = self.headers, proxies = readconfig.proxies, verify = self.send_tls_security())
            if respon.status_code == 200:
                JsonObject = respon.json()
                result = [i['id'] for i in JsonObject]
                res = max(result)
                self.release_id = res
        except Exception as eproject:
            err_msg = 'Error while fetching releases from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res
    
    def get_latest_cycle_phases(self, release_id):
        res = 0
        try:
            relative_path = "/cycle/release/"+str(release_id)
            respon = requests.get(self.zephyrURL+relative_path, headers = self.headers,proxies = readconfig.proxies, verify = self.send_tls_security())
            if respon.status_code == 200:
                JsonObject = respon.json()
                for cycle in JsonObject:
                    cyclename = cycle["name"]
                    for phase in cycle["cyclePhases"]:
                        if res < phase["id"]:
                            res = phase["id"]
        except Exception as eproject:
            err_msg = 'Error while fetching cycles from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res