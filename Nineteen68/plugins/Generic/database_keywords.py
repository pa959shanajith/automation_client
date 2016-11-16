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
from encryption_utility import AESCipher

class DatabaseOperation():
    def runQuery(self, ip , port , userName , password, dbName, query, dbtype):
        """
        def : runQuery
        purpose : Executes the query
        param : database type, IP, port number , database name, username , password , query
        return : boolean
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        try:
            cnxn = self.connection(dbtype, ip , port , dbName, userName , password)
            cursor = cnxn.cursor()
            statement = ['create','update','insert','CREATE','UPDATE','INSERT']
            if any(x in query for x in statement ):
                cursor.execute(query)
                cnxn.commit()
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
            else:
                cursor.execute(query)
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
##                rows = cursor.fetchall()
##                for row in rows:
##                    print row

        except Exception as e:
            Exceptions.error(e)
            return False
        finally:
            cursor.close()
            cnxn.close()
        return status,result

    def secureRunQuery(self, ip , port , userName , password, dbName, query, dbtype):
        """
        def : secureRunQuery
        purpose : Executes the query
        param : database type, IP, port number , database name, username , password , query
        return : boolean
        """
        try:
            encryption_obj = AESCipher()
            decrypted_password = encryption_obj.decrypt(password)
            status,result=self.runQuery(ip,port,userName,decrypted_password,dbName,query,dbtype)
            print status,result
        except Exceptions as e:
            Exceptions.error(e)
        return status,result


    def getData(self, ip , port , userName , password, dbName, query, dbtype):
        """
        def : getData
        purpose : Executes the query and gets the data
        param : database type, IP, port number , database name, username , password , query
        return : data
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        try:
            cnxn = self.connection(dbtype, ip , port , dbName, userName , password)
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                logger.log(row)
            status=generic_constants.TEST_RESULT_PASS
            result=generic_constants.TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
            return False
        finally:
            cursor.close()
            cnxn.close()
            return status,result

    def secureGetData(self, ip , port , userName , password, dbName, query, dbtype):
        """
        def : secureGetData
        purpose : Executes the query and gets the data
        param : database type, IP, port number , database name, username , password , query
        return : data
        """
        try:
            encryption_obj = AESCipher()
            decrypted_password = encryption_obj.decrypt(password)
            status,result=self.getData(ip,port,userName,decrypted_password,dbName,query,dbtype)
        except Exceptions as e:
            Exceptions.error(e)
        return status,result

    def verifyData(self, ip , port , userName , password, dbName, query, dbtype,inp_file,inp_sheet):
        """
        def : verifyData
        purpose : Executes the query and compares the data with data in files
        param : database type, IP, port number , database name, username , password , query , Filename , sheetname
        return : bool
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        try:
            file_path=self.create_file()
            cnxn = self.connection(dbtype, ip , port , dbName, userName , password)
            cursor = cnxn.cursor()
            cursor.execute(query)
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
                    if output == "True":
                        status=generic_constants.TEST_RESULT_PASS
                        result=generic_constants.TEST_RESULT_TRUE
                    else:
                        status=generic_constants.TEST_RESULT_FAIL
                        result=generic_constants.TEST_RESULT_FALSE

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
        return status,result

    def secureVerifyData(self, ip , port , userName , password, dbName, query, dbtype,inp_file,inp_sheet):
        """
        def : secureVerifyData
        purpose : Executes the query and compares the data with data in files
        param : database type, IP, port number , database name, username , password , query , Filename , sheetname
        return : bool
        """
        try:
            encryption_obj = AESCipher()
            decrypted_password = encryption_obj.decrypt(password)
            status,result=self.verifyData(ip,port,userName,decrypted_password,dbName, query, dbtype,inp_file,inp_sheet)
        except Exceptions as e:
            Exceptions.error(e)
        return status,result

    def exportData(self, ip , port , userName , password, dbName, query, dbtype, *args):
        """
        def : exportData
        purpose : Executes the query and exports the data to excel or csv file
        param : database type, IP, port number , database name, username , password , query , Filename , sheetname
        return : bool
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        try:
            cnxn = self.connection(dbtype, ip , port , dbName, userName , password)
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            ##logic for output col reading
            out_tuple = args
            fields = out_tuple[0]
            inp_file = fields[0]
            verify = os.path.isfile(inp_file)
            if (verify == True):
                ext = self.get_ext(inp_file)
                if (ext == '.xls'):
                    inp_sheet = fields[1]
                    obj=excel_operations.ExcelFile()
                    obj.set_excel_path(inp_file,inp_sheet)
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
                    status=generic_constants.TEST_RESULT_PASS
                    result=generic_constants.TEST_RESULT_TRUE
                elif(ext == '.csv'):
                    path = inp_file
                    with open(path,'w') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(columns)
                        for row in rows:
                            writer.writerow(row)
                    status=generic_constants.TEST_RESULT_PASS
                    result=generic_constants.TEST_RESULT_TRUE
                else:
                    logger.log(generic_constants.INVALID_INPUT)
            else:
                logger.log(generic_constants.FILE_NOT_EXISTS)
        except Exception as e:
            Exceptions.error(e)
            return False
        finally:
            cursor.close()
            cnxn.close()
        return status,result

    def secureExportData(self, ip , port , userName , password, dbName, query, dbtype,*args):
        """
        def : secureExportData
        purpose : Executes the query and exports the data to excel or csv file
        param : database type, IP, port number , database name, username , password , query , Filename , sheetname
        return : bool
        """
        try:
            encryption_obj = AESCipher()
            decrypted_password = encryption_obj.decrypt(password)
            out_col = args
            status,result=self.exportData(ip,port,userName,decrypted_password,dbName, query, dbtype, out_col)
        except Exceptions as e:
            Exceptions.error(e)
        return status,result

    def connection(self,dbtype, ip , port , dbName, userName , password):
        """
        def : connection
        purpose : connecting to database based on database type given
        param : database type, IP, port number , database name, username , password , query
        return : connection object
        """
        dbNumber = {4:'{SQL Server}',5:'{Microdsoft ODBC for Oracle}',2:'{IBM DB2 ODBC DRIVER}'}
        try:
            dbtype= int(dbtype)
            self.cnxn = pyodbc.connect('driver=%s;SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s' % ( dbNumber[dbtype], ip, port, dbName, userName ,password ) )
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
           path = maindir + '\Nineteen68\plugins\Generic' + generic_constants.DATABASE_FILE
##           path = 'D:\db5.xls'
           wb.save(path)
           return path
        except Exception as e:
            Exceptions.error(e)


##obj = DatabaseOperation()
##obj.runQuery('10.44.10.54','1433','version20_test','version2.0_Test','Version20_TestDB',"select * from Persons",'4')
##obj.secureRunQuery('10.44.10.54','1433','version20_test','451MwSMdBUUKiSlqb85IKvYYAt8ag1cO0JE5cEDdotg=','Version20_TestDB',"select * from Persons",'4')
##obj.getData('10.44.10.54','1433','version20_test','version2.0_Test','Version20_TestDB',"select * from Persons",'4')
##obj.secureGetData('10.44.10.54','1433','version20_test','O0v/vLLjfD+hR22U9lzTifYYAt8ag1cO0JE5cEDdotg=','Version20_TestDB',"select * from Persons",'4')
##obj.exportData('4','10.44.10.54','1433','Version20_TestDB','version20_test','version2.0_Test',"select * from Persons",'D:\db6.xls','Sheet1')
##obj.secureExportData('10.44.10.54','1433','version20_test','O0v/vLLjfD+hR22U9lzTifYYAt8ag1cO0JE5cEDdotg=','Version20_TestDB',"select * from Persons",'4','D:\db6.xls','Sheet1')
##obj.verifyData('4','10.44.10.54','1433','Version20_TestDB','version20_test','version2.0_Test',"select * from Persons",'D:\db5.xls','Sheet1')
##obj.secureVerifyData('10.44.10.54','1433','version20_test','O0v/vLLjfD+hR22U9lzTifYYAt8ag1cO0JE5cEDdotg=','Version20_TestDB',"select * from Persons",'4','D:\db6.xls','Sheet1')