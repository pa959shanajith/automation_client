#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:     10-11-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logger
import Exceptions
import pause_display_operation
class Delay_keywords:

    def wait(self,input):
        status=False
        try:
            import time
            if not(input is None and input is ''):
                input=int(input)
                logger.log('wait method started')
                time.sleep(input)
                logger.log('wait method completed')
                status=True
        except Exception as e:
            Exceptions.error(e)
        return status

    def pause(self,*args):
        status=False
        try:
            pause_display_operation.execute()
            status=True
        except Exception as e:
            Exceptions.error(e)
        return status

    def display_variable_value(self,input,*args):
        status=False
        try:
            import time
            if not(input is None and input is ''):
                pause_display_operation.display_value(input)
        except Exception as e:
            Exceptions.error(e)
        return status


