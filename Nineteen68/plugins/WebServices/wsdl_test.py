#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     19-09-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import pytest
import wsdlgenerator
import testdata

##for list of ops
##a=wsdlgenerator.WebservicesWSDL()
##test_data=[]
##data= testdata.message('http://www.webservicex.com/BibleWebservice.asmx?wsdl')

test_data=[]
##test_data=testdata.read_excel_data("asv")
data= testdata.message('http://www.webservicex.com/BibleWebservice.asmx?wsdl', 'GetBibleWordsByChapterAndVerse',2)
##test_param=[]
##test_param.append(data)
test_data.append(data)
##test_data.append('ChangePowerUnit')
##test_data.append(2)

@pytest.fixture(params=test_data)
def message(request):
        return request.param


    ## Verify if the request header is same
def test_listofmethod(message):
    b = wsdlgenerator.BodyGenarator(message.wsdl,message.operation_name,message.soap_type)
    assert b.requestHeader()=={'SOAPAction': '"http://www.webserviceX.NET/GetBibleWordsByChapterAndVerse"', 'Content-Type': 'text/xml; charset=utf-8'}
{'SOAPAction': '"http://www.webserviceX.NET/GetBibleWordsByChapterAndVerse"', 'Content-Type': 'application/soap+xml; charset=utf-8'}

##def req(message):
##    print message.wsdl
##    b = wsdlgenerator.BodyGenarator(message.wsdl,message.operation_name,message.soap_type)
##    assert b.requestHeader() == {'SOAPAction': '"http://www.webserviceX.NET/GetBibleWordsByChapterAndVerse"', 'Content-Type': 'text/xml; charset=utf-8'}
##{'SOAPAction': '"http://www.webserviceX.NET/GetBibleWordsByChapterAndVerse"', 'Content-Type': 'application/soap+xml; charset=utf-8'}

def listofmethod(message):
    assert str(a.listOfOperation(message))=="[ChangePowerUnit]"

def requestbody(message):
    b = wsdlgenerator.BodyGenarator(message.wsdl,message.operation_name,message.soap_type)
    assert b.requestBody() == """<soap-env:Envelope xmlns:ns0="http://www.webserviceX.NET" xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"><soap-env:Body><ns0:GetBibleWordsByChapterAndVerse><ns0:BookTitle>?</ns0:BookTitle><ns0:chapter>?</ns0:chapter><ns0:Verse>?</ns0:Verse></ns0:GetBibleWordsByChapterAndVerse></soap-env:Body></soap-env:Envelope>"

##<soap-env:Envelope xmlns:ns0="http://www.webserviceX.NET" xmlns:soap-env="http://www.w3.org/2003/05/soap-envelope">
##  <soap-env:Body>
##    <ns0:GetBibleWordsByChapterAndVerse>
##      <ns0:BookTitle>?</ns0:BookTitle>
##      <ns0:chapter>?</ns0:chapter>
##      <ns0:Verse>?</ns0:Verse>
##    </ns0:GetBibleWordsByChapterAndVerse>
##  </soap-env:Body>
##</soap-env:Envelope>




