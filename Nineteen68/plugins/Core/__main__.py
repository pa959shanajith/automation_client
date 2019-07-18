import wx
import sys
import os
import logging
import logging.config
import argparse
import logger
import readconfig
import platform
import constants
log = logging.getLogger('main.py')

parser = argparse.ArgumentParser(description="Nineteen68 Platform")
parser.add_argument('--NINETEEN68_HOME', type=str, help='A Required path to Nineteen68 root location')
args = parser.parse_args()
if args.NINETEEN68_HOME is None:
    parser.error("Required at least 1 argument")
os.environ["NINETEEN68_HOME"] = args.NINETEEN68_HOME

configvalues = readconfig.readConfig().readJson()

"""
This code snippet blocks the inheritance of file handlers from
parent process to child process. We are applying the same for only on file
which is our log file.
"""
if sys.platform == 'win32':
    from ctypes import *
    import msvcrt
    __builtins__open = __builtins__.open
    def __open_inheritance_hack(*args, **kwargs):
        result = __builtins__open(*args, **kwargs)
        handle = msvcrt.get_osfhandle(result.fileno())
        if configvalues["logFile_Path"] in args:
            windll.kernel32.SetHandleInformation(handle, 1, 0)
        return result
    __builtins__.open = __open_inheritance_hack


if __name__ == "__main__":
    app = wx.App()
    appName = "Nineteen68 ICE"
    constants.SYSTEM_OS = platform.system()
    import clientwindow as cw_obj
    cw_obj.configvalues = configvalues
    cw = cw_obj.ClientWindow(appName)
    if cw.is_config_missing:
        err = "Configure "+appName+" by navigating to Edit -> Configuration"
        logger.print_on_console(err)
        log.info(err)
    elif cw.is_config_invalid:
        err = "[Error]: Syntax error in config file.\n"+str(configvalues['errorflag'])+ " config field is missing. Please check and restart "+appName+"."
        logger.print_on_console(err)
        log.info(err)
        log.error(configvalues['errorflag'])
    elif cw.logfilename_error_flag:
        err = "[Error]: Please provide a valid logfile path in config file and restart "+appName+"."
        logger.print_on_console(err)
        log.info(err)
        cw.logfilename_error_flag = False
    app.MainLoop()
