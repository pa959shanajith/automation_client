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
    "keywordVal": "if",
    "objectName": " ",
    "inputVal": [
      "1;==;1"
    ],
    "appType": "Generic",
    "stepNo": 1,
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
    "stepNo": 1,
    "url": " ",
    "custname": "@Generic"
  },
##  {
##    "outputVal": "",
##    "keywordVal": "navigateToURL",
##    "objectName": " ",
##    "inputVal": [
##      "https://cvg53.ngahrhosting.com/Main/careerportal/JobAgent.cfm"
##    ],
##    "appType": "Web",
##    "stepNo": 2,
##    "url": " ",
##    "custname": "@Browser"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "getCount",
##    "objectName": "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[5]/td[2]/select;null;/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[5]/td[2]/select;null;null;null",
##    "inputVal": [
##      ""
##    ],
##    "appType": "Web",
##    "stepNo": 3,
##    "url": "https://cvg53.ngahrhosting.com/Main/careerportal/JobAgent.cfm",
##    "custname": "Accounting/Finance_elmnt"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "verifyCount",
##    "objectName": "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[5]/td[2]/select;null;/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[5]/td[2]/select;null;null;null",
##    "inputVal": [
##      "47"
##    ],
##    "appType": "Web",
##    "stepNo": 4,
##    "url": "https://cvg53.ngahrhosting.com/Main/careerportal/JobAgent.cfm",
##    "custname": "Accounting/Finance_elmnt"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "selectAllValues",
##    "objectName": "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[5]/td[2]/select;null;/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[5]/td[2]/select;null;null;null",
##    "inputVal": [
##      ""
##    ],
##    "appType": "Web",
##    "stepNo": 5,
##    "url": "https://cvg53.ngahrhosting.com/Main/careerportal/JobAgent.cfm",
##    "custname": "Accounting/Finance_elmnt"
##  },
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





