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
import Logger
import constants
## This class will have the methods to automate Outlook Application
class OutlookKeywords:

        def __init__(self, senderEmail,subject,toMail):
            self.senderEmail=senderEmail
            self.subject=subject
            self.toMail=toMail
            self.Flag=False
            self.Subject=""
            self.ToMailID=""
            self.FromMailId=""
            self.AttachmentStatus=constants.ATTACH_STATUS_NO
            self.Body=""
            self.message=""


##  This method takes 3 params
##  1. senderName (Display name  in Outlook application)
##  2. subject
##  3.to whom mail has been sent
##  On success return the mail content in string format
## else return fail
        def GetEmail(self):

##   Get the Outlook com object registry
            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            inbox = outlook.GetDefaultFolder(constants.INBOX_FOLDER)
            all_inbox = inbox.Items
            folders = inbox.Folders
            for msg in all_inbox:
                if msg.Class==43:
##                    if msg.SenderEmailType=='EX':
                                if msg.SenderName==self.senderEmail:
                                    if msg.Subject==self.subject:
                                        if msg.To==self.toMail:
                                            self.Subject = msg.Subject
                                            self.Body= msg.Body
                                            if msg.SenderEmailType=='EX':
                                                 self.FromMailId= msg.Sender.PropertyAccessor.GetProperty(constants.PR_SMTP_ADDRESS)
                                            else:
                                                self.FromMailId=msg.SenderEmailAddress
                                            for recipient in  msg.Recipients:
                                                self.ToMailID=recipient.PropertyAccessor.GetProperty(constants.PR_SMTP_ADDRESS)+";"
                                                self.ToMailID=self.ToMailID[:-1]
                                            if msg.Attachments.Count>0:
                                                self.AttachmentStatus=constants.ATTACH_STATUS_YES
                                            message="From : "+msg.SenderName+" <"+self.FromMailId+">"+"\n"+ "To: "+ self.ToMailID + "\n"+ "Date: "+str(msg.SentOn)+ "\n"+ "Subject: "+ msg.Subject+ "\n"+ str(msg.Attachments.Count)+ " attachments." + "\n"+ msg.Body
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
                Logger.log("Error: No such mail found")

        def GetFromMailId(self):
            if self.Flag==True:
                return self.FromMailId
            else:
                Logger.log("Error : No such mail id found")
                return constants.STATUS_FAIL


        def GetAttachmentStatus(self):
            if self.Flag==True:
                return self.AttachmentStatus
            else:
                Logger.log("Error : mail does't have such info")
                return constants.STATUS_FAIL

        def GetSubject(self):
            if self.Flag==True:
                return self.Subject
            else:
                Logger.log("Error : No subject found")
                return constants.STATUS_FAIL

        def GetToMailID(self):
            if self.Flag==True:
                return self.ToMailID
            else:
                Logger.log("Error : No such mail id found")
                return constants.STATUS_FAIL

        def GetBody(self):
            if self.Flag==True:
                return self.Body
            else:
                Logger.log("Error : No Body found")
                return constants.STATUS_FAIL

        def VerifyEmail(self):
            if self.Flag==True:
                return Body
            else:
                Logger.log("Error : No Body found")
                return constants.STATUS_FAIL

##a=OutlookKeywords("Microsoft Outlook","Your mailbox is almost full.","Prudhvi Prem Gujjuboyina")
##a.GetEmail()
##b=OutlookKeywords("Arpitha B.V","RE: Want to work on weekends !!!!!!!!!!!!!!!","Vivek Kallaje; Test Automation")
##b.GetEmail()
##b.GetEmail()
##a.GetToMailID()
##a.GetSubject()
##a.GetBody()
##a.GetAttachmentStatus()