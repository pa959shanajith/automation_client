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
## This class will have the methods to automate Outlook Application
class OutlookKeywords:

##  This method takes 3 params
##  1. senderName (Display name  in Outlook application)
##  2. subject
##  3.to whom mail has been sent
##  On success return the mail content in string format
## else return fail
        def GetEmail(self, senderEmail, subject, toMail):
            global Flag
            Flag=False
            global Subject
            Subject=""
            global ToMailID
            ToMailID=""
            global FromMailId
            FromMailId=""
            global AttachmentStatus
            AttachmentStatus="No"
            global Body
            Body=""
            message=""
##   Get the Outlook com object registry
            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            inbox = outlook.GetDefaultFolder("6")
            all_inbox = inbox.Items
            folders = inbox.Folders
            for msg in all_inbox:
                if msg.Class==43:
##                    if msg.SenderEmailType=='EX':
##                            if msg.Sender.GetExchangeUser().PrimarySmtpAddress=="chethan.singh@slkgroup.com":
##                            if msg.SenderEmailAddress=="prudhvi.gujjuboyina@slkgroup.com":

                                if msg.SenderName==senderEmail:
                                    if msg.Subject==subject:
                                        if msg.To==toMail:
##                                            fileName="D:/Python Mails/MyEmail.msg"
##                                            os.makedirs(os.path.dirname(filename), exist_ok=True)
##                                            with open(filename, "w") as f:
##                                                f.write("FOOBAR")
##                                            mail=   msg.SaveAs("D://abc.msg",3)
##                                            print "-----------------"
##                                            global Subject
                                            Subject = msg.Subject
                                            ToMailID= msg.To
                                            Body= msg.Body
                                            if msg.SenderEmailType=='EX':
                                                FromMailId= msg.Sender.GetExchangeUser().PrimarySmtpAddress
                                            else:
                                                FromMailId=msg.SenderEmailAddress
                                            if msg.Attachments.Count>0:
                                                AttachmentStatus="Yes"
                                            else:
                                                AttachmentStatus="No"
##                                            print "From : "+msg.SenderName+" <"+msg.Sender.GetExchangeUser().PrimarySmtpAddress+">"+"\n" + "To: "+ msg.To + "\n"+ "Date: "+str(msg.SentOn) + "\n" + "Subject: "+ msg.Subject+ "\n" + str(msg.Attachments.Count)+ " attachments." + "\n"+ msg.Body

##                                            print "-----------------"


                                            message="From : "+msg.SenderName+" <"+FromMailId+">"+"\n"+ "To: "+ msg.To + "\n"+ "Date: "+str(msg.SentOn)+ "\n"+ "Subject: "+ msg.Subject+ "\n"+ str(msg.Attachments.Count)+ " attachments." + "\n"+ msg.Body

##                                            print message

                                            Flag=True
                                            msg.Display(False)
                                            return True
                                        else :
                                            Logger.log("Error : No such mail found")
                                            return False



        def GetFromMailId(self):
            if Flag==True:
                print FromMailId
                return FromMailId
            else:
                Logger.log("Error : No such mail id found")
                return "fail"


        def GetAttachmentStatus(self):
            if Flag==True:
                print AttachmentStatus
                return AttachmentStatus
            else:
                Logger.log("Error : mail does't have such info")
                return "fail"

        def GetSubject(self):
            if Flag==True:
                print Subject
                return Subject
            else:
                Logger.log("Error : No subject found")
                return "fail"

        def GetToMailID(self):
            if Flag==True:
                print ToMailID
                return ToMailID
            else:
                Logger.log("Error : No such mail id found")
                return "fail"

        def GetBody(self):
            if Flag==True:
                print Body
                return Body
            else:
                Logger.log("Error : No Body found")
                return "fail"

##a=OutlookKeywords()
##a.GetEmail()
##a.GetFromMailId()
##a.GetToMailID()
##a.GetSubject()
##a.GetBody()
##a.GetAttachmentStatus()