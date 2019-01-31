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
                path = curdir + '/Nineteen68/plugins/Mobility/MobileApp/node_modules/appium/build/lib/main.js'
                nodePath = curdir + "/Drivers/node.exe"
                proc = subprocess.Popen([nodePath, path], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            else:
                path = curdir + '/Nineteen68/plugins/Mobility/node_modules/appium/build/lib/main.js'
                proc = subprocess.Popen(path, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
            time.sleep(15)
            logger.print_on_console('Server started')
        except Exception as e:
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
##                print subprocess.check_output([cmd, 'devices'])
                out = self.split_lines(subprocess.check_output([cmd, 'devices']))
                # The first line of `adb devices` just says "List of attached devices", so
                # skip that.
                devices = []
                for line in out[1:]:
                    if not line.strip():
                        continue
                    if 'offline' in line:
                        continue
                    serial, _ = re.split(r'\s+', line, maxsplit=1)
                    devices.append(serial)

                os.chdir(maindir)

        except Exception as e:
            logger.log(e)
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
                    if ':' in serial :
                             output=subprocess.check_output([cmd, 'connect',serial])
                             if 'connected' in output :
                                    print('already connected to the network')
                             else:
                                    print('connection lost please retry')
                    else :

                            cm=cmd + ' tcpip 5555'
                            abc=subprocess.check_output(cm)
                            time.sleep(5)
                            cmmmm=cmd + '  shell ip -f inet addr show wlan0'
                            out1 = subprocess.check_output(cmmmm)
                            b=out1[out1.find('inet'):]
                            b=b.strip('inet')
                            c=b.split('/')
                            ser=c[0] + ':5555'
                            c= cmd + ' connect ' +ser
                            o=subprocess.check_output(c)
                            if 'connected' in o :
                                print(' both devices are connected over wifi unplug the cable ')
                else:
                    print('no device found  connect the device via usb ')

                    # The first line of `adb devices` just says "List of attached devices", so
                    # skip that.


        except Exception as e:
            logger.error(e)
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
                input_list = inputs.split(';')
                if input_list[1] == 'wifi':
                    self.wifi_connect()
                else :
                    self.start_server()
                    time.sleep(5)
                    desired_caps = {}
                    desired_caps['platformName'] = 'Android'
                    desired_caps['platformVersion'] =input_list[1]
                    desired_caps['deviceName'] = input_list[0]
                    desired_caps['udid'] = input_list[0]
                    desired_caps['browserName'] = 'Chrome'
                    ##desired_caps['appium-version'] = '1.4.0'
                    desired_caps['clearSystemFiles']=True
                    desired_caps['newCommandTimeout'] = '36000'
                    device_version= subprocess.check_output(["adb", "shell", "getprop ro.build.version.release"])
                    device_version_data =device_version.split('\r')
                    if str(input_list[1]) == str(device_version_data[0]):
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


        except Exception as e:
            mobile_key_objects.custom_msg.append("ERROR OCURRED WHILE OPENING BROWSER")
            status = domconstants_MW.STATUS_FAIL
            if SYSTEM_OS == 'Darwin':
                curdir = os.environ["NINETEEN68_HOME"]
                path_node_modules = curdir + '/Nineteen68/plugins/Mobility/node_modules'
                if not os.path.exists(path_node_modules):
                    logger.print_on_console("node_modules Directory not Found in /Nineteen68/plugins/Mobility/")
            logger.print_on_console("ERROR OCURRED WHILE OPENING BROWSER")
            ##Exceptions_MW.error(e)
        return status

    def split_lines(self,s):
        """Splits lines in a way that works even on Windows and old devices.
        Windows will see \r\n instead of \n, old devices do the same, old devices
        on Windows will see \r\r\n."""
        # rstrip is used here to workaround a difference between splineslines and
        # re.split:
        # >>> 'foo\n'.splitlines()
        # ['foo']
        # >>> re.split(r'\n', 'foo\n')
        # ['foo', '']
        return re.split(r'[\r\n]+', s.rstrip())

