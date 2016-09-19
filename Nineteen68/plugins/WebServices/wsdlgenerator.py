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
        self.wsdlURL = wsdlURL
        list_method = Client(wsdlURL)
        obt_list_method = [method for method in list_method.wsdl.services[0].ports[0].methods]
        logger.log(obt_list_method)
        return obt_list_method

    def get_string(self ,count):
        str=[]
        for i in range(count):
            str.append('?')
        return str



##  This method takes 3 params
##  1. WSDL url
##  2. Operation name which user selects
##  3. soap_type i.e to which soap version request body and header needs to be generated(SOAP11 or SOAP12)
##  4. returns request header and body


    def requestBody(self, wsdlURL , operation_name , soap_type):
        self.wsdlURL = wsdlURL
        self.operation_name = operation_name
        self.soap_type = soap_type
        client_obj = zeep.Client(wsdlURL)
        if soap_type == 0:
            client_obj.soaptype = 0
            client_obj.service._binding.create_message(operation_name)
            inp_count = zeep.xsd.indicators.inputParameterCount
            args=self.get_string(inp_count)
            obt_body = client_obj.service._binding.create_message(operation_name,*args)
            obt_request_body_soap11 = etree.tostring(obt_body,pretty_print=True)
            logger.log(obt_request_body_soap11)
            request_header_soap11 = client_obj.service._binding.create_message_header(operation_name)
            logger.log(request_header_soap11)

        elif soap_type == 1:
            client_obj.soaptype = 1
            client_obj.service._binding.create_message(operation_name)
            inp_count = zeep.xsd.indicators.inputParameterCount
            args=self.get_string(inp_count)
            obt_body_soap12 = client_obj.service._binding.create_message(operation_name,*args)
            obt_request_body_soap12 = etree.tostring(obt_body_soap12,pretty_print=True)
            logger.log(obt_request_body_soap12)
            request_header_soap12 = client_obj.service._binding.create_message_header(operation_name)
            logger.log(request_header_soap12)

        elif soap_type == 2 :
            client_obj.soaptype = 0
            client_obj.service._binding.create_message(operation_name)
            inp_count = zeep.xsd.indicators.inputParameterCount
            args=self.get_string(inp_count)
            obt_body = client_obj.service._binding.create_message(operation_name,*args)
            obt_request_body_soap11 = etree.tostring(obt_body,pretty_print=True)
            logger.log(obt_request_body_soap11)
            request_header_soap11 = client_obj.service._binding.create_message_header(operation_name)
            logger.log(request_header_soap11)
            client_obj.soaptype = 1
            client_obj.service._binding.create_message(operation_name)
            obt_body_soap12 = client_obj.service._binding.create_message(operation_name,*args)
            obt_request_body_soap12 = etree.tostring(obt_body_soap12,pretty_print=True)
            logger.log(obt_request_body_soap12)
            request_header_soap12 = client_obj.service._binding.create_message_header(operation_name)
            logger.log(request_header_soap12)




clsobject = WebservicesWSDL()
clsobject.listOfOperation('http://www.webservicex.net/ConverPower.asmx?wsdl')
##clsobject.requestBody('http://www.webservicex.net/ConverPower.asmx?wsdl','ChangePowerUnit',0)

##http://www.webservicex.net/ConverPower.asmx?wsdl
##http://www.webservicex.com/BibleWebservice.asmx?wsdl



