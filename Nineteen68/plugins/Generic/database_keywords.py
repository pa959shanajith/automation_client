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

##prerequistes - Respective database drivers should be avialable in client machine

import pyodbc
import csv
import file_operations
import excel_operations
import xlwt
import generic_constants
import os
import logger
from encryption_utility import AESCipher
import logging

from constants import *
log = logging.getLogger('database_keywords.py')

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
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            cnxn = self.connection(dbtype, ip , port , dbName, userName , password)
            cursor = cnxn.cursor()
            statement = ['create','update','insert','CREATE','UPDATE','INSERT']
            if any(x in query for x in statement ):
                log.debug('Inside IF condition')
                cursor.execute(query)
                cnxn.commit()
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
            else:
                log.debug('Inside else condition')
                cursor.execute(query)
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE

        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
            err_msg = str(e)
        finally:
            cursor.close()
            cnxn.close()
        return status,result,verb,err_msg

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
            status,result,verb,err_msg=self.runQuery(ip,port,userName,decrypted_password,dbName,query,dbtype)
        except Exceptions as e:
            log.error(e)
            err_msg = str(e)
            logger.print_on_console(err_msg)

        return status,result,verb,err_msg


    def getData(self, ip , port , userName , password, dbName, query, dbtype, *args):
        """
        def : getData
        purpose : Executes the query and gets the data
        param : database type, IP, port number , database name, username , password , query
        return : data
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        value = None
        err_msg=None
        details = []
        cnxn=None
        try:
##            if len(args)>0 :
            cnxn = self.connection(dbtype, ip , port , dbName, userName , password)
##            out_tuple = args
##            out_tuple=''.join(out_tuple)
##            import re
##            data = re.findall(r'\[([^]]*)\]',out_tuple)
##            row = data[0]
##            col = data[1]
##            row = int(row)
##            col = int(col)
##            cursor = cnxn.cursor()
##            cursor.execute(query)
##            rows = cursor.fetchall()
##            value = rows[row][col]
##            log.info('Value obtained :')
##            log.info(value)
##            for row in rows:
##                logger.print_on_console(row)
            if cnxn is not None:
                details.append(ip)
                details.append(port)
                details.append(userName)
                details.append(password)
                details.append(dbName)
                details.append(query)
                details.append(dbtype)
                status=generic_constants.TEST_RESULT_PASS
                result=generic_constants.TEST_RESULT_TRUE
##            else:
##                log.info('Output column missing required value')
##                logger.print_on_console('Output column missing required value')

        except Exception as e:
            log.error(e)
            err_msg = 'Database Login failed'
            logger.print_on_console(err_msg)
        finally:
##            cursor.close()
            if cnxn!=None:
                cnxn.close()
        return status,result,details,err_msg

    def fetchData(self,input_val,*args):
        value = None
        if(len(input_val)== 8):
            try:
                cnxn = self.connection(input_val[6], input_val[0] , input_val[1] , input_val[4], input_val[2] , input_val[3])
                import re
                data = re.findall(r'\[([^]]*)\]',input_val[7])
                row = data[0]
                col = data[1]
                row = int(row)
                col = int(col)
                row_no = row - 1
                col_no = col - 1
                cursor = cnxn.cursor()
                cursor.execute(input_val[5])
                rows = cursor.fetchall()
                value = rows[row_no][col_no]
                log.info('Value obtained :')
                log.info(value)
            except Exception as e:
                log.error(e)
                err_msg = str(e)
                logger.print_on_console(err_msg)
            finally:
                cursor.close()
                cnxn.close()
            return value



    def secureGetData(self, ip , port , userName , password, dbName, query, dbtype,*args):
        """
        def : secureGetData
        purpose : Executes the query and gets the data
        param : database type, IP, port number , database name, username , password , query
        return : data
        """
        try:
            encryption_obj = AESCipher()
            decrypted_password = encryption_obj.decrypt(password)
            temp = args
            status,result,value,err_msg=self.getData(ip,port,userName,decrypted_password,dbName,query,dbtype,temp)
        except Exceptions as e:
            log.error(e)
            err_msg = str(e)
            logger.print_on_console(err_msg)
        return status,result,value,err_msg

    def verifyData(self, ip , port , userName , password, dbName, query, dbtype,inp_file,inp_sheet):
        """
        def : verifyData
        purpose : Executes the query and compares the data with data in files
        param : database type, IP, port number , database name, username , password , query , Filename , sheetname
        return : bool
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
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
                    if output[1] == "True":
                        status=generic_constants.TEST_RESULT_PASS
                        result=generic_constants.TEST_RESULT_TRUE
                    else:
                        status=generic_constants.TEST_RESULT_FAIL
                        result=generic_constants.TEST_RESULT_FALSE

                else:
                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                    log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
            else:
                logger.print_on_console(generic_constants.FILE_NOT_EXISTS)
        except Exception as e:
            log.error(e)
            err_msg = str(e)
            logger.print_on_console(err_msg)
        finally:
            os.remove(file_path)
            cursor.close()
            cnxn.close()
        return status,result,verb,err_msg

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
            status,result,verb,err_msg=self.verifyData(ip,port,userName,decrypted_password,dbName, query, dbtype,inp_file,inp_sheet)
        except Exceptions as e:
            log.error(e)
            err_msg = str(e)
            logger.print_on_console(err_msg)
        return status,result,verb,err_msg

    def exportData(self, ip , port , userName , password, dbName, query, dbtype, *args):
        """
        def : exportData
        purpose : Executes the query and exports the data to excel or csv file
        param : database type, IP, port number , database name, username , password , query , Filename , sheetname
        return : bool
        """
        status=generic_constants.TEST_RESULT_FAIL
        result=generic_constants.TEST_RESULT_FALSE
        verb = OUTPUT_CONSTANT
        err_msg=None
        try:
            cnxn = self.connection(dbtype, ip , port , dbName, userName , password)
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            ##logic for output col reading
            out_tuple = args
            fields = out_tuple[0]
            inp_sheet = None
            path=None
            if ';' in fields:
                inp_sheet=fields.split(';')[1]
                fields=fields.split(';')[0]
##            verify = os.path.isfile(fields)
##            if (verify == True):
            ext = self.get_ext(fields)
            if (ext == '.xls'):
                verify = os.path.isfile(fields)
                if(verify == False):
                    try:
                       wb = xlwt.Workbook()
                       if(inp_sheet is None or inp_sheet == ''):
                            inp_sheet = 'Sheet0'
                            ws = wb.add_sheet(inp_sheet)
                       else:
                            ws = wb.add_sheet(inp_sheet)
                            log.debug('Input Sheet and file path while creating file :')
                            log.debug(inp_sheet)
                            log.debug(fields)
                       wb.save(fields)
                    except Exception as e:
                        log.error(e)
                        logger.print_on_console(e)
                        err_msg = e
                if(inp_sheet is None or inp_sheet == ''):
                    inp_sheet = 'Sheet0'
                log.debug('Input Sheet is :')
                log.debug(inp_sheet)
                obj=excel_operations.ExcelFile()
                obj.set_excel_path(fields,inp_sheet)
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
                #logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                #log.info(ERROR_CODE_DICT['ERR_INVALID_INPUT'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
##            else:
##                logger.print_on_console(generic_constants.FILE_NOT_EXISTS)
        except Exception as e:
            log.error(e)
            err_msg = str(e)
            logger.print_on_console(err_msg)
        finally:
            cursor.close()
            cnxn.close()
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,result,verb,err_msg

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
            status,result,verb,err_msg=self.exportData(ip,port,userName,decrypted_password,dbName, query, dbtype, out_col[0])
        except Exceptions as e:
            log.error(e)
            err_msg = str(e)
            logger.print_on_console(err_msg)
        return status,result,verb,err_msg

    def connection(self,dbtype, ip , port , dbName, userName , password):
        """
        def : connection
        purpose : connecting to database based on database type given
        param : database type, IP, port number , database name, username , password , query
        return : connection object
        """
        dbNumber = {4:'{SQL Server}',5:'{Microdsoft ODBC for Oracle}',2:'{IBM DB2 ODBC DRIVER}'}
        err_msg=None
        try:
            dbtype= int(dbtype)
            self.cnxn = pyodbc.connect('driver=%s;SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s' % ( dbNumber[dbtype], ip, port, dbName, userName ,password ) )
            return self.cnxn
        except Exception as e:
            log.error(e)
            err_msg = e.msg
        return err_msg


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
                logger.print_on_console(generic_constants.INVALID_FILE_FORMAT)
            return file_ext
        except Exception as e:
            log.error(e)
            err_msg = str(e)
            logger.print_on_console(err_msg)
        return '',status

    def create_file(self):
        """
        def : create_file
        purpose : creates a xls file inside generic folder directory
        param :
        return : path
        """
        path=None
        try:
           wb = xlwt.Workbook()
           ws = wb.add_sheet(generic_constants.DATABASE_SHEET)
           maindir = os.environ["NINETEEN68_HOME"]
           path = maindir + '\Nineteen68\plugins\Generic' + generic_constants.DATABASE_FILE
##           path = 'D:\db5.xls'
           wb.save(path)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg = e
        return path


##obj = DatabaseOperation()
##obj.runQuery('10.44.10.54','1433','version20_test','version2.0_Test','Version20_TestDB',"select * from Persons",'4')
##obj.secureRunQuery('10.44.10.54','1433','version20_test','451MwSMdBUUKiSlqb85IKvYYAt8ag1cO0JE5cEDdotg=','Version20_TestDB',"select * from Persons",'4')
##obj.getData('10.44.10.54','1433','version20_test','version2.0_Test','Version20_TestDB',"select * from Persons",'4')
##obj.secureGetData('10.44.10.54','1433','version20_test','O0v/vLLjfD+hR22U9lzTifYYAt8ag1cO0JE5cEDdotg=','Version20_TestDB',"select * from Persons",'4')
##obj.exportData('4','10.44.10.54','1433','Version20_TestDB','version20_test','version2.0_Test',"select * from Persons",'D:\db6.xls','Sheet1')
##obj.secureExportData('10.44.10.54','1433','version20_test','O0v/vLLjfD+hR22U9lzTifYYAt8ag1cO0JE5cEDdotg=','Version20_TestDB',"select * from Persons",'4','D:\db6.xls','Sheet1')
##obj.exportData('10.44.10.54','1433','version20_test','version2.0_Test','Version20_TestDB',"select * from Persons",'4','D:\db6.xls','Sheet1')
##obj.verifyData('4','10.44.10.54','1433','Version20_TestDB','version20_test','version2.0_Test',"select * from Persons",'D:\db5.xls','Sheet1')
##obj.secureVerifyData('10.44.10.54','1433','version20_test','O0v/vLLjfD+hR22U9lzTifYYAt8ag1cO0JE5cEDdotg=','Version20_TestDB',"select * from Persons",'4','D:\db6.xls','Sheet1')