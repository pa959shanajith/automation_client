# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 09:39:42 2022

@author: byrapuram.reddy
"""
from __future__ import print_function
import requests
import json
import base64
from io import BytesIO
# import numpy as np
# import cv2
from PIL import Image
import readconfig

def client(imgPath) :
    configvalues = readconfig.configvalues
    addr=configvalues['ai_server']
    test_url = addr + '/ai/model'
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    im_file = BytesIO()
    imgPath.save(im_file, format="png")
    im_bytes = im_file.getvalue()
    im_b64 = base64.b64encode(im_bytes)
    response = requests.post(test_url, data=im_b64,verify = False , timeout = 120)
    coordinates=json.loads(response.text)['coordinates']
    return coordinates

def image_save(imgPath) :
    configvalues = readconfig.configvalues
    addr=configvalues['ai_server']
    test_url = addr + '/img/save'
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}
    
    im_file = BytesIO()
    imgPath.save(im_file, format="png")
    im_bytes = im_file.getvalue()
    im_b64 = base64.b64encode(im_bytes)
    response = requests.post(test_url, data=im_b64,verify = False , timeout = 120)
    text=json.loads(response.text)['message']

    return text

def execute_client() :
    configvalues = readconfig.configvalues
    addr=configvalues['ai_server']
    test_url = addr + '/aimodel/execute'
    data={"img":"stored in the server"}
    response = requests.post(test_url, data=data,verify = False , timeout = 120)
    coordinates=json.loads(response.text)['coordinates']
    return coordinates


def ocr_client(imgPath) :
    configvalues = readconfig.configvalues
    addr=configvalues['ai_server']
    test_url = addr + '/text/extract'
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    im_file = BytesIO()
    imgPath.save(im_file, format="png")
    im_bytes = im_file.getvalue()
    im_b64 = base64.b64encode(im_bytes)
    response = requests.post(test_url, data=im_b64,verify = False , timeout = 120)
    text=json.loads(response.text)['reference'][0]

    return text