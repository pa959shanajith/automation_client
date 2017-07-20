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
import ConfigParser
import uuid,json

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
        print 'Writing json to file'

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
        with open('D:\\domelements_Android.json', 'w') as outfile:
                print ('Writing scrape data to domelements.json file')
                print jsonArray
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
    print 'count ++++++++ ',self.elementNameCount
    print 'len ++++++++ ',attsLength
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
            print (self.xPath + "='" + self.buffer.toString() + "'")

    print self.parent
    self.parser.setContentHandler(self.parent)

  def characters(self, data):
    self.buffer += data


##  def clearFields():
##    self.fields = {}
##    self.fields['title'] = None
##    self.fields['job-code'] = None
##    self.fields['detail-url'] = None
##    self.fields['job-category'] = None
##    self.fields['description'] = None
##    self.fields['summary'] = None
##    self.fields['posted-date'] = None
##    self.fields['location'] = None
##    self.fields['address'] = None
##    self.fields['city'] = None
##    self.fields['state'] = None
##    self.fields['zip'] = None
##    self.fields['country'] = None
##    self.fields['company'] = None
##    self.fields['name'] = None
##    self.fields['url'] = None
##
##    self.buffer = ''

if __name__ == '__main__':
  parser = xml.sax.make_parser()
  handler = Exact('/',parser,'')
  parser.setContentHandler(handler)
  string="""<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.FrameLayout index="0" text="" class="android.widget.FrameLayout"
package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false"
focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][480,800]" resource-id=""
instance="0"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc=""
checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false"
password="false" selected="false" bounds="[0,0][480,800]" resource-id="" instance="0"><android.widget.FrameLayout index="0" text=""
class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false"
enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][480,800]"
resource-id="" instance="1"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app"
content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false"
long-clickable="false" password="false" selected="false" bounds="[0,36][480,800]" resource-id="com.slk.tic.bokf.rmb.app:id/action_bar_root"
instance="1"><android.widget.FrameLayout index="0" text="" class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc=""
checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false"
password="false" selected="false" bounds="[0,36][480,800]" resource-id="android:id/content" instance="2"><android.widget.LinearLayout index="0"
text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false"
enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,36][480,800]"
resource-id="" instance="2"><android.view.ViewGroup index="0" text="" class="android.view.ViewGroup" package="com.slk.tic.bokf.rmb.app"
content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false"
long-clickable="false" password="false" selected="false" bounds="[0,36][480,120]" resource-id="com.slk.tic.bokf.rmb.app:id/toolbar"
instance="0"><android.widget.ImageButton index="0" text="" class="android.widget.ImageButton" package="com.slk.tic.bokf.rmb.app" content-desc="BANK
OF OKLAHOMA" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false"
long-clickable="false" password="false" selected="false" bounds="[0,36][84,120]" resource-id="" instance="0"/><android.widget.TextView index="1"
text="Home" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false"
enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[90,57][170,98]"
resource-id="" instance="0"/></android.view.ViewGroup><android.support.v4.widget.DrawerLayout index="1" text=""
class="android.support.v4.widget.DrawerLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false"
enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false"
bounds="[0,120][480,800]" resource-id="com.slk.tic.bokf.rmb.app:id/drawer_layout" instance="0"><android.widget.FrameLayout index="0" text=""
class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false"
enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false"
bounds="[0,120][480,800]" resource-id="com.slk.tic.bokf.rmb.app:id/container" instance="3"><android.widget.LinearLayout index="0" text=""
class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false"
enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false"
bounds="[0,120][480,800]" resource-id="" instance="3"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout"
package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false"
focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,120][480,168]" resource-id=""
instance="4"><android.widget.TextView index="0" text="January  2017" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app"
content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false"
long-clickable="false" password="false" selected="false" bounds="[0,125][240,162]" resource-id="com.slk.tic.bokf.rmb.app:id/currentDate"
instance="1"/><android.widget.TextView index="1" text="Acc No  ***123" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app"
content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false"
long-clickable="false" password="false" selected="false" bounds="[240,125][480,162]" resource-id="com.slk.tic.bokf.rmb.app:id/accNmbr"
instance="2"/></android.widget.LinearLayout><android.view.View index="1" text="" class="android.view.View" package="com.slk.tic.bokf.rmb.app"
content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false"
long-clickable="false" password="false" selected="false" bounds="[0,168][480,171]" resource-id="" instance="0"/><android.widget.FrameLayout index="2"
text="" class="android.widget.FrameLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false"
enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false"
bounds="[0,171][480,406]" resource-id="com.slk.tic.bokf.rmb.app:id/chart_container" instance="4"><android.support.v4.view.ViewPager index="0" text=""
class="android.support.v4.view.ViewPager" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false"
enabled="true" focusable="true" focused="false" scrollable="true" long-clickable="false" password="false" selected="false" bounds="[12,174][468,403]"
resource-id="com.slk.tic.bokf.rmb.app:id/view_pager" instance="0"><android.widget.RelativeLayout index="0" text=""
class="android.widget.RelativeLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false"
enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false"
bounds="[12,174][468,403]" resource-id="" instance="0"><android.view.ViewGroup index="0" text="" class="android.view.ViewGroup"
package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false"
focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[27,189][417,388]"
resource-id="com.slk.tic.bokf.rmb.app:id/piechart" instance="1"/><android.widget.LinearLayout index="1" text="" class="android.widget.LinearLayout"
package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false"
focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[341,189][453,267]"
resource-id="com.slk.tic.bokf.rmb.app:id/legendsView" instance="5"><android.widget.LinearLayout index="0" text="" class="android.widget.LinearLayout"
package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false"
focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,198][453,215]" resource-id=""
instance="6"><android.widget.ImageView index="0" text="" class="android.widget.ImageView" package="com.slk.tic.bokf.rmb.app" content-desc=""
checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false"
password="false" selected="false" bounds="[350,198][362,210]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_img1"
instance="0"/><android.widget.TextView index="1" text="Funds Transfer" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app"
content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false"
long-clickable="false" password="false" selected="false" bounds="[371,198][453,215]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_text1"
instance="3"/></android.widget.LinearLayout><android.widget.LinearLayout index="1" text="" class="android.widget.LinearLayout"
package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false"
focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,224][448,241]" resource-id=""
instance="7"><android.widget.ImageView index="0" text="" class="android.widget.ImageView" package="com.slk.tic.bokf.rmb.app" content-desc=""
checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false"
password="false" selected="false" bounds="[350,224][362,236]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_img2"
instance="1"/><android.widget.TextView index="1" text="Check Deposit" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app"
content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false"
long-clickable="false" password="false" selected="false" bounds="[371,224][448,241]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_text2"
instance="4"/></android.widget.LinearLayout><android.widget.LinearLayout index="2" text="" class="android.widget.LinearLayout"
package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false"
focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[350,250][443,267]" resource-id=""
instance="8"><android.widget.ImageView index="0" text="" class="android.widget.ImageView" package="com.slk.tic.bokf.rmb.app" content-desc=""
checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false"
password="false" selected="false" bounds="[350,252][362,264]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_img3"
instance="2"/><android.widget.TextView index="1" text="Cash Deposit" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app"
content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false"
long-clickable="false" password="false" selected="false" bounds="[371,250][443,267]" resource-id="com.slk.tic.bokf.rmb.app:id/legend_text3"
instance="5"/></android.widget.LinearLayout></android.widget.LinearLayout></android.widget.RelativeLayout></android.support.v4.view.ViewPager></android
.widget.FrameLayout><android.widget.LinearLayout index="3" text="" class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app"
content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false"
long-clickable="false" password="false" selected="false" bounds="[0,406][480,446]" resource-id="com.slk.tic.bokf.rmb.app:id/saveCheckBtnLayout"
instance="9"><android.widget.Button index="0" text="Checking" class="android.widget.Button" package="com.slk.tic.bokf.rmb.app" content-desc=""
checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false"
password="false" selected="false" bounds="[0,406][240,446]" resource-id="com.slk.tic.bokf.rmb.app:id/checkingBtn"
instance="0"/><android.widget.Button index="1" text="Savings" class="android.widget.Button" package="com.slk.tic.bokf.rmb.app" content-desc=""
checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false"
password="false" selected="false" bounds="[240,406][480,446]" resource-id="com.slk.tic.bokf.rmb.app:id/savingsBtn"
instance="1"/></android.widget.LinearLayout><android.widget.LinearLayout index="4" text="" class="android.widget.LinearLayout"
package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false"
focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,455][480,636]"
resource-id="com.slk.tic.bokf.rmb.app:id/saveCheckInforLayout" instance="10"><android.widget.LinearLayout index="0" text=""
class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false"
enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false"
bounds="[0,455][480,492]" resource-id="com.slk.tic.bokf.rmb.app:id/saveCheckTitleLayout" instance="11"><android.widget.TextView index="0"
text="Account No" class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false"
clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false"
bounds="[0,455][240,492]" resource-id="" instance="6"/><android.widget.TextView index="1" text="Balance" class="android.widget.TextView"
package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false"
focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[240,455][480,492]" resource-id=""
instance="7"/></android.widget.LinearLayout><android.widget.ListView index="1" text="" class="android.widget.ListView"
package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="true"
scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,492][480,636]"
resource-id="com.slk.tic.bokf.rmb.app:id/saveCheckListView" instance="0"><android.widget.LinearLayout index="0" text=""
class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true"
enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false"
bounds="[0,492][480,544]" resource-id="" instance="12"><android.widget.TextView index="0" text="***123" class="android.widget.TextView"
package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false"
focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[8,500][232,536]"
resource-id="com.slk.tic.bokf.rmb.app:id/accountColumn" instance="8"/><android.widget.TextView index="1" text="$300.00"
class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true"
focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[248,500][472,536]"
resource-id="com.slk.tic.bokf.rmb.app:id/balanceColumn" instance="9"/></android.widget.LinearLayout><android.widget.LinearLayout index="1" text=""
class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true"
enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false"
bounds="[0,546][480,598]" resource-id="" instance="13"><android.widget.TextView index="0" text="***456" class="android.widget.TextView"
package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false"
focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[8,554][232,590]"
resource-id="com.slk.tic.bokf.rmb.app:id/accountColumn" instance="10"/><android.widget.TextView index="1" text="$400.00"
class="android.widget.TextView" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false" enabled="true"
focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[248,554][472,590]"
resource-id="com.slk.tic.bokf.rmb.app:id/balanceColumn"
instance="11"/></android.widget.LinearLayout></android.widget.ListView></android.widget.LinearLayout><android.widget.LinearLayout index="5" text=""
class="android.widget.LinearLayout" package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="false"
enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false"
bounds="[9,636][471,792]" resource-id="" instance="14"><android.widget.ImageView NAF="true" index="0" text="" class="android.widget.ImageView"
package="com.slk.tic.bokf.rmb.app" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false"
focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[9,636][471,792]"
resource-id="com.slk.tic.bokf.rmb.app:id/rewardsImage"
instance="3"/></android.widget.LinearLayout></android.widget.LinearLayout></android.widget.FrameLayout></android.support.v4.widget.DrawerLayout></andro
id.widget.LinearLayout></android.widget.FrameLayout></android.widget.LinearLayout></android.widget.FrameLayout></android.widget.LinearLayout></android.
widget.FrameLayout></hierarchy>"""
##  parser.parse()
  parser.parse(open('D://Elements.xml'))
  obj=BuildJson()
  obj.xmltojson()
##  for x in XpathList:
##   print x

