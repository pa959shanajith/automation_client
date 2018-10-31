#-------------------------------------------------------------------------------
# Name:        module4
# Purpose:
#
# Author:      anas.ahmed
#
# Created:     29-10-2018
# Copyright:   (c) anas.ahmed 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import platform
import wmi
import os
import time
import pythoncom
import base64
from Crypto.Cipher import AES
unpad = lambda s : s[0:-ord(s[-1])]

def decrypt(enc):
        key = b'\x74\x68\x69\x73\x49\x73\x41\x53\x65\x63\x72\x65\x74\x4b\x65\x79'
        try:
            if not (enc is None or enc is ''):
                enc = base64.b64decode(enc)
                cipher = AES.new(key, AES.MODE_ECB )
                return unpad(cipher.decrypt( enc))
            else:
                print 'ERR_INVALID_INPUT'
        except Exception as e:
            print e

def getWmi(machine_name):
        """Method that creates a COM object related to the machine name(required);user name(optional);password(optional)"""
        wmi_ref=None
        error=None
        try:
            pythoncom.CoInitialize()
            if machine_name is not None:
                if len(machine_name)==3:
                    wmi_ref = wmi.WMI(computer=machine_name[0], user=machine_name[1], password=decrypt(machine_name[2]))
                else:
                    wmi_ref = wmi.WMI(machine_name[0])
            else:
                wmi_ref = wmi.WMI()
        except Exception as error:
            print error
        return wmi_ref,error

def executeCommand(command_data=None):
        """Input(optional): command(required);machine name(required);user name(optional);encripted(AES) password(optional);path of output file"""
        """Output: executes command in local machine ,where the user has set the path"""
        result_data=''
        err_msg=None
        machine_name=None
        path_outfile=None
        path_attrib=None
        command_data=command_data.split (';')

        status = "Fail"
        result = "False"
        try:
            command_toexecute=command_data[0]
            if len(command_data)!=5:
                machine_name=[]
                machine_name.append(command_data[1] if len(command_data)>=2 else None)
                path_outfile = command_data[2] if len(command_data)>=3 else None
            elif len(command_data)==5:
                machine_name = command_data[1:4]
                path_outfile= command_data[4]
            if machine_name is not None or platform.system().lower()=="windows":
                wmi_ref,error=getWmi(machine_name)
                if wmi_ref is not None:
                    if machine_name is None:
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
                        file_name = command_data[4]+file_name
                        process_id, process_status = wmi_ref.Win32_Process.Create(CommandLine="cmd /c "+command_toexecute+" > "+file_name)
                    time.sleep(2)
                    status="Pass"
                    result="True"
                else:
                    err_msg=error
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
            print e
            status = "Fail"
            result = "False"
        return result


var_name=[]
with open("System_executeCommand_input.txt") as f:
    for line in f:
        if(line.strip()!=''):
            eq_index1 = line.find('#')
            var_name.append((line[:eq_index1].strip(),line[eq_index1+1:].strip()))

import pytest
@pytest.mark.parametrize("input1,expected", var_name)
def test_myfunc(input1, expected):
    assert executeCommand(input1) == expected