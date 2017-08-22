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

log = logging.getLogger('device_keywords.py')

class Device_Keywords():


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
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
                os.chdir(maindir)

        except Exception as e:
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,devices,err_msg

    def wifi_connect(self,*args):
        try:
            android_home=os.environ['ANDROID_HOME']
            cmd=android_home+'\\platform-tools\\'
            os.chdir(cmd)
            cmd=cmd +'adb.exe'
            if android_home!=None:
                a,b,serial,d=self.get_device_list(None)

                if len(serial)!=0:
                    if ':' in serial :
                             output=subprocess.check_output([cmd, 'connect',out])
                             if 'connected' in output :
                                    print 'already connected to the network'
                             else:
                                    print 'connection lost please retry'
                    else :
                            cm=cmd + ' tcpip 5555'
                            abc=subprocess.check_output(cm)
                            import time
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
                                print ' both devices areconnected over wifi unplug the cable '
                else:
                    print 'no device found pls connect connect the device via usb '

                    # The first line of `adb devices` just says "List of attached devices", so
                    # skip that.


        except Exception as e:
            log.error(e)
            logger.print_on_console(err_msg)


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
                if device is not None and device[0] in devices:
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                os.chdir(maindir)
        except Exception as e:
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,OUTPUT_CONSTANT,err_msg

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




