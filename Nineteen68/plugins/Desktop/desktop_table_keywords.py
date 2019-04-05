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
log = logging.getLogger('desktop_table_keywords.py')

class Table_Keywords():
    def get_cell_value(self, element, parent, input_val, *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        dictq={}
        try:
            if(len(input_val)>=2):
                indexi=int(input_val[0])
                indexj=int(input_val[1])
                const=0
                if(element.friendly_class_name()=='Table' and element.texts()[0]=='DataGridView'):
                    log.info('Valid row and col number')
                    c=element.children()
                    for i in range(0,len(c)):
                        if c[i].friendly_class_name().lower() == "scrollbar":
                            const+=1
                    b=c[1].children()
                    for i in range(const+1,len(c)):
                        a=c[i].children()
                        dicttab={}
                        for j in range(len(a)):
                            key=j+1
                            value=a[j].legacy_properties()['Value']
                            dicttab[key]=value
                        dictq[i-const]=dicttab
                    status = desktop_constants.TEST_RESULT_PASS
                    result = desktop_constants.TEST_RESULT_TRUE
                    verb=dictq[indexi][indexj]
                    log.info('Returning value in row ',indexi,' col ',indexj)
                else:
                    log.info('Invalid row or col number')
                    err_msg='Invalid row or col number'
                    logger.print_on_console('Invalid row or col number')
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
                log.info('Row and Col number not specified')
                err_msg='Row and Col number not specified'
                logger.print_on_console('Row and Col number not specified')
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)

        return status,result,verb,err_msg

    def get_row_count(self,element,parent,input_val,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if(element.friendly_class_name()=='Table' and element.texts()[0]=='DataGridView'):
                c=element.children()
                const=0
                for i in range(0,len(c)):
                    if c[i].friendly_class_name().lower() == "scrollbar":
                        const+=1
                log.info('Number of rows is',len(c)-const+1)
                status = desktop_constants.TEST_RESULT_PASS
                result = desktop_constants.TEST_RESULT_TRUE
                verb=len(c)-2
            else:
                log.info('Unable to get row count')
                err_msg='Unable to get row count'
                logger.print_on_console('Unable to get row count')
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)

        return status,result,verb,err_msg

    def get_col_count(self,element,parent,input_val,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if(element.friendly_class_name()=='Table' and element.texts()[0]=='DataGridView'):
                c=element.children()
                log.info('Number of rows is',len(c[1].children()))
                status = desktop_constants.TEST_RESULT_PASS
                result = desktop_constants.TEST_RESULT_TRUE
                verb=len(c[1].children())
            else:
                log.info('Unable to get col count')
                err_msg='Unable to get col count'
                logger.print_on_console('Unable to get col count')
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)

        return status,result,verb,err_msg

    def select_row(self,element,parent,input_val,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if(len(input_val)>=1):
                index=int(input_val[0])
                if(element.friendly_class_name()=='Table' and element.texts()[0]=='DataGridView'):
                    log.info('Valid row number')
                    c=element.children()
                    const=0
                    for i in range(0,len(c)):
                        if c[i].friendly_class_name().lower() == "scrollbar":
                            const+=1
                    if (len(c)-const-1)>=index:
                        c[const+index].click_input()
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
            else:
                log.info('Unable to select row')
                err_msg='Unable to select row'
                logger.print_on_console('Unable to select row')
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)

        return status,result,verb,err_msg

    def get_row_num_by_text(self,element,parent,input_val,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        dictq={}
        try:
            if(len(input_val)>=1):
                valuei=str(input_val[0])
                const=0
                flag=0
                if(element.friendly_class_name()=='Table' and element.texts()[0]=='DataGridView'):
                    log.info('Valid row number')
                    c=element.children()
                    for i in range(0,len(c)):
                        if c[i].friendly_class_name().lower() == "scrollbar":
                            const+=1
                    b=c[1].children()
                    for i in range(const+1,len(c)):
                        a=c[i].children()
                        dicttab={}
                        for j in range(len(a)):
                            key=j+1
                            value=a[j].legacy_properties()['Value']
                            dicttab[key]=value
                        dictq[i-const]=dicttab
                    newkey=[]
                    for key1 in list(dictq.keys()):
                        for k,v in list(dictq[key1].items()):
                            if v==valuei:
                                newkey.append(key1)
                                flag+=1
                    if flag==1:
                        verb=newkey[0]
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info('Value is found in row number',verb)
                    elif flag>1:
                        verb=newkey
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info('Values are found in row numbers : ',verb)
            else:
                log.info('Unable to select row')
                err_msg='Unable to select row'
                logger.print_on_console('Unable to select row')
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        return status,result,verb,err_msg

    def get_col_num_by_text(self,element,parent,input_val,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        dictq={}
        try:
            if(len(input_val)>=1):
                valuei=str(input_val[0])
                const=0
                flag=0
                if(element.friendly_class_name()=='Table' and element.texts()[0]=='DataGridView'):
                    log.info('Valid row number')
                    c=element.children()
                    for i in range(0,len(c)):
                        if c[i].friendly_class_name().lower() == "scrollbar":
                            const+=1
                    b=c[1].children()
                    for i in range(const+1,len(c)):
                        a=c[i].children()
                        dicttab={}
                        for j in range(len(a)):
                            key=j+1
                            value=a[j].legacy_properties()['Value']
                            dicttab[key]=value
                        dictq[i-const]=dicttab
                    newkey=[]
                    for key1 in list(dictq.keys()):
                        for k,v in list(dictq[key1].items()):
                            if v==valuei:
                                newkey.append(k)
                                flag+=1
                    if flag==1:
                        verb=newkey[0]
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info('Value is found in column number',key)
                    elif flag>1:
                        verb=newkey
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info('Values are found in column numbers : ',verb)
            else:
                log.info('Unable to select col')
                err_msg='Unable to select col'
                logger.print_on_console('Unable to select col')
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)

        return status,result,verb,err_msg

    def verify_cell_value(self, element, parent, input_val, *args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        dictq={}
        try:
            if(len(input_val)>=3):
                indexi=int(input_val[0])
                indexj=int(input_val[1])
                valuei=str(input_val[2])
                const=0
                if(element.friendly_class_name()=='Table' and element.texts()[0]=='DataGridView'):
                    log.info('Valid row number')
                    c=element.children()
                    for i in range(0,len(c)):
                        if c[i].friendly_class_name().lower() == "scrollbar":
                            const+=1
                    b=c[1].children()
                    for i in range(const+1,len(c)):
                        a=c[i].children()
                        dicttab={}
                        for j in range(len(a)):
                            key=j+1
                            value=a[j].legacy_properties()['Value']
                            dicttab[key]=value
                        dictq[i-const]=dicttab
                    if (dictq[indexi][indexj]==valuei):
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
                        log.info('Returning value in row ',indexi,' col ',indexj,' value ',valuei)
                else:
                    log.info('Invalid row or col number')
                    err_msg='Invalid row or col number'
                    logger.print_on_console('Invalid row or col number')
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
                log.info('Row and Col number not specified')
                err_msg='Invalid row or col number'
                logger.print_on_console('Invalid row or col number')
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)

        return status,result,verb,err_msg

    def click_cell(self,element,parent,input_val,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if(len(input_val)>=2):
                indexi=int(input_val[0])
                indexj=int(input_val[1])
                if(element.friendly_class_name()=='Table' and element.texts()[0]=='DataGridView'):
                    log.info('Valid row number')
                    c=element.children()
                    const=0
                    for i in range(0,len(c)):
                        if c[i].friendly_class_name().lower() == "scrollbar":
                            const+=1
                    if (len(c)-const-1)>=indexi:
                        a=c[const+indexi].children()
                        a[indexj-1].click_input()
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
            else:
                log.info('Unable to select row')
                err_msg='Unable to select row'
                logger.print_on_console('Unable to select row')
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        return status,result,verb,err_msg

    def double_click_cell(self,element,parent,input_val,*args):
        status=desktop_constants.TEST_RESULT_FAIL
        result=desktop_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            if(len(input_val)>=2):
                indexi=int(input_val[0])
                indexj=int(input_val[1])
                if(element.friendly_class_name()=='Table' and element.texts()[0]=='DataGridView'):
                    log.info('Valid row number')
                    c=element.children()
                    const=0
                    for i in range(0,len(c)):
                        if c[i].friendly_class_name().lower() == "scrollbar":
                            const+=1
                    if (len(c)-const-1)>=indexi:
                        a=c[const+indexi].children()
                        a[indexj-1].click_input(double=True)
                        status = desktop_constants.TEST_RESULT_PASS
                        result = desktop_constants.TEST_RESULT_TRUE
            else:
                log.info('Unable to select row')
                err_msg='Unable to select row'
                logger.print_on_console('Unable to select row')
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        return status,result,verb,err_msg