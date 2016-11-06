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
##        dataList.append(data)
##        data=[{ 	"template": "", 	"testscript_name": "getParam", 	"testcase":
##           [
##          {
##            "outputVal": "",
##            "keywordVal": "if",
##            "objectName": " ",
##            "inputVal": [
##              "(10;==;20)"
##            ],
##            "appType": "Generic",
##            "stepNo": 1,
##            "url": " ",
##            "custname": "@Generic"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "pause",
##            "objectName": "",
##            "inputVal": [
##              ""
##            ],
##            "appType": "Generic",
##            "stepNo": 2,
##            "url": "",
##            "custname": "@Generic"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "elseIf",
##            "objectName": " ",
##            "inputVal": [
##              "(20;<;3)"
##            ],
##            "appType": "Generic",
##            "stepNo": 3,
##            "url": " ",
##            "custname": "@Generic"
##          },
##          {
##            "outputVal": "{con1}",
##            "keywordVal": "concatenate",
##            "objectName": "",
##            "inputVal": [
##              "12;23"
##            ],
##            "appType": "Generic",
##            "stepNo": 4,
##            "url": "",
##            "custname": "@Generic"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "displayVariableValue",
##            "objectName": "",
##            "inputVal": [
##              "{con1}"
##            ],
##            "appType": "Generic",
##            "stepNo": 5,
##            "url": "",
##            "custname": "@Generic"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "else",
##            "objectName": "",
##            "inputVal": [
##              ""
##            ],
##            "appType": "Generic",
##            "stepNo": 6,
##            "url": "",
##            "custname": "@Generic"
##          },
##
##          {
##            "outputVal": "",
##            "keywordVal": "createDynVariable",
##            "objectName": " ",
##            "inputVal": [
##              "{10};qwert"
##            ],
##            "appType": "Generic",
##            "stepNo": 8,
##            "url": " ",
##            "custname": "@Generic"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "displayVariableValue",
##            "objectName": " ",
##            "inputVal": [
##              "{10}"
##            ],
##            "appType": "Generic",
##            "stepNo": 9,
##            "url": " ",
##            "custname": "@Generic"
##          },
##
##          {
##            "outputVal": "",
##            "keywordVal": "displayVariableValue",
##            "objectName": "",
##            "inputVal": [
##              "{20}"
##            ],
##            "appType": "Generic",
##            "stepNo": 11,
##            "url": "",
##            "custname": "@Generic"
##          },
##
##          {
##            "outputVal": "##",
##            "keywordVal": "endIf",
##            "objectName": "",
##            "inputVal": [
##              ""
##            ],
##            "appType": "Generic",
##            "stepNo": 13,
##            "url": "",
##            "custname": "@Generic"
##          },
##          {
##            "comments": ""
##          }
##        ]
##        }]
##
##        data=[{ 	"template": "", 	"testscript_name": "getParam", 	"testcase":
##           [
##          {
##            "outputVal": "",
##            "keywordVal": "for",
##            "objectName": " ",
##            "inputVal": [
##              "(10;==;20)"
##            ],
##            "appType": "Generic",
##            "stepNo": 1,
##            "url": " ",
##            "custname": "@Generic",
##            "additionalinfo" : "step1"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "pause",
##            "objectName": "",
##            "inputVal": [
##              ""
##            ],
##            "appType": "Generic",
##            "stepNo": 2,
##            "url": "",
##            "custname": "@Generic",
##            "additionalinfo" : "step2"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "for",
##            "objectName": "",
##            "inputVal": [
##              ""
##            ],
##            "appType": "Generic",
##            "stepNo": 2,
##            "url": "",
##            "custname": "@Generic",
##            "additionalinfo" : "step3"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "pause",
##            "objectName": "",
##            "inputVal": [
##              ""
##            ],
##            "appType": "Generic",
##            "stepNo": 2,
##            "url": "",
##            "custname": "@Generic",
##            "additionalinfo" : "step4"
##
##          },
##
##          {
##            "outputVal": "",
##            "keywordVal": "endFor",
##            "objectName": "",
##            "inputVal": [
##              ""
##            ],
##            "appType": "Generic",
##            "stepNo": 13,
##            "url": "",
##            "custname": "@Generic",
##            "additionalinfo" : "step5"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "endfor",
##            "objectName": "",
##            "inputVal": [
##              ""
##            ],
##            "appType": "Generic",
##            "stepNo": 13,
##            "url": "",
##            "custname": "@Generic",
##            "additionalinfo" : "step6"
##          },
##          {
##            "comments": ""
##          }
##        ]
##        }]

        dataList=[]
##        dataList.append(data)
        ##data=[{"template":"","testscript_name":"getParam","testcase":[   {     "outputVal": "",     "keywordVal": "for",     "objectName": "",     "inputVal": [       "3"     ],     "appType": "Generic",     "stepNo": 1,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "createDynVariable",     "objectName": " ",     "inputVal": [       "{jp2}; inside for"     ],     "appType": "Generic",     "stepNo": 2,     "url": " ",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "for",     "objectName": "",     "inputVal": [       "2"     ],     "appType": "Generic",     "stepNo": 3,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "displayVariableValue",     "objectName": "",     "inputVal": [       "{jp2}"     ],     "appType": "Generic",     "stepNo": 4,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endFor",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 5,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endFor",     "objectName": " ",     "inputVal": [       "DATE_OPERATIONS"     ],     "appType": "Generic",     "stepNo": 6,     "url": " ",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endFor",     "objectName": " ",     "inputVal": [       "DATE_OPERATIONS"     ],     "appType": "Generic",     "stepNo": 7,     "url": " ",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "if",     "objectName": "",     "inputVal": [       "(sjhfsj)"     ],     "appType": "Generic",     "stepNo": 8,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "copyValue",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 9,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endIf",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 10,     "url": "",     "custname": "@Generic"   },   {     "comments": ""   } ]}]
        ##data=[{"template":"","testscript_name":"Script1","testcase":[   {     "outputVal": "",     "keywordVal": "copyValue",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 1,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "getParam",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 2,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "startLoop",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 3,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "pause",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 4,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endLoop",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 5,     "url": "",     "custname": "@Generic"   },   {     "comments": ""   } ]}]
##        data=[{ 	"template": "", 	"testscript_name": "getParam", 	"testcase":
##           [
####
##          {
##            "outputVal": "{con1}",
##            "keywordVal": "concatenate",
##            "objectName": "",
##            "inputVal": [
##              "Slk ;Software"
##            ],
##            "appType": "Generic",
##            "stepNo": 4,
##            "url": "",
##            "custname": "@Generic",
##            "additionalinfo" : "step6"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "toUpperCase",
##            "objectName": "",
##            "inputVal": [
##              "Wasimakram"
##            ],
##            "appType": "Generic",
##            "stepNo": 5,
##            "url": "",
##            "custname": "@Generic",
##            "additionalinfo" : "step6"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "setText",
##            "objectName": "",
##            "inputVal": [
##              ""
##            ],
##            "appType": "Web",
##            "stepNo": 6,
##            "url": "",
##            "custname": "abc",
##            "additionalinfo" : "This is a web test step"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "setEndPointURL",
##            "objectName": " ",
##            "inputVal": [
##              "http://services.groupkt.com/state/get/IND/all"
##            ],
##            "appType": "Webservice",
##            "stepNo": 7,
##            "url": " ",
##            "custname": "@Generic",
##            "additionalinfo" : "step6"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "for",
##            "objectName": " ",
##            "inputVal": [
##              "3"
##            ],
##            "appType": "Generic",
##            "stepNo": 1,
##            "url": " ",
##            "custname": "@Generic",
##            "additionalinfo" : "step6"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "toUpperCase",
##            "objectName": "",
##            "inputVal": [
##              "Nitte"
##            ],
##            "appType": "Generic",
##            "stepNo": 5,
##            "url": "",
##            "custname": "@Generic",
##            "additionalinfo" : "step6"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "endFor",
##            "objectName": "",
##            "inputVal": [
##              ""
##            ],
##            "appType": "Generic",
##            "stepNo": 13,
##            "url": "",
##            "custname": "@Generic",
##            "additionalinfo" : "step5"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "createDynVariable",
##            "objectName": " ",
##            "inputVal": [
##              "{10};qwert"
##            ],
##            "appType": "Generic",
##            "stepNo": 8,
##            "url": " ",
##            "custname": "@Generic",
##            "additionalinfo" : "step6"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "displayVariableValue",
##            "objectName": " ",
##            "inputVal": [
##              "{10}"
##            ],
##            "appType": "Generic",
##            "stepNo": 9,
##            "url": " ",
##            "custname": "@Generic",
##            "additionalinfo" : "step6"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "else",
##            "objectName": "",
##            "inputVal": [
##              ""
##            ],
##            "appType": "Generic",
##            "stepNo": 10,
##            "url": "",
##            "custname": "@Generic",
##            "additionalinfo" : "step6"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "displayVariableValue",
##            "objectName": "",
##            "inputVal": [
##              "{20}"
##            ],
##            "appType": "Generic",
##            "stepNo": 11,
##            "url": "",
##            "custname": "@Generic",
##            "additionalinfo" : "step6"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "endIf",
##            "objectName": "",
##            "inputVal": [
##              ""
##            ],
##            "appType": "Generic",
##            "stepNo": 12,
##            "url": "",
##            "custname": "@Generic",
##            "additionalinfo" : "step6"
##          },
##          {
##            "outputVal": "",
##            "keywordVal": "endIf",
##            "objectName": "",
##            "inputVal": [
##              ""
##            ],
##            "appType": "Generic",
##            "stepNo": 13,
##            "url": "",
##            "custname": "@Generic",
##            "additionalinfo" : "step6"
##          },
##          {
##            "comments": ""
##          }
##        ]
##        }]





##        data=[{"template":"","testscript_name":"getParam","testcase":[   {     "outputVal": "",     "keywordVal": "for",     "objectName": "",     "inputVal": [       "3"     ],     "appType": "Generic",     "stepNo": 1,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "createDynVariable",     "objectName": " ",     "inputVal": [       "{jp2}; inside for"     ],     "appType": "Generic",     "stepNo": 2,     "url": " ",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "for",     "objectName": "",     "inputVal": [       "2"     ],     "appType": "Generic",     "stepNo": 3,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "toUpperCase",     "objectName": "",     "inputVal": [       "Wasimakram"     ],     "appType": "Generic",     "stepNo": 4,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endFor",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 5,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endFor",     "objectName": " ",     "inputVal": [       "DATE_OPERATIONS"     ],     "appType": "Generic",     "stepNo": 6,     "url": " ",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endFor",     "objectName": " ",     "inputVal": [       "DATE_OPERATIONS"     ],     "appType": "Generic",     "stepNo": 7,     "url": " ",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "if",     "objectName": "",     "inputVal": [       "(sjhfsj)"     ],     "appType": "Generic",     "stepNo": 8,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "copyValue",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 9,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endIf",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 10,     "url": "",     "custname": "@Generic"   },   {     "comments": ""   } ]}]

##
##        data=[{ 	"template": "", 	"testscript_name": "getParam", 	"testcase":
##   [
##  {
##    "outputVal": "",
##    "keywordVal": "for",
##    "objectName": " ",
##    "inputVal": [
##      "3"
##    ],
##    "appType": "Generic",
##    "stepNo": 1,
##    "url": " ",
##    "custname": "@Generic"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "pause",
##    "objectName": "",
##    "inputVal": [
##      ""
##    ],
##    "appType": "Generic",
##    "stepNo": 2,
##    "url": "",
##    "custname": "@Generic"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "for",
##    "objectName": "",
##    "inputVal": [
##      "2"
##    ],
##    "appType": "Generic",
##    "stepNo": 2,
##    "url": "",
##    "custname": "@Generic"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "pause",
##    "objectName": "",
##    "inputVal": [
##      ""
##    ],
##    "appType": "Generic",
##    "stepNo": 2,
##    "url": "",
##    "custname": "@Generic"
##  },
##
##  {
##    "outputVal": "",
##    "keywordVal": "endFor",
##    "objectName": "",
##    "inputVal": [
##      ""
##    ],
##    "appType": "Generic",
##    "stepNo": 13,
##    "url": "",
##    "custname": "@Generic"
##  },
##  {
##    "outputVal": "",
##    "keywordVal": "endfor",
##    "objectName": "",
##    "inputVal": [
##      ""
##    ],
##    "appType": "Generic",
##    "stepNo": 13,
##    "url": "",
##    "custname": "@Generic"
##  },
##  {
##    "comments": ""
##  }
##]
##}]
##
##dataList=[]
##dataList.append(data)
##data=[{"template":"","testscript_name":"getParam","testcase":[   {     "outputVal": "",     "keywordVal": "for",     "objectName": "",     "inputVal": [       "3"     ],     "appType": "Generic",     "stepNo": 1,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "createDynVariable",     "objectName": " ",     "inputVal": [       "{jp2}; inside for"     ],     "appType": "Generic",     "stepNo": 2,     "url": " ",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "for",     "objectName": "",     "inputVal": [       "2"     ],     "appType": "Generic",     "stepNo": 3,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "displayVariableValue",     "objectName": "",     "inputVal": [       "{jp2}"     ],     "appType": "Generic",     "stepNo": 4,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endFor",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 5,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endFor",     "objectName": " ",     "inputVal": [       "DATE_OPERATIONS"     ],     "appType": "Generic",     "stepNo": 6,     "url": " ",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endFor",     "objectName": " ",     "inputVal": [       "DATE_OPERATIONS"     ],     "appType": "Generic",     "stepNo": 7,     "url": " ",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "if",     "objectName": "",     "inputVal": [       "(sjhfsj)"     ],     "appType": "Generic",     "stepNo": 8,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "copyValue",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 9,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endIf",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 10,     "url": "",     "custname": "@Generic"   },   {     "comments": ""   } ]}]
##data=[{"template":"","testscript_name":"Script1","testcase":[   {     "outputVal": "",     "keywordVal": "copyValue",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 1,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "getParam",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 2,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "startLoop",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 3,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "pause",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 4,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endLoop",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 5,     "url": "",     "custname": "@Generic"   },   {     "comments": ""   } ]}]
        data = [{
	"template": "",
	"testscript_name": "getParam",
	"testcase": [{
			"outputVal": "",
			"keywordVal": "if",
			"objectName": " ",
			"inputVal": [
				"(10!=10)"
			],
			"appType": "Generic",
			"stepNo": 1,
			"url": " ",
			"custname": "@Generic"
		},

		{
			"outputVal": "{con1}",
			"keywordVal": "concatenate",
			"objectName": "",
			"inputVal": [
				"12;23"
			],
			"appType": "Generic",
			"stepNo": 4,
			"url": "",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "displayVariableValue",
			"objectName": "",
			"inputVal": [
				"{con1}"
			],
			"appType": "Generic",
			"stepNo": 5,
			"url": "",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "else",
			"objectName": "",
			"inputVal": [
				""
			],
			"appType": "Generic",
			"stepNo": 6,
			"url": "",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "if",
			"objectName": " ",
			"inputVal": [
				"(a==a)"
			],
			"appType": "Generic",
			"stepNo": 7,
			"url": " ",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "createDynVariable",
			"objectName": " ",
			"inputVal": [
				"{10};qwert"
			],
			"appType": "Generic",
			"stepNo": 8,
			"url": " ",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "displayVariableValue",
			"objectName": " ",
			"inputVal": [
				"{10}"
			],
			"appType": "Generic",
			"stepNo": 9,
			"url": " ",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "else",
			"objectName": "",
			"inputVal": [
				""
			],
			"appType": "Generic",
			"stepNo": 10,
			"url": "",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "displayVariableValue",
			"objectName": "",
			"inputVal": [
				"{20}"
			],
			"appType": "Generic",
			"stepNo": 11,
			"url": "",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "findwindowandattach",
			"objectName": "",
			"inputVal": [
				"{20}"
			],
			"appType": "Generic",
			"stepNo": 11,
			"url": "",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "endIf",
			"objectName": "",
			"inputVal": [
				""
			],
			"appType": "Generic",
			"stepNo": 12,
			"url": "",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "writetocell",
			"objectName": "",
			"inputVal": [
				""
			],
			"appType": "Generic",
			"stepNo": 12,
			"url": "",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "endIf",
			"objectName": "",
			"inputVal": [
				""
			],
			"appType": "Generic",
			"stepNo": 13,
			"url": "",
			"custname": "@Generic"
		}, {
			"comments": ""
		}
	]
}]

        data = [{
	"template": "",
	"testscript_name": "getParam",
	"testcase": [{
			"outputVal": "",
			"keywordVal": "for",
			"objectName": " ",
			"inputVal": [
				"3"
			],
			"appType": "Generic",
			"stepNo": 1,
			"url": " ",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "pause",
			"objectName": "",
			"inputVal": [
				""
			],
			"appType": "Generic",
			"stepNo": 2,
			"url": "",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "for",
			"objectName": "",
			"inputVal": [
				"2"
			],
			"appType": "Generic",
			"stepNo": 2,
			"url": "",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "toUpperCase",
			"objectName": "",
			"inputVal": [
				"hiiiiiiiiii"
			],
			"appType": "Generic",
			"stepNo": 2,
			"url": "",
			"custname": "@Generic"
		},

		{
			"outputVal": "",
			"keywordVal": "endFor",
			"objectName": "",
			"inputVal": [
				""
			],
			"appType": "Generic",
			"stepNo": 13,
			"url": "",
			"custname": "@Generic"
		}, {
			"outputVal": "",
			"keywordVal": "endfor",
			"objectName": "",
			"inputVal": [
				""
			],
			"appType": "Generic",
			"stepNo": 13,
			"url": "",
			"custname": "@Generic"
		}, {
			"comments": ""
		}
	]
}]

        data = [{
	"template": "",
	"testscript_name": "getParam",
	"testcase": [{
		"outputVal": "",
		"keywordVal": "createDynVariable",
		"objectName": "",
		"_id_": "1",
		"inputVal": ["{a};1"],
		"stepNo": 1,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "",
		"keywordVal": "createDynVariable",
		"objectName": "",
		"_id_": "2",
		"inputVal": ["{b};1"],
		"stepNo": 2,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "",
		"keywordVal": "if",
		"objectName": "",
		"_id_": "3",
		"inputVal": ["(1!=1)"],
		"stepNo": 3,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "",
		"keywordVal": "displayVariableValue",
		"objectName": "",
		"_id_": "4",
		"inputVal": ["{a}"],
		"stepNo": 4,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "",
		"keywordVal": "elseIf",
		"objectName": "",
		"_id_": "5",
		"inputVal": ["({a}!={b})"],
		"stepNo": 5,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "",
		"keywordVal": "displayVariableValue",
		"objectName": "",
		"_id_": "6",
		"inputVal": ["{a}"],
		"stepNo": 6,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "",
		"keywordVal": "elseIf",
		"objectName": "",
		"_id_": "7",
		"inputVal": ["({a}=={b})"],
		"stepNo": 7,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "",
		"keywordVal": "displayVariableValue",
		"objectName": "",
		"_id_": "8",
		"inputVal": ["{b}"],
		"stepNo": 8,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "",
		"keywordVal": "endIf",
		"objectName": "",
		"_id_": "9",
		"inputVal": [""],
		"stepNo": 9,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "{1}",
		"keywordVal": "concatenate",
		"objectName": "",
		"_id_": "10",
		"inputVal": ["abc;a"],
		"stepNo": 10,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "",
		"keywordVal": "jumpBy",
		"objectName": "",
		"_id_": "11",
		"inputVal": ["-2"],
		"stepNo": 11,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "",
		"keywordVal": "copyValue",
		"objectName": "",
		"_id_": "12",
		"inputVal": ["{c};{b}"],
		"stepNo": 12,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "{2}",
		"keywordVal": "getCurrentDate",
		"objectName": "",
		"_id_": "13",
		"inputVal": ["MM:dd:yyyy"],
		"stepNo": 13,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "",
		"keywordVal": "toLowerCase",
		"objectName": "",
		"_id_": "14",
		"inputVal": ["ABC"],
		"stepNo": 14,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"outputVal": "",
		"keywordVal": "toUpperCase",
		"objectName": "",
		"_id_": "15",
		"inputVal": ["abc"],
		"stepNo": 15,
		"appType": "Generic",
		"custname": "@Generic",
		"url": ""
	}, {
		"comments": ""
	}]
}]
##        dataList.append(data)
        data=[{ 	"template": "", 	"testscript_name": "getParam", 	"testcase": [{ 		"outputVal": "", 		"keywordVal": "createDynVariable", 		"objectName": "", 		"_id_": "1", 		"inputVal": ["{a};1"], 		"stepNo": 1, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "createDynVariable", 		"objectName": "", 		"_id_": "2", 		"inputVal": ["{b};1"], 		"stepNo": 2, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "if", 		"objectName": "", 		"_id_": "3", 		"inputVal": ["(1!=1)"], 		"stepNo": 3, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "displayVariableValue", 		"objectName": "", 		"_id_": "4", 		"inputVal": ["{a}"], 		"stepNo": 4, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "elseIf", 		"objectName": "", 		"_id_": "5", 		"inputVal": ["({a}!={b})"], 		"stepNo": 5, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "displayVariableValue", 		"objectName": "", 		"_id_": "6", 		"inputVal": ["{a}"], 		"stepNo": 6, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "elseIf", 		"objectName": "", 		"_id_": "7", 		"inputVal": ["({a}=={b})"], 		"stepNo": 7, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "displayVariableValue", 		"objectName": "", 		"_id_": "8", 		"inputVal": ["{b}"], 		"stepNo": 8, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "endIf", 		"objectName": "", 		"_id_": "9", 		"inputVal": [""], 		"stepNo": 9, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "{1}", 		"keywordVal": "concatenate", 		"objectName": "", 		"_id_": "10", 		"inputVal": ["abc;a"], 		"stepNo": 10, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "jumpTo", 		"objectName": "", 		"_id_": "11", 		"inputVal": ["mytest"], 		"stepNo": 11, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "copyValue", 		"objectName": "", 		"_id_": "12", 		"inputVal": ["{c};{b}"], 		"stepNo": 12, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "{2}", 		"keywordVal": "getCurrentDate", 		"objectName": "", 		"_id_": "13", 		"inputVal": ["MM:dd:yyyy"], 		"stepNo": 13, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "toLowerCase", 		"objectName": "", 		"_id_": "14", 		"inputVal": ["ABC"], 		"stepNo": 14, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "toUpperCase", 		"objectName": "", 		"_id_": "15", 		"inputVal": ["abc"], 		"stepNo": 15, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"comments": "" 	}] }]
        data1=[{ 	"template": "", 	"testscript_name": "mytest", 	"testcase": [{ 		"outputVal": "", 		"keywordVal": "createDynVariable", 		"objectName": "", 		"_id_": "1", 		"inputVal": ["{a};1"], 		"stepNo": 1, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "createDynVariable", 		"objectName": "", 		"_id_": "2", 		"inputVal": ["{b};1"], 		"stepNo": 2, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "if", 		"objectName": "", 		"_id_": "3", 		"inputVal": ["(1!=1)"], 		"stepNo": 3, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "displayVariableValue", 		"objectName": "", 		"_id_": "4", 		"inputVal": ["{a}"], 		"stepNo": 4, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "elseIf", 		"objectName": "", 		"_id_": "5", 		"inputVal": ["({a}!={b})"], 		"stepNo": 5, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "displayVariableValue", 		"objectName": "", 		"_id_": "6", 		"inputVal": ["{a}"], 		"stepNo": 6, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "elseIf", 		"objectName": "", 		"_id_": "7", 		"inputVal": ["({a}=={b})"], 		"stepNo": 7, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "displayVariableValue", 		"objectName": "", 		"_id_": "8", 		"inputVal": ["{b}"], 		"stepNo": 8, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "endIf", 		"objectName": "", 		"_id_": "9", 		"inputVal": [""], 		"stepNo": 9, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "{1}", 		"keywordVal": "concatenate", 		"objectName": "", 		"_id_": "10", 		"inputVal": ["abc;a"], 		"stepNo": 10, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "jumpTo", 		"objectName": "", 		"_id_": "11", 		"inputVal": ["2"], 		"stepNo": 11, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "copyValue", 		"objectName": "", 		"_id_": "12", 		"inputVal": ["{c};{b}"], 		"stepNo": 12, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "{2}", 		"keywordVal": "getCurrentDate", 		"objectName": "", 		"_id_": "13", 		"inputVal": ["MM:dd:yyyy"], 		"stepNo": 13, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "toLowerCase", 		"objectName": "", 		"_id_": "14", 		"inputVal": ["ABC"], 		"stepNo": 14, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "toUpperCase", 		"objectName": "", 		"_id_": "15", 		"inputVal": ["abc"], 		"stepNo": 15, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"comments": "" 	}] }]
        data = [{
	"template": "",
	"testscript_name": "Script1",
	"testcase": [{
		"outputVal": "",
		"keywordVal": "concatenate",
		"objectName": "",
		"inputVal": ["Wasim;akram"],
		"appType": "Generic",
		"stepNo": 1,
		"url": "",
		"custname": "@Generic"
	}, {
		"outputVal": "",
		"keywordVal": "getParam",
		"objectName": "",
		"inputVal": ["D:/data2.xlsx;Sheet1;1-3"],
		"appType": "Generic",
		"stepNo": 2,
		"url": "",
		"custname": "@Generic"
	}, {
		"outputVal": "",
		"keywordVal": "startLoop",
		"objectName": "",
		"inputVal": [""],
		"appType": "Generic",
		"stepNo": 3,
		"url": "",
		"custname": "@Generic"
	}, {
		"outputVal": "",
		"keywordVal": "concatenate",
		"objectName": "",
		"inputVal": ["|Username|;|Password|"],
		"appType": "Generic",
		"stepNo": 4,
		"url": "",
		"custname": "@Generic"
	}, {
		"outputVal": "",
		"keywordVal": "endLoop",
		"objectName": "",
		"inputVal": [""],
		"appType": "Generic",
		"stepNo": 5,
		"url": "",
		"custname": "@Generic"
	}, {
		"comments": ""
	}]
}]
        dataList=[]
        dataList.append(data)
##        dataList.append(data1)
        print 'Datalist :',dataList
        for d in dataList:
            flag=obj.parse_json(d)
            if flag == False:
                break
        print '\n'
        tsplist = obj.read_step()
        print tsplist
        return tsplist




