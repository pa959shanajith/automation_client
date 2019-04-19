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

    generic_dict={
        'tolowercase': generic_string.toLowerCase,
        'touppercase' : generic_string.toUpperCase,
        'trim'    : generic_string.trim,
        'left'     : generic_string.left,
        'right'  : generic_string.right,
        'mid' : generic_string.mid,
        'getstringlength'      : generic_string.getStringLength,
        'find'      : generic_string.find,
        'replace':generic_string.replace,
        'split' : generic_string.split,
        'concatenate' : generic_string.concatenate,
        'getsubstring':generic_string.getSubString,
        'stringgeneration':generic_string.stringGeneration,
        'savetoclipboard':generic_string.save_to_clip_board,
        'getfromclipboard':generic_string.get_from_clip_board,
        'getcurrentdate' : generic_date.getCurrentDate,
        'getcurrenttime' : generic_date.getCurrentTime,
        'getcurrentdateandtime': generic_date.getCurrentDateAndTime,
        'getcurrentday' : generic_date.getCurrentDay,
        'getcurrentdaydateandtime' : generic_date.getCurrentDayDateAndTime,
        'datedifference' : generic_date.dateDifference,
        'dateaddition'    : generic_date.dateAddition,
        'monthaddition'  :generic_date.monthAddition,
        'yearaddition' : generic_date.yearAddition,
        'changedateformat'     : generic_date.changeDateFormat,
        'datecompare'  : generic_date.dateCompare,
        'savefile':generic_file.save_file,
        'createfile':generic_file.create_file,
        'renamefile':generic_file.rename_file,
        'deletefile':generic_file.delete_file,
        'verifyfileexists':generic_file.verify_file_exists,
        'createfolder':genric_folder.create_folder,
        'renamefolder':genric_folder.rename_folder,
        'deletefolder':genric_folder.delete_folder,
        'verifyfolderexists':genric_folder.verify_folder_exists,
        'comparecontent':generic_file.compare_content,
        'replacecontent':generic_file.replace_content,
        'verifycontent':generic_file.verify_content,
        'clearfilecontent':generic_file.clear_content,
        'getlinenumber':generic_file.get_line_number,
        'getcontent':generic_file.get_content,
        'writetofile':generic_file.write_to_file,
        'writetocell':generic_excel.write_cell,
        'readcell':generic_excel.read_cell,
        'clearcell':generic_excel.clear_cell,
        'setexcelpath':generic_excel.set_excel_path,
        'storeexcelpath':generic_excel.set_excel_path,
        'clearexcelpath':generic_excel.clear_excel_path,
        'deleterow':generic_excel.delete_row,
        'getrowcount':generic_excel.get_rowcount,
        'getcolumncount':generic_excel.get_colcount,
        'runquery':generic_database.runQuery,
        'securerunquery': generic_database.secureRunQuery,
        'getdata':generic_database.getData,
        'securegetdata': generic_database.secureGetData,
        'exportdata':generic_database.exportData,
        'secureverifydata': generic_database.secureVerifyData,
        'verifydata':generic_database.verifyData,
        'secureexportdata': generic_database.secureExportData,
        'evallogicalexpression':generic_logical.eval_expression,
        'capturescreenshot':generic_screenshot.captureScreenshot,
        'executefile':generic_batch.executeFile,
        'evaluate':generic_math.eval,
        'wait':generic_delay.wait,
        'pause':generic_delay.pause,
        'sendfunctionkeys':generic_sendkeys.sendfunction_keys,
        'getblockcount' : xml_oper.get_block_count,
        'gettagvalue' : xml_oper.get_tag_value,
        'getblockvalue' : xml_oper.get_block_value,
        'verifyobjects': xml_oper.verifyObjects,
        'typecast':util_operation_obj.type_cast,
        'verifyfileimages':util_operation_obj.verify_file_images,
        'imagesimilaritypercentage':util_operation_obj.image_similarity_percentage,
        'stop':util_operation_obj.stop,
        'createdynvariable':dyn_var_obj.create_dynamic_variable,
        'copyvalue':dyn_var_obj.copy_value,
        'modifyvalue':dyn_var_obj.modify_value,
        'deletedynvariable':dyn_var_obj.delete_dyn_value,
        'displayvariablevalue':generic_delay.display_variable_value,
        'verifyvalues':util_operation_obj.verify_values,
        'getindexcount':util_operation_obj.getIndexCount,
        'writewordfile': generic_word.writeWordFile,
        'readworddoc': generic_word.readWorddoc,
        'readallcheckbox': generic_word.readallcheckbox,
        'getalltablesfromdoc': generic_word.getAllTablesFromDoc,
        'readjson': generic_word.readjson,
        'readxml': generic_word.readxml,
        'readpdf': generic_word.readPdf,
        'getkeyvalue': json_oper.get_key_value
    }


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
            if keyword in list(self.generic_dict.keys()):
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
                result= self.generic_dict[keyword](*message)
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
