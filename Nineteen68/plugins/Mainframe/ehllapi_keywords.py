#-------------------------------------------------------------------------------
# Name:        ehllapi_keywords.py
# Purpose:     Seperate class to perform automation on Emulator using HLLAPI
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
import subprocess
from mainframe_constants import *
import logger
import logging
import core_utils

log = logging.getLogger('ehllapi_keywords.py')
emulator = None
soc_api = None
core_utils_obj = core_utils.CoreUtils()

def dataTransmitter(a,*args):
    if emulator is None:
        raise Exception("Unable to contact nineteen68MFapi")
    else:
        key = "".join(['h','f','g','w','e','u','y','R','^','%','$','&','B','8','7',
            'n','x','z','t','7','0','8','r','n','t','.','&','%','^','(','*','@'])
        d={"action":a,"inputs":args}
        data_to_send = core_utils_obj.wrap(json.dumps(d).encode('utf-8'), key) + MF_API_DATA_EOF
        soc_api.send(data_to_send)
        data=""
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
        path = subprocess.os.environ["NINETEEN68_HOME"] + "/Nineteen68/plugins/Mainframe/nineteen68MFapi.exe"
        emulator = subprocess.Popen(path, shell=True)

    if soc_api is None:
        try:
            soc_api = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc_api.connect(("localhost",10001))
            data = dataTransmitter("test", emulator_type)
            if data["stat"] != 0:
                raise Exception(data["emsg"])
        except Exception as e:
            err_msg = "Error: Unable to launch nineteen68MFapi."
            log.error(err_msg)
            log.error(e)
            logger.print_on_console(err_msg)
            subprocess.os.system("TASKKILL /F /IM nineteen68MFapi.exe")
            emulator = None
    else:
        try:
            data = dataTransmitter("test", emulator_type)
            if data["stat"] != 0:
                err_msg = "Error: Unable to launch nineteen68MFapi."
                log.error(err_msg)
                log.error(data["emsg"])
                logger.print_on_console(err_msg)
        except:
            soc_api.close()
            soc_api = None
            check_n_init(emulator_type)


class EhllapiKeywords:

    def __init__(self):
        """The instantiation operation __init__ creates an empty object of the class EhllapiKeywords
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
                time.sleep(1)
                data2 = dataTransmitter("getspacesize", self.host)
                if data2["stat"] == 0:
                    self.rows = int(data2["res"][0])
                    self.cols = int(data2["res"][1])
                    res_msg = "Screen resolution is identified as "+str(data2["res"][0])+"x"+str(data2["res"][1])
                    log.info(res_msg)
                    logger.print_on_console(res_msg)
                else:
                    self.rows = 24
                    self.cols = 80
                    log.error(MAINFRAME_RESOLUTION_FAIL)
                    logger.print_on_console(MAINFRAME_RESOLUTION_FAIL)
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

    def login(self,region,userID,password):
        err_msg=None
        output=OUTPUT_CONSTANT
        return_value = None
        try:
            # Replace Here ##########
            # dataTransmitter(region,userID,password)
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
            # Replace Here ##########
            # dataTransmitter(option)
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
            position = (self.cols * (int(row_number)-1)) + int(column_number)
            data = dataTransmitter("settext", text, position)
            return_value = data["stat"]
            if return_value == 0:
                log.info(MAINFRAME_SET_TEXT)
                logger.print_on_console(MAINFRAME_SET_TEXT)
            else:
                err_msg = "Error: "+data["emsg"]
                log.debug("Return Value is "+str(return_value))
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
            if EHLLAPI_MNEMONICS.has_key(function_key):
                text = EHLLAPI_MNEMONICS[function_key]
                for i in range(number):
                    data1 = dataTransmitter("wait")
                    if data1["stat"] == 0:
                        data2 = dataTransmitter("sendvalue", text)
                        return_value = data2["stat"]
                        if return_value == 0:
                            log.info(MAINFRAME_PRESS_FUNCTION_KEY)
                            logger.print_on_console(MAINFRAME_PRESS_FUNCTION_KEY)
                        else:
                            err_msg = "Error: "+data2["emsg"]
                            break
                    else:
                        err_msg = "Error: "+data1["emsg"]
                        break
                if err_msg is not None:
                    log.debug("Return Value is "+str(return_value))
                    log.error(err_msg)
                    logger.print_on_console(err_msg)
            else:
                err_msg = "Error: Invalid function_key  '"+function_key+"' provided."
                log.error(err_msg)
                logger.print_on_console(err_msg)
                logger.print_on_console("Supported keys are: "+str(", ".join(EHLLAPI_MNEMONICS.keys())))
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
            position = (self.cols * (int(row_number)-1)) + int(column_number)
            data = dataTransmitter("gettext", int(length), position)
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
            # Replace Here ##########
            # dataTransmitter(job_path,member_name)
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
            # Replace Here ##########
            # dataTransmitter(job_no)
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
            position = (self.cols * (int(row_number)-1)) + int(column_number)
            data = dataTransmitter("setcursor", position)
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
            import traceback
            traceback.print_exc()
        return (return_value == 0),output,err_msg


def mf_close():
    time.sleep(2)
    exit()