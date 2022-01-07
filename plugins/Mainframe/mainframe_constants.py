#-------------------------------------------------------------------------------
# Name:        mainframe_constants.py
# Purpose:     File to all the constants related to Mainframe Plugin
#
# Author:      wasimakram.sutar
# Created:     08-09-2016
# Updated      25-10-2017
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

MAINFRAME_EXTRA = 'Extra!'
MAINFRAME_EXTRA_EXE = 'EXTRA.exe'
MAINFRAME_PCOMM = 'Pcomm'
MAINFRAME_PCOMM_EXE = 'pcsws.exe'
MAINFRAME_BLUEZONE = 'Bluezone'
MAINFRAME_BZMD_EXE = 'bzmd.exe'
MAINFRAME_RUMBA = 'Rumba'
MAINFRAME_RUMBA_EXE = 'RumbaPage.exe'
MAINFRAME_HOD = 'Hod'

LAUNCH_MAINFRAME_SUCCESS_MESSAGE = 'Mainframe Launched successfully\n'
MAINFRAME_READY = 'READY'
MAINFRAME_LOGOFF = 'LOGOFF'
MAINFRAME_LOGOFF_MESSAGE = 'Logged off successfully\n'
MAINFRAME_LOGIN_FAIL = 'Incorrect Password entered'
MAINFRAME_WRONG_USERID = 'Please check userid'
MAINFRAME_NOT_AUTHORISED = 'NOT AUTHORIZED'
MAINFRAME_COMMAND_UNRECOGNIZED = 'COMMAND UNRECOGNIZED'
VB_HOST = 'ScriptControl'
VB_LANGUAGE = 'vbscript'
VB_HOST_EVAL = 'getString()'

MAINFRAME_KEY_ENTER = '<Enter>'
MAINFRAME_KEY_F3 = '@3'
MAINFRAME_KEY_F = '@F'
MAINFRAME_KEY_f = 'f '
MAINFRAME_KEY_T = '@T'
MAINFRAME_KEY_3_4 = '3.4'
MAINFRAME_KEY_V = 'V'
MAINFRAME_KEY_SUB = 'SUB'
MAINFRAME_KEY_M_5 = 'm.5'
MAINFRAME_KEY_ST = 'ST'
MAINFRAME_KEY_IKJ = 'IKJ'
MAINFRAME_KEY_R = '@R'
MAINFRAME_KEY_0 = '@0'

MAINFRAME_KEY_FILTER_JOBID = 'FILTER JOBID '
MAINFRAME_JOB_COMPLETED = 'Job completed\n'
MAINFRAME_JOB_NOT_COMPLETED = 'Job not completed\n'
MAINFRAME_PRESS_FUNCTION_KEY = 'Pressed function key\n'
MAINFRAME_CURSOR_SET = 'Cursor Set\n'
MAINFRAME_TEXT_VERIFIED = 'Text verified\n'
MAINFRAME_TEXT_MISMATCHED = 'Text mismatched\n'
MAINFRAME_SENDVALUE = 'Value sent successfully\n'
MAINFRAME_FILE_NOT_FOUND = 'File not found'
MAINFRAME_JOB_NOT_FOUND = 'Job not found'
MAINFRAME_SET_TEXT = 'Text set\n'
MAINFRAME_FAIL_RESPONSE = 'FAIL'
MAINFRAME_TEXT_FAIL_TO_SET = 'Text could not be set at this position\n'
MAINFRAME_SESSION_CONNECTED = 'Session connected\n'
MAINFRAME_SESSION_DISCONNECTED = 'Session disconnected\n'
MAINFRAME_APP_CLOSED = 'Emulator closed\n'
MAINFRAME_RESOLUTION_FAIL = 'Failed to Obtain screen resolution. Switching to default resolution 24x80\n'
MAINFRAME_CLIENT_NOT_CON = "Client is not connected to a host session"

TEST_RESULT_PASS = 'Pass'
TEST_RESULT_FAIL = 'Fail'
TEST_RESULT_FALSE = 'False'
TEST_RESULT_TRUE = 'True'
OUTPUT_CONSTANT = """9cc33d6fe25973868b30f4439f09901a"""
INVALID_KEYWORD = 'Invalid keyword'

MAINFRAME_FN_KEYS = { "enter": "<Enter>", "tab": "<Tab>", "home": "<Home>",
    "insert": "<Insert>", "alt": "<Alt>", "backspace": "<Backspace>",
    "delete":"<Delete>", "end": "<End>", "pageup": "<PageUp>", "pagedown": "<PageDown>",
    "ctrl": "<Ctrl>", "capslock": "<CapsLock>", "shift": "<Shift>",
    "esc": "<Esc>", "pf1": "<F1>", "pf2": "<F2>", "pf3": "<F3>", "pf4": "<F4>",
    "pf5": "<F5>", "pf6": "<F6>", "pf7": "<F7>", "pf8": "<F8>", "pf9": "<F9>",
    "pf10": "<F10>", "pf11": "<F11>", "pf12": "<F12>", "pf13": "<F13>",
    "pf14": "<F14>", "pf15": "<F15>", "pf16": "<F16>", "pf17": "<F17>",
    "pf18": "<F18>", "pf19": "<F19>", "pf20": "<F20>", "pf21": "<F21>",
    "pf22": "<F22>", "pf23": "<F23>", "pf24": "<F24>", "attention": "@A@Q",
    "cursor select": "@A@J", "dup": "@S@x", "erase input": "@A@F", "field mark": "@S@y",
    "insert mode": "@A@I", "sys request": "@A@H", "test request": "@A@C"
}

MF_API_DATA_EOF = b"$r^mB@$"
EHLLAPI_MNEMONICS = {
    "left tab": "@B", "clear": "@C", "delete": "@D", "enter": "@E", "erase eof": "@F",
    "help": "@H", "insert": "@I", "jump": "@J", "left": "@L", "new line": "@N",
    "space": "@O", "print": "@P", "reset": "@R", "tab": "@T", "up": "@U", "down": "@V",
    "right": "@Z", "home": "@0", "pf1": "@1", "pf2": "@2", "pf3": "@3", "pf4": "@4",
    "pf5": "@5", "pf6": "@6", "pf7": "@7", "pf8": "@8", "pf9": "@9", "pf10": "@a",
    "pf11": "@b", "pf12": "@c", "pf13": "@d", "pf14": "@e", "pf15": "@f", "pf16": "@g",
    "pf17": "@h", "pf18": "@i", "pf19": "@j", "pf20": "@k", "pf21": "@l", "pf22": "@m",
    "pf23": "@n", "pf24": "@o", "end": "@q", "pageup": "@u", "pagedown": "@v", "pa1": "@x",
    "pa2": "@y", "pa3": "@z", "backspace": "@<", "pipe": "@X@c", "shift": "@S", "f1": "@1",
    "f2": "@2", "f3": "@3", "f4": "@4", "f5": "@5", "f6": "@6", "f7": "@7", "f8": "@8",
    "f9": "@9", "f10": "@a", "f11": "@b", "f12": "@c", "f13": "@d", "f14": "@e",
    "f15": "@f", "f16": "@g", "f17": "@h", "f18": "@i", "f19": "@j", "f20": "@k",
    "f21": "@l", "f22": "@m", "f23": "@n", "f24": "@o"
}
