#-------------------------------------------------------------------------------
# Name:        Exceptions.py
# Purpose:     To display exception details like message,printstcktrace,name of the exception
#
# Author:      wasimakram.sutar
#
# Created:     21-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys,os
def error(e):
    print 'Exception occured is : %s', e
    print 'Type of the exception : %s', type(e)
    print 'Exception args : %s', e.args
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print 'Line number',fname, exc_tb.tb_lineno
    return type(e)


