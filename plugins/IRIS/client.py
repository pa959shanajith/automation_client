# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 09:39:42 2022

@author: byrapuram.reddy
"""
from __future__ import print_function
import requests
import json
import cv2
import base64
from io import BytesIO
import logger
# import numpy as np
# import cv2
from PIL import Image
import readconfig

class api_request():

    def __init__(self):

        self.configvalues = readconfig.configvalues
        self.addr=self.configvalues['ai_server']
        logger.print_on_console(self.addr)
        self.content_type = 'image/jpeg'
        self.headers = {'content-type': self.content_type}


    def aimodel(self,imgPath) :
        
        test_url = self.addr + '/ai/model'
        im_file = BytesIO()
        imgPath.save(im_file, format="png")
        im_bytes = im_file.getvalue()
        im_b64 = base64.b64encode(im_bytes)
        response = requests.post(test_url, data=im_b64,verify = False , timeout = 120)
        coordinates=json.loads(response.text)['coordinates']
        return coordinates

    def extracttext(self,imgPath,booliean) :

        test_url = self.addr + '/text/extract'
        data={'img':imgPath,'message':booliean}
        #response = requests.post(test_url, data=imgPath,verify = False , timeout = None)
        response = requests.post(test_url, json=data,verify = False , timeout = None)
        text_oldrefer=json.loads(response.text)['reference']
        logger.print_on_console(text_oldrefer)
        return text_oldrefer
    
    def tableextract(self,imgPath) :

        test_url = self.addr + '/table/extract'
        data=imgPath
        #response = requests.post(test_url, data=imgPath,verify = False , timeout = None)
        response = requests.post(test_url, data=data,verify = False , timeout = None)
        #logger.print_on_console(response)
        table_data=json.loads(response.text)['reference']
        logger.print_on_console(table_data)
        return table_data


    def image_save(self,imgPath) :

        test_url = self.addr + '/img/save'

        im_file = BytesIO()
        imgPath.save(im_file, format="png")
        im_bytes = im_file.getvalue()
        im_b64 = base64.b64encode(im_bytes)
        response = requests.post(test_url, data=im_b64,verify = False , timeout = None)
        text=json.loads(response.text)['message']

        return text

    def newtextexecute_client(self) :
        
        test_url = self.addr + '/newtext/extract'
        data={"img":"stored in the server"}
        response = requests.post(test_url, data=data,verify = False , timeout = None)
        coordinates=json.loads(response.text)['reference']
        return coordinates

    # def ocr_client(self,imgPath) :


    #     test_url = self.addr + '/text/extract'
        

    #     return text