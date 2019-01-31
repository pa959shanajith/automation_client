#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pavan.nayak
#
# Created:     08-12-2016
# Copyright:   (c) pavan.nayak 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import mobile_key_objects
##import androidwebserver


import ast
import json
import re
import webconstants_MW
global count
count=''
accessContext=''
accessContextParent = ''
##pathParent = ''
access=''
index=0
k = 0
cordinates = []
states = []
objectDict = {}
objectDictWithNameDesc={}
activeframename=''
deletedobjectlist=[]

def clientresponse():
    clientresp=[]

    if(mobile_key_objects.keyword_output[0] != ''):
        clientresp.append({
            "keywordStatus" : mobile_key_objects.keyword_output[0],
            "keywordValue" : mobile_key_objects.keyword_output[1],
            "keywordMessage" : mobile_key_objects.custom_msg
        })
    else:
        mobile_key_objects.custom_msg.append[:]
        mobile_key_objects.custom_msg.append(webconstants_MW.MSG_ELEMENT_NOT_FOUND)
        clientresp.append({
            "keywordMessage" : mobile_key_objects.custom_msg
        })

    print('RESPONSE IS', str(clientresp))
    return str(clientresp)


def cleardata():
    try:
        del mobile_key_objects.keyword_input[:]
        del mobile_key_objects.keyword_output[:]
        if mobile_key_objects.custom_msg:
            del mobile_key_objects.custom_msg[:]
    except Exception as e:
        log.error(e)