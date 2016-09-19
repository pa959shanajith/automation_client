#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     16-09-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import xlrd

class message:

    url = ""
    method = ""
    operation = ""
    header=""
    body=""
    tagvalue=""
    filepath=""
    # The class "constructor" - It's actually an initializer
    def __init__(self, url, method, operation,header,body,tagvalue,filepath):
        self.url = url
        self.method = method
        self.operation = operation
        self.header = header
        self.body = body
        self.tagvalue = tagvalue
        self.filepath = filepath

def read_excel_data(filePath):
    testdata=[]
##    filePath = "D:\Code Snippets - Python\Webservice Keywords.xlsx"
    Work_book = xlrd.open_workbook(filePath)
    ## Sheet_Name = raw_input("Input Sheet Name:")
    Sheet_Name = "Sheet3"
    Work_sheet = Work_book.sheet_by_name(Sheet_Name)
    row_count = Work_sheet.nrows
    col_count = Work_sheet.ncols
    for row in range (1,5):
            url = Work_sheet.cell_value (row,1)
            method = Work_sheet.cell_value (row,2)
            operation = Work_sheet.cell_value (row,3)
            header = Work_sheet.cell_value (row,4)
            body = Work_sheet.cell_value (row,5)
            tagvalue = Work_sheet.cell_value (row,6)
            filepath = Work_sheet.cell_value(row,7)
            msg=message(url, method, operation,header,body,tagvalue,filepath)
            testdata.append(msg)
    return testdata



