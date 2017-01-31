#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     16-01-2017
# Copyright:   (c) rakesh.v 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from appium import webdriver
import logging
log = logging.getLogger('install_and_launch.py')
import logger
from constants import *
driver = None

class LaunchAndInstall():

    def installApplication(self,ele,input_val,*args):
        status=mobile_app_constants.TEST_RESULT_FAIL
        result=mobile_app_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            LaunchAndInstall().start_server()
            desired_caps = {}
            desired_caps['platformName'] = 'Android'
            desired_caps['platformVersion'] = input_val[1]
            desired_caps['deviceName'] = input_val[2]
            desired_caps['noReset'] = True
            desired_caps['newCommandTimeout'] = 0
            ##desired_caps['app'] = 'D:\\mobility\\selendroid-test-app-0.17.0.apk'
            desired_caps['app'] = input_val[0]
            desired_caps['sessionOverride'] = True
            desired_caps['fullReset'] = False
            desired_caps['logLevel'] = 'debug'
            global driver
            driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
            status=mobile_app_constants.TEST_RESULT_PASS
            result=mobile_app_constants.TEST_RESULT_TRUE
##            import time
##            time.sleep(20)
##            page_source = driver.page_source
##            print page_source
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg = "Not able to install or launch application"
        return status,result,output,err_msg

    def start_server(self):
        try:
            import subprocess
            import os
            maindir = os.getcwd()
            os.chdir('..')
            curdir = os.getcwd()
            path= curdir + '//Nineteen68//plugins//Mobility//node_modules//appium//build//lib//main.js'
##            path='C:\\Nineteen68\\plugins\\Mobility\\node_modules\\appium\\build\\lib\main.js'
            log.info('Server file path')
            log.info(path)
            nodePath = maindir+'//node.exe'
            log.info(nodePath)
##            print ' logic to start server'
##            file_path = 'D:\\mobile_python\\node_modules\\appium\\build\\lib\\main.js'
            proc = subprocess.Popen([nodePath, path], shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
            import time
            time.sleep(15)
            logger.print_on_console('Server started')
            os.chdir(maindir)
        except Exception as e:
            log.error(e)
            logger.print_on_console('Exception in starting server')
            logger.print_on_console(e)

    def stop_server(self):
        try:
            import psutil
            import os
            processes = psutil.net_connections()
            for line in processes:
                p =  line.laddr
                if p[1] == 4723:
                    log.info( 'Pid Found' )
                    log.info(line.pid)
                    os.system("TASKKILL /F /PID " + str(line.pid))
        except Exception as e:
            log.error(e)
            logger.print_on_console('Exception in stoping server')
            logger.print_on_console(e)

    def uninstallApplication(self,input_val):
        status=mobile_app_constants.TEST_RESULT_FAIL
        result=mobile_app_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            apk_loc = input_val[0]
            from apk import APK
            apkf = APK(apk_loc)
            package_name = None
            package_name = apkf.get_package
            log.debug(' package_name')
            log.debug( package_name)
            global driver
            driver.remove_app(package_name)
            status=mobile_app_constants.TEST_RESULT_PASS
            result=mobile_app_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)

    def closeApplication(self):
        status=mobile_app_constants.TEST_RESULT_FAIL
        result=mobile_app_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        try:
            global driver
            driver.quit()
            status=mobile_app_constants.TEST_RESULT_PASS
            result=mobile_app_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg = 'Exception in closing application'
        return status,result,output,err_msg



##obj  = LaunchAndInstall()
##obj.start_server()
##obj.installApplication('x')
##obj.stop_server()
