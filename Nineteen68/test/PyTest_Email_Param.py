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
import os
import sys
import xlrd
##curdir  = os.curdir()
os.chdir('..')
maindir = os.getcwd()
plug_path = maindir + '\Nineteen68\plugins\Outlook'
sys.path.append(plug_path)
os.chdir(plug_path)
import outlook
import testdata
import dispatcher
##  Unit  test to test outlook keywords
##class outlooktestcase():

##a=outlook.OutlookKeywords()
test_path = maindir + '\Nineteen68\\test'
test_data=testdata.read_excel_data(test_path+"\Email Keywords.xlsx")
##message=testdata.message
##for message in test_data:
##    print message


@pytest.fixture(params=test_data)
##@pytest.mark.parametrize("frommail,subject,toMail",test_data )
def message(request):
        return request.param


    ## Verify if the email has been fetched successfully or not. Parameters are: "From" email ID, "Subject" and "To" email ID.
def test_outlook_GetEmail(message):
##    a=outlook.OutlookKeywords(message.fromMail, message.subject,  message.toMail)
    a=dispatcher.Dispatcher()
    assert a.dispatcher('GetEmail',message.fromMail, message.toMail, message.subject )
    assert a.dispatcher('GetFromMailId')==message.fromMail_exp
    assert a.dispatcher('GetToMailID')==message.toMail_exp
    assert a.dispatcher('GetSubject')==message.subject_exp
    assert a.dispatcher('GetAttachmentStatus')==message.GetAttachmentStatus_exp
    assert a.dispatcher('VerifyEmail',message.File_Loc)







   ##
##        print "Printing the data of row:", row
##      print fromMail,fromMail_exp,subject,subject_exp,toMail,toMail_exp

