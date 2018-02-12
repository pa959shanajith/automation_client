#-------------------------------------------------------------------------------
# Name:        webocular_constants.py
# Purpose:     Defines constants used in the webocular plugin
#
# Author:      nikunj.jain
#
# Created:     10-08-2017
# Copyright:   (c) nikunj.jain 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

"""
This file contains all the constants used in Webocular plugin

"""


# User agent strings for all supported browsers
CHROME_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
FX_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/53.09"
IE_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
SAFARI_AGENT = "Mozilla/5.0 AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"

"""request timeout in seconds"""
REQUEST_URL_TIMEOUT=40

"""tuple of file extensions to ignore downloading entire body i.e. file"""
IGNORE_FILE_EXTENSIONS = ('.pdf','.docx','.zip','.dmg')
