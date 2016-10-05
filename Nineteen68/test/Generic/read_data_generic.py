#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      rakesh.v
#
# Created:     04-10-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import xlrd
class message:

    input1 = ""
    input2 = ""
    input3 = ""

    # The class "constructor" - It's actually an initializer
    def __init__(self, input1, input2,input3):
        self.input1 = input1
        self.input2 = input2
        self.input3 = input3

def read_excel_data(filePath):
    testdata=[]
##    filePath = "D:\pypoc\generic.xlsx"
    Work_book = xlrd.open_workbook(filePath)
    Sheet_Name = "Sheet1"
    Work_sheet = Work_book.sheet_by_name(Sheet_Name)
    row_count = Work_sheet.nrows
    col_count = Work_sheet.ncols
    for row in range (1,4):
        input1 = Work_sheet.cell_value (row,1)
        input2 = Work_sheet.cell_value (row,2)
        input3 = Work_sheet.cell_value (row,3)
        msg=message(input1,input2,input3)
        testdata.append(msg)
    return testdata




