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

    def __init__(self):
        print 'init'
        self.txt=TextFile()
        self.pdf=PdfFile()
        self.excel=ExcelFile()
        self.xml=XML()
        self.dict={'.txt_write_to_file':self.txt.write_to_file,
              '.xls_write_to_file':self.excel.write_to_file_xls,
              '.xlsx_write_to_file':self.excel.write_to_file_xlsx,
              '.xml_write_to_file':self.xml.write_to_file,

              '.xls_verify_content':self.excel.write_to_file_xls,
              '.xlsx_verify_content':self.excel.write_to_file_xlsx,
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
        try:
            input=input.strip()
            logger.log(generic_constants.INPUT_IS+input)
            if not (input is None and input is ''):
                if os.path.isfile(input):
                    os.remove(input)
                    return True
                else:
                    logger.log(generic_constants.FILE_NOT_EXISTS)
            else:
                logger.log(generic_constants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return False


    def verify_content(self,input_path,content):
        try:
            input_path=input_path.strip()
            status=False
            if self.verify_file_exists(input_path) == True:
                file_ext,status=self.__get_ext(input_path)
                if status == True:
                    status= self.dict[file_ext+'_verify_content'](input_path,content)
                return status
        except Exception as e:
            Exceptions.error(e)
        return False


    def __get_ext(self,input_path):
        try:
            filename,file_ext=os.path.splitext(input_path)
            if file_ext in generic_constants.FILE_TYPES:
                status=True
            else:
                logger.log(generic_constants.INVALID_FILE_FORMAT)
            return file_ext,status
        except Exception as e:
            Exceptions.error(e)
            return '',False

    def compare_content(self,input_path1,input_path2,*args):
        try:
            input_path1=input_path1.strip()
            input_path2=input_path2.strip()
            status=False
            if self.verify_file_exists(input_path1) == True and self.verify_file_exists(input_path2) :
                file_ext1,status1=self.__get_ext(input_path1)
                file_ext2,status2=self.__get_ext(input_path2)
                if status1 == True and status2==True and file_ext1==file_ext2:
                    status=self.dict[file_ext1+'_compare_content'](input_path1,input_path2)
            return status
        except Exception as e:
            Exceptions.error(e)
        return False

    def clear_content(self,input_path):
        try:
            input_path=input_path.strip()
            status=False
            if self.verify_file_exists(input_path) == True:
                file_ext,status=self.__get_ext(input_path)
                if status == True:
                    status=self.dict[file_ext+'_clear_content'](input_path)
            return status
        except Exception as e:
            Exceptions.error(e)
        return False

    def get_content(self,input_path,*args):
        try:
            input_path=input_path.strip()
            status=False
            if self.verify_file_exists(input_path) == True:
                file_ext,status=self.__get_ext(input_path)
                if status == True:
                    status=self.dict[file_ext+'_get_content'](input_path)
            return status
        except Exception as e:
            Exceptions.error(e)
        return False

    def replace_content(self,input_path,existing_content,replace_content):
        try:
            input_path=input_path.strip()
            status=False
            if self.verify_file_exists(input_path) == True:
                file_ext,status=self.__get_ext(input_path)
                if status == True:
                    status=self.dict[file_ext+'_replace_content'](input_path,existing_content,replace_content)
            return status
        except Exception as e:
            Exceptions.error(e)
        return False

    def write_to_file(self,input_path,content):
        try:
            status=False
            input_path=input_path.strip()
            if self.verify_file_exists(input_path) == True:
                file_ext,status=self.__get_ext(input_path)
                if status == True:
                    status= self.dict[file_ext+'_write_to_file'](input_path,content)
            if status == True:
                logger.log('Content matched')
            return status
        except Exception as e:
            Exceptions.error(e)
        return False

    def get_line_number(self,input_path,content):
        try:
            status=False
            input_path=input_path.strip()
            if self.verify_file_exists(input_path) == True:
                file_ext,status=self.__get_ext(input_paths)
                if status == True:
                    linenumbers= self.dict[file_ext+'_get_line_number'](input_path,content)
                    logger.log(linenumbers)
                    return True
        except Exception as e:
            Exceptions.error(e)
        return False




