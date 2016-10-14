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
from file_comparison_operations import TextFile,PdfFile,XML
from excel_operartions import ExcelFile
import Exceptions


class FileOperations:

    """The instantiation operation __init__ creates an empty object of the class FileOperations when it is instantiated"""
    def __init__(self):
        print 'init'
        self.txt=TextFile()
        self.pdf=PdfFile()
        self.excel=ExcelFile()
        self.xml=XML()
        """Mapping of keywords to its respective methods"""
        self.dict={'.txt_write_to_file':self.txt.write_to_file,
              '.xls_write_to_file':self.excel.write_to_file_xls,
              '.xlsx_write_to_file':self.excel.write_to_file_xlsx,
              '.xml_write_to_file':self.xml.write_to_file,

              '.xls_verify_content':self.excel.verify_content_xls,
              '.xlsx_verify_content':self.excel.verify_content_xlsx,
              '.txt_verify_content':self.txt.verify_content,
              '.pdf_verify_content':self.pdf.verify_content,

              '.txt_compare_content':self.txt.compare_content,
              '.xls_compare_content':self.excel.compare_content_xls,
              '.xlsx_compare_content':self.excel.compare_content_xlsx,
              '.pdf_compare_content':self.pdf.compare_content,

              '.txt_clear_content':self.txt.clear_content,
              '.xls_clear_content':self.excel.clear_content_xls,
              '.xlsx_clear_content':self.excel.clear_content_xlsx,
              '.xml_clear_content':self.xml.clear_content,

              '.txt_get_content':self.txt.get_content,
              '.pdf_get_content':self.pdf.get_content,

              '.txt_replace_content':self.txt.replace_content,
              '.xls_replace_content':self.excel.replace_content_xls,
              '.xlsx_replace_content':self.excel.replace_content_xls,

              '.txt_get_line_number':self.txt.get_linenumber,
              '.xls_get_line_number':self.excel.get_linenumber_xls,
              '.xlsx_get_line_number':self.excel.get_linenumber_xlsx
              }

    def create_file(self,input):
        """
        def : create_file
        purpose : creates the file in the given input path
        param : input
        return : bool

        """
        try:
            input=input.strip()
            logger.log(generic_constants.INPUT_IS+input)
            if not (input is None and input is ''):
                if not os.path.isfile(input):
                    open(input, 'w').close()
                    return True
                else:
                    logger.log(generic_constants.FILE_EXISTS)
            else:
                logger.log(generic_constants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return False


    def verify_file_exists(self,input):
        """
        def : verify_file_exists
        purpose : verifies if file exists in the given input path
        param : input
        return : bool

        """
        try:
            input=input.strip()
            logger.log(generic_constants.INPUT_IS+input)
            if not (input is None and input is ''):
                if os.path.isfile(input):
                    logger.log(generic_constants.FILE_EXISTS)
                    return True
                else:
                    logger.log(generic_constants.FILE_NOT_EXISTS)
            else:
                logger.log(generic_constants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return False

    def rename_file(self,actualpath,renamepath):
        """
        def : rename_file
        purpose : renames the file in the 'actualpath' by 'renamepath'
        param : actualpath,renamepath
        return : bool

        """
        try:
            actualpath=actualpath.strip()
            logger.log(generic_constants.INPUT_IS+actualpath)
            if not (actualpath is None and actualpath is ''):
                if os.path.isfile(actualpath):
                    os.rename(actualpath,renamepath)
                    return True
                else:
                    logger.log(generic_constants.FILE_NOT_EXISTS)
            else:
                logger.log(generic_constants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return False


    def delete_file(self,input):
        """
        def : delete_file
        purpose : deletes the file in the input path
        param : input
        return : bool

        """
        try:
            input=input.strip()
            status=False
            logger.log(generic_constants.INPUT_IS+input)
            if not (input is None and input is ''):
                if os.path.isfile(input):
                    os.remove(input)
                    status= True
                else:
                    logger.log(generic_constants.FILE_NOT_EXISTS)
            else:
                logger.log(generic_constants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status


    def verify_content(self,input_path,content,*args):
        """
        def : verify_content
        purpose : calls the respective method to verify the given content based on file type
        param : input_path,content
        return : bool

        """
        try:
            status=False
            params=self.__split(input_path,content,*args)
            if self.verify_file_exists(params[0]) == True:
                file_ext,res=self.__get_ext(params[0])
                if res == True:
                    status= self.dict[file_ext+'_verify_content'](*params)
        except Exception as e:
            Exceptions.error(e)
        return status


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
                logger.log(generic_constants.INVALID_FILE_FORMAT)
            return file_ext,status
        except Exception as e:
            Exceptions.error(e)
            return '',status

    def compare_content(self,input_path1,input_path2,*args):
        """
        def : verify_content
        purpose : calls the respective method to compare the content of 2 files based on file type
        param : input_path1,input_path2
        return : bool

        """
        try:
            status=False
            params=self.__split(input_path1,input_path2)
            path2=params[1]
            if len(params)>2:
                path2=params[2]
            if self.verify_file_exists(params[0]) == True and self.verify_file_exists(path2) :
                file_ext1,status1=self.__get_ext(params[0])
                file_ext2,status2=self.__get_ext(path2)
                if status1 == True and status2==True and file_ext1==file_ext2:
                    status=self.dict[file_ext1+'_compare_content'](*params)
        except Exception as e:
            Exceptions.error(e)
        return status

    def clear_content(self,input_path):
        """
        def : clear_content
        purpose : calls the respective method to clear the content of given file based on file type
        param : input_path
        return : bool

        """
        try:
            status=False
            params=self.__split(input_path)
            if self.verify_file_exists(params[0]) == True:
                file_ext,res=self.__get_ext(params[0])
                if res == True:
                    status=self.dict[file_ext+'_clear_content'](*params)
        except Exception as e:
            Exceptions.error(e)
        return status

    def get_content(self,input_path,*args):
        """
        def : get_content
        purpose : calls the respective method to get the content of given file based on file type
        param : input_path
        return :string

        """
        try:
            status=False
            params=self.__split(input_path,*args)
            if self.verify_file_exists(params[0]) == True:
                file_ext,res=self.__get_ext(params[0])
                if res == True:
                    status=self.dict[file_ext+'_get_content'](*params)
        except Exception as e:
            Exceptions.error(e)
        return status

    def replace_content(self,input_path,existing_content,replace_content):
        """
        def : replace_content
        purpose : calls the respective method to replace the content of given file based on file type
        param : input_path,existing_content,replace_content
        return : bool

        """
        try:
            status=False
            params=self.__split(input_path,existing_content,replace_content)
            if self.verify_file_exists(params[0]) == True:
                file_ext,res=self.__get_ext(params[0])
                if res == True:
                    status=self.dict[file_ext+'_replace_content'](*params)
        except Exception as e:
            Exceptions.error(e)
        return status

    def write_to_file(self,input_path,content):
        """
        def : replace_content
        purpose : calls the respective method to write the content to given file based on file type
        param : input_path,content
        return : bool

        """
        try:
            status=False
            params=self.__split(input_path,content)
            if self.verify_file_exists(params[0]) == True:
                file_ext,res=self.__get_ext(params[0])
                if res == True:
                    status = self.dict[file_ext+'_write_to_file'](*params)
                    return status
        except Exception as e:
            Exceptions.error(e)
        return status

    def get_line_number(self,input_path,content):
        """
        def : get_line_number
        purpose : calls the respective method to get the line number where the content is present in
                  given file based on file type
        param : input_path,content
        return : linenumbers [list]

        """
        try:
            status=False
            params=self.__split(input_path,content)
            if self.verify_file_exists(params[0]) == True:
                file_ext,res=self.__get_ext(params[0])
                if res == True:
                    linenumbers= self.dict[file_ext+'_get_line_number'](*params)
                    logger.log(linenumbers)
                    if linenumbers is not None and len(linenumbers) !=0:
                        status=True
        except Exception as e:
            Exceptions.error(e)
        return status

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


