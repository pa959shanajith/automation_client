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
import outlook
import xlrd
import testdata
##  Unit  test to test outlook keywords
##class outlooktestcase():

##a=outlook.OutlookKeywords()
test_data=testdata.read_excel_data("C:\Users\prudhvi.gujjuboyina\Documents\pytest\Email Keywords.xlsx")
##message=testdata.message
##for message in test_data:
##    print message


@pytest.fixture(params=test_data)
##@pytest.mark.parametrize("frommail,subject,toMail",test_data )
def message(request):
        return request.param


    ## Verify if the email has been fetched successfully or not. Parameters are: "From" email ID, "Subject" and "To" email ID.
def test_outlook_GetEmail(message):
    a=outlook.OutlookKeywords(message.fromMail, message.subject,  message.toMail)
    assert a.GetEmail()
    assert a.VerifyEmail("C:\Users\prudhvi.gujjuboyina\Desktop\Unit Testing Status - Email  Keywords.msg")
    assert a.GetFromMailId() == message.fromMail_exp
    assert a.GetSubject() == message.subject_exp
    assert a.GetToMailID() == message.toMail_exp
    assert a.GetAttachmentStatus()== message.GetAttachmentStatus_exp




   ##
##        print "Printing the data of row:", row
##      print fromMail,fromMail_exp,subject,subject_exp,toMail,toMail_exp

