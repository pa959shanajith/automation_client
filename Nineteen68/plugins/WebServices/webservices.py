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
import Exceptions

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
        try:
            url=url.strip()
            if not (url is None or url is ''):
                 self.baseEndPointURL = url
                 status = ws_constants.TEST_RESULT_PASS
                 methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                logger.log(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

     def setOperations(self,operation):
        """
        def : setOperations
        purpose : sets the operation provided in param operation
        param operation : operation of the webservice to set
        return : Returns True if it sets the url else False

        """
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        try:
            if type(operation) is str:
                operation=operation.strip()
            if not (operation is None or operation is ''):
                 self.baseOperation = str(operation)
                 status = ws_constants.TEST_RESULT_PASS
                 methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                logger.log(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

     def setMethods(self,method):
        """
        def : setMethods
        purpose : sets the method provided in param method
        param method : method of the webservice to set
        return : Returns True if it sets the url else False
        """
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        try:
            if not (method is None or method is ''):
            	method=method.strip().upper()
                if method in ws_constants.METHOD_ARRAY:
                    self.baseMethod = method
                    logger.log("baseMethod is:"+self.baseMethod)
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
                else:
                    logger.log(ws_constants.METHOD_INVALID)
            else:
                logger.log(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

     def setHeaderTemplate(self,header):
        """
        def : setHeader
        purpose : sets the header provided in param header
        param header : header of the webservice to set
        return : Returns True if it sets the url else False
        """
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        try:
            self.setHeader(header)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput


     def setHeader(self,header):
        """
        def : setHeader
        purpose : sets the header provided in param header
        param header : header of the webservice to set
        return : Returns True if it sets the url else False
        """
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        try:
            if not(header is None and header is ''):
                header = str(header).replace('\n','').replace("'",'')
                header=header.split('##')
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
                    logger.log(header_dict)
                    if 'Content-Type' in header_dict.keys():
                        self.content_type=header_dict['Content-Type']
                else:
                    self.baseReqHeader=header[0]
                status = ws_constants.TEST_RESULT_PASS
                methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                logger.log(ws_constants.METHOD_INVALID_INPUT)

        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

     def setWholeBody(self,body):
        """
        def : setWholeBody
        purpose : sets the body provided in param body
        param body : body of the webservice to set
        return : Returns True if it sets the url else False

        """
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        if not (body is None or body is ''):
             self.baseReqBody = body
             status = ws_constants.TEST_RESULT_PASS
             methodoutput = ws_constants.TEST_RESULT_TRUE
        else:
            logger.log(ws_constants.METHOD_INVALID_INPUT)
        return status,methodoutput


     def __saveResults(self,response):
        logger.log(response.status_code)
        self.baseResHeader=response.headers
        #added status code
        self.baseResHeader['StatusCode']=response.status_code
        logger.log(ws_constants.RESPONSE_HEADER+str(self.baseResHeader))
        self.baseResBody=response.content
        logger.log(ws_constants.RESPONSE_BODY+str(self.baseResBody))
        status = ws_constants.TEST_RESULT_PASS
        methodoutput = ws_constants.TEST_RESULT_TRUE
        output=(self.baseResHeader,self.baseResBody)
        return status,methodoutput,output

     def post(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
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
                logger.log(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput,output

     def get(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        output=None
        try:
            if not (self.baseEndPointURL is '' or self.baseOperation is '' or self.baseReqHeader is ''):
                print self.baseReqHeader
                req=self.baseEndPointURL+'/'+self.baseOperation+'?'+self.baseReqHeader
            elif not (self.baseEndPointURL is ''):
                req=self.baseEndPointURL
            response=requests.get(req)
            status,methodoutput,output=self.__saveResults(response)

        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput,output

     def put(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        output=None
        try:
             s=Session()
             if not (self.baseEndPointURL is '' or self.baseReqBody is '' or self.baseOperation is ''):
                reqUrl=self.baseEndPointURL+'/'+self.baseOperation
                req = requests.Request(method=self.baseMethod, url=reqUrl, data=self.baseReqBody)
                prep=req.prepare()
                response=s.send(prep)
                status,methodoutput,output=self.__saveResults(response)
             else:
                logger.log(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput,output

     def delete(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
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
                logger.log(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput,output

     def head(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        output=None
        try:
            s=Session()

            if not (self.baseEndPointURL is '' or self.baseOperation is ''):
                reqUrl=self.baseEndPointURL+'/'+self.baseOperation
                req = requests.Request(method=self.baseMethod, url=reqUrl)
                prep=req.prepare()
                response=s.send(prep)
                self.baseResHeader=response.headers
                logger.log(ws_constants.RESPONSE_HEADER+str(self.baseResHeader))
                status = ws_constants.TEST_RESULT_PASS
                methodoutput = ws_constants.TEST_RESULT_TRUE
                output= self.baseResHeader
            else:
                logger.log(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput,output

     def executeRequest(self,*args):

        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        dict={'GET':WSkeywords.get,
        'POST':WSkeywords.post,
        'PUT':WSkeywords.put,
        'HEAD':WSkeywords.head,
        'DELETE':WSkeywords.delete}
        if self.baseMethod in ws_constants.METHOD_ARRAY:
            return dict[self.baseMethod](self)
        else:
            logger.log(ws_constants.METHOD_INVALID)
            return status,methodoutput

     def getHeader(self,*args):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        output=None
        try:
            if len(args) == 1:
                key=args[0]
                if key!= None and key != '':
                    logger.log(ws_constants.RESULT+str(self.baseResHeader[key]))
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
                    output=self.baseResHeader[key]
                else:
                    logger.log(ws_constants.RESULT+str(self.baseResHeader))
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
                    output=self.baseResHeader

        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput,output


     def getBody(self,*args):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        output=None
        try:
            if len(args) == 1:
                    logger.log(ws_constants.RESULT+self.baseResBody)
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
                        logger.log(ws_constants.RESULT+response_body)
                        status = ws_constants.TEST_RESULT_PASS
                        methodoutput = ws_constants.TEST_RESULT_TRUE
                        output=response_body
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput,output


     def addClientCertificate(self,filepath_key,filepath_cert,url):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        try:
            response=requests.get(url, cert=(filepath_cert, filepath_key))
            status = ws_constants.TEST_RESULT_PASS
            methodoutput = ws_constants.TEST_RESULT_TRUE
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput

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
            logger.log('Element not found')
        return result

     def setAttributeValue(self,attribute_name,attribute_value,element_path):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        import handler
        if self.baseReqBody == '':
            self.baseReqBody=handler.ws_template
        try:
            if not (self.baseReqBody is None or self.baseReqBody is ''):
                result=self.parse_xml(self.baseReqBody,element_path,attribute_value,attribute_name,'attribute')
                if result != None:
                    self.baseReqBody=result
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                logger.log(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput


     def setTagValue(self,value,element_path):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        import handler
        if self.baseReqBody == '':
            self.baseReqBody=handler.ws_template
        try:
            if not (self.baseReqBody is None or self.baseReqBody is ''):
                result=self.parse_xml(self.baseReqBody,element_path,value,'','tagname')
                if result != None:
                    self.baseReqBody=result
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                logger.log(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)
        return status,methodoutput


     def getServerCertificate(self,url,filepath):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
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
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                logger.log(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            Exceptions.error(e)

        return status,methodoutput

