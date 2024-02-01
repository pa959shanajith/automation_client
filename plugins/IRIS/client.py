# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 09:39:42 2022

@author: byrapuram.reddy
"""
from __future__ import print_function
import requests
from requests.auth import HTTPProxyAuth
import json
#import jsonpickle
import cv2
import base64
from io import BytesIO
import logger
import logging
log = logging.getLogger('client.py')
# import numpy as np
# import cv2
from PIL import Image
import readconfig
import constants

class api_request():

    def __init__(self):

        self.configvalues = readconfig.configvalues
        self.proxy_path=constants.PROXY_PATH
        self.conf=open(self.proxy_path,'r')
        self.proxy=json.load(self.conf)
        self.conf.close()
        self.addr=self.configvalues['ai_server']
        #logger.print_on_console(self.addr)
        self.content_type = 'image/jpeg'
        self.headers = {'content-type': self.content_type}
        self.proxyobj=readconfig.readProxyConfig().readRawJson()

        if self.proxy['enabled']=='Enabled':
            self.proxy_url=self.proxyobj['url']
            self.proxy_username=self.proxyobj['username']
            self.proxy_password=self.proxyobj['password']
            self.proxy_auth=HTTPProxyAuth(self.proxy_username,self.proxy_password)
            self.proxies=readconfig.readProxyConfig().readJson()
            # self.proxies={
            #     'http': self.proxy_url,
            #     'https':self.proxy_url,            
            #     }


    def aimodel(self,imgPath) :

        try:
            test_url = self.addr + '/ai/model'
            im_file = BytesIO()
            imgPath.save(im_file, format="png")
            im_bytes = im_file.getvalue()
            im_b64 = base64.b64encode(im_bytes)
            # logger.print_on_console(im_b64)
            if 'enabled' in self.proxy and self.proxy['enabled']=='Enabled':

                response = requests.post(test_url, data=im_b64,proxies=self.proxies)

                # response = requests.post(test_url, data=im_b64,proxies=self.proxies,auth=self.proxy_auth, timeout = 120)

            else:
                response = requests.post(test_url, data=im_b64,verify = False , timeout = 120)



            logger.print_on_console(response.text)
            #coordinates=jsonpickle.decode(response.content)['coordinates']
            coordinates=json.loads(response.text)['coordinates']
            #logger.print_on_console(coordinates)
            log.info('server response is : '+str(response.status_code))
            return coordinates
        
        except Exception as e:
            log.error(e)
            # err_msg = "Error occurred in aimodel execution, Err_Msg : " + str(response.status_code)
            # log.info('server response is : '+str(response.status_code))
            # logger.print_on_console("Error occurred in client and server interaction----",response.status_code)
            # log.error(e)


    def extracttext(self,imgPath,booliean) :

        try:

            test_url = self.addr + '/text/extract'
            data={'img':imgPath,'message':booliean}
            #response = requests.post(test_url, data=imgPath,verify = False , timeout = None)

            if 'enabled' in self.proxy and self.proxy['enabled']=='Enabled':

                response = requests.post(test_url, data=data,proxies=self.proxies)

                # response = requests.post(test_url, data=im_b64,proxies=self.proxies,auth=self.proxy_auth, timeout = 120)

            else:
                response = requests.post(test_url, data=data,verify = False , timeout = 120)



            # response = requests.post(test_url, json=data,verify = False , timeout = None)
            text_oldrefer=json.loads(response.text)['reference']
            #logger.print_on_console(text_oldrefer)
            log.info('server response is : '+str(response.status_code))
            return text_oldrefer
        
        except Exception as e:
            log.error(e)
            err_msg = "Error occurred in extracttext execution, Err_Msg : " + str(response.status_code)
            logger.print_on_console("Error occurred in client and server interaction----",response.status_code)
            log.error(err_msg)
    
    def tableextract(self,imgPath) :

        try:

            test_url = self.addr + '/table/extract'
            data=imgPath
            #response = requests.post(test_url, data=imgPath,verify = False , timeout = None)

            if 'enabled' in self.proxy and self.proxy['enabled']=='Enabled':

                response = requests.post(test_url, data=data,proxies=self.proxies)

                # response = requests.post(test_url, data=im_b64,proxies=self.proxies,auth=self.proxy_auth, timeout = 120)

            else:
                response = requests.post(test_url, data=data,verify = False , timeout = 120)

            # response = requests.post(test_url, data=data,verify = False , timeout = None)
            #logger.print_on_console(response)
            table_data=json.loads(response.text)['reference']
            #logger.print_on_console(table_data)
            log.info('server response is : '+str(response.status_code))
            return table_data
        
        except Exception as e:
            log.error(e)
            err_msg = "Error occurred in table extraction, Err_Msg : " + str(response.status_code)
            logger.print_on_console("Error occurred in client and server interaction----",response.status_code)
            log.error(err_msg)
    
    def getting_text(self,imgPath):

        try:

            test_url = self.addr + '/get/text'

            im_file = BytesIO()
            imgPath.save(im_file, format="png")
            im_bytes = im_file.getvalue()
            im_b64 = base64.b64encode(im_bytes)

            if 'enabled' in self.proxy and self.proxy['enabled']=='Enabled':

                response = requests.post(test_url, data=im_b64,proxies=self.proxies)

                # response = requests.post(test_url, data=im_b64,proxies=self.proxies,auth=self.proxy_auth, timeout = 120)

            else:
                response = requests.post(test_url, data=im_b64,verify = False , timeout = 120)
            # response = requests.post(test_url, data=im_b64,verify = False , timeout = None)

            gettext=json.loads(response.text)['reference']
            log.info('server response is : '+str(response.status_code))
            #logger.print_on_console(gettext)

            return gettext
        
        except Exception as e:
            log.error(e)
            err_msg = "Error occurred in getting text, Err_Msg : " + str(response.status_code)
            logger.print_on_console("Error occurred in client and server interaction----",response.status_code)
            log.error(err_msg)



    def image_save(self,imgPath) :

        try:

            test_url = self.addr + '/img/save'

            im_file = BytesIO()
            imgPath.save(im_file, format="png")
            im_bytes = im_file.getvalue()
            im_b64 = base64.b64encode(im_bytes)
            response = requests.post(test_url, data=im_b64,verify = False , timeout = None)
            text=json.loads(response.text)['message']
            log.info('server response is : '+str(response.status_code))

            return text
        
        except Exception as e:
            log.error(e)
            err_msg = "Error occurred in image save, Err_Msg : " + str(response.status_code)
            logger.print_on_console("Error occurred in client and server interaction----",response.status_code)
            log.error(err_msg)

    def newtextexecute_client(self,imgPath) :


        try:
        
            test_url = self.addr + '/executetext/extract'

            im_file = BytesIO()
            imgPath.save(im_file, format="png")
            im_bytes = im_file.getvalue()
            im_b64 = base64.b64encode(im_bytes)


            if 'enabled' in self.proxy and self.proxy['enabled']=='Enabled':

                response = requests.post(test_url, data=im_b64,proxies=self.proxies)

                # response = requests.post(test_url, data=im_b64,proxies=self.proxies,auth=self.proxy_auth, timeout = 120)

            else:
                response = requests.post(test_url, data=im_b64,verify = False , timeout = 120)




            # response = requests.post(test_url, data=im_b64,verify = False , timeout = None)
            logger.print_on_console(response)
            # data={"img":"stored in the server"}
            #response = requests.post(test_url, data=data,verify = False , timeout = None)
            coordinates=json.loads(response.text)['reference']
            log.info('server response is : '+str(response.status_code))
            return coordinates
        
        except Exception as e:
            log.error(e)
            err_msg = "Error occurred in newtextexecute, Err_Msg : " + str(response.status_code)
            logger.print_on_console("Error occurred in client and server interaction----",response.status_code)
            log.error(err_msg)

    # def ocr_client(self,imgPath) :


    #     test_url = self.addr + '/text/extract'
        

    #     return text