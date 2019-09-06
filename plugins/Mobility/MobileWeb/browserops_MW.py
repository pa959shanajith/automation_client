#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pavan.nayak
#
# Created:     29-11-2016
# Copyright:   (c) pavan.nayak 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os
import subprocess
import re
import platform
from constants import SYSTEM_OS
import domconstants_MW
import logger
import logging
log = logging.getLogger('browserops_MW.py')
import Exceptions_MW
import mobile_server_utilities
import webconstants_MW
import mobile_key_objects

hwndg = None
status = ''
driver = None
browser = 0
class BrowserOperations():
    """
    ___init__ def
    """
    def __init__(self):
       logger.log( '------------Opening the browser ------------')
       self.status = ''
##        self.xtree = ET.parse(domconstants_MW.CONFIG_FILE)
##        self.xroot = xtree.getroot()
    """
    def: openBrowser
    param : Browser name such as CH - Chrome, IE - Internet Explorer, ANDROID - Android Chrome, and FX - Firefox
    """

    def start_server(self):
        try:
##            maindir = os.getcwd()
##            os.chdir('..')
            curdir = os.environ["NINETEEN68_HOME"]
            if (SYSTEM_OS != 'Darwin'):
                path = curdir + '/plugins/Mobility/MobileApp/node_modules/appium/build/lib/main.js'
                nodePath = curdir + "/Lib/Drivers/node.exe"
                proc = subprocess.Popen([nodePath, path], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            else:
                path = curdir + '/plugins/Mobility/node_modules/appium/build/lib/main.js'
                proc = subprocess.Popen(path, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
            time.sleep(15)
            logger.print_on_console('Server started')
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console('Exception in starting server')

    def get_device_list(self,input_val,*args):


        maindir=os.getcwd()
        devices = []
        try:
            android_home=os.environ['ANDROID_HOME']
            cmd=android_home+'\\platform-tools\\'
            os.chdir(cmd)
            cmd=cmd +'adb.exe'
            if android_home!=None:
                with open(os.devnull, 'wb') as devnull:
                    subprocess.check_call([cmd, 'start-server'], stdout=devnull,
                              stderr=devnull)
                proc = subprocess.Popen([cmd, 'devices'], stdout=subprocess.PIPE)
                for line in proc.stdout.readlines():
                    line = str(line)[2:-1]
                    line = line.rstrip('\\n\\r')
                    if "List" in line:
                        continue
                    if "offline" in line:
                        continue
                    if not line.strip():
                        continue
                    serial = line.split('\\t')
                    devices.append(serial[0])

                os.chdir(maindir)

        except Exception as e:
            log.error(e,exc_info=True)
##            logger.print_on_console(e)
        return devices

    def wifi_connect(self,*args):
        try:
            android_home=os.environ['ANDROID_HOME']
            cmd=android_home+'\\platform-tools\\'
            os.chdir(cmd)
            cmd=cmd +'adb.exe'
            if android_home!=None:
                serial=self.get_device_list(None)
                if len(serial)!=0:
                    for i in serial:
                        if ':' in i :
                            output=subprocess.check_output([cmd, 'connect',i])
                            if 'connected' in str(output) :
                                logger.print_on_console('Already connected to the network')
                                return i
                            else:
                                logger.print_on_console('Connection lost please retry')
                                return ''
                    cm=cmd + ' tcpip 5555'
                    abc=str(subprocess.check_output(cm))
                    time.sleep(5)
                    cmmmm=cmd + ' shell ip -f inet addr show wlan0'
                    out1 = str(subprocess.check_output(cmmmm))
                    b=out1[out1.find('inet'):]
                    b=b.strip('inet')
                    c=b.split('/')
                    ser=c[0] + ':5555'
                    c= cmd + ' connect ' +ser
                    o=str(subprocess.check_output(c))
                    if 'connected' in o :
                        logger.print_on_console('Both devices are connected over wifi unplug the cable')
                        return ser[1:]
                    else:
                        logger.print_on_console('Error connecting the device through wifi')
                        return ''
                else:
                    logger.print_on_console('No devices found please connect the device via usb to configure adb through WiFi')
                    return ''
        except Exception as e:
            log.error(e,exc_info=True)
##            logger.print_on_console(e)


    def stop_server(self):
        try:
            if SYSTEM_OS != 'Darwin':
                import psutil
                import os
                processes = psutil.net_connections()
                for line in processes:
                    p = line.laddr
                    if p[1] == 4723:
                        os.system("TASKKILL /F /PID " + str(line.pid))
                        logger.print_on_console('Server stopped')
            else:
                import os
                os.system("killall -9 node")
        except Exception as e:
            log.error(e,exc_info=True)
            logger.print_on_console('Exception in stopping server')

    def closeandroidBrowser(self  , *args):
         mobile_server_utilities.cleardata()
         status=webconstants_MW.TEST_RESULT_FAIL
         result=webconstants_MW.TEST_RESULT_FALSE
         value=''
         try:

            if( driver!= None):

                driver.close()

                logger.log('chrome browser closed')
                status=webconstants_MW.TEST_RESULT_PASS
                result=webconstants_MW.TEST_RESULT_TRUE
            else:
                mobile_key_objects.custom_msg.append("ERR_WEB_DRIVER_EXCEPTION")
         except Exception as e:
            log.error(e,exc_info=True)
            mobile_key_objects.custom_msg.append("ERR_WEB_DRIVER")

         mobile_key_objects.keyword_output.append(str(status))
         mobile_key_objects.keyword_output.append(str(value))

    def openBrowser(self,inputs):
        global driver
        try:
           if SYSTEM_OS == "Darwin":

               self.stop_server()
               self.start_server()
               input_list = inputs.split(';')
               time.sleep(5)
               desired_caps = {}
               desired_caps['platformName'] = 'iOS'
               desired_caps['platformVersion'] =input_list[1]
               desired_caps['deviceName'] = input_list[0]
               if len(input_list) > 2:
                   desired_caps['udid'] = input_list[2]
               desired_caps['browserName'] = 'Safari'
               desired_caps['autoWebview'] = True
               desired_caps['startIWDP'] = True
               ##desired_caps['appium-version'] = '1.4.0'
               desired_caps['fullReset'] = False
               desired_caps['newCommandTimeout'] = 3600
               desired_caps['launchTimeout'] = 180000
               driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
               logger.log('FILE: browserops_MW.py , DEF: openSafariBrowser() , MSG:  Navigating to blank page')
               driver.get(domconstants_MW.BLANK_PAGE)
               logger.log(
                   'FILE: browserops_MW.py , DEF: openSafariBrowser() , MSG:  Safari browser opened successfully')
               status = domconstants_MW.STATUS_SUCCESS
           else:
                import psutil
                import os
                processes = psutil.net_connections()
                for line in processes:
                    p = line.laddr
                    if p[1] == 4723:
                        status = domconstants_MW.STATUS_SUCCESS
                        return status
                input_list = inputs.split(';')
                device_name = input_list[0]
                if device_name == 'wifi':
                    device_name=self.wifi_connect()
                if device_name != '':
                    self.start_server()
                    time.sleep(5)
                    desired_caps = {}
                    desired_caps['platformName'] = 'Android'
                    desired_caps['platformVersion'] =input_list[1]
                    desired_caps['deviceName'] = device_name
                    desired_caps['udid'] = device_name
                    desired_caps['browserName'] = 'Chrome'
                    desired_caps['clearSystemFiles']=True
                    desired_caps['newCommandTimeout'] = '36000'
                    device_version= subprocess.check_output(["adb","-s",device_name, "shell", "getprop ro.build.version.release"])
                    device_version=str(device_version)[2:-1]
                    device_version_data =device_version.split('\\r')
                    version = device_version_data[-2]
                    if (version[0] == '\\n'):
                        version = version[1:]
                    if str(input_list[1]) == str(version):
                        driver= webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
                        logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Navigating to blank page')
                        driver.get(domconstants_MW.BLANK_PAGE)
                        logger.log('FILE: browserops_MW.py , DEF: openChromeBrowser() , MSG:  Chrome browser opened successfully')
                        status = domconstants_MW.STATUS_SUCCESS
                    else:
                        logger.log('Invalid Input')
                        mobile_key_objects.custom_msg.append("Invalid Input")
                        status = domconstants_MW.STATUS_FAIL
                        logger.print_on_console("Invalid Input")
                else:
                    status = domconstants_MW.STATUS_FAIL


        except Exception as e:
            mobile_key_objects.custom_msg.append("ERROR OCURRED WHILE OPENING BROWSER")
            status = domconstants_MW.STATUS_FAIL
            if SYSTEM_OS == 'Darwin':
                curdir = os.environ["NINETEEN68_HOME"]
                path_node_modules = curdir + '/plugins/Mobility/node_modules'
                if not os.path.exists(path_node_modules):
                    logger.print_on_console("node_modules Directory not Found in /plugins/Mobility/")
            logger.print_on_console("ERROR OCURRED WHILE OPENING BROWSER")
            log.error(e,exc_info=True)
            ##Exceptions_MW.error(e)
        return status
