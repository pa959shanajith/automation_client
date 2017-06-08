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
        output=None
        try:
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
            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output

     def post(self):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        log.debug(STATUS_METHODOUTPUT_LOCALVARIABLES)
        output=None
        err_msg=None
        try:
            if  ws_constants.CONTENT_TYPE_JSON in self.content_type.lower():
                response = requests.post(self.baseEndPointURL,data = json.dumps(self.baseReqBody), headers=self.baseReqHeader)
                status,methodoutput,output=self.__saveResults(response)
            elif ws_constants.CONTENT_TYPE_XML in self.content_type.lower() or ws_constants.CONTENT_TYPE_SOAP_XML in self.content_type.lower():
                if not (self.baseEndPointURL is '' and self.baseReqBody is '' and self.baseReqHeader is ''):
                    response = requests.post(self.baseEndPointURL,data=self.baseReqBody,headers=self.baseReqHeader)
                    status,methodoutput,output=self.__saveResults(response)
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

        #data size verification
        import sys
        try:
            if(result[2] != None):
                headerresp = ''
                res = result[2]
                if type(res) == tuple:
                    for key in res[0]:
                        headerresp = headerresp +str(key) + ":" + str (res[0][key]) + "##"
                    datasize = sys.getsizeof(res[1])
                    kilobytes = datasize/1024
                    megabytes = kilobytes/1024
                    if megabytes > 5:
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
                    output=self.baseResHeader[key]
                else:
##                    logger.print_on_console(ws_constants.RESULT,str(self.baseResHeader))
                    log.debug(STATUS_METHODOUTPUT_UPDATE)
                    if self.baseResHeader != None:
                        status = ws_constants.TEST_RESULT_PASS
                        methodoutput = ws_constants.TEST_RESULT_TRUE
                    output=self.baseResHeader
        except Exception as e:
            log.error(e)
            err_msg=ws_constants.ERR_MSG1+'getBody'
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
                    if self.baseResBody != None:
                        status = ws_constants.TEST_RESULT_PASS
                        methodoutput = ws_constants.TEST_RESULT_TRUE
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


     def addClientCertificate(self,filepath_key,filepath_cert,url):
        status = ws_constants.TEST_RESULT_FAIL
        methodoutput = ws_constants.TEST_RESULT_FALSE
        err_msg=None
        output=OUTPUT_CONSTANT
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            response=requests.get(url, cert=(filepath_cert, filepath_key))
            log.debug(STATUS_METHODOUTPUT_UPDATE)
            status = ws_constants.TEST_RESULT_PASS
            methodoutput = ws_constants.TEST_RESULT_TRUE
        except Exception as e:
            log.error(e)
            logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

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

           logger.print_on_console(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

