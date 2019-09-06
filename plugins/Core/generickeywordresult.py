#-------------------------------------------------------------------------------
# Name:        generickeywordresult.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     02-11-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class GenericKeywordResult():
    def __init__(self,result,returnVal):
        self.result=result
        self.returnVal=returnVal

    def getresult(self):
        return self.result

    def setresult(self,result):
        self.result = result

    def getreturnVal(self):
        return self.returnVal

    def setreturnVal(self,returnVal):
        self.returnVal = returnVal

    def print_result(self):
        print(self.result,self.returnVal,self.apptype)
