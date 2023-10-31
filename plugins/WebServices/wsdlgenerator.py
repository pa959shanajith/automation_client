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
import os
import requests
from requests.auth import HTTPBasicAuth

try:
    from wsdllib_override import zeep
except ImportError:
    import zeep
global server_certs
auth_set= False
log = logging.getLogger('wsdlgenerator.py')

## This class will have the methods to generate request header and body of WSDL
class WebservicesWSDL():

    """This method takes 1 params
    1. WSDL url
    returns the operations present in WSDL
    """
    def listOfOperation(self,wsdlURL,import_def):
        try:
            self.wsdlURL = wsdlURL
            #list_method = Client(wsdlURL)
            base_url=wsdlURL.replace("?WSDL", "?op=")
            list_method = Client(wsdlURL, doctor=ImportDoctor(imp))
            allmethodslist=[]
            import_wsdl_definition={}
            import_wsdl_definition['CollectionName']=''
            import_wsdl_definition['APIS']=[]
            for portindex in range(0,len(list_method.wsdl.services[0].ports)):
                portname=list_method.wsdl.services[0].ports[portindex].name
                import_wsdl_definition['CollectionName']=list_method.wsdl.services[0].name
                obt_list_method = [method for method in list_method.wsdl.services[0].ports[portindex].methods]
                for methodindex in range(0,len(obt_list_method)):
                    # temp = {}
                    # temp['requestHeader']=''
                    # temp['requestBody']=''
                    if 'Soap12' in portname:
                        allmethodslist.append(str('SOAP1.2-'+obt_list_method[methodindex]))
                        if import_def:
                            temp={}
                            wsdl_object = BodyGenarator(self.wsdlURL,obt_list_method[methodindex],'1','','','','')
                            requestHeader = wsdl_object.requestHeader()
                            requestBody = wsdl_object.requestBody()
                            requestBody, requestHeader=self.beautify_req_header(requestHeader,requestBody)
                            # working
                            # import_wsdl_definition[str('SOAP1.2-'+obt_list_method[methodindex])]={'requestHeader':requestHeader, 'requestBody':requestBody, 'HTTPmethod':'POST'}
                            temp[str('SOAP1.2-'+obt_list_method[methodindex])]={'endPointURL':base_url+obt_list_method[methodindex],'requestHeader':requestHeader, 'requestBody':requestBody, 'HTTPmethod':'POST', 'operation':obt_list_method[methodindex]}
                            import_wsdl_definition['APIS'].append(temp)
                            # temp['requestHeader']=requestHeader
                            # temp['requestBody']=requestBody
                    elif 'Soap' in portname:
                        allmethodslist.append(str('SOAP1.1-'+obt_list_method[methodindex]))
                        if import_def:
                            temp={}
                            wsdl_object = BodyGenarator(self.wsdlURL,obt_list_method[methodindex],'0','','','','')
                            requestHeader = wsdl_object.requestHeader()
                            requestBody = wsdl_object.requestBody()
                            requestBody, requestHeader=self.beautify_req_header(requestHeader,requestBody)
                            # working
                            # import_wsdl_definition[str('SOAP1.1-'+obt_list_method[methodindex])]={'requestHeader':requestHeader, 'requestBody':requestBody, 'HTTPmethod':'POST'}
                            temp[str('SOAP1.1-'+obt_list_method[methodindex])]={'endPointURL':base_url+obt_list_method[methodindex],'requestHeader':requestHeader, 'requestBody':requestBody, 'HTTPmethod':'POST', 'operation':obt_list_method[methodindex]}
                            import_wsdl_definition['APIS'].append(temp)
                            # temp['requestHeader']=requestHeader
                            # temp['requestBody']=requestBody
                    else:
                        allmethodslist.append(str(obt_list_method[methodindex]))
                        if import_def:
                            temp={}
                            wsdl_object = BodyGenarator(self.wsdlURL,obt_list_method[methodindex],'2','','','','')
                            requestHeader = wsdl_object.requestHeader()
                            requestBody = wsdl_object.requestBody()
                            requestBody, requestHeader=self.beautify_req_header(requestHeader,requestBody)
                            # working
                            # import_wsdl_definition[str(obt_list_method[methodindex])]={'requestHeader':requestHeader, 'requestBody':requestBody, 'HTTPmethod':'POST'}
                            temp[str(obt_list_method[methodindex])]={'endPointURL':base_url+obt_list_method[methodindex],'requestHeader':requestHeader, 'requestBody':requestBody, 'HTTPmethod':'POST', 'operation':obt_list_method[methodindex]}
                            import_wsdl_definition['APIS'].append(temp)
                            # temp['requestHeader']=requestHeader
                            # temp['requestBody']=requestBody
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
            if import_def:
                log.info("List Of Operations:")
                log.info(import_wsdl_definition)
                # logger.print_on_console('List Of Operations:::::',import_wsdl_definition)
                return import_wsdl_definition
            else:
                log.info("List Of Operations:")
                log.info(allmethodslist)
                logger.print_on_console('List Of Operations:::::',allmethodslist)
                return allmethodslist
        except Exception as e:
            logger.print_on_console('Invalid end point URl')
            log.error(e)
            return "fail"
        
    def beautify_req_header(self,requestHeader,requestBody):
        from bs4 import BeautifulSoup
        requestBody = BeautifulSoup(requestBody, "xml").prettify()
        stringHeader=''
        if(requestHeader != None):
            for key in requestHeader:
                # logger.print_on_console(key,'==========',requestHeader[key])
                log.info(key)
                log.info(requestHeader[key])
                stringHeader = stringHeader + str(key) + ": " + str (requestHeader[key]) + "##"
        requestHeader = stringHeader
        return requestBody, requestHeader


class BodyGenarator():

    """ This constructor takes 3 params
    1. WSDL url
    2. Operation name which user selects
    3. soap_type i.e to which soap version request body and header needs to be generated(SOAP11 or SOAP12)
    It also creates object of client
    """
    def __init__(self, wsdl , operation_name , soap_type,serverCertificate,serverCerificate_pass,auth_uname,auth_pass):
        self.wsdl = str(wsdl)
        self.operation_name=str(operation_name)
        self.soap_type = int(soap_type)
        self.client_obj = zeep.Client(self.wsdl)
        self.client_obj.soaptype = None
        if not(serverCertificate=='' or serverCertificate==None or serverCerificate_pass=='' or serverCerificate_pass==None ) and  not(auth_uname=='' or auth_uname==None or auth_pass=='' or auth_pass==None):
            server_certs = self.server_certs(wsdl,operation_name,soap_type,serverCertificate,serverCerificate_pass,auth_uname,auth_pass)

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
            if auth_set==False:
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
            elif auth_set==True:
                test= self.client_obj.service._binding.create_message_header(self.operation_name)
                if type(server_certs) == tuple:
                    response=server_certs[0]
                response =server_certs
                logger.print_on_console('Status code: ',response.status_code)
                log.info('Status code: ')
                log.info(response.status_code)
                request_header_soap_auth_header=response.headers
                return request_header_soap_auth_header
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
            if auth_set ==False:
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
            elif (server_certs!='' or server_certs!=None):
                import xml.etree.ElementTree as ET
                if type(server_certs) == tuple:
                    response=server_certs[0]
                response =server_certs
                logger.print_on_console('Status code: ',response.status_code)
                log.info('Status code: ')
                log.info(response.status_code)
                rep_content= str(response.content).replace("&gt;",">").replace("&lt;","<")
                res_status_code=response.status_code
                request_header_soap_auth_body=(str(res_status_code),rep_content.replace("&gt;",">").replace("&lt;","<"))
                return request_header_soap_auth_body
        except Exception as e:
            logger.print_on_console('Invalid end point url')
            log.error(e)

    def server_certs(self,wsdl , operation_name, soap_type, serverCertificate,serverCerificate_pass,auth_uname,auth_pass):
        trust_cert_path=None
        import readconfig
        proxies_val = readconfig.proxies
        import webservices as w
        obj=w.WSkeywords()
        if (not(auth_uname == '' or auth_uname == None) and not(auth_pass == '' or auth_pass == None)):
            auth_pass = obj.aes_decript(auth_pass)
            if (not(serverCertificate== '' or serverCertificate==None) and not(serverCerificate_pass=='' or serverCerificate_pass==None)):
                serverCerificate_pass =obj.aes_decript(serverCerificate_pass)
                trust_cert= obj.extract_jks(serverCertificate,serverCerificate_pass.encode('utf-8'))
                if trust_cert:
                    trust_cert_path = os.environ["AVO_ASSURE_HOME"]+'\\TRUSTSTORECERT.pem'
                    resp = requests.get(wsdl, auth=HTTPBasicAuth(auth_uname, auth_pass),verify=trust_cert_path,proxies=proxies_val)
                    status_code = resp.status_code
            else:
                resp = requests.get(wsdl, verify=False,auth=HTTPBasicAuth(auth_uname, auth_pass),proxies=proxies_val)
                status_code = resp.status_code
        else:
            if (not(serverCertificate== '' or serverCertificate==None) and not(serverCerificate_pass=='' or serverCerificate_pass==None)):
                serverCerificate_pass =obj.aes_decript(serverCerificate_pass)
                trust_cert= obj.extract_jks(serverCertificate,serverCerificate_pass.encode('utf-8'))
                if trust_cert:
                    trust_cert_path = os.environ["AVO_ASSURE_HOME"]+'\\TRUSTSTORECERT.pem'
                    resp = requests.get(wsdl, verify=trust_cert_path,proxies=proxies_val)
                    status_code = resp.status_code
            else:
                resp = requests.get(wsdl, verify=False,proxies=proxies_val)
                status_code = resp.status_code
        auth_set= True
        return resp
