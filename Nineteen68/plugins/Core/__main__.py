import wx
import sys
import os
import logging
import logging.config
import argparse
import logger
import readconfig
log = logging.getLogger('main.py')

parser = argparse.ArgumentParser(description="Nineteen68 Platform")
parser.add_argument('--NINETEEN68_HOME', type=str, help='A Required path to Nineteen68 root location')
args = parser.parse_args()

if args.NINETEEN68_HOME < 1:
    parser.error("Required at least 1 argument")
os.environ["NINETEEN68_HOME"] = args.NINETEEN68_HOME

configobj = readconfig.readConfig()
configvalues = configobj.readJson()
jsonSyntaxErrorFlag = False
configMissingFlag = False
if configvalues.has_key('errorflag'):
    jsonSyntaxErrorFlag = True
elif configvalues.has_key('configmissing'):
    configMissingFlag = True

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
    import clientwindow as cw_obj
    cw_obj.configvalues = configvalues
    cw = cw_obj.ClientWindow()
    print('*******************************************************************************************************')
    print('=========================================Nineteen68 Client Window======================================')
    print('*******************************************************************************************************')
    if configMissingFlag:
        logger.print_on_console( "Configure Nineteen68 Client by navigating to Configuration ->Edit ->Edit Config")
        log.info("Configure Nineteen68 Client by navigating to Configuration ->Edit ->Edit Config")
    elif jsonSyntaxErrorFlag:
        logger.print_on_console( "[Error]: Syntax error in config.json file, please check and restart the client window.")
        log.info("[Error]: Syntax error in config.json file, and please check and restart the client window.")
        log.error(configvalues['errorflag'])
    elif cw.logfilename_error_flag:
        logger.print_on_console( "[Error]: Please provide a valid logfile path in config.json file and restart the client window.")
        log.info("[Error]: Please provide a valid logfile path in config.json file and restart the client window.")
        cw.logfilename_error_flag = False
    app.MainLoop()
