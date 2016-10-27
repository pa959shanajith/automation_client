#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     27-10-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pytest
import os
import sys
import readexcel_filefolder

os.chdir('..')
maindir = os.getcwd()
plug_path = maindir + '\Nineteen68\plugins\Generic'
sys.path.append(plug_path)
os.chdir(plug_path)

##test_data=readexcel_filefolder.read_excel_data(maindir + '\Nineteen68\\test\Generic' + '\generic.xls')
print '---------------',os.getcwd()
import generic_dispatcher
dispatcher_obj = generic_dispatcher.GenericKeywordDispatcher()


##@pytest.fixture(params=test_data)
##def message(request):
##        print request.param
##        return request.param

def test_generic_executor():


    assert dispatcher_obj.dispatcher('evaluate','(3*3)+(3/2)')
    assert dispatcher_obj.dispatcher('evalLogicalExpression','(3*3)>=(3/2)')
    assert dispatcher_obj.dispatcher('captureScreenshot','D:/Screenshots/')
    assert dispatcher_obj.dispatcher('executeFile','C:\Users\prudhvi.gujjuboyina\Desktop\run.vbs')

