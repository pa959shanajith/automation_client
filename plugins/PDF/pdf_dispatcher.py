#-------------------------------------------------------------------------------
# Name:        pdf_dispatcher
# Purpose:	   PDF dispatcher for PDF utility operations
#
# Author:      shree.p
#
# Created:
# Copyright:   (c) shree.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import pdf_ops
import logger
import logging
##import oebs_constants

import os
import base64
import json
import time
from constants import *
import constants
import core_utils
from pdf_ops import PDFOperations
import pdf_constants
pdfV = None
##log = logging.getLogger('pdf_dispatcher.py')
windownametoscrape = ''

log = logging.getLogger('pdf_dispatcher.py')

class PDFDispatcher:
    pdf_keywords_obj = PDFOperations()

    def __init__(self):
        self.exception_flag=''
        self.action = None

    def dispatcher(self,teststepproperty,input):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name.lower()
        url = teststepproperty.url
        err_msg=None
        result=[pdf_constants.TEST_RESULT_FAIL,pdf_constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]

        try:
            dict = { 'gettext': self.pdf_keywords_obj.gettext,
                     'verifytext': self.pdf_keywords_obj.verifytext,
                     'getindexcount' : self.pdf_keywords_obj.getindexcount
                   }
            keyword=keyword.lower()
            if keyword in list(dict.keys()):
                result= dict[keyword](objectname,input,output)
            else:
                err_msg=pdf_constants.INVALID_KEYWORD
                result=list(result)
                result[3]=err_msg
        except Exception as e:
            logger.print_on_console('Exception at pdf dispatcher',e)

        return result