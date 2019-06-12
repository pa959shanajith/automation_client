#-------------------------------------------------------------------------------
# Name:        outlook.py
# Purpose:     To automate 'Outlook'
#
# Author:      prudhvi.gujjuboyina, anas.ahmed
#
# Created:     07-09-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016, (c) anas.ahmed 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from  win32com.client import Dispatch
import outlook_constants
from   pywintypes import  com_error
import random
import string
import desktop_constants
import logging
from constants import *
import logger
import pythoncom
import threading
import core_utils
log = logging.getLogger( 'outlook.py' )

## This class will have the methods to automate Outlook Application
class OutlookKeywords:

        def __init__(self):
            self.senderEmail = ''
            self.subject = ''
            self.toMail = ''
            self.targetFolder = None
            self.outlook = None
            self.store = None
            self.GetEmailList = []
            #----------------------sendmail
            self.sendFlag = False
            self.subjectFlag = False
            self.Msg = ''

        def getOutlookComObj(self, optflag):
            import pythoncom
            pythoncom.CoInitialize()
            if ( optflag == 1 ):
                try:
                    outlookObj = Dispatch('Outlook.Application').GetNamespace('MAPI')
                except Exception as e:
                    log.error( e )
                    logger.print_on_console(e)
            elif ( optflag == 2 ):
                try:
                    from win32com.client.gencache import EnsureDispatch
                    outlookObj = EnsureDispatch('Outlook.Application').GetNamespace('MAPI')
                except Exception as e:
                    log.error( e )
                    logger.print_on_console(e)
            elif ( optflag == 3 ):
                try:
                    outlookObj = Dispatch("Outlook.Application")
                except Exception as e:
                    log.error( e )
                    logger.print_on_console(e)

            return outlookObj



#To support seperate accounts and  subFolders this method is implemented , Input should be the folder path in properties of outlook folder
        def switchToFolder(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            error_msg = None
            result = OUTPUT_CONSTANT
            folders = []
            try:
                folderPath = input[0]
                folderPath = folderPath.strip('\\')
                folders = str(folderPath).split('\\')
                #---------------------------------
                while '' in folders:
                    folders.remove('')
                #---------------------------------
                accountname = folders[0]
##                global count
##                if count>0:
##                    import pythoncom
##                    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
##                count=count+1
                self.outlook = self.getOutlookComObj(1)
#               get the message stores in outlook
                stores = self.outlook.Stores
                if ( accountname != '' ):
                    for store in stores:
                        if ( store.DisplayName == accountname ):
                            self.store = store
                            if ( folders[1].strip() == 'Inbox' ):
                                inbox_folder = store.GetDefaultFolder(outlook_constants.INBOX_FOLDER)
                                index = 0;
                                folder = None
                                for foldername in folders:
                                    if ( index == 0 or index == 1 ):
                                        folder = inbox_folder
                                        self.targetFolder=folder
                                    else:
                                        folder = folder.Folders.Item(folders[index])
                                        self.targetFolder = self.findFolder(foldername, self.targetFolder)
                                    index += 1
                                if ( self.targetFolder == None ):
                                    error_msg = 'Unable to find the target folder'
                                    break
                                else:
                                    ##logger.print_on_console('Switched to folder')
                                    status = desktop_constants.TEST_RESULT_PASS
                                    method_output = desktop_constants.TEST_RESULT_TRUE
                            else:
                                error_msg = 'The given path is invalid'
                else:
                    error_msg = 'Check the path given'
                if ( error_msg ):
                    log.info( error_msg )
                    logger.print_on_console( error_msg )
            except Exception as e:
                logger.print_on_console( 'Check the given path' )
                error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                log.error( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, result, error_msg


        """  This method takes 3 Input Params :1.Sender Name (Display name  in Outlook application) 2.Subject  3.To whom mail has been sent On success return the mail content in string format else return fail"""
        def GetEmail(self, input, *args):
            try:
                status = desktop_constants.TEST_RESULT_FAIL
                method_output = desktop_constants.TEST_RESULT_FALSE
                result = OUTPUT_CONSTANT
                error_msg = None
                self.senderEmail = input[0]
                self.subject = input[2]
                self.toMail = input[1].strip()
                #clearing all the variables before fetching the values
                Subject = ''
                ToMailID = ''
                FromMailId = ''
                AttachmentStatus = outlook_constants.ATTACH_STATUS_NO
                Body = ''
                Flag = False
                if ( self.outlook == None ):
                     self.outlook = self.getOutlookComObj(2)
                     inbox = self.outlook.GetDefaultFolder(outlook_constants.INBOX_FOLDER)
                else:
                    inbox = self.targetFolder
                if ( inbox == None ):
                    self.outlook = self.getOutlookComObj(2)
                    inbox = self.outlook.GetDefaultFolder(outlook_constants.INBOX_FOLDER)
                all_inbox = inbox.Items
                folders = inbox.Folders
                #all_inbox=reversed(list(all_inbox))
                #-------------fetching sorted mails and storing in list variable mails
                mails = self.messageSegregator(all_inbox, self.toMail, self.senderEmail, self.subject)
                msg = mails[0] # as it is the latest msg object by date/time.
                #----------------------------------------------------------------------
                if ( msg.SenderEmailType == 'EX' ):
                    try:
                        FromMailId = msg.Sender.PropertyAccessor.GetProperty(outlook_constants.PR_SMTP_ADDRESS)
                    except:
                        pass
                else:
                    FromMailId = msg.SenderEmailAddress
                for recipient in  msg.Recipients:
                    if ( recipient.Type == 1 ):
                        ToMailID += recipient.PropertyAccessor.GetProperty(outlook_constants.PR_SMTP_ADDRESS) + ';'
                ToMailID = ToMailID[: - 1]
                if ( msg.Attachments.Count > 0 ):
                    AttachmentStatus = outlook_constants.ATTACH_STATUS_YES
                try:
                        msg.Display()
                        Flag = True
                        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)) #creating a random key of length '5'
                        self.GetEmailList.append({'Subject' : msg.Subject, 'ToMailID' : ToMailID, 'FromMailId' : FromMailId, 'AttachmentStatus' : AttachmentStatus, 'Body' : msg.Body, 'Flag' : Flag, 'Key' : key, 'Content' : msg})
                        result = key
                        status = desktop_constants.TEST_RESULT_PASS
                        method_output = desktop_constants.TEST_RESULT_TRUE
                except Exception as e:# done to handle popups and dialog boxes
                    f = e[2]
                    if ( str(f[2]) == "Outlook can't do this because a dialog box is open. Please close it and try again." ):
                        logger.print_on_console(str(f[2]))
                        error_msg = str(f[2])

                if ( Flag != True ):
                    if ( error_msg ):
                        error_msg = 'Error: No such mail found'
                        log.info( error_msg )
                        logger.print_on_console( error_msg )
            except Exception as e:
                logger.print_on_console( 'Error: No such mail found' )
                error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                log.error( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, result, error_msg

        def GetFromMailId(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            error_msg = None
            res = None
            Fail_Flag = True
            try:
                for data in self.GetEmailList:
                    if ( input[0] == data['Key'] and data['Flag'] == True ):
                        res = data['FromMailId']
                        status = desktop_constants.TEST_RESULT_PASS
                        method_output = desktop_constants.TEST_RESULT_TRUE
                        Fail_Flag = False
                if ( Fail_Flag == True ):
                    error_msg = 'Error : No such mail id found'
                    log.info( error_msg )
                    logger.print_on_console( error_msg )
            except Exception as  e:
                logger.print_on_console( 'Error : No such mail id found' )
                error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                log.error( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, res, error_msg


        def GetAttachmentStatus(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            res = None
            error_msg = None
            Fail_Flag = True
            try:
                for data in self.GetEmailList:
                    if ( len(input) == 1 ):
                        if ( input[0] == data['Key'] and data['Flag'] == True ):
                            res= data['AttachmentStatus']
                            if ( res =='Yes' ):
                                res='Present'
                            elif ( res == 'No' ):
                                res = 'Not present'
                            status = desktop_constants.TEST_RESULT_PASS
                            method_output = desktop_constants.TEST_RESULT_TRUE
                            Fail_Flag = False
                    else:
                        error_msg = 'Invalid Input'
                if ( Fail_Flag == True ):
                    logger.print_on_console( 'Error : mail does not have such info' )
                if ( error_msg ):
                    log.info( error_msg )
                    logger.print_on_console( error_msg )
            except Exception as  e:
                logger.print_on_console( 'Error : mail does''t have such info' )
                error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                log.error( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, res, error_msg

        def GetSubject(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            res = None
            error_msg = None
            Fail_Flag = True
            try:
                for data in self.GetEmailList:
                    if ( input[0] == data['Key'] and data['Flag'] == True ):
                        res = data['Subject']
                        status = desktop_constants.TEST_RESULT_PASS
                        method_output = desktop_constants.TEST_RESULT_TRUE
                        Fail_Flag = False
                if ( Fail_Flag == True ):
                    error_msg = 'Error : No subject found'
                    log.info( error_msg )
                    logger.print_on_console( error_msg )
            except Exception as  e:
                logger.print_on_console( 'Error : No subject found' )
                error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                log.error( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, res, error_msg

        def GetToMailID(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            res = None
            error_msg = None
            Fail_Flag = True
            try:
                for data in self.GetEmailList:
                    if ( input[0] == data['Key'] and data['Flag'] == True ):
                        res = data['ToMailID']
                        status = desktop_constants.TEST_RESULT_PASS
                        method_output = desktop_constants.TEST_RESULT_TRUE
                        Fail_Flag = False
                if ( Fail_Flag == True ):
                    error_msg = 'Error : No such mail id found'
                    log.info( error_msg )
                    logger.print_on_console( error_msg )
            except Exception as  e:
                logger.print_on_console( 'Error : No such mail id found' )
                error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                log.error( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, res, error_msg


        def GetBody(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            res = None
            error_msg = None
            Fail_Flag = True
            try:
                for data in self.GetEmailList:
                    if ( input[0] == data['Key'] and data['Flag'] == True ):
                        res = data['Body']
                        coreutilsobj = core_utils.CoreUtils()
                        res = coreutilsobj.get_UTF_8(res)
                        status = desktop_constants.TEST_RESULT_PASS
                        method_output = desktop_constants.TEST_RESULT_TRUE
                        Fail_Flag = False
                if ( Fail_Flag == True ):
                    error_msg = 'No Body found'
                    log.info( error_msg )
                    logger.print_on_console( error_msg )
            except Exception as  e:
                logger.print_on_console( 'Error : No Body found' )
                error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                log.error( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, res, error_msg


        def VerifyEmail(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            error_msg = None
            res = OUTPUT_CONSTANT
            Fail_Flag = True
            try:
                for data in self.GetEmailList:
                    if ( input[1] == data['Key'] and data['Flag'] == True ):
                            FilePath = input[0]
                            mail_content = self.outlook.OpenSharedItem(FilePath)
                            if ( str(data['Content'].SenderName) == str(mail_content.SenderName) and data['Content'].To == mail_content.To and data['Content'].Subject == mail_content.Subject and data['Content'].Body == mail_content.Body and str(data['Content'].Attachments) == str(mail_content.Attachments) and data['Content'].SentOn == mail_content.SentOn):
                                status = desktop_constants.TEST_RESULT_PASS
                                method_output = desktop_constants.TEST_RESULT_TRUE
                                Fail_Flag = False
                if ( Fail_Flag == True ):
                    error_msg = 'Error : No such mail found'
                    log.info( error_msg )
                    logger.print_on_console( error_msg )
            except Exception as  e:
                logger.print_on_console( 'Wrong input given' )
                error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                log.error( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, res, error_msg

        """Internal method to search for a folder in given folder"""
        def findFolder(self, folderName, searchIn):
            try:
                lowerAccount = searchIn.Folders
                for x in lowerAccount:
                    if ( x.Name == folderName ):
##                        print 'found it %s '%x.Name
                        objective = x
                        return objective
##                    else:
##                        print folderName+' folder not found'
                return None
            except Exception as error:
                logger.print_on_console( "Looks like we had an issue accessing the searchIn object" )
                return None

        """Returns a list of segregated msg com-objects"""
        """This method might return a delayed response as it has to iterate through all objects of the msg folder"""
        """Input : msg_objects[]; 'To' Address; 'Sender' Address; Subject'"""
        """Output: List of segregated message objects 'segregatedList' """
        """Reason for using this method, was because different versions of outlook ,return msg objects in different order.This method segregates the required messages and arranges them to get the last recieved mesage"""
        def messageSegregator(self, all_inbox_msgs, To_add, From_add, sub):
            segregatedList = []
            try:
                """To filtering msg objects by 'Class','SenderName' and 'Subject' address """
                """Returns a List of msg objects"""
                def mailSegregator(all_inbox_msgs, To_add, From_add,sub):
                    mSegList = []
                    try:
                        #all_inbox_msgs.Item(1).RecievedTime>all_inbox_msgs.Item(all_inbox_msgs.Count).RecieveTime
                        for message in all_inbox_msgs:
                            if ( message.Class == 43 and message.SenderName.strip() == From_add.strip() and message.Subject.strip() == sub.strip() ):
                                ToMail = message.To
                                tomailsList = ToMail.split(';')
                                for to in tomailsList:
                                    if ( str(to).strip() == To_add.strip() ):
                                        mSegList.append(message)
                                        break
                    except Exception as e:
                        log.error( 'Error at mail segregator : ' + str(e) )
                        logger.print_on_console( 'Error at mail segregator : ' + str(e) )
                        return mSegList

                """To segregate msg objects by 'To' address and then by day/date/time """
                """Returns a List of msg objects"""
                def timeSegregator(mailList):
                    times = []
                    sortedList = []
                    try:
                        for i in range(0, len(mailList)):
                            times.append(mailList[i].CreationTime)
                        sortedTime = sorted(times, reverse = True)
                        for i in range(0, len(sortedTime)):
                            for msg in mailList:
                                if ( msg.CreationTime == sortedTime[i] ):
                                    sortedList.append(msg)
                                    break
                    except Exception as e:
                       log.info( 'Error at time segregator : ' + str(e) )
                       logger.print_on_console( 'Error at time segregator : ' + str(e) )
                    return sortedList

                mailSegList=mailSegregator(all_inbox_msgs, To_add, From_add, sub)
                segregatedList=timeSegregator(mailSegList)
            except Exception as e:
                logger.print_on_console( 'Error at mail segregator' )
                log.error( desktop_constants.ERROR_MSG + ' : ' + str(e) )
                logger.print_on_console( desktop_constants.ERROR_MSG + ' : ' + str(e) )
            return segregatedList
#------------------------------------------------------------------------------------------------------------Send email function

        def send_to_mail(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            result = OUTPUT_CONSTANT
            error_msg = None
            self.sendFlag = False
            self.Msg=  ''
            MsgObj = ''
            failFlag = True
            outlookobj = self.getOutlookComObj(3)
            if ( len(input) > 1 ):
                input = ";".join(input)
            else:
                input = input[0]
                if ( len(input) == 0 ):
                    failFlag=False
            if ( failFlag == True ):
                try:
                    self.Msg = outlookobj.CreateItem(0)
                    MsgObj = self.Msg
                    MsgObj.To = input
                    self.sendFlag = True
                    status = desktop_constants.TEST_RESULT_PASS
                    method_output = desktop_constants.TEST_RESULT_TRUE
                except Exception as e:
                    error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                    log.error( error_msg )
                    logger.print_on_console( error_msg )
            else:
                error_msg = "'To...' field is not set"
                log.info( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, result, error_msg

        def send_CC(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            result = OUTPUT_CONSTANT
            error_msg =  None
            MsgObj = ''
            if ( len(input) > 1 ):
                input = ";".join(input)
            else:
                input=input[0]
            if ( self.sendFlag == True ):
                if ( len(input) > 0 ):
                    try:
                        MsgObj = self.Msg
                        MsgObj.CC = input
                        status = desktop_constants.TEST_RESULT_PASS
                        method_output = desktop_constants.TEST_RESULT_TRUE
                    except Exception as e:
                        error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                        log.error( error_msg )
                else:
                    error_msg = "Please set CC"
            else:
                error_msg = "Please set the to mail ID"
            if ( error_msg ):
                log.info( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, result, error_msg

        def send_BCC(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            result = OUTPUT_CONSTANT
            error_msg = None
            MsgObj = ''
            if ( len(input) > 1 ):
                input = ";".join(input)
            else:
                input = input[0]
            if ( self.sendFlag == True ):
                if ( len(input) > 0 ):
                    try:
                        MsgObj = self.Msg
                        MsgObj.BCC = input
                        status = desktop_constants.TEST_RESULT_PASS
                        method_output=desktop_constants.TEST_RESULT_TRUE
                    except Exception as e:
                        error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                        log.error( error_msg )
                else:
                    error_msg = "Please set BCC"
            else:
                error_msg = "Please set the to mail ID"
            if ( error_msg ):
                log.info( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, result, error_msg

        def send_subject(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            result = OUTPUT_CONSTANT
            error_msg = None
            MsgObj = ''
            sendSubject = input[0]
            if ( len(sendSubject) == 0 ):
                self.subjectFlag = False
            else:
                self.subjectFlag = True
            if ( self.sendFlag == True ):
                if ( self.subjectFlag == True ):
                    try:
                        MsgObj = self.Msg
                        MsgObj.Subject = sendSubject
                        status = desktop_constants.TEST_RESULT_PASS
                        method_output = desktop_constants.TEST_RESULT_TRUE
                    except Exception as e:
                        error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                        log.error( error_msg )
                else:
                    error_msg = "Please set the subject of the mail"
            else:
                error_msg = "Please set the to mail ID"
            if ( error_msg ):
                log.info( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, result, error_msg

        def send_body(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            result = OUTPUT_CONSTANT
            error_msg = None
            MsgObj = ''
            body = input[0]
            if ( self.sendFlag == True ):
                if ( len(body) > 0 ):
                    try:
                        MsgObj = self.Msg
                        MsgObj.Body = body
                        status = desktop_constants.TEST_RESULT_PASS
                        method_output = desktop_constants.TEST_RESULT_TRUE
                    except Exception as e:
                        error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                        log.error( error_msg )
                else:
                    error_msg = "Please set the body of the mail"
            else:
                error_msg = "Please set the to mail ID"
            if ( error_msg ):
                log.info( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, result, error_msg

        def send_attachments(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            result = OUTPUT_CONSTANT
            error_msg = None
            MsgObj = ''
            Flg = True
            if ( self.sendFlag == True ):
                if ( len(input) > 0 ):
                    try:
                        MsgObj = self.Msg
                        for i in input:
                            try:
                                MsgObj.Attachments.Add(i)
                            except:
                                Flg = False
                        if ( Flg == True ):
                            status = desktop_constants.TEST_RESULT_PASS
                            method_output = desktop_constants.TEST_RESULT_TRUE
                    except Exception as e:
                        error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                        log.error( error_msg )
                else:
                    error_msg = "Please set the attachment path"
            else:
                error_msg = "Please set the to mail ID"
            if ( error_msg ):
                log.info( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, result, error_msg

        def send_mail(self, input, *args):
            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            result = OUTPUT_CONSTANT
            error_msg = None
            input = str(input[0]).lower().strip()
            MsgObj = ''
            if ( self.sendFlag == True ):
                try:
                    MsgObj = self.Msg
                    if ( input == "ignore subject" ):
                        d1, d2, d3, d4 = self.send_subject(" ")
                        if ( self.subjectFlag == True ):
                            MsgObj.Display()
                            import time
                            time.sleep(5)
                            MsgObj.Send()
                            status = desktop_constants.TEST_RESULT_PASS
                            method_output = desktop_constants.TEST_RESULT_TRUE
                    else:
                        MsgObj.Display()
                        import time
                        time.sleep(5)
                        MsgObj.Send()
                        status = desktop_constants.TEST_RESULT_PASS
                        method_output = desktop_constants.TEST_RESULT_TRUE
                except Exception as e:
                    error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                    log.error( error_msg )
            else:
                error_msg = "Please set the to mail ID"
            if ( error_msg ):
                log.info( error_msg )
                logger.print_on_console( error_msg )
            return status, method_output, result, error_msg