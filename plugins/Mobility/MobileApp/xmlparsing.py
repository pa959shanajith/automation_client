#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:
# Copyright:   (c) sushma.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from xml.sax.handler import ContentHandler
import xml.sax
import xml.parsers.expat
import configparser
import uuid,json
import logging

XpathList=[]
resource_id=[]
class_name=[]
enabled=[]
rectangle=[]
focusable=[]
content_desc=[]
checked=[]
label=[]
name=[]
ScrapeList=[]
driver=None

log = logging.getLogger('xmlparsing.py')

class Json_fields:

    def __init__(self,xpath,id,tag,label,reference,enabled,rectangle):
        self.xpath=xpath
        self.id=xpath
        self.tag=tag
        self.label=label
        self.reference=reference
        self.enabled=enabled
        self.rectangle=rectangle




class BuildJson:


    def xmltojson(self):
        print('Writing json to file')

        for i in range(len(XpathList)):
            text=class_name[i]
            if label[i] != '':
                text=label[i]
            elif content_desc[i] != '':
                text=content_desc[i]
##            rect=rectangle[i]
##            print rect[0],rect[1]
##            bounds={'x':rect[0][0],
##            'y':rect[0][1],
##            'height':rect[1][0],
##            'width':rect[1][1]}
            ScrapeList.append({'xpath': XpathList[i], 'tag': class_name[i],
                                                    'text': text,
                                                    'id': resource_id[i], 'custname': text,
                                                    'reference': str(uuid.uuid4()),'enabled':enabled[i],'rectangle':rectangle[i]})
##            obj=Json_fields(,,,text,,,rectangle[i])
##            ScrapeList.append(obj)
        self.save_json(ScrapeList)

    def save_json(self,scrape_data):
        from collections import OrderedDict
        jsonArray=OrderedDict()
        jsonArray['view']= scrape_data
        jsonArray['mirror']='IMAGEEEEE'
##        jsonArray['mirror']=driver.get_screenshot_as_base64()
        with open(os.environ["NINETEEN68_HOME"] + '/output/domelements_Android.json', 'w') as outfile:
                print ('Writing scrape data to domelements.json file')
                log.info(jsonArray)
                json.dump(jsonArray, outfile, indent=4, sort_keys=False)
        outfile.close()




class Exact(xml.sax.handler.ContentHandler):


  def __init__(self,xpath,xmlreader,parent):
    self.curpath = []
    self.xPath=xpath
    self.parser=xmlreader
    self.elementNameCount={}
    self.buffer=''
    self.parent=parent


  def startElement(self, qName, attrs):
##    print qName,attrs
    count = self.elementNameCount.get(qName)

##    print count
    if count==None:
        count=1
    else:
        count=count+1
    self.elementNameCount[qName]=count
    childXPath = self.xPath + "/" + qName + "[" + str(count) + "]";


    attsLength = len(attrs)
    if(attsLength>1):
        XpathList.append(childXPath)
    for x in attrs.getQNames():
##        print x
        value=attrs.getValue(x)

        if x.lower()=='text':
            if(value == ''):
                label.append(qName)
            else:
                if value in label:
                    label.append(qName)
                else:
                    label.append(value)

            name.append(qName)

        elif x.lower()=='bounds':
            rectangle.append(value)

        elif x.lower()=='enabled':
            enabled.append(value)

        elif x.lower()=='resource-id':
            resource_id.append(value)

        elif x.lower()=='focusable':
            focusable.append(value)

        elif x.lower()=='class':
            class_name.append(value)

        elif x.lower()=='content-desc':
            content_desc.append(value)

        elif x.lower()=='checked':
            checked.append(value)
    curobj=self

    child = Exact(childXPath,self.parser,curobj)
    self.parser.setContentHandler(child)



##    self.clearFields()


  def endElement(self, name):
    value = self.buffer.strip();
    if(value != ''):
            print((self.xPath + "='" + self.buffer.toString() + "'"))

    print(self.parent)
    self.parser.setContentHandler(self.parent)

  def characters(self, data):
    self.buffer += data



