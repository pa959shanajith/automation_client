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

_pump = None
_isPumpPending = False

window_name = ''

status = False
thread = None

# thread event
exit_event = None
running_event = None

core = None

def get_core(windowName = ''):
    global core, window_name
    window_name = windowName 
    if not core:
        try:
            core = Core(windowName)
            core.init_scrape_thread()
            return core
        except Exception as e:
            log.debug(e)
    return core


def terminate_core():
    global core
    if core:
        data = core.terminate()
        core = None
        return data
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

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="OEBS")
        self.Show(False)

    def on_exit(self,frame,event=None):
        wx.CallAfter(self.Destroy)
        #global frame
        if frame is not None:
            wx.CallAfter(frame.Destroy)
            frame = None

class Core():
     
    def start_thread(self):
        global thread
        try:
            thread = threading.Thread(target=self.main,args=())
            thread.setDaemon(True)
            thread.start()
            thread.set_name("OEBS_Scrape_Thread")

        except Exception as e:
            log.debug(e)

    def init_scrape_thread(self):
        global exit_event
        global running_event
        global core
        try:
            #core = oebs_core1.Core()
            #exit_event = threading.Event()
            #running_event = threading.Event()
            self.start_thread()
            #core.main(windowName)
            #running_event.wait()
            #running_event = None
            if self.dll_loaded:
                if self.res_find_window:
                    return 'Pass',""
                else:
                    try:
                        self.terminate()
                    except Exception as e:
                        log.debug(e)
                    return 'Fail','Unable to find the application'
            else:
                try:
                    self.terminate()
                except Exception as e:
                    log.debug(e)
                return 'Fail','Unable to load the dll'

        except Exception as e:
            log.debug(e)

    def __init__(self, windowName):
        self.PUMP_MAX_DELAY = 10
        self.mainThreadId = None
        self.window_name = windowName
        self.app = None
        self.frame = None
        self.res_find_window = False
        self.dll_loaded = False

    def find_window_and_attach(self,windowname='',*args):
        res,err_msg = oebs_utils.Utils().find_oebswindow_and_attach(windowname=windowname)
        return res

    def main(self,):
        try:
            self.mainThreadId = _thread.get_ident()
            self.app = wx.App()
            self.frame = Frame()
            self.app.SetAssertMode(wx.APP_ASSERT_SUPPRESS)
            try:
                oebs_api.initialize()
                self.dll_loaded = True
                log.info("initializing Java Access Bridge support")
            except Exception as e:
                log.info("Java Access Bridge not available")
                log.debug(e)
            except:
                log.debug('ERR_ACCESS_BRIDGE_INIT_ERROR')
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
                self.res_find_window = self.find_window_and_attach(windowname=self.window_name)
            # in wx self.app loop
            log.info("OEBS initialized")
            self.app.MainLoop()

        except Exception as e:
            log.debug(e)

    def get_window_name(self):
        return self.window_name

    def terminate(self):
        try:
            global exit_event
            #added local 
            thread=None
            if self.frame is not None:
                self.frame.on_exit(frame=self.frame)
            self.app = None
            self.frame = None
            # wait for the exit event
            if exit_event:
                exit_event.wait()
            #To Check the loaded bridgeDll should run after the scrape completed with debug TestCase, Commited the terminate evevent
            oebs_api.terminateEvents()
            data_rec = oebs_api.path_obj.create_file(self.window_name)

            if thread:
                thread = None
            exit_event = None
            return data_rec
        except Exception as e:
            log.debug(e)

    def _terminate(self,module, name=None):
        if name is None:
            name = module.__name__
        log.debug("Terminating %s" % name)
        try:
            module.terminate()
        except:
            log.debug("Error terminating %s" % name)

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

