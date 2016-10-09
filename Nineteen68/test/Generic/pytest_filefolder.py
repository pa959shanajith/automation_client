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
import readexcel_filefolder

os.chdir('..')
maindir = os.getcwd()
plug_path = maindir + '\Nineteen68\plugins\Generic'
sys.path.append(plug_path)
os.chdir(plug_path)

test_data=readexcel_filefolder.read_excel_data(maindir + '\Nineteen68\\test\Generic' + '\generic.xls')
import generic_dispatcher
dispatcher_obj = generic_dispatcher.GenericKeywordDispatcher()
@pytest.fixture(params=test_data)
def message(request):
        print request.param
        return request.param

def test_generic_executor(message):

##    assert dispatcher_obj.dispatcher('createFile',message.inputpath1)
## assert dispatcher_obj.dispatcher('renameFile',message.inputpath1,message.inputpath2)
##    assert dispatcher_obj.dispatcher('verifyFileExists',message.inputpath1)
####    assert dispatcher_obj.dispatcher('deleteFile',message.inputpath1)
##    assert dispatcher_obj.dispatcher('verifyFileExists',message.inputpath1)
##    assert dispatcher_obj.dispatcher('createFolder',message.inputpath1)
##    assert dispatcher_obj.dispatcher('verifyFolderExists',message.inputpath1)
##    assert dispatcher_obj.dispatcher('renameFolder',message.inputpath1,message.inputpath2)
####    assert dispatcher_obj.dispatcher('deleteFolder',message.inputpath1)
####    assert dispatcher_obj.dispatcher('deleteFolder',message.inputpath1,message.forcedelete)
    assert dispatcher_obj.dispatcher('compareContent',message.inputpath1,message.inputpath2)
##    assert dispatcher_obj.dispatcher('verifyContent',message.inputpath1,message.content)
##    assert dispatcher_obj.dispatcher('writeToFile',message.inputpath1,message.content)
##    assert dispatcher_obj.dispatcher('getLineNumber',message.inputpath1,message.content)
##    assert dispatcher_obj.dispatcher('replaceContent',message.inputpath1,message.existingcontent,message.replacecontent)
##    assert dispatcher_obj.dispatcher('getContent',message.inputpath1)
####    assert dispatcher_obj.dispatcher('clearFileContent',message.inputpath1)




