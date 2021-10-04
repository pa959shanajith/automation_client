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
import file_operations_pdf
import file_operations_xml
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
import constant_variable
import constants
import logging
import threading
local_generic = threading.local()

class GenericKeywordDispatcher:
    def __init__(self):
        self.action=None
        local_generic.generic_date = date_ops_keywords.DateOperation()
        local_generic.generic_string =string_ops_keywords.StringOperation()
        local_generic.generic_file=file_operations.FileOperations()
        local_generic.generic_file_pdf=file_operations_pdf.FileOperationsPDF()
        local_generic.generic_file_xml=file_operations_xml.FileOperationsXml()
        local_generic.genric_folder=folder_operations.FolderOperations()
        local_generic.generic_excel=excel_operations.ExcelFile()
        local_generic.generic_word=word_operations.WordFile()
        local_generic.generic_database =database_keywords.DatabaseOperation()
        local_generic.generic_batch=batch_operation_keyword.BatchOperationKeyword()
        local_generic.generic_math=math_operation_keywords.NumericStringParser()
        local_generic.generic_screenshot=screenshot_keywords.Screenshot()
        local_generic.generic_logical=logical_operation_keywords.logical_eval()
        local_generic.generic_delay=delay_operations.Delay_keywords()
        local_generic.generic_sendkeys=sendfunction_keys.SendFunctionKeys()
        local_generic.xml_oper = xml_operations.XMLOperations()
        local_generic.json_oper = xml_operations.JSONOperations()
        local_generic.util_operation_obj=util_operations.UtilOperations()
        local_generic.dyn_var_obj=dynamic_variable.DynamicVariables()
        local_generic.const_var_obj=constant_variable.ConstantVariables()
        local_generic.log = logging.getLogger("generic_dispatcher.py")
        self.generic_dict={
            'tolowercase': local_generic.generic_string.toLowerCase,
            'touppercase' : local_generic.generic_string.toUpperCase,
            'trim'    : local_generic.generic_string.trim,
            'left'     : local_generic.generic_string.left,
            'right'  : local_generic.generic_string.right,
            'mid' : local_generic.generic_string.mid,
            'getstringlength'      : local_generic.generic_string.getStringLength,
            'find'      : local_generic.generic_string.find,
            'replace':local_generic.generic_string.replace,
            'split' : local_generic.generic_string.split,
            'concatenate' : local_generic.generic_string.concatenate,
            'getsubstring':local_generic.generic_string.getSubString,
            'stringgeneration':local_generic.generic_string.stringGeneration,
            'savetoclipboard':local_generic.generic_string.save_to_clip_board,
            'getfromclipboard':local_generic.generic_string.get_from_clip_board,
            'getcurrentdate' : local_generic.generic_date.getCurrentDate,
            'getcurrenttime' : local_generic.generic_date.getCurrentTime,
            'getcurrentdateandtime': local_generic.generic_date.getCurrentDateAndTime,
            'getcurrentday' : local_generic.generic_date.getCurrentDay,
            'getcurrentdaydateandtime' : local_generic.generic_date.getCurrentDayDateAndTime,
            'datedifference' : local_generic.generic_date.dateDifference,
            'dateaddition'    : local_generic.generic_date.dateAddition,
            'monthaddition'  :local_generic.generic_date.monthAddition,
            'yearaddition' : local_generic.generic_date.yearAddition,
            'changedateformat'     : local_generic.generic_date.changeDateFormat,
            'datecompare'  : local_generic.generic_date.dateCompare,
            'savefile':local_generic.generic_file.save_file,
            'createfile':local_generic.generic_file.create_file,
            'renamefile':local_generic.generic_file.rename_file,
            'deletefile':local_generic.generic_file.delete_file,
            'verifyfileexists':local_generic.generic_file.verify_file_exists,
            'copyfilefolder':local_generic.generic_file.copyFileFolder,
            'movefilefolder':local_generic.generic_file.moveFileFolder,
            'createfolder':local_generic.genric_folder.create_folder,
            'renamefolder':local_generic.genric_folder.rename_folder,
            'deletefolder':local_generic.genric_folder.delete_folder,
            'verifyfolderexists':local_generic.genric_folder.verify_folder_exists,
            'comparecontent':local_generic.generic_file.compare_content,
            'comparepdfs':local_generic.generic_file_pdf.compare_content,
            'findimageinpdf':local_generic.generic_file_pdf.locate_image,
            'comparejsoncontent':local_generic.generic_file.json_compare_content,
            'replacecontent':local_generic.generic_file.replace_content,
            'verifycontent':local_generic.generic_file.verify_content,
            'clearfilecontent':local_generic.generic_file.clear_content,
            'getlinenumber':local_generic.generic_file.get_line_number,
            'getcontent':local_generic.generic_file.get_content,
            'writetofile':local_generic.generic_file.write_to_file,
            'writetocell':local_generic.generic_excel.write_cell,
            'readcell':local_generic.generic_excel.read_cell,
            'clearcell':local_generic.generic_excel.clear_cell,
            'setexcelpath':local_generic.generic_excel.set_excel_path,
            'storeexcelpath':local_generic.generic_excel.set_excel_path,
            'clearexcelpath':local_generic.generic_excel.clear_excel_path,
            'deleterow':local_generic.generic_excel.delete_row,
            'getrowcount':local_generic.generic_excel.get_rowcount,
            'getcolumncount':local_generic.generic_excel.get_colcount,
            'runquery':local_generic.generic_database.runQuery,
            'securerunquery': local_generic.generic_database.secureRunQuery,
            'getdata':local_generic.generic_database.getData,
            'securegetdata': local_generic.generic_database.secureGetData,
            'exportdata':local_generic.generic_database.exportData,
            'secureverifydata': local_generic.generic_database.secureVerifyData,
            'verifydata':local_generic.generic_database.verifyData,
            'secureexportdata': local_generic.generic_database.secureExportData,
            'evallogicalexpression':local_generic.generic_logical.eval_expression,
            'capturescreenshot':local_generic.generic_screenshot.captureScreenshot,
            'executefile':local_generic.generic_batch.executeFile,
            'evaluate':local_generic.generic_math.eval,
            'wait':local_generic.generic_delay.wait,
            'pause':local_generic.generic_delay.pause,
            'sendfunctionkeys':local_generic.generic_sendkeys.sendfunction_keys,
            'sendsecurefunctionkeys':local_generic.generic_sendkeys.sendsecurefunction_keys,
            'getblockcount' : local_generic.xml_oper.get_block_count,
            'gettagvalue' : local_generic.xml_oper.get_tag_value,
            'getblockvalue' : local_generic.xml_oper.get_block_value,
            'verifyobjects': local_generic.xml_oper.verifyObjects,
            'typecast':local_generic.util_operation_obj.type_cast,
            'verifyfileimages':local_generic.util_operation_obj.verify_file_images,
            'imagesimilaritypercentage':local_generic.util_operation_obj.image_similarity_percentage,
            'stop':local_generic.util_operation_obj.stop,
            'createdynvariable':local_generic.dyn_var_obj.create_dynamic_variable,
            'copyvalue':local_generic.dyn_var_obj.copy_value,
            'modifyvalue':local_generic.dyn_var_obj.modify_value,
            'deletedynvariable':local_generic.dyn_var_obj.delete_dyn_value,
            'displayvariablevalue':local_generic.generic_delay.display_variable_value,
            'nullcheck':local_generic.util_operation_obj.nullCheck,
            'verifyvalues':local_generic.util_operation_obj.verify_values,
            'getindexcount':local_generic.util_operation_obj.getIndexCount,
            'disableanchoriris':local_generic.util_operation_obj.disableAnchorIris,
            'getkeystatus':local_generic.util_operation_obj.getKeyStatus,
            'writewordfile': local_generic.generic_word.writeWordFile,
            'readworddoc': local_generic.generic_word.readWorddoc,
            'readallcheckbox': local_generic.generic_word.readallcheckbox,
            'getalltablesfromdoc': local_generic.generic_word.getAllTablesFromDoc,
            'readjson': local_generic.generic_word.readjson,
            'readxml': local_generic.generic_word.readxml,
            'readpdf': local_generic.generic_word.readPdf,
            'getkeyvalue': local_generic.json_oper.get_key_value,
            'setkeyvalue': local_generic.json_oper.set_key_value,
            'comparefiles': local_generic.generic_file_xml.compare_files,
            'beautify': local_generic.generic_file_xml.beautify_file,
            'compareinputs': local_generic.generic_file_xml.compare_inputs,
            'getxmlblockdata' :local_generic.generic_file_xml.getXmlBlockData,
            'selectivexmlfilecompare' : local_generic.generic_file_xml.selectiveXmlFileCompare,
            'compxmlfilewithxmlblock' : local_generic.generic_file_xml.compXmlFileWithXmlBlock,
            'cellbycellcompare': local_generic.generic_file.cell_by_cell_compare,
            'findfilepath': local_generic.generic_file.find_file_path,
            'selectivecellcompare': local_generic.generic_file.selective_cell_compare,
            'createconstvariable':local_generic.const_var_obj.create_constant_variable,
            'deleteconstvariable':local_generic.const_var_obj.delete_const_variable
            }
	#Call to fetch data in database keywords
    def fetch_data(self,input):
        output=None
        try:
            output=local_generic.generic_database.fetchData(input)
        except Exception as e:
            local_generic.log.error(e)
        return output

    def dispatcher(self,tsp,wxObject,mythread,*message):
         keyword=tsp.name
         logger.print_on_console('Keyword is '+keyword)
         keyword=keyword.lower()
         err_msg=None
         dataflag=False                  #flag for database operation keyword to resolve invalid input issue
         result=[constants.TEST_RESULT_FAIL,constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]
         try:
            if keyword in list(self.generic_dict.keys()):
                if keyword in [generic_constants.DISPLAY_VARIABLE_VALUE,generic_constants.SENDFUNCTIONKEYS,generic_constants.PAUSE]:
                    actual_input=tsp.inputval[0].split(';')
                    message=list(message)
                    if keyword != generic_constants.SENDFUNCTIONKEYS:
                        message.append(';')
                    message.extend(actual_input)
                    if keyword == generic_constants.DISPLAY_VARIABLE_VALUE or keyword == generic_constants.PAUSE:
                        message.append(wxObject)
                        message.append(mythread)
                elif keyword in generic_constants.DATA_BASE_KEYWORDS:
                    message=list(message)
                    output=[tsp.outputval]
                    if ';' in tsp.outputval:
                        output=tsp.outputval.split(';')
                    # if(keyword == "exportdata" or keyword=="secureexportdata" or keyword == "getdata" or keyword=="securegetdata") and len(message)>7:
                    #     dataflag=True
                    #Changes for defect #983 - to resolve values of static and dynamic variables in output for this particular keyword
                    if(keyword == "exportdata" or keyword=="secureexportdata") and (len(output)>1):
                        #comment the below code for Azure Issue #22199
                        '''
                        if tsp.outputval.find(';')!=-1:
                            i = (tsp.outputval).index(';')
                            tsp.outputval = tsp.outputval[i+1:]
                        if str(output[0]).startswith("{") and str(output[0]).endswith("}"):
                            import dynamic_variable_handler
                            import controller
                            con = controller.Controller()
                            dynamic_var_handler_obj=dynamic_variable_handler.DynamicVariables()
                            output[0] = dynamic_var_handler_obj.replace_dynamic_variable(output[0],keyword,con)
                        '''
                        if str(output[0]).startswith("|") and str(output[0]).endswith("|"):
                            import handler
                            import controller
                            con = controller.Controller()
                            for test in handler.local_handler.tspList:
                                if((test.name).lower() == "getparam"):
                                    teststep = test
                                    break
                            rawinput = teststep.inputval
                            inpval,ignore_stat=con.split_input(rawinput,tsp.name)
                            data = teststep.invokegetparam(inpval)
                            var = str(output[0])[1:len(str(output[0]))-1]
                            output[0] = data[var][0]
                    message.extend(output)
                if( keyword in ['exportdata','comparefiles',"comparepdfs","findimageinpdf",'beautify','compareinputs','getxmlblockdata','selectivexmlfilecompare','compxmlfilewithxmlblock','cellbycellcompare','findfilepath','selectivecellcompare'] ):
                    input = list(message)
                    output = tsp.outputval
                    if (str(output)==''):
                        output=output
                    if str(output).startswith("|") and str(output).endswith("|"):
                        if ';' in output:
                            # 2 static variables being passed
                            output = output.split(';')
                            # perform parsing of the first static variable
                            output[0] =  local_generic.util_operation_obj.staticFetch(tsp.index, output[0])
                            output = ';'.join(output)
                        else:
                            # only single variable being passed
                            output = local_generic.util_operation_obj.staticFetch(tsp.index,output)
                    result= self.generic_dict[keyword](input,output)
                elif(keyword =='capturescreenshot'):
                    screenshot_data={}
                    message = list(message)
                    if(len(message)>1):
                        screenshot_data['inputs'] = message
                    elif(len(message)==1 and message[0]!=''):
                        message.append('')
                        screenshot_data['inputs'] = message
                    else:
                        screenshot_data['inputs'] = ''
                    if(mythread.action == 'execute'):
                        screen_data = mythread.json_data['suitedetails'][0]
                        screenshot_data['screen_data'] = screen_data
                    screenshot_data['action'] = mythread.action
                    result= self.generic_dict[keyword](screenshot_data)
                elif(dataflag):
                    err_msg=generic_constants.INVALID_INPUT
                    result[3]=err_msg
                else:
                    result= self.generic_dict[keyword](*message)
            else:
                err_msg=generic_constants.INVALID_KEYWORD
                result[3]=err_msg
            if self.action ==constants.EXECUTE and keyword =='capturescreenshot':
                if result != constants.TERMINATE:
                    result=list(result)
                    result.append(result[2])
         except TypeError as e:
            err_msg = constants.ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            local_generic.log.error(e, exc_info=True)
            result[3]=err_msg
            result[2]=None
         except Exception as e:
            local_generic.log.error(e)
         if err_msg!=None:
            local_generic.log.error(err_msg)
            logger.print_on_console(err_msg)
         return result
