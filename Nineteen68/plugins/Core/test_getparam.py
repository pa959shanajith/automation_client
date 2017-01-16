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
    "objectName": "",
    "_id_": "1",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 1,
    "url": "",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "navigateToURL",
    "objectName": "",
    "_id_": "2",
    "inputVal": [
      "http://10.41.31.131:8085/bug_report_page.php"
    ],
    "appType": "Web",
    "stepNo": 2,
    "url": "",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "getParam",
    "objectName": " ",
    "_id_": "3",
    "inputVal": [
      "D:\\Test.xlsx;getparam"
    ],
    "appType": "Generic",
    "stepNo": 3,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "startLoop",
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
    "outputVal": "",
    "keywordVal": "sendValue",
    "objectName": "//*[@id=\"username\"];username;/html/body/div/div[2]/form/fieldset/div[1]/span[1]/input;null;null;null",
    "_id_": "5",
    "inputVal": [
      "|user|"
    ],
    "appType": "Web",
    "stepNo": 5,
    "url": "http://10.41.31.131:8085/login_page.php",
    "custname": "username_txtbox"
  },
  {
    "outputVal": "",
    "keywordVal": "sendValue",
    "objectName": "//*[@id=\"password\"];password;/html/body/div/div[2]/form/fieldset/div[2]/span[1]/input;null;null;null",
    "_id_": "6",
    "inputVal": [
      "|pwd|"
    ],
    "appType": "Web",
    "stepNo": 6,
    "url": "http://10.41.31.131:8085/login_page.php",
    "custname": "password_txtbox"
  },
  {
    "outputVal": "",
    "keywordVal": "sendValue",
    "objectName": "//*[@id=\"username\"];username;/html/body/div/div[2]/form/fieldset/div[1]/span[1]/input;null;null;null",
    "_id_": "7",
    "inputVal": [
      "|real|"
    ],
    "appType": "Web",
    "stepNo": 7,
    "url": "http://10.41.31.131:8085/login_page.php",
    "custname": "username_txtbox"
  },
  {
    "outputVal": "",
    "keywordVal": "endLoop",
    "objectName": " ",
    "_id_": "8",
    "inputVal": [
      ""
    ],
    "appType": "Generic",
    "stepNo": 8,
    "url": " ",
    "custname": "@Generic"
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





