#-------------------------------------------------------------------------------
# Name:        module3
# Purpose:
#
# Author:      rakesh.v
#
# Created:     27-10-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pytest
import os
import sys


os.chdir('..')
maindir = os.getcwd()
plug_path = maindir + '\Nineteen68\plugins\Generic'
sys.path.append(plug_path)
os.chdir(plug_path)


##test_data=readexcel_filefolder.read_excel_data(maindir + '\Nineteen68\\test\Generic' + '\generic.xls')
import generic_dispatcher
dispatcher_obj =  generic_dispatcher.GenericKeywordDispatcher()


def test_generic_executor():


    assert dispatcher_obj.dispatcher('runQuery','10.44.10.54','1433','version20_test','version2.0_Test','Version20_TestDB',"select * from Persons",'4')
    assert dispatcher_obj.dispatcher('getData','10.44.10.54','1433','version20_test','version2.0_Test','Version20_TestDB',"select * from Persons",'4')
##    assert dispatcher_obj.exportData(maindir + '\Nineteen68\\test\Generic' + '\generic.xls','Sheet4')
##    assert dispatcher_obj.verifyData(maindir + '\Nineteen68\\test\Generic' + '\generic.xls','Sheet5')
