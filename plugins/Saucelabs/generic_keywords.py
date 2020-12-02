#-------------------------------------------------------------------------------
# Name:        generic_keywords.py
# Purpose:
#
# Author:      rakshak.kamath
#
# Created:     17-10-2020
# Copyright:   (c) rakshak.kamath 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import os
import subprocess


class Util:

    def __init__(self,f):
        self.f=f

    def wait(self,space,input,*args):
        self.f.write(space+"input='"+str(int(input[0][1:-1]))+"'")
        self.f.write(space+"time.sleep(int(input))")
        self.f.write(space+"status='Pass'")

    def executeFile(self,space,input,*args):
        filePath=input
        filename,file_ext=os.path.splitext(filePath)
        self.f.write(space+"filePath="+filePath)
        if file_ext in ".bat" or  file_ext in ".exe":
            self.f.write(space+"p = subprocess.Popen(filePath,cwd=os.path.dirname(filePath), creationflags=subprocess.CREATE_NEW_CONSOLE)")
        elif file_ext in ".vbs":
            self.f.write(space+"os.chdir(os.path.dirname(filePath))")
            self.f.write(space+"os.startfile(filePath)")
        self.f.write(space+"status='Pass'")

class DynamicVariables:

    def __init__(self,f):
        self.f=f
        # self.f.write(space+"from collections import OrderedDict")
        # self.f.write(space+"variable_map=OrderedDict()")

    def createDynVariable(self,space,input,*args):
        self.f.write(space+"variable="+input[0])
        self.f.write(space+"value="+input[1])
        self.f.write(space+"dyn_var_map[variable]=value")
        self.f.write(space+"status='Pass'")

    def modifyValue(self,space,input,*args):
        self.f.write(space+"variable="+input[0])
        self.f.write(space+"value="+input[1])
        self.f.write(space+"dyn_var_map[variable]=value")
        self.f.write(space+"status='Pass'")

    def copyValue(self,space,input,*args):
        self.f.write(space+"variable="+input[0])
        self.f.write(space+"value="+input[1])
        self.f.write(space+"variable_map[variable]=value")
        self.f.write(space+"status='Pass'")

    def deleteDynVariable(self,space,input,*args):
        self.f.write(space+"variable="+input[0])
        self.f.write(space+"dyn_var_map.pop(variable)")
        self.f.write(space+"status='Pass'")

class FolderOperation:

    def __init__(self,f):
        self.f=f

    def createFolder(self,space,input,*args):
        inputVal=input
        inputpath=inputVal[0]
        folder_name=inputVal[1]
        input_val=inputpath+os.sep+folder_name
        self.f.write(space+"input="+input_val)
        self.f.write(space+"os.makedirs(input)")
        self.f.write(space+"status='Pass'")

    def verifyFolderExists(self,space,input,*args):
        inputVal=input
        inputpath=inputVal[0]
        folder_name=inputVal[1]
        input_val=inputpath+os.sep+folder_name
        self.f.write(space+"input="+input_val)
        self.f.write(space+"output=os.path.exists(input)")
        self.f.write(space+"status='Pass' if output else 'Fail'")

    def renameFolder(self,space,input,*args):
        inputVal=input
        inputpath=inputVal[0]
        folder_name=inputVal[1]
        rename_folder=inputVal[2]
        old_path=inputpath+os.sep+folder_name
        rename_path=inputpath+os.sep+rename_folder
        self.f.write(space+"old_path="+old_path)
        self.f.write(space+"rename_path="+rename_path)
        self.f.write(space+"os.renames(old_path,rename_path)")
        self.f.write(space+"status='Pass'")

    def deleteFolder(self,space,input,*args):
        inputVal=input
        inputpath=inputVal[0]
        folder_name=inputVal[1]
        input_val=inputpath+os.sep+folder_name
        self.f.write(space+"input="+input_val)
        self.f.write(space+"os.rmdir(input)")
        self.f.write(space+"status='Pass'")

class StringOperation:

    def __init__(self,f):
        self.f=f

    def toLowerCase(self,space,input):
        inputVal=input[0]
        self.f.write(space+"input="+inputVal)
        self.f.write(space+"output=input.lower()")
        self.f.write(space+"status='Pass'")

    def toUpperCase(self,space,input):
        inputVal=input[0]
        self.f.write(space+"input="+inputVal)
        self.f.write(space+"output=input.upper()")
        self.f.write(space+"status='Pass'")

    def trim(self,space,input):
        inputVal=input[0]
        self.f.write(space+"input="+inputVal)
        self.f.write(space+"output=input.strip()")
        self.f.write(space+"status='Pass'")

    def left(self,space,input):
        inputVal=input
        self.f.write(space+"input="+inputVal[0])
        self.f.write(space+"index="+inputVal[1])
        self.f.write(space+"output=input[:index]")
        self.f.write(space+"status='Pass'")

    def right(self,space,input):
        inputVal=input
        self.f.write(space+"input="+inputVal[0])
        self.f.write(space+"index="+inputVal[1])
        self.f.write(space+"output=input[-index:]")
        self.f.write(space+"status='Pass'")

    def mid(self,space,input):
        inputVal=input
        self.f.write(space+"input="+inputVal[0])
        self.f.write(space+"output=input[int(len(input)/2)]")
        self.f.write(space+"status='Pass'")

    def getStringLength(self,space,input):
        inputVal=input
        self.f.write(space+"input="+inputVal[0])
        self.f.write(space+"output=len(input)")
        self.f.write(space+"status='Pass'")

    def find(self,space,input):
        inputVal=input
        self.f.write(space+"input="+inputVal[0])
        self.f.write(space+"substring="+inputVal[1])
        self.f.write(space+"output=.find(substring)")
        self.f.write(space+"status='Pass'")

    def replace(self,space,input):
        inputVal=input
        self.f.write(space+"input="+inputVal[0])
        self.f.write(space+"substring="+inputVal[1])
        self.f.write(space+"newsubstring="+inputVal[2])
        self.f.write(space+"output=input.replace(substring,newsubstring)")
        self.f.write(space+"status='Pass'")

    def split(self,space,input):
        inputVal=input
        self.f.write(space+"input="+inputVal[0])
        self.f.write(space+"character="+inputVal[1])
        self.f.write(space+"output=input.split(character)")
        self.f.write(space+"status='Pass'")

    def concatenate(self,space,input):
        inputVal=input
        self.f.write(space+"input="+inputVal)
        self.f.write(space+"output=''.join(input)")
        self.f.write(space+"status='Pass'")

    def getSubString(self,space,input):
        inputVal=input
        self.f.write(space+"input="+inputVal[0])
        index=inputVal[1]
        if '-' in index:
            val = index.split('-')
            self.f.write(space+"low="+int(val[0]))
            self.f.write(space+"high="+int(val[1]))
            self.f.write(space+"output=input[low:high]")
        else:
            self.f.write(space+"index="+int(inputVal[1]))
            self.f.write(space+"output=input[index:]")
        self.f.write(space+"status='Pass'")

    def stringGeneration(self,space,input):
        inputVal=input
        data_type=inputVal[0]
        self.f.write(space+"input="+inputVal[1])
        if data_type=='char':
            self.f.write(space+"output=''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(input))")
        elif data_type=='int':
            self.f.write(space+"output=''.join(random.choice(string.digits) for i in range(input))")
        self.f.write(space+"status='Pass'")

    def typeCast(self,space,input):
        inputVal=input
        self.f.write(space+"input="+inputVal[0])
        to_value=inputVal[1]
        if(to_value=="string"):
            self.f.write(space+"output=input")
        elif(to_value=="int"):
            self.f.write(space+"output=int(float(input))")
        elif(to_value=="float"):
            self.f.write(space+"output=float(input)")
        self.f.write(space+"status='Pass'")

    def verifyValues(self,space,input):
        inputVal=input
        self.f.write(space+"input1="+inputVal[0])
        self.f.write(space+"input2="+inputVal[1])
        self.f.write(space+"output= input1==input2")
        self.f.write(space+"status='Pass' if output else 'Fail'")

    def stop(self,space,*args):
        self.f.write(space+"driver.quit()")
        self.f.write(space+"status='Pass'")

    def getIndexCount(self,space,input):
        self.f.write(space+"input="+input[0])
        self.f.write(space+"output=len(input)")
        self.f.write(space+"status='Pass'")

class DateOperation:

    def __init__(self,f):
        self.f=f
        self.dict1={
            'dd/MM/yyyy': '%d/%m/%Y',
            'MM/dd/yyyy': '%m/%d/%Y',
            'yyyy/MM/dd': '%Y/%m/%d',
            'yyyyMMdd': '%Y%m%d',
            'dd/MM/yy': '%d/%m/%y',
            'MM/dd/yy': '%m/%d/%y',
            'yy/MM/dd': '%y/%m/%d',
            'yyMMdd': '%y%m%d',
            '1yyMMdd': '1%y%m%d',
            '1yy/MM/dd': '1%y/%m/%d',
            'dd/MMM/yyyy': '%d/%b/%Y',
            'MMM/dd/yyyy': '%b/%d/%Y',
            'MMM dd, yyyy': '%b %d, %Y',
            'MMM dd, yyy': '%b %d, %Y',
            'MMM dd,YYYY': '%b %d,%Y',
            'MMMM dd,yyyy': '%B %d,%Y',
            'MMMM dd, yyyy': '%B %d, %Y',
            'HH:mm:ss': '%H:%M:%S',
            'dd/MM/yyyy HH:mm:ss':'%d/%m/%Y %H:%M:%S',
            'MM/dd/yyyy HH:mm:ss': '%m/%d/%Y %H:%M:%S',
            'dd/MMM/yyyy HH:mm:ss': '%d/%b/%Y %H:%M:%S',
            'MMM/dd/yyyy HH:mm:ss':'%b/%d/%Y %H:%M:%S'
            }

    def getCurrentDate(self,space,input):
        if input[0] in self.dict1:
            ret_format=self.dict1[input[0]]
        else:
            ret_format=-1
        self.f.write(space+"ret_format="+ret_format)
        self.f.write(space+"cur_date = datetime.datetime.now()")
        self.f.write(space+"output = cur_date.strftime(ret_format)")
        self.f.write(space+"status='Pass'")
    
    def getCurrentTime(self,space,input):
        if input[0] in self.dict1:
            ret_format=self.dict1[input[0]]
        else:
            ret_format=-1
        self.f.write(space+"ret_format="+ret_format)
        self.f.write(space+"cur_time = datetime.datetime.now()")
        self.f.write(space+"output = cur_time.strftime(ret_format)")
        self.f.write(space+"status='Pass'")

    def getCurrentDateAndTime(self,space,input):
        if input[0] in self.dict1:
            ret_format=self.dict1[input[0]]
        else:
            ret_format=-1
        self.f.write(space+"ret_format="+ret_format)
        self.f.write(space+"cur_date_time = datetime.datetime.now()")
        self.f.write(space+"output = cur_date_time.strftime(ret_format)")
        self.f.write(space+"status='Pass'")

    def getCurrentDay(self,space,input):
        self.f.write(space+"cur_day = datetime.datetime.now()")
        self.f.write(space+"output = cur_day.strftime('%A')")
        self.f.write(space+"status='Pass'")

    def getCurrentDayDateAndTime(self,space,input):
        self.f.write(space+"cur_day = datetime.datetime.now()")
        self.f.write(space+"output = cur_day.strftime('%A %d/%m/%Y %H:%M:%S')")
        self.f.write(space+"status='Pass'")

    # def dateDifference(self,space,input):
    #     input=input[0].split(';')
    #     inputdata=[0]
    #     date_or_count=input[1]
    #     ret_format=dict1[input[2]]

    #     self.f.write(space+"ret_format="+ret_format)
    #     date1 = datetime.datetime.strptime(input_date, ret_inp_format)
    #     if ret_format == -1:
    #         temp = count - timedelta (int(days))
    #     pass


    # def dateAddition(self,space,input):
    #     pass

    # def monthAddition(self,space,input):
    #     pass

    # def yearAddition(self,space,input):
    #     pass
    
    # def changeDateFormat(self,space,input):
    #     pass

    # def dateCompare(self,space,input):
    #     pass


class FileOperation:

    def __init__(self,f):
        self.f=f

    # def saveFile(self,space,input):

    def createFile(self,space,input):
        ext=input[1].split('.')[1]
        fullpath=input[0]+"/"+input[1]
        if ext == "xls":
            self.f.write(space+"import xlwt")
            self.f.write(space+" wb = xlwt.Workbook()")
            self.f.write(space+"wb.add_sheet(sheet_name)")
            self.f.write(space+"wb.save(fullpath)")
        elif ext == "xlsx":
            self.f.write(space+"from openpyxl import Workbook")
            self.f.write(space+"wb = Workbook()")
            self.f.write(space+"ws = wb.active")
            self.f.write(space+"ws.title = sheet_name")
            self.f.write(space+"wb.save(excel_path)")
        else:
            self.f.write(space+"open(input,'w').close()")
        self.f.write(space+"status='Pass'")

    def renameFile(self,space,input):
        inputval=input
        rename_path=inputval[0]+'/'+inputval[2]
        inputpath=inputval[0]+'/'+inputval[1]
        self.f.write(space+"inputpath="+inputpath)
        self.f.write(space+"rename_path="+rename_path)
        self.f.write(space+"os.rename(inputpath,rename_path)")
        self.f.write(space+"status='Pass'")

    def deleteFile(self,space,input):
        inputval=input
        inputpath=inputval[0]+'/'+inputval[1]
        self.f.write(space+"inputpath="+inputpath)
        self.f.write(space+"os.remove(inputpath)")
        self.f.write(space+"status='Pass'")

    def verifyFileExists(self,space,input):
        inputval=input
        inputpath=inputval[0]+'/'+inputval[1]
        self.f.write(space+"output=os.path.isfile(inputpath)")
        self.f.write(space+"status='Pass' if output else 'Fail'")