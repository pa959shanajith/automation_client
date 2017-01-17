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
    "outputVal": "##",
    "keywordVal": "FindWindowAndAttach",
    "objectName": "",
    "_id_": "1",
    "inputVal": [
      "Oracle Applications - EBSDB"
    ],
    "appType": "DesktopJava",
    "stepNo": 1,
    "url": "",
    "custname": "@Oebs"
  },
  {
    "outputVal": "",
    "keywordVal": "launchApplication",
    "objectName": "",
    "_id_": "1",
    "inputVal": [
      "D:\\Java Access Bridge\\SwingSet2.jar;SwingSet2"
    ],
    "appType": "DesktopJava",
    "stepNo": 1,
    "url": "",
    "custname": "@Oebs"
  },
    {
    "outputVal": "",
    "keywordVal": "pause",
    "objectName": "frame[Oracle Applications - EBSDB]/panel[1]/panel[1]/panel[0]/menu bar[1]/menu[File ALT F];File ALT F;0;16;;frame[Oracle Applications - EBSDB]/panel[1]/panel[1]/panel[0]/menu bar[1];7;1;menu bar;menu;",
    "_id_": "2",
    "inputVal": [
      ""
    ],
    "appType": "Generic",
    "stepNo": 2,
    "url": "Oracle Applications - EBSDB",
    "custname": "File ALT F"
  },
  {
    "outputVal": "##",
    "keywordVal": "closeApplication",
    "objectName": "frame[Oracle Applications - EBSDB]/panel[1]/panel[1]/panel[0]/menu bar[1]/menu[File ALT F];File ALT F;0;16;;frame[Oracle Applications - EBSDB]/panel[1]/panel[1]/panel[0]/menu bar[1];7;1;menu bar;menu;",
    "_id_": "2",
    "inputVal": [
      "Oracle Applications - EBSDB"
    ],
    "appType": "DesktopJava",
    "stepNo": 2,
    "url": "Oracle Applications - EBSDB",
    "custname": "File ALT F"
  },
##  {
##    "outputVal": "",
##    "keywordVal": "verifyVisible",
##    "objectName": "frame[Oracle Applications - EBSDB]/panel[1]/panel[1]/panel[0]/menu bar[1]/menu[File ALT F];File ALT F;0;16;;frame[Oracle Applications - EBSDB]/panel[1]/panel[1]/panel[0]/menu bar[1];7;1;menu bar;menu;",
##    "_id_": "2",
##    "inputVal": [
##      ""
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 2,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "File ALT F"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "clickElement",
##    "objectName": "@Custom",
##    "_id_": "3",
##    "inputVal": [
##      "textbox;;1"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 3,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },
##  {
##    "outputVal": "##",
##    "keywordVal": "rightClick",
##    "objectName": "@Custom",
##    "_id_": "4",
##    "inputVal": [
##      "textbox;;1"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 4,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "setText",
##    "objectName": "@Custom",
##    "_id_": "5",
##    "inputVal": [
##      "textbox;;1;peter"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 5,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },
##    {
##    "outputVal": "",
##    "keywordVal": "sendFunctionKeys",
##    "objectName": "@Custom",
##    "_id_": "8",
##    "inputVal": [
##      "textbox;;1;backspace;5"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 8,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "sendFunctionKeys",
##    "objectName": "@Custom",
##    "_id_": "5",
##    "inputVal": [
##      "textbox;;1;tab"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 5,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },
##  {
##    "outputVal": "{t1}",
##    "keywordVal": "getElementText",
##    "objectName": "@Custom",
##    "_id_": "6",
##    "inputVal": [
##      "textbox;;1"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 6,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },


#------------------------------
##  {
##    "outputVal": "{text}",
##    "keywordVal": "getText",
##    "objectName": "@Custom",
##    "_id_": "7",
##    "inputVal": [
##      "textbox;;1"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 7,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },

##  {
##    "outputVal": "",
##    "keywordVal": "setFocus",
##    "objectName": "@Custom",
##    "_id_": "9",
##    "inputVal": [
##      "textbox;;1"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 9,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "setText",
##    "objectName": "@Custom",
##    "_id_": "10",
##    "inputVal": [
##      "textbox;;3"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 10,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "verifyExists",
##    "objectName": "@Custom",
##    "_id_": "11",
##    "inputVal": [
##      "textbox;;1"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 11,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "verifyHidden",
##    "objectName": "@Custom",
##    "_id_": "12",
##    "inputVal": [
##      "textbox;;1"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 12,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "verifyReadOnly",
##    "objectName": "@Custom",
##    "_id_": "13",
##    "inputVal": [
##      "textbox;;1"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 13,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "verifyElementText",
##    "objectName": "@Custom",
##    "_id_": "14",
##    "inputVal": [
##      "textbox;;1;{t1}"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 14,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "verifyVisible",
##    "objectName": "@Custom",
##    "_id_": "15",
##    "inputVal": [
##      "textbox;;1"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 15,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "waitForElementVisible",
##    "objectName": "@Custom",
##    "_id_": "16",
##    "inputVal": [
##      "textbox;;1"
##    ],
##    "appType": "DesktopJava",
##    "stepNo": 16,
##    "url": "Oracle Applications - EBSDB",
##    "custname": "@Custom"
##  },
  {
    "comments": ""
  }
]


}]
        scenario1.append(data1)


        flag = True
        return scenario1,flag







