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
import re
import logger
import handler
import dynamic_variable_handler
from teststepproperty import TestStepProperty
import controller
import logging
from constants import *
statCnt=0

log = logging.getLogger("getparam.py")

"""The xml.etree.ElementTree module implements a simple and efficient API for parsing and creating XML data."""
import xml.etree.ElementTree as ET
class GetParam():
    """Object instantiation of 'getparam,startloop,endloop' object"""
    def __init__(self,index,name,inputval,outputval,stepnum,testscript_name,info_dict,executed,apptype,additionalinfo,testcase_num,remark,testcase_details):
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
        self.testcase_num=testcase_num
        self.remarks=remark
        self.testcase_details=testcase_details

    def print_step(self):
        ##        logger.print_on_console('Step: '+str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+str(self.info_dict))
        log.info('Step: '+str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+str(self.info_dict))


    def getparam(self,input,datatables):
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
                        # log.info('File is accesible')
                        # logger.print_on_console('File is accesible')
                        wb = open_workbook(filepath)
                        log.info('Work Book object is created')
                        log.debug('Going to iterate through the sheets present in the work book')
                        for s in wb.sheets():
                            if s.name == sheetname:
                                log.info('Input sheet name matched with the actual sheet name')
                                # logger.print_on_console('Input sheet name matched with the actual sheet name')
                                # logger.print_on_console('Expected: ',s.name)
                                log.info('Expected:')
                                log.info(s.name)
                                # logger.print_on_console('Actual: ',sheetname)
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
                                    # logger.print_on_console(sheetname + ' contains unique column names, continue..')
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
                    columnNamesList = next(filereader)
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
            elif filepath.split("/")[0] == "avoassure":
                """datatable check goes here"""
                key = filepath.split("/")[1]
                dt = None
                for item in datatables:
                    if item.get(key) != None:
                        dt = item.get(key)
                        break
                if dt:
                    log.info('Datatable %s exists'%key)
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = TEST_RESULT_PASS
                else:
                    log.info('Datatable %s does not exist'%key)
                    logger.print_on_console('Datatable %s does not exist'%key)

            return status
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console("Error occured in getparam")

    def readcsvfile(self,fileinfo):
        """
        def : readcsvfile
        purpose : To read the content of the csv file and store it in dictionary
        param input : input contains File name, Sheet name(Mandatory) and filters (optional)
        return : Returns dictionary
        """
        try:
            print(len(fileinfo))
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
                        logger.print_on_console('Data Param end row: ',endRow)
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
                        colcount = colcount + len(firstrowelements)
                    if rowcount >= 1:
                        testdataexist = True
                    rowcount = rowcount + 1
                logger.print_on_console ('Rowcount : ',rowcount)
                logger.print_on_console( 'Colcount :',colcount)
                if testdataexist == True:
                    for columnindex in range(colcount)  :
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
                                        for col in reader.fieldnames:
                                            myDict[col] = []
                                        for row in reader:
                                            for col in reader.fieldnames:
                                                myDict[col].append(row[col])
                                log.debug('Reading data completed')
            log.info('Returning the output dictionary')
            return myDict
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console("Error while reading CSV file")

    def xmlTreeReader(self,xroot,sdata):
        """
        Reading XML element Tree Recursively

        """
        if len(xroot.getchildren())==0:
            tagname= re.sub('\{.*\}','',xroot.tag)
            if tagname in sdata:
                sdata[tagname].append(xroot.text)
            else:
                sdata[tagname]=[]
                sdata[tagname].append(xroot.text)
            return sdata
        for child in xroot:
            self.xmlTreeReader(child,sdata)
        return sdata

    def readxmlfile(self,fileinfo):
        """
        def : readxmlfile
        purpose : To read the content of the xml file and store it in dictionary
        param input : input contains File name, Sheet name(Mandatory) and filters (optional)
        return : Returns dictionary
        """
        try:
            sdata = dict()
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
                        logger.print_on_console('Data Param end row: ',endRow)
                    else:
                        filter = fileinfo[1]
                        log.info('Data Param  row: ')
                        log.info(filter)
                        logger.print_on_console('Data Param  row: ',filter)
                xroot = xtree.getroot()
                log.debug('Reading data started')
                sdata = self.xmlTreeReader(xroot,sdata)
                log.debug('Reading data completed')
                log.info('Returning the output dictionary')
                return sdata
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console("Error while reading xml data")


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
                                if isinstance(colname,float):
                                    if colname % 1 == 0.0:
                                        colname = int(colname)
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
            log.error(e,exc_info=True)
            logger.print_on_console("Error while reading excel data")

    def readDatatable(self,fileinfo,datatables):
        """
        def : readDatatable
        purpose : To read the content of the datatable(format: [{'col1':'row1'},{'col1':'row2'}])
            and store it in dictionary
        param input : input contains Datatable name and filters (optional)
        return : Returns dictionary (format: {'col1':['row1','row2']})
        """
        try:
            filepath = fileinfo[0]
            #fetch current datatable from list of datatable
            currentdt = filepath.split("/")[1]
            for item in datatables:
                if item.get(currentdt) != None:
                    datatable = item.get(currentdt)
                    break
            #format datatable into dictionary
            sdata = dict.fromkeys(datatable[0].keys())
            for col in sdata:
                sdata[col] = []
                for dt in datatable:
                    sdata[col].append(dt[col])
            return sdata
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console("Error while reading datatable")


    def getexternaldatalist(self,input,datatables):
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
            getparamres = self.getparam(input,datatables)
            log.info( 'Get Param Result :'+ str(getparamres) )
            logger.print_on_console( 'Get Param Result :',getparamres )
            if getparamres == TEST_RESULT_PASS:
                externalDataList=''
                log.debug( "File is valid, try to fetch the data...")
                #need to check dynamic variable for filepath
                filename, file_extension = os.path.splitext(filepath)
                if file_extension[1:].lower() == FILE_TYPE_XLS or file_extension[1:].lower() == FILE_TYPE_XLSX:
                    log.debug( "Type is Excel")
                    """Excel .xls file check goes here"""
                    externalDataList = self.readxlsandxlsxfile(fileinfo)
                elif file_extension[1:].lower() == FILE_TYPE_CSV:
                    log.debug( "Type is .csv")
                    """CSV .csv file check goes here"""
                    externalDataList = self.readcsvfile(fileinfo)
                elif file_extension[1:].lower() == FILE_TYPE_XML:
                    log.debug( "Type is .xml")
                    """XML .xml file check goes here"""
                    externalDataList = self.readxmlfile(fileinfo)
                elif filepath.split("/")[0] == "avoassure":
                    log.debug( "Type is datatable")
                    """Datatable check goes here"""
                    externalDataList = self.readDatatable(fileinfo,datatables)
                return externalDataList
            else:
                log.error( 'Invalid file! Please provide valid file name and/or sheet name')
                logger.print_on_console(  'Invalid file! Please provide valid file name and/or sheet name')
                return getparamres
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console('Error while reading file')

    def invokegetparam(self,input,datatables):
        """
        def : invokegetparam
        purpose : make calls to getexternaldatalist
        param input : input contains File name, Sheet name(Mandatory) and filters (optional)
        return : Returns dictionary
        """
        data =  self.getexternaldatalist(input,datatables)

        return data

    def retrievestaticvariable(self,data,paramindex,row):
        """
        def : retrievestaticvariable
        purpose : To retrieve actual value of the static variable
        param input : data - Dictionary, variable - static variable , row i
        return : Returns actual value of the static variable
        """

        if data is None:
            return None
        teststepproperty =handler.local_handler.tspList[paramindex]
        inputval = teststepproperty.inputval
        inputlistwithval = (list)( inputval)
        global statCnt
        try:
            for i in range(0,len(inputval)):
                inputvalstring = inputval[i]
                resultinput = inputvalstring
                inputresult = ''
                variable = ''
                temp = ''
                columnname = ''
                arr=[]
                if teststepproperty.name.lower() in [IF,ELSE_IF]:
                    static_var_list=re.findall("\|(.*?)\|", inputvalstring)
                    statDict={}
                    statDict[STATIC_NONE]=None
                    for var in static_var_list:
                        inputresult=self.get_static_value(data,row,var)
                        var = PIPE + var + PIPE
                        if inputresult is None:
                            temp = STATIC_NONE
                        elif inputresult == IGNORE_THIS_STEP:
                            temp = IGNORE_THIS_STEP
                        else:
                            if isinstance(inputresult,float):
                                if inputresult%1 == 0.0:
                                    inputresult= int(inputresult)
                            temp=STATIC_DV_NAME[:9]+str(statCnt)+STATIC_DV_NAME[9:]
                            statCnt+=1
                            dynamic_variable_handler.local_dynamic.dynamic_variable_map[temp]=inputresult
                        resultinput = resultinput.replace(var,temp)
                    inputlistwithval.insert(i,resultinput)
                else:
                    keywordList=[EVALUATE,DATE_COMPARE]
                    if teststepproperty.name.lower() in keywordList :
                        static_var_list=re.findall("\|(.*?)\|", inputvalstring)
                        for var in static_var_list:
                            arr.append(PIPE+var+PIPE)
                    else:
                        arr = inputvalstring.split(';')
                    for item in arr:
                        if self.checkforstaticvariable(item.strip()):
                            p=0
                            pLen=len(item.strip())-1
                            while p < pLen:
                                temp = item[p+1:len(item)]
                                columnname = temp[0:temp.find(PIPE)]
                                variable = PIPE + columnname + PIPE
                                p = p + len(variable)
                                inputresult=self.get_static_value(data,row,columnname)
                                if inputresult is None:
                                    temp=STATIC_NONE
                                elif inputresult == IGNORE_THIS_STEP:
                                    temp=IGNORE_THIS_STEP
                                else:
                                    if isinstance(inputresult,float):
                                        if inputresult%1 == 0.0:
                                            inputresult = int(inputresult)
                                    temp=STATIC_DV_NAME[:9]+str(statCnt)+STATIC_DV_NAME[9:]
                                    statCnt+=1
                                    dynamic_variable_handler.local_dynamic.dynamic_variable_map[temp]=inputresult
                                resultinput = resultinput.replace(variable,temp)
                                inputlistwithval.insert(i,resultinput)
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console("Error while retrieving the value of static variable")
        return inputlistwithval

    def checkforstaticvariable(self,statvariable):
        """
        def : checkforstaticvariable
        purpose : To check variable is static or not
        param input :  statvariable - static variable
        return : Returns True if the variable is staticvariable else False
        """
        return (statvariable.startswith('|') and statvariable.endswith('|'))

    #To get the value of given static variable
    def get_static_value(self,data,i,var):
        #returns the value of the static variable if it exists otherwise returns None
        value=None
        if var in data:
            if i>=0 and i<len(data[var]):
                value=data[var][i]
                if value=='':
                    value=None
            #else:
            #    emsg='No data found at Row: '+i
            #    value=ValueError(emsg)
        else:
            log.error('Column name '+var+' not found')
            logger.print_on_console('Column name '+var+' not found')
        return value

    def add_report_end_iteration(self,reporting_obj,step_description,iteration_count,loop_count):
        #Reporting part
        self.step_description=step_description
        self.parent_id=reporting_obj.get_pid()
        reporting_obj.pop_pid()
        #(iteration_count<loop_count-1) condition i smade to avoid adding of  the Iteration completed message of last iteration step twice t
        # the report
        #since it is added in the 'methodInvocation' in controller
        if self.name.lower() != ENDLOOP and (iteration_count<loop_count):
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

    def performdataparam(self,input,con,reporting_obj,execution_env,datatables):
        try:

            endlopnum = list(self.info_dict[0].keys())[0]
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



            if self.getparam(input,datatables) == TEST_RESULT_PASS :
                step_description='Parameterization method executed and status is Pass'
                fileinfo = input
                filepath = fileinfo[0]
                data = self.invokegetparam(input,datatables)
                handler.local_handler.paramData=data
                startRow = None
                endRow =None
                filter = None
                k = 1
                filename, file_extension = os.path.splitext(filepath)
                if file_extension[1:].lower() in [FILE_TYPE_XLS,FILE_TYPE_XLSX]:# or file_extension[1:].lower() == FILE_TYPE_XLSX
                    if len(fileinfo) == 2 :
                        if fileinfo[1].find(HYPHEN) != -1:
                            filters = fileinfo[1].split(HYPHEN)
                            start = filters[0]
                            #start - check for dynamic variable
                            end = filters[1]
                            #end - check for dynamic variable
                            startRow = int(start)
                            endRow = int(end)
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
                            startRow = int(start)
                            endRow = int(end)
                            log.info('Data Param start row: ')
                            log.info(startRow)
                            logger.print_on_console('Data Param start row: ',startRow)
                            log.info('Data Param end row: ')
                            log.info(endRow)
                            logger.print_on_console('Data Param end row: ',endRow)
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
                            startRow = int(start)
                            endRow = int(end)
                            log.info('Data Param start row: ')
                            log.info(startRow)
                            logger.print_on_console('Data Param start row: ',startRow)
                            log.info('Data Param end row: ')
                            log.info(endRow)
                            logger.print_on_console('Data Param end row: ',endRow)
                        elif fileinfo[1] != '':
                            filter1 = fileinfo[1]
                            filter = int(filter1)
                            log.info('Data Param  row: ')
                            log.info(filter)
                            logger.print_on_console('Data Param  row: ',filter)
                    elif len(fileinfo) == 3 :
                        if fileinfo[2].find(HYPHEN) != -1:
                            filters = fileinfo[2].split(HYPHEN)
                            start = filters[0]
                            #start - check for dynamic variable
                            end = filters[1]
                            #end - check for dynamic variable
                            startRow = int(start)
                            endRow = int(end)
                            log.info('Data Param start row: ')
                            log.info(startRow)
                            logger.print_on_console('Data Param start row: ',startRow)
                            log.info('Data Param end row: ')
                            log.info(endRow)
                            logger.print_on_console('Data Param end row: ',endRow)
                        elif fileinfo[2] != '':
                            filter1 = fileinfo[2]
                            filter = int(filter1)
                            log.info('Data Param  row: ')
                            log.info(filter)
                            logger.print_on_console('Data Param  row: ',filter)

                if startRow !=None and endRow != None:
                    if startRow > endRow or startRow <= 1 or endRow <=1:
                        log.info( 'Invalid filter, Provide valid Start row and End row value')
                        logger.print_on_console( '***Invalid filter, Provide valid start row and end row value***')
                        return_value =TERMINATE
                    else:
                        numRows = 0
                        if(len(data.values()) == 0 or len(list(data.values())[0]) == 0):
                            log.info('Empty Data. Please provide valid data')
                            logger.print_on_console( '***Empty Data. Please provide valid data***')
                            paramindex = TERMINATE
                        elif(len(data.values()) > 0):
                            numRows = len(list(data.values())[0])+1
                        endLimit = min(endRow, numRows)
                        if endLimit < endRow:
                            log.info("Data Param end row value is greater than the number of rows")
                            logger.print_on_console("Data Param end row value is greater than the number of rows")
                        log.info( '***Data Parameterization started***')
                        logger.print_on_console( '***Data Parameterization started***')
                        #Reporting part
                        reporting_obj.name=GETPARAM
                        self.add_report_step_getparam(reporting_obj,step_description)
                        if len(input)>1:
                            step_description='Read file: '+str(input[0])+', Sheet name: '+str(input[1])
                        self.add_report_step_getparam(reporting_obj,step_description)
                        step_description='Start Loop'
                        self.add_report_step_getparam(reporting_obj,step_description)
                        #Reporting part ends
                        for i in range(startRow-1,endLimit):
                            if self.name.lower()==GETPARAM:
                                inputval = self.inputval[0]
                                paramindex = self.index+2
                                if handler.local_handler.tspList[self.index+1].name.lower()==STARTLOOP:
                                    handler.local_handler.tspList[self.index+1].executed=True
                                if (inputval != None):
                                    log.info(  '***Data Param: Iteration '+ str(k) +  ' started***')
                                    logger.print_on_console(  '***Data Param: Iteration ',k, ' started***')
                                    step_description='Dataparam: Iteration '+str(k)+' started'
                                    reporting_obj.name='Iteration '+str(k)
                                    self.add_report_step_getparam(reporting_obj,step_description)
                                    iterations = len(list(data.values())[0])
                                    while (paramindex < endlopnum):
                                        input = self.retrievestaticvariable(data,paramindex,i-1)
                                        paramindex =con.methodinvocation(paramindex,execution_env,datatables,input)
                                        if paramindex in [TERMINATE,BREAK_POINT,STOP]:
                                            return paramindex
                                    log.info( '***Data Param: Iteration ' + str(k) + ' completed***\n')
                                    logger.print_on_console( '***Data Param: Iteration ',k, ' completed***\n')
                                    #Reporting part
                                    step_description='Dataparam: Iteration '+str(k)+' executed'
                                    reporting_obj.name='Iteration '+str(k)
                                    self.add_report_end_iteration(reporting_obj,step_description,k,endRow+1)
                                    #Reporting part ends
                                    k = k + 1
                        log.info( '***Data Parameterization completed***')
                        logger.print_on_console( '***Data Parameterization completed***')
                        return_value=paramindex

                elif filter != None:
                    if filter<=1:
                        log.info( 'Invalid filter, Provide valid filter value')
                        logger.print_on_console( '***Invalid filter, Provide valid filter value***')
                        return_value =TERMINATE
                    else:
                        log.info( '***Data Parameterization started***')
                        logger.print_on_console('***Data Parameterization started***')
                        #Reporting part
                        reporting_obj.name=GETPARAM
                        self.add_report_step_getparam(reporting_obj,step_description)
                        if len(input)>1:
                            step_description='Read file: '+str(input[0])+str(input[1])+' :Dataparam'
                        else:
                            step_description='Read file: '+str(input[0])+' :Dataparam'
                        self.add_report_step_getparam(reporting_obj,step_description)
                        step_description='Start Loop'
                        self.add_report_step_getparam(reporting_obj,step_description)
                        #Reporting part ends
                        filter = filter - 2
                        if self.name.lower()==GETPARAM:
                            inputval = self.inputval[0]
                            paramindex = self.index+2
                            if handler.local_handler.tspList[self.index+1].name.lower()==STARTLOOP:
                                handler.local_handler.tspList[self.index+1].executed=True
                            if (inputval != None):
                                log.info( '***Data Param: Iteration '+str(k)+ ' started***')
                                logger.print_on_console( '***Data Param: Iteration ',k, ' started***')
                                #Reporting part
                                step_description='Dataparam: Iteration '+str(k)+' started'
                                reporting_obj.name='Iteration '+str(k)
                                self.add_report_step_getparam(reporting_obj,step_description)
                                #Reporting part ends
                                iterations = len(list(data.values())[0])
                                while (paramindex < endlopnum):
                                    input = self.retrievestaticvariable(data,paramindex,filter)
                                    paramindex =con.methodinvocation(paramindex,execution_env,datatables,input)
                                    if paramindex in [TERMINATE,BREAK_POINT,STOP]:
                                        return paramindex
                                log.info( '***Data Param: Iteration '+str(k)+ ' completed***\n')
                                logger.print_on_console('***Data Param: Iteration ',k, ' completed***\n')
                                #Reporting part
                                step_description='Dataparam: Iteration '+str(k)+' executed'
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
                    if len(input)>1:
                        step_description='Read file: '+str(input[0])+str(input[1])+' :Dataparam'
                    else:
                        step_description='Read file: '+str(input[0])+' :Dataparam'
                    self.add_report_step_getparam(reporting_obj,step_description)
                    step_description='Start Loop'
                    self.add_report_step_getparam(reporting_obj,step_description)
                    #Reporting part ends
                    count=len(list(data.values())[0])
                    for i in range(count):
                        if self.name.lower()==GETPARAM:
                            inputval = self.inputval[0]
                            paramindex = self.index+2
                            if handler.local_handler.tspList[self.index+1].name.lower()==STARTLOOP:
                                handler.local_handler.tspList[self.index+1].executed=True
                            if (inputval != None):
                                log.info( '***Data Param: Iteration '+str(k)+ ' started***')
                                logger.print_on_console( '***Data Param: Iteration ',k, ' started***')
                                #Reporting part
                                reporting_obj.name='Iteration '+str(k)
                                step_description='Dataparam: Iteration '+str(k)+' started'
                                self.add_report_step_getparam(reporting_obj,step_description)
                                #Reporting part ends
                                iterations = len(list(data.values())[0])
                                logger.print_on_console ('Iterations : ',iterations)
                                while (paramindex < endlopnum):
                                    input = self.retrievestaticvariable(data,paramindex,i)
                                    paramindex =con.methodinvocation(paramindex,execution_env,datatables,input)
                                    if paramindex in [TERMINATE,BREAK_POINT,STOP]:
                                        return paramindex
                                log.info( '***Data Param: Iteration '+str(k)+ ' completed***\n')
                                logger.print_on_console('***Data Param: Iteration ',k, ' completed***\n')
                                #Reporting part
                                step_description='Dataparam: Iteration '+str(k)+' executed'
                                reporting_obj.name='Iteration '+str(k)
                                self.add_report_end_iteration(reporting_obj,step_description,k,count)
                                #Reporting part ends
                                k = k + 1

                    log.info( '***Data Parameterization completed***')
                    logger.print_on_console( '***Data Parameterization completed***')
                    return_value=paramindex
            else:
                log.error( 'Data parameterization failed : Wrong datatable name/ file name/ Sheet name given')
                log.error( 'Wrong datatable name/ file name/ Sheet name given, Please check and provide valid one')
                logger.print_on_console( 'Data parameterization failed : Wrong datatable name/ file name/ Sheet name given')
                logger.print_on_console('Wrong datatable name/ file name/ Sheet name given, Please check and provide valid one')
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
            log.error(e,exc_info=True)
        return return_value
