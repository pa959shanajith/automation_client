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

import xml
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

    def __init__(self):
        self.xmlfile=None
        self.xmlroot=None
        
    def xmlfileread(self,xml_file):
        #reading the xml file and saving in object.
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        try:
        if os.path.exists(xml_file)!=False:
            log.info("Specified Path Exists")
            fileName,file_ext=os.path.splitext(xml_file)
            logger.print_on_console("Checking the file extension")
            if file_ext.lower().find('.xml')!=-1:
                logger.print_on_console("File Extension found True")
                self.xmlfile = ET.parse(xml_file)
                output=self.xmlfile
                status = TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
                logger.print_on_console("XML file reading success")
            else:
                log.debug("File Extension Found False")
                logger.print_on_console("File Extension is not '.xml'")
        else:
            log.info("Specified Path not exists")
            logger.print_on_console("Specified Path not exists")

        except Exception as e:
            log.error(e)
            err_msg = generic_constants.INVALID_INPUT
        if err_msg != None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        
        return  status, result, output, err_msg
        
    def xmlreadfromstring(self,xml_string):
        # reading the xml from string
        pass
        
    def getroot(self):
        #Getting the xml file root and print the root name:
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        try:
            if self.xmlfile!=None or self.xmlfile!='':
                log.info("xmlfile not found empty")
                self.xmlroot=self.xmlfile.getroot()
                output=self.xmlroot
                status = TEST_RESULT_PASS
                result = TEST_RESULT_TRUE
                logger.print_on_console("Root found and Value is {}".format(self.xmlroot.tag))
            else:
                log.debug("Xmlfile data read found empty")
                logger.print_on_console("Not Found Proper XML Data")

        except Exception as e:
            log.error(e)
            err_msg = generic_constants.INVALID_INPUT
        if err_msg != None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        
        return  status, result, output, err_msg
 
    def getelement_attribute(self,root,elementname):
        #getting the attribute of the node
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        list_attribute=None
        try:
            if type(root).find("<class 'xml.etree.ElementTree")!=-1:
                if elementname!=None or elementname!='':
                    #finding the attribute of the specified element.
                    log.debug("finding the attribute of element {}".format(elementname))
                    list_attribute = [child.attrib for child in root.iter(elementname)]
                    log.debug("Assign the output with list attribute")
                    output=list_attribute
                    logger.print_on_console("Found list of attributes {} for the element {}".format(output,elementname))
                    status = TEST_RESULT_PASS
                    result = TEST_RESULT_TRUE
                else:
                    #logging the error  
                    log.info("Please provide the proper element")
                    logger.print_on_console("Please provide the proper element")
            else:
                log.debug("Please Provide the Root element")
                logger.print_on_console("Please Provide the Root element")
                
        except Exception as e:
            log.error(e)
            err_msg = generic_constants.INVALID_INPUT
        if err_msg != None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        
        return  status, result, output, err_msg
        
    def getelement_tag(self,root,elementname):
        #getting the tag of the node
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        list_tag = None
        try:
            if type(root).find("<class 'xml.etree.ElementTree")!=-1:
                if elementname!=None or elementname!='':
                    #finding the attribute of the specified element.
                    log.debug("finding the attribute of element {}".format(elementname))
                    list_tag = [child.tag for child in root.iter(elementname)]
                    log.debug("Assign the ouput with listtag")
                    output=list_tag
                    logger.print_on_console("Found the list of tags {} for the element {}".format(output,elementname))
                    status = TEST_RESULT_PASS
                    result = TEST_RESULT_TRUE
                else:
                    #logging the error  
                    log.info("Please provide the proper element")
                    logger.print_on_console("Please provide the proper element")
                    
            else:
                log.debug("Please Provide the Root element")
                logger.print_on_console("Please Provide the Root element")
                
        except Exception as e:
            log.error(e)
            err_msg = generic_constants.INVALID_INPUT
        if err_msg != None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        
        return  status, result, output, err_msg
    
    def findall(self,root,elementname):
        #finding all the elements of the node
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        findall_list = []
        try:
            if type(root).find("<class 'xml.etree.ElementTree")!=-1::
                if elementname!=None or elementname!='':
                    finddict = {}
                    log.debug("Finding tag,attribute,text of the element {} ".format(elementname))
                    for each_child in root.iter(elementname)
                        if elementname not in finddict.keys():
                            finddict[elementname.tag] = [each_child.tag,each_child.attrib,each_child.text]
                        else:
                            finddict[elementname.tag].append([each_child.tag,each_child.attrib,each_child.text])
                    log.debug("Collected all the values of the element {}".format(elementname))
                    logger.print_on_console("Collected Values of the element {}".format(finddict))
                    output=finddict
                    logger.print_on_console("Find all the values of the element {}".format(output))
                else:
                    findall_list = [[] for each_child in root.iter() for each_element in each_child.iter()]
                    #logg for element not found.
                    log.debug("Provided Element not Found")
                    logger.print_on_console("Please Provide the Valid Element")
                    
            else:
                #logg for root element not found.
                log.debug("Root Element not provided")
                logger.print_on_console("Please Provide the root element")
  
        except Exception as e:
            log.error(e)
            err_msg = generic_constants.INVALID_INPUT
        if err_msg != None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        
        return  status, result, output, err_msg
        
    def find_element(self,root,elementname):
    
        #finding the elements of the node
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        elementname_list = None:
        try:
            if type(root).find("<class 'xml.etree.ElementTree")!=-1:
                if elementname!=None or elementname!='':
                    log.info("finding the elements of the specified element")
                    elementname_list=[each_child.tag for each_element in root.iter(elementname) for each_child in each_element.iter()]
                    output = elementname_list
                    log.debug("Found elements {} for the provided element {}".format(elementname_list,elementname))
                    logger.print_on_console("Result Obtined for the element {} : {}".format(elementname,elementname_list))
                
                else:
                    log.debug("Please Provide the Element to find")
                    logger.print_on_console("Please Provide the element to find")
                    
            else:
                log.debug("Please provide the root element")
                logger.print_on_console("Please Provided the root element")
                
        except Exception as e:
            log.error(e)
            err_msg = generic_constants.INVALID_INPUT
        if err_msg != None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        
        return  status, result, output, err_msg

    def get_elements_text(self,root,elementname):
        #getting the elements text
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        element_text = None
        try:
            if type(root).find("<class 'xml.etree.ElementTree")!=-1:
                if elementname!=None or elementname!='':
                    #looping to get the all the text of specified element.
                    log.info("Finding the provided elements text")
                    element_text= [(child.find(elementname).text,child.find(elementname).tail) for child in root.iter() if child.find(elementname)!=None]
                    output=element_text
                    status = TEST_RESULT_PASS
                    result = TEST_RESULT_TRUE
                    logger.print_on_console("Result Obtined for the provided element {}".format(output))
                    
                else:
                    log.debug("Element not specified")
                    logger.print_on_console("Element not Provided")
            else:
                log.debug("root element not specified")
                logger.print_on_console("root element not specified")

        except Exception as e:
            log.error(e)
            err_msg = generic_constants.INVALID_INPUT
        if err_msg != None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        
        return  status, result, output, err_msg   
        
    def nested_looping(self,root,elementname,depth,result_dict):
        #looping to find the elements and attribute of elements.
        if elementname!=None or elementname!='':
            for each_element in root.findall(elementname)[:int(depth)]:
                for each_child in each_element.iter():
                    if each_element not in result_dict.keys():
                        result_dict[each_element] = {}
                    else:
                        result_dict[each_element].update({each_child.tag:[each_child.attrib,each_child.text]})
            
        else:
        
            for each_element in root[:int(depth)]:
                for each_child in each_element.iter():
                    if each_element not in result_dict.keys():
                        result_dict[each_element] = {}
                    else:
                        result_dict[each_element].update({each_child.tag:[each_child.attrib,each_child.text]})
        
        return result_dict
 
    def nestedxml_operation(self,root,elementname,depth):
    
        # Nested XML Operation: if the elementname and depth given, get the child elements tag,attribute,text.
        status = TEST_RESULT_FAIL
        result = TEST_RESULT_FALSE
        output = OUTPUT_CONSTANT
        err_msg = None
        result_dict={}
        try:
            if type(root).find("<class 'xml.etree.ElementTree")!=-1:
                if elementname!=None or elementname!='':
                    if int(depth)>0:
                        result_dict=self.nested_looping(root,elementname,depth,result_dict)        
                    elif depth==0:
                        result_dict=self.nested_looping(root,elementname,-1,result_dict)
                    else:
                        #log for to mention the depth
                        log.debug("Please Provide the depth for Iter")
                elif elementname=='' or elementname==None:
                    if int(depth)>0:
                        result_dict=self.nested_looping(root,None,depth,result_dict)        
                    elif depth==0:
                        result_dict=self.nested_looping(root,None,-1,result_dict)
                    else:
                        #log for to mention the depth
                        log.debug("Please Provide the depth for Iter")
                    
                log.debug("Result {}".format(result_dict))
                output=result_dict
                logger.print_on_console("Result Obtined : {}".format(output)

        except Exception as e:
            log.error(e)
            err_msg = generic_constants.INVALID_INPUT
        if err_msg != None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        
        return  status, result, output, err_msg

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
    
    def jsonfile_read(self,json_file):
        #reading the JSON File.
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        key_value=None
        exception_json=None
        err_msg=None
        output=None
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            if json_file!='' or json_file!=None:
                if os.path.exists(json_file)!=False:
                    fileName,file_ext=os.path.splitext(xml_file)
                    if file_ext.lower().find('.json')!=-1:
                        with open(json_file) as json_read:
                            output=str(json.load(json_read))
                            status = TEST_RESULT_PASS
                            result = TEST_RESULT_TRUE
                            logger.print_on_console("Result Obtined:".format(output))
                    else:
                        log.debug("File extension not json")
                        logger.print_on_console("File extension not json")
                        
                else:
                    log.debug("File Not Found in the specified Location")
                    logger.print_on_console("File Not Found in the specified Location")
            else:
                log.info("Please Mention the Json File Path")
                logger.print_on_console("Please Mention the Json File Path")

        except Exception as e:
            log.error(e)
            err_msg = generic_constants.INVALID_INPUT
        if err_msg != None:
            log.error(err_msg)
            logger.print_on_console(err_msg)
        
        return  status, result, output, err_msg
