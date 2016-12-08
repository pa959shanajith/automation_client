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
        		"outputVal": "##",
        		"keywordVal": "if",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["(a==b)"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},
            {
        		"outputVal": "##",
        		"keywordVal": "concatenate",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["23432;234234"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "##",
        		"keywordVal": "elseIf",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["(a==a)"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "",
        		"keywordVal": "concatenate",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["23432;234234"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "##",
        		"keywordVal": "jumpBy",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["-2"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "##",
        		"keywordVal": "for",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["2"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "",
        		"keywordVal": "split",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["abc;a"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "##",
        		"keywordVal": "pause",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "##",
        		"keywordVal": "endFor",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	}, {
        		"outputVal": "##",
        		"keywordVal": "endFor",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "##",
        		"keywordVal": "endIf",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "##",
        		"keywordVal": "pause",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "##",
        		"keywordVal": "if",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "",
        		"keywordVal": "pause",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "##",
        		"keywordVal": "else",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "##",
        		"keywordVal": "pause",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "##",
        		"keywordVal": "endIf",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "",
        		"keywordVal": "pause",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"comments": ""
        	}]
        }]

        data =[{
        	"template": "",
        	"testscript_name": "Script1",
        	"testcase": [
            {
        		"outputVal": "##",
        		"keywordVal": "stop",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["D:/data.xlsx;Sheet1"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},
            {
        		"outputVal": "",
        		"keywordVal": "getparam",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["D:/data.xlsx;Sheet1"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "",
        		"keywordVal": "startLoop",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["abc;a"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "",
        		"keywordVal": "toLowerCase",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["|abc|"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},
            {
        		"outputVal": "",
        		"keywordVal": "if",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["a==a"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "##",
        		"keywordVal": "jumpBy",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["2"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "",
        		"keywordVal": "for",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["2"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},
            {
        		"outputVal": "",
        		"keywordVal": "split",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["3324728;2"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "",
        		"keywordVal": "pause",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "",
        		"keywordVal": "toUpperCase",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["|abc|"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "",
        		"keywordVal": "find",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["abc;b"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	}, {
        		"outputVal": "",
        		"keywordVal": "endFor",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "",
        		"keywordVal": "endIf",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "",
        		"keywordVal": "endLoop",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"outputVal": "",
        		"keywordVal": "pause",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": [""],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	},{
        		"comments": ""
        	}]
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




