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
import os
import sys


os.chdir('..')
maindir = os.getcwd()
plug_path = maindir + '\Nineteen68\plugins\WebServices'
sys.path.append(plug_path)
os.chdir(plug_path)

import dispatcher
import testdata_xml

dispatcher_obj = dispatcher.Dispatcher()
test_data=testdata_xml.read_excel_data(maindir + '\Nineteen68\\test\WebServices' + '\Webservice_Keywords.xlsx')



@pytest.fixture(params=test_data)
def message(request):
        print request.param
        return request.param





def test_Webservice_executor(message):

    #verify whether the endPointUrl is set or not
    """set the endpoint URL"""
    assert dispatcher_obj.dispatcher('setEndPointURL',message.url)
##    assert WSobj.setEndPointURL(message.url)

    #verify whether the method is set or not
    """set the Method"""
    assert dispatcher_obj.dispatcher('setMethods',message.method)
##    assert WSobj.setMethods(message.method)

    #verify whether the operation is set or not
    """set the setOperations"""
    assert dispatcher_obj.dispatcher('setOperations',message.operation)
##    assert WSobj.setOperations(message.operation)

    #verify whether the header is set or not
    """set the Header"""
    assert dispatcher_obj.dispatcher('setHeader',message.header)
##    assert WSobj.setHeader(message.header)

    #verify whether the body is set or not
    """set the Body"""
    assert dispatcher_obj.dispatcher('setWholeBody',message.body)
##    assert WSobj.setWholeBody(message.body)

    #executes the request and verifies the header and response
    """Execute the request"""
    assert dispatcher_obj.dispatcher('executeRequest')
##    assert WSobj.executeRequest()

    #verfies the response header
    """Get the header"""
    assert dispatcher_obj.dispatcher('getHeader')
##    assert WSobj.getHeader()
##
    #verfies the response body
    """Get the getBody"""
    assert dispatcher_obj.dispatcher('getBody')

##    assert WSobj.getBody()

     #get server certificate
##    print message.url
##    print message.filepath
##    assert WSobj.getServerCertificate(message.url,message.filepath)



