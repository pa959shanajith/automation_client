#-------------------------------------------------------------------------------
# Name:        module2
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
from ast import literal_eval
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

def removingUnicodeSign(val):
        """Method that removes unicode signs form an input unicode string"""
        val = repr(val).replace("u'","'")
        val = literal_eval(val)
        if not isinstance(val,basestring):
            val=str(val)
        return val

def getAllInstalledApps(machine_name=None):
        """Input(optional): machine name(required);user name(optional);encripted(AES) password(optional)"""
        """Output: returns the systems's apps_data as a list"""
        apps_data=[]
        err_msg=None
        status = "Fail"
        result = "False"
        machine_name=machine_name.split(';')
        try:
            if machine_name is not None or platform.system().lower()=="windows":
                wmi_ref,error=getWmi(machine_name)
                if wmi_ref is not None:
                    for p in wmi_ref.Win32_Product():
                        #apps_data.append({'caption':p.Caption,'version':p.Version,'name':p.Name,'vendor':p.Vendor})
                        value = removingUnicodeSign(p.Name)
                        value+="--"
                        value+= removingUnicodeSign(p.Version)
                        apps_data.append(value)
                    status="Pass"
                    result="True"
                else:
                    err_msg=error
                    pass
            elif platform.system().lower()=="darwin":
                #find / -iname *.app
                pass
            else:
                #dpkg --get-selections
                pass
        except Exception as e:
            if err_msg ==None:
                err_msg = 'ERR_GET_INSTALLED_APP'
            status = "Fail"
            result = "False"
        return result

var_name=[]
with open("System_getAllInstalledApps_input.txt") as f:
    for line in f:
        if(line.strip()!=''):
            eq_index1 = line.find('#')
            var_name.append((line[:eq_index1].strip(),line[eq_index1+1:].strip()))

import pytest
@pytest.mark.parametrize("input1,expected", var_name)
def test_myfunc(input1, expected):
    assert getAllInstalledApps(input1) == expected

def main():
    pass

if __name__ == '__main__':
    main()
