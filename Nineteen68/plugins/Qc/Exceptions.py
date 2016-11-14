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

def error(e):
    print 'Exception occured is : %s', e
    print 'Type of the exception : %s', type(e)
    print 'Exception args : %s', e.args


