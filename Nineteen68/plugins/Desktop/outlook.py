#-------------------------------------------------------------------------------
# Name:        outlook
# Purpose:      To automate outlook keywords
#
# Author:      prudhvi.gujjuboyina
#
# Created:     07-09-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from  win32com.client import Dispatch
import outlook_constants
from   pywintypes import  com_error

import desktop_constants
import logging
from constants import *
import logger
log = logging.getLogger('outlook.py')

## This class will have the methods to automate Outlook Application
class OutlookKeywords:

        def __init__(self):
            self.senderEmail=''
            self.subject=''
            self.toMail=''
            self.Flag=False
            self.Subject=''
            self.ToMailID=''
            self.FromMailId=''
            self.AttachmentStatus=outlook_constants.ATTACH_STATUS_NO
            self.Body=''
            self.message=''
            self.Content=None
            self.targetFolder=None
            self.outlook=None
            self.store=None


#To support seperate accounts and  subFolders this method is implemented , Input should be the folder path in properties of outlook folder
        def switchToFolder(self,input,*args):
            status=desktop_constants.TEST_RESULT_FAIL
            method_output=desktop_constants.TEST_RESULT_FALSE
            error_msg=None
            result=OUTPUT_CONSTANT
            try:
                logger.print_on_console('switching to the folder')
                folderPath=input[0]
                folderPath=folderPath.strip('\\')
                folders=folderPath.split('\\')
                accountname=folders[0]
                self.outlook = Dispatch('Outlook.Application').GetNamespace('MAPI')
#               get the message stores in outlook
                stores=self.outlook.Stores
                if accountname!='':
                    for store in stores:
                        if store.DisplayName==accountname:
                            self.store=store
                            if folders[1]=='Inbox':
                                inbox_folder = store.GetDefaultFolder(outlook_constants.INBOX_FOLDER)
                                index=0;
                                folder=None
                                for foldername in folders:
                                    if index==0 or index==1:
                                        folder=inbox_folder
                                        self.targetFolder=folder
                                    else:
                                        folder=folder.Folders.Item(folders[index])
                                        self.targetFolder=self.findFolder(foldername,self.targetFolder)
                                    index+=1
                                if(self.targetFolder==None):
                                    logger.print_on_console('Unable to find the target folder')
                                    error_msg='Unable to find the target folder'
                                    break
                                else:
                                    logger.print_on_console('Switched to folder')
                                    status=desktop_constants.TEST_RESULT_PASS
                                    method_output=desktop_constants.TEST_RESULT_TRUE

                            else:
                                logger.print_on_console('The given path is invalid')
                else:
                    logger.print_on_console('Check the path given')
                    error_msg='Check the path given'
            except Exception as e:
                log.error(e)
                logger.print_on_console(e)
            return status,method_output,result,error_msg


##  This method takes 3 params
##  1. senderName (Display name  in Outlook application)
##  2. subject
##  3.to whom mail has been sent
##  On success return the mail content in string format
## else return fail
        def GetEmail(self,input,*args):

##   Get the Outlook com object registry
            try:
                status=desktop_constants.TEST_RESULT_FAIL
                method_output=desktop_constants.TEST_RESULT_FALSE
                result=OUTPUT_CONSTANT
                error_msg=None
                self.senderEmail=input[0]
                self.subject=input[2]
                self.toMail=input[1]
                if (self.outlook==None):
                    self.outlook = Dispatch('Outlook.Application').GetNamespace('MAPI')
                    inbox = self.outlook.GetDefaultFolder(outlook_constants.INBOX_FOLDER)
                else:
                    inbox=self.targetFolder
                all_inbox = inbox.Items
                folders = inbox.Folders
                all_inbox=reversed(list(all_inbox))
                for msg in all_inbox:
                    if msg.Class==43:
                        if msg.SenderName==self.senderEmail:
                            if msg.Subject==self.subject:
                                if self.toMail in msg.To:
                                    self.Content=msg
                                    self.Subject = msg.Subject
                                    self.Body= msg.Body
                                    if msg.SenderEmailType=='EX':
                                         self.FromMailId= msg.Sender.PropertyAccessor.GetProperty(outlook_constants.PR_SMTP_ADDRESS)
                                    else:
                                        self.FromMailId=msg.SenderEmailAddress
                                    for recipient in  msg.Recipients:
                                        if recipient.Type==1:
                                            self.ToMailID+=recipient.PropertyAccessor.GetProperty(outlook_constants.PR_SMTP_ADDRESS)+';'
                                    self.ToMailID=self.ToMailID[:-1]
                                    if msg.Attachments.Count>0:
                                        self.AttachmentStatus=outlook_constants.ATTACH_STATUS_YES
##                                    message="From : "+msg.SenderName+" <"+self.FromMailId+">"+"\n"+ "To: "+ self.ToMailID + "\n"+ "Date: "+str(msg.SentOn)+ "\n"+ "Subject: "+ msg.Subject+ "\n"+ str(msg.Attachments.Count)+ " attachments." + "\n"+ msg.Body
                                    self.Flag=True
                                    msg.Display(False)
                                    status=desktop_constants.TEST_RESULT_PASS
                                    method_output=desktop_constants.TEST_RESULT_TRUE
                                    break
                                else:
                                    continue
                            else:
                                continue
                        else :
                            continue
                if self.Flag!=True:
                    logger.print_on_console('Error: No such mail found')
                    error_msg='Error: No such mail found'
            except Exception as e:
               log.error(e)
               logger.print_on_console(e)
            return status,method_output,result,error_msg

        def GetFromMailId(self,input,*args):
            try:
                status=desktop_constants.TEST_RESULT_FAIL
                method_output=desktop_constants.TEST_RESULT_FALSE
                error_msg=None
                res=None
                if self.Flag==True:
                    res= self.FromMailId
                    status=desktop_constants.TEST_RESULT_PASS
                    method_output=desktop_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Error : No such mail id found')
                    error_msg='Error : No such mail id found'
            except Exception as  e:
                log.error(e)
                logger.print_on_console(e)
            return status,method_output,res,error_msg


        def GetAttachmentStatus(self,input,*args):
            try:
                status=desktop_constants.TEST_RESULT_FAIL
                method_output=desktop_constants.TEST_RESULT_FALSE
                res=None
                error_msg=None
                if self.Flag==True:
                    res= self.AttachmentStatus
                    status=desktop_constants.TEST_RESULT_PASS
                    method_output=desktop_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Error : mail does''t have such info')
                    error_msg='Error : mail does''t have such info'
            except Exception as  e:
                log.error(e)
                logger.print_on_console(e)
            return status,method_output,res,error_msg

        def GetSubject(self,input,*args):
            try:
                status=desktop_constants.TEST_RESULT_FAIL
                method_output=desktop_constants.TEST_RESULT_FALSE
                res=None
                error_msg=None
                if self.Flag==True:
                    res= self.Subject
                    status=desktop_constants.TEST_RESULT_PASS
                    method_output=desktop_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Error : No subject found')
                    error_msg='Error : No subject found'
            except Exception as  e:
                log.error(e)
                logger.print_on_console(e)
            return status,method_output,res,error_msg

        def GetToMailID(self,input,*args):
            status=desktop_constants.TEST_RESULT_FAIL
            method_output=desktop_constants.TEST_RESULT_FALSE
            res=None
            error_msg=None
            try:
                if self.Flag==True:
                    res= self.ToMailID
                    status=desktop_constants.TEST_RESULT_PASS
                    method_output=desktop_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Error : No such mail id found')
                    error_msg='Error : No such mail id found'
            except Exception as  e:
                log.error(e)
                logger.print_on_console(e)
            return status,method_output,res,error_msg


        def GetBody(self,input,*args):
            status=desktop_constants.TEST_RESULT_FAIL
            method_output=desktop_constants.TEST_RESULT_FALSE
            res=None
            error_msg=None
            try:
                if self.Flag==True:
                    res= self.Body
                    status=desktop_constants.TEST_RESULT_PASS
                    method_output=desktop_constants.TEST_RESULT_TRUE
                else:
                    logger.print_on_console('Error : No Body found')
                    error_msg='Error : No Body found'
            except Exception as  e:
                    log.error(e)
                    logger.print_on_console(e)
            return status,method_output,str(res),error_msg


        def VerifyEmail(self,input,*args):
            try:
                status=desktop_constants.TEST_RESULT_FAIL
                method_output=desktop_constants.TEST_RESULT_FALSE
                error_msg=None
                res=OUTPUT_CONSTANT
                if self.Flag==True:
                    try:
                        FilePath=input[0]
                        mail_content = self.outlook.OpenSharedItem(FilePath)
                        if str(self.Content.SenderName) == str(mail_content.SenderName):
                            if self.Content.To==mail_content.To:
                                if self.Content.Subject==mail_content.Subject:
                                    if self.Content.Body==mail_content.Body:
                                        if str(self.Content.Attachments)==str(mail_content.Attachments):
                                            if self.Content.SentOn==mail_content.SentOn:
                                                status=desktop_constants.TEST_RESULT_PASS
                                                method_output=desktop_constants.TEST_RESULT_TRUE


                    except (com_error):
                        logger.print_on_console('Error occured : File not found')
                else:
                    logger.print_on_console('Error : No such mail found')
            except Exception as  e:
                Exceptions.error(e)
            return status,method_output,res,error_msg

# Internal method to search for a folder in given folder
        def findFolder(self,folderName,searchIn):
            try:
                lowerAccount = searchIn.Folders
                for x in lowerAccount:
                    if x.Name == folderName:
##                        print 'found it %s '%x.Name
                        objective = x
                        return objective
##                    else:
##                        print folderName+' folder not found'
                return None
            except Exception as error:
                logger.print_on_console( "Looks like we had an issue accessing the searchIn object")
                return None


