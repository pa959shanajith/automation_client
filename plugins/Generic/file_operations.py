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
from file_comparison_operations import TextFile,PdfFile,XML,JSON
import excel_operations
import core_utils
import urllib.request, urllib.error, urllib.parse
import xml.dom.minidom	
import json	
import difflib	
from xmldiff import main, formatting

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
            ##url_save=None
            ##import browser_Keywords
            ##url_save=browser_Keywords.url_save
            ##print url_save
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
                obj.type(folder_path)
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
                obj.type(file_path)
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

    	#--------------------------------------------------------------------------------File compare	
    def file_get_contents(self,input):	
        if os.path.isfile(input):	
            logger.print_on_console(input, 'This file has been found. ')	
            with file(input) as f:	
                s = f.read()	
            return s	
        else:	
            logger.print_on_console(input, 'This file has not been found. Enter correct path. ')	
            return input	

    def beautify_xml_file(self,input):	
        pretty_xml_as_string = ''	
        flag = False	
        try:	
            if os.path.isfile(input):	
                dom = xml.dom.minidom.parse(input)	
            else:	
                dom = xml.dom.minidom.parseString(input)	
            xml_string = dom.toprettyxml()	
            pretty_xml_as_string = xml_string.replace('<?xml version="1.0" ?>\n','',1)	
            pretty_xml_as_string = os.linesep.join([s for s in pretty_xml_as_string.splitlines() if s.strip()])	
            flag = True	
        except Exception as e:	
            logger.print_on_console('Invalid xml input ')	
            log.error(e)	
        if not (flag):	
            logger.print_on_console('Unable to beautify')	
            # self.file_get_contents(input)	
        return pretty_xml_as_string	

    def beautify_json_file(self,input):	
        pretty_json_as_string = ''	
        flag = False	
        try:	
            if os.path.isfile(input):	
                with open(input, 'r') as handle:	
                    parsed = json.load(handle)	
            else:	
                parsed = json.loads(input)	
            pretty_json_as_string = json.dumps(parsed, indent=4)	
            flag = True	
        except Exception as e:	
            logger.print_on_console('Invalid json input ')	
            log.error(e)	
        if not (flag):	
            logger.print_on_console('Unable to beautify')	
            # self.file_get_contents(input)	
        return pretty_json_as_string	

    def beautify_file(self, input_val, *args):	
        """	
        def : beautify_file	
        purpose : beautifies/pretifies a file/string of type json or xml	
        param : inputpath,file type	
        return : beautified text, bool	
        """	
        status = TEST_RESULT_FAIL	
        result = TEST_RESULT_FALSE	
        err_msg = None	
        value = OUTPUT_CONSTANT	
        beautified_output = None	
        output_path = None
        try:	
            if ( len(input_val) == 2):	
                iv1 = input_val[0]	
                iv2 = input_val[1]
                if ( args[0] ) : 	
                    out_path = args[0].split(";")[0]		
                    if(not out_path.startswith("{")):	
                        output_path = out_path	
                if (str(iv2).lower() == 'json'):	
                    beautified_output = self.beautify_json_file(iv1)	
                elif (str(iv2).lower() == 'xml'):	
                    beautified_output = self.beautify_xml_file(iv1)	
                else:	
                    err_msg = 'File format not supported'	
                if(beautified_output):	
                    flg = True	
                    try:	
                        if(output_path):	
                            if(os.path.isfile(output_path) or os.path.exists(os.path.dirname(output_path))):	
                                with open(output_path,'w') as f:	
                                    f.write(beautified_output)	
                            else:	
                                flg = False	
                                err_msg='Wrong file path entered'	
                    except Exception as ex:	
                        err_msg = ("Exception occurred while writing to output file in beautify_file : "+str(ex))	
                        log.error( err_msg )	
                        logger.print_on_console( "Error occured while writing to output file in Beautify File" )	
                    if(flg):	
                        value = beautified_output	
                        status=TEST_RESULT_PASS	
                        result=TEST_RESULT_TRUE	
            else:	
                err_msg = 'Invalid number of inputs'	
            if ( err_msg != None ):	
                log.error(err_msg)	
                logger.print_on_console(err_msg)	
        except Exception as e:	
            err_msg = ("Exception occurred in beautify_file : "+str(e))	
            log.error( err_msg )	
            logger.print_on_console( "Error occured in Beautify File" )	
        return status, result, value ,err_msg	

    def compare_inputs(self,input_val,*args):	
        """	
        def : compare_inputs	
        purpose : compares two text inputs	
        param : inputtext-1,inputtext-2	
        return : differed text, bool	
        """	
        status = TEST_RESULT_FAIL	
        result = TEST_RESULT_FALSE	
        err_msg = None	
        value = OUTPUT_CONSTANT	
        beautified_output = None	
        res_opt = 'all'		
        output_path = None	
        try:	
            if ( len(input_val) == 2 or len(input_val) == 3):	
                inputtext1 = input_val[0]	
                inputtext2 = input_val[1]	
                if (len(inputtext1)!=0 and len(inputtext2)!=0):	
                    log.info("Comparing texts...")	
                    if ( args[0] ) : 	
                        out_path = args[0].split(";")[0]		
                        if(not out_path.startswith("{")):	
                            output_path = out_path	
                    if ( len(input_val) == 3 and (input_val[2] != None or input_val[2] != '' )) : res_opt = input_val[2].strip().lower()	
                    output_res = self.compare_texts(inputtext1,inputtext2)	
                    if ( output_res ):	
                        flg = True	
                        try:	
                            num_diff,ch_lines = self.get_diff_count(output_res)	
                            if(num_diff):	
                                logger.print_on_console("The number of differences in compare_inputs are: ",num_diff)	
                            if ( res_opt == 'selective' or res_opt == 'all') :		
                                log.info("Result to be displayed is : " + str(res_opt))		
                                logger.print_on_console("Result to be displayed is : " + str(res_opt))		
                                if (res_opt == 'selective') : output_res = ch_lines	
                            output_res = '\n'.join(output_res)	
                            if(output_path):	
                                if(os.path.isfile(output_path) or os.path.exists(os.path.dirname(output_path))):	
                                    with open(output_path,'w') as f:	
                                        f.write(output_res)	
                                else:	
                                    err_msg='Wrong file path entered'	
                                    flg = False	
                        except Exception as ex:	
                            err_msg = ("Exception occurred while writing to output file in compare_inputs : "+str(ex))	
                            log.error( err_msg )	
                            logger.print_on_console( "Error occured while writing to output file in Compare Inputs" )	
                        if(flg):	
                            log.info("Comparision of texts completed")	
                            value = output_res	
                            status = TEST_RESULT_PASS	
                            result = TEST_RESULT_TRUE	
                else:	
                    err_msg = 'Empty inputs'	
            else:	
                err_msg = 'Invalid number of inputs'	
            if ( err_msg != None ):	
                log.error(err_msg)	
                logger.print_on_console(err_msg)	
        except Exception as e:	
            err_msg = ("Exception occurred in compare_inputs while comparing inputs"+str(e))	
            log.error( err_msg )	
            logger.print_on_console( "Error occured in Compare Inputs" )	
        return status, result, value ,err_msg	

    def compare_texts(self,text1,text2):	
        """	
        def : compare_texts	
        purpose : compares both texts line by line	
        param : text1,text2	
        return : list of differences in texts	
        """	
        out = None	
        try:	
            text1_lines = text1.splitlines()	
            text2_lines = text2.splitlines()	
            if(text1_lines==text2_lines):	
                logger.print_on_console( "Inputs are same" )	
                log.info( "Inputs are same" )	
                out = list(difflib.Differ().compare(text1_lines, text2_lines))	
            else:	
                out = list(difflib.Differ().compare(text1_lines, text2_lines))	
        except Exception as e:	
            logger.print_on_console("Exception occurred in compare_texts while comparing two texts")	
            log.error("Exception occurred in compare_texts while comparing two texts"+str(e))	
        return out	

    def compare_xmls(self, xml_input1, xml_input2):	
        """	
        def : compare_xmls	
        purpose : compares two xml files	
        param : inputPath-1,inputPath-2	
        return : differed xml	
        """	
        out = None	
        try:	
            text1_lines = xml_input1.splitlines()	
            text2_lines = xml_input2.splitlines()	
            if(text1_lines==text2_lines):	
                logger.print_on_console( "Inputs are same" )	
                log.info( "Inputs are same" )	
                out = main.diff_files(xml_input1, xml_input2,diff_options={'fast_match': True},formatter=formatting.XMLFormatter(normalize=formatting.WS_BOTH)).split("\n")	
            else:	
                out = main.diff_files(xml_input1, xml_input2,diff_options={'fast_match': True},formatter=formatting.XMLFormatter(normalize=formatting.WS_BOTH)).split("\n")	
        except Exception as e:	
            logger.print_on_console("Exception occurred in compare_xmls while comparing two texts")	
            log.error("Exception occurred in compare_xmls while comparing two texts"+str(e))	
        return out	

    def compare_files(self,input_val,*args):	
        """	
        def : compare_file	
        purpose : compares two files	
        param : inputPath-1,inputPath-2	
        return : differed text, bool	
        """	
        status = TEST_RESULT_FAIL	
        result = TEST_RESULT_FALSE	
        err_msg = None	
        value = OUTPUT_CONSTANT	
        res_opt = 'all'		
        output_path = None	
        try:	
            if ( len(input_val) == 2 or len(input_val) == 3):	
                filePathA = input_val[0]	
                filePathB = input_val[1]	
                if ( args[0] ) : 	
                    out_path = args[0].split(";")[0]		
                    if(not out_path.startswith("{")):	
                        output_path = out_path		
                if ( len(input_val) == 3 and (input_val[2] != None or input_val[2] != '' )) : res_opt = input_val[2].strip().lower()	
                if ( os.path.isfile(filePathA) and os.path.isfile(filePathB) ):	
                    if( os.path.getsize(filePathA)>0 and os.path.getsize(filePathB)>0):	
                        fileNameA, fileExtensionA = os.path.splitext(filePathA)	
                        fileNameB, fileExtensionB = os.path.splitext(filePathB)	
                        log.info("Comparing files...")	
                        with open(filePathA) as fa, open(filePathB) as fb:	
                            file1_lines=fa.read()	
                            file2_lines=fb.read()	
                        if(fileExtensionA == '.xml' and fileExtensionB == '.xml'):	
                            output_res = self.compare_xmls(filePathA,filePathB)	
                            if(output_res):	
                                num_diff,ch_lines = self.get_diff_count_xml(output_res)	
                        else:	
                            output_res = self.compare_texts(file1_lines,file2_lines)	
                            if(output_res):	
                                num_diff,ch_lines = self.get_diff_count(output_res)		
                                	
                        if ( output_res ):	
                            flg = True	
                            try:	
                                if ( res_opt == 'selective' or res_opt == 'all') :		
                                    log.info("Result to be displayed is : " + str(res_opt))		
                                    logger.print_on_console("Result to be displayed is : " + str(res_opt))		
                                    if (res_opt == 'selective') : output_res = ch_lines	
                                output_res = '\n'.join(output_res)	
                                if(num_diff):	
                                    logger.print_on_console("The number of differences in compare_file are: ",num_diff)	
                                if(output_path):	
                                    if(os.path.exists(output_path) or os.path.exists(os.path.dirname(output_path))):	
                                        with open(output_path,'w') as f:	
                                            f.write(output_res)	
                                    else:	
                                        err_msg='Wrong file path entered'	
                                        flg = False	
                            except Exception as ex:	
                                err_msg = ("Exception occurred while writing to output file in compare_file : "+str(ex))	
                                log.error( err_msg )	
                                logger.print_on_console( "Error occured while writing to output file in Compare File" )	
                            if(flg):	
                                log.info("Comparision of files completed")	
                                value = output_res	
                                status = TEST_RESULT_PASS	
                                result = TEST_RESULT_TRUE	
                    else:	
                        err_msg = 'One or more files are empty'	
                else:	
                    err_msg = 'Invalid file paths'	
            else:	
                err_msg = 'Invalid number of inputs'	
            if ( err_msg != None ):	
                log.error(err_msg)	
                logger.print_on_console(err_msg)	
        except Exception as e:	
            err_msg = ("Exception occurred in compare_files while comparing two files"+str(e))	
            log.error( err_msg )	
            logger.print_on_console( "Error occured in Compare Files" )	
        return status, result, value ,err_msg	

    def get_diff_count(self,output_response):	
        """	
        def : get_diff_count	
        purpose : counts number of differences between inputs	
        param : difference of inputs	
        return : count of differences	
        """	
        num_que = 0	
        num_diff = 0	
        prev_sign = ''	
        ch_lines = []	
        for line in output_response:	
            if(prev_sign=='+' and (not line.startswith('?')) and num_que==1):	
                num_diff-=1	
                num_que=0	
            elif(line.startswith(('-','+'))):	
                num_diff+=1	
                ch_lines.append(line)	
                prev_sign=line[0]	
            elif(line.startswith('?')):	
                ch_lines.append(line)	
                if(prev_sign=='-'):	
                    num_que+=1	
                elif(prev_sign=='+'):	
                    num_diff-=1	
                    num_que=0  	
                prev_sign='?'                  	
        return num_diff,ch_lines	

    def get_diff_count_xml(self,output_response):	
        """	
        def : get_diff_count_xml	
        purpose : counts number of differences between xml inputs	
        param : difference of inputs	
        return : count of differences	
        """	
        ch_lines = []	
        num_diff = int(str(output_response).count("diff:"))-int(str(output_response).count("/diff:"))
        for line in output_response:	
            if(line.find("diff:") != -1):	
                ch_lines.append(line)	
        return num_diff,ch_lines	
#--------------------------------------------------------------------------------File compare


