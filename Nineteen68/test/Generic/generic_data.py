#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     04-10-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pytest
import xlrd
import os
import sys
import read_data_generic

os.chdir('..')
maindir = os.getcwd()
plug_path = maindir + '\Nineteen68\plugins\Generic'
sys.path.append(plug_path)
os.chdir(plug_path)

test_data=read_data_generic.read_excel_data(maindir + '\Nineteen68\\test\Generic' + '\generic.xls')
import generic_dispatcher
dispatcher_obj = generic_dispatcher.GenericKeywordDispatcher()

@pytest.fixture(params=test_data)
def message(request):
        print request.param
        return request.param

def test_generic_executor(message):

##    assert dispatcher_obj.dispatcher('getCurrentDate',message.input1)
##    assert dispatcher_obj.dispatcher('getCurrentTime',message.input1)
    assert dispatcher_obj.dispatcher('toLowerCase',message.input1)
##    assert dispatcher_obj.dispatcher('getCurrentDateAndTime',message.input1)
##    assert dispatcher_obj.dispatcher('dateDifference',message.input1, message.input2,message.input3)
##    assert dispatcher_obj.dispatcher('dateAddition',message.input1, message.input2,message.input3)
##    assert dispatcher_obj.dispatcher('changeDateFormat',message.input1, message.input2,message.input3)
##    assert dispatcher_obj.dispatcher('dateCompare',message.input1, message.input2,message.input3)
##    assert dispatcher_obj.dispatcher('concatenate',message.input1, message.input2)