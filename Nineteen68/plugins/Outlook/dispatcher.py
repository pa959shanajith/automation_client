#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     22-09-2016
# Copyright:   (c) prudhvi.gujjuboyina 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import Exceptions
import outlook
import Logger
import constants
class Dispatcher:

    def dispatcher(self,keyword,*message):

        try:
            if keyword=='GetEmail':
                self.outook_obj = outlook.OutlookKeywords(message[0],message[1],message[2])
            dict={'GetEmail': self.outook_obj.GetEmail(),
                  'GetFromMailId' : self.outook_obj.GetFromMailId(),
                  'GetAttachmentStatus'    : self.outook_obj.GetAttachmentStatus(),
                  'GetSubject'     : self.outook_obj.GetSubject(),
                  'GetToMailID'  : self.outook_obj.GetToMailID(),
                  'GetBody' : self.outook_obj.GetBody(),
                  'VerifyEmail' : self.outook_obj.VerifyEmail(message)
                }
            if keyword in dict.keys():
                    return dict[keyword]

            else:
                Logger.log(constants.METHOD_INVALID)
        except Exception as e:
            Exceptions.error(e)

