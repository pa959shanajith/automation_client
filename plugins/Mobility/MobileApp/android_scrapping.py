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
import ctypes
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


    def print_error(self,e):
        log.error(e)
        logger.print_on_console(e)
        return e


    def start_server(self,platform_name=""):
        try:
            err_msg = None
            curdir = os.environ["AVO_ASSURE_HOME"]
            path_node_modules = curdir + '/plugins/Mobility/MobileApp/node_modules'
            if not os.path.exists(path_node_modules):
                self.print_error('node_modules Directory not Found in /plugins/Mobility/MobileApp')
                return False
            if (SYSTEM_OS != 'Darwin'):
                path = curdir + '/plugins/Mobility/MobileApp/node_modules/appium/build/lib/main.js'
                nodePath = os.environ["AVO_ASSURE_HOME"] + "/Lib/Drivers/node.exe"
                proc = subprocess.Popen([nodePath, path], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
                start = time.time()
                timeout = 120 #tentative; as it depends on the system performance.
                server_flag = False
                while(True):
                    if int(time.time()-start) >= timeout:
                        err_msg = self.print_error('Timeout starting the Appium server')
                        break
                    processes = psutil.net_connections()
                    for line in processes:
                        p = line.laddr
                        if p[1] == 4723:
                            time.sleep(2)
                            server_flag = True
                            break
                    if server_flag: break
                    time.sleep(5)
                if err_msg is None:
                    logger.print_on_console('Server started')
                    return True
            else:
                path = curdir + '/plugins/Mobility/MobileApp/node_modules/appium/build/lib/main.js'
                nodePath = curdir + '/plugins/Mobility/MobileApp/node_modules/node_appium'
                proc = subprocess.Popen([nodePath, path], shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
                time.sleep(25) # psutil.net_connections() doesn't work on Mac, insearch of alternatives
                logger.print_on_console('Server started')
                return True
        except Exception as e:
            self.print_error('Error while starting server')
            log.error(e,exc_info=True)
        return False


    def installApplication(self, apk_path, platform_version, device_name, udid, *args):
        global driver
        from appium import webdriver
        try:
            if SYSTEM_OS == 'Darwin' :
                if driver is not None:
                    return driver
                if self.start_server():
                    self.desired_caps = {}
                    self.desired_caps['platformName'] = 'iOS'
                    self.desired_caps['automationName'] = 'XCUITest'
                    self.desired_caps['platformVersion'] = platform_version
                    self.desired_caps['deviceName'] = device_name
                    self.desired_caps['udid'] = udid
                    self.desired_caps['fullReset'] = False
                    self.desired_caps['xcodeConfigFile'] = os.environ["AVO_ASSURE_HOME"]+ '/assets/appium.xcconfig'
                    self.desired_caps['showXcodeLog'] = True
                    # self.desired_caps['launchTimeout'] = 120000
                    self.desired_caps['noReset'] = True
                    self.desired_caps['newCommandTimeout'] = 0
                    self.desired_caps['sessionOverride'] = True
                    self.desired_caps['log_level'] = False
                    self.desired_caps['app'] = apk_path
                    driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', self.desired_caps)
                else:
                    driver = None
                    return None
            else:
                global device_id, packageName, device_keywords_object
                processes = psutil.net_connections()
                for line in processes:
                    p = line.laddr
                    if p[1] == 4723 and driver is not None:
                        return driver
                try:
                    if self.start_server():
                        if device_name == 'wifi':
                            device_name = device_keywords_object.wifi_connect()
                        result_cdd=self.check_device_details(device_name,platform_version)
                        if device_name != '' and result_cdd==TEST_RESULT_TRUE:
                            activityName = device_keywords_object.activity_name(apk_path)
                            packageName = device_keywords_object.package_name(apk_path)
                            logger.print_on_console("Connected device name:",device_name)
                            logger.print_on_console("App package name:",packageName)
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
                            if packageName is not None:
                                self.desired_caps['appPackage'] = packageName
                                self.desired_caps['appActivity'] = activityName
                                self.desired_caps['skipUnlock'] = True
                                self.desired_caps['automationName'] = 'UiAutomator2'
                                self.desired_caps['ignoreUnimportantViews'] = True
                                self.desired_caps['uiautomator2ServerInstallTimeout'] = 120000
                                self.desired_caps['uiautomator2ServerLaunchTimeout'] = 120000
                                self.desired_caps['adbExecTimeout'] = 120000
                            driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
                            device_id = device_name
                    else:
                        driver = None
                        device_id = None
                        return None
                except Exception as e:
                    self.print_error("Not able to install or launch application")
                    log.error(e,exc_info=True)
                    driver = None
                    device_id = None
        except Exception as e:
            self.print_error("Not able to install or launch application")
            log.error(e,exc_info=True)
            driver = None
            device_id = None
        return driver

    def check_device_details(self,dv_name,platform_ver):
        res_1=TEST_RESULT_TRUE
        res_2=TEST_RESULT_FALSE
        res=TEST_RESULT_FALSE
        try:
            temp_res=device_keywords_object.get_device_list('')
            if dv_name not in temp_res[2]:
                self.print_error("Please provide valid Device ID")
                res_1=TEST_RESULT_FALSE
            if platform_ver!='' and res_1==TEST_RESULT_TRUE:
                adb=os.environ['ANDROID_HOME']+"\\platform-tools\\adb.exe"
                if dv_name is not None:
                    cmd = adb + ' -s '+ dv_name+' shell getprop ro.build.version.release '
                s = subprocess.check_output(cmd.split(),universal_newlines=True).strip()
                if s==platform_ver:
                    res_2=TEST_RESULT_TRUE
                else:
                    self.print_error("Please provide valid Platform version")
            if res_1==TEST_RESULT_TRUE and res_2==TEST_RESULT_TRUE:
                res=TEST_RESULT_TRUE
        except Exception as e:
            self.print_error("Not able to check device details")
            log.error(e,exc_info=True)
        return res

    def scrape(self):
        if driver is not None:
            finalJson=''
            page_source=driver.page_source
            parser = xml.sax.make_parser()
            handler = Exact('/',parser,'')
            parser.setContentHandler(handler)
            
            file_path_xml=os.environ["AVO_ASSURE_HOME"]+'/output/Elements.xml'
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
                self.print_error("Error occured in scraping")
                log.error(e,exc_info=True)
            return finalJson
        else:
            return None
            
    '''
        Definition: Saves the mobile screenshot, corrects the dimensions if wrong, resizes according to requirement
                    returns the dimensions
        Output: Screenshot/Device dimensions
        Output Type: Tuple
        Reference: iris_mobile.py, mobile_app_scrape.py
    '''
    def get_screenshot(self, resizeImg=False):
        coords = None
        img_ratio = None
        new_height = None
        new_width = None
        resized_screenshot_img = None
        user32 = ctypes.windll.user32
        if driver is not None:
            screen_shot = driver.get_screenshot_as_file("test_screenshot.png")
            # mobile screenshot is saved as test_screenshot locally
            if screen_shot:
                from PIL import Image
                screenshot_img = Image.open("test_screenshot.png")
                # original_width = driver.get_window_size()['width']
                # original_height = driver.get_window_size()['height']
                result = subprocess.run("adb shell wm size", stdout=subprocess.PIPE)   # device dimensions are retrieved through adb command because driver.get_window_size is giving wrong dimensions for some device ex. HTC
                device_dimensions = result.stdout.decode("utf-8").split(" ")[-1].split("x")
                original_width = int(device_dimensions[0])
                original_height = int(device_dimensions[1])
                if screenshot_img.size[0] != original_width or screenshot_img.size[1] != original_height:
                    '''
                        screenshot saved can have wrong dimension from actual device dimension (happening in HTC) so 
                        resizing it to correct device dimensions
                    '''
                    screenshot_img = screenshot_img.resize((int(original_width), int(original_height)), Image.ANTIALIAS)
                    screenshot_img.save("test_screenshot.png")
                if resizeImg:
                    '''
                        flag to check if resize for display monitor is required or not
                    '''
                    img_ratio = original_width/original_height 
                    new_width = img_ratio * int(87.890625*user32.GetSystemMetrics(79)/100)
                    new_height = new_width / img_ratio
                    resized_screenshot_img = screenshot_img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
                    resized_screenshot_img.save("resized_test_screenshot.png")
                # os.remove("test_screenshot.png")
                coords =  (original_width, original_height)
                
                del(screen_shot)
                del(screenshot_img)
                del(result)
                del(device_dimensions)
                del(img_ratio)
                del(new_width)
                del(new_height)
                del(resized_screenshot_img)
                
        return coords


    '''
        --- def get_driver() ---
        Definition: Returns the driver object
        Reference: iris_mobile.py
    '''
    def get_driver(self):
        return driver

class BuildJson:

    def xmltojson(self,driver):
        import re
        global ScrapeList,XpathList,label,content_desc,class_name,resource_id,enabled,rectangle,x_coordinate,y_coordinate,width,height#,visible
        ScrapeList=[]
        custnamelist=[]
        global counter
        object_type = {
            #Android
            'android.widget.TimePicker' : '_timepicker', 'android.widget.DatePicker' : '_datepicker', 'android.widget.RadioButton' : '_radiobtn', 'android.widget.Button' : '_btn',
            'android.widget.EditText' : '_txtbox', 'android.widget.Switch' : '_switch', 'android.widget.CheckBox' : '_chkbox', 'android.widget.CheckedTextView' : '_chkdtxtview', 'android.widget.Spinner' : '_spinner',
            'android.widget.NumberPicker' : '_numberpicker', 'android.widget.SeekBar' : '_seekbar', 'android.widget.ListView' : '_listview', 'android.widget.ImageButton' : '_imagebtn',
            'android.widget.LinearLayout' : '_linearlayout', 'android.widget.TextView' : '_txtview', 'android.widget.FrameLayout' : '_framelayout', 'android.widget.ImageView' : '_img',
            'android.widget.RelativeLayout' : '_relativelayout', 'android.view.View' : '_view',
            #iOS
            'XCUIElementTypeTextField' : '_textfield', 'XCUIElementTypeSearchField' : '_searchfield', 'XCUIElementTypeSecureTextField' : '_securetextfield', 'XCUIElementTypeRadioButton' : '_radio',
            'XCUIElementTypeButton' : '_button', 'XCUIElementTypeSwitch' : '_switch', 'XCUIElementTypeToggle' : '_toggle', 'XCUIElementTypeCheckBox' : '_checkbox',
            'XCUIElementTypePickerWheel' : '_picker', 'XCUIElementTypeSlider': '_slider', 'XCUIElementTypeLink' : '_link', 'XCUIElementTypeTextView' : '_txtview', 'XCUIElementTypeStaticText' : '_statictxt',
            'XCUIElementTypeImage' : '_image', 'XCUIElementTypeIcon' : '_icon', 'XCUIElementTypeTable' : '_table', 'XCUIElementTypeCell' : '_cell', 'XCUIElementTypeKey'  : '_key'
        }
        try:
            ##Changes done for appium upgrade from 1.7.2 to 1.16.0
            if XpathList[0] == '//hierarchy[1]':
                del XpathList[0],rectangle[0],label[0],content_desc[0],class_name[0],resource_id[0],enabled[0]
            elif (len(class_name) == len(XpathList) + 1) and class_name[0] == "":
                del label[0],class_name[0],enabled[0],x_coordinate[0],y_coordinate[0],width[0],height[0]
            for i in range(len(XpathList)):
                text=''
                if label[i] != '':
                    text=label[i]
                elif SYSTEM_OS!='Darwin' and content_desc[i]  != '':
                    text=content_desc[i]
                if text=='' or text==None:
                    text='NONAME'

                if class_name[i] in object_type:
                    text1 = text + object_type[class_name[i]]
                    if text1 not in custnamelist:
                        text = text1
                        custnamelist.append(text)
                    else:
                        text=text+str(counter) + object_type[class_name[i]]
                        custnamelist.append(text)
                        counter=counter+1
                else:
                    text1 = text + '_elmnt'
                    if text1 not in custnamelist:
                        text = text1
                        custnamelist.append(text)
                    else:
                        text=text+str(counter) + '_elmnt'
                        custnamelist.append(text)
                        counter=counter+1

                if SYSTEM_OS!='Darwin':
                    xpath = resource_id[i] + ';' + XpathList[i] + ';' + class_name[i]
                    ele_bounds=re.findall('\d+',rectangle[i])
                    width_=(int(ele_bounds[2])-int(ele_bounds[0])) if len(ele_bounds)==4 else ""
                    height_=int(ele_bounds[3])-int(ele_bounds[1]) if len(ele_bounds)==4 else ""
                    left = ele_bounds[0] if len(ele_bounds)==4 else ""
                    top = ele_bounds[1] if len(ele_bounds)==4 else ""
                    ScrapeList.append({'xpath': xpath, 'tag': class_name[i],
                        'text': text,
                        'id': resource_id[i], 'custname': text,
                        'reference': str(uuid.uuid4()),'enabled':enabled[i],'left':left,'top':top,'width':width_,'height':height_})
                elif SYSTEM_OS=='Darwin':
                    xpath = XpathList[i] + ';' + class_name[i]
                    ScrapeList.append({'xpath': xpath, 'tag': class_name[i],
                       'text': text,
                       'custname': text,
                       'reference': str(uuid.uuid4()),
                       # 'visible': visible[i],
                       'enabled': enabled[i], 'left': x_coordinate[i], 'top': y_coordinate[i],
                       'width': width[i], 'height': height[i]})
        except Exception as e:
            log.error(e,exc_info=True)
        XpathList=[]
        label=[]
        content_desc=[]
        class_name=[]
        resource_id=[]
        enabled=[]
        rectangle=[]
        x_coordinate=[]
        y_coordinate=[]
        width=[]
        height=[] #visible
        return self.save_json(ScrapeList, driver)


    def save_json(self,scrape_data,driver):
        try:
            jsonArray=OrderedDict()
            jsonArray['view']= scrape_data
            jsonArray['mirror']=driver.get_screenshot_as_base64()
            dimension = driver.get_window_size()
            jsonArray['mirrorwidth'] = dimension['width']
            jsonArray['mirrorheight'] = dimension['height']
            file_path_json=os.environ["AVO_ASSURE_HOME"] + '/output/domelements_Android.json'
            with open(file_path_json, 'w') as outfile:
                logger.print_on_console('Writing scrape data to domelements.json file')
                json.dump(jsonArray, outfile, indent=4, sort_keys=False)
                outfile.close()
        except Exception as e:
            log.error(e)
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
        try:
            count = self.elementNameCount.get(qName)
            if count==None:
                count=1
            else:
                count=count+1
            self.elementNameCount[qName]=count
            childXPath = self.xPath + "/" + qName + "[" + str(count) + "]"
            attsLength = len(attrs)
            if(attsLength>1):# and childXPath != '//hierarchy[1]':
                XpathList.append(childXPath)
            elements_list = attrs.getQNames()
            label_flag = False
            if SYSTEM_OS=='Darwin':
                label.append(attrs.getValue('label') if 'label' in elements_list else "")
                name.append(qName if 'label' in elements_list else "")
                enabled.append(attrs.getValue('enabled') if 'enabled' in elements_list else "")
                #visible.append(attrs.getValue('visible') if 'visible' in elements_list else "")
                x_coordinate.append(attrs.getValue('x') if 'x' in elements_list else "")
                y_coordinate.append(attrs.getValue('y') if 'y' in elements_list else "")
                width.append(attrs.getValue('width') if 'width' in elements_list else "")
                height.append(attrs.getValue('height') if 'height' in elements_list else "")
                class_name.append(attrs.getValue('type') if 'type' in elements_list else "")

            if SYSTEM_OS!='Darwin':
                label.append(attrs.getValue('text') if 'text' in elements_list else "")
                name.append(qName if 'text' in elements_list else "")
                rectangle.append(attrs.getValue('bounds') if 'bounds' in elements_list else "")
                enabled.append(attrs.getValue('enabled') if 'enabled' in elements_list else "")
                resource_id.append(attrs.getValue('resource_id') if 'resource_id' in elements_list else "")
                focusable.append(attrs.getValue('focusable') if 'focusable' in elements_list else "")
                class_name.append(attrs.getValue('class') if 'class' in elements_list else "")
                content_desc.append(attrs.getValue('content-desc') if 'content-desc' in elements_list else "")
                checked.append(attrs.getValue('checked') if 'checked' in elements_list else "")

            curobj=self
            child = Exact(childXPath,self.parser,curobj)
            self.parser.setContentHandler(child)
        except Exception as e:
            log.error(e,exc_info = True)

    def endElement(self, name):
        value = self.buffer.strip()
        if(value != ''):
            log.info(self.xPath + "='" + self.buffer.toString() + "'")
        self.parser.setContentHandler(self.parent)


    def characters(self, data):
        self.buffer += data
