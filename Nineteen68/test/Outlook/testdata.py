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

    fromMail = ""
    fromMail_exp = ""
    subject = ""
    subject_exp=""
    toMail=""
    toMail_exp=""
    GetAttachmentStatus_exp=""
    File_Loc=""
    # The class "constructor" - It's actually an initializer
    def __init__(self, fromMail, fromMail_exp, subject,subject_exp,toMail,toMail_exp,GetAttachmentStatus_exp,File_Loc):
        self.fromMail = fromMail
        self.fromMail_exp = fromMail_exp
        self.subject = subject
        self.subject_exp = subject_exp
        self.toMail = toMail
        self.toMail_exp = toMail_exp
        self.GetAttachmentStatus_exp = GetAttachmentStatus_exp
        self.File_Loc = File_Loc

def read_excel_data(filePath):
    testdata=[]
##    filePath = "C:\Users\prudhvi.gujjuboyina\Documents\pytest\Email Keywords.xlsx"
    Work_book = xlrd.open_workbook(filePath)
    ## Sheet_Name = raw_input("Input Sheet Name:")
    Sheet_Name = "Sheet3"
    Work_sheet = Work_book.sheet_by_name(Sheet_Name)
    row_count = Work_sheet.nrows
    col_count = Work_sheet.ncols
    for row in range (1,2):
            fromMail = Work_sheet.cell_value (row,1)
            fromMail_exp = Work_sheet.cell_value (row,2)
            subject = Work_sheet.cell_value (row,3)
            subject_exp = Work_sheet.cell_value (row,4)
            toMail = Work_sheet.cell_value (row,5)
            toMail_exp = Work_sheet.cell_value (row,6)
            GetAttachmentStatus_exp = Work_sheet.cell_value(row,7)
            File_Loc=Work_sheet.cell_value(row,8)
            msg=message(fromMail,fromMail_exp,subject,subject_exp,toMail,toMail_exp,GetAttachmentStatus_exp,File_Loc)
            testdata.append(msg)
    return testdata



