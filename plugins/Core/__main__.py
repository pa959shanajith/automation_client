import sys
import os
import logging
import argparse
import platform
import wx
from loadingwindow import Loading_window
log = logging.getLogger('Avo_Assure')
ice_ver = '3.0.0'

def loading_ui():
    global loadingobj
    app = wx.App()
    loadingobj = Loading_window(None,args)

try:
    cfile = os.path.abspath(__file__)
    with open(os.path.normpath(os.path.dirname(cfile)+("/../.." if os.path.splitext(cfile)[-1]==".py" else "")+"/assets/about_manifest.json")) as m:
        import json
        ice_ver = json.load(m)["version"]
except: pass

parser = argparse.ArgumentParser(description="Avo Assure Client Platform")
parser.add_argument('-n', '--AVO_ASSURE_HOME', required=True, type=str, help='A Required path to Avo Assure root location')
parser.add_argument('-v', '--version', action='version', version=('Avo Assure Client '+ice_ver), help='Show Avo Assure Client version information')
parser.add_argument('--register', action='store_true', help='Register Avo Assure Client with Avo Assure Web Application.')
parser.add_argument('--execute', action='store_true', help='Execute from agent')
reg_group = parser.add_argument_group("Arguments for register/guest-connect")
reg_group.add_argument('--host', type=str, help='Avo Assure Web Application URL. Eg: https://example.com:8443. If no value is provided then value is read from configuration file.')
reg_group.add_argument('--token', type=str, help='Registration token obtained during Avo Assure Client Provisioning. Input can be filepath or text.')
reg_group.add_argument('--configkey', type=str, help='Configuration Key holding configuration information')
reg_group.add_argument('--agentname', nargs='?', type=str, help='Agentname is mandatory')
reg_group.add_argument('--serverurl', nargs='?', type=str, help='serverurl is mandatory')
reg_group.add_argument('--serverport', nargs='?', type=str, help='serverport is mandatory')
reg_group.add_argument('--executionListId', nargs='?', type=str, help='executionListId is mandatory')
reg_group.add_argument('--instanceid', nargs='?', type=str, help="Agent will provide auto increment instanceid")
parser.add_argument('--connect', action='store_true', help='Establish a connection between Avo Assure Web Application and Avo Assure Client.')
args = parser.parse_args()
if args.AVO_ASSURE_HOME and not os.path.exists(args.AVO_ASSURE_HOME+os.sep+'/plugins'):
    parser.error("Invalid path provided for AVO_ASSURE_HOME")
if args.connect and args.register:
    parser.error("Register operation cannot be used with connect operation")
if not (args.register or args.connect) and (args.host or args.token):
    parser.error("Host/Token arguments can only be used with register/connect operation")
if args.register or args.connect:
    if args.token is None:
        if args.register: parser.error("Token cannot be empty for register operation")
        elif args.host is not None:
            parser.error("Host cannot be specified without token")
    else:
        if os.path.exists(args.token):
            try:
                with open(args.token) as token_file:
                    args.token = token_file.read().replace('\n','').replace('\r','').strip()
            except: parser.error("Invalid Token provided for register operation")
        if args.host is None:
            print("No value provided for host. Reading values from configuration file")
if args.execute:
    if args.configkey is None or args.serverurl is None or args.serverport is None or args.executionListId is None:
        log.error("For execution configuration key, executionListId, serverurl and serverport are mandatory")
        parser.error("For execution configuration key, executionListId, serverurl and serverport are mandatory")

os.environ["AVO_ASSURE_HOME"] = os.path.normpath(args.AVO_ASSURE_HOME)
os.environ['AVO_ASSURE_VERSION'] = ice_ver
os.environ["ICE_CLEAR_STORAGE"] = os.getenv("ICE_CLEAR_STORAGE", "False")

import constants
import readconfig
configvalues = readconfig.readConfig().readJson()
proxies = readconfig.readProxyConfig().readJson()

"""
This code snippet blocks the inheritance of file handlers from
parent process to child process. We are applying the same for only on file
which is our log file.
"""
if sys.platform == 'win32':
    from ctypes import windll
    host_os = platform.platform()
    if 'Windows-10' in host_os or 'Windows-8.1' in host_os:
        windll.shcore.SetProcessDpiAwareness(2)
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
        appName = "Avo Assure Client"
        path = os.environ["AVO_ASSURE_HOME"]+os.sep
        if not os.path.exists(path+"logs"): os.mkdir(path+"logs")
        if not os.path.exists(path+"output"): os.mkdir(path+"output")
        loading_ui()
        import core
        import cicd_core
        core.configvalues = configvalues
        core.proxies = proxies
        cicd_core.configvalues = configvalues
        cicd_core.proxies = proxies
        if args.execute:
            cicd_core.CiCdCore(appName, args)
        else:
            core.Main(appName, args, loadingobj)
    except Exception as e:
        log.error(e, exc_info=True)
