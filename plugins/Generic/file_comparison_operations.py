#-------------------------------------------------------------------------------
# Name:        file_comparison_operations.py
# Purpose:
#
# Author:      sushma.p
#
# Created:     29-09-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logger
import generic_constants
import constants
import json
import difflib
import tempfile
import os
import string
import random
import core_utils
import dynamic_variable_handler
import logging
import fitz
import cv2
import imutils
import numpy as np
import PyPDF2
import difflib
log = logging.getLogger('file_operations_pdf.py')



class TextFile:

    def verify_content(self,input_path,content,abs=False):
        """
        def : verify_content
        purpose : verifies whether the content is given text file
        param : input_path,pagenumber,content
        return : bool

        """
        status=False
        err_msg=None
        log.info("Performing verifyContent for text file")
        try:
            abs_flag = True if abs.lower() == 'abs' else False
            if not abs_flag:
                log.debug('Verifying content of Text file')
                with open(input_path) as myFile:
                    for num, line in enumerate(myFile, 1):
                        line = line.replace('\n','')
                        if content == line :
                            log.info('found at line:'+str(num))
    ##                        logger.print_on_console('found at line:',(num))
                            status=True
                if not(status):
                    err_msg=generic_constants.CONTENT_NOT_PRESENT
            elif abs_flag:
                log.debug("Absolute verifyContent")
                file_content=[]
                with open(input_path) as myFile:
                    for num, line in enumerate(myFile, 1):
                        line = line.replace('\n', '')
                        file_content.append(line)
                full_file_content = ''.join(file_content)
                content=content.replace("\n","")
                del file_content
                if full_file_content==content:
                    log.info("Content matched")
                    status=True
                    del full_file_content
        except IOError:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Verifying Text content'+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,err_msg


    def compare_content(self,input_path1,input_path2):
        """
        def : compare_content
        purpose : compares the content of given 2 text files
        param : input_path1,input_path2
        return : bool

        """
        status=False
        err_msg=None
        log.debug('Comparing content of text files: '+str(input_path1)+','+str(input_path2))
        try:
            content1=self.get_content(input_path1,"getfullcontent")
            content2=self.get_content(input_path2,"getfullcontent")

            if content1==content2:
                status=True
            else:
                err_msg=generic_constants.CONTENT_NOT_SAME
        except IOError:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Comparing Text content'+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        return status,err_msg



    def clear_content(self,input_path,file_name):
        """
        def : clear_content
        purpose : clears the content of given text file
        param : input_path
        return : bool

        """
        status=False
        err_msg=None
        log.debug('Clearing content of Text file '+str(input_path)+' '+str(file_name))
        input_path=input_path+'/'+file_name
        try:
            with open(input_path,'w') as myFile:
                myFile.write('')
                myFile.close()
                status=True
        except IOError:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Clearing Text content'+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        return status,err_msg


    def get_content(self,input_path,linenumber):
        """
        def : get_content
        purpose : returns the content of given text file
        param : input_path
        return : bool

        """
        status=False
        content=None
        err_msg=None
        log.debug('Get the content of Text file '+str(input_path))
        try:
            with open(input_path) as myFile:
                content = myFile.read()
                if linenumber == "getfullcontent":
                    status=True
                elif linenumber == 'nolinenumber':
                    display_msg = "WARNING: Fetching entire text file content as the line number is not specified."
                    logger.print_on_console(display_msg)
                    status=True
                else:
                    linenumber = int(linenumber)
                    split_content = content.splitlines()
                    if linenumber > 0:
                        linenumber = linenumber - 1
                    if (linenumber <= len(split_content)) and (linenumber >= 0):
                        content = split_content[linenumber]
                        log.info('Content is '+str(content))
                        status=True
                    else:
                        content = ''
                        err_msg=constants.ERROR_CODE_DICT['ERR_INVALID_INPUT']
        except IOError:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Fetching Text content'+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        # if err_msg!=None:
        #     logger.print_on_console(err_msg)
        return status,content,err_msg

    def get_linenumber(self,input_path,content):
        """
        def : get_linenumber
        purpose : returns the linenumber at which content is present in text file
        param : input_path,content
        return : bool

        """
        status=False
        line_numbers=[]
        err_msg=None
        log.debug('Get the line number of Text file '+str(input_path)+' containing the content '+str(content))
        try:
            with open(input_path) as myFile:
                for num, line in enumerate(myFile, 1):
                    line =line.replace('\n','')
                    if content == line:
                        log.debug('found at line: '+str(num))
                        line_numbers.append(num)
                        status=True
            log.info(line_numbers)
##            logger.print_on_console(line_numbers)
        except IOError:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Fetching line number of text '+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,line_numbers,err_msg

    def replace_content(self,input_path,existing_content,replace_content):
        """
        def : replace_content
        purpose : replace the 'existingcontent' by 'replacecontent' in given text file
        param : input_path,content
        return : bool

        """
        filecontent=''
        status=False
        err_msg=None
        try:
            log.debug('Replace_content of Text file ')
            with open(input_path,'r') as myFile:
                filecontent=myFile.read()
                filecontent=filecontent.replace(existing_content,replace_content)
                log.debug('Replaced content successfully')
            with open(input_path, 'w') as file:
                    file.write(filecontent)
                    file.close()
                    status= True
        except IOError:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Replacing of text '+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,err_msg

    def write_to_file(self,input_path,content,*args):
        """
        def : write_to_file
        purpose : writes the content to given text file
        param : input_path,content
        return : bool

        """
        status=False
        err_msg=None
##        logger.print_on_console('Writing '+str(content)+' to text file '+str(input_path))
##        log.info('Writing '+str(content)+' to text file '+str(input_path))
        coreutilsobj=core_utils.CoreUtils()
        input_path=coreutilsobj.get_UTF_8(input_path)
        log.info('Writing ',content,' to text file ',input_path)
        try:
            ##for i in args:
            ##    content='\n'.join(i)
            len_args=len(args)
            ##print "len_args",len_args
            ##print len_args
            ##print args[len_args-1]
            with open(input_path, 'a+') as file:
                if len(args)>0 and (args[len_args-1]).lower()=="newline" :
                    ##print "Newline"
                    ##print "size: ",os.stat(input_path).st_size

            #872 unicode write file support (Himanshu)
                    try:
                        ##print "hiiiiiiiiiii"
                        if os.stat(input_path).st_size == 0:
                            ##print "Zero"
                            file.write(content)
                        else:
                            ##print "NotZero"
                            #fix for #14921: Removed \n before writing content
                            file.write(content)
                    except:
                        ##print "except"
                        if os.stat(input_path).st_size == 0:
                            file.write(content.encode('UTF-8'))
                        else:
                            file.write("\n")
                            file.write(content.encode('UTF-8'))
                    for i in range(0,(len(args)-1)):
                        try:
                            #fix for #14921
                            # \\n \\t \\r are replaced by \n \t \r
                            file.write("\n")
                            file.write(args[i].replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r").strip())
                        except:
                            file.write("\n")
                            file.write(args[i].replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r").strip())


                else:

                    content+=''.join(args)
                    # \\n \\t \\r are replaced by \n \t \r
                    content = content.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r").strip()
                    try:
                        file.write(content)
                    except:
                        file.write(content.encode('UTF-8'))
                file.close()
                log.debug('Content is written successfully')
                status= True
        except (IOError,OSError) as e:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Writing to text '+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is ',status)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,err_msg


class XML:

    def write_to_file(self,input_path,content):
        """
        def : write_to_file
        purpose : writes the content to given XML file
        param : input_path,content
        return : bool

        """
        status=False
        err_msg=None
##        logger.print_on_console('Writing '+str(content)+' to XML file '+str(input_path))
##        log.info('Writing '+str(content)+' to XML file '+str(input_path))
        coreutilsobj=core_utils.CoreUtils()
        import xml.dom.minidom as minidom
        from xml.etree import ElementTree as ET
        from xml.etree import ElementTree
        try:
        #872 Unicode file write support for XML (Himanshu)
            log.info('Writing '+content+' to XML file '+input_path)
            input_path=coreutilsobj.get_UTF_8(input_path)
            try:
                tree = ET.XML(content)
            except:
                tree = ET.XML(content.encode('UTF-8'))
            if 'Envelope' in tree.tag and tree.tag.split('}')[1] == 'Envelope':
                val=content
            else:
                rough_string = ElementTree.tostring(tree,'utf-8')
                reparsed = minidom.parseString(rough_string)
                val=reparsed.toprettyxml(indent="\t")
            with open(input_path, 'w') as file:
                #val=val.encode('utf-8')
                file.write(val)
                file.close()
                log.debug('Content is written successfully')
                status=True
        except IOError:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Writing to XML '+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,err_msg


    def clear_content(self,input_path,file_name):
        """
        def : clear_content
        purpose : clears the content of given xml file
        param : input_path
        return : bool

        """
        status=False
        err_msg=None
        log.debug('Clearing content of XML file '+str(input_path)+' '+str(file_name))
        input_path=input_path+'/'+file_name
        try:
            with open(input_path,'w') as myFile:
                myFile.write('')
                myFile.close()
                status=True
        except IOError:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Clearing XML '+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        return status,err_msg

class JSON:

    def write_to_file(self,input_path,content,*args):
        """
        def : write_to_file
        purpose : writes the content to given json file
        param : input_path,content
        return : bool

        """
        status=False
        err_msg=None
        coreutilsobj=core_utils.CoreUtils()
        try:
            input_path=coreutilsobj.get_UTF_8(input_path)
            log.info('Writing ',content,' to json file ',input_path)
            json.loads(content)
            with open(input_path,'w') as file_write:
                file_write.write(content)
                file_write.close()
            status=True
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Writing to JSON '+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is ',status)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,err_msg

    def ordered(self,obj):
        if isinstance(obj, dict):
            return sorted((k, self.ordered(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return sorted(self.ordered(x) for x in obj)
        else:
            return obj

    def compare_content(self,content1,content2):
        """
        def : compare_content
        purpose : compares the content of given 2 Json inputs
        param : content1,content2
        return : bool

        """
        status=False
        err_msg=None
        
        try:
            log.debug('Comparing content of Json Content: '+str(content1)+','+str(content2))
            if (self.ordered(json.loads(content1))==self.ordered(json.loads(content2)))==True:
                status=True
            else:
                err_msg=generic_constants.CONTENT_NOT_SAME
        
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Comparing Text content'+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        return status,err_msg

