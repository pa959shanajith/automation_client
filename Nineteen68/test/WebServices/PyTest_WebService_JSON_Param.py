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
import testdata_json
import sys
import os

curpath = os.getcwd()
os.chdir('..')
os.chdir('..')
basepath = os.getcwd()
basepath = basepath +'\plugins\WebServices'
sys.path.append(basepath)

import Dispatcher

dispatcher = Dispatcher.Dispatcher()
test_data=testdata_json.read_excel_data(curpath +'\Restful_jsonWebService_Keywords.xlsx')

@pytest.fixture(params=test_data)
def message(request):
        print request.param
        return request.param

def test_webservice_execute(message):
    """set the endpoint URL"""
    assert dispatcher.dispatcher('setEndPointURL',message.endpoint_url)
##    assert a.setEndPointURL(message.endpoint_url)
    """set the Method"""
    assert dispatcher.dispatcher('setMethods',message.method)
##    assert a.setMethods(message.method)
    """set the Header"""
    assert dispatcher.dispatcher('setHeader',message.header)
##    assert a.setHeader(message.header)
    """set the Body"""
    assert dispatcher.dispatcher('setWholeBody',message.body)
##    assert a.setWholeBody(message.body)
    """Execute the request"""
    assert dispatcher.dispatcher('executeRequest')
##    assert a.executeRequest()
    """Get the header"""
    assert dispatcher.dispatcher('getHeader')
##    assert a.getHeader()


