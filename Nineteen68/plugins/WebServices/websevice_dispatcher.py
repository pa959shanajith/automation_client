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

import webservices
import logger
import ws_constants
import constants
import logging
log = logging.getLogger('websevice_dispatcher.py')
class Dispatcher:
    webservice = webservices.WSkeywords()
    def dispatcher(self,tsp,socketIO,*message):
        keyword=tsp.name
        err_msg=None
        result=[constants.TEST_RESULT_FAIL,constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]
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
                  'setTagAttribute':self.webservice.setTagAttribute,
                  'setHeaderTemplate':self.webservice.setHeaderTemplate
                }
            if keyword in dict.keys():
                if keyword in ['setTagValue','setTagAttribute']:
                    message=list(message)
                    message.append(tsp.objectname)
                elif keyword == 'executeRequest':
                    message=list(message)
                    message.append(socketIO)

                result= dict[keyword](*message)
            else:
                err_msg=ws_constants.METHOD_INVALID
                result[3]=err_msg
        except TypeError as e:
            err_msg=constants.ERROR_CODE_DICT['ERR_INDEX_OUT_OF_BOUNDS_EXCEPTION']
            result[3]=err_msg
        except Exception as e:
            log.error(e)
            logger.print_on_console('Exception at dispatcher')
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        return result

