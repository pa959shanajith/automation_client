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

import logging
def error(e):
    print 'Exception occured is : %s', e
    print 'Type of the exception : %s', type(e)
    print 'Exception args : %s', e.args
    logging.debug('MSG: Exception occured is : %s', e)
    logging.debug('MSG: Type of the exception : %s', type(e))
    logging.debug('MSG: Exception args : %s', e.args)


