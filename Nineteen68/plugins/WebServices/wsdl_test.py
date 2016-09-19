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
import wsdlgenerator

a=wsdlgenerator.WebservicesWSDL()

test_data=[]
test_data.append('http://www.webservicex.net/ConverPower.asmx?wsdl')
test_data.append('ChangePowerUnit')
test_data.append(2)

@pytest.fixture(params=test_data)
##@pytest.mark.parametrize("frommail,subject,toMail",test_data )
def message(request):
        print request.param
        return request.param


    ## Verify if the email has been fetched successfully or not. Parameters are: "From" email ID, "Subject" and "To" email ID.
def test_listofmethod(message):
    assert str(a.listOfOperation(message))=="[ChangePowerUnit]"

##def req(message):
##    assert


