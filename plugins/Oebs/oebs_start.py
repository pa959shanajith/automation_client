import traceback
import time
import win32gui
import threading
import sys
import logging
log=logging.getLogger('oebs_start.py')
import oebs_api

status = False
thread = None

# thread event
exit_event = None
running_event = None

import oebs_core1
core = oebs_core1.Core()

def call_core(windowName):
    #if 'core' in sys.modules:
    global core
    try:
        core.main(windowName)
    except Exception as e:
        log.debug(e)

def start_thread(windowName=''):
    global thread
    try:
        thread = threading.Thread(target=call_core,args=(windowName,))
        thread.setDaemon(True)
        thread.start()

    except Exception as e:
        log.debug(e)

def main(windowName=''):
    global exit_event
    global running_event
    global core
    global window_name
    try:
        #core = oebs_core1.Core()
        #exit_event = threading.Event()
        #running_event = threading.Event()
        window_name = windowName
        start_thread(windowName)
        #core.main(windowName)
        #running_event.wait()
        #running_event = None
        if core.dll_loaded:
            if core.res_find_window:
                return 'Pass',""
            else:
                try:
                    core.terminate()
                except Exception as e:
                    log.debug(e)
                return 'Fail','Unable to find the application'
        else:
            try:
                core.terminate()
            except Exception as e:
                log.debug(e)
            return 'Fail','Unable to load the dll'

    except Exception as e:
        log.debug(e)

def terminate():
    global exit_event
    import threading
    global core
    #added local 
    thread=None
    try:
        core.terminate()
    except Exception as e:
        log.debug(e)
    # wait for the exit event
    if exit_event:
        exit_event.wait()
    #To Check the loaded bridgeDll should run after the scrape completed with debug TestCase, Commited the terminate evevent
    oebs_api.terminateEvents()
    data_rec = oebs_api.path_obj.create_file(core.get_window_name())

    if thread:
        thread = None
    exit_event = None
    return data_rec
    
