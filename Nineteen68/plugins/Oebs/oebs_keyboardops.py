from ctypes import *
from ctypes.wintypes import *
from time import sleep
import win32ui
import oebs_constants
from oebs_msg import *

class KeywordOperations:
    # CONSTANTS
    KEYEVENTF_EXTENDEDKEY = 1
    KEYEVENTF_KEYUP = 2

    # VIRTUAL KEYCODES

    virtualkeycodes={
    'CONTROL' : 0xA2,
    'ENTER' : 0x0D,
    'CAPSLOCK' : 0x14,
    'SHIFT' : 0xA1,
    '*' : 0x6A,
    'A_UP' : 0x26,
    'HOME' : 0x24,
    'A_DOWN' : 0x28,
    'ALT' : 0x12,
    #keycodes for number
    '0' : 0x30,
    '1' : 0x31,
    '2' : 0x32,
    '3' : 0x33,
    '4' : 0x34,
    '5' : 0x35,
    '6' : 0x36,
    '7' : 0x37,
    '8' : 0x38,
    '9' : 0x39,

    'A' : 0x41,
    'B' : 0x42,
    'C' : 0x43,
    'D' : 0x44,
    'E' : 0x45,
    'F' : 0x46,
    'G' : 0x47,
    'H' : 0x48,
    'I' : 0x49,
    'J' : 0x4A,
    'K' : 0x4B,
    'L' : 0x4C,
    'M' : 0x4D,
    'N' : 0x4E,
    'O' : 0x4F,
    'P' : 0x50,
    'Q' : 0x51,
    'R' : 0x52,
    'S' : 0x53,
    'T' : 0x54,
    'U' : 0x55,
    'V' : 0x56,
    'W' : 0x57,
    'X' : 0x58,
    'Y' : 0x59,
    'Z' : 0x5A,
    '6' : 0x5B,
    '7' : 0x5C,
    '8' : 0x5D,
    '9' : 0x5E,
    '9' : 0x45F,

    }


    def sendkeydown(self,key):
        windll.user32.keybd_event(self.virtualkeycodes.get(key),0,0,0)

    def sendkeyup(self,key):
        windll.user32.keybd_event(self.virtualkeycodes.get(key),0,self.KEYEVENTF_KEYUP,0)

    def sendkeypress(self,key):
        windll.user32.keybd_event(self.virtualkeycodes.get(key), 0,0,0)
        windll.user32.keybd_event(self.virtualkeycodes.get(key),0,self.KEYEVENTF_KEYUP,0)

    def keyboard_operation(self,action,key):
        print 'WHAT i sthe keyyyyyyyyyyyy',key
        if(action == 'keydown'):
            self.sendkeydown(key)
            return True
        elif(action == 'keyup'):
            self.sendkeyup(key)
            return True
        elif(action == 'keypress'):
            self.sendkeypress(key)
            return True
        else:
            return MSG_INVALID_ACTION_INFO
