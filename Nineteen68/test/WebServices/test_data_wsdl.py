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
import wsdl_test_data
import os
import sys

curpath = os.getcwd()
os.chdir('..')
os.chdir('..')
basepath = os.getcwd()
basepath = basepath +'\plugins\WebServices'
sys.path.append(basepath)
import wsdlgenerator

test_data=wsdl_test_data.read_excel_data(curpath + '\wsdl.xlsx')

@pytest.fixture(params=test_data)
def message(request):
        return request.param


def test_requestbody(message):
    a=wsdlgenerator.BodyGenarator(message.wsdl, message.operation_name, message.soap_type)
    a.requestBody()
    a.requestHeader()
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
    assert a.requestBody() == message.expected_body
    assert a.requestHeader() == message.expected_header



