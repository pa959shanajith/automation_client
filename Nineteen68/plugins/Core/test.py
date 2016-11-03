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
obj=handler.Handler()
data=[{ 	"template": "", 	"testscript_name": "getParam", 	"testcase":
   [
  {
    "outputVal": "",
    "keywordVal": "if",
    "objectName": " ",
    "inputVal": [
      "(10;==;20)"
    ],
    "appType": "Generic",
    "stepNo": 1,
    "url": " ",
    "custname": "@Generic"
  },
  {
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
  },
  {
    "outputVal": "",
    "keywordVal": "elseIf",
    "objectName": " ",
    "inputVal": [
      "(20;<;3)"
    ],
    "appType": "Generic",
    "stepNo": 3,
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
  },
  {
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
  },
  {
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
  },

  {
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
  },
  {
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
  },

  {
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
  },

  {
    "outputVal": "##",
    "keywordVal": "endIf",
    "objectName": "",
    "inputVal": [
      ""
    ],
    "appType": "Generic",
    "stepNo": 13,
    "url": "",
    "custname": "@Generic"
  },
  {
    "comments": ""
  }
]
}]

data=[{ 	"template": "", 	"testscript_name": "getParam", 	"testcase":
   [
  {
    "outputVal": "",
    "keywordVal": "for",
    "objectName": " ",
    "inputVal": [
      "(10;==;20)"
    ],
    "appType": "Generic",
    "stepNo": 1,
    "url": " ",
    "custname": "@Generic"
  },
  {
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
  },
  {
    "outputVal": "",
    "keywordVal": "for",
    "objectName": "",
    "inputVal": [
      ""
    ],
    "appType": "Generic",
    "stepNo": 2,
    "url": "",
    "custname": "@Generic"
  },
  {
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
  },
  {
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
  },
  {
    "comments": ""
  }
]
}]

dataList=[]
dataList.append(data)
##data=[{"template":"","testscript_name":"getParam","testcase":[   {     "outputVal": "",     "keywordVal": "for",     "objectName": "",     "inputVal": [       "3"     ],     "appType": "Generic",     "stepNo": 1,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "createDynVariable",     "objectName": " ",     "inputVal": [       "{jp2}; inside for"     ],     "appType": "Generic",     "stepNo": 2,     "url": " ",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "for",     "objectName": "",     "inputVal": [       "2"     ],     "appType": "Generic",     "stepNo": 3,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "displayVariableValue",     "objectName": "",     "inputVal": [       "{jp2}"     ],     "appType": "Generic",     "stepNo": 4,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endFor",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 5,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endFor",     "objectName": " ",     "inputVal": [       "DATE_OPERATIONS"     ],     "appType": "Generic",     "stepNo": 6,     "url": " ",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endFor",     "objectName": " ",     "inputVal": [       "DATE_OPERATIONS"     ],     "appType": "Generic",     "stepNo": 7,     "url": " ",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "if",     "objectName": "",     "inputVal": [       "(sjhfsj)"     ],     "appType": "Generic",     "stepNo": 8,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "copyValue",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 9,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endIf",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 10,     "url": "",     "custname": "@Generic"   },   {     "comments": ""   } ]}]
##data=[{"template":"","testscript_name":"Script1","testcase":[   {     "outputVal": "",     "keywordVal": "copyValue",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 1,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "getParam",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 2,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "startLoop",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 3,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "pause",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 4,     "url": "",     "custname": "@Generic"   },   {     "outputVal": "",     "keywordVal": "endLoop",     "objectName": "",     "inputVal": [       ""     ],     "appType": "Generic",     "stepNo": 5,     "url": "",     "custname": "@Generic"   },   {     "comments": ""   } ]}]
data=[{ 	"template": "", 	"testscript_name": "getParam", 	"testcase":
   [
  {
    "outputVal": "",
    "keywordVal": "if",
    "objectName": " ",
    "inputVal": [
      "(10;==;20)"
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
  },
  {
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
  },
  {
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
  },
  {
    "outputVal": "",
    "keywordVal": "if",
    "objectName": " ",
    "inputVal": [
      "(a;!=;a)"
    ],
    "appType": "Generic",
    "stepNo": 7,
    "url": " ",
    "custname": "@Generic"
  },
  {
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
  },
  {
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
  },
  {
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
  },
  {
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
  },
  {
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
  },
  {
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
  },
  {
    "comments": ""
  }
]
}]
dataList.append(data)
for d in dataList:
    flag=obj.parse_json(d)
    if flag == False:
        break
print '\n'
obj.read_step()




