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
import time


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
            
    def modify_data(self,input_data, parent_name=""):
        modified_data = []
        for item in input_data:
            current_name = f"{parent_name}/{item['name']}" if parent_name else item['name']
            modified_data.append({"id": item["id"], "name": current_name})

            if item["hasChildren"] and "children" in item and len(item["children"])>0 :
                modified_data.extend(self.modify_data(item["children"], current_name))

        return modified_data        

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
            area_url = f'{org_url}/{project_name}/_apis/wit/classificationnodes/areas?$depth=100&api-version=6.1'
            iteration_url = f'{org_url}/{project_name}/_apis/wit/classificationnodes/iterations?$depth=100&api-version=6.1'

            response_area = requests.get(area_url, headers=headers)
            if response_area.status_code == 200:
                data_area = response_area.json()
                if 'children' in data_area and len(data_area['children']) > 0:
                  area_paths.append({'id':data_area['id'],'name':data_area['name']})  
                  for node in data_area['children']:
                    grandparent_name = f"{data_area['name']}/{node['name']}"  
                    area_paths.append({'id':node['id'],'name':grandparent_name})    
                    if node['hasChildren'] and "children" in node and len(node["children"])>0 :
                        child_data = self.modify_data(node["children"], grandparent_name)
                        area_paths.extend(child_data)
                elif 'id' in data_area and 'name' in data_area:
                    area_paths.append({'id':data_area['id'],'name':data_area['name']})         

            response_iteration = requests.get(iteration_url, headers=headers)
            if response_iteration.status_code == 200:
                data_iteration = response_iteration.json()
                if 'children' in data_iteration and len(data_iteration['children']) > 0:
                  iteration_paths.append({'id':data_iteration['id'],'name':data_iteration['name']})  
                  for node in data_iteration['children']:
                    grandparent_name = f"{data_iteration['name']}/{node['name']}"  
                    iteration_paths.append({'id':node['id'],'name':grandparent_name})    
                    if node['hasChildren'] and "children" in node and len(node["children"])>0 :
                        child_data = self.modify_data(node["children"], grandparent_name)
                        iteration_paths.extend(child_data)
                elif 'id' in data_iteration and 'name' in data_iteration:
                    iteration_paths.append({'id':data_iteration['id'],'name':data_iteration['name']})             


            endpoint_url = f'{org_url}/{project_name}/_apis/wit/workitemtypes/{issue_type}/fields?$expand=all&api-version=7.0'

            
            # get projects
            respon = requests.get(url=endpoint_url, headers=headers)

            required_comp = {}
            if respon.status_code == 200:
                JsonObject = respon.json()
                for details in JsonObject['value']:
                    if details['name'] == 'State':
                        details['allowedValues'] = []
                        details['allowedValues'].append(details['defaultValue'])
                    required_comp[details['name']] = details
                required_comp['Area_Paths'] = {'name':data_area['name'] or '','child':area_paths}
                required_comp['Iteration_Paths'] = {'name':data_iteration['name'] or '','child':iteration_paths}
            if respon.status_code == 404:
                required_comp['Error']={'status':404,'msg':'project not found'}
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
                socket.emit('Azure_details','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('Azure_details','Invalid Credentials')
            else:
                socket.emit('Azure_details','Fail')
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
            skip_value = azure_input_dict['skip']
            endpoint_url = f'{org_url}/{project_name}/_apis/wit/wiql?api-version=6.1'

            # WIQL query to fetch all user stories
            wiql_query = f"SELECT * FROM WorkItems WHERE [System.WorkItemType] = 'User Story' AND [System.TeamProject] = '{project_name}' ORDER BY [System.CreatedDate] DESC"

            # Request body with WIQL query
            body = {
                'query': wiql_query
            }
            
            retry_limit = 5
            retry_counter = 0
            while retry_counter < retry_limit:
                try:
                    # Send request to API endpoint
                    respon = requests.post(endpoint_url, headers=headers, json=body)
                    if respon.status_code != 200:
                        log.info("Unable to connect to server retrying Status code is: %s",
                            respon.status_code)
                        logger.print_on_console("Connection error occurred with:"+ endpoint_url)
                        time.sleep(2)
                    else:
                        break
                
                except Exception as e:
                    log.error(e)
                    logger.print_on_console("Unable to connect to server retrying.")
                    time.sleep(2)
                retry_counter += 1
            if retry_counter == retry_limit:
                logger.print_on_console("Maximum retry limit reached. Unable to connect to the server.")

            if respon.status_code == 200:
                JsonObject = respon.json()
                total_count = len(JsonObject['workItems'])
                if len(JsonObject)>0:
                    ids = ''
                    list_count = 0
                    start_index = skip_value
                    end_index = start_index + 100
                    my_list = []
                    for details in JsonObject['workItems'][start_index:end_index]:
                        if list_count >= 100:
                            break
                        ids += str(details['id'])
                        my_list.append(str(details['id']))
                        
                        ids += ','
                        list_count += 1
                        
                # call api to fetch name of user stories
                ids = ids[:-1]
                # Using list comprehension and join()
                flat_string = ','.join([str(num) for num in my_list])

                # Using map() and join()
                flat_string = ','.join(map(str, my_list))
                # maximum limit of API response data  200
                endpoint_url = f'{org_url}/{project_name}/_apis/wit/workitems?ids={flat_string}&api-version=7.0'
                
                retry_limit = 5
                retry_counter = 0
                while retry_counter < retry_limit:
                    try:
                        # Send request to API endpoint
                        respon = requests.get(endpoint_url, headers=headers)
                        if respon.status_code != 200:
                            log.info("Unable to connect to server retrying. Status code is: %s",
                                respon.status_code)
                            logger.print_on_console("Connection error occurred with:"+ endpoint_url)
                            time.sleep(2)
                        else:
                            if respon.status_code == 200:
                                JsonObject = respon.json()
                                if len(JsonObject)>0:
                                    res = {}
                                    res['userStories'] = JsonObject['value']
                                    res['total_count'] = total_count
                            break
                    
                    except Exception as e:
                        log.error(e)
                        logger.print_on_console("Unable to connect to server retrying.")
                        time.sleep(2)
                    retry_counter += 1
                if retry_counter == retry_limit:
                    logger.print_on_console("Maximum retry limit reached. Unable to connect to the server.")

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
            elif 'Max retries exceeded' in str(e):
                socket.emit('auto_populate','Max retries exceeded')    
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
                    inputs = {
                        'workItem':details['workItem'],
                        'points': [i['id'] for i in details['pointAssignments']]
                    }
                    res['testcases'].append(inputs)

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
            userstory_id = azure_input_dict['mappedId'] if 'mappedId' in azure_input_dict else ''
            type='Bug'
            endpoint_url = f'{org_url}/{project_name}/_apis/wit/workitems/${type}?api-version=6.0'

            # Document creation for creating the bug
            patch_document = []
            for key,value in azure_input_dict['info']['chosenList'].items():
                data = ""
                if isinstance(value['data'], dict):
                    data = value['data']['text']
                elif 'name' in value and (value['name'] == 'Area Path' or value['name'] == 'Iteration Path'):
                    convert_str = value['data'].replace("/","\\")
                    # if(project_name != convert_str):
                    #    data = f'{project_name}\\' + convert_str
                    # else:
                    data = convert_str   
                elif 'name' in value and value['name'] == "Failed Retest" and value['data'].isdigit():
                    convert_num = int(value['data'])
                    data =  convert_num      
                else:
                    data = value['data']

                if 'name' in value and value['name'] == 'Repro Steps':
                    data = azure_input_dict['info']['reproSteps']['value']
                if 'url' in value:        
                    patch_document.append(
                        {
                            "op": "add",
                            # "path": "/fields/System.Title",
                            "path": "/fields" + value['url'].split('fields',1)[1],
                            "value": data
                        }
                    )
            if 'mappedId' in azure_input_dict:
                patch_document.append(
                        {
                            'op': 'add',
                            'path': '/relations/-',
                            'value': {
                                'rel': 'System.LinkTypes.Hierarchy-Reverse',
                                'url': f'{org_url}/{project_name}/_apis/wit/workitems/{userstory_id}',
                                'attributes': {
                                    'comment': 'Relates to'
                                }
                            }
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

    def update_azure_test_details(self,azure_input_dict):
        """
            Method to update executed test details to Azure (Azure Execution)
        """
        try:
            pat = azure_input_dict['azurepat']
            testplan_id = azure_input_dict['mapping_details']['TestPlanId']
            testsuite_id = azure_input_dict['mapping_details']['TestSuiteId']
            testpoint_id = azure_input_dict['mapping_details']['TestPoints']
            test_status = azure_input_dict['status'] 
            org_url = azure_input_dict['azureBaseUrl']

            testpoint_id_flat_string = ','.join([str(num) for num in testpoint_id])

                        
            authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
            headers = {
                            'Accept': 'application/json',
                            'Authorization': 'Basic '+authorization
                        }
            #finding user details before update
            # org_name = azure_input_dict['azureOrgname']
            users_endpoint = f'{org_url}/_apis/connectionData?connectOptions=includeServices&api-version=7.1-preview.1'
                        
            user_respon = requests.get(users_endpoint, headers=headers)
            if user_respon.status_code == 200:
                user_json = user_respon.json()

            # Azure DevOps organization URL
            project_name = azure_input_dict['mapping_details']['projectName']
            endpoint_url = f'{org_url}/{project_name}/_apis/test/Plans/{testplan_id}/Suites/{testsuite_id}/points/{testpoint_id_flat_string}?api-version=7.0'
            payload = {
                    "outcome":test_status,
                    "tester":{
                        "id":user_json['authenticatedUser']['id'],
                        "displayName":user_json['authenticatedUser']['customDisplayName'] if 'customDisplayName' in user_json['authenticatedUser'] and user_json['authenticatedUser']['customDisplayName'] else user_json['authenticatedUser']['providerDisplayName']
                        # "displayName":user_json['authenticatedUser']['customDisplayName']
                    }
                    }
            # Send request to API endpoint
            respon = requests.patch(endpoint_url,json=payload, headers=headers)
            if respon.status_code == 200:
                logger.print_on_console(' azure devops test details updated successfully')
                return 1
            elif respon.status_code == 400:
                logger.print_on_console('Bad Request')
                return 0
            elif respon.status_code == 401:
                logger.print_on_console('Unauthorized user')
                return 0
            elif respon.status_code == 403:
                logger.print_on_console('user does not have the necessary permissions to access')
                return 0
            elif respon.status_code == 404 :
                logger.print_on_console('Source not found')
                return 0
            elif respon.status_code == 500 :
                logger.print_on_console('Internal Server Error')
                return 0
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                log.error('Invalid URL')
            elif 'Unauthorized' in str(e):
                log.error('Invalid Credentials')
            else:
                log.error(e,' Fail')
            logger.print_on_console('Exception in updating test details in azure')
            return 0