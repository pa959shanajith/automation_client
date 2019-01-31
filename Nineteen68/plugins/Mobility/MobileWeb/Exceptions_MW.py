#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pavan.nayak
#
# Created:     28-11-2016
# Copyright:   (c) pavan.nayak 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def error(e):
    print('Exception occured is : %s', e)
    print('Type of the exception : %s', type(e))
    print('Exception args : %s', e.args)
    return type(e)