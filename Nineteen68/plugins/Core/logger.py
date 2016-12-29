#-------------------------------------------------------------------------------
# Name:        logger.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     14-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import datetime


import logging


def print_on_console(message,*args):
    ts = time.time()
    sttime = datetime.datetime.fromtimestamp(ts).strftime('%y-%m-%d %H:%M:%S')
    print sttime + ':  CONSOLE: '   + message,''.join(str(i) if (type(i)==unicode or type(i)==str) else  repr(i) for i in args)


def log(message,*args):
    ts = time.time()
    sttime = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%y     %H:%M:%S')
##    debug =  logging.getLevelName('DEBUG')
##    info =  logging.getLevelName('INFO')
##    error =  logging.getLevelName('ERROR')
##    print sttime +  ':    ' + message,''.join(str(i) if (type(i)==unicode or type(i)==str) else  repr(i) for i in args)

##    print sttime + ':      ' + level.upper() + ':    ' + message,''.join(str(i) if (type(i)==unicode or type(i)==str) else  repr(i) for i in args)

##    if info == 'i' and  level =='info' :
####        logging.info(message + ''.join(repr(i) for i in args))
####        print  sttime + ':      ' + level.upper() + ':      ' + (str)( message) + '\n\n'
##        print sttime + ':      ' + level.upper() + ':    ' + message,''.join(repr(i) for i in args)
##    elif info == 'i' and level == 'error':
####        logging.error(message + ''.join(repr(i) for i in args))
####        print  sttime + ':      ' + level.upper() + ':      ' + (str)( message) + '\n\n'
##        print sttime + ':      ' + level.upper() + ':    ' + message,''.join(repr(i) for i in args)
##    elif error == 'e'  and level == 'error'  :
####        logging.error(message + ''.join(repr(i) for i in args))
####        print  sttime + ':      ' + level.upper() + ':      ' + (str)( message) + '\n\n'
##        print sttime + ':      ' + level.upper() + ':    ' + message,''.join(repr(i) for i in args)
##    elif debug == 'd' and level == 'debug':
####        logging.debug(message + ''.join(repr(i) for i in args))
####        print  sttime + ':      ' + level.upper() + ':      ' + (str)( message) + '\n\n'
##        print sttime + ':      ' + level.upper() +':    ' + message,''.join(repr(i) for i in args)
##    elif debug == 'd' and level == 'info':
##        logging.debug(message + ''.join(repr(i) for i in args))
####        print  sttime + ':      ' + level.upper() + ':      ' + (str)( message) + '\n\n'
##        print sttime + ':      ' + level.upper() +':    ' + message,''.join(repr(i) for i in args)
##    elif debug == 'd' and level == 'error':
####        logging.debug(message + ''.join(repr(i) for i in args))
####        print  sttime + ':      ' + level.upper() + ':      ' + (str)( message) + '\n\n'
##        print sttime + ':      ' + level.upper() + ':    ' +message,''.join(repr(i) for i in args)



