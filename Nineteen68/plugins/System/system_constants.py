#-------------------------------------------------------------------------------
# Name:        system_constants
# Purpose:     Module for System constants & Error codes
#
# Author:      Arpit.Koolwal

# Created:
# Copyright:   (c) arpit.koolwal 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# CONSTANTS

INVALID_KEYWORD='Invalid keyword'

INVALID_INPUT='Input value is Invalid,Please provide a valid input'

TEST_RESULT_PASS = "Pass"

TEST_RESULT_FAIL = "Fail"

TEST_RESULT_TRUE = "True"

TEST_RESULT_FALSE = "False"

ACCESS_DENIED = 'Insufficient Access Privileges'

ERROR_CODE_DICT ={
                    'ERR_UNABLE_TO_CONNECT':'Unable to connect with machine',
                    'ERR_OS_INFO':'Error Occured while executing getOSInfo Keyword',
                    'ERR_GET_INSTALLED_APP':'Error Occured while executing getallinstalledapps Keyword',
                    'ERR_GET_ALL_PROCESS':'Error Occured while executing getallprocess Keyword',
                    'ERR_EXECUTE_COMMAND':'Error Occured while executing executeCommand Keyword'
                 }