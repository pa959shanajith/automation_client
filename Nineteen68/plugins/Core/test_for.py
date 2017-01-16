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
        obj=handler.Handler()
        suite_list = []
        suite = []
        dataList1=[]
        dataList2 = []
        dataList3 = []

        data1 =[{
        	"template": "",
        	"testscript_name": "Script1",
        	"testcase": [
  {
    "outputVal": "",
    "keywordVal": "createDynVariable",
    "objectName": " ",
    "inputVal": [
      "{a};sushma"
    ],
    "appType": "Generic",
    "stepNo": 1,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "for",
    "objectName": " ",
    "inputVal": [
      "2"
    ],
    "appType": "Generic",
    "stepNo": 2,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "displayVariableValue",
    "objectName": " ",
    "inputVal": [
      "{a}"
    ],
    "appType": "Generic",
    "stepNo": 3,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "endFor",
    "objectName": " ",
    "inputVal": [
      ""
    ],
    "appType": "Generic",
    "stepNo": 4,
    "url": " ",
    "custname": "@Generic"
  },

  {
    "comments": ""
  }
]
        }]



        data2 =[{
        	"template": "",
        	"testscript_name": "s2",
        	"testcase": [
  {
    "outputVal": "",
    "keywordVal": "for",
    "objectName": "",
    "_id_": "1",
    "inputVal": [
      "2"
    ],
    "appType": "Generic",
    "stepNo": 1,
    "url": "",
    "custname": "@Generic"
  },
  {
    "outputVal": "{a}",
    "keywordVal": "pause",
    "objectName": " ",
    "_id_": "2",
    "inputVal": [
      "abc;d"
    ],
    "appType": "Generic",
    "stepNo": 2,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "endFor",
    "objectName": " ",
    "_id_": "3",
    "inputVal": [
      "{a}"
    ],
    "appType": "Generic",
    "stepNo": 3,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "##",
    "keywordVal": "endIf",
    "objectName": " ",
    "_id_": "4",
    "inputVal": [
      ""
    ],
    "appType": "Generic",
    "stepNo": 4,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "comments": ""
  }
]
        }]


        dataList1.append(data1)
        dataList=[]
        dataList2.append(data2)


        suite.append(dataList1)
        suite.append(dataList2)

        suite_list.append(suite)



        flag = True
        return suite_list,flag
























##                print tsplist

##        print '===================Scenario execution completed=========================='





