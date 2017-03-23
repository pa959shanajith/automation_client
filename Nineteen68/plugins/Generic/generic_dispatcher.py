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
import excel_operations
import database_keywords
import math_operation_keywords
import screenshot_keywords
import logical_operation_keywords
import batch_operation_keyword
import delay_operations
import sendfunction_keys
import xml_operations
import util_operations
import dynamic_variable
import constants
import logging
log = logging.getLogger("generic_dispatcher.py")

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
    xml_oper = xml_operations.XMLOperations()
    util_operation_obj=util_operations.UtilOperations()
    dyn_var_obj=dynamic_variable.DynamicVariables()

	#Call to fetch data in database keywords
    def fetch_data(self,input):
        output=None
        try:
            output=self.generic_database.fetchData(input)
        except Exception as e:
            log.error(e)
        return output

    def dispatcher(self,tsp,wxObject,mythread,*message):
         keyword=tsp.name
         logger.print_on_console('Keyword is '+keyword)
         err_msg=None
         result=[constants.TEST_RESULT_FAIL,constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]
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
                  'saveFile':self.generic_file.save_file,
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
                  'storeExcelPath':self.generic_excel.set_excel_path,
                  'clearExcelPath':self.generic_excel.clear_excel_path,
                  'deleteRow':self.generic_excel.delete_row,
                  'getRowCount':self.generic_excel.get_rowcount,
                  'getColumnCount':self.generic_excel.get_colcount,
                  'runQuery':self.generic_database.runQuery,
                  'secureRunQuery': self.generic_database.secureRunQuery,
                  'getData':self.generic_database.getData,
                  'secureGetData': self.generic_database.secureGetData,
                  'exportData':self.generic_database.exportData,
                  'secureVerifyData': self.generic_database.secureVerifyData,
                  'verifyData':self.generic_database.verifyData,
                  'secureExportData': self.generic_database.secureExportData,
                  'evalLogicalExpression':self.generic_logical.eval_expression,
                  'captureScreenshot':self.generic_screenshot.captureScreenshot,
                  'executeFile':self.generic_batch.executeFile,
                  'evaluate':self.generic_math.eval,
                  'wait':self.generic_delay.wait,
                  'pause':self.generic_delay.pause,
                  'sendFunctionKeys':self.generic_sendkeys.sendfunction_keys,
                  'getBlockCount' : self.xml_oper.get_block_count,
                  'getTagValue' : self.xml_oper.get_tag_value,
                  'GetBlockValue' : self.xml_oper.get_block_value,
                  'VerifyObjects': self.xml_oper.verifyObjects,
                  'typeCast':self.util_operation_obj.type_cast,
                  'verifyFileImages':self.util_operation_obj.verify_file_images,
                  'stop':self.util_operation_obj.stop,
                  'createDynVariable':self.dyn_var_obj.create_dynamic_variable,
                  'copyValue':self.dyn_var_obj.copy_value,
                  'modifyValue':self.dyn_var_obj.modify_value,
                  'deleteDynVariable':self.dyn_var_obj.delete_dyn_value,
                  'displayVariableValue':self.generic_delay.display_variable_value,
                  'VerifyValues':self.util_operation_obj.verify_values


                }
            if keyword in dict.keys():
                if keyword in [generic_constants.DISPLAY_VARIABLE_VALUE,generic_constants.SENDFUNCTIONKEYS,generic_constants.PAUSE]:
                    actual_input=tsp.inputval[0].split(';')
                    message=list(message)
                    if keyword != generic_constants.SENDFUNCTIONKEYS:
                        message.append(';')
                    message.extend(actual_input)
                    if keyword ==generic_constants.DISPLAY_VARIABLE_VALUE or keyword == generic_constants.PAUSE:
                        message.append(wxObject)
                        message.append(mythread)
                elif keyword in generic_constants.DATA_BASE_KEYWORDS:
                    message=list(message)
                    output=[tsp.outputval]
                    message.extend(output)
                result= dict[keyword](*message)
            else:
                err_msg=generic_constants.INVALID_KEYWORD
                result[3]=err_msg
         except TypeError as e:
            err_msg=constants.ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result[3]=err_msg
         except Exception as e:
            log.error(e)
##            logger.print_on_console('Exception at dispatcher')
         if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
         return result
