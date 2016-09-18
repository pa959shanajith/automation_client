#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     08-09-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import Logger
import requests
import WSConstants
from requests import Request,Session


class WSkeywords:




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


     def setEndPointURL(self,url):
        url=url.strip()
        if not (url is None or url is ''):

             self.baseEndPointURL = url
             return True
        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False


     def setOperations(self,operation):

        operation=operation.strip()
        if not (operation is None or operation is ''):

             self.baseOperation = operation
             return True
        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False

     def setMethods(self,method):

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

        header=header.strip()
        if not (header is None or header is ''):
             str=header.replace(' ','')

             if WSConstants.TYPE_XML in str :
                self.baseReqHeader = WSConstants.CONTENT_TYPE_XML
             elif WSConstants.TYPE_JSON in str:
                self.baseReqHeader = WSConstants.CONTENT_TYPE_JSON
             elif WSConstants.TYPE_SOAP_XML in str:
                self.baseReqHeader = WSConstants.CONTENT_TYPE_SOAP_XML
             else:
                self.baseReqHeader = header

             print self.baseReqHeader
             return True
        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False

     def setWholeBody(self,body):

        if not (body is None or body is ''):

             self.baseReqBody = body
             return True
        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False

     def saveResults(self,response):

        self.baseResHeader=response.headers
        Logger.log(WSConstants.RESPONSE_HEADER+str(self.baseResHeader))
        self.baseResBody=response.content
        Logger.log(WSConstants.RESPONSE_BODY+str(self.baseResBody))



     def post(self):
        if self.baseReqHeader == WSConstants.CONTENT_TYPE_JSON:
            response = requests.post(self.baseEndPointURL)
            print response.content
            WSkeywords.saveResults(self,response)
            return self.baseResHeader,self.baseResBody
        elif self.baseReqHeader == WSConstants.CONTENT_TYPE_XML:
##        baseReqHeader={'content-type': 'text/xml'}
            if not (self.baseEndPointURL is '' or self.baseReqBody is '' or self.baseReqHeader is ''):
                response = requests.post(self.baseEndPointURL,data=self.baseReqBody,headers=self.baseReqHeader)
                WSkeywords.saveResults(self,response)
                return self.baseResHeader,self.baseResBody
        else :
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return None

     def get(self):
        if self.baseReqHeader == WSConstants.CONTENT_TYPE_JSON:
            response=requests.get(self.baseEndPointURL)
            print response.content
            WSkeywords.saveResults(self,response)
            return self.baseResHeader,self.baseResBody
        else:
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


     def setTagValue(self,tagValue):
        print


     def setTagAttribute(self):
        print



     def getHeader(self,*args):
        print len(args)
        print args
        print args[0]
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


     def ignoreCertificate(self):
        self.verify=False
        print

     def addClientCertificate(self,filepath,url):
        print


     def getServerCertificate(self,url,filepath):
        import ssl
        import re
        url=url.strip()

        if not(url is None or url is '' or filepath is None or filepath is ''):

            p = '(?:https.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
            m = re.search(p,url)

            hostname=m.group('host')
            port=m.group('port')
            if port is '':
                port=443

##            cert = ssl.get_server_certificate((hostname, 443), ssl_version=ssl.PROTOCOL_TLSv1)
            cert = ssl.get_server_certificate((hostname, port))
            cert=str(cert)
            cert=cert.replace('\n','')

            with open(filepath, "w") as text_file:
                text_file.write(cert)
                text_file.close()
        else :
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
