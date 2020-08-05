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
import string
import random
import dynamic_variable_handler
import logging
log = logging.getLogger('file_operations_xml.py')

class FileOperationsXml:
    def __init__(self):
        self.DV = dynamic_variable_handler.DynamicVariables()
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
        try:
            if ( args[0] ) :
                if(str(args[0].split(";")[0]).startswith("{") and str(args[0].split(";")[0]).endswith("}")):
                    out_path = self.DV.get_dynamic_value(args[0].split(";")[0])
                    if ( out_path ): output_path = out_path
                else:
                    output_path = args[0].split(";")[0]
            if ( len(input_val) >= 2 ):
                blockVal = ';'.join(input_val[1:])
                path = input_val[0]
                if os.path.isfile(path):
                    searchList= self.searchPatternBuild(blockVal)
                    elm = etree.parse(path)
                    for i in range(0,len(searchList)):
                        elm = self.getTreeElemByXpath(elm,searchList[i])
                    for ele in elm:
                        el = self.treeElemToString(ele)
                        elementList.append(el)
                        del el
                    if ( len(elementList) > 0 ):
                        flg = True
                        if ( elementList and output_path ):
                            try:
                                if( os.path.exists(output_path) or os.path.exists(os.path.dirname(output_path)) ):
                                    logger.print_on_console( "Writing the output of getXmlBlockData to file : " + str(output_path) )
                                    with open(output_path,'w') as f:
                                        for v in elementList:
                                            f.write(v)
                                else:
                                    err_msg = generic_constants.FILE_NOT_EXISTS
                                    flg = False
                            except Exception as e:
                                err_msg = ("Exception occurred while writing to output file in getXmlBlockData : " + str(ex))
                                log.error( err_msg )
                                logger.print_on_console( "Error occured while writing to output file in getXmlBlockData" )
                        if( flg ):
                            status = TEST_RESULT_PASS
                            result = TEST_RESULT_TRUE
                            logger.print_on_console( "Blocks found with given block xpath : " +str(len(elementList)) )
                            value = elementList
                    else:
                        err_msg = 'Invalid block : XML data not found'
                    del elm,searchList
                else:
                    err_msg = generic_constants.FILE_NOT_EXISTS
            else:
                err_msg = generic_constants.INVALID_INPUT
            if ( err_msg != None ):
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = ("Exception occurred in getXmlBlockData, ERROR : " + str(e))
            log.error( err_msg )
            logger.print_on_console( "Error occured in getXmlBlockData" )
        del blockVal,input_val,elementList,path
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
                else:
                    output_path = args[0].split(";")[0]
            if (len(input_val)>=4):
                path1 = input_val[0]
                path2 = input_val[1]
                if ((input_val[2]) != '') : res_opt = input_val[2].lower().strip()
                blockVal = ';'.join(input_val[3:])
                if ( os.path.isfile(path1) and os.path.isfile(path2) ):
                    if ( blockVal ):
                        searchList= self.searchPatternBuild(blockVal)
                        def writeSelectiveData(path,tempFile,searchList):
                            flag = True
                            elm = etree.parse(path)
                            elementList = []
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
                                        if( os.path.isfile(output_path) or os.path.exists(os.path.dirname(output_path)) ):
                                            logger.print_on_console( "Writing the output of selectiveXmlFileCompare to : " + str(output_path) )
                                            with open(output_path,'w') as f:
                                                f.write(output_res)
                                        else:
                                            err_msg = generic_constants.FILE_NOT_EXISTS
                                            flg = False
                                else:
                                    err_msg = INVALID_INPUT
                                    flg = False
                                #-----------------------------------------------------------------selective output
                            except Exception as e:
                                err_msg = ("Exception occurred while writing to output file in selectiveXmlFileCompare : " + str(ex))
                                log.error( err_msg )
                                logger.print_on_console( "Error occured while writing to output file in selectiveXmlFileCompare" )
                        else:
                            err_msg = 'Invalid block : XML data not found'
                            flg = False
                        if( flg ):
                            log.info( "Comparision of files completed" )
                            value = output_res
                            status = TEST_RESULT_PASS
                            result = TEST_RESULT_TRUE
                    else:
                        err_msg = generic_constants.INVALID_INPUT
                else:
                    err_msg = generic_constants.FILE_NOT_EXISTS
            else:
                err_msg = generic_constants.INVALID_INPUT
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
        try:
            if ( args[0] ) :
                if(str(args[0].split(";")[0]).startswith("{") and str(args[0].split(";")[0]).endswith("}")):
                    out_path = self.DV.get_dynamic_value(args[0].split(";")[0])
                    if ( out_path ): output_path = out_path
                else:
                    output_path = args[0].split(";")[0]
            if ( len(input_val) >= 4 ):
                blockVal = ';'.join(input_val[3:])
                if ((input_val[2]) != '') : res_opt = input_val[2].lower().strip()
                blockData = input_val[1]
                path = input_val[0]
                if os.path.isfile( path ):
                    searchList= self.searchPatternBuild( blockVal )
                    elm = etree.parse( path )
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
                    try : xml.dom.minidom.parseString(self.beautify_xml_file(blockData))
                    except : fg1 = False
                    for eL in elementList:
                        try : xml.dom.minidom.parseString(self.beautify_xml_file(eL))
                        except : fg2 = False
                    for eL in elementList:
                        if ( fg1 and fg2 ):
                            out = self.compare_xmls( self.beautify_xml_file( blockData ), self.beautify_xml_file( eL ) )
                        else :
                            out = self.compare_texts( self.beautify_xml_file( blockData ), self.beautify_xml_file( eL ) )
                        output_res.extend( out )
                    if ( output_res and len(output_res) > 0 ):
                        flg = True
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
                                if(output_path):
                                    if( os.path.isfile(output_path) or os.path.exists(os.path.dirname(output_path)) ):
                                        logger.print_on_console( "Writing the output of compXmlFileWithXmlBlock to : " + str(output_path) )
                                        with open(output_path,'w') as f:
                                            f.write(output_res)
                                    else:
                                        err_msg = generic_constants.FILE_NOT_EXISTS
                                        flg = False
                            else:
                                err_msg = INVALID_INPUT
                                flg = False
                        except Exception as e:
                            err_msg = ("Exception occurred while writing to output file in compXmlFileWithXmlBlock : " + str(ex))
                            log.error( err_msg )
                            logger.print_on_console( "Error occured while writing to output file in compXmlFileWithXmlBlock" )
                    else:
                        err_msg = 'Invalid block : XML data not found'
                        flg = False
                    if( flg ):
                        log.info( "Comparision of texts completed" )
                        value = output_res
                        status = TEST_RESULT_PASS
                        result = TEST_RESULT_TRUE
                    del ele,elm,searchList
                else:
                    err_msg = generic_constants.FILE_NOT_EXISTS
            else:
                err_msg = generic_constants.INVALID_INPUT
            if ( err_msg != None ):
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = ("Exception occurred in compXmlFileWithXmlBlock, ERROR : " + str(e))
            log.error( err_msg )
            logger.print_on_console( "Error occured in compXmlFileWithXmlBlock" )
        del elementList, blockVal, blockData, output_path, output_res, input_val #deleting variables
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
                        else:
                            output_path = args[0].split(";")[0]
                    if ( len(input_val) == 3 and (input_val[2] != None or input_val[2] != '' )) : res_opt = input_val[2].strip().lower()
                    output_res = self.compare_texts(inputtext1,inputtext2)
                    if ( output_res ):
                        flg = True
                        try:
                            num_diff,ch_lines = self.get_diff_count(output_res)
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
                                if(os.path.isfile(output_path) or os.path.exists(os.path.dirname(output_path))):
                                    logger.print_on_console( "Writing the output of compareInputs to file: " + str(output_path) )
                                    with open(output_path,'w') as f:
                                        f.write(output_res)
                                else:
                                    err_msg='Wrong file path entered'
                                    flg = False
                        except Exception as ex:
                            err_msg = ("Exception occurred while writing to output file in compareInputs : "+str(ex))
                            log.error( err_msg )
                            logger.print_on_console( "Error occured while writing to output file in compareInputs" )
                        if(flg):
                            log.info("Comparision of texts completed")
                            value = output_res
                            status = TEST_RESULT_PASS
                            result = TEST_RESULT_TRUE
                else:
                    err_msg = 'Empty inputs'
            else:
                err_msg = 'Invalid number of inputs'
            if ( err_msg != None ):
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = ("Exception occurred in compare_inputs while comparing inputs"+str(e))
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
                    try:
                        if(output_path):
                            if(os.path.isfile(output_path) or os.path.exists(os.path.dirname(output_path))):
                                logger.print_on_console( "Writing the output of beautify to file: " + str(output_path) )
                                with open(output_path,'w') as f:
                                    f.write(beautified_output)
                            else:
                                flg = False
                                err_msg='Wrong file path entered'
                    except Exception as ex:
                        err_msg = ("Exception occurred while writing to output file in beautify_file : "+str(ex))
                        log.error( err_msg )
                        logger.print_on_console( "Error occured while writing to output file in Beautify" )
                    if(flg):
                        value = beautified_output
                        status=TEST_RESULT_PASS
                        result=TEST_RESULT_TRUE
            else:
                err_msg = 'Invalid number of inputs'
            if ( err_msg != None ):
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = ("Exception occurred in beautify_file : "+str(e))
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
                        else:
                            output_res = self.compare_texts(file1_lines,file2_lines)
                            if(output_res):
                                num_diff,ch_lines = self.get_diff_count(output_res)

                        if ( output_res ):
                            flg = True
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
                                    if(os.path.exists(output_path) or os.path.exists(os.path.dirname(output_path))):
                                        logger.print_on_console( "Writing the output of compareFiles to file : " + str(output_path) )
                                        with open(output_path,'w') as f:
                                            f.write(output_res)
                                    else:
                                        err_msg = generic_constants.FILE_NOT_EXISTS
                                        flg = False
                            except Exception as ex:
                                err_msg = ("Exception occurred while writing to output file in compareFile : "+str(ex))
                                log.error( err_msg )
                                logger.print_on_console( "Error occured while writing to output file in compareFile" )
                            if(flg):
                                log.info("Comparision of files completed")
                                value = output_res
                                status = TEST_RESULT_PASS
                                result = TEST_RESULT_TRUE
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
        return status, result, value ,err_msg
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
        except Exception as e:
            logger.print_on_console( "Exception occurred in compare_xmls while comparing two xml data" )
            log.error( "Exception occurred in compare_xmls while comparing two xml data, ERR_MSG:" + str(e) )
        return out

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
        tempList = searchInput.split(';')
        finalList = []
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
        return finalList
    #-----------------------------------------------block data operations end
    def createTempFile(self):
        fileName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        return  tempfile.gettempdir() + '\\' + fileName + ".xml"

    def deleteTempFile(self,filePath):
        try : os.remove(filePath)
        except Exception as e : log.error('WARNING! : File ' + filePath + ' could not be removed from temp location, ERR_MSG : ' + str(e))

#------------------------------------------keyword-operations end-----------------------------------