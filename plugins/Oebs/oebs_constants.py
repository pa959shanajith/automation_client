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
OEBS_SCRAPE_KEYWORDS=['clickandadd','fullscrape']

INVALID_KEYWORD='Invalid keyword'

CUSTOM='@Custom'

ERROR_CODE_DICT = {
    'invalid_input': 'Invalid input, Please provide the valid input',
    'invalid_window': 'Window Handle not Found',
    'err_close_window':  'Unable to Close Window',
    'err_attach_window': 'Unable to Attach to Window',
    'err_launch_app': 'Unable to Launch Application',
    'err_highlight': 'Unable to highlight Object',
    'window_not_foreground': 'Window not in foreground' 
}

