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
class Test():
    def gettsplist(self):
        obj=handler.Handler()
        dataList=[]

        data =[{
        	"template": "",
        	"testscript_name": "Script1",
        	"testcase": [
  {
    "outputVal": "",
    "keywordVal": "openBrowser",
    "objectName": " ",
    "_id_": "1",
    "inputVal": [
      "2"
    ],
    "appType": "Web",
    "stepNo": 1,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "navigateToURL",
    "objectName": " ",
    "_id_": "2",
    "inputVal": [
      "http://software-ingenuity.com/formdemo.html"
    ],
    "appType": "Web",
    "stepNo": 2,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "{chk_status}",
    "keywordVal": "mouseClick",
    "objectName": "/html/body/form/div[1]/table;null;/html/body/form/div[1]/table;null;null;null",
    "_id_": "3",
    "inputVal": [
      "4;2"
    ],
    "appType": "Web",
    "stepNo": 3,
    "url": "http://software-ingenuity.com/formdemo.html",
    "custname": "table_1"
  },
##  {
##    "outputVal": "{rd_st1}",
##    "keywordVal": "getStatus",
##    "objectName": "/html/body/form/div[1]/table;null;/html/body/form/div[1]/table;null;null;null",
##    "_id_": "4",
##    "inputVal": [
##      "5;2;radio"
##    ],
##    "appType": "Web",
##    "stepNo": 4,
##    "url": "http://software-ingenuity.com/formdemo.html",
##    "custname": "table_1"
##  },
##  {
##    "outputVal": "{rd_st2}",
##    "keywordVal": "getStatus",
##    "objectName": "/html/body/form/div[1]/table;null;/html/body/form/div[1]/table;null;null;null",
##    "_id_": "5",
##    "inputVal": [
##      "5;2;radio;2"
##    ],
##    "appType": "Web",
##    "stepNo": 5,
##    "url": "http://software-ingenuity.com/formdemo.html",
##    "custname": "table_1"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "displayVariableValue",
##    "objectName": " ",
##    "_id_": "6",
##    "inputVal": [
##      "{chk_status};{rd_st1};{rd_st2}"
##    ],
##    "appType": "Generic",
##    "stepNo": 6,
##    "url": " ",
##    "custname": "@Generic"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "verifyExists",
##    "objectName": "/html/body/form/div[2]/table;null;/html/body/form/div[2]/table;null;null;null",
##    "_id_": "7",
##    "inputVal": [
##      ""
##    ],
##    "appType": "Web",
##    "stepNo": 7,
##    "url": "http://software-ingenuity.com/formdemo.html",
##    "custname": "table_2"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "selectValueByIndex",
##    "objectName": "/html/body/form/div[2]/table;null;/html/body/form/div[2]/table;null;null;null",
##    "_id_": "8",
##    "inputVal": [
##      "1;2;dropdown;1;1"
##    ],
##    "appType": "Web",
##    "stepNo": 8,
##    "url": "http://software-ingenuity.com/formdemo.html",
##    "custname": "table_2"
##  },
##  {
##    "outputVal": "{selected}",
##    "keywordVal": "getSelected",
##    "objectName": "/html/body/form/div[2]/table;null;/html/body/form/div[2]/table;null;null;null",
##    "_id_": "9",
##    "inputVal": [
##      "1;2;dropdown;1;1"
##    ],
##    "appType": "Web",
##    "stepNo": 9,
##    "url": "http://software-ingenuity.com/formdemo.html",
##    "custname": "table_2"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "selectValueByText",
##    "objectName": "/html/body/form/div[2]/table;null;/html/body/form/div[2]/table;null;null;null",
##    "_id_": "10",
##    "inputVal": [
##      "1;2;dropdown;1;BMW"
##    ],
##    "appType": "Web",
##    "stepNo": 10,
##    "url": "http://software-ingenuity.com/formdemo.html",
##    "custname": "table_2"
##  },
  {
    "comments": ""
  }
]
        }]
        dataList.append(data)
        flag=True
        for d in dataList:
            flag=obj.parse_json(d)
            if flag == False:
                break
        print '\n'
        tsplist = obj.read_step()
        return tsplist,flag




