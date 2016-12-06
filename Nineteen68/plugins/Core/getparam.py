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

import Exceptions

import handler

from teststepproperty import TestStepProperty

import controller

"""The xml.etree.ElementTree module implements a simple and efficient API for parsing and creating XML data."""
import xml.etree.ElementTree as ET
import constants
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

    def print_step(self):
        logger.log(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name+' '+str(self.info_dict))

    def getparam(self,input):
        """
        def : getParam
        purpose : to check input file for the Data Parameterization is valid or not
        param input : input contains File name, Sheet name(Mandatory) and filters (optional)
        return : Returns Pass if the file is Valid  else Fail
        """
        status = constants.TEST_RESULT_FAIL
        try:
            """Logic to find the input file is valid or not"""
            fileinfo = input.split(';')
            filepath = fileinfo[0]
            #need to check dynamic variable for filepath
            filename, file_extension = os.path.splitext(filepath)
            if file_extension[1:].lower() == constants.FILE_TYPE_XLS or file_extension[1:].lower() == constants.FILE_TYPE_XLSX:
                """Excel file check goes here"""
                columnNamesList = []
                columnNamesSet = []
                if len(fileinfo) > 1:
                    filepath = fileinfo[0]
                    sheetname = fileinfo[1]
                    if os.access(filepath, os.R_OK):
                        wb = open_workbook(filepath)
                        for s in wb.sheets():
                            if s.name == sheetname:
                                for col in range(s.ncols):
                                    data = s.cell(0,col).value
                                    if data != '':
                                        columnNamesList.append(data)
                                columnNamesSet = set(columnNamesList)
                                if len(columnNamesList) == len(columnNamesSet):
                                    print "File contains unique column names"
                                    status = constants.TEST_RESULT_PASS
                                else:
                                    print "File contains duplicate column names"

            elif file_extension[1:].lower() == constants.FILE_TYPE_CSV:
                """CSV .csv file check goes here"""
                print 'File path :', filepath
                if os.access(filepath, os.R_OK):
                    print "File is readable"
                    filereader = csv.reader(open(filepath))
                    columnNamesList = filereader.next()
                    columnNamesSet = set(columnNamesList)
                    if len(columnNamesList) == len(columnNamesSet):
                        print "File contains unique column names"
                        status = constants.TEST_RESULT_PASS
                    else:
                        print "File contains duplicate column names"
                else:
                    print "File is not readable"
            elif file_extension[1:].lower() == constants.FILE_TYPE_XML:
                """XML .xml file check goes here"""
                if os.access(filepath, os.R_OK):
                    columnNamesList = []
                    print "File is readable"
                    xtree = ET.parse(filepath)
                    xroot = xtree.getroot()
                    for topchild in xroot:
                        topch =  topchild
                        for child in topch:
                            columnNamesList.append(child.tag)
                        break
                    columnNamesSet = set(columnNamesList)
                    if len(columnNamesList) == len(columnNamesSet):
                        print "File contains unique column names"
                        status = constants.TEST_RESULT_PASS
                    else:
                        print "File contains duplicate column names"
                else:
                    print "File is not readable"

            return status
        except Exception as e:
            print 'Exception occured'

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
                    if fileinfo[1].find(constants.HYPHEN) != -1:
                        filters = fileinfo[1].split(constants.HYPHEN)
                        start = filters[0]
                        #start - check for dynamic variable
                        end = filters[1]
                        #end - check for dynamic variable
                        startRow = int(start);
                        endRow = int(end);
                    else:
                        filter = fileinfo[1]
                        #filter - check for dynamic variable
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
                print 'Rowcount : ',rowcount
                print 'Colcount :',colcount
                if testdataexist == True:
                    for columnindex in range(colcount - 1)  :
                        rowcount1 = 1
                        for row in allRows:
                            if rowcount1 == 0:
                                pass
                            else:
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
            return myDict
        except Exception as e:
            print 'Exception occured :',e


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
                    if fileinfo[1].find(constants.HYPHEN) != -1:
                        filters = fileinfo[1].split(constants.HYPHEN)
                        start = filters[0]
                        #start - check for dynamic variable
                        end = filters[1]
                        #end - check for dynamic variable
                        startRow = int(start);
                        endRow = int(end);
                    else:
                        filter = fileinfo[1]
                xroot = xtree.getroot()
                for topchild in xroot:
                    topch =  topchild
                    for child in topch:
                        sdata[child.tag] = []
    ##                        break
                for topchild in xroot:
                    topch =  topchild
                    for child in topch:
                        if child.text == None:
                            sdata[child.tag].append('')
                        else:
                            sdata[child.tag].append(child.text)

                return sdata
        except Exception as e:
            print 'Exception occured :',e


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
            print 'Exception occured :',e




    def getexternaldatalist(self,input):
        """
        def : getexternaldatalist
        purpose : make calls to perticular file reading methods based on the file type
        param input : input contains File name, Sheet name(Mandatory) and filters (optional)
        return : Returns dictionary
        """

        try:
            fileinfo = input.split(';')
            #check for dynamic variables for fileinfo
            filepath = fileinfo[0]
            getparamres = self.getparam(input)
            print 'Filepath : ',filepath
            print 'Get Param Result :',getparamres
            if getparamres == constants.TEST_RESULT_PASS:
                print "File is valid, try to fetch the data..."
                #need to check dynamic variable for filepath
                filename, file_extension = os.path.splitext(filepath)
                print 'File name : ',filepath
                if file_extension[1:].lower() == constants.FILE_TYPE_XLS or file_extension[1:].lower() == constants.FILE_TYPE_XLSX:
                    print "Type is Excel"
                    """Excel .xls file check goes here"""
                    externalDataList = self.readxlsandxlsxfile(fileinfo);
                elif file_extension[1:].lower() == constants.FILE_TYPE_CSV:
                    print "Type is .csv"
                    """CSV .csv file check goes here"""
                    externalDataList = self.readcsvfile(fileinfo);
                    status = constants.TEST_RESULT_PASS
                elif file_extension[1:].lower() == constants.FILE_TYPE_XML:
                    """XML .xml file check goes here"""
                    externalDataList = self.readxmlfile(fileinfo);
                    status = constants.TEST_RESULT_PASS
                return externalDataList
            else:
                print 'Invalid file! Please provide valid file name and/or sheet name'
                return getparamres
        except Exception as e:
            print 'Exception occured :',e

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
                arr = inputvalstring.split(';')
                for item in arr:
                    if self.checkforstaticvariable(item.strip()):
                        p = 0
                        while p < len(item.strip()) - 1:
                            if(item.find(constants.PIPE) != -1):
                                temp = item[p+1 : len(item)]
                                columnname = temp[0:temp.find(constants.PIPE)]
                                variable = constants.PIPE + columnname + constants.PIPE
                                p = p + len(variable)
                                inputresult = data[columnname][row]
                                resultinput = resultinput.replace(variable,inputresult)
                                inputlistwithval.insert(i,resultinput)
            return inputlistwithval

    def checkforstaticvariable(self, statvariable):
        """
        def : checkforstaticvariable
        purpose : To check variable is static or not
        param input :  statvariable - static variable
        return : Returns True if the variable is staticvariable else False
        """
        return (statvariable.startswith('|') and statvariable.endswith('|'))

    def performdataparam(self):
        try:
            input = self.inputval[0]
            con= controller.Controller()
            endlopnum = self.info_dict[0].keys()[0]
            self.executed=True

            if self.name.lower() == constants.ENDLOOP:
                return self.index + 1

            if self.name.lower() == constants.STARTLOOP:
                return self.index + 1



            if self.getparam(input) == constants.TEST_RESULT_PASS :
                fileinfo = input.split(';')
                filepath = fileinfo[0]
                data = self.invokegetparam(input)
                startRow = None
                endRow =None
                filter = None
                k = 1
                filename, file_extension = os.path.splitext(filepath)
                if file_extension[1:].lower() == constants.FILE_TYPE_XLS or file_extension[1:].lower() == constants.FILE_TYPE_XLSX:
                    if len(fileinfo) == 2 :
                        if fileinfo[1].find(constants.HYPHEN) != -1:
                            filters = fileinfo[1].split(constants.HYPHEN)
                            start = filters[0]
                            #start - check for dynamic variable
                            end = filters[1]
                            #end - check for dynamic variable
                            startRow = int(start);
                            endRow = int(end);
                    elif len(fileinfo) == 3 :
                        if fileinfo[2].find(constants.HYPHEN) != -1:
                            filters = fileinfo[2].split(constants.HYPHEN)
                            start = filters[0]
                            #start - check for dynamic variable
                            end = filters[1]
                            #end - check for dynamic variable
                            startRow = int(start);
                            endRow = int(end);
                        else:
                            filter1 = fileinfo[2]
                            filter = int(filter1)
                else:
                    if len(fileinfo) == 2 :
                        if fileinfo[1].find(constants.HYPHEN) != -1:
                            filters = fileinfo[1].split(constants.HYPHEN)
                            start = filters[0]
                            #start - check for dynamic variable
                            end = filters[1]
                            #end - check for dynamic variable
                            startRow = int(start);
                            endRow = int(end);
                        else:
                            filter1 = fileinfo[1]
                            filter = int(filter1)

                if startRow !=None and endRow != None:
                    print '***Data Parameterization started***'
                    for i in range(startRow,endRow+1):
                        if self.name.lower()==constants.GETPARAM:
                            inputval = self.inputval[0]
                            paramindex = self.index+1;
                            if (inputval != None):
                                j = 0
                                print '***Data Param: Iteration ',k, ' started***'
                                iterations = len(data.values()[0])
                                while (paramindex <= endlopnum):
                                    input = self.retrievestaticvariable(data,paramindex,i-1)
                                    paramindex =con.methodinvocation(paramindex,input)
                                    if paramindex in [constants.TERMINATE,constants.BREAK_POINT]:
                                        return paramindex
                                print '***Data Param: Iteration ',k, ' completed***\n\n'
                                k = k + 1
                    return paramindex
                    print '***Data Parameterization completed***'
                elif filter != None:
                    print '***Data Parameterization started***'
                    if self.name.lower()==constants.GETPARAM:
                        inputval = self.inputval[0]
                        paramindex = self.index+1;
                        if (inputval != None):
                            print '***Data Param: Iteration ',k, ' started***'
                            iterations = len(data.values()[0])
                            while (paramindex <= endlopnum):
                                    input = self.retrievestaticvariable(data,paramindex,filter-1)
                                    paramindex =con.methodinvocation(paramindex,input)
                                    if paramindex in [constants.TERMINATE,constants.BREAK_POINT]:
                                        return paramindex
                            print '***Data Param: Iteration ',k, ' completed***\n\n'
                            k = k + 1
                    print '***Data Parameterization completed***'
                    return paramindex

                else:
                    print '***Data Parameterization started***'
                    for i in range(len(data.values()[0])):
                        if self.name.lower()==constants.GETPARAM:
                            inputval = self.inputval[0]
                            paramindex = self.index+1;
                            if (inputval != None):
                                print '***Data Param: Iteration ',k, ' started***'
                                iterations = len(data.values()[0])
                                print 'Iterations : ',iterations
                                while (paramindex < endlopnum):
                                    input = self.retrievestaticvariable(data,paramindex,i)
                                    paramindex =con.methodinvocation(paramindex,input)
                                    if paramindex in [constants.TERMINATE,constants.BREAK_POINT]:
                                        return paramindex
                                print '***Data Param: Iteration ',k, ' completed***\n\n'
                                k = k + 1

                    print '***Data Parameterization completed***'
                    return paramindex
            else:
                print 'Data parameterization failed'
                print 'Wrong file name/ Sheet name given, Please check and provide valid one'
                return endlopnum + 1
        except Exception as e:
            print 'Data parameterization failed'
            print 'Wrong filters given, please check and provide correct one'
            Exceptions.error(e)
            return endlopnum + 1






