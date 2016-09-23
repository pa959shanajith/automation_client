#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      rakesh.v
#
# Created:     20-09-2016
# Copyright:   (c) rakesh.v 2016
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
import wsdlgenerator
import wsdl_test_data

test_data=wsdl_test_data.read_excel_data(maindir + '\Nineteen68\\test\WebServices' + '\wsdl.xlsx')

@pytest.fixture(params=test_data)
def message(request):
        return request.param

def test_requestbody(message):
    a=wsdlgenerator.BodyGenarator(message.wsdl, message.operation_name, message.soap_type)
    assert(a.requestBody(),message.expected_body)

def test_requestheader(message):
    a=wsdlgenerator.BodyGenarator(message.wsdl, message.operation_name, message.soap_type)
    assert(a.requestHeader(),message.expected_header)


##    a.requestBody()
##    a.requestHeader()
##    assert a.requestBody() == message.expected_body
##    assert a.requestHeader() == message.expected_header

##    body= """<soap-env:Envelope xmlns:ns0="http://www.webserviceX.NET" xmlns:soap-env="http://www.w3.org/2003/05/soap-envelope">
##      <soap-env:Body>
##        <ns0:GetBibleWordsByChapterAndVerse>
##          <ns0:BookTitle>?</ns0:BookTitle>
##          <ns0:chapter>?</ns0:chapter>
##          <ns0:Verse>?</ns0:Verse>
##        </ns0:GetBibleWordsByChapterAndVerse>
##      </soap-env:Body>
##    </soap-env:Envelope>"""

##    head = {'SOAPAction': '"http://www.webserviceX.NET/GetBibleWordsByChapterAndVerse"', 'Content-Type': 'application/soap+xml; charset=utf-8'}

