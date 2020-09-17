#-------------------------------------------------------------------------------
# Name:        file_operations_xml
# Purpose:     comparison between two xml data, in respective functions
#
# Author:      anas.ahmed
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
import logging
import PyPDF2
import difflib
import itertools
import cv2
import numpy as np
import imutils
import fitz
log = logging.getLogger('file_operations_xml.py')

class FileOperationsPDF:
    def __init__(self):
        self.DV = dynamic_variable_handler.DynamicVariables()
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
        status = constants.TEST_RESULT_FAIL
        result = constants.TEST_RESULT_FALSE
        err_msg = None
        value = constants.OUTPUT_CONSTANT
        res_opt = 'all'
        type_opt = 'pagewise'
        output_path = None
        try:
            if len(input_val) == 2 or len(input_val) == 3 or len(input_val) == 4:
                filePathA = input_val[0]
                filePathB = input_val[1]
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
                    else:
                        output_path = args.split(";")[0]
                if len(input_val) >= 3 and (input_val[2] != None or input_val[2] != '' ): 
                    res_opt = input_val[2].strip().lower()
                if len(input_val) == 4 and (input_val[3] != None or input_val[3] != '' ): 
                    type_opt = input_val[3].strip().lower()
                if os.path.isfile(filePathA) and os.path.isfile(filePathB):
                    if os.path.getsize(filePathA)>0 and os.path.getsize(filePathB)>0:
                        fileNameA, fileExtensionA = os.path.splitext(filePathA)
                        fileNameB, fileExtensionB = os.path.splitext(filePathB)
                        if fileExtensionB.lower() == ".pdf" and fileExtensionA.lower() == ".pdf":
                            pdf1 = open(filePathA, 'rb')  
                            pdf2 = open(filePathB, 'rb')  
                            # creating a pdf reader object  
                            pdfReader1 = PyPDF2.PdfFileReader(pdf1)  
                            pdfReader2 = PyPDF2.PdfFileReader(pdf2)  
                            doc1 = fitz.open(filePathA)
                            doc2 = fitz.open(filePathB)
                            if type_opt == 'pagewise':
                                output_res = self.compare_pagewise(pdfReader1,pdfReader2,res_opt,doc1,doc2)
                            if type_opt == 'complete': 
                                output_res = self.compare_complete(pdfReader1,pdfReader2,res_opt,doc1,doc2)
                            pdf1.close()
                            pdf2.close()
                            doc1.close()
                            doc2.close()
                            if output_res is not None:
                                flg = True
                                optFlg = True
                                try:
                                    log.info("Result to be displayed is : " + str(res_opt))
                                    logger.print_on_console("Result to be displayed is : " + str(res_opt))            
                                    if len(output_res):
                                        logger.print_on_console("The number of pages with differences in comparePDFs are: ",len(output_res))
                                    else:
                                        logger.print_on_console("No Difference between inputs in comparePDFs")
                                    if output_path:
                                        if(os.path.exists(output_path) or os.path.exists(os.path.dirname(output_path))):
                                            log.debug( "Writing the output of compareFiles to file : " + str(output_path) )
                                            logger.print_on_console( "Writing the output of compareFiles to file.")
                                            optFlg = False
                                            with open(output_path,'w') as f:
                                                f.write(str(output_res))
                                            json_object = json.dumps(output_res, indent = 4) 
                                            with open("sample2.json", "w") as outfile: 
                                                outfile.write(json_object) 
                                        else:
                                            err_msg = generic_constants.FILE_NOT_EXISTS
                                            flg = False
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
            err_msg = ("Exception occurred in compare_files while comparing two files"+str(e))
            log.error( err_msg )
            logger.print_on_console( "Error occured in Compare Files" )
        return status, result, value, err_msg

    def compare_pagewise(self,pdfReader1,pdfReader2,opt,doc1,doc2):
        result = {}
        for i in range(pdfReader1.numPages):
            result[i + 1] = {}
            result[i+1]['images'] = {}
            if pdfReader2.numPages <= i:
                result[i + 1]["deletions"] = pdfReader1.getPage(i).extractText().replace('\n',"")
                result[i + 1]["images"] = self.compare_images(doc1,None,i,i,opt)
                continue
            result[i + 1]["images"] = self.compare_images(doc1,doc2,i,i,opt)
            test_str2 = pdfReader2.getPage(i).extractText().replace('\n',"")
            total_char2 = len(test_str2)
            test_str1 = pdfReader1.getPage(i).extractText().replace('\n',"")
            total_char1 = len(test_str1)
            test_str1_copy = test_str1
            result[i + 1]['deletions'] = test_str1
            result[i + 1]['additions'] = test_str2
            matches = difflib.SequenceMatcher(None, test_str1, test_str2).get_matching_blocks()
            result[i + 1]["matches"] = []
            matched_count = 0
            for match in matches:
                matched = test_str1_copy[match.a:match.a + match.size]
                matched_count = len(matched) + matched_count
                if opt == "all":
                    result[i + 1]['matches'].append(matched)
                result[i + 1]['deletions'] = result[i + 1]["deletions"].replace(matched, "")
                result[i + 1]['additions'] = result[i + 1]["additions"].replace(matched, "")
            result[i + 1]["matchedSource"] = matched_count/total_char1*100
            result[i + 1]["matchedDest"] = matched_count/total_char2*100
        if pdfReader1.numPages < pdfReader2.numPages:
            for i in range(pdfReader1.numPages,pdfReader2.numPages):
                result[i + 1]["images"] = self.compare_images(None,doc2,i,i,opt)
                result[i + 1]["additions"] = pdfReader2.getPage(i)

        return result

    def compare_complete(self,pdfReader1,pdfReader2,opt,doc1,doc2):
        sim = {}
        result = {}
        pageMatched = {}
        for i in range(pdfReader1.numPages):
            j = 0
            result[i + 1] = {}
            result[i+1]['images'] = {}
            lastMathc = -1
            while j < pdfReader2.numPages:
                if(j in pageMatched and pageMatched[j] == 1):
                    j = j + 1
                    continue
                pageMatched[j] = -1
                test_str2 = pdfReader2.getPage(j).extractText().replace('\n',"")
                total_char2 = len(test_str2)
                test_str1 = pdfReader1.getPage(i).extractText().replace('\n',"")
                total_char1 = len(test_str1)
                test_str1_copy = test_str1
                matched_count = 0
                deletions = test_str1
                additions = test_str2
                matches = [] 
                match_page = difflib.SequenceMatcher(None, test_str1, test_str2).get_matching_blocks()
                for match in match_page:
                    matched = test_str1_copy[match.a:match.a + match.size]
                    matched_count = len(matched) + matched_count
                    matches.append(matched)
                    deletions = deletions.replace(matched, "")
                    additions = additions.replace(matched, "")
                if i not in sim or sim[i] < matched_count/total_char1*100:
                    if matched_count/total_char1*100 > 20:
                        sim[i] =  matched_count/total_char1*100
                        result[i + 1]["matchedSource"] = matched_count/total_char1*100
                        result[i + 1]["matchedDest"] = matched_count/total_char2*100
                        result[i + 1]["pageMatch"] = j + 1
                        result[i + 1]['images'] = self.compare_images(doc1,doc2,i,j,opt)
                        pageMatched[lastMathc] = -1
                        lastMathc = j
                        pageMatched[j] = 1
                        if opt == "all":
                            result[i + 1]["matches"] = matches
                        result[i + 1]["deletions"] = deletions
                        result[i + 1]["additions"] = additions
                j += 1
            if lastMathc is -1:
                result[i + 1]["matchedSource"] = -1
                result[i + 1]["matchedDest"] = -1
                result[i + 1]["pageMatch"] = -1
                if opt == "all":
                    result[i + 1]["matches"] = "None"
                result[i + 1]["deletions"] = test_str1
                result[i + 1]["additions"] = "None"
                result[i + 1]["images"] = self.compare_images(doc1,None,i,j,opt)
            
        j = pdfReader1.numPages + 1
        while i < pdfReader2.numPages and pageMatched[i] != 1:
            result[j]["matchedSource"] = -1
            result[j]["images"] = self.compare_images(None,doc2,i,i,opt)
            result[j]["matchedDest"] = -1
            result[j]["pageMatch"] = j+1
            if opt == "all":
                result[j]["matches"] = "None"
            result[j]["deletions"] = "None"
            result[j]["additions"] = pdfReader2.getPage(i).extractText().replace('\n',"")
            j += 1

        return result

    def compare_images(self,doc1,doc2,index1,index2,opt):
        result = {}
        if opt == "all":
            result['matches'] = 0
        result['deletion'] = 0
        result['addition'] = 0
        i = 1
        if doc1 is None:
            result["additions"] = len(doc2.getPageImageList(index2))
            return result
        if doc2 is None:
            result["deletions"] = len(doc1.getPageImageList(index1))
            return result
        for (img1,img2) in itertools.zip_longest(doc1.getPageImageList(index1),doc2.getPageImageList(index2)):
            if index1 == 5 and index2 == 6:
                print("yoli")
            if img1 and img2 and img1 == img2:
                if opt == "all":
                    result['matches'] += 1
            elif img1 is None:
                result['addition'] += 1
            elif img2 is None:
                result['deletion'] += 1
            else:
                result['addition'] += 1
                result['deletion'] += 1
        return result

    def locate_image(self,input_val,args):
        status = constants.TEST_RESULT_FAIL
        result = constants.TEST_RESULT_FALSE
        err_msg = None
        value = constants.OUTPUT_CONSTANT
        output_path = None
        result = {}
        result['count'] = 0
        try:
            if len(input_val) == 2:
                filePathA = input_val[0]
                filePathB = input_val[1]
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
                    else:
                        output_path = args.split(";")[0]
                if os.path.isfile(filePathA) and os.path.isfile(filePathB):
                    if os.path.getsize(filePathA)>0 and os.path.getsize(filePathB)>0:
                        fileNameA, fileExtensionA = os.path.splitext(filePathA)
                        fileNameB, fileExtensionB = os.path.splitext(filePathB)
                        if fileExtensionA.lower() == ".pdf" and fileExtensionB.lower() == ".png":   
                            result = self.get_thresholded_similar_images(filePathA,filePathB)
                            if result is not None:
                                flg = True
                                optFlg = True
                                try:  
                                    if result['total_count'] > 0:      
                                        logger.print_on_console("Total number of image occurances are: ",result['total_count'])
                                    else:
                                        logger.print_on_console("No image occurances in PDF")
                                    if output_path:
                                        if(os.path.exists(output_path) or os.path.exists(os.path.dirname(output_path))):
                                            log.debug( "Writing the output of PDFimageCompare to file : " + str(result) )
                                            logger.print_on_console( "Writing the output of PDFimageCompare to file.")
                                            optFlg = False
                                            with open(output_path,'w') as f:
                                                f.write(str(result))
                                            with open("sample1.json", "w") as outfile: 
                                                outfile.write(str(result)) 
                                        else:
                                            err_msg = generic_constants.FILE_NOT_EXISTS
                                            flg = False
                                except Exception as ex:
                                    err_msg = ("Exception occurred while writing to output file in compareFile : " + str(ex))
                                    log.debug( err_msg )
                                    flg = False
                                if(flg):
                                    status = constants.TEST_RESULT_PASS
                                    result = constants.TEST_RESULT_TRUE
                                    log.info("Comparision of files completed")
                                    if( optFlg ):
                                        value = result
                            else:
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
        im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        y1 = np.ascontiguousarray(im[..., [2, 1, 0]])  # rgb to bgr
        return y1 

    def get_thresholded_similar_images(self,filePathA,filePathB):
        doc1 = fitz.open(filePathA)
        template = cv2.imread(filePathB)
        output_res = {}
        output_res['total_count'] = 0
        output_res['abs_max'] = 0
        for i in range(0,doc1.pageCount):
            output_res[i + 1] = {}
            imTemp = doc1.loadPage(i).getPixmap(alpha=False)
            image = self.pix2np(imTemp)
            value = [255,255,255]
            image = cv2.copyMakeBorder(image,100,100,100,100,cv2.BORDER_CONSTANT,None,value)
            #cv2.imwrite("pdf1"+str(i)+".png",image)
            output_res[i + 1] ,output_res["abs_max"] = self.compare(image,template,output_res['abs_max'])
        if output_res["abs_max"] < 0.3:
            return None
        for image in output_res:
            if not isinstance(image,int):
                continue
            if output_res[image]['max_corr'] > output_res['abs_max'] - 0.02 and output_res[image]['max_corr'] <= output_res['abs_max']:
                #cv2.imwrite("result"+str(image)+".png",output_res[image]["image"])
                output_res['total_count'] += output_res[image]['count'] 
            else:
                output_res[image]['count'] = 0
                output_res[image]['location'] = None

        return output_res         

    def compare(self,image,template,abs_max):
        template = cv2.Canny(template, 50, 200)
        (tH, tW) = template.shape[:2]
        gray = image
        found = None
        results = {}
        count = 0
        max_val = 0
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
                location.append(maxLoc)
                found = (maxVal, maxLoc, r)
                xx = cv2.minMaxLoc(result)
                max_val = maxVal
            elif maxVal == found[0]:
                count += 1
                location.append(maxLoc)
            if maxVal > abs_max:
                abs_max = maxVal
        # unpack the bookkeeping variable and compute the (x, y) coordinates
        # of the bounding box based on the resized ratio
        (_, maxLoc, r) = found
        dimensions = image.shape
        r1,r2,r3 = dimensions[0]/3,dimensions[0]/1.5 - 10,dimensions[0]
        c1,c2,c3 = dimensions[1]/3,dimensions[1]/1.5 - 10,dimensions[1]
        x,y = 0,3
        results['location'] = []
        for found in location:
            if found[0] > r1:
                x = 2
                if found[0] > r2:
                    x = 2
            if found[1] > c1:
                y = 1
                if found[1] > c2:
                    y = 2
            results["location"].append({x,y})
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
        # draw a bounding box around the detected result and display the image
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
        #results["image"] = image
        results["max_corr"] = max_val
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
        from PyPDF2 import PdfFileReader, PdfFileWriter
        import fitz
        try:
             log.debug('Get the content of pdf file: '+str(input_path)+','+str(pagenumber))
             doc=fitz.open(input_path)
             pagenumber=int(pagenumber)-1
             if pagenumber<doc.pageCount:
                page = doc[pagenumber]
                content=page.getText()
##                content=content.encode('utf-8')
                if len(args)>1 and args[1]=='_internal_verify_content':
                    return content
                if len(args) >= 2 and not (args[0] is None and args[1] is None):
                    start=args[0].strip()
                    end=args[1].strip()
                    startIndex=0
                    endIndex=len(content)
                    log.info('Start string: '+str(start)+' End string: '+str(end))
                    if not start is '':
                        startIndex=content.find(start)+len(start)
                    if not end is '':
                        endIndex=content.find(end)
                    content=content[startIndex:endIndex]
                    log.info('Content between Start and End string is ')
##                    logger.print_on_console('Content between Start and End string is ')
                elif len(args)==1:
                    with open(args[0],'w') as file:
                        file.write(content)
                        file.close()
                log.info(content)
                status=True
##        try:
##             log.debug('Get the content of pdf file: '+str(input_path)+','+str(pagenumber))
##             reader=PdfFileReader(open(input_path,'rb'))
##             pagenumber=int(pagenumber)-1
##             if pagenumber<reader.getNumPages():
##                page=reader.getPage(pagenumber)
##                content=page.extractText()
##                if len(args)>1 and args[1]=='_internal_verify_content':
##                    return content
##                if len(args) >= 2 and not (args[0] is None and args[1] is None):
##                    start=args[0].strip()
##                    end=args[1].strip()
##                    startIndex=0
##                    endIndex=len(content)
##                    log.info('Start string: '+str(start)+' End string: '+str(end))
##                    if not start is '':
##                        startIndex=content.find(start)+len(start)
##                    if not end is '':
##                        endIndex=content.find(end)
##                    content=content[startIndex:endIndex]
##                    log.info('Content between Start and End string is ')
##                elif len(args)==1:
##                    with open(args[0],'w') as file:
##                        file.write(content)
##                        file.close()
##                log.info(content)
##                status=True
             else:
                err_msg=generic_constants.INVALID_INPUT
                log.error(err_msg)

        except ValueError as e:
            err_msg=generic_constants.INVALID_INPUT
            log.error(e)
        except IOError as e:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
            log.error(e)
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Fetching PDF content'+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,content,err_msg

