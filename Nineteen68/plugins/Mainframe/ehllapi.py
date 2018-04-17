#-------------------------------------------------------------------------------
# Name:        ehllapi.py
# Purpose:     API to perform automation on Emulator using HLLAPI
#
# Author:      ranjan.agrawal
#
# Created:     15-02-2018
# Copyright:   (c) ranjan.agrawal 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import json
import time
import socket
import subprocess
from ctypes import *
Ehllapi32 = windll.ehlapi32
hllapi = Ehllapi32.hllapi
emulator = None
con = None

class EHLLAPI():

    def __init__(self):
        pass

    def hll_api(self,fnum,data,length,pos):
        status = -1
        try:
            status = hllapi(fnum,data,length,pos)
        except Exception as e:
            print e
        return status

    def launch(self,file_path):
        global emulator
        status = {"stat": -1}
        try:
            emulator = subprocess.Popen(file_path, shell=True)
            status['stat'] = 0
        except Exception as e:
            print e
            status["emsg"] = "Error while launching " + subprocess.os.path.basename(file_path)
            import traceback
            traceback.print_exc()
        return status

    def kill(self):
        status = {"stat": 0}
        if emulator is not None:
            try:
                status["stat"] = subprocess.call("TASKKILL /F /T /PID " + str(emulator.pid))
            except:
                status["emsg"] = "Error while closing " + subprocess.os.path.basename(file_path)
        return status
        #subprocess.sys.exit()

    def querySessions(self):
        status = {"stat": -1}
        function_number = c_int(10)
        data_string = c_char_p(" "*16)
        length = c_int(16)
        ps_position = c_int(0)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 2:
            status["emsg"] = "Invalid Input provided."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        status["res"] = data_string.value
        return status

    def connectPresentationSpace(self,presentation_space):
        status = {"stat": -1}
        function_number = c_int(1)
        data_string = c_char_p(str(presentation_space))
        length = c_int(4)
        ps_position = c_int(0)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Invalid ShortSessionID provided."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        elif status["stat"] == 11:
            status["emsg"] = "This resource is unavailable. The host presentation space is already being used by another system function."
        return status

    def disconnectPresentationSpace(self):
        status = {"stat": -1}
        function_number = c_int(2)
        data_string = c_char_p()
        length = c_int(4)
        ps_position = c_int(0)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Tool is not connected to a host session."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        return status

    def getPresentationSpaceSize(self,presentation_space):
        status = {"stat": -1}
        opts=[[24,80], [32,80], [43,80], [27,132]]
        function_number = c_int(99)
        data_string = c_char_p(str(presentation_space)+"   P")
        length = c_int(0)
        ps_position = c_int(1921)
        ret = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if ret == 9998:
            status["emsg"] = "Invalid host session provided."
        elif ret == 9999:
            status["emsg"] = "Invalid Input provided."
        else:
            status["stat"] = 0
            row = length.value
            if ret == 0 and row == 0:
                status["res"] = opts[0]
            elif ret == 73 and row == 15:
                status["res"] = opts[3]
            else:
                length = c_int(0)
                ps_position = c_int(2561)
                ret = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
                row = length.value
                if ret == 0 and row == 0:
                    status["res"] = opts[1]
                else:
                    status["res"] = opts[2]
        return status

    def wait(self):
        status = {"stat": -1}
        function_number = c_int(4)
        data_string = c_char_p()
        length = c_int()
        ps_position = c_int()
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Tool is not connected to a host session."
        elif status["stat"] == 4:
            status["emsg"] = "Timeout while waitng for response from host."
        elif status["stat"] == 5:
            status["emsg"] = "Sending keystrokes are still disabled."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        return status

    def sendValue(self,key):
        status = {"stat": -1}
        function_number = c_int(3)
        data_string = c_char_p(key)
        length = c_int(len(key))
        ps_position = c_int(0)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Tool is not connected to a host session."
        elif status["stat"] == 2:
            status["emsg"] = "Invalid Input provided."
        elif status["stat"] == 4 or status["stat"] == 5:
            status["emsg"] = "The host session was busy. sendValue failed."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        return status

    def copyPresentationSpace(self):
        status = {"stat": -1}
        function_number = c_int(5)
        data_string = c_char_p(" "*1920)
        length = c_int(0)
        ps_position = c_int(0)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Tool is not connected to a host session."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        status["res"] = data_string.value.decode('latin-1')
        return status

    def searchPresentationSpace(self,searchStr):
        status = {"stat": -1}
        function_number = c_int(6)
        data_string = c_char_p(searchStr)
        length = c_int(len(searchStr))
        ps_position = c_int(0)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Tool is not connected to a host session."
        elif status["stat"] == 2 or status["stat"] == 7:
            status["emsg"] = "Invalid Input provided."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        return status

    def setCursor(self,position):
        status = {"stat": -1}
        function_number = c_int(40)
        data_string = c_char_p()
        length = c_int()
        ps_position = c_int(position)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Tool is not connected to a host session."
        elif status["stat"] == 4:
            status["emsg"] = "Host session is busy."
        elif status["stat"] == 7:
            status["emsg"] = "Invalid position provided."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        return status

    def getCursor(self):
        status = {"stat": -1}
        function_number = c_int(7)
        data_string = c_char_p()
        length = c_int(0)
        ps_position = c_int(0)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Tool is not connected to a host session."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        status["res"] = length.value
        return status

    def setText(self,text,position):
        status = {"stat": -1}
        text = text.encode('ascii', 'ignore')
        function_number = c_int(15)
        data_string = c_char_p(text)
        length = c_int(len(text))
        ps_position = c_int(position)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Tool is not connected to a host session."
        elif status["stat"] == 2 or status["stat"] == 5:
            status["emsg"] = "Invalid Input provided."
        elif status["stat"] == 6:
            status["emsg"] = "Entire text is not set. Some part is truncated."
        elif status["stat"] == 7:
            status["emsg"] = "Invalid position provided."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        return status

    def getText(self,size,position):
        status = {"stat": -1}
        function_number = c_int(8)
        data_string = c_char_p(" "*size)
        length = c_int(size)
        ps_position = c_int(position)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Tool is not connected to a host session."
        elif status["stat"] == 2:
            status["emsg"] = "Invalid Input provided."
        elif status["stat"] == 9 or status["stat"] == 7:
            status["emsg"] = "A system error was encountered."
        status["res"] = data_string.value.decode('latin-1')
        return status

    ##def findFieldPosition(self,string, position):
    ##    status = {"stat": -1}
    ##    function_number = c_int(31)
    ##    data_string = c_char_p(string)
    ##    length = c_int(len(string))
    ##    ps_position = c_int(position)
    ##    status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
    ##    return {'returnCode':ps_position.value, 'length':length.value}


def test_conn():
    return {"stat": 0}

from Crypto import Random
from Crypto.Cipher import AES
BS = 16
def pad(data):
    padding = BS - len(data) % BS
    return data + padding * chr(padding)

def unpad(data):
    return data[0:-ord(data[-1])]

def encode(data, iv='0'*16):
    key = "".join(['h','f','g','w','e','u','y','R','^','%','$','&','B','8','7',
        'n','x','z','t','7','0','8','r','n','t','.','&','%','^','(','*','@'])
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.encrypt(pad(data)).encode('hex')
def decode(hex_data, iv='0'*16):
    key = "".join(['h','f','g','w','e','u','y','R','^','%','$','&','B','8','7',
        'n','x','z','t','7','0','8','r','n','t','.','&','%','^','(','*','@'])
    data = ''.join(map(chr, bytearray.fromhex(hex_data)))
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(data))


if __name__ == '__main__':
    host = 'localhost'
    port = 10001
    EHLLAPI_DATA_EOF = "$r^mB@$"
    print 'EHLLAPI started...'
    ehllapi_obj=EHLLAPI()
    fail_status = {"stat": -1, "emsg": "Something went wrong."}

    keyword_dict={
        'launchmainframe': ehllapi_obj.launch,
        'getspacesize': ehllapi_obj.getPresentationSpaceSize,
        'connectsession': ehllapi_obj.connectPresentationSpace,
        'sendvalue': ehllapi_obj.sendValue,
        'gettext': ehllapi_obj.getText,
        'settext': ehllapi_obj.setText,
        'wait': ehllapi_obj.wait,
        'setcursor': ehllapi_obj.setCursor,
        'verifytextexists': ehllapi_obj.searchPresentationSpace,
        'disconnectsession': ehllapi_obj.disconnectPresentationSpace,
        'closemainframe': ehllapi_obj.kill,
        'test': test_conn
    }

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(10)
        con,addr = s.accept()
        client_data =''
        while(True):
            try:
                data_stream = con.recv(1024)
                client_data += data_stream
                if(EHLLAPI_DATA_EOF in data_stream):
                    parsed_data = client_data[:client_data.find(EHLLAPI_DATA_EOF)]
                    client_data = ''
                    data_to_use = json.loads(decode(parsed_data.decode('utf-8')))
                    result = keyword_dict[data_to_use["action"]](*tuple(data_to_use["inputs"]))
                    data_to_send = encode(json.dumps(result))+EHLLAPI_DATA_EOF
                    con.send(data_to_send)
            except Exception as e:
                print e
                print 'Error in API while reading instructions'
                con.send(json.dumps(fail_status)+EHLLAPI_DATA_EOF)
                #break
    except Exception as e:
        print 'Error in API'

