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

import Loggers
import requests
from requests import Request,Session

baseEndPointURL=''
baseOperation=''
baseMethod=''
baseReqHeader= ''
baseReqBody=''
headerBuffer=''
baseResHeader = ''
baseResBody=''
modifiedTemplate = ''
obj=Loggers.Loggers()



class WSkeywords:



     def setEndPointURL(self,url):
        global baseEndPointURL
        global obj
        url=url.strip()
        if not (url is None or url is ''):
             baseEndPointURL = url
             return True
        else:
            obj.printLogger('Invalid input')
            return False


     def setOperations(self,operation):
        global baseOperation
        global obj
        operation=operation.strip()
        if not (operation is None or operation is ''):
             baseOperation = operation
             return True
        else:
            obj.printLogger('Invalid input')
            return False

     def setMethods(self,method):
        methodArray = [ "GET", "POST", "HEAD", "PUT", "DELETE" ]
        global baseMethod
        global obj
        method=method.strip().upper()

        if not (method is None or method is ''):
            if method in methodArray:
                baseMethod = method
                obj.printLogger(baseMethod)
                return True
            else:
                obj.printLogger('Invalid method')
                return False


        else:
            obj.printLogger('Invalid input')
            return False

     def setHeader(self,header):
        global baseReqHeader
        global obj
        header=header.strip()
        if not (header is None or header is ''):
             baseReqHeader = header
             return True
        else:
            obj.printLogger('Invalid input')
            return False

     def setWholeBody(self,body):
        global baseReqBody
        global obj
        body=body.strip()
        if not (body is None or body is ''):
             baseReqBody = body
             return True
        else:
            obj.printLogger('Invalid input')
            return False


     def executeRequest(self,array):
        global baseEndPointURL
        global baseMethod
        global baseOperation
        global baseReqHeader
        global baseReqBody
        global baseResBody
        global baseResHeader

        if baseMethod == 'GET':
            if not (baseEndPointURL is '' or baseOperation is '' or baseReqHeader is ''):
                req=baseEndPointURL+'/'+baseOperation+'?'+baseReqHeader
                response=requests.get(req)
                baseResHeader=response.headers
                obj.printLogger("Response header is:"+str(baseResHeader))
                baseResBody=response.content
                obj.printLogger("Response body is:"+str(baseResBody))
                return baseResHeader,baseResBody
            else :
                obj.printLogger('Invalid input')
                return None



        elif baseMethod == 'POST':
            baseReqHeader={'content-type': 'text/xml'}
            if not (baseEndPointURL is '' or baseReqBody is '' or baseReqHeader is ''):
                response = requests.post(baseEndPointURL,data=baseReqBody,headers=baseReqHeader)
                baseResHeader=response.headers
                obj.printLogger("Response header is:"+str(baseResHeader))
                baseResBody=response.content
                obj.printLogger("Response body is:"+str(baseResBody))
                return baseResHeader,baseResBody
            else :
                obj.printLogger('Invalid input')
                return None

        elif baseMethod == 'PUT':
            s=Session()
            if not (baseEndPointURL is '' or baseReqBody is '' or baseOperation is ''):
                reqUrl=baseEndPointURL+'/'+baseOperation
                req = requests.Request(method=baseMethod, url=reqUrl, data=baseReqBody)
                prep=req.prepare()
                response=s.send(prep)
                baseResHeader=response.headers
                obj.printLogger("Response header is:"+str(baseResHeader))
                baseResBody=response.content
                obj.printLogger("Response body is:"+str(baseResBody))
                return baseResHeader,baseResBody
            else :
                obj.printLogger('Invalid input')
                return None

        elif baseMethod == 'DELETE':
            s=Session()
            if not (baseEndPointURL is '' or baseOperation is ''):
                reqUrl=baseEndPointURL+'/'+baseOperation
                req = requests.Request(method=baseMethod, url=reqUrl)
                prep=req.prepare()
                response=s.send(prep)
                baseResHeader=response.headers
                obj.printLogger("Response header is:"+str(baseResHeader))
                baseResBody=response.content
                obj.printLogger("Response body is:"+str(baseResBody))
                return baseResHeader,baseResBody
            else :
                obj.printLogger('Invalid input')
                return None

        elif baseMethod == 'HEAD':
            s=Session()
            if not (baseEndPointURL is '' or baseOperation is ''):
                reqUrl=baseEndPointURL+'/'+baseOperation
                req = requests.Request(method=baseMethod, url=reqUrl)
                prep=req.prepare()
                response=s.send(prep)
                baseResHeader=response.headers
                obj.printLogger("Response header is:"+str(baseResHeader))
                return baseResHeader
            else :
                obj.printLogger('Invalid input')
                return None

     def getHeader(self,array):
        global setEndPointURL
        setEndPointURL = url
        print 'myname'
        print url

     def getBody(self,array):
        global setEndPointURL
        setEndPointURL = url
        print 'myname'
        print url


     def addClientCertificate(self,array):
        global setEndPointURL
        setEndPointURL = url
        print 'myname'
        print url

     def getServerCertificate(self,array):
        global setEndPointURL
        setEndPointURL = url
        print 'myname'
        print url























