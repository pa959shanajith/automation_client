#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      arpit.koolwal
#
# Created:     09-04-2018
# Copyright:   (c) arpit.koolwal 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import platform
import wmi
import system_constants
import os
import logger
import logging
import pythoncom
log = logging.getLogger('system_keywords.py')

class N68System_Keywords():

    def __init__(self):
        pass

    def getWmi(self,machine_name):
        wmi_ref=None
        try:
            pythoncom.CoInitialize()
            if machine_name is not None:
                wmi_ref = wmi.WMI(machine_name)
            else:
                wmi_ref = wmi.WMI()
        except Exception as e:
            logger.print_on_console('Error : Unable to connect with machine')
        return wmi_ref

    def getOsInfo(self,machine_name=None):

        os_info={}
        err_msg=None
        status = system_constants.TEST_RESULT_FAIL
        result = system_constants.TEST_RESULT_FALSE
        try:
            if machine_name is not None or platform.system().lower()=="windows":
                wmi_ref=self.getWmi(machine_name)
                if wmi_ref is not None:
                    os_details = wmi_ref.Win32_OperatingSystem()
                    for iterator in os_details:
                        os_info['system']='windows'
                        os_info['machine']=iterator.Caption
                        os_info['version']=iterator.Version
                    status=system_constants.TEST_RESULT_PASS
                    result = system_constants.TEST_RESULT_TRUE
                else:
                    pass
            else:
                os_info['system'] = platform.system()
                os_info['machine'] = platform.machine()
                os_info['version'] = platform.version()
                os_info['platform_info'] = platform.platform()
                status=system_constants.TEST_RESULT_PASS
                result = system_constants.TEST_RESULT_TRUE
        except Exception as e:
            logger.print_on_console('Error Occured in getOsInfo Keyword')
            err_msg ='Error Occured in getOsInfo Keyword'
        return status,result,os_info,err_msg

    def getAllInstalledApps(self,machine_name=None):

        apps_data=[]
        err_msg=None
        status = system_constants.TEST_RESULT_FAIL
        result = system_constants.TEST_RESULT_FALSE
        try:
            if machine_name is not None or platform.system().lower()=="windows":
                wmi_ref=self.getWmi(machine_name)
                if wmi_ref is not None:
                    for p in wmi_ref.Win32_Product():
                        #apps_data.append({'caption':p.Caption,'version':p.Version,'name':p.Name,'vendor':p.Vendor})
                        apps_data.append(p.Name)
                    status=system_constants.TEST_RESULT_PASS
                    result=system_constants.TEST_RESULT_TRUE
                    pass
                else:
                    pass
            elif platform.system().lower()=="darwin":
                #find / -iname *.app
                pass
            else:
                #dpkg --get-selections
                pass
        except Exception as e:
            logger.print_on_console('Error Occured in GetAllInstalledApps Keyword')
            err_msg = "Error Occured in GetAllInstalledApps Keyword"
        return status,result,apps_data,err_msg

    def getInstalledAppInfo(self,app_name,machine_name=None):
        pass

    def getAllProcess(self,machine_name=None):

        process_data=[]
        err_msg=None
        status = system_constants.TEST_RESULT_FAIL
        result = system_constants.TEST_RESULT_FALSE
        try:
            if machine_name is not None or platform.system().lower()=="windows":
                wmi_ref=self.getWmi(machine_name)
                if wmi_ref is not None:
                    for process in wmi_ref.Win32_Process():
                        #process_data.append({"pid":process.ProcessId,"pname":process.Name})
                        process_data.append(process.Name)
                    status=system_constants.TEST_RESULT_PASS
                    result=system_constants.TEST_RESULT_TRUE
                else:
                    pass
        except Exception as e:
            logger.print_on_console('Error Occured in getAllProcess Keyword')
            err_msg = "Error Occured in getAllProcess Keyword"
        return status,result,process_data,err_msg

    def getProcessInfo(self):
        pass

    def executeCommand(self,command_data=None):

        result_data=''
        err_msg=None
        machine_name=None
        path_outfile=None
        status = system_constants.TEST_RESULT_FAIL
        result = system_constants.TEST_RESULT_FALSE
        try:
            command_toexecute=command_data[0]
            machine_name = command_data[1] if len(command_data)==2 else None
            if machine_name is not None or platform.system().lower()=="windows":
                wmi_ref=self.getWmi(machine_name)
                if wmi_ref is not None:
                    if machine_name is None:
                        path_outfile=os.environ["NINETEEN68_HOME"]+"//Nineteen68//plugins//System//n68sys.txt"
                    else:
                        path_outfile="//"+machine_name+"/c$/n68sys.txt"
                    process_id, process_status = wmi_ref.Win32_Process.Create(CommandLine="cmd /c "+command_toexecute+" > C://n68sys.txt")
                    status=system_constants.TEST_RESULT_PASS
                    result=system_constants.TEST_RESULT_TRUE
                else:
                    pass
            elif platform.system().lower()=="darwin":
                pass
            else:
                pass
            f= open(path_outfile,"r")
            for i in f:
                result_data+=i
        except Exception as e:
            logger.print_on_console('Error Occured in executeCommand Keyword')
            err_msg = "Error Occured in executeCommand Keyword"
        return status,result,result_data,err_msg


if __name__ == '__main__':
    #test_keyword = N68System_Keywords()
    #test_keyword.executeCommand(['ipconfig','wslk13fodc6-054'])
    pass