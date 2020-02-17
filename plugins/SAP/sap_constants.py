#-------------------------------------------------------------------------------
# Name:        sap_constants
# Purpose:     Module for Sap constants & Error codes
#
# Author:      anas.ahmed1,kavyasree

# Created:     07-04-2017
# Copyright:   (c) anas.ahmed1 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

CUSTOM = '@Custom'

#Dictionary used for send function keys special characters

SENDFUNCTION_KEYS_DICT = {'!':'1',
                          '@': '2',
                          '#':'3',
                          '$':'4',
                          '%':'5',
                          '^':'6',
                          '&':'7',
                          '*':'8',
                          '(':'9',
                          ')':'0'}

SAP_ERROR_CODES = {'0':'The operating system is out of memory or resources.',
                          '2': 'The specified file was not found.',
                          '3':'The specified path was not found.',
                          '5':'The operating system denied access to the specified file',
                          '8':'There was not enough memory to complete the operation.',
                          '10':'Wrong Windows version',
                          '11':'The .EXE file is invalid (non-Win32 .EXE or error in .EXE image)',
                          '12':'Application was designed for a different operating system.',
                          '13':'Application was designed for MS-DOS 4.0',
                          '15':'Attempt to load a real-mode program.',
                          '16':'Attempt to load a second instance of an application with non-readonly data segments',
                          '19':'Attempt to load a compressed application file',
                          '20':'Dynamic-link library (DLL) file failure.',
                          '26':'A sharing violation occurred.',
                          '27':'The filename association is incomplete or invalid.',
                          '28':'The DDE transaction could not be completed because the request timed out..',
                          '29':'The DDE transaction failed.',
                          '30':'The DDE transaction could not be completed because other DDE transactions were being processed..',
                          '31':'There is no application associated with the given filename extension.',
                          '32':'The specified dynamic-link library was not found.'}

SAP_SCRAPE_KEYWORDS = ['clickandadd','fullscrape']

INVALID_KEYWORD = 'Invalid keyword'

INVALID_INPUT = 'Input value is invalid, please provide a valid input'

INVALID_ELELMENT_TYPE = 'Invalid element type, element state does not allow to perform the operation'

ELELMENT_NOT_FOUND = 'Element is not present on the page where the operation is trying to be performed'

ELEMENT_NOT_CHANGEABLE = 'Element is not changeable, element state does not allow to perform the operation'

ELELMENT_NOT_FOUND_HIGHLIGHT = "Element not present on the current window. Please scroll down and try again."

ERROR_HIGHLIGHT = "Error occured while highlighting"

SESSION_ERROR = "Session not found"

SESSION_AND_WINDOW_ERROR = "SAP Session and Window not found"

NO_INSTANCE_OPEN_ERROR = "No instance open of SAP GUI"

TEST_RESULT_PASS = "Pass"

TEST_RESULT_FAIL = "Fail"

TEST_RESULT_TRUE = "True"

TEST_RESULT_FALSE = "False"

FILE_NOT_EXISTS ='File does not exists'

ENABLED_CHECK = 'enabled'

VISIBLE_CHECK = 'visible'

CHECKED_CHECK = 'checked'

UNCHECKED_CHECK = 'unchecked'

SELECTED_CHECK = 'selected'

UNSELECTED_CHECK = 'unselected'

COMBO_BOX = 'cbo'

LIST_BOX = 'list'

LIST_ITEM = 'list_item'

CLASS = 'class'

CHILD = 'children'

LABEL = 'label'

ELEMENT_FOUND = True

ERROR_MSG = 'Error occured'

APPLICATION_KEYWORDS = ['serverconnect','launchapplication','starttransaction','closeapplication']

#refer this to find more icon and the significance
#https://experience.sap.com/files/guidelines/icons_sap/icons_e1_4.htm
ICON_BITMAP = {'S_OKAY':'CHECKED',
             'S_NONO':'INCOMPLETE',
             'S_ERRO':'FAILURE',
             'S_POSI':'POSITIVE',
             'S_NEGA':'NEGATIVE',
             'S_LOCL':'LOCKED',
             'S_LOOP':'UNLOCKED',
             'STA_OK':'STATUS_OK',
             'STABST':'STATUS_BEST',
             'B_SPCE':'SPACE'}

GET_KEYWORDS = ['gettext','gettextboxlength','getstatus','getbuttonname','getselected','getcount','getelementtext','gettooltiptext','geticonname','getinputhelp','getrowcount','getcolumncount','getcolnumbytext','getrownumbytext','getcellvalue','getcellstatus','getcountofrows','getcountofcolumns','getcelltext','getrowcolbytext','getcellcolor','gettreenodetext','gettreenodecount','getcolvaluecorrtoselectednode','getnodenamebyindex']

#-----------------SAP Shell Calender Constants---------------------------------------------
#Dictonary to hold key name and Virtual Key value(used for keyboard inputs)
VK_CODE = {'backspace':0x08,
           'tab':0x09,
           'clear':0x0C,
           'enter':0x0D,
           'shift':0x10,
           'ctrl':0x11,
           'alt':0x12,
           'pause':0x13,
           'caps_lock':0x14,
           'esc':0x1B,
           'spacebar':0x20,
           'page_up':0x21,
           'page_down':0x22,
           'end':0x23,
           'home':0x24,
           'left_arrow':0x25,
           'up_arrow':0x26,
           'right_arrow':0x27,
           'down_arrow':0x28,
           'select':0x29,
           'print':0x2A,
           'execute':0x2B,
           'print_screen':0x2C,
           'ins':0x2D,
           'del':0x2E,
           'help':0x2F,
           '0':0x30,
           '1':0x31,
           '2':0x32,
           '3':0x33,
           '4':0x34,
           '5':0x35,
           '6':0x36,
           '7':0x37,
           '8':0x38,
           '9':0x39,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A,
           'numpad_0':0x60,
           'numpad_1':0x61,
           'numpad_2':0x62,
           'numpad_3':0x63,
           'numpad_4':0x64,
           'numpad_5':0x65,
           'numpad_6':0x66,
           'numpad_7':0x67,
           'numpad_8':0x68,
           'numpad_9':0x69,
           'multiply_key':0x6A,
           'add_key':0x6B,
           'separator_key':0x6C,
           'subtract_key':0x6D,
           'decimal_key':0x6E,
           'divide_key':0x6F,
           'F1':0x70,
           'F2':0x71,
           'F3':0x72,
           'F4':0x73,
           'F5':0x74,
           'F6':0x75,
           'F7':0x76,
           'F8':0x77,
           'F9':0x78,
           'F10':0x79,
           'F11':0x7A,
           'F12':0x7B,
           'F13':0x7C,
           'F14':0x7D,
           'F15':0x7E,
           'F16':0x7F,
           'F17':0x80,
           'F18':0x81,
           'F19':0x82,
           'F20':0x83,
           'F21':0x84,
           'F22':0x85,
           'F23':0x86,
           'F24':0x87,
           'num_lock':0x90,
           'scroll_lock':0x91,
           'left_shift':0xA0,
           'right_shift ':0xA1,
           'left_control':0xA2,
           'right_control':0xA3,
           'left_menu':0xA4,
           'right_menu':0xA5,
           'browser_back':0xA6,
           'browser_forward':0xA7,
           'browser_refresh':0xA8,
           'browser_stop':0xA9,
           'browser_search':0xAA,
           'browser_favorites':0xAB,
           'browser_start_and_home':0xAC,
           'volume_mute':0xAD,
           'volume_Down':0xAE,
           'volume_up':0xAF,
           'next_track':0xB0,
           'previous_track':0xB1,
           'stop_media':0xB2,
           'play/pause_media':0xB3,
           'start_mail':0xB4,
           'select_media':0xB5,
           'start_application_1':0xB6,
           'start_application_2':0xB7,
           'attn_key':0xF6,
           'crsel_key':0xF7,
           'exsel_key':0xF8,
           'play_key':0xFA,
           'zoom_key':0xFB,
           'clear_key':0xFE,
           '+':0xBB,
           ',':0xBC,
           '-':0xBD,
           '.':0xBE,
           '/':0xBF,
           '`':0xC0,
           ';':0xBA,
           '[':0xDB,
           '\\':0xDC,
           ']':0xDD,
           "'":0xDE,
           '`':0xC0}

date_day = { 'MO' : 1,'TU' : 2,'WE' : 3,'TH' : 4,'FR' : 5,'SA' : 6,'SU' : 7 }

Month = {'jan' : 1,'january' : 1,
        'feb' : 2,'february' : 2,
        'mar' :3,'march' :3,
        'apr' :4,'april' :4,
        'may' :5,
        'jun' :6,'june' :6,
        'jul' :7,'july' :7,
        'aug' :8,'august' :8,
        'sept' :9,'september' :9,
        'oct' :10,'october' :10,
        'nov' :11,'november' :11,
        'dec' :12,'december' :12}
#-----------------SAP Shell Calender Constants---------------------------------------------