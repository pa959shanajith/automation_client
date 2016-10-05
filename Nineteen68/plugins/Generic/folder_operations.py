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


    def delete_folder(self,input,force_delete):
        try:
            logger.log(generic_constants.INPUT_IS+input)
            if not (input is None and input is ''):
                try:

                    if os.path.exists(input):
                        if force_delete==1:
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




##obj=FolderOperations()
##input1='D:\\1968-2.0\\nineteen68\\Nineteen68\\plugins\\Generic\\file_operationsNEW.txt'
##delete='D:\\1968-2.0\\Nineteen68\\Nineteen68\\plugins\\Generic\\delete'
####input2='D:\\1968-2.0\\nineteen68\\Nineteen68\\plugins\\Generic\\hi.txt'
####obj.create_file(input1)
##obj.verify_folder_exists(delete)
####obj.rename_file(input1,input2)
####obj.verify_file_exists(input2)
##obj.delete_folder(delete)




