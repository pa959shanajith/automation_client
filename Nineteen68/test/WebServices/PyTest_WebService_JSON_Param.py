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

import Webservices

a = Webservices.WSkeywords()
test_data=testdata_json.read_excel_data(curpath +'\Restful_jsonWebService Keywords.xlsx')

@pytest.fixture(params=test_data)
def message(request):
        print request.param
        return request.param

def test_webservice_execute(message):
    """set the endpoint URL"""
    assert a.setEndPointURL(message.endpoint_url)
    """set the Method"""
    assert a.setMethods(message.method)
    """set the Header"""
    assert a.setHeader(message.header)
    """Execute the request"""
    assert a.executeRequest()
    """Execute the request"""
    assert a.getHeader()


