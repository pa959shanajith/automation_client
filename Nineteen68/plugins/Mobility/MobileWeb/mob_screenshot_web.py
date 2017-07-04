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

##import generic_constants
import os
from constants import *
import browser_Keywords

import logging


log = logging.getLogger('mob_screenshot.py')
class Screenshot():
    def captureScreenshot(self,*args):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
##        inputval,filename,
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
                        filePath=str(inputval) + '//'+ filename
                    else:
                        filename=self.generateUniqueFileName()
                        filePath=str(inputval) + '//'+ filename
                except Exception as e:
                    logger.print_on_console( e)
            else:
                try:
                    import readconfig
                    configobj = readconfig.readConfig()
                    configvalues = configobj.readJson()
                    path = configvalues['screenShot_PathName']
                    if not os.path.exists(path):
                        os.makedirs(path)
                    filename=self.generateUniqueFileName()
                    filePath = path + filename
                    output = filePath+'.png'
                except Exception as e:
                    logger.print_on_console( e)


            log.debug('screenshot captured')

            if browser_Keywords.driver_obj==None:
                img=ImageGrab.grab()
                img.save(filePath+'.png')
##                logger.print_on_console('screenshot captured')
            else:

                img=browser_Keywords.driver_obj.save_screenshot(filePath+'.png')
##                logger.print_on_console('screenshot captured')

            status=TEST_RESULT_PASS
            methodoutput=TEST_RESULT_TRUE
##            log.debug('screenshot captured and saved in : ',filePath+'.png')
##            logger.print_on_console('The Specified path is not found, hence screenshot captured and saved in default path')
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg="Screenshot not captured - You do not have write permission to screenshot folder!!! - "
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def generateUniqueFileName(self):
        filename=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S_"+str(time.strftime("%Y%m%d%H%M%S")))
        return filename