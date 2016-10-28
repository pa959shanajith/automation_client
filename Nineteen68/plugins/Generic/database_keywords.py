#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     20-10-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pyodbc
import Exceptions
import csv
import file_operations
import excel_operations
import xlwt
import generic_constants
import os
import logger

class DatabaseOperation():
    def __init__(self, ip , port , userName , password, dbName, query, dbtype):
        self.dbtype = dbtype
        self.ip = ip
        self.port = port
        self.dbName = dbName
        self.userName = userName
        self.password = password
        self.query = query


    def runQuery(self):
        """
        def : runQuery
        purpose : Executes the query
        param : database type, IP, port number , database name, username , password , query
        return : boolean
        """
        try:
            cnxn = self.connection()
            cursor = cnxn.cursor()
            statement = ['create','update','insert','CREATE','UPDATE','INSERT']
            if any(x in self.query for x in statement ):
                cursor.execute(self.query)
                cnxn.commit()
                return True
            else:
                cursor.execute(self.query)
                return True
##                rows = cursor.fetchall()
##                for row in rows:
##                    print row

        except Exception as e:
            Exceptions.error(e)
            return False
        finally:
            cursor.close()
            cnxn.close()

    def getData(self):
        """
        def : getData
        purpose : Executes the query and gets the data
        param : database type, IP, port number , database name, username , password , query
        return : data
        """
        try:
            cnxn = self.connection()
            cursor = cnxn.cursor()
            cursor.execute(self.query)
            rows = cursor.fetchall()
            for row in rows:
                logger.log(row)
            return True
        except Exception as e:
            Exceptions.error(e)
            return False
        finally:
            cursor.close()
            cnxn.close()

    def verifyData(self,inp_file,inp_sheet):
        """
        def : verifyData
        purpose : Executes the query and compares the data with data in files
        param : database type, IP, port number , database name, username , password , query , Filename , sheetname
        return : bool
        """
        try:
            file_path=self.create_file()
            cnxn = self.connection()
            cursor = cnxn.cursor()
            cursor.execute(self.query)
            rows = cursor.fetchall()
            verify = os.path.isfile(inp_file)
            if (verify == True):
                ext = self.get_ext(inp_file)
                if (ext == '.xls'):
                    obj=excel_operations.ExcelFile()
                    obj.set_excel_path(file_path,generic_constants.DATABASE_SHEET)
                    columns = [column[0] for column in cursor.description]
                    i=1
                    j=1
                    for x in columns:
                        obj.write_cell(i,j,x)
                        j+=1
                    b =0
                    k=2
                    for row in rows:
                        l=1
                        for y in row:
                            obj.write_cell(k,l,y)
                            l+=1
                        k+=1
                    obj = file_operations.FileOperations()
                    output = obj.compare_content(file_path,generic_constants.DATABASE_SHEET,inp_file,inp_sheet)
                    if output == True:
                        return True
                    else:
                        return False

                else:
                    logger.log(generic_constants.INVALID_INPUT)
            else:
                logger.log(generic_constants.FILE_NOT_EXISTS)
        except Exception as e:
            Exceptions.error(e)
        finally:
            os.remove(file_path)
            cursor.close()
            cnxn.close()

    def exportData(self,inp_file,inp_sheet=None):
        """
        def : exportData
        purpose : Executes the query and exports the data to excel or csv file
        param : database type, IP, port number , database name, username , password , query , Filename , sheetname
        return : bool
        """
        try:
            cnxn = self.connection()
            cursor = cnxn.cursor()
            cursor.execute(self.query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            verify = os.path.isfile(inp_file)
            if (verify == True):
                ext = self.get_ext(inp_file)
                if (ext == '.xls'):
                    obj=excel_operations.ExcelFile()
                    obj.set_excel_path(inp_file,inp_sheet)
##                    columns = [column[0] for column in cursor.description]
##                    print columns
                    i=1
                    j=1
                    for x in columns:
                        obj.write_cell(i,j,x)
                        j+=1
                    b =0
                    k=2
                    for row in rows:
                        l=1
                        for y in row:
                            obj.write_cell(k,l,y)
                            l+=1
                        k+=1
                    return True
                elif(ext == '.csv'):
                    path = inp_file
                    with open(path,'w') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(columns)
                        for row in rows:
                            writer.writerow(row)
                    return True
                else:
                    logger.log(generic_constants.INVALID_INPUT)
                    return False
            else:
                logger.log(generic_constants.FILE_NOT_EXISTS)
                return False

        except Exception as e:
            Exceptions.error(e)
            return False
        finally:
            cursor.close()
            cnxn.close()

    def connection(self):
        """
        def : connection
        purpose : connecting to database based on database type given
        param : database type, IP, port number , database name, username , password , query
        return : connection object
        """
        dbNumber = {4:'{SQL Server}',5:'{Microdsoft ODBC for Oracle}',2:'{IBM DB2 ODBC DRIVER}'}
        try:
            self.dbtype= int(self.dbtype)
            self.cnxn = pyodbc.connect('driver=%s;SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s' % ( dbNumber[self.dbtype], self.ip, self.port, self.dbName, self.userName ,self.password ) )
            return self.cnxn
        except Exception as e:
            Exceptions.error(e)

    def get_ext(self,input_path):
        """
        def : __get_ext
        purpose : returns the file type and verifies if it is valid file type
        param : input_path
        return : bool,filetype
        """
        try:
            status=False
            filename,file_ext=os.path.splitext(input_path)
            if file_ext in generic_constants.FILE_TYPES:
                status=True
            else:
                logger.log(generic_constants.INVALID_FILE_FORMAT)
            return file_ext
        except Exception as e:
            Exceptions.error(e)
            return '',status

    def create_file(self):
        """
        def : create_file
        purpose : creates a xls file inside generic folder directory
        param :
        return : path
        """
        try:
           wb = xlwt.Workbook()
           ws = wb.add_sheet(generic_constants.DATABASE_SHEET)
           os.chdir('..')
           maindir = os.getcwd()
           path = maindir + '\Generic' + generic_constants.DATABASE_FILE
##           path = 'D:\db6.xls'
           wb.save(path)
           return path
        except Exception as e:
            Exceptions.error(e)

##obj =DatabaseOperation('10.44.10.54','1433','version20_test','version2.0_Test','Version20_TestDB',"select * from Persons",'4')
##obj.runQuery()
##obj.getData()
##obj.exportData('D:\db5.xls','Sheet1')
##obj.exportData('D:\\test.csv')
##obj.verifyData('D:\db5.xls','Sheet1')
