#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     05-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import pytest
import xlrd
import os
import sys
##import readexcel_filefolder

os.chdir('..')
maindir = os.getcwd()
plug_path = maindir + '\Nineteen68\plugins\Oebs'
sys.path.append(plug_path)
os.chdir(plug_path)

##test_data=readexcel_filefolder.read_excel_data(maindir + '\Nineteen68\\test\Generic' + '\generic.xls')
import oebs_dispatcher
dispatcher_obj = oebs_dispatcher.OebsDispatcher()
##@pytest.fixture(params=test_data)
##def message(request):
##        print request.param
##        return request.param

def test_generic_executor():


    assert dispatcher_obj.dispatcher('findwindowandattach','Oracle Applications - Tiger')
    xpath="""frame[Oracle Applications - Tiger]/panel[1]/panel[1]/scroll pane[0]/viewport[0]/desktop pane[0]/internal frame[Transaction Batches (Progress FR: EUR)]/panel[0]/scroll pane[2]/viewport[0]/panel[0]/scroll pane[0]/viewport[0]/panel[0]/text[Source RequiredList of Values];Source RequiredList of Values;1;0;;frame[Oracle Applications - Tiger]/panel[1]/panel[1]/scroll pane[0]/viewport[0]/desktop pane[0]/internal frame[Transaction Batches (Progress FR: EUR)]/panel[0]/scroll pane[2]/viewport[0]/panel[0]/scroll pane[0]/viewport[0]/panel[0];19;0;panel;text;Source RequiredList of Values"""

    assert dispatcher_obj.dispatcher('settext','Oracle Applications - Tiger',xpath,'settext',['sushma'],'')
    assert dispatcher_obj.dispatcher('gettext','Oracle Applications - Tiger',xpath,'gettext',['sushma'],'res')





