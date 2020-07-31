#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     29-09-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import os
import logger
import xlwt
from xlutils.copy import copy as xl_copy
import openpyxl
from openpyxl.utils import get_column_letter
import generic_constants
from constants import *
import folder_operations
from file_comparison_operations import TextFile,PdfFile,XML,JSON
import excel_operations
import core_utils
import urllib.request, urllib.error, urllib.parse
import xml.dom.minidom
import json
import difflib
from xmldiff import main, formatting
import readconfig
from xlrd import open_workbook
import dynamic_variable_handler
import logging
log = logging.getLogger('file_operations.py')


class FileOperations:

    """The instantiation operation __init__ creates an empty object of the class FileOperations when it is instantiated"""
    def __init__(self):
        self.txt=TextFile()
        self.pdf=PdfFile()
        self.xml=XML()
        self.json=JSON()
        self.folder=folder_operations.FolderOperations()
        self.xls_obj=excel_operations.ExcelXLS()
        self.xlsx_obj=excel_operations.ExcelXLSX()
        self.csv_obj=excel_operations.ExcelCSV()
        self.DV = dynamic_variable_handler.DynamicVariables()

        """Mapping of keywords to its respective methods"""
        self.dict={'.txt_write_to_file':self.txt.write_to_file,
              '.xls_write_to_file':self.xls_obj.write_to_file_xls,
              '.xlsx_write_to_file':self.xlsx_obj.write_to_file_xlsx,
              '.xml_write_to_file':self.xml.write_to_file,
              '.json_write_to_file':self.json.write_to_file,

              '.xls_verify_content':self.xls_obj.verify_content_xls,
              '.xlsx_verify_content':self.xlsx_obj.verify_content_xlsx,
              '.txt_verify_content':self.txt.verify_content,
              '.pdf_verify_content':self.pdf.verify_content,

              '.txt_compare_content':self.txt.compare_content,
              '.xls_compare_content':self.xls_obj.compare_content_xls,
              '.xlsx_compare_content':self.xlsx_obj.compare_content_xlsx,
              '.pdf_compare_content':self.pdf.compare_content,
              '.csv_compare_content':self.csv_obj.compare_content_csv,
              '.json_compare_content':self.json.compare_content,

              '.txt_clear_content':self.txt.clear_content,
              '.xls_clear_content':self.xls_obj.clear_content_xls,
              '.xlsx_clear_content':self.xlsx_obj.clear_content_xlsx,
              '.xml_clear_content':self.xml.clear_content,

              '.txt_get_content':self.txt.get_content,
              '.pdf_get_content':self.pdf.get_content,

              '.txt_replace_content':self.txt.replace_content,
              '.xls_replace_content':self.xls_obj.replace_content_xls,
              '.xlsx_replace_content':self.xlsx_obj.replace_content_xlsx,

              '.txt_get_line_number':self.txt.get_linenumber,
              '.xls_get_line_number':self.xls_obj.get_linenumber_xls,
              '.xlsx_get_line_number':self.xlsx_obj.get_linenumber_xlsx,

              '.xlsx_create_file':self.xlsx_obj.create_file_xlsx,
              '.xls_create_file':self.xls_obj.create_file_xls
              }

    def create_file(self,inputpath,file_name):
        """
        def : create_file
        purpose : creates the file in the given input path
        param : inputpath,file_name
        return : bool

        """
        try:

            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            output_res=OUTPUT_CONSTANT
            log.debug('reading the inputs')
            inputpath=inputpath.strip()
            log.debug(generic_constants.INPUT_IS+inputpath+' File name '+file_name)

            if not (input is None and input is '') and self.folder.validateFolderName(file_name) :
                if not os.path.isfile(inputpath + '/' + file_name):
                    log.debug('creating the file')
                    fullpath = inputpath + '/' + file_name
                    file_extension,status_get_ext = self.__get_ext(fullpath)
                    if status_get_ext and file_extension is not None and file_extension in generic_constants.EXCEL_TYPES:
                        status_excel_create_file,e_msg = self.dict[file_extension + '_create_file'](fullpath,'Sheet1')
                        if status_excel_create_file and e_msg is None:
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                        else:
                            err_msg = e_msg
                    else:
                        open(fullpath, 'w').close()
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=generic_constants.FILE_EXISTS
            else:
                err_msg=generic_constants.INVALID_INPUT
        except Exception as e:
            log.error(e)
            err_msg=generic_constants.ERR_MSG1+'Creating'+generic_constants.ERR_MSG2
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg


    def verify_file_exists(self,inputpath,file_name):
        """
        def : verify_file_exists
        purpose : verifies if file exists in the given input path
        param : inputpath,file_name
        return : bool

        """
        try:
            coreutilsobj=core_utils.CoreUtils()
            inputpath=coreutilsobj.get_UTF_8(inputpath)
            file_name=coreutilsobj.get_UTF_8(file_name)
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            output_res=OUTPUT_CONSTANT
            log.debug('reading the inputs')
            inputpath=inputpath.strip()
            info_msg=generic_constants.INPUT_IS+inputpath
            log.info(info_msg)
            if inputpath!= None and inputpath!='':
                if file_name!= None and file_name!='':
                    log.info(' and File name is:'+file_name)
                    inputpath=inputpath+os.sep+file_name
                if os.path.isfile(inputpath):
                    log.debug(generic_constants.FILE_EXISTS)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_NO_SUCH_FILE_EXCEPTION']
            else:
                err_msg=generic_constants.INVALID_INPUT
        except (IOError,WindowsError):
            err_msg=ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Verifying'+generic_constants.ERR_MSG2
            log.error(e)
        if err_msg:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg

    def rename_file(self,inputpath,file_name,rename_file):
        """
        def : rename_file
        purpose : renames the file in the 'inputpath' by 'renamepath'
        param : inputpath,file_name
        return : bool

        """
        try:

            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            output_res=OUTPUT_CONSTANT
            log.debug('reading the inputs')
            inputpath=inputpath.strip()
            log.debug(generic_constants.INPUT_IS+inputpath+' File name '+file_name)
##            logger.print_on_console(generic_constants.INPUT_IS+inputpath+' File name '+file_name)
            if not (inputpath is None and inputpath is ''):
                rename_path=inputpath+'/'+rename_file
                inputpath=inputpath+'/'+file_name
                if os.path.isfile(inputpath):
                    log.debug('renaming the file')
                    os.rename(inputpath,rename_path)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_FILE_NOT_FOUND_EXCEPTION']
            else:
                err_msg=generic_constants.INVALID_INPUT
        except (IOError,WindowsError):
            err_msg=ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Renaming'+generic_constants.ERR_MSG2
            log.error(e)
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg

    def delete_file(self,inputpath,file_name):
        """
        def : delete_file
        purpose : deletes the file in the input path
        param : inputpath,file_name
        return : bool

        """
        try:

            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            output_res=OUTPUT_CONSTANT
            log.debug('reading the inputs')
            log.debug(generic_constants.INPUT_IS+inputpath+' File name '+file_name)
##            logger.print_on_console(generic_constants.INPUT_IS+inputpath+' File name '+file_name)
            if not (input is None and input is ''):
                if os.path.isfile(inputpath+'/'+file_name):
                    log.debug('removing the file')
                    os.remove(inputpath+'/'+file_name)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_FILE_NOT_FOUND_EXCEPTION']
            else:
                err_msg=generic_constants.INVALID_INPUT
        except (IOError,WindowsError):
            err_msg=ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Deleting'+generic_constants.ERR_MSG2
            log.error(e)
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg


    def verify_content(self,input_path,content,*args):
        """
        def : verify_content
        purpose : calls the respective method to verify the given content based on file type
        param : input_path,content
        return : bool

        """
        try:

            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            output_res=OUTPUT_CONSTANT
            log.debug('reading the inputs')
            params=self.__split(input_path,content,*args)
            result=self.verify_file_exists(params[0],'')
            if result[1] == TEST_RESULT_TRUE:
                file_ext,res=self.__get_ext(params[0])
                if res == True:
                    log.debug('verifying the contents')
                    res,err_msg= self.dict[file_ext+'_verify_content'](*params)
                    if res:
                        log.debug('content present in the given file')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
            else:
                err_msg=result[3]
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Verifying content of'+generic_constants.ERR_MSG2
            log.error(e)
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg


    def __get_ext(self,input_path):
        """
        def : __get_ext
        purpose : returns the file type and verifies if it is valid file type
        param : input_path
        return : bool,filetype

        """
        try:
            status=False
            filename,file_ext=os.path.splitext(input_path)
            if file_ext.lower() in generic_constants.FILE_TYPES:
                status=True
            else:
                log.info(generic_constants.INVALID_FILE_FORMAT)
                err_msg=generic_constants.INVALID_FILE_FORMAT
            return file_ext,status
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=INPUT_ERROR
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return '',status

    def compare_content(self,input_path1,input_path2,*args):
        """
        def : verify_content
        purpose : calls the respective method to compare the content of 2 files based on file type
        param : input_path1,input_path2
        return : bool

        """
        try:

            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            output_res=OUTPUT_CONSTANT
            log.debug('reading the inputs')
            input_path1 = str(input_path1)
            input_path2 = str (input_path2)
            input_path1 = input_path1.replace(',',';')
            input_path2 = input_path2.replace(',',';')
            params=self.__split(input_path1,input_path2,*args)
            path2=params[1]
            if len(params)>2:
                path2=params[2]
            log.debug('verifying whether the files exists')
            result1=self.verify_file_exists(params[0],'')
            result2=self.verify_file_exists(path2,'')
            if result1[1] == TEST_RESULT_TRUE and result2[1]==TEST_RESULT_TRUE :
                file_ext1,status1=self.__get_ext(params[0])
                file_ext2,status2=self.__get_ext(path2)
                log.debug('comparing the contents')
                if status1 == True and status2==True and file_ext1==file_ext2:
                    res,err_msg=self.dict[file_ext1+'_compare_content'](*params)
                    if res:
                        log.info('files contents are same')
                        logger.print_on_console('files contents are same')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=ERROR_CODE_DICT['ERR_FILE_EXT_MISMATCH']
            else:
                err_msg=result1[3]
                if err_msg==None:
                    err_msg=result2[3]
        except TypeError as e:
            err_msg=ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Comapring content of'+generic_constants.ERR_MSG2
            log.error(e)
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg

    def clear_content(self,input_path,file_name,*args):
        """
        def : clear_content
        purpose : calls the respective method to clear the content of given file based on file type
        param : input_path
        return : bool

        """
        try:

            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            output_res=OUTPUT_CONSTANT
            log.debug('reading the inputs')
            params=self.__split(input_path,file_name,*args)
            log.debug('verifying whether the files exist')
            result=self.verify_file_exists(params[0],params[1])
            if result[1]==TEST_RESULT_TRUE:
                file_ext,res=self.__get_ext(params[1])
                if res == True:
                    log.debug('clearing the content of file')
                    res,err_msg=self.dict[file_ext+'_clear_content'](*params)
                    if res:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
            else:
                err_msg=result[3]
        except TypeError as e:
            err_msg=ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Clearing'+generic_constants.ERR_MSG2
            log.error(e)
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg

    def get_content(self,input_path,*args):
        """
        def : get_content
        purpose : calls the respective method to get the content of given file based on file type
        param : input_path
        return :string

        """
        try:

            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            content=None
            err_msg=None

            log.debug('reading the inputs')
            params=self.__split(input_path,*args)
            log.debug('verifying whether the files exists')
            result=self.verify_file_exists(params[0],'')
            if result[1]==TEST_RESULT_TRUE:
                file_ext,res=self.__get_ext(params[0])
                if file_ext not in ['.xls','.xlsx']:
                    if res == True:
                        log.debug('clearing the content of file')
                        res,content,err_msg=self.dict[file_ext+'_get_content'](*params)
                        if res:
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=generic_constants.NOT_SUPPORTED
            else:
                err_msg=result[3]
        except TypeError as e:
            err_msg=ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
        except Exception as e:
             log.error(e)
             err_msg=generic_constants.ERR_MSG1+'Fetching content of'+generic_constants.ERR_MSG2
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,content,err_msg

    def replace_content(self,input_path,existing_content,replace_content,*args):
        """
        def : replace_content
        purpose : calls the respective method to replace the content of given file based on file type
        param : input_path,existing_content,replace_content
        return : bool

        """
        try:

            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            output_res=OUTPUT_CONSTANT
            log.debug('reading the inputs')
            params=self.__split(input_path,existing_content,replace_content,*args)
            log.debug('verifying whether the files exist')
            result=self.verify_file_exists(params[0],'')
            if result[1]:
                file_ext,res=self.__get_ext(params[0])
                if res == True:
                    log.debug('replacing the content of file')
                    res1=self.dict[file_ext+'_replace_content'](*params)
                    if res1:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
            else:
                err_msg=result[3]
        except TypeError as e:
            err_msg=ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
        except Exception as e:
            err_msg=err_msg=generic_constants.ERR_MSG1+'Replacing content of'+generic_constants.ERR_MSG2
            log.error(e)
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg

    def write_to_file(self,input_path,content,*args):
        """
        def : replace_content
        purpose : calls the respective method to write the content to given file based on file type
        param : input_path,content
        return : bool

        """
        # Defect #872 Special Language Support using unicode to address the issue (Himanshu)
        coreutilsobj=core_utils.CoreUtils()
        try:
            input_path=coreutilsobj.get_UTF_8(input_path)
            content=coreutilsobj.get_UTF_8(content)
            if SYSTEM_OS != 'Darwin':
                import win32com.client
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            output_res=OUTPUT_CONSTANT
            log.debug('reading the inputs')
            params=[]
            log.debug('verifying whether the file exists')
            result=self.verify_file_exists(input_path,'')
            if result[1]==TEST_RESULT_TRUE:
                file_ext,res=self.__get_ext(input_path)
                if file_ext.lower()=='.json':
                    params.append(input_path)
                    params.append(content)
                else:
                    params=self.__split(input_path,content,*args)
                if res == True:
                    log.debug('writing to the file')
                    res,err_msg = self.dict[file_ext+'_write_to_file'](*params)
                    if res:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
            else:
                err_msg=result[3]
        except TypeError as e:
            err_msg=ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Writing to'+generic_constants.ERR_MSG2
            log.error(e)
        if err_msg:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg

    def get_line_number(self,input_path,content,*args):
        """
        def : get_line_number
        purpose : calls the respective method to get the line number where the content is present in
                  given file based on file type
        param : input_path,content
        return : linenumbers [list]

        """
        Tflag= False
        try:

            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            linenumbers=None
            err_msg=None
            output_res=OUTPUT_CONSTANT
            log.debug('reading the inputs')
            data=content
            try:
                if content != '':
                    params=self.__split(input_path,content,*args)
                    result=self.verify_file_exists(params[0],'')
                    if result[1]==TEST_RESULT_TRUE:
                        file_ext,res=self.__get_ext(params[0])
                        if res == True:
                            res,linenumbers,err_msg= self.dict[file_ext+'_get_line_number'](*params)
        ##                    logger.print_on_console(linenumbers)
                            if linenumbers is not None and len(linenumbers) > 0:
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                                Tflag=True
                    else:
                        err_msg=result[3]
            except:
                params=[]
                params.append(input_path)
                params.append(content)
                result=self.verify_file_exists(params[0],'')
                if result[1]==TEST_RESULT_TRUE:
                    file_ext,res=self.__get_ext(params[0])
                    try:
                        if res == True:
                            res,linenumbers,err_msg= self.dict[file_ext+'_get_line_number'](*params)
        ##                    logger.print_on_console(linenumbers)
                            if linenumbers is not None and len(linenumbers) > 0:
                                status=TEST_RESULT_PASS
                                methodoutput=TEST_RESULT_TRUE
                                Tflag=True
                    except:
                        for src, dest in list(self.cp1252.items()):
                            if src in content:
                                content = content.replace(src, dest)
                        content = content.encode('raw_unicode_escape')
                        params=self.__split(input_path,content,*args)
                        result=self.verify_file_exists(params[0],'')
                        if result[1]==TEST_RESULT_TRUE:
                            file_ext,res=self.__get_ext(params[0])
                            if res == True:
                                res,linenumbers,err_msg= self.dict[file_ext+'_get_line_number'](*params)
            ##                    logger.print_on_console(linenumbers)
                                if linenumbers is not None and len(linenumbers) > 0:
                                    status=TEST_RESULT_PASS
                                    methodoutput=TEST_RESULT_TRUE
                                    Tflag=True
                                else:
                                    content=data.encode('cp1252')
                                    params=self.__split(input_path,content,*args)
                                    result=self.verify_file_exists(params[0],'')
                                    if result[1]==TEST_RESULT_TRUE:
                                        file_ext,res=self.__get_ext(params[0])
                                        if res == True:
                                            res,linenumbers,err_msg= self.dict[file_ext+'_get_line_number'](*params)
                        ##                    logger.print_on_console(linenumbers)
                                            if linenumbers is not None and len(linenumbers) > 0:
                                                status=TEST_RESULT_PASS
                                                methodoutput=TEST_RESULT_TRUE
                                                Tflag=True
                                    else:
                                        err_msg=result[3]
                        else:
                            err_msg=result[3]
            if Tflag!=True:
                ##content=data.encode('cp1252')
                for src, dest in list(self.cp1252.items()):
                    if src in content:
                        content = content.replace(src, dest)
                content = content.encode('raw_unicode_escape')
                params=self.__split(input_path,content,*args)
                result=self.verify_file_exists(params[0],'')
                if result[1]==TEST_RESULT_TRUE:
                    file_ext,res=self.__get_ext(params[0])
                    if res == True:
                        res,linenumbers,err_msg= self.dict[file_ext+'_get_line_number'](*params)
    ##                    logger.print_on_console(linenumbers)
                        if linenumbers is not None and len(linenumbers) > 0:
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                            Tflag=True
                        else:
                            content=data.encode('cp1252')
                            params=self.__split(input_path,content,*args)
                            result=self.verify_file_exists(params[0],'')
                            if result[1]==TEST_RESULT_TRUE:
                                file_ext,res=self.__get_ext(params[0])
                                if res == True:
                                    res,linenumbers,err_msg= self.dict[file_ext+'_get_line_number'](*params)
                ##                    logger.print_on_console(linenumbers)
                                    if linenumbers is not None and len(linenumbers) > 0:
                                        status=TEST_RESULT_PASS
                                        methodoutput=TEST_RESULT_TRUE
                                        Tflag=True
                            else:
                                err_msg=result[3]
                else:
                    err_msg=result[3]

        except TypeError as e:
            err_msg=ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
        except Exception as e:
            err_msg=err_msg=generic_constants.ERR_MSG1+'getting line number of'+generic_constants.ERR_MSG2
            log.error(e)
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,linenumbers,err_msg

    def save_file(self,folder_path,file_path):
        """
        def : save_file
        purpose : Saving a file in windows
        param : folder_path,file_path
        return :

        """
        try:
            configvalues = readconfig.readConfig().readJson()
            delay_stringinput = float(configvalues['delay_stringinput'])
            import time
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            err_msg=None
            output_res=OUTPUT_CONSTANT
            log.debug('reading the inputs')
            folder_path=str(folder_path)
            file_path=str(file_path)
            log.debug('Folder path is '+folder_path+' and File is '+file_path)

##            logger.print_on_console('Folder path is '+folder_path+' and File is '+file_path)
            if (not(folder_path is None or folder_path == '' or file_path is None or file_path == '') and os.path.exists(folder_path)):
                log.debug('saving the file')
                """
                if (url_save is not None):
                    ##print folder_path,file_path
                    response = urllib2.urlopen(url_save)
                    file = open(folder_path+"\\"+file_path+".pdf", 'wb')
                    file.write(response.read())
                    file.close()
                    ##print("Completed")
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                    log.info('File has been saved')
                else:
                """

                from sendfunction_keys import SendFunctionKeys
                obj=SendFunctionKeys()

                #Get the focus on Windows Dialog box by pressing 'alt+d'
                obj.press_multiple_keys(['alt','d'],1)      ##added timer after every step
                time.sleep(1)

                #Enter the folder path
                obj.type(folder_path,delay_stringinput)
                time.sleep(1)
                #Press 'Enter' key
                obj.execute_key('enter',1)
                time.sleep(1)
                #Press 'tab' key to get the focus on 'search tab'
                obj.execute_key('tab',1)
                time.sleep(1)
                #Press 'alt+n' key to create a new file
                obj.press_multiple_keys(['alt','n'],1)
                time.sleep(1)
                #Enter the file name
                obj.type(file_path,delay_stringinput)
                time.sleep(1)
                #Press 'Enter' key
                obj.execute_key('enter',1)
                time.sleep(2)
                #Press 'alt+y' key in case if the file is already existing
                obj.press_multiple_keys(['alt','y'],1)   #added alt+y sendfunction key for automating overwrite process if the file is already existed.

                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE

                log.info('File has been saved')


            else:
                err_msg=generic_constants.INVALID_INPUT
        except (IOError,WindowsError):
            err_msg=ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            log.error(e)
            err_msg=generic_constants.ERR_MSG1+'Saving'+generic_constants.ERR_MSG2
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg

    def json_compare_content(self,input_path1,input_path2,*args):
        """
        def : verify_Json_content
        purpose : calls the respective method to compare the content of 2 Json
        param : input_path1,input_path2
        return : bool

        """

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_res=OUTPUT_CONSTANT
        try:

            file_ext1,status1=self.__get_ext(input_path1)
            file_ext2,status2=self.__get_ext(input_path2)

            if status1 == True and status2==True and file_ext1==file_ext2:
                log.debug('verifying whether the files exists')
                result1=self.verify_file_exists(input_path1,'')
                result2=self.verify_file_exists(input_path2,'')
                if result1[1] == TEST_RESULT_TRUE and result2[1]==TEST_RESULT_TRUE :
                    content1 = json.dumps(input_path1)
                    with open(input_path1) as file_open:
                        content1=json.dumps((json.load(file_open)))
                        file_open.close()

                    with open(input_path2) as file_open:
                        content2=json.dumps((json.load(file_open)))
                        file_open.close()
                    params=[content1,content2]
                    res,err_msg=self.dict[file_ext1.lower()+'_compare_content'](*params)
                    if res:
                        log.info('files contents are same')
                        logger.print_on_console('files contents are same')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=result1[3]
                    if err_msg==None:
                        err_msg=result2[3]

            else:
                err_msg=ERROR_CODE_DICT['ERR_FILE_EXT_MISMATCH']
                try:
                    json.loads(input_path1)
                    json.loads(input_path2)
                    params=[input_path1,input_path2]
                    res,err_msg=self.dict['.json_compare_content'](*params)
                    if res:
                        log.info('files contents are same')
                        logger.print_on_console('files contents are same')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                except Exception as e:
                    if err_msg==None:
                        err_msg="Failed to load the JSON"
                    log.error(e)
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Comapring content of'+generic_constants.ERR_MSG2
            log.error(e)
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg

    def __split(self,*args):
        """
        def : __split
        purpose : splits each argumnet by ';' and add it to list and returns
        param : variable number of args
        return : list

        """
        params=[]
        for x in args:
            if isinstance(x, str):
                x.strip()
                val=x.split(';')
                for y in val:
                    params.append(y)
            else:
                params.append(x)
        return params

    cp1252 = {
        # from http://www.microsoft.com/typography/unicode/1252.htm
        "\\u20AC": "\x80", # EURO SIGN
        "\\u201A": "\x82", # SINGLE LOW-9 QUOTATION MARK
        "\\u0192": "\x83", # LATIN SMALL LETTER F WITH HOOK
        "\\u201E": "\x84", # DOUBLE LOW-9 QUOTATION MARK
        "\\u2026": "\x85", # HORIZONTAL ELLIPSIS
        "\\u2020": "\x86", # DAGGER
        "\\u2021": "\x87", # DOUBLE DAGGER
        "\\u02C6": "\x88", # MODIFIER LETTER CIRCUMFLEX ACCENT
        "\\u2030": "\x89", # PER MILLE SIGN
        "\\u0160": "\x8A", # LATIN CAPITAL LETTER S WITH CARON
        "\\u2039": "\x8B", # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
        "\\u0152": "\x8C", # LATIN CAPITAL LIGATURE OE
        "\\u017D": "\x8E", # LATIN CAPITAL LETTER Z WITH CARON
        "\\u2018": "\x91", # LEFT SINGLE QUOTATION MARK
        "\\u2019": "\x92", # RIGHT SINGLE QUOTATION MARK
        "\\u201C": "\x93", # LEFT DOUBLE QUOTATION MARK
        "\\u201D": "\x94", # RIGHT DOUBLE QUOTATION MARK
        "\\u2022": "\x95", # BULLET
        "\\u2013": "\x96", # EN DASH
        "\\u2014": "\x97", # EM DASH
        "\\u02DC": "\x98", # SMALL TILDE
        "\\u2122": "\x99", # TRADE MARK SIGN
        "\\u0161": "\x9A", # LATIN SMALL LETTER S WITH CARON
        "\\u203A": "\x9B", # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
        "\\u0153": "\x9C", # LATIN SMALL LIGATURE OE
        "\\u017E": "\x9E", # LATIN SMALL LETTER Z WITH CARON
        "\\u0178": "\x9F", # LATIN CAPITAL LETTER Y WITH DIAERESIS
    }

    def write_result_file(self,outputFilePath,content,sheetname):
        """
        def : write_result_file
        purpose : Writing the compare results into the specified file, supporting xls and xlsx extension.
        param : outputFilePath;content;sheetname
        return : bool
        """
        status = False
        err_msg = None
        result3 = None
        index_sheet = None
        try:
            result3=os.path.isfile(outputFilePath)
            file_ext,status1=self.__get_ext(outputFilePath)

            if ( file_ext == '.xls' ):
                #checking the file exists and open the exists file.
                if result3==True:
                    rb = open_workbook(outputFilePath)
                    work_book = xl_copy(rb)
                else:
                    #creating the new file, while given file fails.
                    work_book = xlwt.Workbook(encoding="utf-8")

                log.debug('Input Sheet is :')
                log.debug(sheetname)
                try:
                    #adding the new sheet.
                    work_sheet = work_book.add_sheet(sheetname)

                except:
                    #geeting the existing sheet
                    work_sheet = work_book.get_sheet(sheetname)

                index_sheet = work_book.sheet_index(sheetname)

                log.debug('Input Sheet and file path while creating file :')
                log.debug(sheetname)
                log.debug(outputFilePath)
                for column in content.keys():
                    row = 0
                    max_col_width=2962
                    for value in content[column]:
                        work_sheet.write(row,int(column),value)
                        row+=1
                        #add the adjusting width to expand the column.
                        adjusted_width = len(value)*367
                        if (len(value)*367) > max_col_width:
                            max_col_width=(len(value)*367)
                        work_sheet.col(int(column)).width = max_col_width
                work_book.set_active_sheet(index_sheet)
                log.info("WorkSheet Saving : {}".format(outputFilePath))
                work_book.save(outputFilePath)
                del column,row,max_col_width,adjusted_width,value,work_book,work_sheet
                status=True

            elif( file_ext == '.xlsx' ):
                if result3==True:
                    #checking the file and open the existing file.
                    wb = openpyxl.load_workbook(outputFilePath)
                else:
                    #creating the new file.
                    wb = openpyxl.Workbook()

                log.debug(sheetname)
                sheet_names = wb.sheetnames
                if len(sheet_names)>0:
                    if sheetname in sheet_names:
                        index_sheet=sheet_names.index(sheetname)
                    else:
                        index_sheet = 0
                        #adding the New sheet.
                        wb.create_sheet(index=index_sheet, title=sheetname)

                log.debug('Input Sheet and file path while creating file :')
                log.debug(sheetname)
                log.debug(input_file)
                #reading the existing sheet
                sheet = wb[sheetname]
                for column in content.keys():
                    row=1
                    max_col_width = 2.4
                    for value in content[column]:
                        sheet.cell(row=row, column=int(column)+1).value = value
                        row+=1
                        adjusted_width = (len(value) + 2) * 1.2
                        if adjusted_width > max_col_width:
                            max_col_width=adjusted_width
                        sheet.column_dimensions[get_column_letter(int(column)+1)].width = max_col_width
                wb.active=index_sheet
                log.info("WorkBook Saving: {}".format(outputFilePath))
                wb.save(outputFilePath)
                del column,row,max_col_width,adjusted_width,value,sheet_names,wb
                status=True

        except Exception as e:
            err_msg='Writing to Excel Sheet Failed'
            log.error(e)
        log.info('Status of write_result_file is ' + str(status) )
        del outputFilePath,sheetname,result3,index_sheet
        return status, err_msg

    def cell_by_cell_compare(self,input_val,*args):
        """
        def : cell_by_cell_compare
        purpose : compares the data of given sheets of 2 different excel files and write down the result in another result sheet.
        param : input : <input_path1>;<sheet1(optional)>;<input_path2>;<sheet2(optional)>;<selective(optional- will print diff b/w mismatched text of each cell in provided output excel file )> output: output_path(optional)
        return : bool/ if output file mentioned then prints cell by cell to that file
        """
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        output = OUTPUT_CONSTANT
        flg = False
        desc = None
        collect_content={}
        opt = False
        input_path1 = None
        sheetname1 = None
        input_path2 = None
        sheetname2 = None
        output_feild = None
        log.debug('Comparing content cell by cell of .xls files ')
        try:
            input_path1 = input_val[0]
            sheetname1 = input_val[1]
            input_path2 = input_val[2]
            sheetname2 = input_val[3]
            if ( len(input_val) == 5 and input_val[4].strip().lower() == 'selective'):
                opt = True

            if ( args[0] ) :
                out_path = self.DV.get_dynamic_value(args[0].split(";")[0])
                if ( out_path ): output_feild = out_path


            book1 = open_workbook(input_path1)
            book2 = open_workbook(input_path2)
            if (sheetname1.strip() != ''):sheet1 = book1.sheet_by_name(sheetname1)
            else : sheet1 = book1.sheet_by_index(0)
            if (sheetname2.strip() != ''):sheet2 = book2.sheet_by_name(sheetname2)
            else : sheet2 = book2.sheet_by_index(0)

            log.debug('verifying whether the files exists')
            result1=self.verify_file_exists(input_path1,'')
            result2=self.verify_file_exists(input_path2,'')
            log.info("taking the maxium row and column")
            row_max=max(sheet1.nrows,sheet2.nrows)
            col_max=max(sheet1.ncols,sheet2.ncols)

            if result1[1] == TEST_RESULT_TRUE and result2[1]==TEST_RESULT_TRUE:
                for rownum in range(int(row_max)):
                    for colnum in range(int(col_max)):
                        try:
                            c1=str(sheet1.cell(rownum, colnum).value)
                        except:
                            c1=None
                        try:
                            c2=str(sheet2.cell(rownum, colnum).value)
                        except:
                            c2=None
                        if (c1!=None and c2!=None) and (c1!='' and c2!=''):
                            if c1 != c2:
                                out='Not Matched'
                                desc="Not Matched, Cell Values {} and {}".format(c1,c2)
                            else:
                                out="Matched"
                                desc="Matched"
                        elif (c1==None or c1=='') and (c2== '' or c2==None):
                            out=''
                            desc=''
                        else:
                            out= 'Not Matched'
                            desc="Not Matched, Cell Values {} and {}".format(c1,c2)

                        if colnum not in collect_content.keys():
                            collect_content[colnum]=[]
                            if( opt == True ):
                                collect_content[colnum].append(desc)
                            else:
                                collect_content[colnum].append(out)
                        else:
                            if( opt == True ):
                                collect_content[colnum].append(desc)
                            else:
                                collect_content[colnum].append(out)
                del rownum, colnum, desc, out, c1, c2 #deleting variables
                if( output_feild ):
                    if( os.path.exists(output_feild) or os.path.exists(os.path.dirname(output_feild)) ):
                        logger.print_on_console( "Writing the output of cellByCellCompare to file : " + str(output_feild) )
                        flg, err_msg = self.write_result_file(output_feild, collect_content, 'CellByCellCompare_Result')
                    else:
                        status_excel_create_file = False
                        file_extension,status_get_ext = self.__get_ext(output_feild)
                        if status_get_ext and file_extension is not None and file_extension in generic_constants.EXCEL_TYPES:
                            status_excel_create_file,e_msg = self.dict[file_extension + '_create_file'](output_feild,'CellByCellCompare_Result')
                        else:
                            err_msg = 'Warning! : Invalid file extension. Output file format should be either ".xls" or ".xlxs".'
                        if (status_excel_create_file):
                            logger.print_on_console( "Writing the output of cellByCellCompare to file : " + str(output_feild) )
                            flg, err_msg = self.write_result_file(output_feild, collect_content, 'CellByCellCompare_Result')
                    if ( flg ):
                        status = TEST_RESULT_PASS
                        result = TEST_RESULT_TRUE
                else:
                    logger.print_on_console("Output file not provided")
                    if (collect_content) :
                        output = collect_content
                        status = TEST_RESULT_PASS
                        result = TEST_RESULT_TRUE
                    else :
                        err_msg = "Content is empty"
            else:
                err_msg = 'Error : Validity of file path 1 is : ' + str(result1[1]) + 'and validity of file path 2 is : ' + str(result2[1]) + '. Please make sure file paths entered are correct'
            if ( err_msg ):
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = 'Error occured in compare content of two files ERR_MSG: ' + str(e)
            log.error(err_msg)
            logger.print_on_console(err_msg)
        del input_path1, sheetname1, input_path2, sheetname2, book1, book2, row_max, col_max, output_feild, result1, result2, collect_content #deleting variables
        return status, result, output, err_msg