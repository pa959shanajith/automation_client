##------------------------------------------------------------------------------
# Name : oebs_msg.py
# Purpose : This file contains all the static string assigned to variables.
# Created : 11/12/2015-shaik.shanawaz
# Modified : 8/4/2016-himantika
##------------------------------------------------------------------------------

## code related Constants
MSG_ACCESS_BRIDGE_INIT_ERROR = "Access Bridge Initialization Error."
MSG_NOT_JAVA_WINDOW_INFO = "is not a Java Window."
MSG_INVALID_ACTION_INFO = "Invalid Action specified."
MSG_FAIL = 'Fail'
MSG_PASS = 'Pass'
MSG_TRUE = True
MSG_FALSE = False
MSG_KEYWORD_NA = "Keyword Not Available"


MSG_TEXTBOX_CLEARED = 'The Text in the TextBox is Cleared.'

MSG_STATUS = "Executed and the status is:"
MSG_INVALID_INPUT='Input cannot be empty/null.'
MSG_RESULT = "Executed and the result is:"
MSG_INVALID_OBJECT = 'This Element is not Accessible.'
MSG_HIDDEN_OBJECT = 'The Element is Hidden.'
MSG_DISABLED_OBJECT = 'The Element is Disabled.'
MSG_EXCEPTION = 'Exception occurred:'
MSG_CODE_ERROR = 'Code Error.'
MSG_RESULT_IS = 'Result obtained is:'
MSG_OBJECTSELECTED='Element already Selected'
MSG_OBJECTUNSELECTED='Element already Unselected'
MSG_SELECETED='The Selected values are :'
MSG_VERIFYFAIL = 'Verification failed.'
MSG_INVALID_NOOF_INPUT='Invalid Input.'
MSG_INVALID_FORMAT_INPUT='Invalid Input format.'
MSG_ELEMENT_NOT_FOCUSABLE = 'Element is not Focusable.'
MSG_TEXT_NOT_DEFINED = 'Text not Defined.'
MSG_NAME_NOT_DEFINED = 'Name not Defined.'
MSG_CLICK_SUCCESSFUL = 'Clicked Successfully.'
MSG_ELEMENT_NOT_FOUND = 'Element Not Found'
MSG_ELEMENT_EXIST = 'Element Exists.'
MSG_ELEMENT_NOT_EXISTS='Element doesn not Exists'
MSG_SINGLESELECTION_LIST = 'This operation not supported on SingleSelection list'
MSG_OBJECT_EDITABLE = 'Object is editable.'
MSG_OBJECT_SELECTABLE = 'Object is selectable.'
MSG_OBJECT_READONLY = 'Object is readonly.'
MSG_ELEMENT_NOT_VISIBLE = 'Element is not visible.'
MSG_OBJECT_VISIBLE='Element is visible'
MSG_ELEMENT_NON_EDITABLE='Element is not editable'
MSG_OBJECT_ENABLED='Element is Enabled'
MSG_TIME_OUT_EXCEPTION='Timeout exception'








## Logging Related Constants FILE NAMES
FILE_OEBSCLICKANADD='oebsclickandadd'
FILE_OEBSSERVER = 'oebsServer'
OEBS_TEXTOPS = 'oebs_textops'
OEBS_UTILOPS = 'oebs_utilops'
OEBS_BUTTONOPS = 'oebs_buttonops'
OEBS_RADIOCHECKBOXOPS = 'oebs_radiocheckboxops'
OEBS_DROPDOWNLISTBOX = 'oebs_dropdownlistboxops'
OEBS_ELEMENTS = 'oebs_elementsops'
OEBS_TABLEOPS = 'oebs_tableops'
OEBS_SCROLLBAR = 'oebs_scrollbarops'
OEBS_INTERNALFRAMEOPS = 'oebs_internalframeops'

    #DEFINITIONS RELATED TO oebsServer
DEF_CLICKANDADD = 'clickandadd'
DEF_WINDOWSRUN = 'windowsrun'
DEF_GETHWNDFROMWINDOWNAME = 'GetHwndFromWindowName'
DEF_GETENTIREOBJECTLIST = 'getentireobjectlist'
DEF_ISJAVAWINDOW = 'isjavawindow'
DEF_GETOBJECTFORCUSTOM = 'getobjectforcustom'
DEF_REGISTERFUNCTIONS='register_functions'

    #DEFINITIONS RELATED TO BUTTON/LINK
DEF_GETBUTTONNAME='getbuttonname'
DEF_VERIFYBUTTONNAME='verifybuttonname'
DEF_CLICK='click'
DEF_DOUBLECLICK='doubleclick'
DEF_GETLINKTEXT='getlinktext'
DEF_VERIFYLINKTEXT='verifylinktext'

    #DEFINITION RELATED TO TEXTBOX
DEF_GETTEXT='gettext'
DEF_SETTEXT = 'settext'
DEF_GETTEXTBOXLENGTH='gettextboxlength'
DEF_VERIFYTEXTBOXLENGTH='verifytextboxlength'
DEF_VERIFYTEXT='verifytext'
DEF_CLEARTEXT='cleartext'

    #DEFINITIONS RELATED TO GENERIC KEYWORDS
DEF_SETFOCUS='setfocus'
DEF_VERIFYENABLED='verifyenabled'
DEF_VERIFYDISABLED='verifydisabled'
DEF_VERIFYVISIBLE='verifyvisible'
DEF_VERIFYHIDDEN='verifyhidden'
DEF_VERIFYREADONLY='verifyreadonly'
DEF_GETTOOLTIPTEXT='gettooltiptext'
DEF_VERIFYTOOLTIPTEXT='verifytooltiptext'
DEF_VERIFYEXISTS='verifyexists'
DEF_VERIFYDOESNOTEXISTS='verifydoesnotexists'
DEF_SENDFUNCTIONKEYS = 'sendfunctionkeys'
DEF_RIGHTCLICK = 'rightclick'
DEF_DRAG = 'drag'
DEF_DROP = 'drop'

#DEFINITIONS RELATED TO SCROLLBAR KEYWORDS
DEF_RIGHT = 'right'
DEF_LEFT = 'left'
DEF_UP = 'up'
DEF_DOWN = 'down'

#DEFINITIONS RELATED TO INTERNALFRAME
DEF_CLOSEFRAME = 'closeframe'
DEF_TOGGLEMAXIMIZE = 'togglemaximize'
DEF_TOGGLEMINIMIZE = 'toggleminimize'


#DEFINITIONS RELATED TO RADIO BUTTON/CHECKBOX
DEF_SELECTRADIOBUTTON='selectradiobutton'
DEF_SELECTCHECKBOX='selectcheckbox'
DEF_UNSELECTCHECKBOX='unselectcheckbox'
DEF_GETSTATUS='getstatus'

DEF_SWITCHTOFRAME='switchtoframe'


#DEFINITIONS RELATED TO DROPDOWN/LISTBOX
DEF_GETMULTIPLEVALUESBYINDEXES='getmultiplevaluesbyindexes'
DEF_GETVALUEBYINDEX='getvaluebyindex'
DEF_VERIFYSELECTEDVALUES='verifyselectedvalues'
DEF_SELECTVALUEBYINDEX='selectvaluebyindex'
DEF_SELECTALLVALUES='selectallvalues'
DEF_DESELECTALL='deselectall'
DEF_SELECTMULTIPLEVALUESBYINDEXES='selectmultiplevaluesbyindexes'
DEF_SELECTVALUEBYTEXT='selectvaluebytext'
DEF_SELECTMULTIPLEVALUEBYTEXT='selectmultiplevaluebytext'
DEF_GETSELECTED='getselected'
DEF_VERIFYSELECTEDVALUE='verifyselectedvalue'
DEF_GETCOUNT='getcount'
DEF_VERIFYCOUNT='verifycount'
DEF_VERIFYALLVALUES='verifyallvalues'
DEF_VERIFYVALUESEXISTS='verifyvaluesexists'


#DEFINITIONS RELATED TO ELEMENTS
DEF_CLICKELEMENT = 'clickelement'
DEF_GETELEMENTTEXT = 'getelementtext'
DEF_VERIFYELEMENTTEXT = 'verifyelementtext'

#DEFINITIONS RELATED TO TABLE
DEF_GETROWCOUNT = 'getrowcount'
DEF_GETCOLUMNCOUNT = 'getcolumncount'
DEF_GETCELLVALUE = 'getcellvalue'
DEF_VERIFYCELLVALUE = 'verifycellvalue'
DEF_GETCELLVALUEJAVA='getcellvaluejava'
DEF_GETCELLVALUEOEBS='getcellvalueOebs'
DEF_CELLCLICK = 'cellclick'

#waitForElementVisible
DEF_WAITFORELEMENTVISIBLE = "waitforelementvisible"

#New constants
TEST_RESULT_PASS = 'Pass'
TEST_RESULT_FAIL = 'Fail'
TEST_RESULT_FALSE = 'False'
TEST_RESULT_TRUE = 'True'

ELEMENT_FOUND=True

OUTPUT_CONSTANT ="""9cc33d6fe25973868b30f4439f09901a"""

APPLICATION_ERROR_CODES = {'0':'The operating system is out of memory or resources.',
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




