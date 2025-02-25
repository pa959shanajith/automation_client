#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      arpit.koolwal
#
# Created:     10-04-2018
# Copyright:   (c) arpit.koolwal 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import system_keywords
import system_constants
import logger
import logging
log = logging.getLogger('system_dispatcher.py')


class SystemDispatcher:

    system_keyword_obj = system_keywords.System_Keywords()

    def __init__(self):
        self.exception_flag=''
        self.action = None

    def dispatcher(self,teststepproperty,input):
        objectname = teststepproperty.objectname
        output = teststepproperty.outputval
        objectname = objectname.strip()
        keyword = teststepproperty.name.lower()
        err_msg=None
        try:
            keyword_dict={
                            'getosinfo': self.system_keyword_obj.getOsInfo,
                            'getallinstalledapps' : self.system_keyword_obj.getAllInstalledApps,
                            'getallprocess' : self.system_keyword_obj.getAllProcess,
                            'executecommand':self.system_keyword_obj.executeCommand
                         }
            result=()
            if input != ['']:
                result = keyword_dict[keyword](input)
            else:
                result = keyword_dict[keyword]()
        except Exception as e:
            logger.print_on_console('Input Error : Provide valid input')
            log.error(e)
        return result

