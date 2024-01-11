#-------------------------------------------------------------------------------
# Name:        file_operations_xml
# Purpose:     comparison between two xml data, in respective functions
#
# Author:      anas.ahmed
#
# Created:     15-06-2020
# Copyright:   (c) anas.ahmed 2020
# Licence:     <your licence>

import logger
import generic_constants
from constants import *
import json
import difflib
from xmldiff import main, formatting
import xml.dom.minidom
from lxml import etree
import tempfile
import os
import sys
import string
import random
import dynamic_variable_handler
import constant_variable_handler
import logging
import ast
log = logging.getLogger('file_operations_xml.py')

class FileOperationsXml:
    def __init__(self):
        self.DV = dynamic_variable_handler.DynamicVariables()
        self.CV = constant_variable_handler.ConstantVariables()
        pass
#------------------------------------------keywords---------------------------------------------
    def getXmlBlockData(self,input_val,*args):
        """
        Purpose: This function will get all xml blocks of data, from provided xml file.
        Input: <file-path>;<block xpath>
        Output: list of blocks
        """
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT

        elementList = []
        blockVal = None
        output_path = None

        elm = None
        searchList = []
        try:
            if ( args[0] ) :
                if(str(args[0].split(";")[0]).startswith("{") and str(args[0].split(";")[0]).endswith("}")):
                    out_path = self.DV.get_dynamic_value(args[0].split(";")[0])
                    if ( out_path ): output_path = out_path
                elif (str(args[0].split(";")[0]).startswith("_") and str(args[0].split(";")[0]).endswith("_")):
                    out_path = self.CV.get_constant_value(args[0].split(";")[0])
                    if ( out_path ): output_path = out_path
                else:
                    output_path = args[0].split(";")[0]
            if ( len(input_val) == 2 and len(input_val[-1]) != 0 ):
                blockVal = ';'.join(input_val[1:])
                path = input_val[0]
                if os.path.isfile(path):
                    try:elm = etree.parse(path)
                    except Exception as e:log.error(e)
                    if ( elm ):
                        searchList = self.searchPatternBuild(blockVal)
                        if( searchList ):
                            for i in range(0,len(searchList)):
                                elm = self.getTreeElemByXpath(elm,searchList[i])
                            for ele in elm:
                                el = self.treeElemToString(ele)
                                elementList.append(el)
                                del el
                            if ( len(elementList) > 0 ):
                                flg = True
                                optFlg = True
                                if ( elementList and output_path ):
                                    try:
                                        if isinstance(output_path, str) and (os.path.exists(output_path) or os.path.exists(os.path.dirname(output_path))):
                                            log.debug( "Writing the output of getXmlBlockData to file : " + str(output_path) )
                                            logger.print_on_console( "Writing the output of getXmlBlockData to file.")
                                            optFlg = False
                                            with open(output_path,'w') as f:
                                                for v in elementList:
                                                    f.write(v)
                                        else:
                                            logger.print_on_console(generic_constants.INVALID_OUTPUT_PATH)
                                    except Exception as e:
                                        err_msg = ("Exception occurred while writing to output file in getXmlBlockData : " + str(e))
                                        log.error( err_msg )
                                        flg = False
                                if( flg ):
                                    status = TEST_RESULT_PASS
                                    result = TEST_RESULT_TRUE
                                    logger.print_on_console( "Blocks found with given block xpath : " + str(len(elementList)) )
                                    if( optFlg ):
                                        value = elementList
                            else:
                                err_msg = 'Invalid tag, requires a valid tag identifier'
                        else:
                            err_msg = 'Invalid tag, requires a valid tag identifier'
                    else:
                        err_msg = 'Invalid XML data'
                else:
                    err_msg = generic_constants.FILE_NOT_EXISTS
            else:
                err_msg = generic_constants.INVALID_NUMBER_OF_INPUTS
            if ( err_msg != None ):
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = ("Exception occurred in getXmlBlockData, ERROR : " + str(e))
            log.error( err_msg )
            logger.print_on_console( "Error occured in getXmlBlockData" )
        del blockVal,input_val,elementList,path,elm,searchList
        return status, result, value ,err_msg

    def selectiveXmlFileCompare(self,input_val,*args):
        """
        Purpose: This function will selectively compare the block of data between two xml files
        Input: <file-path1>;<file-path2>;<all/selective - output result (optional)>;<block xpath>
        Output: differed text
        """
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        output_path = None
        res_opt = 'all'
        try:
            if ( args[0] ) :
                if(str(args[0].split(";")[0]).startswith("{") and str(args[0].split(";")[0]).endswith("}")):
                    out_path = self.DV.get_dynamic_value(args[0].split(";")[0])
                    if ( out_path ): output_path = out_path
                elif (str(args[0].split(";")[0]).startswith("_") and str(args[0].split(";")[0]).endswith("_")):
                    out_path = self.CV.get_constant_value(args[0].split(";")[0])
                    if ( out_path ): output_path = out_path
                else:
                    output_path = args[0].split(";")[0]
            # if input length is 4 then only proceed.
            if (len(input_val) == 4 and len(input_val[-1]) != 0):
                path1 = input_val[0]
                path2 = input_val[1]
                if ((input_val[2]) != '') : res_opt = input_val[2].lower().strip()
                blockVal = ';'.join(input_val[3:])
                if ( os.path.isfile(path1) and os.path.isfile(path2) ):
                    if ( blockVal ):
                        searchList= self.searchPatternBuild(blockVal)
                        if ( searchList ):
                            def writeSelectiveData(path,tempFile,searchList):
                                flag = True
                                elm = None
                                try:elm = etree.parse(path)
                                except Exception as e:log.error(e)
                                elementList = []
                                if (elm):
                                    for i in range(0,len(searchList)):
                                        elm = self.getTreeElemByXpath(elm,searchList[i])
                                    for ele in elm:
                                        el = self.treeElemToString(ele)
                                        elementList.append(el)
                                        del el
                                    with open(tempFile,'w') as f:
                                        for v in elementList:
                                            f.write(self.beautify_xml_file(v))
                                    if ( not elementList ):
                                        flag = False
                                        log.debug( 'Element list not found for file : ' + str(path) )
                                        #logger.print_on_console('Invalid block : XML data not found')
                                else:
                                    flag = False
                                    log.debug( 'Invalid XML file : ' + str(path) )
                                del elm, path, searchList, elementList
                                return flag
                            fp1 = self.createTempFile() #create temp file 1
                            fp2 = self.createTempFile() #create temp file 2
                            flg1 = writeSelectiveData(path1,fp1,searchList) #write the blocks (matched xml block data by block xml path) to temp file 1
                            flg2 = writeSelectiveData(path2,fp2,searchList) #write the blocks (matched xml block data by block xml path) to temp file 2
                            output_res = self.compare_xmls(fp1,fp2) # compare the two temp files
                            self.deleteTempFile(fp1) #delete temp file 1
                            self.deleteTempFile(fp2) #delete temp file 2
                            if ( output_res and flg1 and flg2):
                                flg = True
                                optFlg = True
                                num_diff,ch_lines = self.get_diff_count_xml(output_res)
                                try:
                                    #-----------------------------------------------------------------selective output
                                    if ( res_opt == 'selective' or res_opt == 'all') :
                                        log.info("Result to be displayed is : " + str(res_opt))
                                        logger.print_on_console("Result to be displayed is : " + str(res_opt))
                                        if (res_opt == 'selective') : output_res = ch_lines
                                        output_res = '\n'.join(output_res)
                                        if(num_diff):
                                            logger.print_on_console("The number of differences in selectiveXmlFileCompare are : ", num_diff)
                                        elif(int(num_diff) == 0):
                                            logger.print_on_console("No Difference between files in selectiveXmlFileCompare" )
                                        if(output_path):
                                            if isinstance(output_path,str) and ( os.path.isfile(output_path) or os.path.exists(os.path.dirname(output_path)) ):
                                                log.debug( "Writing the output of selectiveXmlFileCompare to file : " + str(output_path) )
                                                logger.print_on_console( "Writing the output of selectiveXmlFileCompare to file.")
                                                optFlg = False
                                                # Changed to append mode from write mode
                                                with open(output_path,'w') as f:
                                                    f.write(output_res)
                                            else:
                                                logger.print_on_console(generic_constants.INVALID_OUTPUT_PATH)
                                    else:
                                        err_msg = INVALID_INPUT
                                        flg = False
                                    #-----------------------------------------------------------------selective output
                                except Exception as e:
                                    err_msg = ("Exception occurred while writing to output file in selectiveXmlFileCompare : " + str(e))
                                    log.debug( err_msg )
                                    flg = False
                            else:
                                if output_res != "Invalid XML data":
                                    err_msg = 'Invalid XML data'
                                flg = False
                            if( flg ):
                                status = TEST_RESULT_PASS
                                result = TEST_RESULT_TRUE
                                log.info( "Comparision of files completed" )
                                if( optFlg ):
                                    value = output_res
                        else:
                            err_msg = 'Invalid block : incorrect input block data'
                    else:
                        err_msg = generic_constants.INVALID_INPUT
                else:
                    err_msg = generic_constants.FILE_NOT_EXISTS
            else:
                err_msg = generic_constants.INVALID_NUMBER_OF_INPUTS
            if ( err_msg != None ):
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = ("Exception occurred in selectiveXmlFileCompare while comparing two files, ERROR : " + str(e))
            log.error( err_msg )
            logger.print_on_console( "Error occured in selectiveXmlFileCompare" )
        return status, result, value ,err_msg

    def compXmlFileWithXmlBlock(self,input_val,*args):
        """
        Purpose: This function will compare data from getXmlBlockData with all blocks of data from mentioned file.
        Input: <file-path>;<blockData from getXmlBlockData>;<all/selective - output result (optional)>;<block xpath>
        Output: differed text
        """
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        res_opt = 'all'
        elementList = []
        blockVal = None
        blockData = None
        output_path = None
        output_res = []

        elm = None
        searchList = []
        try:
            if( args[0] ) :
                if(str(args[0].split(";")[0]).startswith("{") and str(args[0].split(";")[0]).endswith("}")):
                    out_path = self.DV.get_dynamic_value(args[0].split(";")[0])
                    if ( out_path ): output_path = out_path
                elif (str(args[0].split(";")[0]).startswith("_") and str(args[0].split(";")[0]).endswith("_")):
                    out_path = self.CV.get_constant_value(args[0].split(";")[0])
                    if ( out_path ): output_path = out_path
                else:
                    output_path = args[0].split(";")[0]
            # if input length is 4 then proceed
            if(len(input_val) == 4 and len(input_val[-1]) != 0):
                blockVal = ';'.join(input_val[3:])
                if ((input_val[2]) != '') : res_opt = input_val[2].lower().strip()
                blockData = input_val[1]
                if "[" in blockData and "]" in blockData:
                    blockData = ast.literal_eval(blockData)
                else:
                    blockData = [blockData]

                path = input_val[0]
                if( os.path.isfile( path ) ):
                    try: elm = etree.parse( path )
                    except Exception as e:log.error(e)
                    if( elm ):
                        searchList= self.searchPatternBuild( blockVal )
                        if( searchList ):
                            for i in range( 0, len(searchList) ):
                                elm = self.getTreeElemByXpath( elm, searchList[i] )
                            for ele in elm:
                                el = self.treeElemToString( ele )
                                elementList.append( el )
                                del el
                            # compare block of data to each block of data in file to be compared
                            logger.print_on_console( "Blocks found with given block xpath : " + str(len(elementList)) )
                            fg1 = True
                            fg2 = True
                            for data in blockData:
                                try : xml.dom.minidom.parseString(self.beautify_xml_file(data))
                                except : fg1 = False
                            for eL in elementList:
                                try : xml.dom.minidom.parseString(self.beautify_xml_file(eL))
                                except : fg2 = False
                            if blockData == elementList:
                                output_res.extend(blockData)
                            else:
                                for eL in elementList:
                                    out = []
                                    if ( fg1 and fg2 ):
                                        for data in blockData:
                                            out_1 = self.compare_xmls( self.beautify_xml_file( data ), self.beautify_xml_file( eL ) )
                                            if out_1 and out_1 not in out:
                                                out.extend(out_1)
                                    else :
                                        for data in blockData:
                                            out_1 = self.compare_texts( self.beautify_xml_file( data ), self.beautify_xml_file( eL ) )
                                            if out_1 and out_1 not in out:
                                                out.extend(out_1)
                                    output_res.extend( out )
                                    del out
                            if ( output_res and len(output_res) > 0 ):
                                flg = True
                                optFlg = True
                                num_diff,ch_lines = self.get_diff_count_xml(output_res)
                                #num_diff,ch_lines = self.get_diff_count( output_res )
                                try:
                                    #-----------------------------------------------------------------selective output
                                    if ( res_opt == 'selective' or res_opt == 'all') :
                                        log.info("Result to be displayed is : " + str(res_opt))
                                        logger.print_on_console("Result to be displayed is : " + str(res_opt))
                                        if (res_opt == 'selective') : output_res = ch_lines
                                        output_res = '\n'.join(output_res)
                                        if(num_diff):
                                            logger.print_on_console("The number of differences in compXmlFileWithXmlBlock are : ", num_diff)
                                        elif(int(num_diff) == 0):
                                            logger.print_on_console("No Difference between files in compXmlFileWithXmlBlock" )
                                        if( output_path ):
                                            if isinstance(output_path,str) and ( os.path.isfile(output_path) or os.path.exists(os.path.dirname(output_path)) ):
                                                log.debug( "Writing the output of compXmlFileWithXmlBlock to file : " + str(output_path) )
                                                logger.print_on_console( "Writing the output of compXmlFileWithXmlBlock to file.")
                                                optFlg = False
                                                with open(output_path,'w') as f:
                                                    f.write(output_res)
                                            else:
                                                logger.print_on_console(generic_constants.INVALID_OUTPUT_PATH)
                                    else:
                                        err_msg = INVALID_INPUT
                                        flg = False
                                except Exception as e:
                                    err_msg = "Exception occurred while writing to output file in compXmlFileWithXmlBlock : " + str(e)
                                    log.debug( err_msg )
                                    flg = False
                            else:
                                err_msg = 'Invalid block : XML data not found'
                                flg = False
                            if( flg ):
                                status = TEST_RESULT_PASS
                                result = TEST_RESULT_TRUE
                                log.info( "Comparision of texts completed" )
                                if( optFlg ):
                                    value = output_res
                        else:
                            err_msg = 'Invalid block : incorrect input block data'
                    else:
                        err_msg = 'Invalid XML data'
                else:
                    err_msg = generic_constants.FILE_NOT_EXISTS
            else:
                err_msg = generic_constants.INVALID_NUMBER_OF_INPUTS
            if ( err_msg != None ):
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = ("Exception occurred in compXmlFileWithXmlBlock, ERROR : " + str(e))
            log.error( err_msg )
            logger.print_on_console( "Error occured in compXmlFileWithXmlBlock" )
        del elementList, blockVal, blockData, output_path, output_res, input_val, elm, searchList #deleting variables
        return status, result, value ,err_msg

    def compare_inputs(self,input_val,*args):
        """
        def : compare_inputs
        Purpose :  compares two text inputs
        Input : inputtext-1,inputtext-2,<all/selective - output result (optional)>
        Output : differed text, bool
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
                        if(str(args[0].split(";")[0]).startswith("{") and str(args[0].split(";")[0]).endswith("}")):
                            out_path = self.DV.get_dynamic_value(args[0].split(";")[0])
                            if ( out_path ): output_path = out_path
                        elif (str(args[0].split(";")[0]).startswith("_") and str(args[0].split(";")[0]).endswith("_")):
                            out_path = self.CV.get_constant_value(args[0].split(";")[0])
                            if ( out_path ): output_path = out_path
                        else:
                            output_path = args[0].split(";")[0]
                    if ( len(input_val) == 3 and (input_val[2] != None or input_val[2] != '' )) : res_opt = input_val[2].strip().lower()
                    try:
                        import xml.etree.ElementTree as ET
                        root1 = ET.fromstring(inputtext1)
                        root2 = ET.fromstring(inputtext2)
                        xml_data_flag = True
                        del root1,root2
                    except:
                        xml_data_flag = False
                    if not xml_data_flag:
                        output_res = self.compare_texts(inputtext1, inputtext2)
                    else:output_res = self.compare_xml_texts(inputtext1, inputtext2)
                    if ( output_res ):
                        flg = True
                        optFlg = True
                        try:
                            if not xml_data_flag: num_diff, ch_lines = self.get_diff_count(output_res)
                            else: num_diff, ch_lines = self.get_diff_count_xml(output_res)
                            if(num_diff):
                                logger.print_on_console("The number of differences in compareInputs are: ",num_diff)
                            elif(int(num_diff) == 0):
                                    logger.print_on_console("No Difference between inputs in compareInputs")
                            if ( res_opt == 'selective' or res_opt == 'all') :
                                log.info("Result to be displayed is : " + str(res_opt))
                                logger.print_on_console("Result to be displayed is : " + str(res_opt))
                                if (res_opt == 'selective') : output_res = ch_lines
                            output_res = '\n'.join(output_res)
                            if(output_path):
                                if isinstance(output_path,str) and (os.path.isfile(output_path) or os.path.exists(os.path.dirname(output_path))):
                                    log.debug( "Writing the output of compareInputs to file : " + str(output_path) )
                                    logger.print_on_console( "Writing the output of compareInputs to file.")
                                    optFlg = False
                                    with open(output_path,'w') as f:
                                        f.write(output_res)
                                else:
                                    logger.print_on_console(generic_constants.INVALID_OUTPUT_PATH)
                        except Exception as ex:
                            err_msg = ("Exception occurred while writing to output file in compareInputs : " + str(ex))
                            log.debug( err_msg )
                            flg = False
                        if( flg ):
                            status = TEST_RESULT_PASS
                            result = TEST_RESULT_TRUE
                            log.info("Comparision of texts completed")
                            if( optFlg ):
                                value = output_res
                else:
                    err_msg = 'Empty inputs'
            else:
                err_msg = 'Invalid number of inputs'
            if ( err_msg != None ):
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = ("Exception occurred in compare_inputs while comparing inputs " + str(e))
            log.error( err_msg )
            logger.print_on_console( "Error occured in Compare Inputs" )
        return status, result, value ,err_msg

    def beautify_file(self, input_val, *args):
        """
        def : beautify_file
        Purpose : beautifies/pretifies a file/string of type json or xml
        Input : inputpath,file type
        Output : beautified text, bool
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
                    if(str(args[0].split(";")[0]).startswith("{") and str(args[0].split(";")[0]).endswith("}")):
                        out_path = self.DV.get_dynamic_value(args[0].split(";")[0])
                        if ( out_path ): output_path = out_path
                    elif (str(args[0].split(";")[0]).startswith("_") and str(args[0].split(";")[0]).endswith("_")):
                        out_path = self.CV.get_constant_value(args[0].split(";")[0])
                        if ( out_path ): output_path = out_path
                    else:
                        output_path = args[0].split(";")[0]
                if (str(iv2).lower() == 'json'):
                    beautified_output = self.beautify_json_file(iv1)
                elif (str(iv2).lower() == 'xml'):
                    beautified_output = self.beautify_xml_file(iv1)
                else:
                    err_msg = 'File format not supported'
                if(beautified_output):
                    flg = True
                    optFlg = True
                    try:
                        if(output_path):
                            if isinstance(output_path,str) and (os.path.isfile(output_path) or os.path.exists(os.path.dirname(output_path))):
                                log.debug( "Writing the output of beautify to file: " + str(output_path) )
                                logger.print_on_console( "Writing the output of beautify to file.")
                                optFlg = False
                                with open(output_path,'w') as f:
                                    f.write(beautified_output)
                            else:
                                logger.print_on_console(generic_constants.INVALID_OUTPUT_PATH)
                    except Exception as ex:
                        err_msg = ("Exception occurred while writing to output file in beautify_file : " + str(ex))
                        log.debug( err_msg )
                        flg = False
                    if(flg):
                        status=TEST_RESULT_PASS
                        result=TEST_RESULT_TRUE
                        log.info('Input text/file is beautified')
                        if( optFlg ):
                            value = beautified_output
            else:
                err_msg = 'Invalid number of inputs'
            if ( err_msg != None ):
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = ("Exception occurred in beautify_file : " + str(e))
            log.error( err_msg )
            logger.print_on_console( "Error occured in Beautify File" )
        return status, result, value ,err_msg

    def compare_files(self,input_val,*args):
        """
        def : compare_file
        Purpose : compares two files
        Input : inputPath-1,inputPath-2,<all/selective - output result (optional)>
        Output : differed text, bool
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
                    if(str(args[0].split(";")[0]).startswith("{") and str(args[0].split(";")[0]).endswith("}")):
                        out_path = self.DV.get_dynamic_value(args[0].split(";")[0])
                        if ( out_path ): output_path = out_path
                    elif (str(args[0].split(";")[0]).startswith("_") and str(args[0].split(";")[0]).endswith("_")):
                        out_path = self.CV.get_constant_value(args[0].split(";")[0])
                        if ( out_path ): output_path = out_path
                    else:
                        output_path = args[0].split(";")[0]
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
                            self.storeSortFileTempLoc(filePathA,filePathB)
                            fp1 = tempfile.gettempdir()+"\\FileA.xml"
                            fp2 = tempfile.gettempdir()+"\\FileB.xml"
                            output_res = self.compare_xmls(fp1,fp2)
                            self.deleteSortFileTempLoc()
                            if(output_res):
                                num_diff,ch_lines = self.get_diff_count_xml(output_res)
                        elif (fileExtensionA == '.json' and fileExtensionB == '.json'):
                            # output_res contains the diffs, name_list contains the common names between 2 JSON content
                            output_res,name_list = self.compare_json(filePathA, filePathB)
                            if(output_res):
                                num_diff, ch_lines = self.get_diff_count_json(output_res)
                                output_res = name_list+output_res
                            else:
                                # files are similar
                                flg = True
                                optFlg = False
                                logger.print_on_console("The JSON Files are similar.")
                                log.info("The JSON Files are similar.")
                        else:
                            output_res = self.compare_texts(file1_lines,file2_lines)
                            if(output_res):
                                num_diff,ch_lines = self.get_diff_count(output_res)

                        if ( output_res ):
                            flg = True
                            optFlg = True
                            try:
                                if ( res_opt == 'selective' or res_opt == 'all') :
                                    log.info("Result to be displayed is : " + str(res_opt))
                                    logger.print_on_console("Result to be displayed is : " + str(res_opt))
                                    if (res_opt == 'selective') : output_res = ch_lines
                                output_res = '\n'.join(output_res)
                                if(num_diff):
                                    logger.print_on_console("The number of differences in compare_file are: ",num_diff)
                                elif(int(num_diff) == 0):
                                    logger.print_on_console("No Difference between inputs in compareFile")
                                if(output_path):
                                    if isinstance(output_path,str) and (os.path.exists(output_path) or os.path.exists(os.path.dirname(output_path))):
                                        log.debug( "Writing the output of compareFiles to file : " + str(output_path) )
                                        logger.print_on_console( "Writing the output of compareFiles to file.")
                                        optFlg = False
                                        with open(output_path,'w') as f:
                                            f.write(output_res)
                                    else:
                                        logger.print_on_console(generic_constants.INVALID_OUTPUT_PATH)
                            except Exception as ex:
                                err_msg = ("Exception occurred while writing to output file in compareFile : " + str(ex))
                                log.debug( err_msg )
                                flg = False
                        if(flg):
                            status = TEST_RESULT_PASS
                            result = TEST_RESULT_TRUE
                            log.info("Comparision of files completed")
                            if( optFlg ):
                                value = output_res
                    else:
                        err_msg = 'One or more files are empty'
                else:
                    err_msg = generic_constants.FILE_NOT_EXISTS
            else:
                err_msg = 'Invalid number of inputs'
            if ( err_msg != None ):
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = ("Exception occurred in compare_files while comparing two files"+str(e))
            log.error( err_msg )
            logger.print_on_console( "Error occured in Compare Files" )
        return status, result, value, err_msg
#------------------------------------------keywords end---------------------------------------------

#------------------------------------------keyword-operations-----------------------------------
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
            if( text1_lines == text2_lines ):
                logger.print_on_console( "Inputs are same" )
                log.info( "Inputs are same" )
            out = list(difflib.Differ().compare(text1_lines, text2_lines))
        except Exception as e:
            logger.print_on_console("Exception occurred in compare_texts while comparing two texts")
            log.error("Exception occurred in compare_texts while comparing two texts, ERR_MSG:" + str(e))
        return out

    def compare_xml_texts(self, xml_input1, xml_input2):
        """
        def : compare_xml_text
        purpose : compares two xml content
        param : xml data-1, xml data-2
        return : differed xml
        """
        out = None
        try:
            out = main.diff_texts(xml_input1, xml_input2, diff_options={'fast_match': True,'ratio_mode':'accurate'}, formatter=formatting.XMLFormatter(normalize=formatting.WS_BOTH)).split("\n")
        except Exception as e:
            log.debug("Could not found the difference in XML content", e)
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
            #check if xml is a file path'
            if ( os.path.isfile(xml_input1) and os.path.isfile(xml_input1) ) :
                log.info('Comparison between xml files')
                out = main.diff_files(xml_input1, xml_input2, diff_options={'fast_match': False},formatter=formatting.XMLFormatter(normalize=formatting.WS_BOTH)).split("\n")
            elif( not(os.path.isfile(xml_input1)) and not(os.path.isfile(xml_input2)) ):
                log.info('Comparison between xml text data')
                text1_lines = xml_input1.splitlines()
                text2_lines = xml_input2.splitlines()
                if ( text1_lines == text2_lines ):
                    log.info('Inputs are same')
                    logger.print_on_console( 'Inputs are same' )
                out = main.diff_texts(xml_input1, xml_input2, diff_options={'fast_match': False},formatter=formatting.XMLFormatter(normalize=formatting.WS_BOTH)).split("\n")
        # Handling the empty xml document exception.
        except etree.XMLSyntaxError as e:
            # get caller method name
            called_method_name = sys._getframe(1).f_code.co_name
            if called_method_name == "selectiveXmlFileCompare" and "Document is empty" in e.msg:
                out = "Invalid XML data"
                logger.print_on_console("Invalid XML data")
                log.error("Invalid XML data")
            else:
                log.error(e.msg)
            return out
        except Exception as e:
            logger.print_on_console( "Exception occurred in compare_xmls while comparing two xml data" )
            log.error( "Exception occurred in compare_xmls while comparing two xml data, ERR_MSG:" + str(e) )
        return out

    def compare_json(self, json_file1, json_file2):
        """
        def : compare_json
        purpose : compares two json files
        param : inputPath-1,inputPath-2
        return : differed json and common names list
        """
        try:
            with open(json_file1, 'r') as f:
                json1 = json.load(f)
            with open(json_file2, 'r') as f:
                json2 = json.load(f)
            not_in_json1 = []
            not_in_json2 = []
            name_list=[]
            # diff_count = 0            
            for key in json1:
                if key not in json2:
                    not_in_json2.append(f'- {dict({key: json1[key]})}')
                    # diff_count += 1
                elif key in json2:
                    if isinstance(json1[key], list) and isinstance(json2[key], list):
                        if not (sorted(json1[key]) == sorted(json2[key])):
                            not_in_json2.append(f'- {dict({key: json1[key]})}')
                            diff_count += 1
                        else:
                            name_list.append(f'{dict({key: json1[key]})}')
                    elif json1[key] != json2[key]:
                        not_in_json2.append(f'- {dict({key: json1[key]})}')
                        # diff_count += 1
                    else:
                        name_list.append(f'{dict({key: json1[key]})}')
            for key in json2:
                if key not in json1:
                    not_in_json1.append(f'+ {dict({key: json2[key]})}')
                    # diff_count += 1
                elif key in json1:
                    if isinstance(json1[key], list) and isinstance(json2[key], list):
                        if not (sorted(json1[key]) == sorted(json2[key])):
                            not_in_json1.append(f'+ {dict({key: json2[key]})}')
                            # diff_count += 1
                    elif json1[key] != json2[key]:
                        not_in_json1.append(f'+ {dict({key: json2[key]})}')
                        # diff_count += 1
        except Exception as e:
            logger.print_on_console( "Exception occurred in compare_json while comparing two json file data" )
            log.error( "Exception occurred in compare_json while comparing two json file data, ERR_MSG:" + str(e) )
        return not_in_json2+not_in_json1, name_list

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
    def get_diff_count_json(self,output_response):
        """
        def : get_diff_count_json
        purpose : counts number of differences between json inputs
        param : difference of inputs
        return : count of differences
        """
        # ch_lines = [] ch_lines same as output_response
        num_diff=0
        for line in output_response:
            if line.startswith('+') or line.startswith('-'):
                num_diff+=1
        return num_diff,output_response

    #-----------------------------------------------sorting functions
    def get_node_key(self,node, attr=None):
        """
        Return the sorting key of an xml node using tag and attributes
        """
        if attr is None:
            return '%s' % node.tag + ':'.join([node.get(attr)
                                            for attr in sorted(node.attrib)])
        if attr in node.attrib:
            return '%s:%s' % (node.tag, node.get(attr))
        return '%s' % node.tag


    def sort_children(self,node, attr=None):
        """
        Sort children along tag and given attribute.
        if attr is None, sort along all attributes
        """
        if not isinstance(node.tag, str):  # PYTHON 2: use basestring instead
            # not a TAG, it is comment or DATA
            # no need to sort
            return
        # sort child along attr
        node[:] = sorted(node, key=lambda child: self.get_node_key(child, attr))
        # and recurse
        for child in node:
            self.sort_children(child, attr)


    def sort(self, unsorted_file, sorted_file, attr=None):
        """
        Sort unsorted xml file and save to sorted_file
        """
        tree = etree.parse(unsorted_file)
        root = tree.getroot()
        self.sort_children(root, attr)

        sorted_unicode = etree.tostring(root,
                                        pretty_print=True,
                                        encoding='unicode')
        with open(sorted_file, 'w') as output_fp:
            output_fp.write('%s' % sorted_unicode)
            log.info('written sorted file %s', sorted_unicode)

    def storeSortFileTempLoc(self,FileA,FileB):
        self.sort(FileA,tempfile.gettempdir()+"\\FileA.xml")
        self.sort(FileB,tempfile.gettempdir()+"\\FileB.xml")

    def deleteSortFileTempLoc(self):
        os.remove(tempfile.gettempdir()+"\\FileA.xml")
        os.remove(tempfile.gettempdir()+"\\FileB.xml")
    #-----------------------------------------------sorting functions end

    #-----------------------------------------------block data operations
    def writeToFileTemp(self,outFile,data):
        outFile.write(data)

    def getTreeElemByXpath(self,element,search):
        res = None
        try:
            for e in element:
                res = e.xpath(search)
        except:
            res =element.xpath(search)
        if (res == None):
            log.info('Entered element xpath is incorrect : '+ str(search))
            logger.print_on_console('Entered element xpath is incorrect : '+ str(search))
        return res

    def treeElemToString(self,element):
        tree = etree.tostring(element,encoding="unicode")
        return tree

    def igSplit(self,t):
        splitList = []
        start = 0
        si = 0
        for i in range(0,len(t)):
            if(t[i]==' '):
                si = i
            if(i>0 and t[i-1]=='=' and t[i]=='"'):
                splitList.append(t[start:si])
                start=si
                while (t[start]==' ' and start<len(t)):
                    start=start+1
        if(start<len(t)):
            splitList.append(t[start:len(t)])
        del start,si,t,i
        return splitList

    def searchPatternBuild(self,searchInput):
        """splits input to xml searchable format
            Input: string
            Output:List (of searchable formats)
            Eg: Input : '<m d="ClassCd" i="CLASS - CD" v="8017A"/>'
                Output : .//m[@d="ClassCd" and @i="CLASS - CD" and @v="8017A"]
        """
        finalList = []
        try:
            tempList = searchInput.split(';')
            for t in tempList:
                st = None
                t = t[1:len(t) - 1]
                if ( t[len(t)-1] == '/' ):t = t[:len(t)-1]
                t = self.igSplit(t)
                st = ".//" + t[0]
                if(len(t)>1):
                    st = st + '[' +'@'+t[1]
                    if (len(t) == 2):
                        st = st + ']'
                    else:
                        for i in range(2,len(t)):
                            st  = st + ' and ' + '@' +t[i]
                        st = st + ']'
                finalList.append(st)
            del tempList,t,st,i,searchInput
        except Exception as e:
            log.debug('Error occoured in searchPatternBuild : ' + str(e))
        return finalList
    #-----------------------------------------------block data operations end
    def createTempFile(self):
        fileName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        return  tempfile.gettempdir() + '\\' + fileName + ".xml"

    def deleteTempFile(self,filePath):
        try : os.remove(filePath)
        except Exception as e : log.error('WARNING! : File ' + filePath + ' could not be removed from temp location, ERR_MSG : ' + str(e))

#------------------------------------------keyword-operations end-----------------------------------
