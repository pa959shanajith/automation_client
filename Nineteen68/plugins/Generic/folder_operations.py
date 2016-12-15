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
import Exceptions
import file_operations
from constants import *


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
        try:
            logger.log(generic_constants.INPUT_IS+inputpath+' folder name '+folder_name)
            if not (inputpath is None and inputpath is '') and self.validateFolderName(inputpath,'path') and self.validateFolderName(folder_name):
                if not os.path.exists(inputpath+'/'+folder_name):
                    os.makedirs(inputpath+'/'+folder_name)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    logger.log(generic_constants.FOLDER_EXISTS)
            else:
                logger.log(generic_constants.INVALID_INPUT)
        except WindowsError as e:
            logger.log("A Folder/File name can't contain any of the following characters "+generic_constants.INVALID_CHARS)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput



    def verify_folder_exists(self,inputpath,folder_name):
        """
        def : verify_folder_exists
        purpose : verifies if the given folder exists
        param : inputpath,folder_name
        return : bool

        """
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            logger.log(generic_constants.INPUT_IS+inputpath+' folder name '+folder_name)
            if not (inputpath is None and inputpath is ''):
                if os.path.exists(inputpath+'/'+folder_name):
                    logger.log(generic_constants.FOLDER_EXISTS)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    logger.log(generic_constants.FOLDER_NOT_EXISTS)
            else:
                logger.log(generic_constants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def rename_folder(self,inputpath,folder_name,rename_folder):
        """
        def : rename_folder
        purpose : renames the 'folder_name' in the 'inputpath' by 'rename_folder'
        param : inputpath,folder_name
        return : bool

        """
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            logger.log(generic_constants.INPUT_IS+inputpath+' folder name '+folder_name+' new folder name '+rename_folder)
            if not (inputpath is None and inputpath is ''):
                old_path=inputpath+'/'+folder_name
                rename_path=inputpath+'/'+rename_folder
                if os.path.exists(old_path):
                    os.renames(old_path,rename_path)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                else:
                    logger.log(generic_constants.FOLDER_NOT_EXISTS)
            else:
                logger.log(generic_constants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput


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
        try:
            logger.log(generic_constants.INPUT_IS+inputpath+' folder name '+folder_name)
            if not (inputpath is None and inputpath is ''):
                try:

                    if os.path.exists(inputpath+'/'+folder_name):
                        if len(args)==1 and int(args[0]) == 1:
                            import shutil
                            shutil.rmtree(inputpath+'/'+folder_name)
                        else:
                            os.rmdir(inputpath+'/'+folder_name)
                        status=TEST_RESULT_PASS
                        methodoutput=TEST_RESULT_TRUE
                    else:
                        logger.log(generic_constants.FOLDER_NOT_EXISTS)
                except ValueError,WindowsError:
                    logger.log(generic_constants.INVALID_INPUT)
            else:
                logger.log(generic_constants.INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

    def validateFolderName(self,name,*args):
        chars = set(generic_constants.INVALID_CHARS)
        if len(args)>0 and args[0]=='path':
            chars=set(generic_constants.INVALID_CHARS_PATH)
        if any((c in chars) for c in name):
            logger.log("A Folder/File name can't contain any of the following characters "+generic_constants.INVALID_CHARS)
            return False
        else:
            return True
