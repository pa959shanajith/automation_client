#-------------------------------------------------------------------------------
# Name:        test
# Purpose:
#
# Author:      sushma.p
#
# Created:     27-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------



import handler
import controller
import logger
class Test():
    def gettsplist(self):

        scenario1=[]


        data1 =[{
        	"template": "",
        	"testscript_name": "Script1",
           "testcase": [
  {
    "outputVal": "",
    "keywordVal": "setEndPointURL",
    "objectName": "",
    "_id_": "1",
    "inputVal": [
      "http://10.41.133.135:8500/Service1.svc"
    ],
    "appType": "Webservice",
    "stepNo": 1,
    "url": "",
    "custname": "WebService List"
  },
  {
    "outputVal": "",
    "keywordVal": "setMethods",
    "objectName": "",
    "_id_": "2",
    "inputVal": [
      "POST"
    ],
    "appType": "Webservice",
    "stepNo": 2,
    "url": "",
    "custname": "WebService List"
  },
  {
    "outputVal": "",
    "keywordVal": "setHeader",
    "objectName": "",
    "_id_": "3",
    "inputVal": [
      "POST /Service1.svc HTTP/1.1##Host: 10.41.133.135:8500##Content-Type: text/xml; charset=utf-8##Content-Length: length##SOAPAction: \"http://tempuri.org/IService1/Authenticate\"\n"
    ],
    "appType": "Webservice",
    "stepNo": 3,
    "url": "",
    "custname": "WebService List"
  },
  {
    "outputVal": "##",
    "keywordVal": "setHeader",
    "objectName": "",
    "_id_": "4",
    "inputVal": [
      "Content-Type: text/xml; charset=utf-8"
    ],
    "appType": "Webservice",
    "stepNo": 4,
    "url": "",
    "custname": "WebService List"
  },
  {
    "outputVal": "##",
    "keywordVal": "setHeader",
    "objectName": "",
    "_id_": "5",
    "inputVal": [
      "POST /Service1.svc HTTP/1.1"
    ],
    "appType": "Webservice",
    "stepNo": 5,
    "url": "",
    "custname": "WebService List"
  },
  {
    "outputVal": "##",
    "keywordVal": "setHeader",
    "objectName": "",
    "_id_": "6",
    "inputVal": [
      "SOAPAction: \"http://tempuri.org/IService1/Authenticate\""
    ],
    "appType": "Webservice",
    "stepNo": 6,
    "url": "",
    "custname": "WebService List"
  },
  {
    "outputVal": "##",
    "keywordVal": "setHeader",
    "objectName": "",
    "_id_": "7",
    "inputVal": [
      "Content-Length: length"
    ],
    "appType": "Webservice",
    "stepNo": 7,
    "url": "",
    "custname": "WebService List"
  },
  {
    "outputVal": "##",
    "keywordVal": "setHeader",
    "objectName": "",
    "_id_": "8",
    "inputVal": [
      "Host: 10.41.133.135:8500"
    ],
    "appType": "Webservice",
    "stepNo": 8,
    "url": "",
    "custname": "WebService List"
  },
  {
    "outputVal": "",
    "keywordVal": "setTagValue",
    "objectName": "/s11:Envelope/s11:Body/ns1:Authenticate/ns1:username",
    "_id_": "9",
    "inputVal": [
      "admin"
    ],
    "appType": "Webservice",
    "stepNo": 9,
    "url": "",
    "custname": "ns1:username"
  },
  {
    "outputVal": "",
    "keywordVal": "setTagValue",
    "objectName": "/s11:Envelope/s11:Body/ns1:Authenticate/ns1:password",
    "_id_": "10",
    "inputVal": [
      "admin"
    ],
    "appType": "Webservice",
    "stepNo": 10,
    "url": "",
    "custname": "ns1:password"
  },
  {
    "outputVal": "",
    "keywordVal": "executeRequest",
    "objectName": "",
    "_id_": "11",
    "inputVal": [
      ""
    ],
    "appType": "Webservice",
    "stepNo": 11,
    "url": "",
    "custname": "WebService List"
  },
  {
    "outputVal": "{body}",
    "keywordVal": "getBody",
    "objectName": "",
    "_id_": "12",
    "inputVal": [
      ""
    ],
    "appType": "Webservice",
    "stepNo": 12,
    "url": "",
    "custname": "WebService List"
  },
  {
    "outputVal": "{header}",
    "keywordVal": "getHeader",
    "objectName": "",
    "_id_": "13",
    "inputVal": [
      ""
    ],
    "appType": "Webservice",
    "stepNo": 13,
    "url": "",
    "custname": "WebService List"
  },
  {
    "outputVal": "",
    "keywordVal": "displayVariableValue",
    "objectName": " ",
    "_id_": "14",
    "inputVal": [
      "{body};{header}"
    ],
    "appType": "Generic",
    "stepNo": 14,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "comments": ""
  }
]


}]
        scenario1.append(data1)


        flag = True
        return scenario1,flag







