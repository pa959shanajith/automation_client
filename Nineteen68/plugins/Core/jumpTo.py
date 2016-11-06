#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     04-11-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     03-11-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import handler
import logger
import Exceptions
import constants

# Handles JumpTo keyword
class  JumpTo():

    def __init__(self,index,name,inputval,outputval,stepnum,testscript_name,executed,apptype):
        self.index=index
        self.name=name
        self.inputval=inputval[0]
        self.testscript_name=testscript_name
        self.outputval=outputval
        self.stepnum=stepnum
        self.executed=executed
        self.apptype=apptype

    def print_step(self):
        logger.log(str(self.index)+' '+self.name+' '+str(self.inputval)+' '+self.testscript_name)

    # returns jumpTo index of step to executed by taking the script name as parameter
    def invoke_jumpto(self):
        try:
            tspList=handler.tspList
            flag=False
            i=-1
            for tsp in tspList:
                i+=1
                if self.inputval==tsp.testscript_name:
                    flag=True
                    logger.log('Target index ' +str(i))
                    return i
            if(flag==False):
                logger.log('Test script name not found')
        except Exception as e:
            Exceptions.error(e)
        return self.index+1


if __name__ == '__main__':
    data=[{ 	"template": "", 	"testscript_name": "getParam", 	"testcase": [{ 		"outputVal": "", 		"keywordVal": "createDynVariable", 		"objectName": "", 		"_id_": "1", 		"inputVal": ["{a};1"], 		"stepNo": 1, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "createDynVariable", 		"objectName": "", 		"_id_": "2", 		"inputVal": ["{b};1"], 		"stepNo": 2, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "if", 		"objectName": "", 		"_id_": "3", 		"inputVal": ["(1;!=;1)"], 		"stepNo": 3, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "displayVariableValue", 		"objectName": "", 		"_id_": "4", 		"inputVal": ["{a}"], 		"stepNo": 4, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "elseIf", 		"objectName": "", 		"_id_": "5", 		"inputVal": ["({a};!=;{b})"], 		"stepNo": 5, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "displayVariableValue", 		"objectName": "", 		"_id_": "6", 		"inputVal": ["{a}"], 		"stepNo": 6, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "elseIf", 		"objectName": "", 		"_id_": "7", 		"inputVal": ["({a};==;{b})"], 		"stepNo": 7, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "displayVariableValue", 		"objectName": "", 		"_id_": "8", 		"inputVal": ["{b}"], 		"stepNo": 8, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "endIf", 		"objectName": "", 		"_id_": "9", 		"inputVal": [""], 		"stepNo": 9, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "{1}", 		"keywordVal": "concatenate", 		"objectName": "", 		"_id_": "10", 		"inputVal": ["abc;a"], 		"stepNo": 10, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "jumpTo", 		"objectName": "", 		"_id_": "11", 		"inputVal": ["mytest"], 		"stepNo": 11, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "copyValue", 		"objectName": "", 		"_id_": "12", 		"inputVal": ["{c};{b}"], 		"stepNo": 12, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "{2}", 		"keywordVal": "getCurrentDate", 		"objectName": "", 		"_id_": "13", 		"inputVal": ["MM:dd:yyyy"], 		"stepNo": 13, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "toLowerCase", 		"objectName": "", 		"_id_": "14", 		"inputVal": ["ABC"], 		"stepNo": 14, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "toUpperCase", 		"objectName": "", 		"_id_": "15", 		"inputVal": ["abc"], 		"stepNo": 15, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"comments": "" 	}] }]
    data1=[{ 	"template": "", 	"testscript_name": "mytest", 	"testcase": [{ 		"outputVal": "", 		"keywordVal": "createDynVariable", 		"objectName": "", 		"_id_": "1", 		"inputVal": ["{a};1"], 		"stepNo": 1, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "createDynVariable", 		"objectName": "", 		"_id_": "2", 		"inputVal": ["{b};1"], 		"stepNo": 2, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "if", 		"objectName": "", 		"_id_": "3", 		"inputVal": ["(1;!=;1)"], 		"stepNo": 3, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "displayVariableValue", 		"objectName": "", 		"_id_": "4", 		"inputVal": ["{a}"], 		"stepNo": 4, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "elseIf", 		"objectName": "", 		"_id_": "5", 		"inputVal": ["({a};!=;{b})"], 		"stepNo": 5, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "displayVariableValue", 		"objectName": "", 		"_id_": "6", 		"inputVal": ["{a}"], 		"stepNo": 6, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "elseIf", 		"objectName": "", 		"_id_": "7", 		"inputVal": ["({a};==;{b})"], 		"stepNo": 7, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "displayVariableValue", 		"objectName": "", 		"_id_": "8", 		"inputVal": ["{b}"], 		"stepNo": 8, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "endIf", 		"objectName": "", 		"_id_": "9", 		"inputVal": [""], 		"stepNo": 9, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "{1}", 		"keywordVal": "concatenate", 		"objectName": "", 		"_id_": "10", 		"inputVal": ["abc;a"], 		"stepNo": 10, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "jumpTo", 		"objectName": "", 		"_id_": "11", 		"inputVal": ["2"], 		"stepNo": 11, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "copyValue", 		"objectName": "", 		"_id_": "12", 		"inputVal": ["{c};{b}"], 		"stepNo": 12, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "{2}", 		"keywordVal": "getCurrentDate", 		"objectName": "", 		"_id_": "13", 		"inputVal": ["MM:dd:yyyy"], 		"stepNo": 13, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "toLowerCase", 		"objectName": "", 		"_id_": "14", 		"inputVal": ["ABC"], 		"stepNo": 14, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"outputVal": "", 		"keywordVal": "toUpperCase", 		"objectName": "", 		"_id_": "15", 		"inputVal": ["abc"], 		"stepNo": 15, 		"appType": "Generic", 		"custname": "@Generic", 		"url": "" 	}, { 		"comments": "" 	}] }]
    dataList=[]
    dataList.append(data)
    dataList.append(data1)
    obj=handler.Handler()
    for d in dataList:
        flag=obj.parse_json(d)
        if flag == False:
            break
    print '\n'
##    obj.read_step()
    tspList=handler.tspList
    a=JumpToHandler()

    print a.jumpTo(2,'mytest')
##    for tsp in  handler.tspList:
##
##        if  ( tsp.keyword=='jumpBy'):
##            print tsp.index
##            print a.jumpBy(tsp.index,2,False)

