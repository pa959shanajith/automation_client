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
#import appium
#from appium import webdriver
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
driver = android_scrapping.driver
device_keywords_object = device_keywords.Device_Keywords()
#device_id=None
class LaunchAndInstall():

    def installApplication(self, ele, input_val, *args):
        status = mobile_app_constants.TEST_RESULT_FAIL
        result = mobile_app_constants.TEST_RESULT_FALSE
        err_msg = None
        output = OUTPUT_CONSTANT
        logger.print_on_console('Input is ',input_val)
        global driver, device_keywords_object
        try:
            if SYSTEM_OS != 'Darwin':
                #global device_id
                # device_id=input_val[2]
                # apk_path = input_val[0]
                # activityName = device_keywords_object.activity_name(apk_path)
                # packageName = device_keywords_object.package_name(apk_path)
                # #logger.print_on_console("Apk path:",apk_path)
                # #logger.print_on_console("Package name:",packageName)
                # #logger.print_on_console("Activity name:",activityName)
                # if device_id == 'wifi':
                #     device_id = device_keywords_object.wifi_connect()
                #     logger.print_on_console("Connected device name:",device_id)
                # if device_id != '':
                #     self.start_server()
                #     desired_caps = {}
                #     desired_caps['platformName'] = 'Android'
                #     desired_caps['platformVersion'] = input_val[1]
                #     desired_caps['deviceName'] = device_id
                #     desired_caps['udid'] = device_id
                #     desired_caps['noReset'] = True
                #     desired_caps['newCommandTimeout'] = 0
                #     desired_caps['app'] = apk_path
                #     desired_caps['sessionOverride'] = True
                #     desired_caps['fullReset'] = False
                #     desired_caps['logLevel'] = 'debug'
                #     desired_caps['appPackage'] = packageName
                #     desired_caps['appActivity'] = activityName
                #     driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
                #     self.driver_obj = driver
                driver = install_obj.installApplication(input_val[0], input_val[1], input_val[2], None)
                #self.driver_obj = driver
                status = mobile_app_constants.TEST_RESULT_PASS
                result = mobile_app_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console(e)
            err_msg = "Not able to install or launch application"
        return status, result, output, err_msg

    def start_server(self):
        try:
            curdir = os.environ["NINETEEN68_HOME"]
            if (SYSTEM_OS != 'Darwin'):
                path = curdir + '/Nineteen68/plugins/Mobility/MobileApp/node_modules/appium/build/lib/main.js'
                nodePath = curdir + "/Drivers" + '/node.exe'
                proc = subprocess.Popen([nodePath, path], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            else:
                path = curdir + '/Nineteen68/plugins/Mobility/node_modules/appium/build/lib/main.js'
                proc = subprocess.Popen(path, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
            time.sleep(15)
            logger.print_on_console('Server started')
        except Exception as e:
            log.error(e)
            logger.print_on_console('Exception in starting server')
            logger.print_on_console(e)

    def stop_server(self,input_val,*args):
        status = mobile_app_constants.TEST_RESULT_FAIL
        result = mobile_app_constants.TEST_RESULT_FALSE
        err_msg = None
        output = OUTPUT_CONSTANT
        global driver
        try:
            if SYSTEM_OS != 'Darwin':
                processes = psutil.net_connections()
                for line in processes:
                    p =  line.laddr
                    if p[1] == 4723:
                        log.info( 'Pid Found' )
                        log.info(line.pid)
                        os.system("TASKKILL /F /PID " + str(line.pid))
                        driver = None
                        status = mobile_app_constants.TEST_RESULT_PASS
                        result = mobile_app_constants.TEST_RESULT_TRUE
            else:
                os.system("killall -9 node")
                status = mobile_app_constants.TEST_RESULT_PASS
                result = mobile_app_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console('Exception in stoping server')
            logger.print_on_console(e)
            err_msg = 'Exception in stoping server'
        return status,result,output,err_msg

    def uninstallApplication(self,objectname,input_val,*args):
        status=mobile_app_constants.TEST_RESULT_FAIL
        result=mobile_app_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        global driver,device_keywords_object
        try:
            logger.print_on_console('Input is ',input_val)
            apk_loc = input_val[0]
            package_name = device_keywords_object.package_name(apk_loc)
            processes = psutil.net_connections()
            for line in processes:
                p = line.laddr
                if p[1] == 4723 and driver is not None:
                    driver_flag = True
                    break
            if driver_flag is True:
                driver.remove_app(package_name)
            else:
                device_keywords_object.uninstall_app(package_name, android_scrapping.device_id)
            status = mobile_app_constants.TEST_RESULT_PASS
            result = mobile_app_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console(e)
        return status,result,output,err_msg

    def closeApplication(self,inputval,*args):
        status=mobile_app_constants.TEST_RESULT_FAIL
        result=mobile_app_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        global driver, device_keywords_object
        try:
            # processes = psutil.net_connections()
            # for line in processes:
            #     p = line.laddr
            #     if p[1] == 4723 and driver is not None:
            #         driver_flag = True
            #         break
            # if driver_flag is True:
            logger.print_on_console("Package name to be terminated:"+android_scrapping.packageName)
            device_keywords_object.close_app(android_scrapping.packageName, android_scrapping.device_id)
            status=mobile_app_constants.TEST_RESULT_PASS
            result=mobile_app_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console(e)
            ##err_msg = 'Exception in closing application'
        return status,result,output,err_msg

    def launchApp(self, ele, input_val, *args):
        status = mobile_app_constants.TEST_RESULT_FAIL
        result = mobile_app_constants.TEST_RESULT_FALSE
        err_msg = None
        driver_flag = False
        output = OUTPUT_CONSTANT
        #logger.print_on_console('Input is ', input_val)
        global driver,device_keywords_object
        apk_path = input_val[0]
        package_name = device_keywords_object.package_name(apk_path)
        try:
            processes = psutil.net_connections()
            for line in processes:
                p = line.laddr
                if p[1] == 4723 and driver is not None:
                    driver_flag = True
                    break
            if driver_flag is True:
                android_scrapping.packageName = package_name
                activity_name = device_keywords_object.activity_name(apk_path)
                #driver.start_activity(package_name,activity_name)
                msg = device_keywords_object.launch_app(apk_path,package_name,activity_name,android_scrapping.device_id)
                if 'Error' in msg:
                    log.error(msg)
                    status = mobile_app_constants.TEST_RESULT_FAIL
                    result = mobile_app_constants.TEST_RESULT_FALSE
                    err_msg = msg
                else:
                    log.info(msg)
                    status = mobile_app_constants.TEST_RESULT_PASS
                    result = mobile_app_constants.TEST_RESULT_TRUE
            else:
                status, result, output, err_msg = self.installApplication(ele, input_val)
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console(e)
        return status,result,output,err_msg
