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
import time
import logging
import pythoncom
from ast import literal_eval
log = logging.getLogger('system_keywords.py')

class System_Keywords():

    def __init__(self):
        pass

    def getWmi(self,machine_name):
        wmi_ref=None
        err_msg=None
        try:
            pythoncom.CoInitialize()
            if machine_name is not None:
                if isinstance(machine_name,list):
                    machine_name=machine_name[0]
                wmi_ref = wmi.WMI(machine_name)
            else:
                wmi_ref = wmi.WMI()
        except Exception as e:
            log.error(e)
            err_msg = system_constants.ERROR_CODE_DICT['ERR_UNABLE_TO_CONNECT']
        return wmi_ref

    def removingUnicodeSign(self,val):
        val = repr(val).replace("u'","'")
        val = literal_eval(val)
        if not isinstance(val,basestring):
            val=str(val)
        return val

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
                        os_info['machine']=self.removingUnicodeSign(iterator.Caption)
                        os_info['version']=self.removingUnicodeSign(iterator.Version)
                        os_info['OSArchitecture'] = self.removingUnicodeSign(iterator.OSArchitecture)
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
            log.error(e)
            err_msg =system_constants.ERROR_CODE_DICT['ERR_OS_INFO']
            status = system_constants.TEST_RESULT_FAIL
            result = system_constants.TEST_RESULT_FALSE
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
                        value = self.removingUnicodeSign(p.Name)
                        value+="-"
                        value+= self.removingUnicodeSign(p.Version)
                        apps_data.append(value)
                    status=system_constants.TEST_RESULT_PASS
                    result=system_constants.TEST_RESULT_TRUE
                else:
                    pass
            elif platform.system().lower()=="darwin":
                #find / -iname *.app
                pass
            else:
                #dpkg --get-selections
                pass
        except Exception as e:
            log.error(e)
            err_msg = system_constants.ERROR_CODE_DICT['ERR_GET_INSTALLED_APP']
            status = system_constants.TEST_RESULT_FAIL
            result = system_constants.TEST_RESULT_FALSE
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
                        value = self.removingUnicodeSign(process.Name)
                        value+="-"
                        value+=self.removingUnicodeSign(process.ProcessId)
                        process_data.append(value)
                    status=system_constants.TEST_RESULT_PASS
                    result=system_constants.TEST_RESULT_TRUE
                else:
                    pass
        except Exception as e:
            log.error(e)
            err_msg = system_constants.ERROR_CODE_DICT['ERR_GET_ALL_PROCESS']
            status = system_constants.TEST_RESULT_FAIL
            result = system_constants.TEST_RESULT_FALSE
        return status,result,process_data,err_msg

    def getProcessInfo(self):
        pass

    def executeCommand(self,command_data=None):

        result_data=''
        err_msg=None
        machine_name=None
        path_outfile=None
        path_attrib=None

        status = system_constants.TEST_RESULT_FAIL
        result = system_constants.TEST_RESULT_FALSE
        try:
            command_toexecute=command_data[0]
            machine_name = command_data[1] if len(command_data)>=2 else None
            path_outfile = command_data[2] if len(command_data)>=3 else None
            if machine_name is not None or platform.system().lower()=="windows":
                wmi_ref=self.getWmi(machine_name)
                if wmi_ref is not None:
                    if machine_name is None:
                        path_outfile=os.environ["NINETEEN68_HOME"]+"//Nineteen68//plugins//System//nineteen68_system.txt"
                        process_id, process_status = wmi_ref.Win32_Process.Create(CommandLine="cmd /c "+command_toexecute+" > "+path_outfile)
                    else:
                        file_name=None
                        if(path_outfile is None):
                            raise Exception('Invalid file path.')
                        else:
                            path_attrib=path_outfile.split(':')
                            if(len(path_attrib)==2):
                                if path_attrib[1].endswith('\\'):
                                    file_name ="nineteen68_system.txt"
                                else:
                                    file_name="/nineteen68_system.txt"

                                path_outfile = "//"+machine_name+"/"+path_attrib[0]+"$"+path_attrib[1]+file_name
                            else:
                                raise Exception('Invalid file path.')
                        file_name = command_data[2]+file_name
                        process_id, process_status = wmi_ref.Win32_Process.Create(CommandLine="cmd /c "+command_toexecute+" > "+file_name)
                    time.sleep(2)
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
            if not result_data:
                raise Exception('Command not found or Unable to connect to machine')
        except Exception as e:
            log.error(e)
            err_msg = system_constants.ERROR_CODE_DICT['ERR_EXECUTE_COMMAND']
            status = system_constants.TEST_RESULT_FAIL
            result = system_constants.TEST_RESULT_FALSE
        return status,result,result_data,err_msg

'''
if __name__ == '__main__':
    #test_keyword = N68System_Keywords()
    #test_keyword.executeCommand(['ipconfig','wslk13fodc6-054'])
    pass

'''