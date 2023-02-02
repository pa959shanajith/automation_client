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

def client(imgPath) :
    #addr='http://152.67.10.91:80'
    proxies = {'https': 'http://152.67.10.91'}
    addr='https://avoaiapi.avoautomation.com'

    #addr = 'http://localhost:8080'

    test_url = addr + '/ai/model'
    #test_url='https://srv01nineteen68:443/getExecScenario'
    #data_dict = {"configkey" :"123456789" , "executionListId" :"123456789" ,

     #                   "agentName" : "sreenu", "iceInstanceId" : 1}

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    im_file = BytesIO()
    #print(im_file)
    imgPath.save(im_file, format="png")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = base64.b64encode(im_bytes)

    #img = cv2.imread(imgPath)
    
    # encode image as jpeg
    #_, img_encoded = cv2.imencode('.png', img)
    # send http request with image and receive response
    #response = requests.post(test_url, json = data_dict, verify = False, timeout = 120)
    response = requests.post(test_url, data=im_b64,verify = False , timeout = 120)
    # decode response
    #print(response.text)
    #print(json.loads(response.text))

    coordinates=json.loads(response.text)['coordinates']

    return coordinates

def image_save(imgPath) :
    #addr='http://152.67.10.91:80'
    proxies = {'https': 'http://152.67.10.91'}
    addr='https://avoaiapi.avoautomation.com'

    #addr = 'http://localhost:8080'

    test_url = addr + '/img/save'
    #test_url='https://srv01nineteen68:443/getExecScenario'
    #data_dict = {"configkey" :"123456789" , "executionListId" :"123456789" ,

     #                   "agentName" : "sreenu", "iceInstanceId" : 1}

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    im_file = BytesIO()
    #print(im_file)
    imgPath.save(im_file, format="png")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = base64.b64encode(im_bytes)

    #img = cv2.imread(imgPath)
    
    # encode image as jpeg
    #_, img_encoded = cv2.imencode('.png', img)
    # send http request with image and receive response
    #response = requests.post(test_url, json = data_dict, verify = False, timeout = 120)
    response = requests.post(test_url, data=im_b64,verify = False , timeout = 120)
    # decode response
    #print(response.text)
    #print(json.loads(response.text))

    text=json.loads(response.text)['message']

    return text

def execute_client() :
    #addr='http://152.67.10.91:80'
    proxies = {'https': 'http://152.67.10.91'}
    addr='https://avoaiapi.avoautomation.com'

    #addr = 'http://localhost:8080'

    test_url = addr + '/aimodel/execute'
    #test_url='https://srv01nineteen68:443/getExecScenario'
    #data_dict = {"configkey" :"123456789" , "executionListId" :"123456789" ,

     #                   "agentName" : "sreenu", "iceInstanceId" : 1}

    # prepare headers for http request
    #content_type = 'image/jpeg'
    #headers = {'content-type': content_type}

    #img = cv2.imread(imgPath)
    
    # encode image as jpeg
    #_, img_encoded = cv2.imencode('.png', img)

    data={"img":"stored in the server"}
    # send http request with image and receive response
    #response = requests.post(test_url, json = data_dict, verify = False, timeout = 120)
    response = requests.post(test_url, data=data,verify = False , timeout = 120)
    # decode response
    #print(response.text)
    #print(json.loads(response.text))

    coordinates=json.loads(response.text)['coordinates']

    return coordinates


def ocr_client(imgPath) :
    #addr='http://152.67.10.91:80'
    proxies = {'https': 'http://152.67.10.91'}
    
    addr='https://avoaiapi.avoautomation.com'

    #addr = 'http://localhost:8080'

    test_url = addr + '/text/extract'
    #test_url='https://srv01nineteen68:443/getExecScenario'
    #data_dict = {"configkey" :"123456789" , "executionListId" :"123456789" ,

     #                   "agentName" : "sreenu", "iceInstanceId" : 1}

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    im_file = BytesIO()
    #print(im_file)
    imgPath.save(im_file, format="png")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = base64.b64encode(im_bytes)

    #img = cv2.imread(imgPath)
    
    # encode image as jpeg
    #_, img_encoded = cv2.imencode('.png', img)
    # send http request with image and receive response
    #response = requests.post(test_url, json = data_dict, verify = False, timeout = 120)
    response = requests.post(test_url, data=im_b64,verify = False , timeout = 120)
    # decode response
    #print(response.text)
    #print(json.loads(response.text))

    text=json.loads(response.text)['reference'][0]

    return text