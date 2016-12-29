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
      "https://cvg53.ngahrhosting.com/Main/careerportal/JobAgent.cfm"
    ],
    "appType": "Web",
    "stepNo": 2,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "rightClick",
    "objectName": "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/a;null;/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/a;null;null;null",
    "_id_": "3",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 3,
    "url": "https://cvg53.ngahrhosting.com/Main/careerportal/JobAgent.cfm",
    "custname": "View All_lnk"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyExists",
    "objectName": "/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/a;null;/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/a;null;null;null",
    "_id_": "4",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 4,
    "url": "https://cvg53.ngahrhosting.com/Main/careerportal/JobAgent.cfm",
    "custname": "View All_lnk"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyExists",
    "objectName": "@Custom",
    "_id_": "5",
    "inputVal": [
      "listbox;;0"
    ],
    "appType": "Web",
    "stepNo": 5,
    "url": "",
    "custname": "@Custom"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyExists",
    "objectName": "@Custom",
    "_id_": "6",
    "inputVal": [
      "dropdown;;0"
    ],
    "appType": "Web",
    "stepNo": 6,
    "url": "",
    "custname": "@Custom"
  },
  {
    "outputVal": "",
    "keywordVal": "mouseHover",
    "objectName": "@Custom",
    "_id_": "7",
    "inputVal": [
      "listbox;;1"
    ],
    "appType": "Web",
    "stepNo": 7,
    "url": "",
    "custname": "@Custom"
  },
  {
    "outputVal": "",
    "keywordVal": "selectValueByIndex",
    "objectName": "@Custom",
    "_id_": "8",
    "inputVal": [
      "listbox;;0;2"
    ],
    "appType": "Web",
    "stepNo": 8,
    "url": "",
    "custname": "@Custom"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyExists",
    "objectName": "@Custom",
    "_id_": "9",
    "inputVal": [
      "dropdown;;4"
    ],
    "appType": "Web",
    "stepNo": 9,
    "url": "",
    "custname": "@Custom"
  },
  {
    "outputVal": "",
    "keywordVal": "selectValueByIndex",
    "objectName": "@Custom",
    "_id_": "10",
    "inputVal": [
      "dropdown;;4;4"
    ],
    "appType": "Web",
    "stepNo": 10,
    "url": "",
    "custname": "@Custom"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyExists",
    "objectName": "@Custom",
    "_id_": "11",
    "inputVal": [
      "dropdown;;3"
    ],
    "appType": "Web",
    "stepNo": 11,
    "url": "",
    "custname": "@Custom"
  },
  {
    "outputVal": "",
    "keywordVal": "selectValueByIndex",
    "objectName": "@Custom",
    "_id_": "12",
    "inputVal": [
      "dropdown;;3;0"
    ],
    "appType": "Web",
    "stepNo": 12,
    "url": "",
    "custname": "@Custom"
  },
  {
    "outputVal": "",
    "keywordVal": "setText",
    "objectName": "@Custom",
    "_id_": "13",
    "inputVal": [
      "textbox;;0;wertyu"
    ],
    "appType": "Web",
    "stepNo": 13,
    "url": "",
    "custname": "@Custom"
  },
  {
    "outputVal": "",
    "keywordVal": "selectValueByIndex",
    "objectName": "@Custom",
    "_id_": "14",
    "inputVal": [
      "listbox;;2;2"
    ],
    "appType": "Web",
    "stepNo": 14,
    "url": "",
    "custname": "@Custom"
  },
  {
    "outputVal": "",
    "keywordVal": "selectValueByIndex",
    "objectName": "@Custom",
    "_id_": "15",
    "inputVal": [
      "dropdown;;0;6"
    ],
    "appType": "Web",
    "stepNo": 15,
    "url": "",
    "custname": "@Custom"
  },
  {
    "comments": ""
  }
]
        }]
        dataList1.append(data1)

        data2 =[{
        	"template": "",
        	"testscript_name": "Script2",
        	"testcase": [
                    {
                    "outputVal": "##",
                    "keywordVal": "for",
                    "objectName": "",
                    "_id_": "9",
                    "inputVal": [
                      "5"
                    ],
                    "appType": "Generic",
                    "stepNo": 9,
                    "url": "",
                    "custname": "@Generic"
                  },
                  {
                    "outputVal": "",
                    "keywordVal": "getBlockCount",
                    "objectName": "",
                    "_id_": "9",
                    "inputVal": [
                      "<Parameter><Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30301</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set>-<Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30302</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set>-<Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30303</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set>-<Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30304</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set>-<Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30305</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set></Parameter>;Set"
                    ],
                    "appType": "Generic",
                    "stepNo": 9,
                    "url": "",
                    "custname": "@Generic"
                  },
                  {
                    "outputVal": "",
                    "keywordVal": "getTagValue",
                    "objectName": "",
                    "_id_": "9",
                    "inputVal": [
                      "<Parameter><Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30301</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set>-<Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30302</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set>-<Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30303</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set>-<Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30304</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set>-<Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30305</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set></Parameter>;2;Set;ZIP"
                    ],
                    "appType": "Generic",
                    "stepNo": 9,
                    "url": "",
                    "custname": "@Generic"
                  },
                  {
                    "outputVal": "",
                    "keywordVal": "GetBlockValue",
                    "objectName": "",
                    "_id_": "9",
                    "inputVal": [
                      "<Parameter><Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30301</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set><Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30302</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set><Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30303</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set><Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30304</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set><Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30305</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set></Parameter>;2;Set"
                    ],
                    "appType": "Generic",
                    "stepNo": 9,
                    "url": "",
                    "custname": "@Generic"
                  },{
                    "outputVal": "##",
                    "keywordVal": "endfor",
                    "objectName": "",
                    "_id_": "9",
                    "inputVal": [
                      "5"
                    ],
                    "appType": "Generic",
                    "stepNo": 9,
                    "url": "",
                    "custname": "@Generic"
                  },
                  {
                    "comments": ""
                  }
                ]
  }]
        dataList1.append(data2)
        suite.append(dataList1)


        data3 =[{
        	"template": "",
        	"testscript_name": "Script3",
        	"testcase": [
  {
    "outputVal": "",
    "keywordVal": "openBrowser",
    "objectName": " ",
    "_id_": "1",
    "inputVal": [
      "1"
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
    "comments": ""
  }
]
        }]
        dataList2.append(data3)

        data4 =[{
        	"template": "",
        	"testscript_name": "Script4",
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
      "https://www.redbus.in/"
    ],
    "appType": "Web",
    "stepNo": 2,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "comments": ""
  }
]
  }]
        dataList2.append(data4)
        suite.append(dataList2)

        data5 =[{
        	"template": "",
        	"testscript_name": "Script3",
        	"testcase": [
  {
    "outputVal": "",
    "keywordVal": "openBrowser",
    "objectName": " ",
    "_id_": "1",
    "inputVal": [
      "1"
    ],
    "appType": "Web",
    "stepNo": 1,
    "url": " ",
    "custname": "@Browser"
  },

  {
    "comments": ""
  }
]
        }]
        dataList3.append(data5)

        data6 =[{
        	"template": "",
        	"testscript_name": "Script4",
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
    "comments": ""
  }
]
  }]
        dataList3.append(data6)
        suite.append(dataList3)
        flag = True
        return suite,flag
























##                print tsplist

##        print '===================Scenario execution completed=========================='





