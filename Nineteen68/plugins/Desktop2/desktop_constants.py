#-------------------------------------------------------------------------------
# Name:        oebs_constants
# Purpose:
#
# Author:      sushma.p
#
# Created:     24-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# CONSTANTS
##KEYEVENTF_EXTENDEDKEY = 1
##KEYEVENTF_KEYUP = 2

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

DESKTOP_ERROR_CODES = {'0':'The operating system is out of memory or resources.',
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
OEBS_SCRAPE_KEYWORDS=['clickandadd','fullscrape']

INVALID_KEYWORD='Invalid keyword'

TEST_RESULT_PASS = "Pass"

TEST_RESULT_FAIL = "Fail"

TEST_RESULT_TRUE = "True"

TEST_RESULT_FALSE = "False"

FILE_NOT_EXISTS='File does not exists'

ENABLED_CHECK = 'enabled'

VISIBLE_CHECK = 'visible'

CHECKED_CHECK = 'checked'

SELECTED_CHECK = 'selected'

COMBO_BOX='cbo'

LIST_BOX='list'

LIST_ITEM='list_item'

CLASS='class'

CHILD='children'

LABEL='label'

ELEMENT_FOUND=True

ERROR_MSG = 'Error occured'

APPLICATION_KEYWORDS = ['launchapplication','findwindowandattach','closeapplication','switchtofolder','getemail','getfrommailid','getattachmentstatus','getsubject','gettomailid','getbody','verifyemail']
