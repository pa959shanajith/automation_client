#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     23-01-2017
# Copyright:   (c) prudhvi.gujjuboyina 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from constants import *
from mobile_app_constants import *
import subprocess
import os
import re
import logging
import logger
import android_scrapping
import time
log = logging.getLogger('device_keywords.py')

class Device_Keywords():

    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def get_device_list(self,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        maindir=os.getcwd()
        devices = []
        try:
            android_home=os.environ['ANDROID_HOME']
            cmd=android_home+'\\platform-tools\\'
            os.chdir(cmd)
            cmd=cmd +'adb.exe'
            if android_home!=None:
                with open(os.devnull, 'wb') as devnull:
                    subprocess.check_call([cmd, 'start-server'], stdout=devnull, stderr=devnull)
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
                output = devices
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
                os.chdir(maindir)
            else:
                err_msg = self.print_error(NO_ANDROID_HOME)
        except Exception as e:
            err_msg = self.print_error("Error occurred in GetDevices")
            log.error(e,exc_info=True)
        return status,methodoutput,output,err_msg


    def wifi_connect(self,*args):
        try:
            err_msg=None
            android_home=os.environ['ANDROID_HOME']
            cmd=android_home+'\\platform-tools\\'
            os.chdir(cmd)
            cmd=cmd +'adb.exe'
            if android_home!=None:
                a,b,serial,d=self.get_device_list(None)
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
                    if 'TCP' in abc:
                        time.sleep(3)
                        cmmmm=cmd + ' shell ip -f inet addr show wlan0'
                        out1 = str(subprocess.check_output(cmmmm))
                        if 'error' in out1:
                            logger.print_on_console('Error connecting the device through wifi! Please restart USB debugging')
                            return ''
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
                            logger.print_on_console('Error connecting the device through wifi! Please restart USB debugging')
                            return ''
                    else:
                        logger.print_on_console('Error connecting the device through wifi! Please restart USB debugging')
                        return ''
                else:
                    logger.print_on_console('No devices found please connect the device via usb to configure adb through WiFi')
                    return ''
            else:
                logger.print_on_console('ANDROID_HOME not set in system path')
        except Exception as e:
            err_msg = self.print_error("Error occurred in WifiConnect")
            log.error(e,exc_info=True)


    def invoke_device(self,input_val,*args):
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=OUTPUT_CONSTANT
        err_msg=None
        devices = []
        device=None
        maindir=os.getcwd()
        try:
            device=args[0]
            log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
            android_home=os.environ['ANDROID_HOME']
            cmd=android_home+'\\platform-tools\\'
            os.chdir(cmd)
            cmd=cmd +'adb.exe'
            if android_home!=None:
                with open(os.devnull, 'wb') as devnull:
                    subprocess.check_call([cmd, 'start-server'], stdout=devnull, stderr=devnull)
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
                if device is not None and device in devices:
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                os.chdir(maindir)
            else:
                err_msg = self.print_error(NO_ANDROID_HOME)
        except Exception as e:
            err_msg = self.print_error("Error occurred in InvokeDevice")
            log.error(e,exc_info=True)
        return status,methodoutput,OUTPUT_CONSTANT,err_msg


    def package_name(self,apk):
        packageName = None
        maindir=os.getcwd()
        try:
            # aapt_home=os.environ['AAPT_HOME']
            aapt_home=os.environ['ANDROID_HOME']+"\\build-tools\\33.0.1\\"
            if aapt_home != None:
                cmd=aapt_home
                os.chdir(cmd)
                cmd = cmd + 'aapt.exe'
                out = subprocess.Popen([cmd, 'dump','badging',apk],stdout= subprocess.PIPE, close_fds=True)
                for line in out.stdout.readlines():
                    curr_line = str(line)[2:-1]
                    if 'package:' in curr_line:
                        curr_line = curr_line.strip().split()
                        packageName = curr_line[1][6:-1]
                        break
            else:
                err_msg = self.print_error(NO_AAPT_HOME)
            os.chdir(maindir)
        except Exception as e:
            err_msg = self.print_error("Error occurred in Fetching Package")
            log.error(e,exc_info=True)
        return packageName


    def activity_name(self, apk):
        activityName = None
        maindir=os.getcwd()
        try:
            # aapt_home=os.environ['AAPT_HOME']
            aapt_home=os.environ['ANDROID_HOME']+"\\build-tools\\33.0.1\\"
            if aapt_home != None:
                cmd=aapt_home
                os.chdir(cmd)
                cmd = cmd + 'aapt.exe'
                out = subprocess.Popen([cmd, 'dump', 'badging', apk],stdout= subprocess.PIPE, close_fds=True)
                for line in out.stdout.readlines():
                    curr_line = str(line)[2:-1]
                    if 'launchable' in curr_line:
                        curr_line = curr_line.strip().split()
                        activityName = curr_line[1][6:-1]
                        break
            else:
                err_msg = self.print_error(NO_AAPT_HOME)
            os.chdir(maindir)
        except Exception as e:
            err_msg = self.print_error("Error occurred in Fetching Activity")
            log.error(e,exc_info=True)
        return activityName


    def uninstall_app(self, pkg, device):
        maindir = os.getcwd()
        flag = False
        err_msg = None
        try:
            android_home = os.environ['ANDROID_HOME']
            cmd = android_home + '\\platform-tools\\'
            os.chdir(cmd)
            cmd = cmd + 'adb.exe'
            if android_home is not None:
                if device is not None:
                    c = cmd+ ' -s '+ device+ ' uninstall '+ pkg
                else:
                    c = cmd+ ' uninstall '+ pkg
                out = str(subprocess.check_output(c))
                if 'Success' in out:
                    flag = True
                os.chdir(maindir)
                if flag is False:
                    raise Exception('Error Uninstalling App using adb; App not installed')
            else:
                err_msg = self.print_error(NO_ANDROID_HOME)
        except Exception as e:
            err_msg = self.print_error("Error occurred in Uninstall App")
            log.error(e, exc_info=True)
        return err_msg


    def close_app(self, pkg, device):
        maindir = os.getcwd()
        flag = False
        err_msg = None
        try:
            android_home = os.environ['ANDROID_HOME']
            cmd = android_home + '\\platform-tools\\'
            os.chdir(cmd)
            cmd = cmd + 'adb.exe'
            if android_home is not None:
                if pkg is not None and device is not None:
                    cmd1=cmd + ' -s ' + device + ' shell am force-stop ' + pkg
                    out = subprocess.check_output(cmd1)
                else:
                    raise Exception('Driver not running; App not launched')
                os.chdir(maindir)
            else:
                err_msg = self.print_error(NO_ANDROID_HOME)
        except Exception as e:
            err_msg = self.print_error("Error occurred in Close App")
            log.error(e,exc_info=True)
        return err_msg


    def launch_app(self, apk_path, package, activity, device):
        maindir = os.getcwd()
        try:
            result = 'Error in Starting App'
            result1 = ' App already installed; '
            connected = 'Connection error;'
            android_home = os.environ['ANDROID_HOME']
            cmd = android_home + '\\platform-tools\\'
            os.chdir(cmd)
            cmd = cmd + 'adb.exe'
            cmp = package+'/'+activity
            o1, o2, o3, o4 = self.get_device_list(None)
            for i in o3:
                if device == i:
                    connected = 'Connected;'
                    break
            if android_home is not None:
                if not(android_scrapping.driver.is_app_installed(package)):
                    install = subprocess.Popen([cmd, '-s', device, 'install', apk_path], stdout=subprocess.PIPE)
                    for line in install.stdout.readlines():
                        curr_line = str(line)[2:-1]
                        if 'Success' in curr_line:
                            result1 = ' App installed; '
                            break
                time.sleep(3)
                out = subprocess.Popen([cmd, '-s', device, 'shell', 'am', 'start', '-a', 'android.intent.action.MAIN', '-n', cmp], stdout=subprocess.PIPE)
                for line in out.stdout.readlines():
                    curr_line = str(line)[2:-1]
                    if 'Starting' in curr_line:
                        result = 'Starting App'
                    if 'Warning' in curr_line:
                        result = 'App was already started; Its current task has been brought to the front'
                        break
                    if 'Error' in curr_line:
                        result = 'Error in Starting App'
                        break
            else:
                err_msg = self.print_error(NO_ANDROID_HOME)
            os.chdir(maindir)
        except Exception as e:
            err_msg = self.print_error('Error in Starting App')
            log.error(e, exc_info=True)
        return connected+result1+result
