#-------------------------------------------------------------------------------
# Name:        testdata_json
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     16-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import xlrd

class message:

    endpoint_url = ''
    method = ''
    operation = ''
    header=''
    # The class "constructor" - It's actually an initializer
    def __init__(self, endpoint_url, method, operation,header):
        self.endpoint_url = endpoint_url
        self.method = method
        self.operation = operation
        self.header = header

def read_excel_data(filePath):
    testdata=[]
    Work_book = xlrd.open_workbook(filePath)
    Sheet_Name = 'Keywords'
    Work_sheet = Work_book.sheet_by_name(Sheet_Name)
    row_count = Work_sheet.nrows
    col_count = Work_sheet.ncols
    for row in range (1,5):
            endpoint_url = Work_sheet.cell_value (row,1)
            method = Work_sheet.cell_value (row,2)
            operation = Work_sheet.cell_value (row,3)
            header = Work_sheet.cell_value (row,4)
            msg=message(endpoint_url,method,operation,header)
            testdata.append(msg)
    return testdata



