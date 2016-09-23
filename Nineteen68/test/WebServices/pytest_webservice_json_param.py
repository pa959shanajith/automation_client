#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     20-09-2016
# Copyright:   (c) wasimakram.sutar 2016
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
import testdata_json

dispatcher_obj = dispatcher.Dispatcher()
test_data=testdata_json.read_excel_data(maindir + '\Nineteen68\\test\WebServices' + '\Restful_jsonWebService_Keywords.xlsx')

@pytest.fixture(params=test_data)
def message(request):
        print request.param
        return request.param

def test_webservice_execute(message):
    """set the endpoint URL"""
    assert dispatcher_obj.dispatcher('setEndPointURL',message.endpoint_url)
##    assert a.setEndPointURL(message.endpoint_url)
    """set the Method"""
    assert dispatcher_obj.dispatcher('setMethods',message.method)
##    assert a.setMethods(message.method)
    """set the Header"""
    assert dispatcher_obj.dispatcher('setHeader',message.header)
##    assert a.setHeader(message.header)
    """set the Body"""
    assert dispatcher_obj.dispatcher('setWholeBody',message.body)
##    assert a.setWholeBody(message.body)
    """Execute the request"""
    assert dispatcher_obj.dispatcher('executeRequest')
##    assert a.executeRequest()
    """Get the header"""
    assert dispatcher_obj.dispatcher('getHeader')

##    assert a.getHeader()


