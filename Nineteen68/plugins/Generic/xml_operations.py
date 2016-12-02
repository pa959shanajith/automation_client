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
        try:
            print 'input1 : ',input_string, '\ninput2 : ',input_tag
            root = ET.fromstring(str(input_string))
            items = root.getiterator(str(input_tag))
            if len(items) > 0:
                block_count = len(items)
                logger.log("Block count:  ")
                logger.log(block_count)
                status = TEST_RESULT_PASS
                methodoutput = TEST_RESULT_TRUE
        except Exception as e:
            if isinstance(e,ET.ParseError):
                logger.log('Invalid tag/missing tag/blockcount in XML input')
            else:
                Exceptions.error(e)
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
        try:
            print 'input1 : ',input_string, '\ninput2 : ',block_number,'\ninput3 : ',input_tag, '\ninput4 : ',child_tag
            root = ET.fromstring(str(input_string))
            items = root.getiterator(str(input_tag))
            if len(items) > 0:
                block_count = len(items)
                block_number = int(block_number)
                block = items[block_number-1].getchildren()
                for child in block:
                    if child.tag == str(child_tag):
                        tagvalue =  child.text
                        status = TEST_RESULT_PASS
                        methodoutput = TEST_RESULT_TRUE
                    else:
                        invalidinput = True
                if status == TEST_RESULT_FAIL:
                    logger.log(INVALID_INPUT)
                    logger.log('Please check the input tag')
        except Exception as e:
            if isinstance(e,ValueError):
                logger.log("Block number should be a number")
            elif isinstance(e,ET.ParseError):
                logger.log('Invalid tag/missing tag/blockcount in XML input')
            else:
                Exceptions.error(e)
        return status,methodoutput,tagvalue

    def get_block_value(self,input_string,input_tag,block_number):
        """
        def : get_block_value
        purpose : get_block_value is used to get the Block Value of the specified tag in the given XML
        param : inputs : 1. xml 2. input_tag 3.block_number
        return : pass,true / fail,false, blockvalue

        """
        status = TEST_RESULT_FAIL
        methodoutput = TEST_RESULT_FALSE
        block_count = 0
        invalidinput = False
        blockvalue = ''
        try:
            print 'input1 : ',input_string, '\ninput2 : ',input_tag,'\ninput3 : ',block_number
            root = ET.fromstring(str(input_string))
            blocks = root.getiterator(str(input_tag))
            if len(blocks) > 0:
                block_count = len(blocks)
                block_number = int(block_number)
                block = blocks[block_number-1].getchildren()
                blockvalue = '<' + blocks[block_number-1].tag + '>'
                insidedata = ''
                for child in block:
                    line = '<' + child.tag + '>' + child.text +  '</' + child.tag + '>'
                    insidedata = insidedata + line

                blockvalue = blockvalue + insidedata +'</' + blocks[block_number-1].tag + '>'
                status = TEST_RESULT_PASS
                methodoutput = TEST_RESULT_TRUE
                if status == TEST_RESULT_FAIL:
                    logger.log(INVALID_INPUT)
                    logger.log('Please check the input tag')
        except Exception as e:
            if isinstance(e,ValueError):
                logger.log("Block number should be a number")
            elif isinstance(e,ET.ParseError):
                logger.log('Invalid tag/missing tag/blockcount in XML input')
            else:
                Exceptions.error(e)
        return status,methodoutput,blockvalue


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

