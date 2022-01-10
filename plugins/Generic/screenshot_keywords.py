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
from reportnfs import reportNFS
import generic_constants
import os
import uuid
from constants import *
import constants
import logging

log = logging.getLogger('screenshot_keywords.py')
class Screenshot():
    def captureScreenshot(self,*args,web=False,driver=False,accessibility=False):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        path = constants.SCREENSHOT_PATH
        filePath = ''
        try:
            if('action' in args[0]):
                ## for generic keyword capture screen
                log.debug('Reading the inputs')
                if(len(args[0]['inputs'])>2):
                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_NO_INPUT'])
                    output = None
                elif(args[0]['inputs']!='' and len(args[0]['inputs'])==2):
                    inputval = args[0]['inputs'][0]
                    filename = args[0]['inputs'][1]
                    if(inputval=='' or not os.path.isdir(inputval)):
                        logger.print_on_console("Invalid file path! Saving screenshot in the default folder")
                        inputval = path
                    if (filename!=''):
                        if '.' in filename:
                            filename = filename.split('.')[0]
                        if str(inputval).endswith(os.sep):
                            filePath = str(inputval) + filename
                        else:
                            filePath = str(inputval) + os.sep+ filename
                    else:
                        filename = self.generateUniqueFileName()
                        if str(inputval).endswith(os.sep):
                            filePath = str(inputval) + filename
                        else:
                            filePath = str(inputval) + os.sep + filename
                elif(args[0]['action']==EXECUTE and args[0]['inputs']==''):
                    filename = self.generateUniqueFileName()
                    screenData = args[0]['screen_data']
                    path = path+screenData['projectname']+os.sep+screenData['releaseid']+os.sep+screenData['cyclename']+os.sep+datetime.datetime.now().strftime("%Y-%m-%d")+os.sep
                    if(not os.path.exists(path)):
                        os.makedirs(path)
                    filePath = path + filename
                elif(args[0]['action']=='debug' and args[0]['inputs']==''):
                    filePath = path+self.generateUniqueFileName()
                else:
                    output = None
            else:
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
            if output==None:
                log.debug('screenshot capture failed')
                output=OUTPUT_CONSTANT
            else:
                bucketname = 'screenshots'
                tempobj=self.generateUniqueFileName() +'.png'
                tempPath=os.sep.join([os.getcwd(),'output','.screenshots', tempobj])
                objpath = args[0]['projectname']+'/'+args[0]['releaseid']+'/'+args[0]['cyclename']+'/'+tempobj
                if accessibility:
                    bucketname = 'accessibilityscreenshots'
                    tempPath = args[0]['temppath']
                    objpath = args[0]['projectname']+'/'+args[0]['releaseid']+'/'+args[0]['cyclename']+'/'+args[0]['executionid']+'/'+tempobj
                elif driver:
                    driver.save_screenshot(tempPath)
                elif not(web):
                    img=ImageGrab.grab()
                    img.save(tempPath)
                else:
                    pass #add logic for capture through driver to be added here
                r = reportNFS().saveimage(bucketname,objpath,tempPath)
                if not accessibility: #add logic to clear accessibility screenshots after some time period
                    os.remove(tempPath)
                if r=='fail':
                    raise Exception('error while saving in reportNFS') 
                else:
                    output = objpath
                log.debug('screenshot captured')
                logger.print_on_console('Screenshot captured')
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            output=OUTPUT_CONSTANT
            logger.print_on_console("Error while capturing screenshot")
            err_msg=ERROR_CODE_DICT['ERR_SCREENSHOT_PATH']
            logger.print_on_console(err_msg)
        return status,methodoutput,output,err_msg

    def generateUniqueFileName(self):
        filename=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S_"+str(uuid.uuid4()))
        return filename

