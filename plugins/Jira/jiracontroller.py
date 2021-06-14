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
log = logging.getLogger("jiracontroller.py")


class JiraWindow():
    jira = None
    def __init__(self,x=0):
        self.x = x

    def connectJIRA(self,jira_serverlocation , jira_uname , jira_pwd ):
        try:
            jira_options = {'server': jira_serverlocation}
            jira = JIRA(options=jira_options,basic_auth=(jira_uname,jira_pwd))
            return jira
        except Exception as e:
            logger.print_on_console("Failed to connect to JIRA")

    def createIssue(self,data,socket):
        """
            Method to create issue in JIRA
            inputs project id , summary , issuetype , priority , description , label , attachment
            returns issue id created in JIRA
        """
        issue_id = None
        jira = None
        create_issues = None
        try:
            username= data['username']
            password = data['password']
            url = data['url']
            if(';' in url):
                jira_options = {'server':url.split(';')[0],'verify':False}
                jira = JIRA(options=jira_options,basic_auth=(username,password),proxies={'http':url.split(';')[1],'https':url.split(';')[1]})
            else:
                jira_options = {'server': url}
                jira = JIRA(options=jira_options,basic_auth=(username,password))
            project_id = data['project']
            summary = data['summary']
            issue_type = data['issuetype']
            priority = data['priority']
            parentid=data['parentissue']
            flag = False
            if all(check1 is not None for check1 in [project_id, summary, issue_type, priority]):
                log.debug('Condition passed inside if not none check')
                description = data['description']
                label = data['label']
                attachement_path = str(data['attachment'])
                check = None
                if attachement_path != '':
                    log.debug('Condition passed inside if condition of attachment path')
                    if(attachement_path.startswith('\\')):
                        log.debug('attachment path obtained of server location')
                        new_path = attachement_path
                        new_path=new_path.strip()
                        check = os.path.exists(new_path)
                    else:
                        log.debug('attachment path of local machine')
                        check = os.path.exists(attachement_path)
                    if check == True:
                        flag = True
                else:
                    flag = True
                if(flag):
                    if(issue_type == 'Story' or issue_type == 'Epic'):
                        issue_dict = {'project': {'id': project_id},'summary': summary,'description': description,'issuetype': {'name': issue_type},'labels':label}
                    else:
                        issue_dict = {'project': {'id': project_id},'summary': summary,'description': description,'issuetype': {'name': issue_type},'priority':{'name' : priority},'labels':label}
                    if(issue_type=='Sub-task'):
                        issue_dict['parent']={'key':parentid}
                    create_issues = jira.create_issue(issue_dict)
                    issue_id = create_issues.key
                    if attachement_path != '' and check == True:
                        try:
                            file_obj = None
                            if(attachement_path.startswith('\\')):
                                new_path = attachement_path
                                file_obj=open(new_path,'rb')
                            else:
                                file_obj=open(attachement_path,'rb')
                            attachement_object=jira.add_attachment(create_issues.id,file_obj)
                            file_obj.close()
                        except Exception as e:
                            log.error(e)
                            socket.emit('issue_id','Fail')
                            logger.print_on_console('Error in reading/loading file')
        except Exception as e:
            log.error(e)
            socket.emit('issue_id','Fail')
            logger.print_on_console('Failed to create issue')
        if issue_id != None:
            logger.print_on_console('Issue id created is ',issue_id)
            socket.emit('issue_id',issue_id)
        elif(issue_id==None and check == False):
            log.debug("Invalid Attachment Path")
            log.error("Invalid Attachment Path")
            socket.emit('issue_id','Invalid Path')
        else:
            socket.emit('issue_id','Fail')

    def getAllAutoDetails(self,jira_credentials,socket):
        """
            Method to login using the user provided credentials and get projects, issue type and priority lists
            related to user credentials
            returns list of projects, issue type and priority
        """
        data = {}
        projects_list = []
        issue_types = []
        priority_list = []
        data['projects'] = []
        data['issuetype'] = []
        data['priority'] = []
        jira = None
        try:
            if(';' in jira_credentials['jira_serverlocation']):
                log.debug('Connecting to JIRA through proxy')
                jira_server = jira_credentials['jira_serverlocation'].split(';')[0]
                jira_proxy = jira_credentials['jira_serverlocation'].split(';')[1]
                jira_options = {'server':jira_server,'verify':False}
                jira = JIRA(options=jira_options,basic_auth=(jira_credentials['jira_uname'],jira_credentials['jira_pwd']),proxies={'http':jira_proxy,'https':jira_proxy})
            else:
                jira_options = {'server': jira_credentials['jira_serverlocation']}
                jira = JIRA(options=jira_options,basic_auth=(jira_credentials['jira_uname'],jira_credentials['jira_pwd']))
            projects_list = jira.projects()
            issue_types = jira.issue_types()
            priority_list = jira.priorities()
            for index,item in enumerate(projects_list):
                data['projects'].append({'id': item.id , 'name':item.name})
            for index,item in enumerate(issue_types):
                data['issuetype'].append({'id': item.id , 'name':item.name})
            for index,item in enumerate(priority_list):
                data['priority'].append({'id': item.id , 'name':item.name})
            socket.emit('auto_populate',data)
        except Exception as e:
            log.error(e)
            if 'Invalid URL' in str(e):
                socket.emit('auto_populate','Invalid Url')
            elif 'Unauthorized' in str(e):
                socket.emit('auto_populate','Invalid Credentials')
            else:
                socket.emit('auto_populate','Fail')
            logger.print_on_console('Exception in login and auto populating data')
