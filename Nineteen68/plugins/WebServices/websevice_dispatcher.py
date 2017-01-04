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
import webservices
import logger
import ws_constants
class Dispatcher:
    webservice = webservices.WSkeywords()
    def dispatcher(self,tsp,*message):
        keyword=tsp.name
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
                  'getServerCertificate' : self.webservice.getServerCertificate,
                  'setAttributeValue':self.webservice.setAttributeValue,
                  'setHeaderTemplate':self.webservice.setHeaderTemplate
                }
            if keyword in dict.keys():
                if keyword in ['setTagValue','setAttributeValue']:
                    message=list(message)
                    message.append(tsp.objectname)
                return dict[keyword](*message)
            else:
                log.error(ws_constants.METHOD_INVALID)
                err_msg=ws_constants.METHOD_INVALID
                logger.print_on_console(ws_constants.METHOD_INVALID)
        except Exception as e:
            log.error(e)
            log.error(e.msg)
            logger.print_on_console(e.msg)

