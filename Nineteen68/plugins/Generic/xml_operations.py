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

import logger
from generic_constants import *
import Exceptions
from loggermessages import *
import logging
from constants import *
from lxml import etree
log = logging.getLogger('xml_operations.py')
class XMLOperations():
    def get_block_count(self,input_string,input_tag):
        """
        def : get_block_count
        purpose : get the count of blocks present in the input XML
        param : inputs : 1. xml 2. tag name
        return : pass,true / fail,false, block count

        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        block_count = 0
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            root = ET.fromstring(str(input_string))
            log.debug('Root object created with input string')
            items = root.getiterator(str(input_tag))
            log.debug('Getting children node from the root')
            if len(items) > 0:
                log.debug('There are children in the root node, get the total number of children')
                block_count = len(items)
                log.info('Number of blocks in input XML :'+ str( block_count))
                logger.print_on_console("Number of blocks in input XML:  ",block_count)
                log.info(STATUS_METHODOUTPUT_UPDATE)
                status = TEST_RESULT_PASS
                methodoutput = TEST_RESULT_TRUE
        except Exception as e:
            if isinstance(e,ET.ParseError):
                logger.print_on_console('Invalid tag/missing tag/blockcount in XML input')
                log.error('Invalid tag/missing tag/blockcount in XML input')
            else:
                logger.print_on_console(EXCEPTION_OCCURED,e)
                log.error(EXCEPTION_OCCURED)
                log.error(e)
        log.info(RETURN_RESULT)
        return status,methodoutput,block_count

    def get_tag_value(self,input_string,block_number,input_tag,child_tag):
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
        tagvalue = ''
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            root = ET.fromstring(str(input_string))
            log.debug('Root object created with input string')
            items = root.getiterator(str(input_tag))
            log.debug('Getting children node from the root')
            if len(items) > 0:
                log.debug('There are children in the root node, get the total number of children')
                block_count = len(items)
                block_number = int(block_number)
                block = items[block_number-1].getchildren()
                log.info('Block number: ' + str(block_number))
                for child in block:
                    log.info('Iterating child in the block')
                    if child.tag == str(child_tag):
                        log.info('Child mathed with the input child tag')
                        tagvalue =  child.text
                        logger.print_on_console('Tag : ',input_tag, '       Tag Value : ',tagvalue)
                        log.info('Got the child text value and stored in tagvalue')
                        log.info(STATUS_METHODOUTPUT_UPDATE)
                        status = TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
                    else:
                        invalidinput = True
                if status == TEST_RESULT_FAIL:
                    log.info(INVALID_INPUT + 'Please check the input tag')
                    logger.print_on_console(INVALID_INPUT , 'Please check the input tag')
        except Exception as e:
            if isinstance(e,ValueError):
                log.error("Block number should be a number")
                logger.print_on_console("Block number should be a number")
            elif isinstance(e,ET.ParseError):
                logger.print_on_console('Invalid tag/missing tag/blockcount in XML input')
                log.error('Invalid tag/missing tag/blockcount in XML input')
            else:
                log.error(EXCEPTION_OCCURED)
                log.error(e)
                logger.print_on_console(EXCEPTION_OCCURED,e)
        log.info(RETURN_RESULT)
        return status,methodoutput,tagvalue

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
        blockvalue = []
        log.info(STATUS_METHODOUTPUT_LOCALVARIABLES)
        try:
            root = ET.fromstring(str(input_string))
            log.debug('Root object created with input string')
            blocks = root.getiterator(str(input_tag))
            log.debug('Getting children node from the root')
            if len(blocks) > 0:
                log.debug('There are children in the root node, get the total number of children')
                block_count = len(blocks)
                block_number = int(block_number)
                log.info('Block number: ' + str(block_number))
                block = blocks[block_number-1].getchildren()
                log.info('Iterating child in the block')
                for child in block:
                    log.info('Child text :' + str(child.text))
                    blockvalue.append(  '<' + child.tag + '>' + child.text +  '</' + child.tag + '>')
                status = TEST_RESULT_PASS
                methodoutput = TEST_RESULT_TRUE
                log.info(STATUS_METHODOUTPUT_UPDATE)
                if status == TEST_RESULT_FAIL:
                    log.info(INVALID_INPUT + ' Please check the input tag' )
        except Exception as e:
            if isinstance(e,ValueError):
                log.error("Block number should be a number")
                logger.print_on_console("Block number should be a number")
            elif isinstance(e,ET.ParseError):
                logger.print_on_console('Invalid tag/missing tag/blockcount in XML input')
                log.error('Invalid tag/missing tag/blockcount in XML input')
            else:
                log.error(EXCEPTION_OCCURED)
                log.error(e)
                logger.print_on_console(EXCEPTION_OCCURED,e)
        log.info(RETURN_RESULT)
        return status,methodoutput,blockvalue

    def verifyObjects(self,object_string1,object_string2):
        """
        def : verifyObjects
        purpose : To compare two xml chunks
        param  : object_string1 and object_string2
        return : Returns True if xml chunks return True else False

        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        try:
            #Make sure params are strings
            log.debug('Conver xml param to string')
            object_string1 = str(object_string1)
            object_string2 = str(object_string2)

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
                logger.print_on_console('xml chunks are not equal')
                log.info('xml chunks are not equal')

        except Exception as e:
            log.error(EXCEPTION_OCCURED)
            log.error(e)
            logger.print_on_console(EXCEPTION_OCCURED,e)
        log.info(RETURN_RESULT)
        return status,methodoutput


##if __name__ == '__main__':
##    obj = XMLOperations()
##
##    inputs = []
##    a = """<Parameter><Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30301</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set>-<Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30302</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set>-<Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30303</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set>-<Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30304</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set>-<Set><CITY>Atlanta</CITY><STATE>GA</STATE><ZIP>30305</ZIP><AREA_CODE>404</AREA_CODE><TIME_ZONE>E</TIME_ZONE></Set></Parameter>"""
##    b = '2'
##    c = """Set"""
##    d = """ZIP"""
####    inputs.append()
##    bcount = obj.get_block_count(a,c)
##    print bcount
##    print """================================================="""
##
##    tvalue = obj.get_tag_value(a,b,c,d)
##    print tvalue
##
##    print """================================================="""
##
##    bvalue = obj.get_block_value(a,c,b)
##    print bvalue

