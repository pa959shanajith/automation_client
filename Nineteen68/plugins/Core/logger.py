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

        isunicode = False
        #for loop to check if the arguments is containing unicode value
        # isunicode is updated if the arguments contain a unicode
        for values in args:
            if isinstance(values, str):
                isunicode = True
        if not isinstance(message,str) and not isunicode:
            print(sttime + ':  CONSOLE: ' +filename+':'+str(caller.lineno) +' ' +str(message),''.join(str(i) if (type(i)==str or type(i)==str) else  repr(i) for i in args))
        else:
            # code checks if the value has a unicode and appends accordingly
            resultant=''
            for values in args:
                if not isinstance(values,str):
                    values=str(values)
                if not isinstance(message,str):
                    message=str(message)
                resultant=resultant+values
            print(sttime + ':  CONSOLE: ' +filename+':'+str(caller.lineno) +' ' + message + resultant)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(e)

def log(message):
    print(message)




