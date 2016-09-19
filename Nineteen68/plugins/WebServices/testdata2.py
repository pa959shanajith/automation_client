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

    endpoint_url = ""
    method = ""
    operation = ""
    header=""
    # The class "constructor" - It's actually an initializer
    def __init__(self, endpoint_url, method, operation,header):
        self.endpoint_url = endpoint_url
        self.method = method
        self.operation = operation
        self.header = header
##        self.toMail = toMail
##        self.toMail_exp = toMail_exp
##        self.GetAttachmentStatus_exp = GetAttachmentStatus_exp

def read_excel_data(filePath):
    testdata=[]
##    filePath = "D:\V2.0\WebServices\Nineteen68\plugins\WebServices\Restful_jsonWebService Keywords.xlsx"
    Work_book = xlrd.open_workbook(filePath)
    ## Sheet_Name = raw_input("Input Sheet Name:")
    Sheet_Name = "Keywords"
    Work_sheet = Work_book.sheet_by_name(Sheet_Name)
    row_count = Work_sheet.nrows
    col_count = Work_sheet.ncols
    for row in range (1,5):
            endpoint_url = Work_sheet.cell_value (row,1)
            method = Work_sheet.cell_value (row,2)
            operation = Work_sheet.cell_value (row,3)
            header = Work_sheet.cell_value (row,4)
##            toMail = Work_sheet.cell_value (row,5)
##            toMail_exp = Work_sheet.cell_value (row,6)
##            GetAttachmentStatus_exp = Work_sheet.cell_value(row,7)
            msg=message(endpoint_url,method,operation,header)
            testdata.append(msg)
    return testdata



