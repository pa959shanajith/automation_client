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
                print subprocess.check_output([cmd, 'devices'])
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

        except Exception as e:
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,devices,err_msg

    def invoke_device(self,input_val,*args):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        output=None
        err_msg=None
        device=input_val[0]
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)

        devices = []
        try:
            android_home=os.environ['ANDROID_HOME']
            cmd=android_home+'\\platform-tools\\'
            print cmd
            os.chdir(cmd)
            cmd=cmd +'adb.exe'
            if android_home!=None:
                with open(os.devnull, 'wb') as devnull:
                    subprocess.check_call([cmd, 'start-server'], stdout=devnull,
                              stderr=devnull)
                print subprocess.check_output([cmd, 'devices'])
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
                if device is not None and device in devices:
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console(err_msg)
        return status,methodoutput,devices,err_msg

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




