#-------------------------------------------------------------------------------
# Name:        xml_operations.py
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     02-11-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import xml.etree.ElementTree as ET
import ast
import logger
from generic_constants import *
import core_utils

import json
import logging
from constants import *
from lxml import etree
log = logging.getLogger('xml_operations.py')
class XMLOperations():

    def build_dict(self,json_obj):
     keys={}
     if isinstance(json_obj,dict):
      for key,value in list(json_obj.items()):
         if isinstance(value,dict):
            keys[key]=value
            keys.update(self.build_dict(value))
         elif isinstance(value,list):
             keys[key]=value
             log.debug(key,value)
             val=None
             if len(value)>0:
                val=self.build_dict(value[0])
             if val!=None:
                keys.update(val)
         else:
            keys[key]=value
      return keys


    def get_block_count(self,input_string,input_tag,*args):
        """
        def : get_block_count
        purpose : get the count of blocks present in the input XML
        param : inputs : 1. xml 2. tag name
        return : pass,true / fail,false, block count

        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        block_count = None
        block_number=-1
        err_msg=None
        exception_json=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:

            encoded_inp_string=input_string
            json_obj=None
            if isinstance(input_string,str):
                encoded_inp_string=input_string.encode('utf-8')
            try:
                json_obj=json.loads(encoded_inp_string)
                if len(args)>0:
                    block_number=args[0]
            except Exception as e:
               try:
                    json_obj=ast.literal_eval(encoded_inp_string)
               except Exception as e:
                    log.error(e)
                    exception_json=e

##            print json_obj
            if json_obj != None:
                #json logic
                json_obj_dict=self.build_dict(json_obj)
                block = input_tag.split('.')
                number = block_number.split(',')
                log.info('Json Input:',json_obj_dict)
                log.info('Block:',block)
                log.info('Block_Number:',number)
                block_count = 0
                if len(block)==1:
                    if block[0] in json_obj_dict:
                        block_count=1
                    else:
                        log.debug("Key Not Found")
                        err_msg=ERR_XML
                else:
                    for i in range(0,len(block)-1):
                        if(block[i] in json_obj_dict and isinstance(json_obj_dict,dict)):
                            json_obj_dict=json_obj_dict[block[i]]
                        elif(isinstance(json_obj_dict,list)):
                            if int(number[i])-1 != -1:
                                json_obj_dict=json_obj_dict[int(number[i])-1]
                            else:
                                json_obj_dict=json_obj_dict[0]
                    try:
                        if isinstance(json_obj_dict,dict) and block[i+1] in json_obj_dict:
                            block_count=1
                        elif isinstance(json_obj_dict,list):
                            if int(number[i+1])-1 != -1:
                                log.debug('Finding key in given index')
                                json_obj_dict=json_obj_dict[int(number[i])-1]
                                if(block[i+1] in json_obj_dict):
                                    block_count=1
                            else:
                                log.debug('Finding count keys in list')
                                for j in json_obj_dict:
                                    if block[i+1] in j:
                                        block_count+=1
                    except Exception as e:
                        log.debug(e)
                        log.debug('Number of index doesnot match number of key blocks')
                        err_msg=ERR_XML
                if(block_count>0 and err_msg == None):
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
                    log.info("Number of blocks in input Json :", block_count)
                    logger.print_on_console("Number of blocks in input Json:  ",block_count)

            else:
                root = ET.fromstring(encoded_inp_string)
                log.debug('Root object created with input string')
                items=[]
                ##vishvas.a 17/06/06 Defect #578 ALM
                #this condition checks if the XML type received is SOAP type
                #if true then "items" tag names are added using looping
                #else the regular flow continues
                if 'Envelope' in root.tag and root.tag.split('}')[1] == 'Envelope':
                    for elem in root.iter():
                        tag = elem.tag.split('}')[1]
                        if tag == input_tag:
                            items.append(tag)
                else:
    ##                items = root.getiterator(str(input_tag))
                    items = list(root.getiterator(input_tag))
                    log.debug(items)
    ##            items = root.getiterator(str(input_tag))
                log.debug('Getting children node from the root')
                if len(items) > 0:
                    log.debug('There are children in the root node, get the total number of children')
                    block_count = len(items)
    ##                log.info('Number of blocks in input XML :'+ str( block_count))
                    log.info('Number of blocks in input XML :', block_count)
                    logger.print_on_console("Number of blocks in input XML:  ",block_count)
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE





        except Exception as e:
            log.error(e)
            if isinstance(e,ET.ParseError):
                err_msg=ERR_XML
            elif isinstance(exception_json,ValueError):
                err_msg="Invalid json input"

            else:
                err_msg=EXCEPTION_OCCURED
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        log.info(RETURN_RESULT)
        return status,methodoutput,block_count,err_msg

    def get_tag_value(self,input_string,block_number,input_tag,child_tag,*args):
        """
        def : get_tag_value
        purpose : get_tag_value is used to get the Tag Value of the specified tag in the given XML
        param : inputs : 1. xml 2. block_number 3.input_tag 4. child_tag
        return : pass,true / fail,false, tagvalue

        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        block_count = 0
        invalidinput = False
        err_msg=None
        tagvalue = None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
##            root = ET.fromstring(str(input_string))
            if isinstance(input_string,str):
                root = ET.fromstring(input_string.encode('utf-8'))
            else:
                root = ET.fromstring(input_string)
            log.debug('Root object created with input string')
            items=[]
            ##vishvas.a 17/06/06 Defect #578 ALM
            #this condition checks if the XML type received is SOAP type
            #if true then "items" are added using looping
            #else the regular flow continues
            if 'Envelope' in root.tag and root.tag.split('}')[1] == 'Envelope':
                for elem in root.iter():
                    tag = elem.tag.split('}')[1]
                    if tag == input_tag:
                        items.append(elem)
            else:
##                items = root.getiterator(str(input_tag))
                items = list(root.getiterator(input_tag))
            log.debug(items)
            log.debug('Getting children node from the root')
            if len(items) > 0:
                log.debug('There are children in the root node, get the total number of children')
                block_count = len(items)
                block_number = int(block_number)
                block = items[block_number-1].getchildren()
##                log.info('Block number: ' + str(block_number))
                log.info('Block number: ')
                log.info(block_number)
                if len(block)==0:
                    block=[items[0]]
                list_tag=[]
                for child in block:
                    log.info('Iterating child in the block')
                    # added condition in 'or' for SOAP types
##                    if child.tag == str(child_tag) or ('}' in child.tag
##                                and child.tag.split('}')[1] == str(child_tag)):
                    if child.tag == child_tag or ('}' in child.tag
                        and child.tag.split('}')[1] == child_tag):
                        log.info('Child matched with the input child tag')
                        if len(args)>0:
                            attribute=args[0]
                            attribute_dict=child.attrib
                            if attribute in attribute_dict:
                                tagvalue=attribute_dict[attribute]
                                logger.print_on_console('Tag Attribute : ',attribute, ' Tag Value : ',tagvalue)
                                log.info('Got the child attribute value and stored in tagvalue')
                                log.info(STATUS_METHODOUTPUT_UPDATE)
                                status = TEST_RESULT_PASS
                                methodoutput = TEST_RESULT_TRUE
                            else:
                                logger.print_on_console('Invalid attribute key')
                                log.info('Invalid attribute key')


                        else:
                            tagvalue =  child.text
                            logger.print_on_console('Tag : ',input_tag, ' Tag Value : ',tagvalue)
                            log.info('Got the child text value and stored in tagvalue')
                            log.info(STATUS_METHODOUTPUT_UPDATE)
                            status = TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                        list_tag.append(tagvalue)
                    else:
                        invalidinput = True
                if status == TEST_RESULT_FAIL:
                    err_msg=INVALID_INPUT + ' Please check the input tag'
        except Exception as e:
            log.error(e)
            if isinstance(e,ValueError):
                err_msg=ERR_XML_BLOCK
            elif isinstance(e,ET.ParseError):
                err_msg=ERR_XML
            else:
                err_msg=EXCEPTION_OCCURED
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        log.info(RETURN_RESULT)
        if len(list_tag) <=1:
            tagvalue=list_tag[0]
        else:
            tagvalue=list_tag
        return status,methodoutput,tagvalue,err_msg

    def get_block_value(self,input_string,block_number,input_tag):
        """
        def : get_block_value
        purpose : get_block_value is used to get the Block Value of the specified tag in the given XML
        param : inputs : 1. xml 2. input_tag 3.block_number
        return : pass,true / fail,false, blockvalue

        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        block_count = 0
        blockvalue = None
        exception_json=None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            encoded_inp_string=input_string
            json_obj=None
            if isinstance(input_string,str):
                encoded_inp_string=input_string.encode('utf-8')
            try:
                json_obj=json.loads(encoded_inp_string)

            except Exception as e:
                try:
                    json_obj=ast.literal_eval(encoded_inp_string)
                except Exception as e:
                    log.error(e)
                    exception_json=e


            if json_obj != None:
                #json logic
                json_obj_dict=self.build_dict(json_obj)
                if(input_tag in json_obj_dict):
                    blockvalue = []
                    json_value=json_obj_dict[input_tag]
                    block_count=len(json_value)
                    block_number = int(block_number)
                    if(block_count>0 and block_number>0):
                        if isinstance(json_value,dict):
                            tag_value=list(json_value.values())
                            log.info('Tag value is ')
                            log.info(tag_value)
                            if len(tag_value)>=block_number:
                                blockvalue=tag_value[block_number-1]
                            else:
                                err_msg='Invalid block_number'
                        elif isinstance(json_value,list):
                            if len(json_value)>=block_number:
                                blockvalue=json_value[block_number-1]
                            else:
                                err_msg='Invalid block_number'
                        elif isinstance(json_value,str) or isinstance(json_value,str):
                            blockvalue=json_value

                        log.info('Block value is ',blockvalue)
                        logger.print_on_console("Block value is ",blockvalue)
                        if len(blockvalue)>0:
                            status = TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                    else:
                        err_msg='Tag value empty/Invalid block_number'
                else:
                    err_msg=ERR_XML
            else:
                root = ET.fromstring(input_string)
                log.debug('Root object created with input string')
                blocks=[]
                ##vishvas.a 17/06/06 Defect #578 ALM
                #this condition checks if the XML type received is SOAP type
                #if true then "blocks" are added using looping
                #else the regular flow continues
                if 'Envelope' in root.tag and root.tag.split('}')[1] == 'Envelope':
                    for elem in root.iter():
                        tag = elem.tag.split('}')[1]
                        if tag == input_tag:
                            blocks.append(elem)
                else:
                    blocks = list(root.getiterator(input_tag))
                log.debug('Getting children node from the root')
                log.debug(blocks)
                if len(blocks) > 0:
                    blockvalue = []
                    log.debug('There are children in the root node, get the total number of children')
                    block_count = len(blocks)
                    block_number = int(block_number)
                    log.info('Block number: ',block_number)
                    block = blocks[block_number-1].getchildren()
                    log.info('Iterating child in the block')
                    for child in block:
                        log.info('Child text :',child.text)
                        if '}' in child.tag:
                            if child.text != None:
                                blockvalue.append(  '<' + child.tag.split('}')[1]  + '>' + child.text +  '</' + child.tag.split('}')[1]  + '>')
                            else:
                                blockvalue.append(  '<' + child.tag.split('}')[1]  + '/>')
                        else:
                            blockvalue.append(  '<' + child.tag + '>' + child.text +  '</' + child.tag + '>')
                    status = TEST_RESULT_PASS
                    methodoutput = TEST_RESULT_TRUE
                    log.info(STATUS_METHODOUTPUT_UPDATE)
                    if status == TEST_RESULT_FAIL:
                        log.info(INVALID_INPUT + ' Please check the input tag' )
        except Exception as e:
            log.error(e,exc_info=True)
            if isinstance(e,ValueError):
                err_msg=ERR_XML_BLOCK
            elif isinstance(e,ET.ParseError):
                err_msg=ERR_XML
            elif isinstance(exception_json,ValueError):
                err_msg='Invalid Json format'
            else:
                import traceback
                traceback.print_exc()
                err_msg=EXCEPTION_OCCURED
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        log.info(RETURN_RESULT)
        return status,methodoutput,blockvalue,err_msg

    def verifyObjects(self,object_string1,object_string2):
        """
        def : verifyObjects
        purpose : To compare two xml chunks
        param  : object_string1 and object_string2
        return : Returns True if xml chunks return True else False

        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg=None
        try:
            #Make sure params are strings
            log.debug('Conver xml param to string')
##            object_string1 = str(object_string1)
##            object_string2 = str(object_string2)
            #Remove new lines
            log.debug('Remove new lines')
            object_string1 = object_string1.replace('\n','')
            object_string2 = object_string2.replace('\n','')

            #Remove spaces between tags
            log.debug('Remove spaces if more than one')
            object_string1 = object_string1.replace('  ','')
            object_string2 = object_string2.replace('  ','')

            #Remove the leading and trailing spaces
            log.debug('Remove leading and trailing spaces')
            object_string1 = object_string1.strip()
            object_string2 = object_string2.strip()

            #Prepare xml element
            log.debug('Build xml element')
            tree1=''
            tree2=''
            if isinstance(object_string1,str):
                tree1 = etree.fromstring(object_string1.encode('utf-8'))
                tree2 = etree.fromstring(object_string2.encode('utf-8'))
            else:
                tree1 = etree.fromstring(object_string1)
                tree2 = etree.fromstring(object_string2)
            #Convert tree to strings
            log.debug('convert to string')
            tree1_string = etree.tostring(tree2)
            tree2_string = etree.tostring(tree1)

            #compare the xml strings
            if tree1_string == tree2_string:
                logger.print_on_console('xml chunks are equal')
                log.info('xml chunks are equal')
                log.info(STATUS_METHODOUTPUT_UPDATE)
                status = TEST_RESULT_PASS
                methodoutput = TEST_RESULT_TRUE
            else:
                err_msg='xml chunks are not equal'
        except Exception as e:
            err_msg=EXCEPTION_OCCURED
            log.error(e)
        if err_msg!=None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        log.info(RETURN_RESULT)
        return status,methodoutput,output,err_msg

class JSONOperations():

    def get_key_value(self,input_string,block_key_name,block_count,key_name,*args):
        """
        def : get_key_value
        purpose : get_key_value is used to get the key Value of the specified key in the given json
        param  : inputs : 1. json 2. block_key_name 3. block_count 4. key_name
        return : pass,true / fail,false, keyvalue

        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        key_value=None
        exception_json=None
        err_msg=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            encoded_inp_string=input_string
            if isinstance(input_string,str):
                encoded_inp_string=input_string.encode('utf-8')
            input_json=json.loads(encoded_inp_string)
            block=block_key_name.split('.')
            number=block_count.split(',')
            nested=input_json
            for i in range(0,len(block)):
                if(block[i] in nested and isinstance(nested,dict)):
                    nested=nested[block[i]]
                elif(isinstance(nested,list)):
                    if int(number[i])-1 != -1:
                        nested=nested[int(number[i])-1]
                    else:
                        nested=nested[0]
            try:
                if isinstance(nested,list) and int(number[i+1]) != None and int(number[i+1])!='':
                    if int(number[i+1])-1 != -1 :
                        if key_name in nested[int(number[i+1])-1]:
                            key_value = nested[int(number[i+1])-1][key_name];
                            logger.print_on_console('Key : ',key_name, ' Value : ',key_value)
                            status = TEST_RESULT_PASS
                            methodoutput = TEST_RESULT_TRUE
                        else:
                            log.debug('Invalid key given')
                            err_msg= ERR_XML
                    else:
                        log.debug('Index out of range')
                        err_msg= ERR_XML
                elif isinstance(nested,dict):
                    if key_name in nested:
                        key_value = nested[key_name]
                        logger.print_on_console('Key : ',key_name, ' Value : ',key_value)
                        status = TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
                    else:
                        log.debug('Invalid key given')
                        err_msg= ERR_XML
                else:
                        key_value = nested[0][key_name];
                        logger.print_on_console('Key : ',key_name, ' Value : ',key_value)
                        status = TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
                if(err_msg != None):
                    logger.print_on_console(err_msg)
            except Exception as e:
                err_msg=ERR_XML
                logger.print_on_console(err_msg)
                log.error(e)
        except Exception as e:
            err_msg=EXCEPTION_OCCURED
            log.error(e)
##        key_value=key_value.encode('utf-8')
        return status,methodoutput,key_value,err_msg
