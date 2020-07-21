#-------------------------------------------------------------------------------
# Name:        file_operations_xml
# Purpose:     comparison between two xml data, in respective menthods
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
from lxml import etree
import tempfile
import os
import string
import random
import logging

log = logging.getLogger('file_operations_xml.py')

class FileOperationsXml:
    def __init__(self):
        pass
#------------------------------------------keywords---------------------------------------------
    def getXmlBlockData(self,input_val,*args):
        """
        This function will get all xml blocks of data, from provided xml file.
        Input: <file-path>;<block xpath>
        output: list of blocks
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
                out_path = args[0].split(";")[0]
                if(not out_path.startswith("{")):
                    output_path = out_path
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
                                    with open(output_path,'w') as f:
                                        for v in elementList:
                                            f.write(v)
                                else:
                                    err_msg = generic_constants.FILE_NOT_EXISTS
                                    flg = False
                            except Exception as e:
                                err_msg = ("Exception occurred while writing to output file in compare_file : " + str(ex))
                                log.error( err_msg )
                                logger.print_on_console( "Error occured while writing to output file in Compare File" )
                        if( flg ):
                            status = TEST_RESULT_PASS
                            result = TEST_RESULT_TRUE
                            value = elementList
                    del ele,elm,searchList
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
        This function will selectively compare the block of data between two xml files
        Input: <file-path1>;<file-path2>;<block xpath>
        output: differed text
        """
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        output_path = None
        try:
            if ( args[0] ) :
                out_path = args[0].split(";")[0]
                if(not out_path.startswith("{")):
                    output_path = out_path
            if (len(input_val)>=3):
                path1 = input_val[0]
                path2 = input_val[1]
                blockVal = ';'.join(input_val[2:])
                if ( os.path.isfile(path1) and os.path.isfile(path2) ):
                    if ( blockVal ):
                        searchList= self.searchPatternBuild(blockVal)
                        def writeSelectiveData(path,tempFile,searchList):
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
                                    f.write(v)
                            del elm,path,tempFile,searchList,elementList
                        fp1 = self.createTempFile()
                        fp2 = self.createTempFile()
                        writeSelectiveData(path1,fp1,searchList)
                        writeSelectiveData(path2,fp2,searchList)
                        output_res = self.compare_texts(fp1,fp2)
                        if ( output_res ):
                            flg = True
                            num_diff,ch_lines = self.get_diff_count_xml(output_res)
                            try:
                                output_res = '\n'.join(output_res)
                                if(num_diff):
                                    logger.print_on_console("The number of differences in compare_file are : ", num_diff)
                                if(output_path):
                                    if( os.path.exists(output_path) or os.path.exists(os.path.dirname(output_path)) ):
                                        with open(output_path,'w') as f:
                                            f.write(output_res)
                                    else:
                                        err_msg = generic_constants.FILE_NOT_EXISTS
                                        flg = False
                            except Exception as e:
                                err_msg = ("Exception occurred while writing to output file in compare_file : " + str(ex))
                                log.error( err_msg )
                                logger.print_on_console( "Error occured while writing to output file in Compare File" )
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
            import traceback
            traceback.print_exc()
            err_msg = ("Exception occurred in selectiveXmlFileCompare while comparing two files, ERROR : " + str(e))
            log.error( err_msg )
            logger.print_on_console( "Error occured in selectiveXmlFileCompare" )
        return status, result, value ,err_msg

    def compXmlFileWithXmlBlock(self,input_val,*args):
        """
        This function will compare data from getXmlBlockData with all blocks of data from mentioned file.
        Input: <file-path>;<blockData from getXmlBlockData>;<block xpath>
        output: differed text
        """
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT

        elementList = []
        blockVal = None
        blockData = None
        output_path = None
        output_res = []
        try:
            if ( args[0] ) :
                out_path = args[0].split(";")[0]
                if(not out_path.startswith("{")):
                    output_path = out_path
            if ( len(input_val) >= 3 ):
                blockVal = ';'.join(input_val[2:])
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
                    for eL in elementList:
                        output_res.extend( self.compare_texts( blockData, eL ) )
                    if( output_res ):
                        num_diff,ch_lines = self.get_diff_count( output_res )
                        output_res = '\n'.join(output_res)
                    if ( len(output_res) > 0 ):
                        flg = True
                        if ( output_res and output_path ):
                            try:
                                #output_res = '\n'.join(output_res)
                                if( os.path.exists(output_path) or os.path.exists(os.path.dirname(output_path)) ):
                                    with open(output_path,'w') as f:
                                            f.write(output_res)
                                else:
                                    err_msg = generic_constants.FILE_NOT_EXISTS
                                    flg = False
                            except Exception as e:
                                err_msg = ("Exception occurred while writing to output file in compare_file : " + str(ex))
                                log.error( err_msg )
                                logger.print_on_console( "Error occured while writing to output file in Compare File" )
                        if( flg ):
                            log.info("Comparision of texts completed")
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
            import traceback
            traceback.print_exc()
            err_msg = ("Exception occurred in compXmlFileWithXmlBlock, ERROR : " + str(e))
            log.error( err_msg )
            logger.print_on_console( "Error occured in compXmlFileWithXmlBlock" )
        return status, result, value ,err_msg

    def compare_inputs(self,input_val,*args):
        """
        def : compare_inputs
        purpose : compares two text inputs
        param : inputtext-1,inputtext-2
        return : differed text, bool
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
                        out_path = args[0].split(";")[0]
                        if(not out_path.startswith("{")):
                            output_path = out_path
                    if ( len(input_val) == 3 and (input_val[2] != None or input_val[2] != '' )) : res_opt = input_val[2].strip().lower()
                    output_res = self.compare_texts(inputtext1,inputtext2)
                    if ( output_res ):
                        flg = True
                        try:
                            num_diff,ch_lines = self.get_diff_count(output_res)
                            if(num_diff):
                                logger.print_on_console("The number of differences in compare_inputs are: ",num_diff)
                            if ( res_opt == 'selective' or res_opt == 'all') :
                                log.info("Result to be displayed is : " + str(res_opt))
                                logger.print_on_console("Result to be displayed is : " + str(res_opt))
                                if (res_opt == 'selective') : output_res = ch_lines
                            output_res = '\n'.join(output_res)
                            if(output_path):
                                if(os.path.isfile(output_path) or os.path.exists(os.path.dirname(output_path))):
                                    with open(output_path,'w') as f:
                                        f.write(output_res)
                                else:
                                    err_msg='Wrong file path entered'
                                    flg = False
                        except Exception as ex:
                            err_msg = ("Exception occurred while writing to output file in compare_inputs : "+str(ex))
                            log.error( err_msg )
                            logger.print_on_console( "Error occured while writing to output file in Compare Inputs" )
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
        purpose : beautifies/pretifies a file/string of type json or xml
        param : inputpath,file type
        return : beautified text, bool
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
                    out_path = args[0].split(";")[0]
                    if(not out_path.startswith("{")):
                        output_path = out_path
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
                                with open(output_path,'w') as f:
                                    f.write(beautified_output)
                            else:
                                flg = False
                                err_msg='Wrong file path entered'
                    except Exception as ex:
                        err_msg = ("Exception occurred while writing to output file in beautify_file : "+str(ex))
                        log.error( err_msg )
                        logger.print_on_console( "Error occured while writing to output file in Beautify File" )
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
        purpose : compares two files
        param : inputPath-1,inputPath-2
        return : differed text, bool
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
                    out_path = args[0].split(";")[0]
                    if(not out_path.startswith("{")):
                        output_path = out_path
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
                                if(output_path):
                                    if(os.path.exists(output_path) or os.path.exists(os.path.dirname(output_path))):
                                        with open(output_path,'w') as f:
                                            f.write(output_res)
                                    else:
                                        err_msg = generic_constants.FILE_NOT_EXISTS
                                        flg = False
                            except Exception as ex:
                                err_msg = ("Exception occurred while writing to output file in compare_file : "+str(ex))
                                log.error( err_msg )
                                logger.print_on_console( "Error occured while writing to output file in Compare File" )
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
            import traceback
            traceback.print_exc()
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
            if(text1_lines==text2_lines):
                logger.print_on_console( "Inputs are same" )
                log.info( "Inputs are same" )
                out = list(difflib.Differ().compare(text1_lines, text2_lines))
            else:
                out = list(difflib.Differ().compare(text1_lines, text2_lines))
        except Exception as e:
            logger.print_on_console("Exception occurred in compare_texts while comparing two texts")
            log.error("Exception occurred in compare_texts while comparing two texts"+str(e))
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
            text1_lines = xml_input1.splitlines()
            text2_lines = xml_input2.splitlines()
            if(text1_lines==text2_lines):
                logger.print_on_console( "Inputs are same" )
                log.info( "Inputs are same" )
                out = main.diff_files(xml_input1, xml_input2,diff_options={'fast_match': False},formatter=formatting.XMLFormatter(normalize=formatting.WS_BOTH)).split("\n")
            else:
                out = main.diff_files(xml_input1, xml_input2,diff_options={'fast_match': False},formatter=formatting.XMLFormatter(normalize=formatting.WS_BOTH)).split("\n")
        except Exception as e:
            logger.print_on_console("Exception occurred in compare_xmls while comparing two texts")
            log.error("Exception occurred in compare_xmls while comparing two texts"+str(e))
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
            print('Entered xpath is incorrect : ',search)
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