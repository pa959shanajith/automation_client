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
log = logging.getLogger("testrail.py")
class testrailWindow():
    def __init__(self):
        self.testrail_dict = {
            'getProjects': self.getProjects,
            'getSuites' : self.getSuites,
            'getTestCases':self.getTestCases,
            'getTestPlansAndRuns':self.getTestPlansAndRuns,
            'getSuiteAndRunInfo':self.getSuiteAndRunInfo,
            'getSections':self.getSections,
            'updateResult':self.updateResult
        }
        self.baseUrl = None
        self.testrailUsername = None
        self.testrailApiToken = None
        self.verify_flag = False
        self.proxies = None
        if readconfig.proxies:
            self.proxies = readconfig.proxies
            self.verify_flag = True
        
    def getProjects(self,data):
        try:
            # Set your TestRail base URL, username, and API key
            base_url = data['baseUrl']
            username =  data['testrailUsername']
            api_key = data['testrailApiToken']
            self.baseUrl = data['baseUrl']
            self.testrailUsername = data['testrailUsername']
            self.testrailApiToken = data['testrailApiToken']
            # Construct the API endpoint for getting projects
            endpoint = "/index.php?/api/v2/get_projects"
 
            # Make the GET request
            url = f"{base_url}{endpoint}"
            headers = {"Content-Type": "application/json"}
            auth = (username, api_key)
            
            response = requests.get(url, headers=headers, auth=auth, verify = self.verify_flag, proxies = self.proxies)
            
            # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                projects = response.json()
                log.info(projects)
                return projects
            elif response.status_code == 429:
                return 'API rate limit exceeded'
            elif response.status_code == 401:
                return 'Invalid Credentials'
            else:
                return 'failed to fetch data from testrail'
        except Exception as e:
            return e
        
    def getSuites(self,data):
        res = "invalidcredentials"
        try:
            # Construct the API endpoint for getting suites
            endpoint = f"/index.php?/api/v2/get_suites/{data['projectId']}"
           
            # Make the GET requestcls
            url = f"{self.baseUrl}{endpoint}"
            headers = {"Content-Type": "application/json"}
            auth = (self.testrailUsername, self.testrailApiToken)
            
            response = requests.get(url, headers=headers, auth=auth, verify = self.verify_flag, proxies = self.proxies)
            
            # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                suites = response.json()
                log.info(suites)
                if len(suites) == 0:
                    return []
                else :
                    return suites
            elif response.status_code == 429:
                return 'API rate limit exceeded'
            elif response.status_code == 401:
                return 'Invalid Credentials'
            else:
                return 'failed to fetch data from testrail'
        except Exception as e:
            return 'error'
        
    
    def getTestCases(self,data):
        res = "invalidcredentials"
        try:
            endpoint = f"/index.php?/api/v2/get_cases/{data['projectId']}&suite_id={data['suiteId']}&section_id={data['sectionId']}"
            # Construct the API endpoint for getting testcases on the basis of request.
            url = f"{self.baseUrl}{endpoint}"
            headers = {"Content-Type": "application/json"}
            auth = (self.testrailUsername, self.testrailApiToken)
                # # requesting testrail for getting the testcases
            response = requests.get(url, headers=headers, auth=auth, verify = self.verify_flag, proxies = self.proxies)
                
            # # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                testcases = response.json()
                log.info(testcases['cases'])
                if len(testcases['cases']) == 0:
                    return [{'section_id':data['sectionId'],'message': []}]
                else:
                    return [{'section_id':data['sectionId'],'message': testcases['cases']}]
            elif response.status_code == 429:
                return [{'section_id':data['sectionId'],'message':'API rate limit exceeded'}]
            elif response.status_code == 401:
                return [{'section_id':data['sectionId'],'message':'Invalid Credentials'}]
            else:
                return [{'section_id':data['sectionId'],'message':'failed to fetch data from testrail'}]
                
        
        except Exception as e:
            return [{'section_id':data['sectionId'],'message':'error'}]
        
    
    def getTestPlansAndRuns(self,data):
        res = "invalidcredentials"
        try:
            plans = []
            runs = []
            
            # Construct the API endpoint for getting testcases on the basis of request
            endpoint = f"/index.php?/api/v2/get_plans/{data['projectId']}"
            testPlansUrl = f"{self.baseUrl}{endpoint}"
            headers = {"Content-Type": "application/json"}
            testRunsUrl = f"{self.baseUrl}/index.php?/api/v2/get_runs/{data['projectId']}"
            auth = (self.testrailUsername, self.testrailApiToken)
            # # requesting testrail for getting the testplans
            testPlans = requests.get(testPlansUrl, headers=headers, auth=auth, verify = self.verify_flag, proxies = self.proxies)
             # Check if the request was successful (HTTP status code 200)
            if testPlans.status_code == 200:
                response = testPlans.json()
                log.info(response)
                plans = response['plans']
            
            testRuns =  requests.get(testRunsUrl, headers=headers, auth=auth)
            if testRuns.status_code == 200:
                response = testRuns.json()
                log.info(response)
                runs = response['runs']
            elif testPlans.status_code == 429 or testRuns.status_code == 429:
                return 'API rate limit exceeded'
            elif testPlans.status_code == 401 or testRuns.status_code == 429:
                return 'Invalid Credentials'
            else:
                return 'failed to fetch data from testrail'
            
            return {'testPlans':plans,'testRuns':runs}
        except Exception as e:
            return 'error'
        
    def getSuiteAndRunInfo(self,data):
        res = "invalidcredentials"
        try:
            # Construct the API endpoint for getting testcases on the basis of request
            endpoint = f"/index.php?/api/v2/get_plan/{data['testPlanId']}"
            url = f"{self.baseUrl}{endpoint}"
            headers = {"Content-Type": "application/json"}
            auth = (self.testrailUsername, self.testrailApiToken)
            # # requesting testrail for getting the testcases
            response = requests.get(url, headers=headers, auth=auth, verify = self.verify_flag, proxies = self.proxies)
                
             # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                testSuiteandRuns = response.json()
                log.info(testSuiteandRuns)
                return testSuiteandRuns
            elif response.status_code == 429:
                return 'API rate limit exceeded'
            elif response.status_code == 401:
                return 'Invalid Credentials'
            else:
                return 'failed to fetch data from testrail'
        except Exception as e:
            return 'error'
    
    def getSections(self,data):
        res = "invalidcredentials"
        try:
            # Construct the API endpoint for getting testcases on the basis of request
            endpoint = f"/index.php?/api/v2/get_sections/{data['projectId']}&suite_id={data['suiteId']}"
            url = f"{self.baseUrl}{endpoint}"
            headers = {"Content-Type": "application/json"}
            auth = (self.testrailUsername, self.testrailApiToken)
            # # requesting testrail for getting the testcases
            response = requests.get(url, headers=headers, auth=auth, verify = self.verify_flag, proxies = self.proxies)
            
             # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                testSections = response.json()
                log.info(testSections['sections'])
                if len(testSections['sections']) == 0:
                    return [{'suite_id':data['suiteId'],'message':[]}]
                else:
                    return [{'suite_id':data['suiteId'],'message':testSections['sections']}]
            elif response.status_code == 429:
                return [{'suite_id':data['suiteId'],'message':'API rate limit exceeded'}]
            elif response.status_code == 401:
                return [{'suite_id':data['suiteId'],'message':'Invalid Credentials'}]
            else:
                return [{'suite_id':data['suiteId'],'message':'failed to fetch data from testrail'}]
        except Exception as e:
            return 'error'


    def updateResult(self,baseurl,username,apitoken,mappedDetails,status):
        try:
            headers = {"Content-Type": "application/json"}
            auth = (username, apitoken)
            
            request = []
            projectId = mappedDetails[-1]['projectid'][-1]
            
            testPlansUrl = f"{baseurl}/index.php?/api/v2/get_plans/{projectId}"

            testPlans = requests.get(testPlansUrl,headers=headers, auth=auth, verify = self.verify_flag, proxies = self.proxies)

            plans = testPlans.json()['plans']
            
            testPlanId = plans[0]['id']
            
            testRunsUrl =  f"{baseurl}/index.php?/api/v2/get_plan/{testPlanId}"

            testRuns = requests.get(testRunsUrl,headers=headers, auth=auth, verify = self.verify_flag,  proxies = self.proxies)
            
            runs = testRuns.json()['entries']

            allTestRunsUrl = f"{baseurl}/index.php?/api/v2/get_runs/{projectId}"

            allTestRuns = requests.get(allTestRunsUrl,headers=headers, auth=auth, verify = self.verify_flag,  proxies = self.proxies)

            latestTestRun = allTestRuns.json()['runs'][0]
            
            testRunId = 0

            if latestTestRun['created_on'] > plans[0]['created_on']:
                testRunId = latestTestRun['id']
            else:
                testRunId = runs[-1]['runs'][-1]['id']
            
            endpoint = f"{baseurl}/index.php?/api/v2/add_results_for_cases/{testRunId}"

            successCount = 0

            totalCount = 0
            # constructing the endpoint
            for i in range(len(mappedDetails)):
                for j in range(len(mappedDetails[i]["testid"])):
                    request = [{
                        "case_id":mappedDetails[i]['testid'][j],
                        "status_id":status
                    }]
                    
                    response = requests.post(endpoint, headers=headers, auth=auth,json = {"results":request},verify = self.verify_flag,  proxies = self.proxies)
                    totalCount += 1
                    if response.status_code == 200:
                        successCount += 1
                    
            
            return {'status':1,'successCount':successCount,'totalCount':totalCount}
        except Exception as e:
            return {'status':0}