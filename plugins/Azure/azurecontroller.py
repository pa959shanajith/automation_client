#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:
# Copyright:   (c) rakesh.v
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from jira.client import JIRA
import os
import logger
import logging
import requests
from requests.auth import HTTPBasicAuth
import json
log = logging.getLogger("azurecontroller.py")
import base64


class AzureWindow():
    # jira = None
    # def __init__(self,x=0):
    #     self.x = x
    #     self.jira_details=None

    # def connectJIRA(self,jira_serverlocation , jira_uname , jira_pwd ):
    #     try:
    #         jira_options = {'server': jira_serverlocation}
    #         jira = JIRA(options=jira_options,basic_auth=(jira_uname,jira_pwd))
    #         return jira
    #     except Exception as e:
    #         logger.print_on_console("Failed to connect to JIRA")

    def get_all_auto_details(self,azure_input_dict,socket):
        """
            Method to login using the user provided credentials and get projects, issue type lists
            related to user credentials
            returns list of projects, issue type
        """
        data = {}
        projects_list = []
        issue_types = []
        data['projects'] = []
        data['issuetype'] = []
        azure = None

        try:
            #Azure changes
            pat = azure_input_dict['azurepat']
            authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Basic '+authorization
            }
            # Azure DevOps organization URL
            org_url = azure_input_dict['azureBaseUrl']
            endpoint_url = f'{org_url}/_apis/projects?api-version=7.0'

            
            # get projects
            respon = requests.get(url=endpoint_url, headers=headers)

            if respon.status_code == 200:
                JsonObject = respon.json()
                if len(JsonObject)>0:
                    res = {}
                    res['projects']= JsonObject['value']
            # if(';' in org_url):
            #     log.debug('Connecting to JIRA through proxy')
            #     jira_server = jira_input_dict['jira_serverlocation'].split(';')[0]
            #     jira_proxy = jira_input_dict['jira_serverlocation'].split(';')[1]
            #     jira_options = {'server':jira_server,'verify':False}
            #     jira = JIRA(options=jira_options,basic_auth=(jira_input_dict['jira_uname'],jira_input_dict['jira_pwd']),proxies={'http':jira_proxy,'https':jira_proxy})
            # else:
            #     True
            #     # jira_options = {'server': org_url}
            #     # jira = JIRA(options=jira_options,basic_auth=())

            socket.emit('auto_populate',res)
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('auto_populate','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('auto_populate','Invalid Credentials')
            else:
                socket.emit('auto_populate','Fail')
            logger.print_on_console('Exception in login and auto populating data')

    def get_configure_fields(self,azure_input_dict,socket):
        """
            Method to get Configure fields using the user selected project and issue_type
            returns list of Configurable fields
        """
        config_data={}
        inp_project=azure_input_dict['project']
        issue_type=azure_input_dict['issuetype']
        project_key=None
        project_name=None
        data_area=[]
        data_iteration=[]
        area_paths=[]
        iteration_paths=[]
        try:

             #Azure changes
            pat = azure_input_dict['azurepat']
            authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Basic '+authorization
            }
            # Azure DevOps organization URL
            org_url = azure_input_dict['azureBaseUrl']
            project_name = azure_input_dict['project']

            # API endpoint URL for classification nodes
            area_url = f'{org_url}/{project_name}/_apis/wit/classificationnodes/areas?$depth=2&api-version=6.1'
            iteration_url = f'{org_url}/{project_name}/_apis/wit/classificationnodes/iterations?$depth=2&api-version=6.1'

            response_area = requests.get(area_url, headers=headers)
            if response_area.status_code == 200:
                data_area = response_area.json()
                area_paths = [{'id':node['id'],'name':node['name']} for node in data_area['children']]

            response_iteration = requests.get(iteration_url, headers=headers)
            if response_iteration.status_code == 200:
                data_iteration = response_iteration.json()
                iteration_paths = [{'id':node['id'],'name':node['name']} for node in data_iteration['children']]

            endpoint_url = f'{org_url}/{project_name}/_apis/wit/workitemtypes/{issue_type}/fields?$expand=all&api-version=7.0'

            
            # get projects
            respon = requests.get(url=endpoint_url, headers=headers)

            required_comp = {}
            if respon.status_code == 200:
                JsonObject = respon.json()
                for details in JsonObject['value']:
                    # if details['alwaysRequired']:
                    required_comp[details['name']] = details
                required_comp['Area_Paths'] = {'name':data_area['name'] or '','child':area_paths}
                required_comp['Iteration_Paths'] = {'name':data_iteration['name'] or '','child':iteration_paths}

            socket.emit('configure_field',required_comp)
        except Exception as e:
            log.error(e)
            socket.emit('configure_field','Fail')
            logger.print_on_console('Exception in fetching Configure Fields')

    def get_projects(self,azure_input_dict,socket):
        """
            Method to login to Azure and get the projects from Azure (Azure integration screen)
            returns list of projects
        """
        res = "invalidcredentials"
        try:

            #Azure changes
            pat = azure_input_dict['azurepat']
            authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Basic '+authorization
            }
            # Azure DevOps organization URL
            org_url = azure_input_dict['azureBaseUrl']
            endpoint_url = f'{org_url}/_apis/projects?api-version=7.0'

            
            # get projects
            respon = requests.get(url=endpoint_url, headers=headers)

            if respon.status_code == 200:
                JsonObject = respon.json()
                if len(JsonObject)>0:
                    res = {}
                    res['projects']= JsonObject['value']
            # if(';' in org_url):
            #     log.debug('Connecting to JIRA through proxy')
            #     jira_server = jira_input_dict['jira_serverlocation'].split(';')[0]
            #     jira_proxy = jira_input_dict['jira_serverlocation'].split(';')[1]
            #     jira_options = {'server':jira_server,'verify':False}
            #     jira = JIRA(options=jira_options,basic_auth=(jira_input_dict['jira_uname'],jira_input_dict['jira_pwd']),proxies={'http':jira_proxy,'https':jira_proxy})
            # else:
            #     True
            #     # jira_options = {'server': org_url}
            #     # jira = JIRA(options=jira_options,basic_auth=())

            socket.emit('Azure_details',res)
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('auto_populate','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('auto_populate','Invalid Credentials')
            else:
                socket.emit('auto_populate','Fail')
            logger.print_on_console('Exception in login and auto populating projects')

    def get_userstories(self,azure_input_dict,socket):
        """
            Method to login to Azure and get the projects from Azure (Azure integration screen)
            returns list of projects
        """
        res = "invalidcredentials"
        try:

            #Azure changes
            pat = azure_input_dict['azurepat']
            authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Basic '+authorization
            }
            # Azure DevOps organization URL
            org_url = azure_input_dict['azureBaseUrl']
            project_name = azure_input_dict['projectDetails']['name']
            endpoint_url = f'{org_url}/{project_name}/_apis/wit/wiql?api-version=7.0'

            # WIQL query to fetch all user stories
            wiql_query = "SELECT * FROM WorkItems WHERE [System.WorkItemType] = 'User Story' ORDER BY [System.Id]"

            # Request body with WIQL query
            body = {
                'query': wiql_query
            }
            
            # Send request to API endpoint
            respon = requests.post(endpoint_url, headers=headers, json=body)

            if respon.status_code == 200:
                JsonObject = respon.json()
                if len(JsonObject)>0:
                    ids = ''
                    list_count = 0
                    for details in JsonObject['workItems'][::-1]:
                        if list_count >= 100:
                            break
                        ids += str(details['id'])
                        ids += ','
                        list_count += 1

                # call api to fetch name of user stories
                ids = ids[:-1]
                endpoint_url = f'{org_url}/{project_name}/_apis/wit/workitems?ids={ids}&api-version=7.0'

                # Send request to API endpoint
                respon = requests.get(endpoint_url, headers=headers)

                if respon.status_code == 200:
                    JsonObject = respon.json()
                    if len(JsonObject)>0:
                        res = {}
                        res['userStories'] = JsonObject['value']

            # if(';' in org_url):
            #     log.debug('Connecting to JIRA through proxy')
            #     jira_server = jira_input_dict['jira_serverlocation'].split(';')[0]
            #     jira_proxy = jira_input_dict['jira_serverlocation'].split(';')[1]
            #     jira_options = {'server':jira_server,'verify':False}
            #     jira = JIRA(options=jira_options,basic_auth=(jira_input_dict['jira_uname'],jira_input_dict['jira_pwd']),proxies={'http':jira_proxy,'https':jira_proxy})
            # else:
            #     True
            #     # jira_options = {'server': org_url}
            #     # jira = JIRA(options=jira_options,basic_auth=())

            socket.emit('Azure_details',res)
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('auto_populate','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('auto_populate','Invalid Credentials')
            else:
                socket.emit('auto_populate','Fail')
            logger.print_on_console('Exception in login and auto populating projects')

    def get_testplans(self,azure_input_dict,socket):
        """
            Method to login to Azure and get the projects from Azure (Azure integration screen)
            returns list of projects
        """
        res = "invalidcredentials"
        try:

            #Azure changes
            pat = azure_input_dict['azurepat']
            authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Basic '+authorization
            }
            # Azure DevOps organization URL
            org_url = azure_input_dict['azureBaseUrl']
            project_name = azure_input_dict['projectDetails']['name']
            endpoint_url = f'{org_url}/{project_name}/_apis/testplan/plans?api-version=7.0'

            # Send request to API endpoint
            respon = requests.get(endpoint_url, headers=headers)

            if respon.status_code == 200:
                JsonObject = respon.json()
                if len(JsonObject)>0:
                   res = {}
                   res['testplans'] = JsonObject['value']

            # if(';' in org_url):
            #     log.debug('Connecting to JIRA through proxy')
            #     jira_server = jira_input_dict['jira_serverlocation'].split(';')[0]
            #     jira_proxy = jira_input_dict['jira_serverlocation'].split(';')[1]
            #     jira_options = {'server':jira_server,'verify':False}
            #     jira = JIRA(options=jira_options,basic_auth=(jira_input_dict['jira_uname'],jira_input_dict['jira_pwd']),proxies={'http':jira_proxy,'https':jira_proxy})
            # else:
            #     True
            #     # jira_options = {'server': org_url}
            #     # jira = JIRA(options=jira_options,basic_auth=())

            socket.emit('Azure_details',res)
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('auto_populate','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('auto_populate','Invalid Credentials')
            else:
                socket.emit('auto_populate','Fail')
            logger.print_on_console('Exception in login and auto populating projects')

    def get_testsuites(self,azure_input_dict,socket):
        """
            Method to login to Azure and get the projects from Azure (Azure integration screen)
            returns list of projects
        """
        res = "invalidcredentials"
        try:

            #Azure changes
            pat = azure_input_dict['azurepat']
            authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Basic '+authorization
            }
            # Azure DevOps organization URL
            org_url = azure_input_dict['azureBaseUrl']
            project_name = azure_input_dict['projectDetails']['name']
            planId = str(azure_input_dict['testPlanDetails']['id'])
            endpoint_url = f'{org_url}/{project_name}/_apis/testplan/Plans/{planId}/suites?api-version=7.0'

            # Send request to API endpoint
            respon = requests.get(endpoint_url, headers=headers)

            if respon.status_code == 200:
                JsonObject = respon.json()
                if len(JsonObject)>0:
                   res = {}
                   res['testsuites'] = JsonObject['value']

            # if(';' in org_url):
            #     log.debug('Connecting to JIRA through proxy')
            #     jira_server = jira_input_dict['jira_serverlocation'].split(';')[0]
            #     jira_proxy = jira_input_dict['jira_serverlocation'].split(';')[1]
            #     jira_options = {'server':jira_server,'verify':False}
            #     jira = JIRA(options=jira_options,basic_auth=(jira_input_dict['jira_uname'],jira_input_dict['jira_pwd']),proxies={'http':jira_proxy,'https':jira_proxy})
            # else:
            #     True
            #     # jira_options = {'server': org_url}
            #     # jira = JIRA(options=jira_options,basic_auth=())

            socket.emit('Azure_details',res)
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('auto_populate','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('auto_populate','Invalid Credentials')
            else:
                socket.emit('auto_populate','Fail')
            logger.print_on_console('Exception in login and auto populating projects')

    def get_testcases(self,azure_input_dict,socket):
        """
            Method to login to Azure and get the projects from Azure (Azure integration screen)
            returns list of projects
        """
        res = "invalidcredentials"
        try:

            #Azure changes
            pat = azure_input_dict['azurepat']
            authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Basic '+authorization
            }
            # Azure DevOps organization URL
            org_url = azure_input_dict['azureBaseUrl']
            project_name = azure_input_dict['projectDetails']['name']
            planId = str(azure_input_dict['testPlanDetails']['id'])
            suiteId = str(azure_input_dict['testSuiteDetails']['id'])

            endpoint_url = f'{org_url}/{project_name}/_apis/testplan/Plans/{planId}/Suites/{suiteId}/TestCase?api-version=7.0'

            # Send request to API endpoint
            respon = requests.get(endpoint_url, headers=headers)

            if respon.status_code == 200:
                JsonObject = respon.json()
                if len(JsonObject)>0:
                   res = {}
                   res['testcases'] = []
                   for details in JsonObject['value']:
                    res['testcases'].append(details['workItem'])

            # if(';' in org_url):
            #     log.debug('Connecting to JIRA through proxy')
            #     jira_server = jira_input_dict['jira_serverlocation'].split(';')[0]
            #     jira_proxy = jira_input_dict['jira_serverlocation'].split(';')[1]
            #     jira_options = {'server':jira_server,'verify':False}
            #     jira = JIRA(options=jira_options,basic_auth=(jira_input_dict['jira_uname'],jira_input_dict['jira_pwd']),proxies={'http':jira_proxy,'https':jira_proxy})
            # else:
            #     True
            #     # jira_options = {'server': org_url}
            #     # jira = JIRA(options=jira_options,basic_auth=())

            socket.emit('Azure_details',res)
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('auto_populate','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('auto_populate','Invalid Credentials')
            else:
                socket.emit('auto_populate','Fail')
            logger.print_on_console('Exception in login and auto populating projects')

    def get_createWorkItem(self,azure_input_dict,socket):
        """
            Method to login to Azure and get the projects from Azure (Azure integration screen)
            returns list of projects
        """
        res = "Fail"
        try:

            #Azure changes
            pat = azure_input_dict['pat']
            authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json-patch+json',
                'Authorization': 'Basic '+authorization
            }
            # Azure DevOps organization URL
            org_url = azure_input_dict['url']
            project_name = azure_input_dict['info']['project']['text']
            type='Bug'
            endpoint_url = f'{org_url}/{project_name}/_apis/wit/workitems/${type}?api-version=6.0'

            # Document creation for creating the bug
            patch_document = []
            for key,value in azure_input_dict['info']['chosenList'].items():
                data = ""
                if isinstance(value['data'], dict):
                    data = value['data']['text']
                elif value['name'] == 'Area Path' or value['name'] == 'Iteration Path':
                    data = f'{project_name}\\' + value['data']
                else:
                    data = value['data']

                if value['name'] == 'Repro Steps':
                    data = azure_input_dict['info']['reproSteps']['value']
                patch_document.append(
                     {
                        "op": "add",
                        # "path": "/fields/System.Title",
                        "path": "/fields" + value['url'].split('fields',1)[1],
                        "value": data
                    }
                )
            respon = requests.patch(endpoint_url, headers=headers, data=json.dumps(patch_document))

            if respon.status_code == 200:
                res = []
                JsonObject = respon.json()
                if len(JsonObject)>0:
                        bug_id = str(JsonObject['id'])
                        link_to_page = f'{org_url}/{project_name}/_workitems/edit/{bug_id}'
                        res.append(JsonObject['id'])
                        res.append(link_to_page)
                        res=str(res)
                
                logger.print_on_console('Bug created is ',bug_id)


            socket.emit('issue_id',res)
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('auto_populate','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('auto_populate','Invalid Credentials')
            else:
                socket.emit('auto_populate','Fail')
            logger.print_on_console('Exception in login and auto populating projects')
