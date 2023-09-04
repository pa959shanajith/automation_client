# -------------------------------------------------------------------------------
# Name:        oebs_constants
# Purpose:
#
# Author:      sushma.p
#
# Created:     24-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
# -------------------------------------------------------------------------------

# CONSTANTS
##KEYEVENTF_EXTENDEDKEY = 1
##KEYEVENTF_KEYUP = 2

# Dictionary used for send function keys special characters

SENDFUNCTION_KEYS_DICT = {
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "%": "5",
    "^": "6",
    "&": "7",
    "*": "8",
    "(": "9",
    ")": "0",
}
OEBS_SCRAPE_KEYWORDS = ["clickandadd", "fullscrape"]

INVALID_KEYWORD = "Invalid keyword"

CUSTOM = "@Custom"

ERROR_CODE_DICT = {
    "invalid_input": "Invalid input, Please provide the valid input",
    "invalid_window": "Window Handle not Found",
    "err_close_window": "Unable to Close Window",
    "err_attach_window": "Unable to Attach to Window",
    "err_launch_app": "Unable to Launch Application",
    "err_highlight": "Unable to highlight Object",
    "window_not_foreground": "Window not in foreground",
    "err_verify_button": "Unable to verify button name",
    "err_click": "Unable to perform click on object",
    "err_double_click": "Unable to perform double click on object",
    "err_object": "Invalid Object",
    "err_get_link_text": "Unable to get link text",
    "err_verify_link_text": "Unable to verify link text",
    "err_get_selected": "Unable to get selected",
    "err_verify_selected": "Unable to verify selected value",
    "err_get_count": "Unable to get count",
    "err_verify_count": "Unable to verify count",
    "err_verify_all_values": "Unable to verify all values",
    "err_verify_values_exist": "Unable to verify if values exist",
    "err_verify_selected_values": "Unable to verify selected values",
    "err_get_multiple_index": "Unable to get multiple values by index",
    "err_select_value_index": "Unable to select value by index",
    "err_get_value_index": "Unable to get value by Index",
    "err_get_all_values": "Unalbe to get all values",
    "err_select_all_values": "Unable to select all values",
    "err_deselect_all": "Unable to deselect all",
    "err_select_multiple_values": "Unalbe to select multiple values by index",
    "err_select_value_text": "Unable to select value by text",
    "err_select_multiple_value_text": "Unable to select multiple values by text",
    "err_click_element": "Unable to click element",
    "err_get_element_text": "Unable to get element text",
    "err_verify_element_exists": "Unable to verify if element exists",
    "err_verify_element_text": "Unable to verify element text",
    "err_wait_element_visible": "Unable to wait for element visible",
    "err_close_frame": "Unable to close frame",
    "err_toggle_maxamize": "Unable to toggle maxamize",
    "err_toggle_minimize": "Unable to toggle minimize",
    "err_get_button_name": "Unable to get button name",
    "err_get_status": "Unable to get status",
    "err_unselect_checkbox": "Unable to unselect checkbox",
    "err_select_checkbox": "Unable to select checkbox",
    "err_select_radiobutton": "Unable to select radiobutton",
    "err_right": "Unable to perform right opertaion",
    "err_left": "Unable to perform left operation",
    "err_up": "Unable to perform up operation",
    "err_down": "Unable to perform down operation",
    "err_get_row_count": "Unable to get row count",
    "err_get_column_count": "Unable to get column count",
    "err_get_cell_value": "Unable to get cell value",
    "err_verify_cell_value": "Unable to verify cell value",
    "err_cell_click": "Unable to perform cell click",
    "err_get_text": "Unable to get text",
    "err_set_text": "Unable to set text",
    "err_set_secure_text": "Unable to set secure text",
    "err_verify_text": "Unable to verify text",
    "err_clear_text": "Unable to clear text",
    "err_set_focus": "Unable to set focus",
    "err_drag": "Unable to perform drag operation",
    "err_drop": "Unable to perform drop operation",
    "err_mouse_hover": "Unable to perform mouse hover",
    "err_verify_enabled": "Unable to verify if object is enabled",
    "err_verify_disabled": "Unable to verify if object is disabled",
    "err_verify_visible": "Unable to verify if object it visible",
    "err_verify_hidden": "Unable to verify if object is hidden",
    "err_verify_read_only": "Unable to verify if object is read only",
    "err_get_tooltip_text": "Unable to get tooltip text",
    "err_verify_tooltip_text": "Unable to verify tooltip text",
    "err_verify_exists": "Unable to verify if object exists",
    "err_verify_not_exists": "Unable to verify if object does not exist",
    "err_right_click": "Unable to perform right click",
    "err_switch_frame": "Unable to switch to frame",
    "err_select_menu": "Error occurred in select menu operation",
    "err_send_function": "Unable to perform send function keys",
    "err_init_core": "Unable to intialise core",
    "err_click_add": "Error occurred during click and add",
    "err_res_window": "Unable to attach to window",
    "err_load_dll": "Unable to load DLL",
    "err_jab": "Java Access Bridge not available",
    "err_jab_base": "Base exception occured while Running DLL",
    "err_run_dll": "Error occurred while trying to run DLL",
    "err_multi_select": "Unable to find element in list",
    "err_visibility_click": "Unable to click, object not present in screen",
    "err_window_find": "Unable to find active window, containing object",
    "err_object_highlight": "Object not found, unable to highlight",
    "invalid_input_scroll": "Invalid input, Please provide number of entries to scroll",
    "err_minimize": "Unable to minimize window",
    "err_maximize": "Unable to maximize window",
    "err_close": "Unable to close window",
    "err_foreground": "Unable to bring window to foreground",
    'err_alternate_path': 'Object not found in alternate xpaths, unable to locate object',
    'err_visible': 'Element not visible, unable to highlight',
    'err_found_not_visible': 'Hidden Object found, Enable Ignore Visibility Check from ICE config to use this object',
    'err_push_btn_scroll_bar': 'Push Buttons inside scroll bars can not be scraped',
    'err_scroll_in_list': 'Scroll bar inside list can not be scraped',
    'wrn_found_not_visible': 'Hidden Object found, but Ignore Visibility Check is enabled, performing operation',
    'err_object_background': 'Window containing object is not on top, can not perform operation',
    'err_value': 'Value does not exist',
    'err_operation_detect': 'Element clicked but operation not detected, Please use alternative keyword double click',
    'err_shell': 'Unable to use shell to bring window on top',
    'err_select_navigator': 'Error occurred in select from navigator',
    'err_finding_object': 'Element not found with primary identifer'
}


## code related Constants
MSG_ACCESS_BRIDGE_INIT_ERROR = "Access Bridge Initialization Error."
MSG_NOT_JAVA_WINDOW_INFO = "is not a Java Window."
MSG_INVALID_ACTION_INFO = "Invalid Action specified."
MSG_FAIL = "Fail"
MSG_PASS = "Pass"
MSG_TRUE = True
MSG_FALSE = False
MSG_KEYWORD_NA = "Keyword Not Available"


MSG_TEXTBOX_CLEARED = "The Text in the TextBox is Cleared."

MSG_STATUS = "Executed and the status is:"
MSG_INVALID_INPUT = "Input cannot be empty/null/invalid."
MSG_RESULT = "Executed and the result is:"
MSG_INVALID_OBJECT = "This Element is not Accessible."
MSG_HIDDEN_OBJECT = "The Element is Hidden."
MSG_DISABLED_OBJECT = "The Element is Disabled."
MSG_EXCEPTION = "Exception occurred:"
MSG_CODE_ERROR = "Code Error."
MSG_RESULT_IS = "Result obtained is:"
MSG_OBJECTSELECTED = "Element already Selected"
MSG_OBJECTUNSELECTED = "Element already Unselected"
MSG_SELECETED = "The Selected values are :"
MSG_VERIFYFAIL = "Verification failed."
MSG_INVALID_NOOF_INPUT = "Invalid Input."
MSG_INVALID_FORMAT_INPUT = "Invalid Input format."
MSG_ELEMENT_NOT_FOCUSABLE = "Element is not Focusable."
MSG_TEXT_NOT_DEFINED = "Text not Defined."
MSG_NAME_NOT_DEFINED = "Name not Defined."
MSG_CLICK_SUCCESSFUL = "Clicked Successfully."
MSG_ELEMENT_NOT_FOUND = "Element Not Found"
MSG_ELEMENT_EXIST = "Element Exists."
MSG_ELEMENT_NOT_EXISTS = "Element does not Exists"
MSG_SINGLESELECTION_LIST = "This operation not supported on SingleSelection list"
MSG_OBJECT_EDITABLE = "Object is editable."
MSG_OBJECT_SELECTABLE = "Object is selectable."
MSG_OBJECT_READONLY = "Object is readonly."
MSG_ELEMENT_NOT_VISIBLE = "Element is not visible."
MSG_OBJECT_VISIBLE = "Element is visible"
MSG_ELEMENT_NON_EDITABLE = "Element is not editable"
MSG_OBJECT_ENABLED = "Element is Enabled"
MSG_TIME_OUT_EXCEPTION = "Timeout exception"

## Logging Related Constants FILE NAMES
FILE_OEBSCLICKANADD = "oebsclickandadd"
OEBS_TEXTOPS = "oebs_textops"
OEBS_UTILOPS = "oebs_utilops"
OEBS_BUTTONOPS = "oebs_buttonops"
OEBS_RADIOCHECKBOXOPS = "oebs_radiocheckboxops"
OEBS_DROPDOWNLISTBOX = "oebs_dropdownlistboxops"
OEBS_ELEMENTS = "oebs_elementsops"
OEBS_TABLEOPS = "oebs_tableops"
OEBS_SCROLLBAR = "oebs_scrollbarops"
OEBS_INTERNALFRAMEOPS = "oebs_internalframeops"

# DEFINITIONS RELATED TO full scrape
DEF_GETENTIREOBJECTLIST = "getentireobjectlist"
DEF_ISJAVAWINDOW = "isjavawindow"

# DEFINITIONS RELATED TO BUTTON/LINK
DEF_GETBUTTONNAME = "getbuttonname"
DEF_VERIFYBUTTONNAME = "verifybuttonname"
DEF_CLICK = "click"
DEF_DOUBLECLICK = "doubleclick"
DEF_GETLINKTEXT = "getlinktext"
DEF_VERIFYLINKTEXT = "verifylinktext"

# DEFINITION RELATED TO TEXTBOX
DEF_GETTEXT = "gettext"
DEF_SETTEXT = "settext"
DEF_GETTEXTBOXLENGTH = "gettextboxlength"
DEF_VERIFYTEXTBOXLENGTH = "verifytextboxlength"
DEF_VERIFYTEXT = "verifytext"
DEF_CLEARTEXT = "cleartext"

# DEFINITIONS RELATED TO GENERIC KEYWORDS
DEF_SETFOCUS = "setfocus"
DEF_VERIFYENABLED = "verifyenabled"
DEF_VERIFYDISABLED = "verifydisabled"
DEF_VERIFYVISIBLE = "verifyvisible"
DEF_VERIFYHIDDEN = "verifyhidden"
DEF_VERIFYREADONLY = "verifyreadonly"
DEF_GETTOOLTIPTEXT = "gettooltiptext"
DEF_VERIFYTOOLTIPTEXT = "verifytooltiptext"
DEF_VERIFYEXISTS = "verifyexists"
DEF_VERIFYDOESNOTEXISTS = "verifydoesnotexists"
DEF_SENDFUNCTIONKEYS = "sendfunctionkeys"
DEF_RIGHTCLICK = "rightclick"
DEF_DRAG = "drag"
DEF_DROP = "drop"

# DEFINITIONS RELATED TO SCROLLBAR KEYWORDS
DEF_RIGHT = "right"
DEF_LEFT = "left"
DEF_UP = "up"
DEF_DOWN = "down"

# DEFINITIONS RELATED TO INTERNALFRAME
DEF_CLOSEFRAME = "closeframe"
DEF_TOGGLEMAXIMIZE = "togglemaximize"
DEF_TOGGLEMINIMIZE = "toggleminimize"


# DEFINITIONS RELATED TO RADIO BUTTON/CHECKBOX
DEF_SELECTRADIOBUTTON = "selectradiobutton"
DEF_SELECTCHECKBOX = "selectcheckbox"
DEF_UNSELECTCHECKBOX = "unselectcheckbox"
DEF_GETSTATUS = "getstatus"

DEF_SWITCHTOFRAME = "switchtoframe"


# DEFINITIONS RELATED TO DROPDOWN/LISTBOX
DEF_GETMULTIPLEVALUESBYINDEXES = "getmultiplevaluesbyindexes"
DEF_GETVALUEBYINDEX = "getvaluebyindex"
DEF_VERIFYSELECTEDVALUES = "verifyselectedvalues"
DEF_SELECTVALUEBYINDEX = "selectvaluebyindex"
DEF_SELECTALLVALUES = "selectallvalues"
DEF_DESELECTALL = "deselectall"
DEF_SELECTMULTIPLEVALUESBYINDEXES = "selectmultiplevaluesbyindexes"
DEF_SELECTVALUEBYTEXT = "selectvaluebytext"
DEF_SELECTMULTIPLEVALUEBYTEXT = "selectmultiplevaluebytext"
DEF_GETSELECTED = "getselected"
DEF_VERIFYSELECTEDVALUE = "verifyselectedvalue"
DEF_GETCOUNT = "getcount"
DEF_VERIFYCOUNT = "verifycount"
DEF_VERIFYALLVALUES = "verifyallvalues"
DEF_VERIFYVALUESEXISTS = "verifyvaluesexists"
DEF_SELECTFROMNAVIGATOR = "selectfromnavigator"


# DEFINITIONS RELATED TO ELEMENTS
DEF_CLICKELEMENT = "clickelement"
DEF_GETELEMENTTEXT = "getelementtext"
DEF_VERIFYELEMENTTEXT = "verifyelementtext"

# DEFINITIONS RELATED TO TABLE
DEF_GETROWCOUNT = "getrowcount"
DEF_GETCOLUMNCOUNT = "getcolumncount"
DEF_GETCELLVALUE = "getcellvalue"
DEF_VERIFYCELLVALUE = "verifycellvalue"
DEF_GETCELLVALUEJAVA = "getcellvaluejava"
DEF_GETCELLVALUEOEBS = "getcellvalueOebs"
DEF_CELLCLICK = "cellclick"

# waitForElementVisible
DEF_WAITFORELEMENTVISIBLE = "waitforelementvisible"

# New constants
TEST_RESULT_PASS = "Pass"
TEST_RESULT_FAIL = "Fail"
TEST_RESULT_FALSE = "False"
TEST_RESULT_TRUE = "True"

ELEMENT_FOUND = True

OUTPUT_CONSTANT = """9cc33d6fe25973868b30f4439f09901a"""

APPLICATION_ERROR_CODES = {
    "0": "The operating system is out of memory or resources.",
    "2": "The specified file was not found.",
    "3": "The specified path was not found.",
    "5": "The operating system denied access to the specified file",
    "8": "There was not enough memory to complete the operation.",
    "10": "Wrong Windows version",
    "11": "The .EXE file is invalid (non-Win32 .EXE or error in .EXE image)",
    "12": "Application was designed for a different operating system.",
    "13": "Application was designed for MS-DOS 4.0",
    "15": "Attempt to load a real-mode program.",
    "16": "Attempt to load a second instance of an application with non-readonly data segments",
    "19": "Attempt to load a compressed application file",
    "20": "Dynamic-link library (DLL) file failure.",
    "26": "A sharing violation occurred.",
    "27": "The filename association is incomplete or invalid.",
    "28": "The DDE transaction could not be completed because the request timed out..",
    "29": "The DDE transaction failed.",
    "30": "The DDE transaction could not be completed because other DDE transactions were being processed..",
    "31": "There is no application associated with the given filename extension.",
    "32": "The specified dynamic-link library was not found.",
}
