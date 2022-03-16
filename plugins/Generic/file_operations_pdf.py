#-------------------------------------------------------------------------------
# Name:        file_operations_pdf
# Purpose:     comparison between two xml data, in respective functions
#
# Author:      divyansh.singh
#
# Created:     11-09-2020
# Copyright:   (c) divyansh.singh 2020
# Licence:     <your licence>

import logger
import generic_constants
import constants
import json
import difflib
import tempfile
import os
import string
import random
import dynamic_variable_handler
import constant_variable_handler
import logging
import PyPDF2
import difflib
import itertools
import cv2
import numpy as np
import imutils
import fitz
import re
import copy
import time
from PIL import Image
from constants import *
import subprocess
import readconfig
if SYSTEM_OS == 'Windows':
    import win32api,win32gui,win32print
    from pywinauto import Application
    import pywinauto
    import psutil
log = logging.getLogger('file_operations_pdf.py')
from pytesseract import pytesseract
TESSERACT_PATH = os.environ["AVO_ASSURE_HOME"] + '/Lib/Tesseract-OCR'
TESSERACT_PATH_EXISTS = os.path.isdir(TESSERACT_PATH)

class FileOperationsPDF:
    def __init__(self):
        self.DV = dynamic_variable_handler.DynamicVariables()
        self.CV = constant_variable_handler.ConstantVariables()
        pass

    def verify_content(self,input_path,pagenumber,content):
        """
        def : verify_content
        purpose : verifies whether the content is given pagenumber of pdf file
        param : input_path,pagenumber,content
        return : bool

        """
        status=False
        err_msg=None
        try:
            log.debug('Verifying content of pdf file')
            pdf_content=self.get_content(input_path,pagenumber,content,'_internal_verify_content')
            log.debug('pdf_content is '+str(pdf_content))
            if content in pdf_content.replace('\n',''):
                status=True
            else:
                err_msg=generic_constants.CONTENT_NOT_PRESENT
        except IOError:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'verifying PDF content'+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,err_msg

    def compare_content(self,input_val,args):
        """
        def : compare_content
        purpose : compares_content of two PDFs
        param : list[], list[]
        """
        status = constants.TEST_RESULT_FAIL
        result = constants.TEST_RESULT_FALSE
        err_msg = None
        value = constants.OUTPUT_CONSTANT
        res_opt = 'all'
        type_opt = 'pagewise'
        select_input = False
        type_input = False
        output_path = None
        try:
            #check for permissable number of inputs
            if len(input_val) == 2 or len(input_val) == 3 or len(input_val) == 4:
                #extract filepaths of the PDFs to be compared
                filePathA = input_val[0]
                filePathB = input_val[1]
                #logic to check wether output variable is a filepath, dynamic variable contating filepath or empty dynamic variable
                if args:
                    if os.path.exists(args):
                        output_path = args
                    elif str(args.split(";")[0]).startswith("{") and str(args.split(";")[0]).endswith("}"):
                        path_temp = args.split(";")[0].replace("{","").replace("}","")
                        if os.path.exists(path_temp):
                            output_path = path_temp
                        else:
                            out_path = self.DV.get_dynamic_value(args.split(";")[0])
                            if ( out_path ): output_path = out_path
                    elif str(args.split(";")[0]).startswith("_") and str(args.split(";")[0]).endswith("_"):
                        path_temp = args.split(";")[0].replace("_","").replace("_","")
                        if os.path.exists(path_temp):
                            output_path = path_temp
                        else:
                            out_path = self.CV.get_constant_value(args.split(";")[0])
                            if ( out_path ): output_path = out_path
                    else:
                        output_path = args.split(";")[0]
                #check for optional input values
                if len(input_val) == 2:
                    select_input = True
                    type_input = True
                #check wether third optional input if it exists is empty string or selective or all
                if len(input_val) >= 3 and input_val[2] != None  and (input_val[2].strip() == 'selective' or input_val[2].strip() == "all" or input_val[2].strip() == ""):
                    if input_val[2] != "":
                        res_opt = input_val[2].strip().lower()
                    select_input = True
                #check wether fourth optional input if it exists is empty string or pagewise or complete
                if len(input_val) == 4 and input_val[3] != None and (input_val[3].strip() == 'pagewise' or input_val[3].strip() == "complete" or input_val[3].strip() == ""):
                    if input_val[3] != "":
                        type_opt = input_val[3].strip().lower()
                    type_input = True
                elif len(input_val) == 3:
                    type_input = True
                #check wether both filepath exists and wether the optional inputs are valid
                if os.path.isfile(filePathA) and os.path.isfile(filePathB) and select_input and type_input:
                    if os.path.getsize(filePathA)>0 and os.path.getsize(filePathB)>0:
                        fileNameA, fileExtensionA = os.path.splitext(filePathA)
                        fileNameB, fileExtensionB = os.path.splitext(filePathB)
                        #check wether both files are PDF
                        if fileExtensionB.lower() == ".pdf" and fileExtensionA.lower() == ".pdf":
                            pdf1 = open(filePathA, 'rb')
                            pdf2 = open(filePathB, 'rb')
                            #creating a pdf reader object via PYPDF2 for text comparison
                            pdfReader1 = PyPDF2.PdfFileReader(pdf1, overwriteWarnings=False)
                            pdfReader2 = PyPDF2.PdfFileReader(pdf2, overwriteWarnings=False)
                            #opening documents via fitz for image comparison
                            doc1 = fitz.open(filePathA)
                            doc2 = fitz.open(filePathB)
                            #check which comparison (pagewise/complete) is requested
                            if type_opt == 'pagewise':
                                output_res_dict = self.compare_pagewise(pdfReader1,pdfReader2,res_opt,doc1,doc2)
                                output_res = self.convert_output_to_list(output_res_dict)
                            if type_opt == 'complete':
                                output_res_dict = self.compare_complete(pdfReader1,pdfReader2,res_opt,doc1,doc2)
                                output_res = self.convert_output_to_list(output_res_dict)
                            #closing all reader objects
                            pdf1.close()
                            pdf2.close()
                            doc1.close()
                            doc2.close()
                            if output_res is not None:
                                #mark the test case to be executed successfully
                                flg = True
                                optFlg = True
                                try:
                                    log.info("Result to be displayed is : " + str(res_opt))
                                    logger.print_on_console("Result to be displayed is : " + str(res_opt))
                                    #checking wether extractText of pyPDF2 failed
                                    if "error" in output_res_dict and output_res_dict['error']:
                                        logger.print_on_console("Pages empty or text not supported in comparePDFs")
                                    elif len(output_res):
                                        logger.print_on_console("The number of pages with differences in comparePDFs are: ",self.get_number_diff_pages(output_res_dict))
                                    else:
                                        logger.print_on_console("No Difference between inputs in comparePDFs")
                                    #checking if output path exists and is not an instance of some other type not supported
                                    if output_path and not isinstance(output_path,list):
                                        #checking wether path exists
                                        if isinstance(output_path,str) and (os.path.exists(output_path) or os.path.exists(os.path.dirname(output_path))):
                                            log.debug( "Writing the output of comparePDFs to file : " + str(output_path) )
                                            logger.print_on_console( "Writing the output of comparePDFs to file.")
                                            #writing to file therefore no need to write to dynamic variable
                                            optFlg = False
                                            with open(output_path,'w') as f:
                                                f.write(str(output_res))
                                        else:
                                            logger.print_on_console(generic_constants.INVALID_OUTPUT_PATH)
                                except Exception as ex:
                                    err_msg = ("Exception occurred while writing to output file in compareFile : " + str(ex))
                                    log.debug( err_msg )
                                    flg = False
                                if(flg):
                                    status = constants.TEST_RESULT_PASS
                                    result = constants.TEST_RESULT_TRUE
                                    log.info("Comparision of files completed")
                                    logger.print_on_console("Warning!:Table content within PDFs is not supported, It might show inconsistencies in result.")
                                    #checking wether the output is to be written to dyanamic variable or not
                                    if( optFlg ):
                                        value = output_res
                        else:
                            err_msg = generic_constants.INVALID_FILE_FORMAT
                    else:
                        err_msg = 'One or more files are empty'
                else:
                    if not select_input:
                        err_msg = "Invalid third input"
                    elif not type_input:
                        err_msg = "Invalid fourth input"
                    else:
                        err_msg = generic_constants.FILE_NOT_EXISTS
            else:
                err_msg = 'Invalid number of inputs'
            if ( err_msg != None ):
                log.error(err_msg)
                logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = ("Exception occurred in comparePDFs while comparing two files"+str(e))
            log.error( err_msg )
            logger.print_on_console( "Error occured in comparePDFs" )
        return status, result, value, err_msg

    def compare_pagewise(self,pdfReader1,pdfReader2,opt,doc1,doc2):
        """
        def : compare_pagewise
        purpose : compares_content of two PDFs pagewise, (one to one comparison)
        param : PDF reader object for PDF1, PDF reader object for PDF2, optional value (all/selective), fitz reader PDF1, fitz reader PDF2
        return : {page_number:{"error":string,"images":[int,int,int],"comparison_result":string},"error":bool,page_number{},page_number{}}
        """
        result = {}
        #iterate over the pages of first PDF
        for i in range(pdfReader1.numPages):
            #create result object
            result[i + 1] = {}
            result[i+1]['images'] = {}
            #extract text in the page PDF1
            test_str1 = pdfReader1.getPage(i).extractText().replace('\n',"")
            total_char1 = len(test_str1)
            #check if the page is empty or extractText failed, (fail in case of scattered text )
            if total_char1 == 0 or test_str1 == " ":
                #continue to next page after storing error for this page
                result['error'] = True
                result[i + 1]["error"] = "Page empty or unsupported text"
                result[i + 1]["images"] = self.compare_images(doc1,doc2,i,i)
                continue
            #check wether the current page index (page number) exists in the second PDF
            if pdfReader2.numPages <= i:
                #page index does not exist in PDF2 hence the entire content of this page from PDF1 was deleted
                result[i + 1]["comparison_result"] = "||---" + pdfReader1.getPage(i).extractText().replace('\n',"") + "---||"
                result[i + 1]["images"] = self.compare_images(doc1,None,i,i)
                continue
            #compare images in the page
            result[i + 1]["images"] = self.compare_images(doc1,doc2,i,i)
            #extract text in the page from PDF2
            test_str2 = pdfReader2.getPage(i).extractText().replace('\n',"")
            total_char2 = len(test_str2)
            #check wether any text is present in the current index (page number) of PDF2
            if total_char2 == 0 or len(test_str2.strip()) == 0:
                #No text found on current page in PDF2, therefore the page is blank and entire textual content of PDF1 was deleted
                result[i + 1]["comparison_result"] = "||---" + pdfReader1.getPage(i).extractText().replace('\n',"") + "---||"
                result[i + 1]["images"] = self.compare_images(doc1,None,i,i)
                continue
            test_str1_copy = test_str1
            #extract all the mathcing sequence from both the pages being compared from PDF1 and PDF2
            matches = difflib.SequenceMatcher(None, test_str1, test_str2).get_matching_blocks()
            result[i + 1]["matches"] = []
            match_arr = []
            matched_count = 0
            #iterating over all the matched character sequences (white spaces also considered)
            for match in matches:
                matched = test_str1_copy[match.a:match.a + match.size]
                matched_count = len(matched) + matched_count
                match_arr.append(matched)
            #get comparison result in the fomr of ||+++ +++|| / ||--- ---|| from get_formatted_comparison_result
            result[i + 1]["comparison_result"] = self.get_formatted_comparison_result(test_str1,test_str2,match_arr,opt)
            #get matched percentage, for future use
            result[i + 1]["matchedSource"] = matched_count/total_char1*100
            result[i + 1]["matchedDest"] = matched_count/total_char2*100
        #check wether PDF2 is larger than PDF1 and hence needs to be iterated
        if pdfReader1.numPages < pdfReader2.numPages:
            #iterate over PDF2 for every extra page
            for i in range(pdfReader1.numPages,pdfReader2.numPages):
                result[i + 1] = {}
                #get text in the extra page from PDF2
                test_str2 = pdfReader2.getPage(i).extractText().replace('\n',"")
                total_char2 = len(test_str2)
                #check wether extractText failed
                if total_char2 == 0 or test_str2 == " ":
                    result['error'] = True
                    result[i + 1]['error'] = "Page empty or unsupported text"
                    result[i + 1]["images"] = self.compare_images(None,doc2,i,i)
                    continue
                #since this is an extra page the entire content in this page is addition
                result[i + 1]["comparison_result"] = "||+++" + test_str2 + "+++||"
                result[i + 1]["images"] = self.compare_images(None,doc2,i,i)
        return result

    def get_formatted_comparison_result(self,pageA,pageB,match_arr,opt):
        """
        def : get_formatted_comparison_result
        purpose : returns the difference in a page in the format of ||+++ +++|| / ||--- ---||
        param : str(source page),  str(target page), [str](list of all the matching character sequences), optional argument (selective/all)
        return : str

        """
        #define pattern where an addition or subtraction can be found
        pattern = '--cEND-- (.*?) --cSTART--'
        #to be added/removed when common sequence ends, reffered as end
        end = "--cEND-- "
        #to be added/removed when common sequence starts, reffered as start
        start = " --cSTART--"
        #iterate over all common charcter sequences
        add_index = None
        for cmn_str in match_arr:
            #check if the sequence is not empty string
            if cmn_str != '' and cmn_str != ' ' and len(cmn_str) > 1:
                #enclose common character sequence in start end identifiers
                comman_match = start + cmn_str + end
                #replace the common character sequence with the same sequence enclosed in identifiers for both the PDFs
                pageA = pageA.replace(cmn_str, comman_match)
                pageB = pageB.replace(cmn_str, comman_match)
        #all the additions are values between end and start identifiers in the page of PDF2
        #find all the character sequence between the end () start pattern
        add = re.findall(pattern,pageB)
        #all the deletions are values between end and start identifiers in the page of PDF1
        #find all the character sequence between the end () start pattern
        dele = re.findall(pattern,pageA)
        #iterate over all the deletions
        for deletion in dele:
            #for each deletion found replace (end deletion start) pattern witth ||--- deletion ---|| pattern
            pageA = pageA.replace(end + deletion + start," ||---" + deletion + " ---|| ")
        #iterate over all additions
        for addition in add:
            if addition == "":
                continue
            #get index where this addition is found
            find_str = addition + start
            index = pageB.find(find_str)
            #find all common character sequence preceeding this addition
            prev_matches = re.findall('--cSTART--(.*?)--cEND--',pageB[:index + len(find_str)])
            #find all common character sequences proceeding this addition
            post_matches = re.findall('--cSTART--(.*?)--cEND--',pageB[index + len(find_str):])
            #delete this addition to avoid conflicts in proceeding iterations
            pageB = pageB[:index + len(find_str)].replace(addition,"") + pageB[index+len(find_str):]
            try:
                #The deletion occurs after the last matching character sequence hence it has to be displayed after this sequence in page of PDF1
                #iterate over all occurences of last matching character sequence
                for i in re.finditer(prev_matches[len(prev_matches) -1],pageA):
                    #check if proceeding common character sequences exist and
                    # if the index of last preceeding common charcter sequence is less then the proceeding common sequence
                    if not post_matches or (post_matches and i.start() < pageA.find(post_matches[0])):
                        add_index = i.start()  + len(prev_matches[len(prev_matches) - 1])
                if (add_index == None):
                    add_index = pageA.find(prev_matches[len(prev_matches) - 1]) + len(prev_matches[len(prev_matches) - 1])
            except Exception as e:
                #exception occurs because the last precceding common character sequence has special characters not supported by regex
                log.info("Un accepted regex caharchter")
                #find the first occurence of last precceding common character sequence
                add_index = pageA.find(prev_matches[len(prev_matches) - 1]) + len(prev_matches[len(prev_matches) - 1])
            #add addition after last precceding common character sequence of page of PDF1
            pageA = pageA[:add_index] + " ||+++ " + addition + " +++|| " + pageA[add_index:]
        if opt == 'selective':
            #remove all comman character sequences if optional arugment is slective
            for cmn_str in match_arr:
                if cmn_str != "" and cmn_str != " ":
                    pageA = pageA.replace(cmn_str,"")
        #remove start and end identifiers from result
        pageA = pageA.replace(start , "")
        pageA = pageA.replace(end, "")
        return pageA

    def get_number_diff_pages(self,comparison_result):
        """
        def : get_number_diff_pages
        purpose : returns the number of different pages found in comparePDFs
        param : {{}}
        return : int

        """
        difference_found = 0
        #iterate over result and check if element contains addition (+++) or deletions (---)
        for page in comparison_result:
            if comparison_result[page]['comparison_result'].find("+++") != -1 or comparison_result[page]['comparison_result'].find("---") != -1:
                difference_found += 1
        return difference_found

    def convert_output_to_list(self,dictionary):
        """
        def : convert_output_to_list
        purpose : converts comparison result form comparePDFs to list form dictionary
        param : {{}}
        return : [[]]

        """
        result = []
        #iterate over every page in dictionary and append to list
        for page in dictionary:
            #checke wether keys exist and append
            if page == "error":
                continue
            temp_page = []
            current_page = dictionary[page]
            temp_page.append(page)
            if "error" in current_page:
                temp_page.append(current_page["error"])
                result.append(temp_page)
                if "images" in current_page:
                    temp_page.append(current_page["images"])
                continue
            temp_page.append(current_page["comparison_result"])
            temp_page.append(current_page["images"])
            if "pageMatch" in  current_page:
                temp_page.append(current_page["pageMatch"])
            if "mathces" in current_page:
                temp_page.append(current_page["matches"])
            result.append(temp_page)
        return result

    def compare_complete(self,pdfReader1,pdfReader2,opt,doc1,doc2):
        sim = {}
        result = {}
        pageMatched = {}
        #iterate over every page in PDF1
        for i in range(pdfReader1.numPages):
            j = 0
            result[i + 1] = {}
            result[i+1]['images'] = {}
            #declare that this page is not matched to any page from PDF2
            lastMathc = -1
            #iterate over every page in PDF2
            while j < pdfReader2.numPages:
                #check wether if this page from PDF2 is already matched with some other page or not
                if(j in pageMatched and pageMatched[j] == 1):
                    j = j + 1
                    continue
                #declare this page in PDF2 has not been matched yet
                pageMatched[j] = -1
                test_str2 = pdfReader2.getPage(j).extractText().replace('\n',"")
                total_char2 = len(test_str2)
                test_str1 = pdfReader1.getPage(i).extractText().replace('\n',"")
                total_char1 = len(test_str1)
                #check wether extractText failed
                if total_char1 == 0 or test_str1 == " ":
                    lastMathc = -99
                    result['error'] = True
                    result[i + 1]["error"] = "Page empty or unsupported text"
                    result[i + 1]["images"] = [-1,-1,-1]
                    break
                test_str1_copy = test_str1
                matched_count = 0
                matches = []
                #get all mathcing character sequences between both pages of PDF1 and PDF2 (page i of PDF1 compared to page j of PDF2)
                match_page = difflib.SequenceMatcher(None, test_str1, test_str2).get_matching_blocks()
                for match in match_page:
                    matched = test_str1_copy[match.a:match.a + match.size]
                    matched_count = len(matched) + matched_count
                    matches.append(matched)
                #check wether the current page from PDF2 has the highest matching percentage from previously compared pages
                if total_char1 != 0 and (i not in sim or sim[i] < matched_count/total_char1*100):
                    #check wether matching percentage is greater than 20
                    if matched_count/total_char1*100 > 20:
                        #add comparison result to output
                        sim[i] =  matched_count/total_char1*100
                        result[i + 1]["matchedSource"] = matched_count/total_char1*100
                        result[i + 1]["matchedDest"] = matched_count/total_char2*100
                        result[i + 1]["pageMatch"] = j + 1
                        result[i + 1]['images'] = self.compare_images(doc1,doc2,i,j)
                        pageMatched[lastMathc] = -1
                        lastMathc = j
                        pageMatched[j] = 1
                        result[i + 1]["comparison_result"] = self.get_formatted_comparison_result(test_str1,test_str2,matches,opt)
                j += 1
            if lastMathc is -1:
                #since the current page from PDF1 does not match to any page of PDF2 mark the entire content of this page as deleted
                result[i + 1]["matchedSource"] = -1
                result[i + 1]["matchedDest"] = -1
                result[i + 1]["pageMatch"] = -1
                result[i + 1]["comparison_result"] = "||---" + test_str1 + "---||"
                result[i + 1]["images"] = self.compare_images(doc1,None,i,j)

        j = 0
        i = pdfReader1.numPages + 1
        #iterate over entire PDF2 and check wether ther are extra/unmatched pages ind PDF2
        while j < pdfReader2.numPages:
            #check wether current page has mathced with any page in PDF1
            if j in pageMatched and pageMatched[j] == 1:
                j += 1
                continue
            test_str2 = pdfReader2.getPage(j).extractText().replace('\n',"")
            result[i] = {}
            #check wether extractText failed
            if  len(test_str2) == 0 or test_str2 == " ":
                result['error'] = True
                result[i]['error'] = "Page empty or unsupported text"
                result[i]["images"] = [-1,-1,-1]
                result[i]["pageMatch"] = -1
                j += 1
                i += 1
                continue
            result[i]["matchedSource"] = -1
            result[i]["images"] = self.compare_images(None,doc2,j,j)
            result[i]["matchedDest"] = -1
            result[i]["pageMatch"] = j+1
            #mark entire content as addition since this an extra/unmatched page
            result[i]["comparison_result"] = "||+++" + test_str2 + "+++||"
            j += 1
            i += 1

        return result

    def compare_images(self,doc1,doc2,index1,index2):
        """
        def : compare_images
        purpose : in order compares images from two pages and verifies if identical or not
        param : fitz PDF1,fitz PDF2, int (page number of PDF1), int (page number of PDF2)
        return : [int,int,int]

        """
        result = [0,0,0]
        i = 1
        #check if page in PDF1 exists
        if doc1 is None:
            #all images in this page deleted since no source page to compare
            result[0] = len(doc2.getPageImageList(index2))
            return result
        if doc2 is None:
            result[1] = len(doc1.getPageImageList(index1))
            return result
        #iterate over all the images in both the page in order
        for (img1,img2) in itertools.zip_longest(doc1.getPageImageList(index1),doc2.getPageImageList(index2)):
            if img1 and img2:
                xref1 = img1[0]
                xref2 = img2[0]
                pix1 = fitz.Pixmap(doc1, xref1)
                pix2 = fitz.Pixmap(doc2, xref2)
                #check if images are identical
                if self.subtract_and_check_if_identical(pix1,pix2):
                    result[2] += 1
                    continue
                else:
                    #since not identical one image is added and one is deleted
                    result[0] += 1
                    result[1] += 1
                    continue
            #extra image in page of pdf1 not found in pdf2 hence deleted
            elif img1 is None:
                result[0] += 1
            #extra image in page of pdf2 not found in pdf1 hence added
            elif img2 is None:
                result[1] += 1

        return result

    def subtract_and_check_if_identical(self,img1,img2):
        """
        def : subtract_and_check_if_identical
        purpose : verifies if two images are identical or not
        param : np array (image 1), np array (image 2)
        return : bool

        """
        img1 = self.pix2np(img1)
        img2 = self.pix2np(img2)
        #check if the two images are identical in shape and size
        if img1.shape != img2.shape:
            #images are different since they have different dimensions
            return False
        #subtract and check if two images are identical
        difference = cv2.subtract(img1, img2)
        result = not np.any(difference)
        return result

    def locate_image(self,input_val,args):
        """
        def : locate_image
        purpose : find all location of a template image in a PDF

        """
        status = constants.TEST_RESULT_FAIL
        result = constants.TEST_RESULT_FALSE
        err_msg = None
        value = constants.OUTPUT_CONSTANT
        output_path = None
        try:
            #check if inputs are permissible
            if len(input_val) == 2:
                #get filepath of PDF and template image
                filePathA = input_val[0]
                filePathB = input_val[1]
                #logic to check wether output variable is a filepath, dynamic variable contating filepath or empty dynamic variable
                if args:
                    if os.path.exists(args):
                        output_path = args
                    if str(args.split(";")[0]).startswith("{") and str(args.split(";")[0]).endswith("}"):
                        path_temp = args.split(";")[0].replace("{","").replace("}","")
                        if os.path.exists(path_temp):
                            output_path = path_temp
                        else:
                            out_path = self.DV.get_dynamic_value(args.split(";")[0])
                            if ( out_path ): output_path = out_path
                    elif str(args.split(";")[0]).startswith("_") and str(args.split(";")[0]).endswith("_"):
                        path_temp = args.split(";")[0].replace("_","").replace("_","")
                        if os.path.exists(path_temp):
                            output_path = path_temp
                        else:
                            out_path = self.CV.get_constant_value(args.split(";")[0])
                            if ( out_path ): output_path = out_path
                    else:
                        output_path = args.split(";")[0]
                #check wether both filepath exists
                if os.path.isfile(filePathA) and os.path.isfile(filePathB):
                    if os.path.getsize(filePathA)>0 and os.path.getsize(filePathB)>0:
                        fileNameA, fileExtensionA = os.path.splitext(filePathA)
                        fileNameB, fileExtensionB = os.path.splitext(filePathB)
                        #check if input 1 is pdf and input 2 is PNG
                        if fileExtensionA.lower() == ".pdf" and fileExtensionB.lower() == ".png":
                            #get output and total occurencs of tempate image found
                            output_res,total_found = self.get_thresholded_similar_images(filePathA,filePathB)
                            if output_res is not None:
                                #mark test step as successfull
                                flg = True
                                optFlg = True
                                try:
                                    if total_found > 0:
                                        logger.print_on_console("Total number of image occurances are: ",total_found)
                                    else:
                                        logger.print_on_console("No image occurances in PDF")
                                    #checking if output path exists and is not an instance of some other type not supported
                                    if output_path and not isinstance(output_path,list):
                                        if isinstance(output_path, str) and (os.path.exists(output_path) or os.path.exists(os.path.dirname(output_path))):
                                            log.debug( "Writing the output of PDFimageCompare to file : " + str(output_res) )
                                            logger.print_on_console( "Writing the output of PDFimageCompare to file.")
                                            #writing to file therefore no need to write to dynamic variable
                                            optFlg = False
                                            with open(output_path,'w') as f:
                                                f.write(str(output_res))
                                        else:
                                            logger.print_on_console(generic_constants.INVALID_OUTPUT_PATH)
                                except Exception as ex:
                                    err_msg = ("Exception occurred while writing to output file in compareFile : " + str(ex))
                                    log.debug( err_msg )
                                    flg = False
                                if(flg):
                                    status = constants.TEST_RESULT_PASS
                                    result = constants.TEST_RESULT_TRUE
                                    log.info("Comparision of files completed")
                                    if( optFlg ):
                                        value = output_res
                            else:
                                #output none hence the template image provided is not accurate enough, throw tempalte error
                                err_msg = generic_constants.TEMPLATE_ERR
                        else:
                            err_msg = generic_constants.INVALID_FILE_FORMAT
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
            err_msg = ("Exception occurred in findImageInPDF"+str(e))
            log.error( err_msg )
            logger.print_on_console( "Error occured in findImageInPDF" )
        return status, result, value, err_msg

    def pix2np(self,pix):
        """
        def : pix2np
        purpose : convert pixmap (obtained from fitz) to np array
        param : pixmap
        return : np array

        """
        im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        y1 = np.ascontiguousarray(im[..., [2, 1, 0]])  # rgb to bgr
        return y1

    def get_thresholded_similar_images(self,filePathA,filePathB):
        """
        def : get_thresholded_similar_images
        purpose : find occurences of template image after calculating similarities in each page
        param : str (filePath to PDF),str (filepath to PNG)
        return : [[]]

        """
        #open PDF with fitz
        doc1 = fitz.open(filePathA)
        #read template image with cv2
        template = cv2.imread(filePathB)
        output_res = {}
        output_res['total_count'] = 0
        output_res['abs_max'] = 0
        #iterate over PDF1
        for i in range(0,doc1.pageCount):
            output_res[i + 1] = {}
            #convert page to pixmap
            imTemp = doc1.loadPage(i).getPixmap(alpha=False)
            #convert pixmap to np array
            image = self.pix2np(imTemp)
            value = [255,255,255]
            #padd the image of the page
            image = cv2.copyMakeBorder(image,100,100,100,100,cv2.BORDER_CONSTANT,None,value)
            #get similarity and location of template image found page
            output_res[i + 1] ,output_res["abs_max"] = self.compare(image,template,output_res['abs_max'])
        #check if the maximum similarity obtained is greater than 30 percentage
        if output_res["abs_max"] < 0.29:
            #fail the test step due to poor template image
            return None, 0
        output = []
        log_output = []
        total_found = 0
        #iterate over all the pages in output
        for image in output_res:
            if not isinstance(image,int):
                continue
            #check wether the similarity found in this page is equal to or less than 2% of the max similarity found
            if output_res[image]['max_corr'] > output_res['abs_max'] - 0.02 and output_res[image]['max_corr'] <= output_res['abs_max']:
                #cv2.imwrite("result"+str(image)+".png",output_res[image]["image"])
                #tempate image found, add to to output, increase total found by 1
                page = []
                page.append(image)
                page.append(output_res[image]['count'])
                total_found += output_res[image]['count']
                page.append(output_res[image]['location'])

            else:
                #template not found
                page = []
                page.append(image)
                page.append(0)
                page.append([])
            output.append(page)
            #deep copy result for page and add similarity percentage for logging
            page_copy = copy.deepcopy(page)
            page_copy.append(output_res[image]["correlations"])
            log_output.append(page_copy)
        #log ouptut containing similarity percentage for reference
        log.info("Result of findImageInPDF"+ str(log_output))
        return output,total_found

    def compare(self,image,template,abs_max):
        template = cv2.Canny(template, 50, 200)
        location_dict = {(1,1):"bottom-left",(1,2):"bottom-center",(1,3):"bottom-right",(2,1):"middle-left",(2,2):"middle-center",(2,3):"middle-right",(3,1):"top-left",(3,2):"top-center",(3,3):"top-right"}
        (tH, tW) = template.shape[:2]
        gray = image
        found = None
        results = {}
        count = 0
        max_val = 0
        correlations = []
        location = []
        # loop over the scales of the image
        for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            # resize the image according to the scale, and keep track
            # of the ratio of the resizing
            resized = imutils.resize(image, width = int(gray.shape[1] * scale))
            r = image.shape[1] / float(resized.shape[1])
            # if the resized image is smaller than the template, then break
            # from the loop
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break
            edged = cv2.Canny(resized, 50, 200)
            result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
            # if we have found a new maximum correlation value, then update
            # the bookkeeping variable
            if found is None or maxVal > found[0]:
                count = 1
                location = []
                correlations = []
                correlations.append(round(max_val*100,2))
                location.append(maxLoc)
                found = (maxVal, maxLoc, r)
                xx = cv2.minMaxLoc(result)
                max_val = maxVal
            elif maxVal == found[0]:
                count += 1
                correlations.append(round(max_val*100,2))
                location.append(maxLoc)
            #check if new absolute max (max similarity of all pages compared so far) is found
            if maxVal > abs_max:
                abs_max = maxVal
        # unpack the bookkeeping variable and compute the (x, y) coordinates
        # of the bounding box based on the resized ratio
        (_, maxLoc, r) = found
        dimensions = image.shape
        r1,r2 = dimensions[0]/3-50,dimensions[0]/1.5 - 50
        c1,c2 = dimensions[1]/3-50,dimensions[1]/1.5 - 50
        #intialise the location as top left
        x,y = 1,3
        results['location'] = []
        for found in location:
            #check if the x coordinate (column) is left|center|right
            if (found[0]+150)/dimensions[0] > 1/3:
                x = 2
                if (found[0]+150)/dimensions[0] >2/3:
                    x = 3
            #check if the y coordinate (row) id top|middle|bottom
            if found[1]/dimensions[1] > 1/3:
                y = 2
                if found[1]/dimensions[1] >2/3:
                    y = 1
            #store location
            results["location"].append(location_dict[y,x])
        #make a bounding box on the found location, for future use
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
        #results["image"] = image
        results["max_corr"] = max_val
        results['correlations'] = correlations
        results['count'] = count
        return results,abs_max

    def get_content(self,input_path,pagenumber,*args):
        """
        def : get_content
        purpose : return the content present in given pagnumber of pdf file
        param : input_path1,input_path2
        return : bool

        """
        status=False
        content=None
        err_msg=None
        form_type='Adobe LiveCycle Forms 7.2'
        from PyPDF2 import PdfFileReader, PdfFileWriter
        import fitz
        try:
             log.debug('Get the content of pdf file: '+str(input_path)+','+str(pagenumber))
             doc=fitz.open(input_path)
             pagenumber=int(pagenumber)-1
             if pagenumber<doc.pageCount:
                page = doc[pagenumber]
                content=page.getText()
                ## content=content.encode('utf-8')
                if len(args) == 0:
                    log.info('Content is ')
                    log.info(content)
                    status=True
                if len(args)>1 and args[1]=='_internal_verify_content':
                    return content
                if len(args) >= 2 and not (args[0] is None and args[1] is None):
                    start=args[0].strip()
                    end=args[1].strip()
                    startIndex=0
                    endIndex=len(content)
                    log.info('Start string: '+str(start)+' End string: '+str(end))
                    if not start is '':
                        if content.find(start) == -1:
                            content = None
                            err_msg="Start string not found in the content"
                        else:
                            startIndex=content.find(start)+len(start)
                    if not end is '':
                        if content.find(end) == -1:
                            content = None
                            err_msg="End string not found in the content"
                        else:
                            endIndex=content.find(end)
                    if not(err_msg):
                        content=content[startIndex:endIndex]
                        log.info('Content between Start and End string is ')
                        ## logger.print_on_console('Content between Start and End string is ')
                        log.info(content)
                        status=True
                elif len(args)==1:
                    # with open(args[0],'w') as file:
                    #     file.write(content)
                    #     file.close()
                    start=args[0].strip()
                    startIndex=0
                    endIndex=len(content)
                    log.info('Start string: '+str(start))
                    if not start is '':
                        if content.find(start) == -1:
                            content = None
                            err_msg="Start string not found in the content"
                        else:
                            startIndex=content.find(start)+len(start)
                    if not(err_msg):
                        content=content[startIndex:endIndex]
                        log.info('Content after Start string is ')
                        log.info(content)
                        status=True
                if len(args)>2 and args[2] in ['image','all']:
                    logger.print_on_console( "Retreving Text of all images within .pdf file. Please wait..." )
                    #for i in range(len(doc)):
                    log.debug( 'Image count : ' + str(len(doc.getPageImageList(pagenumber))) + ' on page : ' + str(pagenumber+1) )
                    if(TESSERACT_PATH_EXISTS):
                        output_res = []
                        img_count = 0
                        for img in doc.getPageImageList(pagenumber):
                            img_count = img_count + 1
                            xref = img[0]
                            pix = fitz.Pixmap(doc, xref)
                            pix.writePNG("p%s-%s.png" % (pagenumber, xref))
                            image = cv2.imread(str("p%s-%s.png" % (pagenumber, xref)),1)
                            rez_image = cv2.resize(image,(0,0),fx=5,fy=5)
                            gray_img = cv2.cvtColor(rez_image, cv2.COLOR_BGR2GRAY)
                            filter_img = cv2.medianBlur(gray_img, 5)
                            thresh_img = cv2.threshold(filter_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                            filename = str(int(time.time()))+".png"
                            cv2.imwrite(filename, thresh_img)
                            try:
                                #---------------------------------------------------------------taking Tessaract path for respective OS
                                if constants.SYSTEM_OS != 'Darwin':
                                    pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract'
                                    os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/tessdata'
                                else:
                                    pytesseract.tesseract_cmd = TESSERACT_PATH + '/bin/tesseract'
                                    os.environ["TESSDATA_PREFIX"] = TESSERACT_PATH + '/share/tessdata'
                                #--------------------------------------------------------------e-taking Tessaract path for respective OS
                                text = pytesseract.image_to_string(Image.open(filename))
                            except Exception as e:
                                log.error(e, exc_info= True)
                                log.info('WARNING!: error occured in get_ocr, ERR_MSG : ' + str(e))
                                if(TESSERACT_PATH_EXISTS) :
                                    log.info('pytessaract is not pointing to TESSERACT_PATH, adding TESSERACT_PATH to path')
                                    pytesseract.tesseract_cmd = TESSERACT_PATH + '/tesseract.exe'
                                    text = pytesseract.image_to_string(Image.open(filename))
                            os.remove(filename)

                            del image, rez_image, gray_img, filter_img, thresh_img, filename
                            os.remove(str("p%s-%s.png" % (pagenumber, xref)))#del image
                            txt = None
                            if( text ):
                                txt = text
                            output_res.append(txt)
                        log.debug( 'Total image count of the PDF file : ' + str(img_count) )
                        if( output_res ):
                            if args[2] == 'image':
                                content = output_res
                            else:
                                # if condition is "all" and pdf contains both text and image text
                                text_content = [content]
                                del content
                                content = [text_content, output_res]
                                logger.print_on_console("The first item in the output list is the text fetched from the PDF, the second item is a list containing text from the images")
                        else:
                            err_msg = 'No images found in the PDF file'
                            # if condition is "all" and pdf contains both text and image text
                            if args[2] == "all":
                                text_content = [content]
                                del content
                                content = [text_content, output_res]
                                logger.print_on_console("The first item in the output list is the text fetched from the PDF, the second item is a list containing text from the images")

                elif len(args)>2 and args[2] not in ['text','']:
                    content = None
                    status=False
                    err_msg=generic_constants.INVALID_INPUT
             else:
                err_msg=generic_constants.INVALID_INPUT

        except ValueError as e:
            err_msg=generic_constants.INVALID_INPUT
        except IOError as e:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Fetching PDF content'+generic_constants.ERR_MSG2
        log.info('Status is '+str(status))
        return status,content,err_msg

    def __get_file_dialog_handle(self):
        hwnds = []
        def winEnum(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == 'Save Print Output As':
                hwnds.append(hwnd)
        win32gui.EnumWindows(winEnum, hwnds)
        handle = hwnds[0] if (len(hwnds) > 0) else None
        return handle

    def __save_as_output_time_func(self, tries=10, time_sleep=0.75):
        while tries > 0:
            win_handle = self.__get_file_dialog_handle()
            if win_handle is not None:
                log.info("Window handle found: %s", win_handle)
                return win_handle
            time.sleep(time_sleep)
            tries -= 1
        return None
    def __save_file(self,src_file_path,file_name,dest_path,opt):
        err_msg=None
        final_path=None
        if not os.path.splitext(dest_path)[1]:
            if os.path.isdir(dest_path):
                dest_file_path=dest_path+os.sep+file_name
                if opt==0:
                    # do not overwrite
                    if os.path.isfile(dest_file_path):
                        err_msg='File already exists in the directory'
                        return False, err_msg, final_path
                    else:
                        # file does not already exist
                        final_path = dest_file_path
                elif opt==1:
                    # overwrite   
                    if os.path.isfile(dest_file_path):
                        if src_file_path==dest_file_path:
                            err_msg="Source file path and desitnation file path cant be the same"
                            return False, err_msg, final_path
                        else:
                            os.remove(dest_file_path)
                            final_path=dest_file_path
                            return True, err_msg, final_path
            else:
                # should be only destination folder
                err_msg="Destination should be folder"
                return False,err_msg,final_path
        else:
            # dhould be only destination folder
            err_msg = "Destination should be folder"
            return False, err_msg, final_path

    def normalize_pdf(self,acrobat_path,pdf_file_path,destination_path,opt=0):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output_res = OUTPUT_CONSTANT
        err_msg = None
        exe_name = os.path.split(acrobat_path)[1]
        file_name = os.path.split(pdf_file_path)[1]
        if(not(isinstance(opt, int)) and opt.strip() == ''):opt = 0
        if SYSTEM_OS=='Windows':
            if os.path.isfile(acrobat_path) and os.path.isfile(pdf_file_path):
                if exe_name.split('.')[1]=='exe' and file_name.split('.')[1]=='pdf' and int(opt) in [0,1]:
                    configvalues = readconfig.readConfig().readJson()
                    connect_tries = int(configvalues['max_retries_app_launch'])
                    wait_timeout=connect_tries
                    connect_sl = 1
                    appId = None
                    p_found=None
                    def_printer = None
                    tries = 10
                    time_sleep = 0.5
                    data=subprocess.check_output(['wmic','printer','list','brief']).decode('utf-8').split('\r\r\n')
                    data=data[1:]
                    printer_list=[]
                    for line in data:
                        for pn in line.split("  "):
                            if pn!="":
                                printer_list.append(pn)
                                break
                    if 'Microsoft Print to PDF' in printer_list:
                        p_found=True
                        def_printer = win32print.GetDefaultPrinter()
                        win32print.SetDefaultPrinter("Microsoft Print to PDF")
                    # temp_file_loc = os.environ['AVO_ASSURE_HOME'] +os.sep+"output"+os.sep+file_name  
                    res = self.__save_file(pdf_file_path, file_name, destination_path, int(opt))
                    if res[0]:
                        file_loc=res[2]
                        for proc in psutil.process_iter():
                            if proc.name() == exe_name:
                                proc.kill()
                        time.sleep(1)
                        # win32api.ShellExecute(0, "print", filePath, None, ".", 0)
                        subprocess.Popen([acrobat_path, " /t ", pdf_file_path, " Microsoft Print To PDF"])
                        for proc in psutil.process_iter():
                            if proc.name() == exe_name:
                                appId = proc.pid
                        msg = "Acrobat Process found with ID " + str(appId)
                        log.debug(msg)
                        while connect_tries > 0:
                            try:
                                app_1 = Application().connect(process=appId)
                                app_1.top_window()
                                connect_tries = 0
                                break
                            except Exception as e:
                                log.debug("Exception occured while connecting to the Acrobat")
                                log.error(e)
                                connect_tries = connect_tries-1
                                time.sleep(connect_sl)
                                if connect_tries == 0:
                                    log.debug("Tried connecting to the Acrobat process. Process not launched")
                                    msg = "Tried connecting to "+exe_name+" . Process not launched"
                                    logger.print_on_console(msg)
                                    break
                        win_handle = self.__save_as_output_time_func(tries, time_sleep)
                        if win_handle is not None:
                            try:
                                win32gui.SetForegroundWindow(win_handle)
                                app = Application().connect(handle=win_handle, allow_magic_lookup=False)
                                main_window = app[win32gui.GetWindowText(win_handle)]
                                main_window.wait('exists enabled visible ready', timeout=wait_timeout, retry_interval=1)
                                main_window.set_focus()
                                temp = file_loc
                                main_window['5'].type_keys(file_loc.replace(' ', '{SPACE}')+"{ENTER}")
                                time.sleep(2)
                                log.debug("AdobeLive Form PDF flattened and placed in ")
                                log.debug(temp)
                                status = TEST_RESULT_PASS
                                methodoutput = TEST_RESULT_TRUE
                            except Exception as e:
                                log.debug("Exception occured in entering the path")
                                log.error(e)
                        else:
                            log.debug("Window not found")
                    else:
                        err_msg=res[1]
                        logger.print_on_console(err_msg)
                else:
                    err_msg="Invalid input"
                    logger.print_on_console(err_msg)
            else:
              err_msg="File not found"
              logger.print_on_console(err_msg)  
        if status==TEST_RESULT_PASS and err_msg==None:
            msg="PDF normalized and placed at "+str(temp)
            logger.print_on_console(msg)
        if p_found and def_printer:
            win32print.SetDefaultPrinter(def_printer)
        return status, methodoutput, output_res, err_msg
