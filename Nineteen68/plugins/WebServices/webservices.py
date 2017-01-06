#-------------------------------------------------------------------------------
# Name:        Webservices.py
# Purpose:     Keywords for XML on SOA and RestfulJSON
#
# Author:      sushma.p and wasimakram.sutar
#
# Created:     08-09-2016
# Copyright:   (c) sushma.p wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

"""logger - File which prints the code loggers """
import logger

"""request - requests is an elegant and simple HTTP library for Python to perform webservice operations"""
import requests

"""ws_constants - File consists of Webservice constants"""
import ws_constants

from requests import Request,Session

"""json - JSON (JavaScript Object Notation) is a lightweight data interchange format inspired by JavaScript object literal syntax """
import json

"""ast - The ast module helps Python applications to process trees of the Python abstract syntax grammar."""
import ast


from lxml import etree


import logging
from constants import *

log = logging.getLogger('webservices.py')
class WSkeywords:

     """The instantiation operation __init__ creates an empty object of the class WSkeywords when it is instantiated"""

     def __init__(self):
        self.baseEndPointURL=''
        self.baseOperation=''
        self.baseMethod=''
        self.baseReqHeader= ''
        self.baseReqBody=''
        self.baseResHeader = ''
        self.baseResBody=''
        self.modifiedTemplate = ''
        self.verify=''
        self.content_type=''


     def setEndPointURL(self,url):
        """
        def : setEndPointURL
        purpose : sets the endpoint url provided in param url
        param url : url of the webservice to set
        return : Returns True if it sets the url else False

        """
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            url=url.strip()
            if not (url is None or url is ''):
                 self.baseEndPointURL = url
                 log.debug('End point URL is set')
                 logger.print_on_console('End point URL ',url , 'has been set')
                 log.info(STATUS_METHODOUTPUT_UPDATE)
                 status = ws_constants.TEST_RESULT_PASS
                 methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                log.info(ERROR_CODE_DICT['ERR_INVALID_END_POINT_URL'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_END_POINT_URL']
                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_END_POINT_URL'])
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

     def setOperations(self,operation):
        """
        def : setOperations
        purpose : sets the operation provided in param operation
        param operation : operation of the webservice to set
        return : Returns True if it sets the url else False

        """
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if type(operation) is str:
                log.debug('Removing leading and trailing spaces from operation')
                operation=operation.strip()
                log.debug('Removed leading and trailing spaces from operation')
            if not (operation is None or operation is ''):
                 log.debug('Setting base operation name with the input operation name')
                 self.baseOperation = str(operation)
                 log.info('Base operation name has been set to input operation name')
                 logger.print_on_console('Base operation name has been set to: ',operation)
                 log.info(STATUS_METHODOUTPUT_UPDATE)
                 status = ws_constants.TEST_RESULT_PASS
                 methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                log.info(ERROR_CODE_DICT['ERR_INVALID_OPERATION'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_OPERATION']
                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_OPERATION'])
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

     def setMethods(self,method):
        """
        def : setMethods
        purpose : sets the method provided in param method
        param method : method of the webservice to set
        return : Returns True if it sets the url else False
        """
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if not (method is None or method is ''):
                log.debug('Removing leading and trailing spaces from method name and converting it to uppercase')
            	method=method.strip().upper()
                log.debug('Removed leading and trailing spaces from method name and converting it to uppercase')
                if method in ws_constants.METHOD_ARRAY:
                    log.debug('Setting input method name to base method name ')
                    self.baseMethod = method
                    log.info('Base method name has been set to input method name')
                    logger.print_on_console('Base method name has been set to: ',method)
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
                else:
                    log.info(ERROR_CODE_DICT['ERR_INVALID_METHOD'])
                    err_msg = ERROR_CODE_DICT['ERR_INVALID_METHOD']
                    logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_METHOD'])
            else:
                log.info(ERROR_CODE_DICT['ERR_INVALID_METHOD'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_METHOD']
                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_METHOD'])
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

     def setHeaderTemplate(self,header):
        """
        def : setHeader
        purpose : sets the header provided in param header
        param header : header of the webservice to set
        return : Returns True if it sets the url else False
        """
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if not (method is None or method is ''):
                log.debug('Setting the input header template to Header ')
                self.setHeader(header)
                log.info('Input header template has been set ')
                log.info(STATUS_METHODOUTPUT_UPDATE)
                status = ws_constants.TEST_RESULT_PASS
                methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                log.info(ERROR_CODE_DICT['ERR_INVALID_HEADER'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_HEADER']
                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_HEADER'])
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg


     def setHeader(self,header):
        """
        def : setHeader
        purpose : sets the header provided in param header
        param header : header of the webservice to set
        return : Returns True if it sets the url else False
        """
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if not(header is None and header is ''):
                header = str(header).replace('\n','').replace("'",'')
                log.info('Removed new line and single quote from the input header')
                header=header.split('##')
                log.info('Header is split with ##')
                header_dict={}
                if self.baseReqHeader is not None and isinstance(self.baseReqHeader,dict):
                    header_dict=self.baseReqHeader
                #to support update of header multiple times
                for x in header:
                    if ':' in x:
                        index=x.index(':')
                        header_dict[x[0:index].strip()]=x[index+1:].strip()
                if len(header_dict) !=0:
                    self.baseReqHeader=header_dict
                    log.info(header_dict)
                    if 'Content-Type' in header_dict.keys():
                        self.content_type=header_dict['Content-Type']
                else:
                    self.baseReqHeader=header[0]
                log.info('Header is set')
                log.info(STATUS_METHODOUTPUT_UPDATE)
                status = ws_constants.TEST_RESULT_PASS
                methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                log.info(ERROR_CODE_DICT['ERR_INVALID_HEADER'])
                err_msg = ERROR_CODE_DICT['ERR_INVALID_HEADER']
                logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_HEADER'])

        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

     def setWholeBody(self,body):
        """
        def : setWholeBody
        purpose : sets the body provided in param body
        param body : body of the webservice to set
        return : Returns True if it sets the url else False

        """
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if not (body is None or body is ''):
                 self.baseReqBody = body
                 log.info('Input body has been set to base Request body ')
                 log.info(STATUS_METHODOUTPUT_UPDATE)
                 status = ws_constants.TEST_RESULT_PASS
                 methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                log.info(ws_constants.METHOD_INVALID_INPUT)
                err_msg = ws_constants.METHOD_INVALID_INPUT
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg


     def __saveResults(self,response):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        output=None
        try:
            logger.print_on_console('Status code: ',response.status_code)
            log.info('Status code: ')
            log.info(response.status_code)
            self.baseResHeader=response.headers
            #added status code
            self.baseResHeader['StatusCode']=response.status_code
            logger.print_on_console(ws_constants.RESPONSE_HEADER,str(self.baseResHeader))
            self.baseResBody=response.content
            logger.print_on_console(ws_constants.RESPONSE_BODY,str(self.baseResBody))
            log.info(STATUS_METHODOUTPUT_UPDATE)
            status = ws_constants.TEST_RESULT_PASS
            methodoutput = ws_constants.TEST_RESULT_TRUE
            output=(self.baseResHeader,self.baseResBody)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output

     def post(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        output=None
        try:
            if  ws_constants.CONTENT_TYPE_JSON in self.content_type.lower():
                response = requests.post(self.baseEndPointURL,data = json.dumps(self.baseReqBody), headers=self.baseReqHeader)
                status,methodoutput,output=self.__saveResults(response)
            elif ws_constants.CONTENT_TYPE_XML in self.content_type.lower() or ws_constants.CONTENT_TYPE_SOAP_XML in self.content_type.lower():
                if not (self.baseEndPointURL is '' or self.baseReqBody is '' or self.baseReqHeader is ''):
                    response = requests.post(self.baseEndPointURL,data=self.baseReqBody,headers=self.baseReqHeader)
                    status,methodoutput,output=self.__saveResults(response)
            else:
                log.info(ws_constants.METHOD_INVALID_INPUT)
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output

     def get(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        output=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if not (self.baseEndPointURL is '' or self.baseOperation is '' or self.baseReqHeader is ''):
                print self.baseReqHeader
                req=self.baseEndPointURL+'/'+self.baseOperation+'?'+self.baseReqHeader
            elif not (self.baseEndPointURL is ''):
                req=self.baseEndPointURL
            response=requests.get(req)
            logger.print_on_console('Response: ',response)
            log.info(response)
            status,methodoutput,output=self.__saveResults(response)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output

     def put(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        output=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
             s=Session()
             if not (self.baseEndPointURL is '' or self.baseReqBody is '' or self.baseOperation is ''):
                reqUrl=self.baseEndPointURL+'/'+self.baseOperation
                req = requests.Request(method=self.baseMethod, url=reqUrl, data=self.baseReqBody)
                prep=req.prepare()
                response=s.send(prep)
                status,methodoutput,output=self.__saveResults(response)
             else:
                log.info(ws_constants.METHOD_INVALID_INPUT)
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output

     def delete(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        output=None
        try:
            s=Session()
            if not (self.baseEndPointURL is '' or self.baseOperation is ''):
                reqUrl=self.baseEndPointURL+'/'+self.baseOperation
                req = requests.Request(method=self.baseMethod, url=reqUrl)
                prep=req.prepare()
                response=s.send(prep)
                status,methodoutput,output=self.__saveResults(response)
            else:
                log.info(ws_constants.METHOD_INVALID_INPUT)
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output

     def head(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        output=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            s=Session()

            if not (self.baseEndPointURL is '' or self.baseOperation is ''):
                reqUrl=self.baseEndPointURL+'/'+self.baseOperation
                req = requests.Request(method=self.baseMethod, url=reqUrl)
                prep=req.prepare()
                response=s.send(prep)
                self.baseResHeader=response.headers
                logger.print_on_console(ws_constants.RESPONSE_HEADER,str(self.baseResHeader))
                output= self.baseResHeader
                log.info(STATUS_METHODOUTPUT_UPDATE)
                status = ws_constants.TEST_RESULT_PASS
                methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                log.info(ws_constants.METHOD_INVALID_INPUT)
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output

     def executeRequest(self,*args):

        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        dict={'GET':WSkeywords.get,
        'POST':WSkeywords.post,
        'PUT':WSkeywords.put,
        'HEAD':WSkeywords.head,
        'DELETE':WSkeywords.delete}
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        if self.baseMethod in ws_constants.METHOD_ARRAY:
            log.info(STATUS_METHODOUTPUT_UPDATE)
            status = ws_constants.TEST_RESULT_PASS
            methodoutput = ws_constants.TEST_RESULT_TRUE
            return dict[self.baseMethod](self)
        else:
            log.info(ERROR_CODE_DICT['ERR_INVALID_METHOD'])
            err_msg = ERROR_CODE_DICT['ERR_INVALID_METHOD']
            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_METHOD'])
            return status,methodoutput,output,err_msg

     def getHeader(self,*args):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if len(args) == 1:
                key=args[0]
                if key!= None and key != '':
                    logger.print_on_console(ws_constants.RESULT,str(self.baseResHeader[key]))
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
                    output=self.baseResHeader[key]
                else:
                    logger.print_on_console(ws_constants.RESULT,str(self.baseResHeader))
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
                    output=self.baseResHeader
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg


     def getBody(self,*args):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        err_msg=None
        output=None
        try:
            if len(args) == 1:
                    logger.print_on_console(ws_constants.RESULT,self.baseResBody)
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
                    output= self.baseResBody
            elif len(args) == 2:
                key=args[0]
                if not(self.baseResBody is None):
                    response_body=self.baseResBody
                    if not (args[0] is '' or args[1] is ''):
                        start=response_body.find(args[0])+len(args[0])
                        end=response_body.find(args[1])
                        response_body=response_body[start:end]
                        logger.print_on_console(ws_constants.RESULT,response_body)
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = ws_constants.TEST_RESULT_PASS
                        methodoutput = ws_constants.TEST_RESULT_TRUE
                        output=response_body
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg


     def addClientCertificate(self,filepath_key,filepath_cert,url):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            response=requests.get(url, cert=(filepath_cert, filepath_key))
            log.info(STATUS_METHODOUTPUT_UPDATE)
            status = ws_constants.TEST_RESULT_PASS
            methodoutput = ws_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

     def parse_xml(self,input_xml,path,value,attribute_name,flag):
        result=None
        from lxml import etree
        doc=etree.fromstring(self.baseReqBody)
        namespaces={}
        xyz={}

        for ns in doc.xpath('//namespace::*'):
            namespaces[ns[0]]=ns[1]

        new_path=path.split('/')
        new_path= new_path[1:]
        for x in new_path:
            x=x.split(':')
            xyz[x[0]]=namespaces[x[0]]
        element=doc.xpath(path,namespaces=xyz)
        if len(element)>0:
            element=element[0]
            if flag=='tagname':
                element.text=value
            elif flag=='attribute':
                element.attrib[attribute_name]=value
            result=etree.tostring(doc,pretty_print=True)
        else:
            logger.print_on_console('Element not found')
        return result

     def setAttributeValue(self,attribute_name,attribute_value,element_path):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        import handler
        if self.baseReqBody == '':
            self.baseReqBody=handler.ws_template
        try:
            if not (self.baseReqBody is None or self.baseReqBody is ''):
                result=self.parse_xml(self.baseReqBody,element_path,attribute_value,attribute_name,'attribute')
                if result != None:
                    self.baseReqBody=result
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                log.info(ws_constants.METHOD_INVALID_INPUT)
                err_msg = ws_constants.METHOD_INVALID_INPUT
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg


     def setTagValue(self,value,element_path):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        import handler
        if self.baseReqBody == '':
            self.baseReqBody=handler.ws_template
        try:
            if not (self.baseReqBody is None or self.baseReqBody is ''):
                result=self.parse_xml(self.baseReqBody,element_path,value,'','tagname')
                if result != None:
                    self.baseReqBody=result
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                log.info(ws_constants.METHOD_INVALID_INPUT)
                err_msg = ws_constants.METHOD_INVALID_INPUT
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            log.error(e)

            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg


     def getServerCertificate(self,url,filepath):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            import ssl
            import re
            url=url.strip()
            if not(url is None or url is '' or filepath is None or filepath is ''):
                p = '(?:https.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
                m = re.search(p,url)
                hostname=m.group('host')
                port=m.group('port')
                if str(port) is '':
                    port=443
                cert = ssl.get_server_certificate((hostname, int(str(port))))
                cert=str(cert)
                cert=cert.replace('\n','')
                with open(filepath, 'w') as text_file:
                    text_file.write(cert)
                    text_file.close()
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                log.info(ws_constants.METHOD_INVALID_INPUT)
                err_msg = ws_constants.METHOD_INVALID_INPUT
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
           log.error(e)

           logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

