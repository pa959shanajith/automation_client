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

class FolderOperations:

    def create_folder(self,input):
        """
        def : create_folder
        purpose : creates the all the intermediate folders in the given path
        param : input
        return : bool

        """
        try:
            logger.log(generic_constants.INPUT_IS+input)
            if not (input is None and input is ''):
                if not os.path.exists(input):
                    os.makedirs(input)
                    return True
                else:
                    logger.log(generic_constants.FILE_EXISTS)
                    return False

            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False



    def verify_folder_exists(self,input):
        """
        def : verify_folder_exists
        purpose : verifies if the given folder exists
        param : input
        return : bool

        """
        try:
            logger.log(generic_constants.INPUT_IS+input)
            if not (input is None and input is ''):
                if os.path.exists(input):
                    logger.log(generic_constants.FILE_EXISTS)
                    return True
                else:
                    logger.log(generic_constants.FILE_NOT_EXISTS)
            else:
                logger.log(generic_constants.INVALID_INPUT)
            return False
        except Exception as e:
            Exceptions.error(e)
            return False

    def rename_folder(self,actualpath,renamepath):
        """
        def : rename_folder
        purpose : renames the folder in the 'actualpath' by 'renamepath'
        param : actualpath,renamepath
        return : bool

        """
        try:
            logger.log(generic_constants.INPUT_IS+actualpath)
            if not (actualpath is None and actualpath is ''):
                if os.path.exists(actualpath):
                    os.renames(actualpath,renamepath)
                    return True
                else:
                    logger.log(generic_constants.FILE_NOT_EXISTS)
                    return False

            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False


    def delete_folder(self,input):
        """
        def : delete_folder
        purpose : deletes / force deletes the given folder based on the argument
                  optional argument '1' which indicates 'force_delete'
        param : input,force_delete
        return : bool

        """
        try:
            logger.log(generic_constants.INPUT_IS+input)
            if not (input is None and input is ''):
                try:

                    if os.path.exists(input):
                        if len(args)==1 and args[0] == 1:
                            import shutil
                            shutil.rmtree(input)
                        else:
                            os.rmdir(input)
                        return True
                    else:
                        logger.log(generic_constants.FILE_NOT_EXISTS)
                        return False
                except ValueError,WindowsError:
                    Exception.message('Error occured')

            else:
                logger.log(generic_constants.INVALID_INPUT)
                return False
        except Exception as e:
            Exceptions.error(e)
            return False

