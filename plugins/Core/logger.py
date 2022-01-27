#-------------------------------------------------------------------------------
# Name:        logger.py
# Purpose:      logging on client window
#
# Author:      wasimakram.sutar
#
# Created:     14-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#
# Modified Author: vishvas.a
#
# Created:     13-07-2017
# Copyright:   (c) vishvas.a 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import datetime
import os
import sys
import json
# from colorama import Fore, Style, init as init_colorama
from inspect import getframeinfo, stack
from constants import *
import reportnfs
from logging.handlers import BaseRotatingHandler
import logging
logger = logging.getLogger('logger.py')

def print_on_console(message,*args, **kwargs):
    try:
        ts = time.time()
        sttime = datetime.datetime.fromtimestamp(ts).strftime('%y-%m-%d %H:%M:%S')
        try:
            caller = getframeinfo(sys._getframe(-1))
            filename=os.path.basename(caller.filename)[0:-3]
            if filename == 'logger':
                caller = getframeinfo(sys._getframe(1))
                filename=os.path.basename(caller.filename)[0:-3]
            filename += ':'+str(caller.lineno) + ' '
        except ValueError:
            filename = ''

        resultant=''
        style1=''
        if isinstance(message,bytes): message=message.decode('utf-8')
        elif not isinstance(message,str): message=str(message)
        for values in args:
            if isinstance(values,bytes): values=values.decode('utf-8')
            elif not isinstance(values,str): values=str(values)
            resultant+=values
        msg_part_1 = sttime + ':  CONSOLE: ' + filename
        msg_part_2 = message + resultant
        # if 'color' in kwargs:
        #     if os.environ["ice_mode"] == "gui":
        #         sys.stdout.write(msg_part_1)
        #         sys.stdout.write_color(msg_part_2 + os.linesep, kwargs['color'])
        #     else:
        #         if(kwargs['color']=="RED"): style1=Fore.RED
        #         elif(kwargs['color']=="GREEN"): style1=Fore.GREEN
        #         elif(kwargs['color']=="YELLOW"): style1=Fore.YELLOW
        #         print(msg_part_1 + style1 + msg_part_2) # + Style.RESET_ALL)
        # else:
        print(msg_part_1 + msg_part_2)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(e)

def log(message):
    print(message)


class CustomHandler(BaseRotatingHandler):

    def __init__(self, excType, excData, ind=0, mode='a', encoding=None, delay=False):
        
        logpath = os.sep.join([os.getcwd(),'output','.logs',excData['batchId'],excData['executionId']])
        if not os.path.exists(logpath):
            os.makedirs(logpath, exist_ok=True)
        if excType==PARALLEL:
            manifest_filepath = os.path.normpath(logpath + os.sep + BROWSER_NAME[ind]+'_manifest.json').replace("\\","\\\\")
            filename = os.path.normpath(logpath + os.sep +BROWSER_NAME[ind]+'.log').replace("\\","\\\\")
        else:
            filename = os.path.normpath(logpath+ os.sep + 'Execution.log').replace("\\","\\\\")
            manifest_filepath = os.path.normpath(logpath + os.sep + 'manifest.json').replace("\\","\\\\")

        BaseRotatingHandler.__init__(self, filename, mode, encoding=None, delay=False)
        
        self.manifest_path = manifest_filepath
        self.filename = filename
        self.excType = excType
        self.logpath = logpath
        self.manifest = {"root":[]}
        self.temp = {}
        self.projectId = excData['projectname']
         
    def logline(self,_,start=False):
        with open(self.filename) as fo:
            if start:
                return [ self.filename.split("\\")[-1] , sum(1 for _ in fo) + 1]
            else:
                return sum(1 for _ in fo)

    def createTspObj(self,scenario_id,browser):
        self.manifest["root"].append({"scenario_id":scenario_id,"browser":browser,"tcdetails":[]})
        if(scenario_id in self.temp):
            self.temp[scenario_id][browser]=len(self.manifest["root"])-1
        else :
            self.temp[scenario_id]={browser:len(self.manifest["root"])-1}
        return 1

    def shouldRollover(self, record):#1st
        return 0

    def doRollover(self):#2nd
        return 0

    def starttsp(self,tsp,scenario_id,browser):
        a = tsp.testcase_num
        name = tsp.testscript_name
        stepno = tsp.stepnum
        ind = self.temp[scenario_id][browser]
        k = self.manifest["root"][ind]["tcdetails"]
        if(a>len(k)):
            k.append({
                'tcname': name, 
                'steps': { 
                    stepno: self.logline(browser,start=True),
                }
            })
        else:
            k[a-1]['steps'][stepno] = self.logline(browser,start=True)

    def stoptsp(self,tsp,scenario_id,browser):
        count = self.logline(browser)
        i = self.temp[scenario_id][browser]
        a = tsp.testcase_num
        k = self.manifest["root"][i]["tcdetails"]
        stepno = tsp.stepnum
        k[a-1]['steps'][stepno].append(count)
        return 0
    
    def writeManifest(self):
        try:
            with open(self.manifest_path,'w+') as f:
                json.dump(self.manifest,f)
            fn = self.projectId + self.filename.replace("\\\\","/").split(".logs")[1]
            mn = self.projectId + self.manifest_path.replace("\\\\","/").split(".logs")[1]
            r = reportnfs.client.savelogs('logs',fn,self.filename)
            m = reportnfs.client.savelogs('logs',mn,self.manifest_path)
            if r =='fail' or m=='fail' :
                raise Exception('error while saving in reportNFS')
        except Exception as e:
            logger.error(e)
            err_msg = ERROR_CODE_DICT['ERR_CAPTURE_LOGS']
            print_on_console(err_msg)