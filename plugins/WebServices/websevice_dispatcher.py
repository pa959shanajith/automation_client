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
        keyword=tsp.name.lower()
        err_msg=None
        result=[constants.TEST_RESULT_FAIL,constants.TEST_RESULT_FALSE,constants.OUTPUT_CONSTANT,err_msg]
        try:
            ws_dict={'setendpointurl': self.webservice.setEndPointURL,
                  'setoperations' : self.webservice.setOperations,
                  'setmethods'    : self.webservice.setMethods,
                  'setheader'     : self.webservice.setHeader,
                  'setwholebody'  : self.webservice.setWholeBody,
                  'executerequest' : self.webservice.executeRequest,
                  'getheader'      : self.webservice.getHeader,
                  'getbody'      : self.webservice.getBody,
                  'addclientcertificate':self.webservice.addClientCertificate,
                  'settagvalue' : self.webservice.setTagValue,
                  'getservercertificate' : self.webservice.getServerCertificate,
                  'settagattribute':self.webservice.setTagAttribute,
                  'setheadertemplate':self.webservice.setHeaderTemplate,
                  'setproxies':self.webservice.setProxies,
                  # Authentication methods
                  'setbasicauth': self.webservice.setBasicAuth,
                  'setoauth2.0': self.webservice.setOAuth2,
                  'setparam':self.webservice.setParam,
                  'setparamvalue':self.webservice.setParamValue
                }
            if keyword in ws_dict.keys():
                if keyword in ['settagvalue','settagattribute','setparamvalue']:
                    message=list(message)
                    message.append(tsp.objectname)
                elif keyword == 'executerequest':
                    message=list(message)
                    message.append(socketIO)

                result= ws_dict[keyword](*message)
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

