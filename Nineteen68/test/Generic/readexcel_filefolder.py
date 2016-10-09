#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     05-10-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import xlrd
class message:

    inputpath1 = ""
    inputpath2 = ""
    content = ""

    # The class "constructor" - It's actually an initializer
    def __init__(self, inputpath1, inputpath2,content):
        self.inputpath1 = inputpath1
        self.inputpath2 = inputpath2
        self.content = content

def read_excel_data(filePath):
    testdata=[]
##    filePath = "D:\pypoc\generic.xlsx"
    Work_book = xlrd.open_workbook(filePath)
    Sheet_Name = "Sheet3"
    Work_sheet = Work_book.sheet_by_name(Sheet_Name)
    row_count = Work_sheet.nrows
    col_count = Work_sheet.ncols
    for row in range (9,10):
        inputpath1 = Work_sheet.cell_value (row,1)
        inputpath2 = Work_sheet.cell_value (row,2)
        content = Work_sheet.cell_value (row,3)
        msg=message(inputpath1,inputpath2,content)
        print inputpath1

        testdata.append(msg)
    return testdata



read_excel_data('D:\\64Bit\\Nineteen68\\test\\Generic\\generic.xls')

