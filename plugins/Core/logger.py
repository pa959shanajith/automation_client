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
import sys
# from colorama import Fore, Style, init as init_colorama
from inspect import getframeinfo, stack

def print_on_console(message,*args, **kwargs):
    try:
        ts = time.time()
        sttime = datetime.datetime.fromtimestamp(ts).strftime('%y-%m-%d %H:%M:%S')
        try:
            caller = getframeinfo(sys._getframe(-1))
            filename=os.path.basename(caller.filename)[0:-3]
            if filename == 'logger':
                caller = getframeinfo(sys._getframe(1))
                filename=os.path.basename(caller.filename)[0:-3]
            filename = filename + ':'+str(caller.lineno) +' '
        except ValueError:
            filename = ''

        resultant=''
        style1=''
        if isinstance(message,bytes): message=message.decode('utf-8')
        elif not isinstance(message,str): message=str(message)
        for values in args:
            if isinstance(values,bytes): values=values.decode('utf-8')
            elif not isinstance(values,str): values=str(values)
            resultant+=values
        msg_part_1 = sttime + ':  CONSOLE: ' + filename
        msg_part_2 = message + resultant
        # if 'color' in kwargs:
        #     if os.environ["ice_mode"] == "gui":
        #         sys.stdout.write(msg_part_1)
        #         sys.stdout.write_color(msg_part_2 + os.linesep, kwargs['color'])
        #     else:
        #         if(kwargs['color']=="RED"): style1=Fore.RED
        #         elif(kwargs['color']=="GREEN"): style1=Fore.GREEN
        #         elif(kwargs['color']=="YELLOW"): style1=Fore.YELLOW
        #         print(msg_part_1 + style1 + msg_part_2) # + Style.RESET_ALL)
        # else:
        print(msg_part_1 + msg_part_2)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(e)

def log(message):
    print(message)
