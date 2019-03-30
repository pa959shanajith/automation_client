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
import word_operations
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
    generic_word=word_operations.WordFile()
    generic_database =database_keywords.DatabaseOperation()
    generic_batch=batch_operation_keyword.BatchOperationKeyword()
    generic_math=math_operation_keywords.NumericStringParser()
    generic_screenshot=screenshot_keywords.Screenshot()
    generic_logical=logical_operation_keywords.logical_eval()
    generic_delay=delay_operations.Delay_keywords()
    generic_sendkeys=sendfunction_keys.SendFunctionKeys()
    xml_oper = xml_operations.XMLOperations()
    json_oper = xml_operations.JSONOperations()
    util_operation_obj=util_operations.UtilOperations()
    dyn_var_obj=dynamic_variable.DynamicVariables()


    def __init__(self):
        self.action=None
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
         keyword=keyword.lower()
         err_msg=None
         result=[constants.TEST_RESULT_FAIL,constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]
         try:
            dict={'tolowercase': self.generic_string.toLowerCase,
                  'touppercase' : self.generic_string.toUpperCase,
                  'trim'    : self.generic_string.trim,
                  'left'     : self.generic_string.left,
                  'right'  : self.generic_string.right,
                  'mid' : self.generic_string.mid,
                  'getstringlength'      : self.generic_string.getStringLength,
                  'find'      : self.generic_string.find,
                  'replace':self.generic_string.replace,
                  'split' : self.generic_string.split,
                  'concatenate' : self.generic_string.concatenate,
                  'getsubstring':self.generic_string.getSubString,
                  'stringgeneration':self.generic_string.stringGeneration,
                  'savetoclipboard':self.generic_string.save_to_clip_board,
                  'getfromclipboard':self.generic_string.get_from_clip_board,
                  'getcurrentdate' : self.generic_date.getCurrentDate,
                  'getcurrenttime' : self.generic_date.getCurrentTime,
                  'getcurrentdateandtime': self.generic_date.getCurrentDateAndTime,
                  'getcurrentday' : self.generic_date.getCurrentDay,
                  'getcurrentdaydateandtime' : self.generic_date.getCurrentDayDateAndTime,
                  'datedifference' : self.generic_date.dateDifference,
                  'dateaddition'    : self.generic_date.dateAddition,
                  'monthaddition'  :self.generic_date.monthAddition,
                  'yearaddition' : self.generic_date.yearAddition,
                  'changedateformat'     : self.generic_date.changeDateFormat,
                  'datecompare'  : self.generic_date.dateCompare,
                  'savefile':self.generic_file.save_file,
                  'createfile':self.generic_file.create_file,
                  'renamefile':self.generic_file.rename_file,
                  'deletefile':self.generic_file.delete_file,
                  'verifyfileexists':self.generic_file.verify_file_exists,
                  'createfolder':self.genric_folder.create_folder,
                  'renamefolder':self.genric_folder.rename_folder,
                  'deletefolder':self.genric_folder.delete_folder,
                  'verifyfolderexists':self.genric_folder.verify_folder_exists,
                  'comparecontent':self.generic_file.compare_content,
                  'replacecontent':self.generic_file.replace_content,
                  'verifycontent':self.generic_file.verify_content,
                  'clearfilecontent':self.generic_file.clear_content,
                  'getlinenumber':self.generic_file.get_line_number,
                  'getcontent':self.generic_file.get_content,
                  'writetofile':self.generic_file.write_to_file,
                  'writetocell':self.generic_excel.write_cell,
                  'readcell':self.generic_excel.read_cell,
                  'clearcell':self.generic_excel.clear_cell,
                  'setexcelpath':self.generic_excel.set_excel_path,
                  'storeexcelpath':self.generic_excel.set_excel_path,
                  'clearexcelpath':self.generic_excel.clear_excel_path,
                  'deleterow':self.generic_excel.delete_row,
                  'getrowcount':self.generic_excel.get_rowcount,
                  'getcolumncount':self.generic_excel.get_colcount,
                  'runquery':self.generic_database.runQuery,
                  'securerunquery': self.generic_database.secureRunQuery,
                  'getdata':self.generic_database.getData,
                  'securegetdata': self.generic_database.secureGetData,
                  'exportdata':self.generic_database.exportData,
                  'secureverifydata': self.generic_database.secureVerifyData,
                  'verifydata':self.generic_database.verifyData,
                  'secureexportdata': self.generic_database.secureExportData,
                  'evallogicalexpression':self.generic_logical.eval_expression,
                  'capturescreenshot':self.generic_screenshot.captureScreenshot,
                  'executefile':self.generic_batch.executeFile,
                  'evaluate':self.generic_math.eval,
                  'wait':self.generic_delay.wait,
                  'pause':self.generic_delay.pause,
                  'sendfunctionkeys':self.generic_sendkeys.sendfunction_keys,
                  'getblockcount' : self.xml_oper.get_block_count,
                  'gettagvalue' : self.xml_oper.get_tag_value,
                  'getblockvalue' : self.xml_oper.get_block_value,
                  'verifyobjects': self.xml_oper.verifyObjects,
                  'typecast':self.util_operation_obj.type_cast,
                  'verifyfileimages':self.util_operation_obj.verify_file_images,
                  'imagesimilaritypercentage':self.util_operation_obj.image_similarity_percentage,
                  'stop':self.util_operation_obj.stop,
                  'createdynvariable':self.dyn_var_obj.create_dynamic_variable,
                  'copyvalue':self.dyn_var_obj.copy_value,
                  'modifyvalue':self.dyn_var_obj.modify_value,
                  'deletedynvariable':self.dyn_var_obj.delete_dyn_value,
                  'displayvariablevalue':self.generic_delay.display_variable_value,
                  'verifyvalues':self.util_operation_obj.verify_values,
                  'getindexcount':self.util_operation_obj.getIndexCount,
                  'writewordfile': self.generic_word.writeWordFile,
                  'readworddoc': self.generic_word.readWorddoc,
                  'readallcheckbox': self.generic_word.readallcheckbox,
                  'getalltablesfromdoc': self.generic_word.getAllTablesFromDoc,
                  'readjson': self.generic_word.readjson,
                  'readxml': self.generic_word.readxml,
                  'readpdf': self.generic_word.readPdf,
                  'getkeyvalue': self.json_oper.get_key_value

                }
            if keyword in list(dict.keys()):
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
                    if ';' in tsp.outputval:
                        output=tsp.outputval.split(';')
                    #Changes for defect #983 - to resolve values of static and dynamic variables in output for this particular keyword
                    if(keyword == "exportdata" and len(output)>1):
                        i = (tsp.outputval).index(';')
                        tsp.outputval = tsp.outputval[i+1:]
                        if str(output[0]).startswith("{") and str(output[0]).endswith("}"):
                            import dynamic_variable_handler
                            import controller
                            con = controller.Controller()
                            dynamic_var_handler_obj=dynamic_variable_handler.DynamicVariables()
                            output[0] = dynamic_var_handler_obj.replace_dynamic_variable(output[0],keyword,con)
                        elif str(output[0]).startswith("|") and str(output[0]).endswith("|"):
                            import handler
                            import controller
                            con = controller.Controller()
                            for test in handler.tspList:
                                if((test.name).lower() == "getparam"):
                                    teststep = test
                                    break
                            rawinput = teststep.inputval
                            inpval,ignore_stat=con.split_input(rawinput,tsp.name)
                            data = teststep.invokegetparam(inpval)
                            var = str(output[0])[1:len(str(output[0]))-1]
                            output[0] = data[var][0]
                    message.extend(output)
                result= dict[keyword](*message)
            else:
                err_msg=generic_constants.INVALID_KEYWORD
                result[3]=err_msg
            if self.action ==constants.EXECUTE and keyword =='capturescreenshot':
                if result != constants.TERMINATE:
                    result=list(result)
                    result.append(result[2])
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
