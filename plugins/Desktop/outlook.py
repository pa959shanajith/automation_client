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
from outlook_constants import fldname
import string
import desktop_constants
import logging
import platform
from constants import *
import logger
import pythoncom
import threading
import core_utils
import tempfile
import os
import shutil
import fitz
log = logging.getLogger( 'outlook.py' )

AVO_ASSURE_HOME = os.environ["AVO_ASSURE_HOME"]

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

        def removeGenCache(self):
            log.info("Attempting to delete gen_py folder")
            path_gen_py=tempfile.gettempdir()+os.sep+'gen_py'
            valid = os.path.exists(path_gen_py)
            if valid:
                log.info("gen_py folder found")
                shutil.rmtree(path_gen_py)
            else:
                log.info("gen_py folder not found")

        def checkOutlook(self):
            for i in range(1,3):
                log.info("Retrying to get OutlookComObj attempt : " + str(i))
                if ( self.outlook == None):
                    log.info("Checking with OutlookComObj type 2(EnsureDispatch)")
                    self.removeGenCache()
                    self.outlook = self.getOutlookComObj(2)
                    if ( self.outlook == None):
                        log.info("Checking with OutlookComObj type 1(Dispatch)")
                        self.removeGenCache()
                        self.outlook = self.getOutlookComObj(1)
                if self.outlook:
                    log.info("outlookObj found , Success!")
                    break

        def getOutlookComObj(self, optflag):
            import pythoncom
            pythoncom.CoInitialize()
            outlookObj = None
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
                    log.debug( e )
            elif ( optflag == 3 ):
                try:
                    outlookObj = Dispatch("Outlook.Application")
                except Exception as e:
                    log.error( e )
                    logger.print_on_console(e)
            log.info("outlookObj returned is : " + str(outlookObj) )
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
                self.outlook = self.getOutlookComObj(2)
                if ( self.outlook == None ):
                    self.checkOutlook()
                #get the message stores in outlook
                stores = self.outlook.Folders
                if ( accountname != '' ):
                    for store in stores:
                        if ( store.Name == accountname ):
                            self.store = store
                            if ( folders[1].strip() in fldname.keys() ):
                                inbox_folder = self.outlook.GetDefaultFolder(outlook_constants.fldname[folders[1]])
                                index = 0
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
                                    status = desktop_constants.TEST_RESULT_PASS
                                    method_output = desktop_constants.TEST_RESULT_TRUE
                            else:
                                folder_obj = stores.Item(1)#getobj
                                def recursive_call(fld_obj,fld_name):#recursive call to get sub-folder objects
                                    new_fld_obj = fld_obj.Folders[fld_name]
                                    return new_fld_obj
                                for i in range (1,len(folders)):
                                    fld_name = folders[i]
                                    folder_obj = recursive_call(folder_obj,fld_name)
                                self.targetFolder = folder_obj
                                if ( self.targetFolder == None ):
                                    error_msg = 'Unable to find the target folder'
                                    break
                                else:
                                    status = desktop_constants.TEST_RESULT_PASS
                                    method_output = desktop_constants.TEST_RESULT_TRUE
                        else:
                            error_msg = 'Account name mismatch'
                else:
                    error_msg = 'Incorrect path'
                if ( error_msg ):
                    log.info( error_msg )
                    logger.print_on_console( error_msg )
            except Exception as e:
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
                index_flag = False
                zeroindex_flag = False
                if ( len(input)==1 ):
                    self.senderEmail = input[0]
                    self.subject = ''
                    self.toMail = ''
                if ( len(input)==2 ):
                    self.senderEmail = input[0]
                    self.toMail = input[1].strip()
                    self.subject = ''
                if ( len(input)==3 ):
                    self.senderEmail = input[0]
                    self.subject = input[2]
                    self.toMail = input[1].strip()
                if ( len(input)==4 ):
                    self.senderEmail = input[0]
                    self.subject = input[2]
                    self.toMail = input[1].strip()
                    if ( input[3]!='' and int(input[3])==0 ):
                        zeroindex_flag = True
                    elif ( input[3]!='' and int(input[3])>=1 ):
                        self.indexval = int(input[3])-1
                        index_flag = True
                #clearing all the variables before fetching the values
                Subject = ''
                ToMailID = ''
                FromMailId = ''
                AttachmentStatus = outlook_constants.ATTACH_STATUS_NO
                Body = ''
                attachment_list = []
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
                #-------------fetching sorted mails and storing in list variable mails
                if ( self.senderEmail!="" or self.subject!="" or self.toMail!="" ):
                    mails = self.messageSegregator(all_inbox, self.toMail, self.senderEmail, self.subject)
                    if zeroindex_flag:
                        error_msg = 'Please provide index value greater than 1'
                        logger.print_on_console( error_msg )
                        log.info( error_msg )
                    else:
                        if index_flag:
                            msg = mails[self.indexval] # as it is the latest msg object by date/time.
                        else:
                            msg = mails[0]
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
                        attachments_item = msg.Attachments
                        nbrOfAttachmentInMessage = attachments_item.Count
                        log.info( "total number of attachments present in the input mail is %s",str(nbrOfAttachmentInMessage) )
                        x = 1
                        img_count=0
                        non_img_count=0
                        body_image_count=0
                        while x <= nbrOfAttachmentInMessage:
                            attachment_item = attachments_item.Item(x)
                            attachment_list.append(attachment_item)
                            fn = attachment_item.FileName
                            log.info( fn )
                            filename = fn.split('.')
                            if filename[-1].lower() in ['png','jpg','gif']:
                                if ('image0' in filename[0]):
                                    body_image_count=body_image_count+1
                                else:
                                    img_count=img_count+1
                            else:
                                non_img_count=non_img_count+1
                            x+=1
                        if (non_img_count>0 or img_count>0):
                            AttachmentStatus = outlook_constants.ATTACH_STATUS_YES
                        elif ( body_image_count > img_count and body_image_count > non_img_count ):
                            AttachmentStatus = outlook_constants.ATTACH_STATUS_NO
                        try:
                                msg.Display()
                                Flag = True
                                key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)) #creating a random key of length '5'
                                self.GetEmailList.append({'Subject' : msg.Subject, 'ToMailID' : ToMailID, 'FromMailId' : FromMailId, 'AttachmentStatus' : AttachmentStatus, 'Body' : msg.Body, 'Flag' : Flag, 'Key' : key, 'Content' : msg, 'AttachmentList': attachment_list})
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
                else:
                    error_msg = 'Please provide at least one valid input parameter'
                    logger.print_on_console( error_msg )
                    log.info( error_msg )
            except Exception as e:
                logger.print_on_console( 'Error: No such mail found' )
                error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                log.error( error_msg )
                # logger.print_on_console( error_msg )
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
                    error_msg = 'Error : mail does not have such info'
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
                        objective = x
                        return objective
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
                            # from;to;subject
                            if ( To_add != '' and (From_add !="" and sub !="" ) ):
                                if ( message.Class == 43 and message.SenderName.strip() == From_add.strip() and message.Subject.strip() == sub.strip()):
                                    ToMail = message.To
                                    tomailsList = ToMail.split(';')
                                    for to in tomailsList:
                                        if ( str(to).strip() == To_add.strip() ):
                                            mSegList.append(message)
                                            break
                            # from;;
                            elif ( To_add == '' and (From_add !="" and sub =="" ) ):
                                if ( message.Class == 43 and message.SenderName.strip() == From_add.strip()):
                                    frommail = message.SenderName
                                    if ( str(From_add).strip() == frommail.strip() ):
                                        mSegList.append(message)
                            # from;to;
                            elif ( To_add != '' and (From_add !="" and sub =="" ) ):
                                if ( message.Class == 43 and message.SenderName.strip() == From_add.strip()):
                                    ToMail = message.To
                                    tomailsList = ToMail.split(';')
                                    for to in tomailsList:
                                        if ( str(to).strip() == To_add.strip() ):
                                            mSegList.append(message)
                                            break
                            # ;to;subject
                            elif ( To_add != '' and (From_add =="" and sub !="" ) ):
                                if ( message.Class == 43 and message.Subject.strip() == sub.strip()):
                                    ToMail = message.To
                                    tomailsList = ToMail.split(';')
                                    for to in tomailsList:
                                        if ( str(to).strip() == To_add.strip() ):
                                            mSegList.append(message)
                                            break
                            # ;to;
                            elif ( To_add != '' and (From_add =="" and sub =="" ) ):
                                if ( message.Class == 43 ):
                                    ToMail = message.To
                                    tomailsList = ToMail.split(';')
                                    for to in tomailsList:
                                        if ( str(to).strip() == To_add.strip() ):
                                            mSegList.append(message)
                                            break
                            # ;;subject
                            elif ( To_add == '' and (From_add =="" and sub !="" ) ):
                                if ( message.Class == 43 ):
                                    subjectmail = message.Subject
                                    if ( str(sub).strip() == subjectmail.strip() ):
                                        mSegList.append(message)
                            # from;;subject
                            else:
                                if ( message.Class == 43 and message.SenderName.strip() == From_add.strip()):
                                    subjectmail = message.Subject
                                    if ( str(sub).strip() == subjectmail.strip() ):
                                        mSegList.append(message)
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
                log.debug(len(mailSegList))
                segregatedList=timeSegregator(mailSegList)
                log.debug(len(segregatedList))
                logger.print_on_console("Number of emails that matched the input is:",len(segregatedList))
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
                        else:
                            error_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
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
                    Msgsub = MsgObj.Subject
                    if ( input == "ignore subject" ):
                        if (len(Msgsub)==0):
                            d1, d2, d3, d4 = self.send_subject(" ")
                        else:
                            d1, d2, d3, d4 = self.send_subject([Msgsub])
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
        
        def verify_attachment_content(self, input_value, *args):
            """
                def : verify_attachment_content
                purpose : verifies whether the content is present or not in the attachment specified in the input of an Email.
                param  : inputs : 1. list containing the output of the getEmail Keyword, attachment name and content to verify. 
                return : pass,true / fail,false
            """

            status = desktop_constants.TEST_RESULT_FAIL
            method_output = desktop_constants.TEST_RESULT_FALSE
            result = OUTPUT_CONSTANT
            error_msg = None
            status_flag = True
            attachment_path = None

            try:
                attachment_name = input_value[1]
                if len(input_value) == 3 and attachment_name.split('.')[-1] == 'pdf':
                    for data in self.GetEmailList:
                        if input_value[0] == data['Key'] and data['Flag'] == True and data['AttachmentStatus'] == 'Yes' and len(data['AttachmentList']) > 0:
                            for attachment in data['AttachmentList']:
                                if attachment.FileName == attachment_name:
                                    attachment_path = AVO_ASSURE_HOME + '\\' + attachment.FileName
                                    attachment.SaveAsFile(attachment_path)
                                    status_flag = False
                                    break
                            else:
                                error_msg = 'Error: Attachment name ' + attachment_name + ' is not present in the mail'
                    
                    if attachment_path is not None:
                        page_content = None
                        content_to_verify = input_value[2]
                        with fitz.open(attachment_path) as document:
                            page_content = chr(12).join([page.getText() for page in document])
                        if page_content is not None:
                            if content_to_verify in page_content.replace('\n',''):
                                logger.print_on_console(content_to_verify + " is present in the attachment " + attachment_name)
                                status = desktop_constants.TEST_RESULT_PASS
                                method_output = desktop_constants.TEST_RESULT_TRUE
                                status_flag = False
                            else:
                                error_msg = content_to_verify + " is not present in the attachment " + attachment_name

                        if os.path.isfile(attachment_path):
                            os.remove(attachment_path)
                        
                else:
                    error_msg = 'Error: Invalid Input'

                if status_flag and error_msg is None:
                    error_msg = 'Error: mail does not have such info'

                if error_msg:
                    log.info(error_msg)
                    logger.print_on_console(error_msg)
            except Exception as e:
                logger.print_on_console('Error : mail does''t have such info')
                error_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
                log.error(error_msg)
                logger.print_on_console(error_msg)

            return status, method_output, result, error_msg
