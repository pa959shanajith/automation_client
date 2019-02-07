#-------------------------------------------------------------------------------
# Name:        logger.py
# Purpose:      logging on client window
#
# Author:      wasimakram.sutar
#
# Created:     14-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#
# Modified Author: vishvas.a
#
# Created:     13-07-2017
# Copyright:   (c) vishvas.a 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import datetime
import os

from inspect import getframeinfo, stack

def print_on_console(message,*args):
    try:
        ts = time.time()
        sttime = datetime.datetime.fromtimestamp(ts).strftime('%y-%m-%d %H:%M:%S')
        caller = getframeinfo(stack()[1][0])
        filename=os.path.basename(caller.filename)[0:-3]

        resultant=''
        if isinstance(message,bytes): message=message.decode('utf-8')
        elif not isinstance(message,str): message=str(message)
        for values in args:
            if isinstance(values,bytes): values=values.decode('utf-8')
            elif not isinstance(values,str): values=str(values)
            resultant+=values
        print(sttime + ':  CONSOLE: ' +filename + ':'+str(caller.lineno) +' ' + message + resultant)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(e)

def log(message):
    print(message)
