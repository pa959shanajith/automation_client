#-------------------------------------------------------------------------------
# Name:        Dropdown_Keywords
# Purpose:     Module for Dropdown_Keywords
#
# Author:      anas.ahmed1,kavyasree,sakshi.goyal,Saloni
#
# Created:     07-04-2017
# Copyright:   (c) anas.ahmed1 (2017)
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger


import sap_constants
import time
from constants import *
from text_keywords_sap import Text_Keywords

import logging
import logging.config
log = logging.getLogger('dropdown_keywords.py')

class Dropdown_Keywords():
        def getSelected(self,sap_id, *args):

            tk=Text_Keywords()
            id,ses=tk.attach(sap_id)
            status = sap_constants.TEST_RESULT_FAIL
            result = sap_constants.TEST_RESULT_FALSE
            err_msg=None
            value = ''
            try:
                if(id != None):
                    if(ses.FindById(id).Changeable == True):
                        value = ses.FindById(id).Text.strip()
                        status=sap_constants.TEST_RESULT_PASS
                        result=sap_constants.TEST_RESULT_TRUE
                else:
                    log.error('Error occured')
                    err_msg = sap_constants.ERROR_MSG

            except Exception as e:
                log.error('Error occured',e)
                err_msg = sap_constants.ERROR_MSG
            return status,result,value,err_msg



        def selectValueByIndex(self,sap_id,url,input_val, *args):
            tk=Text_Keywords()
            id,ses=tk.attach(sap_id)
            status = sap_constants.TEST_RESULT_FAIL
            result = sap_constants.TEST_RESULT_FALSE
            verb = OUTPUT_CONSTANT
            index=int(input_val[0])
            index=index+1
            err_msg=None
            i = 0
            result = None
            try:
                if(id != None):
                    if(ses.FindById(id).Changeable == True):
                        entries = ses.FindById(id).Entries
                        while True:
                            try:
                                #print entries(i).key
                                if(int(entries(i).key) == index):
                                    ses.FindById(id).value = entries(i).value
                                    status=sap_constants.TEST_RESULT_PASS
                                    result=sap_constants.TEST_RESULT_TRUE
                            except Exception as e:
                                err_msg = sap_constants.ERROR_MSG
                                log.info(err_msg)
                                break
                            i = i + 1

            except Exception as e:
                 log.error('Error occured',e)
            return status,result,verb,err_msg

        def getValueByIndex(self, sap_id, url,input_val,*args):
            tk=Text_Keywords()
            id,ses=tk.attach(sap_id)
            status = sap_constants.TEST_RESULT_FAIL
            result = sap_constants.TEST_RESULT_FALSE
            #verb = OUTPUT_CONSTANT
            value=''
            index=int(input_val[0])
            index=index+1
            err_msg=None
            i = 0
            result = None
            try:
                if(id != None):
                    if(ses.FindById(id).Changeable == True):
                        entries = ses.FindById(id).Entries
                        while True:
                            try:
                                #print entries(i).key
                                if(int(entries(i).key) == index):
                                    value = entries(i).value
                                    status=sap_constants.TEST_RESULT_PASS
                                    result=sap_constants.TEST_RESULT_TRUE
                            except Exception as e:
                                err_msg = sap_constants.ERROR_MSG
                                log.error(err_msg,e)
                                break
                            i = i + 1
                    else:
                        err_msg = sap_constants.ERROR_MSG
                        log.info(err_msg)
            except Exception as e:
                err_msg = sap_constants.ERROR_MSG
                log.error(err_msg,e)
            return status,result,value,err_msg

        def selectValueByText(self,sap_id,url,input_val, *args):
            tk=Text_Keywords()
            id,ses=tk.attach(sap_id)
            status = sap_constants.TEST_RESULT_FAIL
            result = sap_constants.TEST_RESULT_FALSE
            text=input_val[0]
            #verb = OUTPUT_CONSTANT
            value=OUTPUT_CONSTANT
            err_msg=None
            i = 0
            result = None
            try:
                if(id != None):
                    if(ses.FindById(id).Changeable == True):
                        entries = ses.FindById(id).Entries
                        while True:
                            try:
                                #print entries(i).value
                                if(entries(i).value == text):
                                    ses.FindById(id).value = text
                                    status=sap_constants.TEST_RESULT_PASS
                                    result=sap_constants.TEST_RESULT_TRUE

                            except Exception as e:
                                err_msg = sap_constants.ERROR_MSG
                                log.error(err_msg)
                                break
                            i = i + 1
            except Exception as e:
                  log.error('Error occured',e)
            return status,result,value,err_msg



        def verifySelectedValue(self,sap_id,url,input_val ,*args):
            tk=Text_Keywords()
            id,ses=tk.attach(sap_id)
            in_value=input_val[0]
            status = sap_constants.TEST_RESULT_FAIL
            result = sap_constants.TEST_RESULT_FALSE

            verb = OUTPUT_CONSTANT
            #value=OUTPUT_CONSTANT
            err_msg=None
            result = None
            try:
                if(id != None):
                    if(ses.FindById(id).Changeable == True):
                        if(ses.FindById(id).Text.strip() == in_value):
                                    status=sap_constants.TEST_RESULT_PASS
                                    result=sap_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = sap_constants.ERROR_MSG
                            log.info(err_msg)
            except Exception as e:
                log.error('Error occured',e)
                err_msg = sap_constants.ERROR_MSG
            return status,result,verb,err_msg


        def getCount(self,sap_id, *args):
            tk=Text_Keywords()
            id,ses=tk.attach(sap_id)

            status = sap_constants.TEST_RESULT_FAIL
            result = sap_constants.TEST_RESULT_FALSE
            value=''
            err_msg=None
            count = 0
            try:
                if(id != None):
                    if(ses.FindById(id).Changeable == True):
                        entries = ses.FindById(id).Entries
                        while True:
                            try:
                                value = entries(count).value
                                count = count + 1
                                value=count
                                status=sap_constants.TEST_RESULT_PASS
                                result=sap_constants.TEST_RESULT_TRUE
                            except Exception as e:
                                log.error('Error occured',e)
                                break
            except Exception as e:
                  log.error('Error occured',e)
            return status,result,value,err_msg

        def verifyCount(self,sap_id,url,input_val, *args):
            length = int(input_val[0])
            tk=Text_Keywords()
            id,ses=tk.attach(sap_id)
            verb = OUTPUT_CONSTANT
            value=''
            status = sap_constants.TEST_RESULT_FAIL
            result = sap_constants.TEST_RESULT_FALSE
            count = 0
            try:
                if(id != None):
                    if(ses.FindById(id).Changeable == True):
                        entries = ses.FindById(id).Entries
                        while True:
                            try:
                                value = entries(count).value
                                count = count + 1
                            except Exception as e:
                                err_msg = sap_constants.ERROR_MSG
                                break
                    if(length == count):
                         status=sap_constants.TEST_RESULT_PASS
                         result=sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = sap_constants.ERROR_MSG
                        log.info('Count Verify has failed ')
            except Exception as e:
                  log.error('Error occured',e)
            return status,result,verb,err_msg

        def verifyValuesExists(self,sap_id,url,input_val, *args):
            tk=Text_Keywords()
            id,ses=tk.attach(sap_id)
            status = sap_constants.TEST_RESULT_FAIL
            result = sap_constants.TEST_RESULT_FALSE
            err_msg=None
            verb = OUTPUT_CONSTANT
            #value=OUTPUT_CONSTANT
            val=input_val[0]
            i = 0
            result = None
            try:

                if(id != None):
                    if(ses.FindById(id).Changeable == True):
                        entries = ses.FindById(id).Entries
                        while True:
                            try:
                                value = entries(i).value
                                i = i + 1
                                if(value == val):
                                    status=sap_constants.TEST_RESULT_PASS
                                    result=sap_constants.TEST_RESULT_TRUE
                            except Exception as e:
                                err_msg = sap_constants.ERROR_MSG
                                break
                    else:
                         err_msg = sap_constants.ERROR_MSG

            except Exception as e:
                  log.error('Error occured',e)
            return status,result,verb,err_msg


        def verifyAllValues(self,sap_id,url,input_val, *args):
            status = sap_constants.TEST_RESULT_FAIL
            result = sap_constants.TEST_RESULT_FALSE
            tk=Text_Keywords()
            id,ses=tk.attach(sap_id)
            val=input_val
            err_msg=None
            verb = OUTPUT_CONSTANT
            i = 0
            dd_entries = []
            result = None
            try:
                if(id != None):
                    if(ses.FindById(id).Changeable == True):
                        entries = ses.FindById(id).Entries
                        while True:
                            try:
                                dd_entries.append(str(entries(i).value))
                                i = i + 1
                            except Exception as e:
                                #print e
                                break
                    if(cmp(dd_entries,val) == 0):

                        result =sap_constants.TEST_RESULT_PASS
                        status =sap_constants.TEST_RESULT_TRUE
                    else:
                      err_msg = sap_constants.ERROR_MSG

            except Exception as e:
                  log.error('Error occured',e)
            return status,result,verb,err_msg



##        def clickOnCombo(self,objectName):
##            try:
##                a = ldtp.getobjectsize(launch_keywords.window_name,objectName);
##                ldtp.generatemouseevent(a[0] + (a[2]) / 2, a[1]+ (a[3] / 2), "b1c")
##            except Exception as e:
##                logger.print_on_console('')


