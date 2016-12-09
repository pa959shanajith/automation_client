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
import logger
import outlook_constants
from   pywintypes import  com_error
import Exceptions
import desktop_constants

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
            try:
                logger.log('switching to the folder')
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
                                        folder=folder.Folders.Item(folders[index-1])
                                        self.targetFolder=self.findFolder(foldername,folder)
                                    index+=1
                                if(self.targetFolder==None):
                                    logger.log('Unable to find the target folder')
                                    break
                                else:
                                    logger.log('Switched to folder')
                                    return True
                            else:
                                logger.log('The given path is invalid')
                else:
                    logger.log('Check the path given')
                    return False
            except Exception as e:
                Exceptions.error(e)
            return False


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
                                else:
                                    continue
                            else:
                                continue
                        else :
                            continue
                if self.Flag!=True:
                    logger.log('Error: No such mail found')
            except Exception as e:
                Exceptions.error(e)
            return status

        def GetFromMailId(self,input,*args):
            try:
                status=desktop_constants.TEST_RESULT_FAIL
                res=None
                if self.Flag==True:
                    res= self.FromMailId
                    status=desktop_constants.TEST_RESULT_PASS
                else:
                    logger.log('Error : No such mail id found')
            except Exception as  e:
                Exceptions.error(e)
            return status,res


        def GetAttachmentStatus(self,input,*args):
            try:
                status=desktop_constants.TEST_RESULT_FAIL
                res=None
                if self.Flag==True:
                    res= self.AttachmentStatus
                    status=desktop_constants.TEST_RESULT_PASS
                else:
                    logger.log('Error : mail does''t have such info')
            except Exception as  e:
                Exceptions.error(e)
            return status,res

        def GetSubject(self,input,*args):
            try:
                status=desktop_constants.TEST_RESULT_FAIL
                res=None
                if self.Flag==True:
                    res= self.Subject
                    status=desktop_constants.TEST_RESULT_PASS
                else:
                    logger.log('Error : No subject found')
            except Exception as  e:
                Exceptions.error(e)
            return status,res

        def GetToMailID(self,input,*args):
            try:
                if self.Flag==True:
                    res= self.ToMailID
                    status=desktop_constants.TEST_RESULT_PASS
                else:
                    logger.log('Error : No such mail id found')
            except Exception as  e:
                Exceptions.error(e)
            return status,res


        def GetBody(self,input,*args):
            try:
                if self.Flag==True:
                    res= self.Body
                    status=desktop_constants.TEST_RESULT_PASS
                else:
                    logger.log('Error : No Body found')
            except Exception as  e:
                    Exceptions.error(e)
            return status,str(res)


        def VerifyEmail(self,input,*args):
            try:
                status=desktop_constants.TEST_RESULT_FAIL
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


                    except (com_error):
                        logger.log('Error occured : File not found')
                else:
                    logger.log('Error : No such mail found')
            except Exception as  e:
                Exceptions.error(e)
            return status

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
                logger.log( "Looks like we had an issue accessing the searchIn object")
                return None


