#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     16-09-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

METHOD_GET='GET'

METHOD_POST='POST'

METHOD_PUT='PUT'

METHOD_DELETE='DELETE'

METHOD_HEAD='HEAD'

METHOD_PATCH='PATCH'

METHOD_LINK='LINK'

METHOD_UNLINK='UNLINK'

METHOD_PURGE='PURGE'

METHOD_COPY='COPY'

METHOD_LOCK='LOCK'

METHOD_UNLOCK='UNLOCK'

METHOD_OPTIONS='OPTIONS'

METHOD_VIEW='VIEW'

METHOD_PROPFIND='PROPFIND'


METHOD_INVALID_INPUT='Invalid Input'

METHOD_INVALID='Invalid Method'

METHOD_ARRAY=[METHOD_GET,METHOD_POST,METHOD_PUT,METHOD_HEAD,METHOD_DELETE, METHOD_PATCH,
                METHOD_COPY, METHOD_LINK, METHOD_UNLINK, METHOD_LOCK, METHOD_UNLOCK, METHOD_OPTIONS,
                METHOD_PROPFIND, METHOD_PURGE, METHOD_VIEW]

RESPONSE_HEADER='Response header is:'

RESPONSE_BODY='Response body is:'

RESULT='Result is:'

CONTENT_TYPE_XML = 'text/xml';

CONTENT_TYPE_JSON = 'application/json'

CONTENT_TYPE_SOAP_XML = 'application/soap+xml'

ERR_MSG1='Error occurred in '

ERR_SET_WHOLE_BODY='Invalid input : Whole Body is invalid or missing.'

ERR_SET_PARAMS='Invalid input : Invalid Request Parameters'

ERR_SET_TAG_VALUE='Request body is empty'

ERR_AUTH_COMPONENT_MISSING = 'Invalid Input: Authentication component missing'

ERR_INVALID_FILE = 'Invalid Input: Issue with file path.'

##TYPE_XML="""Content-Type:text/xml;"""
##
##TYPE_JSON="""Content-Type:application/json;"""
##
##TYPE_SOAP_XML="""Content-Type:application/soap+xml;"""

TEST_RESULT_PASS = "Pass"

TEST_RESULT_FAIL = "Fail"

TEST_RESULT_TRUE = "True"

TEST_RESULT_FALSE = "False"

COOKIES = "Requested Cookie is"




