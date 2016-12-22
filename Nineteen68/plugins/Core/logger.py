#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     14-09-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def log(message,*args):

	#Printing variable number of argumnents in loggers
    print message,''.join(str(i) if (type(i)==unicode or type(i)==str) else  repr(i) for i in args)


