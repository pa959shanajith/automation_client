#-------------------------------------------------------------------------------
# Name:        constants
# Purpose:
#
# Author:      sushma.p
#
# Created:     21-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import platform
from os.path import normpath

OS_SEP = os.sep

AVO_ASSURE_HOME = os.environ["AVO_ASSURE_HOME"]

IF='if'

ELSE_IF='elseif'

ELSE='else'

ENDIF='endif'

FOR='for'

ENDFOR='endfor'

GETPARAM='getparam'

STARTLOOP='startloop'

ENDLOOP = 'endloop'

FILE_TYPE_XLS = 'xls'

FILE_TYPE_XLSX = 'xlsx'

FILE_TYPE_CSV = 'csv'

FILE_TYPE_XML = 'xml'

TEST_RESULT_PASS = 'Pass'

TEST_RESULT_FAIL = 'Fail'

TEST_RESULT_FALSE = 'False'

TEST_RESULT_TRUE = 'True'

HYPHEN = '-'

APPTYPE_WEB = 'web'

APPTYPE_GENERIC = 'generic'

APPTYPE_SYSTEM = 'system'

APPTYPE_WEBSERVICE = 'webservice'

APPTYPE_MAINFRAME = 'mainframe'

APPTYPE_DESKTOP = 'desktop'

APPTYPE_SAP = 'sap'

APPTYPE_DESKTOP_JAVA = 'oebs'

APPTYPE_MOBILE='mobileweb'

APPTYPE_MOBILE_APP = 'mobileapp'

APPTYPE_PDF = 'pdf'

IGNORE_THIS_STEP = '<<Ignore.This.Step>>'

SEMICOLON = ';'

JUMP_TO = 'jumpto'

JUMP_BY = 'jumpby'

PIPE = '|'

INVALID='Invalid'

TERMINATE='Terminate'

INCOMPLETE = 'Incomplete'

BREAK_POINT='Debug Stopped'

PAUSE='pause'

CONTINUE='continue'

CUSTOM='@Custom'

VERIFY_EXISTS='verifyexists'

VERIFY_VISIBLE='verifyvisible'

DYNAMIC_KEYWORDS=['createdynvariable','copyvalue','modifyvalue','deletedynvariable']

CONSTANT_KEYWORDS=['createconstvariable','deleteconstvariable']

CREATE_DYN_VARIABLE='createdynvariable'

CREATE_CONST_VARIABLE='createconstvariable'

COPY_VALUE='copyvalue'

MODIFY_VALUE='modifyvalue'

DELETE_DYN_VARIABLE='deletedynvariable'

WS_KEYWORDS=['setheader','setheadertemplate']

PARALLEL = 'parallel'

SERIAL = 'serial'

ERROR_CODE_DICT = {
                    'NULL_DATA' : 'Cannot verify text with the null data',
                    'MSG_STATUS' : 'Executed and the status is:',
                    'ERR_INVALID_INPUT':'Input error: please provide the valid input.',
                    'INCORRECT_VARIABLE_FORMAT':'Incorrect variable format to store custom object',
                    'MSG_RESULT':'Executed and the result is:',
                    'ERR_INVALID_OBJECT':'This Element is not Accessible.',
                    'ERR_HIDDEN_OBJECT':'The element is Hidden.',
                    'ERR_DISABLED_OBJECT':'The Element is Disabled.',
                    'ERR_EXCEPTION':'Exception occurred:',
                    'ERR_REMEMBERED_CREDENTIALS_PRESENT':'Remembered Credentials Present',
                    'ERR_WIN32':'Error occured when entering credentials',
                    'ERR_CODE_ERROR':'Code Error.',
                    'MSG_RESULT_IS':'Result obtained is:',
                    'ERR_OBJECTSELECTED':'Checkbox already Selected',
                    'ERR_OBJECTUNSELECTED':'Checkbox already Unselected',
                    'MSG_SELECETED':'The Selected values are :',
                    'MSG_ELEMENT_NOT_FOUND':'Element not found.',
                    'MSG_OBJECT_ENABLED':'The Element is enabled.',
                    'ERR_OBJECT_DISABLED':'The object is disabled.',
                    'MSG_OBJECT_DISPLAYED':'The object is displayed.',
                    'MSG_OBJECT_NOT_DISPLAYED':'The object is not displayed.',
                    'ERR_UNABLE_TO_SELECT':'Unable to select.',
                    'ERR_CURRENT_STATE':'The current operation cannot be performed because of the object state.',
                    'ERR_OBJECT_NOT_FOUND':'Object Not Found.',
                    'ERR_UNABLE_TO_GET_COUNT':'Unable to get the count.',
                    'ERR_EMPTY_LIST':'List is empty.',
                    'ERR_NEGATIVE_ELEMENT_INDEX':'Element index should be greater than or equal to zero.',
                    'ERR_APPLICATION_ALREADY_OPEN':'Window with the same name already exists; close to proceed further.',
                    'ERR_WINDOW_NOT_FOUND_TERMINATE':'Unable to find the window hence terminating the execution.',
                    'ERR_LESS_MEMORY':'Insufficient memory.',
                    'ERR_OPERATING_SYSTEM_MEMORY':'The operating system is out of memory or resources.',
                    'ERR_DENIED_ACCESS':'The operating system denied access to the specified file.',
                    'ERR_WRONG_WINDOW_VERSION':'Wrong Windows version.',
                    'ERR_INVALID_EXE_FILE':'The .EXE file is invalid (non-Win32 .EXE or error in .EXE image).',
                    'ERR_DIFFERENT_OPERATING_SYSTEM':'Application was designed for a different operating system.',
                    'ERR_APPLCATION_DESIGNED_FOR_MS_DOS': 'Application was designed for MS-DOS 4.0.',
                    'ERR_REAL_MODE_PROGRAM': 'Attempt to load a real-mode program.',
                    'ERR_SECOND_INSTANCE': 'Attempt to load a second instance of an application with non-readonly data segments.',
                    'ERR_COMPRESSED_FILE': 'Attempt to load a compressed application file.',
                    'ERR_DLL_FAILURE': 'Dynamic-link library (DLL) file failure.',
                    'ERR_SHARING_VIOLATION': 'A sharing violation occurred.',
                    'ERR_INCOMPLETE_FILENAME_ASSOCIATION': 'The filename association is incomplete or invalid.',
                    'ERR_DDE_TIMED_OUT' : 'The DDE transaction could not be completed because the request timed out.',
                    'ERR_DDE_FAILED':'The DDE transaction failed.',
                    'ERR_DDE_PROCESSING':'The DDE transaction could not be completed because other DDE transactions were being processed.',
                    'ERR_DLL_NOT_FOUND':'The specified dynamic-link library was not found.',
                    'ERR_UNABLE_TO_LAUNCH': 'unable to launch the application.',
                    'ERR_TOOLTIP_NOT_GIVEN': 'Tooltip text not available.',
                    'ERR_PLUGINS_PATH': 'please check your plugins path.',
                    'ERR_BROWSER_INPUT': 'Invalid Browser Input.',
                    'ERR_CHROME_INSTANCE': 'Unable to terminate the chrome driver instance.',
                    'ERR_NO_SUCH_FILE_EXCEPTION':"File doesn't exist.",
                    'TERMINATE':'Terminated Successfully.',
                    'ERR_NULL_POINTER_EXCEPTION' : 'Input Error:Please provide valid input.',
                    'ERR_SQL_EXCEPTION': 'Unable to establish connection to DB, please check your Input Query.',
                    'ERR_FILE_NOT_FOUND_EXCEPTION': 'File not found in the specified path.',
                    'ERR_FILE_NOT_ACESSIBLE': 'Permisson denied, File is already open',
                    'ERR_FOLDER_NOT_ACESSIBLE': 'Permisson denied, Folder not accessible',
                    'ERR_ILLEGAL_ARGUMENT_EXCEPTION': 'Input Error: Please provide valid input.',
                    'ERR_NO_IMAGE_SOURCE': 'Image source not available.',
                    'MSG_IMAGE_COMPARE_PASS':'Image comparision is Pass',
                    'ERR_IMAGE_COMPARE_FAIL':'Image comparision is Fail',
                    'ERR_NUMBER_FORMAT_EXCEPTION': 'Input Error: Invalid input format.',
                    'ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION': 'Input Error: Invalid number of inputs.',
                    'ERR_ARRAY_INDEX_OUT_OF_BOUNDS_EXCEPTION': 'Input Error: Invalid number of inputs.',
                    'ERR_STRING_INDEX_OUT_OF_BOUNDS_EXCEPTION': 'Input Error: Invalid number of inputs.',
                    'ERR_INPUT_EXCEEDS': 'The input provided exceeds the number of windows open',
                    'ERR_WEB_DRIVER_EXCEPTION': 'Error occurred with browser',
                    'INVALID_TABLE_INDEX': 'Invalid Input: Index input cannot be 0 for table',
                    'CLICKABLE_EXCEPTION': 'File type input Element is not Clickable, use uploadFile keyword instead.',
                    'PRESSABLE_EXCEPTION': 'File type input Element is not Pressable, use uploadFile keyword instead.',
                    'ERR_NO_SUCH_WINDOW_EXCEPTION': "Requested web page can't be found.",
                    'ERR_UNHANDELED_ALERT_EXCEPTION': 'Error occurred due to unexpected alert.',
                    'ERR_INVALID_SELECTOR_EXCEPTION': 'Object Not Found.',
                    'ERR_ELEMENT_NOT_VISIBLE_EXCEPTION': 'Object is hidden.',
                    'ERR_NO_SUCH_ELEMENT_EXCEPTION': 'Object Not Found.',
                    'ERR_INVALID_ELEMENT_STATE_EXCEPTION': 'The current operation cannot be performed because of the object state.',
                    'ERR_TIME_OUT_EXCEPTION': "Can't locate the object in the specified time.",
                    'ERR_NO_ALERT_PRESENT_EXCEPTION': 'Alert not present.',
                    'ERR_SAX_EXCEPTION': 'Input error: please provide the valid input.',
                    'ERR_JSON_EXCEPTION': 'Please provide valid JSON.',
                    'ERR_MALFORMED_EXCEPTION': 'Malformed Json with syntax errors.',
                    'ERR_INPUT_MISS_MATCH': 'Input does not match',
                    'ERR_STALE_ELEMENT_REFERENCE_EXCEPTION': 'Object Not Found.',
                    'ERR_ELEMENT_NOT_FOUND_EXCEPTION': 'Object Not Found.',
                    'ERR_IO_EXCEPTION': 'File is read only.',
                    'ERR_ILLEGAL_STATE_EXCEPTION': 'The current operation cannot be performed because of the object state.',
                    'ERR_OBJECT_VISIBLE': 'The Element is visible.',
                    'ERR_EMPTY_STACK_EVAL_EXCEPTION': 'Input error:Verify syntax.',
                    'ERR_PARSE_EXCEPTION': 'Input Error:Please provide valid input.',
                    'ERR_INVALID_OPERATION': 'Invalid input: Operation name invalid or missing.',
                    'ERR_INVALID_HEADER': 'Invalid input: Header name invalid or missing.',
                    'ERR_INVALID_METHOD': 'Invalid input: Method name invalid or missing.',
                    'ERR_INVALID_END_POINT_URL': 'Invalid input: End Point URL is invalid or missing.',
                    'ERR_VALUE_NOT_FETCHED': 'Sorry! Values could not be fetched.',
                    'ERR_RESPONSE_HEADER_EMPTY': 'Response Header Value is Empty.',
                    'ERR_RESPONSE_BODY': 'Response Body could not be Obtained.',
                    'ERR_RESPONSE_BODY_EMPTY': 'Response Body  is Empty.',
                    'ERR_NO_TEMPLATE': 'Template Not Found.',
                    'ERR_HTML_SOURCE_CODE': 'Unable to render the HTML source code.',
                    'ERR_SET_CURSOR': 'Row or Column value exceeds the limit specified(22/80).',
                    'ERR_JOB_STATUS': 'Job Status is Failed.',
                    'ERR_GETTEXT_MAINFRAME': 'Text not found.',
                    'ERR_DATE_MISMATCH': 'Inputs do not match.',
                    'ERR_DATE_VALID': 'Please provide valid date.',
                    'ERR_DISPLAY_TIMEOUT': 'Display Timeout cannot be less than or equal to 0.',
                    'ERR_CONTENT_NULL': 'Invalid Input:No content found in the specified location.',
                    'ERR_IMAGE_CLASS_CAST_EXCEPTION' : 'Image operations does not supported 8 or 32 bit depth images.',
                    'ERR_EVAL_INVALIDINPUT_FLAG' : 'Invalid input, Hence evaluate method failed.',
                    'ERR_EVAL_DIVIDEBYZERO_FLAG': 'Ooops !! Divide by zero occured, Hence evaluate method failed.',
                    'ERR_EVAL_LONGRESULT_FLAG': 'Input|Output value exceeds seventeen digits.',
                    'ERR_INVALID_NO_INPUT': 'Input Error: Invalid number of inputs.',
                    'ERR_GETPARAM_EXCEL': "Excel sheet doesn't contain column names.",
                    'ERR_GETPARAM_UNIQUECOLUMN': 'Excel sheet should contain Unique Column names',
                    'ERR_XML_INVALID': 'Invalid XML format.',
                    'ERR_DYNVAR': 'Variable does not exist.',
                    'ERR_CONVAR': 'Constant Variable does not exist.',
                    'ERR_DYNVAR_ALREADY_EXISTS': 'Variable already exists',
                    'ERR_CONSVAR_ALREADY_EXISTS': 'Constant Variable already exists',
                    'ERR_XML_TAGNAMES': "XML file doesn't contain tag names.",
                    'MSG_EXTERNAL_DATALIST_STATICVARIABLE': 'Invalid Input:No externalData List exists for static variable.',
                    'ERR_CAPTURE_SCREENSHOT':'Unable to capture the screenshots.',
                    'ERR_CAPTURE_LOGS':'Unable to capture the logs.',
                    'ERR_SAVE_IMG':'Unable to save the screenshot in report NFS',
                    'ERR_SAVE_LOGS':'Unable to save the logs in report NFS',
                    'ERR_GET_OBJ':'Unable to fetch the screenshot url from report NFS',
                    'ERR_DOUBLECLICK':'Error occurred while performing double click.',
                    'ERR_OBJECT_IS_NOT_LINK':'Given object is not a link.',
                    'ERR_ELEMENT_NOT_SELECTED':'Object not selected.',
                    'ERR_TEXTBOX_SIZE_UNDEFINED':'Textbox size is not defined.',
                    'MSG_ELEMENT_EXISTS':'Element exists.',
                    'ERR_ELEMENT_NOT_EXISTS':'Element does not exists.',
                    'ERR_ELEMENT_EXISTS':'Element exists.',
                    'ERR_GET_COLUMN_COUNT_EXCEPTION':'Exception occured in getColumnCount.',
                    'ERR_ROW_COLUMN':'Row number and Column nunber shoud be greater than 0.',
                    'ERR_ROW_COL_OUT_OF_RANGE':'Row number and column number should be within range',
                    'ERR_SAFARI_EXCEPTION':'This action cannot be performed in safari for encoded elements.',
                    'ERR_SET_FOCUS_EXCEPTION':'Exception occurred in setFocus.',
                    'ERR_ELEMENT_IS_NOT_READONLY':'Element is not readonly.',
                    'ERR_ELEMENT_IS_READONLY':'Element is readonly.',
                    'ERR_IIO_EXCEPTION':'File not found in the specified path.',
                    'ERR_DRIVER_IS_NULL':'Driver is null. Hence cannot capture screenshot.',
                    'ERR_NO_MATCH':'The Cell value and Expected value do-not Match.',
                    'ERR_WEB_ELEMENT_IS_NULL':'The WebElement Value is null.',
                    'ERR_NO_ACCESS_TO_FOLDER':'Invalid input: No access to folder or folder doesnot exists.',
                    'ERR_CONNECTION_FAILED':'Unable to establish connection to DB',
                    'ERR_VALUES_DOESNOT_MATCH':'Values does not match',
                    'ERR_INPUT_TYPE_MISMATCH': 'Cannot set text to a numerical textbox',
                    'ERR_INPUT_NOT_PRESENT':'Content does not exist in the file',
                    #controller messages
                    'ERR_ENDIF_TERMINATE_EXECUTION': ' Execution Terminated : End if/Endfor is missing',
                    'ERR_INVALID_TESTCASE':'Execution Terminated : Jump to test case name not present',
                    'ERR_ENDFOR_TERMINATE_EXECUTION':'Execution Terminated : Endfor/End if is missing',
                    'ERR_START_END_LOOP':'Execution Terminated : Start Loop or End Loop is missing',
                    'ERR_TERMINATE_EXECUTION':'-------Terminating the execution-------',
                    'ERR_OOPS_NODATA_GETPARAM':'Oops!! There is no data in external file to Perform Data Parameterization',
                    'ERR_INVALIDFILE_GETPARAM':'Invalid file\n',
                    'ERR_FILE_EXT_MISMATCH':'File not found/File types are not same',
                    'ERR_CUSTOM_VERIFYEXISTS':'Previous step VerifyExists is missing',
                    'ERR_CUSTOM_NOTFOUND':'Custom Object not Found',
                    'ERR_CUSTOM_MISMATCH':'Input type and keyword mismatch',
                    'ERR_PREVIOUS_CLICKELEMENT':'Previous step ClickElement is missing !',
                    'ERR_PRECONDITION_NOTMET':'PreCondition for CustomObject not met',
                    'ERR_REF_ELE_NULL':'Reference Element is null',
                    'ERR_IF_FAIL':'IF condition is Fail \n',
                    'ERR_FOR_STARTED':'---------- Started executing FOR ----------\n',
                    'ERR_FOR_END':'EndFor\n',
                    'ERR_KILL_DRIVER':'Error occured:Unable to terminate the driver instance\n',
                    'ERR_KILL_CHROMEDRIVER':'Unable to terminate the chrome driver instance',
                    'ERR_ENCOUNTERED_DANGLING_START':'Encountered Dangling Pointer startLoop',
                    'ERR_CONTROLLER_IO':'Generating Json report failed\n',
                    'ERR_SCREENSHOT_PATH':'Screenshot not captured - User does not have sufficient privileges for screenshot folder\n',
                    #Excel error messages
                    'ERR_ROW_NUMBER':'Invalid row number',
                    'ERR_COL_NUMBER':'Invalid column number',
                    "ERR_ROW_DOESN'T_EXIST": "Row doesn't exist",
                    "ERR_COL_DOESN'T_EXIST": "Column doesn't exist",
                    'ERR_FILE_FORMAT': 'The specified file is not Excel file\n',
                    "ERR_MULTIROW_DOESN'T_EXIST":"Rows doesn't exist",
                    #JumpBy error messages
                    "ERR_JUMPY_STEP_DOESN'T_EXISTS" : "Invalid input, jumpBy Step doesn't exist",
                    "ERR_JUMPBY_CAN'T_BE_0": "Invalid input, jumpBy Step?cannot be '0'",
                    'ERR_CUSTOM_ELE_NOTFOUND':'Error occured in finding Custom element',
                    # Database Keywords
                    "ERR_DB_CONNECTION": "Error with database connection",
                    "ERR_DB_OPS": "Error with database operation",
                    "ERR_DB_QUERY": "Error with database query",
                    "ERR_FILE_WRITE": "Error writing to file",
                    "ERR_JAVA_NOT_FOUND": "JAVA_HOME environment variable is not set",
                    "ERR_INVALID_SHEET": "Input error: Invalid Sheet name",
                    "ERR_TIMEOUT_EXCEEDED":"Delay Timeout Exceeded"
                }

STOP='stop'

#Reporting constants

ROWS='rows'

OVERALLSTATUS='overallstatus'

COMMENTS_LENGTH='commentsLength'

ID='id'

PARENT_ID='parentId'

STATUS='status'

STEP='Step'

COMMENTS='Comments'

SCREENSHOT_PATH = 'screenshot_path'

SCREENSHOT_PATH_ALT = 'screenshot_path_alt'

SCREENSHOT_NFS_AVAILABLE = False

SCREENSHOT_PATH_LOCAL = AVO_ASSURE_HOME + OS_SEP + 'Screenshots'

STEP_DESCRIPTION='StepDescription'

ELLAPSED_TIME='EllapsedTime'

REMARKS='Remark'

TESTCASE_DETAILS='testcase_details'

KEYWORD='Keyword'

TEST_SCRIPT_NAME='TestCase Name'

END_TIME='EndTime'

BROWSER_VERSION='browserVersion'

BROWSER_TYPE='browserType'

DATE='date'

TIME='time'

START_TIME='StartTime'

TIME_FORMAT='%Y-%m-%d %H:%M:%S'

CYCLE_NAME='cycleName'

PROJECT_NAME='projectName'

DOMAIN_NAME='domainName'

SCENARIO_NAME='scenarioName'

RELEASE_NAME='releaseName'

VERSION='version'

TERMINATED_BY='terminatedBy'

USER_TERMINATED='user'

PROGRAM_TERMINATED='program'

#Logger constants

KEYWORD_EXECUTION_STARTED = 'Keyword  execution started'

KEYWORD_STATUS = 'Keyword %s executed Successfully and the status is %s'

KEYWORD_EXECUTION_COMPLETED = 'Keyword  execution completed'

METHOD_OUTPUT = 'Result of the Keyword: '

KEYWORD_EXECUTION_FAIL_DUE_TO_NO_WEBELEMENT = 'Keyword Execution failed, Reason : Web Element not found'

STATUS_METHODOUTPUT_LOCALVARIABLES = 'Status, Method output and local variable are initialised to default values'

STATUS_METHODOUTPUT_UPDATE = 'Updating  Status and Method output to Pass and True respectively'

EXCEPTION_OCCURED = 'Exception occured'

RETURN_RESULT = 'Returning Result of keyword execution'

WEB_ELEMENT_FOUND = 'Web Element found'

WEB_ELEMENT_NOT_FOUND = 'Web Element not found'

WEB_ELEMENT_ENABLED = 'Web Element Enabled'

ELEMENT_ENABLED = 'Element Enabled'

WEB_ELEMENT_DISABLED = 'Web Element is disabled, hence cannot perform operation'

WEB_ELEMENT_FILE_TYPE = 'Web element is file type, click can not be performed'

INVALID_INPUT = 'Invalid input, Please provide the valid input'

WEB_ELEMENT_FOUND_INSIDE_IFRAME='Web Element is found inside iframe/frame '

OUTPUT_CONSTANT ="9cc33d6fe25973868b30f4439f09901a"

MD5_TEMP_RES  ="9cc33d6fe25973868b30f4439f09901a"

MSG_CUSTOM_FOUND='Custom Object is Found'

EXPECTED='Expected: '

ACTUAL='Actual :'

INPUT_IS='Input is: '

MAX_SIZE_EXCEEDED='Maximum size of Web element map is 4 '

INPUT_ERROR='Input error'

EXECUTE='execute'

DEBUG='debug'

STEP_BY_SETP_DEBUG='step_debug'

CORE='Core'

INVALID_KEYWORD='Invalid Keyword'

DRAG='drag'

DROP='drop'

USER_TERMINATION='Terminated by the user'

PROGRAM_TERMINATION='Terminated'

DATABASE_KEYWORDS=['getdata','securegetdata']

DESKTOP_LIST_KEYWORDS=['getmultiplevaluesbyindexes','getvaluebyindex']

DB_VAR='ret_riever'

COMPLETED='success'

MULTIPLE_OUTPUT_KEYWORDS=['split']

DISPALY_VARIABLE_VALUE='displayvariablevalue'

DATE_COMPARE='datecompare'

STEPSTATUS_INREPORTS_ZERO = '0'

EVALUATE='evaluate'

NUMBER_FORMATTER='numberformatter'

ENDFOR_DESCRIPTION='EndFor: completed'

JIRA_ACTION_1 = 'loginToJira'

JIRA_ACTION_2 = 'createIssueInJira'

JIRA_ACTION_3 = 'getJiraConfigureFields'

STATIC_NONE = "{#@#n_o_n_e#@#}"

STATIC_DV_NAME = "{#@#n_u_m#@#}"

WEB_ELEMENT_FOUND_FROM_GetInnerTable = 'Web Element found from GetInnerTable'

BROWSER_NAME = {'1': 'Chrome', '2': 'Firefox', '3': 'Internet Explorer', '6': 'Safari', '7': 'Edge Legacy', '8': 'Edge Chromium'}

BROWSER_NAME_LOG = {'1': 'Chrome', '2': 'FireFox', '3': 'InternetExplorer', '6': 'Safari', '7': 'EdgeLegacy', '8': 'EdgeChromium'}

FIREFOX_BROWSER_VERSION = {"0.13":[52,53],"0.16":[52,53],"0.19":[55,62],"0.21":[55,62],"0.23":[55,64],"0.30":[80,100]}

CHROME_DRIVER_VERSION = {"2.45":[70,72],"2.44":[69,71],"2.43":[69,71],"2.41":[67,69],"2.40":[66,68],"2.39":[66,68],"2.38":[65,67],"2.37":[64,66],"2.36":[63,65],"2.35":[62,65]}

EDGE_VERSION = {"10.0.17763.1":[44.17763,44.17763]}

EDGE_CHROMIUM_VERSION = {"80.0":[80,80]}

SYSTEM_OS = platform.system()

AWSKEYWORDS=[]

line_separator = "======================================================================================================="

IMAGES_PATH = normpath(AVO_ASSURE_HOME + "/assets/images") + OS_SEP

os.environ["IMAGES_PATH"] = IMAGES_PATH

ICE_CONST = normpath(AVO_ASSURE_HOME + "/assets/ice_const.json")

MANIFEST_LOC = normpath(AVO_ASSURE_HOME + "/assets/about_manifest.json")

LOC_7Z = normpath(AVO_ASSURE_HOME + '/Lib/7zip/7z.exe')

UPDATER_LOC = normpath(AVO_ASSURE_HOME + '/assets/Update.exe')

CONFIG_PATH = normpath(AVO_ASSURE_HOME + "/assets/config.json")

PROXY_PATH= normpath(AVO_ASSURE_HOME + "/assets/proxy.json")

CERTIFICATE_PATH = normpath(AVO_ASSURE_HOME + "/assets/CA_BUNDLE")

LOGCONFIG_PATH = normpath(AVO_ASSURE_HOME + "/assets/logging.conf")

DRIVERS_PATH = normpath(AVO_ASSURE_HOME + "/lib/Drivers")

CHROME_DRIVER_PATH = DRIVERS_PATH + OS_SEP + "chromedriver"

GECKODRIVER_PATH = DRIVERS_PATH + OS_SEP + "geckodriver"

EDGE_DRIVER_PATH = DRIVERS_PATH + OS_SEP + "MicrosoftWebDriver.exe"

EDGE_CHROMIUM_DRIVER_PATH = DRIVERS_PATH + OS_SEP + "msedgedriver"

if SYSTEM_OS == "Windows":
    CHROME_DRIVER_PATH += ".exe"
    GECKODRIVER_PATH += ".exe"
    EDGE_CHROMIUM_DRIVER_PATH += ".exe"

if (os.path.exists(UPDATER_LOC[:-3] + "py")): UPDATER_LOC = UPDATER_LOC[:-3] + "py"

TEMP_PATH = AVO_ASSURE_HOME + OS_SEP + "output"

PREDICTION_IMG_DIR = "Disabled"

FILEPATH_OUTPUT_FIELD_KEYWORDS=["exportData","cellByCellCompare","getXmlBlockData","selectiveXmlFileCompare","compXmlFileWithXmlBlock","compareInputs","beautify","compareFiles","comparePDFs","findImageInPDF","selectiveCellCompare"]

VERIFY_KEYWORDS = ["dummyverifykeyword"]