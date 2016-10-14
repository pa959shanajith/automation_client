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
        """
        def : verify_content
        purpose : verifies whether the content is given pagenumber of pdf file
        param : input_path,pagenumber,content
        return : bool

        """
        pdf_content=self.get_content(input_path,pagenumber,content,'_internal_verify_content')
        if content in pdf_content.replace('\n',''):
            return True
        return False

    def compare_content(self,input_path1,input_path2):
        """
        def : compare_content
        purpose : compares all pages of given 2 pdf files
        param : input_path1,input_path2
        return : bool

        """
        import filecmp
        return filecmp.cmp(input_path1,input_path2)


    def get_content(self,input_path,pagenumber,output_file,*args):
        """
        def : get_content
        purpose : return the content present in given pagnumber of pdf file
        param : input_path1,input_path2
        return : bool

        """
        from PyPDF2 import PdfFileReader, PdfFileWriter
        try:
             reader=PdfFileReader(open(input_path,'rb'))
             pagenumber=int(pagenumber)-1
             if pagenumber<reader.getNumPages():
                page=reader.getPage(pagenumber)
                content=page.extractText()
                content=content.encode('utf-8')
                logger.log('Content is:'+content)
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
        """
        def : verify_content
        purpose : verifies whether the content is given text file
        param : input_path,pagenumber,content
        return : bool

        """
        with open(input_path) as myFile:
            for num, line in enumerate(myFile, 1):
                print line
                if content in line:
                    print 'found at line:'+str(num)
                    return True
        return False


    def compare_content(self,input_path1,input_path2):
        """
        def : compare_content
        purpose : compares the content of given 2 text files
        param : input_path1,input_path2
        return : bool

        """
        content1=self.get_content(input_path1)
        content2=self.get_content(input_path2)
        logger.log('File1 content is '+content1)
        logger.log('File2 content is '+content2)
        if content1==content2:
            print 'pass'
            return True


    def clear_content(self,input_path):
        """
        def : clear_content
        purpose : clears the content of given text file
        param : input_path
        return : bool

        """
        with open(input_path,'w') as myFile:
            myFile.write('')
            myFile.close()
            return True


    def get_content(self,input_path):
        """
        def : get_content
        purpose : returns the content of given text file
        param : input_path
        return : bool

        """
        str=""
        with open(input_path) as myFile:
            str=myFile.read()
        logger.log(str)
        return str

    def get_linenumber(self,input_path,content):
        """
        def : get_linenumber
        purpose : returns the linenumber at which content is present in text file
        param : input_path,content
        return : bool

        """
        line_numbers=[]
        with open(input_path) as myFile:
            for num, line in enumerate(myFile, 1):
                if content in line:
                    print 'found at line:', num
                    line_numbers.append(num)
        logger.log(line_numbers)
        return line_numbers



    def replace_content(self,input_path,existing_content,replace_content):
        """
        def : replace_content
        purpose : replace the 'existingcontent' by 'replacecontent' in given text file
        param : input_path,content
        return : bool

        """
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
        """
        def : write_to_file
        purpose : writes the content to given text file
        param : input_path,content
        return : bool

        """
        logger.log('Writing to text file')
        try:
            with open(input_path, 'a') as file:
                file.write(content)
                file.close()
                return True
        except (OSError, IOError) as e:
            Exception.message('Cannot open file')
        return False


class XML:

    def write_to_file(self,input_path,content):
        """
        def : write_to_file
        purpose : writes the content to given XML file
        param : input_path,content
        return : bool

        """
        logger.log('Writing to XML file')
        import xml.dom.minidom as minidom
        from xml.etree import ElementTree as ET
        from xml.etree import ElementTree
        try:
            tree = ET.XML(content)
            rough_string = ElementTree.tostring(tree)
            reparsed = minidom.parseString(rough_string)
            val=reparsed.toprettyxml(indent="\t")
            logger.log(val)
            with open(input_path, 'a') as file:
                file.write(val)
                file.close()
                return True
        except Exception as e:
            Exceptions.error(e)
        return False


    def clear_content(self,input_path):
        """
        def : clear_content
        purpose : clears the content of given xml file
        param : input_path
        return : bool

        """
        with open(input_path,'w') as myFile:
            myFile.write('')
            myFile.close()
            return True
















