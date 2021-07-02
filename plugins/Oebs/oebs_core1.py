import sys
import _thread
import os
import time
import ctypes
import wx
import re
import logging
log=logging.getLogger('oebs_core1.py')
import win32gui
import win32process
import threading
import re
import oebs_api

_pump = None
_isPumpPending = False

global window_name

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

    def __init__(self):
        self.PUMP_MAX_DELAY = 10
        self.mainThreadId = None
        self.window_name = ''
        self.app = None
        self.frame = None
        self.res_find_window = False
        self.dll_loaded = False

    def set_to_foreground(self,window_name=''):
        try:
            aut_handle = win32gui.FindWindow(None,window_name)
            if aut_handle > 0:
                foreground = win32gui.GetForegroundWindow()
                application_pid = win32process.GetWindowThreadProcessId(aut_handle)
                foreground_pid = win32process.GetWindowThreadProcessId(foreground)
                if application_pid != foreground_pid:
                    process_id = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                    i = win32gui.GetWindowRect(aut_handle)
                    if i[0] <= -32000:
                        fg_thread, fg_process = win32process.GetWindowThreadProcessId(foreground)
                        aut_thread, aut_process = win32process.GetWindowThreadProcessId(aut_handle)
                        win32process.AttachThreadInput(aut_thread, fg_thread, True)
                        self.bring_to_top(aut_handle,4)
                        return True
                    else:
                        self.bring_to_top(aut_handle,5)
                        return True
                else:
                    self.bring_to_top(aut_handle,1)
                    return True
        except Exception as e:
            log.debug(e)
        return False

    def bring_to_top(self,aut_handle,value):
        try:
            win32gui.BringWindowToTop(aut_handle)
            win32gui.ShowWindow(aut_handle,value)
            win32gui.SetForegroundWindow(aut_handle)
        except Exception as e:
            log.debug(e)

    def find_oebswindow_and_attach(self,windowname,*args):
        log.info('windowname is '+windowname)
        status=False
        err_msg=None
        new_window_name = None
        try:
            #import oebs_rpc
            import time
            load_timeout=1
            if len(args)>0:
                load_timeout=args[0]

            if not(windowname is None and windowname is ''):
                start_time = time.time()
                while (time.time() - start_time) < load_timeout:
                    handle , new_window_name = self.find_window(windowname)
                    aut_handle=None
                    if handle is not None:
                        aut_handle=handle
                        break
            if new_window_name is None:
                new_window_name = windowname
            if aut_handle is not None:
                self.set_to_foreground(new_window_name)
                status=True
        except Exception as e:
            err_msg=str(e)
            log.debug(e)
        return status,err_msg

    def find_window_and_attach(self,windowname='',*args):
        res,err_msg=self.find_oebswindow_and_attach(windowname=windowname)
        return res

    def getProcessWindows(self,windowName):
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible

        handles = []
        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                if self.patternMatching(windowName,buff.value):
                    handles.append(hwnd)
            return True
        win32gui.EnumWindows(foreach_window, None)
        return handles

    def patternMatching(self,toMatch,matchIn):
        regex=None
        pattern=None
        status=None
        toMatch=toMatch.strip().replace('*','.*')
        matchIn=matchIn.strip()
        if toMatch.endswith('*'):
            regex=toMatch+"([^a-zA-Z0-9-#.()%@!:;\"'?><,$+=()|{}&\\s]|$).*"
        elif toMatch.startswith('.'):
            regex=".*([^a-zA-Z0-9-#.()%@!:;\"'?><,$+=()|{}&\\s]|^)" + toMatch
        elif '*' in toMatch and toMatch.index('*')>0 and toMatch.index('*')<len(toMatch):
            toMatch = toMatch.replaceAll("[^a-zA-Z0-9*.]", ".*")
            regex=toMatch.replace(".*",".*([a-zA-Z0-9-#.()%@!:;\"'?><,$+=()|{}&\\s]|^)")
        else :
            return toMatch==matchIn
        status= re.match(regex,matchIn)

        try:
            if status.group()==matchIn:
                return True
        except Exception as e:
                return False
        return False

    def getWindowText(self,hwnd):
        text=None
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible
        if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                text=buff.value
        return text

    def find_window(self,windowname):
        if windowname is None or windowname is "":
            return None
        title_matched_windows=self.getProcessWindows(windowname)
        if len(title_matched_windows)==1:
            window_handle=title_matched_windows[0]
            windowname=self.getWindowText(window_handle)
            log.debug('Given windowname is '+windowname)
            return window_handle,windowname
        elif len(title_matched_windows)==0:
            log.error('The given window name is not found')
        return None,None

    def main(self,windowName=''):
        try:
            self.window_name = windowName
            self.mainThreadId = _thread.get_ident()
            window_name = windowName
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
            if self.frame is not None:
                self.frame.on_exit(frame=self.frame)
            self.app = None
            self.frame = None

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

