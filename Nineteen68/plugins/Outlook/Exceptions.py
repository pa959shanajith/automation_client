#-------------------------------------------------------------------------------
# Name:        exceptions
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     22-09-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def error(e):
    print 'Exception occured is : %s', e
    print 'Type of the exception : %s', type(e)
    print 'Exception args : %s', e.args