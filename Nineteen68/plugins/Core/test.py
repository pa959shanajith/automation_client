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
        	"testcase":[
  {
    "outputVal": "",
    "keywordVal": "openBrowser",
    "objectName": " ",
    "_id_": "1",
    "inputVal": [
      ""
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
      "http://www.way2automation.com/angularjs-protractor/calc/"
    ],
    "appType": "Web",
    "stepNo": 2,
    "url": " ",
    "custname": "@Browser"
  },

  {
    "outputVal": "{title}",
    "keywordVal": "getPageTitle",
    "objectName": " ",
    "_id_": "5",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 5,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyPageTitle",
    "objectName": " ",
    "_id_": "6",
    "inputVal": [
        "{title}"
    ],
    "appType": "Web",
    "stepNo": 6,
    "url": " ",
    "custname": "@Browser"
  },

  {
    "comments": ""
  }
]

        }]
        dataList1.append(data1)


        suite.append(dataList1)

        suite_list.append(suite)



        flag = True
        return suite_list,flag
























##                print tsplist

##        print '===================Scenario execution completed=========================='





