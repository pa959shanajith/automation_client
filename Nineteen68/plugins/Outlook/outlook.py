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
import constants
from   pywintypes import  com_error

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
            self.AttachmentStatus=constants.ATTACH_STATUS_NO
            self.Body=''
            self.message=''
            self.Content=None

##  This method takes 3 params
##  1. senderName (Display name  in Outlook application)
##  2. subject
##  3.to whom mail has been sent
##  On success return the mail content in string format
## else return fail
        def GetEmail(self,senderEmail,toMail,subject):

##   Get the Outlook com object registry
            try:
                self.senderEmail=senderEmail
                self.subject=subject
                self.toMail=toMail
                self.outlook = Dispatch('Outlook.Application').GetNamespace('MAPI')
                inbox = self.outlook.GetDefaultFolder(constants.INBOX_FOLDER)
                all_inbox = inbox.Items
                folders = inbox.Folders
                for msg in all_inbox:
                    if msg.Class==43:
                        if msg.SenderName==self.senderEmail:
                            if msg.Subject==self.subject:
                                if self.toMail in msg.To:
                                    self.Content=msg
                                    self.Subject = msg.Subject
                                    self.Body= msg.Body
                                    if msg.SenderEmailType=='EX':
                                         self.FromMailId= msg.Sender.PropertyAccessor.GetProperty(constants.PR_SMTP_ADDRESS)
                                    else:
                                        self.FromMailId=msg.SenderEmailAddress
                                    for recipient in  msg.Recipients:
                                        if recipient.Type==1:
                                            self.ToMailID+=recipient.PropertyAccessor.GetProperty(constants.PR_SMTP_ADDRESS)+';'
                                    self.ToMailID=self.ToMailID[:-1]
                                    if msg.Attachments.Count>0:
                                        self.AttachmentStatus=constants.ATTACH_STATUS_YES
##                                    message="From : "+msg.SenderName+" <"+self.FromMailId+">"+"\n"+ "To: "+ self.ToMailID + "\n"+ "Date: "+str(msg.SentOn)+ "\n"+ "Subject: "+ msg.Subject+ "\n"+ str(msg.Attachments.Count)+ " attachments." + "\n"+ msg.Body
                                    self.Flag=True
                                    msg.Display(False)
                                    return True
                                else:
                                    continue
                            else:
                                continue
                        else :
                            continue
                if self.Flag!=True:
                    logger.log('Error: No such mail found')
            except Exception as e:
                logger.log('Error occured: com error')
            return False

        def GetFromMailId(self):
            if self.Flag==True:
                return self.FromMailId
            else:
                logger.log('Error : No such mail id found')
                return constants.STATUS_FAIL


        def GetAttachmentStatus(self):
            if self.Flag==True:
                return self.AttachmentStatus
            else:
                logger.log('Error : mail does''t have such info')
                return constants.STATUS_FAIL

        def GetSubject(self):
            if self.Flag==True:
                return self.Subject
            else:
                logger.log('Error : No subject found')
                return constants.STATUS_FAIL

        def GetToMailID(self):
            if self.Flag==True:
                return self.ToMailID
            else:
                logger.log('Error : No such mail id found')
                return constants.STATUS_FAIL

        def GetBody(self):
            if self.Flag==True:
                return self.Body
            else:
                logger.log('Error : No Body found')
                return constants.STATUS_FAIL

        def VerifyEmail(self,FilePath):
            if self.Flag==True:
                try:
                    mail_content = self.outlook.OpenSharedItem(FilePath)
                    if str(self.Content.SenderName) == str(mail_content.SenderName):
                        if self.Content.To==mail_content.To:
                            if self.Content.Subject==mail_content.Subject:
                                if self.Content.Body==mail_content.Body:
                                    if str(self.Content.Attachments)==str(mail_content.Attachments):
                                        if self.Content.SentOn==mail_content.SentOn:
                                            return True
                                        else:
                                            return False
                                    else:
                                        return False
                                else:
                                    return False
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                except (com_error):
                    return False
                    logger.log('Error occured : File not found')
            else:
                logger.log('Error : No such mail found')
                return constants.STATUS_FAIL

