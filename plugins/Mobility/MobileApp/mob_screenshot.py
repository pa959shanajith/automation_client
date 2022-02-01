#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     12-05-2017
# Copyright:   (c) prudhvi.gujjuboyina 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PIL import ImageGrab
import  datetime
import time
import logger
import os
import uuid
from constants import *
import android_scrapping

import logging


log = logging.getLogger('mob_screenshot.py')
class Screenshot():
    def captureScreenshot(self,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
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
                        filePath=str(inputval) + os.sep+ filename
                    else:
                        filename=self.generateUniqueFileName()
                        filePath=str(inputval) + os.sep+ filename
                except Exception as e:
                    log.error(e)
            else:
                try:
                    import constants
                    path = constants.SCREENSHOT_PATH
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
                log.debug('Capturing Screenshot')
                if android_scrapping.driver==None:
                    img=ImageGrab.grab()
                    img.save(filePath+'.png')
                    log.debug('screenshot captured')
                else:
                    img=android_scrapping.driver.save_screenshot(filePath+'.png')
                    log.debug('screenshot captured')
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
                log.debug('screenshot captured and saved in : ',filePath+'.png')
        except Exception as e:
            log.error(e)
            err_msg=ERROR_CODE_DICT['ERR_SCREENSHOT_PATH']
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def generateUniqueFileName(self):
        filename=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S_"+str(uuid.uuid4()))
        return filename