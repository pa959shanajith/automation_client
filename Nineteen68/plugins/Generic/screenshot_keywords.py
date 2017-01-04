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
import Exceptions
import generic_constants
import os
from constants import *

class Screenshot():
    status=False
    def captureScreenshot(self,fileDir):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        try:
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
            filename=self.generateUniqueFileName()
            filePath=str(fileDir)+filename
            logger.print_on_console('capturing the screenshot')
            img=ImageGrab.grab()
            img.save(filePath+'.png', "png")
            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            raise e
            logger.print_on_console('unable to capture the screenshot')
            Exceptions.error(e)
        return status,methodoutput

    def generateUniqueFileName(self):
        filename=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S_"+str(time.strftime("%Y%m%d%H%M%S")))
        return filename

