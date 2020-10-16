#-------------------------------------------------------------------------------
# Name:        mf_api.py
# Purpose:     API to perform automation on Mainframe Emulators
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
import pythoncom
import win32com.client
from ctypes import *
emulator = None
con = None
hllapi = None

class EHLLAPI():

    def __init__(self):
        try:
            global hllapi
            Ehllapi32 = windll.ehlapi32
            hllapi = Ehllapi32.hllapi
            self.error = False
        except Exception as e:
            print(e)
            print("Error while looking up for installation of HLLAPI instance.")
            self.error = True

    def hll_api(self,fnum,data,length,pos):
        status = -1
        try:
            status = hllapi(fnum,data,length,pos)
            print('Status in hll_api : ',status)
        except Exception as e:
            print('Error in hll_api : ',e)
        return status

    def launch(self,file_path):
        print("---------------------launch-----------------------------")
        global emulator
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        try:
            emulator = subprocess.Popen(file_path, shell=True)
            status['stat'] = 0
        except Exception as e:
            print(e)
            status["emsg"] = "Error while launching " + subprocess.os.path.basename(file_path)
            import traceback
            traceback.print_exc()
        print('Status of launch : ',status)
        return status

    def kill(self):
        print("---------------------kill-----------------------------")
        status = {"emsg": "Something Went Wrong"}
        if emulator is not None:
            try:
                status["stat"] = subprocess.call("TASKKILL /F /T /PID " + str(emulator.pid))
            except:
                status["emsg"] = "Error while closing " + subprocess.os.path.basename(file_path)
        print('Status of kill : ',status)
        return status
        #subprocess.sys.exit()

    def querySessions(self):
        print("---------------------querySessions-----------------------------")
        status = {"stat": -1, "emsg": "Something Went Wrong"}
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
        print('Status of querySessions : ',status)
        return status

    def connectPresentationSpace(self,presentation_space):
        print("---------------------connectPresentationSpace-----------------------------")
        status = {"stat": -1, "emsg": "Something Went Wrong"}
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
        print('Status of connectPresentationSpace : ',status)
        return status

    def disconnectPresentationSpace(self):
        print("---------------------disconnectPresentationSpace-----------------------------")
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        function_number = c_int(2)
        data_string = c_char_p()
        length = c_int(4)
        ps_position = c_int(0)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        print('Status of disconnectPresentationSpace : ',status)
        return status

    def getPresentationSpaceSize(self,presentation_space):
        print("---------------------getPresentationSpaceSize-----------------------------")
        status = {"stat": -1, "emsg": "Something Went Wrong"}
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
        print('Status of getPresentationSpaceSize : ',status)
        return status

    def wait(self):
        print("---------------------wait-----------------------------")
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        function_number = c_int(4)
        data_string = c_char_p()
        length = c_int()
        ps_position = c_int()
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 4:
            status["emsg"] = "Timeout while waitng for response from host."
        elif status["stat"] == 5:
            status["emsg"] = "Sending keystrokes are still disabled."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        print('Status of wait : ',status)
        return status

    def sendValue(self,key):
        print("---------------------sendValue-----------------------------")
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        function_number = c_int(3)
        data_string = c_char_p(key)
        length = c_int(len(key))
        ps_position = c_int(0)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 2:
            status["emsg"] = "Invalid Input provided."
        elif status["stat"] == 4 or status["stat"] == 5:
            status["emsg"] = "The host session was busy. sendValue failed."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        print('Status of sendValue : ',status)
        return status

    def copyPresentationSpace(self):
        print("---------------------copyPresentationSpace-----------------------------")
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        function_number = c_int(5)
        data_string = c_char_p(" "*1920)
        length = c_int(0)
        ps_position = c_int(0)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        status["res"] = data_string.value.decode('latin-1')
        print('Status of copyPresentationSpace : ',status)
        return status

    def searchPresentationSpace(self,searchStr):
        print("---------------------searchPresentationSpace-----------------------------")
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        function_number = c_int(6)
        data_string = c_char_p(searchStr)
        length = c_int(len(searchStr))
        ps_position = c_int(0)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 2 or status["stat"] == 7:
            status["emsg"] = "Invalid Input provided."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        print('Status of searchPresentationSpace : ',status)
        return status

    def setCursor(self,position):
        print("---------------------setCursor-----------------------------")
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        function_number = c_int(40)
        data_string = c_char_p()
        length = c_int()
        ps_position = c_int(position)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 4:
            status["emsg"] = "Host session is busy."
        elif status["stat"] == 7:
            status["emsg"] = "Invalid position provided."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        print('Status of setCursor : ',status)
        return status

    def getCursor(self):
        print("---------------------getCursor-----------------------------")
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        function_number = c_int(7)
        data_string = c_char_p()
        length = c_int(0)
        ps_position = c_int(0)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        status["res"] = length.value
        print('Status of getCursor : ',status)
        return status

    def setText(self,text,position):
        print("---------------------setText-----------------------------")
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        text = text.encode('ascii', 'ignore')
        function_number = c_int(15)
        data_string = c_char_p(text)
        length = c_int(len(text))
        ps_position = c_int(position)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 2 or status["stat"] == 5:
            status["emsg"] = "Invalid Input provided."
        elif status["stat"] == 6:
            status["emsg"] = "Entire text is not set. Some part is truncated."
        elif status["stat"] == 7:
            status["emsg"] = "Invalid position provided."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        print('Status of setText : ',status)
        return status

    def getText(self,size,position):
        print("---------------------getText-----------------------------")
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        function_number = c_int(8)
        data_string = c_char_p(" "*size)
        length = c_int(size)
        ps_position = c_int(position)
        status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 2:
            status["emsg"] = "Invalid Input provided."
        elif status["stat"] == 9 or status["stat"] == 7:
            status["emsg"] = "A system error was encountered."
        status["res"] = data_string.value.decode('latin-1')
        print('Status of getText : ',status)
        return status

    def waitForText(self):
        return {"stat": -1, "emsg": "Invalid Request"}

    ##def findFieldPosition(self,string, position):
    ##    status = {"stat": -1, "emsg": "Something Went Wrong"}
    ##    function_number = c_int(31)
    ##    data_string = c_char_p(string)
    ##    length = c_int(len(string))
    ##    ps_position = c_int(position)
    ##    status["stat"] = self.hll_api(byref(function_number),data_string,byref(length),byref(ps_position))
    ##    return {'returnCode':ps_position.value, 'length':length.value}

class BZWhll_API():

    def __init__(self):
        try:
            global emulator
            pythoncom.CoInitialize()
            emulator = win32com.client.Dispatch("BZWhll.WhllObj")
            self.error = False
        except Exception as e:
            print(e)
            print("Error while looking up for BlueZone installation.")
            self.error = True

    def launch(self,file_path):
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        try:
            emulator.OpenSession(0, 1, file_path, 30, 1)
            status["stat"] = emulator.Connect()
            if status["stat"] == 5:
                emulator.ConnectToHost(0, 0)
                status["stat"] = emulator.Connect()
            if status["stat"] == 1:
                status["emsg"] = "Unable to connect to default Emulator session. Use 'connect_session' keyword."
        except Exception as e:
            print(e)
            status["emsg"] = "Error while launching " + subprocess.os.path.basename(file_path)
        return status

    def kill(self):
        status = {"emsg": "Something Went Wrong"}
        status["stat"] = emulator.CloseSession(0, 1)
        #pythoncom.CoUninitialize()
        return status

    def connectPresentationSpace(self,presentation_space):
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        status["stat"] = emulator.Connect(presentation_space)
        if status["stat"] == 5:
            emulator.ConnectToHost(0, 0)
            status["stat"] = emulator.Connect(presentation_space)
        if status["stat"] == 1:
            status["emsg"] = "Invalid ShortSessionID provided."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        elif status["stat"] == 11:
            status["emsg"] = "This resource is unavailable. The host presentation space is already being used by another system function."
        return status

    def disconnectPresentationSpace(self):
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        emulator.DisconnectFromHost(0,0)
        status["stat"] = emulator.Disconnect()
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        elif status["stat"] == 11:
            status["emsg"] = "This resource is unavailable. The host presentation space is already being used by another system function."
        return status

    def getPresentationSpaceSize(self,presentation_space):
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        opts=[[24,80], [32,80], [43,80], [27,132]]
        emulator.PSCursorPos = 1921
        ret = emulator.GetCursor(0, 0)
        if ret == 9998:
            status["emsg"] = "Invalid host session provided."
        elif ret == 9999:
            status["emsg"] = "Invalid Input provided."
        else:
            status["stat"] = 0
            if ret[1] == 0 and ret[2] == 0:
                status["res"] = opts[0]
            elif ret[1] == 73 and ret[2] == 15:
                status["res"] = opts[3]
            else:
                emulator.PSCursorPos = 2561
                ret = emulator.GetCursor(0, 0)
                if ret[1] == 0 and ret[2] == 0:
                    status["res"] = opts[1]
                else:
                    status["res"] = opts[2]
        return status

    def wait(self,time1,time2):
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        #status["stat"] = emulator.WaitForReady()
        status["stat"] = emulator.WaitReady(time1,time2)
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 4:
            status["emsg"] = "Timeout while waitng for response from host."
        elif status["stat"] == 5:
            status["emsg"] = "Sending keystrokes are still disabled."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        return status

    def sendValue(self,keys):
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        emulator.WaitReady(10,1000)
        emulator.Focus
        if type(keys) != type([]): keys = [keys]
        for key in keys:
            emulator.WaitReady(10,1000)
            status["stat"] = emulator.SendKeys(key)
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 2:
            status["emsg"] = "Invalid Input provided."
        elif status["stat"] == 4 or status["stat"] == 5:
            status["emsg"] = "The host session was busy. Send failed."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        return status

    def copyPresentationSpace(self):
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        status["stat"] = emulator.Copy()
        status["res"] = emulator.GetClipboardText().decode('latin-1').replace('\r','')
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        return status

    def searchPresentationSpace(self,searchStr):
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        ret = emulator.Search(searchStr, 1, 1)
        status["stat"] = ret[0]
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 2 or status["stat"] == 7:
            status["emsg"] = "Invalid Input provided."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        elif status["stat"] == 24:
            status["emsg"] = "Text Not Found."
        return status

    def setCursor(self, row, col):
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        status["stat"] = emulator.SetCursor(row, col)
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 4:
            status["emsg"] = "Host session is busy."
        elif status["stat"] == 7:
            status["emsg"] = "Invalid position provided."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        return status

    def getCursor(self):
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        ret = emulator.GetCursor(0, 0)
        status["stat"] = ret[0]
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        status["res"] = [ret[1], ret[2]]
        return status

    def setText(self,text,row,col):
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        status["stat"] = emulator.WriteScreen(text, row, col)
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 2 or status["stat"] == 5:
            status["emsg"] = "Invalid Input provided."
        elif status["stat"] == 6:
            status["emsg"] = "Entire text is not set. Some part is truncated."
        elif status["stat"] == 7:
            status["emsg"] = "Invalid position provided."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        return status

    def getText(self,size,row,col):
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        ret = emulator.ReadScreen('', size, row, col)
        status["stat"] = ret[0]
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 2:
            status["emsg"] = "Invalid Input provided."
        elif status["stat"] == 9 or status["stat"] == 7:
            status["emsg"] = "A system error was encountered."
        status["res"] = ret[1].decode('latin-1')
        return status

    def waitForText(self,text,row,col,timeout):
        status = {"stat": -1, "emsg": "Something Went Wrong"}
        status["stat"] = emulator.WaitForText(text,row,col,timeout)
        if status["stat"] == 1:
            status["emsg"] = "Client is not connected to a host session."
        elif status["stat"] == 4:
            status["emsg"] = "Text Not Found."
        elif status["stat"] == 9:
            status["emsg"] = "A system error was encountered."
        return status


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
    DATA_EOF = "$r^mB@$"
    print('Avo Assure Mainframe API started...')
    fail_status = {"stat": -1, "emsg": "Something went wrong."}
    keyword_dict = None
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
                if(DATA_EOF in data_stream):
                    parsed_data = client_data[:client_data.find(DATA_EOF)]
                    client_data = ''
                    data_to_use = json.loads(decode(parsed_data.decode('utf-8')))
                    if data_to_use["action"] == "test":
                        result = {"stat": 0}
                        emulator_type = data_to_use["inputs"][0]
                        if emulator_type.lower() == "bluezone":
                            api_obj = BZWhll_API()
                        else:
                            api_obj = EHLLAPI()
                        if api_obj.error:
                            result = {"stat": 1, "emsg": "Error while looking up for "+emulator_type+" installation"}
                        keyword_dict = {
                            'launchmainframe': api_obj.launch,
                            'getspacesize': api_obj.getPresentationSpaceSize,
                            'connectsession': api_obj.connectPresentationSpace,
                            'sendvalue': api_obj.sendValue,
                            'gettext': api_obj.getText,
                            'settext': api_obj.setText,
                            'wait': api_obj.wait,
                            'getcursor': api_obj.getCursor,
                            'setcursor': api_obj.setCursor,
                            'getscreen': api_obj.copyPresentationSpace,
                            'verifytextexists': api_obj.searchPresentationSpace,
                            'waitfortext': api_obj.waitForText,
                            'disconnectsession': api_obj.disconnectPresentationSpace,
                            'closemainframe': api_obj.kill
                        }
                    else:
                        result = keyword_dict[data_to_use["action"]](*tuple(data_to_use["inputs"]))
                    data_to_send = encode(json.dumps(result))+DATA_EOF
                    con.send(data_to_send)
            except Exception as e:
                print(e)
                print('Error in API while reading instructions')
                con.send(encode(json.dumps(fail_status))+DATA_EOF)
                #break
    except Exception as e:
        print('Error in API')
