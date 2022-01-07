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
import logging
log = logging.getLogger('install_and_launch.py')
import logger
import time
import subprocess
import os
from constants import *
import psutil
import mobile_app_constants
import platform
import device_keywords
import android_scrapping
install_obj = android_scrapping.InstallAndLaunch()
device_keywords_object = device_keywords.Device_Keywords()
class LaunchAndInstall():

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def installApplication(self, ele, input_val, *args):
        status = mobile_app_constants.TEST_RESULT_FAIL
        result = mobile_app_constants.TEST_RESULT_FALSE
        err_msg = None
        output = OUTPUT_CONSTANT
        logger.print_on_console('Input is ',input_val)
        global device_keywords_object
        try:
            if SYSTEM_OS != 'Darwin':
                driver = install_obj.installApplication(input_val[0], input_val[1], input_val[2], None)
            else:
                driver = install_obj.installApplication(input_val[0], input_val[1], input_val[2], input_val[3])
            if driver is not None:
                status = mobile_app_constants.TEST_RESULT_PASS
                result = mobile_app_constants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg = self.print_error("Not able to install or launch application")
            log.error(e,exc_info=True)
        return status, result, output, err_msg


    def stop_server(self,input_val,*args):
        status = mobile_app_constants.TEST_RESULT_FAIL
        result = mobile_app_constants.TEST_RESULT_FALSE
        err_msg = None
        output = OUTPUT_CONSTANT
        try:
            if SYSTEM_OS != 'Darwin':
                processes = psutil.net_connections()
                for line in processes:
                    p =  line.laddr
                    if p[1] == 4723:
                        log.info( 'Pid Found' )
                        log.info(line.pid)
                        os.system("TASKKILL /F /PID " + str(line.pid))
                        android_scrapping.driver = None
                        status = mobile_app_constants.TEST_RESULT_PASS
                        result = mobile_app_constants.TEST_RESULT_TRUE
            else:
                os.system("killall -9 node_appium")
                os.system("killall -9 xcodebuild")
                status = mobile_app_constants.TEST_RESULT_PASS
                result = mobile_app_constants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg = self.print_error('Exception in stoping server')
            log.error(e,exc_info=True)
        return status,result,output,err_msg


    def uninstallApplication(self,objectname,input_val,*args):
        status=mobile_app_constants.TEST_RESULT_FAIL
        result=mobile_app_constants.TEST_RESULT_FALSE
        err_msg=None
        driver_flag = False
        output=OUTPUT_CONSTANT
        global device_keywords_object
        try:
            logger.print_on_console('Input is ',input_val)
            apk_loc = input_val[0]
            if SYSTEM_OS != 'Darwin':
                package_name = device_keywords_object.package_name(apk_loc)
                processes = psutil.net_connections()
                for line in processes:
                    p = line.laddr
                    if p[1] == 4723 and android_scrapping.driver is not None:
                        driver_flag = True
                        break
            if driver_flag is True and SYSTEM_OS != 'Darwin':
                android_scrapping.driver.remove_app(package_name)
                status = mobile_app_constants.TEST_RESULT_PASS
                result = mobile_app_constants.TEST_RESULT_TRUE
            elif SYSTEM_OS == 'Darwin':
                android_scrapping.driver.remove_app(apk_loc)#input for darwin should be bundleid
                status = mobile_app_constants.TEST_RESULT_PASS
                result = mobile_app_constants.TEST_RESULT_TRUE
            else:
                err_msg = device_keywords_object.uninstall_app(package_name, android_scrapping.device_id)
                if err_msg is None:
                    status = mobile_app_constants.TEST_RESULT_PASS
                    result = mobile_app_constants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg = self.print_error("Error occurred in Uninstall App")
            log.error(e,exc_info=True)
        return status,result,output,err_msg


    def closeApplication(self, ele, inputval, *args):
        status=mobile_app_constants.TEST_RESULT_FAIL
        result=mobile_app_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        global device_keywords_object
        try:
            logger.print_on_console("Package name to be terminated:",android_scrapping.packageName)
            if SYSTEM_OS != 'Darwin':
                err_msg = device_keywords_object.close_app(android_scrapping.packageName, android_scrapping.device_id)
            else:
                if (inputval):
                    android_scrapping.driver.terminate_app(inputval[0])
                else:
                    android_scrapping.driver.close_app()
                android_scrapping.driver.quit()
                android_scrapping.driver = None
            if err_msg is None:
                status=mobile_app_constants.TEST_RESULT_PASS
                result=mobile_app_constants.TEST_RESULT_TRUE
        except Exception as e:
            err_msg = self.print_error("Error occurred in Close App")
            log.error(e,exc_info=True)
        return status,result,output,err_msg


    def launchApp(self, ele, input_val, *args):
        status = mobile_app_constants.TEST_RESULT_FAIL
        result = mobile_app_constants.TEST_RESULT_FALSE
        err_msg = None
        driver_flag = False
        output = OUTPUT_CONSTANT
        global device_keywords_object
        apk_path = input_val[0]
        if SYSTEM_OS != 'Darwin':
            package_name = device_keywords_object.package_name(apk_path)
        try:
            if SYSTEM_OS != 'Darwin':
                processes = psutil.net_connections()
                for line in processes:
                    p = line.laddr
                    if p[1] == 4723 and android_scrapping.driver is not None:
                        driver_flag = True
                        break
            if driver_flag is True:
                android_scrapping.packageName = package_name
                activity_name = device_keywords_object.activity_name(apk_path)
                msg = device_keywords_object.launch_app(apk_path,package_name,activity_name,android_scrapping.device_id)
                if 'error' in msg.lower():
                    err_msg = self.print_error(msg)
                    status = mobile_app_constants.TEST_RESULT_FAIL
                    result = mobile_app_constants.TEST_RESULT_FALSE
                else:
                    log.info(msg)
                    status = mobile_app_constants.TEST_RESULT_PASS
                    result = mobile_app_constants.TEST_RESULT_TRUE
            else:
                status, result, output, err_msg = self.installApplication(ele, input_val)
        except Exception as e:
            err_msg = self.print_error("Error occurred in Launch App")
            log.error(e,exc_info=True)
        return status,result,output,err_msg
