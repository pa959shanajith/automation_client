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

from constants import *
from webconstants_MW import *
import subprocess
import os
import re
import logging
import logger
# import android_scrapping
import time
log = logging.getLogger('device_keywords_MW.py')

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
                    subprocess.check_call([cmd, 'start-server'], stdout=devnull, stderr=devnull, creationflags=subprocess.CREATE_NO_WINDOW)
                proc = subprocess.Popen([cmd, 'devices'], stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
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
                # err_msg = self.print_error(NO_ANDROID_HOME)
                err_msg = self.print_error("error")
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
                            output=subprocess.check_output([cmd, 'connect',i], creationflags=subprocess.CREATE_NO_WINDOW)
                            if 'connected' in str(output) :
                                logger.print_on_console('Already connected to the network')
                                return i
                            else:
                                logger.print_on_console('Connection lost please retry')
                                return ''
                    cm=cmd + ' tcpip 5555'
                    abc=str(subprocess.check_output(cm, creationflags=subprocess.CREATE_NO_WINDOW))
                    if 'TCP' in abc:
                        time.sleep(3)
                        cmmmm=cmd + ' shell ip -f inet addr show wlan0'
                        out1 = str(subprocess.check_output(cmmmm, creationflags=subprocess.CREATE_NO_WINDOW))
                        if 'error' in out1:
                            logger.print_on_console('Error connecting the device through wifi! Please restart USB debugging')
                            return ''
                        b=out1[out1.find('inet'):]
                        b=b.strip('inet')
                        c=b.split('/')
                        ser=c[0] + ':5555'
                        c= cmd + ' connect ' +ser
                        o=str(subprocess.check_output(c, creationflags=subprocess.CREATE_NO_WINDOW))
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
                    subprocess.check_call([cmd, 'start-server'], stdout=devnull, stderr=devnull, creationflags=subprocess.CREATE_NO_WINDOW)
                proc = subprocess.Popen([cmd, 'devices'], stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
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
                # err_msg = self.print_error(NO_ANDROID_HOME)
                err_msg = self.print_error("error")
        except Exception as e:
            err_msg = self.print_error("Error occurred in InvokeDevice")
            log.error(e,exc_info=True)
        return status,methodoutput,OUTPUT_CONSTANT,err_msg