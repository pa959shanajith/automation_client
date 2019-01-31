#-------------------------------------------------------------------------------
# Name:        Webservices.py
# Purpose:     Keywords for XML on SOA and RestfulJSON
#
# Author:      sushma.p and wasimakram.sutar
#
# Created:     08-09-2016
# Copyright:   (c) sushma.p wasimakram.sutar 2016
# Licence:     <your licence>
#
# Author:      vishvas.a
#
# Created:     28-04-2017
# Copyright:   (c) vishvas.a 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
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


from xml.etree import ElementTree as etree


import logging
from constants import *
import encryption_utility
import handler
log = logging.getLogger('webservices.py')
class WSkeywords:

     """The instantiation operation __init__ creates an empty object of the class WSkeywords when it is instantiated"""

     def __init__(self):
        self.baseEndPointURL=''
        self.baseOperation=''
        self.baseMethod=''
        self.baseReqHeader= ''
        self.baseReqBody=''
        self.baseResHeader = None
        self.baseResBody=None
        self.modifiedTemplate = ''
        self.verify=''
        self.content_type=''
        # Certificate elements
        self.server_cert_path = None
        self.server_key_path = None
        self.client_cert_path = None
        self.client_key_path = None
        self.certdetails = {}
        self.auth_uname = ''
        self.auth_pass = ''

     def clearValues(self):
        self.baseEndPointURL=''
        self.baseOperation=''
        self.baseMethod=''
        self.baseReqHeader= ''
        self.baseReqBody=''
        self.baseResHeader = None
        self.baseResBody=None
        self.modifiedTemplate = ''
        self.verify=''
        self.content_type=''
        # Certificate elements
        self.server_cert_path = None
        self.server_key_path = None
        self.client_cert_path = None
        self.client_key_path = None
        self.certdetails = {}
        self.auth_uname = ''
        self.auth_pass = ''
     def clearCertFiles(self):
        try:
            os.remove("PRIVATECERT.pem")
            os.remove("PRIVATEKEY.pem")
            os.remove("RSAPRIVATEKEY.pem")
            os.remove("TRUSTSTORECERT.pem")
        except Exception as fileremovalexc:
            log.error(fileremovalexc)
            if self.client_cert_path != '' and self.client_cert_path != None:
                log.error(fileremovalexc)
                log.info(fileremovalexc)
                logger.print_on_console('Cannot find the Certificate' )

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
            url=str(url)
            if url != None and url.strip() != '':
                self.clearValues()
                url=url.strip()
                self.baseEndPointURL = url
                log.debug('End point URL is set')
                logger.print_on_console('End point URL: ',url , ' has been set.')
                log.debug(STATUS_METHODOUTPUT_UPDATE)
                status = ws_constants.TEST_RESULT_PASS
##                output=self.baseEndPointURL
                methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                err_msg = ERROR_CODE_DICT['ERR_INVALID_END_POINT_URL']
        except Exception as e:
            log.error(e)
            err_msg=ws_constants.ERR_MSG1+'setEndPointURL'
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
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
            operation=str(operation)
            if   operation != None and operation.strip() != '':
                 operation=operation.strip()
                 log.debug('Setting base operation name with the input operation name')
                 self.baseOperation = str(operation)
                 logger.print_on_console('Operation has been set to :',operation)
                 log.info('Base operation name has been set to input operation name')
                 log.debug(STATUS_METHODOUTPUT_UPDATE)
                 status = ws_constants.TEST_RESULT_PASS
##                 output=self.baseOperation
                 methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                err_msg =ERROR_CODE_DICT['ERR_INVALID_OPERATION']
        except Exception as e:
            log.error(e)
            err_msg=ws_constants.ERR_MSG1+'setOperations'
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
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
            method=str(method)
            if method != None and method.strip() != '':
                log.debug('Removing leading and trailing spaces from method name and converting it to uppercase')
                method=method.strip().upper()
                log.debug('Removed leading and trailing spaces from method name and converting it to uppercase')
                if method in ws_constants.METHOD_ARRAY:
                    log.debug('Setting input method name to base method name ')
                    self.baseMethod = method
                    log.info('Base method name has been set to input method name')
                    logger.print_on_console('Method name has been set to: ',method)
                    log.debug(STATUS_METHODOUTPUT_UPDATE)
##                    output=self.baseMethod
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
                else:
                    err_msg =ERROR_CODE_DICT['ERR_INVALID_METHOD']
            else:
                err_msg =ERROR_CODE_DICT['ERR_INVALID_METHOD']
        except Exception as e:
            log.error(e)
            err_msg=ws_constants.ERR_MSG1+'setMethods'
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
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
            header=str(header)
            if header != None and header.strip() != '':
                header=header.strip()
                log.debug('Setting the input header template to Header ')
                self.setHeader(header)
##                logger.print_on_console('Header has been set to :',self.baseReqHeader)
                log.info('Input header template has been set ')
                log.debug(STATUS_METHODOUTPUT_UPDATE)
##                output=self.baseReqHeader
                status = ws_constants.TEST_RESULT_PASS
                methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                err_msg =ERROR_CODE_DICT['ERR_INVALID_HEADER']
        except Exception as e:
            log.error(e)
            err_msg=ws_constants.ERR_MSG1+'setHeaderTemplate'
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
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
            header=str(header)
            if header != None and header.strip() != '':
                header = str(header).replace('\n','').replace("'",'').strip()
                log.debug('Removed new line and single quote from the input header')
                header=header.split('##')
                log.debug('Header is split with ##')
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
                log.debug(STATUS_METHODOUTPUT_UPDATE)
##                output=self.baseReqHeader
                status = ws_constants.TEST_RESULT_PASS
                methodoutput = ws_constants.TEST_RESULT_TRUE
                logger.print_on_console('Request Header has been set to :',self.baseReqHeader)
            else:
                err_msg = ERROR_CODE_DICT['ERR_INVALID_HEADER']
        except Exception as e:
            log.error(e)
            err_msg=ws_constants.ERR_MSG1+'setHeader'
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
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
            body=str(body)
            if body != None and body.strip() != '':
                 body=body.strip()
                 self.baseReqBody = body
                 log.info('Input body has been set to base Request body ')
                 log.debug(STATUS_METHODOUTPUT_UPDATE)
##                 output=self.baseReqBody
                 status = ws_constants.TEST_RESULT_PASS
                 methodoutput = ws_constants.TEST_RESULT_TRUE
                 logger.print_on_console('Request Body has been set to :',self.baseReqBody)
            else:
                err_msg = ws_constants.ERR_SET_WHOLE_BODY
        except Exception as e:
            log.error(e)
            err_msg=ws_constants.ERR_MSG1+'setWholeBody'
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg


     def __saveResults(self,response):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        log.debug(STATUS_METHODOUTPUT_LOCALVARIABLES)
        output=OUTPUT_CONSTANT
        try:
            if type(response) == tuple:
                response=response[0]
            logger.print_on_console('Status code: ',response.status_code)
            log.info('Status code: ')
            log.info(response.status_code)
            self.baseResHeader=response.headers
            #added status code
            self.baseResHeader['StatusCode']=response.status_code
            log.info(ws_constants.RESPONSE_HEADER+'\n'+str(self.baseResHeader))
            self.baseResBody=str(response.content).replace("&gt;",">").replace("&lt;","<")
            log.info(ws_constants.RESPONSE_BODY+'\n'+str(self.baseResBody))
            log.debug(STATUS_METHODOUTPUT_UPDATE)
            status = ws_constants.TEST_RESULT_PASS
            methodoutput = ws_constants.TEST_RESULT_TRUE
            output=(self.baseResHeader,str(self.baseResBody).replace("&gt;",">").replace("&lt;","<"))
        except Exception as e:
            log.error(e)
            log.info(e)
            err_msg=ws_constants.METHOD_INVALID_INPUT
            logger.print_on_console(err_msg)
        log.info(RETURN_RESULT)
        return status,methodoutput,output

     def post(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        log.debug(STATUS_METHODOUTPUT_LOCALVARIABLES)
        output=OUTPUT_CONSTANT
        err_msg=None
        try:
            if ws_constants.CONTENT_TYPE_JSON in self.content_type.lower():

                if (not(self.client_cert_path == '' or self.client_cert_path == None)):
                    #if client certificates exists
                    response,err_msg = self.client_Authentication()
                elif(not(self.auth_uname == '' or self.auth_uname == None)
                        and not (self.auth_pass == '' or self.auth_pass == None)):
                    #if only basic authentication required
                    response = self.basic_Authentication()
                elif(not(self.server_cert_path == '' or self.server_cert_path == None)):
                    #if only server certificate
                    response = self.server_Verification()
                else:
                    try:
                        req_body=json.loads(self.baseReqBody)
                    except:
                        req_body=self.baseReqBody
                    response = requests.post(self.baseEndPointURL,data = json.dumps(req_body), headers=self.baseReqHeader)

                if response != None and response != False:
                    self.clearCertFiles()
                    status,methodoutput,output=self.__saveResults(response)
                else:
                    err_msg=ws_constants.METHOD_INVALID_INPUT
                    log.error(err_msg)
            elif ws_constants.CONTENT_TYPE_XML in self.content_type.lower() or ws_constants.CONTENT_TYPE_SOAP_XML in self.content_type.lower():
                if not (self.baseEndPointURL is '' and self.baseReqBody is '' and self.baseReqHeader is ''):
                    if (not(self.client_cert_path == '' or self.client_cert_path == None)):
                        #if client certificates exists
                        response = self.client_Authentication()
                    elif(not(self.auth_uname == '' or self.auth_uname == None)
                            and not (self.auth_pass == '' or self.auth_pass == None)):
                        #if only basic authentication required
                        response = self.basic_Authentication()
                    elif(not(self.server_cert_path == '' or self.server_cert_path == None)):
                        #if only server certificate
                        response = self.server_Verification()
                    else:
                        response = requests.post(self.baseEndPointURL,data=self.baseReqBody,headers=self.baseReqHeader)

                    if response != None and response != False:
                        self.clearCertFiles()
                        status,methodoutput,output=self.__saveResults(response)
                    else:
                        err_msg=ws_constants.METHOD_INVALID_INPUT
                        log.error(err_msg)
                else:
                    err_msg=ws_constants.METHOD_INVALID_INPUT
                    log.error(err_msg)
                    logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)

            else:
                err_msg=ws_constants.METHOD_INVALID_INPUT
                log.error(err_msg)
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            err_msg=str(e)
            log.error(e)
            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

     def get(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        output=None
        err_msg=None
        log.debug(STATUS_METHODOUTPUT_LOCALVARIABLES)
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
            err_msg=str(e)
            log.error(e)
            logger.print_on_console(e)
        log.debug(RETURN_RESULT)
        return status,methodoutput,output,err_msg

     def put(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        output=None
        err_msg=None
        log.debug(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
             s=Session()
             if not (self.baseEndPointURL is '' or self.baseReqBody is '' or self.baseOperation is ''):
                reqUrl=self.baseEndPointURL+'/'+self.baseOperation
                req = requests.Request(method=self.baseMethod, url=reqUrl, data=self.baseReqBody)
                prep=req.prepare()
                response=s.send(prep)
                status,methodoutput,output=self.__saveResults(response)
             else:
                err_msg=ws_constants.METHOD_INVALID_INPUT
                log.error(err_msg)
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            err_msg=str(e)
            log.error(e)
            logger.print_on_console(e)
        log.debug(RETURN_RESULT)
        return status,methodoutput,output,err_msg

     def delete(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        log.debug(STATUS_METHODOUTPUT_LOCALVARIABLES)
        output=None
        err_msg=None
        try:
            s=Session()
            if not (self.baseEndPointURL is '' or self.baseOperation is ''):
                reqUrl=self.baseEndPointURL+'/'+self.baseOperation
                req = requests.Request(method=self.baseMethod, url=reqUrl)
                prep=req.prepare()
                response=s.send(prep)
                status,methodoutput,output=self.__saveResults(response)
            else:
                err_msg=ws_constants.METHOD_INVALID_INPUT
                log.error(err_msg)
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            err_msg=str(e)
            log.error(e)
            logger.print_on_console(e)
        log.debug(RETURN_RESULT)
        return status,methodoutput,output,err_msg

     def head(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        output=None
        err_msg=None
        log.debug(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            s=Session()

            if not (self.baseEndPointURL is '' or self.baseOperation is ''):
                reqUrl=self.baseEndPointURL+'/'+self.baseOperation
                req = requests.Request(method=self.baseMethod, url=reqUrl)
                prep=req.prepare()
                response=s.send(prep)
                self.baseResHeader=response.headers
                self.baseResHeader['StatusCode']=response.status_code
##                logger.print_on_console(ws_constants.RESPONSE_HEADER,str(self.baseResHeader))
                output= self.baseResHeader
                log.info(STATUS_METHODOUTPUT_UPDATE)
                status = ws_constants.TEST_RESULT_PASS
                methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                err_msg=ws_constants.METHOD_INVALID_INPUT
                log.error(err_msg)
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            err_msg=str(e)
            log.error(e)
            logger.print_on_console(e)
        log.debug(RETURN_RESULT)
        return status,methodoutput,output,err_msg

     def executeRequest(self,*args):
        testcasename = handler.testcasename
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=None
        result=status,methodoutput,output,err_msg
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
            result= dict[self.baseMethod](self)
        else:
            log.error(ERROR_CODE_DICT['ERR_INVALID_METHOD'])
            err_msg = ERROR_CODE_DICT['ERR_INVALID_METHOD']
            logger.print_on_console(ERROR_CODE_DICT['ERR_INVALID_METHOD'])
        response=''
        socketIO = args[1]

        #data size check
        import sys
        try:
            if(result[2] != None and result[2] != OUTPUT_CONSTANT):
                headerresp = ''
                res = result[2]
                if type(res) == tuple:
                    for key in res[0]:
                        headerresp = headerresp +str(key) + ":" + str (res[0][key]) + "##"
                    datasize = sys.getsizeof(res[1])
                    kilobytes = datasize/1024
                    megabytes = kilobytes/1024
                    if megabytes > 10:
                        response = headerresp+'rEsPONseBOdY: Response Body exceeds max. Limit., please use writeToFile keyword.'
##                        res[1]='Data length is '+str(megabytes)+', please use writeToFile'
##                        result[2]=headerresp+res[1]
                    else:
                        response=headerresp+'rEsPONseBOdY:'+res[1]
                else:
                    for key in res:
                        headerresp = headerresp +str(key) + ":" + str (res[key]) + "##"
                    response=headerresp+'rEsPONseBOdY: '
            response = str(response)
            if response == '':
                response = 'fail'
            if testcasename == '':
                response = unicode(response, "utf-8")
                socketIO.emit('result_debugTestCaseWS',response)
        except Exception as e:
            logger.print_on_console(e)
        return result

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
##                    logger.print_on_console(ws_constants.RESULT,str(self.baseResHeader[key]))
                    log.debug(STATUS_METHODOUTPUT_UPDATE)
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
                    if self.baseResHeader is not None and  key in self.baseResHeader:
                        output=self.baseResHeader[key]
                    else:
                        output = 'null'
                        logger.print_on_console('Please provide valid Input - Invalid Header Key ='+key)
                else:
##                    logger.print_on_console(ws_constants.RESULT,str(self.baseResHeader))
                    log.debug(STATUS_METHODOUTPUT_UPDATE)
                    if self.baseResHeader != None:
                        status = ws_constants.TEST_RESULT_PASS
                        methodoutput = ws_constants.TEST_RESULT_TRUE
                    output=self.baseResHeader
            else:
                output = []
                for i in range(0,len(args)):
                    key = args[i]
                    if key!= None and key != '':
##                    logger.print_on_console(ws_constants.RESULT,str(self.baseResHeader[key]))
                        log.debug(STATUS_METHODOUTPUT_UPDATE)
                        status = ws_constants.TEST_RESULT_PASS
                        methodoutput = ws_constants.TEST_RESULT_TRUE
                        if self.baseResHeader is not None and key in self.baseResHeader:
                            output.append(self.baseResHeader[key])
                        else:
                            output.append('null')
                            logger.print_on_console('Please provide valid Input - Invalid Header Key ='+key)
                    else:
    ##                    logger.print_on_console(ws_constants.RESULT,str(self.baseResHeader))
                        log.debug(STATUS_METHODOUTPUT_UPDATE)
                        if self.baseResHeader != None:
                            status = ws_constants.TEST_RESULT_PASS
                            methodoutput = ws_constants.TEST_RESULT_TRUE
                        if self.baseResHeader is not None and key in self.baseResHeader:
                            output.append(self.baseResHeader[key])
                        else:
                            output.append('null')
                            logger.print_on_console('Please provide valid Input - Invalid Header Key ='+key)
        except Exception as e:
            log.error(e)
            err_msg=ws_constants.ERR_MSG1+'getHeader'
            logger.print_on_console(err_msg)
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
##                    logger.print_on_console(ws_constants.RESULT,self.baseResBody)
                    log.debug(STATUS_METHODOUTPUT_UPDATE)
                    try:
                        flag=0
                        if self.baseResBody != None:
                            status = ws_constants.TEST_RESULT_PASS
                            methodoutput = ws_constants.TEST_RESULT_TRUE
                            if 'soap:Envelope' in self.baseResBody:
                                from lxml import etree as et
                                root = et.fromstring(self.baseResBody)
                                respBody = et.tostring(root,pretty_print=True)
                                if respBody.find(args[0])==-1:
                                    status = ws_constants.TEST_RESULT_FAIL
                                    methodoutput = ws_constants.TEST_RESULT_FALSE
                                    logger.print_on_console("Input error: please provide the valid input")
                                    flag=1
                                else:
                                    self.baseResBody = respBody
                        if not flag:
                            output= self.baseResBody
                    except Exception as e:
                        log.error(e)
                        output= self.baseResBody
            elif len(args) == 2:
                key=args[0]
                print 'args[2]',args
                if not(self.baseResBody is None):
                    response_body=self.baseResBody
                    if args[0] !='' and args[1]!='' and args[0] !=None and args[1]!=None:
                        start=response_body.find(args[0])+len(args[0])
                        end=response_body.find(args[1])
                        response_body=response_body[start:end]
##                        logger.print_on_console(ws_constants.RESULT,response_body)
                        log.debug(STATUS_METHODOUTPUT_UPDATE)
                        status = ws_constants.TEST_RESULT_PASS
                        methodoutput = ws_constants.TEST_RESULT_TRUE
                        output=response_body
                    else:
                        err_msg='Invalid input'

        except Exception as e:
            log.error(e)
            err_msg=ws_constants.ERR_MSG1+'getBody'
            logger.print_on_console(err_msg)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

    # keyword accepts only JKS,PEM and CERT/CRT/CER-KEY types
    # JKS:
    # input: <<clcert.jks>>;<<clkey.jks>>(opt);<<jkspass>>;<<servcert.jks>>(opt)
    # PEM:
    # input: <<clcert.pem>>;<<clkey.pem>>;<<pempass>>(opt);<<servcert.pem>>(opt)
    # CERT/CER/CRT-KEY
    # input: <<clcert.cert>>;<<clkey.cert>>;<<certpass>>(opt);<<servcert.cert>>(opt)

     def addClientCertificate(self,client_cert,client_key,keystore_pass,server_cert):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
##            response=requests.get(url, cert=(filepath_cert, filepath_key))
##            log.debug(STATUS_METHODOUTPUT_UPDATE)
##            status = ws_constants.TEST_RESULT_PASS
##            methodoutput = ws_constants.TEST_RESULT_TRUE
            if (client_cert != '' and client_cert != None):
                if (os.path.exists(client_cert) == True):
                    # if client trusted cert and client trusted key files are given seperate
                    # possible types cert/cer/crt and pem
                    if (client_key != '' and client_key != None):
                        if (os.path.exists(client_cert) == True):
                            logger.print_on_console('Feature not Supported.')
                        else:
                            logger.print_on_console('Invalid Input: File not found')
                    # if client trusted cert and client trusted key files are combined
                    # possible types pem and jks
                    else:
                        filename,file_ext=os.path.splitext(client_cert)
                        if file_ext.lower() == '.jks':
                            if keystore_pass != '' and keystore_pass != None:
                                keystore_pass = self.aes_decript(keystore_pass)
                                extract_status = self.extract_jks(client_cert,keystore_pass)
                                if extract_status:
                                    logger.print_on_console('Certificate/s have been enabled.')
                                    status = ws_constants.TEST_RESULT_PASS
                                    methodoutput = ws_constants.TEST_RESULT_TRUE
                            else:
                                err_msg = ERR_AUTH_COMPONENT_MISSING
                                logger.print_on_console(ERR_AUTH_COMPONENT_MISSING)
                        elif file_ext.lower() == '.pem':
                            err_msg = 'Feature not Supported.'
                            logger.print_on_console('Feature not Supported.')
                        else:
                            err_msg = 'Invalid Input'
                            logger.print_on_console('Invalid Input')
                else:
                    err_msg = 'Invalid Input'
                    logger.print_on_console('Invalid Input')
            else:
                err_msg = ERR_AUTH_COMPONENT_MISSING
                logger.print_on_console(ERR_AUTH_COMPONENT_MISSING)
        except Exception as e:
            log.error(e)
            err_msg = str(e)
            logger.print_on_console(str(e))
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

     def extract_jks(self,client_cert,keystore_pass):
        extract_status = False
        try:
            import jks
            keystore = jks.KeyStore.load(client_cert, keystore_pass)#,'serverkey')
            # if any of the keys in the store use a password that is not the same as the store password:
            # keystore.entries["key1"].decrypt("key_password")
            for alias, pk in keystore.private_keys.items():
                #print("Private key: %s" % pk.alias)
                if pk.algorithm_oid == jks.util.RSA_ENCRYPTION_OID:
                    rsaprivatepemfile = self.cert_formatter(pk.pkey, "RSA PRIVATE KEY")
                    self.certdetails['RSA PRIVATE KEY'] = rsaprivatepemfile

                try:
                    privatepemfile  = self.cert_formatter(pk.pkey_pkcs8, "PRIVATE KEY")
                    self.certdetails['PRIVATE KEY'] = privatepemfile
                except Exception as e:
                     logger.print_on_console('there is no private key with pkcs8')
                     log.error(e)

                for c in pk.cert_chain:
                    certpemfile = self.cert_formatter(c[1], "CERTIFICATE")
                    self.certdetails['PRIVATE CERT'] =certpemfile

            for alias, c in keystore.certs.items():
                #logger.print_on_console("Certificate:",c.alias)
                truststorepemfile = self.cert_formatter(c.cert, "CERTIFICATE")
                self.certdetails['TRUSTSTORE CERT'] = truststorepemfile

            for alias, secretkey in keystore.secret_keys.items():
                logger.print_on_console("------------------------------------")
                logger.print_on_console("Secret key: %s" % secretkey.alias)
                logger.print_on_console(" Algorithm: %s" % secretkey.algorithm)
                logger.print_on_console(" Key size: %d bits" % secretkey.key_size)
                logger.print_on_console(" Key: %s" % "".join("{:02x"
                +"}".format(bytedata) for bytedata in bytearray(secretkey.key)))
                logger.print_on_console("------------------------------------")

            for each in self.certdetails:
                extract_status = True
                filecreated = open(each.replace(" ","")+".pem","w")
                filecreated.write(self.certdetails[each])
                filecreated.close()
                self.client_cert_path = "PRIVATECERT.pem"
                if self.certdetails['RSA PRIVATE KEY'] == "":
                    self.client_key_path = "PRIVATEKEY.pem"
                else:
                    self.client_key_path = "RSAPRIVATEKEY.pem"
                self.server_cert_path = "TRUSTSTORECERT.pem"

        except Exception as e:
            log.error(e)
            logger.print_on_console(str(e))
        return extract_status


     def cert_formatter(self,certdata_bytes,certtype):
        try:
            import base64, textwrap
            pemfile = ""
            pemfile=("-----BEGIN "+ certtype+"-----\n"
            +"\n".join(textwrap.wrap(base64.b64encode(certdata_bytes).decode('ascii'), 64))
            +"\n-----END "+certtype+"-----")
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        return pemfile


     def server_Verification(self):
        logger.print_on_console('This feature is not available')
        return ''

     def basic_Authentication(self):
        logger.print_on_console('This feature is not available')
        return ''


     def client_Authentication(self):
        response=False
        err_msg = None
        try:
            cert = (self.client_cert_path, self.client_key_path)
            if (cert != (None, None)):
            # if basic auth details are available
                if (not(self.auth_uname == '' and self.auth_uname == None)
                    and not (self.auth_pass == '' and self.auth_pass == None)):
                    # if server side certificates are available
                    if (not (self.server_cert_path == '' or self.server_cert_path == None)):
                        log.debug('TWO WAY HANDSHAKE with basic authentication')
                        response = requests.post(self.baseEndPointURL,
                                                    data = self.baseReqBody,
                                                    headers=self.baseReqHeader,
                                                    cert=cert,
                                                    verify=self.server_cert_path,
                                                    auth=(self.auth_uname,self.auth_pass))
                    else:
                        log.debug('ONE WAY HANDSHAKE with basic authentication')
                        response = requests.post(self.baseEndPointURL,
                                                        data = self.baseReqBody,
                                                        headers=self.baseReqHeader,
                                                        cert=cert,
                                                        verify=False,
                                                        auth=(self.auth_uname,self.auth_pass))
                else:
                    if (not (self.server_cert_path == '' or self.server_cert_path == None)):
                        log.debug('TWO WAY HANDSHAKE without basic authentication')
                        response = requests.post(self.baseEndPointURL,
                                                    data = self.baseReqBody,
                                                    headers=self.baseReqHeader,
                                                    cert=cert,
                                                    verify=self.server_cert_path
                                                    #auth=(self.auth_uname,self.auth_pass)
                                                    )
                    else:
                        log.debug('ONE WAY HANDSHAKE without basic authentication')
                        response = requests.post(self.baseEndPointURL,
                                                        data = self.baseReqBody,
                                                        headers=self.baseReqHeader,
                                                        cert=cert,
                                                        verify=False
                                                        #auth=(self.auth_uname,self.auth_pass)
                                                        )
            else:
                response = requests.post(self.baseEndPointURL,data=self.baseReqBody,headers=self.baseReqHeader)
        except Exception as e:
            log.error(e)
            if '[SSL: CERTIFICATE_VERIFY_FAILED]' in str(e):
                err_msg = 'Certificate Mismatched.'
                logger.print_on_console('Certificate Mismatched.')
            else:
                log.error(str(e))
                log.info(str(e))
                err_msg=ws_constants.METHOD_INVALID_INPUT
                logger.print_on_console(err_msg)
        return response,err_msg

     def parse_xml(self,input_xml,path,value,attribute_name,flag):
        template = etree.fromstring(input_xml)
        index=0
        new_path=path.split('/')
        new_path= new_path[1:]
        result=None
        element_to_change=new_path[len(new_path)-1]
        if element_to_change.startswith('ns',0,2):
            element_to_change=element_to_change.split(":")[1]
        self.actual_parser(element_to_change,value,template,index,attribute_name,flag)
        result=etree.tostring(template)
        return result

     def actual_parser(self,element_to_change,value,obj,index,attribute_name,flag):
        index+=1
        for body_object in obj:
            if flag == 'tagname':
                actual_tag=str(body_object.tag).split('}')[1]
                if element_to_change == actual_tag:
                    body_object.text = value
                    break
            if flag == 'attribute':
                actual_tag=str(body_object.tag).split('}')[1]
                if element_to_change == actual_tag:
                    if len(body_object.attrib) > 0:
                        if attribute_name in body_object.attrib:
                            body_object.attrib[attribute_name]=value
                            break
            self.actual_parser(element_to_change,value,body_object,index,attribute_name,flag)

     def setTagAttribute(self,attribute_value,element_path):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.debug(STATUS_METHODOUTPUT_LOCALVARIABLES)
        import handler
        if self.baseReqBody == '':
            self.baseReqBody=handler.ws_template
        try:
            splitattr=element_path.split('/')
            attribute_name=splitattr[len(splitattr)-1]
            element_path=element_path.rsplit('/',1)[0]
            if attribute_name != None and attribute_name != '' and element_path != None and element_path != '':
                if self.baseReqBody != None and self.baseReqBody != '':
                    result=self.parse_xml(self.baseReqBody,element_path,attribute_value,attribute_name,'attribute')
                    if result != None:
                        self.baseReqBody=result
                        handler.ws_template=self.baseReqBody
                        log.debug(STATUS_METHODOUTPUT_UPDATE)
                        status = ws_constants.TEST_RESULT_PASS
                        methodoutput = ws_constants.TEST_RESULT_TRUE
                        logger.print_on_console('Tag Attribute changed to :',self.baseReqBody)
                else:
                    err_msg=err_msg=ws_constants.ERR_SET_TAG_VALUE
            else:
                err_msg = ws_constants.METHOD_INVALID_INPUT
        except Exception as e:
            log.error(e)
            err_msg=ws_constants.ERR_MSG1+'setTagAttribute'
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg


     def setTagValue(self,value,element_path):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.debug(STATUS_METHODOUTPUT_LOCALVARIABLES)
        import handler
        if self.baseReqBody == '':
            self.baseReqBody=handler.ws_template
        try:
            if value != None and value != '' and element_path != None and element_path != '':
                if self.baseReqBody != None and self.baseReqBody != '':
                    result=self.parse_xml(self.baseReqBody,element_path,value,'','tagname')
                    if result != None:
                        self.baseReqBody=result
                        handler.ws_template=self.baseReqBody
                        log.debug(STATUS_METHODOUTPUT_UPDATE)
                        status = ws_constants.TEST_RESULT_PASS
                        methodoutput = ws_constants.TEST_RESULT_TRUE
                        logger.print_on_console('Tag Value changed to :',self.baseReqBody)
                else:
                    err_msg=ws_constants.ERR_SET_TAG_VALUE
            else:
                err_msg=ws_constants.METHOD_INVALID_INPUT

        except Exception as e:
            log.error(e)
            err_msg=ws_constants.ERR_MSG1+'setTagValue'
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg


     def getServerCertificate(self,url,filepath):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.debug(STATUS_METHODOUTPUT_LOCALVARIABLES)
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
                cert = ssl.get_server_certificate((hostname, int(str(port))),ssl_version=ssl.PROTOCOL_TLSv1)
                cert=str(cert)
                cert=cert.replace('\n','')
                with open(filepath, 'w') as text_file:
                    text_file.write(cert)
                    text_file.close()
                    log.debug(STATUS_METHODOUTPUT_UPDATE)
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                log.info(ws_constants.METHOD_INVALID_INPUT)
                err_msg = ws_constants.METHOD_INVALID_INPUT
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
           log.error(e)
           if ('EOF occurred in violation of protocol' in str(e)) or ('Errno' in str(e)):
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
                err_msg = ws_constants.METHOD_INVALID_INPUT
           else:
                logger.print_on_console(e)
                err_msg = e
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

     def setBasicAuth(self,uname,password):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.debug(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if (not(uname == '' and uname == None) and
                not(password == '' and password == None)):
                    self.auth_uname = uname
                    self.auth_pass = self.aes_decript(password)
                    log.debug(STATUS_METHODOUTPUT_UPDATE)
                    logger.print_on_console('Basic Authentication enabled.')
                    status = ws_constants.TEST_RESULT_PASS
                    methodoutput = ws_constants.TEST_RESULT_TRUE
            else:
                log.info(ws_constants.METHOD_INVALID_INPUT)
                err_msg = ws_constants.METHOD_INVALID_INPUT
                logger.print_on_console(ws_constants.METHOD_INVALID_INPUT)
        except Exception as e:
            log.error(e)
            err_msg = e
            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

     def aes_decript(self,encrypted_data):
        decrypted_data = ''
        try:
            encrypt_obj=encryption_utility.AESCipher()
            decrypted_data=encrypt_obj.decrypt(encrypted_data)
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        return decrypted_data

