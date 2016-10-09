#-------------------------------------------------------------------------------
# Name:        module1
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
import Exceptions


class PdfFile:

    def verify_content(self,input_path,pagenumber,content):
        pdf_content=self.get_content(input_path,pagenumber,'_internal_verify_content')
        if pdf_content == content:
            return True
        return False

    def compare_content(self,input_path1,input_path2):
        import filecmp
        return filecmp.cmp(input_path1,input_path2)


    def get_content(self,input_path,pagenumber,output_file,*args):
        from PyPDF2 import PdfFileReader, PdfFileWriter
        try:
             reader=PdfFileReader(open(input_path,'rb'))
             pagenumber=int(pagenumber)-1
             if pagenumber<reader.getNumPages():
                page=reader.getPage(pagenumber)
                content=page.extractText()
                content=content.encode('utf-8')
                logger.log('Content is:',content)
                if output_file=='_internal_verify_content':
                    return content
                if len(args) == 2:
                    start=args[0].strip()
                    end=args[1].strip()
                    content=content[content.find(start)+1:content.find(end)]
                    return content
                else:
                    with open(output_file,'w') as file:
                        file.write(content)
                return content
             else:
                logger.log(generic_constants.INVALID_INPUT)

        except ValueError as e:
            Exception.message(generic_constants.INVALID_INPUT)



class TextFile:

    def verify_content(self,input_path,content):
        with open(input_path) as myFile:
            for num, line in enumerate(myFile, 1):
                print line
                if content in line:
                    print 'found at line:'
                    break;


    def compare_content(self,input_path1,input_path2):
        content1=self.get_content(input_path1)
        content2=self.get_content(input_path2)
        logger.log('File1 content is '+content1)
        logger.log('File2 content is '+content2)
        if content1==content2:
            print 'pass'
            return True
        return False


    def clear_content(self,input_path):
        with open(input_path) as myFile:
            myFile.write('')
            myFile.close()


    def get_content(self,input_path):
        str=""
        with open(input_path) as myFile:
            str=myFile.read()
        logger.log(str)
        return str

    def get_linenumber(self,input_path,content):
        line_numbers=[]
        with open(input_path) as myFile:
            for num, line in enumerate(myFile, 1):
                if content in line:
                    print 'found at line:', num
                    line_numbers.append(num)
        logger.log(line_numbers)



    def replace_content(self,input_path,existing_content,replace_content):
        filecontent=''
        try:
            with open(input_path,'r') as myFile:
                filecontent=myFile.read()
                filecontent=filecontent.replace(existing_content,replace_content)
            with open(input_path, 'w') as file:
                    file.write(filecontent)
                    file.close()
            return True
        except:
            Exception.message('Error occurred')
            return False



    def write_to_file(self,input_path,content):
        logger.log('Writing to text file')
        try:
            with open(input_path, 'a') as file:
                file.write(content)
                file.close()
        except (OSError, IOError) as e:
            Exception.message('Cannot open file')


class XML:

    def write_to_file(self,input_path,content):
        import xml.dom.minidom as minidom
        from xml.etree import ElementTree as ET
        from xml.etree import ElementTree
        logger.log('Writing to XML file')
        try:
            tree = ET.XML(content)
            val =  prettify(tree)
            logger.log(val)
            with open(input_path, 'a') as file:
                file.write(content)
                file.close
        except Exception as e:
            Exceptions.error(e)

    def prettify(elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem)
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t")

    def clear_content(self,input_path):
        with open(input_path) as myFile:
            myFile.write('')
            myFile.close()















