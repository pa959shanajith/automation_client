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
            'maptestcase': self.get_mapped_testcases
        }
        self.baseURL = None
        self.zephyrURL = None
        self.zephyrUserName = None
        self.zephyrPassword = None
        self.headers = None

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
                respon = requests.get(self.zephyrURL+relative_path, headers=self.headers, proxies=readconfig.proxies)
                if respon.status_code == 200:
                    JsonObject = respon.json()
                    res = [{'id':i['id'],'name':i['name']} for i in JsonObject]
            else:
                self.headers = {'Authorization':'Bearer %s'% zephyrPayload["zephyrApiToken"]}
                respon = requests.get(self.zephyrURL+relative_path, headers=self.headers, proxies=readconfig.proxies)
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
            respon = requests.get(self.zephyrURL+relative_path, headers=self.headers, proxies=readconfig.proxies)
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
            respon = requests.get(self.zephyrURL+relative_path, headers=self.headers, proxies=readconfig.proxies)
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
            relative_path = "/cycle/release/"+str(releaseid)
            respon = requests.get(self.zephyrURL+relative_path, headers=self.headers,proxies=readconfig.proxies)
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
            mappedPhases = filePath["mappedPhases"]
            relative_path = "/cycle/release/"+str(releaseid)
            respon = requests.get(self.zephyrURL+relative_path, headers=self.headers,proxies=readconfig.proxies)
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
                respon = requests.get(self.zephyrURL+relative_path, headers=self.headers, proxies=readconfig.proxies)
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
            relative_path = "/testcasetree/"+str(treeid)
            respon = requests.get(self.zephyrURL+relative_path, headers=self.headers, proxies=readconfig.proxies)
            if respon.status_code == 200:
                JsonObject = respon.json()
                if "categories" in JsonObject and len(JsonObject["categories"]) != 0:
                    for modul in JsonObject["categories"]:
                        phaseObj = {modul["id"]:modul["name"]}
                        res["modules"].append(phaseObj)
                        if updateflag: 
                            res["testcases"] = self.get_testcases_treeid(modul["id"], res["testcases"])
                if updateflag: res["parentids"] = self.get_modules(filePath["parentFetchList"],[])
            relative_path = "/testcase/planning/"+str(treeid)+"?pagesize=0&isascorder=true"
            respon = requests.get(self.zephyrURL+relative_path, headers=self.headers, proxies=readconfig.proxies)
            if respon.status_code == 200:
                JsonObject = respon.json()
                # Fetch testcases
                if JsonObject["resultSize"] != 0:
                    results = JsonObject["results"]
                    # Fetch requirement details of testcases
                    for i in results:
                        if 'rts' in i:
                            req_id = i['testcase']['requirementIds']
                            requirement_details = self.get_requirement_details(req_id)
                            res["testcases"].append({
                                'id':i['testcase']['testcaseId'],
                                'name':i['testcase']['name'],
                                'cyclePhaseId': i['rts']['cyclePhaseId'],
                                'parentId': treeid,
                                'reqdetails': requirement_details,
                            })
        except Exception as eproject:
            err_msg = 'Error while fetching testcases from Zephyr'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(eproject, exc_info=True)
        return res

    def get_testcases_treeid(self, treeid, tests):
        try:
            relative_path = "/testcasetree/"+str(treeid)
            respon = requests.get(self.zephyrURL+relative_path, headers=self.headers, proxies=readconfig.proxies)
            if respon.status_code == 200:
                JsonObject = respon.json()
                if "categories" in JsonObject and len(JsonObject["categories"]) != 0:
                    for modul in JsonObject["categories"]:
                        self.get_testcases_treeid(modul["id"], tests)
            relative_path = "/testcase/planning/"+str(treeid)+"?pagesize=0&isascorder=true"
            respon = requests.get(self.zephyrURL+relative_path, headers=self.headers, proxies=readconfig.proxies)
            if respon.status_code == 200:
                JsonObject = respon.json()
                # Fetch testcases
                if JsonObject["resultSize"] != 0:
                    results = JsonObject["results"]
                    # Fetch requirement details of testcases
                    for i in results:
                        if 'rts' in i:
                            req_id = i['testcase']['requirementIds']
                            requirement_details = self.get_requirement_details(req_id)
                            tests.append({
                                'id':i['testcase']['testcaseId'],
                                'name':i['testcase']['name'],
                                'cyclePhaseId': i['rts']['cyclePhaseId'],
                                'parentId': treeid,
                                'reqdetails': requirement_details,
                            })
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
            relative_path = "/testcasetree/"+str(treeid)
            respon = requests.get(self.zephyrURL+relative_path, headers=self.headers, proxies=readconfig.proxies)
            if respon.status_code == 200:
                JsonObject = respon.json()
                if "categories" in JsonObject and len(JsonObject["categories"]) != 0:
                    for modul in JsonObject["categories"]:
                        phaseObj = {modul["id"]:modul["name"]}
                        res["modules"].append(phaseObj)
            relative_path = "/testcase/planning/"+str(treeid)+"?pagesize=0&isascorder=true"
            respon = requests.get(self.zephyrURL+relative_path, headers=self.headers, proxies=readconfig.proxies)
            if respon.status_code == 200:
                JsonObject = respon.json()
                # Fetch testcases
                if JsonObject["resultSize"] != 0:
                    results = JsonObject["results"]
                    # Fetch requirement details of testcases
                    for i in results:
                        if 'rts' in i:
                            req_id = i['testcase']['requirementIds']
                            requirement_details = self.get_requirement_details(req_id)
                            if int(i['testcase']['testcaseId']) in mappedTests:
                                res["testcases"].append({
                                    'id':i['testcase']['testcaseId'],
                                    'name':i['testcase']['name'],
                                    'cyclePhaseId': i['rts']['cyclePhaseId'],
                                    'parentId': treeid,
                                    'reqdetails': requirement_details
                                })
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
            for index in range(len(cyclephaseid)):
                relative_path = "/execution?parentid="+str(parentid[index])+"&cyclephaseid="+str(cyclephaseid[index])+"&releaseid="+str(releaseid)+"&pagesize=0&isascorder=true"
                # relative_path = "/execution/user/project?cyclephaseid="+str(cyclephaseid)+"&releaseid="+str(releaseid)
                respon = requests.get(self.zephyrURL+relative_path, headers=self.headers, proxies=readconfig.proxies)
                if respon.status_code == 200:
                    JsonObject = respon.json()
                    if JsonObject["resultSize"] != 0:
                        results = JsonObject["results"]
                        result = [i for i in results if str(i["tcrTreeTestcase"]["testcase"]["testcaseId"])==str(testcaseid[index])]
                        scheduleid = result[0]["id"]
                        testerid = result[0]["testerId"]
                        relative_path_update = "/execution/bulk?scheduleids="+str(scheduleid)+"&status="+str(status_tc)+"&testerid="+str(testerid)+"&tcrCatalogTreeId=&allExecutions=&includeanyoneuser="
                        ids = []
                        ids.append(scheduleid)
                        data1 = {"ids":ids, "selectedAll":1, "serachView": "false", "teststepUpdate": "false"}
                        response = requests.put(self.zephyrURL+relative_path_update , headers=self.headers, json=data1 ,proxies=readconfig.proxies)
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
                    respon = requests.get(self.zephyrURL+relative_path, headers=self.headers, proxies=readconfig.proxies)
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