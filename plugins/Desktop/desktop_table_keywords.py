#-------------------------------------------------------------------------------
# Name:        desktop_table_keywords
# Purpose:     To automate Table object/element in a give window
#
# Author:      rakshak.kamath
#
# Created:     06-08-2018
# Copyright:   (c) rakshak.kamath 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import desktop_launch_keywords
import pywinauto
from desktop_editable_text import Text_Box
import logger
import desktop_constants
import desktop_editable_text
import time
import string
from constants import *
import logging
log = logging.getLogger( 'desktop_table_keywords.py' )

class Table_Keywords():
    def get_cell_value(self, element, parent, input_val, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        dictq = {}
        try:
            if( len(input_val) >= 2):
                indexi = int(input_val[0])
                indexj = int(input_val[1])
                #get row and col count
                col = self.get_col_count(element, '', '', '')
                row = self.get_row_count(element, '', '', '')
                if ( row[2] >= indexi > 0  and col[2] >= indexj > 0 ):
                    const = 0
                    if ( element.friendly_class_name() == 'Table' and element.texts()[0] == 'DataGridView' ):
                        log.info( 'Valid row and col number' )
                        c = element.children()
                        for i in range(0, len(c)):
                            if ( c[i].friendly_class_name().lower() == "scrollbar" ):
                                const += 1
                        b = c[1].children()
                        for i in range(const + 1, len(c)):
                            a = c[i].children()
                            dicttab = {}
                            for j in range(len(a)):
                                key = j + 1
                                value = a[j].legacy_properties()['Value']
                                dicttab[key] = value
                            dictq[i - const] = dicttab
                        verb = dictq[indexi][indexj]
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info( 'Returning value in row :', indexi, ' col :', indexj )
                else:
                    err_msg = 'Invalid row or col number'
            else:
                err_msg = 'Row and Col number not specified'
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
            logger.print_on_console( err_msg )
            log.error( err_msg )
        return status, result, verb, err_msg

    def get_row_count(self, element, parent, input_val, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        try:
            if ( element.friendly_class_name() == 'Table' and element.texts()[0] == 'DataGridView' ):
                c = element.children()
                const = 0
                for i in range(0, len(c)):
                    if ( c[i].friendly_class_name().lower() == "scrollbar" ):
                        const += 1
                log.info( 'Number of rows is : ', len(c) - const + 1)
                status = desktop_constants.TEST_RESULT_PASS
                result = desktop_constants.TEST_RESULT_TRUE
                verb = len(c) - 1 - const
            else:
                err_msg = 'Unable to get row count'
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
            logger.print_on_console( err_msg )
            log.error( err_msg )
        return status, result, verb, err_msg

    def get_col_count(self, element, parent, input_val, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        row_ele = None
        try:
            if ( element.friendly_class_name() == 'Table' and element.texts()[0] == 'DataGridView' ):
                c = element.children()
                for i in range(0, len(c)):
                    if( str(c[i].friendly_class_name().lower()) != 'scrollbar' ):
                        log.debug( 'Element is of type : ' + str(c[i].friendly_class_name().lower()) )
                        row_ele = c[i]
                        break
                log.info( 'Number of rows is', len(row_ele.children()) )
                status = desktop_constants.TEST_RESULT_PASS
                result = desktop_constants.TEST_RESULT_TRUE
                verb = len(row_ele.children())
            else:
                err_msg = 'Unable to get col count'
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
            logger.print_on_console( err_msg )
            log.error( err_msg )
        return status, result, verb, err_msg

    def select_row(self, element, parent, input_val, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        try:
            if ( len(input_val) >= 1 ):
                index = int(input_val[0])
                if ( element.friendly_class_name() == 'Table' and element.texts()[0] == 'DataGridView' ):
                    log.info( 'Valid row number' )
                    c = element.children()
                    const = 0
                    for i in range(0,len(c)):
                        if ( c[i].friendly_class_name().lower() == "scrollbar" ):
                            const += 1
                    if ( (len(c) - const - 1) >= index ):
                        c[const + index].click_input()
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
            else:
                err_msg = 'Unable to select row'
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
            logger.print_on_console( err_msg )
            log.error( err_msg )
        return status, result, verb, err_msg

    def get_row_num_by_text(self, element, parent, input_val, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        dictq = {}
        try:
            if( len(input_val) >= 1 ):
                valuei = str(input_val[0])
                const = 0
                flag = 0
                if( element.friendly_class_name() == 'Table' and element.texts()[0] == 'DataGridView'):
                    log.info( 'Valid row number' )
                    c = element.children()
                    for i in range(0, len(c)):
                        if ( c[i].friendly_class_name().lower() == "scrollbar" ):
                            const += 1
                    b = c[1].children()
                    for i in range(const + 1, len(c)):
                        a = c[i].children()
                        dicttab = {}
                        for j in range(len(a)):
                            key = j + 1
                            value = a[j].legacy_properties()['Value']
                            dicttab[key] = value
                        dictq[i - const] = dicttab
                    newkey = []
                    for key1 in list(dictq.keys()):
                        for k, v in list(dictq[key1].items()):
                            if ( v == valuei ):
                                newkey.append(key1)
                                flag += 1
                    if ( flag == 1 ):
                        verb = newkey[0]
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info( 'Value is found in row number', verb )
                    elif ( flag > 1 ):
                        verb = newkey
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info( 'Values are found in row numbers : ', verb )
            else:
                err_msg = 'Unable to select row'
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
            logger.print_on_console( err_msg )
            log.error( err_msg )
        return status, result, verb, err_msg

    def get_col_num_by_text(self, element, parent, input_val, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        dictq = {}
        try:
            if( len(input_val) >= 1):
                valuei = str(input_val[0])
                const = 0
                flag = 0
                if( element.friendly_class_name() == 'Table' and element.texts()[0] == 'DataGridView' ):
                    log.info( 'Valid row number' )
                    c = element.children()
                    for i in range(0,len(c)):
                        if ( c[i].friendly_class_name().lower() == "scrollbar" ):
                            const += 1
                    b = c[1].children()
                    for i in range(const + 1, len(c)):
                        a = c[i].children()
                        dicttab = {}
                        for j in range(len(a)):
                            key = j + 1
                            value = a[j].legacy_properties()['Value']
                            dicttab[key] = value
                        dictq[i - const] = dicttab
                    newkey=[]
                    for key1 in list(dictq.keys()):
                        for k, v in list(dictq[key1].items()):
                            if ( v == valuei ):
                                newkey.append(k)
                                flag += 1
                    if ( flag ==1 ):
                        verb = newkey[0]
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info( 'Value is found in column number : ', key )
                    elif ( flag > 1):
                        verb = newkey
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info( 'Values are found in column numbers : ', verb )
            else:
                err_msg = 'Unable to select column'
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
            logger.print_on_console( err_msg )
            log.error( err_msg )
        return status, result, verb, err_msg

    def verify_cell_value(self, element, parent, input_val, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        dictq = {}
        try:
            if ( len(input_val) >= 3 ):
                indexi = int(input_val[0])
                indexj = int(input_val[1])
                valuei = str(input_val[2])
                const = 0
                if ( element.friendly_class_name() == 'Table' and element.texts()[0] == 'DataGridView'):
                    log.info( 'Valid row number' )
                    c = element.children()
                    for i in range(0,len(c)):
                        if ( c[i].friendly_class_name().lower() == "scrollbar" ):
                            const += 1
                    b = c[1].children()
                    for i in range(const + 1, len(c)):
                        a = c[i].children()
                        dicttab = {}
                        for j in range(len(a)):
                            key = j + 1
                            value = a[j].legacy_properties()['Value']
                            dicttab[key] = value
                        dictq[i-const] = dicttab
                    if ( dictq[indexi][indexj] == valuei ):
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info( 'Returning value in row : ',indexi,' ,col : ',indexj,' ,value : ',valuei)
                else:
                    err_msg = 'Invalid row or column number'
            else:
                #return entire dict to output variable
    ##            if(element.friendly_class_name()=='Table' and element.texts()[0].encode('utf-8')=='DataGridView'):
    ##                log.info('No row number entered')
    ##                c=element.children()
    ##                b=c[1].children()
    ##                for i in range(2,len(c)):
    ##                    a=c[i].children()
    ##                    dicttab={}
    ##                    for j in range(len(a)):
    ##                        key=b[j].legacy_properties()['Value'].encode('utf-8')
    ##                        value=a[j].legacy_properties()['Value'].encode('utf-8')
    ##                        dicttab[key]=value
    ##                    dictq[i-2]=dicttab
    ##            verb=dictq
    ##            status = desktop_constants.TEST_RESULT_PASS
    ##            result = desktop_constants.TEST_RESULT_TRUE
                #---------------------------------------------
                err_msg = 'Row and Col number not specified / Invalid row or col number'
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
            logger.print_on_console( err_msg )
            log.error( err_msg )
        return status, result, verb, err_msg

    def click_cell(self, element, parent, input_val, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        try:
            if ( len(input_val) >= 2 ):
                indexi = int(input_val[0])
                indexj = int(input_val[1])
                if ( element.friendly_class_name() == 'Table' and element.texts()[0] == 'DataGridView'):
                    log.info('Valid row number')
                    c = element.children()
                    const = 0
                    for i in range(0, len(c)):
                        if ( c[i].friendly_class_name().lower() == "scrollbar" ):
                            const += 1
                    if ( (len(c) - const-1) >= indexi ):
                        a = c[const + indexi].children()
                        a[indexj - 1].click_input()
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
            else:
                err_msg = 'Unable to select row'
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
            logger.print_on_console( err_msg )
            log.error( err_msg )
        return status, result, verb, err_msg

    def double_click_cell(self, element, parent, input_val, *args):
        status = desktop_constants.TEST_RESULT_FAIL
        result = desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg = None
        try:
            if( len(input_val) >= 2 ):
                indexi = int(input_val[0])
                indexj = int(input_val[1])
                if ( element.friendly_class_name() == 'Table' and element.texts()[0] == 'DataGridView' ):
                    log.info('Valid row number')
                    c = element.children()
                    const = 0
                    for i in range(0, len(c)):
                        if ( c[i].friendly_class_name().lower() == "scrollbar" ):
                            const += 1
                    if ( (len(c) - const-1) >= indexi ):
                        a = c[const + indexi].children()
                        a[indexj - 1].click_input(double = True)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
            else:
                err_msg = 'Unable to select row'
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = desktop_constants.ERROR_MSG + ' : ' + str(e)
            logger.print_on_console( err_msg )
            log.error( err_msg )
        return status, result, verb, err_msg
