#-------------------------------------------------------------------------------
# Name:        bluezone_keywords.py
# Purpose:     Seperate class to perform automation on Bluezone Emulator
#
# Author:      ranjan.agrawal
#
# Created:     15-02-2018
# Copyright:   (c) ranjan.agrawal 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import json
import time
import socket
import pythoncom
import win32com.client
import subprocess
from mainframe_constants import *
import logger
import logging
import core_utils
from ctypes import *
from sys import *
emulator = None
soc_api = None
core_utils_obj = core_utils.CoreUtils()

import logger
import logging
log = logging.getLogger('bluezone_keywords.py')

func_keys = {}
func_keys.update(MAINFRAME_FN_KEYS)
func_keys.update(EHLLAPI_MNEMONICS)

class BluezoneKeywords:

    def __init__(self):
        """The instantiation operation __init__ creates an empty object of the class Bluezonekeywords
            when it is instantiated"""
        self.emulator_path = ''
        self.emulator_type = ''
        self.host = None
        self.rows = 0
        self.cols = 0

    def launch_mainframe(self,emulator_path,emulator_type):
        #Logic to launch Bluezone Emulator goes here
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            # Co-Initializing the pythoncom object, this is required to overcome the issue running of client.
            # Dispatch more then one time on same instance.
            pythoncom.CoInitialize()
            self.emulator_path = emulator_path
            self.emulator_type = emulator_type
            self.host = win32com.client.Dispatch("BZWhll.WhllObj")
            self.host.OpenSession(0, 1, self.emulator_path, 30, 1)
            return_value = self.host.Connect()
            if return_value == 1:
                err_msg = "Error: Unable to connect to default Emulator session. Use 'connect_session' keyword."
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error: Unable to launch " + self.emulator_type + " Mainframe."
            if (type(e).__name__ == "com_error") and ("Class not registered" in str(e)):
                output = "x86"
                err_msg = err_msg[:-1]+" in 64-bit mode. Trying again in 32 bit-mode."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def connect_session(self,psid):
        #Logic to connect to specific Bluezone Emulator Session goes here
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            self.host_id = psid
            self.host.Disconnect()
            return_value = self.host.Connect()
        except Exception as e:
            err_msg = "Error: Unable to connect to Emulator."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def login(self,region,userID,password):
        #Logic to Login to Bluezone Emulator goes here
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            region = region.replace("@","@@")
            userID = userID.replace("@","@@")
            password = password.replace("@","@@")
            return_value = self.host.sendkeys(region)
            if return_value == 1:
                err_msg = MAINFRAME_CLIENT_NOT_CON
                log.error(err_msg)
                logger.print_on_console(err_msg)
            else:
                self.host.Waitready(10,2000)
                self.host.sendkeys(MAINFRAME_KEY_ENTER)
                self.host.Waitready(10,2000)
                self.host.sendkeys(userID)
                self.host.Waitready(10,1000)
                self.host.sendkeys(MAINFRAME_KEY_ENTER)
                self.host.Waitready(10,1000)
                self.host.sendkeys(password)
                self.host.Waitready(10,1000)
                self.host.sendkeys(MAINFRAME_KEY_ENTER)
                self.host.Waitready(10,1000)
                self.host.sendkeys(MAINFRAME_KEY_ENTER)
                self.host.Waitready(10,1000)
                uidchk = self.host.WaitForText(userID, (6, 20,5000))
                if uidchk == 4:
                     self.host.Waitready(10,2000)
                    #  self.host.sendkeys(password)
                    #  self.host.Waitready(10,2000)
                    #  self.host.sendkeys(MAINFRAME_KEY_ENTER)
                     pwdchk = self.host.WaitForText(MAINFRAME_NOT_AUTHORISED, (0o2, 21,5000))
                     if pwdchk == 4:
                        self.host.Waitready(10,2000)
                        self.host.sendkeys(MAINFRAME_KEY_F3)
                        self.host.Waitready(10,2000)
                        err_msg=MAINFRAME_LOGIN_FAIL
                     else:
                        self.host.Waitready(10,2000)
                        self.host.sendkeys(MAINFRAME_KEY_ENTER)
                        return_value = 0
                else:
                     self.host.Waitready(10,2000)
                     self.host.sendkeys(MAINFRAME_KEY_F3)
                     log.info(MAINFRAME_WRONG_USERID)
                     err_msg=MAINFRAME_WRONG_USERID
        except Exception as e:
            err_msg = "Error: Unable to login into Emulator."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def logoff(self,option):
        #Logic to Login to Bluezone Emulator goes here
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            return_value = self.host.WaitReady(10,1000)
            if return_value == 1:
                err_msg = MAINFRAME_CLIENT_NOT_CON
                log.error(err_msg)
                logger.print_on_console(err_msg)
            else:
                self.host.SendKeys(MAINFRAME_KEY_F3)
                scrncnt = self.host.ReadScreen('',5,1,2)
                if scrncnt != MAINFRAME_READY:
                    self.host.SendKeys(option)
                    self.host.WaitReady(10,1000)
                    self.host.SendKeys(MAINFRAME_KEY_ENTER)
                    self.host.WaitReady(10,1000)
                    self.host.Setcursor(3,1)
                self.host.WaitReady(10,1000)
                self.host.SendKeys(MAINFRAME_LOGOFF)
                self.host.WaitReady(10,1000)
                self.host.SendKeys(MAINFRAME_KEY_ENTER)
                logger.print_on_console( MAINFRAME_LOGOFF_MESSAGE)
                log.info(MAINFRAME_LOGOFF_MESSAGE)
                return_value = 0
        except Exception as e:
            err_msg = "Error: Unable to logoff from Emulator."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def send_value(self,text):
        #Logic to Login to Bluezone Emulator goes here
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = 0
        try:
            text=text.replace("@","@@")
            self.host.SendKeys(text)
            self.host.WaitReady(10,1000)
            logger.print_on_console( MAINFRAME_SENDVALUE)
            log.info(MAINFRAME_SENDVALUE)
            return_value = 1
        except Exception as e:
            err_msg = "Error: Unable to send value to the Emulator screen."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
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
            err_msg = "Error: Unable to set text to the Emulator screen."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 1),output,err_msg

    def send_function_keys(self,function_key,number):
        #Logic for send_function_keys
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = 0
        try:
            if function_key in func_keys:
                function_key = func_keys[function_key]
                for i in range(int(number)):
                    self.host.Waitready(10,1000)
                    self.host.Focus
                    self.host.SendKeys(function_key)
                    log.info(MAINFRAME_PRESS_FUNCTION_KEY)
                return_value = 1
            else:
                err_msg = "Error: Invalid function key '"+function_key+"' provided."
                log.error(err_msg)
                logger.print_on_console(err_msg)
                logger.print_on_console("Supported keys are: "+str(", ".join(list(func_keys.keys()))))
        except Exception as e:
            err_msg = "Error: Unable to send function key to the Emulator screen."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 1),output,err_msg

    def get_text(self,row_number,column_number,length):
        #Logic to get the text at the specified location
        err_msg=None
        output=None
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
                err_msg = "Error: Row number, Column number and Length of the text should be integer."
            else:
                err_msg = "Error: Unable to get the text from Emulator screen."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
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
            if output_dict[0] == 0:
                return_value = 1
                logger.print_on_console(MAINFRAME_TEXT_VERIFIED)
                log.info(MAINFRAME_TEXT_VERIFIED)
            else:
                err_msg=MAINFRAME_TEXT_MISMATCHED
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error: Unable to verify the text present in Emulator screen."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 1),output,err_msg

    def submit_job(self,job_path,member_name):
        #Logic to submit the job
        err_msg=None
        output=None
        return_value = 0
        try:
            buffer_var = ''
            self.host.SendKeys(MAINFRAME_KEY_3_4)
            self.host.SendKeys(MAINFRAME_KEY_ENTER)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_T)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_F)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(job_path)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_ENTER)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_f)
            self.host.SendKeys(job_path)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_ENTER)
            self.host.WaitReady(10,1000)
            file_status =  self.host.WaitForText((job_path), (8, 11, 5000))
            jobno = None
            if file_status== 4 or file_status== True:
                self.host.Setcursor(8,2)
                self.host.SendKeys(MAINFRAME_KEY_V)
                self.host.WaitReady(10,1000)
                self.host.SendKeys(MAINFRAME_KEY_ENTER)
                self.host.WaitReady(10,1000)
                self.host.SendKeys(MAINFRAME_KEY_f)
                self.host.SendKeys(member_name)
                self.host.WaitReady(10,2000)
                self.host.SendKeys(MAINFRAME_KEY_ENTER)
                self.host.WaitReady(10,2000)
                jobname = self.host.ReadScreen(buffer_var,8,6,12)
                self.host.WaitReady(10,1000)
                if jobname[1].strip().lower() == member_name:
                    self.host.SendKeys(MAINFRAME_KEY_T)
                    self.host.WaitReady(5,100)
                    self.host.SendKeys(MAINFRAME_KEY_T)
                    self.host.SendKeys(MAINFRAME_KEY_SUB)
                    self.host.SendKeys(MAINFRAME_KEY_ENTER)
                    ResultCode = self.host.WaitForText(MAINFRAME_KEY_IKJ,1, 1, 1000)
                    self.host.WaitReady(10,1000)
                    if ResultCode:
                        content1 =self.host.ReadScreen(buffer_var,8,1,25)
                        jobno = content1[1]
                        return_value = 1
                        output=jobno
                    else:
                        content = self.host.ReadScreen(buffer_var,8,21,25)
                        log.debug('Job Number :' + str(jobno))
                        jobno = content[1]
                        self.host.WaitReady(10,1000)
                        self.host.SendKeys(MAINFRAME_KEY_ENTER)
                        return_value = 1
                        output=jobno
                else:
                    self.host.SendKeys(MAINFRAME_KEY_F3)
                    self.host.WaitReady(10,1000)
                    self.host.SendKeys(MAINFRAME_KEY_F3)
                    self.host.WaitReady(10,1000)
                    self.host.SendKeys(MAINFRAME_KEY_F3)
                    err_msg=MAINFRAME_JOB_NOT_FOUND
                    log.info(err_msg)
                    logger.print_on_console(err_msg)
            else:
                self.host.SendKeys(MAINFRAME_KEY_F3)
                self.host.WaitReady(10,1000)
                self.host.SendKeys(MAINFRAME_KEY_F3)
                self.host.WaitReady(10,1000)
                err_msg=MAINFRAME_FILE_NOT_FOUND
                log.info(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error: Unable to Submit the job."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 1),output,err_msg

    def job_status(self,job_no):
        #Logic to submit the job
        err_msg=None
        output=None
        return_value = 0
        try:
            self.host.WaitReady(10,1000)
            self.host.WaitReady(10,1000)
            self.host.Setcursor(4,15)
            self.host.SendKeys(MAINFRAME_KEY_M_5)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_ENTER)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_ST)
            self.host.SendKeys(MAINFRAME_KEY_ENTER)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(MAINFRAME_KEY_FILTER_JOBID)
            self.host.WaitReady(10,1000)
            self.host.SendKeys(job_no)
            self.host.SendKeys(MAINFRAME_KEY_ENTER)
            self.host.WaitReady(10,1000)
            #self.host.Setcursor(6,25)
            status = self.host.ReadScreen('',7,6,25)
            job_status = status[1]
            if job_status != " ":
                logger.print_on_console('Job Status :'+ job_status+MAINFRAME_JOB_COMPLETED)
                log.info('Job Status : %s',job_status+MAINFRAME_JOB_COMPLETED)
                return_value = 1
                output=job_status
            else:
                logger.print_on_console('Job Status :' + job_status+MAINFRAME_JOB_NOT_COMPLETED)
                log.info('Job Status : %s',job_status+MAINFRAME_JOB_NOT_COMPLETED)
                err_msg=MAINFRAME_JOB_NOT_COMPLETED
        except Exception as e:
            err_msg = "Error: Unable to retrieve job status."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
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
                err_msg = "Error: Row number and Column number should be integer."
            else:
                err_msg = "Error: Unable to set the cursor on Emulator screen."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 1),output,err_msg

    def disconnect_session(self):
        #Logic to disconnect from Bluezone Emulator goes here
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            return_value = self.host.Disconnect()
        except Exception as e:
            err_msg = "Error: Unable to disconnect from Emulator."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def close_mainframe(self):
        #Logic to close Bluezone Emulator Session goes here
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            return_value = self.host.CloseSession(0,1)
        except Exception as e:
            err_msg = "Error: Unable to close emulator."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg


class BluezoneAPIKeywords:

    def __init__(self):
        """The instantiation operation __init__ creates an empty object of the class BluezoneAPIKeywords
            when it is instantiated"""
        self.emulator_path = ''
        self.emulator_type = ''
        self.host = None
        self.rows = 0
        self.cols = 0

    def launch_mainframe(self,emulator_path,emulator_type):
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            self.emulator_path = emulator_path
            self.emulator_type = emulator_type
            check_n_init(self.emulator_type)
            data = dataTransmitter("launchmainframe", self.emulator_path)
            return_value = data["stat"]
            time.sleep(5)
            if return_value == 0:
                self.get_screen_resolution()
                log.info(LAUNCH_MAINFRAME_SUCCESS_MESSAGE)
                logger.print_on_console(LAUNCH_MAINFRAME_SUCCESS_MESSAGE)
            else:
                err_msg = "Error: "+data["emsg"]
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error: Unable to launch " + self.emulator_type + " Mainframe."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def connect_session(self,psid):
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            self.host = psid
            data = dataTransmitter("connectsession", self.host)
            return_value = data["stat"]
            if return_value == 0:
                self.get_screen_resolution()
                log.info(MAINFRAME_SESSION_CONNECTED)
                logger.print_on_console(MAINFRAME_SESSION_CONNECTED)
            else:
                err_msg = "Error: "+data["emsg"]
                log.debug("Return Value is "+str(return_value))
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error: Unable to connect to " + self.emulator_type + " Mainframe."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def get_screen_resolution(self):
        try:
            data = dataTransmitter("getspacesize", self.host)
            if data["stat"] == 0:
                self.rows = int(data["res"][0])
                self.cols = int(data["res"][1])
                res_msg = "Screen resolution is identified as "+str(self.rows)+"x"+str(self.cols)
                log.info(res_msg)
                logger.print_on_console(res_msg)
            else:
                self.rows = 24
                self.cols = 80
                log.error(MAINFRAME_RESOLUTION_FAIL)
                logger.print_on_console(MAINFRAME_RESOLUTION_FAIL)
                res_msg = "Switching to Default resolution: "+str(self.rows)+"x"+str(self.cols)
                log.info(res_msg)
                logger.print_on_console(res_msg)
        except Exception as e:
            err_msg = MAINFRAME_RESOLUTION_FAIL
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)

    def login(self,region,userID,password):
        err_msg = None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            region = region.replace("@","@@")
            userID = userID.replace("@","@@")
            password = password.replace("@","@@")
            data = dataTransmitter("sendvalue", [region, MAINFRAME_KEY_ENTER])
            stat = data["stat"]
            if stat == 0:
                dataTransmitter("sendvalue", [userID, MAINFRAME_KEY_ENTER, password, MAINFRAME_KEY_ENTER, MAINFRAME_KEY_ENTER])
                uidcheck = dataTransmitter("waitfortext", userID, 6, 20, 5)
                if uidcheck["stat"] == 4:
                    dataTransmitter("sendvalue", [password, MAINFRAME_KEY_ENTER])
                    pwdcheck = dataTransmitter("waitfortext", MAINFRAME_NOT_AUTHORISED, 2, 21, 5)
                    if pwdcheck["stat"] == 4:
                        dataTransmitter("sendvalue", MAINFRAME_KEY_ENTER)
                        return_value = 0
                    else:
                        dataTransmitter("sendvalue", [MAINFRAME_KEY_F3])
                        err_msg = MAINFRAME_LOGIN_FAIL
                else:
                    dataTransmitter("sendvalue", MAINFRAME_KEY_F3)
                    err_msg = MAINFRAME_WRONG_USERID
            else:
                err_msg = "Error: "+data["emsg"]
                log.debug("Return Value is "+str(stat))
            if err_msg != 0:
                err_msg = "Error: Unable to login into " + self.emulator_type + " Mainframe."
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error: Unable to login into " + self.emulator_type + " Mainframe."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def logoff(self,option):
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            data = dataTransmitter("sendvalue", MAINFRAME_KEY_F3)
            stat = data["stat"]
            if stat == 0:
                scrncnt = dataTransmitter("gettext", 5, 1, 2)
                if scrncnt["res"] != MAINFRAME_READY:
                    dataTransmitter("sendvalue", [option, MAINFRAME_KEY_ENTER])
                    dataTransmitter("setcursor", 3, 1)
                data = dataTransmitter("sendvalue", [MAINFRAME_LOGOFF,MAINFRAME_KEY_ENTER])
                logger.print_on_console(MAINFRAME_LOGOFF_MESSAGE)
                log.info(MAINFRAME_LOGOFF_MESSAGE)
                return_value = 0
            else:
                err_msg = "Error: "+data["emsg"]
                log.debug("Return Value is "+str(stat))
            if err_msg is not None:
                err_msg = "Error: Unable to logoff from " + self.emulator_type + " Mainframe."
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error: Unable to logoff from " + self.emulator_type + " Mainframe."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def send_value(self,text):
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            text=text.replace("@","@@")
            data = dataTransmitter("sendvalue", text)
            return_value = data["stat"]
            if return_value == 0:
                log.info(MAINFRAME_SENDVALUE)
                logger.print_on_console(MAINFRAME_SENDVALUE)
            else:
                err_msg = "Error: "+data["emsg"]
                log.debug("Return Value is "+str(return_value))
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error: Unable to send value to the Emulator screen."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def set_text(self,row_number,column_number,text):
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            data = dataTransmitter("settext", text, int(row_number), int(column_number))
            stat = data["stat"]
            if stat == 0:
                textlength = len(text)
                output_text = dataTransmitter("gettext", textlength, row_number, column_number)
                if text == output_text["res"]:
                    logger.print_on_console(MAINFRAME_SET_TEXT)
                    log.info(MAINFRAME_SET_TEXT)
                    return_value = 0
                else:
                    dataTransmitter("sendvalue", [MAINFRAME_KEY_R, MAINFRAME_KEY_0])
                    err_msg=MAINFRAME_TEXT_FAIL_TO_SET
                    logger.print_on_console("Fail: " + err_msg)
                    log.info("Fail: " + err_msg)
            else:
                err_msg = "Error: "+data["emsg"]
                log.debug("Return Value is "+str(stat))
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error: Unable to set text to the Emulator screen."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def send_function_keys(self,function_key,number):
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            if function_key in func_keys:
                text = func_keys[function_key]
                for i in range(int(number)):
                    data = dataTransmitter("sendvalue", text)
                    return_value = data["stat"]
                    if return_value == 0:
                        log.info(MAINFRAME_PRESS_FUNCTION_KEY)
                        logger.print_on_console(MAINFRAME_PRESS_FUNCTION_KEY)
                    else:
                        err_msg = "Error: "+data["emsg"]
                        break
                if err_msg is not None:
                    log.error(err_msg)
                    log.debug("Return Value is "+str(return_value))
                    logger.print_on_console(err_msg)
            else:
                err_msg = "Error: Invalid function key '"+function_key+"' provided."
                log.error(err_msg)
                logger.print_on_console(err_msg)
                logger.print_on_console("Supported keys are: "+str(", ".join(list(func_keys.keys()))))
        except Exception as e:
            err_msg = "Error: Unable to send function key to the Emulator screen."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def get_text(self,row_number,column_number,length):
        err_msg=None
        output=None
        return_value = None
        try:
            data = dataTransmitter("gettext", int(length), int(row_number), int(column_number))
            return_value = data["stat"]
            if return_value == 0:
                output = data["res"]
                log.info("Output text = %s",output)
                logger.print_on_console("Output text = "+output)
            else:
                err_msg = "Error: "+data["emsg"]
                log.debug("Return Value is "+str(return_value))
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            if isinstance(e,ValueError):
                err_msg = "Error: Row number, Column number and Length of the text should be integer."
            else:
                err_msg = "Error: Unable to get the text from Emulator screen."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def verify_text_exists(self,text):
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            data = dataTransmitter("verifytextexists", text)
            return_value = data["stat"]
            if return_value == 0:
                logger.print_on_console(MAINFRAME_TEXT_VERIFIED)
                log.info(MAINFRAME_TEXT_VERIFIED)
            elif return_value == 24:
                err_msg=MAINFRAME_TEXT_MISMATCHED
                log.info(err_msg)
                log.debug("Return Value is "+str(return_value))
                logger.print_on_console(err_msg)
            else:
                err_msg = "Error: "+data["emsg"]
                log.debug("Return Value is "+str(return_value))
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error: Unable to verify the text present in Emulator screen."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def submit_job(self,job_path,member_name):
        #Logic to submit the job
        err_msg=None
        output=None
        return_value = None
        try:
            data = dataTransmitter("setcursor", 4, 15)
            stat = data["stat"]
            if stat == 0:
                dataTransmitter("sendvalue", [MAINFRAME_KEY_3_4, MAINFRAME_KEY_ENTER, MAINFRAME_KEY_T,
                    MAINFRAME_KEY_F, job_path, MAINFRAME_KEY_ENTER, MAINFRAME_KEY_f, MAINFRAME_KEY_ENTER])
                file_status = dataTransmitter("waitfortext", job_path, 8, 11, 5)
                jobno = None
                if file_status["stat"] != 4:
                    dataTransmitter("setcursor", 8, 2)
                    dataTransmitter("sendvalue", [MAINFRAME_KEY_V, MAINFRAME_KEY_ENTER, MAINFRAME_KEY_f,
                        member_name,MAINFRAME_KEY_ENTER])
                    jobname = dataTransmitter("gettext", 8, 6, 12)
                    if jobname["ret"] == member_name:
                        dataTransmitter("sendvalue", [MAINFRAME_KEY_T, MAINFRAME_KEY_T, MAINFRAME_KEY_SUB,
                            MAINFRAME_KEY_ENTER])
                        resultCode = dataTransmitter("waitfortext", MAINFRAME_KEY_IKJ, 1, 1, 2)
                        if resultCode["stat"] == 4:
                            jobno = dataTransmitter("gettext", 8, 1, 25)
                        else:
                            jobno = dataTransmitter("gettext", 8, 1, 25)
                            dataTransmitter("sendvalue", MAINFRAME_KEY_ENTER)
                        jobno = jobno["ret"]
                        log.debug('Job Number: ' + str(jobno))
                        return_value = 0
                        output = jobno
                    else:
                        dataTransmitter("sendvalue", [MAINFRAME_KEY_F3, MAINFRAME_KEY_F3, MAINFRAME_KEY_F3])
                        err_msg=MAINFRAME_JOB_NOT_FOUND
                        log.info(err_msg)
                        logger.print_on_console(err_msg)
                else:
                    dataTransmitter("sendvalue", [MAINFRAME_KEY_F3, MAINFRAME_KEY_F3])
                    err_msg=MAINFRAME_FILE_NOT_FOUND
                    log.info(err_msg)
                    logger.print_on_console(err_msg)
            else:
                err_msg = "Error: "+data["emsg"]
                log.error(err_msg)
                log.debug("Return Value is "+str(stat))
                logger.print_on_console(err_msg)
                err_msg = "Error: Unable to Submit the job."
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error: Unable to Submit the job."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def job_status(self,job_no):
        #Logic to submit the job
        err_msg=None
        output=None
        return_value = None
        try:
            data = dataTransmitter("setcursor", 4, 15)
            stat = data["stat"]
            if stat == 0:
                dataTransmitter("sendvalue", [MAINFRAME_KEY_M_5, MAINFRAME_KEY_ENTER, MAINFRAME_KEY_ST, MAINFRAME_KEY_ENTER,
                    MAINFRAME_KEY_FILTER_JOBID, job_no, MAINFRAME_KEY_ENTER])
                #dataTransmitter("setcursor", 6, 25)
                status = dataTransmitter("gettext", 7, 6, 25)
                job_status = status["ret"]
                if job_status == " ":
                    err_msg = MAINFRAME_JOB_NOT_COMPLETED
                    log.error(err_msg)
                    logger.print_on_console(err_msg)
                else:
                    logger.print_on_console('Job Status :'+ job_status + MAINFRAME_JOB_COMPLETED)
                    log.info('Job Status : %s', job_status + MAINFRAME_JOB_COMPLETED)
                    output = job_status
                    return_value = 0
            else:
                err_msg = "Error: "+data["emsg"]
                log.error(err_msg)
                log.debug("Return Value is "+str(stat))
                logger.print_on_console(err_msg)
                err_msg = "Error: Unable to retrieve job status."
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error: Unable to retrieve job status."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def set_cursor(self,row_number,column_number):
        #Logic to submit the job
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            data = dataTransmitter("setcursor", int(row_number), int(column_number))
            return_value = data["stat"]
            if return_value == 0:
                log.error(MAINFRAME_CURSOR_SET)
                logger.print_on_console(MAINFRAME_CURSOR_SET)
            else:
                err_msg = "Error: "+data["emsg"]
                log.debug("Return Value is "+str(return_value))
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            if isinstance(e,ValueError):
                err_msg = "Error: Row number and Column number should be integer."
            else:
                err_msg = "Error: Unable to set the cursor on Emulator screen."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def disconnect_session(self):
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            data = dataTransmitter("disconnectsession")
            return_value = data["stat"]
            if return_value == 0:
                log.error(MAINFRAME_SESSION_DISCONNECTED)
                logger.print_on_console(MAINFRAME_SESSION_DISCONNECTED)
            else:
                err_msg = "Error: "+data["emsg"]
                log.debug("Return Value is "+str(return_value))
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error: Unable to disconnect from Emulator."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg

    def close_mainframe(self):
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            data = dataTransmitter("closemainframe")
            return_value = data["stat"]
            if return_value == 0:
                log.error(MAINFRAME_APP_CLOSED)
                logger.print_on_console(MAINFRAME_APP_CLOSED)
            else:
                err_msg = "Error: "+data["emsg"]
                log.debug("Return Value is "+str(return_value))
                log.error(err_msg)
                logger.print_on_console(err_msg)
            from threading import Timer
            Timer(10,mf_close).start()
        except Exception as e:
            err_msg = "Error: Unable to close emulator."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
        return (return_value == 0),output,err_msg


def dataTransmitter(a,*args):
    if emulator is None:
        raise Exception("Unable to contact AvoAssureMFapi")
    else:
        key = "".join(['h','f','g','w','e','u','y','R','^','%','$','&','B','8','7',
            'n','x','z','t','7','0','8','r','n','t','.','&','%','^','(','*','@'])
        d={"action":a,"inputs":args}
        data_to_send = core_utils_obj.wrap(json.dumps(d), key) + MF_API_DATA_EOF
        soc_api.send(data_to_send)
        data=b''
        while True:
            data_stream = soc_api.recv(1024)
            data += data_stream
            if MF_API_DATA_EOF in data_stream:
                break
        data = data[:data.find(MF_API_DATA_EOF)]
        return json.loads(core_utils_obj.unwrap(data, key))

def check_n_init(emulator_type):
    global emulator, soc_api
    if emulator is None:
        path = subprocess.os.environ["AVO_ASSURE_HOME"] + "/plugins/Mainframe/AvoAssureMFapi.exe"
        emulator = subprocess.Popen(path, shell=True)
        time.sleep(1)
    if soc_api is None:
        try:
            soc_api = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #add the time sleep due to some connectivity issue in one of the ODC:
            #[ERROR: WINERROR10061]
            time.sleep(5)
            soc_api.connect(("localhost",10001))
            data = dataTransmitter("test", emulator_type)
            if data["stat"] != 0:
                logger.print_on_console(data["emsg"])
                raise Exception(data["emsg"])
        except Exception as e:
            err_msg = "Error: Unable to launch AvoAssureMFapi."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
            subprocess.os.system("TASKKILL /F /IM AvoAssureMFapi.exe")
            emulator = None
    else:
        try:
            data = dataTransmitter("test", emulator_type)
            if data["stat"] != 0:
                err_msg = "Error: Unable to launch AvoAssureMFapi."
                log.error(err_msg)
                log.error(data["emsg"])
                logger.print_on_console(err_msg)
        except:
            soc_api.close()
            soc_api = None
            check_n_init(emulator_type)

def mf_close():
    time.sleep(2)
    exit()
