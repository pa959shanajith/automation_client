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
test_path = maindir + '\Nineteen68\\test\Outlook'
os.chdir(test_path)
test_data=testdata.read_excel_data(test_path+"\Email Keywords.xlsx")

@pytest.fixture(params=test_data)
def message(request):
        return request.param



def test_outlook_GetEmail(message):
    a=dispatcher.Dispatcher()
    assert a.dispatcher('GetEmail',message.fromMail, message.toMail, message.subject )
    assert a.dispatcher('GetFromMailId')==message.fromMail_exp
    assert a.dispatcher('GetToMailID')==message.toMail_exp
    assert a.dispatcher('GetSubject')==message.subject_exp
    assert a.dispatcher('GetAttachmentStatus')==message.GetAttachmentStatus_exp
    assert a.dispatcher('VerifyEmail',message.File_Loc)







