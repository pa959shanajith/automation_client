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
        	"testscript_name": "getParam",
        	"testcase": [{
        		"outputVal": "",
        		"keywordVal": "concatenate",
        		"objectName": "",
        		"_id_": "3",
        		"inputVal": ["23432;234234"],
        		"appType": "Generic",
        		"stepNo": 3,
        		"url": "",
        		"custname": "@Generic"
        	}, {
        		"comments": ""
        	}]
        }]
        dataList.append(data)
##        dataList.append(data1)
##        print 'Datalist :',dataList
        for d in dataList:
            flag=obj.parse_json(d)
            if flag == False:
                break
        print '\n'
        tsplist = obj.read_step()
##        print tsplist
        return tsplist




