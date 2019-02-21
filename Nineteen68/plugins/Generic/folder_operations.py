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

import file_operations
import logging

from constants import *
log = logging.getLogger('folder_operations.py')


class FolderOperations:

    def create_folder(self,inputpath,folder_name):
        """
        def : create_folder
        purpose : creates the all the intermediate folders in the given path
        param : inputpath,folder_name
        return : bool

        """
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg=None
        try:
            logger.print_on_console(generic_constants.INPUT_IS+inputpath+' folder name '+folder_name)
            if not (inputpath is None and inputpath is '') and self.validateFolderName(inputpath,'path') and self.validateFolderName(folder_name):
                if not os.path.exists(inputpath+os.sep+folder_name):
                    os.makedirs(inputpath+os.sep+folder_name)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=generic_constants.FOLDER_EXISTS
            else:
                err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except WindowsError as e:
            err_msg="A Folder/File name can't contain any of the following characters "+generic_constants.INVALID_CHARS
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Creating '+generic_constants.ERR_MSG3
            log.error(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,methodoutput,output,err_msg


    def verify_folder_exists(self,inputpath,folder_name):
        """
        def : verify_folder_exists
        purpose : verifies if the given folder exists
        param : inputpath,folder_name
        return : bool

        """
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg=None
        try:
            logger.print_on_console(generic_constants.INPUT_IS+inputpath+' folder name '+folder_name)
            if not (inputpath is None and inputpath is ''):
                if os.path.exists(inputpath+os.sep+folder_name):
                    logger.print_on_console(generic_constants.FOLDER_EXISTS)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=generic_constants.FOLDER_NOT_EXISTS
            else:
                err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except WindowsError as e:
            err_msg=ERROR_CODE_DICT['ERR_FOLDER_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Verifying '+generic_constants.ERR_MSG3
            log.error(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,methodoutput,output,err_msg


    def rename_folder(self,inputpath,folder_name,rename_folder):
        """
        def : rename_folder
        purpose : renames the 'folder_name' in the 'inputpath' by 'rename_folder'
        param : inputpath,folder_name
        return : bool

        """
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg=None
        try:
            logger.print_on_console(generic_constants.INPUT_IS+inputpath+' folder name '+folder_name+' new folder name '+rename_folder)
            if not (inputpath is None and inputpath is ''):
                old_path=inputpath+os.sep+folder_name
                rename_path=inputpath+os.sep+rename_folder
                if os.path.exists(old_path):
                    os.renames(old_path,rename_path)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    err_msg=generic_constants.FOLDER_NOT_EXISTS
            else:
                err_msg=ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except WindowsError as e:
            err_msg=ERROR_CODE_DICT['ERR_FOLDER_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Renaming '+generic_constants.ERR_MSG3
            log.error(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,methodoutput,output,err_msg


    def delete_folder(self,inputpath,folder_name,*args):
        """
        def : delete_folder
        purpose : deletes / force deletes the given folder based on the argument
                  optional argument '1' which indicates 'force_delete'
        param : inputpath,folder_name
        return : bool

        """
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg=None
        try:
            logger.print_on_console(generic_constants.INPUT_IS+inputpath+' folder name '+folder_name)
            if not (inputpath is None and inputpath is ''):
                try:
                    if os.path.exists(inputpath+os.sep+folder_name):
                        if len(args)==1 and int(args[0]) == 1:
                            import shutil
                            shutil.rmtree(inputpath+os.sep+folder_name)
                        else:
                            os.rmdir(inputpath+os.sep+folder_name)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        err_msg=generic_constants.FOLDER_NOT_EXISTS
                except (ValueError,WindowsError) as e:
                    log.error(e)
                    err_msg=ERROR_CODE_DICT['ERR_FOLDER_NOT_ACESSIBLE']
            else:
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Deleting '+generic_constants.ERR_MSG3
            log.error(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
            log.error(err_msg)
        return status,methodoutput,output,err_msg

    def validateFolderName(self,name,*args):
        chars = set(generic_constants.INVALID_CHARS)
        if len(args)>0 and args[0]=='path':
            chars=set(generic_constants.INVALID_CHARS_PATH)
        if any((c in chars) for c in name):
            logger.print_on_console("A Folder/File name can't contain any of the following characters "+generic_constants.INVALID_CHARS)
            return False
        else:
            return True
