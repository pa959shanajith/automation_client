#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      vidya.baduru
#
# Created:     15-09-2016
# Copyright:   (c) vidya.baduru 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import pytest
import xlrd
import testdata_xml
import os
import sys

curpath = os.getcwd()
os.chdir('..')
os.chdir('..')
basepath = os.getcwd()
basepath = basepath +'\plugins\WebServices'
sys.path.append(basepath)

import Dispatcher

dispatcher = Dispatcher.Dispatcher()
test_data=testdata_xml.read_excel_data(curpath + '\Webservice_Keywords.xlsx')



@pytest.fixture(params=test_data)
def message(request):
        print request.param
        return request.param





def test_Webservice_executor(message):

    #verify whether the endPointUrl is set or not
    """set the endpoint URL"""
    assert dispatcher.dispatcher('setEndPointURL',message.url)
##    assert WSobj.setEndPointURL(message.url)

    #verify whether the method is set or not
    """set the Method"""
    assert dispatcher.dispatcher('setMethods',message.method)
##    assert WSobj.setMethods(message.method)

    #verify whether the operation is set or not
    """set the setOperations"""
    assert dispatcher.dispatcher('setOperations',message.operation)
##    assert WSobj.setOperations(message.operation)

    #verify whether the header is set or not
    """set the Header"""
    assert dispatcher.dispatcher('setHeader',message.header)
##    assert WSobj.setHeader(message.header)

    #verify whether the body is set or not
    """set the Body"""
    assert dispatcher.dispatcher('setWholeBody',message.body)
##    assert WSobj.setWholeBody(message.body)

    #executes the request and verifies the header and response
    """Execute the request"""
    assert dispatcher.dispatcher('executeRequest')
##    assert WSobj.executeRequest()

    #verfies the response header
    """Get the header"""
    assert dispatcher.dispatcher('getHeader')
##    assert WSobj.getHeader()
##
    #verfies the response body
    """Get the getBody"""
    assert dispatcher.dispatcher('getBody')

##    assert WSobj.getBody()

     #get server certificate
##    print message.url
##    print message.filepath
##    assert WSobj.getServerCertificate(message.url,message.filepath)



