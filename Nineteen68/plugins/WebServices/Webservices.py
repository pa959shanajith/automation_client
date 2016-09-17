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

baseEndPointURL=''
baseOperation=''
baseMethod=''
baseReqHeader= ''
baseReqBody=''
baseResHeader = ''
baseResBody=''
modifiedTemplate = ''
dict={}




class WSkeywords:




     def __init__(self):
        print
        # what to do

     def setEndPointURL(self,url):
        url=url.strip()
        if not (url is None or url is ''):
             global baseEndPointURL
             baseEndPointURL = url
             return True
        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False


     def setOperations(self,operation):

        operation=operation.strip()
        if not (operation is None or operation is ''):
             global baseOperation
             baseOperation = operation
             return True
        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False

     def setMethods(self,method):

        method=method.strip().upper()

        if not (method is None or method is ''):
            if method in WSConstants.METHOD_ARRAY:
                global baseMethod
                baseMethod = method
                Logger.log("baseMethod is:"+baseMethod)
                return True
            else:
                Logger.log(WSConstants.METHOD_INVALID)
                return False

        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False

     def setHeader(self,header):

        header=header.strip()

        header.get('Content-Type')
        if not (header is None or header is ''):
             global baseReqHeader
             baseReqHeader = header
             return True
        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False

     def setWholeBody(self,body):

        if not (body is None or body is ''):
             global baseReqBody
             baseReqBody = body
             return True
        else:
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return False

     def saveResults(self,response):
        global baseResHeader
        global baseReqBody

        baseResHeader=response.headers
        Logger.log(WSConstants.RESPONSE_HEADER+str(baseResHeader))
        baseResBody=response.content
        Logger.log(WSConstants.RESPONSE_BODY+str(baseResBody))
        print type(baseResHeader)
        print type(baseResBody)


     def post(self):
        if baseReqHeader == WSConstants.CONTENT_TYPE_JSON:
            response = requests.post(baseEndPointURL)
            print response.content
            WSkeywords().saveResults(response)
            return baseResHeader,baseResBody
        elif baseReqHeader == WSConstants.CONTENT_TYPE_XML:
##        baseReqHeader={'content-type': 'text/xml'}
            if not (baseEndPointURL is '' or baseReqBody is '' or baseReqHeader is ''):
                response = requests.post(baseEndPointURL,data=baseReqBody,headers=baseReqHeader)
                WSkeywords().saveResults(response)
                return baseResHeader,baseResBody
        else :
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return None

     def get(self):
        if baseReqHeader == WSConstants.CONTENT_TYPE_JSON:
            response=requests.get(baseEndPointURL)
            print response.content
            WSkeywords().saveResults(response)
            return baseResHeader,baseResBody
        elif baseReqHeader == WSConstants.CONTENT_TYPE_XML:

            if not (baseEndPointURL is '' or baseOperation is '' or baseReqHeader is ''):
                req=baseEndPointURL+'/'+baseOperation+'?'+baseReqHeader
                response=requests.get(req)
                WSkeywords().saveResults(response)
                return baseResHeader,baseResBody
        else :
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return None

     def put(self):

         s=Session()
         if not (baseEndPointURL is '' or baseReqBody is '' or baseOperation is ''):
            reqUrl=baseEndPointURL+'/'+baseOperation
            req = requests.Request(method=baseMethod, url=reqUrl, data=baseReqBody)
            prep=req.prepare()
            response=s.send(prep)
            WSkeywords().saveResults(response)
            return baseResHeader,baseResBody
         else :
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return None

     def delete(self):
        s=Session()
        if not (baseEndPointURL is '' or baseOperation is ''):
            reqUrl=baseEndPointURL+'/'+baseOperation
            req = requests.Request(method=baseMethod, url=reqUrl)
            prep=req.prepare()
            response=s.send(prep)
            WSkeywords().saveResults(response)
            return baseResHeader,baseResBody
        else :
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return None

     def head(self):
        s=Session()
        if not (baseEndPointURL is '' or baseOperation is ''):
            reqUrl=baseEndPointURL+'/'+baseOperation
            req = requests.Request(method=baseMethod, url=reqUrl)
            prep=req.prepare()
            response=s.send(prep)
            baseResHeader=response.headers
            Logger.log(WSConstants.RESPONSE_HEADER+str(baseResHeader))
            return baseResHeader
        else :
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
            return None



     def executeRequest(self):

        dict={'GET':WSkeywords.get,
        'POST':WSkeywords.post,
        'PUT':WSkeywords.put,
        'HEAD':WSkeywords.head,
        'DELETE':WSkeywords.delete}
        if baseMethod in WSConstants.METHOD_ARRAY:

            print 'yes'
            return dict[baseMethod](self)
        else :
            Logger.log(WSConstants.METHOD_INVALID)


     def setTagValue(self):
        print


     def setTagAttribute(self):
        print



     def getHeader(self,*args):
        if len(args) == 0:
            Logger.log(WSConstants.RESULT+baseResHeader)
            return baseResHeader
        elif len(args) == 1:
            key=args[0]
            Logger.log(WSConstants.RESULT+baseResHeader[key])
            return baseResHeader[key]


     def getBody(self,*args):

        if len(args) == 0:
                Logger.log(WSConstants.RESULT+baseResBody)
                return baseResBody
        elif len(args) == 2:
            key=args[0]
            if not(baseResBody is None):
                str=baseResBody
                if not (args[0] is '' or args[1] is ''):
                    start=str.find(args[0])+len(args[0])
                    end=str.find(args[1])
                    str=str[start:end]
                    Logger.log(WSConstants.RESULT+str)
                    return str




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

            cert = ssl.get_server_certificate((hostname, 443), ssl_version=ssl.PROTOCOL_TLSv1)
##        cert = ssl.get_server_certificate((hostname, port))
            cert=str(cert)
            cert=cert.replace('\n','')

            with open(filepath, "w") as text_file:
                text_file.write(cert)
                text_file.close()
        else :
            Logger.log(WSConstants.METHOD_INVALID_INPUT)
