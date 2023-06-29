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
        er =[]
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

    def quickNav(self,elem,input_val):
        status = False
        try:
            elem.firstVisibleDate = input_val
            elem.focusDate = input_val
            elem.selectionInterval = input_val+ ',' + input_val
            status = True
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str( e )
            log.error( err_msg )
            logger.print_on_console( 'Error occured in quickNav' )
        return status

    def navigate_to(self, elem, input_val):
        status_flag = False
        fdate = elem.FocusDate
        log.debug("Focused Date is : ",fdate)
        fday = elem.GetWeekDay(str(fdate))
        log.debug("Focused day of the week is : ",fday)
        dday = elem.GetWeekDay(str(input_val))
        log.debug("To focus date is : ",dday)
        horizontal_movement = sap_constants.date_day[fday] - sap_constants.date_day[dday]
        log.debug("Horizontal Movement is : ",horizontal_movement)
        # if pos move right ,if neg move left ,if zero stay there
        try : elem.SelectRange(str(input_val),str(input_val))
        except : pass
        if ( horizontal_movement == 0 ):
            elem.FocusDate
        elif ( horizontal_movement > 0 ):
            elem.FocusDate
            for i in range(0, horizontal_movement):
                win32api.keybd_event(sap_constants.VK_CODE['left_arrow'], 0, 0, 0)#left_arrow
                time.sleep(0.10)
        elif ( horizontal_movement < 0 ):
            elem.FocusDate
            for i in range(0,abs(horizontal_movement)):
                win32api.keybd_event(sap_constants.VK_CODE['right_arrow'], 0, 0, 0)#right_arrow
                time.sleep(0.10)
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
                    win32api.keybd_event(sap_constants.VK_CODE['up_arrow'], 0, 0, 0)#up_arrow
                    time.sleep(0.10)
        elif( vertical_movement < 0 ):
            breakloop_flag = True
            while breakloop_flag :
                if ( elem.FocusDate == str(input_val) ):
                    status_flag = True
                    breakloop_flag = False
                else:
                    win32api.keybd_event(sap_constants.VK_CODE['down_arrow'], 0, 0, 0)#down_arrow
                    time.sleep(0.10)
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
                # get the co-ordinate or position
                if len(args) >= 2:
                    sap_position = args[-1]
                else:
                    sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

                self.lk.setWindowToForeground(sap_id)
                id, ses = self.uk.getSapElement(sap_id, sap_position)
                if ( id and ses ):
                    elem = ses.FindById(id)
                    if ( elem.type == 'GuiShell' and elem.SubType == 'Calendar' ): #identify if its a shell and calender
                        try : elem.SelectWeek( int(input_val[0]), int(input_val[1]) )
                        except Exception as e : log.info('WARNING: Following issue found in SelectWeek ' + str(e))
                        nav = elem.SelectionInterval
                        if (type(nav) == str): nav = nav.split(',')
                        #self.navigate_to(elem, nav[0])
                        self.quickNav(elem,str(nav[0]))
                        del nav
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
        if ( type(input_val[0]) == str and input_val[0].lower() in sap_constants.Month.keys() ) : input_val[0] = sap_constants.Month[input_val[0].lower()]
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
                # get the co-ordinate or position
                if len(args) >= 2:
                    sap_position = args[-1]
                else:
                    sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

                id, ses = self.uk.getSapElement(sap_id, sap_position)
                if ( id and ses):
                    elem = ses.FindById(id)
                    #self.navigate_to(elem, v)
                    self.quickNav(elem,str(v))
                    if ( elem.type == 'GuiShell' and elem.SubType=='Calendar'): #identify if its a shell and calender
                        try : elem.SelectMonth(int(input_val[0]),int(input_val[1]))
                        except Exception as e : log.info('WARNING: Following issue found in SelectMonth ' + str(e))
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
                # get the co-ordinate or position
                if len(args) >= 2:
                    sap_position = args[-1]
                else:
                    sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

                self.lk.setWindowToForeground(sap_id)
                id, ses = self.uk.getSapElement(sap_id, sap_position)
                if ( id and ses):
                    elem = ses.FindById(id)
                    #self.navigate_to(elem, input_val[0])
                    self.quickNav(elem,str(input_val[0]))
                    if ( elem.type == 'GuiShell' and elem.SubType == 'Calendar'): #identify if its a shell and calender
                        try : elem.SelectRange(int(input_val[0]),int(input_val[1]))
                        except Exception as e : log.info('WARNING: Following issue found in Select Range ' + str(e))
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


    def select_todays_date(self, sap_id, *args):
        """
        output : pass/fail
        operation : will select the dates in the given range
        Steps: select todays date by default(REASON: If any date element is not focused , the date functions do not work and throw error: 'Sufficient data not provided')
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        status_flag = False
        try:
            s,r,v,er = self.create_date(sap_id,[date.today().day, date.today().month, date.today().year])
            er, flag = self.date_validator(v)
            if ( flag == True and len(er) == 0 ):
                self.lk.setWindowToForeground(sap_id)
                id, ses = self.uk.getSapElement(sap_id)
                if ( id and ses):
                    elem = ses.FindById(id)
                    if ( elem.type == 'GuiShell' and elem.SubType == 'Calendar'): #identify if its a shell and calender
                        try:
                            #status_flag = self.navigate_to(elem, v)
                            status_flag = self.quickNav(elem,str(v))
                            if( status_flag and elem.FocusDate == str( v ) ):
                                win32api.keybd_event(sap_constants.VK_CODE['enter'], 0, 0, 0)#enter
                                value = v
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            else:
                                err_msg = 'Unable to focus the input date'
                        except Exception as e:
                            log.info( 'WARNING: Following issue found in Select Todays Date ' + str(e))
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
            logger.print_on_console( 'Error occured in Select Todays Date' )
        return status, result, value, err_msg


    def select_date(self, sap_id, input_val, *args):
        """
        input_val : date(YYYYMMDD)
        output : pass/fail
        operation : will select the dates in the given range
        Steps: select todays date by default(REASON: If any date element is not focused , the date functions do not work and throw error: 'Sufficient data not provided')
        """
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        status_flag = False
        value = OUTPUT_CONSTANT
        if ( len(input_val[0]) != 0 ):
            er, flag = self.date_validator(input_val[0])
            try:
                if ( flag == True and len(er) == 0 ):
                    # get the co-ordinate or position
                    if len(args) >= 2:
                        sap_position = args[-1]
                    else:
                        sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

                    self.lk.setWindowToForeground(sap_id)
                    id, ses = self.uk.getSapElement(sap_id, sap_position)
                    if ( id and ses):
                        elem = ses.FindById(id)
                        if ( elem.type == 'GuiShell' and elem.SubType == 'Calendar'): #identify if its a shell and calender
                            #status_flag = self.navigate_to( elem, input_val[0] )
                            status_flag = self.quickNav( elem, str(input_val[0]) )
                            if( status_flag and elem.FocusDate == str( input_val[0]) ):
                                win32api.keybd_event(sap_constants.VK_CODE['enter'], 0, 0, 0)#enter
                                log.info('Selected date : ' + str(input_val[0]))
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            elif( status_flag and elem.FocusDate != str( input_val[0]) ):
                                err_msg = 'Unable to focus the input date'
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
        else:
            status, result, value, err_msg = self.select_todays_date(sap_id)
        return status, result, value, err_msg