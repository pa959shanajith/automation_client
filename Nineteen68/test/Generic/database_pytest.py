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
import database_keywords
dispatcher_obj = database_keywords.DatabaseOperation('4','10.44.10.54','1433','Version20_TestDB','version20_test','version2.0_Test',"select * from Persons")

def test_generic_executor():


    assert dispatcher_obj.runQuery()
    assert dispatcher_obj.getData()
    assert dispatcher_obj.exportData(maindir + '\Nineteen68\\test\Generic' + '\generic.xls','Sheet4')
    assert dispatcher_obj.verifyData(maindir + '\Nineteen68\\test\Generic' + '\generic.xls','Sheet5')


