#-------------------------------------------------------------------------------
# Name:        android_scrapping.py
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
import uuid, json, os, psutil, subprocess, time, re
from collections import OrderedDict
from constants import *
from mobile_app_constants import *
import logger, subprocess, socket, base64, platform, logging
import device_keywords
log = logging.getLogger('android_scrapping.py')

XpathList=[]
resource_id=[]
class_name=[]
enabled=[]
x_coordinate=[]
y_coordinate=[]
width=[]
height=[]
# visible=[]
rectangle=[]
focusable=[]
content_desc=[]
checked=[]
label=[]
name=[]
ScrapeList=[]
counter=0
driver=None
packageName=None
device_id = None
device_keywords_object = device_keywords.Device_Keywords()

class InstallAndLaunch():
    def __init__(self):
        self.desired_caps={}
    def start_server(self,platform_name=""):
        try:
            ##            maindir = os.getcwd()
            ##            os.chdir('..')
            curdir = os.environ["NINETEEN68_HOME"]
            if (SYSTEM_OS != 'Darwin'):
                path = curdir + '\\Nineteen68\\plugins\\Mobility\\MobileApp\\node_modules\\appium\\build\\lib\\main.js'
                nodePath = os.environ["NINETEEN68_HOME"] + "\\Drivers" + '\\node.exe'
                proc = subprocess.Popen([nodePath, path], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
                time.sleep(5)
                logger.print_on_console('Server started')
            elif platform_name != "ios":
                path = curdir + '/Nineteen68/plugins/Mobility/node_modules/appium/build/lib/main.js'
                proc = subprocess.Popen(path, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
                time.sleep(15)
                logger.print_on_console('Server started')
        except Exception as e:
            err = 'Error while starting server'
            logger.print_on_console(err)
            log.error(err)
            log.error(e)

    def installApplication(self, apk_path, platform_version, device_name, udid, *args):
        global driver, device_id, packageName, device_keywords_object
        #import appium
        from appium import webdriver
        try:
            if SYSTEM_OS == 'Darwin' :
                self.start_server("ios")
                self.desired_caps = {}
                self.desired_caps['platformName'] = 'iOS'
                self.desired_caps['platformVersion'] = platform_version  #ios version
                self.desired_caps['bundle_id'] = device_name             # bundleid
                self.desired_caps['deviceName'] = apk_path               #device name
                self.desired_caps['Ip_Address'] = udid
                self.desired_caps['fullReset'] = False
                self.desired_caps['newCommandTimeout'] = 3600
                self.desired_caps['launchTimeout'] = 180000
                self.driver = "pass"
                current_dir = (os.getcwd())
                dir_path = os.path.dirname(os.path.realpath(__file__))
                # set IP
                if (subprocess.getoutput('pgrep xcodebuild') == ''):
                    try:
                        with open(dir_path + "/Nineteen68UITests/data.txt",'wb') as f:
                            f.write(self.desired_caps['Ip_Address'])  # send IP
                    except Exception as e:
                        log.error(e)
                    # set run command
                    self.desired_caps["deviceName"] = self.desired_caps["deviceName"].split(" ")
                    self.desired_caps["deviceName"] = "\ ".join(self.desired_caps["deviceName"])
                    if (self.desired_caps["deviceName"].split("=")[0] == "id"):
                        name = self.desired_caps["deviceName"]
                    else:
                        name = "name=" + self.desired_caps["deviceName"]
                    try:
                        with open(dir_path + "/run.command", "wb") as f:
                            f.write("#! /bin/bash \n")
                            f.write(
                                "cd " + dir_path + "\n")
                            f.write(
                                "xcodebuild -workspace Nineteen68.xcworkspace -scheme Nineteen68 -destination " +
                                name + " OS=" + self.desired_caps["platformVersion"] +" >/dev/null "+ " test")
                    except Exception as e:
                        log.error(e)
                    # subprocess.call("chmod a+x run.command")
                    try:
                        subprocess.Popen(dir_path + "/run.command", shell=True)
                    except:
                        log.error(ERROR_CODE_DICT["ERR_XCODE_DOWN"])
                    timer = 0
                    while True:
                        try:
                            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            clientsocket.connect((self.desired_caps['Ip_Address'], 8022))
                            clientsocket.send(XCODE_EXECUTE)
                            keyword = "launchapplication"
                            length_keyword = len(keyword.encode('utf-8'))
                            clientsocket.send(str(len(str(length_keyword))))
                            clientsocket.send(str(length_keyword))
                            clientsocket.send(keyword)
                            clientsocket.send("0")
                            clientsocket.send("0")
                            input_text = self.desired_caps['bundle_id']
                            length_input_text = len(input_text.encode('utf-8'))
                            clientsocket.send(str(len(str(length_input_text))))
                            clientsocket.send(str(length_input_text))
                            clientsocket.send(input_text)
                            data = clientsocket.recv(100000)
                            string_data = data.decode('utf-8')
                            if string_data == "":
                                continue
                            break
                        except:
                            timer+=1
                            if timer == 130:
                                log.error(ERROR_CODE_DICT["ERR_TIMEOUT"])
                                break
                            time.sleep(1)
                    return self.driver
                return self.driver
            else:
                activityName = device_keywords_object.activity_name(apk_path)
                packageName = device_keywords_object.package_name(apk_path)
                processes = psutil.net_connections()
                for line in processes:
                    p = line.laddr
                    if p[1] == 4723 and driver is not None:
                        msg = device_keywords_object.launch_app(apk_path,packageName,activityName,device_id)
                        if 'error' not in msg.lower():
                            return driver
                try:
                    if device_name == 'wifi':
                        device_name = device_keywords_object.wifi_connect()
                    if device_name != '':
                        
                        logger.print_on_console("Connected device name:",device_name)
                        logger.print_on_console("App package name:",packageName)
                        self.start_server()
                        self.desired_caps = {}
                        if platform_version is not None:
                            self.desired_caps['platformVersion'] = platform_version
                        self.desired_caps['platformName'] = 'Android'
                        self.desired_caps['deviceName'] = device_name
                        self.desired_caps['udid'] = device_name
                        self.desired_caps['noReset'] = True
                        self.desired_caps['newCommandTimeout'] = 0
                        self.desired_caps['app'] = apk_path
                        self.desired_caps['sessionOverride'] = True
                        self.desired_caps['fullReset'] = False
                        self.desired_caps['log_level'] = False
                        self.desired_caps['appPackage'] = packageName
                        self.desired_caps['appActivity'] = activityName
                        driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
                        device_id = device_name
                except Exception as e:
                    err = "Not able to install or launch application"
                    logger.print_on_console(err)
                    log.error(e,exc_info=True)
                    driver = None
                    device_id = None
        except Exception as e:
            err = "Not able to install or launch application"
            logger.print_on_console(err)
            log.error(e,exc_info=True)
            driver = None
            device_id = None
        return driver

    def scrape(self):
        finalJson=''
        if SYSTEM_OS == 'Darwin':
            EOF = "final"
            fragments = ""
            bundle_id = self.desired_caps['bundle_id']
            length = len(bundle_id.encode('utf-8'))
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.connect((self.desired_caps['Ip_Address'], 8022))
            clientsocket.send(XCODE_SCRAPE)
            clientsocket.send(str(length))
            clientsocket.send(bundle_id)
            while True:
                chunck = clientsocket.recv(10000)
                if chunck.endswith(EOF):
                    idx = chunck.index(EOF)
                    fragments += chunck[:idx]
                    break
                fragments += chunck
            data = fragments.split("!@#$%^&*()")[0]
            image_data = fragments.split("!@#$%^&*()")[1]
            height_data = fragments.split("!@#$%^&*()")[2]
            width_data = fragments.split("!@#$%^&*()")[3]
            data = json.loads(data)
            jsonArray = OrderedDict()
            jsonArray['view'] = data
            jsonArray['mirror'] = image_data
            jsonArray['mirrorwidth'] = width_data
            jsonArray['mirrorheight'] = height_data
            with open("savefile.json", 'w') as outfile:
                logger.print_on_console('Writing scrape data to domelements.json file')
                json.dump(jsonArray, outfile, indent=4, sort_keys=False)
            return jsonArray
        elif driver is not None:
            page_source=driver.page_source
            parser = xml.sax.make_parser()
            handler = Exact('/',parser,'')
            parser.setContentHandler(handler)
            
            file_path_xml=os.environ["NINETEEN68_HOME"]+'/Scripts'+'/Elements.xml'
            page_source=page_source.encode('utf-8').strip()
            try:
                with open(file_path_xml,'wb') as new_file:
                    new_file.write(page_source)
                    new_file.close()
                parser.parse(file_path_xml)
                obj2=BuildJson()
                finalJson=obj2.xmltojson(driver)
                with open(file_path_xml,'w') as new_file:
                    new_file.write('')
                    new_file.close()
            except Exception as e:
                err = "Error occured in scraping"
                logger.print_on_console(err)
                log.error(err)
                log.error(e,exc_info=True)
            return finalJson
        else:
            return None



class BuildJson:

    def xmltojson(self,driver):
        import re
        global ScrapeList
        global XpathList
        global label
        global content_desc
        global class_name
        global resource_id
        global enabled
        global rectangle
        # global visible
        global x_coordinate
        global y_coordinate
        global width
        global height
        ScrapeList=[]
        custnamelist=[]
        global counter
        object_type = {
            'android.widget.TimePicker' : 'timepicker',
            'android.widget.DatePicker' : 'datepicker',
            'android.widget.RadioButton' : 'radiobutton',
            'android.widget.Button' : 'button',
            'android.widget.EditText' : 'edittext',
            'android.widget.Switch' : 'switch',
            'android.widget.CheckBox' : 'checkbox',
            'android.widget.Spinner' : 'spinner',
            'android.widget.NumberPicker' : 'numberpicker',
            'android.widget.SeekBar' : 'seekbar',
            'android.widget.ListView' : 'listview',
            'android.widget.ImageButton' : 'imagebutton',
            'android.widget.LinearLayout' : 'linearlayout',
            'android.widget.TextView' : 'textview',
            'android.widget.FrameLayout' : 'framelayout',
            'android.widget.ImageView' : 'imageview',
            'android.widget.RelativeLayout' : 'relativelayout',
            'android.widget.ScrollView' : 'scrollview',
            'android.view.View' : 'view',
            'android.view.ViewGroup' : 'viewgroup'
        }
        for i in range(len(XpathList)):
            text=''
            # print SYSTEM_OS
            if label[i] != '':
                if class_name[i] in object_type:
                    text=label[i]+'_'+object_type[class_name[i]]
                else:
                    text=label[i]+'_'+class_name[i]
            elif content_desc[i]  != '':
                if class_name[i] in object_type:
                    text=content_desc[i]+'_'+object_type[class_name[i]]
                else:
                    text=content_desc[i]+'_'+class_name[i]
            if text=='' or text==None:
                if class_name[i] in object_type:
                    text='NONAME_'+object_type[class_name[i]]
                else:
                    text='NONAME_'+class_name[i]
            if text not in custnamelist:
                custnamelist.append(text)
            else:
                text=text+str(counter)
                custnamelist.append(text)
                counter=counter+1
            if SYSTEM_OS!='Darwin':
                xpath = resource_id[i] + ';' + XpathList[i]
                ele_bounds=re.findall('\d+',rectangle[i])
    ##            bounds={'x':ele_bounds[0],
    ##            'y':ele_bounds[1],
    ##            'height':ele_bounds[3],
    ##            'width':ele_bounds[2]}
                width=int(ele_bounds[2])-int(ele_bounds[0])
                height=int(ele_bounds[3])-int(ele_bounds[1])
                ScrapeList.append({'xpath': xpath, 'tag': class_name[i],
                    'text': text,
                    'id': resource_id[i], 'custname': text,
                    'reference': str(uuid.uuid4()),'enabled':enabled[i],'left':ele_bounds[0],'top':ele_bounds[1],'width':width,'height':height})
            # elif SYSTEM_OS=='Darwin':
            #     xpath =  XpathList[i]
            #     ScrapeList.append({'xpath': xpath, 'tag': class_name[i],
            #        'text': text,
            #        'custname': text,
            #        'reference': str(uuid.uuid4()),
            #        # 'visible': visible[i],
            #        'enabled': enabled[i], 'left': x_coordinate[i], 'top': y_coordinate[i],
            #        'width': width[i], 'height': height[i]})

        XpathList = []
        label = []
        content_desc = []
        class_name = []
        resource_id = []
        enabled = []
        # visible = []
        rectangle=[]
        x_coordinate = []
        y_coordinate = []
        width = []
        height = []
        # print 'the json is', self.save_json(ScrapeList)
        return self.save_json(ScrapeList, driver)


    def save_json(self,scrape_data,driver):
        jsonArray=OrderedDict()
        jsonArray['view']= scrape_data
##        jsonArray['mirror']='IMAGEEEEE'
        jsonArray['mirror']=driver.get_screenshot_as_base64()
        dimension = driver.get_window_size()
        jsonArray['mirrorwidth'] = dimension['width']
        jsonArray['mirrorheight'] = dimension['height']
        file_path_json=os.environ["NINETEEN68_HOME"]+'/Scripts'+'/domelements_Android.json'
        with open(file_path_json, 'w') as outfile:
            logger.print_on_console('Writing scrape data to domelements.json file')
            json.dump(jsonArray, outfile, indent=4, sort_keys=False)
            outfile.close()
        return jsonArray




class Exact(xml.sax.handler.ContentHandler):

    def __init__(self,xpath,xmlreader,parent):
        self.curpath = []
        self.xPath=xpath
        self.parser=xmlreader
        self.elementNameCount={}
        self.buffer=''
        self.parent=parent


    def startElement(self, qName, attrs):
        count = self.elementNameCount.get(qName)
        if count==None:
            count=1
        else:
            count=count+1
        self.elementNameCount[qName]=count
        childXPath = self.xPath + "/" + qName + "[" + str(count) + "]"
        attsLength = len(attrs)
        if(attsLength>1):
            XpathList.append(childXPath)
        elements_list = attrs.getQNames()
        # label_flag = False
        for x in attrs.getQNames():
            # if SYSTEM_OS=='Darwin':
            #     value = attrs.getValue(x)
            #     # if x.lower()=='text':
            #     if x.lower() == 'label':
            #         ##            if(value == ''):
            #         ##		      label.append(qName)
            #         ##            else:
            #         label_flag = True
            #         label.append(value)
            #         name.append(qName)
            #         # elif x.lower()=='bounds':
            #     # 	rectangle.append(value)

            #     elif x.lower() == 'enabled':
            #         enabled.append(value)

            #     # elif x.lower() == 'visible':
            #     #     visible.append(value)

            #     elif x.lower() == 'x':
            #         x_coordinate.append(value)

            #     elif x.lower() == 'y':
            #         y_coordinate.append(value)

            #     elif x.lower() == 'width':
            #         width.append(value)

            #     elif x.lower() == 'height':
            #         height.append(value)

            #         # elif x.lower()=='resource-id':
            #     # 	resource_id.append(value)

            #     # elif x.lower()=='focusable':
            #     # 	focusable.append(value)

            #     elif x.lower() == 'type':
            #         class_name.append(value)

            #         # elif x.lower()=='content-desc':
            #         # 	content_desc.append(value)

            #         # elif x.lower()=='checked':
            #         # 	checked.append(value)
            if SYSTEM_OS!='Darwin':
                value=attrs.getValue(x)

                if x.lower()=='text':
        ##            if(value == ''):
        ##		      label.append(qName)
        ##            else:
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
        # if SYSTEM_OS == 'Darwin':
        #     if label_flag == False and len(elements_list) > 0:
        #         label.append(qName)
        curobj=self
        child = Exact(childXPath,self.parser,curobj)
        self.parser.setContentHandler(child)

    def endElement(self, name):
        value = self.buffer.strip()
        if(value != ''):
            log.info(self.xPath + "='" + self.buffer.toString() + "'")

        self.parser.setContentHandler(self.parent)

    def characters(self, data):
        self.buffer += data

