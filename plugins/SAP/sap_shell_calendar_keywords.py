#-------------------------------------------------------------------------------
# Name:         SAP_Shell_Calender_keywords
# Purpose:      Handling SAP-Shell-Calender elements
#
# Author:       anas.ahmed
#
# Created:      03-01-2020
# Copyright:    (c) anas.ahmed 2020
# Licence:      <your licence>
#-------------------------------------------------------------------------------
import sap_constants
from constants import *
import logger
from saputil_operations import SapUtilKeywords
from sap_launch_keywords import Launch_Keywords
import logging
import win32api
import time
from datetime import date
log = logging.getLogger("sap_shell_calendar_keywords.py")

"""
In-built functions for calender shell objects (common things : <date> format: YYYYMMDD):
1.GetColor(<date(str)>)
2.GetColorInfo(<output of get GetColor(int)>)
3.GetDateTooltip(<date(str)>)
4.GetDay(<date(str)>)
5.GetMonth(<date(str)>)
6.GetWeekday(<date(str)>)
7.GetWeekNumber(<date(str)>)
8.GetYear(<date(str)>)
9.IsWeekend(<date(str)>)
10.SelectWeek(<week(int)>,<year(int)>)
11.SelectRange(<From date(int)>,<To date(int)>)
12.SelectMonth(<month(int)>,<year(int)>)
13.SelectContextMenuItem(<Fcode(str)>)
14.SelectContextMenuItemByPosition(<PositionDesc(str)>)
15.SelectContextMenuItemByText(<Text(str)>)
16.ContextMenu(<CtxMenuId(int)>,<CtxMenuCellRow(int)>,<CtxMenuCellCol(int)>,<DateBegin(str)>,<DateEnd(str)>)
"""


Month = {'jan' : 1,'january' : 1,
        'feb' : 2,'february' : 2,
        'mar' :3,'march' :3,
        'apr' :4,'april' :4,
        'may' :5,
        'jun' :6,'june' :6,
        'jul' :7,'july' :7,
        'aug' :8,'august' :8,
        'sept' :9,'september' :9,
        'oct' :10,'october' :10,
        'nov' :11,'november' :11,
        'dec' :12,'december' :12}

date_day = { 'MO':1,'TU':2,'WE':3,'TH':4,'FR':5,'SA':6,'SU':7 }

flag_message = ['ERROR: Given date is of incorrect format/value',
                'Date value is not an integer',
                'Month value is incorrect',
                'Day value is incorrect',
                'Day value is incorrect for given month/year',
                'Year value is not an integer',
                'Week value is not an integer']

class Shell_Calendar_Keywords():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()


    def date_validator(self, given_date):
        """validates if the given date is of correct format(YYYYMMDD) and of correct value(int)"""
        """returns error message and flag"""
        flag = False
        er = []
        try:
            if( int(given_date) ): #given date is an integer
                year = int(given_date[:4]) #year is an integer
                month = int(given_date[4:6]) #month is an integer
                if ( month <= 12 and month >= 1 ):
                    day = int(given_date[6:8]) #day is an integer
                    if( day <= 31 and day >= 1 ):
                        if( month in [1, 3, 5, 8, 10, 12] ):# months with  31 days
                            flag = True
                        elif( month in [4, 6, 7, 9, 11] and day <= 30 ):# months with  30 days
                            flag = True
                        elif( month == 2 and day <= 28 ):# sad feb :'(
                            flag = True
                        else: er.append(flag_message[4])
                    else : er.append(flag_message[3])
                else : er.append(flag_message[2])
            else : er.append(flag_message[1])
        except :
            er.append(flag_message[0])
        return er,flag

    def create_date(self, sap_id, input_val, *args):
        """
        input : day;month;year
        output : returns date in YYYYMMDD format
        operation : returns created date
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        flag = [False,False,False]
        flag_message = ['Day value is not an integer','Month value is not an integer','Year value is not an integer']
        er=[]
        for i in range(0,len(input_val)):#check if input values are of int type
            try:
                if( int(input_val[i]) ):
                    flag[i] = True
            except : er.append(flag_message[i])
        try:
            if ( flag[0] == True and flag[1] == True and flag[2] == True):
                self.lk.setWindowToForeground(sap_id)
                id, ses = self.uk.getSapElement(sap_id)
                if ( id and ses):
                    elem = ses.FindById(id)
                    if ( elem.type == 'GuiShell' and elem.SubType=='Calendar'): #identify if its a shell and calender
                        value = elem.CreateDate(int(input_val[0]),int(input_val[1]),int(input_val[2]))
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = 'Element is not a shell-calender object'
                else:
                    err_msg = sap_constants.ELELMENT_NOT_FOUND
            else:
                err_msg = 'Wrong input data provided error : ' + str(er[:])[1:len(str(er))-1]
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str( e )
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Create Date' )
        return status, result, value, err_msg

    def navigate_to(self, elem, input_val):
        status_flag = False
        fdate = elem.FocusDate
        fday = elem.GetWeekDay(str(fdate))
        dday = elem.GetWeekDay(str(input_val))
        horizontal_movement = date_day[fday] - date_day[dday]
        # if pos move right ,if neg move left ,if zero stay there
        try : elem.SelectRange(str(input_val),str(input_val))
        except : pass
        if ( horizontal_movement == 0 ):
            elem.FocusDate
        elif ( horizontal_movement > 0 ):
            elem.FocusDate
            for i in range(0,horizontal_movement):
                win32api.keybd_event(VK_CODE['left_arrow'], 0,0,0)#left_arrow
                time.sleep(0.20)
        elif ( horizontal_movement < 0 ):
            elem.FocusDate
            for i in range(0,abs(horizontal_movement)):
                win32api.keybd_event(VK_CODE['right_arrow'], 0,0,0)#right_arrow
                time.sleep(0.20)
        #if focusdate is lesser or greater that date to focus
        fdate = elem.FocusDate
        vertical_movement = int(fdate) - int(input_val)
        # if pos move up ,if neg move down ,if zero stay there
        if ( vertical_movement == 0 ):
            status_flag = True
        elif( vertical_movement > 0 ):
            breakloop_flag = True
            while breakloop_flag :
                if ( elem.FocusDate == str(input_val) ):
                    status_flag = True
                    breakloop_flag = False
                else:
                    win32api.keybd_event(VK_CODE['up_arrow'], 0,0,0)#up_arrow
                    time.sleep(0.20)
        elif( vertical_movement < 0 ):
            breakloop_flag = True
            while breakloop_flag :
                if ( elem.FocusDate == str(input_val) ):
                    status_flag = True
                    breakloop_flag = False
                else:
                    win32api.keybd_event(VK_CODE['down_arrow'], 0,0,0)#down_arrow
                    time.sleep(0.20)
        return status_flag

    def select_week(self, sap_id, input_val, *args):
        """
        input : week(number);year(YYYY)
        output : pass/fail
        operation : will select the given week
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        flag = [False,False]
        er=[]
        for i in range(0,len(input_val)):#check if input values are of int type
            try:
                if( int(input_val[i]) ):
                    flag[i] = True
            except : er.append(flag_message[i])
        try:
            if ( flag[0] == True and flag[1] == True ):
                self.lk.setWindowToForeground(sap_id)
                id, ses = self.uk.getSapElement(sap_id)
                if ( id and ses ):
                    elem = ses.FindById(id)
                    if ( elem.type == 'GuiShell' and elem.SubType == 'Calendar' ): #identify if its a shell and calender
                        try : elem.SelectWeek( int(input_val[0]), int(input_val[1]) )
                        except Exception as e : log.info('WARNING: Following issue found in SelectWeek ', e)
                        self.navigate_to(elem, elem.SelectionInterval[0])
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else : err_msg = 'Element is not a shell-calender object'
                else : err_msg = sap_constants.ELELMENT_NOT_FOUND
            else : err_msg = 'Wrong input data provided error : '+str(er[:])[1:len(str(er))-1]
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str( e )
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Select Week' )
        return status, result, value, err_msg


    def select_month(self, sap_id, input_val, *args):
        """
        input : month(can be integer or string or month relative substring(Eg: jan,feb, etc));year(YYYY)
        output : pass/fail
        operation : will select the given month
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        flag = [False,False]
        er=[]
        #---------month
        if ( type(input_val[0]) == str and input_val[0].lower() in Month.keys() ) : input_val[0] = Month[input_val[0]]
        try:
            if ( int(input_val[0]) <= 12 and int(input_val[0]) >= 1): flag[0] = True
            else : er.append(flag_message[2])
            if ( int(input_val[1]) ): flag[1]=True
            else : er.append(flag_message[5])
        except : er.append(flag_message[0])
        try:
            if ( flag[0] == True and flag[1] == True ):
                s,r,v,e = self.create_date(sap_id,['01',input_val[0],input_val[1]]) #get 1st of month/year
                self.lk.setWindowToForeground(sap_id)# to navigate to the start date
                id, ses = self.uk.getSapElement(sap_id)
                if ( id and ses):
                    elem = ses.FindById(id)
                    self.navigate_to(elem, v)
                    if ( elem.type == 'GuiShell' and elem.SubType=='Calendar'): #identify if its a shell and calender
                        try : elem.SelectMonth(int(input_val[0]),int(input_val[1]))
                        except Exception as e : log.info('WARNING: Following issue found in SelectMonth ', e)
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else : err_msg = 'Element is not a shell-calender object'
                else : err_msg = sap_constants.ELELMENT_NOT_FOUND
            else : err_msg = 'Wrong input data provided error : '+str(er[:])[1:len(str(er))-1]
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str( e )
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Select Month' )
        return status, result, value, err_msg

    def select_range(self, sap_id, input_val, *args):
        """
        input_val : 'from' date (YYYYMMDD), 'to' date (YYYYMMDD)
        output : pass/fail
        operation : will select the dates in the given range
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        flag = [False, False]
        flag_message = ['"From" value is incorrect', '"To" value is incorrect']
        er = []
        for i in range(0, len(input_val)):#check if input values are of int type
            temp_er, temp_flag = self.date_validator(input_val[i])
            if (len(temp_er) == 0 and temp_flag == True ) : flag[i] = temp_flag
            else : er.append('ERROR_MSG : ' + flag_message[i] + ', Tracked : ' + str(temp_er[:])[1:len(str(temp_er))-1])
        try:
            if ( flag[0] == True and flag[1] == True ):
                self.select_date(sap_id,input_val)#to navigate to start date
                self.lk.setWindowToForeground(sap_id)
                id, ses = self.uk.getSapElement(sap_id)
                if ( id and ses):
                    elem = ses.FindById(id)
                    if ( elem.type == 'GuiShell' and elem.SubType == 'Calendar'): #identify if its a shell and calender
                        try : elem.SelectRange(int(input_val[0]),int(input_val[1]))
                        except Exception as e : log.info('WARNING: Following issue found in SelectWeek ', e)
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else : err_msg = 'Element is not a shell-calender object'
                else : err_msg = sap_constants.ELELMENT_NOT_FOUND
            else : err_msg = 'Wrong input data provided error : ' + str(er[:])[1:len(str(er))-1]
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str( e )
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Select Range' )
        return status, result, value, err_msg


    def select_date(self, sap_id, input_val, *args):
        """
        input_val : date(YYYYMMDD)
        output : pass/fail
        operation : will select the dates in the given range
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        er, flag = self.date_validator(input_val[0])
        status_flag = False
        try:
            if ( flag == True and len(er) == 0 ):
                self.lk.setWindowToForeground(sap_id)
                id, ses = self.uk.getSapElement(sap_id)
                if ( id and ses):
                    elem = ses.FindById(id)
                    if ( elem.type == 'GuiShell' and elem.SubType == 'Calendar'): #identify if its a shell and calender
                        try:
                            status_flag = self.navigate_to(elem,input_val[0])
                            if( status_flag and elem.FocusDate == str(input_val[0]) ):
                                win32api.keybd_event(VK_CODE['enter'], 0,0,0)#enter
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            elif(status_flag and elem.FocusDate != str(input_val[0]) ):
                                err_msg = 'Unable to focus the input date'
                        except Exception as e:
                            log.info('WARNING: Following issue found in SelectMonth ',e)
                    else : err_msg = 'Element is not a shell-calender object'
                else : err_msg = sap_constants.ELELMENT_NOT_FOUND
            else : err_msg = 'Wrong input data provided error : ' + str(er[:])[1:len(str(er))-1]
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str( e )
            log.error( err_msg )
            logger.print_on_console( 'Error occured in Select Date' )
        return status, result, value, err_msg