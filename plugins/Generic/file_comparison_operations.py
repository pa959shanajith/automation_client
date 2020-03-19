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
import logging
import constants
import core_utils
import os
import json

log = logging.getLogger('file_comparison_operations.py')

class PdfFile:

    def verify_content(self,input_path,pagenumber,content):
        """
        def : verify_content
        purpose : verifies whether the content is given pagenumber of pdf file
        param : input_path,pagenumber,content
        return : bool

        """
        status=False
        err_msg=None
        try:
            log.debug('Verifying content of pdf file')
            pdf_content=self.get_content(input_path,pagenumber,content,'_internal_verify_content')
            log.debug('pdf_content is '+str(pdf_content))
            if content in pdf_content.replace('\n',''):
                status=True
            else:
                err_msg=generic_constants.CONTENT_NOT_PRESENT
        except IOError:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'verifying PDF content'+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,err_msg

    def compare_content(self,input_path1,input_path2):
        """
        def : compare_content
        purpose : compares all pages of given 2 pdf files
        param : input_path1,input_path2
        return : bool

        """
        status=False
        err_msg=None
        log.debug('Comparing content of pdf files: '+str(input_path1)+','+str(input_path2))
        try:
            import filecmp
            status=filecmp.cmp(input_path1,input_path2)
            if not(status):
                err_msg=generic_constants.CONTENT_NOT_SAME
        except IOError:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Comparing PDF content'+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,err_msg


    def get_content(self,input_path,pagenumber,*args):
        """
        def : get_content
        purpose : return the content present in given pagnumber of pdf file
        param : input_path1,input_path2
        return : bool

        """
        status=False
        content=None
        err_msg=None
        from PyPDF2 import PdfFileReader, PdfFileWriter
        import fitz
        try:
             log.debug('Get the content of pdf file: '+str(input_path)+','+str(pagenumber))
             doc=fitz.open(input_path)
             pagenumber=int(pagenumber)-1
             if pagenumber<doc.pageCount:
                page = doc[pagenumber]
                content=page.getText()
##                content=content.encode('utf-8')
                if len(args)>1 and args[1]=='_internal_verify_content':
                    return content
                if len(args) >= 2 and not (args[0] is None and args[1] is None):
                    start=args[0].strip()
                    end=args[1].strip()
                    startIndex=0
                    endIndex=len(content)
                    log.info('Start string: '+str(start)+' End string: '+str(end))
                    if not start is '':
                        startIndex=content.find(start)+len(start)
                    if not end is '':
                        endIndex=content.find(end)
                    content=content[startIndex:endIndex]
                    log.info('Content between Start and End string is ')
##                    logger.print_on_console('Content between Start and End string is ')
                elif len(args)==1:
                    with open(args[0],'w') as file:
                        file.write(content)
                        file.close()
                log.info(content)
                status=True
##        try:
##             log.debug('Get the content of pdf file: '+str(input_path)+','+str(pagenumber))
##             reader=PdfFileReader(open(input_path,'rb'))
##             pagenumber=int(pagenumber)-1
##             if pagenumber<reader.getNumPages():
##                page=reader.getPage(pagenumber)
##                content=page.extractText()
##                if len(args)>1 and args[1]=='_internal_verify_content':
##                    return content
##                if len(args) >= 2 and not (args[0] is None and args[1] is None):
##                    start=args[0].strip()
##                    end=args[1].strip()
##                    startIndex=0
##                    endIndex=len(content)
##                    log.info('Start string: '+str(start)+' End string: '+str(end))
##                    if not start is '':
##                        startIndex=content.find(start)+len(start)
##                    if not end is '':
##                        endIndex=content.find(end)
##                    content=content[startIndex:endIndex]
##                    log.info('Content between Start and End string is ')
##                elif len(args)==1:
##                    with open(args[0],'w') as file:
##                        file.write(content)
##                        file.close()
##                log.info(content)
##                status=True
             else:
                err_msg=generic_constants.INVALID_INPUT
                log.error(err_msg)

        except ValueError as e:
            err_msg=generic_constants.INVALID_INPUT
            log.error(e)
        except IOError as e:
            err_msg=constants.ERROR_CODE_DICT['ERR_FILE_NOT_ACESSIBLE']
            log.error(e)
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Fetching PDF content'+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is '+str(status))
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,content,err_msg



class TextFile:

    def verify_content(self,input_path,content):
        """
        def : verify_content
        purpose : verifies whether the content is given text file
        param : input_path,pagenumber,content
        return : bool

        """
        status=False
        err_msg=None
        try:
            log.debug('Verifying content of Text file ')
            with open(input_path) as myFile:
                for num, line in enumerate(myFile, 1):
                    line = line.replace('\n','')
                    if content == line :
                        log.info('found at line:'+str(num))
##                        logger.print_on_console('found at line:',(num))
                        status=True
            if not(status):
                err_msg=generic_constants.CONTENT_NOT_PRESENT
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
        if err_msg!=None:
            logger.print_on_console(err_msg)
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
        if err_msg!=None:
            logger.print_on_console(err_msg)
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
                            file.write("\n"+content)
                    except:
                        ##print "except"
                        if os.stat(input_path).st_size == 0:
                            file.write(content.encode('UTF-8'))
                        else:
                            file.write("\n")
                            file.write(content.encode('UTF-8'))
                    for i in range(0,(len(args)-1)):
                        try:
                            file.write("\n")
                            file.write(args[i])

                        except:
                            file.write("\n")
                            file.write(args[i].encode('UTF-8'))


                else:

                    content+=''.join(args)
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
        log.info('Writing '+content+' to XML file '+input_path)
        coreutilsobj=core_utils.CoreUtils()
        input_path=coreutilsobj.get_UTF_8(input_path)
        import xml.dom.minidom as minidom
        from xml.etree import ElementTree as ET
        from xml.etree import ElementTree
        try:
        #872 Unicode file write support for XML (Himanshu)
            try:
                tree = ET.XML(content)
            except:
                tree = ET.XML(content.encode('UTF-8'))
            rough_string = ElementTree.tostring(tree,'utf-8')
            reparsed = minidom.parseString(rough_string)
            val=reparsed.toprettyxml(indent="\t")
            with open(input_path, 'a') as file:
                val=val.encode('utf-8')
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
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,err_msg


class JSON:

    def write_to_file(self,input_path,content):
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
                json.dump(content,file_write)
            status=True
        except Exception as e:
            err_msg=generic_constants.ERR_MSG1+'Writing to JSON '+generic_constants.ERR_MSG2
            log.error(e)
        log.info('Status is ',status)
        if err_msg!=None:
            logger.print_on_console(err_msg)
        return status,err_msg

