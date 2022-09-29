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
import reportnfs
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
        genericStep = False
        DEBUG_ACTION =  False
        path = constants.SCREENSHOT_PATH
        filePath = ''
        try:

            if('action' in args[0]):
                DEBUG_ACTION = args[0]['action']==DEBUG
                ## for generic keyword capture screen
                log.debug('Reading the inputs')
                if(len(args[0]['inputs'])<=2):
                    genericStep = self.genericScreenshot(args[0]['inputs'])
                else:
                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_NO_INPUT'])
                    log.error(ERROR_CODE_DICT['ERR_INVALID_NO_INPUT'])
                    output = None
            elif path=="Disabled":
                logger.print_on_console(ERROR_CODE_DICT['ERR_SCREENSHOT_PATH'])
                output=None

            if output!=None:
                r="pass"
                objpath = ''
                if not DEBUG_ACTION:
                    data = args[0]
                    if(genericStep):
                        data = args[0]["screen_data"]
                    # bucketname = 'screenshots' #switch
                    tempobj=self.generateUniqueFileName() +'.png' #necessary? coz genericStep already there
                    # objpath = data['projectname']+'/'+data['releaseid']+'/'+data['cyclename']+'/'+tempobj
                    tempPath=os.path.join(path, data['projectname'],data['releaseid'],data['cyclename'], datetime.datetime.now().strftime("%Y-%m-%d"))
                    if not os.path.exists(tempPath):
                        os.makedirs(tempPath)
                    tempPath=tempPath+OS_SEP+tempobj
                    # if accessibility:
                        # bucketname = 'accessibilityscreenshots' #switch
                        # tempPath = data['temppath']
                        # objpath = data['projectname']+'/'+data['releaseid']+'/'+data['cyclename']+'/'+data['executionid']+'/'+tempobj
                    if driver:
                        driver.save_screenshot(tempPath)
                    elif not(web):
                        img=ImageGrab.grab()
                        img.save(tempPath)
                    #pushing screenshots to NFS #switch
                    # if constants.SCREENSHOT_NFS_AVAILABLE: #switch
                    #     r = reportnfs.client.saveimage(bucketname,objpath,tempPath)
                    # if not accessibility or constants.SCREENSHOT_NFS_AVAILABLE: 
                    #     #add logic to clear accessibility screenshots after some time period
                    #     os.remove(tempPath)
                if(genericStep):
                    if driver:
                        driver.save_screenshot(genericStep)
                    else:
                        if web:
                            log.warn("Capturing screenshot using generic since browser driver is not available")
                        img=ImageGrab.grab()
                        img.save(genericStep)
                #  keeping a copy of screenshot in folder for generic keyword
                if r=='fail':
                    raise Exception('error while saving in reportNFS') 
                elif not DEBUG_ACTION:
                    output = tempPath
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

    def genericScreenshot(self,arg):
        inputval=filename=''
        if arg != '':
            inputval=arg[0]
            filename=arg[1]
        if(inputval=='' or not os.path.isdir(inputval)):
            logger.print_on_console("Invalid file path! Saving screenshot in the default folder screenshots")
            logger.warning("Invalid file path! Saving screenshot in the default folder screenshots")
            inputval = SCREENSHOT_PATH_LOCAL
        if filename.strip() == '': filename = self.generateUniqueFileName()
        elif '.' in filename: filename = filename.split('.')[0]
        filepath = os.path.join(os.path.normpath(inputval), filename)
        return filepath +'.png'
        

