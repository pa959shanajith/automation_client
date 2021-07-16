import traceback
import time
import win32gui
import threading
import sys
import logging
log=logging.getLogger('oebs_start.py')
import oebs_api
import _thread
import os
import ctypes
import wx
import re
import win32process
import oebs_utils
from oebs_constants import *
import logger
_pump = None
_isPumpPending = False
window = ''
status = False
core = None

def init_core(windowName = ''):
    global core, window
    window = windowName 
    try:
        core = Core(windowName)
        core.init_scrape()
    except Exception as e:
        log.debug(e)
        log.error(ERROR_CODE_DICT['err_init_core'])
        logger.print_on_console(ERROR_CODE_DICT['err_click_add'])
    
def get_core():
    global core
    return core


def terminate_core():
    global core, window, exit_event, data
    data, err = '', ERROR_CODE_DICT['err_click_add']
    if core:
        try:
            oebs_api.terminateEvents()
            if oebs_api.path_obj:
                data = oebs_api.path_obj.create_file(core.window_name)
                err = None
        except Exception as e:
            log.error(err)
            log.debug(e)
        core = None
        window = None
    return data, err

class Timer(object):
    def __init__(self):
        self.status = False

    def IsRunning(self):
        return self.status

    def Start(self,milliseconds=-1,oneShot=False):
        self.status = True
        try:
            time.sleep(milliseconds/1000.0)
        except:
            log.debug("TIME ERROR")
        self.run()
        self.status = False

class NonReEntrantTimer(Timer):
    """
    Before WXPython 4, wx.Timer was nonre-entrant,
    meaning that if code within its callback pumped messages (E.g. called wx.Yield) and this timer was ready to fire again,
    the timer would not fire until the first callback had completed.
    However, in WXPython 4, wx.Timer is now re-entrant.
    Code in NVDA is not written to handle re-entrant timers, so this class provides a Timer with the old behaviour.
    This should be used in place of wx.Timer and wx.PyTimer where the callback will directly or indirectly call wx.Yield or some how process the Windows window message queue.
    For example, NVDA's core pump or other timers that run in NVDA's main thread.
    Timers on braille display drivers for key detection don't need to use this as they only queue gestures rather than actually executing them.
    """
    # If some issue with Timer class, go with wx.Timer

    def __init__(self, run=None):
        if run is not None:
            self.run = run
        self._inNotify = False
        super(NonReEntrantTimer,self).__init__()

    def run(self):
        """Subclasses can override or specify in constructor.
        """
        raise NotImplementedError

    def Notify(self):
        if self._inNotify:
            return
        self._inNotify = True
        try:
            self.run()
        finally:
            self._inNotify = False

class Core():
     
    def init_scrape(self):
        self.main()
        if self.dll_loaded:
            if self.res_find_window:
                return 'Pass',""
            else:
                raise Exception(ERROR_CODE_DICT['err_res_window'])
        raise Exception(ERROR_CODE_DICT['err_load_dll'])
        
    def __init__(self, windowName):
        self.PUMP_MAX_DELAY = 10
        self.mainThreadId = None
        self.window_name = windowName
        self.res_find_window = False
        self.dll_loaded = False


    def find_window_and_attach(self,windowname='',*args):
        res, err_msg = oebs_utils.Utils().find_oebswindow_and_attach(windowname=windowname)
        return res, err_msg

    def main(self,):
        try:
            self.mainThreadId = _thread.get_ident()
            try:
                oebs_api.initialize()
                self.dll_loaded = True
                log.info("initializing Java Access Bridge support")
            except Exception as e:
                log.error(ERROR_CODE_DICT['err_jab'])
                log.debug(e)
                return
            except:
                log.error(ERROR_CODE_DICT['err_jab_base'])
                return
            # Doing this here is a bit ugly, but we don't want these modules imported
            # at module level, including wx.
            log.info("Initializing core pump")
            class CorePump(NonReEntrantTimer):
                def run(self):
                    global _isPumpPending , _pump
                    _isPumpPending = False
                    try:
                        oebs_api.pumpAll()
                        #oebs_queue_handler.pumpAll()
                    except Exception as e:
                        log.debug(e)
                    if _isPumpPending and not _pump.IsRunning():
                        # As our pump is not re-entrant, schedule another pump.
                        _pump.Start(10, True)

            global _pump,_isPumpPending

            _pump = CorePump()

            self.requestPump()
            if self.dll_loaded:
                self.res_find_window, err = self.find_window_and_attach(windowname=self.window_name)

            if err and err != '':
                log.error(err)
                logger.print_on_console(ERROR_CODE_DICT['err_attach_window'])

        except Exception as e:
            log.debug(e)
            log.error(ERROR_CODE_DICT['err_run_dll'])



    def requestPump(self):
        """Request a core pump.
        This will perform any queued activity.
        It is delayed slightly so that queues can implement rate limiting,
        filter extraneous events, etc.
        """
        global _isPumpPending,_pump
        if not _pump or _isPumpPending:
            return
        _isPumpPending = True
        if _thread.get_ident() == self.mainThreadId:
            _pump.Start(10, True)
            return

