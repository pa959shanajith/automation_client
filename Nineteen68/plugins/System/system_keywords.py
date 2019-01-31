#-------------------------------------------------------------------------------
# Name:         system_keywords
# Purpose:      This module is used to perform system related operations
#
# Author:      arpit.koolwal,anas.ahmed
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
from constants import OUTPUT_CONSTANT
from ast import literal_eval
from constants import SYSTEM_OS
log = logging.getLogger('system_keywords.py')
from encryption_utility import AESCipher


class System_Keywords():

    def __init__(self):
        self.encryption_obj = AESCipher()
        self.access_denied_flag=False
        pass

    def getWmi(self,machine_name):
        """Method that creates a COM object related to the machine name(required);user name(optional);password(optional)"""
        wmi_ref=None
        try:
            pythoncom.CoInitialize()
            if machine_name is not None:
                if len(machine_name)==3:
                    wmi_ref = wmi.WMI(computer=machine_name[0], user=machine_name[1], password=self.encryption_obj.decrypt(machine_name[2]))
                else:
                    try:
                        wmi_ref = wmi.WMI(machine_name[0])
                    except Exception as e:
                        log.error(e)
                        self.access_denied_flag=True
            else:
                wmi_ref = wmi.WMI()
        except Exception as error:
            log.error(error)
        return wmi_ref

    def removingUnicodeSign(self,val):
        """Method that removes unicode signs form an input unicode string"""
        val = repr(val).replace("u'","'")
        val = literal_eval(val)
        if not isinstance(val,str):
            val=str(val)
        return val

    def getOsInfo(self,machine_name=None):
        """Input(optional): machine name(required);user name(optional);encripted(AES) password(optional)"""
        """Output: returns the systems's OS name;machine name;OS version;OS Architecture in a dictionary format"""
        os_info={}
        err_msg=None
        self.access_denied_flag=False
        status = system_constants.TEST_RESULT_FAIL
        result = system_constants.TEST_RESULT_FALSE
        try:
            if machine_name is not None or SYSTEM_OS.lower()=="windows":
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
                os_info['system'] = SYSTEM_OS
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
            os_info=OUTPUT_CONSTANT
        if self.access_denied_flag==True:
            err_msg = system_constants.ACCESS_DENIED
            logger.print_on_console(system_constants.ACCESS_DENIED)
            os_info=OUTPUT_CONSTANT
        return status,result,os_info,err_msg

    def getAllInstalledApps(self,machine_name=None):
        """Input(optional): machine name(required);user name(optional);encripted(AES) password(optional)"""
        """Output: returns the systems's apps_data as a list"""
        apps_data=[]
        err_msg=None
        self.access_denied_flag=False
        status = system_constants.TEST_RESULT_FAIL
        result = system_constants.TEST_RESULT_FALSE
        try:
            if machine_name is not None or SYSTEM_OS.lower()=="windows":
                wmi_ref=self.getWmi(machine_name)
                if wmi_ref is not None:
                    for p in wmi_ref.Win32_Product():
                        #apps_data.append({'caption':p.Caption,'version':p.Version,'name':p.Name,'vendor':p.Vendor})
                        value = self.removingUnicodeSign(p.Name)
                        value+="--"
                        value+= self.removingUnicodeSign(p.Version)
                        apps_data.append(value)
                    status=system_constants.TEST_RESULT_PASS
                    result=system_constants.TEST_RESULT_TRUE
                else:
                    pass
            elif SYSTEM_OS.lower()=="darwin":
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
            apps_data=OUTPUT_CONSTANT
        if self.access_denied_flag==True:
            err_msg = system_constants.ACCESS_DENIED
            logger.print_on_console(system_constants.ACCESS_DENIED)
            apps_data=OUTPUT_CONSTANT
        return status,result,apps_data,err_msg

    def getInstalledAppInfo(self,app_name,machine_name=None):
        pass

    def getAllProcess(self,machine_name=None):
        """Input(optional): machine name(required);user name(optional);encripted(AES) password(optional)"""
        """Output: returns the systems's process_data as a list"""
        process_data=[]
        err_msg=None
        self.access_denied_flag=False
        status = system_constants.TEST_RESULT_FAIL
        result = system_constants.TEST_RESULT_FALSE
        try:
            if machine_name is not None or SYSTEM_OS.lower()=="windows":
                wmi_ref=self.getWmi(machine_name)
                if wmi_ref is not None:
                    for process in wmi_ref.Win32_Process():
                        #process_data.append({"pid":process.ProcessId,"pname":process.Name})
                        value = self.removingUnicodeSign(process.Name)
                        value+="--"
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
            process_data=OUTPUT_CONSTANT
        if self.access_denied_flag==True:
            err_msg = system_constants.ACCESS_DENIED
            logger.print_on_console(system_constants.ACCESS_DENIED)
            process_data=OUTPUT_CONSTANT
        return status,result,process_data,err_msg

    def getProcessInfo(self):
        pass

    def executeCommand(self,command_data=None):
        """Input(optional): command(required);machine name(required);user name(optional);encripted(AES) password(optional);path of output file"""
        """Output: executes command in local machine ,where the user has set the path"""
        result_data=''
        err_msg=None
        self.access_denied_flag=False
        machine_name=None
        path_outfile=None
        path_attrib=None

        status = system_constants.TEST_RESULT_FAIL
        result = system_constants.TEST_RESULT_FALSE
        try:
            command_toexecute=command_data[0]
            if len(command_data)!=5:
                machine_name=[]
                machine_name.append(command_data[1] if len(command_data)>=2 else None)
                path_outfile = command_data[2] if len(command_data)>=3 else None
            elif len(command_data)==5:
                machine_name = command_data[1:4]
                path_outfile= command_data[4]
            if machine_name[0] is not None or SYSTEM_OS.lower()=="windows":
                wmi_ref=self.getWmi(machine_name)
                if wmi_ref is not None:
                    if machine_name[0] is None:
                        path_outfile=os.environ["NINETEEN68_HOME"]+"/Nineteen68/plugins/System/nineteen68_system.txt"
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

                                path_outfile = "//"+machine_name[0]+"/"+path_attrib[0]+"$"+path_attrib[1]+file_name
                            else:
                                raise Exception('Invalid file path.')
                        if len(command_data)!=5:
                            file_name = command_data[2]+file_name
                        elif len(command_data)==5:
                            file_name = command_data[4]+file_name
                        process_id, process_status = wmi_ref.Win32_Process.Create(CommandLine="cmd /c "+command_toexecute+" > "+file_name)
                    time.sleep(2)
                    status=system_constants.TEST_RESULT_PASS
                    result=system_constants.TEST_RESULT_TRUE
                    log.debug("Executed command in remote/local machine and stored result in nineteen68_system.txt")
                else:
                    pass
            elif SYSTEM_OS.lower()=="darwin":
                pass
            else:
                pass
            if process_status == 0:
                try:
                    f= open(path_outfile,"r")
                    for i in f:
                        result_data+=i
                    if not result_data:
                        raise Exception('Command not found or Unable to connect to machine')
                except Exception as e:
                    log.error(e)
                    log.error(system_constants.ACCESS_DENIED)
                    log.debug(system_constants.ACCESS_DENIED)
                    logger.print_on_console(system_constants.ACCESS_DENIED)
                    err_msg = system_constants.ACCESS_DENIED
                    status = system_constants.TEST_RESULT_FAIL
                    result = system_constants.TEST_RESULT_FALSE
                    result_data=OUTPUT_CONSTANT
            else:
                raise RuntimeError("Issue while creating process: %d" % process_status)
        except Exception as e:
            log.error(e)
            err_msg = system_constants.ERROR_CODE_DICT['ERR_EXECUTE_COMMAND']
            status = system_constants.TEST_RESULT_FAIL
            result = system_constants.TEST_RESULT_FALSE
            result_data=OUTPUT_CONSTANT
        if self.access_denied_flag==True:
            err_msg = system_constants.ACCESS_DENIED
            logger.print_on_console(system_constants.ACCESS_DENIED)
            result_data=OUTPUT_CONSTANT
        return status,result,result_data,err_msg
