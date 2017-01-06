#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     24-10-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

##import Pillow as ImageGrab
from PIL import ImageGrab
import  datetime
import time
import logger

import generic_constants
import os
from constants import *

import logging


log = logging.getLogger('screenshot_keywords.py')
class Screenshot():
    def captureScreenshot(self,fileDir,*args):
        
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            log.debug('Reading the inputs')
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
            filename=self.generateUniqueFileName()
            filePath=str(fileDir)+filename
            log.debug('capturing the screenshot')
            logger.print_on_console('capturing the screenshot')
            img=ImageGrab.grab()
            img.save(filePath+'.png', "png")
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
            log.debug('screenshot captured and saved in : ',filePath+'.png')
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
            err_msg=INPUT_ERROR
        return status,methodoutput,output,err_msg

    def generateUniqueFileName(self):
        filename=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S_"+str(time.strftime("%Y%m%d%H%M%S")))
        return filename

