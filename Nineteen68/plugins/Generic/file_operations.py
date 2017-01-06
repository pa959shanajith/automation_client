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
import generic_constants
from constants import *
import folder_operations
from file_comparison_operations import TextFile,PdfFile,XML
import excel_operations
import Exceptions
from constants import *
from loggermessages import *
import logging


log = logging.getLogger('file_operations.py')


class FileOperations:

    """The instantiation operation __init__ creates an empty object of the class FileOperations when it is instantiated"""
    def __init__(self):
        self.txt=TextFile()
        self.pdf=PdfFile()
##        self.excel=ExcelFile()
        self.xml=XML()
        self.folder=folder_operations.FolderOperations()
        self.xls_obj=excel_operations.ExcelXLS()
        self.xlsx_obj=excel_operations.ExcelXLSX()

        """Mapping of keywords to its respective methods"""
        self.dict={'.txt_write_to_file':self.txt.write_to_file,
              '.xls_write_to_file':self.xls_obj.write_to_file_xls,
              '.xlsx_write_to_file':self.xlsx_obj.write_to_file_xlsx,
              '.xml_write_to_file':self.xml.write_to_file,

              '.xls_verify_content':self.xls_obj.verify_content_xls,
              '.xlsx_verify_content':self.xlsx_obj.verify_content_xlsx,
              '.txt_verify_content':self.txt.verify_content,
              '.pdf_verify_content':self.pdf.verify_content,

              '.txt_compare_content':self.txt.compare_content,
              '.xls_compare_content':self.xls_obj.compare_content_xls,
              '.xlsx_compare_content':self.xlsx_obj.compare_content_xlsx,
              '.pdf_compare_content':self.pdf.compare_content,

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
              '.xlsx_get_line_number':self.xlsx_obj.get_linenumber_xlsx
              }

    def create_file(self,inputpath,file_name):
        """
        def : create_file
        purpose : creates the file in the given input path
        param : inputpath,file_name
        return : bool

        """
        try:
            log.info(KEYWORD_EXECUTION_STARTED)
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            error_msg=None
            output_res=MD5_TEMP_RES
            log.debug('reading the inputs')
            inputpath=inputpath.strip()
            log.debug(generic_constants.INPUT_IS+inputpath+' File name '+file_name)
            logger.print_on_console(generic_constants.INPUT_IS+inputpath+' File name '+file_name)
            if not (input is None and input is '') and self.folder.validateFolderName(file_name) :
                if not os.path.isfile(inputpath+'/'+file_name):
                    log.debug('opening the file')
                    open(inputpath+'/'+file_name, 'w').close()
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    log.error(generic_constants.FILE_EXISTS)
                    logger.print_on_console(generic_constants.FILE_EXISTS)
            else:
                log.error(generic_constants.INVALID_INPUT)
                logger.print_on_console(generic_constants.INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output_res,error_msg


    def verify_file_exists(self,inputpath,file_name):
        """
        def : verify_file_exists
        purpose : verifies if file exists in the given input path
        param : inputpath,file_name
        return : bool

        """
        try:
            log.info(KEYWORD_EXECUTION_STARTED)
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            error_msg=None
            output_res=MD5_TEMP_RES
            log.debug('reading the inputs')
            inputpath=inputpath.strip()
            log.debug(generic_constants.INPUT_IS+inputpath+' File name '+file_name)
            logger.print_on_console(generic_constants.INPUT_IS+inputpath+' File name '+file_name)
            if not (input is None and input is ''):
                if file_name is not '':inputpath=inputpath+'/'+file_name
                if os.path.isfile(inputpath):
                    log.debug('file exists')
                    logger.print_on_console(generic_constants.FILE_EXISTS)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    log.debug(generic_constants.FILE_NOT_EXISTS)
                    logger.print_on_console(generic_constants.FILE_NOT_EXISTS)
            else:
                log.debug(generic_constants.INVALID_INPUT)
                logger.print_on_console(generic_constants.INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output_res,error_msg

    def rename_file(self,inputpath,file_name,rename_file):
        """
        def : rename_file
        purpose : renames the file in the 'inputpath' by 'renamepath'
        param : inputpath,file_name
        return : bool

        """
        try:
            log.info(KEYWORD_EXECUTION_STARTED)
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            error_msg=None
            output_res=MD5_TEMP_RES
            log.debug('reading the inputs')
            inputpath=inputpath.strip()
            log.debug(generic_constants.INPUT_IS+inputpath+' File name '+file_name)
            logger.print_on_console(generic_constants.INPUT_IS+inputpath+' File name '+file_name)
            if not (inputpath is None and inputpath is ''):
                rename_path=inputpath+'/'+rename_file
                inputpath=inputpath+'/'+file_name
                if os.path.isfile(inputpath):
                    log.debug('renaming the file')
                    os.rename(inputpath,rename_path)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    log.debug(generic_constants.FILE_NOT_EXISTS)
                    logger.print_on_console(generic_constants.FILE_NOT_EXISTS)
            else:
                log.debug(generic_constants.INVALID_INPUT)
                logger.print_on_console(generic_constants.INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output_res,error_msg

    def delete_file(self,inputpath,file_name):
        """
        def : delete_file
        purpose : deletes the file in the input path
        param : inputpath,file_name
        return : bool

        """
        try:
            log.info(KEYWORD_EXECUTION_STARTED)
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            error_msg=None
            output_res=MD5_TEMP_RES
            log.debug('reading the inputs')
            log.debug(generic_constants.INPUT_IS+inputpath+' File name '+file_name)
            logger.print_on_console(generic_constants.INPUT_IS+inputpath+' File name '+file_name)
            if not (input is None and input is ''):
                if os.path.isfile(inputpath+'/'+file_name):
                    log.debug('removing the file')
                    os.remove(inputpath+'/'+file_name)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    log.debug(generic_constants.FILE_NOT_EXISTS)
                    logger.print_on_console(generic_constants.FILE_NOT_EXISTS)
            else:
                log.debug(generic_constants.INVALID_INPUT)
                logger.print_on_console(generic_constants.INVALID_INPUT)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output_res,error_msg


    def verify_content(self,input_path,content,*args):
        """
        def : verify_content
        purpose : calls the respective method to verify the given content based on file type
        param : input_path,content
        return : bool

        """
        try:
            log.info(KEYWORD_EXECUTION_STARTED)
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            error_msg=None
            output_res=MD5_TEMP_RES
            log.debug('reading the inputs')
            params=self.__split(input_path,content,*args)
            if self.verify_file_exists(params[0],'') == True:
                file_ext,res=self.__get_ext(params[0])
                if res == True:
                    log.debug('verifying the contents')
                    res= self.dict[file_ext+'_verify_content'](*params)
                    if res:
                        log.debug('content present the given file')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output_res,error_msg


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
            if file_ext in generic_constants.FILE_TYPES:
                status=True
            else:
                log.debug(generic_constants.INVALID_FILE_FORMAT)
                logger.print_on_console(generic_constants.INVALID_FILE_FORMAT)
            return file_ext,status
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return '',status

    def compare_content(self,input_path1,input_path2,*args):
        """
        def : verify_content
        purpose : calls the respective method to compare the content of 2 files based on file type
        param : input_path1,input_path2
        return : bool

        """
        try:
            log.info(KEYWORD_EXECUTION_STARTED)
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            error_msg=None
            output_res=MD5_TEMP_RES
            log.debug('reading the inputs')
            params=self.__split(input_path1,input_path2,*args)
            path2=params[1]
            if len(params)>2:
                path2=params[2]
            log.debug('verifying whether the files exists')
            if self.verify_file_exists(params[0],'')[1] and self.verify_file_exists(path2,'')[1] :
                file_ext1,status1=self.__get_ext(params[0])
                file_ext2,status2=self.__get_ext(path2)
                log.debug('comparing the contents')
                if status1 == True and status2==True and file_ext1==file_ext2:
                    res=self.dict[file_ext1+'_compare_content'](*params)
                    if res:
                        log.debug('files contenta are same')
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output_res,error_msg

    def clear_content(self,input_path,*args):
        """
        def : clear_content
        purpose : calls the respective method to clear the content of given file based on file type
        param : input_path
        return : bool

        """
        try:
            log.info(KEYWORD_EXECUTION_STARTED)
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            error_msg=None
            output_res=MD5_TEMP_RES
            log.debug('reading the inputs')
            params=self.__split(input_path,*args)
            log.debug('verifying whether the files exist')
            if self.verify_file_exists(params[0],'')[1]:
                file_ext,res=self.__get_ext(params[0])
                if res == True:
                    log.debug('clearing the content of file')
                    res=self.dict[file_ext+'_clear_content'](*params)
                    if res:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output_res,error_msg

    def get_content(self,input_path,*args):
        """
        def : get_content
        purpose : calls the respective method to get the content of given file based on file type
        param : input_path
        return :string

        """
        try:
            log.info(KEYWORD_EXECUTION_STARTED)
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            content=None
            error_msg=None

            log.debug('reading the inputs')
            params=self.__split(input_path,*args)
            log.debug('verifying whether the files exists')
            if self.verify_file_exists(params[0],'')[1]:
                file_ext,res=self.__get_ext(params[0])
                if file_ext not in ['.xls','.xlsx']:
                    if res == True:
                        log.debug('clearing the content of file')
                        res,content=self.dict[file_ext+'_get_content'](*params)
                        if res:
                            status=TEST_RESULT_PASS
                            methodoutput=TEST_RESULT_TRUE
                else:
                    error_msg='Excel files are not supported'
                    log.error('Excel files are not supported')
                    logger.print_on_console('Excel files are not supported')
        except Exception as e:
             log.error(e)
             logger.print_on_console(e)
             error_msg=e
        return status,methodoutput,content,error_msg

    def replace_content(self,input_path,existing_content,replace_content,*args):
        """
        def : replace_content
        purpose : calls the respective method to replace the content of given file based on file type
        param : input_path,existing_content,replace_content
        return : bool

        """
        try:
            log.info(KEYWORD_EXECUTION_STARTED)
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            error_msg=None
            output_res=MD5_TEMP_RES
            log.debug('reading the inputs')
            params=self.__split(input_path,existing_content,replace_content,*args)
            log.debug('verifying whether the files exist')
            if self.verify_file_exists(params[0],'')[1]:
                file_ext,res=self.__get_ext(params[0])
                if res == True:
                    log.debug('replacing the content of file')
                    res=self.dict[file_ext+'_replace_content'](*params)
                    if res:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output_res,error_msg

    def write_to_file(self,input_path,content,*args):
        """
        def : replace_content
        purpose : calls the respective method to write the content to given file based on file type
        param : input_path,content
        return : bool

        """
        try:
            log.info(KEYWORD_EXECUTION_STARTED)
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            error_msg=None
            output_res=MD5_TEMP_RES
            log.debug('reading the inputs')
            params=self.__split(input_path,content,*args)
            log.debug('verifying whether the file exists')
            if self.verify_file_exists(params[0],'')[1]:
                file_ext,res=self.__get_ext(params[0])
                if res == True:
                    log.debug('writing to the file')
                    res = self.dict[file_ext+'_write_to_file'](*params)
                    if res:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output_res,error_msg

    def get_line_number(self,input_path,content,*args):
        """
        def : get_line_number
        purpose : calls the respective method to get the line number where the content is present in
                  given file based on file type
        param : input_path,content
        return : linenumbers [list]

        """
        try:
            log.info(KEYWORD_EXECUTION_STARTED)
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            linenumbers=None
            error_msg=None
            output_res=MD5_TEMP_RES
            log.debug('reading the inputs')
            params=self.__split(input_path,content,*args)
            if self.verify_file_exists(params[0],'')[1]:
                file_ext,res=self.__get_ext(params[0])
                if res == True:
                    res,linenumbers= self.dict[file_ext+'_get_line_number'](*params)
                    logger.print_on_console(linenumbers)
                    if linenumbers is not None:
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,linenumbers,error_msg

    def save_file(self,folder_path,file_path):
        """
        def : save_file
        purpose : Saving a file in windows
        param : folder_path,file_path
        return :

        """
        try:
            log.info(KEYWORD_EXECUTION_STARTED)
            status=TEST_RESULT_FAIL
            methodoutput=TEST_RESULT_FALSE
            error_msg=None
            output_res=MD5_TEMP_RES
            log.debug('reading the inputs')
            folder_path=str(folder_path)
            file_path=str(file_path)
            log.debug('Folder path is '+folder_path+' and File is '+file_path)
            logger.print_on_console('Folder path is '+folder_path+' and File is '+file_path)
            if (not(folder_path is None or folder_path == '' or file_path is None or file_path == '') and os.path.exists(folder_path)):
                log.debug('saving the file')
                from sendfunction_keys import SendFunctionKeys
                obj=SendFunctionKeys()
                #Get the focus on Windows Dialog box by pressing 'alt+d'
                obj.press_multiple_keys(['alt','d'],1)
                #Enter the folder path
                obj.type(folder_path)
                #Press 'Enter' key
                obj.execute_key('enter',1)
                #Press 'tab' key to get the focus on 'search tab'
                obj.execute_key('tab',1)
                #Press 'alt+n' key to create a new file
                obj.press_multiple_keys(['alt','n'],1)
                #Enter the file name
                obj.type(file_path)
                #Press 'Enter' key
                obj.execute_key('enter',1)
                #Press 'ctrl+y' key in case if the file is already existing
                obj.press_multiple_keys(['ctrl','y'],1)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
                log.debug('File has been saved')

            else:
                log.error('Invalid input')
                logger.print_on_console('Invalid input')
                error_msg='Invalid input'

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            error_msg=e
        return status,methodoutput,output_res,error_msg

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

