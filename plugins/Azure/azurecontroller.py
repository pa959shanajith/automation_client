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
    jira = None
    def __init__(self,x=0):
        self.x = x
        self.jira_details=None

    def connectJIRA(self,jira_serverlocation , jira_uname , jira_pwd ):
        try:
            jira_options = {'server': jira_serverlocation}
            jira = JIRA(options=jira_options,basic_auth=(jira_uname,jira_pwd))
            return jira
        except Exception as e:
            logger.print_on_console("Failed to connect to JIRA")

    # def createIssue(self,data,socket):
    #     """
    #         Method to create issue in JIRA
    #         inputs project id , summary , issuetype , description , ConfigureFields(selected)
    #         returns issue id created in JIRA
    #     """
    #     issue_id = None
    #     jira = None
    #     create_issues = None
    #     outwardIssue=None
    #     linkedIssue_Type=None
    #     attachement_path=None
    #     Labels=['AvoAssure']
    #     Execution=data['executionReportNo'].replace(" ","")
    #     Labels.append(Execution)
    #     issue_link=None
    #     try:
    #         username= data['username']
    #         password = data['password']
    #         url = data['url']
    #         self.jira_details = data
    #         if(';' in url):
    #             jira_options = {'server':url.split(';')[0],'verify':False}
    #             jira = JIRA(options=jira_options,basic_auth=(username,password),proxies={'http':url.split(';')[1],'https':url.split(';')[1]})
    #         else:
    #             jira_options = {'server': url}
    #             jira = JIRA(options=jira_options,basic_auth=(username,password))
    #         project_id = data['project']
    #         summary = data['summary']
    #         issue_type = data['issuetype']
    #         parentid=data['parentissue']
    #         flag = False
    #         if all(check1 is not None for check1 in [project_id, summary, issue_type]):
    #             log.debug('Condition passed inside if not none check')
    #             temp_dict={}
    #             for i in data:
    #                 custom_val_dd={'value':''}
    #                 custom_val_tb=None
    #                 if i not in ['project','issuetype','parentissue','reportId','slno','url','username','password','executionId','priority','Attachment','Linked Issues','executionReportNo','mappedItem']:
    #                     if 'userInput' in data[i]:
    #                         if 'key' in data[i]['userInput']:
    #                             if 'customfield' in data[i]['field_name']:
    #                                 custom_val_dd['value']=data[i]['userInput']['text']
    #                                 temp_dict[data[i]['field_name']] = custom_val_dd
    #                                 if data[i]['type']=='array':
    #                                     temp_dict[data[i]['field_name']]=[temp_dict[data[i]['field_name']]]
    #                             else:
    #                                 if data[i]['field_name'].lower()=='priority':
    #                                     temp_dict[data[i]['field_name']] = {'name':data[i]['userInput']['text']}
    #                                 else:
    #                                     if i.lower() == 'labels':
    #                                         Labels.append(data[i]['userInput']['text'])
    #                                         temp_dict[data[i]['field_name']] = Labels
    #                                     else:
    #                                         temp_dict[data[i]['field_name']] = data[i]['userInput']['text']
    #                         else:
    #                             # use below logic is for label text box without suggestion
    #                             # if i.lower() == 'labels':
    #                             #     Labels.append(data[i]['userInput'])
    #                             #     temp_dict[data[i]['field_name']] = Labels
    #                             # else:
    #                             if 'customfield' in data[i]['field_name']:
    #                                 custom_val_tb=data[i]['userInput']
    #                                 temp_dict[data[i]['field_name']] = custom_val_tb
    #                                 if data[i]['type']=='number':
    #                                     temp_dict[data[i]['field_name']]=int(temp_dict[data[i]['field_name']])
    #                             else:
    #                                 temp_dict[data[i]['field_name']] = data[i]['userInput']
    #                     else:
    #                         temp_dict[i]=data[i]
    #                 if i.lower() == 'project': 
    #                     temp_dict[i]={'id': project_id}
    #                 if i.lower() in ['issuetype']: 
    #                     temp_dict[i]={'name': issue_type}
    #                 if i.lower() in ['reporter', 'assignee']:
    #                     user_id = self.getAccountID(data[i]['userInput'])
    #                     temp_dict[data[i]['field_name']]={'accountId':user_id}
    #             if 'labels' not in temp_dict:
    #                 temp_dict['labels']=Labels
    #             if 'Attachment' in data:
    #                 attachement_path = str(data['Attachment']['userInput'])
    #             check = None
    #             if attachement_path != '' and attachement_path is not None:
    #                 log.debug('Condition passed inside if condition of attachment path')
    #                 if(attachement_path.startswith('\\')):
    #                     log.debug('attachment path obtained of server location')
    #                     new_path = attachement_path
    #                     new_path=new_path.strip()
    #                     check = os.path.exists(new_path)
    #                 else:
    #                     log.debug('attachment path of local machine')
    #                     check = os.path.exists(attachement_path)
    #                 if check == True:
    #                     flag = True
    #             else:
    #                 flag = True
    #             if(flag):
    #                 issue_dict={}
    #                 if(issue_type=='Sub-task'):
    #                     issue_dict['parent']={'key':parentid}
    #                 create_issues = jira.create_issue(temp_dict)
    #                 issue_id = create_issues.key
    #                 issue_link = url + "/browse/" + issue_id
    #                 logger.print_on_console('Issue link is', issue_link)
    #                 if attachement_path != '' and  attachement_path is not None and check == True:
    #                     try:
    #                         file_obj = None
    #                         if(attachement_path.startswith('\\')):
    #                             new_path = attachement_path
    #                             file_obj=open(new_path,'rb')
    #                         else:
    #                             file_obj=open(attachement_path,'rb')
    #                         attachement_object=jira.add_attachment(create_issues.id,file_obj)
    #                         file_obj.close()
    #                     except Exception as e:
    #                         log.error(e)
    #                         socket.emit('issue_id','Fail')
    #                         logger.print_on_console('Error in reading/loading file')
    #     except Exception as e:
    #         log.error(e)
    #         socket.emit('issue_id','Fail')
    #         logger.print_on_console('Failed to create issue')
    #     if issue_id != None:
    #         """inwardIssue: current issue(Target issue)
    #             outwardIssue: issues that needs to be linked to current issue (Source issues)
    #         """
    #         if 'Linked Issues' in data:
    #             outwardIssue=data['Linked Issues']['Issues']
    #             outwardIssue=outwardIssue.split(',')
    #             linkedIssue_Type=data['Linked Issues']['userInput']['text']
    #             if outwardIssue!='' and linkedIssue_Type!='':
    #                 for issue in outwardIssue:
    #                     res=jira.create_issue_link(type=linkedIssue_Type,inwardIssue=issue_id,outwardIssue=issue)
    #                     if res.reason=='Created' and res.status_code==201:
    #                         logger.print_on_console('created Issue is linked to ',issue)
    #         if 'mappedItem' in data:
    #             outwardIssue=data['mappedItem']
    #             outwardIssue=outwardIssue.split(',')
    #             linkedIssue_Type='blocks'
    #             if outwardIssue!='' and linkedIssue_Type!='':
    #                 for issue in outwardIssue:
    #                     res=jira.create_issue_link(type=linkedIssue_Type,inwardIssue=issue_id,outwardIssue=issue)
    #                     if res.reason=='Created' and res.status_code==201:
    #                         logger.print_on_console('Bug is linked to ',issue)
    #         logger.print_on_console('Bug created is ',issue_id)
    #         response=[]
    #         response.append(issue_id)
    #         response.append(issue_link)
    #         response=str(response)
    #         socket.emit('issue_id',response)
    #     elif(issue_id==None and check == False):
    #         log.error("Invalid Attachment Path")
    #         # socket.emit('issue_id','Invalid Path')
    #         response=[]
    #         response.append('Invalid Path')
    #         response.append('')
    #         response=str(response)
    #         socket.emit('issue_id',response)
    #     else:
    #         socket.emit('issue_id','Fail')

    def getAllAutoDetails(self,azure_input_dict,socket):
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
        jira = None

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
            if(';' in org_url):
                log.debug('Connecting to JIRA through proxy')
                jira_server = jira_input_dict['jira_serverlocation'].split(';')[0]
                jira_proxy = jira_input_dict['jira_serverlocation'].split(';')[1]
                jira_options = {'server':jira_server,'verify':False}
                jira = JIRA(options=jira_options,basic_auth=(jira_input_dict['jira_uname'],jira_input_dict['jira_pwd']),proxies={'http':jira_proxy,'https':jira_proxy})
            else:
                True
                # jira_options = {'server': org_url}
                # jira = JIRA(options=jira_options,basic_auth=())

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

    def getConfigureFields(self,azure_input_dict,socket):
        """
            Method to get Configure fields using the user selected project and issue_type
            returns list of Configurable fields
        """
        config_data={}
        inp_project=azure_input_dict['project']
        issue_type=azure_input_dict['issuetype']
        project_key=None
        project_name=None
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

            endpoint_url = f'{org_url}/{project_name}/_apis/wit/workitemtypes/{issue_type}/fields?$expand=all&api-version=7.0'

            
            # get projects
            respon = requests.get(url=endpoint_url, headers=headers)

            required_comp = {}
            if respon.status_code == 200:
                JsonObject = respon.json()
                for details in JsonObject['value']:
                    # if details['alwaysRequired']:
                    required_comp[details['name']] = details

            # jira_options = {'server': jira_input_dict['url']}
            # res_jira= JIRA(options=jira_options,basic_auth=(jira_input_dict['username'],jira_input_dict['password']))
            # log.debug('Fetching of Configure fields by the given inputs started')
            # for i in jira_input_dict['projects_data']:
            #     if inp_project in i['key']:
            #         project_key=i['code']
            #         project_name=i['text']
            #         break
            # url=jira_input_dict['url']+"/rest/api/2/issue/createmeta?projectKeys="+project_key+"&issuetypeNames="+issue_type+"&expand=projects.issuetypes.fields"
            # auth = HTTPBasicAuth(jira_input_dict['username'],jira_input_dict['password'])
            # headers={"Accept":"application/json"}
            # respon=requests.request("GET",url,headers=headers,auth=auth)
            # if respon.status_code == 200:
            #     JsonObject = respon.json()
            #     if JsonObject['projects'][0]['name']==project_name:
            #         all_fields=JsonObject['projects'][0]['issuetypes'][0]['fields']
            #         for i in all_fields:
            #             if all_fields[i]['name'] not in ['Project', 'Issue Type','Description'] or 'customfield' in all_fields[i]['key']:
            #                 temp = {}
            #                 temp['name']=all_fields[i]['name']
            #                 temp['key']=all_fields[i]['key']
            #                 temp['value']='Editable'
            #                 temp['required']=all_fields[i]['required']
            #                 temp['type']= all_fields[i]['schema']['type'] if all_fields[i]['schema'] else None
            #                 if 'allowedValues' in all_fields[i] and all_fields[i]['allowedValues']==[]:
            #                     temp['value']='None'
            #                 elif 'allowedValues' in all_fields[i] and all_fields[i]['allowedValues']!=[] and all_fields[i]['name'].lower()!='priority':
            #                     temp['value']=[]
            #                     count=1
            #                     for index,item in enumerate(all_fields[i]['allowedValues']):
            #                         temp['value'].append({'key': count , 'text':item['value']})
            #                         count=count+1
            #                 elif 'allowedValues' in all_fields[i] and all_fields[i]['allowedValues']!=[] and all_fields[i]['name'].lower()=='priority':
            #                     temp['value']=[]
            #                     count=1
            #                     for index,item in enumerate(all_fields[i]['allowedValues']):
            #                         temp['value'].append({'key': count , 'text':item['name']})
            #                         count=count+1
            #                 if all_fields[i]['name'].lower() == 'labels':
            #                     url=jira_input_dict['url']+"/rest/api/3/label"
            #                     auth = HTTPBasicAuth(jira_input_dict['username'],jira_input_dict['password'])
            #                     headers={"Accept":"application/json"}
            #                     respon=requests.request("GET",url,headers=headers,auth=auth)
            #                     if respon.status_code == 200:
            #                         JsonObject = respon.json()
            #                         temp['value']=[]
            #                         count=1
            #                         for index,item in enumerate(JsonObject['values']):
            #                             temp['value'].append({'key': count , 'text':item})
            #                             count=count+1
            #                 config_data[all_fields[i]['name']]=temp
                   
            #         if "Linked Issues" in config_data:
            #             config_data["Linked Issues"]['value']=[]
            #             count=1
            #             for index,item in enumerate(res_jira.issue_link_types()):
            #                 if item.inward != item.outward:
            #                     config_data["Linked Issues"]['value'].append({'key': count , 'text':item.outward})
            #                     count=count+1
            #                     config_data["Linked Issues"]['value'].append({'key': count , 'text':item.inward})
            #                     count=count+1
            #                 else:
            #                     config_data["Linked Issues"]['value'].append({'key': count , 'text':item.outward})
            #                     count=count+1
                   
            # log.debug('Fetching of Configure fields by the given inputs is completed successfully')
            # jira_input_dict['project_selected']={'project':project_name,'key':project_key}
            socket.emit('configure_field',required_comp)
        except Exception as e:
            log.error(e)
            socket.emit('configure_field','Fail')
            logger.print_on_console('Exception in fetching Configure Fields')

    def getAccountID(self,acc_name):
        """
            Method to get Account ID(JIRA) of given name
            returns Account ID
        """
        acc_id=None
        try:
            url=self.jira_details['url']+"/rest/api/3/groupuserpicker"
            auth = HTTPBasicAuth(self.jira_details['username'],self.jira_details['password'])
            headers={"Accept":"application/json"}
            query={
                'query':acc_name
            }
            respon=requests.request("GET",url,headers=headers,params=query,auth=auth)
            if respon.status_code == 200:
                    JsonObject = respon.json()
                    usersObj=JsonObject['users']
                    if usersObj['users'] !=[]:
                        for i in usersObj['users']:
                            if i['displayName']==acc_name and acc_name in i['html']:
                                acc_id=i['accountId']
                                break
        except Exception as e:
            log.error(e)
            logger.print_on_console('Exception in fetching Account ID')
        return acc_id

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
            if(';' in org_url):
                log.debug('Connecting to JIRA through proxy')
                jira_server = jira_input_dict['jira_serverlocation'].split(';')[0]
                jira_proxy = jira_input_dict['jira_serverlocation'].split(';')[1]
                jira_options = {'server':jira_server,'verify':False}
                jira = JIRA(options=jira_options,basic_auth=(jira_input_dict['jira_uname'],jira_input_dict['jira_pwd']),proxies={'http':jira_proxy,'https':jira_proxy})
            else:
                True
                # jira_options = {'server': org_url}
                # jira = JIRA(options=jira_options,basic_auth=())

            socket.emit('Jira_details',res)
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('auto_populate','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('auto_populate','Invalid Credentials')
            else:
                socket.emit('auto_populate','Fail')
            logger.print_on_console('Exception in login and auto populating projects')

    def get_testcases(self,jira_input_dict,socket):
        """
            Method to get the testcases based on project from jira
            returns list of testcases
        """
        res = {}
        res['testcases']=[]
        try:
            project=jira_input_dict['project_selected']['project']
            key=jira_input_dict['project_selected']['key']
            url=jira_input_dict['jira_serverlocation']+"/rest/api/2/search?jql=issueType="+'"'+jira_input_dict['item_type']+'"'+"&fields=id,key,project,summary"
            auth = HTTPBasicAuth(jira_input_dict['jira_uname'],jira_input_dict['jira_pwd'])
            headers={"Accept":"application/json"}
            respon=requests.request("GET",url,headers=headers,auth=auth)
            if respon.status_code == 200:
                JsonObject = respon.json()
                if 'issues' in JsonObject:
                    for index,item in enumerate(JsonObject['issues']):
                        if 'fields' in item:
                            if 'project' in item['fields']:
                                if project == item['fields']['project']['name'] and key == item['fields']['project']['key']:
                                    # res['testcases'].append({'id': item['id'], 'code':item['key']})
                                    # res['testcases'].append({'id': item['key'], 'code':item['fields']['summary']})
                                    res['testcases'].append({'id': item['id'], 'code':item['key'], 'summary':item['fields']['summary']})
            socket.emit('Jira_testcases',res)
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('auto_populate','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('auto_populate','Invalid Credentials')
            else:
                socket.emit('auto_populate','Fail')
            logger.print_on_console('Exception in login and populating testcases')


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
                    for details in JsonObject['workItems'][-20:-1]:
                        ids += str(details['id'])
                        ids+=','

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

            if(';' in org_url):
                log.debug('Connecting to JIRA through proxy')
                jira_server = jira_input_dict['jira_serverlocation'].split(';')[0]
                jira_proxy = jira_input_dict['jira_serverlocation'].split(';')[1]
                jira_options = {'server':jira_server,'verify':False}
                jira = JIRA(options=jira_options,basic_auth=(jira_input_dict['jira_uname'],jira_input_dict['jira_pwd']),proxies={'http':jira_proxy,'https':jira_proxy})
            else:
                True
                # jira_options = {'server': org_url}
                # jira = JIRA(options=jira_options,basic_auth=())

            socket.emit('Jira_details',res)
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

            if(';' in org_url):
                log.debug('Connecting to JIRA through proxy')
                jira_server = jira_input_dict['jira_serverlocation'].split(';')[0]
                jira_proxy = jira_input_dict['jira_serverlocation'].split(';')[1]
                jira_options = {'server':jira_server,'verify':False}
                jira = JIRA(options=jira_options,basic_auth=(jira_input_dict['jira_uname'],jira_input_dict['jira_pwd']),proxies={'http':jira_proxy,'https':jira_proxy})
            else:
                True
                # jira_options = {'server': org_url}
                # jira = JIRA(options=jira_options,basic_auth=())

            socket.emit('Jira_details',res)
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

            if(';' in org_url):
                log.debug('Connecting to JIRA through proxy')
                jira_server = jira_input_dict['jira_serverlocation'].split(';')[0]
                jira_proxy = jira_input_dict['jira_serverlocation'].split(';')[1]
                jira_options = {'server':jira_server,'verify':False}
                jira = JIRA(options=jira_options,basic_auth=(jira_input_dict['jira_uname'],jira_input_dict['jira_pwd']),proxies={'http':jira_proxy,'https':jira_proxy})
            else:
                True
                # jira_options = {'server': org_url}
                # jira = JIRA(options=jira_options,basic_auth=())

            socket.emit('Jira_details',res)
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

            if(';' in org_url):
                log.debug('Connecting to JIRA through proxy')
                jira_server = jira_input_dict['jira_serverlocation'].split(';')[0]
                jira_proxy = jira_input_dict['jira_serverlocation'].split(';')[1]
                jira_options = {'server':jira_server,'verify':False}
                jira = JIRA(options=jira_options,basic_auth=(jira_input_dict['jira_uname'],jira_input_dict['jira_pwd']),proxies={'http':jira_proxy,'https':jira_proxy})
            else:
                True
                # jira_options = {'server': org_url}
                # jira = JIRA(options=jira_options,basic_auth=())

            socket.emit('Jira_details',res)
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
        res = "invalidcredentials"
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
                else:
                    data = value['data']

                if value['name'] == 'Repro Steps':
                    data = azure_input_dict['info']['reproSteps']['value']
                if value['name'] == 'Found In':
                    data = 'demo'
                patch_document.append(
                     {
                        "op": "add",
                        # "path": "/fields/System.Title",
                        "path": "/fields" + value['url'].split('fields',1)[1],
                        "value": data
                    }
                )
                to_make = [
                        {
                            "op": "add",
                            "path": "/fields/System.Title",
                            "value": "Bug created using API march 29"
                        },{
                            "op": "add",
                            "path": "/fields/Microsoft.VSTS.TCM.ReproSteps",
                            "value": "Bug created using API"
                        },{
                            "op": "add",
                            "path": "/fields/Microsoft.VSTS.Common.Priority",
                            "value": "1"
                        },{
                            "op": "add",
                            "path": "/fields/Microsoft.VSTS.Common.Severity",
                            "value": "2 - High"
                        },{
                            "op": "add",
                            "path": "/fields/System.IterationPath",
                            "value": "AvoAssure"
                        },{
                            "op": "add",
                            "path": "/fields/System.AreaPath",
                            "value": "AvoAssure\Product Team"
                        },{
                            "op": "add",
                            "path": "/fields/System.State",
                            "value": "New"
                        },{
                            "op": "add",
                            "path": "/fields/Microsoft.VSTS.Common.ValueArea",
                            "value": "Business"
                        },{
                            "op": "add",
                            "path": "/fields/Custom.Build#",
                            "value": "Avo Assure v22.3.0-rc.1"
                        },{
                            "op": "add",
                            "path": "/fields/Microsoft.VSTS.Build.FoundIn",
                            "value": "demo"
                        }]
            respon = requests.patch(endpoint_url, headers=headers, data=json.dumps(patch_document))

            res = []
            if respon.status_code == 200:
                JsonObject = respon.json()
                if len(JsonObject)>0:
                        res.append(JsonObject['id'])
                        res.append(JsonObject['url'])
                        res=str(res)

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
