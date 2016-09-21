#-------------------------------------------------------------------------------
# Name:        Dispatcher.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     21-09-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import Exceptions
import Webservices
import Logger
import WSConstants
class Dispatcher:
    webservice = Webservices.WSkeywords()
    def dispatcher(self,keyword,*message):
        try:
            dict={'setEndPointURL': self.webservice.setEndPointURL,
                  'setOperations' : self.webservice.setOperations,
                  'setMethods'    : self.webservice.setMethods,
                  'setHeader'     : self.webservice.setHeader,
                  'setWholeBody'  : self.webservice.setWholeBody,
                  'executeRequest' : self.webservice.executeRequest,
                  'getHeader'      : self.webservice.getHeader,
                  'getBody'      : self.webservice.getBody,
                  'addClientCertificate':self.webservice.addClientCertificate,
                  'setTagValue' : self.webservice.setTagValue,
                  'getServerCertificate' : self.webservice.getServerCertificate
                }
            if keyword in dict.keys():
                return dict[keyword](*message)
            else:
                Logger.log(WSConstants.METHOD_INVALID)
        except Exception as e:
            Exceptions.error(e)

