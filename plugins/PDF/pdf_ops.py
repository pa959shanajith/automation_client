#-------------------------------------------------------------------------------
# Name:        PDFOperations
# Purpose:     PDF utility related keywords
#
# Author:      sadia
#
# Created:
# Copyright:   (c) sadia
# Licence:     <your license>
#------------------------------------------------------------------------------


import ast
import logger
import logging

import pdf_constants
from constants import *

log = logging.getLogger('pdf_ops.py')


class PDFOperations:

    def pdf_convertStrToList(self,inputstr):
        inputstr = inputstr.replace("''","'")
        try:
            listVal = []
            if inputstr != None and len(inputstr) > 0:
                listVal = ast.literal_eval(inputstr)
            return listVal
        except Exception as e:
            logger.print_on_console('Error at pdf_convertStrToList')
            log.error(e)


    # def indexcount(self,objectname):
    #     try:
    #         output = self.pdf_convertStrToList(objectname)
    #         output = len(output)
    #         return output
    #     except Exception as e:
    #         logger.print_on_console('Error at indexcount')
    #         log.error(e)



    def getindexcount(self,objectname,inputs,output):
        status = pdf_constants.TEST_RESULT_FAIL
        methodoutput = pdf_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        #return indexcount keyword implementation
        try:
            output = self.pdf_convertStrToList(objectname)
            output = len(output)
            status = pdf_constants.TEST_RESULT_PASS
            methodoutput = pdf_constants.TEST_RESULT_TRUE

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        #return status and methodoutput
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg


    def gettext(self,objectname,inputs,output):
        status = pdf_constants.TEST_RESULT_FAIL
        methodoutput = pdf_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        #gettext keyword implementation
        fulltext = ''
        listVal = []
        logger.print_on_console("inputs : ",inputs)
        #logger.print_on_console("objectname : ",objectname)
        try:
            listVal = self.pdf_convertStrToList(objectname)

            if inputs[0].strip() != None and len(inputs[0].strip()) > 0:
                inpIndex = inputs[0]
                inpIndex = int(inpIndex)

                if(inpIndex not in range(0,len(listVal))):
                    logger.print_on_console('Input Index is not in the range of the element')
                else:
                    output = listVal[inpIndex][4]
                    status = pdf_constants.TEST_RESULT_PASS
                    methodoutput = pdf_constants.TEST_RESULT_TRUE
                    logger.print_on_console('Get Text : ' , output)
            else :
                for i in range(0,len(listVal)):
                    fulltext = fulltext + " " + listVal[i][4]
                    fulltext = fulltext.strip()
                output = fulltext
                status = pdf_constants.TEST_RESULT_PASS
                methodoutput = pdf_constants.TEST_RESULT_TRUE
                logger.print_on_console('Get Text : ' , output)
        except ValueError as v:
            err_msg = "Invalid Input! Only blank and number values are allowed."
            log.error(err_msg)
            logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error while fetching the value"
            log.error(e)
            logger.print_on_console(err_msg)

        #return status and methodoutput
        return status,methodoutput,output,err_msg


    def verifytext(self,objectname,inputs,output):
        status = pdf_constants.TEST_RESULT_FAIL
        methodoutput = pdf_constants.TEST_RESULT_FALSE
        err_msg=None
        fulltext = ''
        output=OUTPUT_CONSTANT
        #verifytext keyword implementation
        try:
            listVal = self.pdf_convertStrToList(objectname)
            if len(inputs) > 0:
                if len(inputs) == 2:
                    inpIndex = inputs[1]
                    inpIndex = int(inpIndex)
                    if(inpIndex not in range(0,len(listVal))):
                        logger.print_on_console('Input Index is not in the range of the element')
                    else:
                        output = listVal[inpIndex][4]
                        logger.print_on_console('Input value provided : ' , inputs[0])
                        logger.print_on_console('Value fetched : ' , output)
                elif(inputs[0].strip() != None and len(inputs[0].strip()) > 0):
                    for i in range(0,len(listVal)):
                        fulltext = fulltext + " " + listVal[i][4]
                        fulltext = fulltext.strip()
                    output = fulltext
                    logger.print_on_console('Input value provided : ' , inputs[0])
                    logger.print_on_console('Value fetched : ' , output)
                else:
                    log.error(INVALID_INPUT)
                    err_msg=INVALID_INPUT
                    logger.print_on_console(INVALID_INPUT)
                methodoutput = [inputs[0],output]
                if inputs[0] == output:
                    output = True
                    status = pdf_constants.TEST_RESULT_PASS
                else:
                    logger.print_on_console('Values does not match')
                    output = False
            else:
                log.error(INVALID_INPUT)
                err_msg=INVALID_INPUT
                logger.print_on_console(INVALID_INPUT)
        except ValueError as v:
            err_msg = "Invalid Input! Only number is allowed as the index input."
            log.error(v)
            logger.print_on_console(err_msg)
        except Exception as e:
            err_msg="Error occurred during verifying values"
            log.error(e)
            logger.print_on_console(err_msg)
        #return status and methodoutput
        return status,methodoutput,output,err_msg

    def gettextdynamic(self,objectname,inputs,output):
        status = pdf_constants.TEST_RESULT_FAIL
        methodoutput = pdf_constants.TEST_RESULT_FALSE
        err_msg=None
        #output=None
        #gettext keyword implementation
        output = ''
        listVal = []
        try:
            listVal = self.pdf_convertStrToList(objectname)
            import fitz
            if inputs[0].strip() != None and len(inputs[0].strip()) >= 0:
                filepath = inputs[0]
                pagenumber = listVal[0][len(listVal[0])-1]
                document = fitz.open(filepath)
                page = document[pagenumber]
                pagewords = page.getTextWords()

                if len(inputs) > 1:
                    inpIndex = int(inputs[1])
                    if(inpIndex not in range(0,len(listVal))):
                        logger.print_on_console('Input Index is not in the range of the element')
                    else:
                        row = listVal[inpIndex][5]
                        col = listVal[inpIndex][7]
                        output = [i for i in pagewords if row==i[5] and col==i[7]][0][4]

                        status = pdf_constants.TEST_RESULT_PASS
                        methodoutput = pdf_constants.TEST_RESULT_TRUE
                        logger.print_on_console('Get Text : ' , output)

                else:
                    for i in range(0,len(listVal)):
                        row = listVal[i][5]
                        col = listVal[i][7]
                        output = output + " " + [j for j in pagewords if row==j[5] and col==j[7]][0][4]
                        output = output.strip()
                    status = pdf_constants.TEST_RESULT_PASS
                    methodoutput = pdf_constants.TEST_RESULT_TRUE
                    logger.print_on_console('Get Text : ' , output)

        except ValueError as v:
            err_msg = "Invalid Input! Only filepath and number values are allowed."
            log.error(err_msg)
            logger.print_on_console(err_msg)
        except Exception as e:
            err_msg = "Error while fetching the value"
            log.error(e)
            logger.print_on_console(err_msg)

        #return status and methodoutput
        return status,methodoutput,output,err_msg

    def verifytextdynamic(self,objectname,inputs,output):
        status = pdf_constants.TEST_RESULT_FAIL
        methodoutput = pdf_constants.TEST_RESULT_FALSE
        err_msg=None
        output=''
        #verifytext keyword implementation
        try:
            listVal = self.pdf_convertStrToList(objectname)
            import fitz
            if len(inputs) > 0:
                filepath = inputs[0]
                pagenumber = listVal[0][len(listVal[0])-1]
                document = fitz.open(filepath)
                page = document[pagenumber]
                pagewords = page.getTextWords()

                if len(inputs) == 3:
                    inpIndex = int(inputs[2])
                    if(inpIndex not in range(0,len(listVal))):
                        logger.print_on_console('Input Index is not in the range of the element')
                    else:
                        row = listVal[inpIndex][5]
                        col = listVal[inpIndex][7]
                        output = [i for i in pagewords if row==i[5] and col==i[7]][0][4]
                        logger.print_on_console('Input value provided : ' , inputs[1])
                        logger.print_on_console('Value fetched : ' , output)

                elif len(inputs)==2:
                    for i in range(0,len(listVal)):
                        row = listVal[i][5]
                        col = listVal[i][7]
                        output = output + " " + [j for j in pagewords if row==j[5] and col==j[7]][0][4]
                        output = output.strip()
                    logger.print_on_console('Input value provided : ' , inputs[1])
                    logger.print_on_console('Value fetched : ' , output)
                else:
                    log.error(INVALID_INPUT)
                    err_msg=INVALID_INPUT
                    logger.print_on_console(INVALID_INPUT)
                methodoutput = [inputs[1],output]
                if inputs[1] == output:
                    output = True
                    status = pdf_constants.TEST_RESULT_PASS
                else:
                    logger.print_on_console('Values does not match')
                    output = False

            else:
                log.error(INVALID_INPUT)
                err_msg=INVALID_INPUT
                logger.print_on_console(INVALID_INPUT)
        except ValueError as v:
            err_msg = "Invalid Input! Only number is allowed as the index input."
            log.error(v)
            logger.print_on_console(err_msg)
        except Exception as e:
            err_msg="Error occurred during verifying values"
            log.error(e)
            logger.print_on_console(err_msg)
        #return status and methodoutput
        return status,methodoutput,output,err_msg
