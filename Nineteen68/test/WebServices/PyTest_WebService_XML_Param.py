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


import pytest
import Webservices
import xlrd
import testdata_xml

curpath = os.getcwd()
os.chdir('..')
os.chdir('..')
basepath = os.getcwd()
basepath = basepath +'\plugins\WebServices'
sys.path.append(basepath)

import Webservices

WSobj=Webservices.WSkeywords()
test_data=testdata_xml.read_excel_data(curpath + '\Webservice Keywords.xlsx')



@pytest.fixture(params=test_data)
def message(request):
        print request.param
        return request.param





def test_Webservice_executor(message):

    #verify whether the endPointUrl is set or not
    assert WSobj.setEndPointURL(message.url)

    #verify whether the method is set or not
    assert WSobj.setMethods(message.method)

    #verify whether the operation is set or not
    assert WSobj.setOperations(message.operation)

    #verify whether the header is set or not
    assert WSobj.setHeader(message.header)

    #verify whether the body is set or not
    assert WSobj.setWholeBody(message.body)

    #executes the request and verifies the header and response
    assert WSobj.executeRequest()

    #verfies the response header
    assert WSobj.getHeader()
##
    #verfies the response body
    assert WSobj.getBody()

     #get server certificate
##    print message.url
##    print message.filepath
##    assert WSobj.getServerCertificate(message.url,message.filepath)



