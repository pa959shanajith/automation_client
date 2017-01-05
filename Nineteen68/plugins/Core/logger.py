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

import os
import logging

from inspect import getframeinfo, stack

def print_on_console(message,*args):
    ts = time.time()
    sttime = datetime.datetime.fromtimestamp(ts).strftime('%y-%m-%d %H:%M:%S')
    caller = getframeinfo(stack()[1][0])
    filename=os.path.basename(caller.filename)
    print sttime + ':  CONSOLE: ' +filename+':'+str(caller.lineno) +' ' +str( message),''.join(str(i) if (type(i)==unicode or type(i)==str) else  repr(i) for i in args)




