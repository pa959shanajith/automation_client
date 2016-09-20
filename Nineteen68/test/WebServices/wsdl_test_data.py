#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      rakesh.v
#
# Created:     20-09-2016
# Copyright:   (c) rakesh.v 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import xlrd

class message:

    wsdl = ""
    operation_name = ""
    soap_type = ""
    # The class "constructor" - It's actually an initializer
    def __init__(self, wsdl , operation_name , soap_type , expected_body ,expected_header):
        self.wsdl = wsdl
        self.operation_name=operation_name
        self.soap_type = soap_type
        self.expected_body = expected_body
        self.expected_header = expected_header

def read_excel_data(filePath):
    testdata=[]
##    filePath = "D:\wsdl.xlsx"
    Work_book = xlrd.open_workbook(filePath)
    ## Sheet_Name = raw_input("Input Sheet Name:")
    Sheet_Name = "Sheet1"
    Work_sheet = Work_book.sheet_by_name(Sheet_Name)
    row_count = Work_sheet.nrows
    col_count = Work_sheet.ncols
    for row in range (1,2):
            wsdl = Work_sheet.cell_value (row,0)
            operation_name = Work_sheet.cell_value (row,1)
            soap_type = Work_sheet.cell_value (row,2)
            expected_body = Work_sheet.cell_value (row,3)
            expected_header = Work_sheet.cell_value (row,4)
            msg=message(wsdl,operation_name,soap_type,expected_body,expected_header)
            testdata.append(msg)
    return testdata


