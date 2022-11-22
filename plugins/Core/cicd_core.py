import logging
import os
import json
from urllib import response
import sys
import logger
import requests
import core
from constants import *

log = logging.getLogger('cicd_core.py')
configvalues={}
proxies=None
root=None
browsercheckFlag=False
updatecheckFlag=False
cicd_isheadless = 'No'
iscicd = False

class CiCdCore():
    def __init__(self, appName, args):
        self.opts = args
        self.name = appName
        self.gui = False
        self.cw = None
        self.testthread = None
        self.socketthread = None
        self.icesession = None
        self.server_url = None
        global root, browsercheckFlag, updatecheckFlag, cicd_isheadless, iscicd
        root = self
        core.root = self
        updatecheckFlag = configvalues['update_check'].lower() == 'no'
        browsercheckFlag = configvalues['browser_check'].lower() == 'no'
        is_config_missing = 'configmissing' in configvalues
        is_config_invalid = 'errorflag' in configvalues
        logfilename_error_flag = False

        self.print_banner()
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.CRITICAL)

        if is_config_missing:
            err = "[Error]: config.json file is empty/missing. Please provide a valid configuration. Please check and restart "+appName+"."
            logger.print_on_console(err)
            log.info(err)
        elif is_config_invalid:
            err = "[Error]: Syntax error in config file.\n"+str(configvalues['errorflag'])+ " config field is missing. Please check and restart "+appName+"."
            logger.print_on_console(err)
            log.info(err)
            log.error(configvalues['errorflag'])
        elif logfilename_error_flag:
            err = "[Error]: Please provide a valid logfile path in config file and restart "+appName+"."
            logger.print_on_console(err)
            log.info(err)
            logfilename_error_flag = False

        try:
            cicd_path = os.path.normpath(AVO_ASSURE_HOME + '/logs/' + 'Avoclient_' + args.instanceid  + '.log')
            logfilename = os.path.normpath(cicd_path).replace("\\","\\\\")
            logging.config.fileConfig(LOGCONFIG_PATH,defaults={'logfilename': logfilename},disable_existing_loggers=False)
        except Exception as e:
            logfilename_error_flag = True
            log.error(e)
        if args.screenshotpath:
            try:
                import constants
                constants.SCREENSHOT_PATH = args.screenshotpath + OS_SEP
            except Exception as e:
                log.error(e)
        exec_req = self.fetchExecutionReq()
        iscicd = True
        md_name = exec_req['suitedetails'][0]['testsuitename']
        log.info('%s Module Execution Started', md_name)
        log.info('===============================================================================')
        logger.print_on_console( md_name + '  Module Execution Started')
        if exec_req['isHeadless']:
            cicd_isheadless = 'Yes'
        aws_mode=False
        if exec_req != None and exec_req['apptype']=='MobileApp':
            if args[0]['suitedetails'][0]['browserType'][0]=='2':
                aws_mode = True
        self.testthread = core.TestThread(root, EXECUTE, exec_req, aws_mode, cicd_mode=True)

        

        #API to send back COMPLETED status

        #close the ICE

    def print_banner(self):
        print('********************************************************************************************************')
        print('============================================ '+self.name+' ============================================')
        print('********************************************************************************************************')
        
    def fetchExecutionReq(self):
        try:
            dataToServer = {"configkey":self.opts.configkey, "executionListId":self.opts.executionListId}
            server_url = 'https://' + self.opts.serverurl + ':' + self.opts.serverport + '/getExecScenario'
            logger.print_on_console("Fetching Execution Request Using configkey : "+ self.opts.configkey)
            res = requests.post(server_url, json=dataToServer, verify=False)
            response = res.json()
            if res.status_code == 200  and response["status"] != "fail":
                # import core
                # core.plugins_list = response["plugins"]
                # Change it after API integration
                return response["status"][0]["executionRequest"]
            else:
                info_msg = "Response status is fail and execution request is None"
                log.info(info_msg)
                logger.print_on_console(info_msg)
                sys.exit("Execution response status is fail and execution request is None")
        except Exception as ex:
            err_msg = 'Error while Fetching Execution Request Using Configuration Key'
            log.error(err_msg)
            logger.print_on_console(err_msg)
            log.error(ex, exc_info=True)
