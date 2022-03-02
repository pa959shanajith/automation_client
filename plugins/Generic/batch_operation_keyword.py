#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     24-10-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import subprocess

from pip import main
import generic_constants
import os
import logger
from constants import *
import time
if SYSTEM_OS=='Windows':
    import win32api,win32gui,win32print
    from pywinauto import Application
    import pywinauto
import logging


log = logging.getLogger('batch_operation_keyword.py')
class BatchOperationKeyword():
    def __get_file_dialog_handle(self):
        hwnds=[]
        def winEnum(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == 'Save Print Output As':
                hwnds.append(hwnd)
        win32gui.EnumWindows(winEnum, hwnds)
        handle = hwnds[0] if (len(hwnds) > 0) else None
        return handle
    def __save_as_output_time_func(self, tries=10, time_sleep=0.75):
        while tries > 0:
            win_handle = self.__get_file_dialog_handle()
            if win_handle is not None:
                log.info("Window handle found: %s", win_handle)
                return win_handle
            time.sleep(time_sleep)
            tries -= 1
        return None
    def executeFile(self, filePath,*args):
        #logger.print_on_console('Executing keyword : executeFile')
        status=TEST_RESULT_FAIL
        methodoutput=TEST_RESULT_FALSE
        err_msg=None
        output_res=OUTPUT_CONSTANT
        tries=10
        time_sleep=0.5
        pdf_file=args[0]
        try:
            log.debug('reading the inputs')
            filename,file_ext=os.path.splitext(filePath)
            if  file_ext in generic_constants.BATCH_FILE_TYPE or  file_ext in generic_constants.EXE_FILE_TYPE:
                if pdf_file=='':
                    log.debug('executing .bat or .exe file')
                    logger.print_on_console('executing .bat or .exe file')
                    p = subprocess.Popen(filePath,cwd=os.path.dirname(filePath), creationflags=subprocess.CREATE_NEW_CONSOLE)
                    status=TEST_RESULT_PASS
                    methodoutput=TEST_RESULT_TRUE
                elif pdf_file and os.path.splitext(pdf_file)[1]=='.pdf':
                    file_name = os.path.split(pdf_file)[1]
                    exe_name = os.path.split(filePath)[1]
                    temp_file_loc = os.environ['AVO_ASSURE_HOME'] +os.sep+"output"+os.sep+file_name
                    import psutil
                    for proc in psutil.process_iter():
                        if proc.name() == exe_name:
                            proc.kill()
                    if os.path.isfile(temp_file_loc):
                        os.remove(temp_file_loc)
                    # win32api.ShellExecute(0, "print", filePath, None, ".", 0)
                    subprocess.Popen([filePath, " /t ", pdf_file, " Microsoft Print To PDF"])
                    connect_tries=20
                    connect_sl=0.1
                    while connect_tries>0:
                        for proc in psutil.process_iter():
                            try:
                                if proc.name() == exe_name:
                                    appId = proc.pid
                                    app_1 = Application().connect(process=appId)
                                    connect_tries=0
                                    break
                            except Exception as e:
                                log.debug("Exception occured while connecting to the Acrobat")
                                connect_tries = connect_tries-1
                                time.sleep(connect_sl)
                                if connect_tries == 0:
                                    log.debug("Tried connecting to the Acrobat process. Process not launched")
                                    msg = "Tried connecting to "+exe_name+" . Process not launched"
                                    logger.print_on_console(msg)
                                break
                    win_handle = self.__save_as_output_time_func(tries,time_sleep)
                    if win_handle is not None:
                        win32gui.SetForegroundWindow(win_handle)
                        app = Application().connect(handle=win_handle, allow_magic_lookup=False)
                        main_window = app[win32gui.GetWindowText(win_handle)]
                        main_window.wait('exists enabled visible ready')
                        main_window.set_focus()
                        temp=temp_file_loc
                        main_window['5'].type_keys(temp_file_loc.replace(' ', '{SPACE}')+"{ENTER}")
                        time.sleep(2)
                        log.debug("AdobeLive Form PDf flattened and placed in ")
                        log.debug(temp)
                        status = TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
                    else:
                        log.debug("Window not found")
                    for proc in psutil.process_iter():
                        if proc.name() == exe_name:
                            proc.kill()

            elif file_ext in generic_constants.VBS_FILE_TYPE:
                log.debug('executing .vbs file')
                logger.print_on_console('executing .vbs file')
                os.chdir(os.path.dirname(filePath))
                os.startfile(filePath)
                status=TEST_RESULT_PASS
                methodoutput=TEST_RESULT_TRUE
            else:
                log.debug('Invalid file format')
                logger.print_on_console(generic_constants.INVALID_FILE_FORMAT)
        except Exception as e:
            log.error(e)
            err_msg=INPUT_ERROR
            logger.print_on_console(err_msg)
        return status,methodoutput,output_res,err_msg

def a():
    import psutil,pywinauto
    pid=10001
    execpt=True
    connect_tries=10
    connect_sl=0.1
    outer_cnt=10
    inner_cnt=10
    while execpt:
        print("wh", connect_tries, execpt)
        for proc in psutil.process_iter():
            try:
                app_1 = pywinauto.Application().connect(process=pid)
                execpt=False
            except:
                connect_tries=connect_tries-1
                if connect_tries==0:
                    print("cnt 0")
                    execpt =False
                    print("Exception ",execpt)
                break
