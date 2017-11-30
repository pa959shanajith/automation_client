#-------------------------------------------------------------------------------
# Name:        mainframe_keywords.py
# Purpose:     To automate Mainframe keywords
# Supported Emulators : Bluezone, Extra and Pcomm
#Keyword Available to Automate :
"""         1. launch_mainframe - This keyword or action specifies the Tool to launch the emulator.
#           2. login            - This keyword or action specifies the Tool to Login to the Mainframe Region using userID and password.
#           3. logoff          - This keyword or action specifies the Tool to Log off from the Mainframe.
#           4. set_text         - This keyword or action specifies the Tool to enter the text at the location specified by the user.
#           5. send_value       - This keyword or action specifies the Tool to send the individual keystrokes to the location where the cursor is present at the point of execution.
#           6. get_text         - This keyword or action specifies the Tool to fetch the text and save the results in the output variable.
#           7. verify_text_exists - This keyword or action specifies the Tool to verify whether the given Text exists in the screen.
#           8. submit_job       - This keyword or action specifies the Tool to submit the specified job to the mainframe and stores the Job ID in the output variable.
#           9. job_status       - This keyword or action specifies the Tool to fetch the job status along with the Job ID based on "SubmitJob" output variable provided as input.
#           10.send_function_keys - This keyword or action specifies the Tool to send the function keys to the application.
#           11.set_cursor       - This keyword or action specifies the Tool to set the cursor at the specified location. The location is identified by the row and column mentioned in the input.
"""
# Author:      wasimakram.sutar
# Created:     08-09-2016
# Updated      30-10-2017
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import time
import os
from mainframe_constants import *
from bluezone_keywords import *
from encryption_utility import AESCipher
import logger
import logging

log = logging.getLogger('mainframe_keywords.py')

class MainframeKeywords:


    def __init__(self):
        """The instantiation operation __init__ creates an empty object of the class Mainframekeywords
            when it is instantiated"""
        self.emulator_path = ''
        self.emulator_type = ''
        self.host = None
        self.region= ''
        self.userID = ''
        self.password = ''
        self.option = ''
        self.job_path = ''
        self.member_name = ''
        self.emulator_types= [MAINFRAME_BLUEZONE,MAINFRAME_EXTRA,MAINFRAME_PCOMM]
        self.keys = {
                    "enter" : "<Enter>",
                    "tab" : "<Tab>",
                    "home" : "<Home>"
                    }
        self.logoff_options = {
                    "1": "Prints the data set and Logoff (Not recommended)",
                    "2": "Delete the dataset and Logoff",
                    "3": "Keep the existing dataset and Logoff",
                    "4": "Keep the new dataset and Logoff"
                    }
        self.bluezone_object = BluezoneKeywords()

    def launch_mainframe(self,inputs):
        """
        method name : launch_mainframe
        inputs      : User can provide input value to LaunchMainframe either from excel sheet or through dynamic variable.
                        1. emulator_path - Path of emulator
                        2. emulator_type - Type of emulator
        Purpose     : This keyword or action specifies the Tool to launch the emulator.
        Support     : Supported Emulators are Bluezone, EXTRA and PCOM.
        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        result = False
        try:
            #check for the exact inputs
            if len(inputs) == 2:
                #store the input values
                self.emulator_path = inputs[0]
                self.emulator_type = inputs[1]
                # Log the input details in log file
                log.info("Input recieved")
                log.info("Emulator Path : %s \t Emulator type : %s",self.emulator_path,self.emulator_type)
                # Print the input details on ICE console
                logger.print_on_console("Input recieved : ")
                logger.print_on_console("Emulator path : "+self.emulator_path + "\t" + "Eulator type :" + self.emulator_type)
                if os.path.isfile(self.emulator_path):
                    #Log the state of file in log file
                    log.info("Emulator path %s is valid, continue execution...",self.emulator_path)
                    #Print the state of file on ICE console
                    logger.print_on_console("Emulator path "+ self.emulator_path + " is valid, continue ...")
                    if self.emulator_type in self.emulator_types:
                        #Log the state of  keyword in log file
                        log.info("Launching %s emulator...",self.emulator_type)
                        #Print the state of keyword on ICE console
                        logger.print_on_console("Launching " + self.emulator_type +" emulator...",)
                    if self.emulator_type == MAINFRAME_EXTRA:
                        print "Extra Emulator code"
                    elif self.emulator_type == MAINFRAME_BLUEZONE:
                        result,output,err_msg =  self.bluezone_object.launch_mainframe(self.emulator_path)
                    elif self.emulator_type == MAINFRAME_PCOMM:
                        print "Pcomm Emulator code"
                    #Update the status variables based on result.
                    if result:
                        status = TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
                else:
                    log.error("Error: File not found!!! - Emulator path %s is wrong.",self.emulator_path)
                    err_msg = "Error: File not found!!! - Emulator path " + self.emulator_path +" is wrong."
                    logger.print_on_console("Error: File not found!!! - Emulator path " + self.emulator_path + " is wrong.")

            else:
                log.error("Error: Invalid input!!! - launch_mainframe need 2 paramemters, 1. Emulator Path 2. Emulator Type.")
                err_msg = "Error: Invalid input!!! - launch_mainframe need 2 paramemters, 1. Emulator Path 2. Emulator Type."
                logger.print_on_console("Error: Invalid input!!! - launch_mainframe need 2 paramemters, 1. Emulator Path 2. Emulator Type.")
        except Exception as e:
            log.error("Error: Unable to launch mainframe.")
            log.error(e)
            err_msg = "Error: Unable to launch mainframe."
            logger.print_on_console("Error: Unable to launch mainframe.")
        #Return the status of the keyword
        return status,methodoutput,output,err_msg


    def login(self,inputs):
        """
        method name : login
        inputs      : User can provide input value to login either from excel sheet or through dynamic variable.
                        1. region - Region to login into  emulator
                        2. userID - Userid to login into  emulator
                        3. password - Password to login into emulator
        Purpose     : This keyword or action specifies the Tool to Login to the Mainframe Region using userID and password.
        Support     : Supported Emulators are Bluezone, EXTRA and Pcomm.
        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            #check for the exact inputs
            if len(inputs) == 3:
                self.region = inputs[0]
                self.userID = inputs[1]
                self.password = inputs[2]
                # Log the input details in log file
                log.info("Input recieved")
                log.info("Region : %s \t UserID : %s \t Password : %s",self.region,self.userID,self.password)
                # Print the input details on ICE console
                logger.print_on_console("Input recieved : ")
                logger.print_on_console("Region : "+self.region + "\t" + "UserID :" + self.userID + "\t" + "Password :" + self.password)
                if self.emulator_type in self.emulator_types:
                    #Log the state of  keyword in log file
                    log.info("Logging to %s emulator...",self.emulator_type)
                    #Print the state of keyword on ICE console
                    logger.print_on_console("Logging to " + self.emulator_type +" emulator...",)
                if self.emulator_type == MAINFRAME_EXTRA:
                    #Logic to launch Extra Emulator goes here
                    print "Extra Emulator code"
                elif self.emulator_type == MAINFRAME_BLUEZONE:
                    result,output,err_msg =  self.bluezone_object.login(self.region,self.userID,self.password)
                elif self.emulator_type == MAINFRAME_PCOMM:
                    print "Pcomm Emulator code"
                if result:
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
            else:
                log.error("Error: Invalid input!!! - login need 3 paramemters, 1. Region 2. UserID 3. Password.")
                err_msg = "Error: Invalid input!!! - login need 3 paramemters, 1. Region 2. UserID 3. Password."
                logger.print_on_console("Error: Invalid input!!! - login need 3 paramemters, 1. Region 2. UserID 3. Password.")
        except Exception as e:
            log.error("Error: Unable to login in to mainframe.")
            log.error(e)
            err_msg = "Error: Unable to login in to mainframe."
            logger.print_on_console("Error: Unable to login in to mainframe.")
        return status,methodoutput,output,err_msg

    def secure_login(self,inputs):
        """
        method name : login
        inputs      : User can provide input value to login either from excel sheet or through dynamic variable.
                        1. region - Region to login into  emulator
                        2. userID - Userid to login into  emulator
                        3. password - Password to login into emulator (Encrypted using AES)
        Purpose     : This keyword or action specifies the Tool to Login to the Mainframe Region using userID and password.
        Support     : Supported Emulators are Bluezone, EXTRA and Pcomm.
        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            #check for the exact inputs
            if len(inputs) == 3:
                self.region = inputs[0]
                self.userID = inputs[1]
                self.password = inputs[2]
                encryption_obj = AESCipher()
                password = encryption_obj.decrypt(self.password)
                # Log the input details in log file
                log.info("Input recieved")
                log.info("Region : %s \t UserID : %s \t Password : %s",self.region,self.userID,password)
                # Print the input details on ICE console
                logger.print_on_console("Input recieved : ")
                #logger.print_on_console("Region : "+self.region + "\t" + "UserID :" + self.userID + "\t" + "Password :" + password)
                if self.emulator_type in self.emulator_types:
                    #Log the state of  keyword in log file
                    log.info("Logging to %s emulator...",self.emulator_type)
                    #Print the state of keyword on ICE console
                    logger.print_on_console("Logging to " + self.emulator_type +" emulator...",)
                if self.emulator_type == MAINFRAME_EXTRA:
                    #Logic to launch Extra Emulator goes here
                    print "Extra Emulator code"
                elif self.emulator_type == MAINFRAME_BLUEZONE:
                    result,output,err_msg =  self.bluezone_object.login(self.region,self.userID,password)
                elif self.emulator_type == MAINFRAME_PCOMM:
                    print "Pcomm Emulator code"
                if result:
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
            else:
                log.error("Error: Invalid input!!! - login need 3 paramemters, 1. Region 2. UserID 3. Password.")
                err_msg = "Error: Invalid input!!! - login need 3 paramemters, 1. Region 2. UserID 3. Password."
                logger.print_on_console("Error: Invalid input!!! - login need 3 paramemters, 1. Region 2. UserID 3. Password.")
        except Exception as e:
            log.error("Error: Unable to login in to mainframe.")
            log.error(e)
            err_msg = "Error: Unable to login in to mainframe."
            logger.print_on_console("Error: Unable to login in to mainframe.")
        return status,methodoutput,output,err_msg


    def logoff(self,inputs):
        """
        method name : login
        inputs      : User can provide input value to login either from excel sheet or through dynamic variable.
                        1. Number
                            Number Function:
                                1.Prints the data set and Logoff (Not recommended)
                                2.Delete the dataset and Logoff
                                3.Keep the existing dataset and Logoff
                                4.Keep the new dataset and Logoff

        Purpose     : This keyword or action specifies the Tool to Log off from the Mainframe.
        Support     : Supported Emulators are Bluezone, EXTRA and Pcomm.
        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            #check for the exact inputs
            if len(inputs) == 1:
                self.option = inputs[0]
                if self.option is not '':
                    # Log the input details in log file
                    log.info("Input recieved")
                    log.info("Option : %s = %s ",self.option,self.logoff_options[self.option])
                    # Print the input details on ICE console
                    logger.print_on_console("Input recieved : ")
                    logger.print_on_console("Option : "+self.option + "=" +  self.logoff_options[self.option])
                    if self.emulator_type in self.emulator_types:
                        #Log the state of  keyword in log file
                        log.info("Logging off from %s emulator...",self.emulator_type)
                        #Print the state of keyword on ICE console
                        logger.print_on_console("Logging off from  " + self.emulator_type +" emulator...",)
                    if self.emulator_type == MAINFRAME_EXTRA:
                        #Logic to launch Extra Emulator goes here
                        print "Extra Emulator code"
                    elif self.emulator_type == MAINFRAME_BLUEZONE:
                        result,output,err_msg =  self.bluezone_object.logoff(self.option)
                    elif self.emulator_type == MAINFRAME_PCOMM:
                        print "Pcomm Emulator code"
                    if result:
                        status = TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
                else:
                    log.error("Error: Invalid input!!! - logoff need 1 paramemter, 1. Option ")
                    err_msg = "Error: Invalid input!!! - logoff need 1 paramemter, 1. Option"
                    logger.print_on_console("Error: Invalid input!!! - logoff need 1 paramemter, 1. Option")
                    logger.print_on_console("Available options :")
                    logger.print_on_console("OPTION" + "\t\tVALUE")
                    for key in self.logoff_options:
                        logger.print_on_console(key + "\t\t" + self.logoff_options[key])
            else:
                log.error("Error: Invalid input!!! - logoff need 1 paramemter, 1. Option ")
                err_msg = "Error: Invalid input!!! - logoff need 1 paramemter, 1. Option"
                logger.print_on_console("Error: Invalid input!!! - logoff need 1 paramemter, 1. Option")
                logger.print_on_console("Available options :")
                logger.print_on_console("OPTION" + "\t\tVALUE")
                for key in self.logoff_options:
                    logger.print_on_console(key + "\t\t" + self.logoff_options[key])
        except Exception as e:
            log.error("Error: Unable to logoff from Emulator.")
            log.error(e)
            err_msg = "Error: Unable to logoff from Emulator."
            logger.print_on_console("Error: Unable to logoff from Emulator.")
        return status,methodoutput,output,err_msg


    def send_value(self,inputs):
        """
        method name : send_value
        inputs      : User can provide input value to send_value either from excel sheet or through dynamic variable.
                        1. text - Tesxt to be sent
        Purpose     : This keyword or action specifies the Tool to send the individual keystrokes to the location where the cursor is present at the point of execution.
        Support     : Supported Emulators are Bluezone, EXTRA and Pcomm.
        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
             #check for the exact inputs
            if len(inputs) == 1:
                self.text = inputs[0]
                # Log the input details in log file
                log.info("Input recieved")
                log.info("Text : %s ",self.text)
                # Print the input details on ICE console
                logger.print_on_console("Input recieved : ")
                logger.print_on_console("Text : "+self.text)
                if self.emulator_type in self.emulator_types:
                    #Log the state of  keyword in log file
                    log.info("Sending Value to %s emulator screen...",self.emulator_type)
                    #Print the state of keyword on ICE console
                    logger.print_on_console("Sending Value to  " + self.emulator_type +" emulator screen...",)
                if self.emulator_type == MAINFRAME_EXTRA:
                    #Logic to launch Extra Emulator goes here
                    print "Extra Emulator code"
                elif self.emulator_type == MAINFRAME_BLUEZONE:
                    result,output,err_msg =  self.bluezone_object.send_value(self.text)
                elif self.emulator_type == MAINFRAME_PCOMM:
                    print "Pcomm Emulator code"
                if result:
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
            else:
                log.error("Error: Invalid input!!! - send_value need 1 paramemter, 1. Text ")
                err_msg = "Error: Invalid input!!! - send_value need 1 paramemter, 1. Text"
                logger.print_on_console("Error: Invalid input!!! - send_value need 1 paramemter, 1. Text")
        except Exception as e:
            log.error("Error: Unable to send value to %s Emulator screen.",self.emulator_type)
            log.error(e)
            err_msg = "Error: Unable to  send value to "+ self.emulator_type +" Emulator screen."
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def set_text(self,inputs):
        """
        method name : set_value
        inputs      : User can provide input value to set_text either from excel sheet or through dynamic variable.
                        1. Row Number
                        2. Column Number
                        3. Text
        Purpose     : This keyword or action specifies the Tool to enter the text at the location specified by the user.
        Support     : Supported Emulators are Bluezone, EXTRA and Pcomm.
        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            #check for the exact inputs
            if len(inputs) == 3:
                row_number = inputs[0]
                column_number = inputs[1]
                text = inputs[2]
                # Log the input details in log file
                log.info("Input recieved")
                log.info("Row number : %s \t Column number : %s \t Text : %s",row_number,column_number,text)
                # Print the input details on ICE console
                logger.print_on_console("Input recieved : ")
                logger.print_on_console("Row number : "+row_number + "\t" + "Column number :" + column_number + "\t" + "Text :" + text)
                if self.emulator_type in self.emulator_types:
                    #Log the state of  keyword in log file
                    log.info("Setting the text in  %s emulator screen...",self.emulator_type)
                    #Print the state of keyword on ICE console
                    logger.print_on_console("Setting the text in " + self.emulator_type +" emulator screen...",)
                if self.emulator_type == MAINFRAME_EXTRA:
                    #Logic to launch Extra Emulator goes here
                    print "Extra Emulator code"
                elif self.emulator_type == MAINFRAME_BLUEZONE:
                    result,output,err_msg =  self.bluezone_object.set_text(row_number,column_number,text)
                elif self.emulator_type == MAINFRAME_PCOMM:
                    print "Pcomm Emulator code"
                if result:
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
            else:
                log.error("Error: Invalid input!!! - SetText need 3 paramemters, 1. Row number 2. Column number 3. Text.")
                err_msg = "Error: Invalid input!!! - SetText need 3 paramemters, 1. Row number 2. Column number 3. Text."
                logger.print_on_console("Error: Invalid input!!! - SetText need 3 paramemters, 1. Row number 2. Column number 3. Text.")
        except Exception as e:
            log.error("Error: Unable to set the text to %s Emulator screen.",self.emulator_type)
            log.error(e)
            err_msg = "Error: Unable to  set the text to "+ self.emulator_type +" Emulator screen."
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def send_function_keys(self,inputs):
        """
        method name : send_value
        inputs      : User can provide input value to send_function_keys either from excel sheet or through dynamic variable.
                        1. Function key
                        2. Number
        Purpose     : This keyword or action specifies the Tool to send the function keys to the application.
        Support     : Supported Emulators are Bluezone, EXTRA and Pcomm.
        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            #check for the exact inputs
            if len(inputs) == 1 or len(inputs) == 2 :
                function_key = self.keys[inputs[0].lower()]
                number = 1
                if len(inputs) == 2:
                    number = inputs[1]
                # Log the input details in log file
                log.info("Input recieved")
                log.info("Function key : %s ",function_key)
                # Print the input details on ICE console
                logger.print_on_console("Input recieved : ")
                logger.print_on_console("Function key : "+function_key)
                if self.emulator_type in self.emulator_types:
                    #Log the state of  keyword in log file
                    log.info("Sending Function key to %s emulator screen...",self.emulator_type)
                    #Print the state of keyword on ICE console
                    logger.print_on_console("Sending function key to  " + self.emulator_type +" emulator screen...",)
                if self.emulator_type == MAINFRAME_EXTRA:
                    #Logic to launch Extra Emulator goes here
                    print "Extra Emulator code"
                elif self.emulator_type == MAINFRAME_BLUEZONE:
                    result,output,err_msg =  self.bluezone_object.send_function_keys(function_key,number)
                elif self.emulator_type == MAINFRAME_PCOMM:
                    print "Pcomm Emulator code"
                if result:
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
            else:
                log.error("Error: Invalid input!!! - send_function_keys need 1 paramemter, 1. Function key ")
                err_msg = "Error: Invalid input!!! - send_function_keys need 1 paramemter, 1. Function key"
                logger.print_on_console("Error: Invalid input!!! - send_send_function_keysvalue need 1 paramemter, 1. Function key")
        except Exception as e:
            log.error("Error: Unable to send function key to %s Emulator screen.",self.emulator_type)
            log.error(e)
            err_msg = "Error: Unable to  Unable to send function key to "+ self.emulator_type +" Emulator screen."
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg


    def get_text(self,inputs):
        """
        method name : get_text
        inputs      : User can provide input value to get_text either from excel sheet or through dynamic variable.
                        1. Row Number
                        2. Column Number
                        3. Length of the text to be fetched
        Purpose     : This keyword or action specifies the Tool to fetch the text and save the results in the output variable.
        Support     : Supported Emulators are Bluezone, EXTRA and Pcomm.
        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            #check for the exact inputs
            if len(inputs) == 3:
                row_number = inputs[0]
                column_number = inputs[1]
                length = inputs[2]
                # Log the input details in log file
                log.info("Input recieved")
                log.info("Row number : %s \t Column number : %s \t Length of text : %s",row_number,column_number,length)
                # Print the input details on ICE console
                logger.print_on_console("Input recieved : ")
                logger.print_on_console("Row number : "+row_number + "\t" + "Column number :" + column_number + "\t" + "Length of Text :" + length)
                if self.emulator_type in self.emulator_types:
                    #Log the state of  keyword in log file
                    log.info("Getting the text from  %s emulator screen...",self.emulator_type)
                    #Print the state of keyword on ICE console
                    logger.print_on_console("Getting the text from " + self.emulator_type +" emulator screen...",)
                if self.emulator_type == MAINFRAME_EXTRA:
                    #Logic to launch Extra Emulator goes here
                    print "Extra Emulator code"
                elif self.emulator_type == MAINFRAME_BLUEZONE:
                    result,output,err_msg =  self.bluezone_object.get_text(row_number,column_number,length)
                elif self.emulator_type == MAINFRAME_PCOMM:
                    print "Pcomm Emulator code"
                if result:
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
            else:
                log.error("Error: Invalid input!!! - GetText need 3 paramemters, 1. Row number 2. Column number 3. Length of Text.")
                err_msg = "Error: Invalid input!!! - GetText need 3 paramemters, 1. Row number 2. Column number 3. Length of Text."
                logger.print_on_console("Error: Invalid input!!! - GetText need 3 paramemters, 1. Row number 2. Column number 3. Length of Text.")
        except Exception as e:
            log.error("Error: Unable to get the text from %s Emulator screen.",self.emulator_type)
            log.error(e)
            err_msg = "Error: Unable to get the text from "+ self.emulator_type +" Emulator screen."
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def verify_text_exists(self,inputs):
        """
        method name : get_text
        inputs      : User can provide input value to get_text either from excel sheet or through dynamic variable.
                        1. Text
        Purpose     : This keyword or action specifies the Tool to verify whether the given Text exists in the screen.
        Support     : Supported Emulators are Bluezone, EXTRA and Pcomm.
        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            #check for the exact inputs
            if len(inputs) == 1:
                text = inputs[0]
                # Log the input details in log file
                log.info("Input recieved")
                log.info("Text : %s ",text)
                # Print the input details on ICE console
                logger.print_on_console("Input recieved : ")
                logger.print_on_console("Text : "+text)
                if self.emulator_type in self.emulator_types:
                    #Log the state of  keyword in log file
                    log.info("Verifying text in  %s emulator screen...",self.emulator_type)
                    #Print the state of keyword on ICE console
                    logger.print_on_console("Verifying text in " + self.emulator_type +" emulator screen...",)
                if self.emulator_type == MAINFRAME_EXTRA:
                    #Logic to launch Extra Emulator goes here
                    print "Extra Emulator code"
                elif self.emulator_type == MAINFRAME_BLUEZONE:
                    result,output,err_msg =  self.bluezone_object.verify_text_exists(text)
                elif self.emulator_type == MAINFRAME_PCOMM:
                    print "Pcomm Emulator code"
                if result:
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
            else:
                log.error("Error: Invalid input!!! - verify_text_exists need 1 paramemter, 1. Text ")
                err_msg = "Error: Invalid input!!! - verify_text_exists need 1 paramemter, 1. Text"
                logger.print_on_console("Error: Invalid input!!! - verify_text_exists need 1 paramemter, 1. Text")

        except Exception as e:
            log.error("Error: Unable to verify the text from %s Emulator screen.",self.emulator_type)
            log.error(e)
            err_msg = "Error: Unable to verify the text from "+ self.emulator_type +" Emulator screen."
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def submit_job(self,inputs):
        """
        method name : submit_job
        inputs      : User can provide input value to submit_job either from excel sheet or through dynamic variable.
                        1. Job path
                        2. Member name
        Purpose     : This keyword or action specifies the Tool to submit the specified job to the mainframe and stores the Job ID in the output variable.
        Support     : Supported Emulators are Bluezone, EXTRA and Pcomm.
        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            #check for the exact inputs
            if len(inputs) == 2:
                self.job_path = inputs[0]
                self.member_name = inputs[1]
                # Log the input details in log file
                log.info("Input recieved")
                log.info("Job path : %s \t Member name : %s ",self.job_path,self.member_name)
                # Print the input details on ICE console
                logger.print_on_console("Input recieved : ")
                logger.print_on_console("Job path : "+self.job_path + "\t" + "Member name :" + self.member_name)
                if self.emulator_type in self.emulator_types:
                    #Log the state of  keyword in log file
                    log.info("Submit the job  %s emulator screen...",self.emulator_type)
                    #Print the state of keyword on ICE console
                    logger.print_on_console("Submit the job to " + self.emulator_type +" emulator screen...",)
                if self.emulator_type == MAINFRAME_EXTRA:
                    #Logic to launch Extra Emulator goes here
                    print "Extra Emulator code"
                elif self.emulator_type == MAINFRAME_BLUEZONE:
                    result,output,err_msg =  self.bluezone_object.submit_job(self.job_path,self.member_name)
                elif self.emulator_type == MAINFRAME_PCOMM:
                    print "Pcomm Emulator code"
                if result:
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
            else:
                log.error("Error: Invalid input!!! - submit_job need 2 paramemters, 1. Job path, 2. Member name ")
                err_msg = "Error: Invalid input!!! - submit_job need 2 paramemters, 1. Job path, 2. Member name"
                logger.print_on_console("Error: Invalid input!!! - submit_job need 2 paramemters, 1. Job path, 2. Member name")
        except Exception as e:
            log.error("Error: Unable to submit the job to %s Emulator screen.",self.emulator_type)
            log.error(e)
            err_msg = "Error: Unable Unable to submit the job to "+ self.emulator_type +" Emulator screen."
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def job_status(self,inputs):
        """
        method name : job_status
        inputs      : User can provide input value to job_status through dynamic variable.
                        1. Output variable of SubmitJob
        Purpose     : This keyword or action specifies the Tool to fetch the job status along with the Job ID based on "SubmitJob" output variable provided as input.
        Support     : Supported Emulators are Bluezone, EXTRA and Pcomm.
        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            #check for the exact inputs
            if len(inputs) == 1:
                self.job_no = inputs[0]
                # Log the input details in log file
                log.info("Input recieved")
                log.info("Job number : %s ",self.job_no)
                # Print the input details on ICE console
                logger.print_on_console("Input recieved : ")
                logger.print_on_console("Job number : "+self.job_no)
                if self.emulator_type in self.emulator_types:
                    #Log the state of  keyword in log file
                    log.info("Check the job status in  %s emulator screen...",self.emulator_type)
                    #Print the state of keyword on ICE console
                    logger.print_on_console("Check the job status in " + self.emulator_type +" emulator screen...",)
                if self.emulator_type == MAINFRAME_EXTRA:
                    #Logic to launch Extra Emulator goes here
                    print "Extra Emulator code"
                elif self.emulator_type == MAINFRAME_BLUEZONE:
                    result,output,err_msg =  self.bluezone_object.job_status(self.job_no)
                elif self.emulator_type == MAINFRAME_PCOMM:
                    print "Pcomm Emulator code"
                if result:
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
            else:
                log.error("Error: Invalid input!!! - job_status need 1 paramemter, 1. Job number ")
                err_msg = "Error: Invalid input!!! - job_status need 1 paramemter, 1. Job number"
                logger.print_on_console("Error: Invalid input!!! - job_status need 1 paramemter, 1. Job number")
        except Exception as e:
            log.error("Error: Unable to check the job status in %s Emulator screen.",self.emulator_type)
            log.error(e)
            err_msg = "Error: Unable to check the job status in "+ self.emulator_type +" Emulator screen."
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def set_cursor(self,inputs):
        """
        method name : set_cursor
        inputs      : User can provide input value to set_cursor through dynamic variable.
                        1. Row number
                        2. Column number
        Purpose     : This keyword or action specifies the Tool to set the cursor at the specified location. The location is identified by the row and column mentioned in the input.
        Support     : Supported Emulators are Bluezone, EXTRA and Pcomm.
        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            #check for the exact inputs
            if len(inputs) == 2:
                row_number = inputs[0]
                column_number = inputs[1]
                # Log the input details in log file
                log.info("Input recieved")
                log.info("Row number : %s \t Column number : %s ",row_number,column_number)
                # Print the input details on ICE console
                logger.print_on_console("Input recieved : ")
                logger.print_on_console("Row number : "+row_number + "\t" + "Column number :" + column_number)
                if self.emulator_type in self.emulator_types:
                    #Log the state of  keyword in log file
                    log.info("Set the cursor on  %s emulator screen...",self.emulator_type)
                    #Print the state of keyword on ICE console
                    logger.print_on_console("Set the cursor on " + self.emulator_type +" emulator screen...",)
                if self.emulator_type == MAINFRAME_EXTRA:
                    #Logic to launch Extra Emulator goes here
                    print "Extra Emulator code"
                elif self.emulator_type == MAINFRAME_BLUEZONE:
                    result,output,err_msg =  self.bluezone_object.set_cursor(row_number,column_number)
                elif self.emulator_type == MAINFRAME_PCOMM:
                    print "Pcomm Emulator code"
                if result:
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
            else:
                log.error("Error: Invalid input!!! - set_cursor need 2 paramemters, 1. Row number 2. Column number.")
                err_msg = "Error: Invalid input!!! - set_cursor need 2 paramemters, 1. Row number 2. Column number."
                logger.print_on_console("Error: Invalid input!!! - set_cursor need 3 paramemters, 1. Row number 2. Column number.")

        except Exception as e:
            log.error("Error: Unable to set the cursor on %s Emulator screen.",self.emulator_type)
            log.error(e)
            err_msg = "Error: Unable to set the cursor on "+ self.emulator_type +" Emulator screen."
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg



    @staticmethod
    def callVB(row,col,leng):
        """def to call vbscript"""
        vbhost = win32com.client.Dispatch(VB_HOST)
        vbhost.language = VB_LANGUAGE
        vbhost.addcode("Function getString()\nDim Sys\nDim Sess\nDim MyScreen\nSet Sys = CreateObject(\"EXTRA.System\")\nSet Sess = Sys.ActiveSession\nSet MyScreen = Sess.Screen\nrow ="+row+"\ncol="+col+"\nlength ="+leng+"\nMyString = MyScreen.GetString(row,col,length)\ngetString=MyString\nEnd Function\n")
        gotStr= vbhost.eval(VB_HOST_EVAL)
if __name__ == '__main__':
    print "***Begin main method***"

    mainframe_obj = MainframeKeywords()
    launch_inputs = ['C:\\Users\\wasimakram.sutar\\Desktop\\CONFIG1.zmd','Bluezone']
    print mainframe_obj.launch_mainframe(launch_inputs)
    print "Launch completed"


##    login_inputs = ['L TSO','EDISTA1','EDISTA1']
##    print mainframe_obj.login(login_inputs)
##    print "Login completed"

##    send_value = ["L TSO"]
##    print mainframe_obj.send_value(send_value)
##    print "SendValue Completed"

    set_text_input = ["24","1","WASIMAKRAM"]
    print mainframe_obj.set_text(set_text_input)
    print "SetText Completed"

##    send_function_input = ["Enter"]
##    print mainframe_obj.send_function_keys(send_function_input)
##    print "send_function_keys Completed"

    get_text_input = ["24","1","10"]
    print mainframe_obj.get_text(get_text_input)
    print "get_text completed"


    verify_text_input = ["WASIMAKRAM"]
    print mainframe_obj.verify_text_exists(verify_text_input)
    print "verify_text_input completed"

    set_cursor_input = ["24","1"]
    print mainframe_obj.set_cursor(set_cursor_input)
    print "verify_text_input completed"

