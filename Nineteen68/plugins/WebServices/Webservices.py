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

"""Logger - File which prints the code loggers """
import Logger

"""request - requests is an elegant and simple HTTP library for Python to perform webservice operations"""
import requests

"""WSConstants - File consists of Webservice constants"""
import WSConstants

from requests import Request,Session

"""json - JSON (JavaScript Object Notation) is a lightweight data interchange format inspired by JavaScript object literal syntax """
import json

"""ast - The ast module helps Python applications to process trees of the Python abstract syntax grammar."""
import ast


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
        url=url.strip()
        if not (url is None or url is ''):

             self.baseEndPointURL = url
             return True
        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False


     def setOperations(self,operation):
        """
        def : setOperations
        purpose : sets the operation provided in param operation
        param operation : operation of the webservice to set
        return : Returns True if it sets the url else False

        """

        if type(operation) is 'str':
            operation=operation.strip()
        if not (operation is None or operation is ''):

             self.baseOperation = str(operation)
             return True
        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False

     def setMethods(self,method):
        """
        def : setMethods
        purpose : sets the method provided in param method
        param method : method of the webservice to set
        return : Returns True if it sets the url else False

        """

        method=method.strip().upper()

        if not (method is None or method is ''):
            if method in WSConstants.METHOD_ARRAY:

                self.baseMethod = method
                Logger.log("baseMethod is:"+self.baseMethod)
                return True
            else:
                Logger.log(WSConstants.METHOD_INVALID)
                return False

        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False

     def setHeader(self,header):
        """
        def : setHeader
        purpose : sets the header provided in param header
        param header : header of the webservice to set
        return : Returns True if it sets the url else False

        """

        header = str(header)
        if WSConstants.CONTENT_TYPE_JSON in header.lower() or WSConstants.CONTENT_TYPE_XML in header.lower() or WSConstants.CONTENT_TYPE_SOAP_XML in header.lower():
            header = ast.literal_eval(header)
            self.content_type=header['Content-Type']

##        header=header.strip()
        if not (header is None):
##             str=header.replace(' ','')

##             if WSConstants.TYPE_XML in str :
##                self.baseReqHeader = WSConstants.CONTENT_TYPE_XML
##             elif WSConstants.TYPE_JSON in str:
##                self.baseReqHeader = WSConstants.CONTENT_TYPE_JSON
##             elif WSConstants.TYPE_SOAP_XML in str:
##                self.baseReqHeader = WSConstants.CONTENT_TYPE_SOAP_XML
##             else:
                self.baseReqHeader = header

                print self.baseReqHeader
                return True
        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False

     def setWholeBody(self,body):
        """
        def : setWholeBody
        purpose : sets the body provided in param body
        param body : body of the webservice to set
        return : Returns True if it sets the url else False

        """

        if not (body is None or body is ''):

             self.baseReqBody = body
             return True
        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False

     def saveResults(self,response):

        Logger.log(response.status_code)
        self.baseResHeader=response.headers
        Logger.log(WSConstants.RESPONSE_HEADER+str(self.baseResHeader))
        self.baseResBody=response.content
        Logger.log(WSConstants.RESPONSE_BODY+str(self.baseResBody))



     def post(self):
        if  WSConstants.CONTENT_TYPE_JSON in self.content_type.lower():
            print type(self.baseReqBody)
            response = requests.post(self.baseEndPointURL,data = json.dumps(self.baseReqBody), headers=self.baseReqHeader)
##            response = requests.post(self.baseEndPointURL)
            WSkeywords.saveResults(self,response)
            return self.baseResHeader,self.baseResBody
        elif WSConstants.CONTENT_TYPE_XML in self.content_type.lower() or WSConstants.CONTENT_TYPE_SOAP_XML in self.content_type.lower():
##        baseReqHeader={'content-type': 'text/xml'}
            if not (self.baseEndPointURL is '' or self.baseReqBody is '' or self.baseReqHeader is ''):
                response = requests.post(self.baseEndPointURL,data=self.baseReqBody,headers=self.baseReqHeader)
                WSkeywords.saveResults(self,response)
                return self.baseResHeader,self.baseResBody
        else :
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return None

     def get(self):
        if  WSConstants.CONTENT_TYPE_JSON in self.content_type.lower():
            response=requests.get(self.baseEndPointURL)
            print response.content
            WSkeywords.saveResults(self,response)
            return self.baseResHeader,self.baseResBody
        else :
            if not (self.baseEndPointURL is '' or self.baseOperation is '' or self.baseReqHeader is ''):
                req=self.baseEndPointURL+'/'+self.baseOperation+'?'+self.baseReqHeader
                response=requests.get(req)
                WSkeywords.saveResults(self,response)
                return self.baseResHeader,self.baseResBody
            else :
                Logger.log(WSConstants.METHOD_INVALID_INPUT)
                return None

     def put(self):

         s=Session()
         if not (self.baseEndPointURL is '' or self.baseReqBody is '' or self.baseOperation is ''):
            reqUrl=self.baseEndPointURL+'/'+self.baseOperation
            req = requests.Request(method=self.baseMethod, url=reqUrl, data=self.baseReqBody)
            prep=req.prepare()
            response=s.send(prep)
            WSkeywords.saveResults(self,response)
            return self.baseResHeader,self.baseResBody
         else :
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return None

     def delete(self):
        s=Session()
        if not (self.baseEndPointURL is '' or self.baseOperation is ''):
            reqUrl=self.baseEndPointURL+'/'+self.baseOperation
            req = requests.Request(method=self.baseMethod, url=reqUrl)
            prep=req.prepare()
            response=s.send(prep)
            WSkeywords.saveResults(self,response)
            return self.baseResHeader,self.baseResBody
        else :
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return None

     def head(self):
        s=Session()
        if not (baseEndPointURL is '' or baseOperation is ''):
            reqUrl=self.baseEndPointURL+'/'+self.baseOperation
            req = requests.Request(method=self.baseMethod, url=reqUrl)
            prep=req.prepare()
            response=s.send(prep)
            self.baseResHeader=response.headers
            Logger.log(WSConstants.RESPONSE_HEADER+str(self.baseResHeader))
            return self.baseResHeader
        else :
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return None



     def executeRequest(self):

        dict={'GET':WSkeywords.get,
        'POST':WSkeywords.post,
        'PUT':WSkeywords.put,
        'HEAD':WSkeywords.head,
        'DELETE':WSkeywords.delete}
        print self.baseMethod
        if self.baseMethod in WSConstants.METHOD_ARRAY:
            return dict[self.baseMethod](self)
        else :
            Logger.log(WSConstants.METHOD_INVALID)



     def getHeader(self,*args):
        if len(args) == 0:
            Logger.log(WSConstants.RESULT+str(self.baseResHeader))
            print self.baseResHeader
            return self.baseResHeader
        elif len(args) == 1:
            key=args[0]
            Logger.log(WSConstants.RESULT+str(self.baseResHeader[key]))
            return self.baseResHeader[key]


     def getBody(self,*args):

        if len(args) == 0:
                Logger.log(WSConstants.RESULT+self.baseResBody)
                return self.baseResBody
        elif len(args) == 2:
            key=args[0]
            if not(self.baseResBody is None):
                str=self.baseResBody
                if not (args[0] is '' or args[1] is ''):
                    start=str.find(args[0])+len(args[0])
                    end=str.find(args[1])
                    str=str[start:end]
                    Logger.log(WSConstants.RESULT+str)
                    return str


     def addClientCertificate(self,filepath_key,filepath_cert,url):
        response=requests.get(url, cert=(filepath_cert, filepath_key))

     def setTagValue(self,tagname,tagvalue):
        if not (self.baseReqBody is None or self.baseReqBody is ''):
            from lxml import etree
            doc=etree.fromstring(self.baseReqBody)
            doc.find('.//'+tagname).text=tagvalue
            return True
        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False


     def getServerCertificate(self,url,filepath):
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

##            cert = ssl.get_server_certificate((hostname, 443), ssl_version=ssl.PROTOCOL_TLSv1)

            cert = ssl.get_server_certificate((hostname, int(str(port))))
            cert=str(cert)
            cert=cert.replace('\n','')

            with open(filepath, "w") as text_file:
                text_file.write(cert)
                text_file.close()
                return True
        else :
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False
