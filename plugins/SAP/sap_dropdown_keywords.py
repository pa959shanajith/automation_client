#-------------------------------------------------------------------------------
# Name:        SAP_Dropdown_Keywords
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
from constants import *
from saputil_operations import SapUtilKeywords
from sap_launch_keywords import Launch_Keywords
import logging
log = logging.getLogger( 'sap_dropdown_keywords.py' )

class Dropdown_Keywords():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()

    def getSelected(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( ses.FindById(id).Changeable == True ):
                    value = ses.FindById(id).Text.strip()
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.ELEMENT_NOT_CHANGEABLE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Get Selected" )
        return status, result, value ,err_msg


    def selectValueByIndex(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        i = 0
        arr_v = []
        arr_k = []
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( ses.FindById(id).Changeable == True ):
                    entries = ses.FindById(id).Entries
                    while True:
                        try:
                            arr_v.append(entries(i).value)
                            arr_k.append(entries(i).key)
                        except :
                            break
                        i = i + 1
                    try:
                        if ( len(input_val) > 1 ):
                            inp = input_val[3]
                        else:
                            inp = input_val[0]
                        ses.FindById(id).key = arr_k[int(inp)]
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                        del inp, entries, id, ses
                    except Exception as e:
                        err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
                        log.error( err_msg )
                        logger.print_on_console( "Error occured : Index out of bound" )
                else:
                    err_msg = sap_constants.ELEMENT_NOT_CHANGEABLE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in getValueByIndex" )
        del i, arr_k, arr_v, sap_id, input_val
        return status, result, value, err_msg

    def getValueByIndex(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        i = 0
        arr = []
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( ses.FindById(id).Changeable == True ):
                    entries = ses.FindById(id).Entries
                    while True:
                        try:
                            arr.append(entries(i).value)
                        except :
                            break
                        i = i + 1
                    try:
                        value = arr[int(input_val[0])]
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    except Exception as e:
                        err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
                        log.error( err_msg )
                        logger.print_on_console( "Error occured : Index out of bound" )
                else:
                    err_msg = sap_constants.ELEMENT_NOT_CHANGEABLE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in getValueByIndex" )
        return status, result, value, err_msg

    def getKeyByIndex(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        i = 0
        arr = []
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( ses.FindById(id).Changeable == True ):
                    entries = ses.FindById(id).Entries
                    while True:
                        try:
                            arr.append(entries(i).key)
                        except :
                            break
                        i = i + 1
                    try:
                        value = arr[int(input_val[0])]
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    except Exception as e:
                        err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
                        log.error( err_msg )
                        logger.print_on_console( "Error occured : Index out of bound" )
                else:
                    err_msg = sap_constants.ELEMENT_NOT_CHANGEABLE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Get Key By Index" )
        return status, result, value, err_msg

    def selectValueByText(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( len(input_val) > 1 ):
                    text = input_val[3]
                else:
                    text = input_val[0]
                i = 0
                if ( ses.FindById(id).Changeable == True ):
                    entries = ses.FindById(id).Entries
                    while True:
                        try:
                            if ( entries(i).value.strip() == text.strip() ):
                                ses.FindById(id).value = text
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                                flag = True
                        except:
                            break
                        i = i + 1
                    if ( flag == False ) :
                        err_msg = sap_constants.INVALID_INPUT
                else:
                    err_msg = sap_constants.ELEMENT_NOT_CHANGEABLE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Select Value By Text" )
        return status, result, value, err_msg

    def selectKeyByText(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        flag = False
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( len(input_val) > 1 ):
                    text = input_val[3]
                else:
                    text = input_val[0]
                i = 0
                if ( ses.FindById(id).Changeable == True ):
                    entries = ses.FindById(id).Entries
                    while True:
                        try:
                            if ( entries(i).key.strip() == text.strip() ):
                                ses.FindById(id).key = text
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                                flag = True
                        except:
                            break
                        i = i + 1
                    if ( flag == False ) :
                        err_msg = sap_constants.INVALID_INPUT
                else:
                    err_msg = sap_constants.ELEMENT_NOT_CHANGEABLE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Select Key By Text" )
        return status, result, value, err_msg

    def verifySelectedValue(self, sap_id, input_val ,*args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( ses.FindById(id).Changeable == True ):
                    if ( ses.FindById(id).Text.strip() == input_val[0] ):
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = "Input text and Element text do not match"
                else:
                    err_msg = sap_constants.ELEMENT_NOT_CHANGEABLE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Verify Selected Value" )
        return status, result, value, err_msg


    def getCount(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        value = OUTPUT_CONSTANT
        err_msg = None
        count = 0
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                if ( ses.FindById(id).type == "GuiComboBox" ):
                    entries = ses.FindById(id).Entries
                    value = count
                    while True:
                        try:
                            value = entries(count).value
                            count = count + 1
                            value = count
                        except:
                            break
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Get Count" )
        return status, result, value, err_msg

    def verifyCount(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        count = 0
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                value = count
                entries = ses.FindById(id).Entries
                while True:
                    try:
                        if ( entries(count).value.isspace() ):
                            count = count + 1
                            continue
                        count = count + 1
                        value = value + 1
                    except:
                        break
                if ( int(input_val[0]) == value ):
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = 'Count Verify has failed '
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Verify Count" )
        return status, result, verb, err_msg

    def verifyValuesExists(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        verb = OUTPUT_CONSTANT
        dd_entries = []
        i = 0
        flag = True
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                entries = ses.FindById(id).Entries
                while True:
                    try:
                        if ( not (entries(i).value.isspace()) ):
                            dd_entries.append(str(entries(i).value).lower())
                        i = i + 1
                    except Exception as e:
                        break
                for inp in input_val:
                    if ( inp.lower().strip() not in dd_entries ):
                        flag = False
                        break
                if ( flag == True ):
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = "No matching data found"
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Verify Values Exists" )
        return status, result, verb, err_msg

    def getAllKeyValuePairs(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        i = 0
        dd_entries = []
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id,ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                entries = ses.FindById(id).Entries
                while True:
                    try:
                        kv_entries = []
                        kv_entries.append(str(entries(i).key))
                        kv_entries.append(str(entries(i).value))
                        dd_entries.append(kv_entries)
                        i = i + 1
                    except:
                        break
                    value = dd_entries
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = "No matching data found"
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Get All Key Value Pair" )
        return status, result, value, err_msg


    def verifyAllValues(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        i = 0
        dd_entries = []
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id,ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                entries = ses.FindById(id).Entries
                while True:
                    try:
                        if ( not (entries(i).value.isspace()) ):
                            dd_entries.append(str(entries(i).value))
                        i = i + 1
                    except:
                        break
                flag = True
                if ( len(dd_entries) == len(input_val) ):
                    for dd in dd_entries:
                        if ( dd not in input_val ):
                            flag = False
                else:
                    flag = False
                if ( flag == True ):
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = "No matching data found"
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #------------------------logging error messages
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( "Error occured in Verify All Values" )
        return status, result, value, err_msg