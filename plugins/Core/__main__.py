import sys
import os
import logging
import argparse
import logger
import readconfig
import platform
import constants
log = logging.getLogger('Nineteen68')

parser = argparse.ArgumentParser(description="Nineteen68 ICE Platform")
parser.add_argument('-n', '--NINETEEN68_HOME', required=True, type=str, help='A Required path to Nineteen68 root location')
parser.add_argument('-v', '--version', action='version', version='Nineteen68 ICE 2.0', help='Show Nineteen68 ICE version information')
parser.add_argument('--register', action='store_true', help='Register Nineteen68 ICE with Nineteen68 Web Application.')
reg_group = parser.add_argument_group("register")
reg_group.add_argument('--host', type=str, help='Nineteen68 Web Application URL. Eg: https://example.com:8443. If no value is provided then value is read from configuration file.')
reg_group.add_argument('--token', type=str, help='Registration token obtained during ICE Provisioning.')
parser.add_argument('--connect', action='store_true', help='Establish a connection between Nineteen68 Web Application and ICE.')
args = parser.parse_args()
if args.NINETEEN68_HOME and not os.path.exists(args.NINETEEN68_HOME+os.sep+'/plugins'):
    parser.error("Invalid path provided for NINETEEN68_HOME")
os.environ["NINETEEN68_HOME"] = args.NINETEEN68_HOME
if args.connect and args.register:
    parser.error("Register operation cannot be used with connect option")
if (not args.register) and (args.host or args.token):
    parser.error("Host/Token arguments can only be used with connect option")
if args.register:
    if args.token is None:
        parser.error("Token cannot be empty for register operation")
    if  args.host is None:
        print("No value provided for host. Reading values from configuration file")
configvalues = readconfig.readConfig().readJson()

"""
This code snippet blocks the inheritance of file handlers from
parent process to child process. We are applying the same for only on file
which is our log file.
"""
if sys.platform == 'win32':
    from ctypes import windll
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
    try:
        appName = "Nineteen68 ICE"
        constants.SYSTEM_OS = platform.system()
        path = os.environ["NINETEEN68_HOME"]+os.sep
        if not os.path.exists(path+"logs"): os.mkdir(path+"logs")
        if not os.path.exists(path+"output"): os.mkdir(path+"output")
        import core
        core.configvalues = configvalues
        core.Main(appName, args)
    except Exception as e:
        log.error(e, exc_info=True)
