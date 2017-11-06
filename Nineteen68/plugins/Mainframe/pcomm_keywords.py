#-------------------------------------------------------------------------------
# Name:        pcomm_keywords.py
# Purpose:     Seperate class to perform automation on Pcomm Emulator
#
# Author:      wasimakram.sutar
#
# Created:     30/10/2017
# Copyright:   (c) wasimakram.sutar 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import win32com.client
import os
from ctypes import *
from sys import *
import logging
from hllApi import HllApi
from mainframe_constants import *

import logger
import logging
log = logging.getLogger('pcomm_keywords.py')

class PcommKeywords:

    def __init__(self):
        """The instantiation operation __init__ creates an empty object of the class PcommKeywords
            when it is instantiated"""
        self.emulator_path = ''
        self.host = None

    def launch_mainframe(self,emulator_path):
        #Logic to launch Bluezone Emulator goes here
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            import pythoncom
            #co- initializing the pythoncom object, this is required to overcome the issue running of client.Dispatch more then
            #one time on same instance.
            pythoncom.CoInitialize()
            self.host = win32com.client.Dispatch("BZWhll.WhllObj")
            self.host.OpenSession(0, 1,emulator_path, 30, 1 )
            return_value = self.host.Connect( HOST_A )
        except Exception as e:
            log.error("Error: Unable to launch mainframe.")
            log.error(e)
            err_msg = "Error: Unable to launch mainframe."
            logger.print_on_console("Error: Unable to launch mainframe.")
        return (return_value == 0),output,err_msg

    def login(self,region,userID,password):
        #Logic to Login to Bluezone Emulator goes here
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = 0
        try:
            self.host.sendkeys(region)
            self.host.Waitready(10,2000)
            self.host.sendkeys(MAINFRAME_KEY_E)
            self.host.Waitready(10,2000)
            self.host.sendkeys(userID)
            self.host.Waitready(10,1000)
            self.host.sendkeys(MAINFRAME_KEY_E)
            self.host.Waitready(10,1000)
            self.host.sendkeys(password)
            self.host.Waitready(10,1000)
            self.host.sendkeys(MAINFRAME_KEY_E)
            self.host.Waitready(10,1000)
            self.host.sendkeys(MAINFRAME_KEY_E)
            self.host.Waitready(10,1000)
            uidchk = self.host.WaitForText(userID, (6, 20,5000))
            if uidchk == 4:
                 self.host.Waitready(10,2000)
                 self.host.sendkeys(password)
                 self.host.Waitready(10,2000)
                 self.host.sendkeys(MAINFRAME_KEY_ENTER)
                 pwdchk = self.host.WaitForText(MAINFRAME_NOT_AUTHORISED, (02, 21,5000))
                 if pwdchk.value:
                    self.host.Waitready(10,2000)
                    self.host.sendkeys(MAINFRAME_KEY_3)
                    self.host.Waitready(10,2000)
                    err_msg=MAINFRAME_LOGIN_FAIL
                 else:
                    self.host.Waitready(10,2000)
                    self.host.sendkeys(MAINFRAME_KEY_ENTER)
                    return_value = 1
            else:
                 self.host.Waitready(10,2000)
                 self.host.sendkeys(MAINFRAME_KEY_3)
                 log.info(MAINFRAME_WRONG_USERID)
                 err_msg=MAINFRAME_WRONG_USERID
        except Exception as e:
            log.error("Error: Unable to login to mainframe.")
            log.error(e)
            err_msg = "Error: Unable to login to mainframe."
            logger.print_on_console("Error: Unable to login to mainframe.")
        return (return_value == 1),output,err_msg


    def logoff(self,option):
        #Logic to Login to Bluezone Emulator goes here
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = 0
        try:
            buffer_var = ''
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_3)
            scrncnt = self.host.ReadScreen(Buf1,5,1,2)
            if scrncnt == MAINFRAME_READY:
               self.host.WaitReady(10,1000)
               self.host.SendKeys(MAINFRAME_LOGOFF)
               self.host.WaitReady(10,1000)
               self.host.SendKeys(MAINFRAME_KEY_E)
               logger.print_on_console(MAINFRAME_LOGOFF_MESSAGE)
               log.info(MAINFRAME_LOGOFF_MESSAGE)
               return_value = 1

            else:
                 self.host.SendKeys(option)
                 self.host.WaitReady(10,1000)
                 self.host.SendKeys(MAINFRAME_KEY_E)
                 self.host.WaitReady(10,1000)
                 self.host.Setcursor(3,1)
                 self.host.WaitReady(10,1000)
                 self.host.SendKeys(MAINFRAME_LOGOFF)
                 self.host.WaitReady(10,1000)
                 self.host.SendKeys(MAINFRAME_KEY_E)
                 logger.print_on_console( MAINFRAME_LOGOFF_MESSAGE)
                 log.info(MAINFRAME_LOGOFF_MESSAGE)
                 return_value = 1
        except Exception as e:
            log.error("Error: Unable to logoff from mainframe.")
            log.error(e)
            err_msg = "Error: Unable to logoff from mainframe."
            logger.print_on_console("Error: Unable to logoff from mainframe.")
        return (return_value == 1),output,err_msg

    def send_value(self,text):
        #Logic to Login to Bluezone Emulator goes here
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = 0
        try:
            self.host.SendKeys(text)
            self.host.WaitReady(10,1000)
            logger.print_on_console( MAINFRAME_SENDVALUE)
            log.info(MAINFRAME_SENDVALUE)
            return_value = 1
        except Exception as e:
            log.error("Error: Unable to send value to the Emulator screen.")
            log.error(e)
            err_msg = "Error: Unable to send value to the Emulator screen."
            logger.print_on_console("Error: Unable to send value to the Emulator screen.")
        return (return_value == 1),output,err_msg

    def set_text(self,row_number,column_number,text):
        #Logic to set the text at the specified location
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = 0
        try:
            buffer_var = ''
            row_number = int(row_number)
            column_number = int(column_number)
            self.host.SetCursor(row_number, column_number)
            self.host.Waitready(10,1000)
            self.host.SendKeys(text)
            textlength = len(text)
            output_text = self.host.ReadScreen(buffer_var,textlength,row_number,column_number)
            if text == output_text[1]:
                logger.print_on_console(MAINFRAME_SET_TEXT)
                log.info(MAINFRAME_SET_TEXT)
                return_value = 1
            else:
                self.host.SendKeys(MAINFRAME_KEY_R)
                self.host.SendKeys(MAINFRAME_KEY_0)
                logger.print_on_console(MAINFRAME_FAIL_RESPONSE + MAINFRAME_TEXT_FAIL_TO_SET)
                log.info(MAINFRAME_FAIL_RESPONSE + MAINFRAME_TEXT_FAIL_TO_SET)
                err_msg=MAINFRAME_TEXT_FAIL_TO_SET
        except Exception as e:
            log.error("Error: Unable to set text to the Emulator screen.")
            log.error(e)
            err_msg = "Error: Unable to set text to the Emulator screen."
            logger.print_on_console("Error: Unable to set text to the Emulator screen.")
        return (return_value == 1),output,err_msg

    def send_function_keys(self,function_key):
        #Logic for send_function_keys
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = 0
        try:
            self.host.Waitready(10,1000)
            self.host.Focus
            self.host.SendKeys(function_key)
            log.info(MAINFRAME_PRESS_FUNCTION_KEY)
            return_value = 1

        except Exception as e:
            log.error("Error: Unable to send function key to the Emulator screen.")
            log.error(e)
            err_msg = "Error: Unable to send function key to the Emulator screen."
            logger.print_on_console("Error: to send function key to the Emulator screen.")
        return (return_value == 1),output,err_msg

    def get_text(self,row_number,column_number,length):
        #Logic to get the text at the specified location
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = 0
        try:
            buffer_var = ''
            row_number = int(row_number)
            column_number = int(column_number)
            length = int(length)
            output_text = self.host.ReadScreen(buffer_var,length,row_number,column_number)
            output = output_text[1]
            log.info("Output text = %s",output)
            logger.print_on_console("Output text = "+output)
            return_value = 1
        except Exception as e:
            if isinstance(e,ValueError):
                log.error("Error: Row number,Column number and Length of the text should be integer.")
                log.error(e)
                err_msg = "Error: Row number,Column number and Length of the text should be integer."
                logger.print_on_console("Error: Row number,Column number and Length of the text should be integer.")
            else:
                log.error("Error: Unable to get the text from Emulator screen.")
                log.error(e)
                err_msg = "Error: Unable to get the text from Emulator screen."
                logger.print_on_console("Error: to get the text from Emulator screen.")
        return (return_value == 1),output,err_msg

    def verify_text_exists(self,text):
        #Logic to verify the text present in screen
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = 0
        try:
            row_number = 1
            column_number = 1
            self.host.WaitReady(10,1000)
            output_dict = self.host.Search(text,row_number,column_number)
            self.host.WaitReady(10,1000)
            if output_dict[2] == 1:
                return_value = 1
                logger.print_on_console(MAINFRAME_TEXT_VERIFIED)
                log.info(MAINFRAME_TEXT_VERIFIED)
            else:
                err_msg=MAINFRAME_TEXT_MISMATCHED
                logger.print_on_console(err_msg)
        except Exception as e:
            log.error("Error: Unable to verify the text present in Emulator screen.")
            log.error(e)
            err_msg = "Error: Unable to verify the text present in Emulator screen."
            logger.print_on_console("Unable to verify the text present in Emulator screen.")
        return (return_value == 1),output,err_msg

    def submit_job(self,job_path,member_name):
        #Logic to submit the job
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = 0
        try:
            buffer_var = ''
            self.host.SendKeys(MAINFRAME_KEY_3_4)
            self.host.SendKeys(MAINFRAME_KEY_E)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_T)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_F)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(job_path)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_E)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_f)
            self.host.SendKeys(job_path)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_E)
            self.host.WaitReady(10,1000)
            file_status =  self.host.WaitForText((job_path), (8, 11, 5000))
            jobno = None
            if file_status== True:
                self.host.Setcursor(8,2)
                self.host.SendKeys(MAINFRAME_KEY_V)
                self.host.WaitReady(10,1000)
                self.host.SendKeys(MAINFRAME_KEY_E)
                self.host.WaitReady(10,1000)
                self.host.SendKeys(MAINFRAME_KEY_f)
                self.host.SendKeys(member_name)
                self.host.WaitReady(10,2000)
                self.host.SendKeys(MAINFRAME_KEY_E)
                self.host.WaitReady(10,2000)
                jobname = self.host.ReadScreen(buffer_var,8,6,12)
                self.host.WaitReady(10,1000)
                if jobname[1] == member_name:
                    self.host.SendKeys(MAINFRAME_KEY_T)
                    self.host.WaitReady(5,100)
                    self.host.SendKeys(MAINFRAME_KEY_T)
                    self.host.SendKeys(MAINFRAME_KEY_SUB)
                    self.host.SendKeys(MAINFRAME_KEY_E)
                    ResultCode = self.host.WaitForText(MAINFRAME_KEY_IKJ,1, 1, 1000)
                    self.host.WaitReady(10,1000)
                    #global jobno
                    if ResultCode:
                        content1 =self.host.ReadScreen(buffer_var,8,1,25)
                        jobno = content1[1]
                        return_value = 1
                        output=jobno
                    else:
                        content = self.host.ReadScreen(buffer_var,8,21,25)
                        #Logger.log( 'Job Number :',jobno)
                        log.debug('Job Number :',jobno)
                        jobno = content[1]
                        self.host.WaitReady(10,1000)
                        self.host.SendKeys(MAINFRAME_KEY_E)
                        return_value = 1
                        output=jobno

                        #return jobno
                else:
                    self.host.SendKeys(MAINFRAME_KEY_3)
                    self.host.WaitReady(10,1000)
                    self.host.SendKeys(MAINFRAME_KEY_3)
                    self.host.WaitReady(10,1000)
                    self.host.SendKeys(MAINFRAME_KEY_3)
                    #Logger.log( MAINFRAME_JOB_NOT_FOUND)
                    #return MAINFRAME_JOB_NOT_FOUND
                    log.info(MAINFRAME_JOB_NOT_FOUND)
                    err_msg=MAINFRAME_JOB_NOT_FOUND
            else:
                self.host.SendKeys(MAINFRAME_KEY_3)
                self.host.WaitReady(10,1000)
                self.host.SendKeys(MAINFRAME_KEY_3)
                self.host.WaitReady(10,1000)
                #Logger.log(MAINFRAME_FILE_NOT_FOUND)
                #return MAINFRAME_FILE_NOT_FOUND
                log.info(MAINFRAME_FILE_NOT_FOUND)
                err_msg=MAINFRAME_FILE_NOT_FOUND
        except Exception as e:
            log.error("Error: Unable to Submit the job.")
            log.error(e)
            err_msg = "Error: Unable to Submit the job."
            logger.print_on_console("Unable to Submit the job.")
        return (return_value == 1),output,err_msg

    def job_status(self,job_no):
        #Logic to submit the job
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = 0
        try:
            buffer_var = ''
            self.host.WaitReady(10,1000)
            self.host.WaitReady(10,1000)
            self.host.Setcursor(4,15)
            self.host.SendKeys(MAINFRAME_KEY_M_5)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_E)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_ST)
            self.host.SendKeys(MAINFRAME_KEY_E)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_FILTER_JOBID)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(job_no)
            self.host.SendKeys(MAINFRAME_KEY_E)
            self.host.WaitReady(10,1000)
            self.host.Setcursor(6,25)
            status = self.host.ReadScreen(Buf1,7,6,25)
            job_status = status[1]
            if job_status != " ":
                logger.print_on_console('Job Status :'+ jobStat+MAINFRAME_JOB_COMPLETED)
                log.info('Job Status : %s',jobStat+MAINFRAME_JOB_COMPLETED)
                return_value = 1
                output=jobStat
            else:
                logger.print_on_console('Job Status :' + jobStat+MAINFRAME_JOB_NOT_COMPLETED)
                log.info('Job Status : %s',jobStat+MAINFRAME_JOB_NOT_COMPLETED)
                err_msg=MAINFRAME_JOB_NOT_COMPLETED
        except Exception as e:
            log.error("Error: Unable to retrieve job status.")
            log.error(e)
            err_msg = "Error: Unable to retrieve job status."
            logger.print_on_console("Unable to retrieve job status.")
        return (return_value == 1),output,err_msg

    def set_cursor(self,row_number,column_number):
        #Logic to submit the job
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = 0
        try:
            row_number = int(row_number)
            column_number = int(column_number)
            self.host.WaitReady(10,1000)
            self.host.SetCursor(row_number,column_number)
            self.host.WaitReady(10,1000)
            return_value = 1
        except Exception as e:
            if isinstance(e,ValueError):
                log.error("Error: Row number and Column number should be integer.")
                log.error(e)
                err_msg = "Error: Row numberand Column number should be integer."
                logger.print_on_console("Error: Row number and Column number should be integer.")
            else:
                log.error("Error: Unable to set the cursor on Emulator screen.")
                log.error(e)
                err_msg = "Error: Unable to set the cursor on Emulator screen."
                logger.print_on_console("Unable to set the cursor on Emulator screen.")
        return (return_value == 1),output,err_msg








