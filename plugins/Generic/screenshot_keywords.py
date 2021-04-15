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
import uuid
from constants import *
import constants
import logging

log = logging.getLogger('screenshot_keywords.py')
class Screenshot():
    def captureScreenshot(self,*args,web=False):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        path = constants.SCREENSHOT_PATH
        filePath = ''
        try:
            if len(args) == 2:
                inputval = args[0]
                filename = args[1]
                log.debug('Reading the inputs')
                try:
                    if not os.path.exists(inputval):
                        os.makedirs(inputval)
                    if filename!=None:
                        if '.' in filename:
                            filename=filename.split('.')[0]
                        filePath=str(inputval) + '/'+ filename
                    else:
                        filename=self.generateUniqueFileName()
                        filePath=str(inputval) + '/'+ filename
                except Exception as e:
                    logger.print_on_console( e)
            else:
                try:
                    if path=="Disabled":
                        logger.print_on_console(ERROR_CODE_DICT['ERR_SCREENSHOT_PATH'])
                        output=None
                    else:
                        filename=self.generateUniqueFileName()
                        path=path+args[0]['projectname']+os.sep+args[0]['releaseid']+os.sep+args[0]['cyclename']+os.sep+datetime.datetime.now().strftime("%Y-%m-%d")+os.sep
                        if(not os.path.exists(path)):
                            os.makedirs(path)
                        filePath = path + filename
                        output = filePath+'.png'
                except Exception as e:
                    log.error(e)
            if output==None:
                log.debug('screenshot capture failed')
                output=OUTPUT_CONSTANT
            else:
                log.debug('screenshot captured')
                logger.print_on_console('Screenshot captured')
                if not(web):
                    img=ImageGrab.grab()
                    img.save(filePath+'.png')
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console("Error while capturing screenshot")
            err_msg=ERROR_CODE_DICT['ERR_SCREENSHOT_PATH']
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def generateUniqueFileName(self):
        filename=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S_"+str(uuid.uuid4()))
        return filename

