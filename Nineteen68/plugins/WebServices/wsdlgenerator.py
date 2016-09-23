#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rakesh.v
#
# Created:     19-09-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import zeep
from suds.client import Client
import zeep.xsd.indicators
from lxml import etree
import logger

## This class will have the methods to generate request header and body of WSDL
class WebservicesWSDL():

##  This method takes 1 params
##  1. WSDL url
##  returns the operations present in WSDL

    def listOfOperation(self,wsdlURL):
        try:
            self.wsdlURL = wsdlURL
            list_method = Client(wsdlURL)
            obt_list_method = [method for method in list_method.wsdl.services[0].ports[0].methods]
            logger.log(obt_list_method)
            return obt_list_method
        except Exception:
            logger.log('exception occured')


class BodyGenarator():

##  This constructor takes 3 params
##  1. WSDL url
##  2. Operation name which user selects
##  3. soap_type i.e to which soap version request body and header needs to be generated(SOAP11 or SOAP12)
##  4. It also creates object of client
    def __init__(self, wsdl , operation_name , soap_type):
        self.wsdl = wsdl
        self.operation_name=operation_name
        self.soap_type = soap_type
        self.client_obj = zeep.Client(self.wsdl)

    def get_string(self ,count):
        str=[]
        for i in range(count):
            str.append('?')
        return str


## 1. requestHeader method generates header based on
## a. operation name
## b. soaptype
## returns request header
    def requestHeader(self):
        try:
            if self.soap_type == 0:
                self.client_obj.soaptype = 0
                request_header_soap11 = self.client_obj.service._binding.create_message_header(self.operation_name)
                request_header_soap11 = str(request_header_soap11)
                logger.log(request_header_soap11)
                return request_header_soap11
            elif self.soap_type == 1:
                self.client_obj.soaptype = 1
                request_header_soap12 = self.client_obj.service._binding.create_message_header(self.operation_name)
                request_header_soap12 = str(request_header_soap12)
                logger.log(request_header_soap12)
                return request_header_soap12
            elif self.soap_type == 2:
                self.client_obj.soaptype = 0
                request_header_soap11 = self.client_obj.service._binding.create_message_header(self.operation_name)
                request_header_soap11 = str(request_header_soap11)
                logger.log(request_header_soap11)
                self.client_obj.soaptype = 1
                request_header_soap12 = self.client_obj.service._binding.create_message_header(self.operation_name)
                request_header_soap12 = str(request_header_soap12)
                logger.log(request_header_soap12)
                return request_header_soap11,request_header_soap12
        except Exception:
            logger.log('Exception occured')


## 1. requestBody method generates header based on
## a. operation name
## b. soaptype
## returns request body
    def requestBody(self):
        try:
            if self.soap_type == 0:
                self.client_obj.soaptype = 0
                self.client_obj.service._binding.create_message(self.operation_name)
                inp_count = zeep.xsd.indicators.inputParameterCount
                args=self.get_string(inp_count)
                obt_body = self.client_obj.service._binding.create_message(self.operation_name,*args)
                obt_request_body_soap11 = etree.tostring(obt_body,pretty_print=True)
                logger.log(obt_request_body_soap11)
                return obt_request_body_soap11

            elif self.soap_type == 1:
                self.client_obj.soaptype = 1
                self.client_obj.service._binding.create_message(self.operation_name)
                inp_count = zeep.xsd.indicators.inputParameterCount
                args=self.get_string(inp_count)
                obt_body_soap12 = self.client_obj.service._binding.create_message(self.operation_name,*args)
                obt_request_body_soap12 = etree.tostring(obt_body_soap12,pretty_print=True)
                logger.log(obt_request_body_soap12)
                return obt_request_body_soap12

            elif self.soap_type == 2:
                self.client_obj.soaptype = 0
                self.client_obj.service._binding.create_message(self.operation_name)
                inp_count = zeep.xsd.indicators.inputParameterCount
                args=self.get_string(inp_count)
                obt_body = self.client_obj.service._binding.create_message(self.operation_name,*args)
                obt_request_body_soap11 = etree.tostring(obt_body,pretty_print=True)
                logger.log(obt_request_body_soap11)
                self.client_obj.soaptype = 1
                self.client_obj.service._binding.create_message(self.operation_name)
                obt_body_soap12 = self.client_obj.service._binding.create_message(self.operation_name,*args)
                obt_request_body_soap12 = etree.tostring(obt_body_soap12,pretty_print=True)
                logger.log(obt_request_body_soap12)
                return obt_request_body_soap11,obt_request_body_soap12
        except Exception:
            logger.log('Exception occured')



##clsobject = WebservicesWSDL()
##clsobject.listOfOperation('http://www.webservicex.net/ConverPower.asmx?wsdl')
##clsobject.requestBody('http://www.webservicex.net/ConverPower.asmx?wsdl','ChangePowerUnit',0)
##clsobject = WebservicesWSDL()
##clsobject.listOfOperation('http://www.webservicex.com/BibleWebservice.asmx?wsdl')
##re = BodyGenarator('http://www.webservicex.com/BibleWebservice.asmx?wsdl','GetBibleWordsByChapterAndVerse',1)
##abc = re.requestHeader()
##xyz = re.requestBody()
##http://www.webservicex.net/ConverPower.asmx?wsdl
##http://www.webservicex.com/BibleWebservice.asmx?wsdl



