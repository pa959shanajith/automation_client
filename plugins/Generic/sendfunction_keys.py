#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     09-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from generic_constants import *
from constants import *
import logger
if SYSTEM_OS != 'Darwin':
    from pyrobot import Robot
import pyautogui
import subprocess
import re
import time
from constants import *
import logging
import readconfig
configvalues = readconfig.readConfig().readJson()
delay_stringinput = float(configvalues['delay_stringinput'])
log = logging.getLogger('sendfunction_keys.py')
class SendFunctionKeys:

    def sendfunction_keys(self,input,*args):

        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_res=OUTPUT_CONSTANT

        '''For bringing the browser to foreground'''
        try:
            import browser_Keywords
            import selenium
            if SYSTEM_OS == "Darwin":
                try:
                    pids = browser_Keywords.pid_set
                    if (len(pids) > 0):
                        pid = pids.pop()
                        apple_script = """osascript<<EOF
                        tell application "System Events"
                        set frontmost of every process whose unix id is """+pid+""" to true
                        end tell
                        EOF"""
                        subprocess.Popen(apple_script, shell=True)
                except Exception as e:
                    log.error("Failed to bring window to foreground")
            else:
                import win32gui,win32api,win32process
                pids = browser_Keywords.local_bk.pid_set
                if(len(pids)>0):
                    pid = pids[-1]
                    toplist, winlist = [], []
                    def enum_cb(hwnd, results):
                        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
                    win32gui.EnumWindows(enum_cb, toplist)
                    app = [(hwnd, title) for hwnd, title in winlist if ((("Chrome" in title) or ("Firefox" in title) or ("Explorer" in title)) and (win32process.GetWindowThreadProcessId(hwnd)[1] == pid))]
                    if(len(app)==1):
                        app = app[0]
                        handle = app[0]
                        foreThread = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                        appThread = win32api.GetCurrentThreadId()
                        if( foreThread != appThread ):
                            win32process.AttachThreadInput(foreThread[0], appThread, True)
                            win32gui.BringWindowToTop(handle)
                            win32gui.ShowWindow(handle,5)
                            win32process.AttachThreadInput(foreThread[0], appThread, False)
                        else:
                            win32gui.BringWindowToTop(handle)
                            win32gui.ShowWindow(handle,5)
                    time.sleep(1)
        except Exception as e:
            log.error("Error in sendfunction_keys : ",e)
        try:
            log.debug('reading the inputs')
            input=str(input)
            if not(input is None or input is ''):
                count=self.get_args(args)
                if count == 'type':
                    log.debug('sending the keys in input')
                    self.type(input,delay_stringinput)
                else:
                    if '+' in input:
                        keys_list=input.split('+')
                        log.debug('sending multiple  keys')
                        self.press_multiple_keys(keys_list,count)

                    else:
                        log.debug('sending the keys in input')
                        self.execute_key(input,count)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            else:
                log.debug('Invalid input')
                err_msg = ERROR_CODE_DICT['ERR_INVALID_INPUT']

        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg

    def execute_key(self,key,count):
        log.debug('press and release the key', key)
        if SYSTEM_OS == "Darwin":
            for x in range(count):
                pyautogui.press(key)
        else:
            for x in range(count):
                robot=Robot()
                robot.press_and_release(key)

    def press_multiple_keys(self,keys_list,count):
        for x in range(count):
            for key in keys_list:
                self.press_key(key)
            for key in keys_list:
                self.release_key(key)

    def type(self,input):
        try:
            if SYSTEM_OS == "Darwin":
                pyautogui.typewrite(str(input))
            else:
                robot=Robot()
                robot.type_string(str(input),1)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
            err_msg=INPUT_ERROR

    def press_key(self,key):
        log.debug('pressing  the key', key)
        if SYSTEM_OS == "Darwin":
            pyautogui.keyDown(key)
        else:
            robot=Robot()
            robot.key_press(key)

    def release_key(self,key):
        log.debug('releasing  the key', key)
        if SYSTEM_OS == "Darwin":
            pyautogui.keyUp(key)
        else:
            robot=Robot()
            robot.key_release(key)

    def get_args(self,args):
        value=1
        if len(args)>1 :
            if args[0] is not None or args[0] != '':
                if (args[0].startswith('|') and args[0].endswith('|')) or (args[0].startswith('{') and args[0].endswith('}')):
                    value= 'type'
                elif args[-1]!='':
                    if (re.match(('^\d+$'),args[-1]))!=False:
                        value=int(args[-1])
        elif len(args)==1:
            if (args[0].startswith('|') and args[0].endswith('|')) or (args[0].startswith('{') and args[0].endswith('}')):
                    value= 'type'
            else:
                value=value
        return value
