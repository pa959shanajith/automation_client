#-------------------------------------------------------------------------------
# Name:        getparam.py
# Purpose:
#
# Author:      WASIMAKRAM.SUTAR
#
# Created:     24-10-2016
#Last Updated 27-10-2016
# Copyright:   (c) WASIMAKRAM.SUTAR 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
"""os - Operating system operation (File read, etc) more: https://docs.python.org/3/library/os.html"""
import os

"""csv - The csv module implements classes to read and write tabular data in CSV format. """
import csv

"""xlrd - Extract data from Excel spreadsheets (.xls and .xlsx,"""
import xlrd

"""json - JSON (JavaScript Object Notation) is a lightweight data interchange format inspired by JavaScript object literal syntax """
import json

"""ast - The ast module helps Python applications to process trees of the Python abstract syntax grammar."""
import ast

from xlrd import open_workbook

import logger

import handler

from teststepproperty import TestStepProperty

import controller

import logging

from constants import *

log = logging.getLogger("getparam.py")

"""The xml.etree.ElementTree module implements a simple and efficient API for parsing and creating XML data."""
import xml.etree.ElementTree as ET
class GetParam():
    """Object instantiation of 'getparam,startloop,endloop' object"""
    def __init__(self,index,name,inputval,outputval,stepnum,testscript_name,info_dict,executed,apptype,additionalinfo):
        self.index=index
        self.name=name
        self.inputval=inputval
        self.info_dict=info_dict
        self.testscript_name=testscript_name
        self.outputval=outputval
        self.stepnum=stepnum
        self.executed=executed
        self.apptype=apptype
        self.additionalinfo = additionalinfo
        self.parent_id=0
        self.step_description=''

    def print_step(self):
##        logger.print_on_console('Step: '+str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+str(self.info_dict))
        log.info('Step: '+str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+str(self.info_dict))


    def getparam(self,input):
        """
        def : getParam
        purpose : to check input file for the Data Parameterization is valid or not
        param input : input contains File name, Sheet name(Mandatory) and filters (optional)
        return : Returns Pass if the file is Valid  else Fail
        """
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        status = TEST_RESULT_FAIL
        try:
            """Logic to find the input file is valid or not"""
##            fileinfo = input.split(';')
            fileinfo = input
            filepath = fileinfo[0]
            #need to check dynamic variable for filepath
            filename, file_extension = os.path.splitext(filepath)
            if file_extension[1:].lower() == FILE_TYPE_XLS or file_extension[1:].lower() == FILE_TYPE_XLSX:
                """Excel file check goes here"""
                log.debug('File type : '+ str(file_extension[1:].lower()))
                columnNamesList = []
                columnNamesSet = []
                if len(fileinfo) > 1:
                    filepath = fileinfo[0]
                    sheetname = fileinfo[1]
                    log.debug('Retrieved file name and sheetname ')
                    if os.access(filepath, os.R_OK):
                        log.info('File is accesible')
                        print '\n'
                        logger.print_on_console('File is accesible')
                        wb = open_workbook(filepath)
                        log.info('Work Book object is created')
                        log.debug('Going to iterate through the sheets present in the work book')
                        for s in wb.sheets():
                            if s.name == sheetname:
                                log.info('Input sheet name matched with the actual sheet name')
                                logger.print_on_console('Input sheet name matched with the actual sheet name')
                                logger.print_on_console('Expected: ',s.name)
                                log.info('Expected:')
                                log.info(s.name)
                                logger.print_on_console('Actual: ',sheetname)
                                log.info('Actual:')
                                log.info(sheetname)
                                for col in range(s.ncols):
                                    data = s.cell(0,col).value
                                    log.info('cell information is stored in the data')
                                    if data != '':
                                        log.info('There is some data in the cell store it in the columnNamesList')
                                        columnNamesList.append(data)
                                log.info('Store the data into the set to remove the duplicate column names')
                                columnNamesSet = set(columnNamesList)
                                log.info('Comparing the length of the columnNamesList and columnNamesSet ')
                                if len(columnNamesList) == len(columnNamesSet):
                                    log.info(sheetname + ' contains unique column names, continue..')
                                    logger.print_on_console(sheetname + ' contains unique column names, continue..')
                                    log.info(STATUS_METHODOUTPUT_UPDATE)
                                    status = TEST_RESULT_PASS
                                else:
                                    log.info(sheetname + ' contains duplicate column names')
                                    logger.print_on_console(sheetname + ' contains duplicate column names')

                    else:
                        log.info('File is not accesible')
                        logger.print_on_console('File is not accesible')


            elif file_extension[1:].lower() == FILE_TYPE_CSV:
                """CSV .csv file check goes here"""
                if os.access(filepath, os.R_OK):
                    log.info('File is accesible')
                    filereader = csv.reader(open(filepath))
                    log.info('filereader object is created')
                    columnNamesList = filereader.next()
                    log.info('Store the data into the set to remove the duplicate column names')
                    columnNamesSet = set(columnNamesList)
                    log.info('Comparing the length of the columnNamesList and columnNamesSet ')
                    if len(columnNamesList) == len(columnNamesSet):
                        log.info(filepath + ' contains unique column names, continue..')
                        logger.print_on_console(filepath + ' contains unique column names, continue..')
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = TEST_RESULT_PASS
                    else:
                        log.info(filepath + ' contains duplicate column names')
                        logger.print_on_console(filepath + ' contains duplicate column names')
                else:
                    log.info('File is not accesible')
                    logger.print_on_console('File is not accesible')
            elif file_extension[1:].lower() == FILE_TYPE_XML:
                """XML .xml file check goes here"""
                if os.access(filepath, os.R_OK):
                    columnNamesList = []
                    log.info('File is accesible')
                    xtree = ET.parse(filepath)
                    xroot = xtree.getroot()
                    for topchild in xroot:
                        topch =  topchild
                        for child in topch:
                            log.info('There is some data in the child store it in the columnNamesList')
                            columnNamesList.append(child.tag)
                        break
                    log.info('Store the data into the set to remove the duplicate column names')
                    columnNamesSet = set(columnNamesList)
                    if len(columnNamesList) == len(columnNamesSet):
                        log.info(filepath + ' contains unique column names, continue..')
                        logger.print_on_console(filepath + ' contains unique column names, continue..')
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = TEST_RESULT_PASS
                    else:
                        log.info(filepath + ' contains duplicate column names')
                        logger.print_on_console(filepath + ' contains duplicate column names')
                else:
                    log.info('File is not accesible')
                    logger.print_on_console('File is not accesible')

            return status
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)

    def readcsvfile(self,fileinfo):
        """
        def : readcsvfile
        purpose : To read the content of the csv file and store it in dictionary
        param input : input contains File name, Sheet name(Mandatory) and filters (optional)
        return : Returns dictionary
        """
        try:
            print len(fileinfo)
            if len(fileinfo) > 0:
                allRows = []
                filepath = fileinfo[0]
                if len(fileinfo) > 1 :
                    if fileinfo[1].find(HYPHEN) != -1:
                        filters = fileinfo[1].split(HYPHEN)
                        start = filters[0]
                        end = filters[1]
                        startRow = int(start);
                        endRow = int(end);
                        log.info('Data Param start row: ')
                        log.info(startRow)
                        logger.print_on_console('Data Param start row: ',startRow)
                        log.info('Data Param end row: ')
                        log.info(endRow)
                        logger.print_on_console('Data Param start row: ',endRow)
                    else:
                        filter = fileinfo[1]
                        log.info('Data Param  row: ')
                        log.info(filter)
                        logger.print_on_console('Data Param  row: ',filter)
                filereader = csv.reader(open(filepath))
                testdataexist = False
                for i, line in enumerate(filereader):
                    allRows.append(line)
                myDict = dict()
                colcount = 0;
                rowcount = 0;
                for row in allRows:
                    if rowcount == 0:
                        firstrowelements = row
                        for a in range(len(firstrowelements)):
                            colcount = colcount + 1
                    if rowcount >= 1:
                        testdataexist = True
                    rowcount = rowcount + 1
                logger.print_on_console ('Rowcount : ',rowcount)
                logger.print_on_console( 'Colcount :',colcount)
                if testdataexist == True:
                    for columnindex in range(colcount - 1)  :
                        rowcount1 = 1
                        for row in allRows:
                            if rowcount1 == 0:
                                log.debug('If the row is first row dont read the data')
                                pass
                            else:
                                log.debug('Reading the file data')
                                currentrow = allRows.pop(rowcount1-1)
                                currentcell = currentrow[columnindex]
                                if currentcell != '' or currentcell != None:
                                    with open(filepath, mode='r') as f:
                                        reader = csv.DictReader(f, delimiter=',')
                                        myReader = None
                                        for col in reader.fieldnames:
                                            myDict[col] = []
                                        for row in reader:
                                            for col in reader.fieldnames:
                                                myDict[col].append(row[col])
                                log.debug('Reading data completed')
            log.info('Returning the output dictionary')
            return myDict
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)


    def readxmlfile(self,fileinfo):
        """
        def : readxmlfile
        purpose : To read the content of the xml file and store it in dictionary
        param input : input contains File name, Sheet name(Mandatory) and filters (optional)
        return : Returns dictionary
        """
        try:
            sdata = dict()
            entries = []
            if len(fileinfo) > 0:
                filepath = fileinfo[0]
                xtree = ET.parse(filepath)
                if len(fileinfo) > 1 :
                    if fileinfo[1].find(HYPHEN) != -1:
                        filters = fileinfo[1].split(HYPHEN)
                        start = filters[0]
                        end = filters[1]
                        startRow = int(start);
                        endRow = int(end);
                        log.info('Data Param start row: ')
                        log.info(startRow)
                        logger.print_on_console('Data Param start row: ',startRow)
                        log.info('Data Param end row: ')
                        log.info(endRow)
                        logger.print_on_console('Data Param start row: ',endRow)
                    else:
                        filter = fileinfo[1]
                        log.info('Data Param  row: ')
                        log.info(filter)
                        logger.print_on_console('Data Param  row: ',filter)
                xroot = xtree.getroot()
                for topchild in xroot:
                    topch =  topchild
                    for child in topch:
                        sdata[child.tag] = []
    ##                        break
                for topchild in xroot:
                    topch =  topchild
                    log.debug('Reading data started')
                    for child in topch:
                        if child.text == None:
                            sdata[child.tag].append('')
                        else:
                            sdata[child.tag].append(child.text)
                    log.debug('Reading data completed')
                log.info('Returning the output dictionary')
                return sdata
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)


    def readxlsandxlsxfile(self,fileinfo):
        """
        def : readxlsandxlsxfile
        purpose : To read the content of the xls and xlsx file and store it in dictionary
        param input : input contains File name, Sheet name(Mandatory) and filters (optional)
        return : Returns dictionary
        """
        try:
            sdata = dict()
            if len(fileinfo) > 0:
                filepath = fileinfo[0]
                wb = open_workbook(filepath)
                colname = ''
                if len(fileinfo) > 1 :
                    sheetname = fileinfo[1]
                    for s in wb.sheets():
                        if s.name == sheetname:
                            for col in range(s.ncols):
                                data = s.cell(0,col).value
                                colname = data
                                sdata [colname] = []

                            for row in range(s.nrows):
                                for col in range(s.ncols):
                                    data = s.cell(row,col).value
                                    cname = s.cell(0,col).value
                                    if row == 0:
                                        pass
                                    else:
                                        sdata [cname].append(data)
            data = ast.literal_eval(json.dumps(sdata))
            return data
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)




    def getexternaldatalist(self,input):
        """
        def : getexternaldatalist
        purpose : make calls to perticular file reading methods based on the file type
        param input : input contains File name, Sheet name(Mandatory) and filters (optional)
        return : Returns dictionary
        """

        try:
##            fileinfo = input.split(';')
            fileinfo = input
            #check for dynamic variables for fileinfo
            filepath = fileinfo[0]
            getparamres = self.getparam(input)
            log.info( 'Get Param Result :'+ str(getparamres) )
            logger.print_on_console( 'Get Param Result :',getparamres )
            if getparamres == TEST_RESULT_PASS:
                log.debug( "File is valid, try to fetch the data...")
                #need to check dynamic variable for filepath
                filename, file_extension = os.path.splitext(filepath)
                if file_extension[1:].lower() == FILE_TYPE_XLS or file_extension[1:].lower() == FILE_TYPE_XLSX:
                    log.debug( "Type is Excel")
                    """Excel .xls file check goes here"""
                    externalDataList = self.readxlsandxlsxfile(fileinfo);
                elif file_extension[1:].lower() == FILE_TYPE_CSV:
                    log.debug( "Type is .csv")
                    """CSV .csv file check goes here"""
                    externalDataList = self.readcsvfile(fileinfo);
                    status = TEST_RESULT_PASS
                elif file_extension[1:].lower() == FILE_TYPE_XML:
                    log.debug( "Type is .xml")
                    """XML .xml file check goes here"""
                    externalDataList = self.readxmlfile(fileinfo);
                    status = TEST_RESULT_PASS
                return externalDataList
            else:
                log.error( 'Invalid file! Please provide valid file name and/or sheet name')
                logger.print_on_console(  'Invalid file! Please provide valid file name and/or sheet name')
                return getparamres
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)

    def invokegetparam(self,input):
        """
        def : invokegetparam
        purpose : make calls to getexternaldatalist
        param input : input contains File name, Sheet name(Mandatory) and filters (optional)
        return : Returns dictionary
        """
        data =  self.getexternaldatalist(input)

        return data

    def retrievestaticvariable(self,data,paramindex,row):
        """
        def : retrievestaticvariable
        purpose : To retrieve actual value of the static variable
        param input : data - Dictionary, variable - static variable , row i
        return : Returns actual value of the static variable
        """

        if data !=None:
            teststepproperty =handler.tspList[paramindex]
            inputval = teststepproperty.inputval
            inputlistwithval = []
            inputlistwithval = (list)( inputval)
            try:
                for i in range(0,len(inputval)):
                    inputvalstring = inputval[i]
                    resultinput = inputvalstring
                    inputresult = ''
    ##                staticlist = []

                    # A check should be made to see static variables in evaluate keyword, like |b| - |c|
    ##                staticlist.append(inputvalstring)
                    variable = ''
                    temp = ''
                    columnname = ''
                    arr=[]
                    keywordList=[IF,FOR,JUMP_BY,JUMP_TO]
                    if teststepproperty.name in keywordList :
                        import re
                        static_var_list=re.findall("\|(.*?)\|", inputvalstring)
                        for var in static_var_list:
                            arr.append('|'+var+'|')
                    else:
                        arr = inputvalstring.split(';')
                    for item in arr:
                        if self.checkforstaticvariable(item.strip()):
                            p = 0
                            while p < len(item.strip()) - 1:
                                if(item.find(PIPE) != -1):
                                    temp = item[p+1 : len(item)]
                                    columnname = temp[0:temp.find(PIPE)]
                                    variable = PIPE + columnname + PIPE
                                    p = p + len(variable)
                                    inputresult = data[columnname][row]
                                    if isinstance(inputresult,float):
                                        if inputresult % 1 == 0.0:
                                            inputresult = int(inputresult)
                                    resultinput = resultinput.replace(variable,str(inputresult))
                                    inputlistwithval.insert(i,resultinput)
            except Exception as e:
                log.error(e)

                logger.print_on_console(e)
            return inputlistwithval

    def checkforstaticvariable(self, statvariable):
        """
        def : checkforstaticvariable
        purpose : To check variable is static or not
        param input :  statvariable - static variable
        return : Returns True if the variable is staticvariable else False
        """
        return (statvariable.startswith('|') and statvariable.endswith('|'))

    def add_report_end_iteration(self,reporting_obj,step_description,iteration_count,loop_count):
        #Reporting part
        self.step_description=step_description
        self.parent_id=reporting_obj.get_pid()
        reporting_obj.pop_pid()
        #(iteration_count<loop_count-1) condition i smade to avoid adding of  the Iteration completed message of last iteration step twice t
        # the report
        #since it is added in the 'methodInvocation' in controller
        if self.name.lower() != ENDLOOP and (iteration_count<loop_count-1):
            reporting_obj.generate_report_step(self,'',step_description,'3.00',False)
        reporting_obj.remove_nested_flag()
        #Reporting part ends

    def add_report_step_getparam(self,reporting_obj,step_description):
        #Reporting part
        self.step_description=step_description
        self.parent_id=reporting_obj.get_pid()
        reporting_obj.add_pid(reporting_obj.name)
        reporting_obj.generate_report_step(self,'',step_description,'3.00',False)
        #Reporting part ends

    def performdataparam(self,input,con,reporting_obj):
        try:

            endlopnum = self.info_dict[0].keys()[0]
            return_value=endlopnum + 1
            self.executed=True

            if self.name.lower() == ENDLOOP:
                step_description='EndLoop : Data Parameterization completed'
                #Reporting part
                self.add_report_end_iteration(reporting_obj,step_description,0,0)
                #Reporting part ends
                return self.index + 1

            if self.name.lower() == STARTLOOP:
                self.step_description='StartLoop'
                self.parent_id=reporting_obj.get_pid()
                return self.index + 1



            if self.getparam(input) == TEST_RESULT_PASS :
                step_description='Data Parameterization started'
                fileinfo = input
                filepath = fileinfo[0]
                data = self.invokegetparam(input)
                startRow = None
                endRow =None
                filter = None
                k = 1
                filename, file_extension = os.path.splitext(filepath)
                if file_extension[1:].lower() == FILE_TYPE_XLS or file_extension[1:].lower() == FILE_TYPE_XLSX:
                    if len(fileinfo) == 2 :
                        if fileinfo[1].find(HYPHEN) != -1:
                            filters = fileinfo[1].split(HYPHEN)
                            start = filters[0]
                            #start - check for dynamic variable
                            end = filters[1]
                            #end - check for dynamic variable
                            startRow = int(start);
                            endRow = int(end);
                            log.info('Data Param start row: ')
                            log.info(startRow)
                            logger.print_on_console('Data Param start row: ',startRow)
                            log.info('Data Param end row: ')
                            log.info(endRow)
                            logger.print_on_console('Data Param start row: ',endRow)
                    elif len(fileinfo) == 3 :
                        if fileinfo[2].find(HYPHEN) != -1:
                            filters = fileinfo[2].split(HYPHEN)
                            start = filters[0]
                            #start - check for dynamic variable
                            end = filters[1]
                            #end - check for dynamic variable
                            startRow = int(start);
                            endRow = int(end);
                            log.info('Data Param start row: ')
                            log.info(startRow)
                            logger.print_on_console('Data Param start row: ',startRow)
                            log.info('Data Param end row: ')
                            log.info(endRow)
                            logger.print_on_console('Data Param start row: ',endRow)
                        else:
                            filter1 = fileinfo[2]
                            filter = int(filter1)
                            log.info('Data Param  row: ')
                            log.info(filter)
                            logger.print_on_console('Data Param  row: ',filter)
                else:
                    if len(fileinfo) == 2 :
                        if fileinfo[1].find(HYPHEN) != -1:
                            filters = fileinfo[1].split(HYPHEN)
                            start = filters[0]
                            #start - check for dynamic variable
                            end = filters[1]
                            #end - check for dynamic variable
                            startRow = int(start);
                            endRow = int(end);
                            log.info('Data Param start row: ')
                            log.info(startRow)
                            logger.print_on_console('Data Param start row: ',startRow)
                            log.info('Data Param end row: ')
                            log.info(endRow)
                            logger.print_on_console('Data Param start row: ',endRow)
                        else:
                            filter1 = fileinfo[1]
                            filter = int(filter1)
                            log.info('Data Param  row: ')
                            log.info(filter)
                            logger.print_on_console('Data Param  row: ',filter)

                if startRow !=None and endRow != None:
                    log.info( '***Data Parameterization started***')
                    logger.print_on_console( '***Data Parameterization started***')
                    #Reporting part
                    reporting_obj.name=GETPARAM
                    self.add_report_step_getparam(reporting_obj,step_description)
                    #Reporting part ends
                    for i in range(startRow,endRow+1):
                        if self.name.lower()==GETPARAM:
                            inputval = self.inputval[0]
                            paramindex = self.index+1;
                            if (inputval != None):
                                j = 0
                                log.info(  '***Data Param: Iteration '+ str(k) +  ' started***')
                                logger.print_on_console(  '***Data Param: Iteration ',k, ' started***')
                                step_description='Data Param: Iteration '+str(k)+' started'
                                reporting_obj.name='Iteration '+str(k)
                                self.add_report_step_getparam(reporting_obj,step_description)
                                iterations = len(data.values()[0])
                                while (paramindex < endlopnum):
                                    input = self.retrievestaticvariable(data,paramindex,i-1)
                                    paramindex =con.methodinvocation(paramindex,input)
                                    if paramindex in [TERMINATE,BREAK_POINT]:
                                        return paramindex
                                log.info( '***Data Param: Iteration ' + str(k) + ' completed***\n\n')
                                logger.print_on_console( '***Data Param: Iteration ',k, ' completed***\n\n')
                                #Reporting part
                                step_description='Data Param: Iteration '+str(k)+' completed'
                                reporting_obj.name='Iteration '+str(k)
                                self.add_report_end_iteration(reporting_obj,step_description,k,endRow+1)
                                #Reporting part ends
                                k = k + 1
                    log.info( '***Data Parameterization completed***')
                    logger.print_on_console( '***Data Parameterization completed***')

                    return_value=paramindex

                elif filter != None:
                    log.info( '***Data Parameterization started***')
                    logger.print_on_console('***Data Parameterization started***')
                    #Reporting part
                    reporting_obj.name=GETPARAM
                    self.add_report_step_getparam(reporting_obj,step_description)
                    #Reporting part ends
                    if self.name.lower()==GETPARAM:
                        inputval = self.inputval[0]
                        paramindex = self.index+1;
                        if (inputval != None):
                            log.info( '***Data Param: Iteration '+str(k)+ ' started***')
                            logger.print_on_console( '***Data Param: Iteration ',k, ' started***')
                            #Reporting part
                            step_description='Data Param: Iteration '+str(k)+' started'
                            reporting_obj.name='Iteration '+str(k)
                            self.add_report_step_getparam(reporting_obj,step_description)
                            #Reporting part ends
                            iterations = len(data.values()[0])
                            while (paramindex < endlopnum):
                                    input = self.retrievestaticvariable(data,paramindex,filter-1)
                                    paramindex =con.methodinvocation(paramindex,input)
                                    if paramindex in [TERMINATE,BREAK_POINT]:
                                        return paramindex
                            log.info( '***Data Param: Iteration '+str(k)+ ' completed***\n\n')
                            logger.print_on_console('***Data Param: Iteration ',k, ' completed***\n\n')
                            #Reporting part
                            step_description='Data Param: Iteration '+str(k)+' completed'
                            reporting_obj.name='Iteration '+str(k)
                            self.add_report_end_iteration(reporting_obj,step_description,k,k)
                            #Reporting part ends
                            k = k + 1
                    log.info( '***Data Parameterization completed***')
                    logger.print_on_console( '***Data Parameterization completed***')

                    return_value=paramindex

                else:
                    log.info( '***Data Parameterization started***')
                    logger.print_on_console('***Data Parameterization started***')
                    #Reporting part
                    reporting_obj.name=GETPARAM
                    self.add_report_step_getparam(reporting_obj,step_description)
                    #Reporting part ends
                    count=len(data.values()[0])
                    for i in range(count):
                        if self.name.lower()==GETPARAM:
                            inputval = self.inputval[0]
                            paramindex = self.index+1;
                            if (inputval != None):
                                log.info( '***Data Param: Iteration '+str(k)+ ' started***')
                                logger.print_on_console( '***Data Param: Iteration ',k, ' started***')
                                #Reporting part
                                reporting_obj.name='Iteration '+str(k)
                                step_description='Data Param: Iteration '+str(k)+' started'
                                self.add_report_step_getparam(reporting_obj,step_description)
                                #Reporting part ends
                                iterations = len(data.values()[0])
                                logger.print_on_console ('Iterations : ',iterations)
                                while (paramindex < endlopnum):
                                    input = self.retrievestaticvariable(data,paramindex,i)
                                    paramindex =con.methodinvocation(paramindex,input)
                                    if paramindex in [TERMINATE,BREAK_POINT]:
                                        return paramindex
                                log.info( '***Data Param: Iteration '+str(k)+ ' completed***\n\n')
                                logger.print_on_console('***Data Param: Iteration ',k, ' completed***\n\n')
                                #Reporting part
                                step_description='Data Param: Iteration '+str(k)+' completed'
                                reporting_obj.name='Iteration '+str(k)
                                self.add_report_end_iteration(reporting_obj,step_description,k,count)
                                #Reporting part ends
                                k = k + 1

                    log.info( '***Data Parameterization completed***')
                    logger.print_on_console( '***Data Parameterization completed***')
                    return_value=paramindex
            else:
                log.error( 'Data parameterization failed : Wrong file name/ Sheet name given')
                log.error( 'Wrong file name/ Sheet name given, Please check and provide valid one')
                logger.print_on_console( 'Data parameterization failed : Wrong file name/ Sheet name given')
                logger.print_on_console('Wrong file name/ Sheet name given, Please check and provide valid one')
                #Reporting part
                step_description='Data Parameterization failed'
                self.add_report_step_getparam(reporting_obj,step_description)
                #Reporting part ends

        except Exception as e:
            log.error( 'Data parameterization failed')
            log.error( 'Wrong filters given, please check and provide correct one')
            logger.print_on_console( 'Data parameterization failed')
            logger.print_on_console( 'Wrong filters given, please check and provide correct one')
            #Reporting part
            step_description='Data Parameterization failed : Wrong filters given'
            self.add_report_end_iteration(reporting_obj,step_description,0,0)
            #Reporting part ends

            log.error(e)

            logger.print_on_console(e)
        return return_value






