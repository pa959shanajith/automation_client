#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     03-10-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import date_ops_keywords
import string_ops_keywords
import file_operations
import folder_operations
import logger
import generic_constants
import Exceptions
import excel_operations
import database_keywords
import math_operation_keywords
import screenshot_keywords
import logical_operation_keywords
import batch_operation_keyword
import delay_operations
import sendfunction_keys

class GenericKeywordDispatcher:
    generic_date = date_ops_keywords.DateOperation()
    generic_string =string_ops_keywords.StringOperation()
    generic_file=file_operations.FileOperations()
    genric_folder=folder_operations.FolderOperations()
    generic_excel=excel_operations.ExcelFile()
    generic_database =database_keywords.DatabaseOperation()
    generic_batch=batch_operation_keyword.BatchOperationKeyword()
    generic_math=math_operation_keywords.NumericStringParser()
    generic_screenshot=screenshot_keywords.Screenshot()
    generic_logical=logical_operation_keywords.logical_eval()
    generic_delay=delay_operations.Delay_keywords()
    generic_sendkeys=sendfunction_keys.SendFunctionKeys()
    def dispatcher(self,keyword,*message):
         logger.log('Keyword is '+keyword)
         try:
            dict={'toLowerCase': self.generic_string.toLowerCase,
                  'toUpperCase' : self.generic_string.toUpperCase,
                  'trim'    : self.generic_string.trim,
                  'left'     : self.generic_string.left,
                  'right'  : self.generic_string.right,
                  'mid' : self.generic_string.mid,
                  'getStringLength'      : self.generic_string.getStringLength,
                  'find'      : self.generic_string.find,
                  'replace':self.generic_string.replace,
                  'split' : self.generic_string.split,
                  'concatenate' : self.generic_string.concatenate,
                  'getSubString':self.generic_string.getSubString,
                  'stringGeneration':self.generic_string.stringGeneration,
                  'getCurrentDate' : self.generic_date.getCurrentDate,
                  'getCurrentTime' : self.generic_date.getCurrentTime,
                  'getCurrentDateAndTime': self.generic_date.getCurrentDateAndTime,
                  'dateDifference' : self.generic_date.dateDifference,
                  'dateAddition'    : self.generic_date.dateAddition,
                  'changeDateFormat'     : self.generic_date.changeDateFormat,
                  'dateCompare'  : self.generic_date.dateCompare,
                  'createFile':self.generic_file.create_file,
                  'renameFile':self.generic_file.rename_file,
                  'deleteFile':self.generic_file.delete_file,
                  'verifyFileExists':self.generic_file.verify_file_exists,
                  'createFolder':self.genric_folder.create_folder,
                  'renameFolder':self.genric_folder.rename_folder,
                  'deleteFolder':self.genric_folder.delete_folder,
                  'verifyFolderExists':self.genric_folder.verify_folder_exists,
                  'compareContent':self.generic_file.compare_content,
                  'replaceContent':self.generic_file.replace_content,
                  'verifyContent':self.generic_file.verify_content,
                  'clearFileContent':self.generic_file.clear_content,
                  'getLineNumber':self.generic_file.get_line_number,
                  'getContent':self.generic_file.get_content,
                  'writeToFile':self.generic_file.write_to_file,
                  'writeToCell':self.generic_excel.write_cell,
                  'readCell':self.generic_excel.read_cell,
                  'clearCell':self.generic_excel.clear_cell,
                  'setExcelPath':self.generic_excel.set_excel_path,
                  'clearExcelPath':self.generic_excel.clear_excel_path,
                  'deleteRow':self.generic_excel.delete_row,
                  'getRowCount':self.generic_excel.get_rowcount,
                  'getColumnCount':self.generic_excel.get_colcount,
                  'runQuery':self.generic_database.runQuery,
                  'getData':self.generic_database.getData,
                  'exportData':self.generic_database.exportData,
                  'verifyData':self.generic_database.verifyData,
                  'evalLogicalExpression':self.generic_logical.eval_expression,
                  'captureScreenshot':self.generic_screenshot.captureScreenshot,
                  'executeFile':self.generic_batch.executeFile,
                  'evaluate':self.generic_math.eval,
                  'wait':self.generic_delay.wait,
                  'pause':self.generic_delay.pause,
                  'sendFunctionKeys':self.generic_sendkeys.sendfunction_keys
                }
            if keyword in dict.keys():
                return dict[keyword](*message)
            else:
                logger.log(generic_constants.INVALID_INPUT)
         except Exception as e:
            Exceptions.error(e)
