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
        	"testcase": [
  {
    "outputVal": "",
    "keywordVal": "openBrowser",
    "objectName": " ",
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
    "inputVal": [
      "https://converge/Home.aspx"
    ],
    "appType": "Web",
    "stepNo": 2,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "##",
    "keywordVal": "drag",
    "objectName": "//*[@id=\"ctl00_RightContent_tvEAMENUt7\"];ctl00_RightContent_tvEAMENUt7;/html/body/form/div[3]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/table[7]/tbody/tr/td[4]/a;null;null;null",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 3,
    "url": "https://converge/Home.aspx",
    "custname": "Payroll (Pay N Comp)"
  },
  {
    "outputVal": "",
    "keywordVal": "drop",
    "objectName": "//*[@id=\"ctl00_RightContent_tvEAMENUt7\"];ctl00_RightContent_tvEAMENUt7;/html/body/form/div[3]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/table[7]/tbody/tr/td[4]/a;null;null;null",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 3,
    "url": "https://converge/Home.aspx",
    "custname": "Payroll (Pay N Comp)"
  },
  {
    "outputVal": "",
    "keywordVal": "switchToWindow",
    "objectName": " ",
    "inputVal": [
      "2"
    ],
    "appType": "Web",
    "stepNo": 4,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "{Url2}",
    "keywordVal": "getCurrentURL",
    "objectName": " ",
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
    "keywordVal": "displayVariableValue",
    "objectName": " ",
    "inputVal": [
      "{Url2}"
    ],
    "appType": "Generic",
    "stepNo": 6,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyExists",
    "objectName": "//*[@id=\"Password\"];Password;/html/body/div[2]/div/div[2]/form/div/div/fieldset/div[2]/div/input;null;null;null",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 7,
    "url": "https://mypnc.neeyamo.com/Account/LogOn",
    "custname": "-----Payroll (Pay N Comp)_lnk-----Pwd_input"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyExists",
    "objectName": "//*[@id=\"RoleCheck\"];RoleCheck;/html/body/div[2]/div/div[2]/form/div/div/fieldset/div[3]/div/div/label[3]/label/input;null;null;null",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 8,
    "url": "https://mypnc.neeyamo.com/Account/LogOn",
    "custname": "Admin_radiobutton"
  },
  {
    "outputVal": "",
    "keywordVal": "switchToWindow",
    "objectName": " ",
    "inputVal": [
      "1"
    ],
    "appType": "Web",
    "stepNo": 9,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyExists",
    "objectName": "//*[@id=\"ctl00_RightContent_tvEAMENUt1\"];ctl00_RightContent_tvEAMENUt1;/html/body/form/div[3]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/table[1]/tbody/tr/td[4]/a;null;null;null",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 10,
    "url": "https://converge/Home.aspx",
    "custname": "NUCLEUS - Oracle ERP_lnk"
  },
  {
    "outputVal": "{Url1}",
    "keywordVal": "getCurrentURL",
    "objectName": " ",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 11,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "displayVariableValue",
    "objectName": " ",
    "inputVal": [
      "{Url1}"
    ],
    "appType": "Generic",
    "stepNo": 12,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "click",
    "objectName": "//*[@id=\"ctl00_RightContent_tvEAMENUt1\"];ctl00_RightContent_tvEAMENUt1;/html/body/form/div[3]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/table[1]/tbody/tr/td[4]/a;null;null;null",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 13,
    "url": "https://converge/Home.aspx",
    "custname": "NUCLEUS - Oracle ERP_lnk"
  },
  {
    "outputVal": "",
    "keywordVal": "switchToWindow",
    "objectName": " ",
    "inputVal": [
      "3"
    ],
    "appType": "Web",
    "stepNo": 14,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "{Url3}",
    "keywordVal": "getCurrentURL",
    "objectName": " ",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 15,
    "url": " ",
    "custname": "@Browser"
  },
   {
    "outputVal": "",
    "keywordVal": "displayVariableValue",
    "objectName": " ",
    "inputVal": [
      "{Url3}"
    ],
    "appType": "Generic",
    "stepNo": 12,
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
      "https://www5.harrisbank.com/HOB/retail/logon"
    ],
    "appType": "Web",
    "stepNo": 2,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyExists",
    "objectName": "//*[@id=\"ContactLinkStyle\"]/a;null;/html/body/div/div[2]/div[1]/div/table/tbody/tr/td/div[1]/form/div/div/div/div/ul/table/tbody/tr[2]/td/div/table/tbody/tr[4]/td/div/table/tbody/tr[2]/td/a;null;null;null",
    "_id_": "3",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 3,
    "url": "https://www5.harrisbank.com/HOB/retail/logon",
    "custname": "BMO Harris Online Services-In"
  },
  {
    "outputVal": "",
    "keywordVal": "pause",
    "objectName": "",
    "_id_": "4",
    "inputVal": [
      ""
    ],
    "appType": "Generic",
    "stepNo": 4,
    "url": "",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "click",
    "objectName": "//*[@id=\"ContactLinkStyle\"]/a;null;/html/body/div/div[2]/div[1]/div/table/tbody/tr/td/div[1]/form/div/div/div/div/ul/table/tbody/tr[2]/td/div/table/tbody/tr[4]/td/div/table/tbody/tr[2]/td/a;null;null;null",
    "_id_": "5",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 5,
    "url": "https://www5.harrisbank.com/HOB/retail/logon",
    "custname": "BMO Harris Online Services-In"
  },
  {
    "outputVal": "",
    "keywordVal": "switchToWindow",
    "objectName": " ",
    "_id_": "6",
    "inputVal": [
      "2"
    ],
    "appType": "Web",
    "stepNo": 6,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "{u2}",
    "keywordVal": "getCurrentURL",
    "objectName": " ",
    "_id_": "7",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 7,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "displayVariableValue",
    "objectName": " ",
    "_id_": "8",
    "inputVal": [
      "{u2}"
    ],
    "appType": "Generic",
    "stepNo": 8,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "switchToWindow",
    "objectName": " ",
    "_id_": "9",
    "inputVal": [
      "1"
    ],
    "appType": "Web",
    "stepNo": 9,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "{u1}",
    "keywordVal": "getCurrentURL",
    "objectName": " ",
    "_id_": "10",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 10,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "displayVariableValue",
    "objectName": " ",
    "_id_": "11",
    "inputVal": [
      "{u1}"
    ],
    "appType": "Generic",
    "stepNo": 11,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "click",
    "objectName": "//*[@id=\"secondaryFooter\"]/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td[1]/small/a;null;/html/body/div/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td[1]/small/a;null;null;null",
    "_id_": "12",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 12,
    "url": "https://www5.harrisbank.com/HOB/retail/logon",
    "custname": "Privacy"
  },
  {
    "outputVal": "",
    "keywordVal": "switchToWindow",
    "objectName": " ",
    "_id_": "13",
    "inputVal": [
      "3"
    ],
    "appType": "Web",
    "stepNo": 13,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "{u3}",
    "keywordVal": "getCurrentURL",
    "objectName": " ",
    "_id_": "14",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 14,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "displayVariableValue",
    "objectName": " ",
    "_id_": "15",
    "inputVal": [
      "{u3}"
    ],
    "appType": "Generic",
    "stepNo": 15,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "outputVal": "",
    "keywordVal": "switchToWindow",
    "objectName": " ",
    "_id_": "16",
    "inputVal": [
      "1"
    ],
    "appType": "Web",
    "stepNo": 16,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "click",
    "objectName": "//*[@id=\"secondaryFooter\"]/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td[2]/small/a;null;/html/body/div/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td[2]/small/a;null;null;null",
    "_id_": "17",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 17,
    "url": "https://www5.harrisbank.com/HOB/retail/logon",
    "custname": "Legal"
  },
  {
    "outputVal": "",
    "keywordVal": "switchToWindow",
    "objectName": " ",
    "_id_": "18",
    "inputVal": [
      "4"
    ],
    "appType": "Web",
    "stepNo": 18,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "{u4}",
    "keywordVal": "getCurrentURL",
    "objectName": " ",
    "_id_": "19",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 19,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "displayVariableValue",
    "objectName": " ",
    "_id_": "20",
    "inputVal": [
      "{u4}"
    ],
    "appType": "Generic",
    "stepNo": 20,
    "url": " ",
    "custname": "@Generic"
  },
  {
    "comments": ""
  }
]
        }]

        data3 =[{
        	"template": "",
        	"testscript_name": "s2",
        	"testcase": [
  {
    "outputVal": "",
    "keywordVal": "openBrowser",
    "objectName": " ",
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
    "inputVal": [
      "http://www.ksrtc.in/oprs-web/"
    ],
    "appType": "Web",
    "stepNo": 2,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "",
    "keywordVal": "click",
    "objectName": "//*[@id=\"searchBtn\"];searchBtn;/html/body/div[5]/div[1]/form/div[1]/div[1]/div/div/div/input;null;null;null",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 3,
    "url": "http://www.ksrtc.in/oprs-web/",
    "custname": "searchBtn_btn"
  },
  {
    "outputVal": "{a}",
    "keywordVal": "getPopUpText",
    "objectName": " ",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 4,
    "url": " ",
    "custname": "@BrowserPopUp"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyPopUpText",
    "objectName": " ",
    "inputVal": [
      "Please select start place."
    ],
    "appType": "Web",
    "stepNo": 5,
    "url": " ",
    "custname": "@BrowserPopUp"
  },
  {
    "outputVal": "##",
    "keywordVal": "acceptPopUp",
    "objectName": " ",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 6,
    "url": " ",
    "custname": "@BrowserPopUp"
  },
  {
    "outputVal": "",
    "keywordVal": "dismissPopUp",
    "objectName": " ",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 7,
    "url": " ",
    "custname": "@BrowserPopUp"
  },
  {
    "comments": ""
  }
]
        }]

        data4 =[{
        	"template": "",
        	"testscript_name": "Defect 143",
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
      "http://10.41.31.131:8085/login_page.php"
    ],
    "appType": "Web",
    "stepNo": 2,
    "url": " ",
    "custname": "@Browser"
  },
  {
    "outputVal": "{a}",
    "keywordVal": "getToolTipText",
    "objectName": "//*[@id=\"login-form\"]/fieldset/span/input;null;/html/body/div/div[2]/form/fieldset/span/input;null;null;null",
    "_id_": "3",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 3,
    "url": "http://10.41.31.131:8085/login_page.php",
    "custname": "NONAME1_btn"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyToolTipText",
    "objectName": "//*[@id=\"login-form\"]/fieldset/span/input;null;/html/body/div/div[2]/form/fieldset/span/input;null;null;null",
    "_id_": "4",
    "inputVal": [
      "{a}"
    ],
    "appType": "Web",
    "stepNo": 4,
    "url": "http://10.41.31.131:8085/login_page.php",
    "custname": "NONAME1_btn"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyButtonName",
    "objectName": "//*[@id=\"login-form\"]/fieldset/span/input;null;/html/body/div/div[2]/form/fieldset/span/input;null;null;null",
    "_id_": "5",
    "inputVal": [
      "Login"
    ],
    "appType": "Web",
    "stepNo": 5,
    "url": "http://10.41.31.131:8085/login_page.php",
    "custname": "NONAME1_btn"
  },
  {
    "outputVal": "",
    "keywordVal": "getLinkText",
    "objectName": "//*[@id=\"version\"]/a;null;/html/body/div/div[3]/address/address/a;null;null;null",
    "_id_": "6",
    "inputVal": [
      ""
    ],
    "appType": "Web",
    "stepNo": 6,
    "url": "http://10.41.31.131:8085/login_page.php",
    "custname": "MantisBT _lnk"
  },
  {
    "outputVal": "",
    "keywordVal": "verifyLinkText",
    "objectName": "//*[@id=\"version\"]/a;null;/html/body/div/div[3]/address/address/a;null;null;null",
    "_id_": "7",
    "inputVal": [
      "MantisBT "
    ],
    "appType": "Web",
    "stepNo": 7,
    "url": "http://10.41.31.131:8085/login_page.php",
    "custname": "MantisBT _lnk"
  },
  {
    "outputVal": "",
    "keywordVal": "uploadFile",
    "objectName": "//*[@id=\"version\"]/a;null;/html/body/div/div[3]/address/address/a;null;null;null",
    "_id_": "8",
    "inputVal": [
      "C:\\Users\\nupoor.kumari\\Desktop\\Test Ref;oracle_logo.png"
    ],
    "appType": "Web",
    "stepNo": 8,
    "url": "http://10.41.31.131:8085/login_page.php",
    "custname": "MantisBT _lnk"
  },
  {
    "comments": ""
  }
]
        }]


        dataList1.append(data1)
##        dataList1.append(data2)
##        dataList1.append(data3)
##        dataList1.append(data4)


        suite.append(dataList1)

        suite_list.append(suite)



        flag = True
        return suite_list,flag
























##                print tsplist

##        print '===================Scenario execution completed=========================='





