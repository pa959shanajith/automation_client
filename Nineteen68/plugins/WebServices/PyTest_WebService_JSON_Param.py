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

##import PyTest_Email_ReadData
import pytest
import Webservices
import xlrd
import testdata2
##  Unit  test to test outlook keywords
##class outlooktestcase():

##a=outlook.OutlookKeywords()
a = Webservices.WSkeywords()
test_data=testdata2.read_excel_data("D:\Code Snippets - Python\Restful_jsonWebService Keywords.xlsx")
##message=testdata.message
##for message in test_data:
##    print message


@pytest.fixture(params=test_data)
##@pytest.mark.parametrize("frommail,subject,toMail",test_data )
def message(request):
        print request.param
        return request.param


    ## Verify if the email has been fetched successfully or not. Parameters are: "From" email ID, "Subject" and "To" email ID.
def test_webservice_execute(message):
##    assert a.GetEmail(message.fromMail, message.subject, message.toMail)
    """set the endpoint URL"""
    assert a.setEndPointURL(message.endpoint_url)
    """set the Method"""
    assert a.setMethods(message.method)
    """set the Header"""
    assert a.setHeader(message.header)
    """Execute the request"""
    assert a.executeRequest()


