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
        	"testscript_name": "V2_SToW_1",
        	"testcase":[
  {
    "outputVal": "",
    "keywordVal": "createDynVariable",
    "objectName": " ",
    "inputVal": [
      "abc"
    ],
    "appType": "Generic",
    "stepNo": 1,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "if",
    "objectName": " ",
    "inputVal": [
      "(abc;==;abc)"
    ],
    "appType": "Generic",
    "stepNo": 2,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "concatenate",
    "objectName": " ",
    "inputVal": [
      "avo;software"
    ],
    "appType": "Generic",
    "stepNo": 3,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "endIf",
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
    "outputVal": "",
    "keywordVal": "jumpTo",
    "objectName": " ",
    "inputVal": [
      "s2"
    ],
    "appType": "Generic",
    "stepNo": 5,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "createDynVariable",
    "objectName": "",
    "inputVal": [
      "{msg};jump to executed "
    ],
    "appType": "Generic",
    "stepNo": 6,
    "url": "",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "displayVariableValue",
    "objectName": "",
    "inputVal": [
      "{msg}"
    ],
    "appType": "Generic",
    "stepNo": 7,
    "url": "",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "stop",
    "objectName": "",
    "inputVal": [
      ""
    ],
    "appType": "Generic",
    "stepNo": 8,
    "url": "",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "evaluate",
    "objectName": " ",
    "inputVal": [
      "1 + 3"
    ],
    "appType": "Generic",
    "stepNo": 9,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "numberFormatter",
    "objectName": " ",
    "inputVal": [
      "1 + 3"
    ],
    "appType": "Generic",
    "stepNo": 10,
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
    "keywordVal": "if",
    "objectName": "",
    "_id_": "1",
    "inputVal": [
      "(1;==;1)"
    ],
    "appType": "Generic",
    "stepNo": 1,
    "url": "",
    "custname": "@Generic"
  },
  {
    "outputVal": "{a}",
    "keywordVal": "concatenate",
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
    "keywordVal": "displayVariableValue",
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
    "outputVal": "",
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
        dataList1.append(data2)
##        dataList1.append(data3)
##        dataList1.append(data4)


        suite.append(dataList1)

        suite_list.append(suite)



        flag = True
        return suite_list,flag
























##                print tsplist

##        print '===================Scenario execution completed=========================='





