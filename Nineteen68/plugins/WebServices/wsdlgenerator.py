#-------------------------------------------------------------------------------
# Name:        wsdlgenerator.py
# Purpose:		listing the wsdl operations
#				generating services provided
#
# Author:      rakesh.v
#
# Created:     19-09-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#
# Author:      vishvas.a
#
# Modified:     27-04-2017
# Copyright:   (c) vishvas.a 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor
imp=Import('http://www.w3.org/2001/XMLSchema',location='http://www.w3.org/2001/XMLSchema.xsd')
imp.filter.add('http://tempuri.org/')
from lxml import etree
import logger
import logging
try:
    from wsdllib_override import zeep
except ImportError:
    import zeep

log = logging.getLogger('wsdlgenerator.py')

## This class will have the methods to generate request header and body of WSDL
class WebservicesWSDL():

    """This method takes 1 params
    1. WSDL url
    returns the operations present in WSDL
    """
    def listOfOperation(self,wsdlURL):
        try:
            self.wsdlURL = wsdlURL
            #list_method = Client(wsdlURL)
            list_method = Client(wsdlURL, doctor=ImportDoctor(imp))
            allmethodslist=[]
            for portindex in range(0,len(list_method.wsdl.services[0].ports)):
                portname=list_method.wsdl.services[0].ports[portindex].name
                obt_list_method = [method for method in list_method.wsdl.services[0].ports[portindex].methods]
                for methodindex in range(0,len(obt_list_method)):
                    if 'Soap12' in portname:
                        allmethodslist.append(str('SOAP1.2-'+obt_list_method[methodindex]))
                    elif 'Soap' in portname:
                        allmethodslist.append(str('SOAP1.1-'+obt_list_method[methodindex]))
                    else:
                        allmethodslist.append(str(obt_list_method[methodindex]))
            ##print list_method.wsdl.services[0].ports[0].name
            ##    obt_list_method = [method for method in list_method.wsdl.services[0].ports[0].methods]
            ##    obt_list_method1 = [method for method in list_method.wsdl.services[0].ports[1].methods]
            ##    log.info('List of methods obtained')
            ##    print obt_list_method
            ##    print obt_list_method1
            ##    for methodindex in range(0,len(obt_list_method)):
            ##       allmethodslist.append(str('SOAP1.1-'+obt_list_method[methodindex]))
            ##    for methodindex in range(0,len(obt_list_method1)):
            ##       allmethodslist.append(str('SOAP1.2-'+obt_list_method[methodindex]))
            ##    log.info(allmethodslist)
            return allmethodslist
        except Exception as e:
            logger.print_on_console('Invalid end point URl')
            log.error(e)
            return "fail"


class BodyGenarator():

    """ This constructor takes 3 params
    1. WSDL url
    2. Operation name which user selects
    3. soap_type i.e to which soap version request body and header needs to be generated(SOAP11 or SOAP12)
    It also creates object of client
    """
    def __init__(self, wsdl , operation_name , soap_type):
        self.wsdl = str(wsdl)
        self.operation_name=str(operation_name)
        self.soap_type = int(soap_type)
        self.client_obj = zeep.Client(self.wsdl)
        self.client_obj.soaptype = None

    def get_string(self ,count):
        str=[]
        for i in range(count):
            str.append('?')
        return str

    """requestHeader method generates header based on
    a. operation name
    b. soaptype
    returns request header
    """
    def requestHeader(self):
        try:
            if self.soap_type == 0:
                self.client_obj.soaptype = 0
                log.info('soap type is 0 i.e is soap 11')
                request_header_soap11 = self.client_obj.service._binding.create_message_header(self.operation_name)
                ##request_header_soap11 = str(request_header_soap11)
                log.info('request header of soap11')
                log.info(request_header_soap11)
                return request_header_soap11
            elif self.soap_type == 1:
                self.client_obj.soaptype = 1
                log.info('soap type is 1 i.e is soap 12')
                request_header_soap12 = self.client_obj.service._binding.create_message_header(self.operation_name)
                ##request_header_soap12 = str(request_header_soap12)
                log.info('request header of soap12')
                log.info(request_header_soap12)
                return request_header_soap12
            elif self.soap_type == 2:
                self.client_obj.soaptype = 0
                request_header_soap11 = self.client_obj.service._binding.create_message_header(self.operation_name)
                request_header_soap11 = str(request_header_soap11)
                log.info('request header of soap11')
                log.info(request_header_soap11)
                self.client_obj.soaptype = 1
                request_header_soap12 = self.client_obj.service._binding.create_message_header(self.operation_name)
                ##request_header_soap12 = str(request_header_soap12)
                log.info('request header of soap12')
                log.info(request_header_soap12)
                return request_header_soap11,request_header_soap12
        except Exception as e:
            logger.print_on_console('Invalid end point url')
            log.error(e)



    """ requestBody method generates header based on
    a. operation name
    b. soaptype
    returns request body
    """
    def requestBody(self):
        try:
            if self.soap_type == 0:
                self.client_obj.soaptype = 0
                log.info('soap type is 0 i.e is soap 11')
                obt_body_base = self.client_obj.service._binding.create_message(self.operation_name)
                obt_body_base = etree.tostring(obt_body_base,pretty_print=True)
                inp_count = zeep.xsd.indicators.inputParameterCount
                args=self.get_string(inp_count)
                try:
                    obt_body = self.client_obj.service._binding.create_message(self.operation_name,*args)
                    obt_request_body_soap11 = etree.tostring(obt_body,pretty_print=True)
                except:
                    logger.print_on_console('No Request data to Enter')
                    obt_request_body_soap11 = obt_body_base
                log.info('request body of soap11')
                log.info(obt_request_body_soap11)
                return obt_request_body_soap11

            elif self.soap_type == 1:
                self.client_obj.soaptype = 1
                log.info('soap type is 1 i.e is soap 12')
                obt_body_base = self.client_obj.service._binding.create_message(self.operation_name)
                obt_body_base = etree.tostring(obt_body_base,pretty_print=True)
                inp_count = zeep.xsd.indicators.inputParameterCount
                args=self.get_string(inp_count)
                try:
                    obt_body = self.client_obj.service._binding.create_message(self.operation_name,*args)
                    obt_request_body_soap12 = etree.tostring(obt_body,pretty_print=True)
                except:
                    logger.print_on_console('No Request data to Enter')
                    obt_request_body_soap12 = obt_body_base
                log.info('request body of soap12')
                log.info(obt_request_body_soap12)
                return obt_request_body_soap12

            elif self.soap_type == 2:
                self.client_obj.soaptype = 0
                obt_body_base1 = self.client_obj.service._binding.create_message(self.operation_name)
                obt_body_base1 = etree.tostring(obt_body_base1,pretty_print=True)
                inp_count = zeep.xsd.indicators.inputParameterCount
                args=self.get_string(inp_count)
                obt_body = self.client_obj.service._binding.create_message(self.operation_name,*args)
                try:
                    obt_body = self.client_obj.service._binding.create_message(self.operation_name,*args)
                    obt_request_body_soap11 = etree.tostring(obt_body,pretty_print=True)
                except:
                    logger.print_on_console('No Request data to Enter')
                    obt_request_body_soap11 = obt_body_base1
                log.info('request body of soap11')
                log.info(obt_request_body_soap11)

                self.client_obj.soaptype = 1
                obt_body_base2 = self.client_obj.service._binding.create_message(self.operation_name)
                try:
                    obt_body = self.client_obj.service._binding.create_message(self.operation_name,*args)
                    obt_request_body_soap12 = etree.tostring(obt_body,pretty_print=True)
                except:
                    logger.print_on_console('No Request data to Enter')
                    obt_request_body_soap12 = obt_body_base2
                log.info('request body of soap12')
                log.info(obt_request_body_soap12)
                return obt_request_body_soap11,obt_request_body_soap12
        except Exception as e:
            logger.print_on_console('Invalid end point url')
            log.error(e)
